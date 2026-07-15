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
description: "Install rousseau-agent, configure a provider, hold your first conversation, wire a transport, and verify the release supply chain in about five minutes."
keywords: "quickstart, install, first conversation, whatsapp, cosign, SLSA, SBOM, provider"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/quickstart/"
subtitle: "rousseau en cinco minutos: instalar, configurar, conversar, verificar."
tags: "quickstart, install, provider, transport, supply-chain"
title: "Inicio rápido"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "quickstart, install, first conversation, whatsapp, cosign, SLSA, SBOM, provider"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Inicio rápido"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 0
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/quickstart/index.html"
item_link: "https://docs.rousseau-agent.dev/quickstart/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Inicio rápido"
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
twitter_description: "Install rousseau-agent, configure a provider, hold your first conversation, wire a transport, and verify the release supply chain in about five minutes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Inicio rápido"
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

## rousseau en 5 minutos

Rousseau es un único binario Go estático que incluye una TUI de Bubble Tea, un almacén de sesiones SQLite en `~/.local/share/rousseau/sessions.db` y nueve transportes de chat (WhatsApp, Signal, Telegram, Slack, Discord, Matrix, iMessage, SMS, email). Sin plano de control SaaS, sin telemetría, sin servidor de licencias. Usted proporciona el LLM.

Esta página lo lleva de principio a fin:

- [ ] **1. Instalar rousseau** — desde el código fuente, `go install` o una release verificada con cosign.
- [ ] **2. Configurar su LLM** — elija un provider (`claudecli` por defecto; Anthropic, Bedrock, Vertex o cualquier endpoint compatible con OpenAI).
- [ ] **3. Tener su primera conversación** — `rousseau chat` en su terminal.
- [ ] **4. Añadir un transporte** — emparejar WhatsApp con un JID permitido.
- [ ] **5. Verificar la cadena de suministro** — verificar con cosign el archivo de sumas de verificación, luego leer el SBOM CycloneDX y la procedencia SLSA-3.

La mayoría de los operadores terminan en menos de diez minutos.

## 1. Instalar rousseau

<aside class="admonition" data-type="tip"><span class="admonition-title">Recomendado</span><p><code>go install</code> es la vía más rápida si ya tiene Go 1.26+. Para producción, use una release firmada con <code>cosign verify-blob</code> para conservar las garantías de la cadena de suministro.</p></aside>

<div class="tabs" data-tabs="qs-install">
  <div class="tab-list" role="tablist" aria-label="Install method">
    <button role="tab" aria-selected="true">go install</button>
    <button role="tab" aria-selected="false">From source</button>
    <button role="tab" aria-selected="false">Signed release</button>
    <button role="tab" aria-selected="false">Container</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
rousseau version
```

El binario incrusta `modernc.org/sqlite` (ver `internal/state/sqlite/store.go`), por lo que no hay dependencia de libc o CGo en tiempo de ejecución. Funciona de forma idéntica en macOS, Linux y Windows.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` ejecuta `go vet`, `golangci-lint`, `go test -race` y `govulncheck` — las mismas puertas que aplica la CI.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Cada release etiquetada publica un archivo con suma de verificación, un SBOM CycloneDX, una atestación de procedencia SLSA-3 y una firma cosign sobre el archivo de sumas de verificación:

```sh
curl -LO https://github.com/sebastienrousseau/rousseau-agent/releases/download/v0.6.0/rousseau_0.6.0_linux_amd64.tar.gz
curl -LO https://github.com/sebastienrousseau/rousseau-agent/releases/download/v0.6.0/rousseau_0.6.0_checksums.txt
curl -LO https://github.com/sebastienrousseau/rousseau-agent/releases/download/v0.6.0/rousseau_0.6.0_checksums.txt.sig

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_0.6.0_checksums.txt.sig \
  rousseau_0.6.0_checksums.txt

sha256sum -c rousseau_0.6.0_checksums.txt --ignore-missing
tar -xzf rousseau_0.6.0_linux_amd64.tar.gz
sudo install -m 0755 rousseau /usr/local/bin/
```

