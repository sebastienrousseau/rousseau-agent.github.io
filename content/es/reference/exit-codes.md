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
description: "Exit codes and signal semantics for the rousseau-agent binary. What init systems can rely on."
keywords: "exit codes, signals, sigterm, sigint, systemd, restart policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/reference/exit-codes/"
subtitle: "Exit codes and signal semantics."
tags: "reference, exit-codes, signals"
title: "Códigos de salida"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "exit codes, signals, sigterm, sigint, systemd, restart policy"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Códigos de salida"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 51
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/exit-codes/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/exit-codes/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Códigos de salida"
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
twitter_description: "Exit codes and signal semantics for the rousseau-agent binary. What init systems can rely on."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Códigos de salida"
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

## Códigos de salida

El CLI de rousseau es deliberadamente conservador: dos códigos de salida cubren cada ruta.

| Código | Emitido por | Significado |
|---|---|---|
| 0 | `cmd/rousseau/main.go` vía `cli.Execute` | El comando se completó exitosamente. Los daemons salen con 0 en apagado ordenado (SIGINT / SIGTERM). |
| 1 | `cmd/rousseau/main.go` vía `cli.Execute` | El comando falló. La cadena de error se imprime a stderr. Cada falla: error de parseo de configuración, fallo de auth de proveedor, panic de transporte, error de cableado de herramienta, se mapea a este código. |

`rousseau doctor` sigue la misma convención: salida 0 cuando cada chequeo pasa, salida 1 cuando algún chequeo es `fail`. Las advertencias y filas de nivel info no afectan el código de salida.

Releases futuros podrían dividir las fallas en códigos distintos (config vs runtime vs red). Hoy, trata cualquier salida distinta de cero como reintentable pero que requiere inspección de logs.

## Manejo de señales

`cmd/rousseau/main.go` instala un manejador de señales que cancela el `context.Context` raíz en `SIGINT` y `SIGTERM`. Cada componente de larga vida (bucle del agente, transporte, planificador cron, servidor MCP) honra la cancelación de contexto, por lo que la ruta de apagado es:

1. Se recibe `SIGINT` / `SIGTERM`.
2. Se cancela el contexto raíz.
3. Los transportes llaman a `Stop()` sobre sí mismos, vaciando mensajes en vuelo.
4. El planificador cron deja de aceptar nuevos disparos; los disparos en ejecución terminan.
5. Se llama a `Close()` del almacén de sesiones vía `defer`, haciendo checkpoint del WAL.
6. `Execute` retorna 0.

`SIGKILL` no puede capturarse. Si al daemon le hacen `kill -9` a mitad de turno, el WAL del almacén de sesiones protege contra corrupción pero el turno en vuelo no se persiste. El siguiente lanzamiento retoma desde el último estado guardado.

## Política de reinicio de systemd

Para la unidad Quadlet de referencia:

```
[Service]
Restart=on-failure
RestartSec=10
```

`on-failure` reinicia en cualquier salida distinta de cero; combinado con la convención de códigos de salida de rousseau esto significa: salida 0 (`SIGTERM` desde `systemctl stop`) no reinicia, salida 1 sí.

Para daemons que caen en errores persistentes (configuración mala, auth de proveedor incorrecta), `on-failure` hará thrashing. Observa `journalctl` para la razón de la falla antes de asumir que el bucle de retry se recuperará.

## Semántica de probes de Kubernetes

Rousseau no distribuye endpoint HTTP de liveness/readiness por diseño. Los probes de Kubernetes deben ser o:

- Probes `exec` ejecutando `rousseau doctor --config /etc/rousseau/config.yaml` (retorna 0 en sano, 1 en falla), o
- Ausentes, con el pod confiando en `restartPolicy: Always` y el manejo de errores propio del daemon.

`rousseau doctor` es barato (~50ms) así que es un buen liveness probe. No lo uses como readiness probe: un `fail` en `provider.claudecli.binary` no debería sacar al pod de rotación si la falla no se auto-sana.

## Errores manejados

Los errores que producen código de salida 1 a través de la superficie de error del CLI incluyen:

- **Fallo de carga de configuración**: error de parseo YAML, campo desconocido, tipo inválido.
- **Fallo de auth de proveedor**: clave de API faltante, credenciales inválidas, región inválida de Bedrock / Vertex.
- **Fallo de arranque de transporte**: token faltante, host IMAP/SMTP inalcanzable, error de protocolo whatsmeow.
- **Fallo de apertura del almacén**: permiso denegado en `~/.local/share/rousseau/`, disco lleno.
- **Fallo de chequeo de doctor**: cualquier fila `fail` hace que doctor retorne salida 1.
- **Fallo de parseo de expresión cron**: `rousseau cron add` valida antes de persistir.

## Panics no manejados

`go test -race` se ejecuta en cada build de CI, por lo que los panics son extremadamente raros. Cuando ocurren, el runtime de Go imprime el panic + stack trace a stderr y sale con un código distinto de cero del runtime, típicamente 2, pero esta es la convención de Go y no algo que rousseau controle.

Para producción, envuelve el daemon en un supervisor que capture stderr en salida anormal y reporte el trace.

## Siguiente

- [Guía de usuario: CLI](/es/user-guide/cli/): cada comando.
- [Guías: Observabilidad](/es/guides/observability/): exponer la señal slog más allá del código de salida.
- [Solución de problemas](/es/troubleshooting/): qué hacer cuando el código de salida no es suficiente.
