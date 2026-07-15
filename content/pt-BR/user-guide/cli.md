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
description: "Full CLI reference for rousseau-agent: every command, every flag, exit codes, per-transport subcommands."
keywords: "cli, cobra, commands, flags, subcommands, exit codes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/user-guide/cli/"
subtitle: "Every command, every flag."
tags: "cli, reference, commands"
title: "Referência CLI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cli, cobra, commands, flags, subcommands, exit codes"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referência CLI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 40
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/cli/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/cli/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Referência CLI"
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
twitter_description: "Full CLI reference for rousseau-agent: every command, every flag, exit codes, per-transport subcommands."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Referência CLI"
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

## Invocação

```
rousseau [--config <path>] <command> [flags]
```

Cada comando lê os padrões de `~/.config/rousseau/config.yaml` (ou do arquivo passado via `--config`). Flags sobrescrevem variáveis de ambiente, variáveis de ambiente sobrescrevem o arquivo, o arquivo sobrescreve os padrões hard-coded.

## Flags globais

| Flag | Tipo | Padrão | Notas |
|---|---|---|---|
| `--config` | string | `$XDG_CONFIG_HOME/rousseau/config.yaml` | Carrega a configuração deste arquivo. Ausente significa o caminho XDG padrão. |
| `--help`, `-h` | bool | — | Imprime a ajuda para o comando atual. |

## Árvore de comandos

```
rousseau
├── chat                Bubble Tea TUI
├── whatsapp            WhatsApp bridge (whatsmeow)
├── signal              Signal bridge (signal-cli JSON-RPC)
├── telegram            Telegram Bot API long-polling
├── matrix              Matrix client-server API
├── slack               Slack Socket Mode
├── discord             Discord Gateway
├── sms                 SMS send-only (Twilio / Vonage)
├── imessage            BlueBubbles-backed iMessage bridge
├── email               IMAP inbound + SMTP outbound
├── mcp                 MCP JSON-RPC 2.0 server over stdio
├── cron                Manage scheduled prompts
├── session             Inspect / delete session store
├── skills              List / show / lint skills
├── doctor              Diagnose the local installation
├── status              Print daemon status
├── init                Write a default config to ~/.config/rousseau/
└── version             Print version, commit, build date
```

## `rousseau chat`

Abre a TUI interativa Bubble Tea.

| Flag | Tipo | Padrão | Notas |
|---|---|---|---|
| `--session` | string | — | Retoma uma sessão existente pelo ID. |
| `--title` | string | timestamp | Título para uma nova sessão. |

## `rousseau whatsapp`

Executa o bridge do WhatsApp. Imprime um QR code no primeiro launch.

| Flag | Tipo | Padrão | Notas |
|---|---|---|---|
| `--store` | string | `$XDG_DATA_HOME/rousseau/whatsapp.db` | Caminho para o device store do whatsmeow. |
| `--allow` | []string | nenhum | Restringe o tratamento de inbound a esses JIDs. Repetível. **Nunca deixe vazio em um número público.** |

## `rousseau signal`

Executa o bridge do Signal. Spawna `signal-cli jsonRpc` como subprocesso.

| Flag | Tipo | Padrão | Notas |
|---|---|---|---|
| `--account` | string | de `signal.account` | Número de telefone E.164 sob o qual o daemon roda. |
| `--binary` | string | `signal-cli` | Caminho para o executável signal-cli. |
| `--allow` | []string | nenhum | Restringe inbound a esses números E.164. |

## `rousseau telegram`

Executa o long-poller da Telegram Bot API.

| Flag | Tipo | Padrão | Notas |
|---|---|---|---|
| `--token` | string | de `telegram.token` | Token do BotFather. |
| `--allow` | []string | nenhum | Restringe inbound a esses chat IDs. |

## `rousseau matrix`

Executa o bridge do Matrix.

| Flag | Tipo | Padrão | Notas |
|---|---|---|---|
| `--homeserver-url` | string | da config | por exemplo, `https://matrix.org`. |
| `--access-token` | string | da config | Access token do bot. |
| `--user-id` | string | da config | User ID Matrix do bot (`@bot:matrix.org`). |
| `--allow` | []string | nenhum | Restringe inbound a esses user IDs. |

## `rousseau slack`

Executa o bridge Socket Mode do Slack.

| Flag | Tipo | Padrão | Notas |
|---|---|---|---|
| `--app-token` | string | da config | Token Socket Mode `xapp-...`. |
| `--bot-token` | string | da config | Token Bot User OAuth `xoxb-...`. |
| `--allow` | []string | nenhum | Restringe inbound a esses user IDs do Slack. |

## `rousseau discord`

Executa o bridge Discord Gateway.

| Flag | Tipo | Padrão | Notas |
|---|---|---|---|
| `--token` | string | da config | Token do bot. |
| `--allow` | []string | nenhum | Restringe inbound a esses user IDs do Discord. |

## `rousseau sms`

SMS somente de envio via Twilio ou Vonage. Sem inbound.

| Flag | Tipo | Padrão | Notas |
|---|---|---|---|
| `--provider` | string | da config | `twilio` ou `vonage`. |
| `--from` | string | da config | Número E.164 remetente. |
| `--account-sid` | string | da config | Account SID do Twilio. |
| `--auth-token` | string | da config | Auth token do Twilio ou secret do Vonage. |
| `--api-key` | string | da config | API key do Vonage. |

## `rousseau imessage`

Bridge de iMessage por BlueBubbles.

| Flag | Tipo | Padrão | Notas |
|---|---|---|---|
| `--base-url` | string | `http://localhost:1234` | URL do servidor BlueBubbles. |
| `--password` | string | da config | Senha do servidor BlueBubbles. |
| `--chat-guid` | string | da config | Alvo de outbound. |
| `--poll-interval` | duration | 5s | Frequência de poll para novas mensagens. |
| `--allow` | []string | nenhum | Restringe inbound. |

