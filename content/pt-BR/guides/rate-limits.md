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
description: "How rousseau-agent handles provider rate limits: 429s, exponential backoff, prompt-cache markers, and per-provider cost notes."
keywords: "rate limits, 429, backoff, retry, prompt cache, anthropic, bedrock, cost"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/guides/rate-limits/"
subtitle: "429 handling, backoff, and cache-marker optimisation."
tags: "guides, rate limits, prompt cache, anthropic"
title: "Guia: limites de taxa"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "rate limits, 429, backoff, retry, prompt cache, anthropic, bedrock, cost"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guia: limites de taxa"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 36
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/rate-limits/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/rate-limits/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guia: limites de taxa"
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
twitter_description: "How rousseau-agent handles provider rate limits: 429s, exponential backoff, prompt-cache markers, and per-provider cost notes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guia: limites de taxa"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>Limites de taxa por provider, custo por token, semântica de retry, economia de cache e uma receita de retry-with-backoff no lado do chamador. Veja a página de preços de cada provider para números autoritativos — a tabela abaixo é um snapshot.</p></aside>

## Onde o rate limiting acontece

O rousseau não implementa seu próprio handling de rate-limit. Cada cliente de provider delega para o SDK upstream:

- **Anthropic direto** — `anthropic-sdk-go` lida com retries HTTP, respeita `Retry-After`, aplica backoff exponencial em 5xx e 429. Veja `internal/llm/anthropic/client.go`.
- **Bedrock** — `aws-sdk-go-v2` trata erros de throttling com retries adaptativos.
- **Vertex** — as bibliotecas de auth do Google fazem seus próprios retries.
- **OpenAI / OpenRouter / Ollama** — o cliente Go compatível com OpenAI lida com 429s.
- **claudecli** — o próprio binário `claude` do Claude Code lida com limites. O rousseau apenas faz shell-out.

Requests falhados aparecem como eventos slog `turn.failed`, `whatsapp.handler_failed` ou `cron.run_failed`. O texto da mensagem incluirá a string de erro do provider (tipicamente `429 Too Many Requests` com um backoff sugerido).

## Quando você realmente bate no limite

Sintomas nos logs:

```jsonl
{"level":"ERROR","msg":"whatsapp.handler_failed","err":"anthropic: complete: 429 Too Many Requests"}
```

Como o rousseau trata um turno como falho em erros irrecuperáveis, o operador vê a falha na resposta do transporte — o daemon não engole silenciosamente. Isso é intencional.

## Reduzindo pressão de rate-limit

Três alavancas, em ordem de impacto:

### 1. Marcadores de prompt cache (Anthropic direto)

`applyCacheMarkers` em `internal/llm/anthropic/client.go` marca uma janela inicial de mensagens para o cache efêmero de prompt da Anthropic. Quando `CacheableMessages > 0`, o system prompt também é marcado para cache. Tokens de entrada cacheados são cobrados a aproximadamente 10% das taxas padrão de entrada e cache hits não consomem o budget padrão de rate-limit de entrada.

O agente (`internal/agent/agent.go`) opta por isso em sessões multi-turno. Se você constrói loops customizados sobre a API Go do rousseau, defina `Request.CacheableMessages` e `Request.System` — mesmo um cache hit raso corta tanto o custo quanto a pressão de rate-limit.

Marcadores de cache são só para Anthropic direto hoje. Providers Bedrock, Vertex e OpenAI-compat os ignoram.

### 2. Compressão

Para sessões longas em um provider pago por token (Anthropic direto, Bedrock, Vertex, OpenRouter), habilite compressão:

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60      # from CompressionConfig default
    keep_recent: 8
