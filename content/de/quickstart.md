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
hreflang: "de"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "de"
locale: "de_DE"
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
permalink: "https://docs.rousseau-agent.dev/de/quickstart/"
subtitle: "rousseau in fünf Minuten: installieren, konfigurieren, chatten, verifizieren."
tags: "quickstart, install, provider, transport, supply-chain"
title: "Schnellstart"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "quickstart, install, first conversation, whatsapp, cosign, SLSA, SBOM, provider"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Schnellstart"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 0
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/quickstart/index.html"
item_link: "https://docs.rousseau-agent.dev/quickstart/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Schnellstart"
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
twitter_title: "Schnellstart"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## rousseau in 5 Minuten

Rousseau ist ein einzelnes statisches Go-Binary, das mit einer Bubble Tea TUI, einem SQLite-Sitzungsspeicher unter `~/.local/share/rousseau/sessions.db` und neun Chat-Transports (WhatsApp, Signal, Telegram, Slack, Discord, Matrix, iMessage, SMS, Email) ausgeliefert wird. Keine SaaS-Steuerungsebene, keine Telemetrie, kein Lizenzserver. Das LLM bringen Sie mit.

Diese Seite führt Sie von Anfang bis Ende durch:

- [ ] **1. rousseau installieren** — aus dem Quellcode, `go install` oder ein mit cosign verifiziertes Release.
- [ ] **2. Ihr LLM konfigurieren** — wählen Sie einen Provider (`claudecli` standardmäßig; Anthropic, Bedrock, Vertex oder einen beliebigen OpenAI-kompatiblen Endpunkt).
- [ ] **3. Ihr erstes Gespräch führen** — `rousseau chat` in Ihrem Terminal.
- [ ] **4. Einen Transport hinzufügen** — WhatsApp mit einer erlaubten JID koppeln.
- [ ] **5. Lieferkette verifizieren** — die Prüfsummen-Datei mit cosign verifizieren, dann die CycloneDX-SBOM und SLSA-3-Provenienz lesen.

Die meisten Operatoren schließen dies in unter zehn Minuten ab.

## 1. rousseau installieren

<aside class="admonition" data-type="tip"><span class="admonition-title">Empfohlen</span><p><code>go install</code> ist der schnellste Weg, wenn Sie bereits Go 1.26+ haben. Verwenden Sie in der Produktion ein signiertes Release mit <code>cosign verify-blob</code>, damit die Lieferketten-Garantien greifen.</p></aside>

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

Das Binary bettet `modernc.org/sqlite` ein (siehe `internal/state/sqlite/store.go`), daher gibt es zur Laufzeit keine libc- oder CGo-Abhängigkeit. Funktioniert identisch auf macOS, Linux und Windows.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` führt `go vet`, `golangci-lint`, `go test -race` und `govulncheck` aus — dieselben Gates, die die CI erzwingt.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Jedes getaggte Release veröffentlicht ein Archiv mit Prüfsumme, eine CycloneDX-SBOM, ein SLSA-3-Provenienz-Attestat und eine cosign-Signatur über die Prüfsummen-Datei:

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

<aside class="admonition" data-type="note"><span class="admonition-title">Hinweis</span><p>Die <code>cosign</code>-Identität ist auf die GitHub Actions OIDC von <code>sebastienrousseau/rousseau-agent</code> beschränkt. Siehe <a href="/de/security/">Sicherheit</a> für den Trust-Root.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau wird mit einem Podman-freundlichen `Dockerfile` unter `docker/Dockerfile` und einer systemd-Quadlet-Unit unter `docker/rousseau-agent.container` ausgeliefert. Ein veröffentlichtes Image auf ghcr.io ist auf der Roadmap; in der Zwischenzeit lokal bauen:

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
```

Siehe [Bereitstellung](/de/deployment/) für die Referenz-Quadlet-Unit mit gehärteter Runtime-Positionierung (rootless, `DropCapability=all`, `NoNewPrivileges=true`, seccomp).

  </div>
</div>

### Betriebssystemspezifische Voraussetzungen

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

Für den Standard-`claudecli`-Provider installieren Sie Claude Code von https://claude.ai/download und führen Sie `claude login` einmal aus.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Installieren Sie Go 1.26+ über Ihren Paketmanager oder von https://go.dev/dl. Verwenden Sie für den Container-Pfad rootless Podman ≥ 5.x mit dem `pasta`-Netzwerkmodus.

```sh
# Debian/Ubuntu
sudo apt install golang-1.26 podman

# Arch
sudo pacman -S go podman

# Fedora
sudo dnf install golang podman
```

