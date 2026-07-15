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
description: "Troubleshoot rousseau-agent: WhatsApp QR won't scan, reconnect loops, cosign verify failures, SELinux bind-mount errors, cron not firing, approval policy denying everything."
keywords: "troubleshooting, WhatsApp QR, reconnect loop, cosign verify, SELinux, bind mount, cron, approval policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/troubleshooting/"
subtitle: "Modos de fallo habituales y cómo resolverlos."
tags: "troubleshooting, support"
title: "Solución de problemas"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "troubleshooting, WhatsApp QR, reconnect loop, cosign verify, SELinux, bind mount, cron, approval policy"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Solución de problemas"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "support"
order: 27
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/troubleshooting/index.html"
item_link: "https://docs.rousseau-agent.dev/troubleshooting/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Solución de problemas"
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
twitter_description: "Troubleshoot rousseau-agent: WhatsApp QR won't scan, reconnect loops, cosign verify failures, SELinux bind-mount errors, cron not firing, approval policy denying everything."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Solución de problemas"
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

## WhatsApp: el QR no se escanea

Síntoma: `rousseau whatsapp` imprime un QR que la app del teléfono rechaza, o el diálogo de emparejamiento muestra "Este dispositivo no está emparejado con WhatsApp."

Correcciones:

1. **Reconstruye el contenedor.** Si estás ejecutando una imagen anterior, `whatsmeow` puede haber publicado una actualización de protocolo. Reconstruye:
   ```sh
   podman build -t rousseau-agent:local -f docker/Dockerfile .
   systemctl --user restart rousseau-agent.service
   ```
2. **Elimina `whatsapp.db`.** Un emparejamiento parcialmente completado deja la BD en un estado que whatsmeow no puede reutilizar. Elimínala y empareja de nuevo:
   ```sh
   rm ~/.local/share/rousseau/whatsapp.db
   ```
3. **Comprueba desviaciones de reloj.** El handshake de WhatsApp es sensible al tiempo. Si el reloj del contenedor está desfasado más de 30 segundos, el emparejamiento falla silenciosamente.
   ```sh
   timedatectl status
   ```

## Bucle de reconexión de WhatsApp

Síntoma: los logs muestran `whatsapp.connected` seguido de `whatsapp.disconnected` cada pocos segundos.

Correcciones:

1. **Desviación de reloj.** Misma corrección que la anterior.
2. **Allowlist mal configurada.** Cada mensaje entrante se descarta como no autorizado; algunos servidores cierran el socket tras demasiados descartes silenciosos. Añade los JIDs correctos con `--allow`.
3. **Bloqueo por parte de Meta.** Si la app móvil de WhatsApp muestra "Este dispositivo ha sido desconectado," Meta ha invalidado el emparejamiento. Empareja de nuevo desde un QR nuevo. Si ocurre repetidamente con el mismo número, deja de usar ese número.

## cosign verify-blob falla

Síntoma:

```
Error: no matching signatures
```

Correcciones:

1. **Regex de certificate-identity incorrecto.** El regex debe coincidir con el repositorio de GitHub que firmó el release. Para releases de rousseau-agent el valor correcto es:
   ```
   --certificate-identity-regexp 'sebastienrousseau/rousseau-agent'
   ```
   No uses `.*` — eso aceptaría una firma cosign de cualquier repositorio.
2. **Emisor OIDC incorrecto.** Las firmas cosign de GitHub Actions se emiten desde `https://token.actions.githubusercontent.com`. Otros proveedores de CI (GitLab, Buildkite) se emiten desde URLs distintas.
3. **Archivo de firma incorrecto.** Verifica que `<version>_checksums.txt.sig` corresponde al `_checksums.txt` que estás verificando (no una copia obsoleta de un release distinto).
4. **La raíz de confianza de Sigstore cambió.** Refresca con `cosign initialize`; la raíz de confianza se actualiza con una rotación lenta.

## El contenedor falla en el bind mount

