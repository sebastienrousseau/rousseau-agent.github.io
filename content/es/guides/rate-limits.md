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
hreflang: "es"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "es"
locale: "es_ES"
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
permalink: "https://docs.rousseau-agent.dev/es/guides/rate-limits/"
subtitle: "429 handling, backoff, and cache-marker optimisation."
tags: "guides, rate limits, prompt cache, anthropic"
title: "Guía: límites de tasa"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "rate limits, 429, backoff, retry, prompt cache, anthropic, bedrock, cost"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: límites de tasa"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 36
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/rate-limits/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/rate-limits/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guía: límites de tasa"
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
twitter_title: "Guía: límites de tasa"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Gracias a cada operador que ejecuta su propio agente de codificación."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">Qué aprenderás</span><p>Límites de tasa por proveedor, coste por token, semántica de reintentos, economía de la caché y una receta de retry con backoff del lado del llamador. Consulta la página de precios de cada proveedor para números autoritativos — la tabla siguiente es una instantánea.</p></aside>

## Dónde ocurre el rate limiting

Rousseau no implementa su propio manejo de rate limits. Cada cliente de proveedor delega en el SDK aguas arriba:

- **Anthropic direct** — `anthropic-sdk-go` gestiona los reintentos HTTP, respeta `Retry-After`, aplica backoff exponencial en 5xx y 429. Consulta `internal/llm/anthropic/client.go`.
- **Bedrock** — `aws-sdk-go-v2` gestiona errores de throttling con reintentos adaptativos.
- **Vertex** — las librerías de auth de Google gestionan sus propios reintentos.
- **OpenAI / OpenRouter / Ollama** — el cliente Go compatible con OpenAI gestiona los 429.
- **claudecli** — el binario `claude` de Claude Code gestiona los límites. Rousseau solo hace shell out.

Las solicitudes fallidas afloran como eventos slog `turn.failed`, `whatsapp.handler_failed` o `cron.run_failed`. El texto del mensaje incluirá la cadena de error del proveedor (típicamente `429 Too Many Requests` con un backoff sugerido).

## Cuando de verdad alcanzas un límite

Síntomas en los logs:

```jsonl
{"level":"ERROR","msg":"whatsapp.handler_failed","err":"anthropic: complete: 429 Too Many Requests"}
```

Como rousseau trata un turno como fallido ante errores irrecuperables, el operador ve el fallo en la respuesta del transporte — el demonio no lo traga en silencio. Esto es intencional.

## Reducir la presión sobre los rate limits

Tres palancas, por orden de impacto:

### 1. Marcadores de caché de prompt (Anthropic directo)

`applyCacheMarkers` en `internal/llm/anthropic/client.go` marca una ventana inicial de mensajes para la caché de prompt efímera de Anthropic. Cuando `CacheableMessages > 0`, el prompt del sistema también se marca para caché. Los tokens de entrada cacheados se facturan aproximadamente al 10 % de la tarifa estándar de entrada y los aciertos de caché no consumen el presupuesto estándar del rate limit de entrada.

El agente (`internal/agent/agent.go`) activa esto en sesiones multi-turno. Si construyes bucles personalizados sobre la API Go de rousseau, establece `Request.CacheableMessages` y `Request.System` — incluso un cache hit superficial reduce tanto el coste como la presión sobre los rate limits.

Los marcadores de caché son solo para Anthropic direct hoy. Bedrock, Vertex y los proveedores compatibles con OpenAI los ignoran.

### 2. Compresión

Para sesiones largas en un proveedor de pago por token (Anthropic direct, Bedrock, Vertex, OpenRouter), activa la compresión:

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60      # desde el default de CompressionConfig
    keep_recent: 8
