---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "Configure rousseau-agent as a read-only inspection agent: deny_all approver with a read/grep exception, plan-mode claudecli, read-only bind mounts."
keywords: "read-only, inspection, deny_all, plan mode, bind mount, ro mount, audit"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/guides/read-only-mode/"
subtitle: "An inspection posture that cannot mutate the workspace."
tags: "guides, read-only, deny_all, plan-mode"
title: "Guide: Read-only Mode"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "read-only, inspection, deny_all, plan mode, bind mount, ro mount, audit"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: Read-only Mode"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 36
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/read-only-mode/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/read-only-mode/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guide: Read-only Mode"
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
twitter_description: "Configure rousseau-agent as a read-only inspection agent: deny_all approver with a read/grep exception, plan-mode claudecli, read-only bind mounts."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide: Read-only Mode"
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

## Scenario

You want rousseau to inspect a repository, answer questions about it, and produce reports — but it must not be able to write, edit, or run destructive shell commands. This is the posture you would deploy for a first-pass audit, an incident-response inspection, or a compliance walk-through.

Three layers stack to make this hard:

1. **Approval policy** — deny every mutating tool.
2. **`claudecli` permission mode** — put Claude Code in `plan` mode so its own approver never edits files.
3. **Filesystem** — bind-mount the workspace read-only.

Belt, braces, and a second belt. Any one of the three fails safely.

## Layer 1 — Approver

The simplest read-only posture uses the `pattern` approver with a whitelist:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "read-only inspection posture — this deployment cannot mutate files"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|find|wc|stat|file|which|pwd|env|git status|git diff|git log|git show|git branch)\\b"}
    # No deny rules needed — default: deny catches everything else.
    # No edit, write, or unrestricted bash — the model can't reach them.
```

An even stricter variant uses `deny_all`, which blocks every tool including `read` and `grep`:

```yaml
agent:
  approver:
    mode: deny_all
    reason: "smoke test — no tool calls allowed"
```

`deny_all` is only useful as a smoke test; the model won't be able to do meaningful work.

## Layer 2 — `claudecli` permission mode

When the provider is `claudecli`, Claude Code itself is running the tool calls. Setting `permission_mode: plan` makes Claude Code refuse every write- or edit-side call in its own layer, even if the rousseau approver would have allowed it:

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: plan
```

Valid values (see `internal/config/config.go` and Claude Code's docs): `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. `plan` is the only value that consistently keeps Claude Code in read-only posture.

## Layer 3 — Filesystem

Mount the workspace read-only. Under the reference Podman Quadlet:

```
Volume=%h/team-rousseau-workspace:/workspace:ro,Z
```

`ro` makes the mount read-only from the container's perspective; even if a compromised binary tried to `open(2)` with `O_WRONLY`, the kernel would return `EROFS`.

Under Kubernetes:

```yaml
volumeMounts:
  - name: workspace
    mountPath: /workspace
    readOnly: true
```

The session store (`~/.local/share/rousseau/`) still needs to be writable — the daemon appends to it on every turn. Keep that mount `rw` and leave only the workspace read-only.

## Dry-run posture

There is no `--dry-run` flag on the daemon. If you want the model to *plan* changes without executing them, the combination above achieves the equivalent:

- The approver blocks every mutating tool → the model gets a `tool_result` error explaining the block.
- `plan` mode in `claudecli` keeps Claude Code from running its own destructive tools.
- Read-only mounts stop anything that leaks through.

The model will typically respond with a plan document rather than a diff. That is the read-only inspection deliverable.

## What still works

- Every `read` and `grep` call.
- `bash` for safe read-side utilities you enumerated.
- Session persistence — the SQLite store still records the conversation.
- Cross-session recall via FTS5, MCP export, skills — all read-only anyway.

## What breaks (intentionally)

- `write` and `edit` — deny.
- Shell mutation commands — deny.
- Cron jobs whose prompt implies file writes — the model tries, gets denied, replies with a plan.
- `rousseau init` — the CLI is not affected by the approver, but it writes to `~/.config/rousseau/` outside the workspace. Run it before rolling out read-only mode.

## Testing the posture

```sh
rousseau chat
> Edit /workspace/README.md to add a footer.
```

Expected log line:

```
WARN tool.denied name=edit reason="read-only inspection posture — this deployment cannot mutate files"
```

Expected chat reply: the model apologises, produces a plan or a diff patch as text, and asks the operator to apply it.

For the `deny_all` variant, every tool call is blocked — the model has no way to inspect anything, so this posture is only useful as a smoke test.

## Layering with other transports

The same three layers apply to WhatsApp, Slack, Discord, and every other transport. Because the approver runs inside the agent loop, it does not care which transport delivered the user turn. A read-only Slack agent is one `mode: pattern` block away.

## Caveats

- The read-only posture is enforced by rousseau's approver and by the filesystem — **not** by the LLM. A model can still emit an `edit` tool call; the approver silently blocks it, but the attempt is logged as `tool.denied`. This is intentional so audit trails record what the model tried, not just what succeeded.
- Read-only bind mounts do not protect against symlinks pointing outside the mount. The reference Podman posture drops all capabilities, which prevents most escape paths, but do not rely on the mount alone.
- The `claudecli` provider's `plan` mode is Claude Code's contract, not rousseau's. If Claude Code changes its permission-mode semantics, rousseau's read-only posture inherits that change.

## Next

- [User Guide: Approval Policies](/user-guide/approval-policies/) — deeper reference.
- [Audit + approval policies](/guides/audit-approval-policies/) — the mutating counterpart.
- [Deployment](/deployment/) — mount and container flags.