<aside class="admonition" data-type="note"><span class="admonition-title">Nota</span><p>La identidad de <code>cosign</code> está limitada al OIDC de GitHub Actions de <code>sebastienrousseau/rousseau-agent</code>. Consulte <a href="/es/security/">Seguridad</a> para la raíz de confianza.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau se distribuye con un `Dockerfile` compatible con Podman en `docker/Dockerfile` y una unidad Quadlet de systemd en `docker/rousseau-agent.container`. Una imagen publicada en ghcr.io está en la hoja de ruta; mientras tanto, constrúyala localmente:

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
```

Consulte [Despliegue](/es/deployment/) para la unidad Quadlet de referencia con postura de ejecución endurecida (rootless, `DropCapability=all`, `NoNewPrivileges=true`, seccomp).

  </div>
</div>

### Prerrequisitos específicos del SO

<div class="tabs" data-tabs="qs-os">
  <div class="tab-list" role="tablist" aria-label="Operating system">
    <button role="tab" aria-selected="true">macOS</button>
    <button role="tab" aria-selected="false">Linux</button>
    <button role="tab" aria-selected="false">Windows</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```sh
brew install go@1.26
# For the container path:
brew install podman
podman machine init && podman machine start
```

Para el provider `claudecli` por defecto, instale Claude Code desde https://claude.ai/download y ejecute `claude login` una vez.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Instale Go 1.26+ mediante su gestor de paquetes o desde https://go.dev/dl. Para la vía de contenedor, use Podman rootless ≥ 5.x con el modo de red `pasta`.

```sh
# Debian/Ubuntu
sudo apt install golang-1.26 podman

# Arch
sudo pacman -S go podman

# Fedora
sudo dnf install golang podman
```

Claude Code CLI (opcional, para el provider `claudecli`): descargue desde https://claude.ai/download.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau se ejecuta de forma nativa en Windows mediante `go install`. El despliegue de referencia por contenedor es solo para Linux; en Windows use WSL 2 para la vía Podman.

```powershell
winget install GoLang.Go
# Or: choco install golang
```

Para `claudecli`, instale Claude Code desde https://claude.ai/download.

<aside class="admonition" data-type="warning"><span class="admonition-title">Nota sobre Windows</span><p>Algunos paquetes de transporte llaman a subprocesos (<code>signal-cli</code>) o abren rutas específicas del SO (<code>~/.local/share/</code>). Los transportes <code>whatsapp</code>, <code>slack</code>, <code>discord</code>, <code>telegram</code>, <code>matrix</code>, <code>email</code>, <code>sms</code> son todos multiplataforma. <code>signal</code> e <code>imessage</code> requieren sus respectivas herramientas host.</p></aside>

  </div>
</div>

## 2. Configurar su LLM

La configuración vive en `~/.config/rousseau/config.yaml` (anulable con `--config`) y cada campo está definido en `internal/config/config.go`. El provider por defecto es `claudecli`, que delega a su CLI local `claude`, por lo que ninguna clave de API sale de su portátil.

### claudecli (por defecto, sin claves)

Si ya tiene Claude Code (`claude`) instalado y autenticado, ya terminó. Rousseau hereda su sesión OAuth:

```yaml
provider: claudecli

claudecli:
  binary: claude              # optional; PATH lookup by default
  permission_mode: default    # or bypassPermissions for unattended daemons
```

Consulte [Providers: claudecli](/es/providers/claudecli/).

### API de Anthropic

Anthropic directo. Usa el SDK oficial `anthropic-sdk-go` en `internal/llm/anthropic/client.go`:

```sh
export ANTHROPIC_API_KEY=sk-ant-…
```

```yaml
provider: anthropic
anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096
```

`ANTHROPIC_API_KEY` se lee directamente del entorno (ver `config.Load` en `internal/config/config.go`); la clave nunca tiene que residir en disco. Consulte [Providers: Anthropic](/es/providers/anthropic/).

### AWS Bedrock

Usa la cadena de credenciales estándar de AWS (perfil, IMDS, IRSA). La región y el modelo provienen de `BedrockConfig` en `internal/config/config.go`:

```yaml
provider: bedrock
bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
  profile: default            # optional named profile
  max_tokens: 4096
```

Sin clave de API en `config.yaml`. Consulte [Providers: Bedrock](/es/providers/bedrock/).

### Google Vertex AI

Anthropic sobre Vertex; lee un archivo JSON de cuenta de servicio. Campos de configuración definidos en `VertexConfig`:

```yaml
provider: vertex
vertex:
  project: my-gcp-project
  region: europe-west4
  model: claude-sonnet-4-6@20250101
  credentials_file: /etc/rousseau/vertex.json
  max_tokens: 4096
```

Consulte [Providers: Vertex](/es/providers/vertex/).

### Compatible con OpenAI (OpenRouter, Ollama, vLLM, LM Studio)

Los nombres de provider `openai`, `openrouter` y `ollama` comparten `OpenAIConfig`. Las URL base para OpenRouter y Ollama tienen valores por defecto en `setDefaults` (`https://openrouter.ai/api/v1` y `http://localhost:11434/v1`); todo lo demás cae en el bloque `openai` con un `base_url` explícito:

```yaml
provider: ollama              # or: openai, openrouter
ollama:
  model: llama3.1:70b-instruct
  base_url: http://localhost:11434/v1
```

Consulte [Providers: Compatible con OpenAI](/es/providers/openai-compatible/) y [Guías: vLLM autoalojado](/es/guides/self-hosted-vllm/).

## 3. Tener su primera conversación

```sh
rousseau chat
```

Verá una TUI de Bubble Tea (`internal/tui/model.go`):

- Un **viewport** en la parte superior desplaza la transcripción. El texto del asistente se transmite a medida que llega.
- Un **área de texto** en la parte inferior toma su entrada. Presione `Enter` para enviar, `Ctrl+C` para salir.
- Un **spinner** se muestra durante los turnos del LLM; un pequeño indicador de streaming aparece mientras llegan los tokens.
- Cada turno se persiste en SQLite en `~/.local/share/rousseau/sessions.db`. El journaling WAL se habilita mediante `Open()` en `internal/state/sqlite/store.go`, por lo que puede ejecutar de forma segura otros comandos de rousseau (`rousseau session list`, `rousseau mcp`) contra la misma base de datos mientras la TUI está abierta.

Empiece por pedir algo pequeño — por ejemplo, "listar los archivos bajo `internal/tools/builtin`" — y rousseau llamará a las herramientas integradas `read`, `grep`, `edit`, `write` o `bash` (`internal/tools/builtin/*.go`) según sea necesario. Consulte [Guía de usuario: TUI](/es/user-guide/tui/) para los atajos de teclado y [Guía de usuario: Herramientas](/es/user-guide/tools/) para los esquemas.

Marcador para captura de pantalla: la TUI muestra una barra de estado de dos líneas (id de sesión y provider), el viewport con mensajes de asistente + usuario tintados de color y el área de texto en foco en la parte inferior.

## 4. Añadir un transporte (WhatsApp)

WhatsApp es el transporte de referencia porque el emparejamiento es el más estricto. Todos los demás transportes (`slack`, `discord`, `telegram`, `matrix`, `signal`, `sms`, `imessage`, `email`) siguen la misma forma.

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

En el primer lanzamiento, `rousseau` imprime un código QR en stdout. Escanéelo en **WhatsApp > Configuración > Dispositivos vinculados** en su teléfono. El cliente whatsmeow (`internal/transport/whatsapp/client.go`) emite tres eventos de log estructurados:

- `whatsapp.qr_ready` — el QR fue renderizado.
- `whatsapp.paired` — el teléfono aceptó el QR.
- `whatsapp.connected` — el websocket a Meta está activo.

Las credenciales del dispositivo se almacenan en caché en `~/.local/share/rousseau/whatsapp.db` (una base de datos SQLite separada, por lo que revincular un dispositivo no toca el historial de conversaciones). El flag `--allow` fija una allowlist de JIDs E.164; cualquier otro remitente es descartado silenciosamente por `router.transport.rejected`.

Rousseau usa el protocolo de WhatsApp Web **no oficial**. Meta ocasionalmente banea los números que ejecutan clientes no oficiales — no lo ejecute en un número del que dependa. Consulte [Transportes: WhatsApp](/es/transports/whatsapp/) para el análisis de riesgos.

## 5. Verificar la cadena de suministro

Cada release etiquetada entrega:

| Artefacto | Propósito |
|---|---|
| `rousseau_<v>_checksums.txt` | SHA-256 de cada archivo en la release. |
| `rousseau_<v>_checksums.txt.sig` | Firma cosign (keyless, emitida por OIDC desde GitHub Actions). |
| `rousseau_<v>_sbom.cdx.json` | SBOM CycloneDX 1.5 del grafo de módulos Go. |
| `rousseau_<v>_provenance.intoto.jsonl` | Atestación de procedencia SLSA-3. |

Verifique la identidad de la firma antes de confiar en las sumas de verificación:

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_0.6.0_checksums.txt.sig \
  rousseau_0.6.0_checksums.txt
