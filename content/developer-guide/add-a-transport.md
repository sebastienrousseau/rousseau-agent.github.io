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
changefreq: "monthly"
description: "How to add a tenth transport to rousseau-agent: implement Start/Stop/Deliver, register in cli, add tests using the fake-injection pattern."
keywords: "add transport, extend, adapter, start stop deliver, fake injection, transport interface"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/developer-guide/add-a-transport/"
subtitle: "Adding a tenth transport in a few hundred lines."
tags: "developer-guide, transport, extend"
title: "Add a Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add transport, extend, adapter, start stop deliver, fake injection, transport interface"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Add a Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 62
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-transport/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-transport/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Add a Transport"
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
twitter_title: "Add a Transport"
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

## What "add a transport" means

Every transport in rousseau is an adapter over an upstream protocol client. The adapter implements a small interface, exposes a `Deliver` method for the cron scheduler, and is registered as a Cobra subcommand in `internal/cli/`.

The agent core does not move. That is the invariant — one interface implementation plus one CLI wire-up equals a new transport.

## The interface

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

`Start` blocks until `ctx` is cancelled or `Stop` is called. `Handle` receives inbound messages and returns the reply text — the router owns per-sender session isolation and allowlist enforcement.

Implementations also typically expose a `Deliver(ctx context.Context, target, body string) error` method so the cron scheduler can send messages that did not originate from an inbound turn.

## Skeleton

Let's add a hypothetical **XMPP** transport.

### Step 1 — Directory and adapter

Create `internal/transport/xmpp/` mirroring the shape of `internal/transport/slack/`:

```
internal/transport/xmpp/
├── client.go        # Config, New, Start, Stop, Deliver
├── client_test.go   # Tests using injected fakes
├── dispatch.go      # onMessage → Handler.Handle → send reply
└── dispatch_test.go
```

### Step 2 — `client.go`

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

### Step 3 — `dispatch.go`

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

## Step 4 — Config surface

Add an `XMPPConfig` type to `internal/config/config.go`:

```go
type XMPPConfig struct {
    Server      string   `mapstructure:"server"`
    JID         string   `mapstructure:"jid"`
    Password    string   `mapstructure:"password"`
    ReplyHeader string   `mapstructure:"reply_header"`
    Allowlist   []string `mapstructure:"allowlist"`
}
```

And a field on `Config`:

```go
XMPP XMPPConfig `mapstructure:"xmpp"`
```

Set any defaults in `setDefaults(v)`.

## Step 5 — CLI wire-up

Add `internal/cli/xmpp.go`:

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

Register it in `internal/cli/root.go`:

```go
root.AddCommand(newXMPPCmd(opts))
```

## Step 6 — Tests

Follow the fake-injection pattern used by `internal/transport/whatsapp/client_test.go` and `internal/transport/slack/*_test.go`:

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
    // Simulate an inbound message.
    up.onMsg("alice@x", "hi")
    // Give the goroutine a moment; usually via a channel signal in real tests.
    cancel()

    require.Len(t, up.sent, 1)
    require.Equal(t, "hello alice@x", up.sent[0].Body)
}
```

## Step 7 — Docs

Add `content/transports/xmpp.md` in the docs site (this repo). Follow the same layout as `content/transports/slack.md` — description, config surface, wiring recipe, caveats.

## Step 8 — CI

The lint gate will catch missing godoc comments on exported identifiers, missing tests, unused imports, and the coverage floor. Run:

```sh
make check
```

If everything passes locally, the CI matrix will pass too (Ubuntu + macOS run the same command).

## Common pitfalls

- **Forgetting `Stop()` idempotency.** The interface allows `Stop` to be called multiple times. Use a mutex + `stopped` bool.
- **Not honouring `ctx` in `Start`.** The daemon signal handler cancels the root context; every long-lived component must return when it does.
- **Baking in the upstream client type.** Define a small interface for the upstream, take it as a constructor parameter, inject a real client in `cli/xmpp.go` and a fake in tests. This is the load-bearing testability pattern.
- **Blocking the callback.** `OnMessage` callbacks typically run on the upstream's goroutine. Route to the handler via a channel or a bounded goroutine pool so a slow model call cannot back up the upstream.

## Troubleshooting

### Interface satisfaction fails at compile

Add `var _ transport.Transport = (*Client)(nil)` at the bottom of your `client.go`. The compiler will point at the missing method.

### `Start` never returns

You forgot to `<-ctx.Done()` before returning. The daemon signal handler cancels the root context on `SIGTERM` / `SIGINT`; every `Start` must respect it.

### Tests hang because the callback runs on a background goroutine

Use a channel + `require.Eventually` (or a `t.Deadline`) to wait for the reply. Do not rely on `time.Sleep`.

### Coverage floor fails

The gate is 75% overall, higher for core packages. Add tests for at least the happy-path resolve + reply loop and one skip-reason (loop prevention or non-text messages).

### Router allowlist blocks your test

Tests should use a `transport.HandlerFunc` directly, not go through the router. If you must exercise router behaviour, pass an empty allowlist (or one that includes the test sender).

## Related pages

- [Developer Guide: Architecture](/developer-guide/architecture/) — where `Transport` fits.
- [Developer Guide: Testing](/developer-guide/testing/) — the injection pattern in depth.
- [Developer Guide: Add a provider](/developer-guide/add-a-provider/) — same shape, different interface.
- [Developer Guide: Contributing](/developer-guide/contributing/) — commit style and PR checklist.
- [Transports](/transports/) — the shipped adapters as reference implementations.

## Further reading

- `internal/transport/transport.go` — the `Transport`, `Handler`, and `IncomingMessage` types.
- `internal/transport/router.go` — how allowlists and session mapping work.
- `internal/transport/whatsapp/client.go` — a canonical medium-complexity adapter.
- `internal/transport/slack/client.go` — a canonical adapter for a WebSocket + REST protocol.
- `internal/cli/whatsapp.go`, `internal/cli/slack.go` — CLI wiring examples.
