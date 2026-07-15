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
description: "Configure OpenAI-compatible endpoints: OpenAI, OpenRouter, Ollama, self-hosted vLLM or LM Studio. BaseURL, model naming, streaming, and Ollama's not-required key."
keywords: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, base_url, chat completions, API key, streaming"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/providers/openai-compatible/"
subtitle: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, and any Chat Completions clone."
tags: "providers, openai, openrouter, ollama"
title: "Provedor compatível com OpenAI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, base_url, chat completions, API key, streaming"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Provedor compatível com OpenAI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 10
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/openai-compatible/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/openai-compatible/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Provedor compatível com OpenAI"
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
twitter_description: "Configure OpenAI-compatible endpoints: OpenAI, OpenRouter, Ollama, self-hosted vLLM or LM Studio. BaseURL, model naming, streaming, and Ollama's not-required key."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Provedor compatível com OpenAI"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>Como o provider <code>openai</code> do rousseau serve seis endpoints diferentes (OpenAI, OpenRouter, Ollama, vLLM, LM Studio, LiteLLM) através de uma única implementação, o valor exato de <code>base_url</code> e <code>model</code> para cada um e quais endpoints suportam uso de tools. Leia <code>internal/llm/openai/client.go</code> junto a esta página.</p></aside>

## Uma implementação, muitos endpoints

`internal/llm/openai/` fala a API OpenAI Chat Completions. Como `base_url` é configurável, o mesmo código serve cada endpoint compatível com OpenAI: a própria OpenAI, OpenRouter, together.ai, DeepInfra, vLLM auto-hospedado, o shim OpenAI do Ollama, LM Studio e LiteLLM.

O nome do provider é um de `openai`, `openrouter` ou `ollama` — cada um corresponde ao seu próprio bloco de configuração com um `base_url` pré-configurado (veja `setDefaults` em `internal/config/config.go`). Use `openai` como o slot genérico e sobrescreva `base_url` ao apontar para um backend auto-hospedado.

## Receitas de endpoints

<div class="tabs" data-tabs="openai-compat-endpoints">
  <div class="tab-list" role="tablist" aria-label="OpenAI-compatible endpoint">
    <button role="tab" aria-selected="true">OpenAI</button>
    <button role="tab" aria-selected="false">OpenRouter</button>
    <button role="tab" aria-selected="false">Ollama</button>
    <button role="tab" aria-selected="false">vLLM</button>
    <button role="tab" aria-selected="false">LM Studio</button>
    <button role="tab" aria-selected="false">LiteLLM</button>
  </div>
  <div class="tab-panel" role="tabpanel">

OpenAI direto. `api.openai.com/v1` é o padrão do SDK — nenhuma sobrescrita de `base_url` é necessária.

```yaml
provider: openai

openai:
  api_key: sk-...
  model: gpt-5
  max_tokens: 4096
```

Uso de tools: sim (array `tools` nativo). Streaming: sim (SSE).

<aside class="admonition" data-type="note"><span class="admonition-title">Nomenclatura de modelo</span><p>IDs de modelo seguem a própria nomenclatura da OpenAI (<code>gpt-4o</code>, <code>gpt-5</code>, <code>o1</code>, <code>o3-mini</code>). Fixe IDs exatos em produção — aliases podem mudar por baixo.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

O OpenRouter agrega dezenas de providers atrás de uma API. IDs de modelo usam a convenção `provider/model`:

```yaml
provider: openrouter

openrouter:
  api_key: sk-or-...
  model: anthropic/claude-sonnet-4-6
```

`base_url` tem padrão `https://openrouter.ai/api/v1`. Uso de tools depende do provider subjacente — modelos Anthropic e OpenAI funcionam, a maioria dos modelos open-weights não.

<aside class="admonition" data-type="tip"><span class="admonition-title">Modelos free-tier</span><p>O OpenRouter expõe variantes free-tier (sufixo <code>:free</code>) para experimentação. Rate limits e cotas diárias se aplicam.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

