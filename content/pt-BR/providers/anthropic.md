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
description: "Configure the direct Anthropic provider: ANTHROPIC_API_KEY, model IDs, max_tokens, prompt cache markers on the last messages, streaming."
keywords: "Anthropic, ANTHROPIC_API_KEY, Claude API, prompt caching, cache_control, ephemeral, streaming"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/providers/anthropic/"
subtitle: "Direct Anthropic API with ephemeral prompt-cache markers."
tags: "providers, anthropic"
title: "Provedor Anthropic"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Anthropic, ANTHROPIC_API_KEY, Claude API, prompt caching, cache_control, ephemeral, streaming"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Provedor Anthropic"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 7
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/anthropic/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/anthropic/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Provedor Anthropic"
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
twitter_description: "Configure the direct Anthropic provider: ANTHROPIC_API_KEY, model IDs, max_tokens, prompt cache markers on the last messages, streaming."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Provedor Anthropic"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>O formato exato no nível do wire das requisições Anthropic que o rousseau envia, quais blocos de conteúdo recebem marcadores de prompt-cache e por quê, como o streaming mapeia para <code>agent.StreamingProvider</code>, e os modos de falha para respostas 401/429/529. Leia <code>internal/llm/anthropic/client.go</code> e <code>internal/llm/anthropic/cache.go</code> junto a esta página.</p></aside>

## Quando usar o provider Anthropic

O provider direto `anthropic` é a escolha certa quando:

- Você tem uma chave de API Anthropic e quer billing por token em `api.anthropic.com`.
- Você quer execução de tools no lado do rousseau (o `Registry` está totalmente em jogo).
- Você quer optar pelos marcadores efêmeros de prompt-cache em prefixos estáveis.
- Você quer completions com streaming no `rousseau chat` (atualizações token a token no viewport).
- Você quer rate limits explícitos e publicados (ao contrário do modo subscrição do `claudecli`).

## Configuração

```yaml
provider: anthropic

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
  max_tokens: 4096
```

| Campo | Padrão | Efeito |
|---|---|---|
| `api_key` | *de `ANTHROPIC_API_KEY`* | Bearer para `api.anthropic.com`. Rejeitado se vazio quando o provider é selecionado. |
| `model` | `claude-sonnet-4-6` | Identificador do modelo. |
| `max_tokens` | `4096` | Limita os tokens de saída por completion. |

A variável de ambiente `ANTHROPIC_API_KEY` é vinculada a `anthropic.api_key` no momento do carregamento, então exportá-la é equivalente a configurá-la. Operadores de contêiner tipicamente a exportam na linha `Environment=` da unidade systemd em vez de colocá-la no `config.yaml`.

## Identificadores de modelo

O `rousseau-agent` passa `model` literalmente para o SDK. Fixe o ID exato do modelo (`claude-sonnet-4-6`, `claude-opus-4-6`) em produção para que seu tráfego não mude por baixo dos panos quando a Anthropic promover novos snapshots.

## Internos do prompt caching

O cache efêmero de prompt da Anthropic permite marcar blocos de conteúdo com `cache_control: { type: "ephemeral" }`. A API cacheia o prefixo até e incluindo qualquer bloco marcado; turnos subsequentes que carregam o mesmo prefixo pagam uma fração do custo usual de tokens de entrada (10% no momento da escrita — consulte a documentação da Anthropic para o preço atual).

O rousseau aplica marcadores via `applyCacheMarkers` em `internal/llm/anthropic/cache.go`. Duas coisas acontecem quando `CacheableMessages > 0` na `Request` de saída:

1. **O system prompt recebe `cache_control: ephemeral`.** Ele sobrevive a cada turno, então sempre vale a pena cacheá-lo uma vez que você opta. Veja linhas 68–75 de `internal/llm/anthropic/client.go`.
2. **As últimas `CacheableMessages` mensagens** recebem `cache_control: ephemeral` em seu último bloco de texto. Isso mantém uma sessão crescente barata: à medida que novos turnos são anexados, o marcador flutua pela transcrição, mas o prefixo até o marcador anterior ainda está quente.

### Quais blocos são marcados

`markLastTextBlock` percorre o conteúdo de um `MessageParam` de trás para frente e define `CacheControl` no primeiro bloco de texto que encontra. Blocos `tool_use` e `tool_result` são pulados — o SDK os modela como variantes diferentes com seus próprios campos opcionais de `CacheControl`, e texto é o denominador comum seguro. Veja `internal/llm/anthropic/cache.go`.

