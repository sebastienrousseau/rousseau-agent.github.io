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
changefreq: "weekly"
description: "Complete configuration reference for rousseau-agent. Every provider, transport, and agent knob with type, default, and effect."
keywords: "configuration, config.yaml, viper, precedence, YAML, provider, transport, approver, compression"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/configuration/"
subtitle: "Cada campo de internal/config/config.go."
tags: "configuration, reference"
title: "Referencia de configuración"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "configuration, config.yaml, viper, precedence, YAML, provider, transport, approver, compression"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Referencia de configuración"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 4
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/configuration/index.html"
item_link: "https://docs.rousseau-agent.dev/configuration/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Referencia de configuración"
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
twitter_description: "Complete configuration reference for rousseau-agent. Every provider, transport, and agent knob with type, default, and effect."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Referencia de configuración"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Gracias a cada operador que ejecuta su propio agente de codificación."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Precedencia

`rousseau` resuelve la configuración en el orden **flag > env > archivo > por defecto**. El archivo se encuentra en `~/.config/rousseau/config.yaml` por defecto; anúlalo con `--config`.

Las variables de entorno usan el prefijo `ROUSSEAU_` reemplazando `.` con `_` — así `provider` se convierte en `ROUSSEAU_PROVIDER`, `anthropic.api_key` se convierte en `ROUSSEAU_ANTHROPIC_API_KEY`. `ANTHROPIC_API_KEY` también se reconoce directamente (se enlaza a `anthropic.api_key` en el momento de la carga).

## Nivel superior

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `provider` | string | `claudecli` | Backend LLM: `claudecli`, `anthropic`, `bedrock`, `vertex`, `openai`, `openrouter`, `ollama`. |

## `anthropic` — API directa de Anthropic

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `api_key` | string | *desde `ANTHROPIC_API_KEY`* | Bearer para `api.anthropic.com`. Se rechaza si está vacío cuando se selecciona el proveedor. |
| `model` | string | `claude-sonnet-4-6` | Identificador de modelo pasado al SDK. |
| `max_tokens` | int64 | `4096` | Limita los tokens de salida por completación. |

Consulta [/providers/anthropic/](/es/providers/anthropic/).

## `bedrock` — AWS Bedrock

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `region` | string | *requerido* | Región de AWS (`us-east-1`, `eu-west-2`). |
| `model` | string | *requerido* | ID de modelo de Bedrock (`anthropic.claude-sonnet-4-6-20260101-v1:0`). |
| `profile` | string | *vacío* | Perfil de credenciales de `~/.aws/credentials`. Si está vacío, se usa la cadena estándar de credenciales de AWS. |
| `max_tokens` | int64 | por defecto del SDK | Limita los tokens de salida. |

Consulta [/providers/bedrock/](/es/providers/bedrock/).

## `vertex` — Google Vertex AI

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `project` | string | *requerido* | ID del proyecto GCP. |
| `region` | string | *requerido* | Región de Vertex (`us-central1`). |
| `model` | string | *requerido* | ID de modelo Anthropic en Vertex (`claude-sonnet-4-6@20260101`). |
| `credentials_file` | string | *vacío* | Ruta al JSON de cuenta de servicio o usuario autorizado. Vacío usa Application Default Credentials. |
| `max_tokens` | int64 | `4096` | Limita los tokens de salida. |

Consulta [/providers/vertex/](/es/providers/vertex/).

