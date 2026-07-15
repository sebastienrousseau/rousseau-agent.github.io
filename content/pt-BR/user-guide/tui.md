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
description: "Bubble Tea TUI keybindings, panels, spinner and streaming semantics for rousseau-agent's rousseau chat command."
keywords: "tui, bubble tea, keybindings, viewport, textarea, spinner, streaming, session"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/user-guide/tui/"
subtitle: "Bubble Tea keybindings, panels, streaming."
tags: "tui, bubble-tea, keybindings"
title: "TUI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tui, bubble tea, keybindings, viewport, textarea, spinner, streaming, session"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "TUI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/tui/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/tui/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "TUI"
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
twitter_description: "Bubble Tea TUI keybindings, panels, spinner and streaming semantics for rousseau-agent's rousseau chat command."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "TUI"
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

## Visão geral

`rousseau chat` abre uma TUI Bubble Tea com três regiões:

```
+------------------------------------------------------+
|                       Header                         |  session title
+------------------------------------------------------+
|                                                      |
|                                                      |
|                     Viewport                         |  scrollable history
|          (messages, streamed reply preview)          |
|                                                      |
|                                                      |
+------------------------------------------------------+
|                     Textarea                         |  input, Enter to send
+------------------------------------------------------+
| status: idle | spinner | streaming | error           |
+------------------------------------------------------+
```

Roda no modo alt-screen do Bubble Tea — a TUI assume o buffer do terminal e o restaura na saída.

## Keybindings

A TUI do rousseau mantém o conjunto de bindings pequeno. Em caso de dúvida, os atalhos padrão de viewport / textarea do Bubble Tea se aplicam.

### Global

| Tecla | Ação |
|---|---|
| `Ctrl+C` | Sai. Salva a sessão atual, não imprime nada na saída. |
| `Esc` | Sai. Mesmo que `Ctrl+C`. |
| `Enter` | Envia o conteúdo atual do textarea. No-op enquanto o agente está ocupado. |

### Textarea (entrada)

Comportamento padrão de textarea do Bubble Tea:

| Tecla | Ação |
|---|---|
| Qualquer caractere imprimível | Insere no cursor. |
| `Backspace` | Apaga caractere antes do cursor. |
| `Delete` | Apaga caractere sob o cursor. |
| Teclas de seta | Move cursor. |
| `Home` / `End` | Vai para o início / fim da linha. |
| `Ctrl+A` / `Ctrl+E` | Vai para o início / fim da linha (bindings Emacs). |
| `Ctrl+U` | Kill até o início da linha. |
| `Ctrl+K` | Kill até o fim da linha. |
| `Shift+Enter` | (Dependente do terminal) newline sem submeter; frequentemente mapeado como `\n` literal. |

O textarea cresce verticalmente conforme o conteúdo quebra; o viewport encolhe para acomodar.

### Viewport (histórico)

O viewport suporta os atalhos usuais de viewport do Bubble Tea. O foco fica no viewport quando o textarea está vazio; digitação é roteada para o textarea automaticamente.

| Tecla | Ação |
|---|---|
| `PgUp` / `PgDn` | Rola uma página. |
| `↑` / `↓` | Rola uma linha. |
| `Home` / `End` | Vai para o topo / final. |
| Roda do mouse | Rola. |

## Semântica dos painéis

### Header

`rousseau · <session title>`. O título vem de `--title` quando a sessão foi criada (padrão: `chat YYYY-MM-DD HH:MM`).

### Viewport

Histórico renderizado mais, enquanto um turno está em voo, um **preview de streaming** no fundo. O preview reflete deltas conforme o provider faz streaming; quando o turno termina, o preview é substituído pela mensagem final do assistente.

Cada mensagem é prefixada por seu role (`you`, `rousseau`, `tool`) para que o fluxo seja inequívoco quando o modelo solicita uma tool call.

### Textarea

Texto de placeholder: `Ask, or press Ctrl+C to quit…`. Enter submete; o textarea reseta ao submeter.

Enquanto o agente está ocupado, `Enter` é um no-op para que double-submits acidentais não empilhem turnos.

### Linha de status

Debaixo do textarea. Conteúdo varia:

| Estado | Linha |
|---|---|
| Ocioso | Vazio. |
| Ocupado | Spinner + `thinking…`. Ticks de spinner vêm de `bubbles/spinner`. |
| Streaming | Spinner continua; o delta de streaming aparece no preview do viewport. |
| Erro | String de erro em vermelho. O próximo turno bem-sucedido a limpa. |

## Persistência de sessão

Cada turno é persistido em `~/.local/share/rousseau/sessions.db` via `state.Store.Save`. Se o daemon crashar no meio do turno:

- O turno do usuário já foi salvo (foi anexado antes de `doTurn` disparar).
- A resposta do assistente só é salva quando o turno completa.

No restart, `rousseau chat --session <id>` retoma do último estado salvo com sucesso.

## Comandos de sessão pelo CLI

A TUI não expõe cada operação de sessão. Gerencie sessões pelo shell:

```sh
rousseau session list
rousseau session show <id>
rousseau session search "kubectl"
rousseau session delete <id>
```

## Semântica de streaming

Providers que implementam `StreamingProvider.ChatStream` (Anthropic, `claudecli`) fazem streaming de deltas no preview do viewport. Providers que só implementam `Provider.Chat` (Bedrock, Vertex, OpenAI-compatible dependendo do shim) entregam a resposta como um bloco único na conclusão do turno — o preview fica vazio e a resposta aparece quando `busy` se torna `false`.

## Quando as coisas dão errado

- **A TUI trava** — `Ctrl+C` duas vezes. O primeiro `Ctrl+C` sinaliza `tea.Quit`, que faz flush do estado. O segundo é capturado pelo OS.
- **O viewport está vazio e o textarea não aceita entrada** — a alt-screen pode ter sido corrompida por um subprocesso emissor de escape-sequence (por exemplo, uma tool call que imprime códigos ANSI). Reinicie a TUI.
- **A linha de status fica em `thinking…`** — o provider não retornou. Verifique o stderr do daemon (o rousseau escreve slog em stderr; se você o piped em outro lugar, traga de volta).

## Próximo

- [Guia do usuário: CLI](/pt-BR/user-guide/cli/) — cada comando fora da TUI.
- [Conceitos](/pt-BR/concepts/) — o agent loop por baixo.
- [Compressão + Recall](/pt-BR/user-guide/compression-recall/) — como chats longos permanecem utilizáveis.