### Quando compensa

<aside class="admonition" data-type="note"><span class="admonition-title">Economia do cache</span><p>O ponto de equilíbrio depende de quanto o prefixo cacheado é reutilizado. Para um transporte de chat que roda 20–100 turnos por sessão com um system prompt de 5–10 kB (típico com skills carregadas), habilitar o cache tipicamente reduz pela metade a conta de tokens de entrada. Para um job cron one-shot que gera uma única resposta, não economiza nada.</p></aside>

O `Compressor` define `CacheableMessages = len(recentMessages) - 1` após uma reescrita para que o bloco de sumário novo esteja quente em cache no próximo turno. Outros caminhos de código deixam `CacheableMessages = 0`, ou seja, o caching é opt-in por requisição. Embedders devem defini-lo explicitamente ao chamar o provider diretamente.

### Verificando cache hits

A API Anthropic retorna `usage.cache_read_input_tokens` e `usage.cache_creation_input_tokens` em cada resposta. `agent.Usage` atualmente expõe apenas `InputTokens` e `OutputTokens`, então verificar a divisão requer ou habilitar debug logging ou ler a resposta bruta do SDK — isto é uma lacuna de observabilidade conhecida, rastreada em `docs/GAP_ANALYSIS_2026.md`.

## Semântica de streaming

O provider implementa `agent.StreamingProvider`. O `rousseau chat` usa streaming por padrão para que tokens apareçam no viewport TUI conforme chegam. Transportes de chat (WhatsApp, Slack, Discord, …) usam completions não-streaming porque transportes orientados a mensagens fazem batch de entrega de qualquer forma — um stream de delta intermediário seria simplesmente descartado antes da mensagem final ser enviada.

A implementação de streaming em `internal/llm/anthropic/stream.go` consome a union `MessageStreamEvent` do SDK:

| Evento | Como é tratado |
|---|---|
| `message_start` | Emite `agent.StreamEvent{Kind: StreamMessageStart}`. |
| `content_block_start` | Emite `agent.StreamEvent{Kind: StreamContentStart}` com o tipo do bloco. |
| `content_block_delta` | Emite `agent.StreamEvent{Kind: StreamTextDelta, Text: delta.Text}` para texto; eventos `input_json_delta` acumulam em uma entrada parcial de tool-use. |
| `content_block_stop` | Emite `agent.StreamEvent{Kind: StreamContentStop}`. |
| `message_delta` | Carrega o stop reason final e o uso cumulativo. |
| `message_stop` | Fim do stream. |

O TUI Bubble Tea se inscreve nesses eventos via `agent.StreamTurn`, que orquestra o loop de stream/tool-use. Veja `internal/agent/stream_turn.go`.

## Uso de tools

Definições de tools do `Registry` são convertidas para o array `tools` da Anthropic em `toSDKTools`. Políticas de aprovação (`agent.approver`) se aplicam — cada bloco `tool_use` passa por `Approver.Approve` no loop do agente antes da execução. Negações são retornadas ao modelo como blocos `tool_result` com `is_error: true`, para que o modelo possa se adaptar (escolher uma ação diferente, perguntar ao usuário, desistir graciosamente).

<aside class="admonition" data-type="warning"><span class="admonition-title">Formato do schema</span><p>O SDK espera que o <code>input_schema</code> da tool seja um objeto JSON Schema com um campo <code>properties</code> no topo. O <code>tools.Definition</code> do rousseau mapeia 1:1 — veja <code>toSDKTools</code> em <code>internal/llm/anthropic/client.go</code>. Tools customizadas que emitem schemas que não são objeto falharão no momento da requisição.</p></aside>

## Tratamento de rate limits

A API Anthropic retorna:

| Código | Significado | Comportamento do rousseau |
|---|---|---|
| 401 | Chave ruim ou ausente | Falha imediatamente, sem retry. |
| 400 | Requisição ruim (schema, encoding, prompt muito longo) | Falha imediatamente com a mensagem de erro do SDK. |
| 429 | Rate limit por minuto excedido | Aparece como um erro `agent`. `Complete` não retenta. |
| 529 | Sobrecarregado (capacidade transitória) | Aparece como um erro `agent`. `Complete` não retenta. |
| 5xx | Erro do servidor | Aparece como um erro `agent`. `Complete` não retenta. |

