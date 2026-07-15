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
hreflang: "pt-BR"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "pt-BR"
locale: "pt_BR"
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
permalink: "https://docs.rousseau-agent.dev/pt-BR/developer-guide/add-a-transport/"
subtitle: "Adding a tenth transport in a few hundred lines."
tags: "developer-guide, transport, extend"
title: "Adicionar um transporte"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add transport, extend, adapter, start stop deliver, fake injection, transport interface"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Adicionar um transporte"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 62
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-transport/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-transport/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Adicionar um transporte"
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
twitter_title: "Adicionar um transporte"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Obrigado a cada operador que executa seu próprio agente de codificação."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## O que "adicionar um transporte" significa

Cada transporte no rousseau é um adapter sobre um cliente de protocolo upstream. O adapter implementa uma interface pequena, expõe um método `Deliver` para o cron scheduler e é registrado como um subcomando Cobra em `internal/cli/`.

O core do agente não se move. Essa é a invariante — uma implementação de interface mais um wire-up de CLI é igual a um novo transporte.

## A interface

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

`Start` bloqueia até `ctx` ser cancelado ou `Stop` ser chamado. `Handle` recebe mensagens inbound e retorna o texto de resposta — o router é dono do isolamento de sessão por remetente e da aplicação da allowlist.

Implementações também tipicamente expõem um método `Deliver(ctx context.Context, target, body string) error` para que o cron scheduler possa enviar mensagens que não se originaram de um turno inbound.

## Skeleton

Vamos adicionar um transporte **XMPP** hipotético.

### Passo 1 — Diretório e adapter

Crie `internal/transport/xmpp/` espelhando a forma de `internal/transport/slack/`:

```
internal/transport/xmpp/
├── client.go        # Config, New, Start, Stop, Deliver
├── client_test.go   # Tests using injected fakes
├── dispatch.go      # onMessage → Handler.Handle → send reply
└── dispatch_test.go
```

### Passo 2 — `client.go`

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

### Passo 3 — `dispatch.go`

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

## Passo 4 — Superfície de config

Adicione um tipo `XMPPConfig` a `internal/config/config.go`:

```go
type XMPPConfig struct {
    Server      string   `mapstructure:"server"`
    JID         string   `mapstructure:"jid"`
    Password    string   `mapstructure:"password"`
    ReplyHeader string   `mapstructure:"reply_header"`
    Allowlist   []string `mapstructure:"allowlist"`
}
```

E um campo em `Config`:

```go
XMPP XMPPConfig `mapstructure:"xmpp"`
```

Defina quaisquer padrões em `setDefaults(v)`.

## Passo 5 — Wire-up de CLI

Adicione `internal/cli/xmpp.go`:

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

Registre em `internal/cli/root.go`:

```go
root.AddCommand(newXMPPCmd(opts))
```

## Passo 6 — Testes

Siga o padrão de injeção de fake usado por `internal/transport/whatsapp/client_test.go` e `internal/transport/slack/*_test.go`:

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

## Passo 7 — Docs

Adicione `content/transports/xmpp.md` no docs site (este repo). Siga o mesmo layout de `content/transports/slack.md` — descrição, superfície de config, receita de wiring, ressalvas.

## Passo 8 — CI

O lint gate vai pegar comentários godoc faltando em identificadores exportados, testes faltando, imports não usados e o floor de cobertura. Rode:

```sh
make check
```

Se tudo passa localmente, a matriz CI vai passar também (Ubuntu + macOS rodam o mesmo comando).

## Armadilhas comuns

- **Esquecer a idempotência de `Stop()`.** A interface permite `Stop` ser chamado várias vezes. Use um mutex + bool `stopped`.
- **Não honrar `ctx` em `Start`.** O signal handler do daemon cancela o context raiz; cada componente de longa duração deve retornar quando o faz.
- **Fixar o tipo do cliente upstream.** Defina uma interface pequena para o upstream, tome-a como parâmetro de construtor, injete um cliente real em `cli/xmpp.go` e um fake nos testes. Esse é o padrão load-bearing de testabilidade.
- **Bloquear o callback.** Callbacks `OnMessage` tipicamente rodam na goroutine do upstream. Roteie para o handler via um canal ou um pool bounded de goroutines para que uma call lenta ao modelo não faça back-up no upstream.

## Solução de problemas

### Satisfação de interface falha no compile

Adicione `var _ transport.Transport = (*Client)(nil)` no final do seu `client.go`. O compilador vai apontar para o método faltante.

### `Start` nunca retorna

Você esqueceu de `<-ctx.Done()` antes de retornar. O signal handler do daemon cancela o context raiz em `SIGTERM` / `SIGINT`; cada `Start` deve respeitar isso.

### Testes travam porque o callback roda em uma goroutine de background

Use um canal + `require.Eventually` (ou um `t.Deadline`) para esperar pela resposta. Não confie em `time.Sleep`.

### Floor de cobertura falha

O gate é 75% geral, maior para pacotes core. Adicione testes para pelo menos o loop de resolve + reply do caminho feliz e uma razão de skip (prevenção de loop ou mensagens não-texto).

### Allowlist do router bloqueia seu teste

Testes devem usar um `transport.HandlerFunc` diretamente, não passar pelo router. Se você precisa exercitar o comportamento do router, passe uma allowlist vazia (ou uma que inclui o remetente de teste).

## Páginas relacionadas

- [Guia do desenvolvedor: Arquitetura](/pt-BR/developer-guide/architecture/) — onde `Transport` se encaixa.
- [Guia do desenvolvedor: Testing](/pt-BR/developer-guide/testing/) — o padrão de injeção em profundidade.
- [Guia do desenvolvedor: Adicionar um provider](/pt-BR/developer-guide/add-a-provider/) — mesma forma, interface diferente.
- [Guia do desenvolvedor: Contribuindo](/pt-BR/developer-guide/contributing/) — estilo de commit e checklist de PR.
- [Transportes](/pt-BR/transports/) — os adapters enviados como implementações de referência.

## Leitura adicional

- `internal/transport/transport.go` — os tipos `Transport`, `Handler` e `IncomingMessage`.
- `internal/transport/router.go` — como allowlists e mapeamento de sessão funcionam.
- `internal/transport/whatsapp/client.go` — um adapter canônico de complexidade média.
- `internal/transport/slack/client.go` — um adapter canônico para um protocolo WebSocket + REST.
- `internal/cli/whatsapp.go`, `internal/cli/slack.go` — exemplos de wiring de CLI.
