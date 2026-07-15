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
description: "Run two rousseau daemons with different providers side-by-side — e.g. claudecli for interactive chat and Bedrock for scheduled reports."
keywords: "multi provider, claudecli, bedrock, config precedence, XDG_CONFIG_HOME"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/guides/multi-provider/"
subtitle: "Two daemons, two providers, one operator."
tags: "guides, providers, multi-provider, deployment"
title: "Guía: multi-proveedor"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "multi provider, claudecli, bedrock, config precedence, XDG_CONFIG_HOME"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guía: multi-proveedor"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 35
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/multi-provider/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/multi-provider/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guía: multi-proveedor"
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
twitter_description: "Run two rousseau daemons with different providers side-by-side — e.g. claudecli for interactive chat and Bedrock for scheduled reports."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guía: multi-proveedor"
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

## Por qué podrías querer esto

El campo `provider` de rousseau es un único escalar (`internal/config/config.go` `Config.Provider`). Un solo proceso de rousseau habla con exactamente un proveedor. Cuando quieres más de uno (lo más común: `claudecli` para uso interactivo en la TUI porque hereda una sesión OAuth, y un proveedor de API de pago (Bedrock, Anthropic direct, Vertex) para daemons en segundo plano donde el OAuth de `claude` de suscripción es incómodo), ejecutas **dos procesos de rousseau** con archivos de configuración diferentes.

Combinaciones razonables:

| Interactivo | Desatendido | Por qué |
|---|---|---|
| `claudecli` | `anthropic` o `bedrock` | OAuth para chat en laptop, clave de API para un daemon en VPS. |
| `claudecli` | `vertex` | Igual, en GCP. |
| `anthropic` | `openai` u `ollama` | Comparar respuestas, o hacer fallback a un modelo más barato/local para cron. |
| `claudecli` | `openai` (OpenRouter) | Claude en TUI, modelo barato de OpenRouter para resúmenes programados. |

## Cómo resuelve rousseau la configuración

`config.Load` (en `internal/config/config.go`) aplica flag > env > archivo > default. El archivo que lee por defecto es `~/.config/rousseau/config.yaml`, pero el flag persistente `--config` en el comando raíz (`internal/cli/root.go`) lo sobrescribe. Eso te da una división limpia.

## Disposición con dos configuraciones

```sh
mkdir -p ~/.config/rousseau
cat > ~/.config/rousseau/chat.yaml <<'YAML'
provider: claudecli
claudecli:
  binary: claude
log:
  level: info
  format: text
YAML

cat > ~/.config/rousseau/cron.yaml <<'YAML'
provider: bedrock
bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
log:
  level: info
  format: json
YAML
```

Ejecuta cada comando con el archivo correcto:

```sh
rousseau --config ~/.config/rousseau/chat.yaml chat
rousseau --config ~/.config/rousseau/cron.yaml whatsapp --allow YOUR_JID@s.whatsapp.net
```

## Estado compartido vs particionado

Ambos procesos apuntan al mismo almacén de sesiones SQLite por defecto (`~/.local/share/rousseau/sessions.db`), y eso es usualmente lo que quieres, para que el puente de WhatsApp y tu chat TUI compartan historial.

Para particionar completamente el estado, sobrescribe `state.path` por configuración:

```yaml
state:
  path: /home/seb/.local/share/rousseau/chat.db
```

El acceso SQLite cross-proceso es seguro gracias al journaling WAL y al `busy_timeout` de 15 segundos establecido por `Open()` en `internal/state/sqlite/store.go`.

## Cableado con systemd

Dos unidades Quadlet, una por configuración. El `Exec=` de cada unidad incluye `--config /home/rousseau/.config/rousseau/<name>.yaml`:

```ini
Exec=--config /home/rousseau/.config/rousseau/cron.yaml whatsapp --allow ...
```

Consulta [Despliegue](/es/deployment/) para la unidad base.

## Políticas de aprobación por configuración

Diferentes proveedores merecen diferentes aprobaciones. El `claudecli` interactivo puede quedarse con seguridad en `mode: allow_all` porque Claude Code tiene su propia UI de aprobación por llamada. El daemon de Bedrock/Anthropic debe ejecutar `mode: pattern` con `default: deny`. Pon cada uno bajo su propio YAML.

## Pruebas

Confirma que cada proceso habla con el endpoint correcto:

```sh
# El interactivo muestra la ruta del subproceso claudecli en strace / lsof
lsof -c rousseau | grep -E 'claude|CLAUDE'

# El de segundo plano muestra HTTPS saliente a bedrock-runtime.<region>.amazonaws.com
ss -tanp | grep rousseau
```

## Lo que esto NO te da

- **No es enrutamiento por solicitud.** Rousseau no hará fallback de un proveedor a otro dentro de un solo turno. La falla del proveedor configurado se muestra como `whatsapp.handler_failed` / `turn.failed` y el modelo no reintenta contra un proveedor diferente. Ese es un ítem del roadmap.
- **No es caché compartido.** El caché de prompt de Anthropic (consulta `applyCacheMarkers` en `internal/llm/anthropic/client.go`) es por endpoint. Un hit bajo Anthropic direct no es un hit contra Bedrock, incluso para la misma familia de modelo.

## Relacionado

- [Proveedores](/es/providers/): comparación de los cinco tipos de proveedor.
- [Configuración](/es/configuration/): cada perilla.
- [Referencia: Variables de entorno](/es/reference/environment-variables/): sobrescrituras basadas en env.
- [Guías: Despliegue de producción](/es/guides/production-deployment/).