## `rousseau email`

Bridge de email sobre IMAP + SMTP.

| Flag | Tipo | Padrão | Notas |
|---|---|---|---|
| `--imap-addr` | string | da config | por exemplo, `imap.example.com:993`. |
| `--imap-username`, `--imap-password` | string | da config | Credenciais IMAP. |
| `--smtp-addr` | string | da config | por exemplo, `smtp.example.com:587`. |
| `--smtp-username`, `--smtp-password` | string | da config | Credenciais SMTP. |
| `--from` | string | da config | Envelope sender. |
| `--poll-interval` | duration | 30s | Cadência de poll IMAP. |
| `--allow` | []string | nenhum | Restringe endereços de remetente inbound. |

## `rousseau mcp`

Inicia o servidor MCP em stdio. Sem flags — cada knob vive em `config.yaml`.

## `rousseau cron`

| Subcomando | Descrição |
|---|---|
| `cron add` | Adiciona um prompt agendado. Flags: `--name`, `--schedule` (cron de 5 campos), `--prompt`, `--deliver-to`. |
| `cron list` | Lista cada job com status `on/off` e timestamp da última execução. |
| `cron remove <name-or-id>` | Deleta um job. |
| `cron enable <name-or-id>` | Habilita um job desabilitado. |
| `cron disable <name-or-id>` | Desabilita um job habilitado (sem deletar). |

## `rousseau session`

| Subcomando | Descrição |
|---|---|
| `session list` | Lista sessões no store, mais recente primeiro. |
| `session search <query>` | Busca FTS5 no conteúdo de mensagens de cada sessão. |
| `session show <id>` | Imprime o histórico de mensagens de uma sessão. |
| `session delete <id>` | Deleta uma sessão. |

## `rousseau skills`

| Subcomando | Descrição |
|---|---|
| `skills list` | Lista skills descobertas em `skills_dir`. |
| `skills show <name>` | Imprime o front-matter YAML e o corpo de uma skill. |
| `skills lint` | Valida skills quanto à conformidade de schema. |

## `rousseau doctor`

Percorre cada dependência de runtime e cada escolha de config. Imprime um relatório de status com linhas marcadas como `ok`, `warn`, `fail`, `info`. Código de saída 1 se qualquer linha for `fail`.

Sem flags hoje; estenda via `--config` no nível global.

## `rousseau status`

Imprime um sumário compacto de status do daemon — provider, contagem de sessões, jobs de cron. Somente leitura.

## `rousseau init`

Escreve um `config.yaml` padrão em `~/.config/rousseau/`. Recusa sobrescrever um arquivo existente a menos que `--force` seja passado.

| Flag | Tipo | Padrão | Notas |
|---|---|---|---|
| `--force` | bool | false | Sobrescreve uma config existente. |

## `rousseau version`

Imprime versão, hash de commit e data de build. Estampados no momento de build via `-ldflags`.

## Códigos de saída

| Código | Significado |
|---|---|
| 0 | Comando completado com sucesso. |
| 1 | Comando falhou. O erro é impresso em stderr. |

Veja [Referência: Códigos de saída](/pt-BR/reference/exit-codes/) para a semântica de sinais do daemon.

## Variáveis de ambiente

Todo campo de config pode ser sobrescrito por uma variável de ambiente usando o prefixo `ROUSSEAU_` e `_` como separador de seção: `ROUSSEAU_LOG_LEVEL=debug`, `ROUSSEAU_ANTHROPIC_API_KEY=sk-ant-...`, etc.

O caso especial é `ANTHROPIC_API_KEY` (sem prefixo) — é lido diretamente pelo config loader para casar com a convenção.

## Solução de problemas

### `unknown command` ao passar um subcomando

Os subcomandos do rousseau são declarados em `internal/cli/root.go`. Se `rousseau <cmd>` reporta unknown, ou a flag está mal escrita ou você está em um binário antigo. `rousseau version` mostra o que você tem.

### Flags repetíveis precisam de múltiplas invocações

`--allow` aceita um JID por flag. Repita a flag para múltiplos valores: `--allow A --allow B`, não `--allow A,B`.

### Variáveis de ambiente silenciosamente ignoradas

O rousseau usa prefixo `ROUSSEAU_` + separador de seção com underscore: `anthropic.model` vira `ROUSSEAU_ANTHROPIC_MODEL`. Case importa.

### `rousseau chat` mostra só uma tela em branco

A TUI Bubble Tea precisa de um terminal com suporte ANSI. Defina `TERM=xterm-256color` e rode interativamente (não sob `nohup` ou um pipe).

### Comando sai com 0 imediatamente

Algumas flags (`--help`, variantes de `--version`) fazem short-circuit. Se seu comando não roda, verifique as flags que você passou.

## Páginas relacionadas

- [Guia do usuário: TUI](/pt-BR/user-guide/tui/) — keybindings dentro do `rousseau chat`.
- [Guia do usuário: Tools](/pt-BR/user-guide/tools/) — schema JSON de cada ferramenta embutida.
- [Referência: Comandos CLI](/pt-BR/reference/cli-commands/) — tabela de comandos.
- [Referência: Variáveis de ambiente](/pt-BR/reference/environment-variables/) — matriz de override.
- [Configuração](/pt-BR/configuration/) — o arquivo de config por trás de cada comando.

## Leitura adicional

- `internal/cli/root.go` — a árvore Cobra.
- `internal/cli/chat.go`, `internal/cli/whatsapp.go`, `internal/cli/slack.go`, … — um arquivo por subcomando.
- `internal/config/config.go` — resolução de env var / flag.
