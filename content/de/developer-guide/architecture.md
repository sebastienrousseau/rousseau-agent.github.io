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
description: "Layered architecture of rousseau-agent: agent core, provider / tool / transport interfaces, module boundaries, cyclic-dependency prevention."
keywords: "architecture, layers, agent, provider, transport, tools, module, cyclic dependency"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/developer-guide/architecture/"
subtitle: "Layered architecture and module boundaries."
tags: "developer-guide, architecture, layers"
title: "Architektur"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "architecture, layers, agent, provider, transport, tools, module, cyclic dependency"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Architektur"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 61
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/architecture/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/architecture/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Architektur"
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
twitter_description: "Layered architecture of rousseau-agent: agent core, provider / tool / transport interfaces, module boundaries, cyclic-dependency prevention."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Architektur"
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

## Geschichtetes Bild

```
+--------------------------------------------------------------------+
|                                CLI                                |
|  chat  whatsapp  slack  discord  ...  mcp  cron  skills  doctor   |
+--------------------------------+-----------------------------------+
                                 |
+--------------------------------v-----------------------------------+
|                              Router                               |
|                  (per-JID session, allowlist, dispatch)           |
+---------------+---------------+-------------------+---------------+
                |                                   |
       transport.Transport                    agent.Agent
       Start / Stop / Deliver                Turn / TurnStream
                |                                   |
     +----------+----------+              +---------+-----------+
     |  9 concrete adapters |              |    agent.Provider  |
     +---------------------+              |    5 concrete impls |
                                          +---------+-----------+
                                                    |
                                          +---------v-----------+
                                          |   tools.Registry   |
                                          |   tools.Tool iface |
                                          +---------+-----------+
                                                    |
                                          +---------v-----------+
                                          |     state.Store    |
                                          | SQLite: sessions, |
                                          | jidmap, FTS5, cron|
                                          +---------------------+
```

## Paketrollen

| Paket | Rolle | Hängt ab von |
|---|---|---|
| `internal/agent` | Session, Message, Turn, Agent-Schleife, Schnittstellen Provider / Tool / Approver / Compressor / SkillsProvider / RecallProvider. | stdlib + `internal/tools` (nur Schnittstelle). |
| `internal/tools` | Tool-Schnittstelle + concurrency-sichere Registry. | stdlib. |
| `internal/tools/builtin` | `read`, `write`, `edit`, `grep`, `bash`. | `internal/tools`. |
| `internal/llm/{anthropic,bedrock,claudecli,openai,vertex}` | Konkrete `agent.Provider`-Implementierungen. | `internal/agent`. |
| `internal/state` | Store-Schnittstelle + Summary-Typ. | stdlib. |
| `internal/state/sqlite` | SQLite-Implementierung, WAL, FTS5, Cron-Tabelle, JID-Map. | `internal/state`, `modernc.org/sqlite`. |
| `internal/transport` | Transport-Schnittstelle + Router. | `internal/agent`, `internal/state`. |
| `internal/transport/{whatsapp,signal,...}` | Neun konkrete Adapter. | `internal/transport`, `internal/agent`. |
| `internal/mcp` | JSON-RPC-2.0-Server über stdio, MCP-Spezifikation 2024-11-05. | `internal/agent`, `internal/tools`, `internal/state`. |
| `internal/skills` | agentskills.io-Loader + Komposition. | stdlib. |
| `internal/cron` | robfig/cron/v3-Scheduler-Goroutine. | `internal/state`, `internal/agent`. |
| `internal/config` | Viper-basierter Konfigurations-Loader. | stdlib + `viper`. |
| `internal/cli` | Cobra-Befehlsbaum, Verdrahtung. | Alles darüber. |
| `internal/tui` | Bubble-Tea-Modell. | `internal/agent`, `internal/state`, `bubbletea`. |
| `cmd/rousseau` | Signalbehandlung + `Execute`. | `internal/cli`. |

## Tragende Invariante

**Das `agent`-Paket hängt nur von Schnittstellen ab, die `tools` exponiert, von seinen eigenen `Provider`-Typen und von der Standardbibliothek.**

