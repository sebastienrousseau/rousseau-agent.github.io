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
description: "How to add a tenth transport to rousseau-agent: implement Start/Stop/Deliver, register in cli, add tests using the fake-injection pattern."
keywords: "add transport, extend, adapter, start stop deliver, fake injection, transport interface"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/developer-guide/add-a-transport/"
subtitle: "Adding a tenth transport in a few hundred lines."
tags: "developer-guide, transport, extend"
title: "Transport hinzufügen"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add transport, extend, adapter, start stop deliver, fake injection, transport interface"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transport hinzufügen"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 62
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-transport/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-transport/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transport hinzufügen"
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
twitter_description: "How to add a tenth transport to rousseau-agent: implement Start/Stop/Deliver, register in cli, add tests using the fake-injection pattern."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transport hinzufügen"
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

## Was "Transport hinzufügen" bedeutet

Jeder Transport in rousseau ist ein Adapter über einem Upstream-Protokoll-Client. Der Adapter implementiert eine kleine Schnittstelle, exponiert eine `Deliver`-Methode für den Cron-Scheduler und wird als Cobra-Unterbefehl in `internal/cli/` registriert.

Der Agent-Kern bewegt sich nicht. Das ist die Invariante – eine Schnittstellen-Implementierung plus eine CLI-Verdrahtung ergibt einen neuen Transport.

## Die Schnittstelle

`internal/transport/transport.go`:

```go
type IncomingMessage struct {
    From string
    Body string
    At   time.Time
}

type Handler interface {
    Handle(ctx context.Context, msg IncomingMessage) (string, error)
}

type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

`Start` blockiert, bis `ctx` abgebrochen oder `Stop` aufgerufen wird. `Handle` empfängt eingehende Nachrichten und gibt den Antworttext zurück – der Router besitzt die Sitzungsisolation pro Absender und die Allowlist-Durchsetzung.

Implementierungen exponieren typischerweise auch eine `Deliver(ctx context.Context, target, body string) error`-Methode, damit der Cron-Scheduler Nachrichten senden kann, die nicht aus einem eingehenden Turn stammen.

## Grundgerüst

Fügen wir einen hypothetischen **XMPP**-Transport hinzu.

### Schritt 1 — Verzeichnis und Adapter

Erstellen Sie `internal/transport/xmpp/` in Anlehnung an die Form von `internal/transport/slack/`:

```
internal/transport/xmpp/
├── client.go        # Config, New, Start, Stop, Deliver
├── client_test.go   # Tests using injected fakes
├── dispatch.go      # onMessage → Handler.Handle → send reply
└── dispatch_test.go
```

### Schritt 2 — `client.go`

```go
// Package xmpp is the XMPP transport adapter.
package xmpp

import (
    "context"
    "fmt"
    "log/slog"
    "sync"

    "github.com/sebastienrousseau/rousseau-agent/internal/transport"
)

// Config configures the XMPP transport.
type Config struct {
    Server      string
    JID         string
    Password    string
    ReplyHeader string
}

// XMPPClient is the abstract interface the adapter needs from the
// upstream client. Kept small so tests can inject a fake.
type XMPPClient interface {
    Connect(ctx context.Context) error
    OnMessage(func(from, body string))
    Send(to, body string) error
    Close() error
}

// Client is the transport adapter.
type Client struct {
    cfg     Config
    logger  *slog.Logger
    upstream XMPPClient

    mu      sync.Mutex
    handler transport.Handler
    stopped bool
}

// New constructs a Client. In production, upstream is a real xmpp.Client;
// in tests, it is a fake.
func New(cfg Config, logger *slog.Logger, upstream XMPPClient) (*Client, error) {
    if cfg.Server == "" || cfg.JID == "" {
        return nil, fmt.Errorf("xmpp: server and JID required")
    }
    return &Client{cfg: cfg, logger: logger, upstream: upstream}, nil
}

// Name satisfies transport.Transport.
func (*Client) Name() string { return "xmpp" }

// Start satisfies transport.Transport.
func (c *Client) Start(ctx context.Context, handler transport.Handler) error {
    c.mu.Lock()
    c.handler = handler
    c.mu.Unlock()

    if err := c.upstream.Connect(ctx); err != nil {
        return fmt.Errorf("xmpp: connect: %w", err)
    }
    c.upstream.OnMessage(func(from, body string) {
        c.onMessage(ctx, from, body)
    })
    <-ctx.Done()
    return c.Stop()
}

// Stop satisfies transport.Transport.
func (c *Client) Stop() error {
    c.mu.Lock()
    if c.stopped {
        c.mu.Unlock()
        return nil
    }
    c.stopped = true
    c.mu.Unlock()
    return c.upstream.Close()
}

