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
changefreq: "weekly"
description: "Selbstgehosteter Coding-Agent mit 9 Chat-Transporten, 5 LLM-Anbietern, MCP-Server, SLSA-3-Provenienz, cosign-signierten Releases."
keywords: "rousseau-agent, coding agent, self-hosted, container-native, MCP, SLSA-3, cosign, SBOM, LLM, WhatsApp, Signal, Slack"
layout: "index"
permalink: "https://docs.rousseau-agent.dev/de/"
subtitle: "Selbstgehosteter, containernativer, MCP-nativer Coding-Agent."
tags: "overview, self-hosted, mcp, security"
title: "rousseau-agent"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "rousseau-agent, coding agent, self-hosted, container-native, MCP, SLSA-3, cosign, SBOM, LLM, WhatsApp, Signal, Slack"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau-agent"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "welcome"
order: 1
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/index.html"
item_link: "https://docs.rousseau-agent.dev/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "rousseau-agent"
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
twitter_description: "Selbstgehosteter Coding-Agent mit 9 Chat-Transporten, 5 LLM-Anbietern, MCP-Server, SLSA-3-Provenienz, cosign-signierten Releases."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau-agent"
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

## Selbstgehosteter, containernativer, MCP-nativer Coding-Agent

**rousseau-agent** ist ein Go-Coding-Assistent, der dort läuft, wo Ihr Code läuft. Der Daemon, die Auth-Materialien und der Modell-Traffic bleiben auf Hardware, die der Betreiber kontrolliert. **9 Transporte · 5 LLM-Anbieter · SLSA-3 · cosign · SBOM.**

```sh
rousseau chat
```

Dieser eine Befehl startet eine Bubble-Tea-TUI, die von dem LLM-Anbieter Ihrer Wahl versorgt wird. Nichts verlässt Ihr Netzwerk-Perimeter außer dem Anbieter-Aufruf selbst.

## Drei Säulen

### Enterprise-gehärtet

- **SLSA Level 3** Build-Provenienz über `slsa-framework/slsa-github-generator`.
- **cosign** keyless-Signaturen auf jeder Release-Checksummen-Datei, verifizierbar gegen das Sigstore-Transparency-Log.
- **CycloneDX** JSON-SBOM zu jedem Release beigelegt.
- **Reproduzierbare Builds**, in CI auf einem frischen Checkout verifiziert.
- Rootless-Podman mit `ReadOnly=true`, `DropCapability=all`, `NoNewPrivileges=true`, Standard-seccomp-Filter, Non-Root-UID 1000, `keep-id`-User-Namespace-Mapping.
- 18-Linter-`golangci-lint`-v2-Gate, CodeQL (Go), `govulncheck` bei jedem CI-Lauf, Dependabot für `gomod` und `github-actions`.

### Multimodale Reichweite

Neun Chat-Transporte hinter einem Daemon:

- [WhatsApp](/de/transports/whatsapp/) (`go.mau.fi/whatsmeow`, Signal-Protokoll-kompatibel)
- [Signal](/de/transports/signal/) (`signal-cli`-JSON-RPC-Subprozess)
- [Telegram](/de/transports/telegram/) (Bot-API-Long-Polling)
- [Matrix](/de/transports/matrix/) (Client-Server-API)
- [Slack](/de/transports/slack/) (Socket Mode, keine öffentliche HTTP-Oberfläche)
- [Discord](/de/transports/discord/) (Gateway v10)
- [iMessage](/de/transports/imessage/) (BlueBubbles-HTTP-Polling)
- [Email](/de/transports/email/) (IMAP + SMTP)
- [SMS](/de/transports/sms/) (Twilio oder Vonage, nur Versand)

### Modell-agnostisch

Fünf LLM-Anbieter-Familien, eine `agent.Provider`-Schnittstelle:

- [claudecli](/de/providers/claudecli/) — Subprozess auf Ihre lokale `claude`-CLI, erbt deren Authentifizierung.
- [Anthropic](/de/providers/anthropic/) — direkte API mit ephemeren Prompt-Cache-Markern.
- [AWS Bedrock](/de/providers/bedrock/) — Standard-AWS-Credential-Chain.
- [Google Vertex AI](/de/providers/vertex/) — Service-Account-JSON oder ADC.
- [OpenAI-kompatibel](/de/providers/openai-compatible/) — OpenAI, OpenRouter, Ollama, vLLM, LM Studio.

## Wohin als Nächstes

- [Erste Schritte](/de/getting-started/) — installieren, erster Start, erster Transport.
- [Konfiguration](/de/configuration/) — jedes Feld in `internal/config/config.go`.
- [Bereitstellung](/de/deployment/) — Rootless-Podman + Quadlet, Kubernetes-Hinweis.
- [Sicherheit](/de/security/) — Supply-Chain-Posture, Trust-Modell, cosign-Rezept.
- [Konzepte](/de/concepts/) — Agent-Loop, Session-Store, MCP, Cron, Skills.
