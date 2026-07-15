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
hreflang: "fr"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "fr"
locale: "fr_FR"
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
permalink: "https://docs.rousseau-agent.dev/fr/developer-guide/add-a-transport/"
subtitle: "Adding a tenth transport in a few hundred lines."
tags: "developer-guide, transport, extend"
title: "Ajouter un transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "add transport, extend, adapter, start stop deliver, fake injection, transport interface"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Ajouter un transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 62
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/add-a-transport/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/add-a-transport/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Ajouter un transport"
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
twitter_title: "Ajouter un transport"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Ce que signifie « ajouter un transport »

Chaque transport dans rousseau est un adaptateur au-dessus d'un client de protocole amont. L'adaptateur implémente une petite interface, expose une méthode `Deliver` pour le planificateur cron, et est enregistré comme sous-commande Cobra dans `internal/cli/`.

Le cœur de l'agent ne bouge pas. C'est l'invariant — une implémentation d'interface plus un câblage CLI égale un nouveau transport.

## L'interface

`internal/transport/transport.go` :

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

`Start` bloque jusqu'à ce que `ctx` soit annulé ou que `Stop` soit appelé. `Handle` reçoit les messages entrants et retourne le texte de réponse — le routeur possède l'isolation de session par émetteur et l'application de l'allowlist.

Les implémentations exposent typiquement aussi une méthode `Deliver(ctx context.Context, target, body string) error` pour que le planificateur cron puisse envoyer des messages qui ne proviennent pas d'un tour entrant.

## Squelette

Ajoutons un transport **XMPP** hypothétique.

### Étape 1 — Répertoire et adaptateur

Créez `internal/transport/xmpp/` reflétant la forme de `internal/transport/slack/` :

```
internal/transport/xmpp/
├── client.go        # Config, New, Start, Stop, Deliver
├── client_test.go   # Tests using injected fakes
├── dispatch.go      # onMessage → Handler.Handle → send reply
└── dispatch_test.go
```

### Étape 2 — `client.go`

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

### Étape 3 — `dispatch.go`

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

## Étape 4 — Surface de config

Ajoutez un type `XMPPConfig` à `internal/config/config.go` :

```go
type XMPPConfig struct {
    Server      string   `mapstructure:"server"`
    JID         string   `mapstructure:"jid"`
    Password    string   `mapstructure:"password"`
    ReplyHeader string   `mapstructure:"reply_header"`
    Allowlist   []string `mapstructure:"allowlist"`
}
```

Et un champ sur `Config` :

```go
XMPP XMPPConfig `mapstructure:"xmpp"`
```

Définissez les défauts éventuels dans `setDefaults(v)`.

## Étape 5 — Câblage CLI

Ajoutez `internal/cli/xmpp.go` :

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

Enregistrez-la dans `internal/cli/root.go` :

```go
root.AddCommand(newXMPPCmd(opts))
```

## Étape 6 — Tests

Suivez le motif d'injection de fake utilisé par `internal/transport/whatsapp/client_test.go` et `internal/transport/slack/*_test.go` :

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

## Étape 7 — Documentation

Ajoutez `content/transports/xmpp.md` dans le site de documentation (ce dépôt). Suivez la même mise en page que `content/transports/slack.md` — description, surface de config, recette de câblage, précautions.

## Étape 8 — CI

Le gate lint attrapera les commentaires godoc manquants sur les identifiants exportés, les tests manquants, les imports inutilisés et le plancher de couverture. Exécutez :

```sh
make check
```

Si tout passe en local, la matrice CI passera aussi (Ubuntu + macOS exécutent la même commande).

## Pièges courants

- **Oublier l'idempotence de `Stop()`.** L'interface autorise l'appel multiple de `Stop`. Utilisez un mutex + booléen `stopped`.
- **Ne pas honorer `ctx` dans `Start`.** Le gestionnaire de signaux du démon annule le contexte racine ; chaque composant longue durée doit retourner à ce moment.
- **Coder en dur le type de client amont.** Définissez une petite interface pour l'amont, prenez-la comme paramètre de constructeur, injectez un vrai client dans `cli/xmpp.go` et un fake dans les tests. C'est le motif de testabilité central.
- **Bloquer le callback.** Les callbacks `OnMessage` tournent typiquement sur la goroutine de l'amont. Routez vers le handler via un canal ou un pool de goroutines borné pour qu'un appel modèle lent ne bloque pas l'amont.

## Dépannage

### La satisfaction d'interface échoue à la compilation

Ajoutez `var _ transport.Transport = (*Client)(nil)` en bas de votre `client.go`. Le compilateur pointera la méthode manquante.

### `Start` ne retourne jamais

Vous avez oublié `<-ctx.Done()` avant de retourner. Le gestionnaire de signaux du démon annule le contexte racine sur `SIGTERM` / `SIGINT` ; chaque `Start` doit le respecter.

### Les tests se figent parce que le callback tourne sur une goroutine en arrière-plan

Utilisez un canal + `require.Eventually` (ou un `t.Deadline`) pour attendre la réponse. Ne comptez pas sur `time.Sleep`.

### Le plancher de couverture échoue

Le gate est à 75 % au global, plus haut pour les packages cœur. Ajoutez au moins des tests pour la boucle resolve + reply du chemin heureux et une raison de skip (prévention de boucle ou messages non-texte).

### L'allowlist du routeur bloque votre test

Les tests devraient utiliser un `transport.HandlerFunc` directement, sans passer par le routeur. Si vous devez exercer le comportement du routeur, passez une allowlist vide (ou une qui inclut l'émetteur du test).

## Pages associées

- [Guide développeur : Architecture](/fr/developer-guide/architecture/) — où s'insère `Transport`.
- [Guide développeur : Testing](/fr/developer-guide/testing/) — le motif d'injection en profondeur.
- [Guide développeur : ajouter un fournisseur](/fr/developer-guide/add-a-provider/) — même forme, interface différente.
- [Guide développeur : contribuer](/fr/developer-guide/contributing/) — style de commit et checklist des PR.
- [Transports](/fr/transports/) — les adaptateurs livrés comme implémentations de référence.

## Pour aller plus loin

- `internal/transport/transport.go` — les types `Transport`, `Handler` et `IncomingMessage`.
- `internal/transport/router.go` — fonctionnement des allowlists et du mapping de session.
- `internal/transport/whatsapp/client.go` — un adaptateur canonique de complexité moyenne.
- `internal/transport/slack/client.go` — un adaptateur canonique pour un protocole WebSocket + REST.
- `internal/cli/whatsapp.go`, `internal/cli/slack.go` — exemples de câblage CLI.
