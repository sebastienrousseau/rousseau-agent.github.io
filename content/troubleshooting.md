---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau)"
banner_alt: "rousseau-agent banner"
banner_height: "398"
banner_width: "1440"
banner: ""
cdn: "https://cloudcdn.pro"
charset: "utf-8"
cname: "docs.rousseau-agent.dev"
copyright: "Copyright © 2026 Sebastien Rousseau. Released under the MIT License."
date: "July 12, 2026"
download: ""
format-detection: "telephone=no"
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "en-GB"
locale: "en_GB"
logo_alt: "rousseau-agent logo"
logo_height: "33"
logo_width: "100"
logo: ""
name: "rousseau-agent"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "rousseau"
theme-color: "26, 58, 138"
url: "https://docs.rousseau-agent.dev"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
changefreq: "monthly"
description: "Troubleshoot rousseau-agent: WhatsApp QR won't scan, reconnect loops, cosign verify failures, SELinux bind-mount errors, cron not firing, approval policy denying everything."
keywords: "troubleshooting, WhatsApp QR, reconnect loop, cosign verify, SELinux, bind mount, cron, approval policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/troubleshooting/"
subtitle: "Common failure modes and how to fix them."
tags: "troubleshooting, support"
title: "Troubleshooting"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "troubleshooting, WhatsApp QR, reconnect loop, cosign verify, SELinux, bind mount, cron, approval policy"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Troubleshooting"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "support"
order: 27
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/troubleshooting/index.html"
item_link: "https://docs.rousseau-agent.dev/troubleshooting/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Troubleshooting"
last_build_date: "Sun, 12 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
ttl: "60"
type: "website"
webmaster: sebastian.rousseau@gmail.com (Sebastien Rousseau)

# Apple - The Apple front matter (YAML).
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "rousseau-agent"
apple-touch-fullscreen: "yes"

# MS Application - The MS Application front matter (YAML).
msapplication-navbutton-color: "rgb(26,58,138)"

# Twitter Card - The Twitter Card front matter (YAML).
twitter_card: "summary"
twitter_creator: "rousseauagent"
twitter_description: "Troubleshoot rousseau-agent: WhatsApp QR won't scan, reconnect loops, cosign verify failures, SELinux bind-mount errors, cron not firing, approval policy denying everything."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Troubleshooting"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## WhatsApp: QR won't scan

Symptom: `rousseau whatsapp` prints a QR that the phone app rejects, or the pairing dialog reads "This device is not paired with WhatsApp."

Fixes:

1. **Rebuild the container.** If you are running an older image, `whatsmeow` may have shipped a protocol update. Rebuild:
   ```sh
   podman build -t rousseau-agent:local -f docker/Dockerfile .
   systemctl --user restart rousseau-agent.service
   ```
2. **Delete `whatsapp.db`.** A partially-completed pairing leaves the DB in a state whatsmeow cannot reuse. Delete it and re-pair:
   ```sh
   rm ~/.local/share/rousseau/whatsapp.db
   ```
3. **Check clock skew.** WhatsApp's handshake is time-sensitive. If the container's clock is off by more than 30 seconds, pairing fails silently.
   ```sh
   timedatectl status
   ```

## WhatsApp reconnect loop

Symptom: logs show repeated `whatsapp.connected` followed by `whatsapp.disconnected` every few seconds.

Fixes:

1. **Clock skew.** Same fix as above.
2. **Allowlist misconfigured.** Every inbound message is dropped as unauthorised; some servers close the socket after too many silent drops. Add the correct JIDs with `--allow`.
3. **Meta-side ban.** If the WhatsApp mobile app shows "This device has been logged out," Meta has invalidated the pairing. Re-pair from a fresh QR. If it happens repeatedly on the same number, stop using that number.

## cosign verify-blob fails

Symptom:

```
Error: no matching signatures
```

Fixes:

1. **Wrong certificate-identity regex.** The regex must match the GitHub repository that signed the release. For rousseau-agent releases the correct value is:
   ```
   --certificate-identity-regexp 'sebastienrousseau/rousseau-agent'
   ```
   Do not use `.*` — that would accept a cosign signature from any repository.
