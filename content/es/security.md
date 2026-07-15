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
description: "rousseau-agent security posture: SLSA-3 provenance, cosign signatures, CycloneDX SBOM, dropped capabilities, seccomp, trust model, cryptography inventory, disclosure SLA."
keywords: "security, SLSA-3, cosign, sigstore, SBOM, CycloneDX, seccomp, drop capabilities, trust model, disclosure, CVSS, coordinated disclosure"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/security/"
subtitle: "Supply chain, runtime, and trust boundaries — honestly stated."
tags: "security, supply-chain, disclosure"
title: "Seguridad"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "security, SLSA-3, cosign, sigstore, SBOM, CycloneDX, seccomp, drop capabilities, trust model, disclosure, CVSS, coordinated disclosure"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Seguridad"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "security"
order: 26
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/security/index.html"
item_link: "https://docs.rousseau-agent.dev/security/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Seguridad"
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
twitter_description: "rousseau-agent security posture: SLSA-3 provenance, cosign signatures, CycloneDX SBOM, dropped capabilities, seccomp, trust model, cryptography inventory, disclosure SLA."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Seguridad"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Qué aprenderás</span><p>El modelo de amenazas de rousseau en forma de prosa y diagrama ASCII, las fronteras esenciales (política de aprobación, aislamiento del contenedor, cadena de suministro), el filtro seccomp de referencia y cómo endurecerlo aún más, la política de egress de red y el rastro de auditoría que llega a <code>slog</code>. Consulta también <code>SECURITY.md</code> en el árbol de fuentes y <code>docker/rousseau-agent.container</code> para la verdad de base.</p></aside>

## Diagrama del modelo de amenazas

```
                          ┌──────────────────────────────────┐
                          │        Chat transport user       │
                          │   (WhatsApp / Slack / Discord)   │
                          └──────────────────┬───────────────┘
                                             │ E2EE (WhatsApp)
                                             │ TLS   (Slack / Discord / …)
                        ─────────────────────┴─────────────────────
                                             │
                                             ▼
      ┌─────────────── rousseau-agent container ────────────────┐
      │                                                          │
      │   ┌─────────────┐    inbound     ┌──────────────────┐   │
      │   │  Transport  │ ───────────▶   │  Router          │   │
      │   │  adapter    │                │  + allowlist     │   │
      │   └─────────────┘                └────────┬─────────┘   │
      │                                           │             │
      │                                           ▼             │
      │                                   ┌─────────────┐       │
      │                                   │   Agent     │       │
      │                                   │  Turn loop  │       │
      │                                   └──────┬──────┘       │
      │                                          │              │
      │                            approver     │              │
      │                          ◀───────────────┤              │
      │                                          ▼              │
      │                                   ┌─────────────┐       │
      │                                   │  Registry   │       │
      │                                   │ read/edit/  │       │
      │                                   │ bash/…      │       │
      │                                   └──────┬──────┘       │
      │                                          │              │
      │  ROOTFS  ReadOnly=true  ─────────────────┤              │
      │  CAPS    DropCapability=all              │              │
      │  UID     1000, keep-id                   │              │
      │  SECCOMP default filter                  │              │
      │                                          │              │
      │            outbound TLS                  ▼              │
      └──────────────────┬───────────────────────┬──────────────┘
                         │                       │
                         ▼                       ▼
                ┌────────────────┐    ┌─────────────────────┐
                │  LLM provider  │    │  bind mounts        │
                │  (Anthropic /  │    │  ~/.local/share/    │
                │   Bedrock /    │    │    rousseau/  RW    │
                │   Vertex / …)  │    │  workspace/   RW    │
                └────────────────┘    │  ~/.claude/   RW    │
                                      └─────────────────────┘
```

Todo lo que está dentro del recuadro del contenedor está bajo el control de rousseau. El ingreso desde el transporte de chat llega ya cifrado E2EE (WhatsApp) o cifrado con TLS (Slack, Discord, Matrix, Telegram, Email, SMS). El egress hacia el proveedor de LLM es TLS. Los bind mounts son el único acceso del servicio al sistema de archivos del host.