```

El `--certificate-identity-regexp` fija la identidad del firmante al repositorio rousseau-agent bajo el namespace de Sebastien. **No la debilite.** Una identidad comodín anula el propósito de la firma keyless.

Una vez verificada la firma, `sha256sum -c` demuestra que el tarball que descargó es el que la CI construyó. Lea el SBOM con `cyclonedx-cli tree`, verifique la procedencia SLSA-3 con `slsa-verifier verify-artifact`, y solo entonces extraiga el archivo.

Consulte [Seguridad](/es/security/) para los límites de confianza completos y [Guías: Onboarding empresarial](/es/guides/enterprise-onboarding/) para la lista de verificación del equipo de plataforma.

## Resolución de problemas

<aside class="admonition" data-type="tip"><span class="admonition-title">Primera parada recomendada</span><p>Ejecute <code>rousseau doctor</code> antes de abrir un issue. Ejercita cada subsistema — auth del provider, almacén de estado, credenciales de transporte — e imprime filas estructuradas pass/warn/fail.</p></aside>

### `rousseau version` imprime "dev" después de `go install`

Los valores `version`, `commit` y `buildDate` son estampados por la cadena de herramientas de release mediante `-ldflags` en `internal/cli/root.go`. `go install` omite esos flags, por lo que el binario informa `dev / none / unknown`. Use la vía de release firmada si necesita una cadena de versión estable; la cadena `dev` es inofensiva en tiempo de ejecución.

### `claudecli: exec: "claude": executable file not found`

`provider: claudecli` delega al binario `claude`. O bien ponga Claude Code en su `$PATH` (ver [Providers: claudecli](/es/providers/claudecli/)) o cambie de provider — la alternativa más rápida es `provider: anthropic` con `ANTHROPIC_API_KEY` exportada.

### El QR de WhatsApp se muestra pero nunca se acepta

Tres causas comunes: (1) el reloj del contenedor está desfasado por más de 30 segundos — el handshake de WhatsApp es sensible al tiempo; (2) un emparejamiento parcialmente completado dejó `whatsapp.db` en un estado no reutilizable — elimine `~/.local/share/rousseau/whatsapp.db` y vuelva a escanear; (3) Meta invalidó el número — pruebe con un número de teléfono nuevo. Consulte [Transportes: WhatsApp](/es/transports/whatsapp/).

### `cosign verify-blob` da error "no matching signatures"

El `--certificate-identity-regexp` debe coincidir con el repositorio GitHub del firmante. Para rousseau-agent, el valor correcto es `sebastienrousseau/rousseau-agent`. Un comodín anula el propósito de la firma keyless — no la debilite. Si la regex es correcta, refresque la raíz de confianza de Sigstore con `cosign initialize`.

### Cada llamada a herramienta es denegada con "denied by pattern policy"

Está ejecutando en modo `pattern` con `default: deny` y sin regla de permiso coincidente. Añada una entrada de permiso para la herramienta, o cambie a `default: allow` y añada reglas de denegación estrechas en su lugar. Consulte [Guía de usuario: Políticas de aprobación](/es/user-guide/approval-policies/) para ejemplos elaborados.

## Páginas relacionadas

- [Primeros pasos: Instalación](/es/getting-started/installation/) — cada método de instalación con la receta de verificación.
- [Primeros pasos: Primer transporte](/es/getting-started/first-transport/) — recorrido de extremo a extremo de WhatsApp/Slack/Discord.
- [Configuración](/es/configuration/) — cada ajuste en `~/.config/rousseau/config.yaml`.
- [Conceptos](/es/concepts/) — el bucle del agente, el almacén de sesiones, MCP, cron, skills.
- [Resolución de problemas](/es/troubleshooting/) — el catálogo completo de modos de fallo.

## Lecturas adicionales

- `README.md` — posicionamiento a nivel de repositorio y matriz de capacidades.
- `SECURITY.md` — límites de confianza y endurecimiento de la cadena de suministro.
- `internal/config/config.go` — la struct de configuración autoritativa.
- `internal/cli/root.go` — cableado del árbol de comandos Cobra.

## Próximos pasos

| A dónde ir | Por qué |
|---|---|
| [Configuración](/es/configuration/) | Cada ajuste en `~/.config/rousseau/config.yaml` con los valores por defecto. |
| [Conceptos](/es/concepts/) | El bucle del agente, el almacén de sesiones, MCP, cron, skills. |
| [Despliegue](/es/deployment/) | Podman rootless + unidad Quadlet de systemd. |
| [Seguridad](/es/security/) | Límites de confianza, procedencia SLSA-3, postura seccomp. |
| [Tutoriales](/es/tutorials/) | Recorridos completos de extremo a extremo. |
| [Referencia](/es/reference/cli-commands/) | Cada flag de CLI, código de salida y campo de configuración. |