Claude Code CLI (optional, für den `claudecli`-Provider): herunterladen von https://claude.ai/download.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau läuft nativ auf Windows via `go install`. Die Referenzbereitstellung für Container ist nur für Linux; verwenden Sie unter Windows WSL 2 für den Podman-Pfad.

```powershell
winget install GoLang.Go
# Or: choco install golang
```

Für `claudecli` installieren Sie Claude Code von https://claude.ai/download.

<aside class="admonition" data-type="warning"><span class="admonition-title">Hinweis zu Windows</span><p>Einige Transport-Pakete rufen Subprozesse auf (<code>signal-cli</code>) oder öffnen betriebssystemspezifische Pfade (<code>~/.local/share/</code>). Die Transports <code>whatsapp</code>, <code>slack</code>, <code>discord</code>, <code>telegram</code>, <code>matrix</code>, <code>email</code>, <code>sms</code> sind alle plattformübergreifend. <code>signal</code> und <code>imessage</code> benötigen ihre jeweiligen Host-Tools.</p></aside>

  </div>
</div>

## 2. Ihr LLM konfigurieren

Die Konfiguration liegt unter `~/.config/rousseau/config.yaml` (überschreibbar mit `--config`) und jedes Feld ist in `internal/config/config.go` definiert. Der Standard-Provider ist `claudecli`, der an Ihre lokale `claude`-CLI delegiert, sodass keine API-Schlüssel Ihren Laptop verlassen.

### claudecli (Standard, keine Schlüssel)

Wenn Sie Claude Code (`claude`) bereits installiert und authentifiziert haben, sind Sie fertig. Rousseau erbt dessen OAuth-Sitzung:

```yaml
provider: claudecli

claudecli:
  binary: claude              # optional; PATH lookup by default
  permission_mode: default    # or bypassPermissions for unattended daemons
```

Siehe [Providers: claudecli](/de/providers/claudecli/).

### Anthropic API

Direkt zu Anthropic. Verwendet das offizielle `anthropic-sdk-go` in `internal/llm/anthropic/client.go`:

```sh
export ANTHROPIC_API_KEY=sk-ant-…
```

```yaml
provider: anthropic
anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096
```

`ANTHROPIC_API_KEY` wird direkt aus der Umgebung gelesen (siehe `config.Load` in `internal/config/config.go`); der Schlüssel muss nie auf der Festplatte liegen. Siehe [Providers: Anthropic](/de/providers/anthropic/).

### AWS Bedrock

Verwendet die Standard-AWS-Credential-Chain (Profil, IMDS, IRSA). Region und Modell stammen aus `BedrockConfig` in `internal/config/config.go`:

```yaml
provider: bedrock
bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
  profile: default            # optional named profile
  max_tokens: 4096
```

Kein API-Schlüssel in `config.yaml`. Siehe [Providers: Bedrock](/de/providers/bedrock/).

### Google Vertex AI

Anthropic auf Vertex; liest eine Service-Account-JSON-Datei. Konfigurationsfelder definiert in `VertexConfig`:

```yaml
provider: vertex
vertex:
  project: my-gcp-project
  region: europe-west4
  model: claude-sonnet-4-6@20250101
  credentials_file: /etc/rousseau/vertex.json
  max_tokens: 4096
```

Siehe [Providers: Vertex](/de/providers/vertex/).

### OpenAI-kompatibel (OpenRouter, Ollama, vLLM, LM Studio)

Die Provider-Namen `openai`, `openrouter` und `ollama` teilen sich `OpenAIConfig`. Basis-URLs für OpenRouter und Ollama haben Standardwerte in `setDefaults` (`https://openrouter.ai/api/v1` und `http://localhost:11434/v1`); alles andere landet im `openai`-Block mit einer expliziten `base_url`:

```yaml
provider: ollama              # or: openai, openrouter
ollama:
  model: llama3.1:70b-instruct
  base_url: http://localhost:11434/v1
```

Siehe [Providers: OpenAI-kompatibel](/de/providers/openai-compatible/) und [Guides: Selbst gehostetes vLLM](/de/guides/self-hosted-vllm/).

## 3. Ihr erstes Gespräch führen

```sh
rousseau chat
```

Sie sehen eine Bubble Tea TUI (`internal/tui/model.go`):