## `claudecli` — subproceso contra el CLI `claude` local

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `binary` | string | `claude` | Ejecutable, resuelto en `$PATH`. |
| `model` | string | *vacío* | Pasado a `--model`. Vacío usa el valor por defecto de claude. |
| `permission_mode` | string | *vacío* | Pasado a `--permission-mode`. Valores: `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. Los servicios no supervisados normalmente necesitan `bypassPermissions`. |
| `extra_args` | []string | `[]` | Antepuestos antes de `-p` en cada invocación. Útil para `--add-dir`, `--allowed-tools`, `--disallowed-tools`, `--plugin-dir`. |

Consulta [/providers/claudecli/](/es/providers/claudecli/).

## `openai` / `openrouter` / `ollama` — endpoints compatibles con OpenAI

Misma forma. `openrouter.base_url` por defecto es `https://openrouter.ai/api/v1`; `ollama.base_url` por defecto es `http://localhost:11434/v1`; `ollama.api_key` por defecto es `not-required`.

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `api_key` | string | *requerido* | Token bearer. No vacío incluso para Ollama (cualquier marcador de posición sirve). |
| `model` | string | *requerido* | Identificador de modelo. No hay valor por defecto universal entre endpoints. |
| `base_url` | string | *por defecto del proveedor* | URL completa del endpoint. |
| `max_tokens` | int64 | por defecto del SDK | Limita los tokens de salida. |

Consulta [/providers/openai-compatible/](/es/providers/openai-compatible/).

## `log`

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `level` | string | `info` | `debug`, `info`, `warn`, `error`. |
| `format` | string | `text` | `text` (humano) o `json` (producción / agregación de logs). |

## `state`

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `path` | string | `~/.local/share/rousseau/sessions.db` | Ruta de la base de datos SQLite (modo WAL, `busy_timeout=15s`). |

## `agent`

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `system_prompt` | string | *vacío* | Anula el valor por defecto incorporado. |
| `max_iterations` | int | `32` | Limita los ciclos con el modelo por `Turn`. |
| `skills_dir` | string | *vacío* | Directorio de archivos skill `*.md`. Vacío desactiva los skills. |

### `agent.compression`

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `enabled` | bool | `false` | Habilita la compresión de sesión respaldada por LLM. |
| `trigger_messages` | int | `60` | Recuento de mensajes por encima del cual se activa la compresión. |
| `keep_recent` | int | `8` | Mensajes recientes preservados textualmente. |
| `prompt` | string | *incorporado* | Anula la instrucción de resumen por defecto. |

### `agent.approver`

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `mode` | string | `allow_all` | `allow_all`, `deny_all` o `pattern`. |
| `reason` | string | *vacío* | Motivo de denegación mostrado al modelo. |
| `default` | string | `deny` | Fallback cuando ninguna regla `allow` o `deny` coincide (modo pattern). |
| `allow` | []PatternEntry | `[]` | Reglas regex de permiso por herramienta. |
| `deny` | []PatternEntry | `[]` | Reglas regex de denegación por herramienta. La denegación gana sobre el permiso. |

Cada `PatternEntry` es `{tool: <nombre>, match: <regex>}`. `tool: ""` coincide con toda herramienta; `match: ""` coincide con toda entrada.

## Bloques de transporte

### `whatsapp`

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `reply_header` | string | `💎 *Rousseau Agent*\n\n` | Antepuesto a cada mensaje saliente. Ponlo en `" "` para desactivarlo. |
| `voice.enabled` | bool | `false` | Transcripción basada en Whisper para notas de voz entrantes. |
| `voice.binary` | string | `whisper` | Ejecutable de Whisper CLI. |
| `voice.model` | string | *vacío* | Pasado a `--model` (`base.en`, `small`). |
| `voice.model_path` | string | *vacío* | Ruta `.bin` explícita, tiene precedencia sobre `model`. |
| `voice.language` | string | *vacío* | Pasado a `--language`. Vacío autodetecta. |
| `voice.extra_args` | []string | `[]` | Añadidos a cada invocación de whisper. |

### `signal`

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `binary` | string | `signal-cli` | Ejecutable a invocar en modo daemon JSON-RPC. |
| `account` | string | *requerido* | Número telefónico E.164 con el que se ejecuta el servicio. |
| `extra_args` | []string | `[]` | Insertados entre `-a <account>` y `jsonRpc`. |
| `reply_header` | string | *vacío* | Antepuesto a cada mensaje saliente. |
| `allowlist` | []string | `[]` | Números E.164 cuyos mensajes se procesan. Vacío acepta todo remitente. |

