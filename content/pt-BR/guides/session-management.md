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
description: "Full session lifecycle: list, search, show, delete, compression triggers, and restoration from the SQLite session store."
keywords: "session, lifecycle, list, search, delete, compression, sqlite"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/session-management/"
subtitle: "List, search, delete, compress, restore."
tags: "guides, session, sqlite, compression"
title: "Guia: gestão de sessões"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "session, lifecycle, list, search, delete, compression, sqlite"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: gestão de sessões"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/session-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/session-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guia: gestão de sessões"
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
twitter_description: "Full session lifecycle: list, search, show, delete, compression triggers, and restoration from the SQLite session store."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guia: gestão de sessões"
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

## Ciclo de vida de sessão

Uma sessão é um valor `agent.Session` persistido como uma linha na tabela `sessions` (`internal/state/sqlite/schema.sql`). Ela tem um `id`, um `title`, um slice ordenado cronologicamente de valores `Message` e timestamps. Uma vez criada, ela existe até você deletá-la.

Sessões são criadas sob demanda por cada ponto de entrada:

- `rousseau chat` — uma sessão por sessão de TUI (uma nova a cada invocação de `chat`; você teria que construir um session-picker para reusar uma existente).
- Cada transporte (`whatsapp`, `slack`, …) — uma sessão por JID, via o JID map (`internal/state/sqlite/jidmap.go`).
- `rousseau cron` — cada disparo é uma sessão one-shot limitada àquela execução.

## Enumerar

```sh
rousseau session list --limit 10
```

Saída (de `newSessionListCmd` em `internal/cli/session.go`):

```
<short-id>  <messages>  <updated_at>  <title>
```

`--limit 0` retorna linhas ilimitadas.

## Buscar

FTS5 em cada mensagem registrada:

```sh
rousseau session search 'retry logic'
rousseau session search '"exponential backoff" AND anthropic'
rousseau session search 'retr*'                # prefix
```

O comando envolve `Store.Search` (`internal/state/sqlite/search.go`) com `SearchOptions{Limit: N}`. O ranqueamento é BM25; snippets são cortados para ~200 caracteres.

## Mostrar

```sh
rousseau session show <session-id>
```

Imprime o transcript completo com marcadores `→ tool_use(name, input)` e `← tool_result` entre mensagens do assistente. Útil para auditar a sessão de um daemon sem supervisão.

## Deletar

```sh
rousseau session delete <session-id> --yes
```

A flag `--yes` é obrigatória (`newSessionDeleteCmd`). Deleção faz cascade pelos triggers FTS5 para que o índice de recall permaneça consistente.

## Gatilhos de compressão

Quando `agent.compression.enabled: true` em `config.yaml`, o `LLMCompressor` (`internal/agent/compressor.go`) verifica duas condições antes de cada turno:

- `len(s.Messages) >= trigger_messages` (padrão 60).
- `len(s.Messages) > keep_recent` (padrão 8).

Se ambas valerem, o compressor resume o slice mais antigo em uma única mensagem sintética de usuário prefixada com o marcador `[rousseau-compressed]`, e mantém as últimas `keep_recent` mensagens literalmente. A sessão reescrita substitui a original em memória e é persistida no próximo `Store.Save`.

Uma segunda compressão em uma sessão já comprimida é pulada a menos que a sessão tenha crescido para mais de `2 * trigger_messages` — isso limita o crescimento descontrolado sem pagar para re-resumir a cada turno.

Linha de log:

```
INFO agent.compressed messages=68
```

## Restauração

Sessões restauram automaticamente. O router de transporte (`internal/transport/router.go`) procura o mapeamento JID → session id em cada mensagem inbound, depois `Store.Load` desmarshala o payload JSON de volta para um `agent.Session`. Nenhum passo manual.

Se um mapeamento estiver stale — session id existe em `jid_sessions` mas não em `sessions` — você verá `router.stale_mapping` (WARN), e o router cria uma sessão nova. Artefato legado de uma deleção parcial; seguro ignorar.

## Restauração manual a partir de um backup

Para reverter o store de sessão inteiro a partir de um snapshot `.backup`:

```sh
systemctl --user stop rousseau-agent
cp /backup/sessions.db.2026-07-12.bak ~/.local/share/rousseau/sessions.db
rm -f ~/.local/share/rousseau/sessions.db-wal ~/.local/share/rousseau/sessions.db-shm
systemctl --user start rousseau-agent
```

Os arquivos `-wal` e `-shm` devem ser removidos junto com o primário; o SQLite os reconstrói no próximo open.

