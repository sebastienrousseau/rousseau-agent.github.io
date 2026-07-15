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
description: "Install rousseau-agent on macOS, Linux, or Windows. From-source build, go install, cosign-verified release archive, Podman / Docker image, checksum verification recipe."
keywords: "install, macos, linux, windows, homebrew, cosign, sha256, podman, docker, go install"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/getting-started/installation/"
subtitle: "Every supported install method with the verification recipe."
tags: "install, macos, linux, windows, cosign, docker"
title: "Installation"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "install, macos, linux, windows, homebrew, cosign, sha256, podman, docker, go install"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Installation"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 21
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/installation/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/installation/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Installation"
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
twitter_title: "Installation"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Jede unterstützte Installationsmethode für rousseau, Befehle pro Betriebssystem, das cosign-/SHA-256-/SLSA-3-Verifikations-Rezept sowie die Fehlermodi, die Erstinstallationen abfangen. Überfliegen Sie die untenstehende Tabelle, um eine Methode auszuwählen, und springen Sie zu Ihrem Betriebssystem.</p></aside>

## Installationsmethode wählen

| Methode | Wann anwenden | Verifizierbar |
|---|---|---|
| Signiertes Release-Archiv | Produktion, Air-Gapped-Umgebungen, jede regulierte Umgebung. | Ja – cosign + SHA-256-Checksums + SLSA-3-Provenance. |
| `go install` | Einzelentwickler, die der Checksum-Datenbank des Go-Modul-Proxys vertrauen. | Teilweise – `go.sum`-Pinning über `pkg.go.dev`. |
| Aus Quellcode (`make build`) | Mitwirkende und Reviewer, die das komplette CI-Gate lokal ausführen wollen. | Ja – Reproducible-Build-Job in CI bestätigt bitidentische Ausgabe. |
| Container-Image | Bereitstellungen neben anderen systemd-Diensten oder in Kubernetes. | Ja – Image wird aus dem getaggten Source gebaut, Provenance ist angehängt. |
| Homebrew (geplant) | macOS-Komfort. | Geplant; noch nicht ausgeliefert. |

<aside class="admonition" data-type="caution"><span class="admonition-title">Verifikation überspringen auf eigene Gefahr</span><p>Der signierte Release-Pfad ist die einzige Methode, die Ihnen eine Kette vom Source-Commit über GitHub Actions OIDC bis zum Archiv auf der Festplatte gibt. Wenn Sie kein beliebiges Binary aus dem Internet ausführen würden, überspringen Sie nicht <code>cosign verify-blob</code> + <code>sha256sum -c</code>. Beide Befehle sind unten pro Betriebssystem gezeigt.</p></aside>

## Installation nach Betriebssystem

<div class="tabs" data-tabs="install-os">
  <div class="tab-list" role="tablist" aria-label="Operating system">
    <button role="tab" aria-selected="true">macOS</button>
    <button role="tab" aria-selected="false">Linux</button>
    <button role="tab" aria-selected="false">Windows</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Signiertes Release (empfohlen).** Funktioniert auf Apple Silicon und Intel – auf Intel-Macs `arm64` gegen `amd64` austauschen.

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

**`go install`.** Schnellster Weg, wenn Sie bereits Go 1.26+ installiert haben:

```sh
brew install go@1.26        # oder von https://go.dev/dl
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

Das Binary bettet `modernc.org/sqlite` ein (siehe `internal/state/sqlite/store.go`), weshalb keine libc- oder CGo-Abhängigkeit und keine Xcode Command Line Tools erforderlich sind.

**Homebrew.** Die Homebrew-Formula steht auf der Roadmap. Bis dahin nutzen Sie den Release-Archiv-Pfad oben.

<aside class="admonition" data-type="note"><span class="admonition-title">Gatekeeper</span><p>Das signierte Archiv ist nicht durch Apples Notarisierungsdienst signiert (rousseau liefert keine Apple-Developer-ID mit). Der erste Start kann eine Gatekeeper-Aufforderung anzeigen; genehmigen Sie sie unter <em>Systemeinstellungen &gt; Datenschutz &amp; Sicherheit</em>. Die Verifikation der cosign-Signatur ist die äquivalente Lieferketten-Prüfung.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Signiertes Release (empfohlen).** `aarch64`-Builds werden unter `linux_arm64` veröffentlicht:

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

**Distro-Pakete.** Noch keine First-Party-Pakete – nutzen Sie die Release-Archive oben.

**Rootless Podman (Produktion).** Siehe [Bereitstellung](/de/deployment/) für die Quadlet-Referenz. Das `pasta`-Netzwerk erfordert Podman 5.x+; Debian 12 und Ubuntu 22.04 liefern 4.x und benötigen einen `slirp4netns`-Fallback (Roadmap).

<aside class="admonition" data-type="warning"><span class="admonition-title">Distributions-Go</span><p>Debian/Ubuntu liefern häufig ein Go, das älter als 1.26 ist. Wenn <code>go version</code> &lt; 1.26 meldet, installieren Sie direkt von <a href="https://go.dev/dl">go.dev/dl</a> oder nutzen Sie das signierte Release-Archiv – <code>go install</code> gegen eine alte Toolchain scheitert an Modul-Features, die rousseau verwendet.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau ist ein First-Class-Build-Ziel für Windows; jeder Transport funktioniert auf Windows ausser `signal` (benötigt den `signal-cli`-JVM-Subprozess) und `imessage` (benötigt macOS). Die Referenz-Bereitstellung mit Podman + Quadlet ist Linux-only – nutzen Sie WSL 2 oder eine Linux-VM für den Container-Pfad.

**Signiertes Release.** PowerShell:

```powershell
$Version = "<pin-a-tag>"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_windows_amd64.zip" -OutFile "rousseau.zip"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_checksums.txt" -OutFile "checksums.txt"
Get-FileHash rousseau.zip -Algorithm SHA256
Expand-Archive rousseau.zip -DestinationPath .
```

Vergleichen Sie die `Get-FileHash`-Ausgabe visuell mit `checksums.txt` oder leiten Sie sie durch PowerShell, um die Prüfung zu skripten.

**`go install`.** Funktioniert auf Windows sofort, sobald Go auf dem PATH liegt:

```powershell
winget install GoLang.Go
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

<aside class="admonition" data-type="warning"><span class="admonition-title">cosign auf Windows</span><p>Die <code>cosign</code>-CLI läuft auf Windows, ist aber ein grosser Download und benötigt eine eigene Abhängigkeits-Kette. Für eine reibungsarme Verifikation führen Sie <code>cosign verify-blob</code> einmalig aus WSL 2 oder einer Linux-VM gegen dieselbe Checksum-Datei aus und vertrauen dann dem SHA-256-Rezept auf Windows.</p></aside>

<aside class="admonition" data-type="warning"><span class="admonition-title">Home-Verzeichnis-Pfade</span><p>Rousseau schreibt State unter Windows nach <code>%APPDATA%\rousseau\sessions.db</code> (über <code>os.UserConfigDir()</code> in <code>internal/config/config.go</code>). Die Dokumentation verweist manchmal auf den Unix-Pfad <code>~/.local/share/rousseau/</code> – dieselbe Datei liegt am plattform-typischen Ort.</p></aside>

  </div>
</div>

## Ein signiertes Release verifizieren

Der Befehl `cosign verify-blob` führt drei Prüfungen gleichzeitig gegen Sigstores öffentliches Transparenz-Log durch:

1. Das in der Signatur eingebettete Zertifikat wurde für die GitHub-Actions-OIDC-Identität ausgestellt, die zur Regex passt.
2. Die Signatur über die Checksum-Datei ist gültig.
3. Das Zertifikat wurde vom Transparenz-Log bezeugt.

`sha256sum -c` bestätigt anschliessend, dass jedes Artefakt in der Checksum-Datei übereinstimmt. Dies ist die tragende Lieferketten-Prüfung – überspringen Sie sie nicht.

### SBOM verifizieren

Jedes Release liefert `rousseau_<version>_sbom.cdx.json` (CycloneDX 1.5). Prüfen Sie mit `cyclonedx-cli`:

