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
description: "Install rousseau-agent on macOS, Linux, or Windows. From-source build, go install, cosign-verified release archive, Podman / Docker image, checksum verification recipe."
keywords: "install, macos, linux, windows, homebrew, cosign, sha256, podman, docker, go install"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/getting-started/installation/"
subtitle: "Every supported install method with the verification recipe."
tags: "install, macos, linux, windows, cosign, docker"
title: "Instalación"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "install, macos, linux, windows, homebrew, cosign, sha256, podman, docker, go install"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Instalación"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 21
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/installation/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/installation/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Instalación"
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
twitter_description: "Install rousseau-agent on macOS, Linux, or Windows. From-source build, go install, cosign-verified release archive, Podman / Docker image, checksum verification recipe."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Instalación"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Qué aprenderás</span><p>Cada método de instalación soportado para rousseau, los comandos por SO, la receta de verificación cosign / SHA-256 / SLSA-3 y los modos de fallo que atrapan a los instaladores por primera vez. Revisa la tabla a continuación para elegir un método, luego salta a tu SO.</p></aside>

## Elegir un método de instalación

| Método | Cuándo usarlo | Verificable |
|---|---|---|
| Archivo de release firmado | Producción, entornos aislados, cualquier entorno regulado. | Sí — cosign + sumas SHA-256 + procedencia SLSA-3. |
| `go install` | Desarrolladores individuales que confían en la base de datos de sumas del proxy de módulos Go. | Parcial — fijación de `go.sum` mediante `pkg.go.dev`. |
| Desde fuente (`make build`) | Contribuyentes y revisores que quieren ejecutar el bloqueo completo de CI localmente. | Sí — el job de build reproducible en CI confirma salida idéntica bit a bit. |
| Imagen de contenedor | Despliegues junto a otros servicios de systemd o en Kubernetes. | Sí — la imagen se construye desde la fuente etiquetada, con procedencia adjunta. |
| Homebrew (planificado) | Comodidad en macOS. | Planificado; aún no publicado. |

<aside class="admonition" data-type="caution"><span class="admonition-title">Saltarse la verificación es bajo tu propio riesgo</span><p>La ruta del release firmado es el único método que te da una cadena desde el commit de fuente pasando por GitHub Actions OIDC hasta el archivo en disco. Si no ejecutarías un binario aleatorio de Internet, no te saltes <code>cosign verify-blob</code> + <code>sha256sum -c</code>. Ambos comandos se muestran por SO a continuación.</p></aside>

## Instalación por SO

<div class="tabs" data-tabs="install-os">
  <div class="tab-list" role="tablist" aria-label="Operating system">
    <button role="tab" aria-selected="true">macOS</button>
    <button role="tab" aria-selected="false">Linux</button>
    <button role="tab" aria-selected="false">Windows</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Release firmado (recomendado).** Funciona en Apple Silicon e Intel — cambia `arm64` por `amd64` en Macs con Intel.

```sh
VERSION=<pin-a-tag>
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_darwin_arm64.tar.gz"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt.sig"

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature "rousseau_${VERSION}_checksums.txt.sig" \
  "rousseau_${VERSION}_checksums.txt"

shasum -a 256 -c "rousseau_${VERSION}_checksums.txt" --ignore-missing
tar -xzf "rousseau_${VERSION}_darwin_arm64.tar.gz"
sudo install -m 0755 rousseau /usr/local/bin/rousseau
rousseau version
```

**`go install`.** La ruta más rápida si ya tienes Go 1.26+:

```sh
brew install go@1.26        # o desde https://go.dev/dl
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

El binario incorpora `modernc.org/sqlite` (consulta `internal/state/sqlite/store.go`), por lo que no hay dependencia de libc o CGo ni requisito de Xcode Command Line Tools.

**Homebrew.** La fórmula de Homebrew está en la hoja de ruta. Hasta que se publique, usa la ruta del archivo de release anterior.

<aside class="admonition" data-type="note"><span class="admonition-title">Gatekeeper</span><p>El archivo firmado no está notarizado por el servicio de notarización de Apple (rousseau no incluye un Apple Developer ID). El primer lanzamiento puede mostrar un aviso de Gatekeeper; apruébalo en <em>Ajustes del sistema &gt; Privacidad y seguridad</em>. La verificación de la firma cosign es la comprobación de cadena de suministro equivalente.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Release firmado (recomendado).** Los builds `aarch64` se publican bajo `linux_arm64`:

```sh
VERSION=<pin-a-tag>
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_linux_amd64.tar.gz"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt.sig"

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature "rousseau_${VERSION}_checksums.txt.sig" \
  "rousseau_${VERSION}_checksums.txt"

sha256sum -c "rousseau_${VERSION}_checksums.txt" --ignore-missing
tar -xzf "rousseau_${VERSION}_linux_amd64.tar.gz"
sudo install -m 0755 rousseau /usr/local/bin/rousseau
rousseau version
```

**Paquetes de distribución.** Aún no hay paquetes oficiales — sigue los archivos de release anteriores.

**Podman sin root (producción).** Consulta [Despliegue](/es/deployment/) para la referencia de Quadlet. La red `pasta` requiere Podman 5.x+; Debian 12 y Ubuntu 22.04 incluyen 4.x y necesitan un fallback a `slirp4netns` (hoja de ruta).

<aside class="admonition" data-type="warning"><span class="admonition-title">Go de distribución</span><p>Debian/Ubuntu suelen incluir un Go anterior a 1.26. Si <code>go version</code> reporta &lt; 1.26, instala directamente desde <a href="https://go.dev/dl">go.dev/dl</a> o usa el archivo de release firmado — <code>go install</code> contra una cadena de herramientas antigua fallará en las características de módulo que rousseau usa.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau es un objetivo de build de primera clase para Windows; cada transporte funciona en Windows excepto `signal` (requiere el subproceso JVM `signal-cli`) e `imessage` (requiere macOS). El despliegue de referencia Podman + Quadlet es solo para Linux — usa WSL 2 o una VM de Linux para la ruta de contenedor.

**Release firmado.** PowerShell:

```powershell
$Version = "<pin-a-tag>"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_windows_amd64.zip" -OutFile "rousseau.zip"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_checksums.txt" -OutFile "checksums.txt"
Get-FileHash rousseau.zip -Algorithm SHA256
Expand-Archive rousseau.zip -DestinationPath .
```

Compara la salida de `Get-FileHash` con `checksums.txt` a ojo, o redirige a través de PowerShell para automatizar la comprobación.

**`go install`.** Funciona directamente en Windows una vez que Go está en el PATH:

```powershell
winget install GoLang.Go
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

<aside class="admonition" data-type="warning"><span class="admonition-title">cosign en Windows</span><p>El CLI <code>cosign</code> se ejecuta en Windows pero es una descarga grande y necesita su propia cadena de dependencias. Para una verificación de baja fricción, ejecuta <code>cosign verify-blob</code> una vez desde WSL 2 o una VM de Linux contra el mismo archivo de sumas, luego confía en la receta SHA-256 en Windows.</p></aside>

<aside class="admonition" data-type="warning"><span class="admonition-title">Rutas del directorio de inicio</span><p>Rousseau escribe el estado en <code>%APPDATA%\rousseau\sessions.db</code> en Windows (mediante <code>os.UserConfigDir()</code> en <code>internal/config/config.go</code>). La documentación a veces cita la ruta Unix <code>~/.local/share/rousseau/</code> — el mismo archivo reside en la ubicación apropiada para la plataforma.</p></aside>

  </div>
</div>

## Verificar un release firmado

El comando `cosign verify-blob` realiza tres comprobaciones a la vez contra el log público de transparencia de Sigstore:

1. El certificado incrustado en la firma fue emitido para la identidad OIDC de GitHub Actions que coincide con el regex.
2. La firma sobre el archivo de sumas de verificación es válida.
3. El certificado fue atestiguado por el log de transparencia.

`sha256sum -c` entonces confirma que cada artefacto en el archivo de sumas coincide. Esta es la comprobación esencial de cadena de suministro — no te la saltes.

