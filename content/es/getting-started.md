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
description: "Install rousseau-agent from source, go install, or a cosign-verified release. Run rousseau chat and configure the first chat transport."
keywords: "install, quickstart, rousseau chat, cosign verify, go install, systemd, podman"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/getting-started/"
subtitle: "Instalar rousseau-agent y llegar a tu primer transporte."
tags: "install, quickstart, getting-started"
title: "Primeros pasos"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "install, quickstart, rousseau chat, cosign verify, go install, systemd, podman"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Primeros pasos"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 2
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Primeros pasos"
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
twitter_description: "Install rousseau-agent from source, go install, or a cosign-verified release. Run rousseau chat and configure the first chat transport."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Primeros pasos"
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

## Para quién es esto

- **Desarrolladores individuales** que quieren un asistente de programación que se ejecute en su propio equipo y utilice su CLI `claude` existente. Sin claves de API canalizadas a través de la configuración de rousseau, sin ningún intermediario en la nube.
- **Operadores de plataforma** que ejecutan un agente de programación compartido para un equipo detrás de un perímetro corporativo. Rousseau es un único binario Go estático en un contenedor Podman sin root con capacidades eliminadas — desplegable junto a cualquier otro servicio de systemd.
- **Revisores de seguridad** que evalúan un agente antes de su despliegue. Procedencia SLSA-3, sumas de verificación de release firmadas con cosign, SBOM CycloneDX, builds reproducibles y cada frontera de confianza documentada en [Seguridad](/es/security/).

## La ruta más rápida

1. **Si ya tienes el CLI `claude` instalado y autenticado**, el inicio más rápido es `rousseau chat` con el proveedor `claudecli` por defecto — la autenticación se hereda, sin claves que canalizar. Continúa con [Primera ejecución](#first-run) más abajo.
2. **Si prefieres una ruta directa a la API con tu propia clave**, define `ANTHROPIC_API_KEY` y cambia a `provider: anthropic` en `~/.config/rousseau/config.yaml`. Consulta [proveedor Anthropic](/es/providers/anthropic/).
3. **Si estás en una empresa con AWS Bedrock o Google Vertex**, elige el proveedor correspondiente — [Bedrock](/es/providers/bedrock/) usa la cadena estándar de credenciales de AWS; [Vertex](/es/providers/vertex/) lee un JSON de cuenta de servicio. Ningún secreto reside en el archivo de configuración de rousseau.
4. **Si estás en un entorno aislado o quieres inferencia totalmente autoalojada**, apunta rousseau a un endpoint compatible con OpenAI — Ollama, vLLM, LM Studio o cualquier shim. Consulta [proveedor compatible con OpenAI](/es/providers/openai-compatible/).

## Qué tendrás al final

- Un binario `rousseau` en `$PATH` verificado contra una firma cosign (ruta de release) o compilado desde fuente (`make check` ejecuta el mismo bloqueo de 18 linters + race + govulncheck que impone CI).
- Un TUI `rousseau chat` funcional respaldado por el proveedor que hayas elegido.
- Un almacén de sesiones SQLite en `~/.local/share/rousseau/sessions.db` — cada turno se persiste, con recuperación entre sesiones disponible a través de FTS5.
- Opcionalmente: un transporte de chat en vivo (WhatsApp, Slack, Signal, ...) accesible desde tu teléfono.

## ¿Prefieres verlo?

Una captura de pantalla breve del flujo siguiente está en la hoja de ruta. Hasta entonces, todo el proceso cabe en esta página — la mayoría de operadores lo completa en menos de diez minutos.

## Requisitos del sistema

| Requisito | Versión | Notas |
|---|---|---|
| Cadena de herramientas Go | 1.26+ | `CGO_ENABLED=0`; el binario es totalmente estático. |
| Runtime de contenedores | Podman 4.4+ | El despliegue de referencia usa Podman sin root + una unidad Quadlet de systemd. Docker funciona pero Quadlet es específico de Podman. |
| CLI `claude` | último | Solo si se usa el proveedor `claudecli` por defecto. |
| `signal-cli` | 0.13+ | Solo si se usa el transporte Signal. |
| Servidor BlueBubbles | 1.9+ | Solo si se usa el transporte iMessage (requiere un host macOS). |
| `whisper.cpp` | 1.5+ | Solo si habilitas la transcripción de notas de voz de WhatsApp. |

## Instalación

### Desde fuente

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` ejecuta vet, `golangci-lint`, `go test -race` y `govulncheck` — los mismos bloqueos que impone CI.

### Mediante `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

El binario incorpora `modernc.org/sqlite`, por lo que no hay dependencia de libc o CGo en tiempo de ejecución.

### Desde un release firmado

Cada release etiquetado publica un archivo con sumas de verificación, un SBOM CycloneDX, una atestación de procedencia SLSA-3 y una firma cosign del archivo de sumas de verificación. Verifica siempre antes de ejecutar:

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_<version>_checksums.txt.sig \
  rousseau_<version>_checksums.txt

sha256sum -c rousseau_<version>_checksums.txt
```

La expresión regular de identidad del certificado es lo que fija la identidad del firmante; no la debilites.

## Primera ejecución

### Chat en terminal

```sh
rousseau chat
```

TUI Bubble Tea. Enter para enviar, `Ctrl+C` para salir. El proveedor por defecto es `claudecli`, que hereda la autenticación de tu instalación local de Claude Code; no se canalizan claves de API a través de la configuración de rousseau.

El historial de sesiones se persiste en `~/.local/share/rousseau/sessions.db` (SQLite con journaling WAL y FTS5 para recuperación entre sesiones).

### Tu primer transporte de chat

WhatsApp es el transporte de referencia (la UX de emparejamiento es la más estricta). Empareja en la primera ejecución escaneando el QR desde tu teléfono:

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

El JID en formato E.164 (`<dígitos>@s.whatsapp.net`) restringe el manejo de mensajes entrantes; cualquier otro remitente se descarta silenciosamente. El estado de emparejamiento se almacena en `whatsapp.db` junto al almacén de sesiones.

Otros transportes siguen la misma forma:

```sh
rousseau slack   --app-token xapp-... --bot-token xoxb-...
rousseau discord --token bot-token
rousseau telegram --token 12345:ABC
rousseau matrix  --homeserver-url https://matrix.org --access-token ... --user-id @bot:matrix.org
```

Cada `rousseau <transport> --help` lista sus flags. Los valores por defecto vienen de `~/.config/rousseau/config.yaml`.

## Dónde se almacena el estado

| Ruta | Propósito |
|---|---|
| `~/.config/rousseau/config.yaml` | Archivo de configuración a nivel de usuario (Viper). |
| `~/.local/share/rousseau/sessions.db` | Sesiones, tareas cron, mapa de JID, índice de recuperación FTS5. |
| `~/.local/share/rousseau/whatsapp.db` | Credenciales de dispositivo Whatsmeow (mantenidas por separado para que un re-enlace de dispositivo no afecte las conversaciones). |
| `~/.claude/` | Tokens OAuth del CLI `claude`, solo al usar el proveedor `claudecli`. |

## Siguientes pasos

- [Conceptos](/es/concepts/) — el bucle del agente, el almacén de sesiones, MCP, cron, skills.
- [Configuración](/es/configuration/) — cada opción.
- [Despliegue](/es/deployment/) — cómo ejecutar el servicio bajo systemd.
