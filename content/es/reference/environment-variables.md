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
description: "Every environment variable rousseau-agent reads: the ROUSSEAU_ prefix from Viper, ANTHROPIC_API_KEY, XDG paths, provider SDK variables."
keywords: "environment variables, ROUSSEAU_, ANTHROPIC_API_KEY, viper, XDG"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/reference/environment-variables/"
subtitle: "Every environment variable rousseau reads, at what layer, with what default."
tags: "reference, environment, viper, secrets"
title: "Referencia: variables de entorno"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "environment variables, ROUSSEAU_, ANTHROPIC_API_KEY, viper, XDG"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referencia: variables de entorno"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 51
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/environment-variables/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/environment-variables/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Referencia: variables de entorno"
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
twitter_description: "Every environment variable rousseau-agent reads: the ROUSSEAU_ prefix from Viper, ANTHROPIC_API_KEY, XDG paths, provider SDK variables."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Referencia: variables de entorno"
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

## Cómo rousseau lee el entorno

Dos mecanismos, en este orden (véase `config.Load` en `internal/config/config.go`):

1. **Binding automático de env de Viper.** `SetEnvPrefix("ROUSSEAU")` más `SetEnvKeyReplacer(".", "_")` significa que cada campo de configuración es alcanzable como `ROUSSEAU_<UPPER_SNAKE>`. Así, `provider` se convierte en `ROUSSEAU_PROVIDER`, `agent.approver.mode` en `ROUSSEAU_AGENT_APPROVER_MODE`.
2. **Override explícito.** `ANTHROPIC_API_KEY` se lee directamente del entorno y se fuerza en `anthropic.api_key`, de modo que la convención estándar del SDK de Anthropic funciona sin más. Ninguna otra clave se toma implícitamente.

Todo lo demás en esta página es o bien una variable mapeada por Viper, o una variable gestionada por SDK que rousseau no toca pero sí la biblioteca subyacente, o una ruta XDG usada para calcular defaults.

La precedencia se mantiene: **flag > env > archivo > default**.

## Prefijo `ROUSSEAU_*`

Cada tag `mapstructure` en `internal/config/config.go` es alcanzable vía `ROUSSEAU_<RUTA_EN_UPPER_SNAKE>`. Ejemplos seleccionados — la lista completa sigue la estructura de la config:

| Variable | Categoría | Default | Descripción |
|---|---|---|---|
| `ROUSSEAU_PROVIDER` | core | `claudecli` | Identificador de proveedor: `claudecli`, `anthropic`, `openai`, `openrouter`, `ollama`, `bedrock`, `vertex`. |
| `ROUSSEAU_LOG_LEVEL` | logging | `info` | Nivel de slog: `debug`, `info`, `warn`, `error`. |
| `ROUSSEAU_LOG_FORMAT` | logging | `text` | `text` o `json`. |
| `ROUSSEAU_STATE_PATH` | state | `$HOME/.local/share/rousseau/sessions.db` | DSN del store de sesiones. |
| `ROUSSEAU_AGENT_MAX_ITERATIONS` | agent | `32` | Tope de iteraciones de tool-use por turno. |
| `ROUSSEAU_AGENT_APPROVER_MODE` | agent | `` | `allow_all`, `deny_all`, `pattern`. |
| `ROUSSEAU_AGENT_APPROVER_DEFAULT` | agent | `` | Para `pattern`: `allow` o `deny` en llamadas sin coincidencia. |
| `ROUSSEAU_AGENT_COMPRESSION_ENABLED` | agent | `false` | Activa el compresor LLM. |
| `ROUSSEAU_AGENT_COMPRESSION_TRIGGER_MESSAGES` | agent | `60` | Comprime cuando el número de mensajes supera este umbral. |
| `ROUSSEAU_AGENT_COMPRESSION_KEEP_RECENT` | agent | `8` | Cuántos mensajes recientes preservar textualmente. |
| `ROUSSEAU_AGENT_SKILLS_DIR` | agent | `$HOME/.local/share/rousseau/skills` | Directorio de skills. |
| `ROUSSEAU_ANTHROPIC_API_KEY` | provider | — | Igual que `ANTHROPIC_API_KEY`. |
| `ROUSSEAU_ANTHROPIC_MODEL` | provider | `claude-sonnet-4-6` | ID de modelo de Anthropic. |
| `ROUSSEAU_ANTHROPIC_MAX_TOKENS` | provider | `4096` | Máximo de tokens de respuesta. |
| `ROUSSEAU_CLAUDECLI_BINARY` | provider | `claude` | Nombre del ejecutable para el proveedor `claudecli`. |
| `ROUSSEAU_CLAUDECLI_MODEL` | provider | — | Pasado a `claude --model`. |
| `ROUSSEAU_CLAUDECLI_PERMISSION_MODE` | provider | — | `default`, `acceptEdits`, `bypassPermissions`, `plan`, etc. |
| `ROUSSEAU_OPENAI_API_KEY` | provider | — | Bearer para endpoints compatibles con OpenAI. |
| `ROUSSEAU_OPENAI_MODEL` | provider | — | ID de modelo. |
| `ROUSSEAU_OPENAI_BASE_URL` | provider | — | Sobrescribe el endpoint. |
| `ROUSSEAU_OPENROUTER_API_KEY` | provider | — | Bearer para OpenRouter. |
| `ROUSSEAU_OPENROUTER_MODEL` | provider | — | Slug del modelo. |
| `ROUSSEAU_OPENROUTER_BASE_URL` | provider | `https://openrouter.ai/api/v1` | Sobrescribe el endpoint. |
| `ROUSSEAU_OLLAMA_MODEL` | provider | — | Tag del modelo. |
| `ROUSSEAU_OLLAMA_BASE_URL` | provider | `http://localhost:11434/v1` | Endpoint local de Ollama. |
| `ROUSSEAU_BEDROCK_REGION` | provider | — | Región AWS. |
| `ROUSSEAU_BEDROCK_MODEL` | provider | — | ID de modelo de Bedrock. |
| `ROUSSEAU_BEDROCK_PROFILE` | provider | — | Perfil nombrado de AWS. |
| `ROUSSEAU_VERTEX_PROJECT` | provider | — | Proyecto GCP. |
| `ROUSSEAU_VERTEX_REGION` | provider | — | Región de Vertex. |
| `ROUSSEAU_VERTEX_MODEL` | provider | — | Modelo Anthropic sobre Vertex. |
| `ROUSSEAU_VERTEX_CREDENTIALS_FILE` | provider | — | Ruta al JSON de service account. |
| `ROUSSEAU_WHATSAPP_REPLY_HEADER` | transport | `💎 *Rousseau Agent*\n\n` | Prefijo de cada mensaje saliente de WhatsApp. |
| `ROUSSEAU_WHATSAPP_VOICE_ENABLED` | transport | `false` | Habilita transcripción con whisper de notas de voz. |
| `ROUSSEAU_WHATSAPP_VOICE_BINARY` | transport | `whisper` | Ejecutable de whisper.cpp. |
| `ROUSSEAU_WHATSAPP_VOICE_MODEL` | transport | — | Nombre del modelo whisper (`base.en`, `small`). |
| `ROUSSEAU_WHATSAPP_VOICE_MODEL_PATH` | transport | — | Ruta explícita a .bin (tiene precedencia sobre `model`). |
| `ROUSSEAU_WHATSAPP_VOICE_LANGUAGE` | transport | — | Código ISO; vacío autodetecta. |
| `ROUSSEAU_SIGNAL_BINARY` | transport | `signal-cli` | Ejecutable de signal-cli. |
| `ROUSSEAU_SIGNAL_ACCOUNT` | transport | — | Número de teléfono E.164. |
| `ROUSSEAU_SIGNAL_REPLY_HEADER` | transport | — | Encabezado de respuesta. |
| `ROUSSEAU_TELEGRAM_TOKEN` | transport | — | Token de la Bot API. |
| `ROUSSEAU_TELEGRAM_BASE_URL` | transport | — | Sobrescribe el endpoint de la Bot API. |
| `ROUSSEAU_MATRIX_HOMESERVER_URL` | transport | — | URL base del homeserver. |
| `ROUSSEAU_MATRIX_ACCESS_TOKEN` | transport | — | Access token de Matrix. |
| `ROUSSEAU_MATRIX_USER_ID` | transport | — | MXID completo (`@bot:example.org`). |
| `ROUSSEAU_SLACK_APP_TOKEN` | transport | — | Token de app `xapp-…`. |
| `ROUSSEAU_SLACK_BOT_TOKEN` | transport | — | Token bot `xoxb-…`. |
| `ROUSSEAU_SLACK_BOT_USER_ID` | transport | — | User id del bot para suprimir auto-ecos. |
| `ROUSSEAU_DISCORD_TOKEN` | transport | — | Token del bot de Discord. |
| `ROUSSEAU_SMS_PROVIDER` | transport | — | `twilio` o `vonage`. |
| `ROUSSEAU_SMS_FROM` | transport | — | Número emisor. |
| `ROUSSEAU_SMS_ACCOUNT_SID` | transport | — | Account SID de Twilio. |
| `ROUSSEAU_SMS_AUTH_TOKEN` | transport | — | Secret de Twilio/Vonage. |
| `ROUSSEAU_SMS_API_KEY` | transport | — | API key de Vonage. |
| `ROUSSEAU_SMS_BASE_URL` | transport | — | Sobrescritura para endpoints regionales o pruebas. |
| `ROUSSEAU_IMESSAGE_BASE_URL` | transport | — | URL del servidor BlueBubbles. |
| `ROUSSEAU_IMESSAGE_PASSWORD` | transport | — | Contraseña de BlueBubbles. |
| `ROUSSEAU_IMESSAGE_CHAT_GUID` | transport | — | Destino de salida. |
| `ROUSSEAU_IMESSAGE_POLL_INTERVAL` | transport | `2s` | Cadena de duración. |
| `ROUSSEAU_EMAIL_IMAP_ADDR` | transport | — | Servidor IMAP. |
| `ROUSSEAU_EMAIL_IMAP_USERNAME` | transport | — | Usuario IMAP. |
| `ROUSSEAU_EMAIL_IMAP_PASSWORD` | transport | — | Contraseña IMAP. |
| `ROUSSEAU_EMAIL_MAILBOX` | transport | — | Carpeta a vigilar. |
| `ROUSSEAU_EMAIL_POLL_INTERVAL` | transport | — | Cadena de duración. |
| `ROUSSEAU_EMAIL_SMTP_ADDR` | transport | — | Host de submission SMTP. |
| `ROUSSEAU_EMAIL_SMTP_USERNAME` | transport | — | Usuario SMTP. |
| `ROUSSEAU_EMAIL_SMTP_PASSWORD` | transport | — | Contraseña SMTP. |
| `ROUSSEAU_EMAIL_FROM` | transport | — | Dirección de origen. |