Síntoma: `podman play kube` o `systemctl --user start rousseau-agent.service` falla con `permission denied` en un bind mount.

Correcciones:

1. **Etiqueta SELinux.** Cada línea de volumen debe terminar con `:Z` (o `:z` para compartido) para que Podman aplique la etiqueta SELinux correcta:
   ```
   Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
   ```
   `:Z` (mayúscula) es la etiqueta privada — apropiada para montajes de un solo contenedor. `:z` (minúscula) comparte la etiqueta entre contenedores.
2. **Mapeo `keep-id`.** Sin `UserNS=keep-id`, el UID 1000 del contenedor se remapea al rango subuid del host y no puede escribir en archivos propiedad del host. Asegúrate de que el Quadlet tenga:
   ```
   UserNS=keep-id
   ```
3. **Directorio faltante.** Podman no crea automáticamente los orígenes de bind mount. Crea el directorio primero:
   ```sh
   mkdir -p ~/.local/share/rousseau
   ```

## La tarea cron no se dispara

Síntoma: `rousseau cron list` muestra la tarea, pero no ocurre nada a la hora programada.

Correcciones:

1. **Comprueba el estado.** `rousseau status` reporta la actividad del planificador. Si el planificador no está en ejecución, el servicio que lo hospeda no está en ejecución.
2. **Zona horaria.** Los horarios usan la zona horaria local del servidor. Confirma con `timedatectl`. Establece `TZ=UTC` en el Quadlet si quieres una programación determinista independientemente del locale del host.
3. **Retraso de PollInterval.** Las nuevas tareas se activan dentro de `PollInterval` (60s por defecto). Espera un minuto.
4. **Fallo de entrega.** La tarea se disparó pero la entrega falló. Revisa los logs para `cron.delivery_failed`; el formato de destino es específico del transporte (consulta [/cron/](/es/cron/)).

## La política de aprobación rechaza todo

Síntoma: cada invocación de herramienta se deniega con "denied by pattern policy" y el modelo se niega a progresar.

Correcciones:

1. **Regla de permiso faltante.** En modo `pattern` con `default: deny`, cada invocación de herramienta necesita una regla de permiso que coincida. Añade una para las herramientas que quieras permitir:
   ```yaml
   agent:
     approver:
       mode: pattern
       default: deny
       allow:
         - {tool: read, match: ".*"}
         - {tool: grep, match: ".*"}
         - {tool: edit, match: "^./workspace/.*"}
   ```
2. **Deny vence a allow.** Una regla `deny` siempre gana sobre una regla `allow` para la misma herramienta. Revisa tu lista de deny para coincidencias accidentales excesivas.
3. **Sube el default.** Para sesiones supervisadas, `default: allow` con reglas deny más estrictas suele ser más viable:
   ```yaml
   agent:
     approver:
       mode: pattern
       default: allow
       deny:
         - {tool: bash, match: "rm -rf|sudo"}
   ```

## El proveedor devuelve 401

Síntoma: el agente falla con `provider: unauthorized`.

Correcciones:

1. **Clave de API incorrecta.** Para el proveedor Anthropic directo, verifica que `ANTHROPIC_API_KEY` esté exportada o definida en `~/.config/rousseau/config.yaml`.
2. **Cadena de credenciales incorrecta.** Para Bedrock, ejecuta `aws sts get-caller-identity` desde el contenedor para confirmar qué principal resuelve el SDK.
3. **Cuenta de servicio de Vertex.** Para el proveedor Vertex, confirma que el archivo en `vertex.credentials_file` sea legible dentro del contenedor y otorgue `roles/aiplatform.user`.

## El proveedor devuelve 429

Síntoma: el agente falla con `provider: rate limited`.

Correcciones:

1. **Reduce `max_tokens`.** Completaciones más cortas liberan la ventana de tasa más rápido.
2. **Habilita la compresión.** Los transcripts largos aumentan la presión de tokens de entrada; `agent.compression.enabled: true` colapsa los mensajes antiguos.
3. **Espera.** rousseau no reintenta dentro de `Complete`; quien llama (transporte de chat, planificador cron o `rousseau chat`) decide si reintentar y cómo.