### Verificar el SBOM

Cada release incluye `rousseau_<version>_sbom.cdx.json` (CycloneDX 1.5). Inspecciona con `cyclonedx-cli`:

```sh
cyclonedx-cli tree --input-file rousseau_<version>_sbom.cdx.json
cyclonedx-cli validate --input-file rousseau_<version>_sbom.cdx.json
```

### Verificar procedencia SLSA-3

```sh
slsa-verifier verify-artifact \
  --provenance-path rousseau_<version>_provenance.intoto.jsonl \
  --source-uri github.com/sebastienrousseau/rousseau-agent \
  --source-tag <version> \
  rousseau_<version>_linux_amd64.tar.gz
```

Cualquier desviación entre el artefacto y lo que CI atestigua haber construido hace que `slsa-verifier` salga con un código distinto de cero.

## macOS

### Release firmado (recomendado)

```sh
VERSION=<pin-a-tag>
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_darwin_arm64.tar.gz"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt.sig"

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature "rousseau_${VERSION}_checksums.txt.sig" \
  "rousseau_${VERSION}_checksums.txt"

shasum -a 256 -c "rousseau_${VERSION}_checksums.txt" --ignore-missing
tar -xzf "rousseau_${VERSION}_darwin_arm64.tar.gz"
sudo install -m 0755 rousseau /usr/local/bin/rousseau
rousseau version
```

Reemplaza `arm64` con `amd64` en Macs con Intel.

### Homebrew (planificado)

La fórmula de Homebrew está en la hoja de ruta. Hasta que se publique, la ruta del archivo de release anterior es la instalación recomendada para macOS.

## Linux

### Release firmado (recomendado)

```sh
VERSION=<pin-a-tag>
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_linux_amd64.tar.gz"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt.sig"

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature "rousseau_${VERSION}_checksums.txt.sig" \
  "rousseau_${VERSION}_checksums.txt"

sha256sum -c "rousseau_${VERSION}_checksums.txt" --ignore-missing
tar -xzf "rousseau_${VERSION}_linux_amd64.tar.gz"
sudo install -m 0755 rousseau /usr/local/bin/rousseau
rousseau version
```

Los builds `aarch64` se publican bajo `linux_arm64`.

El regex de identidad del certificado fija la identidad del firmante. No lo debilites: cualquier archivo de release firmado por una identidad diferente debe ser rechazado de plano.

### Mediante `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

El binario es totalmente estático (`CGO_ENABLED=0`) e incorpora `modernc.org/sqlite`, por lo que no se introduce dependencia de libc o CGo en runtime. Las fijaciones de `go.sum` las impone la base de datos de sumas del proxy de módulos Go.

## Windows

Los binarios de Windows se publican en el mismo diseño de archivo de release:

```powershell
$Version = "<pin-a-tag>"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_windows_amd64.zip" -OutFile "rousseau.zip"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_checksums.txt" -OutFile "checksums.txt"

# Verifica SHA-256 (la verificación cosign es más cómoda en Linux/macOS; en Windows,
# la verificación de sumas por sí sola es utilizable pero más débil que la receta completa).
Get-FileHash rousseau.zip -Algorithm SHA256
Expand-Archive rousseau.zip -DestinationPath .
```

Windows es un objetivo de build de primera clase pero está poco probado — cada transporte de chat funciona, pero el despliegue de referencia (Podman + Quadlet) asume Linux. Reporta problemas específicos de Windows para que puedan detectarse en CI.

## Desde fuente

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` ejecuta el bloqueo exacto de CI: `go vet`, `golangci-lint` v2 (18 linters), `go test -race -count=1 -covermode=atomic ./...` y `govulncheck`.

El job dedicado `reproducible-build` en CI verifica salida idéntica bit a bit desde un checkout limpio en `ubuntu-latest`, por lo que un `make build` local con la misma cadena de herramientas Go producirá un binario cuyo SHA-256 coincide con el release etiquetado.

## Podman / Docker

```sh
# Compila localmente desde la fuente etiquetada.
podman build -t rousseau-agent:local -f docker/Dockerfile .