O Ollama local expõe um shim compatível com Chat Completions em `http://localhost:11434/v1`:

```yaml
provider: ollama

ollama:
  model: llama3.1:8b
```

`ollama.api_key` tem padrão `not-required` (o shim o ignora, mas o SDK rejeita strings vazias — veja `New` em `internal/llm/openai/client.go`). `ollama.base_url` tem padrão `http://localhost:11434/v1`.

Uso de tools: sim a partir do Ollama 0.4+ (via array `tools` na requisição Chat Completions). Builds mais antigas retornam texto puro.

<aside class="admonition" data-type="warning"><span class="admonition-title">Latência</span><p>Ollama somente em CPU em um laptop pode levar dezenas de segundos por turno. Defina o timeout HTTP do seu caller acima de 60s ou use um host com GPU.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

vLLM é o motor auto-hospedado grau de produção. Inicie-o com `--api-key` se quiser autenticação:

```sh
python -m vllm.entrypoints.openai.api_server \
  --model mistralai/Mixtral-8x22B-Instruct-v0.1 \
  --host 0.0.0.0 --port 8000 \
  --api-key sk-vllm-secret
```

```yaml
provider: openai

openai:
  api_key: sk-vllm-secret
  base_url: http://vllm.internal:8000/v1
  model: mistralai/Mixtral-8x22B-Instruct-v0.1
  max_tokens: 4096
```

Uso de tools: sim para modelos com um chat template de tool-use (`Hermes-2-Pro`, `Mistral-Nemo`, `Llama-3.1-8B-Instruct` e superiores). Streaming: sim. Veja [Guias: vLLM auto-hospedado](/pt-BR/guides/self-hosted-vllm/) para a implantação completa.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

O LM Studio entrega um servidor compatível com OpenAI em `http://localhost:1234/v1`:

```yaml
provider: openai

openai:
  api_key: not-required
  base_url: http://localhost:1234/v1
  model: lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF
```

Uso de tools: **não** suportado nas builds atuais (a partir de meados de 2026). O endpoint aceita um array `tools`, mas o ignora e retorna texto puro. Use para cargas somente-chat ou espere o recurso chegar.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

LiteLLM é um proxy que fica na frente de muitos providers atrás de uma API. Aponte o rousseau para ele:

```yaml
provider: openai

openai:
  api_key: sk-litellm-...
  base_url: http://litellm.internal:4000
  model: bedrock/anthropic.claude-sonnet-4-6-20260101-v1:0
```

Nota: a porta padrão do LiteLLM é 4000, e seu prefixo `/v1` é opcional dependendo de como é implantado. Siga a documentação do LiteLLM para sua versão.

Uso de tools: passa direto para o provider subjacente. Streaming: sim. Útil para equipes que querem um ponto único de estrangulamento para tráfego LLM (rate limiting, rastreamento de budget, auditoria).

  </div>
</div>

## Referência de configuração

| Campo | Padrão | Efeito |
|---|---|---|
| `api_key` | *obrigatório* | Token bearer. Use `not-required` para endpoints locais que ignoram autenticação. |
| `model` | *obrigatório* | Identificador do modelo. Sem padrão universal entre endpoints. |
| `base_url` | *depende do nome do provider* | Sobrescreve o endpoint. Veja presets em `setDefaults`. |
| `max_tokens` | padrão do SDK | Limita os tokens de saída por completion. |

Os nomes de provider `openai`, `openrouter` e `ollama` cada um mapeiam para seu próprio bloco de configuração (`OpenAIConfig`, `OpenAIConfig`, `OpenAIConfig`); eles compartilham o mesmo formato, mas permitem que você configure múltiplos endpoints em um único `config.yaml` e alterne entre eles mudando `provider:`.

## Streaming

O provider implementa `agent.StreamingProvider` via SSE. Cada endpoint acima suporta streaming; o shim do Ollama requer uma build recente (0.5+).

## Uso de tools

