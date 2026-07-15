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
description: "Worked example: point rousseau-agent at a self-hosted vLLM endpoint on your internal network via the OpenAI-compatible provider."
keywords: "vllm, self-hosted, openai-compatible, air-gapped, internal network, local llm"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/self-hosted-vllm/"
subtitle: "Point rousseau at a vLLM endpoint on your internal network."
tags: "guides, vllm, self-hosted, openai-compatible"
title: "Guia: vLLM auto-hospedado"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "vllm, self-hosted, openai-compatible, air-gapped, internal network, local llm"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: vLLM auto-hospedado"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 32
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/self-hosted-vllm/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/self-hosted-vllm/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guia: vLLM auto-hospedado"
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
twitter_description: "Worked example: point rousseau-agent at a self-hosted vLLM endpoint on your internal network via the OpenAI-compatible provider."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guia: vLLM auto-hospedado"
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

## Cenário

Você tem uma instância vLLM servindo um modelo de codificação de pesos abertos em uma máquina interna (`llm.internal:8000`). Nenhum tráfego de inferência pode sair da rede. Aponte o rousseau para ela e trate o endpoint como qualquer outro alvo compatível com OpenAI.

O vLLM implementa o schema OpenAI Chat Completions, então o provider `openai` do rousseau funciona sem alterações. LM Studio, Ollama e Text Generation Inference seguem o mesmo padrão.

## Pré-requisitos

- vLLM já no ar em `http://llm.internal:8000/v1` com `/v1/chat/completions` respondendo a um smoke test com curl.
- A tag do modelo com a qual você lançou o vLLM (por exemplo, `Qwen/Qwen3-Coder-30B`).

## Passo 1 — Confirmar o vLLM

```sh
curl -fsS http://llm.internal:8000/v1/models
curl -fsS http://llm.internal:8000/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{
    "model": "Qwen/Qwen3-Coder-30B",
    "messages": [{"role": "user", "content": "say hi"}]
  }' | jq .
```

Ambos devem retornar sem erro. Se a segunda chamada der 4xx, corrija o vLLM primeiro — o cliente do rousseau é um shim JSON fino e herda sua superfície de erros.

## Passo 2 — Conectar o rousseau ao vLLM

Edite `~/.config/rousseau/config.yaml`:

```yaml
provider: openai

openai:
  base_url: http://llm.internal:8000/v1
  api_key: not-required        # vLLM ignores the key but the client sends one
  model: Qwen/Qwen3-Coder-30B
  max_tokens: 4096

log:
  level: info
  format: json
```

O provider `openai` compartilha o schema com `openrouter` e `ollama`; a única diferença é o `base_url` predefinido. Definir `base_url` explicitamente sobrescreve o padrão.

## Passo 3 — Smoke test na TUI

```sh
rousseau chat
```

Digite `explain the difference between goroutines and threads in two paragraphs.` e envie. Se a resposta chegar em streaming, a fiação está correta.

Se não:

```sh
rousseau doctor
```

A linha `provider.selected` mostrará `openai`; um `fail` em alcançabilidade de `provider.openai.base_url` significa que o DNS ou o caminho da rede interna está quebrado, não o rousseau.

## Passo 4 — Ligar o uso de ferramentas

Modelos de codificação variam na fidelidade de uso de ferramentas. O agent loop do rousseau espera que o modelo emita blocos `tool_use` cujo JSON valide contra o `InputSchema` da ferramenta. Se seu modelo vLLM não suportar nativamente o schema de tool-use OpenAI:

- Comece com `provider: openai` + um modelo que suporte (variantes recentes de Qwen, Mistral, Llama 3.1 8B+ anunciam isso).
- Ou envolva o vLLM em um shim como o [adaptador tool_choice compatível com OpenAI do vLLM](https://docs.vllm.ai/) e verifique de novo.

Uma vez que o uso de ferramentas funcione, as ferramentas de codificação (read, write, edit, grep, bash) ficam disponíveis exatamente como em qualquer outro provider.

## Passo 5 — Considere políticas de aprovação

Modelos self-hosted tendem a ser menos cientes de risco do que modelos de fronteira. Travar a ferramenta `bash` com um aprovador em modo `pattern` é prudente:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read,  match: ".*"}
      - {tool: grep,  match: ".*"}
      - {tool: edit,  match: "^./workspace/.*"}
      - {tool: bash,  match: "^(ls|cat|grep|rg|find|git status|git diff) "}
    deny:
      - {tool: bash,  match: "rm -rf|sudo|curl|wget|chmod|chown"}
```

Veja [Guias: Auditoria + Políticas de Aprovação](/pt-BR/guides/audit-approval-policies/) para um passo a passo mais profundo.

## Passo 6 — Observe a performance

Endpoints self-hosted frequentemente se beneficiam de um `max_iterations` maior (o agent loop pode precisar de mais round-trips para chegar à mesma conclusão) e sempre de habilitar a compressão de sessão:

```yaml
agent:
  max_iterations: 48
  compression:
    enabled: true
    trigger_messages: 60
    keep_recent: 8
```

A compressão fica desligada por padrão porque usa um turno de LLM para resumir; numa API pública paga por token isso pode ser desperdício. Num endpoint self-hosted o custo de tokens é zero, então deixe ligado.

## Alternativas ao vLLM

A mesma receita se aplica a:

- **Ollama** — use `provider: ollama` (padrão `base_url` para `http://localhost:11434/v1` e `api_key` para `not-required`).
- **LM Studio** — use `provider: openai` e aponte `base_url` para o servidor LM Studio (`http://host:1234/v1`).
- **TGI (Text Generation Inference)** — use `provider: openai` e aponte `base_url` para o endpoint de compatibilidade OpenAI do TGI.
- **OpenRouter** — use `provider: openrouter` (padrão `base_url` para `https://openrouter.ai/api/v1`).

## Ressalvas

- O rousseau não faz streaming quando o provider não faz streaming. Algumas builds do vLLM vêm com streaming desabilitado — ligue para uma melhor experiência na TUI.
- Prompt caching (`internal/llm/anthropic` usa marcadores `cache_control`) é específico da Anthropic e não faz nada contra vLLM. Isso importa principalmente para sessões de longa duração em providers pagos por token.
- A [página de provider openai-compatible](/pt-BR/providers/openai-compatible/) é a referência definitiva para cada knob.

## Próximo

- [Provider OpenAI-compatible](/pt-BR/providers/openai-compatible/) — cada campo de config.
- [Auditoria + políticas de aprovação](/pt-BR/guides/audit-approval-policies/) — postura de segurança para modelos menos alinhados.
- [Offline](/pt-BR/offline/) — rodando o rousseau sem internet de saída.