2. **Wrong OIDC issuer.** GitHub Actions cosign signatures issue from `https://token.actions.githubusercontent.com`. Other CI providers (GitLab, Buildkite) issue from different URLs.
3. **Wrong signature file.** Check that `<version>_checksums.txt.sig` corresponds to the `_checksums.txt` you are verifying (not a stale copy from a different release).
4. **Sigstore trust root changed.** Refresh with `cosign initialize`; the trust root is updated on a slow rotation.

## Container fails to bind mount

Symptom: `podman play kube` or `systemctl --user start rousseau-agent.service` fails with `permission denied` on a bind mount.

Fixes:

1. **SELinux label.** Every volume line must end with `:Z` (or `:z` for shared) so Podman applies the correct SELinux label:
   ```
   Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
   ```
   `:Z` (uppercase) is the private label — appropriate for single-container mounts. `:z` (lowercase) shares the label across containers.
2. **`keep-id` mapping.** Without `UserNS=keep-id`, container UID 1000 is remapped into the host's subuid range and cannot write to host-owned files. Ensure the Quadlet has:
   ```
   UserNS=keep-id
   ```
3. **Missing directory.** Podman does not auto-create bind-mount sources. Create the directory first:
   ```sh
   mkdir -p ~/.local/share/rousseau
   ```

## Cron job not firing

Symptom: `rousseau cron list` shows the job, but nothing happens at the scheduled time.

Fixes:

1. **Check status.** `rousseau status` reports scheduler activity. If the scheduler is not running, the daemon that hosts it is not running.
2. **Timezone.** Schedules use the server's local timezone. Confirm with `timedatectl`. Set `TZ=UTC` in the Quadlet if you want deterministic scheduling regardless of host locale.
3. **PollInterval delay.** New jobs go live within `PollInterval` (default 60s). Wait one minute.
4. **Delivery failure.** The job fired but delivery failed. Check logs for `cron.delivery_failed`; the target format is transport-specific (see [/cron/](/cron/)).

## Approval policy rejecting everything

Symptom: every tool call is denied with "denied by pattern policy" and the model refuses to make progress.

Fixes:

1. **Missing allow rule.** In `pattern` mode with `default: deny`, every tool call needs a matching allow rule. Add one for the tools you want to permit:
   ```yaml
   agent:
     approver:
       mode: pattern
       default: deny
       allow:
         - {tool: read, match: ".*"}
         - {tool: grep, match: ".*"}
         - {tool: edit, match: "^./workspace/.*"}
   ```
2. **Deny beats allow.** A `deny` rule always wins over an `allow` rule for the same tool. Review your deny list for accidental over-matches.
3. **Raise the default.** For attended sessions, `default: allow` with tightened deny rules is often more workable:
   ```yaml
   agent:
     approver:
       mode: pattern
       default: allow
       deny:
         - {tool: bash, match: "rm -rf|sudo"}
   ```

## Provider returns 401

Symptom: agent errors with `provider: unauthorized`.

Fixes:

1. **Wrong API key.** For the Anthropic direct provider, verify `ANTHROPIC_API_KEY` is exported or set in `~/.config/rousseau/config.yaml`.
2. **Wrong credential chain.** For Bedrock, run `aws sts get-caller-identity` from the container to confirm which principal the SDK resolves.
3. **Vertex service account.** For the Vertex provider, confirm the file at `vertex.credentials_file` is readable inside the container and grants `roles/aiplatform.user`.

## Provider returns 429

Symptom: agent errors with `provider: rate limited`.

Fixes:

1. **Lower `max_tokens`.** Shorter completions clear the rate window faster.
2. **Enable compression.** Long transcripts increase input-token pressure; `agent.compression.enabled: true` collapses old messages.
3. **Wait it out.** rousseau does not retry inside `Complete`; the caller (chat transport, cron scheduler, or `rousseau chat`) decides whether and how to retry.

## `rousseau chat` shows only a blank TUI

Symptom: the Bubble Tea TUI opens but no cursor, no viewport.

Fixes:

1. **TERM environment.** rousseau requires an ANSI-capable terminal. Set `TERM=xterm-256color` (or similar).
2. **Wrapped stdin.** Running under `nohup` or a pipe strips the terminal. Run interactively.

## Slack: `invalid_auth` on start

Symptom: `slack.starting` immediately followed by `invalid_auth`.

Fixes:

1. **Wrong token mixed up.** Rousseau needs both `xapp-…` (app-level, `--app-token`) and `xoxb-…` (bot, `--bot-token`). Passing an app token where a bot token is expected produces this error.
2. **App not installed.** After creating scopes, click *Install to Workspace* in the Slack app config. Tokens are only valid post-install.
3. **Token rotated.** Slack tokens can be manually rotated by an admin. If you rotated one, all daemons using it must be restarted with the new value.

