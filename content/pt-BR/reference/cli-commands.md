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
description: "Compact reference table of every rousseau-agent command mirroring the output of rousseau --help."
keywords: "cli, commands, reference, table, rousseau --help"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/reference/cli-commands/"
subtitle: "Every command tabulated."
tags: "reference, cli, commands"
title: "Comandos CLI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "cli, commands, reference, table, rousseau --help"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Comandos CLI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 50
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/cli-commands/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/cli-commands/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Comandos CLI"
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
twitter_description: "Compact reference table of every rousseau-agent command mirroring the output of rousseau --help."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Comandos CLI"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>A superfície completa da CLI <code>rousseau</code>: cada comando, suas flags, semântica de código de saída e as chaves de config que cada flag sobrescreve. Esta é a referência escaneável — veja <a href="/pt-BR/user-guide/cli/">Guia do usuário: CLI</a> para um walkthrough com exemplos trabalhados.</p></aside>

## Árvore de comandos

Cada comando mostra sua ajuda via `rousseau <cmd> --help`. Esta página é o resumo tabulado.

| Comando | Descrição |
|---|---|
| `chat` | Abre a TUI Bubble Tea interativa. |
| `whatsapp` | Roda o bridge WhatsApp (whatsmeow). |
| `signal` | Roda o bridge Signal (signal-cli JSON-RPC). |
| `telegram` | Roda o long-poller da Bot API do Telegram. |
| `matrix` | Roda o bridge cliente-servidor do Matrix. |
| `slack` | Roda o bridge Slack Socket Mode. |
| `discord` | Roda o bridge Discord Gateway. |
| `sms` | SMS apenas de envio via Twilio ou Vonage. |
| `imessage` | Bridge iMessage apoiado em BlueBubbles. |
| `email` | Bridge IMAP inbound + SMTP outbound. |
| `mcp` | Inicia o servidor MCP JSON-RPC 2.0 em stdio. |
| `cron add` | Adiciona um prompt agendado. |
| `cron list` | Lista cada job agendado. |
| `cron remove` | Deleta um job agendado. |
| `cron enable` | Habilita um job agendado desabilitado. |
| `cron disable` | Desabilita um job agendado habilitado. |
| `session list` | Lista sessões no store, mais novas primeiro. |
| `session search` | Busca FTS5 no conteúdo das mensagens de cada sessão. |
| `session show` | Imprime o histórico de mensagens de uma sessão. |
| `session delete` | Deleta uma sessão. |
| `skills list` | Lista skills descobertos de `skills_dir`. |
| `skills show` | Imprime o front-matter YAML e o corpo de um skill. |
| `skills lint` | Valida skills para conformidade com o schema. |
| `doctor` | Diagnostica a instalação local. Imprime um relatório. |
| `status` | Imprime o status do daemon. |
| `init` | Escreve uma config padrão em `~/.config/rousseau/`. |
| `version` | Imprime versão, commit e data de build. |

## Flags globais

Cada comando aceita estas:

| Flag | Tipo | Chave de config | Notas |
|---|---|---|---|
| `--config` | string | — | Carrega a configuração deste arquivo. Padrão: `$XDG_CONFIG_HOME/rousseau/config.yaml`. |
| `--help`, `-h` | bool | — | Imprime a ajuda para o comando atual. |

## Flags por transporte

### `rousseau whatsapp`

| Flag | Tipo | Chave de config | Notas |
|---|---|---|---|
| `--store` | string | — | Caminho para o device store do whatsmeow. Padrão `$XDG_DATA_HOME/rousseau/whatsapp.db`. |
| `--allow` | []string | `whatsapp.allowlist` | Restringe o inbound a esses JIDs. Repetível. |

### `rousseau slack`

| Flag | Tipo | Chave de config |
|---|---|---|
| `--app-token` | string | `slack.app_token` |
| `--bot-token` | string | `slack.bot_token` |
| `--bot-user-id` | string | `slack.bot_user_id` |
| `--allow` | []string | `slack.allowlist` |

### `rousseau discord`

| Flag | Tipo | Chave de config |
|---|---|---|
| `--token` | string | `discord.token` |
| `--allow` | []string | `discord.allowlist` |

