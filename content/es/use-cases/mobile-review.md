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
changefreq: "monthly"
description: "Use case narrative: reviewing pull requests from WhatsApp on the train, driven by rousseau-agent on a home box."
keywords: "mobile review, whatsapp, pr review, commute, use case, pull request"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/use-cases/mobile-review/"
subtitle: "Reviewing PRs from your phone on the train."
tags: "use-cases, whatsapp, mobile, pr"
title: "Caso de uso: revisión de PR desde el móvil"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mobile review, whatsapp, pr review, commute, use case, pull request"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Caso de uso: revisión de PR desde el móvil"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 72
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/mobile-review/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/mobile-review/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Caso de uso: revisión de PR desde el móvil"
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
twitter_description: "Use case narrative: reviewing pull requests from WhatsApp on the train, driven by rousseau-agent on a home box."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Caso de uso: revisión de PR desde el móvil"
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

## La historia

Eres un staff engineer en una empresa de tamaño medio. Tu bandeja de entrada tiene ocho PRs abiertos esperando tu revisión. Estás en un viaje en tren de 45 minutos y tienes cobertura pero no portátil. Históricamente, revisar PRs desde el móvil significa entrecerrar los ojos sobre la vista de diff de GitHub y teclear comentarios huecos como "LGTM".

Rousseau vive en el pequeño Intel NUC de tu armario. Tiene una conexión de WhatsApp a tu JID, `bypassPermissions` sobre el CLI local `claude` y acceso de lectura a tus checkouts locales de los tres repositorios que revisas. Envías un DM por WhatsApp:

> revisa el PR #4821 en checkout-service

Rousseau ejecuta `gh pr diff 4821`, lee el código y responde:

> El PR #4821 añade retry con backoff al handler del webhook de Stripe. Tres observaciones:
>
> 1. El backoff no tiene tope — si Stripe está realmente caído, acumularemos goroutines indefinidamente. Sugiero un `context.WithTimeout` en el llamador.
> 2. El archivo de pruebas añade dos pruebas nuevas pero ninguna cubre la ruta del timeout.
> 3. `pkg/webhook.go:82` — el mutex se mantiene durante la llamada de red. Menor.
>
> ¿Redacto un stub de comentario de revisión?

Respondes:

> sí, con los tres

Rousseau usa `gh pr review` con `--draft` (el approver bloquea la aprobación final; un humano aún tiene que hacer clic en "submit review"). Cuando llegas a tu escritorio, el comentario borrador te está esperando.

## Lo que eso requiere

### El demonio

Rousseau en el NUC como contenedor Podman sin root:

- **Proveedor**: `claudecli` — hereda tu autenticación local de Claude Code.
- **Transporte**: WhatsApp — el transporte de elección para alcance móvil.
- **Estado**: `~/.local/share/rousseau/sessions.db`.

### Configuración

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: bypassPermissions

whatsapp:
  reply_header: "🚂 *rousseau*\n\n"

log:
  level: info
  format: text                # este es un demonio de un solo usuario; los logs en texto están bien

agent:
  max_iterations: 32
  compression:
    enabled: true             # claudecli con nivel de suscripción; la compresión es gratis
    trigger_messages: 60
    keep_recent: 8
  approver:
    mode: pattern
    default: deny
    reason: "denied — this daemon reviews code, it does not merge it"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(gh pr view|gh pr diff|gh pr list|gh pr review --draft|gh pr comment|git status|git diff|git log|git show) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(go test|go vet|go build|npm test|pnpm test|cargo check) "}
    deny:
      - {tool: bash, match: "gh pr merge|gh pr close|gh pr approve"}
      - {tool: bash, match: "git (push|reset --hard|clean)"}
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit,  match: "\"path\":\"/etc/|/root/|/var/"}
```

### Los bind mounts

- `~/repos/checkout-service/` (solo lectura).
- `~/repos/payments-api/` (solo lectura).
- `~/repos/web-frontend/` (solo lectura).
- `~/.claude/` — los tokens OAuth de Claude Code (lectura-escritura, pero solo para el refresh del token).
- `~/.config/gh/` — el token OAuth de GitHub CLI (lectura-escritura, mismo motivo).

Los mounts de solo lectura evitan que el modelo edite accidentalmente tu copia de trabajo. Las revisiones pasan por GitHub, no por tu checkout.

### Primer arranque

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Escaneas el código QR una vez. A partir de ahí el demonio vive en la unidad Quadlet y arranca al reiniciar el host. Tu allowlist es el JID de tu propio teléfono personal.

## La postura de seguridad

- **La allowlist bloquea el transporte.** Solo tu teléfono puede dirigir el demonio. Cualquier otra persona que descubra el número queda descartada en silencio.
- **El pattern approver bloquea cada merge / push / close.** Rousseau revisa, redacta y comenta — un humano aún debe hacer clic en "Merge" o "Approve".
- **Los mounts de solo lectura** protegen tus checkouts de trabajo.
- **`bypassPermissions` sobre claudecli** solo es tolerable porque el approver hace el trabajo de seguridad. Nunca combines `bypassPermissions` con `mode: allow_all`.

## El alcance

- **La señal se cae en el metro.** La backpressure de WhatsApp es elegante — envías una pregunta, obtienes una respuesta cuando el demonio tiene señal para responder. Rousseau no necesita mantener una sesión TCP viva con tu teléfono.
- **Las notas de voz funcionan.** Con el [modo voz](/es/user-guide/voice-mode/) habilitado y `whisper.cpp` instalado en el NUC, puedes dictar una nota de voz "cuál es el diff del 4821" y obtener una respuesta en texto. Útil cuando teclear en el móvil en un tren en movimiento es molesto.
- **El demonio corre en tu hardware.** Nada sobre tu razonamiento de revisión va a un SaaS de terceros. La única llamada saliente es el subproceso del CLI `claude` a Anthropic, usando tu suscripción existente.

## Lo que rousseau no hace aquí

- **No hace clic en "Merge".** Esa es una decisión humana y el approver la impone.
- **No aprende tu estilo de revisión.** El siguiente PR obtiene la misma checklist genérica salvo que redactes una [skill](/es/skills/) que capture tu estilo.
- **No pone en cola las revisiones.** Cada solicitud es independiente; no hay un job en background del tipo "revisa todos mis PRs abiertos" (a menos que uno se cablee vía [cron](/es/guides/scheduled-tasks/)).

## Lo que cambiarías con más carga

- Añade una [skill](/es/skills/) llamada `pr-review-checklist.md` que codifique las seis cosas que siempre revisas. Las skills se empalman al prompt del sistema cuando aparece un trigger coincidente en el mensaje del usuario.
- Añade un cron nocturno: `0 8 * * 1-5 rousseau ... entrega un resumen de cada PR abierto`.
- Cambia a una ruta API de Anthropic de pago si los rate limits de la suscripción de `claudecli` se convierten en cuello de botella. Cero cambios de configuración aguas abajo.

## Páginas relacionadas

- [Transporte WhatsApp](/es/transports/whatsapp/) — la referencia del transporte.
- [Proveedor claudecli](/es/providers/claudecli/) — autenticación heredada.
- [Skills](/es/skills/) — cómo codificar tu estilo de revisión.
- [Modo voz](/es/user-guide/voice-mode/) — dicta revisiones.
