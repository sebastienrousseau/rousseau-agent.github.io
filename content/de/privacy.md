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
description: "rousseau-agent is self-hosted. No telemetry endpoint, no SaaS control plane. LLM providers have their own retention policies; everything else stays in the operator's infrastructure."
keywords: "privacy, telemetry, self-hosted, data handling, retention, LLM providers"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/privacy/"
subtitle: "Selbstgehostet heißt selbstkontrolliert — nichts verlässt Ihre Infrastruktur außer dem LLM-Aufruf."
tags: "privacy, legal, self-hosted"
title: "Datenschutz"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "privacy, telemetry, self-hosted, data handling, retention, LLM providers"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Datenschutz"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "legal"
order: 30
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/privacy/index.html"
item_link: "https://docs.rousseau-agent.dev/privacy/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Datenschutz"
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
twitter_description: "rousseau-agent is self-hosted. No telemetry endpoint, no SaaS control plane. LLM providers have their own retention policies; everything else stays in the operator's infrastructure."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Datenschutz"
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

## Datenverarbeitung

`rousseau-agent` ist selbstgehostet. Wenn der Operator den Daemon auf eigener Infrastruktur betreibt, **verlassen keine Daten diese Infrastruktur außer dem LLM-Aufruf selbst**.

Es gibt:

- **Keinen Telemetrie-Endpunkt.** rousseau ruft zur Laufzeit weder `rousseau-agent.dev` noch einen anderen vom Autor kontrollierten Server auf.
- **Keine SaaS-Steuerungsebene.** Es gibt keinen Lizenzserver, kein Cloud-Dashboard, kein Phone-Home.
- **Keine Nutzungsanalytik.** Der Daemon meldet nicht, welche Tools aufgerufen wurden, wie viele Turns liefen oder welche Modelle aufgerufen wurden.
- **Keine Crash-Berichte.** Abstürze erscheinen in lokalen Logs (`journalctl --user -u rousseau-agent.service`). Es werden keine Stack-Traces irgendwohin versendet.

## Wo Sitzungsdaten liegen

| Daten | Ort | Verschlüsselung im Ruhezustand |
|---|---|---|
| Sitzungen (Nachrichtenverlauf) | `~/.local/share/rousseau/sessions.db` | Nur auf Dateisystemebene (LUKS / FileVault, falls vom Operator konfiguriert). |
| Cron-Jobs | Dieselbe SQLite-Datenbank | Gleich. |
| WhatsApp-Gerätekopplung | `~/.local/share/rousseau/whatsapp.db` | Gleich. |
| Log-Ausgabe | systemd-Journal (typischerweise `~/.local/state/`) | Gleich. |
| Konfigurationsdatei | `~/.config/rousseau/config.yaml` | Gleich. |
| `claude`-CLI-OAuth-Tokens | `~/.claude/` | Gleich. |

Nichts davon wird vom Daemon irgendwohin übertragen.

## LLM-Anbieter

Der LLM-Anbieter ist der einzige externe Berührungspunkt. Jeder Anbieter hat seine eigene Datenverarbeitungs- und Aufbewahrungsrichtlinie – rousseau kontrolliert keine davon:

| Provider | Aufbewahrungsrichtlinie |
|---|---|
| [claudecli](/de/providers/claudecli/) | Was auch immer die lokale `claude`-CLI zu senden konfiguriert ist. Typischerweise Anthropics Standardaufbewahrung. |
| [Anthropic direkt](/de/providers/anthropic/) | Siehe https://www.anthropic.com/legal/aup |
| [AWS Bedrock](/de/providers/bedrock/) | Vertraglich definiert; typischerweise keine langfristige Aufbewahrung für Inferenz-Traffic auf Bedrock. |
| [Google Vertex AI](/de/providers/vertex/) | Vertraglich definiert; typischerweise keine langfristige Aufbewahrung für Vertex-Inferenz. |
| [OpenAI-kompatibel](/de/providers/openai-compatible/) | Abhängig vom Endpunkt. Ollama und selbstgehostetes vLLM behalten nichts extern; OpenAI und OpenRouter haben eigene Richtlinien. |

Wählen Sie den Provider, dessen Aufbewahrungsrichtlinie zu Ihren betrieblichen Anforderungen passt. Für die strengste Haltung führen Sie gegen ein selbstgehostetes Ollama, vLLM oder LM Studio aus – keine Daten verlassen Ihre Infrastruktur.

## Transport-seitige Daten

Chat-Transporte senden Nachrichten über die Server des Anbieters (WhatsApp, Signal, Slack, Discord usw.). Jeder hat seine eigene Datenverarbeitungshaltung. rousseau fügt keine Schicht darüber hinzu – der Anbieter sieht, was auch immer das zugrundeliegende Protokoll zeigt, was protokollspezifisch ist:

- Signal und WhatsApp: Ende-zu-Ende-verschlüsselt; der Anbieter sieht Metadaten, aber keinen Nachrichteninhalt.
- Slack, Discord: nicht Ende-zu-Ende-verschlüsselt; der Anbieter sieht Nachrichteninhalte.
- Matrix: Ende-zu-Ende-verschlüsselt, wenn der Raum E2E-aktiviert ist; ansonsten serverseitig.
- Email: nicht Ende-zu-Ende-verschlüsselt, es sei denn, Sie legen PGP oder S/MIME darüber (rousseau tut das nicht).
- iMessage: Ende-zu-Ende-verschlüsselt; BlueBubbles sitzt zwischen rousseau und Apple.

## Eine Sitzung löschen

Sitzungen sind Zeilen in einer SQLite-Datenbank. Löschen mit:

```sh
rousseau session delete <session-id>
```

Oder die gesamte Datenbank verwerfen:

```sh
rm ~/.local/share/rousseau/sessions.db
```

Der nächste Start erstellt eine leere Datenbank neu. Dies löscht auch den FTS5-Cross-Session-Recall-Index.

## Drittanbieter-Abhängigkeiten

`go.mod` listet jede Abhängigkeit auf. Keine davon ist so konfiguriert, dass sie nach Hause telefoniert. Build-Zeit-Abhängigkeiten (Linter, statische Analysatoren) laufen nur in der CI. Laufzeit-Abhängigkeiten sind in der CycloneDX-SBOM aufgeführt, die jedem Release beigelegt ist.
