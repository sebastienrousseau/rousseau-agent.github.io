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
description: "rousseau-agent's MCP server exposes its tools and sessions over stdio JSON-RPC. Compatible with Claude Desktop and any MCP host."
keywords: "MCP, Model Context Protocol, JSON-RPC, stdio, Claude Desktop, tools, sessions"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/mcp/"
subtitle: "JSON-RPC 2.0 über stdio, Spec-Revision 2024-11-05."
tags: "MCP, reference"
title: "MCP-Server"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "MCP, Model Context Protocol, JSON-RPC, stdio, Claude Desktop, tools, sessions"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP-Server"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 21
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "MCP-Server"
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
twitter_description: "rousseau-agent's MCP server exposes its tools and sessions over stdio JSON-RPC. Compatible with Claude Desktop and any MCP host."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP-Server"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Das vollständige JSON-RPC-2.0-Wire-Format, das rousseau spricht, jede vom MCP-Server von rousseau implementierte Methode mit Beispiel-Request/Response-Paaren, die Semantik der Fehlercodes und wie Claude Desktop / Cursor / IDE-MCP-Hosts konfiguriert werden, um den Server zu erreichen. Lesen Sie <code>internal/mcp/protocol.go</code> und <code>internal/mcp/server.go</code> begleitend zu dieser Seite.</p></aside>

## Wire-Format

`rousseau mcp` startet einen MCP-Server, der JSON-RPC 2.0 über stdio spricht, gemäß der Spezifikationsrevision **2024-11-05** des [Model Context Protocol](https://modelcontextprotocol.io) (deklariert in `ProtocolVersion` in `internal/mcp/protocol.go`).

- Eine Anfrage pro Zeile auf stdin (`bufio.Scanner` liest bis zu 8 MiB pro Zeile).
- Eine Antwort pro Zeile auf stdout (`json.NewEncoder` gibt zeilenweise getrenntes JSON aus).
- Der Server blockiert, bis stdin geschlossen oder `ctx` abgebrochen wird.

### JSON-RPC-2.0-Envelope

Jede Anfrage, Notification und Antwort verwendet diesen Envelope (aus `internal/mcp/protocol.go`, Zeile 38):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

Welche Felder vorhanden sind, hängt von der Envelope-Art ab:

| Feld | Request | Notification | Response |
|---|:---:|:---:|:---:|
| `jsonrpc` | immer `"2.0"` | immer `"2.0"` | immer `"2.0"` |
| `id` | erforderlich | fehlt | aus dem Request gespiegelt |
| `method` | erforderlich | erforderlich | fehlt |
| `params` | optional | optional | fehlt |
| `result` | fehlt | fehlt | nur bei Erfolg |
| `error` | fehlt | fehlt | nur bei Fehler |

Notifications tragen keine `id` und erhalten keine Antwort. rousseau empfängt nur eine Notification (`notifications/initialized`), die stillschweigend akzeptiert wird.

### Methoden-Referenz

`Server.dispatch` von Rousseau (`internal/mcp/server.go`, Zeile 112) routet diese Methoden:

| Methode | Zweck | Antwort |
|---|---|---|
| `initialize` | Handshake. Client deklariert Protokollversion und Capabilities. | `InitializeResult` |
| `notifications/initialized` | Client bestätigt Bereitschaft. | (Notification, keine Antwort) |
| `ping` | Liveness-Probe. | `{}` |
| `tools/list` | Registrierte Tools aufzählen. | `ToolsListResult` |
| `tools/call` | Tool aufrufen. | `ToolsCallResult` |
| `resources/list` | Platzhalter. Liefert derzeit `{ "resources": [] }`. | `{"resources": []}` |
| `prompts/list` | Platzhalter. Liefert `{ "prompts": [] }`. | `{"prompts": []}` |
| `shutdown` | Vom Client initiiertes Herunterfahren. | `{}` |

<aside class="admonition" data-type="note"><span class="admonition-title">Fehlende Methoden</span><p><code>resources/list</code> und <code>prompts/list</code> liefern leere Arrays zurück, damit Hosts, die diese abfragen, keinen Fehler bekommen. Vollständige Ressourcen-/Prompt-Unterstützung steht auf der Roadmap — siehe <code>docs/GAP_ANALYSIS_2026.md</code>.</p></aside>

## Request/Response-Beispiele

### 1. `initialize`

Client sendet:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"claude-desktop","version":"0.7.0"}}}
```

Server antwortet:

```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","serverInfo":{"name":"rousseau","version":"0.6.0"},"capabilities":{"tools":{"listChanged":false}}}}
```

`listChanged: false`, weil das Tool-Set von rousseau beim Prozessstart statisch ist — kein Hinzufügen/Entfernen zur Laufzeit.

### 2. `tools/list`

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
```

