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
description: "Reference production deployment for rousseau-agent: rootless Podman + systemd Quadlet with dropped capabilities, read-only rootfs, seccomp, pasta networking. Kubernetes / OpenShift note."
keywords: "deployment, Podman, Quadlet, systemd, rootless, ReadOnly, DropCapability, NoNewPrivileges, seccomp, pasta, Kubernetes, OpenShift"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/deployment/"
subtitle: "Podman sin root con una unidad Quadlet de systemd, más una nota sobre Kubernetes."
tags: "deployment, operations, container, systemd"
title: "Despliegue"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "deployment, Podman, Quadlet, systemd, rootless, ReadOnly, DropCapability, NoNewPrivileges, seccomp, pasta, Kubernetes, OpenShift"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Despliegue"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "operations"
order: 25
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/deployment/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Despliegue"
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
twitter_description: "Reference production deployment for rousseau-agent: rootless Podman + systemd Quadlet with dropped capabilities, read-only rootfs, seccomp, pasta networking. Kubernetes / OpenShift note."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Despliegue"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Qué aprenderás</span><p>Las tres topologías de despliegue que rousseau admite — Podman sin root + Quadlet (referencia), Docker plano y Kubernetes — además de la gestión de secretos vía Vault, AWS Secrets Manager y GCP Secret Manager. Fuente de verdad para el Quadlet de referencia: <code>docker/rousseau-agent.container</code>.</p></aside>

## Postura de referencia

El despliegue de referencia es un contenedor Podman sin root gestionado por una unidad Quadlet de systemd — un solo nodo, sin dependencia de Kubernetes, sobrevive a reinicios, sin privilegios de root requeridos.

Fuente de verdad: `docker/rousseau-agent.container` en el repositorio rousseau-agent.

## Elige una topología

<div class="tabs" data-tabs="deployment-topology">
  <div class="tab-list" role="tablist" aria-label="Deployment topology">
    <button role="tab" aria-selected="true">Podman + Quadlet</button>
    <button role="tab" aria-selected="false">Docker Compose</button>
    <button role="tab" aria-selected="false">Kubernetes</button>
  </div>
  <div class="tab-panel" role="tabpanel">

El despliegue de referencia. Sin root, endurecido, sobrevive a reinicios, sin orquestador requerido.

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user enable --now rousseau-agent.service
```

Consulta la unidad Quadlet completa y su justificación más abajo en esta página.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Docker Compose es una forma familiar pero no impone la postura de seguridad que impone Quadlet — debes establecer cada flag de endurecimiento a mano:

```yaml
services:
  rousseau:
    image: rousseau-agent:local
    read_only: true
    cap_drop: [ALL]
    security_opt:
      - no-new-privileges:true
      - seccomp:default
    user: "1000:1000"
    tmpfs:
      - /tmp:size=64m,mode=1777
    volumes:
      - ${HOME}/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
      - ${HOME}/.claude:/home/rousseau/.claude:rw,Z
      - ${HOME}/team-rousseau-workspace:/workspace:rw,Z
    environment:
      HOME: /home/rousseau
    restart: unless-stopped
    command: ["whatsapp", "--allow", "447900123456@s.whatsapp.net"]
```

<aside class="admonition" data-type="warning"><span class="admonition-title">Docker con root</span><p>El daemon clásico de Docker se ejecuta como root. Incluso con <code>user: "1000:1000"</code>, el daemon tiene las capacidades del propietario del socket de Docker. Prefiere Docker sin root o Podman.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Kubernetes necesita un Deployment + PVC. Consulta el manifiesto abajo, además de [Guías: Despliegue de Kubernetes](/es/guides/kubernetes-deployment/) para un ejemplo completo de chart de Helm.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: rousseau-agent, namespace: agents }
spec:
  replicas: 1
  strategy: { type: Recreate }
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        seccompProfile: { type: RuntimeDefault }
      containers:
        - name: rousseau
          image: ghcr.io/sebastienrousseau/rousseau-agent:v0.6.0
          args: ["whatsapp", "--allow", "447900123456@s.whatsapp.net"]
          securityContext:
            allowPrivilegeEscalation: false
            capabilities: { drop: [ALL] }
            readOnlyRootFilesystem: true
          volumeMounts:
            - { name: state, mountPath: /home/rousseau/.local/share/rousseau }
            - { name: tmp,   mountPath: /tmp }
      volumes:
        - name: state
          persistentVolumeClaim: { claimName: rousseau-state }
        - name: tmp
          emptyDir: { medium: Memory, sizeLimit: 64Mi }
```

  </div>