// Deliver sends a message outside the request/response loop (e.g. cron).
func (c *Client) Deliver(_ context.Context, target, body string) error {
    return c.upstream.Send(target, c.cfg.ReplyHeader+body)
}
```

### Schritt 3 — `dispatch.go`

```go
package xmpp

import (
    "context"
    "log/slog"
    "time"

    "github.com/sebastienrousseau/rousseau-agent/internal/transport"
)

func (c *Client) onMessage(ctx context.Context, from, body string) {
    c.mu.Lock()
    handler := c.handler
    c.mu.Unlock()
    if handler == nil {
        return
    }

    reply, err := handler.Handle(ctx, transport.IncomingMessage{
        From: from,
        Body: body,
        At:   time.Now().UTC(),
    })
    if err != nil {
        c.logger.Warn("xmpp.handle_failed", slog.String("err", err.Error()))
        return
    }
    if reply == "" {
        return
    }
    if err := c.upstream.Send(from, c.cfg.ReplyHeader+reply); err != nil {
        c.logger.Warn("xmpp.send_failed", slog.String("err", err.Error()))
    }
}
```

## Schritt 4 — Konfigurationsoberfläche

Fügen Sie einen `XMPPConfig`-Typ zu `internal/config/config.go` hinzu:

```go
type XMPPConfig struct {
    Server      string   `mapstructure:"server"`
    JID         string   `mapstructure:"jid"`
    Password    string   `mapstructure:"password"`
    ReplyHeader string   `mapstructure:"reply_header"`
    Allowlist   []string `mapstructure:"allowlist"`
}
```

Und ein Feld an `Config`:

```go
XMPP XMPPConfig `mapstructure:"xmpp"`
```

Legen Sie Standardwerte in `setDefaults(v)` fest.

## Schritt 5 — CLI-Verdrahtung

Fügen Sie `internal/cli/xmpp.go` hinzu:

```go
package cli

import (
    "github.com/spf13/cobra"

    "github.com/sebastienrousseau/rousseau-agent/internal/transport/xmpp"
)

