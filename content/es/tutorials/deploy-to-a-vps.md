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
description: "Walk a fresh VPS from bare install to a hardened rousseau-agent daemon under rootless Podman and a systemd Quadlet unit."
keywords: "vps, podman, quadlet, systemd, rootless, deployment, hardening"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/tutorials/deploy-to-a-vps/"
subtitle: "Build a container, provision a VPS, install the Quadlet unit, verify the service."
tags: "tutorials, deployment, podman, quadlet, systemd, vps"
title: "Tutorial: desplegar en un VPS"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "vps, podman, quadlet, systemd, rootless, deployment, hardening"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: desplegar en un VPS"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/deploy-to-a-vps/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/deploy-to-a-vps/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: desplegar en un VPS"
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
twitter_description: "Walk a fresh VPS from bare install to a hardened rousseau-agent daemon under rootless Podman and a systemd Quadlet unit."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: desplegar en un VPS"
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

## Qué construyes

Un VPS Ubuntu 24.04 recién creado ejecutando el daemon WhatsApp de rousseau-agent bajo un contenedor Podman rootless, controlado por la unidad Quadlet de systemd en `docker/rousseau-agent.container`. Sistema de archivos raíz de solo lectura, todas las capacidades eliminadas, `NoNewPrivileges=true`, seccomp activo. Cero puertos de red entrantes.

Tiempo estimado: 45 minutos.

## Requisitos previos

- Un VPS con Ubuntu 24.04 (o Debian 12+ / Fedora 40+). 1 GB de RAM y 20 GB de disco son suficientes.
- Acceso SSH con clave a un usuario no root con sudo.
- Tu clave de API de Anthropic o disposición para ejecutar `claudecli`: `claudecli` necesita `claude` instalado en el VPS con una sesión OAuth activa, lo cual es incómodo en un servidor sin cabeza. Anthropic direct o Bedrock es la elección práctica.

## Paso 1: configuración base del SO

```sh
ssh admin@vps
sudo apt update && sudo apt -y upgrade
sudo apt -y install podman uidmap fuse-overlayfs slirp4netns curl git

# podman rootless necesita rangos subuid/subgid para el usuario
grep rousseau /etc/subuid || sudo usermod --add-subuids 200000-265535 rousseau
grep rousseau /etc/subgid || sudo usermod --add-subgids 200000-265535 rousseau
```

Crea el usuario de servicio y su sesión de usuario de systemd:

```sh
sudo useradd -m -s /bin/bash rousseau
sudo loginctl enable-linger rousseau     # mantiene los servicios de usuario ejecutándose cuando nadie está conectado
```

## Paso 2: transferir el código fuente

La unidad Quadlet en `docker/rousseau-agent.container` construye una imagen local. En el VPS:

```sh
sudo -iu rousseau
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
podman build -t rousseau-agent:local -f docker/Dockerfile .
podman image inspect localhost/rousseau-agent:local | head
```

El `Dockerfile` produce un binario Go estático (`CGO_ENABLED=0`), lo copia a una base mínima y se ejecuta como UID 1000. Consulta [Despliegue](/es/deployment/) para la discusión de la imagen base.

## Paso 3: sembrar la configuración

Rousseau lee `~/.config/rousseau/config.yaml`. Créalo en el host: la unidad Quadlet monta con bind el `$HOME` del contenedor de vuelta al host.

```sh
mkdir -p /home/rousseau/.config/rousseau
cat > /home/rousseau/.config/rousseau/config.yaml <<'YAML'
provider: anthropic

anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096

whatsapp:
  reply_header: "*rousseau*\n\n"

agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

log:
  level: info
  format: json
YAML
chown -R rousseau:rousseau /home/rousseau/.config
```

Guarda la clave de API de Anthropic en un archivo de entorno de systemd, nunca en `config.yaml`:

```sh
mkdir -p /home/rousseau/.config/rousseau
cat > /home/rousseau/.config/rousseau/env <<'ENV'
ANTHROPIC_API_KEY=sk-ant-…
ENV
chmod 0600 /home/rousseau/.config/rousseau/env
```