</div>

## Gestión de secretos

Nunca guardes claves de API o tokens en `config.yaml`. Cárgalos en tiempo de ejecución desde un backend de secretos:

<div class="tabs" data-tabs="deployment-secrets">
  <div class="tab-list" role="tablist" aria-label="Secrets backend">
    <button role="tab" aria-selected="true">HashiCorp Vault</button>
    <button role="tab" aria-selected="false">AWS Secrets Manager</button>
    <button role="tab" aria-selected="false">GCP Secret Manager</button>
    <button role="tab" aria-selected="false">credenciales de systemd</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Usa `vault agent` para renderizar variables de entorno en un archivo que rousseau lee. Plantilla de muestra:

```
{{- with secret "kv/rousseau/anthropic" }}
ANTHROPIC_API_KEY={{ .Data.data.api_key }}
{{- end }}
```

Systemd:

```ini
[Service]
EnvironmentFile=/run/rousseau/env
ExecStartPre=/usr/local/bin/vault-agent -config=/etc/vault/agent.hcl
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Usa `aws secretsmanager` para obtener la clave en un archivo de entorno al arranque:

```sh
aws secretsmanager get-secret-value \
  --secret-id rousseau/anthropic \
  --query SecretString --output text | \
  jq -r '"ANTHROPIC_API_KEY=\(.api_key)"' > /run/rousseau/env
```

Systemd:

```ini
[Service]
EnvironmentFile=/run/rousseau/env
ExecStartPre=/usr/local/bin/fetch-secrets.sh
```

Combina con IRSA en EKS para que el SDK resuelva las credenciales de forma transparente — sin claves estáticas de AWS necesarias en el host.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Usa `gcloud secrets versions access`:

```sh
gcloud secrets versions access latest --secret=rousseau-anthropic > /run/rousseau/api_key
```

O bien, en Kubernetes, usa el [driver CSI de Secret Manager](https://cloud.google.com/secret-manager/docs/secret-manager-managed-csi-component) para montar los secretos como archivos.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Las credenciales de systemd (disponibles en systemd 250+) cargan secretos en memoria al arranque de la unidad:

```ini
[Service]
LoadCredential=anthropic_key:/etc/rousseau/anthropic.key
ExecStart=/usr/local/bin/rousseau chat
```

El servicio lee `$CREDENTIALS_DIRECTORY/anthropic_key` al iniciar. Sin escrituras en disco más allá del almacén de credenciales (cifrado).

  </div>
</div>

## Construir la imagen

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
```

Build multi-etapa. Etapa 1: `golang:1.26-alpine` compila el binario estático (`CGO_ENABLED=0`). Etapa 2: `node:22-alpine` proporciona el subproceso del CLI `claude`. La imagen de runtime pesa ~550 MB; la capa de Node solo existe para que el proveedor opcional `claudecli` tenga un lugar donde ejecutarse.

Si usas un proveedor distinto (Anthropic directo, Bedrock, Vertex, compatible con OpenAI), puedes quitar el runtime de Node y reducir la imagen.

## Instalar la unidad Quadlet

```sh
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload
systemctl --user start rousseau-agent.service
journalctl --user -u rousseau-agent.service -f
```

Habilita el arranque en boot con `systemctl --user enable rousseau-agent.service` tras confirmar que el lingering esté activo (`loginctl enable-linger $USER`).

## Postura de runtime — cada configuración de Quadlet

