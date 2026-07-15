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
date: "July 13, 2026"
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
description: "Run two rousseau daemons with different providers side-by-side — e.g. claudecli for interactive chat and Bedrock for scheduled reports."
keywords: "multi provider, claudecli, bedrock, config precedence, XDG_CONFIG_HOME"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/guides/multi-provider/"
subtitle: "Two daemons, two providers, one operator."
tags: "guides, providers, multi-provider, deployment"
title: "Leitfaden: Multi-Anbieter"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "multi provider, claudecli, bedrock, config precedence, XDG_CONFIG_HOME"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: Multi-Anbieter"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 35
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/multi-provider/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/multi-provider/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: Multi-Anbieter"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
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
twitter_description: "Run two rousseau daemons with different providers side-by-side — e.g. claudecli for interactive chat and Bedrock for scheduled reports."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Leitfaden: Multi-Anbieter"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Warum Sie das möchten könnten

Das `provider`-Feld von rousseau ist ein einzelnes Skalar (`internal/config/config.go` `Config.Provider`). Ein einzelner rousseau-Prozess spricht mit genau einem Provider. Wenn Sie mehr als einen möchten — am häufigsten `claudecli` für die interaktive TUI-Nutzung, weil es eine OAuth-Sitzung erbt, und einen kostenpflichtigen API-Provider (Bedrock, Anthropic direkt, Vertex) für Hintergrund-Daemons, wo eine Abonnement-Stufen-`claude`-OAuth unbequem ist — dann betreiben Sie **zwei rousseau-Prozesse** mit verschiedenen Konfigurationsdateien.

Sinnvolle Paarungen:

| Interaktiv | Unbeaufsichtigt | Warum |
|---|---|---|
| `claudecli` | `anthropic` oder `bedrock` | OAuth für Laptop-Chat, API-Schlüssel für einen VPS-Daemon. |
| `claudecli` | `vertex` | Dasselbe, auf GCP. |
| `anthropic` | `openai` oder `ollama` | Antworten vergleichen oder auf ein günstigeres/lokales Modell für Cron zurückfallen. |
| `claudecli` | `openai` (OpenRouter) | Claude im TUI, günstiges OpenRouter-Modell für geplante Zusammenfassungen. |

## Wie rousseau die Konfiguration auflöst

`config.Load` (in `internal/config/config.go`) wendet Flag > Env > Datei > Default an. Die gelesene Datei ist standardmäßig `~/.config/rousseau/config.yaml`, aber das persistente `--config`-Flag am Root-Befehl (`internal/cli/root.go`) überschreibt sie. Das ergibt eine saubere Trennung.

## Zwei-Konfigurations-Layout

```sh
mkdir -p ~/.config/rousseau
cat > ~/.config/rousseau/chat.yaml <<'YAML'
provider: claudecli
claudecli:
  binary: claude
log:
  level: info
  format: text
YAML

cat > ~/.config/rousseau/cron.yaml <<'YAML'
provider: bedrock
bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
log:
  level: info
  format: json
YAML
```

Jeden Befehl mit der richtigen Datei ausführen:

```sh
rousseau --config ~/.config/rousseau/chat.yaml chat
rousseau --config ~/.config/rousseau/cron.yaml whatsapp --allow YOUR_JID@s.whatsapp.net
```

## Geteilter vs. partitionierter Zustand

Beide Prozesse zeigen standardmäßig auf denselben SQLite-Session-Store (`~/.local/share/rousseau/sessions.db`) — und das ist üblicherweise das, was Sie möchten, damit die WhatsApp-Bridge und Ihr TUI-Chat Historie teilen.

Um den Zustand vollständig zu partitionieren, überschreiben Sie `state.path` pro Konfiguration:

```yaml
state:
  path: /home/seb/.local/share/rousseau/chat.db
```

Prozessübergreifender SQLite-Zugriff ist sicher wegen WAL-Journaling und dem 15-Sekunden-`busy_timeout`, das von `Open()` in `internal/state/sqlite/store.go` gesetzt wird.

## systemd-Verdrahtung

Zwei Quadlet-Units, eine pro Konfiguration. Das `Exec=` jeder Unit enthält `--config /home/rousseau/.config/rousseau/<name>.yaml`:

```ini
Exec=--config /home/rousseau/.config/rousseau/cron.yaml whatsapp --allow ...
```

Siehe [Bereitstellung](/de/deployment/) für die Basis-Unit.

## Approver-Richtlinien pro Konfiguration

Verschiedene Provider verdienen verschiedene Freigaben. Interaktives `claudecli` kann sicher in `mode: allow_all` bleiben, weil Claude Code seine eigene Per-Call-Freigabe-UI hat. Der Bedrock/Anthropic-Daemon sollte `mode: pattern` mit `default: deny` laufen. Bringen Sie jeden unter seiner eigenen YAML unter.

## Testen

Bestätigen Sie, dass jeder Prozess mit dem richtigen Endpunkt spricht:

```sh
# Interactive shows the claudecli subprocess path in strace / lsof
lsof -c rousseau | grep -E 'claude|CLAUDE'

# Background shows outbound HTTPS to bedrock-runtime.<region>.amazonaws.com
ss -tanp | grep rousseau
```

## Was das NICHT bietet

- **Kein Per-Request-Routing.** Rousseau wird innerhalb eines einzelnen Turns nicht von einem Provider auf einen anderen zurückfallen. Der Ausfall des konfigurierten Providers erscheint als `whatsapp.handler_failed` / `turn.failed` und das Modell wiederholt nicht gegen einen anderen Provider. Das ist ein Roadmap-Punkt.
- **Kein geteiltes Caching.** Der Anthropic-Prompt-Cache (siehe `applyCacheMarkers` in `internal/llm/anthropic/client.go`) ist per Endpunkt. Ein Treffer unter Anthropic direkt ist kein Treffer gegen Bedrock, selbst bei derselben Modellfamilie.

## Verwandt

- [Provider](/de/providers/) — Vergleich aller fünf Provider-Typen.
- [Konfiguration](/de/configuration/) — jeder Knopf.
- [Referenz: Umgebungsvariablen](/de/reference/environment-variables/) — Env-basierte Überschreibungen.
- [Leitfäden: Produktions-Bereitstellung](/de/guides/production-deployment/).