Definições de tools do `Registry` são convertidas para o array `tools` da OpenAI em `internal/llm/openai/client.go`. Nem todo endpoint compatível com OpenAI suporta uso de tools — verifique seu backend antes de habilitar. O Ollama suporta a partir do 0.4; builds mais antigas do LM Studio não.

Políticas de aprovação se aplicam para endpoints que retornam `tool_calls`. Endpoints sem suporte a tool-use retornarão texto puro e o `Registry` não será consultado.

## Armadilhas

- **Nomenclatura de modelo.** Cada endpoint tem sua própria convenção: OpenAI (`gpt-5`), OpenRouter (`anthropic/claude-sonnet-4-6`), Ollama (`llama3.1:8b`), vLLM (o nome HuggingFace). Não há portabilidade entre endpoints.
- **Chave de API vazia.** O SDK rejeita strings vazias; passe `not-required` (ou qualquer placeholder) para endpoints locais que não precisam de autenticação.
- **Barra final da BaseURL.** Inclua o segmento `/v1`. Não inclua barra final.
- **Timeouts.** Ollama local em CPU pode levar dezenas de segundos por turno — aumente o timeout do seu HTTP client se você envelopa o provider você mesmo. O `rousseau` usa o padrão do SDK.
- **Variação no uso de tools.** OpenAI e Anthropic-atrás-do-OpenRouter suportam tools de forma confiável. O Ollama precisa de uma build recente e um modelo com chat template de tool-use. O LM Studio não suporta tools. Se `tool_calls` chegarem como texto puro, o `Registry` não é consultado.
- **Modelos de raciocínio.** As séries o1/o3 da OpenAI se comportam diferentemente: `max_tokens` é substituído por `max_completion_tokens` e system prompts são limitados. O SDK trata disso, mas espere maior latência por turno.

## Solução de problemas

### `openai: complete: 401 Unauthorized`

Chave de API errada ou ausente. Para OpenRouter, use o token `sk-or-…`. Para endpoints locais, garanta que `api_key` é não-vazio mesmo que o endpoint o ignore.

### `openai: complete: 404 model not found`

A string `model` não corresponde a nada que o endpoint reconheça. Para OpenRouter, inclua o prefixo do provider (`anthropic/claude-sonnet-4-6`, não `claude-sonnet-4-6`). Para Ollama, garanta que o modelo foi baixado (`ollama pull llama3.1:8b`).

### O modelo ignora meus `tools`

O endpoint não suporta uso de tools para este modelo. Verifique apontando para o mesmo modelo via um endpoint conhecido como bom (OpenAI, Anthropic direta, OpenRouter com um modelo Anthropic). Veja a coluna de uso de tools nas receitas acima.

### `context deadline exceeded` no Ollama local

Inferência em CPU é lenta. Opções: (1) aumente o timeout do seu caller, (2) execute o Ollama em um host com GPU, (3) mude para um modelo menor (`llama3.1:8b` vs `70b`).

### O streaming para no meio de uma resposta

Alguns proxies (LiteLLM, proxies corporativos de egresso) fazem buffer de SSE. Configure o proxy para desabilitar buffering para `text/event-stream` ou execute o rousseau no mesmo segmento de rede que o endpoint.

## Páginas relacionadas

- [Guias: vLLM auto-hospedado](/pt-BR/guides/self-hosted-vllm/) — implantação em produção.
- [Providers: Anthropic](/pt-BR/providers/anthropic/) — a alternativa de API direta para o Claude.
- [Guias: Multi-provider](/pt-BR/guides/multi-provider/) — executando providers diferentes por transporte.
- [Guias: Rate limits](/pt-BR/guides/rate-limits/) — playbook de retry provider por provider.
- [Configuração](/pt-BR/configuration/) — os blocos `openai`/`openrouter`/`ollama` em contexto.

## Leitura complementar

- `internal/llm/openai/client.go` — `Complete`, conversão de mensagem, schema de tools.
- `internal/llm/openai/client.go` — implementação de streaming.
- `internal/config/config.go` — struct `OpenAIConfig`, `setDefaults` para presets de `base_url`.