Alles, was variieren kann – der Provider, der Speicher, der Transport, der Approver, der Compressor – ist als Schnittstelle ausgedrückt, die `agent` gehört. Konkrete Implementierungen importieren `agent`; `agent` importiert sie niemals zurück. Das macht die Schleife testbar ohne live Provider, live Netzwerk oder live Transport.

Wenn Sie merken, dass Sie einen Import von `agent` in `llm/*`, `transport/*` oder `state/sqlite` einfügen, halten Sie an. Die Verdrahtung gehört in `cli`, nicht in `agent`.

## Verhinderung zyklischer Abhängigkeiten

Der Go-Compiler fängt Paket-Import-Zyklen zur Bauzeit ab. Die geschichtete Haltung macht Zyklen fast unmöglich: Jede Schicht kennt nur Schichten darunter. Konkret:

- `cli` darf alles importieren.
- `transport/*`, `llm/*`, `state/*` dürfen `agent`, `tools` und (für Transporte und State) ihre Geschwister-Schnittstellenpakete importieren.
- `agent` darf nur `tools` (Schnittstellen) und die Standardbibliothek importieren.
- `tools` importiert nur die Standardbibliothek.

Zwei strukturelle Regeln verhindern Regressionen:

1. Schnittstellen leben im **Consumer**-Paket. `Provider` ist in `agent` definiert, nicht in `llm/anthropic`. `Tool` ist in `tools` definiert, nicht in `tools/builtin`.
2. Test-Doubles leben neben ihrem Consumer. `agent_test.go` definiert Fake-Provider; `transport/whatsapp/client_test.go` definiert Fake-WebSocket-Verbindungen.

## Provider-Schnittstelle

```go
// Provider drives a single request/response round-trip.
type Provider interface {
    Complete(ctx context.Context, req Request) (Response, error)
}

// StreamingProvider streams response deltas.
type StreamingProvider interface {
    Provider
    CompleteStream(ctx context.Context, req Request) (StreamReader, error)
}
```

Jeder LLM-Adapter erfüllt mindestens `Provider`. Streaming ist Opt-in.

## Tool-Schnittstelle

```go
// Tool is a callable capability the model can request.
type Tool interface {
    Name() string
    Description() string
    InputSchema() map[string]any
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

`InputSchema()` liefert eine JSON-Schema-förmige Map zurück; die Form muss gegen die Tool-Use-Erwartungen des Modells validieren.

## Transport-Schnittstelle

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

`Start` soll blockieren, bis `ctx` abgebrochen oder `Stop` aufgerufen wird. Die Zustellung zurück zum Absender wird intern vom Transport übernommen; Adapter exponieren typischerweise eine `Deliver(ctx, target, body)`-Methode, die vom Cron-Scheduler verwendet wird.

## Approver-Schnittstelle

```go
type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

Wird auf dem Hot Path vor jedem Tool-Aufruf aufgerufen. Siehe [Freigaberichtlinien](/de/user-guide/approval-policies/).

## Compressor und Recall

Zwei weitere Schnittstellen, die die Agent-Schleife bei jedem Turn konsultiert:

```go
type Compressor interface {
    Compress(ctx context.Context, s *Session) (changed bool, err error)
}

type RecallProvider interface {
    SystemAppendix(ctx context.Context, s *Session) string
}
```

Siehe [Kompression + Recall](/de/user-guide/compression-recall/).

## Verdrahtung in `cli`

`internal/cli/chat.go` ist das kanonische Verdrahtungsbeispiel. Es:

1. Lädt die Konfiguration.
2. Baut einen Provider (`buildProvider(cfg)`).
3. Öffnet den SQLite-Speicher (`openStore`).
4. Erstellt eine Tool-Registry und registriert die eingebauten Tools.
5. Baut einen Approver aus `cfg.Agent.Approver`.
6. Baut einen Compressor aus `cfg.Agent.Compression`.
7. Konstruiert `agent.New(...)`.
8. Übergibt den Agent an das Bubble-Tea-Modell.