| Configuración | Valor | Justificación |
|---|---|---|
| `Network=pasta` | Pila de red sin root | `slirp4netns` fue eliminado de las versiones recientes de Podman; pasta es más rápido en kernels modernos y bloquea el tráfico entrante desde el host por defecto. |
| `UserNS=keep-id` | UID 1000 del contenedor → UID 1000 del host | Los archivos bind-mounted mantienen la propiedad del host; el proceso del contenedor puede escribir en archivos propiedad del host. |
| `ReadOnly=true` | Sistema de archivos raíz de solo lectura | El servicio nunca debe modificar la imagen en tiempo de ejecución. Cualquier cosa modificable vive en un bind mount o en el tmpfs. |
| `Tmpfs=/tmp:rw,size=64m,mode=1777` | Espacio scratch modificable | Para cualquier cosa que necesite un archivo scratch en tiempo de ejecución (poco común). |
| `DropCapability=all` | Todas las capacidades eliminadas | El binario Go no necesita capacidades elevadas — el TCP saliente no requiere `CAP_NET_BIND_SERVICE` o similar. |
| `NoNewPrivileges=true` | Bit `no_new_privs` activado | Bloquea la escalada setuid dentro del contenedor. |
| `SeccompProfile=/usr/share/containers/seccomp.json` | Filtro seccomp por defecto | Filtrado de llamadas al sistema a nivel de kernel sobre las capacidades eliminadas. |
| `Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z` | Bind mount del estado | Sesiones, emparejamiento de WhatsApp, tareas cron, mapa de JID, índice FTS5. `:Z` establece la etiqueta SELinux. |
| `Volume=%h/.claude:/home/rousseau/.claude:rw,Z` | Autenticación del CLI `claude` | Solo relevante cuando el proveedor `claudecli` está activo. `claude` refresca el OAuth cacheado en el mismo lugar. |
| `Volume=%h/team-rousseau-workspace:/workspace:rw,Z` | Workspace | Solo el workspace es visible desde dentro del contenedor. Nada más del host se monta. |
| `Environment=HOME=/home/rousseau` | Establece `$HOME` | Consumido por Viper, el CLI `claude` y el resolvedor de directorio de estado. |
| `AutoUpdate=disabled` | Podman no auto-actualiza | Las actualizaciones las emite el operador con una cadencia de release, no de forma silenciosa. |

## Línea `Exec=`

El Quadlet viene con:

```
Exec=whatsapp --allow 447906009073@s.whatsapp.net
```

Reemplaza con el transporte de tu elección y tu allowlist. Múltiples transportes normalmente se ejecutan en unidades Quadlet separadas — una imagen, un binario, varias unidades — de modo que un fallo en un transporte no derribe los demás.

## Kubernetes / OpenShift

`rousseau` es un servicio de un solo binario; un `Deployment` mínimo + `PersistentVolumeClaim` para el directorio de estado es suficiente:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: rousseau-agent
spec:
  replicas: 1
  strategy:
    type: Recreate           # do not run two daemons against one state DB
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        seccompProfile: {type: RuntimeDefault}
      containers:
        - name: rousseau
          image: registry.example.com/rousseau-agent:v1.0.0
          args: ["whatsapp", "--allow", "447900123456@s.whatsapp.net"]
          securityContext:
            allowPrivilegeEscalation: false
            capabilities: {drop: [ALL]}
            readOnlyRootFilesystem: true
          volumeMounts:
            - {name: state, mountPath: /home/rousseau/.local/share/rousseau}
            - {name: tmp,   mountPath: /tmp}
      volumes:
        - name: state
          persistentVolumeClaim: {claimName: rousseau-state}
        - name: tmp
          emptyDir: {medium: Memory, sizeLimit: 64Mi}
```

Como no hay superficie HTTP entrante, **no se requiere `Service` ni `Ingress`** para los transportes con WebSocket saliente (Slack, Discord, WhatsApp, Matrix). Solo un transporte tipo webhook necesitaría un `Service`, y rousseau no incluye ninguno por defecto.

La estrategia `Recreate` es deliberada — el archivo de estado SQLite no está diseñado para dos escritores concurrentes. Si necesitas HA, ejecuta un servicio por transporte y confía en el propio estado del transporte (Slack Socket Mode, Discord Gateway) para la semántica de reconexión.

## Destino de logs de systemd

El Quadlet hereda la configuración del journal de systemd. `journalctl --user -u rousseau-agent.service` lee los logs. Para agregación de logs, usa un sidecar journal-to-Loki / journal-to-Fluent-Bit; no redirijas el formato de log de rousseau directamente a disco (rousseau no rota los logs).

Configura rousseau para emitir JSON para que los agregadores puedan parsearlo:

```yaml
log:
  level: info
  format: json