- Ein **Viewport** oben scrollt das Transkript. Assistententext streamt herein, sobald er ankommt.
- Ein **Textbereich** unten nimmt Ihre Eingabe entgegen. Drücken Sie `Enter` zum Senden, `Ctrl+C` zum Beenden.
- Ein **Spinner** zeigt sich während LLM-Turns; ein kleiner Streaming-Indikator erscheint, während Tokens ankommen.
- Jeder Turn wird in SQLite unter `~/.local/share/rousseau/sessions.db` persistiert. Die WAL-Journalisierung wird durch `Open()` in `internal/state/sqlite/store.go` aktiviert, sodass Sie sicher andere rousseau-Befehle (`rousseau session list`, `rousseau mcp`) gegen dieselbe Datenbank ausführen können, während die TUI geöffnet ist.

Fragen Sie zuerst nach etwas Kleinem — z. B. „liste die Dateien unter `internal/tools/builtin`" — und rousseau ruft die eingebauten Tools `read`, `grep`, `edit`, `write` oder `bash` (`internal/tools/builtin/*.go`) nach Bedarf auf. Siehe [Benutzerhandbuch: TUI](/de/user-guide/tui/) für Tastenzuordnungen und [Benutzerhandbuch: Tools](/de/user-guide/tools/) für die Schemata.

Screenshot-Platzhalter: Die TUI zeigt eine zweizeilige Statusleiste (Sitzungs-ID und Provider), den Viewport mit farblich getönten Assistenten- + Benutzer-Nachrichten und den Textbereich unten im Fokus.

## 4. Einen Transport hinzufügen (WhatsApp)

WhatsApp ist der Referenz-Transport, weil die Kopplung am strengsten ist. Alle anderen Transports (`slack`, `discord`, `telegram`, `matrix`, `signal`, `sms`, `imessage`, `email`) folgen derselben Form.

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Beim ersten Start gibt `rousseau` einen QR-Code auf stdout aus. Scannen Sie ihn in **WhatsApp > Einstellungen > Verknüpfte Geräte** auf Ihrem Telefon. Der whatsmeow-Client (`internal/transport/whatsapp/client.go`) emittiert drei strukturierte Log-Events:

- `whatsapp.qr_ready` — QR wurde gerendert.
- `whatsapp.paired` — Telefon hat den QR akzeptiert.
- `whatsapp.connected` — Websocket zu Meta ist aktiv.

Die Geräte-Credentials werden in `~/.local/share/rousseau/whatsapp.db` gecacht (eine separate SQLite-Datenbank, sodass das Neuverknüpfen eines Geräts den Konversationsverlauf nicht berührt). Das Flag `--allow` pinnt eine Allowlist von E.164-JIDs; jeder andere Absender wird stillschweigend von `router.transport.rejected` verworfen.

Rousseau verwendet das **inoffizielle** WhatsApp-Web-Protokoll. Meta sperrt gelegentlich Nummern, die inoffizielle Clients ausführen — führen Sie dies nicht auf einer Nummer aus, auf die Sie angewiesen sind. Siehe [Transports: WhatsApp](/de/transports/whatsapp/) für die Risikoanalyse.

## 5. Lieferkette verifizieren

Jedes getaggte Release liefert:

| Artefakt | Zweck |
|---|---|
| `rousseau_<v>_checksums.txt` | SHA-256 jedes Archivs im Release. |
| `rousseau_<v>_checksums.txt.sig` | cosign-Signatur (keyless, OIDC-ausgestellt aus GitHub Actions). |
| `rousseau_<v>_sbom.cdx.json` | CycloneDX 1.5 SBOM des Go-Modul-Graphen. |
| `rousseau_<v>_provenance.intoto.jsonl` | SLSA-3-Provenienz-Attestation. |

Verifizieren Sie die Signaturidentität, bevor Sie den Prüfsummen vertrauen:

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_0.6.0_checksums.txt.sig \
  rousseau_0.6.0_checksums.txt
