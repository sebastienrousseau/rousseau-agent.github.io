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
description: "Architecture overview of rousseau-agent: agent loop, transport interface, tool registry, approval policies, SQLite session store, MCP server, cron scheduler, skills loader."
keywords: "architecture, agent loop, session, transport, tool registry, approval, MCP, cron, skills, compression, FTS5"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/concepts/"
subtitle: "Wie Agent-Loop, Transporte und Session-Store zusammenspielen."
tags: "architecture, agent, session, mcp"
title: "Konzepte"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "architecture, agent loop, session, transport, tool registry, approval, MCP, cron, skills, compression, FTS5"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Konzepte"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "concepts"
order: 3
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/concepts/index.html"
item_link: "https://docs.rousseau-agent.dev/concepts/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Konzepte"
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
twitter_description: "Architecture overview of rousseau-agent: agent loop, transport interface, tool registry, approval policies, SQLite session store, MCP server, cron scheduler, skills loader."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Konzepte"
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

## Schichtenarchitektur

```
+---------------------------------------------------------------+
|                             CLI                              |
|  chat  whatsapp  slack  discord  ...  mcp  cron  skills      |
+-------------------------+-------------------------------------+
                          |
+-------------------------v-------------------------------------+
|                          Router                              |
|          (per-JID session, allowlist, dispatch)              |
+-------------+---------------------------+---------------------+
              |                           |
     Transport interface           agent.Agent
     Start / Stop / Deliver        Turn / TurnStream
              |                           |
   +----------+----------+       +--------+--------+
   | 9 concrete adapters |       | Provider iface  |
   +---------------------+       | 5 concrete impls|
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 | Tools Registry  |
                                 | read/write/edit |
                                 | grep/bash + ext |
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 |  State (SQLite) |
                                 | sessions, cron, |
                                 | jidmap, FTS5    |
                                 +-----------------+
```

Das `agent`-Paket hängt nur von Interfaces ab, die `tools` exponiert, von seinen eigenen `Provider`-Typen und von der Standardbibliothek. Konkrete Provider, Stores und Transports hängen von `agent` ab – nie umgekehrt.

## Die Agent-Schleife

`Session → Turn → Provider → Tool-Use-Round-Trip`. Jede Benutzernachricht wird zu einem Aufruf an `Agent.Turn`:

1. **Kompressions-Prüfung.** Der konfigurierte `Compressor` erhält die Gelegenheit, die Sitzung vor dem Turn umzuschreiben. Wenn dies geschieht, wird `Request.CacheableMessages` gesetzt, damit der Zusammenfassungs-Block bereits im nächsten Turn gecacht wird.
2. **Skills-Anhang.** Wenn ein `SkillsProvider` konfiguriert ist, prüft er die letzte Benutzernachricht und gibt Text zum Einfügen in den System-Prompt zurück.
3. **Recall-Anhang.** Wenn ein `RecallProvider` konfiguriert ist, fragt er den FTS5-Index über frühere Sitzungen ab und gibt Text zum Einfügen zurück.
4. **Provider-Aufruf.** Die `Provider.Complete`-Implementierung gibt ein `Response` mit einem `StopReason` zurück.
5. **Tool-Use-Dispatch.** Ist `StopReason == StopToolUse`, wird jeder angeforderte Tool-Aufruf an den `Approver` gesendet. Ablehnungen werden zu `tool_result`-Fehlern, damit das Modell reagieren kann. Erlaubte Aufrufe werden gegen die `Registry` ausgeführt und ihre Ausgaben in der nächsten Iteration abgespielt.
6. **Ende des Turns.** Schleife läuft, bis `StopReason == StopEndTurn` oder `MaxIterations` erreicht wird (Standard 32).

`internal/agent/agent.go` ist die kanonische Referenz.

## Transports

Jeder Transport implementiert `transport.Transport`:

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

`Handler.Handle` empfängt eine `IncomingMessage` (`From`, `Body`, `At`) und gibt den Antworttext zurück. Der `Router` sitzt über dem Transport und ist verantwortlich für Sitzungs-Isolation pro Absender, Durchsetzung der Allowlist und Weiterleitung an den `Agent`.

Keiner der ausgelieferten Transports exponiert standardmässig eine öffentliche HTTP-Oberfläche. Slack nutzt Socket Mode (ausgehender WebSocket). Discord nutzt das Gateway (ausgehender WebSocket). Signal ist ein Subprozess. WhatsApp ist Metas Web-Protokoll über TCP. Matrix, Telegram, iMessage und Email nutzen Polling. SMS ist reine Sende-Richtung, da die Empfangsseite einen Webhook erfordern würde.

## Tool-Registry

`internal/tools` definiert das `Tool`-Interface und eine nebenläufigkeitssichere `Registry`. Eingebaute Tools liegen in `internal/tools/builtin/`:

- `read` – Datei lesen.
- `write` – Datei schreiben.
- `edit` – String ersetzen mit Erzwingung eindeutiger Übereinstimmung, um versehentliche Massenersetzungen zu verhindern.
- `grep` – Textsuche.
- `bash` – Befehlsausführung. **Die tragende Sicherheitsgrenze.**

Jedes Tool deklariert ein strenges JSON-Schema. Das Hinzufügen eines Tools ist ein einzelner `registry.MustRegister(myTool)`-Aufruf beim Wire-up; der Agent-Kern ändert sich nicht.

## Approval-Richtlinien

Jeder Tool-Aufruf durchläuft `Approver.Approve` vor der Ausführung. Drei eingebaute Richtlinien liegen in `internal/agent/approver.go`:

| Modus | Verhalten |
|---|---|
| `allow_all` | Jeder Aufruf läuft. Sinnvoll mit dem `claudecli`-Provider, der seine eigenen Freigaben verwaltet. |
| `deny_all` | Jeder Aufruf wird blockiert. Nützlich für Smoke-Tests und schreibgeschützte Sitzungen. |
| `pattern` | Regex-Allow-/Deny-Regeln pro Tool. Deny schlägt Allow. Nicht passende Anfragen fallen auf `Default` (`allow` oder `deny`) zurück. |

Ablehnungsgründe werden dem Modell als `tool_result`-Fehler zurückgemeldet, damit es reagieren kann, anstatt stillschweigend zu scheitern.

## Session-Store

`internal/state/sqlite/` implementiert das `state.Store`-Interface auf `modernc.org/sqlite` – reines Go, kein libc, kein CGo. Merkmale:

- **WAL-Journaling** mit `busy_timeout=15s`.
- **WAL-Checkpoint bei Close**, damit die primäre Datenbankdatei für Backups konsistent bleibt.
- **FTS5-Recall**-Tabelle indexiert jede Nachricht; der `RecallProvider` führt sitzungsübergreifende Suchen durch.
- **JID-Map**-Tabelle normalisiert WhatsApp-LID-Identitäten auf Telefon-JIDs.
- **Cron-Tabelle** persistiert geplante Jobs über Neustarts hinweg.

## MCP-Server

`internal/mcp/server.go` ist ein JSON-RPC-2.0-Server über stdio, Spec-Revision **2024-11-05**. `rousseau mcp` startet ihn. Registrieren Sie Tools mit `server.Register(mcp.ToolSpec{...})` und lassen Sie einen Client (Claude Desktop, eine IDE-Erweiterung, einen anderen Agenten) sie ansteuern.

Tool-Fehler werden über den `content`-Kanal mit `isError=true` gemeldet, nicht über den JSON-RPC-Fehlerkanal – so erwarten es MCP-Hosts.

## Cron-Scheduler

`internal/cron/scheduler.go` kapselt `robfig/cron/v3`. Jobs werden in SQLite gespeichert und überstehen Neustarts. Jedes Auslösen ruft `Runner.RunOnce(ctx, prompt)` auf (ein einmaliger Agent-Turn gegen eine frische Sitzung), und übergibt die Antwort an `Delivery` – eine transport-agnostische Funktion, die die Nachricht versendet.

Neue Jobs, die per `rousseau cron add` angelegt werden, werden innerhalb des nächsten `PollInterval` aktiv (Standard 60s).

## Skills-Loader

`internal/skills/skills.go` durchsucht `skills_dir` nach `*.md`-Dateien. Jede Datei kann YAML-Frontmatter mit `name`, `description` und `triggers` tragen. Wenn ein Trigger in der aktuellen Benutzernachricht auftaucht, wird der Skill-Body in den System-Prompt dieses Turns eingefügt. Das Format orientiert sich bewusst an der [agentskills.io](https://agentskills.io)-Konvention.

## Kompression

`internal/agent/compressor.go` führt LLM-gestützte Zusammenfassung durch, sobald die Sitzung `TriggerMessages` (Standard 60) überschreitet. Die letzten `KeepRecent`-Nachrichten (Standard 8) bleiben wortgetreu erhalten; alles Ältere wird zu einem Zusammenfassungs-Block verdichtet. Standardmässig deaktiviert, weil ein Abonnement-basiertes `claudecli`-Konto dies selten benötigt; aktivieren Sie es, wenn Sie gegen Pay-per-Token-Provider laufen.

## Wie es weitergeht

- [Konfigurationsreferenz](/de/configuration/) – jedes Feld.
- [Agent-Loop-Referenz](/de/agent-loop/) – Vertrag für die Bibliothekseinbettung.
- [MCP](/de/mcp/) – Client-Wire-up.
