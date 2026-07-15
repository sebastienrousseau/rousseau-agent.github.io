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
description: "MCP resources exposed by rousseau's stdio server today (none) and the roadmap for sessions-as-resources."
keywords: "mcp, resources, roadmap, sessions, resources/list"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/mcp/exposed-resources/"
subtitle: "What resources rousseau exposes today, and what is planned."
tags: "mcp, resources, roadmap"
title: "MCP: bereitgestellte Ressourcen"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, resources, roadmap, sessions, resources/list"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP: bereitgestellte Ressourcen"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 73
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/exposed-resources/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/exposed-resources/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP: bereitgestellte Ressourcen"
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
twitter_description: "MCP resources exposed by rousseau's stdio server today (none) and the roadmap for sessions-as-resources."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP: bereitgestellte Ressourcen"
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

## Aktueller Status

Rousseaus MCP-Server (`internal/mcp/server.go`) deklariert nur die `Tools`-Capability. Er liefert eine leere Liste bei `resources/list` zurück:

```
MethodResourcesList → okResponse(env.ID, map[string]any{"resources": []any{}})
```

Die Absicht ist bewusst. Jeder Use Case, der wie eine MCP-Ressource aussehen würde – eine gespeicherte Sitzung, eine Cron-Job-Beschreibung – wird heute über ein Tool exponiert (`rousseau_read_session`, `rousseau_cron_list`), damit der Host genau die Daten anfordern kann, die er benötigt, wenn er sie benötigt, statt jede Sitzung vorab aufzulisten.

## Warum heute keine Ressourcen

MCP-Ressourcen glänzen, wenn ein Host eine überschaubare, wohldefinierte Menge an URIs (Dateien, Seiten) aufzählen und lazy dereferenzieren will. Rousseaus Sitzungsspeicher kann zu Tausenden von Zeilen anwachsen; das Auflisten jeder Sitzung bei jedem `resources/list`-Aufruf würde den Kontext des Hosts sprengen. Die Tool-Oberfläche (search / list / read) ist eine bessere Form für Zustand hoher Kardinalität.

## Roadmap

Zwei Kandidaten, die es wert sind, als MCP-Ressourcen exponiert zu werden, sobald die MCP-Spezifikation paginierte Ressourcen-Aufzählung robust unterstützt:

### Kandidat: `rousseau://sessions/<id>`

Jede rousseau-Sitzung als Ressource. URIs würden so aussehen:

```
rousseau://sessions/1a2b3c4d-…
```

Dereferenzierung würde dasselbe Transkript zurückgeben, das `rousseau_read_session` heute liefert. Dies würde es dem Host ermöglichen, eine bestimmte Sitzung als vollwertigen Bürger an eine Konversation anzuhängen ("Sitzung 1a2b3c… anhängen", Drag-and-Drop), anstatt das Modell daran erinnern zu müssen, das Tool aufzurufen.

Voraussetzung: Eine Ressourcenliste müsste paginiert werden. Aktuelle Versionen der MCP-Spezifikation schlagen Cursor-basierte Paginierung vor; sobald diese erscheint und Hosts sie implementieren, wird dies umsetzbar.

### Kandidat: `rousseau://cron/<name>`

Jeder Cron-Job als Ressource. Nur-Lese-Inspektion des Prompts, des Zeitplans, des Zustellziels und des letzten Ausführungszeitstempels. Kleine Liste – wahrscheinlich sicher heute aufzuzählen, aber nicht wert, separat von `rousseau_cron_list` exponiert zu werden, bis sich die Sessions-als-Ressourcen-Form bewährt hat.

## Prompts-Capability

Ebenfalls heute nicht exponiert. `MethodPromptsList` liefert `{"prompts": []any{}}` in `internal/mcp/server.go` `dispatch`. Rousseau hat keine kuratierte Prompt-Bibliothek zum Exponieren; der Skills-Mechanismus (`internal/skills/skills.go`) ist das äquivalente interne Konzept und wird derzeit nicht über MCP zugänglich gemacht.

Wenn die Skills-Roadmap in teilbare Prompts konvergiert, ist deren Exposition als MCP-Prompts der natürliche nächste Schritt. Siehe [Skills](/de/skills/).

## Wie Sie die Lücke heute umgehen

Wenn Ihr MCP-Host Ressourcen für eine bestimmte UI-Affordanz benötigt (z. B. Drag-and-Drop einer Sitzung), ist die Umgehung:

1. Bitten Sie den Host, zu Beginn des Chats `rousseau_list_sessions` aufzurufen.
2. Kopieren Sie die Sitzungs-ID, auf die Sie sich beziehen möchten.
3. Rufen Sie `rousseau_read_session` mit dieser ID auf.

Nicht so ergonomisch wie native Ressourcendereferenzierung, aber funktional äquivalent.

## Eine Ressourcen-Oberfläche anfordern

Nicht jeder Operator benötigt Ressourcen über MCP. Falls Ihr Team dies tut, ist der konstruktive Weg, ein Issue zu eröffnen mit:

- Dem spezifischen MCP-Host, mit dem Sie integrieren.
- Der benutzerseitigen Aktion, die mit Ressourcen angenehmer wäre.
- Groben Traffic-Erwartungen (wie viele Sitzungen, wie oft).

## Verwandt

- [MCP](/de/mcp/) — die Dachreferenz.
- [MCP: Exponierte Tools](/de/mcp/exposed-tools/) — was heute exponiert wird.
- [MCP: Kompatibilität](/de/mcp/compatibility/) — getestete Clients.
- [Skills](/de/skills/) — das interne Konzept, das zu MCP-Prompts werden könnte.