**Retentativas são responsabilidade do caller.** O TUI `rousseau chat` e o `RouterHandler` do transporte atualmente não implementam backoff — um 429 mata o turno. Isso é uma escolha deliberada de design: retentativas interagem com a semântica de tool_use (chamadas parciais de tool, idempotência), e o caller tem o contexto para tomar a decisão certa. Veja `docs/GAP_ANALYSIS_2026.md` para o helper de retry planejado.

<aside class="admonition" data-type="tip"><span class="admonition-title">Lidando com 429 em um transporte de chat</span><p>Envelope o <code>RouterHandler</code> do transporte em um loop de retry no nível do caller com backoff exponencial e jitter. O <a href="/pt-BR/guides/rate-limits/">guia de rate limits</a> mostra um exemplo trabalhado.</p></aside>

## Higiene de custo

- **Defina `max_tokens` baixo** (2048–4096) para transportes de chat onde as respostas raramente precisam exceder alguns parágrafos. `max_tokens` é um teto, não um alvo — você paga apenas pela saída realmente gerada.
- **Habilite `agent.compression`** para colapsar mensagens antigas quando a transcrição passar de `trigger_messages` (padrão 60). O sumário é muito mais barato que a transcrição bruta.
- **Use `CacheableMessages > 0`** ao embutir a biblioteca do agente — a API direta é onde o prompt caching mais compensa.
- **Prefira Sonnet para loops de tool-use.** Opus é mais caro e mais lento; a menos que você tenha ganhos medidos em sua tarefa específica, o Sonnet é o padrão por uma razão.
- **Cuidado com billing de aborto de stream.** Se um stream é cancelado no meio da resposta, a API ainda cobra pelos tokens gerados até o ponto do cancelamento. Defina um teto de timeout no seu caller.

## Solução de problemas

### `anthropic: complete: 401 unauthorized`

Sua `ANTHROPIC_API_KEY` está ausente, revogada ou definida para um workspace/organização à qual você não tem mais acesso. Verifique com `curl -H "x-api-key: $ANTHROPIC_API_KEY" https://api.anthropic.com/v1/messages`.

### `anthropic: complete: 400 messages: too many messages`

A transcrição cresceu além da janela de contexto. Habilite `agent.compression.enabled: true` (os padrões geralmente estão bons) e execute novamente. Se a compressão está ativa e ainda dispara, reduza `trigger_messages` ou aumente `keep_recent` para que o compressor dispare mais cedo.

### `anthropic: unsupported content block <type>`

O SDK retornou um tipo de bloco de conteúdo que o rousseau não modela — atualmente apenas `text` e `tool_use` são suportados (veja `fromSDKResponse`). Isso pode acontecer se o modelo emite blocos `thinking` (modo extended thinking). O rousseau ainda não os expõe; desabilite extended thinking na sua configuração de provider até o suporte chegar.

### 429s sob carga sustentada

Você está atingindo o rate limit por minuto de tokens de saída. Opções: (1) solicite um aumento de limite à Anthropic, (2) enfileire turnos no caller e processe-os serialmente, (3) mude para Bedrock ou Vertex onde cotas de empresa geralmente são maiores.

### Misses de prompt cache apesar de `CacheableMessages > 0`

A Anthropic invalida o cache quando o prefixo muda. Causas comuns: o system prompt é regenerado por turno (skills que mudam com cada mensagem do usuário), o ID do modelo mudou, ou `MaxTokens` diferem. Logue o payload da requisição e faça diff entre dois turnos para isolar.

## Páginas relacionadas

- [Providers: claudecli](/pt-BR/providers/claudecli/) — trade-offs de subprocesso vs API direta.
- [Providers: Bedrock](/pt-BR/providers/bedrock/) — Claude gerenciado pela AWS com cotas empresariais.
- [Guias: Rate limits](/pt-BR/guides/rate-limits/) — o playbook de retry e backoff.
- [Loop do agente](/pt-BR/agent-loop/) — como streaming e uso de tools se compõem.
- [Guia do usuário: Compressão e Recall](/pt-BR/user-guide/compression-recall/) — o mecanismo que mantém as contagens de tokens de entrada sãs.

## Leitura complementar

- `internal/llm/anthropic/client.go` — `Complete`, conversão de mensagem, schema de tools.
- `internal/llm/anthropic/stream.go` — implementação de streaming.
- `internal/llm/anthropic/cache.go` — helper de marcadores de cache.
- `internal/agent/stream_turn.go` — como o loop do agente consome eventos de streaming.
- `internal/agent/compressor.go` — como o compressor prepara `CacheableMessages`.