```

`LLMCompressor` (`internal/agent/compressor.go`) resume el slice más antiguo de la sesión en un único mensaje de usuario sintético cuando el número de mensajes supera `trigger_messages`, y preserva los últimos `keep_recent` mensajes textualmente. Menos tokens por turno = menos presión sobre los rate limits.

La compresión está desactivada por defecto porque el despliegue de referencia usa `claudecli` en un nivel de suscripción, donde el número de tokens no se factura.

### 3. Cadencia de cron más lenta

Para demonios de fondo puros, reducir a la mitad la cadencia de cron reduce a la mitad las solicitudes. Las cadencias de `rousseau cron` son expresiones cron — pasa de cada 15 minutos a cada hora si el requisito de frescura lo permite.

## Coste aproximado por proveedor

Los rate limits y el coste por token se mueven de forma independiente, pero ambos suelen estar correlacionados (los niveles de pago tienen límites más altos). Guía aproximada a fecha de 2026-07:

| Proveedor | Entrada $/MTok (clase Sonnet) | Salida $/MTok | Lectura de caché $/MTok |
|---|---|---|---|
| `anthropic` direct | ~3 | ~15 | ~0,30 |
| `bedrock` (Sonnet-4.6) | ~3 | ~15 | Caché: N/A al momento de escribir |
| `vertex` (Anthropic en Vertex) | ~3 | ~15 | Caché: N/A al momento de escribir |
| `openrouter` | depende del modelo | depende del modelo | depende del proveedor |
| `ollama` autoalojado | $0 | $0 | $0 (pagas el cómputo) |
| `claudecli` | facturación por nivel de suscripción | incluido | N/A |

Obtén los números actuales de la página de precios de cada proveedor.

## Cuando el SDK agota los reintentos

Si el SDK del proveedor se rinde, rousseau expone el error final. El turno se pierde — no hay cola ni reintento en disco. Dos mitigaciones:

- **Mensaje al operador por el mismo canal.** El fallo del turno es visible en la respuesta del transporte; el operador puede reformular.
- **Fallback manual a un segundo proveedor.** Consulta [Guías: multi-proveedor](/es/guides/multi-provider/) para el patrón de dos demonios.

El failover automático entre proveedores está en la hoja de ruta.

## Depurar problemas de rate limit

1. Establece `log.level: debug` en `config.yaml`. La salida de debug del SDK muestra el valor exacto de `Retry-After`.
2. Busca `turn.failed`, `whatsapp.handler_failed`, `cron.run_failed` en el journal.
3. Revisa el dashboard del proveedor (Anthropic Console, AWS CloudWatch, GCP Cloud Monitoring) para ver el consumo real de la cuota.
4. Si estás en un nivel de suscripción, presta atención a los resets de cuota diaria — el error del SDK suele incluir la hora de reset.

## Referencia rápida por proveedor

<aside class="admonition" data-type="warning"><span class="admonition-title">Cita tus fuentes</span><p>Los precios y límites cambian sin aviso. Los números de esta tabla son de mediados de 2026 y son ilustrativos. Enlaza siempre a la página de precios actual del proveedor para valores autoritativos.</p></aside>

| Proveedor | Comportamiento de retry | Señal de rate | Coste por 1M de entrada | Coste por 1M de salida | Coste de lectura de caché |
|---|---|---|---|---|---|
| `anthropic` direct | SDK reintenta 5xx; 429 con `Retry-After` respetado | La cabecera `429 Too Many Requests` lleva la hora de reset | ~$3 (Sonnet) | ~$15 (Sonnet) | ~$0,30 |
| `bedrock` | Retry adaptativo del SDK de AWS | `ThrottlingException` | ~$3 (Sonnet) | ~$15 (Sonnet) | aún no |
| `vertex` | Retry exponencial del SDK de Google | `429 RESOURCE_EXHAUSTED` | ~$3 (Sonnet) | ~$15 (Sonnet) | aún no |
| `openai` | SDK reintenta 5xx; 429 respetado | `429 Too Many Requests` | específico del modelo | específico del modelo | específico del modelo |
| `openrouter` | passthrough al proveedor subyacente | depende del proveedor | específico del modelo | específico del modelo | depende del proveedor |
| `ollama` | El SDK reintenta; local, rara vez se dispara | ninguna | $0 (coste de cómputo) | $0 (coste de cómputo) | N/A |
| `claudecli` | los errores del subproceso afloran; sin retry por parte de rousseau | opaco | suscripción | suscripción | opaco |

Fuentes autoritativas:

- [Anthropic pricing](https://www.anthropic.com/pricing)
- [AWS Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)
- [Vertex AI pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- [OpenAI pricing](https://openai.com/pricing)
- [OpenRouter model list](https://openrouter.ai/models)

## Receta de retry del lado del llamador

Rousseau no reintenta dentro de `Complete`. Si embebes la librería del agente, envuelve `Turn` en tu propio bucle de reintentos con backoff exponencial y jitter:

```go
func retryTurn(ctx context.Context, ag *agent.Agent, sess *agent.Session, maxRetries int) (agent.Message, error) {
    var lastErr error
    for attempt := 0; attempt < maxRetries; attempt++ {
        m, err := ag.Turn(ctx, sess)
        if err == nil {
            return m, nil
        }
        if !isRateLimit(err) {
            return agent.Message{}, err // no reintentable
        }
        lastErr = err
        // Backoff exponencial con jitter: 1s, 2s, 4s, 8s, ...
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

## Solución de problemas

### `429 Too Many Requests` en cada solicitud

Estás en un nivel bajo u otra carga está consumiendo la cuota. Opciones: (1) solicitar un aumento de límite, (2) repartir carga entre proveedores, (3) ejecutar `claudecli` para cargas que solo requieren suscripción.

### `529 Overloaded` intermitente

El sistema de Anthropic está al máximo de capacidad. No es throttling por cuenta — la región entera está cargada. Reintenta con backoff.

### Marcadores de caché establecidos pero sin ahorro de coste visible

Verifica que `CacheableMessages` realmente se esté estableciendo. `applyCacheMarkers` en `internal/llm/anthropic/cache.go` es un no-op para cero. Verifica también que el prefijo es estable — un prompt del sistema que se regenera por turno anula la caché.

### `ThrottlingException` en Bedrock con volumen bajo

La cuota de Bedrock es por cuenta, por modelo y por región. Algunos modelos tienen por defecto cuotas muy bajas (2–5 solicitudes por minuto). Solicita un aumento en la consola de Service Quotas.

### Respuestas de API lentas a pesar de un uso bajo

Algunos proveedores despriorizan cuentas de nivel bajo bajo carga global. Las cabeceras de respuesta `x-ratelimit-*` de Anthropic indican el estado actual del bucket — inspecciónalas si tienes acceso al SDK.

## Páginas relacionadas

- [Proveedores: Anthropic](/es/providers/anthropic/) — detalles de los marcadores de caché.
- [Configuración](/es/configuration/) — cada opción de compresión.
- [Guía de usuario: compresión + recall](/es/user-guide/compression-recall/) — discusión más profunda de la compresión.
- [Guías: multi-proveedor](/es/guides/multi-provider/) — reparte la carga entre endpoints.
- [Guías: cambio de tasa/modelo](/es/guides/rate-model-swap/) — cambio en caliente de proveedores ante fallos.

## Lecturas adicionales

- `internal/llm/anthropic/client.go` — invocación del SDK.
- `internal/llm/anthropic/cache.go` — helper de marcadores de caché.
- `internal/agent/agent.go` — dónde afloran los fallos de turno.
- Páginas de precios de proveedores enlazadas más arriba.
