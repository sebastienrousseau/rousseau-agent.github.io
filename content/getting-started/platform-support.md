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
description: "Support matrix for rousseau-agent: operating systems, CPU architectures, container runtimes, provider authentication methods, transport backing libraries."
keywords: "platform support, os matrix, architecture, container runtime, provider auth, linux, macos, windows, arm64, amd64"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/getting-started/platform-support/"
subtitle: "OS, architectures, container runtimes, provider auth methods."
tags: "platform, support, matrix"
title: "Platform Support"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "platform support, os matrix, architecture, container runtime, provider auth, linux, macos, windows, arm64, amd64"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Platform Support"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 23
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/platform-support/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/platform-support/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Platform Support"
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
twitter_description: "Support matrix for rousseau-agent: operating systems, CPU architectures, container runtimes, provider authentication methods, transport backing libraries."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Platform Support"
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

## Operating systems

| OS | Support tier | Notes |
|---|---|---|
| Linux (glibc, kernel 5.10+) | Tier 1 | CI runs `ubuntu-latest` on every push. Reference deployment target. |
| Linux (musl / Alpine) | Tier 1 | Container image is Alpine-based. |
| macOS 13+ (Ventura or newer) | Tier 1 | CI runs `macos-latest` on every push. Bubble Tea TUI verified. |
| Windows 10 / 11 | Tier 2 | Binaries are built and shipped, but CI does not run the full race matrix on Windows. Chat transports work; the Podman + Quadlet reference deployment assumes Linux. |
| FreeBSD / OpenBSD | Best-effort | Pure-Go build, but no CI job. Community reports welcome. |

## CPU architectures

| Architecture | Support tier | Release naming |
|---|---|---|
| `amd64` (x86-64) | Tier 1 | `_linux_amd64`, `_darwin_amd64`, `_windows_amd64` |
| `arm64` (aarch64) | Tier 1 | `_linux_arm64`, `_darwin_arm64` (Apple Silicon) |
| `armv7` (32-bit ARM) | Best-effort | Buildable via `GOARCH=arm GOARM=7`; not released. |
| `riscv64` | Best-effort | Buildable via `GOARCH=riscv64`; not released. |

`CGO_ENABLED=0` on every target — `modernc.org/sqlite` is pure Go, so cross-compilation is friction-free.

## Container runtimes

| Runtime | Support tier | Notes |
|---|---|---|
| Podman 4.4+ (rootless) | Tier 1 | Reference deployment. Uses systemd Quadlet units for declarative hardening. |
| Docker 24+ | Tier 1 | The Dockerfile works unchanged. Runtime hardening is your responsibility (no Quadlet equivalent). |
| containerd + `nerdctl` | Tier 2 | Same image; nerdctl consumes the same OCI artefact. |
| Kubernetes 1.27+ | Tier 2 | See [Guides: Kubernetes deployment](/guides/kubernetes-deployment/). |

## Provider authentication methods

| Provider | Auth mechanism | Config keys |
|---|---|---|
| `claudecli` (default) | Inherits Claude Code's OAuth tokens from `~/.claude/`. No key in rousseau's config. | `claudecli.binary`, `claudecli.permission_mode` |
| `anthropic` | Direct API key. | `ANTHROPIC_API_KEY` env var, or `anthropic.api_key` |
| `openai` | OpenAI API key or third-party token. | `OPENAI_API_KEY`, or `openai.api_key` |
| `openrouter` | OpenRouter API key. Uses OpenAI schema with `openrouter.base_url` preset. | `openrouter.api_key` |
| `ollama` | Local endpoint, no key required (`ollama.api_key` defaults to `not-required`). | `ollama.base_url` preset to `http://localhost:11434/v1` |
| `bedrock` | Standard AWS credential chain (env vars, `~/.aws/credentials`, IMDS, IAM role). | `bedrock.region`, `bedrock.profile`, `bedrock.model` |
| `vertex` | GCP service-account JSON, or Application Default Credentials. | `vertex.project`, `vertex.region`, `vertex.credentials_file` |

## Transport backing libraries

Every transport is a thin adapter over an upstream client. Support is bounded by the upstream project's viability.

| Transport | Upstream | Protocol |
|---|---|---|
| WhatsApp | `go.mau.fi/whatsmeow` | Unofficial WhatsApp Web protocol (Signal-compatible). |
| Signal | `signal-cli` subprocess | Signal JSON-RPC. |
| Telegram | Direct Bot API client | Long polling. |
| Matrix | Direct client-server API client | HTTPS polling. |
| Slack | Direct Socket Mode client | Outbound WebSocket. |
| Discord | Direct Gateway client | Outbound WebSocket + intents. |
| iMessage | BlueBubbles HTTP client | BlueBubbles polling. Requires a macOS host running BlueBubbles Server. |
| Email | Standard `net/smtp` + IMAP client | IMAP + SMTP over TLS. |
| SMS | Direct Twilio / Vonage REST | Outbound only. |

## Optional runtime dependencies

| Dependency | Required for | Version |
|---|---|---|
| `claude` CLI | `provider: claudecli` (default). | Latest. |
| `signal-cli` | Signal transport. | 0.13+. Requires a JVM. |
| BlueBubbles Server | iMessage transport. | 1.9+. Runs on a macOS host. |
| `whisper.cpp` CLI | WhatsApp voice-note transcription (`whatsapp.voice.enabled: true`). | 1.5+. Not shipped in the container image. |
| `podman` | Reference deployment. | 4.4+ for Quadlet support. |
| `systemd` (user session) | Reference deployment. | 249+ for Quadlet. |

## Compiler and toolchain

| Component | Version | Notes |
|---|---|---|
| Go | 1.26+ | `go.mod` pins the module graph exactly. |
| golangci-lint | v2 | 18 linters, exact pins in `.golangci.yml`. |
| govulncheck | Latest | Run on every CI build. |
| cosign | 2.2+ | Only for verifying signed releases. |

## Next

- [Installation](/getting-started/installation/) — install matching your platform.
- [Updating](/getting-started/updating/) — move between versions safely.