# Descarga la imagen preconstruida (una vez publicada).
podman pull ghcr.io/sebastienrousseau/rousseau-agent:<tag>
```

Docker funciona idénticamente: cambia `podman` por `docker`. El despliegue de referencia ([Despliegue](/es/deployment/)) usa **Podman sin root** con una unidad Quadlet de systemd porque Quadlet proporciona endurecimiento declarativo (`ReadOnly=true`, `DropCapability=all`, `NoNewPrivileges=true`, filtro seccomp, mapeo de espacio de nombres de usuario `keep-id`) que el Docker plano no.

La imagen de runtime pesa ~550 MB, construida como un builder multi-etapa `golang:1.26-alpine` que alimenta un runtime `node:22-alpine`. La capa de Node existe solo para que el subproceso opcional del CLI `claude` tenga un lugar donde ejecutarse; el propio servicio no tiene dependencia de intérprete.

## Verificar un release firmado

El comando `cosign verify-blob` realiza tres comprobaciones a la vez contra el log público de transparencia de Sigstore:

1. El certificado incrustado en la firma fue emitido para la identidad OIDC de GitHub Actions que coincide con el regex.
2. La firma sobre el archivo de sumas de verificación es válida.
3. El certificado fue atestiguado por el log de transparencia.

`sha256sum -c` entonces confirma que cada artefacto en el archivo de sumas coincide. Esta es la comprobación esencial de cadena de suministro — no te la saltes.

## Solución de problemas

### `go: module github.com/sebastienrousseau/rousseau-agent/cmd/rousseau: no matching versions`

Tu cadena de herramientas `go` es anterior a 1.26. `go install` rechaza módulos con una directiva `go` superior a la versión de la cadena de herramientas. Actualiza Go, o usa el archivo de release firmado.

### `sha256sum: WARNING: X computed checksums did NOT match`

El archivo se corrompió durante la descarga, o (peor) fue manipulado. Vuelve a descargar y a ejecutar la receta desde el principio — `cosign verify-blob` debería haber detectado la manipulación, pero siempre confía en el resultado de SHA-256 sobre cualquier suposición.

### `cosign: no matching signatures`

Tienes `cosign` pero el `--certificate-identity-regexp` no coincide con el firmante. Para rousseau, usa `sebastienrousseau/rousseau-agent`. Si aún falla, ejecuta `cosign initialize` para refrescar la raíz de confianza de Sigstore — la raíz rota con una cadencia lenta.

### `rousseau version` imprime `dev / none / unknown`

Instalaste vía `go install` y las marcas de versión `-ldflags` en `internal/cli/root.go` no se poblaron. Es solo cosmético, pero el archivo de release firmado es la solución.

### macOS Gatekeeper se niega a abrir el binario

Clic derecho sobre el binario en Finder, elige <em>Abrir</em>, luego <em>Abrir</em> de nuevo en el diálogo. Alternativamente `xattr -d com.apple.quarantine ./rousseau` elimina el bit de cuarentena. El release firmado no está notarizado — la verificación cosign es la comprobación de cadena de suministro equivalente.

## Páginas relacionadas

- [Primeros pasos: Soporte de plataforma](/es/getting-started/platform-support/) — matriz de SO, arquitectura y autenticación por proveedor.
- [Primeros pasos: Tu primer transporte](/es/getting-started/first-transport/) — configura WhatsApp de principio a fin.
- [Primeros pasos: Actualización](/es/getting-started/updating/) — cómo moverse entre versiones de forma segura.
- [Despliegue](/es/deployment/) — el despliegue de referencia Podman sin root + Quadlet.
- [Seguridad](/es/security/) — fronteras de confianza y endurecimiento de cadena de suministro.

## Lectura adicional

- `README.md` — posicionamiento a nivel de repositorio y matriz de capacidades.
- `SECURITY.md` — divulgación de vulnerabilidades y controles de cadena de suministro.
- `Makefile` — el bloqueo exacto de CI reproducido localmente mediante `make check`.
- `docker/Dockerfile` — build multi-etapa (`golang:1.26-alpine` &rarr; `node:22-alpine`).