```

O `LLMCompressor` (`internal/agent/compressor.go`) resume o slice mais antigo da sessão em uma única mensagem sintética de usuário quando a contagem de mensagens cruza `trigger_messages`, e preserva as últimas `keep_recent` mensagens literalmente. Menos tokens por turno = menos pressão de rate-limit.

Compressão fica desligada por padrão porque a implantação de referência usa `claudecli` em um tier de assinatura, onde a contagem de tokens não é cobrada.

### 3. Cadência de cron mais lenta

Para daemons puros de background, dividir a cadência de cron pela metade divide os requests pela metade. As cadências de `rousseau cron` são expressões cron — vá de a cada 15 minutos para a cada hora se o requisito de frescor permitir.

## Custo aproximado por provider

Rate limits e custo por token se movem independentemente, mas os dois usualmente estão correlacionados (tiers pagos têm limites mais altos). Guia aproximado em 2026-07:

| Provider | Entrada $/MTok (classe Sonnet) | Saída $/MTok | Leitura de cache $/MTok |
|---|---|---|---|
| `anthropic` direto | ~3 | ~15 | ~0.30 |
| `bedrock` (Sonnet-4.6) | ~3 | ~15 | Cache: N/A no momento em que este texto foi escrito |
| `vertex` (Anthropic no Vertex) | ~3 | ~15 | Cache: N/A no momento em que este texto foi escrito |
| `openrouter` | dependente de modelo | dependente de modelo | dependente do provider |
| `ollama` self-hosted | $0 | $0 | $0 (você paga o compute) |
| `claudecli` | cobrança por tier de assinatura | incluído | N/A |

Pegue os números atuais na página de preços de cada provider.

## Quando o SDK esgota retries

Se o SDK do provider desiste, o rousseau expõe o erro final. O turno é perdido — não há fila e nenhum retry em disco. Duas mitigações:

- **Mensagem para o operador pelo mesmo canal.** A falha do turno é visível na resposta do transporte; o operador pode reformular.
- **Faça fallback para um segundo provider manualmente.** Veja [Guias: Multi-provider](/pt-BR/guides/multi-provider/) para o padrão de dois daemons.

Failover cross-provider automático é um item do roadmap.

## Depurando problemas de rate-limit

1. Defina `log.level: debug` em `config.yaml`. A saída de debug do SDK mostra o valor exato de `Retry-After`.
2. Procure por `turn.failed`, `whatsapp.handler_failed`, `cron.run_failed` no journal.
3. Verifique o dashboard do provider (Anthropic Console, AWS CloudWatch, GCP Cloud Monitoring) para consumo real de quota.
4. Se você está em um tier de assinatura, fique atento a resets de quota diária — o erro do SDK geralmente inclui o horário de reset.

## Referência rápida por provider

<aside class="admonition" data-type="warning"><span class="admonition-title">Cite suas fontes</span><p>Preços e limites mudam sem aviso. Os números nesta tabela são de meados de 2026 e são ilustrativos. Sempre linke para a página de preços atual do provider para valores autoritativos.</p></aside>

| Provider | Comportamento de retry | Sinal de rate | Custo por 1M de entrada | Custo por 1M de saída | Custo de leitura de cache |
|---|---|---|---|---|---|
| `anthropic` direto | SDK faz retry em 5xx; 429 com `Retry-After` respeitado | header `429 Too Many Requests` carrega tempo de reset | ~$3 (Sonnet) | ~$15 (Sonnet) | ~$0.30 |
| `bedrock` | retry adaptativo do AWS SDK | `ThrottlingException` | ~$3 (Sonnet) | ~$15 (Sonnet) | ainda não |
| `vertex` | retry exponencial do Google SDK | `429 RESOURCE_EXHAUSTED` | ~$3 (Sonnet) | ~$15 (Sonnet) | ainda não |
| `openai` | SDK faz retry em 5xx; 429 respeitado | `429 Too Many Requests` | específico do modelo | específico do modelo | específico do modelo |
| `openrouter` | passthrough para o provider subjacente | dependente do provider | específico do modelo | específico do modelo | dependente do provider |
| `ollama` | SDK faz retry; local, então raramente dispara | nenhum | $0 (custo de compute) | $0 (custo de compute) | N/A |
| `claudecli` | erros de subprocesso aparecem; sem retry do lado do rousseau | opaco | assinatura | assinatura | opaco |

Fontes autoritativas:

- [Anthropic pricing](https://www.anthropic.com/pricing)
- [AWS Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)
- [Vertex AI pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- [OpenAI pricing](https://openai.com/pricing)
- [OpenRouter model list](https://openrouter.ai/models)

## Receita de retry no lado do chamador

O rousseau não faz retry dentro de `Complete`. Se você embutir a biblioteca do agente, envolva `Turn` no seu próprio loop de retry com backoff exponencial e jitter:

```go
func retryTurn(ctx context.Context, ag *agent.Agent, sess *agent.Session, maxRetries int) (agent.Message, error) {
    var lastErr error
    for attempt := 0; attempt < maxRetries; attempt++ {
        m, err := ag.Turn(ctx, sess)
        if err == nil {
            return m, nil
        }
        if !isRateLimit(err) {
            return agent.Message{}, err // non-retryable
        }
        lastErr = err
        // Exponential backoff with jitter: 1s, 2s, 4s, 8s, ...
        backoff := time.Duration(1<<attempt) * time.Second
        jitter := time.Duration(rand.Int63n(int64(backoff / 2)))
        select {
        case <-time.After(backoff + jitter):
        case <-ctx.Done():
            return agent.Message{}, ctx.Err()
        }
    }
    return agent.Message{}, fmt.Errorf("giving up after %d retries: %w", maxRetries, lastErr)
}

