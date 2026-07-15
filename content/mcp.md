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
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "en-GB"
locale: "en_GB"
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
permalink: "https://docs.rousseau-agent.dev/mcp/"
subtitle: "JSON-RPC 2.0 over stdio, spec revision 2024-11-05."
tags: "MCP, reference"
title: "MCP Server"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "MCP, Model Context Protocol, JSON-RPC, stdio, Claude Desktop, tools, sessions"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP Server"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 21
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "MCP Server"
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
twitter_title: "MCP Server"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>The full JSON-RPC 2.0 wire format rousseau speaks, every method rousseau's MCP server implements with example request/response pairs, error-code semantics, and how to configure Claude Desktop / Cursor / IDE MCP hosts to reach the server. Read <code>internal/mcp/protocol.go</code> and <code>internal/mcp/server.go</code> alongside this page.</p></aside>

## Wire format

`rousseau mcp` starts an MCP server that speaks JSON-RPC 2.0 over stdio, per the [Model Context Protocol](https://modelcontextprotocol.io) specification revision **2024-11-05** (declared in `ProtocolVersion` in `internal/mcp/protocol.go`).

- One request per line on stdin (`bufio.Scanner` reads up to 8 MiB per line).
- One response per line on stdout (`json.NewEncoder` emits newline-delimited JSON).
- The server blocks until stdin closes or `ctx` is cancelled.

### JSON-RPC 2.0 envelope

Every request, notification, and response uses this envelope (from `internal/mcp/protocol.go` line 38):

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

Fields present depend on the envelope kind:

| Field | Request | Notification | Response |
|---|:---:|:---:|:---:|
| `jsonrpc` | always `"2.0"` | always `"2.0"` | always `"2.0"` |
| `id` | required | absent | echoed from the request |
| `method` | required | required | absent |
| `params` | optional | optional | absent |
| `result` | absent | absent | success only |
| `error` | absent | absent | failure only |

Notifications carry no `id` and receive no response. rousseau only receives one notification (`notifications/initialized`), which is silently accepted.

### Method reference

Rousseau's `Server.dispatch` (`internal/mcp/server.go` line 112) routes these methods:

| Method | Purpose | Response |
|---|---|---|
| `initialize` | Handshake. Client declares protocol version and capabilities. | `InitializeResult` |
| `notifications/initialized` | Client confirms it is ready. | (notification, no response) |
| `ping` | Liveness probe. | `{}` |
| `tools/list` | Enumerate registered tools. | `ToolsListResult` |
| `tools/call` | Invoke a tool. | `ToolsCallResult` |
| `resources/list` | Placeholder. Returns `{ "resources": [] }` today. | `{"resources": []}` |
| `prompts/list` | Placeholder. Returns `{ "prompts": [] }`. | `{"prompts": []}` |
| `shutdown` | Client-initiated shutdown. | `{}` |

<aside class="admonition" data-type="note"><span class="admonition-title">Missing methods</span><p><code>resources/list</code> and <code>prompts/list</code> return empty arrays so hosts that probe them do not error. Full resource/prompt support is on the roadmap — see <code>docs/GAP_ANALYSIS_2026.md</code>.</p></aside>

## Request/response examples

### 1. `initialize`

Client sends:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"claude-desktop","version":"0.7.0"}}}
```

Server replies:

```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","serverInfo":{"name":"rousseau","version":"0.6.0"},"capabilities":{"tools":{"listChanged":false}}}}
```

`listChanged: false` because rousseau's tool set is static at process start — no runtime add/remove.

### 2. `tools/list`

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
```

Server replies with the registered tools in insertion order:

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

Success:

```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"my-host.example.com\n"}]}}
```

Handler-level failure (surfaced as content, not as a JSON-RPC error — this is MCP convention):

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

## Error codes

Rousseau uses the standard JSON-RPC 2.0 error range plus one MCP extension:

| Code | Constant | Meaning | When emitted |
|---|---|---|---|
| -32700 | `CodeParseError` | Invalid JSON in the envelope. | Envelope failed `json.Unmarshal`. |
| -32600 | `CodeInvalidRequest` | Envelope shape is wrong. | `jsonrpc` field is not `"2.0"`. |
| -32601 | `CodeMethodNotFound` | Method not implemented. | Dispatch fell through to the default case. |
| -32602 | `CodeInvalidParams` | Params failed to decode. | `params` did not unmarshal into the expected shape. |
| -32603 | `CodeInternalError` | Something went wrong marshalling the response. | Rare — indicates a bug. |
| -32000 | `CodeToolNotFound` | Tool name is not registered. | `tools/call` with an unknown `name`. |

