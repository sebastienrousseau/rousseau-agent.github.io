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
hreflang: "es"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "es"
locale: "es_ES"
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
permalink: "https://docs.rousseau-agent.dev/es/developer-guide/add-a-transport/"
subtitle: "Adding a tenth transport in a few hundred lines."
tags: "developer-guide, transport, extend"
title: "Añadir un transporte"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add transport, extend, adapter, start stop deliver, fake injection, transport interface"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Añadir un transporte"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 62
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-transport/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-transport/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Añadir un transporte"
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
twitter_title: "Añadir un transporte"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Gracias a cada operador que ejecuta su propio agente de codificación."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Qué significa "añadir un transporte"

Cada transporte en rousseau es un adaptador sobre un cliente de protocolo aguas arriba. El adaptador implementa una interfaz pequeña, expone un método `Deliver` para el planificador cron y se registra como subcomando de Cobra en `internal/cli/`.

El núcleo del agente no se mueve. Ese es el invariante — una implementación de interfaz más un cableado en el CLI equivalen a un nuevo transporte.

## La interfaz

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

`Start` bloquea hasta que `ctx` sea cancelado o se llame a `Stop`. `Handle` recibe mensajes entrantes y devuelve el texto de respuesta — el router se encarga del aislamiento de sesiones por remitente y de la aplicación de la allowlist.

Las implementaciones normalmente también exponen un método `Deliver(ctx context.Context, target, body string) error` para que el planificador cron pueda enviar mensajes que no se originaron en un turno entrante.

## Esqueleto

Añadamos un transporte hipotético **XMPP**.

### Paso 1 — Directorio y adaptador

Crea `internal/transport/xmpp/` reflejando la forma de `internal/transport/slack/`:

```
internal/transport/xmpp/
├── client.go        # Config, New, Start, Stop, Deliver
├── client_test.go   # Pruebas usando fakes inyectados
├── dispatch.go      # onMessage → Handler.Handle → enviar respuesta
└── dispatch_test.go
```

### Paso 2 — `client.go`

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

### Paso 3 — `dispatch.go`

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

## Paso 4 — Superficie de configuración

Añade un tipo `XMPPConfig` a `internal/config/config.go`:

```go
type XMPPConfig struct {
    Server      string   `mapstructure:"server"`
    JID         string   `mapstructure:"jid"`
    Password    string   `mapstructure:"password"`
    ReplyHeader string   `mapstructure:"reply_header"`
    Allowlist   []string `mapstructure:"allowlist"`
}
```

Y un campo en `Config`:

```go
XMPP XMPPConfig `mapstructure:"xmpp"`
```

Establece los valores por defecto en `setDefaults(v)`.

## Paso 5 — Cableado en el CLI

Añade `internal/cli/xmpp.go`:

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

Regístralo en `internal/cli/root.go`:

```go
root.AddCommand(newXMPPCmd(opts))
```

## Paso 6 — Pruebas

Sigue el patrón de inyección de fakes usado por `internal/transport/whatsapp/client_test.go` y `internal/transport/slack/*_test.go`:

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
    // Simular un mensaje entrante.
    up.onMsg("alice@x", "hi")
    // Dar un momento a la goroutine; normalmente vía señal por canal en pruebas reales.
    cancel()

    require.Len(t, up.sent, 1)
    require.Equal(t, "hello alice@x", up.sent[0].Body)
}
```

## Paso 7 — Documentación

Añade `content/transports/xmpp.md` en el sitio de docs (este repositorio). Sigue el mismo esquema que `content/transports/slack.md` — descripción, superficie de configuración, receta de cableado y advertencias.

## Paso 8 — CI

El gate de lint detectará comentarios godoc ausentes en identificadores exportados, pruebas faltantes, imports no utilizados y el umbral de cobertura. Ejecuta:

```sh
make check
```

Si todo pasa en local, la matriz de CI también pasará (Ubuntu + macOS ejecutan el mismo comando).

## Errores comunes

- **Olvidar la idempotencia de `Stop()`.** La interfaz permite que `Stop` se invoque varias veces. Usa un mutex + bool `stopped`.
- **No respetar `ctx` en `Start`.** El manejador de señales del demonio cancela el contexto raíz; cada componente de vida larga debe retornar cuando lo hace.
- **Codificar directamente el tipo del cliente upstream.** Define una interfaz pequeña para el upstream, tómala como parámetro del constructor, inyecta un cliente real en `cli/xmpp.go` y uno falso en las pruebas. Este es el patrón de testabilidad clave.
- **Bloquear el callback.** Los callbacks de `OnMessage` normalmente corren en la goroutine del upstream. Enruta al handler mediante un canal o un pool de goroutines acotado para que una llamada lenta al modelo no atasque al upstream.

## Solución de problemas

### La satisfacción de la interfaz falla en compilación

Añade `var _ transport.Transport = (*Client)(nil)` al final de tu `client.go`. El compilador señalará el método faltante.

### `Start` nunca retorna

Olvidaste `<-ctx.Done()` antes de retornar. El manejador de señales del demonio cancela el contexto raíz en `SIGTERM` / `SIGINT`; cada `Start` debe respetarlo.

### Las pruebas se cuelgan porque el callback corre en una goroutine en background

Usa un canal + `require.Eventually` (o un `t.Deadline`) para esperar la respuesta. No te apoyes en `time.Sleep`.

### El umbral de cobertura falla

El gate es del 75 % global, más alto para paquetes core. Añade pruebas al menos para el bucle happy-path de resolver + responder y para un motivo de skip (prevención de bucles o mensajes no textuales).

### La allowlist del router bloquea tu prueba

Las pruebas deben usar un `transport.HandlerFunc` directamente, no pasar por el router. Si necesitas ejercitar el comportamiento del router, pasa una allowlist vacía (o una que incluya al remitente de prueba).

## Páginas relacionadas

- [Guía del desarrollador: arquitectura](/es/developer-guide/architecture/) — dónde encaja `Transport`.
- [Guía del desarrollador: pruebas](/es/developer-guide/testing/) — el patrón de inyección en profundidad.
- [Guía del desarrollador: añadir un proveedor](/es/developer-guide/add-a-provider/) — misma forma, distinta interfaz.
- [Guía del desarrollador: contribuir](/es/developer-guide/contributing/) — estilo de commits y checklist de PR.
- [Transportes](/es/transports/) — los adaptadores incluidos como implementaciones de referencia.

## Lecturas adicionales

- `internal/transport/transport.go` — los tipos `Transport`, `Handler` e `IncomingMessage`.
- `internal/transport/router.go` — cómo funcionan las allowlists y el mapeo de sesiones.
- `internal/transport/whatsapp/client.go` — un adaptador canónico de complejidad media.
- `internal/transport/slack/client.go` — un adaptador canónico para un protocolo WebSocket + REST.
- `internal/cli/whatsapp.go`, `internal/cli/slack.go` — ejemplos de cableado en el CLI.