**Arrays de allowlist** (`ROUSSEAU_SLACK_ALLOWLIST`, `ROUSSEAU_DISCORD_ALLOWLIST`, `ROUSSEAU_TELEGRAM_ALLOWLIST`, …) son soportados por Viper, pero el parseo de cadenas env separadas por comas es quisquilloso — prefiere establecerlos en `config.yaml`.

## Variables env explícitas (fuera del prefijo ROUSSEAU_)

| Variable | Origen | Propósito |
|---|---|---|
| `ANTHROPIC_API_KEY` | `config.Load` (`internal/config/config.go` línea 275) | Puebla `anthropic.api_key`. Convención estándar del SDK de Anthropic. |
| `HOME` | `internal/cli/init.go` | Usada por `rousseau init` para calcular la ruta de estado por defecto. |

## Variables propiedad de los SDK que rousseau no toca

Algunas bibliotecas de proveedores toman su propio entorno. Rousseau no las lee directamente, pero influyen en el comportamiento cuando se selecciona el proveedor correspondiente:

| Variable | Consumidor | Notas |
|---|---|---|
| `AWS_PROFILE`, `AWS_REGION`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_WEB_IDENTITY_TOKEN_FILE` | `aws-sdk-go-v2` (Bedrock) | La cadena estándar de credenciales. Prefiere IRSA o creds basadas en perfil sobre claves estáticas. |
| `GOOGLE_APPLICATION_CREDENTIALS` | Bibliotecas de auth de Google (Vertex) | Ruta a un JSON de service account. Sustituida por `vertex.credentials_file` en `config.yaml` si está definida. |
| `OPENAI_API_KEY` | Los clientes Go aguas arriba de OpenAI suelen leerla | Rousseau cablea la clave explícitamente a través de `openai.api_key`; nada implícito. |
| `HTTP_PROXY`, `HTTPS_PROXY`, `NO_PROXY` | Go net/http | Variables universales de proxy de Go. Útiles para rutas de egreso corporativo. |

## Variables de rutas XDG

Rousseau sigue la XDG Base Directory Specification para state y config, con dos fallbacks:

| Variable | Efecto |
|---|---|
| `XDG_CONFIG_HOME` | `$XDG_CONFIG_HOME/rousseau/config.yaml` es la ruta de config por defecto (referenciada en `internal/cli/root.go`). |
| `XDG_DATA_HOME` | Ruta de state por defecto `$XDG_DATA_HOME/rousseau/sessions.db` (referenciada por `whatsapp.go`, `skills.go`, `init.go`). |
| `HOME` | Fallback cuando las variables XDG no están definidas; rousseau usa `os.UserHomeDir()` en `internal/config/config.go`. |

La unidad Quadlet del contenedor en `docker/rousseau-agent.container` establece tanto `HOME=/home/rousseau` como `XDG_DATA_HOME=/home/rousseau/.local/share`.

## Higiene de secretos

Almacena los secretos en uno de tres sitios:

1. **Un `EnvironmentFile=` de una unidad systemd** — `chmod 0600`, propiedad de root o del usuario según corresponda. Referenciado desde la unidad Quadlet — consulta el [tutorial de despliegue en VPS](/es/tutorials/deploy-to-a-vps/).
2. **Un archivo `.env` cargado por tu shell.** Solo para uso en escritorio; mantenlo fuera del control de código.
3. **Un gestor de secretos.** AWS Secrets Manager, HashiCorp Vault o `pass`/`gopass`. Canaliza el valor al proceso al arrancar.

Nunca comprometas secretos en `config.yaml`. `config.yaml` es el sitio correcto para allowlists, URLs base y configuración no secreta; es el sitio equivocado para API keys y tokens de bot.

## Solución de problemas

### `ROUSSEAU_...` establecida pero rousseau sigue usando el default

Las variables env se leen al arrancar. Reinicia el demonio tras el export. Verifica también la regla de transformación: los puntos en la clave de configuración se convierten en guiones bajos, y el prefijo es `ROUSSEAU_` (mayúscula, exacto).

### `ANTHROPIC_API_KEY` aparentemente ignorada

La env var solo se consulta cuando `provider: anthropic` está activo. Bajo `provider: claudecli`, el CLI `claude` lee sus propias credenciales.

### Valor distinto en hosts distintos

La precedencia es **flag &gt; env &gt; archivo &gt; default**. Si un flag está establecido (desde el `ExecStart` de la unidad systemd por ejemplo), gana tanto sobre env como sobre archivo.

### `GOOGLE_APPLICATION_CREDENTIALS` ilegible dentro del contenedor

Asegúrate de que el archivo esté bind-mounted en solo lectura dentro del contenedor y que el UID del contenedor (1000 por defecto) pueda leerlo.

## Páginas relacionadas

- [Configuración](/es/configuration/) — cada campo de configuración con su default.
- [Referencia: esquema de configuración](/es/reference/config-schema/) — la estructura YAML.
- [Referencia: comandos CLI](/es/reference/cli-commands/) — flags por transporte.
- [Guías: onboarding empresarial](/es/guides/enterprise-onboarding/) — manejo de secretos en producción.
- [Despliegue](/es/deployment/) — opciones de gestión de secretos.

## Lecturas adicionales

- `internal/config/config.go` — `Load` establece el prefijo env y el reemplazador de guion bajo por punto.
- `internal/cli/root.go` — dónde se llama a `Load`.