## Modelo de confianza — qué está dentro del alcance

`rousseau-agent` es un **servicio local, nativo de contenedores**. Tres fronteras esenciales:

### 1. La shell del usuario

La herramienta incorporada `bash` ejecuta comandos arbitrarios con los privilegios del usuario. **Esta es la frontera de seguridad principal.** Cada invocación de herramienta se expone antes de la ejecución y está sujeta a la política de aprobación configurada (`allow_all`, `deny_all` o modo `pattern` con reglas regex de permiso/denegación por herramienta y un valor por defecto configurable).

Los operadores que ejecutan servicios no supervisados (transportes de chat) **deben**:

- imponer el modo `pattern` con `default: deny` y reglas de permiso explícitas, o
- aceptar la postura `bypassPermissions` con un entendimiento explícito de la exposición.

No hay término medio en el que el modelo mismo se controle a sí mismo. Si el servicio puede ejecutar comandos y el servicio es accesible desde un transporte de chat, los usuarios accesibles pueden, en principio, controlar la shell.

### 2. Aislamiento del contenedor

El despliegue de referencia es un contenedor Podman sin root con:

- `ReadOnly=true`
- `DropCapability=all`
- `NoNewPrivileges=true`
- Filtro seccomp por defecto (`/usr/share/containers/seccomp.json`)
- UID 1000 no-root
- Mapeo de espacio de nombres de usuario `keep-id`
- `Network=pasta` (sin root, sin entrada desde el host por defecto)

Solo el bind mount del workspace, el directorio de estado y `~/.claude` son visibles desde dentro del contenedor. Consulta [/deployment/](/es/deployment/).

### 3. Cadena de suministro

Cada commit ejecuta `govulncheck` y CodeQL. Cada release incluye:

- **Procedencia SLSA Nivel 3** a través de `slsa-framework/slsa-github-generator`, firmada mediante GitHub Actions OIDC.
- **Firma cosign** sobre el archivo de sumas de verificación, verificable contra el log de transparencia de Sigstore.
- **SBOM CycloneDX en JSON.**
- **Atestación de build reproducible** — un job dedicado en CI verifica que la salida sea idéntica bit a bit a partir de un checkout limpio.

## Modelo de confianza — qué está fuera del alcance

- **Salida maliciosa del modelo.** El operador es responsable de revisar las invocaciones de herramientas antes de aprobarlas. Las políticas de aprobación hacen que esto sea menos propenso a errores; no eliminan la necesidad de juicio humano.
- **Cadena de herramientas Go, runtime de contenedor o SO del host comprometidos.** Se asume un entorno de build confiable.
- **Acceso físico a la máquina.**
- **Ataques contra el propio proveedor de LLM.** Las vulnerabilidades del proveedor son responsabilidad de ese proveedor.

## Controles de cadena de suministro

| Control | Implementación |
|---|---|
| Fijación de dependencias directas | Versiones exactas en `go.mod`; resolución transitiva congelada en `go.sum`. |
| Escaneo de vulnerabilidades | `govulncheck ./...` en cada build de CI. Los builds fallan ante cualquier vulnerabilidad conocida que alcance un símbolo importado. |
| Análisis estático | `golangci-lint` v2 (18 linters) + GitHub CodeQL (Go). |
| Actualizaciones de dependencias | Dependabot para `gomod` y `github-actions`, cadencia semanal. |
| Procedencia de build | SLSA Nivel 3 vía `slsa-framework/slsa-github-generator`; atestada mediante GitHub Actions OIDC y publicada en el log de transparencia de Sigstore. |
| Firma de releases | Las sumas de verificación de release se firman con cosign (sin claves, mediante GitHub Actions OIDC). |
| Lista de materiales de software | SBOM CycloneDX en JSON adjunto a cada artefacto de release. |
| Builds reproducibles | Un job dedicado `reproducible-build` en CI verifica la salida idéntica bit a bit. |

