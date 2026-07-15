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
description: "Rousseau's SQLite session store: sessions table, FTS5 recall index, JID mapping table, cron jobs, and WAL journaling."
keywords: "sqlite, fts5, session store, sessions, jid, cron, WAL, schema"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/reference/session-store/"
subtitle: "The SQLite schema at the heart of rousseau's state."
tags: "reference, sqlite, fts5, session, wal"
title: "Referência: armazenamento de sessões"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "sqlite, fts5, session store, sessions, jid, cron, WAL, schema"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referência: armazenamento de sessões"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 53
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/session-store/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/session-store/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Referência: armazenamento de sessões"
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
twitter_description: "Rousseau's SQLite session store: sessions table, FTS5 recall index, JID mapping table, cron jobs, and WAL journaling."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Referência: armazenamento de sessões"
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

## Localização e driver

O session store é um único database SQLite em `state.path` (padrão para `~/.local/share/rousseau/sessions.db`, veja `internal/config/config.go` `setDefaults`).

O rousseau usa `modernc.org/sqlite` — um driver SQLite puro-Go. **Não há dependência de CGO ou libsqlite3**. O binário Go em `bin/rousseau` é totalmente estático.

`internal/state/sqlite/store.go` `Open()` aplica quatro pragmas em cada open:

| PRAGMA | Propósito |
|---|---|
| `journal_mode=WAL` | Write-ahead logging. Habilita leitores concorrentes, backups live seguros. |
| `foreign_keys=ON` | Garantia padrão de integridade. |
| `busy_timeout=15000` | Espera de 15 segundos em contenção de lock — crítico assim que múltiplos transportes escrevem concorrentemente. |
| — | `EnsureSearch` roda depois para instalar o schema FTS5. |

O store é aberto uma vez por processo. Múltiplos daemons apontando para o mesmo arquivo DB são suportados por causa da combinação busy-timeout + WAL — o bridge WhatsApp, `rousseau mcp` e `rousseau session list` podem compartilhar o arquivo com segurança.

## Tour de schema

### Tabela: `sessions`

Definida em `internal/state/sqlite/schema.sql`:

```sql
CREATE TABLE IF NOT EXISTS sessions (
    id             TEXT PRIMARY KEY,
    title          TEXT NOT NULL,
    payload        TEXT NOT NULL,        -- JSON blob of the full agent.Session
    message_count  INTEGER NOT NULL DEFAULT 0,
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sessions_updated_at
    ON sessions(updated_at DESC);
```

**Formato do payload.** A coluna `payload` armazena o JSON completo de `agent.Session` — roles, blocos de conteúdo, blocos tool-use e tool-result, timestamps. Veja `Save`/`Load` em `internal/state/sqlite/store.go`. Manter a sessão inteira como um único blob JSON mantém migrações de schema raras; queries contra internals vão pelo índice FTS5 abaixo.

**Timestamps** são ISO-8601 com precisão de milissegundos (`2006-01-02T15:04:05.000Z` na sintaxe de time do Go), UTC.

**Ordenação.** `idx_sessions_updated_at` alimenta `List` e `RecentSessions` (ambos em `store.go` / `search.go`).

### Tabela virtual: `sessions_fts` (FTS5)

Instalada por `searchSchema` em `internal/state/sqlite/search.go`:

```sql
CREATE VIRTUAL TABLE IF NOT EXISTS sessions_fts USING fts5(
    session_id UNINDEXED,
    title,
    body,
    tokenize = 'porter unicode61'
);
```

Três escritas dirigidas por trigger a mantêm consistente com `sessions`:

- `sessions_fts_ai` — após INSERT em `sessions`, espelha a linha.
- `sessions_fts_au` — após UPDATE, delete + reinsert.
- `sessions_fts_ad` — após DELETE, apaga a linha FTS.

**Backfill.** `EnsureSearch` roda um `LEFT JOIN` em cada `Open()` para inserir quaisquer linhas de `sessions` que o índice FTS ainda não tem. Isso torna o índice seguro para adicionar a um database existente — sem migração manual.

**Tokenização.** `porter unicode61` — stemmer Porter + casefolding ciente de Unicode. Case-insensitive, trata morfologia inglesa (`retry`/`retries`/`retried`).