```sh
cyclonedx-cli tree --input-file rousseau_<version>_sbom.cdx.json
cyclonedx-cli validate --input-file rousseau_<version>_sbom.cdx.json
```

### SLSA-3-Provenance verifizieren

```sh
slsa-verifier verify-artifact \
  --provenance-path rousseau_<version>_provenance.intoto.jsonl \
  --source-uri github.com/sebastienrousseau/rousseau-agent \
  --source-tag <version> \
  rousseau_<version>_linux_amd64.tar.gz
```

Jede Abweichung zwischen dem Artefakt und dem, was CI attestiert gebaut zu haben, führt dazu, dass `slsa-verifier` mit einem Nicht-Null-Status beendet wird.

## macOS

### Signiertes Release (empfohlen)

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

Ersetzen Sie `arm64` durch `amd64` auf Intel-Macs.

### Homebrew (geplant)

Die Homebrew-Formula steht auf der Roadmap. Bis dahin ist der Release-Archiv-Pfad oben die empfohlene macOS-Installation.

## Linux

### Signiertes Release (empfohlen)

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

`aarch64`-Builds werden unter `linux_arm64` veröffentlicht.

Die certificate-identity-Regex fixiert die Signer-Identität. Weichen Sie sie nicht auf: Jedes Release-Archiv, das von einer anderen Identität signiert wurde, sollte umgehend abgelehnt werden.

### Via `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

Das Binary ist voll statisch (`CGO_ENABLED=0`) und bettet `modernc.org/sqlite` ein, weshalb keine libc- oder CGo-Runtime-Abhängigkeit eingeführt wird. `go.sum`-Pins werden durch die Checksum-Datenbank des Go-Modul-Proxys erzwungen.

## Windows

Windows-Binaries werden im gleichen Release-Archiv-Layout veröffentlicht:

```powershell
$Version = "<pin-a-tag>"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_windows_amd64.zip" -OutFile "rousseau.zip"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_checksums.txt" -OutFile "checksums.txt"

# SHA-256 verifizieren (cosign-Verifikation ist Linux/macOS-freundlich; auf Windows
# ist reine Checksum-Verifikation nutzbar, aber schwächer als das vollständige Rezept).
Get-FileHash rousseau.zip -Algorithm SHA256
Expand-Archive rousseau.zip -DestinationPath .
```

Windows ist ein First-Class-Build-Ziel, aber untertestet – jeder Chat-Transport funktioniert, jedoch setzt die Referenz-Bereitstellung (Podman + Quadlet) Linux voraus. Melden Sie Windows-spezifische Probleme, damit sie in CI erkannt werden.

## Aus Quellcode

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # erzeugt ./bin/rousseau
./bin/rousseau version
```

`make check` führt exakt das CI-Gate aus: `go vet`, `golangci-lint` v2 (18 Linter), `go test -race -count=1 -covermode=atomic ./...` und `govulncheck`.

Der dedizierte `reproducible-build`-CI-Job verifiziert bitidentische Ausgabe aus einem frischen Checkout auf `ubuntu-latest`, weshalb ein lokales `make build` mit derselben Go-Toolchain ein Binary erzeugt, dessen SHA-256 mit dem des getaggten Release übereinstimmt.

## Podman / Docker

```sh
# Lokal aus dem getaggten Source bauen.
podman build -t rousseau-agent:local -f docker/Dockerfile .