```

Das `--certificate-identity-regexp` pinnt die Signaturidentität auf das rousseau-agent-Repository unter Sebastiens Namespace. **Schwächen Sie es nicht ab.** Eine Wildcard-Identität hebelt den Sinn der keyless Signatur aus.

Sobald die Signatur verifiziert ist, beweist `sha256sum -c`, dass der heruntergeladene Tarball derjenige ist, den die CI gebaut hat. Lesen Sie die SBOM mit `cyclonedx-cli tree`, verifizieren Sie die SLSA-3-Provenienz mit `slsa-verifier verify-artifact`, und extrahieren Sie das Archiv erst dann.

Siehe [Sicherheit](/de/security/) für die vollständigen Vertrauensgrenzen und [Guides: Enterprise-Onboarding](/de/guides/enterprise-onboarding/) für die Checkliste des Plattform-Teams.

## Fehlerbehebung

<aside class="admonition" data-type="tip"><span class="admonition-title">Empfohlener erster Stopp</span><p>Führen Sie <code>rousseau doctor</code> aus, bevor Sie ein Issue öffnen. Es beansprucht jedes Subsystem — Provider-Auth, Zustandsspeicher, Transport-Credentials — und gibt strukturierte pass/warn/fail-Zeilen aus.</p></aside>

### `rousseau version` gibt nach `go install` „dev" aus

Die Werte `version`, `commit` und `buildDate` werden von der Release-Toolchain via `-ldflags` in `internal/cli/root.go` gestempelt. `go install` überspringt diese Flags, daher meldet das Binary `dev / none / unknown`. Verwenden Sie den signierten Release-Pfad, wenn Sie einen stabilen Versionsstring benötigen; der `dev`-String ist zur Laufzeit harmlos.

### `claudecli: exec: "claude": executable file not found`

`provider: claudecli` delegiert an das `claude`-Binary. Setzen Sie Claude Code entweder in Ihr `$PATH` (siehe [Providers: claudecli](/de/providers/claudecli/)) oder wechseln Sie den Provider — die schnellste Alternative ist `provider: anthropic` mit exportiertem `ANTHROPIC_API_KEY`.

### WhatsApp-QR wird angezeigt, aber nie akzeptiert

Drei häufige Ursachen: (1) die Container-Uhr ist um mehr als 30 Sekunden verschoben — der WhatsApp-Handshake ist zeitkritisch; (2) eine teilweise abgeschlossene Kopplung hat `whatsapp.db` in einem unbrauchbaren Zustand hinterlassen — löschen Sie `~/.local/share/rousseau/whatsapp.db` und scannen Sie erneut; (3) Meta hat die Nummer invalidiert — versuchen Sie eine neue Telefonnummer. Siehe [Transports: WhatsApp](/de/transports/whatsapp/).

### `cosign verify-blob` gibt „no matching signatures" aus

Das `--certificate-identity-regexp` muss dem GitHub-Repository des Unterzeichners entsprechen. Für rousseau-agent ist der korrekte Wert `sebastienrousseau/rousseau-agent`. Eine Wildcard hebelt den Sinn der keyless Signatur aus — schwächen Sie sie nicht ab. Wenn die Regex korrekt ist, aktualisieren Sie den Trust-Root von Sigstore mit `cosign initialize`.

### Jeder Tool-Aufruf wird mit „denied by pattern policy" abgelehnt

Sie laufen im `pattern`-Modus mit `default: deny` und ohne passende Allow-Regel. Fügen Sie einen Allow-Eintrag für das Tool hinzu, oder schalten Sie auf `default: allow` um und fügen Sie stattdessen enge Deny-Regeln hinzu. Siehe [Benutzerhandbuch: Genehmigungsrichtlinien](/de/user-guide/approval-policies/) für ausgearbeitete Beispiele.

## Verwandte Seiten

- [Einstieg: Installation](/de/getting-started/installation/) — jede Installationsmethode mit dem Verifikationsrezept.
- [Einstieg: Erster Transport](/de/getting-started/first-transport/) — End-to-End-Walkthrough für WhatsApp/Slack/Discord.
- [Konfiguration](/de/configuration/) — jeder Regler in `~/.config/rousseau/config.yaml`.
- [Konzepte](/de/concepts/) — die Agent-Schleife, der Sitzungsspeicher, MCP, cron, Skills.
- [Fehlerbehebung](/de/troubleshooting/) — der vollständige Fehlermodus-Katalog.

## Weiterführende Literatur

- `README.md` — Positionierung auf Repository-Ebene und Fähigkeitsmatrix.
- `SECURITY.md` — Vertrauensgrenzen und Lieferketten-Härtung.
- `internal/config/config.go` — die autoritative Config-Struct.
- `internal/cli/root.go` — Cobra-Kommandobaum-Verkabelung.

## Nächste Schritte

| Wohin gehen | Warum |
|---|---|
| [Konfiguration](/de/configuration/) | Jeder Regler in `~/.config/rousseau/config.yaml` mit Standardwerten. |
| [Konzepte](/de/concepts/) | Die Agent-Schleife, der Sitzungsspeicher, MCP, cron, Skills. |
| [Bereitstellung](/de/deployment/) | Rootless Podman + systemd-Quadlet-Unit. |
| [Sicherheit](/de/security/) | Vertrauensgrenzen, SLSA-3-Provenienz, seccomp-Positionierung. |
| [Tutorials](/de/tutorials/) | Vollständige End-to-End-Walkthroughs. |
| [Referenz](/de/reference/cli-commands/) | Jedes CLI-Flag, jeder Exit-Code und Config-Feld. |