Referéncialo desde la unidad Quadlet: consulta el siguiente paso.

## Paso 4: instalar la unidad Quadlet

```sh
mkdir -p /home/rousseau/.config/containers/systemd
cp docker/rousseau-agent.container /home/rousseau/.config/containers/systemd/
```

Edita para tu JID y archivo de secretos:

```sh
sed -i 's|Exec=whatsapp --allow.*|Exec=whatsapp --allow YOUR_JID@s.whatsapp.net|' \
  /home/rousseau/.config/containers/systemd/rousseau-agent.container

cat >> /home/rousseau/.config/containers/systemd/rousseau-agent.container <<'EOF'
EnvironmentFile=%h/.config/rousseau/env
EOF
```

Recarga e inicia:

```sh
systemctl --user daemon-reload
systemctl --user enable --now rousseau-agent
systemctl --user status rousseau-agent
```

## Paso 5: primer emparejamiento

El puente de WhatsApp necesita imprimir un código QR la primera vez. Conéctate:

```sh
podman logs -f rousseau-agent
# escanea el QR desde tu teléfono: WhatsApp > Configuración > Dispositivos vinculados
```

Secuencia de log esperada (de `internal/transport/whatsapp/client.go`):

```
INFO whatsapp.starting store=… allowlist=1
INFO whatsapp.qr_ready
INFO whatsapp.paired
INFO whatsapp.connected
```

Las credenciales del dispositivo persisten en `/home/rousseau/.local/share/rousseau/whatsapp.db`. Los reinicios posteriores omiten el QR.

## Paso 6: verificar

```sh
podman exec rousseau-agent rousseau status
```

Un código de salida 0 significa que el daemon está sano. Cualquier valor distinto de cero es una alerta: consulta [Referencia: Códigos de salida](/es/reference/exit-codes/).

Envíate un mensaje de prueba desde el teléfono en la allowlist. Los logs estructurados muestran:

```
INFO whatsapp.incoming from=447900123456@s.whatsapp.net
INFO tool.execute name=read id=t_1
INFO whatsapp.handler_ok elapsed=…
```

## Paso 7: revisión de endurecimiento

La unidad Quadlet ya aplica:

- `ReadOnly=true` + `Tmpfs=/tmp`: sin mutación de la imagen en tiempo de ejecución.
- `DropCapability=all`: el binario Go no necesita capacidades elevadas.
- `NoNewPrivileges=true`: los procesos hijo no pueden obtener privilegios.
- `SeccompProfile=/usr/share/containers/seccomp.json`: filtro de syscalls a nivel de kernel.
- `Network=pasta`: pila de red rootless, bloquea entrada por defecto.
- `UserNS=keep-id`: los archivos con bind-mount tienen la propiedad esperada en ambos lados.

Si quieres la postura más estricta, envuelve el daemon en un firewall solo saliente (nftables o Cloudflare Zero-Trust) que permita únicamente los rangos de CDN a los que Anthropic + Meta realmente resuelven. Consulta [Guías: Onboarding empresarial](/es/guides/enterprise-onboarding/) para la lista de verificación.

## Paso 8: backup

Todo el estado persistente es un directorio: `/home/rousseau/.local/share/rousseau/`. Haz backup con `restic` o `borg` cada noche.

```sh
sudo -iu rousseau -- restic backup /home/rousseau/.local/share/rousseau
```

Las bases de datos SQLite son seguras para hacer snapshot en vivo porque el journaling WAL está habilitado por `Open()` en `internal/state/sqlite/store.go`.

## Relacionado

- [Despliegue](/es/deployment/): referencia completa de la unidad Quadlet.
- [Guías: Despliegue de producción](/es/guides/production-deployment/): envío de logs, reinicios rolling.
- [Guías: Onboarding empresarial](/es/guides/enterprise-onboarding/): verificación de SBOM, auditoría de seccomp.
- [Seguridad](/es/security/): fronteras de confianza.
