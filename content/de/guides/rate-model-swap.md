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
description: "Hot-swap the underlying model mid-session by editing config.yaml and restarting the daemon — the SQLite session store survives."
keywords: "model swap, hot swap, mid-session, restart, session store, sonnet, opus, haiku"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/guides/rate-model-swap/"
subtitle: "Swap Sonnet for Opus mid-session; the session store survives the restart."
tags: "guides, model, swap, restart, session"
title: "Leitfaden: Modell im Betrieb wechseln"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "model swap, hot swap, mid-session, restart, session store, sonnet, opus, haiku"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: Modell im Betrieb wechseln"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/rate-model-swap/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/rate-model-swap/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: Modell im Betrieb wechseln"
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
twitter_description: "Hot-swap the underlying model mid-session by editing config.yaml and restarting the daemon — the SQLite session store survives."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Leitfaden: Modell im Betrieb wechseln"
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

## Warum es funktioniert

Rousseau liest seinen Provider und sein Modell einmal beim Prozessstart aus `config.yaml` (`config.Load` in `internal/config/config.go`). Der Sitzungszustand lebt in SQLite. Das Modell zu wechseln bedeutet, die Konfiguration zu bearbeiten, den Daemon neu zu starten und die nächste eingehende Nachricht vom neuen Modell verarbeiten zu lassen — während jede Sitzung, an der das vorherige Modell teilnahm, in `sessions.db` intakt bleibt.

Nichts am Session-Store ist an ein bestimmtes Modell gebunden. Die Spalte `payload` (`internal/state/sqlite/schema.sql`) ist ein einfaches JSON-Blob von `agent.Session`; Rolle, Content, Tool-Use-Blöcke. Jedes Modell, das die Anthropic-Content-Block-Konvention spricht (oder über die SDK-Adapter in `internal/llm/*/client.go` angepasst wird), kann dort weitermachen, wo das vorherige aufgehört hat.

## Wechsel innerhalb desselben Providers

Der einfache Fall. Bearbeiten Sie das Modell-Feld:

```yaml
# was:
anthropic:
  model: claude-sonnet-4-6

# now:
anthropic:
  model: claude-opus-4-6
```

Neu starten:

```sh
systemctl --user restart rousseau-agent
# or, if you're running rousseau chat interactively, quit and relaunch
```

Senden Sie die nächste Nachricht. Die Antwort kommt von Opus; der Sitzungskontext ist unverändert.

## Wechsel über Provider hinweg

Etwas aufwendiger, weil Content-Block-Formen variieren. Die Adapter von rousseau (`internal/llm/anthropic/client.go`, `internal/llm/openai/client.go`) reisen `agent.Message`-Werte bei jedem Turn durch die nativen Typen des SDK. Das bedeutet:

- **`claudecli` → `anthropic`** — sauberer Wechsel. Beide nutzen dieselbe Content-Block-Form.
- **`claudecli` → `bedrock` / `vertex`** — sauberer Wechsel. Anthropic-on-Bedrock und Anthropic-on-Vertex sprechen dasselbe Messages-Format.
- **Anthropic-Familie → `openai` / `openrouter` / `ollama`** — Tool-Use-Blöcke werden in das OpenAI-Function-Call-Format umgeformt. Vorherige tool_use-/tool_result-Paare in der Sitzung durchlaufen den Adapter. Sollte für Text nahtlos sein; Randfälle (Multi-Tool-Use in einem einzelnen Turn, Streaming-Partials) können anders gerendert werden.

Wenn die Sitzung viel Tool-Use-Historie hat und Sie Providerfamilien wechseln, testen Sie zuerst mit einer frischen Sitzung.

## Deployment-Provider wechseln, ohne den Zustand zu berühren

Derselbe Session-Store, andere Daemon-Konfiguration:

```sh
cp ~/.config/rousseau/config.yaml ~/.config/rousseau/config.yaml.bak
$EDITOR ~/.config/rousseau/config.yaml   # change provider + model
systemctl --user restart rousseau-agent
```

`state.path` hat sich nicht geändert, sodass die JID→Session-Zuordnung (`jid_sessions`-Tabelle in `internal/state/sqlite/jidmap.go`) für jeden WhatsApp-/Slack-/Matrix-Absender weiterhin auf dieselbe Konversationshistorie zeigt.

## Was erhalten bleibt

| Zustand | Überlebt Neustart | Anmerkungen |
|---|---|---|
| Sitzungs-Transkripte | Ja | `sessions`-Tabelle. |
| FTS5-Recall-Index | Ja | `sessions_fts`-Virtual-Table. Beim Backfill re-tokenisiert. |
| JID → Session-Zuordnung | Ja | `jid_sessions`-Tabelle. |
| Cron-Jobs | Ja | `cron_jobs`-Tabelle. |
| WhatsApp-Gerätepairing | Ja | `whatsapp.db` (separate Datei). |
| Anthropic-Prompt-Cache-Treffer | **Nein** | Der Cache ist per Endpunkt. Ein neues Modell oder ein neuer Endpunkt startet kalt. |

## Was verloren geht

Die Anthropic-Prompt-Cache-Marker (`applyCacheMarkers` in `internal/llm/anthropic/client.go`) leben im ephemeren Cache des Modells — sie persistieren nicht über Modell- oder Provider-Neustarts hinweg. Die nächsten paar Turns nach einem Wechsel zahlen volle Input-Tokens; nachfolgende Turns bauen den Cache neu auf. Das ist für die Kostenplanung erwähnenswert, nicht aber für die Korrektheit.

## Wann wechseln vs. neu beginnen

An Ort und Stelle wechseln, wenn:

- Die Sitzung erhaltenswert ist und der Inhalt textlastig ist.
- Die Modelle in derselben Familie sind (beide Anthropic oder via Bedrock/Vertex).
- Sie einen einmaligen Cache-Miss akzeptieren.

Neu beginnen, wenn:

- Die Sitzung veralteten Kontext enthält, den ein klügeres Modell nicht verfolgen soll.
- Sie Providerfamilien wechseln und deterministisches Verhalten möchten.
- Die Token-Zahl ohnehin am Komprimierungs-Trigger ist — komprimieren und wechseln in einem Zug.

## Testen nach einem Wechsel

```sh
rousseau session list | head -3
rousseau session show <id> | tail -20
# in TUI or via a transport:
> what did we just decide about X?
```

Wenn die Antwort die vorherige Konversation kohärent referenziert, funktioniert der Wechsel. Wenn das Modell sich für „fehlenden Kontext" entschuldigt oder sich wiederholt, verliert der Adapter-Roundtrip möglicherweise Tool-Use-Metadaten — melden Sie einen Bug oder fallen Sie zurück auf das vorherige Modell.

## Verwandt

- [Provider](/de/providers/) — jeder unterstützte Provider.
- [Konfiguration](/de/configuration/) — die exakten Feldnamen.
- [Leitfäden: Rate-Limits](/de/guides/rate-limits/) — Cache-Marker-Diskussion.
- [Leitfäden: Sitzungsverwaltung](/de/guides/session-management/) — vollständiger Lebenszyklus.
