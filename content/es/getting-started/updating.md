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
description: "How to update rousseau-agent: go install refresh, container tag rollover, config migration between minor versions, session-store compatibility policy."
keywords: "update, upgrade, go install, container tag, config migration, minor version"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/getting-started/updating/"
subtitle: "Move between versions without losing sessions or bricking the daemon."
tags: "update, upgrade, migration"
title: "Actualización"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "update, upgrade, go install, container tag, config migration, minor version"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Actualización"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 24
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/updating/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/updating/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Actualización"
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
twitter_description: "How to update rousseau-agent: go install refresh, container tag rollover, config migration between minor versions, session-store compatibility policy."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Actualización"
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

## Política de versionado

Rousseau sigue [Semantic Versioning](https://semver.org):

| Incremento | Qué cambia |
|---|---|
| Patch (`0.1.2 → 0.1.3`) | Correcciones de errores, correcciones de seguridad, actualizaciones de dependencias. Sin cambios en la configuración ni en el formato en disco. |
| Minor (`0.1.x → 0.2.0`) | Nuevas funcionalidades. Las adiciones de configuración siempre son no disruptivas; si se elimina un campo, un fallback con alias cubre al menos una versión menor. |
| Major (`0.x → 1.0`) | Cambios disruptivos. Requiere una receta de migración documentada en el [registro de cambios](/es/changelog/). |

La [política SECURITY.md](https://github.com/sebastienrousseau/rousseau-agent/blob/main/SECURITY.md) es explícita: solo `main` y la release etiquetada más reciente reciben correcciones de seguridad. No hay una rama de soporte a largo plazo.

## Método de actualización según la ruta de instalación

### Archivo de release firmado

```sh
VERSION=<new-tag>
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

La verificación no es opcional. Cada release incluye una firma cosign nueva; omitir la verificación anula la postura de cadena de suministro.

### `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

Para fijar una etiqueta exacta:

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@v0.4.2
```

`$GOBIN` (típicamente `~/go/bin`) debe estar en `$PATH` antes de `/usr/local/bin` si quieres que el binario nuevo tenga precedencia.

### Imagen de contenedor

Cambia la etiqueta en la referencia de la imagen y reinicia el servicio de systemd. Si usas la unidad Quadlet de referencia:

```sh
sed -i "s#Image=ghcr.io/sebastienrousseau/rousseau-agent:.*#Image=ghcr.io/sebastienrousseau/rousseau-agent:<new-tag>#" \
  ~/.config/containers/systemd/rousseau-agent.container
systemctl --user daemon-reload
systemctl --user restart rousseau-agent.service
journalctl --user -u rousseau-agent.service -f
```

Fijar `:latest` no es seguro en un despliegue con conciencia de cadena de suministro: siempre fija una etiqueta inmutable (`:v0.4.2`) y verifica el digest de la imagen contra las notas de release.

### Desde el código fuente

```sh
cd rousseau-agent
git fetch --tags
git checkout <new-tag>
make check          # ejecuta la validación completa de CI localmente
make build
sudo install -m 0755 bin/rousseau /usr/local/bin/rousseau
```

`make check` es la misma validación de 18 linters + race + govulncheck que aplica CI: una ejecución local exitosa garantiza que el trabajo de compilación reproducible también pasará.

## Migración de configuración

Los cambios en el esquema de configuración se documentan en el [registro de cambios](/es/changelog/) para cada versión menor. Los valores por defecto de Viper mantienen las claves antiguas funcionando durante un ciclo menor; se aplica el siguiente patrón:

- **Nueva clave agregada**: recibe un valor por defecto que preserva el comportamiento previo. No se requiere acción.
- **Clave renombrada**: la clave antigua queda aliasada por una versión menor. Se registra una advertencia cuando se accede al alias.
- **Clave eliminada**: se emite un error fail-fast en tiempo de carga. El registro de cambios nombra el reemplazo.

Para hacer una prueba en seco de una configuración contra un binario nuevo:

```sh
rousseau doctor --config ~/.config/rousseau/config.yaml
```

`rousseau doctor` recorre cada dependencia de tiempo de ejecución y cada opción de configuración; una fila `fail` muestra exactamente qué clave necesita atención.

## Compatibilidad del almacén de sesiones

`~/.local/share/rousseau/sessions.db` usa SQLite con un esquema versionado. Las migraciones del esquema son aditivas e idempotentes: el daemon ejecuta `CREATE TABLE IF NOT EXISTS` y `ALTER TABLE ADD COLUMN` al iniciar. **Nunca degrades** entre versiones menores una vez que el nuevo esquema se haya ejecutado; SQLite no eliminará columnas automáticamente, pero el código de la aplicación asume su presencia.

Si necesitas empezar de cero:

```sh
mv ~/.local/share/rousseau/sessions.db ~/.local/share/rousseau/sessions.db.bak
```

El daemon recrea el almacén en el siguiente arranque. Las credenciales del dispositivo de WhatsApp se almacenan por separado en `whatsapp.db`, por lo que reiniciar el almacén de sesiones no fuerza un nuevo emparejamiento.

## Compatibilidad del almacén de WhatsApp

`whatsapp.db` (el almacén de dispositivos de whatsmeow) está separado del almacén de sesiones precisamente para que una migración de esquema de sesión no pueda inutilizar el emparejamiento de WhatsApp. Si whatsmeow mismo cambia el formato en disco entre actualizaciones de rousseau, el registro de cambios lo marcará y la ruta de recuperación es: eliminar `whatsapp.db`, reiniciar, escanear de nuevo el QR.

## Reversión

- **Archivo de release firmado / `go install`**: reinstala la etiqueta anterior con la misma receta.
- **Contenedor**: cambia la etiqueta de la imagen a la anterior y reinicia.
- **Desde el código fuente**: `git checkout <old-tag> && make build`.

Las reversiones son seguras siempre que el esquema del almacén de sesiones en la versión anterior sea un superconjunto de lo que escribió la versión más nueva. En la práctica esto siempre es cierto dentro de una misma serie menor y usualmente cierto entre versiones menores adyacentes. Las actualizaciones mayores incluyen una receta de migración con una advertencia explícita de reversión en el registro de cambios.

## Siguiente

- [Registro de cambios](/es/changelog/): desglose release por release.
- [Solución de problemas](/es/troubleshooting/): si `rousseau doctor` muestra una fila `fail`.