## `rousseau chat` solo muestra una TUI en blanco

Síntoma: la TUI de Bubble Tea se abre pero sin cursor, sin viewport.

Correcciones:

1. **Entorno TERM.** rousseau requiere un terminal capaz de ANSI. Establece `TERM=xterm-256color` (o similar).
2. **stdin envuelto.** Ejecutar bajo `nohup` o una tubería quita el terminal. Ejecuta de forma interactiva.

## Slack: `invalid_auth` al inicio

Síntoma: `slack.starting` seguido inmediatamente de `invalid_auth`.

Correcciones:

1. **Tokens confundidos.** Rousseau necesita tanto `xapp-…` (a nivel de app, `--app-token`) como `xoxb-…` (bot, `--bot-token`). Pasar un app token donde se espera un bot token produce este error.
2. **App no instalada.** Después de crear scopes, haz clic en *Install to Workspace* en la configuración de la app de Slack. Los tokens solo son válidos tras la instalación.
3. **Token rotado.** Los tokens de Slack pueden ser rotados manualmente por un admin. Si has rotado uno, todos los servicios que lo usen deben reiniciarse con el nuevo valor.

## Slack: el bot responde a sus propios mensajes (bucle)

Síntoma: el mensaje saliente de rousseau dispara un evento entrante al que el servicio responde, causando respuestas descontroladas.

Correcciones:

1. **Establece `bot_user_id`.** El flag `--bot-user-id` (o `slack.bot_user_id` en config) le dice al servicio que ignore los mensajes enviados por ese ID de usuario. Obtenlo con `curl -H "Authorization: Bearer xoxb-..." https://slack.com/api/auth.test`.
2. **Verifica el filtro de eventos.** El transporte ignora subtipos `bot_message` por defecto, pero una app de Slack mal configurada puede sortear esto.

## Discord: el texto del mensaje llega vacío

Síntoma: `discord.incoming from=... body=` — los mensajes llegan pero sin contenido.

Correcciones:

1. **Message Content Intent desactivado.** En el Discord Developer Portal, bajo <em>Bot &gt; Privileged Gateway Intents</em>, activa **Message Content Intent**. Sin él, Discord elimina el texto del mensaje de los eventos del Gateway.
2. **Scopes faltantes.** La URL de invitación debe haber otorgado al bot `Read Message History` y `Send Messages` para el canal/DM que estés usando.

## Discord: `disallowed intents`

Síntoma: los errores de inicio muestran `Discord returned 4014 disallowed intents`.

Correcciones:

1. **Intents privilegiados.** Habilita *Message Content Intent* (ver arriba). Incluso si nunca lo pides, Discord devuelve 4014 si lo solicitas sin aprobación.
2. **Verificación.** Los bots en 100+ servidores deben ser verificados por Discord para usar intents privilegiados. Sigue el recorrido del portal de desarrolladores.

## Telegram: `unauthorized`

Síntoma: `telegram.starting` seguido de `getUpdates: 401`.

Correcciones:

1. **Token incorrecto.** BotFather devuelve el token una vez — no incluyas el punto final. El token tiene la forma `<bot_id>:<secret>`.
2. **Token revocado.** `/revoke` en BotFather invalida el token actual; obtén uno nuevo.

## Email: `dial tcp: i/o timeout`

Síntoma: la conexión IMAP o SMTP nunca se completa.

Correcciones:

1. **Puerto incorrecto.** IMAP es `993` (TLS implícito). El envío SMTP es `587` (STARTTLS) o `465` (TLS implícito). Rousseau usa TLS implícito en ambos — los servidores solo con STARTTLS aún no están soportados. Consulta [Transportes: Email](/es/transports/email/) para la migración.
2. **Egress bloqueado.** Los firewalls corporativos suelen bloquear el SMTP saliente. Prueba con `openssl s_client -connect smtp.example.com:465` desde el contenedor.
3. **El proveedor requiere contraseña de aplicación.** Gmail, Fastmail y similares requieren una contraseña de aplicación (no tu contraseña de cuenta) cuando 2FA está activado. Genera una desde la configuración de seguridad del proveedor.