**Ranqueamento.** `Search()` ordena por `bm25(sessions_fts)` (menor é mais relevante). `SearchHit.Rank` o expõe.

**Sintaxe de query.** Passada ao FTS5 literalmente. Veja [Tutorial: Expor ferramentas via MCP](/pt-BR/tutorials/expose-tools-via-mcp/) para o cheat sheet do operador.

### Tabela: `jid_sessions`

Persiste mapeamentos de platform-sender-para-session-id; instalada por `NewJIDMap` em `internal/state/sqlite/jidmap.go`:

```sql
CREATE TABLE IF NOT EXISTS jid_sessions (
    jid         TEXT PRIMARY KEY,
    session_id  TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
```

Cada transporte de longa duração usa o JID map para que o mesmo número de telefone, usuário Matrix ou usuário Slack retome a mesma conversa entre restarts. `Router.Handle` (`internal/transport/router.go`) faz o lookup em inbound; `Put` escreve após `Save`.

O espaço de JID é específico de transporte — `447900123456@s.whatsapp.net` para WhatsApp, `@user:matrix.org` para Matrix, `U01ABC…` para Slack. O transporte é responsável pela canonicalização.

### Tabela: `cron_jobs`

Instalada por `NewCronStore` em `internal/state/sqlite/cron.go`:

```sql
CREATE TABLE IF NOT EXISTS cron_jobs (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    cron_expr   TEXT NOT NULL,
    prompt      TEXT NOT NULL,
    deliver_to  TEXT NOT NULL,
    enabled     INTEGER NOT NULL DEFAULT 1,
    created_at  TEXT NOT NULL,
    last_run_at TEXT
);
```

`UNIQUE(name)` previne duplicatas. `rousseau cron add/list/remove/enable/disable` (de `internal/cli/cron.go`) todos fazem round-trip por esta tabela. O scheduler em `internal/cron/scheduler.go` reconcilia dela a cada `poll_interval`. O MCP a expõe somente leitura via `rousseau_cron_list`.

## Postura de concorrência

- **WAL** permite leitores concorrentes ilimitados ao lado de um único escritor.
- **`busy_timeout=15000`** significa que um escritor que bate em contenção espera até 15 s em vez de falhar rapidamente. Na prática o bridge WhatsApp mantém o papel de escritor enquanto `rousseau mcp` e `rousseau session list` são visitantes somente leitura.
- O store não é desenhado para concorrência cross-machine. Dois hosts escrevendo no mesmo arquivo sobre NFS é comportamento indefinido — use um único escritor e rsync o DB para outro lugar para read replicas.

## Fazendo backup

A abordagem mais segura é um `sqlite3 .backup` live:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db ".backup '/backup/sessions.db.$(date -I).bak'"
```

`.backup` usa a API de backup online do SQLite e funciona enquanto o primário está sendo escrito. Snapshots `restic` / `borg` no arquivo bruto também são seguros por causa do WAL — o backup pega um snapshot consistente no momento em que o arquivo foi lido.

O arquivo `whatsapp.db` (credenciais de device do whatsmeow) é um database separado; faça backup do mesmo jeito se você quer evitar re-pareamento após um restore.

## Reconstruindo o índice FTS

Se o índice FTS5 sair de sincronia (extremamente raro — os triggers o mantêm consistente), reconstrua-o:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions_fts;
INSERT INTO sessions_fts (session_id, title, body)
SELECT id, title, payload FROM sessions;
SQL
```

O `EnsureSearch` do rousseau não desfará isso; os triggers apenas retomam de um estado limpo.

## Relacionado

- [Conceitos](/pt-BR/concepts/) — onde o store se encaixa na arquitetura geral.
- [Guia do usuário: Compressão + Recall](/pt-BR/user-guide/compression-recall/) — como o índice FTS é exposto ao modelo.
- [MCP: Ferramentas expostas](/pt-BR/mcp/exposed-tools/) — a superfície somente leitura sobre este schema.
- [Guias: Gerenciando workspaces](/pt-BR/guides/managing-workspaces/) — compartilhando / particionando o store entre máquinas.
