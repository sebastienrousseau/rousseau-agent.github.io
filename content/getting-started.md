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
description: "Install rousseau-agent from source, go install, or a cosign-verified release. Run rousseau chat and configure the first chat transport."
keywords: "install, quickstart, rousseau chat, cosign verify, go install, systemd, podman"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/getting-started/"
subtitle: "Install rousseau-agent and reach your first transport."
tags: "install, quickstart, getting-started"
title: "Getting Started"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "install, quickstart, rousseau chat, cosign verify, go install, systemd, podman"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Getting Started"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 2
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Getting Started"
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
twitter_description: "Install rousseau-agent from source, go install, or a cosign-verified release. Run rousseau chat and configure the first chat transport."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Getting Started"
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

## Who this is for

- **Individual developers** who want a coding assistant that runs on their own laptop and drives their existing `claude` CLI. No API keys plumbed through rousseau's config, no cloud broker in the middle.
- **Platform operators** running a shared coding agent for a team behind a corporate perimeter. Rousseau is a single static Go binary in a rootless Podman container with dropped capabilities — deployable next to any other systemd service.
- **Security reviewers** vetting an agent before rollout. SLSA-3 provenance, cosign-signed release checksums, CycloneDX SBOM, reproducible builds, and every trust boundary is documented in [Security](/security/).

## The fastest path

1. **If you already have the `claude` CLI installed and authenticated,** the fastest start is `rousseau chat` with the default `claudecli` provider — auth is inherited, no keys to plumb. Continue with [First run](#first-run) below.
2. **If you want a direct API path with your own key,** set `ANTHROPIC_API_KEY` and switch `provider: anthropic` in `~/.config/rousseau/config.yaml`. See [Anthropic provider](/providers/anthropic/).
3. **If you're in an enterprise with AWS Bedrock or Google Vertex,** pick the matching provider — [Bedrock](/providers/bedrock/) uses the standard AWS credential chain; [Vertex](/providers/vertex/) reads a service-account JSON. No secrets sit in rousseau's config file.
4. **If you're air-gapped or want fully self-hosted inference,** point rousseau at an OpenAI-compatible endpoint — Ollama, vLLM, LM Studio, or any shim. See [OpenAI-compatible provider](/providers/openai-compatible/).

## What you'll have at the end

- A `rousseau` binary on `$PATH` verified against a cosign signature (release path) or built from source (`make check` runs the same 18-linter + race + govulncheck gate CI enforces).
- A working `rousseau chat` TUI backed by whichever provider you picked.
- A SQLite session store at `~/.local/share/rousseau/sessions.db` — every turn is persisted, cross-session recall via FTS5 is available.
- Optionally: one live chat transport (WhatsApp, Slack, Signal, ...) reachable from your phone.

## Prefer to watch?

A short screencast of the flow below is on the roadmap. Until then, the whole ceremony fits on this page — most operators finish in under ten minutes.

## System requirements

| Requirement | Version | Notes |
|---|---|---|
| Go toolchain | 1.26+ | `CGO_ENABLED=0`; the binary is fully static. |
| Container runtime | Podman 4.4+ | Reference deployment uses rootless Podman + a systemd Quadlet unit. Docker works but Quadlet is Podman-specific. |
| `claude` CLI | latest | Only if using the default `claudecli` provider. |
| `signal-cli` | 0.13+ | Only if using the Signal transport. |
| BlueBubbles server | 1.9+ | Only if using the iMessage transport (macOS host required). |
| `whisper.cpp` | 1.5+ | Only if you enable WhatsApp voice-note transcription. |

## Install

### From source

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` runs vet, `golangci-lint`, `go test -race`, and `govulncheck` — the same gates CI enforces.

### Via `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

The binary embeds `modernc.org/sqlite`, so there is no libc or CGo dependency at runtime.

### From a signed release

Every tagged release publishes a checksummed archive, a CycloneDX SBOM, a SLSA-3 provenance attestation, and a cosign signature of the checksum file. Always verify before running:

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_<version>_checksums.txt.sig \
  rousseau_<version>_checksums.txt

sha256sum -c rousseau_<version>_checksums.txt
```

The certificate-identity regex is what pins the signer identity; do not weaken it.

## First run

### Terminal chat

```sh
rousseau chat
```

Bubble Tea TUI. Enter to send, `Ctrl+C` to quit. The default provider is `claudecli`, which inherits authentication from your local Claude Code install; no API keys are plumbed through rousseau's config.

Session history persists to `~/.local/share/rousseau/sessions.db` (SQLite with WAL journaling and FTS5 for cross-session recall).

### First chat transport

WhatsApp is the reference transport (pairing UX is the most stringent). Pair on first launch by scanning the QR from your phone:

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

The E.164 JID (`<digits>@s.whatsapp.net`) restricts inbound handling; every other sender is silently dropped. Pairing state is stored in `whatsapp.db` alongside the session store.

Other transports follow the same shape:

```sh
rousseau slack   --app-token xapp-... --bot-token xoxb-...
rousseau discord --token bot-token
rousseau telegram --token 12345:ABC
rousseau matrix  --homeserver-url https://matrix.org --access-token ... --user-id @bot:matrix.org
```

Every `rousseau <transport> --help` lists its flags. Defaults come from `~/.config/rousseau/config.yaml`.

## Where state is stored

| Path | Purpose |
|---|---|
| `~/.config/rousseau/config.yaml` | User-level configuration file (Viper). |
| `~/.local/share/rousseau/sessions.db` | Sessions, cron jobs, JID map, FTS5 recall index. |
| `~/.local/share/rousseau/whatsapp.db` | Whatsmeow device credentials (kept separate so a device relink does not touch conversations). |
| `~/.claude/` | `claude` CLI OAuth tokens, only when using the `claudecli` provider. |

## Next steps

- [Concepts](/concepts/) — the agent loop, session store, MCP, cron, skills.
- [Configuration](/configuration/) — every knob.
- [Deployment](/deployment/) — how to run the daemon under systemd.