<aside class="admonition" data-type="warning"><span class="admonition-title">Tool errors vs JSON-RPC errors</span><p>Handler-level failures — <code>bash</code> command that exited non-zero, <code>read</code> against a missing file — return through <code>result.content</code> with <code>isError: true</code>, NOT through the JSON-RPC <code>error</code> field. Only protocol-level failures use <code>error</code>. Hosts that treat both channels as equivalent will misclassify recoverable failures.</p></aside>

## What is exposed

Two surfaces:

- **Tools.** Every `mcp.ToolSpec` registered before `Serve` is advertised in `tools/list` and callable via `tools/call`. rousseau wires the same tool implementations the local agent loop uses: `read`, `write`, `edit`, `grep`, `bash`.
- **Sessions.** rousseau's SQLite session store is exposed so an MCP host can enumerate and read past conversations. `resources/list` returns one entry per session.

Tool failures are surfaced through the `content` channel with `isError=true`, not the JSON-RPC error channel. This is the MCP convention.

## Client configuration — Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or the platform equivalent:

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

Restart Claude Desktop. `rousseau` will appear in the tools palette; every registered tool is invocable.

For a rousseau built into a Podman image, the entry becomes:

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

Bind-mount the state directory so the MCP host sees the same sessions as the daemon.

## Registering a custom tool

Embedding the MCP server in your own binary:

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

Duplicate registrations return an error; `MustRegister` panics on duplicate (reserved for wire-up in `main`).

## Concurrency

`Serve` may be called concurrently on independent transports (stdin/stdout for the MCP host, plus a control channel if you want one). The server's tool map is protected by an RWMutex; handler execution is not serialised — implementations must be safe for concurrent use.

## Debugging

Every request/response envelope is logged at `debug` level by default. Enable with:

```yaml
log:
  level: debug
  format: text
```

Or:

```sh
ROUSSEAU_LOG_LEVEL=debug rousseau mcp 2>/tmp/mcp.log
```

The MCP host consumes stdout; keep the log stream on stderr.

## Troubleshooting

### Claude Desktop / Cursor never shows the rousseau tools

Almost always a wiring error, not a rousseau problem. Check: (1) the `command` and `args` in the host config invoke `rousseau mcp` (not `rousseau chat`); (2) the config file was saved and the host restarted; (3) `rousseau mcp </dev/null` from a shell doesn't crash — if it does, fix that first.

### `parse error` on the very first message

The host is not sending line-delimited JSON. Some early MCP implementations send framed messages (`Content-Length: N\r\n\r\n<body>`); rousseau expects `\n`-delimited. Update the host to a build that uses stdio framing (all current major hosts do).

### `method not found: <foo>`

The host is calling a method rousseau does not implement. Empty `resources/list` and `prompts/list` are provided as no-ops for the common probes; anything else returns `-32601`. Check `internal/mcp/server.go` `dispatch()` for the full method list.

### Tool calls succeed but the host reports them as errors

The tool handler returned an error the wrong way. Handlers should return `[]Content{{Type: "text", Text: err.Error()}}, err != nil` — rousseau catches the error and wraps it into `isError: true`. Do not return the error via the JSON-RPC `error` channel unless it is a protocol-level failure.

### Container-based MCP fails with `permission denied` on state directory

The `podman run` invocation from Claude Desktop must include a `-v` for the state directory with the right SELinux label. Use `:Z` (private) unless the container is shared with other Podman workloads. Also verify the host UID inside the container matches the file ownership.

## Related pages

- [MCP: Exposed Tools](/mcp/exposed-tools/) — the tool set rousseau publishes.
- [MCP: Exposed Resources](/mcp/exposed-resources/) — session enumeration and read.
- [MCP: Compatibility](/mcp/compatibility/) — tested host matrix.
- [Tutorials: Expose Tools via MCP](/tutorials/expose-tools-via-mcp/) — end-to-end walkthrough.
- [Agent loop](/agent-loop/) — how the same tools are used inside rousseau.

## Further reading

- `internal/mcp/protocol.go` — envelope, method names, error codes.
- `internal/mcp/server.go` — `Serve`, `dispatch`, tool registry.
- `internal/mcp/tools.go` — helpers for registering rousseau's built-in tools.
- `internal/cli/mcp.go` — the `rousseau mcp` command wiring.
- [Model Context Protocol spec](https://modelcontextprotocol.io) — external reference.