Der Server antwortet mit den registrierten Tools in Einfügereihenfolge:

```json
{"jsonrpc":"2.0","id":2,"result":{"tools":[
  {"name":"read","description":"Read a file...","inputSchema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
  {"name":"grep","description":"Search for a regex...","inputSchema":{"type":"object","properties":{"pattern":{"type":"string"},"path":{"type":"string"}},"required":["pattern"]}},
  {"name":"bash","description":"Execute a shell command...","inputSchema":{"type":"object","properties":{"command":{"type":"string"}},"required":["command"]}}
]}}
```

### 3. `tools/call`

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"read","arguments":{"path":"/etc/hostname"}}}
```

Erfolg:

```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"my-host.example.com\n"}]}}
```

Fehler auf Handler-Ebene (als Content zurückgeliefert, nicht als JSON-RPC-Fehler — dies ist MCP-Konvention):

```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"read: open /nope: no such file or directory"}],"isError":true}}
```

### 4. `ping`

```json
{"jsonrpc":"2.0","id":4,"method":"ping"}
```

```json
{"jsonrpc":"2.0","id":4,"result":{}}
```

## Fehlercodes

Rousseau verwendet den Standard-Fehlerbereich von JSON-RPC 2.0 plus eine MCP-Erweiterung:

| Code | Konstante | Bedeutung | Wann emittiert |
|---|---|---|---|
| -32700 | `CodeParseError` | Ungültiges JSON im Envelope. | `json.Unmarshal` des Envelope schlug fehl. |
| -32600 | `CodeInvalidRequest` | Envelope-Form ist falsch. | Feld `jsonrpc` ist nicht `"2.0"`. |
| -32601 | `CodeMethodNotFound` | Methode nicht implementiert. | Dispatch fiel in den Default-Fall. |
| -32602 | `CodeInvalidParams` | Params konnten nicht decodiert werden. | `params` ließ sich nicht in die erwartete Form deserialisieren. |
| -32603 | `CodeInternalError` | Fehler beim Marshalling der Antwort. | Selten — deutet auf einen Bug hin. |
| -32000 | `CodeToolNotFound` | Tool-Name ist nicht registriert. | `tools/call` mit unbekanntem `name`. |

<aside class="admonition" data-type="warning"><span class="admonition-title">Tool-Fehler vs. JSON-RPC-Fehler</span><p>Fehler auf Handler-Ebene — ein <code>bash</code>-Kommando, das mit Non-Zero endete, ein <code>read</code> auf eine fehlende Datei — werden über <code>result.content</code> mit <code>isError: true</code> zurückgeliefert, NICHT über das JSON-RPC-Feld <code>error</code>. Nur Fehler auf Protokollebene nutzen <code>error</code>. Hosts, die beide Kanäle als gleichwertig behandeln, klassifizieren behebbare Fehler falsch.</p></aside>

## Was exponiert wird

Zwei Flächen:

- **Tools.** Jede vor `Serve` registrierte `mcp.ToolSpec` wird in `tools/list` beworben und ist über `tools/call` aufrufbar. rousseau verdrahtet dieselben Tool-Implementierungen, die auch der lokale Agent-Loop nutzt: `read`, `write`, `edit`, `grep`, `bash`.
- **Sessions.** Der SQLite-Session-Store von rousseau wird exponiert, sodass ein MCP-Host frühere Konversationen auflisten und lesen kann. `resources/list` liefert einen Eintrag pro Session.

Tool-Fehler werden über den `content`-Kanal mit `isError=true` gemeldet, nicht über den JSON-RPC-Fehlerkanal. Dies ist MCP-Konvention.

## Client-Konfiguration — Claude Desktop

In `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) oder das plattform-äquivalente Pendant eintragen:

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "rousseau",
      "args": ["mcp"],
      "env": {
        "HOME": "/Users/you"
      }
    }
  }
}
```

Claude Desktop neu starten. `rousseau` erscheint in der Tools-Palette; jedes registrierte Tool ist aufrufbar.

Für ein in ein Podman-Image gebautes rousseau lautet der Eintrag:

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "podman",
      "args": [
        "run", "--rm", "-i",
        "-v", "/Users/you/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z",
        "localhost/rousseau-agent:local",
        "mcp"
      ]
    }
  }
}
```

Das State-Verzeichnis per Bind-Mount einhängen, damit der MCP-Host dieselben Sessions sieht wie der Daemon.

## Ein eigenes Tool registrieren

Einbetten des MCP-Servers in ein eigenes Binary:

```go
srv := mcp.NewServer("rousseau", "0.1.0", logger)

srv.MustRegister(mcp.ToolSpec{
    Name:        "count_files",
    Description: "Count files under a path.",
    InputSchema: json.RawMessage(`{
      "type": "object",
      "properties": {"path": {"type": "string"}},
      "required": ["path"]
    }`),
    Handler: func(ctx context.Context, args json.RawMessage) ([]mcp.Content, error) {
        var in struct{ Path string }
        if err := json.Unmarshal(args, &in); err != nil {
            return nil, fmt.Errorf("bad input: %w", err)
        }
        // ... count files ...
        return []mcp.Content{{Type: "text", Text: fmt.Sprintf("%d", n)}}, nil
    },
})

_ = srv.Serve(ctx, os.Stdin, os.Stdout)
```

Doppelte Registrierungen liefern einen Fehler zurück; `MustRegister` panict bei Duplikaten (vorgesehen für die Verdrahtung in `main`).

## Nebenläufigkeit

`Serve` darf nebenläufig auf unabhängigen Transports aufgerufen werden (stdin/stdout für den MCP-Host, plus optional ein Steuerkanal). Die Tool-Map des Servers ist durch eine RWMutex geschützt; die Handler-Ausführung wird nicht serialisiert — Implementierungen müssen nebenläufigkeitssicher sein.

## Debugging

Jeder Request-/Response-Envelope wird standardmäßig auf Level `debug` geloggt. Aktivieren mit:

```yaml
log:
  level: debug
  format: text
```

Or:

```sh
ROUSSEAU_LOG_LEVEL=debug rousseau mcp 2>/tmp/mcp.log
```

Der MCP-Host konsumiert stdout; den Log-Stream auf stderr halten.

## Troubleshooting

### Claude Desktop / Cursor zeigt die rousseau-Tools nie an

Fast immer ein Verdrahtungsfehler, kein Problem von rousseau. Prüfen: (1) `command` und `args` in der Host-Konfiguration rufen `rousseau mcp` auf (nicht `rousseau chat`); (2) die Konfigurationsdatei wurde gespeichert und der Host neu gestartet; (3) `rousseau mcp </dev/null` in einer Shell stürzt nicht ab — falls doch, zuerst das beheben.

### `parse error` auf die allererste Nachricht

Der Host sendet kein zeilengetrenntes JSON. Einige frühe MCP-Implementierungen senden geframte Nachrichten (`Content-Length: N\r\n\r\n<body>`); rousseau erwartet `\n`-getrennt. Auf einen Host-Build aktualisieren, der stdio-Framing verwendet (alle aktuellen großen Hosts tun das).

### `method not found: <foo>`

Der Host ruft eine Methode auf, die rousseau nicht implementiert. Leere `resources/list` und `prompts/list` werden als No-Ops für die üblichen Probes bereitgestellt; alles Weitere liefert `-32601`. Die vollständige Methodenliste steht in `dispatch()` in `internal/mcp/server.go`.

### Tool-Aufrufe gelingen, der Host meldet sie aber als Fehler

Der Tool-Handler hat den Fehler auf die falsche Weise zurückgegeben. Handler sollten `[]Content{{Type: "text", Text: err.Error()}}, err != nil` zurückgeben — rousseau fängt den Fehler ab und verpackt ihn in `isError: true`. Den Fehler nicht über den JSON-RPC-`error`-Kanal zurückgeben, sofern es sich nicht um einen Protokollfehler handelt.

### Container-basiertes MCP scheitert mit `permission denied` am State-Verzeichnis

Der `podman run`-Aufruf aus Claude Desktop muss ein `-v` für das State-Verzeichnis mit dem richtigen SELinux-Label enthalten. `:Z` (privat) verwenden, sofern der Container nicht mit anderen Podman-Workloads geteilt wird. Zusätzlich prüfen, dass die Host-UID innerhalb des Containers der Dateibesitzstruktur entspricht.

## Verwandte Seiten

- [MCP: Exponierte Tools](/de/mcp/exposed-tools/) — das Tool-Set, das rousseau veröffentlicht.
- [MCP: Exponierte Ressourcen](/de/mcp/exposed-resources/) — Session-Enumeration und -Lesen.
- [MCP: Kompatibilität](/de/mcp/compatibility/) — getestete Host-Matrix.
- [Tutorials: Tools über MCP exponieren](/de/tutorials/expose-tools-via-mcp/) — vollständiger End-to-End-Durchlauf.
- [Agent-Loop](/de/agent-loop/) — wie dieselben Tools intern in rousseau verwendet werden.

## Weiterführende Literatur

- `internal/mcp/protocol.go` — Envelope, Methodennamen, Fehlercodes.
- `internal/mcp/server.go` — `Serve`, `dispatch`, Tool-Registry.
- `internal/mcp/tools.go` — Helfer zum Registrieren der eingebauten Tools von rousseau.
- `internal/cli/mcp.go` — die Verdrahtung des `rousseau mcp`-Befehls.
- [Model-Context-Protocol-Spezifikation](https://modelcontextprotocol.io) — externe Referenz.
