---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "How to add a new built-in tool to rousseau-agent: declare a JSON schema, implement Execute, register with the tool registry."
keywords: "add tool, tool registry, json schema, execute, extend, custom tool"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/developer-guide/add-a-tool/"
subtitle: "Schema, Execute, register — three moving parts."
tags: "developer-guide, tools, extend"
title: "Werkzeug hinzufügen"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add tool, tool registry, json schema, execute, extend, custom tool"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Werkzeug hinzufügen"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 64
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-tool/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-tool/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Werkzeug hinzufügen"
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
twitter_description: "How to add a new built-in tool to rousseau-agent: declare a JSON schema, implement Execute, register with the tool registry."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Werkzeug hinzufügen"
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

`internal/tools/tool.go` (paraphrasiert):

```go
type Tool interface {
    Name() string
    Description() string
    InputSchema() map[string]any
    Execute(ctx context.Context, input json.RawMessage) (string, error)
}
```

Vier Methoden, kein Lebenszyklus. Tools sind aus Sicht der Schleife zustandslos – jeglicher Zustand, den das Tool benötigt (ein kompilierter Regex-Cache, ein In-Process-Index), ist ein privates Feld am konkreten Typ.

## Grundgerüst für ein neues Tool

Fügen wir ein hypothetisches **`http_get`**-Tool hinzu, das eine URL abruft und deren Body zurückliefert.

### Schritt 1 — Der Typ

```go
package builtin

import (
    "context"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "time"

    "github.com/sebastienrousseau/rousseau-agent/internal/tools"
)

// HTTPGetTool fetches a URL over HTTPS and returns the response body.
type HTTPGetTool struct {
    Timeout time.Duration
    client  *http.Client
}

// NewHTTPGetTool constructs an HTTPGetTool. Zero timeout uses 30s.
func NewHTTPGetTool(timeout time.Duration) *HTTPGetTool {
    if timeout == 0 {
        timeout = 30 * time.Second
    }
    return &HTTPGetTool{
        Timeout: timeout,
        client:  &http.Client{Timeout: timeout},
    }
}
```

### Schritt 2 — Metadaten

```go
// Name satisfies tools.Tool.
func (*HTTPGetTool) Name() string { return "http_get" }

// Description satisfies tools.Tool.
func (*HTTPGetTool) Description() string {
    return "Fetch an HTTPS URL and return the response body. Input: url (string). Redirects are followed up to 10 hops. Response is capped at 1 MiB."
}
```

Die **Beschreibung ist modell-seitig**. Sie sollte sich lesen wie ein kurzer Docstring für einen anderen Ingenieur – was das Tool tut, was seine Eingaben bedeuten, wie die Ausgabeform ist.

### Schritt 3 — Eingabeschema

```go
// InputSchema satisfies tools.Tool.
func (*HTTPGetTool) InputSchema() map[string]any {
    return map[string]any{
        "type": "object",
        "properties": map[string]any{
            "url": map[string]any{
                "type":        "string",
                "description": "Absolute HTTPS URL to fetch.",
            },
        },
        "required": []string{"url"},
    }
}
```

Halten Sie das Schema strikt. Jede Eigenschaft erhält eine `description`. Das `required`-Array wird vom Tool-Use-Validator des Modells durchgesetzt – fehlende Felder verursachen einen `tool_use`-Retry, keinen Laufzeitfehler.

### Schritt 4 — Execute

```go
type httpGetInput struct {
    URL string `json:"url"`
}

// Execute satisfies tools.Tool.
func (t *HTTPGetTool) Execute(ctx context.Context, raw json.RawMessage) (string, error) {
    var in httpGetInput
    if err := json.Unmarshal(raw, &in); err != nil {
        return "", fmt.Errorf("http_get: parse input: %w", err)
    }
    if in.URL == "" {
        return "", fmt.Errorf("http_get: url is required")
    }
    // Refuse plaintext HTTP; refuse non-http schemes.
    if !strings.HasPrefix(in.URL, "https://") {
        return "", fmt.Errorf("http_get: only https:// URLs are permitted")
    }

    req, err := http.NewRequestWithContext(ctx, http.MethodGet, in.URL, nil)
    if err != nil {
        return "", fmt.Errorf("http_get: build request: %w", err)
    }
    req.Header.Set("user-agent", "rousseau-agent/http_get")

    resp, err := t.client.Do(req)
    if err != nil {
        return "", fmt.Errorf("http_get: transport: %w", err)
    }
    defer func() { _ = resp.Body.Close() }()

    body, err := io.ReadAll(io.LimitReader(resp.Body, 1<<20))
    if err != nil {
        return "", fmt.Errorf("http_get: read body: %w", err)
    }
    return fmt.Sprintf("HTTP %d\n%s", resp.StatusCode, string(body)), nil
}

// Compile-time interface satisfaction check.
var _ tools.Tool = (*HTTPGetTool)(nil)
```

### Schritt 5 — Registrieren

Verdrahten Sie es in `internal/cli/chat.go` (und in jedem anderen Befehl, der eine Registry konstruiert – `grep`en Sie nach `registry.MustRegister`, um sie zu finden):

