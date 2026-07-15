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
description: "Contribution guide for rousseau-agent: conventional commits, PR process, reviewer checklist, release cadence."
keywords: "contributing, conventional commits, pr process, reviewer checklist, release"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/developer-guide/contributing/"
subtitle: "PR process, standards, review checklist."
tags: "developer-guide, contributing"
title: "Contribuir"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "contributing, conventional commits, pr process, reviewer checklist, release"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Contribuir"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 66
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/contributing/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/contributing/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Contribuir"
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
twitter_description: "Contribution guide for rousseau-agent: conventional commits, PR process, reviewer checklist, release cadence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Contribuir"
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

## Reglas básicas

Se aceptan contribuciones de colaboradores invitados. Cada PR se mantiene con el mismo listón: CI en verde, estándares de código listados abajo, aprobación del revisor. Un CI verde es necesario pero no suficiente.

La fuente autoritativa es el [`CONTRIBUTING.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/CONTRIBUTING.md) en la raíz del repositorio. Esta página lo refleja con la voz del sitio de docs.

## Entorno de desarrollo

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make setup      # instala golangci-lint (v2) y govulncheck
make check      # vet + lint + tests con race + govulncheck
```

Cada comprobación que corre en CI está disponible en local mediante el Makefile. Si un cambio pasa `make check`, pasará el CI.

## Estándares de commits

- **Conventional Commits** — `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `ci:`, `perf:`.
- Línea de asunto ≤ 72 caracteres. El cuerpo explica **por qué**, no qué. Referencia la decisión motora, la issue o el incidente.
- No enmiendes commits publicados. Crea un nuevo commit; el revisor prefiere una serie que pueda bisecar.
- Firma tus commits si tienes firma configurada. No es requerido actualmente, pero recomendado para commits de release-tag.

## Estándares de código

- Cada identificador exportado tiene un comentario godoc que empieza por el nombre del identificador.
- Nada de `interface{}` / `any` en APIs exportadas sin una justificación escrita en el comentario de documentación.
- `context.Context` se propaga por cada ruta de I/O. Sin globales ocultos ni loggers ambientales; pasa `*slog.Logger` de forma explícita.
- Los errores se envuelven hacia arriba con `fmt.Errorf("...: %w", err)`. Los errores centinela van en el `errors.go` del paquete. Prefiere `errors.Is` / `errors.As` en los sitios de llamada sobre el matching por cadena.
- Sin panics fuera de `main` y helpers de test. Se permiten variantes `Must*` que hacen panic ante error del operador (registro duplicado, esquema estático inválido) con una justificación documentada.
- Sin `fmt.Print*` en código de librería. Usa `slog` o un modelo TUI. El linter `forbidigo` lo aplica.

## Estándares de pruebas

- Los tests unitarios viven junto al código: `foo.go` → `foo_test.go`.
- Se prefieren tests table-driven. Usa `require` para aserciones que detienen, `assert` para las que no lo hacen.
- Inyección de tests basada en interfaces sobre el patching global. Cada paquete de transporte define una interfaz reducida (`WSConn`, `IMAPClient`, `HTTPClient`, `Sender`) que las pruebas satisfacen con fakes.
- Objetivo de cobertura: 85 % para paquetes de lógica de negocio pura; 75 % global.
- Race-safe: `go test -race` debe pasar. El código concurrente nuevo necesita un test de race si introduce sincronización no trivial.
- Funciones fuzz para cada parser (`FuzzParseFoo` junto a `parseFoo`). `make fuzz` ejecuta el corpus.

Consulta [Pruebas](/es/developer-guide/testing/) para el patrón de inyección.

## Proceso de pull request

1. Abre el PR contra `main`. Rebase (no merge) si `main` avanza mientras trabajas.
2. Cada PR requiere:
   - Una justificación en la descripción (2–3 frases enlazando a la decisión subyacente).
   - CI en verde: `vet`, `lint`, `test-race` en Linux + macOS, `govulncheck`, `codeql`, `reproducible-build`, umbral de cobertura.
   - Aprobación del revisor.
3. Solo merges squash. El mensaje del commit de merge es el mensaje final del commit y aterriza en `main` como un cambio atómico.
4. Si el PR añade una dependencia nueva, indica la justificación en la descripción. Prefiere la biblioteca estándar frente a añadir una dependencia; prefiere una dependencia existente frente a añadir una nueva.

## Checklist del revisor

Los revisores verifican, en orden:

1. **Necesidad.** ¿Es el cambio requerido, o añade superficie de abstracción / funcionalidad sin un requisito motor?
2. **Alcance.** ¿El cambio se mantiene dentro de su propósito declarado, o agrupa limpiezas no relacionadas?
3. **Integridad de fronteras.** ¿El cambio respeta la dirección de dependencia `agent → concreto`? Consulta [Arquitectura](/es/developer-guide/architecture/).
4. **Cobertura de pruebas.** ¿Están cubiertas las nuevas rutas de código? ¿Se ejercitan los casos límite?
5. **Manejo de errores.** ¿Se envuelven los errores con contexto? ¿Las rutas de limpieza son honestas (`_ =` con una justificación `//nolint:errcheck`, no silenciadas)?
6. **Godoc + linter limpio.** Cada símbolo exportado documentado; la salida de lint son 0 issues.
7. **Seguridad.** ¿El cambio toca la herramienta `bash`, la política de aprobación, la autenticación del transporte o la postura del contenedor? Si es así, ¿lo señala la descripción del PR?

## Contribuciones a la documentación

La documentación vive en un repositorio separado. Cuando un PR de código toca superficie visible al usuario (un nuevo flag, un nuevo campo, una nueva herramienta), el mismo PR — o un PR de seguimiento inmediato al repositorio de docs — debe actualizar las páginas afectadas.

- **Cambio en el CLI** → [Guía de usuario: CLI](/es/user-guide/cli/) y [Referencia: comandos CLI](/es/reference/cli-commands/).
- **Cambio de configuración** → [Configuración](/es/configuration/) y [Referencia: esquema de configuración](/es/reference/config-schema/).
- **Nueva herramienta** → [Guía de usuario: herramientas](/es/user-guide/tools/).
- **Nuevo transporte** → `content/transports/<name>.md`.
- **Nuevo proveedor** → `content/providers/<name>.md`.
- **Cambio de comportamiento** → [Changelog](/es/changelog/).

## Proceso de release

Las releases se cortan desde `main`:

1. Actualiza las entradas del changelog.
2. Etiqueta como `vX.Y.Z` en el commit de release.
3. El workflow `release` construye mediante GoReleaser, genera un SBOM CycloneDX, publica una firma cosign de los checksums y genera procedencia SLSA-3.
4. Los consumidores verifican según la receta en [Seguridad](/es/security/) e [Instalación](/es/getting-started/installation/).

Rousseau sigue [Versionado Semántico](/es/getting-started/updating/): patch arregla bugs, minor añade funcionalidades sin romper, major rompe — siempre con una receta de migración.

## Gobernanza

`rousseau-agent` es un proyecto de único mantenedor. La autoridad de decisión reside en el mantenedor de registro listado en `go.mod` y `LICENSE`. Los colaboradores proponen cambios de dirección vía discusión en PR o por correo a `sebastian.rousseau@gmail.com`.

## Divulgaciones de seguridad

**No abras una incidencia pública para un reporte de seguridad.** Envía correo a `sebastian.rousseau@gmail.com` según la [política de seguridad](/es/security/). Acuse en un plazo de 72 horas.

## Siguiente

- [Arquitectura](/es/developer-guide/architecture/) — el mapa antes de cambiarla.
- [Pruebas](/es/developer-guide/testing/) — el patrón que el revisor espera.
- [Seguridad](/es/security/) — la ruta de divulgación.
