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
description: "Set up rousseau-agent's WhatsApp transport: QR pairing, E.164 allowlist, LID vs phone-JID normalisation, voice-note transcription with whisper.cpp."
keywords: "WhatsApp, whatsmeow, QR pairing, JID, LID, allowlist, voice notes, whisper, transcription"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/transports/whatsapp/"
subtitle: "Whatsmeow-backed WhatsApp bridge with QR pairing."
tags: "transports, WhatsApp"
title: "WhatsApp Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "WhatsApp, whatsmeow, QR pairing, JID, LID, allowlist, voice notes, whisper, transcription"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "WhatsApp Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 12
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/whatsapp/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/whatsapp/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "WhatsApp Transport"
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
twitter_description: "Set up rousseau-agent's WhatsApp transport: QR pairing, E.164 allowlist, LID vs phone-JID normalisation, voice-note transcription with whisper.cpp."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "WhatsApp Transport"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>How the WhatsApp transport pairs with your phone, the LID vs phone-JID normalisation rules, voice-note transcription flow, media downloads, allowlist regex patterns, and the failure modes that catch first-time operators. Read <code>internal/transport/whatsapp/client.go</code>, <code>resolve.go</code>, and <code>dispatch.go</code> alongside this page.</p></aside>

## Overview

The WhatsApp transport (`internal/transport/whatsapp/`) is backed by `go.mau.fi/whatsmeow` — a reverse-engineered WhatsApp Web multi-device client. Meta considers this an unofficial client; do not run it on a personal number you rely on for anything important.

Signal-protocol end-to-end encryption is preserved (whatsmeow uses the same protocol as the WhatsApp mobile app). The daemon holds device credentials in a SQLite file separate from the session store, so a device relink does not touch conversation history.

<aside class="admonition" data-type="caution"><span class="admonition-title">Unofficial protocol</span><p>Meta occasionally bans numbers running unofficial clients. Even if you comply with WhatsApp's rate limits and behave responsibly, a phone number used with <code>whatsmeow</code> may be banned without warning. Use a dedicated number, not a personal one.</p></aside>

## Pairing

First launch:

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

A QR code prints to stdout via `mdp/qrterminal/v3`. Scan it with the WhatsApp phone app (**Settings → Linked Devices → Link a Device**). The pairing state is written to `whatsapp.db` under the state directory (typically `~/.local/share/rousseau/whatsapp.db`).

Subsequent launches reuse the paired device silently. If the QR reappears, the pairing has been revoked from the phone side — delete `whatsapp.db` and pair again.

## Allowlist

`--allow` restricts inbound handling. Multiple flags accumulate:

```sh
rousseau whatsapp \
  --allow 447900123456@s.whatsapp.net \
  --allow 442071234567@s.whatsapp.net
```

The value is a WhatsApp **JID** — the E.164 phone number (no `+`) followed by `@s.whatsapp.net`. Group JIDs (`<id>@g.us`) are also supported.

Empty allowlist accepts every sender. For a chat-transport daemon you always want at least one entry.

## LID vs phone-JID normalisation

WhatsApp uses two identifier formats for a user:

| Format | Example | Meaning |
|---|---|---|
| Phone JID | `447900123456@s.whatsapp.net` | The E.164 phone number, without `+`, followed by `@s.whatsapp.net`. Stable across time; leaks the phone number. |
| LID | `1234567890@lid` | Location-Independent ID — a random-looking string that does not reveal the phone number. Also stable, but not directly linkable to a number. |
| Device suffix | `447900123456:5@s.whatsapp.net` | Any JID can carry a device-address suffix (`:N`). WhatsApp reports messages with the specific device that sent them. |

Rousseau's inbound handler (`ResolveInbound` in `internal/transport/whatsapp/resolve.go`) normalises every event to a canonical form before dispatching:

1. **Strip the device suffix.** `447900:5@s.whatsapp.net` becomes `447900@s.whatsapp.net`. This lets allowlists written as bare user JIDs match regardless of which linked device sent the message.
2. **Substitute LID for the account holder's phone JID in self-chat.** When the account holder is the sender (`IsFromMe=true`), WhatsApp reports the sender as the account's LID (a privacy hash), not the phone JID. Rousseau substitutes the account's own JID so operators can allowlist `<phone>@s.whatsapp.net` and have self-chat testing route correctly.
3. **Drop unparseable senders.** Empty `User` or `Server` fields — discovered by `FuzzResolveInbound` — cannot be routed safely. The message is silently skipped rather than passed to the handler as a malformed From.

### Self-chat gotcha

When you send a message to yourself in WhatsApp (to test the bot), the sender field arrives as your LID. If you allowlisted your phone JID, the naive lookup would miss. Rousseau's substitution — `if evt.Info.IsFromMe && ownID != nil { from = ownID.ToNonAD() }` — fixes this.

### Loop prevention

`IsFromMe=true` also fires for messages sent by *this* linked device (rousseau's outbound replies echoing back). The transport drops those when the device ID matches:

```go
if evt.Info.IsFromMe && ownID != nil && evt.Info.Sender.Device == ownID.Device {
    return Resolved{Skip: SkipOwnDevice}
}
```

Messages from the account's *other* linked devices (e.g. the primary phone testing "message yourself") carry `IsFromMe=true` but a different device ID — those are handled normally.

## Allowlist regex patterns

The `--allow` flag takes exact strings, not regexes — rousseau performs a case-insensitive equality check in `router.go`. If you want pattern matching, use the config file with `pattern` mode (the same as approval policies):

```yaml
whatsapp:
  allowlist:
    - "447900123456@s.whatsapp.net"
    - "447900654321@s.whatsapp.net"
```

For groups (`<hash>@g.us`), add them the same way. To allow everyone from a given country code, you would need a custom `Router.Allow` implementation — the built-in enforcer does not do prefix matching by design.

<aside class="admonition" data-type="warning"><span class="admonition-title">Empty allowlist</span><p>An empty allowlist accepts every sender. Do not run a chat transport with no allowlist on a public number — anyone who knows the number becomes an operator of your agent.</p></aside>

## Reply header

Every outbound message is prefixed with a header so the sender knows which bot they are talking to. The default:

```
💎 *Rousseau Agent*

<message body>
```

WhatsApp renders `*text*` as bold. Override in config:

```yaml
whatsapp:
  reply_header: "🤖 *Coding bot*\n\n"
```

Set to a single space `" "` to disable the prefix entirely.

## Voice-note transcription

Inbound voice notes are transcribed via `whisper.cpp` when the operator opts in. Off by default because it requires the `whisper` CLI to be installed.

```yaml
whatsapp:
  voice:
    enabled: true
    binary: whisper
    model: base.en
    language: en
    extra_args:
      - --threads
      - "4"
```

| Field | Effect |
|---|---|
| `enabled` | Toggle. When off, audio messages are logged and skipped. |
| `binary` | Whisper CLI executable. Empty defaults to `whisper`. |
| `model` | Passed to `--model` (`base.en`, `small`, `medium`). |
| `model_path` | Explicit `.bin` path. Takes precedence over `model`. |
| `language` | Passed to `--language`. Empty auto-detects. |
| `extra_args` | Appended to every invocation. |

The transcribed text is handed to the agent as if the user had typed it.

## Container deployment

The reference Podman Quadlet unit (`docker/rousseau-agent.container`) mounts the state directory read-write so the pairing survives restarts:

```
Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
```

`Network=pasta` gives the container a rootless egress-only stack. Whatsmeow needs no elevated capabilities; `DropCapability=all` is safe.

## Voice-note transcription flow

When a voice note arrives, the standard resolver returns `SkipEmptyText` (no text content). `Dispatch` detects this specifically for audio messages and — if a `Transcriber` is configured — proceeds through this path:

```
Inbound audio message
  │
  ├── Downloader.Download(ctx, audioMsg)
  │     • bytes []byte, mimetype string, err error
  │     • Logs whatsapp.audio_downloaded on success
  │
  ├── Transcriber.Transcribe(ctx, audio, mimetype)
  │     • Returns plain-text transcription
  │     • Logs whatsapp.transcribed with duration
  │
  └── Re-enter handleTextMessage with the transcription as `Body`
```

If no transcriber is configured, the daemon logs `whatsapp.audio_ignored reason=transcriber_not_configured` and drops the message. Voice notes never trigger a "silence" reply — an empty inbound produces an empty outbound.

## Media downloads

The `Downloader` interface is small on purpose:

```go
type Downloader interface {
    Download(ctx context.Context, msg DownloadableAudio) (bytes []byte, mimetype string, err error)
}
```

Currently only audio download is wired. Image and video downloads are on the roadmap — they arrive as `waProto.ImageMessage` / `VideoMessage` and would need a corresponding `DownloadableMedia` interface. Track [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md) for the plan.

## Typing indicators

The handler wraps every reply in `SendPresence(Composing, Paused)` calls so the sender sees the "…is typing" indicator while the model thinks. Both calls have a 5-second timeout and are best-effort — a presence failure never blocks the reply itself.

## Failure modes

| Symptom | Fix |
|---|---|
| QR reprints on every restart | Pairing has been revoked from the phone; delete `whatsapp.db` and re-pair. |
| WhatsApp reconnect loop | Check clock skew against `pool.ntp.org` — whatsmeow's handshake is time-sensitive. |
| Inbound messages ignored | Verify the sender is in the `--allow` list; check logs for `router.transport.rejected`. |
| Meta bans the number | Do not run on a personal number. The protocol is unofficial. |
| Self-chat "hello" not routed | Self-chat uses LID; rousseau substitutes to phone JID for allowlist matching. Verify `ownID` is initialised — the daemon logs `whatsapp.connected` when it is. |
| Voice notes silently dropped | Either `whatsapp.voice.enabled: false` or the `whisper` binary is missing. Log line: `whatsapp.audio_ignored`. |
| Every reply comes back to me twice | Loop prevention is off. Ensure you are running a recent build; the fix landed in `ResolveInbound` early in the whatsmeow multi-device rollout. |

## Troubleshooting

### QR is printed but the phone app rejects it

Three common causes: (1) a partially-completed prior pairing left `whatsapp.db` in a state whatsmeow cannot reuse — delete the file and re-scan; (2) the clock is skewed by more than 30 seconds (common in containers without NTP) — check with `timedatectl status`; (3) an older `whatsmeow` version can miss a Meta protocol update.

### `whatsapp.connected` then `whatsapp.disconnected` in a loop

Clock skew, or Meta has invalidated the pairing. Check `whatsapp.logged_out` events in the log — that's the definitive signal.

### Voice notes arrive but never get transcribed

The transcriber binary is not resolvable. Check `whatsapp.voice.binary` and `whatsapp.voice.model_path` — both must point at real files (or `binary` must be on `PATH`).

### Allowlist regex not matching

Rousseau's allowlist is exact-string, not regex. To match a range of senders, list each one explicitly or add a custom router.

### Reply header shows up as literal `*` characters

The recipient's client does not render WhatsApp Markdown. This is a client-side rendering issue; use plain text if your recipients are on older clients.

## Related pages

- [Getting Started: First Transport](/getting-started/first-transport/) — end-to-end walkthrough.
- [User Guide: Voice Mode](/user-guide/voice-mode/) — voice-note deep dive.
- [Configuration](/configuration/) — the `whatsapp` config block.
- [Transports](/transports/) — the other eight transports.
- [Deployment](/deployment/) — running WhatsApp in a Podman container.

## Further reading

- `internal/transport/whatsapp/client.go` — connect, QR pairing, event pump.
- `internal/transport/whatsapp/resolve.go` — LID/JID normalisation and self-chat handling.
- `internal/transport/whatsapp/dispatch.go` — inbound message dispatch with voice-note branching.
- `internal/transport/whatsapp/whisper.go` — reference whisper-cpp transcriber.
- `internal/cli/whatsapp.go` — CLI wiring, store DSN, transcriber selection.