## Deleção em massa por idade

Não há CLI embutido para "deletar sessões mais velhas que X". Faça direto pelo SQLite:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions WHERE updated_at < datetime('now', '-90 days');
SQL
```

Os triggers FTS5 mantêm o índice de recall consistente.

## Preservando privacidade

Como o conteúdo da sessão é armazenado em texto plano em um blob JSON, trate `sessions.db` como sensível. Opções:

- **Criptografia em nível de filesystem.** LUKS no Linux, FileVault no macOS.
- **Backups criptografados.** `restic` e `borg` ambos criptografam em repouso.
- **Delete-on-completion para sessões one-shot.** Para daemons dirigidos por cron, um hook pós-execução poderia rodar `rousseau session delete` no id da sessão recém-completada. Não é embutido hoje; veja [Guias: Onboarding Corporativo](/pt-BR/guides/enterprise-onboarding/) para a revisão.

## Referência completa de comandos `rousseau session`

<div class="tabs" data-tabs="session-commands">
  <div class="tab-list" role="tablist" aria-label="Subcomando de sessão">
    <button role="tab" aria-selected="true">list</button>
    <button role="tab" aria-selected="false">show</button>
    <button role="tab" aria-selected="false">search</button>
    <button role="tab" aria-selected="false">delete</button>
    <button role="tab" aria-selected="false">export</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Liste sessões, mais recente primeiro:

```sh
rousseau session list
rousseau session list --limit 100
rousseau session list --json
```

Colunas: `ID`, `Title`, `Messages`, `UpdatedAt`. A flag `--json` emite um objeto por linha para consumidores em script.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Imprima o transcript completo de uma sessão:

```sh
rousseau session show <session-id>
rousseau session show <session-id> --raw
```

`--raw` imprime o JSON como armazenado (útil para debug). Sem `--raw`, tool calls renderizam como `→ tool_use(name, input)` e resultados como `← tool_result`.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Busca full-text em cada sessão:

```sh
rousseau session search "refactor login"
rousseau session search "TODO" --limit 10
```

Usa o índice FTS5 (veja `internal/state/sqlite/`). Resultados são ranqueados por relevância e incluem um snippet com os termos correspondentes destacados.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Delete uma sessão e suas entradas FTS5:

```sh
rousseau session delete <session-id> --yes
```

A flag `--yes` é obrigatória — sem confirmação interativa. Deleção faz cascade via triggers SQL para que o índice de recall permaneça consistente.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Exporte uma sessão como JSON:

```sh
rousseau session export <session-id> > session.json
```

O formato exportado corresponde ao blob JSON em disco; re-import ainda não é suportado (roadmap).

  </div>
</div>

## Solução de problemas

### `session not found`

O ID que você passou não existe. É case-sensitive. Use `rousseau session list` para ver IDs válidos.

### Busca FTS5 não retorna nada

O índice pode estar desatualizado em sessões legadas importadas antes do FTS5 ser conectado. Reconstrua rodando qualquer operação mutante de conteúdo (uma deleção dispara reindex), ou reindexe manualmente via SQLite.

### `database is locked` em leitura

Outro daemon está segurando um WAL write lock. Use um DSN read-only (`?mode=ro`) se você só precisa ler.

### Store de sessão crescendo rápido demais

Habilite compressão (`agent.compression.enabled: true`) e periodicamente `VACUUM` o arquivo SQLite para recuperar espaço.

### Restore de backup produz estado stale

Garanta que você removeu `-wal` e `-shm` antes de iniciar o daemon. O SQLite reproduzirá o WAL se `-wal` estiver presente, potencialmente desfazendo seu restore.

## Páginas relacionadas

- [Referência: Session store](/pt-BR/reference/session-store/) — schema e DDL.
- [Guias: Gerenciando workspaces](/pt-BR/guides/managing-workspaces/) — stores por workspace.
- [Guias: Gerenciamento de contexto](/pt-BR/guides/context-management/) — como a compressão decide o que manter.
- [Guia do usuário: CLI](/pt-BR/user-guide/cli/) — assinaturas de comando.
- [Guia do usuário: Compressão &amp; Recall](/pt-BR/user-guide/compression-recall/) — internals do compressor e do recall FTS5.

## Leitura adicional

- `internal/cli/session.go` — wiring do CLI.
- `internal/state/sqlite/store.go` — DSN, WAL, índices.
- `internal/agent/session.go` — o struct `Session`.
- `internal/agent/compressor.go` — `LLMCompressor`.
- `internal/agent/recall.go` — `SQLiteRecall`.
