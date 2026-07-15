---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "How the LLM compressor decides what to keep, the roles of trigger_messages and keep_recent, and a before/after diagram of a compressed session."
keywords: "compression, context, keep_recent, trigger_messages, summariser, marker"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/context-management/"
subtitle: "trigger_messages, keep_recent, and the compressed-marker convention."
tags: "guides, context, compression, summariser"
title: "Guia: gestão de contexto"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "compression, context, keep_recent, trigger_messages, summariser, marker"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: gestão de contexto"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/context-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/context-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guia: gestão de contexto"
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
twitter_description: "How the LLM compressor decides what to keep, the roles of trigger_messages and keep_recent, and a before/after diagram of a compressed session."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guia: gestão de contexto"
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

## O problema

Uma sessão que roda por semanas acumula centenas de mensagens. Cada uma é reenviada ao provider a cada turno. O custo cresce linearmente com a contagem de turnos; a latência também. O `LLMCompressor` do rousseau (`internal/agent/compressor.go`) troca um pequeno custo pontual — uma chamada de sumarização por compressão — por economia permanente em cada turno subsequente.

A compressão está **desligada por padrão** porque a implantação de referência usa `claudecli` em tier por assinatura, onde a contagem de tokens não é cobrada. Ligue-a ao rodar contra Anthropic direct, Bedrock, Vertex, ou providers compatíveis com OpenAI pagos por token.

## Os botões

De `CompressionConfig` em `internal/config/config.go`:

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60        # zero uses the default 60
    keep_recent: 8              # zero uses the default 8
    prompt: ""                  # overrides the default summariser prompt
```

Significados:

| Campo | O que faz |
|---|---|
| `enabled` | Liga a compressão. Quando false, o agente usa `NoopCompressor` e toda esta seção é no-op. |
| `trigger_messages` | A compressão dispara quando `len(session.Messages) >= trigger_messages`. |
| `keep_recent` | Número de mensagens mais recentes preservadas na íntegra após a compressão. |
| `prompt` | Sobrescreve o prompt padrão do sumarizador. Defina apenas se você precisar de instruções customizadas (ex. preservar saída JSON, sempre citar caminhos de arquivo). |

## O prompt padrão do sumarizador

```
Summarise the following conversation in <=200 words. Preserve every
commitment, TODO, credential, filename, and quoted output. Skip
pleasantries. Return only the summary — no preamble.
```

Definido como `defaultSummaryPrompt` em `internal/agent/compressor.go`. Sobrescreva com `agent.compression.prompt` em `config.yaml`.

## Antes / depois

A session of 68 messages, `trigger_messages: 60`, `keep_recent: 8`:

```
Before compression:                        After compression:

┌──────────────────────────┐              ┌──────────────────────────────┐
│ msg[0]  user             │              │ msg[0]  user (synthetic)     │
│ msg[1]  assistant        │              │   [rousseau-compressed]      │
│ msg[2]  user             │              │   (summary of prior 60       │
│  …  (60 messages)        │      →       │    messages): …              │
│ msg[59] assistant        │              ├──────────────────────────────┤
├──────────────────────────┤              │ msg[1]  user       — verbatim │
│ msg[60] user   verbatim  │              │ msg[2]  assistant  — verbatim │
│ msg[61] assistant        │              │ msg[3]  user       — verbatim │
│  …                       │              │ msg[4]  assistant  — verbatim │
│ msg[67] assistant        │              │ msg[5]  user       — verbatim │
└──────────────────────────┘              │ msg[6]  assistant  — verbatim │
                                          │ msg[7]  user       — verbatim │
                                          │ msg[8]  assistant  — verbatim │
                                          └──────────────────────────────┘
Total messages: 68                        Total messages: 9
Input tokens: ~5000 per turn              Input tokens: ~800 per turn
```

## O marcador

O compressor prefixa a mensagem sintética de usuário com `[rousseau-compressed]` (constante `DefaultCompressorMarker` em `internal/agent/compressor.go`). Em turnos subsequentes, `headAlreadyCompressed()` usa o marcador para detectar um prefixo já comprimido e pula a compressão repetida a menos que a sessão tenha crescido para `2 * trigger_messages`.

É isso que mantém a compressão limitada — você não paga para re-sumarizar o resumo a cada 60 mensagens.

## Escolhendo valores

| Situação | Recomendado |
|---|---|
| Daemon de transporte de longa duração em provider pago. | `trigger_messages: 60`, `keep_recent: 8`. Padrões estão ajustados para isso. |
| TUI interativa em que você quer tudo no contexto. | `enabled: false`. |
| Sessões altamente técnicas com muito código / logs citados. | `trigger_messages: 40`, `keep_recent: 12`. Preserve mais contexto recente; comprima antes. |
| Sumarizador batch crítico em custo (cron). | Cada rodada de cron é uma sessão fresca, então a compressão raramente dispara. Deixe os padrões ligados. |

## Custo de uma passada de compressão

Uma chamada de sumarização por disparo. O Provider usado é o que `Config.Provider` seleciona — o mesmo que o agente usa. Isso significa:

- Chamada do compressor em modelo classe Sonnet: ~1-2 segundos, aproximadamente o custo de ~2 turnos de tokens de entrada.
- Break-even depois de ~5-10 turnos subsequentes, dependendo da forma da sessão.

Para um compressor mais barato, rode o rousseau no padrão multi-provider de dois daemons com um modelo classe Haiku para o daemon compressor. Veja [Guias: Multi-provider](/pt-BR/guides/multi-provider/).

## Emergência: sessão grande demais para carregar

Se o payload de uma sessão crescer além da janela de contexto do modelo antes que a compressão dispare — raro, mas possível com um `trigger_messages` muito pequeno e saídas de tool grandes — o próximo turno vai falhar com um erro de provider "context length exceeded". Recuperação:

```sh
rousseau session delete <id> --yes
```

E comece de novo. Ou reduza manualmente via SQLite:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
UPDATE sessions SET payload = json_set(payload, '$.messages',
  json_extract(payload, '$.messages[-8:]'))
WHERE id = '<session-id>';
SQL
```

Nota: a sintaxe exata do path JSON depende da versão do SQLite. Confirme com um `SELECT payload` primeiro.

## Relacionados

- [Guia do usuário: Compressão + Recall](/pt-BR/user-guide/compression-recall/) — referência mais profunda.
- [Guias: Rate limits](/pt-BR/guides/rate-limits/) — implicações de custo.
- [Guias: Gerenciamento de sessão](/pt-BR/guides/session-management/) — ciclo de vida da sessão.
- [Referência: Schema de config](/pt-BR/reference/config-schema/) — cada campo.