### `rousseau telegram`

| Flag | Tipo | Chave de config |
|---|---|---|
| `--token` | string | `telegram.token` |
| `--allow` | []string | `telegram.allowlist` |

### `rousseau matrix`

| Flag | Tipo | Chave de config |
|---|---|---|
| `--homeserver-url` | string | `matrix.homeserver_url` |
| `--access-token` | string | `matrix.access_token` |
| `--user-id` | string | `matrix.user_id` |
| `--allow` | []string | `matrix.allowlist` |

### `rousseau signal`

| Flag | Tipo | Chave de config |
|---|---|---|
| `--account` | string | `signal.account` |
| `--binary` | string | `signal.binary` |
| `--allow` | []string | `signal.allowlist` |

### `rousseau email`

| Flag | Tipo | Chave de config |
|---|---|---|
| `--imap-addr` | string | `email.imap_addr` |
| `--imap-username` | string | `email.imap_username` |
| `--imap-password` | string | `email.imap_password` |
| `--smtp-addr` | string | `email.smtp_addr` |
| `--smtp-username` | string | `email.smtp_username` |
| `--smtp-password` | string | `email.smtp_password` |
| `--from` | string | `email.from` |
| `--mailbox` | string | `email.mailbox` |
| `--poll-interval` | string | `email.poll_interval` |

### `rousseau sms`

| Flag | Tipo | Chave de config |
|---|---|---|
| `--provider` | string | `sms.provider` |
| `--from` | string | `sms.from` |
| `--to` | string | (positional) |

### `rousseau imessage`

| Flag | Tipo | Chave de config |
|---|---|---|
| `--base-url` | string | `imessage.base_url` |
| `--password` | string | `imessage.password` |
| `--chat-guid` | string | `imessage.chat_guid` |

## Códigos de saída

| Código | Significado |
|---|---|
| 0 | Saída limpa — comando completou. Não é típico para daemons de longa duração (eles geralmente terminam em sinal). |
| 1 | Qualquer erro que surge de `Execute`. Veja [Referência: Códigos de saída](/pt-BR/reference/exit-codes/) para a classificação. |

## Precedência

Valores de config são resolvidos na ordem **flag &gt; env &gt; arquivo &gt; padrão** (veja `config.Load` em `internal/config/config.go`). Variáveis de ambiente têm prefixo `ROUSSEAU_` com pontos substituídos por underscores — ex. `ROUSSEAU_ANTHROPIC_MODEL` sobrescreve `anthropic.model`. A variável de ambiente simples `ANTHROPIC_API_KEY` também é honrada (caso especial em `config.Load`).

## Solução de problemas

### `unknown flag: --allow` em `rousseau chat`

`--allow` é escopado por transporte. `chat` não tem allowlist porque não há ingresso. Use `rousseau whatsapp --allow …`.

### A ordem das flags importa para flags repetíveis

`--allow A --allow B` são dois valores, mas `--allow=A,B` é um valor que por acaso contém uma vírgula. Prefira flags separadas.

### Override de env não pego

O rousseau lê o env apenas no start. Reinicie o daemon depois de mudar variáveis de ambiente, ou use `--config` para forçar um recarregamento.

### `flag provided but not defined`

O Cobra rejeita flags desconhecidas. Se você copia uma flag de uma versão mais nova, verifique `rousseau <cmd> --help` para a grafia atual.

## Páginas relacionadas

- [Guia do usuário: CLI](/pt-BR/user-guide/cli/) — cada comando com exemplos trabalhados.
- [Referência: Códigos de saída](/pt-BR/reference/exit-codes/) — semântica de sinais.
- [Referência: Schema de config](/pt-BR/reference/config-schema/) — cada campo de configuração.
- [Referência: Variáveis de ambiente](/pt-BR/reference/environment-variables/) — matriz de override de env.
- [Configuração](/pt-BR/configuration/) — o walkthrough completo do arquivo de config.

## Leitura adicional

- `internal/cli/root.go` — árvore de comandos Cobra.
- `internal/cli/*.go` — um arquivo por subcomando.
- `internal/config/config.go` — `Load` e resolução de defaults.