Los archivos de workflow de CI se encuentran bajo `.github/workflows/` en el árbol de fuentes: `ci.yml`, `codeql.yml`, `slsa.yml`, `release.yml`, `reproducible-build.yml`.

## Verificar un release

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_<version>_checksums.txt.sig \
  rousseau_<version>_checksums.txt

sha256sum -c rousseau_<version>_checksums.txt
```

Los dos flags que fijan la identidad:

- `--certificate-identity-regexp` coincide con el repositorio de GitHub que emite el certificado de firma. Nunca lo amplíes a `.*`; es lo que impide que la firma cosign de otro repositorio valide contra tu archivo de sumas de verificación.
- `--certificate-oidc-issuer` fija el emisor OIDC a GitHub Actions.

La entrada en el log de transparencia de Sigstore puede consultarse por separado en https://search.sigstore.dev/.

## Controles de runtime

Cada configuración a continuación está aplicada en la unidad Quadlet de referencia y pertenece al baseline de cualquier operador de contenedores:

- **Usuario no-root (UID 1000)** — sin privilegios para escalar a root dentro del contenedor.
- **`ReadOnly=true`** — la imagen no es modificable en tiempo de ejecución; el binario no puede modificarse a sí mismo ni a sus dependencias.
- **`Tmpfs=/tmp:rw,size=64m,mode=1777`** — la única ubicación modificable fuera de los bind mounts.
- **`DropCapability=all`** — sin bits `CAP_*` establecidos. El TCP saliente no requiere ninguno.
- **`NoNewPrivileges=true`** — bloquea la escalada setuid.
- **Filtro seccomp por defecto** — filtrado de llamadas al sistema a nivel de kernel.
- **`Network=pasta`** — pila de red sin root; sin entrada desde el host por defecto.
- **Sin puertos publicados** — no hay `PublishPort=` en el Quadlet. No hay superficie HTTP entrante que publicar.

## Inventario de criptografía

| Uso | Implementación |
|---|---|
| TLS a endpoints de LLM / transporte | Biblioteca estándar de Go `crypto/tls` con el almacén de confianza del sistema. |
| WhatsApp | `whatsmeow` (protocolo Signal). |
| Matrix | API cliente-servidor sobre HTTPS. |
| SMTP (transporte de correo) | Biblioteca estándar de Go `net/smtp` con `PlainAuth` sobre TLS. |
| Almacén de sesiones en reposo | **No cifrado a nivel de aplicación.** Los operadores que requieran cifrado en reposo deben montar el directorio de estado sobre un sistema de archivos cifrado (LUKS, FileVault). |

No se implementan primitivas criptográficas personalizadas en este proyecto.

## Divulgación

Reporta de forma privada a **sebastian.rousseau@gmail.com**. **No** abras un issue público para reportes con impacto de seguridad.

Incluye:

- Descripción concisa y vector CVSS 3.1.
- Componente afectado (ruta del archivo + rango de líneas, o ruta del módulo de dependencia).
- Detalles del entorno (`rousseau version`, versión de Go, SO, runtime de contenedor).
- Reproducción mínima — idealmente una prueba que falle.

### Compromisos de respuesta

| Evento | SLA |
|---|---|
| Acuse de recibo del reporte | ≤ 72 horas |
| Decisión de triaje (aceptar / rechazar / solicitar más información) | ≤ 7 días |
| Corrección publicada para **Crítica** (CVSS ≥ 9.0) | ≤ 14 días |
| Corrección publicada para **Alta** (7.0–8.9) | ≤ 30 días |
| Corrección publicada para **Media / Baja** | programada en un release rutinario |
| Divulgación pública (coordinada) | después del release con la corrección |

## Versiones soportadas

Solo la rama `main` y el release etiquetado más reciente reciben correcciones de seguridad. No hay ramas de soporte a largo plazo.

## Desglose del filtro seccomp

La unidad Quadlet de referencia usa el perfil seccomp por defecto de Podman en `/usr/share/containers/seccomp.json`. Bloquea unas 70 llamadas al sistema que ninguna invocación correcta de rousseau necesita, entre ellas:

| Familia de syscall | Bloqueada | Justificación |
|---|---|---|
| Keyring del kernel (`add_key`, `keyctl`, `request_key`) | sí | rousseau no toca el keyring del kernel. |
| Gestión de montajes (`mount`, `umount`, `pivot_root`, `chroot`) | sí | Sin cambios dinámicos de montaje en tiempo de ejecución. |
| Módulos de kernel (`init_module`, `finit_module`, `delete_module`) | sí | El servicio no puede cargar módulos de kernel. |
| Namespaces (`setns`, `unshare` con ciertos flags) | filtrada | Previene escape del contenedor mediante intercambio de namespace. |
| Primitivas de depuración (`ptrace`, `process_vm_readv`, `process_vm_writev`) | sí | Rousseau no se adjunta a otros procesos. |
| BPF (`bpf`) | sí | Sin programas eBPF desde dentro del contenedor. |
| Reinicio (`reboot`, `kexec_*`) | sí | El contenedor no tiene motivo legítimo para reiniciar el host. |
| Cambios de reloj (`clock_settime`, `adjtimex`) | sí | La hora la gestiona el host. |

El perfil por defecto permite suficientes llamadas al sistema para la biblioteca estándar, el driver SQLite (`modernc.org/sqlite`), el cliente whatsmeow y los SDK de OpenAI/Anthropic. Si necesitas endurecer más — por ejemplo, quitar `personality` porque nunca emulas otras ABI — copia el perfil por defecto, elimina la syscall y referencia la copia mediante `SeccompProfile=/path/to/profile.json` en el Quadlet.

<aside class="admonition" data-type="caution"><span class="admonition-title">Pruebas de perfiles más estrictos</span><p>Cada ajuste seccomp necesita cobertura en tu smoke test — una syscall que no sabías que rousseau necesita hará que una completación o un transporte falle en tiempo de ejecución. Prueba con una ida y vuelta de chat real antes de desplegar a producción.</p></aside>

## Política de egress de red

Por defecto el contenedor no tiene ingreso y tiene egress sin restricciones (`Network=pasta`). Para despliegues de alta seguridad, añade un conjunto de reglas nftables que solo permita los dominios que rousseau necesita:

```
# /etc/nftables.d/rousseau.nft — example only, adjust to your provider
table inet rousseau_out {
    chain output {
        type filter hook output priority 0; policy drop;

        # LLM providers
        ip daddr { 3.5.0.0/16, 15.230.0.0/16 } tcp dport 443 accept  # Anthropic + Bedrock
        ip daddr { 34.107.0.0/16 } tcp dport 443 accept              # Vertex

        # Chat transports
        ip daddr { 157.240.0.0/16 } tcp dport 443 accept             # Meta (WhatsApp)
        ip daddr { 3.208.0.0/16 } tcp dport 443 accept               # Slack

        # DNS
        udp dport 53 accept
        tcp dport 53 accept

        # NTP
        udp dport 123 accept
    }
}
```

Los rangos CIDR cambian — considera lo anterior como un andamiaje. Lo importante es que el egress de rousseau es finito y enumerable; el ejemplo `docker/example-nftables.rules` en el código fuente es un conjunto de reglas de punto de partida.

## Rastro de auditoría vía slog

Cada evento relevante para la seguridad se registra vía `log/slog` de Go en nivel JSON estructurado (`log.format: json`). Los eventos que deberías vigilar en producción:

| Evento | Nivel | Origen | Qué te indica |
|---|---|---|---|
| `tool.execute` | info | `internal/agent/agent.go` | Qué herramienta pidió ejecutar el modelo, en qué sesión. |
| `tool.denied` | warn | `internal/agent/agent.go` | Un aprobador denegó una invocación; contiene la cadena de motivo. |
| `tool.error` | warn | `internal/agent/agent.go` | La herramienta se ejecutó pero devolvió un error. |
| `router.transport.rejected` | info | `internal/transport/router.go` | Un mensaje entrante no pasó la allowlist. |
| `whatsapp.logged_out` | error | `internal/transport/whatsapp/client.go` | Meta invalidó el emparejamiento. |
| `mcp.tool_error` | warn | `internal/mcp/server.go` | Un handler de herramienta MCP devolvió un error. |
| `cron.delivery_failed` | warn | `internal/cron/` | La entrega por transporte de un trabajo programado tuvo un error. |

Alimenta el flujo JSON a Loki / Datadog / Splunk / un pipeline de Vector; consulta [Guías: Observabilidad](/es/guides/observability/).

<aside class="admonition" data-type="tip"><span class="admonition-title">Nomenclatura de campos</span><p>Las claves de atributos de slog se agrupan por punto (<code>whatsapp.connected</code>, no <code>event=whatsapp_connected</code>). Consulta con la clave sin transformar en la herramienta de logs que uses.</p></aside>

## Solución de problemas

### El contenedor se niega a iniciar con `mount: permission denied`

Discrepancia de etiqueta SELinux. Asegúrate de que cada línea de bind mount termine con `:Z` (etiqueta privada) o `:z` (compartida). Sin etiqueta, el proceso del contenedor no puede leer/escribir archivos que fueron etiquetados por el host.

### Seccomp está bloqueando una syscall que necesito

Podman imprime `syscall X blocked` en el journal. Reproduce con `strace -f -e trace=X` fuera del contenedor para confirmar qué necesita la llamada. Si es legítima, copia el perfil seccomp por defecto, añade la syscall a la lista de permitidas y referencia el perfil vía `SeccompProfile=`.

### `cosign verify-blob` muestra "certificate identity does not match"

Tu `--certificate-identity-regexp` es incorrecto. Usa `sebastienrousseau/rousseau-agent`. Cualquier regex más laxo (`.*`, `.+`) anula el propósito de la firma sin claves.

### El egress del proveedor falla bajo restricciones de nftables

Tu conjunto de reglas no incluye el rango de IP actual del proveedor. Los proveedores rotan CIDRs. Usa egress basado en DNS con un ipset que se resuelva mediante cron, o usa un proxy de egress que resuelva nombres en el momento de la conexión.

### No hay nada en slog cuando espero eventos de auditoría

Nivel de log demasiado alto. Establece `log.level: info` (o `debug` para detalle a nivel de cable) y confirma que el servicio realmente inicie una nueva sesión — `slog.Default()` se usa antes de que se cargue la configuración, por lo que los mensajes de arranque temprano se dirigen a stderr en formato de texto de todas formas.

## Páginas relacionadas

- [Despliegue](/es/deployment/) — la unidad Quadlet de referencia.
- [Guía de usuario: Políticas de aprobación](/es/user-guide/approval-policies/) — la palanca de seguridad principal.
- [Guías: Inyección de prompts](/es/guides/prompt-injection/) — ataques que llegan a través de la salida del modelo.
- [Guías: Modo de solo lectura](/es/guides/read-only-mode/) — cómo ejecutar un servicio "mirar, no tocar".
- [Guías: Observabilidad](/es/guides/observability/) — pipeline slog + Loki / Datadog.

## Lectura adicional

- `SECURITY.md` — el documento de política canónico.
- `docker/rousseau-agent.container` — la unidad Quadlet de referencia.
- `docker/example-nftables.rules` — conjunto de reglas de egress de muestra.
- `internal/agent/agent.go` — donde se emiten los eventos `tool.execute` y `tool.denied`.
- `internal/agent/approver.go` — implementaciones de política de aprobación.