Jeder andere Befehl folgt demselben Muster – die daemon-spezifischen Teile sind nur der Transport-Konstruktor und dessen `Start`-Aufruf.

## Testmuster

Die Schnittstellen jeder Schicht machen es möglich, isoliert zu testen:

- `agent_test.go` verwendet einen Fake-`Provider`, der vorkonservierte `Response`-Werte zurückliefert.
- `transport/whatsapp/client_test.go` verwendet eine Fake-`WSConn` und einen Fake-`Sender`.
- `state/sqlite/*_test.go` verwendet ein In-Memory-SQLite (`file::memory:`).
- `tools/builtin/*_test.go` verwendet `testing/fstest.MapFS` (wo relevant) und Temp-Dateien.

Siehe [Tests](/de/developer-guide/testing/) für das Injektionsmuster.

## Paketabhängigkeitsgraph

```
cmd/rousseau/               (entry point)
    │
    ▼
internal/cli/               (Cobra command tree)
    │
    ├───▶ internal/config/  (Viper-driven config)
    ├───▶ internal/agent/   (Turn loop, session, provider iface, approver, compressor)
    │        │
    │        └───▶ internal/tools/           (Tool iface + Registry)
    │                    │
    │                    └───▶ internal/tools/builtin/   (read, write, edit, grep, bash)
    │
    ├───▶ internal/llm/anthropic/  ─────┐
    ├───▶ internal/llm/bedrock/    ─────┤
    ├───▶ internal/llm/claudecli/  ─────┼─▶ implements agent.Provider
    ├───▶ internal/llm/openai/     ─────┤
    ├───▶ internal/llm/vertex/     ─────┘
    │
    ├───▶ internal/transport/           (Transport iface + Router)
    │        │
    │        ├───▶ whatsapp/    (whatsmeow)
    │        ├───▶ slack/       (Socket Mode)
    │        ├───▶ discord/     (Gateway v10)
    │        ├───▶ telegram/    (Bot API)
    │        ├───▶ matrix/      (Client-Server)
    │        ├───▶ signal/      (signal-cli JSON-RPC)
    │        ├───▶ email/       (IMAP + SMTP)
    │        ├───▶ sms/         (Twilio / Vonage REST)
    │        └───▶ imessage/    (BlueBubbles)
    │
    ├───▶ internal/cron/        (scheduled prompts)
    ├───▶ internal/mcp/         (JSON-RPC 2.0 server)
    ├───▶ internal/skills/      (agentskills.io loader)
    ├───▶ internal/state/       (Store iface)
    │        │
    │        └───▶ internal/state/sqlite/   (WAL, FTS5)
    │
    └───▶ internal/tui/         (Bubble Tea model)
```

Tragende Eigenschaft: `internal/agent` hängt nur von der Standardbibliothek, `internal/tools` (über seine schmale Schnittstelle) und seinen eigenen Unterpaketen ab. Jeder Provider, jeder Speicher und jeder Transport hängt von `agent` ab – niemals umgekehrt.

## ADR-artige Begründung

Ausgewählte Grenzentscheidungen und warum sie existieren:

### ADR-1: Provider ist eine Schnittstelle, kein Plugin

Wir haben ein Plugin-Modell (`plugin.Open` oder `hashicorp/go-plugin`) in Betracht gezogen. Abgelehnt, weil:

- Statische Builds leichter zu signieren, zu reproduzieren und zu verteilen sind.
- Plugin-ABIs über Go-Versionen hinweg fragil sind.
- Jeder Provider, den wir bedienen wollen, klein genug ist, um vendored zu werden.

Abwägung: Einen Provider hinzuzufügen erfordert einen Rebuild. Akzeptabel.

### ADR-2: Tools leben in `internal/tools/builtin`, nicht in einem `pkg/tools`

Wir haben in Betracht gezogen, die Tool-Registry öffentlich zu exportieren. Abgelehnt, weil:

- `internal/` versehentliche Kopplung entmutigt.
- Aufrufer, die den Agent einbetten, ihre eigenen Tools über die exportierte `Registry`-Schnittstelle registrieren können – sie tun das nur über das `tools`-Paket, statt einen Builtin zu importieren.

Abwägung: Benutzer können `rousseau/tools/builtin` nicht direkt importieren. Sie importieren `rousseau/agent` und `rousseau/tools` und bauen ihre eigene Registry, was `examples/embed-agent` demonstriert.

### ADR-3: SQLite über `modernc.org/sqlite`, nicht `mattn/go-sqlite3`

`modernc.org/sqlite` ist ein Pure-Go-Port; `mattn/go-sqlite3` verwendet cgo. Gewählt, weil:

- `CGO_ENABLED=0` das Binary statisch hält.
- Statische Binaries leichter zu signieren, zu reproduzieren und zu verteilen sind.
- Der Reproducible-Build-CI-Job mit cgo viel schwieriger wäre.

Abwägung: `modernc.org/sqlite` ist bei schreiblastigen Workloads langsamer. Akzeptabel – rousseau ist keine schreiblastige Datenbank.

### ADR-4: MCP-Server ist minimal, nicht das offizielle SDK

Das Paket `internal/mcp/` umfasst ~200 Zeilen selbst geschriebenes JSON-RPC. Gewählt, weil:

- Die MCP-Oberfläche, die rousseau benötigt, klein ist (initialize, tools/list, tools/call, ping, shutdown).
- Das offizielle Go-SDK zum Zeitpunkt der Code-Erstellung noch nicht stabil war.
- Eine kleine Oberfläche den Umstieg schmerzlos macht, wenn das SDK sich stabilisiert.

Abwägung: Einige MCP-Features (Ressourcen, Prompts, List-Changed-Benachrichtigungen) sind Stubs. Roadmap.

### ADR-5: Der `claudecli`-Provider nutzt rousseaus Tool-Registry nicht

Der `claude`-Subprozess führt seine eigene Tool-Use-Schleife aus. Rousseaus Approver kann daher die Tool-Aufrufe nicht sehen. Dies ist eine bewusste Annahme:

- Der `claudecli`-Provider existiert, um Abonnenten die Nutzung ihrer Claude-Code-Auth ohne API-Schlüssel zu ermöglichen.
- Wenn rousseau die Tool-Schleife abfangen würde, müssten wir jede Ein- und Ausgabe durch die Subprozess-Grenze piping – langsam und fehleranfällig.
- Nutzer, die rousseau-seitige Freigabe wollen, verwenden einen Nicht-`claudecli`-Provider.

Abwägung: `claudecli`-Nutzer müssen dem Berechtigungsmodell von `claude` vertrauen. Dokumentiert in [Provider: claudecli](/de/providers/claudecli/).

## Weiter

- [Transport hinzufügen](/de/developer-guide/add-a-transport/) — wie ein neuer Schnittstellen-Implementierer aussieht.
- [Provider hinzufügen](/de/developer-guide/add-a-provider/) — gleiches Muster, andere Schnittstelle.
- [Tool hinzufügen](/de/developer-guide/add-a-tool/) — der kleinste Erweiterungspunkt.

## Verwandte Seiten

- [Konzepte](/de/concepts/) — Übersicht auf hoher Ebene.
- [Agent-Schleife](/de/agent-loop/) — die Laufzeit-Form.
- [MCP](/de/mcp/) — externe Tool-Exposition.
- [Konfiguration](/de/configuration/) — die Konfigurations-Oberfläche, die jede Schnittstelle liest.

## Weiterführende Lektüre

- `README.md` — Repository-Ebenen-Positionierung und Fähigkeitsmatrix.
- `internal/agent/agent.go` — die Kern-Schleife.
- `internal/agent/provider.go` — die `Provider`- und `StreamingProvider`-Schnittstellen.
- `internal/transport/transport.go` — die `Transport`-Schnittstelle.
- `internal/tools/registry.go` — die `Tool`-Schnittstelle und `Registry`.
