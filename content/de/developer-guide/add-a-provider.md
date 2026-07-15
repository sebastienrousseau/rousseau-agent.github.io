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
description: "How to add a sixth LLM provider to rousseau-agent: implement Provider.Complete and optionally StreamingProvider.CompleteStream."
keywords: "add provider, llm, chat completion, streaming, agent provider, extend"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/developer-guide/add-a-provider/"
subtitle: "Provider.Complete and StreamingProvider.CompleteStream."
tags: "developer-guide, provider, llm, extend"
title: "Anbieter hinzufügen"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add provider, llm, chat completion, streaming, agent provider, extend"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Anbieter hinzufügen"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 63
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-provider/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-provider/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Anbieter hinzufügen"
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
twitter_description: "How to add a sixth LLM provider to rousseau-agent: implement Provider.Complete and optionally StreamingProvider.CompleteStream."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Anbieter hinzufügen"
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

## Die Schnittstelle

`internal/agent/provider.go` (paraphrasiert):

```go
type Request struct {
    SessionID string
    System    string
    Messages  []Message
    Tools     []ToolDefinition
}

type Response struct {
    Message    Message
    StopReason StopReason
}

// Provider drives a single round-trip.
type Provider interface {
    Complete(ctx context.Context, req Request) (Response, error)
}

// StreamingProvider streams response deltas as they arrive.
type StreamingProvider interface {
    Provider
    CompleteStream(ctx context.Context, req Request) (StreamReader, error)
}
```

Jeder LLM-Adapter erfüllt mindestens `Provider`. `StreamingProvider` ist Opt-in – die TUI- und Chat-Transport-Handler fallen auf den Non-Streaming-Pfad zurück, wenn ein Provider ihn nicht implementiert.

`StopReason` ist einer von `StopEndTurn`, `StopToolUse`, `StopMaxTokens`. Die Agent-Schleife behandelt `StopEndTurn` als terminal und `StopToolUse` als "das Modell will einen Tool-Aufruf".

## Grundgerüst für einen neuen Provider

Fügen wir einen hypothetischen **Cohere-Command-R**-Provider hinzu.

### Schritt 1 — Verzeichnis

```
internal/llm/cohere/
├── client.go        # Config, New
├── complete.go      # Provider.Complete
├── stream.go        # StreamingProvider.CompleteStream (optional)
└── *_test.go
```

### Schritt 2 — `client.go`

```go
// Package cohere implements the Cohere Command R provider.
package cohere

import (
    "net/http"
    "time"
)

// Config configures the Cohere provider.
type Config struct {
    APIKey    string
    Model     string
    BaseURL   string
    MaxTokens int64
}

// Provider is the Cohere adapter.
type Provider struct {
    cfg    Config
    client *http.Client
}

// New constructs a Provider.
func New(cfg Config) *Provider {
    if cfg.BaseURL == "" {
        cfg.BaseURL = "https://api.cohere.com/v1"
    }
    if cfg.MaxTokens == 0 {
        cfg.MaxTokens = 4096
    }
    return &Provider{
        cfg:    cfg,
        client: &http.Client{Timeout: 120 * time.Second},
    }
}
```

### Schritt 3 — `complete.go`

`Complete` implementieren:

```go
package cohere

import (
    "bytes"
    "context"
    "encoding/json"
    "fmt"
    "net/http"

    "github.com/sebastienrousseau/rousseau-agent/internal/agent"
)

// Complete satisfies agent.Provider.
func (p *Provider) Complete(ctx context.Context, req agent.Request) (agent.Response, error) {
    body, err := p.encodeRequest(req)
    if err != nil {
        return agent.Response{}, fmt.Errorf("cohere: encode: %w", err)
    }

    httpReq, err := http.NewRequestWithContext(ctx, http.MethodPost, p.cfg.BaseURL+"/chat", bytes.NewReader(body))
    if err != nil {
        return agent.Response{}, err
    }
    httpReq.Header.Set("content-type", "application/json")
    httpReq.Header.Set("authorization", "Bearer "+p.cfg.APIKey)

    httpResp, err := p.client.Do(httpReq)
    if err != nil {
        return agent.Response{}, fmt.Errorf("cohere: transport: %w", err)
    }
    defer httpResp.Body.Close()

    if httpResp.StatusCode >= 400 {
        return agent.Response{}, fmt.Errorf("cohere: HTTP %d", httpResp.StatusCode)
    }

    var raw cohereResponse
    if err := json.NewDecoder(httpResp.Body).Decode(&raw); err != nil {
        return agent.Response{}, fmt.Errorf("cohere: decode: %w", err)
    }
    return p.decodeResponse(raw), nil
}

// Compile-time interface check.
var _ agent.Provider = (*Provider)(nil)
```

Die Bodies `encodeRequest`, `decodeResponse` und die `cohereResponse`-Form sind Cohere-spezifisch – sie übersetzen rousseaus Provider-agnostische Typen `agent.Request` und `agent.Response` in und aus Coheres Wire-Format.

### Schritt 4 — Streaming (optional)

Wenn Cohere SSE-artiges Streaming unterstützt, implementieren Sie `CompleteStream`. Überspringen Sie es in einem ersten Durchgang; die Agent-Schleife fällt automatisch auf Non-Streaming zurück.

### Schritt 5 — Konfigurationsoberfläche

Fügen Sie `CohereConfig` zu `internal/config/config.go` hinzu:

```go
type CohereConfig struct {
    APIKey    string `mapstructure:"api_key"`
    Model     string `mapstructure:"model"`
    BaseURL   string `mapstructure:"base_url"`
    MaxTokens int64  `mapstructure:"max_tokens"`
}
```

Fügen Sie ein Feld zu `Config` hinzu:

```go
Cohere CohereConfig `mapstructure:"cohere"`
```

Erweitern Sie `setDefaults` mit einem sinnvollen Modell-Standardwert:

```go
v.SetDefault("cohere.model", "command-r-plus")
```

### Schritt 6 — CLI-Verdrahtung

Erweitern Sie in `internal/cli/provider.go` `buildProvider(cfg *config.Config)`:

```go
func buildProvider(cfg *config.Config) (agent.Provider, error) {
    switch cfg.Provider {
    // ...existing cases...
    case "cohere":
        return cohere.New(cohere.Config{
            APIKey:    cfg.Cohere.APIKey,
            Model:     cfg.Cohere.Model,
            BaseURL:   cfg.Cohere.BaseURL,
            MaxTokens: cfg.Cohere.MaxTokens,
        }), nil
    default:
        return nil, fmt.Errorf("unknown provider %q", cfg.Provider)
    }
}
```

Erweitern Sie `rousseau doctor` (`internal/cli/doctor.go`), um einen `provider.cohere.*`-Prüfblock hinzuzufügen, wenn `cfg.Provider == "cohere"`. Spiegeln Sie die bestehenden anthropic-Prüfungen.

## Vertragsdetails, die die Agent-Schleife voraussetzt

- **`Complete` respektiert `ctx`.** Lange HTTP-Anfragen müssen die Kontextabbruch-Signale beachten, sonst hängt der `SIGTERM`-Shutdown des Daemons.
- **Tool-Use-Round-Trip.** Wenn das Modell `tool_use`-Blöcke ausgibt, muss das `StopReason` der Antwort `StopToolUse` sein und der Nachrichteninhalt muss `Content{Kind: ContentToolUse, ToolUse: &ToolUse{Name, Input, ID}}` für jeden angeforderten Aufruf enthalten. Die Agent-Schleife leitet jeden an die `Registry`, führt ihn aus und leitet die Ergebnisse im nächsten `Complete`-Aufruf zurück.
- **`tool_result`-Verarbeitung.** Beim nächsten Aufruf enthält `req.Messages` eine Benutzernachricht, deren Inhalt für jeden ausgeführten Aufruf `Content{Kind: ContentToolResult, ToolResult: &ToolResult{ToolUseID, Output, IsError}}` enthält. Der Provider muss diese in die von der Upstream-API erwartete Form rendern.
- **Compile-Time-Schnittstellen-Prüfung.** `var _ agent.Provider = (*Provider)(nil)` auf Paket-Ebene fängt Schnittstellen-Drift zur Bauzeit ab.

## Streaming-Vertrag

Wenn Sie `StreamingProvider` implementieren:

```go
type StreamReader interface {
    Next(ctx context.Context) (StreamChunk, error)
    Close() error
}

type StreamChunk struct {
    Delta     string       // partial text delta
    Done      bool         // final chunk
    Response  *Response    // final Response, non-nil only on Done
}
```

Die TUI- und Chat-Transport-Handler lesen Deltas, sobald sie eintreffen; die finale `Response` wird verwendet, um die vollständig geformte Assistenten-Nachricht an die Sitzung anzuhängen.

## Prompt-Caching

`internal/llm/anthropic` platziert `cache_control`-Marker auf den letzten beiden Nachrichten der Anfrage. Wenn Ihr Provider Prompt-Caching unterstützt, tun Sie dasselbe – das wandelt Kompression + Recall (siehe [Kompression + Recall](/de/user-guide/compression-recall/)) von einem token-hungrigen Muster in ein günstiges um.

## Tests

Verwenden Sie `httptest.NewServer`, um ein Fake-Upstream aufzusetzen. `internal/llm/anthropic/*_test.go` ist die Referenz. Das Muster:

1. Starten Sie `httptest.NewServer` mit einem Handler, der vorgefertigtes JSON zurückliefert.
2. Konstruieren Sie den Provider und zeigen Sie `BaseURL` auf den Testserver.
3. Rufen Sie `Complete` mit einer vorgefertigten `Request` auf.
4. Verifizieren Sie die zurückgelieferte `Response`-Form.

Für Streaming unterstützt `httptest` ebenfalls Server-Sent Events – siehe `internal/llm/anthropic/stream.go`.

## Dokumentation

Fügen Sie `content/providers/cohere.md` in dieser Docs-Site hinzu. Folgen Sie der Form von `content/providers/anthropic.md` – Beschreibung, Konfigurationsoberfläche, Auth-Details, provider-spezifische Vorbehalte.

## Häufige Fallstricke

- **Stilles Umschreiben von `Messages`.** Die Agent-Schleife ist die Wahrheitsquelle für den Konversationszustand. Provider müssen die Form übersetzen, ohne die Semantik zu mutieren.
- **Tool-Use-IDs verlieren.** Jede `ToolUse.ID` in einer Antwort muss zu einer `ToolResult.ToolUseID` in der nächsten Anfrage passen. Wenn Ihr Provider eigene IDs vergibt, übersetzen Sie sorgfältig.
- **`MaxTokens` ignorieren.** Einige Provider lehnen Anfragen ohne explizites Limit ab. Setzen Sie einen sinnvollen Standardwert in `New`.
- **Die Schleife mit Retry-Richtlinien blockieren.** Retries gehören in den Provider-Adapter, nicht in die Agent-Schleife. Begrenzen Sie sie; schnelles Fehlschlagen ist besser als Hängen.

## Weiter

- [Tests](/de/developer-guide/testing/) — wie Sie die `_test.go` des Providers schreiben.
- [Tool hinzufügen](/de/developer-guide/add-a-tool/) — der kleinste Erweiterungspunkt.
- [Konfiguration](/de/configuration/) — die Konfigurationsoberfläche, die jeder Provider exponiert.