# Vorgebautes Image pullen (sobald veröffentlicht).
podman pull ghcr.io/sebastienrousseau/rousseau-agent:<tag>
```

Docker funktioniert identisch: Ersetzen Sie `podman` durch `docker`. Die Referenz-Bereitstellung ([Bereitstellung](/de/deployment/)) verwendet **rootless Podman** mit einer systemd-Quadlet-Unit, weil Quadlet deklarative Härtung (`ReadOnly=true`, `DropCapability=all`, `NoNewPrivileges=true`, seccomp-Filter, `keep-id`-User-Namespace-Mapping) bereitstellt, die einfaches Docker nicht bietet.

Das Runtime-Image ist ~550 MB gross, als Multi-Stage-Build aus einem `golang:1.26-alpine`-Builder gebaut, der in eine `node:22-alpine`-Runtime einspeist. Der Node-Layer existiert nur, damit der optionale `claude`-CLI-Subprozess ein Zuhause hat; der Daemon selbst hat keine Interpreter-Abhängigkeit.

## Ein signiertes Release verifizieren

Der Befehl `cosign verify-blob` führt drei Prüfungen gleichzeitig gegen Sigstores öffentliches Transparenz-Log durch:

1. Das in der Signatur eingebettete Zertifikat wurde für die GitHub-Actions-OIDC-Identität ausgestellt, die zur Regex passt.
2. Die Signatur über die Checksum-Datei ist gültig.
3. Das Zertifikat wurde vom Transparenz-Log bezeugt.

`sha256sum -c` bestätigt anschliessend, dass jedes Artefakt in der Checksum-Datei übereinstimmt. Dies ist die tragende Lieferketten-Prüfung – überspringen Sie sie nicht.

## Fehlerbehebung

### `go: module github.com/sebastienrousseau/rousseau-agent/cmd/rousseau: no matching versions`

Ihre `go`-Toolchain ist älter als 1.26. `go install` lehnt Module ab, deren `go`-Direktive über der Toolchain-Version liegt. Aktualisieren Sie Go oder nutzen Sie das signierte Release-Archiv.

### `sha256sum: WARNING: X computed checksums did NOT match`

Das Archiv wurde beim Download beschädigt oder (schlimmer) manipuliert. Erneut herunterladen und das Rezept von vorn ausführen – `cosign verify-blob` sollte Manipulation abgefangen haben, aber vertrauen Sie stets dem SHA-256-Ergebnis über jeder Annahme.

### `cosign: no matching signatures`

Sie haben `cosign`, aber die `--certificate-identity-regexp` stimmt nicht mit dem Signer überein. Für rousseau nutzen Sie `sebastienrousseau/rousseau-agent`. Wenn es weiterhin scheitert, führen Sie `cosign initialize` aus, um Sigstores Trust-Root aufzufrischen – die Root rotiert in langsamem Rhythmus.

### `rousseau version` gibt `dev / none / unknown` aus

Sie haben per `go install` installiert, und die `-ldflags`-Versionsstempel in `internal/cli/root.go` wurden nicht gefüllt. Nur kosmetisch, aber das signierte Release-Archiv ist die Lösung.

### macOS-Gatekeeper weigert sich, das Binary zu öffnen

Rechtsklick auf das Binary im Finder, <em>Öffnen</em> wählen, dann im Dialog erneut <em>Öffnen</em>. Alternativ entfernt `xattr -d com.apple.quarantine ./rousseau` das Quarantäne-Bit. Das signierte Release ist nicht notarisiert – die cosign-Verifikation ist die äquivalente Lieferketten-Prüfung.

## Verwandte Seiten

- [Getting Started: Plattform-Unterstützung](/de/getting-started/platform-support/) – Betriebssystem-, Architektur- und Provider-Auth-Matrix.
- [Getting Started: Erster Transport](/de/getting-started/first-transport/) – WhatsApp End-to-End einrichten.
- [Getting Started: Aktualisieren](/de/getting-started/updating/) – wie man zwischen Versionen sicher wechselt.
- [Bereitstellung](/de/deployment/) – die rootless Podman + Quadlet-Referenz-Bereitstellung.
- [Sicherheit](/de/security/) – Vertrauensgrenzen und Lieferketten-Härtung.

## Weiterführende Lektüre

- `README.md` – Positionierung auf Repository-Ebene und Fähigkeits-Matrix.
- `SECURITY.md` – Schwachstellen-Offenlegung und Lieferketten-Kontrollen.
- `Makefile` – das exakte CI-Gate, das lokal durch `make check` reproduziert wird.
- `docker/Dockerfile` – Multi-Stage-Build (`golang:1.26-alpine` &rarr; `node:22-alpine`).