## Vertex: `permission denied on resource`

Síntoma: `vertex: HTTP 403 permission denied on resource projects/.../models/claude-sonnet-4-6@…:rawPredict`.

Correcciones:

1. **Rol faltante.** Otorga `roles/aiplatform.user` a la cuenta de servicio o usuario que llama a la API. Los cambios de IAM tardan hasta un minuto en propagarse.
2. **Proyecto incorrecto.** El `project` en la configuración debe coincidir con el proyecto que posee la cuota. Si la facturación está en un proyecto distinto, usa quota-project mediante `gcloud auth application-default set-quota-project`.
3. **Discrepancia de región.** El modelo debe estar disponible en la región solicitada — el Vertex Model Garden lo indica.

## Bedrock: `You don't have access to the model`

Síntoma: `AccessDeniedException: You don't have access to the model with the specified model ID`.

Correcciones:

1. **Acceso al modelo no solicitado.** Bedrock requiere solicitud explícita de acceso al modelo vía la consola (*Foundation models &gt; Model access*). Incluso con IAM permitiendo `InvokeModel`, este paso es requerido.
2. **Región incorrecta.** La disponibilidad de modelos es regional. Revisa la consola de Bedrock.
3. **Mala configuración cross-account.** Si usas AssumeRole, verifica que la política del rol destino permita `bedrock:InvokeModel` sobre el ARN exacto del modelo.

## Ollama: `context deadline exceeded`

Síntoma: rousseau agota el tiempo de espera mientras Ollama aún está generando.

Correcciones:

1. **La inferencia por CPU es lenta.** Un modelo de 70B en un CPU de portátil puede tardar minutos por turno. Usa un modelo más pequeño (`llama3.1:8b`) o un host con GPU.
2. **Herencia del timeout.** rousseau usa el timeout HTTP por defecto del SDK. Si envuelves el proveedor tú mismo, extiende el timeout a al menos 120 s.

## Notas de voz: transcriptor no configurado

Síntoma: `whatsapp.audio_ignored reason=transcriber_not_configured`.

Correcciones:

1. **Whisper desactivado.** Establece `whatsapp.voice.enabled: true` en la configuración y asegúrate de que el binario `whisper` esté en `PATH` (o establece `whatsapp.voice.binary` a una ruta absoluta).
2. **Archivo de modelo faltante.** Establece `whatsapp.voice.model_path` a un archivo `.bin` explícito. Los modelos de Whisper.cpp se descargan manualmente — la configuración apunta a donde residen.

## Almacén de sesiones: `database is locked`

Síntoma: el escritor WAL se bloquea; las solicitudes agotan el tiempo.

Correcciones:

1. **Dos servicios, una BD.** SQLite con WAL admite lectores concurrentes pero solo un escritor. Si ejecutas dos procesos rousseau contra el mismo `state.path`, uno se bloqueará. Usa rutas de estado distintas.
2. **`busy_timeout` demasiado bajo.** El DSN establece `busy_timeout=15000`. Bajo contención sostenida, súbelo — pero investiga la causa raíz primero.
3. **Archivo WAL obsoleto.** Un escritor que crashee puede dejar `sessions.db-wal` bloqueado. Detén todo, elimina `sessions.db-wal` y `sessions.db-shm`, reinicia.

## MCP: Claude Desktop no ve las herramientas de rousseau

Síntoma: rousseau lanzado mediante `command: "rousseau"` en `claude_desktop_config.json` pero no aparecen herramientas.

Correcciones:

1. **Configuración no guardada.** Claude Desktop hace hot-reload al guardar; si editaste el archivo en una instancia en ejecución, reiníciala.
2. **`command` no está en PATH.** Claude Desktop lanza subprocesos desde su propio entorno; `/usr/local/bin/rousseau` puede no ser visible. Usa una ruta absoluta.
3. **Ruido en stderr.** rousseau escribe logs estructurados a stderr; un logger muy verboso puede saturar al host. Establece `log.level: warn` cuando ejecutes MCP contra un host estricto.

## Skills: `skill loader: parse: yaml: line X`

Síntoma: rousseau falla al iniciar con un error de parseo de YAML.

Correcciones:

1. **Frontmatter mal formado.** Los skills usan frontmatter YAML delimitado por `---`. Asegúrate de que ambas vallas estén presentes y de que no haya indentación con tabuladores.
2. **Dos puntos sin comillas.** Un dos puntos dentro de un valor (`description: this: that`) se parsea como un map anidado. Entrecomilla el valor: `description: "this: that"`.

## `rousseau doctor` reporta `warn`

Síntoma: doctor se completa pero con filas ámbar.

Correcciones:

1. **Lee el motivo.** Cada fila warn incluye un motivo. Los comunes: `whatsapp.paired=false` (nunca enlazado), `state.wal_size=large` (checkpoint atrasado), `provider.claudecli.model=unset` (usando el default de claude).
2. **Los warns no son fallos.** El servicio arrancará; la fila señala algo que vale la pena revisar.

## Kubernetes: pod atascado en `CrashLoopBackOff`

Síntoma: el deployment nunca llega a Ready.

Correcciones:

1. **Lee los logs.** `kubectl logs -p <pod>` muestra el stderr del contenedor previo. Nueve de cada diez veces es un error de configuración o credenciales.
2. **Volumen de estado faltante.** Sin un PVC para `~/.local/share/rousseau`, el emparejamiento no sobrevive al reinicio y el servicio puede entrar en bucle intentando re-emparejar.
3. **Mala configuración de IRSA / Workload Identity.** Verifica que la anotación de la cuenta de servicio coincida con un rol de IAM que tenga permisos del proveedor. `kubectl exec` en el pod y ejecuta `aws sts get-caller-identity` (Bedrock) o `gcloud auth print-access-token` (Vertex) para confirmar.

## El conjunto de reglas nftables bloquea el egress del proveedor

Síntoma: `dial tcp: i/o timeout` en la primera llamada al proveedor tras aplicar un conjunto de reglas de egress.

Correcciones:

1. **CIDR rotado.** Los rangos de IP del proveedor cambian. Usa egress basado en DNS mediante un ipset que se refresque en un cron, o usa un proxy de egress que resuelva en el momento de la conexión.
2. **DNS bloqueado.** El conjunto de reglas de egress debe permitir UDP/53 (o TCP/53) hacia tu resolvedor DNS.

## Faltan campos en los logs estructurados

Síntoma: `whatsapp.incoming` aparece con `from` y sin otros atributos.

Correcciones:

1. **Nivel de log demasiado alto.** Algunos campos solo se emiten en `debug`. Establece `log.level: debug` en la configuración.
2. **Parser JSON eliminando campos.** Redirigir a través de un filtro que quita campos desconocidos puede eliminar `elapsed`, `bytes`, etc. Verifica contra stdout sin procesar.

## Páginas relacionadas

- [Primeros pasos: Tu primer transporte](/es/getting-started/first-transport/) — recorrido de principio a fin.
- [Proveedores](/es/providers/) — solución de problemas por proveedor.
- [Transportes](/es/transports/) — solución de problemas por transporte.
- [Configuración](/es/configuration/) — la fuente de verdad para cada opción.
- [Seguridad](/es/security/) — fronteras de confianza y rastro de auditoría.

## Lectura adicional

- `internal/cli/doctor.go` — la implementación de doctor.
- `internal/state/sqlite/store.go` — DSN del almacén de sesiones y manejo de WAL.
- `internal/transport/router.go` — enrutamiento de eventos entrantes y allowlist.
- Referencia de claves de atributos de Slog — cada `.info()`/`.warn()`/`.error()` en el árbol de fuentes.
