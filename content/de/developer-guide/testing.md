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
description: "Testing pattern for rousseau-agent: dependency injection via interfaces (WSConn, IMAPClient, HTTPClient), fake generators, race + coverage thresholds."
keywords: "testing, dependency injection, fake, mock, coverage, race, go test, httptest"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/developer-guide/testing/"
subtitle: "Dependency injection, fakes, race, coverage."
tags: "developer-guide, testing, di, fakes"
title: "Tests"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "testing, dependency injection, fake, mock, coverage, race, go test, httptest"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tests"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 65
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/testing/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/testing/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Tests"
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
twitter_description: "Testing pattern for rousseau-agent: dependency injection via interfaces (WSConn, IMAPClient, HTTPClient), fake generators, race + coverage thresholds."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tests"
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

## Das Muster

Jedes Paket, das mit der Außenwelt spricht, definiert eine kleine Schnittstelle für seine Abhängigkeit, nimmt diese Schnittstelle als Konstruktor-Parameter und injiziert einen echten Client in `cli/*.go` (Produktion) oder einen Fake in `*_test.go` (Tests).

Beispiele im Baum:

| Paket | Schnittstelle | Echt | Fake für Tests |
|---|---|---|---|
| `internal/transport/whatsapp` | `WSConn` | whatsmeows WebSocket | In-Memory-Struct mit einem `send`-Channel |
| `internal/transport/email` | `IMAPClient` | `emersion/go-imap`-Client | Skriptgesteuerter Channel von Nachrichten |
| `internal/transport/whatsapp` | `Sender` | Direktes whatsmeow-Send | In-Memory-Slice zur Verifikation |
| `internal/llm/*` | `HTTPClient` (indirekt über `http.Client`) | `http.DefaultTransport` | `httptest.NewServer` |
| `internal/state/sqlite` | `state.Store` (Schnittstelle im Besitz von `state`) | `modernc.org/sqlite` auf Disk | In-Memory-`:memory:`-DSN |
| `internal/agent` | `Provider`, `Approver`, `Compressor`, `RecallProvider` | Konkrete `llm/*`-Typen | Struct-Implementierungen in `_test.go` |

Die Regel: **Schnittstelle beim Consumer, Implementierung beim Provider.** `Provider` ist in `agent` definiert, nicht in `llm/anthropic`. `Store` ist in `state` definiert, nicht in `state/sqlite`.

## Das Gate ausführen

```sh
make check
```

ist äquivalent zu:

```sh
go vet ./...
golangci-lint run
go test -race -count=1 -covermode=atomic ./...
govulncheck ./...
```

Die CI führt denselben Befehl auf `ubuntu-latest` und `macos-latest` aus. Wenn er lokal besteht, besteht er auch in der CI – abgesehen von plattform-spezifischen Bugs, weshalb macOS in der Matrix ist.

## Race-Detektor

`-race` ist nicht verhandelbar. Jeder Daemon in rousseau umfasst mehrere Goroutinen (Transport-Pump, Agent-Schleife, Cron-Scheduler, Sitzungsspeicher-Writer). Eine Race Condition in einer von ihnen ist ein echter Bug.

Wenn Sie einen Test finden, der nur unter `-race` fehlschlägt, ist das ein Bug im zu testenden Code, nicht im Test. Deaktivieren Sie `-race` nicht.

## Coverage-Untergrenze

Die aktuelle Coverage-Untergrenze beträgt **75 % gesamt**. Kernpakete (`internal/agent`, `internal/tools`, `internal/state/sqlite`) liegen bei 85–100 % und werden dort von der bestehenden Testsuite gehalten; neuer Code in diesen Paketen darf sie nicht senken.

Ein CI-Job läuft nach `go test -race -covermode=atomic ./... -coverprofile=coverage.out` und inspiziert `coverage.out`. Das Unterschreiten der Untergrenze lässt den Build fehlschlagen.

## Fake-Generatoren

Rousseau verwendet keine Mock-Generierungsbibliothek. Fakes sind handgeschriebene Struct-Typen, klein genug, um sie auf einen Blick zu lesen:

```go
type fakeProvider struct {
    responses []agent.Response
    calls     []agent.Request
}

func (f *fakeProvider) Complete(_ context.Context, req agent.Request) (agent.Response, error) {
    f.calls = append(f.calls, req)
    if len(f.responses) == 0 {
        return agent.Response{}, errors.New("no more canned responses")
    }
    resp := f.responses[0]
    f.responses = f.responses[1:]
    return resp, nil
}
```

Zwei Eigenschaften ergeben sich:

1. Der Fake ist inspizierbar – `calls` erfasst jede Anfrage, sodass Assertions prüfen können, was der zu testende Code ausgegeben hat.
2. Der Fake ist deterministisch – vorgefertigte Antworten werden in Reihenfolge konsumiert.

## `httptest` für HTTP-geformte Provider

Jeder LLM-Adapter, der HTTP spricht, verwendet `httptest.NewServer` für Tests:

```go
srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    _ = json.NewEncoder(w).Encode(map[string]any{
        "role":       "assistant",
        "content":    []map[string]any{{"type": "text", "text": "hello"}},
        "stop_reason":"end_turn",
    })
}))
defer srv.Close()

p := anthropic.New(anthropic.Config{
    APIKey:  "test",
    BaseURL: srv.URL,
    Model:   "test-model",
})
```

Für SSE-artiges Streaming funktioniert dieselbe Technik – `http.Flusher` ist auf dem Response-Writer verfügbar.

## Fuzz-Korpus

Jeder Parser hat eine `Fuzz*`-Funktion. Die vollständige Batterie ausführen:

```sh
make fuzz
```

Unter CI läuft Fuzz für eine begrenzte Zeit (`-fuzztime`). Lokal länger ausführen, um das Korpus zu seeden.

## Tabellengesteuerte Tests

Rousseaus Tests stützen sich stark auf tabellengesteuerte Form. Beispielform:

```go
func TestPatternApprover_Approve(t *testing.T) {
    tests := []struct {
        name     string
        approver *agent.PatternApprover
        req      agent.ApprovalRequest
        want     agent.Decision
    }{
        {
            name:     "erlaube read",
            approver: &agent.PatternApprover{Allow: []agent.PatternRule{{ToolName: "read"}}},
            req:      agent.ApprovalRequest{ToolName: "read"},
            want:     agent.DecisionAllow,
        },
        {
            name:     "deny gewinnt über allow",
            approver: &agent.PatternApprover{
                Allow: []agent.PatternRule{{ToolName: "bash"}},
                Deny:  []agent.PatternRule{{ToolName: "bash", Match: "rm"}},
            },
            req:  agent.ApprovalRequest{ToolName: "bash", Input: json.RawMessage(`{"command":"rm -rf /"}`)},
            want: agent.DecisionDeny,
        },
    }
    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            got, _ := tc.approver.Approve(context.Background(), tc.req)
            require.Equal(t, tc.want, got)
        })
    }
}
```

Das skaliert – jede neue Regelform wird zu einer Tabellenzeile.

## Goroutine-Lecks

Tests, die Goroutinen starten, müssen sie joinen. Übliche Muster:

- Verwenden Sie `context.WithCancel` und `cancel()` am Ende des Tests.
- Verwenden Sie eine `sync.WaitGroup` und `wg.Wait()`.
- Konsumieren Sie jeden Channel bis zum `close`.

Wenn ein Test eine Goroutine leakt, kann `go test -race` dies über einen Nil-Receiver-Panic auf der geleakten Goroutine abfangen, nachdem `main` der Testdatei beendet wurde. Günstiger, von Anfang an diszipliniert zu sein.

## Deterministische Zeit

Für zeitkritische Tests (Cron, Recall-Aktualitäts-Ranking) injizieren Sie einen `time.Time`-Provider:

```go
type Clock interface {
    Now() time.Time
}
```

Verdrahten Sie das echte `time.Now` in `cli/*` und ein Fake-`time.Time` im Test. Der Scheduler in `internal/cron/scheduler.go` verwendet dieses Muster.

## Testen der TUI

`internal/tui/model_test.go` verwendet den `TestModel`-Helper von `bubbletea`. `View()` ist eine reine String-Funktion des Modells, sodass die meisten Assertions zu "führe dieses Update aus, erwarte diese View-Ausgabe" werden.

## Was nicht zu testen ist

- Drittanbieter-Bibliotheken. Rousseau schattet whatsmeows oder `signal-cli`s Upstream-Tests nicht.
- Die Go-Standardbibliothek. `net/http` funktioniert.
- CLI-Flag-Registrierung durch Cobra. Cobras eigene Tests decken das ab.

Testen Sie stattdessen den Code, den Sie schreiben: die Verdrahtung, das Branching, die Fehlerpfade, die Wiederherstellungspfade.

## Weiter

- [Transport hinzufügen](/de/developer-guide/add-a-transport/) — das Fake-Injection-Muster auf einen vollständigen Transport angewendet.
- [Provider hinzufügen](/de/developer-guide/add-a-provider/) — `httptest` in Aktion.
- [Mitwirken](/de/developer-guide/contributing/) — die PR-Checkliste.