```

## Bloqueo de egress con nftables (opcional)

`docker/nftables.rules.example` en el árbol de fuentes incluye una plantilla para endurecimiento de egress a nivel de kernel — descartar todo excepto los rangos de WhatsApp Web de Meta, Anthropic (detrás de CloudFront, así que usa filtro basado en dominio) y Signal. Aplica esto sobre el namespace del contenedor para la postura más estricta. Consulta [seguridad](/es/security/) para el razonamiento.

## Chart de Helm (hoja de ruta)

Un chart de Helm oficial está en la hoja de ruta. Hasta que se lance, los manifiestos anteriores son suficientes para un despliegue mínimo. Sigue el progreso en [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md).

Borrador del esquema `values.yaml` (para que usuarios potenciales lo revisen):

```yaml
image:
  repository: ghcr.io/sebastienrousseau/rousseau-agent
  tag: v0.6.0
transport:
  name: whatsapp
  args: ["--allow", "447900123456@s.whatsapp.net"]
provider:
  name: anthropic
  # api_key sourced from a Secret
persistence:
  size: 4Gi
  storageClass: fast-ssd
resources:
  requests: { cpu: "100m", memory: "128Mi" }
  limits:   { cpu: "1",    memory: "512Mi" }
networkPolicy:
  enabled: true
  # egress: allowed CIDRs list
```

## Solución de problemas

### `podman play kube` falla con `permission denied` en un bind mount

Falta la etiqueta SELinux. Cada volumen debe terminar con `:Z` (o `:z` para compartido). Consulta [Solución de problemas: El contenedor falla al hacer bind mount](/es/troubleshooting/#container-fails-to-bind-mount).

### Pod de Kubernetes en CrashLoopBackOff al primer inicio

El volumen de estado no fue pre-creado, o su propiedad no coincide con UID 1000. Añade un initContainer para hacer `chown` del volumen:

```yaml
initContainers:
  - name: chown-state
    image: busybox
    command: ["sh", "-c", "chown -R 1000:1000 /state"]
    volumeMounts: [{ name: state, mountPath: /state }]
    securityContext: { runAsUser: 0 }
```

### `systemctl --user` no encuentra la unidad Quadlet

No se ejecutó `daemon-reload`, o el archivo de unidad tiene un error tipográfico. Confirma con `systemctl --user cat rousseau-agent.service` — Quadlet genera la unidad al vuelo, así que cat es la herramienta de depuración más rápida.

### Tras reiniciar, el servicio no arranca

Habilita lingering: `loginctl enable-linger $USER`. Sin lingering, el gestor de usuario de systemd se detiene al cerrar sesión y no se reactiva hasta el próximo login.

### Dos servicios se pisan y la base de datos de estado está corrupta

Nunca ejecutes dos servicios contra el mismo `state.path`. Si ocurre corrupción, respalda el archivo, `rm sessions.db{,-wal,-shm}`, reinicia. El historial de sesiones se pierde; el emparejamiento sobrevive si `whatsapp.db` está separado (lo está por defecto).

## Páginas relacionadas

- [Guías: Despliegue de Kubernetes](/es/guides/kubernetes-deployment/) — chart de Helm completo y ejemplo de NetworkPolicy.
- [Guías: Despliegue de producción](/es/guides/production-deployment/) — la checklist de producción.
- [Guías: Observabilidad](/es/guides/observability/) — logs y métricas.
- [Seguridad](/es/security/) — fronteras de confianza, seccomp, egress.
- [Configuración](/es/configuration/) — cada opción.

## Lectura adicional

- `docker/Dockerfile` — el build multi-etapa.
- `docker/rousseau-agent.container` — la unidad Quadlet.
- `docker/example-nftables.rules` — conjunto de reglas de egress de muestra.
- `Makefile` — automatización del build.
- Documentación de systemd: [Quadlet](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html).