```go
registry.MustRegister(builtin.NewHTTPGetTool(30 * time.Second))
```

Einmal registriert, steht das Tool dem Modell bei jedem Turn zur Verfügung.

### Schritt 6 — Tests

Folgen Sie `internal/tools/builtin/read_test.go` für das Muster:

```go
func TestHTTPGetTool_Execute_Success(t *testing.T) {
    srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
        _, _ = w.Write([]byte("hello"))
    }))
    defer srv.Close()

    // Das Tool lehnt Klartext-HTTP ab; für einen echten Integrationstest den Testserver hinter httptest.NewTLSServer
    // hüllen oder eine interne Naht bereitstellen, die `http://` nur in Tests erlaubt.
    // Das Grundgerüst hier ist illustrativ.
}

func TestHTTPGetTool_Execute_RejectsPlaintextHTTP(t *testing.T) {
    tool := builtin.NewHTTPGetTool(0)
    _, err := tool.Execute(context.Background(), json.RawMessage(`{"url":"http://example.com"}`))
    require.Error(t, err)
    require.Contains(t, err.Error(), "only https")
}
```

### Schritt 7 — Freigaberichtlinie

Das Tool steht dem Modell nun zur Verfügung, vorbehaltlich der [Freigaberichtlinie](/de/user-guide/approval-policies/). Empfehlen Sie in der Dokumentation eine Ablehnungsregel für die Standardhaltung:

```yaml
deny:
  - {tool: http_get, match: "\"url\":\"https://(169\\.254|10\\.|192\\.168\\.|172\\.(1[6-9]|2[0-9]|3[01])\\.)"}
```

Dies verhindert, dass das Tool AWS IMDS oder privaten RFC1918-Adressraum anspricht – eine übliche Anforderung für HTTP-abrufende Tools.

### Schritt 8 — Dokumentation

Fügen Sie einen Abschnitt zu `content/user-guide/tools.md` hinzu, der das neue Tool beschreibt: Schema, Semantik, Sicherheitshinweise. Folgen Sie der Form der bestehenden fünf Tools.

## Vertragsdetails

- **Zustandslosigkeit**: `Execute` darf zwischen Aufrufen keinen Zustand tragen, der nicht explizit privat zu den eigenen Feldern des Tools ist. Zwei gleichzeitige Turns auf zwei Sitzungen können dasselbe Tool gleichzeitig aufrufen.
- **Kontext-Respekt**: `Execute` muss `ctx`-Abbruch respektieren. Langlaufende Arbeit sollte regelmäßig `ctx.Err()` prüfen oder die Arbeit über einen kontextsensitiven Bibliotheksaufruf leiten.
- **Keine Panics**: Geben Sie stattdessen Fehler zurück. Die Agent-Schleife wandelt einen Fehler in ein `tool_result` mit `IsError: true` um, an das sich das Modell anpassen kann.
- **Ausgabeform**: Die Ausgabe ist ein einfacher String, der dem Modell im nächsten Turn zurückgegeben wird. Fügen Sie genug Struktur hinzu (z. B. Zeilennummern, Statuscodes), damit das Modell darüber schlussfolgern kann.

## Benutzerdefinierte Tools, ohne den Quellcode zu berühren

Wenn Sie rousseau nicht forken wollen, betten Sie die Agent-Schleife in Ihr eigenes Binary ein und registrieren Sie dort Ihre Tools:

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewWriteTool())
// ...
registry.MustRegister(mypkg.NewMyTool())

ag := agent.New(provider, registry, logger, agent.Options{})
```

Siehe `examples/embed-agent/` im Quellbaum für ein vollständiges Einbettungsbeispiel.

## Häufige Fallstricke

- **Zu weit gefasstes Schema.** Nur `type: object` zu verlangen hilft dem Modell nicht. Zählen Sie jede Eigenschaft auf, beschreiben Sie jedes Feld.
- **Blockieren an I/O ohne Deadline.** Verwenden Sie immer `NewRequestWithContext`, setzen Sie immer einen `http.Client{Timeout: ...}`, respektieren Sie immer `ctx`.
- **Zu viel zurückgeben.** Die Ausgabe wird dem Modell im nächsten Turn zurückgegeben. Eine 1-MB-Antwort verbrennt Tokens; begrenzen Sie sie.
- **Seiteneffekte entkommen lassen.** Ein Tool, das die Welt verändert, sollte protokollieren, was es tat, im Rückgabe-String, damit der Audit-Trail des Approvers vollständig ist.
- **Die Compile-Time-Schnittstellen-Prüfung vergessen.** `var _ tools.Tool = (*MyTool)(nil)` auf Paket-Ebene fängt Schnittstellen-Drift zur Bauzeit ab.

## Weiter

- [Benutzerleitfaden: Tools](/de/user-guide/tools/) — die fünf eingebauten Tools mit Schemas.
- [Benutzerleitfaden: Freigaberichtlinien](/de/user-guide/approval-policies/) — wie Sie das neue Tool absichern.
- [Tests](/de/developer-guide/testing/) — das Muster für Tool-Tests.