## Slack: bot replies to its own messages (loop)

Symptom: rousseau's outbound message triggers an inbound event that the daemon responds to, causing runaway replies.

Fixes:

1. **Set `bot_user_id`.** The `--bot-user-id` flag (or `slack.bot_user_id` in config) tells the daemon to ignore messages sent by that user ID. Retrieve it with `curl -H "Authorization: Bearer xoxb-..." https://slack.com/api/auth.test`.
2. **Verify the event filter.** The transport ignores `bot_message` subtypes by default, but a poorly-configured Slack app can bypass this.

## Discord: message text arrives empty

Symptom: `discord.incoming from=... body=` — messages come through but with no content.

Fixes:

1. **Message Content Intent disabled.** In the Discord Developer Portal under <em>Bot &gt; Privileged Gateway Intents</em>, toggle **Message Content Intent**. Without it, Discord strips message text from Gateway events.
2. **Missing scopes.** The invite URL must have granted the bot `Read Message History` and `Send Messages` for the channel/DM you are using.

## Discord: `disallowed intents`

Symptom: startup errors with `Discord returned 4014 disallowed intents`.

Fixes:

1. **Privileged intents.** Enable *Message Content Intent* (see above). Even if you never ask for it, Discord returns 4014 if you request it without approval.
2. **Verification.** Bots in 100+ servers must be verified by Discord to use privileged intents. Follow the developer portal walkthrough.

## Telegram: `unauthorized`

Symptom: `telegram.starting` followed by `getUpdates: 401`.

Fixes:

1. **Wrong token.** BotFather returns the token once — do not include the trailing period. The token has the shape `<bot_id>:<secret>`.
2. **Token revoked.** `/revoke` in BotFather invalidates the current token; get a fresh one.

## Email: `dial tcp: i/o timeout`

Symptom: the IMAP or SMTP connect never completes.

Fixes:

1. **Wrong port.** IMAP is `993` (implicit TLS). SMTP submission is `587` (STARTTLS) or `465` (implicit TLS). Rousseau uses implicit TLS on both — STARTTLS-only servers are not yet supported. See [Transports: Email](/transports/email/) for migration.
2. **Egress blocked.** Corporate firewalls often block outbound SMTP. Test with `openssl s_client -connect smtp.example.com:465` from the container.
3. **Provider requires app password.** Gmail, Fastmail, and similar require an app password (not your account password) when 2FA is on. Generate one from the provider's security settings.

## Vertex: `permission denied on resource`

Symptom: `vertex: HTTP 403 permission denied on resource projects/.../models/claude-sonnet-4-6@…:rawPredict`.

Fixes:

1. **Missing role.** Grant `roles/aiplatform.user` to the service account or user calling the API. IAM changes take up to a minute to propagate.
2. **Wrong project.** The `project` in config must match the project that owns the quota. If billing is on a different project, use quota-project via `gcloud auth application-default set-quota-project`.
3. **Region mismatch.** The model must be available in the requested region — Vertex Model Garden lists this.

## Bedrock: `You don't have access to the model`

Symptom: `AccessDeniedException: You don't have access to the model with the specified model ID`.

Fixes:

1. **Model access not requested.** Bedrock requires explicit model-access request via the console (*Foundation models &gt; Model access*). Even with IAM permitting `InvokeModel`, this step is required.
2. **Wrong region.** Model availability is regional. Check the Bedrock console.
3. **Cross-account misconfiguration.** If using AssumeRole, verify the target role's policy allows `bedrock:InvokeModel` on the exact model ARN.

## Ollama: `context deadline exceeded`

Symptom: rousseau times out while Ollama is still generating.

Fixes:

1. **CPU inference is slow.** A 70B model on a laptop CPU can take minutes per turn. Use a smaller model (`llama3.1:8b`) or a GPU host.
2. **Timeout inheritance.** rousseau uses the SDK default HTTP timeout. If you wrap the provider yourself, extend the timeout to at least 120 s.

## Voice notes: transcriber not configured

Symptom: `whatsapp.audio_ignored reason=transcriber_not_configured`.

Fixes:

