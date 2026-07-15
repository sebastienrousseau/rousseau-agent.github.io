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
description: "Wire rousseau-agent to a Slack channel that runs read and grep over the workspace whenever an operator asks."
keywords: "slack, code review, socket mode, read tool, grep tool, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/tutorials/build-a-code-review-bot/"
subtitle: "A Slack channel that lets rousseau review a repo on demand."
tags: "tutorials, slack, code review, socket mode, read, grep"
title: "Tutorial: Code-Review-Bot bauen"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "slack, code review, socket mode, read tool, grep tool, allowlist"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: Code-Review-Bot bauen"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/build-a-code-review-bot/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/build-a-code-review-bot/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: Code-Review-Bot bauen"
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
twitter_description: "Wire rousseau-agent to a Slack channel that runs read and grep over the workspace whenever an operator asks."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: Code-Review-Bot bauen"
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

## Was Sie bauen

Einen privaten Slack-Kanal, in dem Teammitglieder `@rousseau` mit einem Repo-Pfad und einer Frage erwähnen. Rousseau greift auf den Workspace zu, führt `read` und `grep` aus `internal/tools/builtin/` aus und postet eine Antwort mit Zitat-Zeilenreferenzen. Keine öffentliche HTTP-Fläche — Slack Socket Mode treibt alles über einen ausgehenden WebSocket.

Geschätzte Dauer: 20 Minuten, sofern Sie bereits Slack-Admin-Zugriff auf einen Workspace haben.

## Voraussetzungen

- rousseau installiert und ein Provider konfiguriert (siehe [Quickstart](/de/quickstart/)).
- Slack-Workspace-Admin.
- Ein bereits ausgechecktes Repository unter einem Pfad in Ihrem `$HOME` — dieses wird zum "Workspace", auf dem der Bot `read`/`grep` ausführen kann.

## Schritt 1: eine Slack-App anlegen

Slack Socket Mode macht diesen Bot erst möglich: Ihr Daemon öffnet einen ausgehenden WebSocket zu Slack, kein Ingress erforderlich.

1. Zu <https://api.slack.com/apps> gehen und eine neue App **from scratch** anlegen.
2. Unter **Socket Mode** aktivieren und ein **App-Level-Token** mit `connections:write` erzeugen. Den Wert `xapp-...` kopieren.
3. Unter **OAuth & Permissions** diese **Bot Token Scopes** hinzufügen:
   - `chat:write`
   - `app_mentions:read`
   - `channels:history` (oder `groups:history` für private Kanäle)
4. App im Workspace installieren. Das **Bot User OAuth Token** — den `xoxb-...`-Wert — kopieren.
5. Unter **Event Subscriptions** Events aktivieren und den Bot für `app_mention` und `message.channels` (oder `message.groups`) subscriben.
6. Bot in den Review-Kanal einladen: `/invite @rousseau`.

## Schritt 2: rousseau konfigurieren

In `~/.config/rousseau/config.yaml` einfügen. Die relevanten Felder stammen aus `SlackConfig` in `internal/config/config.go`:

```yaml
provider: claudecli           # or anthropic — whatever you set in Quickstart

slack:
  app_token:  xapp-1-…
  bot_token:  xoxb-…
  bot_user_id: U0ROUSSEAU     # from https://api.slack.com/methods/auth.test
  reply_header: "*rousseau-agent*\n\n"
  allowlist:
    - U01ABC…                 # your Slack user IDs

agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
    # no bash, no write, no edit — read-only reviewer
```

Die `allowlist` beschränkt, von wem der Router Nachrichten annimmt. Der Router in `internal/transport/router.go` emittiert `transport.rejected` für jeden anderen Absender.

## Schritt 3: die Bridge starten

```sh
rousseau slack \
  --app-token "$SLACK_APP_TOKEN" \
  --bot-token "$SLACK_BOT_TOKEN" \
  --bot-user-id "$SLACK_BOT_USER_ID"
```

`--bot-user-id` verhindert, dass der Bot auf seine eigenen Nachrichten antwortet. Strukturierte Logs aus `internal/transport/slack/client.go` zeigen:

```
INFO slack.started
INFO slack.incoming from=U01ABC channel=C01REVIEW text="…"
INFO tool.execute name=read id=t_1
INFO tool.execute name=grep id=t_2
```

## Schritt 4: ausprobieren

Im Review-Kanal:

```
@rousseau look under /home/seb/repos/acme-api and tell me
where request logging is set up
```

Der `claudecli`-Provider (oder Anthropic — je nach Ihrer Wahl) ruft `read` und `grep` aus `internal/tools/builtin/` gegen den Workspace-Bind-Mount auf. Da der Approver im Modus `pattern` läuft und ausschließlich `read` und `grep` allowlisted sind, kann das Modell weder schreiben noch eine Shell öffnen — selbst wenn ein kompromittierter Prompt dies verlangen würde.

## Schritt 5: härten

Approver im Modus Pattern arbeiten mit **Regex über den JSON-Tool-Input**. Um `read` und `grep` auf einen bestimmten Projekt-Tree zu beschränken:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: "\"path\":\"/home/seb/repos/acme-api/[^\"]*\""}
      - {tool: grep, match: "\"path\":\"/home/seb/repos/acme-api\""}
```

Der vollständige Durchlauf zu `default: deny` + Audit steht im [Tutorial: Den Approver härten](/de/tutorials/harden-approver-policy/).

## Deployment unter systemd

Alles jenseits einer Laptop-Session sollte über die Podman-Quadlet-Unit unter `docker/rousseau-agent.container` laufen — `Exec=whatsapp --allow …` gegen `Exec=slack --app-token … --bot-token …` austauschen. Die vollständige Unit siehe [Deployment](/de/deployment/).

## Verwandt

- [Transports: Slack](/de/transports/slack/)
- [Benutzerhandbuch: Genehmigungsrichtlinien](/de/user-guide/approval-policies/)
- [Benutzerhandbuch: Tools](/de/user-guide/tools/)
- [Tutorial: Den Approver härten](/de/tutorials/harden-approver-policy/)