### `telegram`

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `token` | string | *requerido* | Token de bot de BotFather. |
| `base_url` | string | `https://api.telegram.org` | Override para un servidor Bot API local. |
| `reply_header` | string | *vacío* | Antepuesto a cada respuesta saliente. |
| `allowlist` | []string | `[]` | IDs de usuario de Telegram cuyos mensajes se procesan. |

### `matrix`

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `homeserver_url` | string | *requerido* | URL base, por ejemplo `https://matrix.org`. |
| `access_token` | string | *requerido* | Token de acceso del usuario bot. |
| `user_id` | string | *vacío* | MXID completo del usuario bot (`@bot:matrix.org`). Opcional pero recomendado (supresión de eco de mensajes propios). |
| `reply_header` | string | *vacío* | Antepuesto a cada respuesta saliente. |
| `allowlist` | []string | `[]` | IDs de Matrix cuyos mensajes se procesan. |

### `slack`

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `app_token` | string | *requerido* | Token a nivel de app `xapp-*` con `connections:write`. |
| `bot_token` | string | *requerido* | Token de bot `xoxb-*` con `chat:write`. |
| `bot_user_id` | string | *vacío* | ID propio `U…` del usuario bot para prevención de bucles con mensajes propios. |
| `reply_header` | string | *vacío* | Antepuesto a cada mensaje saliente. |
| `allowlist` | []string | `[]` | IDs de usuario de Slack cuyos mensajes se procesan. |

### `discord`

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `token` | string | *requerido* | Token de bot del Developer Portal. |
| `reply_header` | string | *vacío* | Antepuesto a cada respuesta saliente. |
| `allowlist` | []string | `[]` | IDs de usuario de Discord cuyos mensajes se procesan. |

### `sms`

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `provider` | string | *requerido* | `twilio` o `vonage`. |
| `from` | string | *requerido* | Remitente E.164 o SID de Twilio Messaging Service. |
| `account_sid` | string | *requerido para twilio* | SID de cuenta de Twilio (`AC…`). |
| `auth_token` | string | *requerido* | Token de autenticación de Twilio o secreto de API de Vonage. |
| `api_key` | string | *requerido para vonage* | Clave de API de Vonage. |
| `base_url` | string | *por defecto del proveedor* | Override para endpoints regionales o de prueba. |
| `reply_header` | string | *vacío* | Antepuesto a cada mensaje saliente. |

### `imessage`

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `base_url` | string | *requerido* | URL del servidor BlueBubbles (`http://localhost:1234`). |
| `password` | string | *requerido* | Contraseña del servidor BlueBubbles. |
| `chat_guid` | string | *vacío* | GUID de destino saliente. |
| `poll_interval` | duration | `5s` | Cadencia de sondeo contra `/api/v1/message`. |
| `reply_header` | string | *vacío* | Antepuesto a cada mensaje saliente. |

### `email`

| Campo | Tipo | Por defecto | Efecto |
|---|---|---|---|
| `imap_addr` | string | *requerido* | `host:port` para IMAP envuelto en TLS (típicamente `:993`). |
| `imap_username` | string | *requerido* | Nombre de usuario IMAP. |
| `imap_password` | string | *requerido* | Contraseña IMAP. |
| `mailbox` | string | `INBOX` | Buzón a sondear. |
| `poll_interval` | duration | `30s` | Con qué frecuencia buscar correo UNSEEN. |
| `smtp_addr` | string | *requerido* | `host:port` para envío SMTP (típicamente `:587`). |
| `smtp_username` | string | *requerido* | Nombre de usuario SMTP. |
| `smtp_password` | string | *requerido* | Contraseña SMTP. |
| `from` | string | *requerido* | Dirección `From` del envelope y del encabezado. |
| `reply_header` | string | *vacío* | Antepuesto al cuerpo de cada mensaje saliente. |

