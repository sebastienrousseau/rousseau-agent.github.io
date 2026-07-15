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
hreflang: "de"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "de"
locale: "de_DE"
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
permalink: "https://docs.rousseau-agent.dev/de/getting-started/platform-support/"
subtitle: "OS, architectures, container runtimes, provider auth methods."
tags: "platform, support, matrix"
title: "Plattformunterstützung"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "platform support, os matrix, architecture, container runtime, provider auth, linux, macos, windows, arm64, amd64"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Plattformunterstützung"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 23
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/platform-support/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/platform-support/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Plattformunterstützung"
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
twitter_title: "Plattformunterstützung"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Betriebssysteme

| OS | Support-Stufe | Hinweise |
|---|---|---|
| Linux (glibc, Kernel 5.10+) | Tier 1 | CI läuft `ubuntu-latest` bei jedem Push. Referenz-Bereitstellungsziel. |
| Linux (musl / Alpine) | Tier 1 | Container-Image ist Alpine-basiert. |
| macOS 13+ (Ventura oder neuer) | Tier 1 | CI läuft `macos-latest` bei jedem Push. Bubble-Tea-TUI verifiziert. |
| Windows 10 / 11 | Tier 2 | Binaries werden gebaut und ausgeliefert, aber die CI führt die vollständige Race-Matrix nicht unter Windows aus. Chat-Transporte funktionieren; die Podman-+-Quadlet-Referenzbereitstellung setzt Linux voraus. |
| FreeBSD / OpenBSD | Best-effort | Pure-Go-Build, aber kein CI-Job. Community-Berichte willkommen. |

## CPU-Architekturen

| Architektur | Support-Stufe | Release-Namensschema |
|---|---|---|
| `amd64` (x86-64) | Tier 1 | `_linux_amd64`, `_darwin_amd64`, `_windows_amd64` |
| `arm64` (aarch64) | Tier 1 | `_linux_arm64`, `_darwin_arm64` (Apple Silicon) |
| `armv7` (32-Bit-ARM) | Best-effort | Baubar über `GOARCH=arm GOARM=7`; nicht veröffentlicht. |
| `riscv64` | Best-effort | Baubar über `GOARCH=riscv64`; nicht veröffentlicht. |

`CGO_ENABLED=0` bei jedem Ziel – `modernc.org/sqlite` ist reines Go, daher ist Cross-Kompilierung reibungslos.

## Container-Laufzeiten

| Runtime | Support-Stufe | Hinweise |
|---|---|---|
| Podman 4.4+ (rootless) | Tier 1 | Referenzbereitstellung. Verwendet systemd-Quadlet-Units für deklarative Härtung. |
| Docker 24+ | Tier 1 | Das Dockerfile funktioniert unverändert. Laufzeit-Härtung liegt in Ihrer Verantwortung (kein Quadlet-Äquivalent). |
| containerd + `nerdctl` | Tier 2 | Gleiches Image; nerdctl konsumiert dasselbe OCI-Artefakt. |
| Kubernetes 1.27+ | Tier 2 | Siehe [Leitfäden: Kubernetes-Bereitstellung](/de/guides/kubernetes-deployment/). |

## Provider-Authentifizierungsmethoden

| Provider | Auth-Mechanismus | Konfigurationsschlüssel |
|---|---|---|
| `claudecli` (Standard) | Erbt die OAuth-Tokens von Claude Code aus `~/.claude/`. Kein Schlüssel in rousseaus Konfiguration. | `claudecli.binary`, `claudecli.permission_mode` |
| `anthropic` | Direkter API-Schlüssel. | `ANTHROPIC_API_KEY`-Umgebungsvariable oder `anthropic.api_key` |
| `openai` | OpenAI-API-Schlüssel oder Drittanbieter-Token. | `OPENAI_API_KEY` oder `openai.api_key` |
| `openrouter` | OpenRouter-API-Schlüssel. Verwendet das OpenAI-Schema mit vorbelegtem `openrouter.base_url`. | `openrouter.api_key` |
| `ollama` | Lokaler Endpunkt, kein Schlüssel erforderlich (`ollama.api_key` hat Standardwert `not-required`). | `ollama.base_url` vorbelegt mit `http://localhost:11434/v1` |
| `bedrock` | Standard-AWS-Credential-Chain (Umgebungsvariablen, `~/.aws/credentials`, IMDS, IAM-Rolle). | `bedrock.region`, `bedrock.profile`, `bedrock.model` |
| `vertex` | GCP-Service-Account-JSON oder Application Default Credentials. | `vertex.project`, `vertex.region`, `vertex.credentials_file` |

## Zugrundeliegende Transport-Bibliotheken

Jeder Transport ist ein dünner Adapter über einem Upstream-Client. Der Support ist durch die Lebensfähigkeit des Upstream-Projekts begrenzt.

| Transport | Upstream | Protokoll |
|---|---|---|
| WhatsApp | `go.mau.fi/whatsmeow` | Inoffizielles WhatsApp-Web-Protokoll (Signal-kompatibel). |
| Signal | `signal-cli`-Subprozess | Signal-JSON-RPC. |
| Telegram | Direkter Bot-API-Client | Long-Polling. |
| Matrix | Direkter Client-Server-API-Client | HTTPS-Polling. |
| Slack | Direkter Socket-Mode-Client | Ausgehende WebSocket. |
| Discord | Direkter Gateway-Client | Ausgehende WebSocket + Intents. |
| iMessage | BlueBubbles-HTTP-Client | BlueBubbles-Polling. Erfordert einen macOS-Host, auf dem BlueBubbles Server läuft. |
| Email | Standard-`net/smtp` + IMAP-Client | IMAP + SMTP über TLS. |
| SMS | Direktes Twilio-/Vonage-REST | Nur ausgehend. |

## Optionale Laufzeit-Abhängigkeiten

| Abhängigkeit | Erforderlich für | Version |
|---|---|---|
| `claude`-CLI | `provider: claudecli` (Standard). | Aktuellste. |
| `signal-cli` | Signal-Transport. | 0.13+. Erfordert eine JVM. |
| BlueBubbles Server | iMessage-Transport. | 1.9+. Läuft auf einem macOS-Host. |
| `whisper.cpp`-CLI | Transkription von WhatsApp-Sprachnachrichten (`whatsapp.voice.enabled: true`). | 1.5+. Nicht im Container-Image enthalten. |
| `podman` | Referenzbereitstellung. | 4.4+ für Quadlet-Unterstützung. |
| `systemd` (User-Session) | Referenzbereitstellung. | 249+ für Quadlet. |

## Compiler und Toolchain

| Komponente | Version | Hinweise |
|---|---|---|
| Go | 1.26+ | `go.mod` pinnt den Modulgraph exakt. |
| golangci-lint | v2 | 18 Linter, exakte Pins in `.golangci.yml`. |
| govulncheck | Aktuellste | Läuft bei jedem CI-Build. |
| cosign | 2.2+ | Nur zur Verifikation signierter Releases. |

## Weiter

- [Installation](/de/getting-started/installation/) — passend zu Ihrer Plattform installieren.
- [Aktualisieren](/de/getting-started/updating/) — sicher zwischen Versionen wechseln.
