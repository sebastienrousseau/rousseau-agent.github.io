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
date: "July 13, 2026"
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
description: "How rousseau's session store partitions by workspace, how to switch workspaces, share sessions across machines, and drop a workspace's history."
keywords: "workspace, session store, state path, sync, rsync, XDG_DATA_HOME"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/managing-workspaces/"
subtitle: "Partition state per project, share history across machines, drop history cleanly."
tags: "guides, workspace, session store, sqlite"
title: "Guia: gestão de workspaces"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "workspace, session store, state path, sync, rsync, XDG_DATA_HOME"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: gestão de workspaces"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 38
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/managing-workspaces/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/managing-workspaces/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guia: gestão de workspaces"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
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
twitter_description: "How rousseau's session store partitions by workspace, how to switch workspaces, share sessions across machines, and drop a workspace's history."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guia: gestão de workspaces"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Obrigado a cada operador que executa seu próprio agente de codificação."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## A convenção

O rousseau não tem um conceito de primeira classe de "workspace". Ele tem um `state.path` em `internal/config/config.go` (`StateConfig`) e por padrão aponta cada processo para `~/.local/share/rousseau/sessions.db`. Todas as sessões, jobs de cron, mapeamentos JID e o índice de recall FTS5 vivem naquele único arquivo.

Para a maioria dos operadores isso é exatamente certo. Quando você quer isolamento — por projeto, por máquina, por cliente — você aponta o rousseau para um arquivo SQLite diferente. Aquele arquivo **é** o workspace.

## Troca de workspace por invocação

Dois knobs, qualquer um funciona:

```sh
# 1. flag on any rousseau command
rousseau --config ~/.config/rousseau/acme.yaml chat

# 2. env var (Viper picks it up via ROUSSEAU_STATE_PATH)
ROUSSEAU_STATE_PATH=~/.local/share/rousseau/acme.db rousseau chat
```

Nenhuma das abordagens requer um restart do rousseau quando você pula entre workspaces — cada processo abre seu próprio arquivo.

## Layout de workspace por projeto

```
~/.config/rousseau/
├── acme.yaml         # provider = anthropic, state.path = …/acme.db
├── personal.yaml     # provider = claudecli, state.path = …/personal.db
└── work.yaml         # provider = bedrock,    state.path = …/work.db
```

Cada arquivo de config sobrescreve `state.path`:

```yaml
state:
  path: /home/seb/.local/share/rousseau/acme.db
```

Depois lance cada sessão com a config certa. A TUI (`internal/tui/model.go`) expõe o session id + provider em sua barra de status — confirmação visual de que você está no workspace certo.

## Compartilhando histórico entre máquinas

O session store é um único arquivo SQLite. O journaling WAL é habilitado por `Open()` em `internal/state/sqlite/store.go`, então snapshots live são seguros:

```sh
# Snapshot laptop-to-desktop (both idle)
rsync -avz --partial \
  ~/.local/share/rousseau/sessions.db \
  desktop:~/.local/share/rousseau/sessions.db
```

**Apenas um escritor por vez.** Não rode `rousseau whatsapp` em duas máquinas contra o mesmo arquivo SQLite sobre NFS — isso é indefinido. Sincronize quando nada estiver escrevendo, ou rode um único escritor com read replicas.

Uma alternativa mais segura é o snapshot `.backup`:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db ".backup '/tmp/sessions.snap.db'"
scp /tmp/sessions.snap.db desktop:~/.local/share/rousseau/sessions.db
```

`.backup` usa a API de backup online do SQLite e produz um arquivo consistente point-in-time.

## Migrando um workspace

Mova o diretório inteiro; ele é o workspace:

```sh
rsync -avz ~/.local/share/rousseau/ new-host:~/.local/share/rousseau/
```

`whatsapp.db` (credenciais de device) é separado — você ou o traz também (device continua pareado) ou o deixa para trás e re-escaneia o QR no novo host.

## Descartando o histórico de um workspace

```sh
rousseau session list                 # confirm what you're about to lose
rm ~/.local/share/rousseau/acme.db*   # includes -wal and -shm sidecars
```

O próximo processo a abrir o caminho vai recriá-lo com o schema em `internal/state/sqlite/schema.sql`.

Se você só quer descartar um subconjunto de sessões, use o CLI:

```sh
rousseau session delete <id> --yes
```

`rousseau session delete` (`internal/cli/session.go`) chama `Store.Delete`, que faz cascade pelos triggers FTS5 para manter o índice de recall consistente. A flag `--yes` é obrigatória — o comando recusa rodar sem ela.

## Deleção parcial via SQL

Para limpeza em massa — cada sessão mais velha que 90 dias:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions WHERE updated_at < datetime('now', '-90 days');
SQL
```

Os triggers FTS5 (`sessions_fts_ad` em `internal/state/sqlite/search.go`) disparam no DELETE e mantêm o índice em sincronia automaticamente.

## Approvers por workspace

Como o arquivo de config e o arquivo de estado são ambos por workspace, o approver também é:

```yaml
# work.yaml — strict pattern approver
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

state:
  path: /home/seb/.local/share/rousseau/work.db
```

Um `personal.yaml` separado pode manter `mode: allow_all` para trabalho interativo. Veja [Tutorial: Endurecer o approver](/pt-BR/tutorials/harden-approver-policy/).

## Relacionado

- [Referência: Session store](/pt-BR/reference/session-store/) — schema.
- [Guias: Multi-provider](/pt-BR/guides/multi-provider/) — o padrão de duas configs, dois providers.
- [Referência: Variáveis de ambiente](/pt-BR/reference/environment-variables/) — cada env var de path.
- [Guia do usuário: CLI](/pt-BR/user-guide/cli/) — comandos `rousseau session`.