1. **Whisper disabled.** Set `whatsapp.voice.enabled: true` in config and ensure the `whisper` binary is on `PATH` (or set `whatsapp.voice.binary` to an absolute path).
2. **Model file missing.** Set `whatsapp.voice.model_path` to an explicit `.bin` file. Whisper.cpp models are downloaded manually — the config points at where they live.

## Session store: `database is locked`

Symptom: WAL writer blocks; requests time out.

Fixes:

1. **Two daemons, one DB.** SQLite with WAL supports concurrent readers but only one writer. If you run two rousseau processes against the same `state.path`, one will block. Use different state paths.
2. **`busy_timeout` too low.** The DSN sets `busy_timeout=15000`. Under sustained contention, raise it — but investigate the root cause first.
3. **Stale WAL file.** A crashed writer can leave `sessions.db-wal` locked. Stop everything, delete `sessions.db-wal` and `sessions.db-shm`, restart.

## MCP: Claude Desktop does not see rousseau tools

Symptom: rousseau launched via `command: "rousseau"` in `claude_desktop_config.json` but no tools appear.

Fixes:

1. **Config not saved.** Claude Desktop hot-reloads on save; if you edited the file in a running instance, restart it.
2. **`command` not on PATH.** Claude Desktop launches subprocesses from its own environment; `/usr/local/bin/rousseau` may not be visible. Use an absolute path.
3. **stderr noise.** rousseau writes structured logs to stderr; a very chatty logger can overwhelm the host. Set `log.level: warn` when running MCP against a strict host.

## Skills: `skill loader: parse: yaml: line X`

Symptom: rousseau errors on start with a YAML parse error.

Fixes:

1. **Malformed frontmatter.** Skills use `---`-delimited YAML frontmatter. Ensure both fences are present and there is no tab indentation.
2. **Unquoted colons.** A colon inside a value (`description: this: that`) is parsed as a nested map. Quote the value: `description: "this: that"`.

## `rousseau doctor` reports `warn`

Symptom: doctor completes but with amber rows.

Fixes:

1. **Read the reason.** Every warn row includes a reason. Common ones: `whatsapp.paired=false` (never linked), `state.wal_size=large` (checkpoint overdue), `provider.claudecli.model=unset` (using claude's default).
2. **Warns are not failures.** The daemon will start; the row is signalling something worth reviewing.

## Kubernetes: pod stuck in `CrashLoopBackOff`

Symptom: the deployment never reaches Ready.

Fixes:

1. **Read the logs.** `kubectl logs -p <pod>` shows the previous container's stderr. Nine times out of ten it is a config or credential error.
2. **Missing state volume.** Without a PVC for `~/.local/share/rousseau`, pairing does not survive restart and the daemon may loop trying to re-pair.
3. **IRSA / Workload Identity misconfiguration.** Verify the service account annotation matches an IAM role that has provider permissions. `kubectl exec` into the pod and run `aws sts get-caller-identity` (Bedrock) or `gcloud auth print-access-token` (Vertex) to confirm.

## nftables ruleset blocks provider egress

Symptom: `dial tcp: i/o timeout` on the first provider call after applying an egress ruleset.

Fixes:

1. **CIDR rotated.** Provider IP ranges change. Use DNS-based egress via an ipset that refreshes on a cron, or use an egress proxy that resolves at connect time.
2. **DNS blocked.** Egress ruleset must allow UDP/53 (or TCP/53) to your DNS resolver.

## Structured logs missing fields

Symptom: `whatsapp.incoming` shows up with `from` and no other attributes.

Fixes:

1. **Log level too high.** Some fields are only emitted at `debug`. Set `log.level: debug` in config.
2. **JSON parser eating fields.** Piping through a filter that strips unknown fields can drop `elapsed`, `bytes`, etc. Verify against raw stdout.

## Related pages

- [Getting Started: First Transport](/getting-started/first-transport/) — end-to-end walkthrough.
- [Providers](/providers/) — per-provider troubleshooting.
- [Transports](/transports/) — per-transport troubleshooting.
- [Configuration](/configuration/) — the source of truth for every knob.
- [Security](/security/) — trust boundaries and audit trail.

## Further reading

- `internal/cli/doctor.go` — the doctor implementation.
- `internal/state/sqlite/store.go` — session-store DSN and WAL handling.
- `internal/transport/router.go` — inbound event routing and allowlist.
- Slog attribute key reference — every `.info()`/`.warn()`/`.error()` in the source tree.