## Ejemplo completo

```yaml
provider: claudecli

anthropic:
  api_key: sk-ant-...
  model: claude-sonnet-4-6
  max_tokens: 4096

bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
  profile: default

vertex:
  project: my-gcp-project
  region: us-central1
  model: claude-sonnet-4@20260101
  credentials_file: ~/.config/gcloud/vertex-key.json

claudecli:
  binary: claude
  model: sonnet
  permission_mode: bypassPermissions
  extra_args: []

log:
  level: info
  format: json

state:
  path: ~/.local/share/rousseau/sessions.db

agent:
  system_prompt: ""
  max_iterations: 32
  skills_dir: ~/.local/share/rousseau/skills
  compression:
    enabled: true
    trigger_messages: 60
    keep_recent: 8
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "^./workspace/.*"}
    deny:
      - {tool: bash, match: "rm -rf|sudo|:\\(\\)\\{ :\\|:& \\};:"}

whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
  voice:
    enabled: false

signal:
  account: "+447900123456"
  allowlist: ["+447900654321"]

telegram:
  token: "123:ABC"
  allowlist: ["12345678"]

matrix:
  homeserver_url: "https://matrix.org"
  access_token: "syt_..."
  user_id: "@bot:matrix.org"
  allowlist: ["@alice:matrix.org"]

slack:
  app_token: "xapp-..."
  bot_token: "xoxb-..."
  bot_user_id: "U0123ABCD"

discord:
  token: "bot-token"
  allowlist: ["123456789012345678"]

sms:
  provider: twilio
  from: "+15550000000"
  account_sid: "AC..."
  auth_token: "..."

imessage:
  base_url: "http://localhost:1234"
  password: "..."
  poll_interval: "5s"

email:
  imap_addr: "imap.example.com:993"
  imap_username: "bot@example.com"
  imap_password: "..."
  smtp_addr: "smtp.example.com:587"
  smtp_username: "bot@example.com"
  smtp_password: "..."
  from: "bot@example.com"
  poll_interval: "30s"
```

## Solución de problemas

### `config: unmarshal: 1 error(s) decoding: ...`

El YAML es válido pero un campo tiene el tipo incorrecto. El mensaje de error indica el campo — verifica el tipo en `internal/config/config.go`.

### La sobrescritura por variable de entorno no se aplica

Rousseau prefija las variables de entorno con `ROUSSEAU_` y reemplaza puntos por guiones bajos. `anthropic.model` se convierte en `ROUSSEAU_ANTHROPIC_MODEL`. `ANTHROPIC_API_KEY` es un caso especial conectado directamente a `anthropic.api_key`.

### `config: read: yaml: line X: found character that cannot start any token`

Indentación con tabuladores. YAML requiere espacios.

### Los cambios en `config.yaml` no surten efecto

Rousseau lee la configuración una vez al inicio. Reinicia el servicio.

### Parecen estar activos dos valores de configuración

La precedencia es **flag > env > archivo > por defecto**. Habilita `log.level: debug` y busca con grep `config.loaded` para ver el valor resuelto.

## Páginas relacionadas

- [Referencia: Esquema de configuración](/es/reference/config-schema/) — cada campo.
- [Referencia: Variables de entorno](/es/reference/environment-variables/) — matriz de sobrescritura.
- [Referencia: Comandos CLI](/es/reference/cli-commands/) — flags por transporte.
- [Proveedores](/es/providers/) — bloques específicos por proveedor.
- [Transportes](/es/transports/) — bloques específicos por transporte.

## Lectura adicional

- `internal/config/config.go` — la struct autoritativa.
- `internal/cli/root.go` — donde se carga la configuración.
- `internal/config/config_test.go` — la matriz de pruebas de la semántica de carga.