func isRateLimit(err error) bool {
    s := err.Error()
    return strings.Contains(s, "429") || strings.Contains(s, "rate limit") || strings.Contains(s, "ThrottlingException")
}
```

## Solução de problemas

### `429 Too Many Requests` em toda request

Você está em um tier baixo ou outro workload está consumindo a quota. Opções: (1) solicitar aumento de limite, (2) dividir carga entre providers, (3) rodar `claudecli` para workloads exclusivos de assinatura.

### `529 Overloaded` intermitentemente

O sistema da Anthropic está em capacidade. Não é throttling por conta — a região inteira está carregada. Faça retry com backoff.

### Marcadores de cache definidos mas sem economia visível

Verifique se `CacheableMessages` está realmente sendo definido. `applyCacheMarkers` em `internal/llm/anthropic/cache.go` é um no-op para zero. Verifique também que o prefixo é estável — um system prompt que se regenera por turno derrota o cache.

### `ThrottlingException` no Bedrock com baixo volume

A quota do Bedrock é por conta, por modelo, por região. Alguns modelos têm quotas padrão muito baixas (2–5 requests por minuto). Solicite um aumento no console Service Quotas.

### Respostas de API lentas apesar de baixo uso

Alguns providers despriorizam contas de tier baixo sob carga global. Os headers de resposta `x-ratelimit-*` da Anthropic indicam o estado atual do bucket — inspecione se você tem acesso ao SDK.

## Páginas relacionadas

- [Providers: Anthropic](/pt-BR/providers/anthropic/) — detalhes de marcador de cache.
- [Configuração](/pt-BR/configuration/) — cada knob de compressão.
- [Guia do usuário: Compressão + Recall](/pt-BR/user-guide/compression-recall/) — discussão mais profunda de compressão.
- [Guias: Multi-provider](/pt-BR/guides/multi-provider/) — divida carga entre endpoints.
- [Guias: Rate/Model Swap](/pt-BR/guides/rate-model-swap/) — troca a quente de providers em caso de falha.

## Leitura adicional

- `internal/llm/anthropic/client.go` — invocação do SDK.
- `internal/llm/anthropic/cache.go` — helper de marcador de cache.
- `internal/agent/agent.go` — onde falhas de turno aparecem.
- Páginas de preços de providers linkadas acima.