func newXMPPCmd(opts *Options) *cobra.Command {
    var allow []string
    cmd := &cobra.Command{
        Use:   "xmpp",
        Short: "Run the XMPP bridge",
        RunE: func(cmd *cobra.Command, _ []string) error {
            setUnattendedPermissionDefault(opts, "xmpp")
            ctx := cmd.Context()

            wiring, err := assembleDaemon(ctx, opts, allow)
            if err != nil {
                return err
            }
            defer func() { _ = wiring.Sessions.Close() }() //nolint:errcheck

            upstream, err := newRealXMPPClient(opts.Config.XMPP)
            if err != nil {
                return err
            }

            client, err := xmpp.New(xmpp.Config{
                Server:      opts.Config.XMPP.Server,
                JID:         opts.Config.XMPP.JID,
                Password:    opts.Config.XMPP.Password,
                ReplyHeader: opts.Config.XMPP.ReplyHeader,
            }, opts.Logger, upstream)
            if err != nil {
                return err
            }

            shutdown, err := wiring.startCron(ctx, client.Deliver, opts.Logger)
            if err != nil {
                return err
            }
            defer shutdown()

            return client.Start(ctx, wiring.Router)
        },
    }
    cmd.Flags().StringSliceVar(&allow, "allow", nil, "restrict inbound to these XMPP JIDs")
    return cmd
}
```

Registrieren Sie ihn in `internal/cli/root.go`:

```go
root.AddCommand(newXMPPCmd(opts))
```

## Schritt 6 — Tests

Folgen Sie dem Fake-Injection-Muster von `internal/transport/whatsapp/client_test.go` und `internal/transport/slack/*_test.go`:

```go
type fakeXMPP struct {
    connectErr error
    onMsg      func(from, body string)
    sent       []struct{ To, Body string }
}

func (f *fakeXMPP) Connect(context.Context) error { return f.connectErr }
func (f *fakeXMPP) OnMessage(fn func(from, body string)) { f.onMsg = fn }
func (f *fakeXMPP) Send(to, body string) error {
    f.sent = append(f.sent, struct{ To, Body string }{to, body})
    return nil
}
func (f *fakeXMPP) Close() error { return nil }

func TestClient_ReplyRoundTrip(t *testing.T) {
    up := &fakeXMPP{}
    c, err := xmpp.New(xmpp.Config{Server: "s", JID: "j"}, slog.Default(), up)
    require.NoError(t, err)

    handler := transport.HandlerFunc(func(_ context.Context, m transport.IncomingMessage) (string, error) {
        return "hello " + m.From, nil
    })

    ctx, cancel := context.WithCancel(context.Background())
    go func() { _ = c.Start(ctx, handler) }()
    // Eine eingehende Nachricht simulieren.
    up.onMsg("alice@x", "hi")
    // Der Goroutine einen Moment geben; in echten Tests üblicherweise über ein Channel-Signal.
    cancel()

    require.Len(t, up.sent, 1)
    require.Equal(t, "hello alice@x", up.sent[0].Body)
}
```

## Schritt 7 — Dokumentation

Fügen Sie `content/transports/xmpp.md` in der Docs-Site (diesem Repository) hinzu. Folgen Sie demselben Layout wie `content/transports/slack.md` – Beschreibung, Konfigurationsoberfläche, Verdrahtungsrezept, Vorbehalte.

## Schritt 8 — CI

Das Lint-Gate fängt fehlende godoc-Kommentare an exportierten Identifiern, fehlende Tests, ungenutzte Imports und die Coverage-Untergrenze ab. Ausführen:

```sh
make check
```

Wenn lokal alles besteht, wird auch die CI-Matrix bestehen (Ubuntu + macOS führen denselben Befehl aus).

## Häufige Fallstricke

- **`Stop()`-Idempotenz vergessen.** Die Schnittstelle erlaubt, dass `Stop` mehrfach aufgerufen wird. Verwenden Sie einen Mutex + `stopped`-bool.
- **`ctx` in `Start` nicht respektieren.** Der Signal-Handler des Daemons bricht den Root-Kontext ab; jede langlebige Komponente muss dann zurückkehren.
- **Den Upstream-Client-Typ einbetonieren.** Definieren Sie eine kleine Schnittstelle für den Upstream, nehmen Sie sie als Konstruktor-Parameter, injizieren Sie in `cli/xmpp.go` einen echten Client und in Tests einen Fake. Dies ist das tragende Testbarkeits-Muster.
- **Den Callback blockieren.** `OnMessage`-Callbacks laufen typischerweise auf der Goroutine des Upstreams. Leiten Sie sie über einen Channel oder einen begrenzten Goroutine-Pool an den Handler, damit ein langsamer Modell-Aufruf den Upstream nicht aufstauen kann.

## Fehlerbehebung

### Schnittstellenerfüllung schlägt zur Compile-Zeit fehl

Fügen Sie `var _ transport.Transport = (*Client)(nil)` am Ende Ihrer `client.go` hinzu. Der Compiler zeigt auf die fehlende Methode.

### `Start` kehrt nie zurück

Sie haben `<-ctx.Done()` vor dem Zurückgeben vergessen. Der Signal-Handler des Daemons bricht bei `SIGTERM` / `SIGINT` den Root-Kontext ab; jedes `Start` muss ihn respektieren.

### Tests hängen, weil der Callback auf einer Hintergrund-Goroutine läuft

Verwenden Sie einen Channel + `require.Eventually` (oder ein `t.Deadline`), um auf die Antwort zu warten. Verlassen Sie sich nicht auf `time.Sleep`.

### Coverage-Untergrenze schlägt fehl

Das Gate ist 75 % insgesamt, höher für Kernpakete. Fügen Sie mindestens Tests für die Happy-Path-Resolve-+-Reply-Schleife und einen Skip-Grund (Schleifenverhinderung oder Nicht-Text-Nachrichten) hinzu.

### Router-Allowlist blockiert Ihren Test

Tests sollten direkt einen `transport.HandlerFunc` verwenden, nicht durch den Router gehen. Wenn Sie Router-Verhalten testen müssen, übergeben Sie eine leere Allowlist (oder eine, die den Test-Absender enthält).

## Verwandte Seiten

- [Entwicklerleitfaden: Architektur](/de/developer-guide/architecture/) — wo `Transport` passt.
- [Entwicklerleitfaden: Tests](/de/developer-guide/testing/) — das Injektionsmuster im Detail.
- [Entwicklerleitfaden: Provider hinzufügen](/de/developer-guide/add-a-provider/) — gleiche Form, andere Schnittstelle.
- [Entwicklerleitfaden: Mitwirken](/de/developer-guide/contributing/) — Commit-Stil und PR-Checkliste.
- [Transporte](/de/transports/) — die ausgelieferten Adapter als Referenzimplementierungen.

## Weiterführende Lektüre

- `internal/transport/transport.go` — die Typen `Transport`, `Handler` und `IncomingMessage`.
- `internal/transport/router.go` — wie Allowlists und Session-Mapping funktionieren.
- `internal/transport/whatsapp/client.go` — ein kanonischer Adapter mittlerer Komplexität.
- `internal/transport/slack/client.go` — ein kanonischer Adapter für ein WebSocket-+-REST-Protokoll.
- `internal/cli/whatsapp.go`, `internal/cli/slack.go` — CLI-Verdrahtungsbeispiele.
