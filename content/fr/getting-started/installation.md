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
hreflang: "fr"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "fr"
locale: "fr_FR"
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
permalink: "https://docs.rousseau-agent.dev/fr/getting-started/installation/"
subtitle: "Every supported install method with the verification recipe."
tags: "install, macos, linux, windows, cosign, docker"
title: "Installation"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "install, macos, linux, windows, homebrew, cosign, sha256, podman, docker, go install"
news_language: "fr"
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
item_description: Flux RSS de rousseau-agent
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
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>Chaque méthode d'installation supportée pour rousseau, les commandes par OS, la recette de vérification cosign / SHA-256 / SLSA-3 et les modes d'échec typiques des premières installations. Parcourez le tableau ci-dessous pour choisir une méthode, puis passez à votre OS.</p></aside>

## Choisir une méthode d'installation

| Méthode | Quand l'utiliser | Vérifiable |
|---|---|---|
| Archive de release signée | Production, air-gap, tout environnement régulé. | Oui — cosign + checksums SHA-256 + provenance SLSA-3. |
| `go install` | Développeurs individuels qui font confiance à la base de données de checksums du proxy de modules Go. | Partielle — pinning via `go.sum` sur `pkg.go.dev`. |
| Depuis les sources (`make build`) | Contributeurs et relecteurs qui veulent rejouer localement la porte CI complète. | Oui — le job de build reproductible en CI confirme une sortie bit-à-bit identique. |
| Image conteneur | Déploiements aux côtés d'autres services systemd ou sous Kubernetes. | Oui — l'image est construite depuis les sources taggées, la provenance est attachée. |
| Homebrew (prévu) | Confort macOS. | Prévu ; pas encore livré. |

<aside class="admonition" data-type="caution"><span class="admonition-title">Sauter la vérification à vos risques et périls</span><p>La voie de la release signée est la seule qui vous donne une chaîne allant du commit source jusqu'à l'archive sur disque via l'OIDC de GitHub Actions. Si vous n'exécuteriez pas un binaire aléatoire d'internet, ne sautez pas <code>cosign verify-blob</code> + <code>sha256sum -c</code>. Les deux commandes sont indiquées par OS ci-dessous.</p></aside>

## Installer par OS

<div class="tabs" data-tabs="install-os">
  <div class="tab-list" role="tablist" aria-label="Operating system">
    <button role="tab" aria-selected="true">macOS</button>
    <button role="tab" aria-selected="false">Linux</button>
    <button role="tab" aria-selected="false">Windows</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Release signée (recommandée).** Fonctionne sur Apple Silicon et Intel — remplacez `arm64` par `amd64` sur les Mac Intel.

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

**`go install`.** Le plus rapide si vous avez déjà Go 1.26+ :

```sh
brew install go@1.26        # or from https://go.dev/dl
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

Le binaire embarque `modernc.org/sqlite` (voir `internal/state/sqlite/store.go`), sans dépendance libc ni CGo, et sans exigence des Xcode Command Line Tools.

**Homebrew.** La formule Homebrew figure sur la roadmap. En attendant, utilisez la voie de la release-archive ci-dessus.

<aside class="admonition" data-type="note"><span class="admonition-title">Gatekeeper</span><p>L'archive signée n'est pas notarisée par Apple (rousseau ne dispose pas d'un Apple Developer ID). Le premier lancement peut afficher un prompt Gatekeeper ; approuvez-le dans <em>Réglages Système &gt; Confidentialité &amp; Sécurité</em>. La vérification de la signature cosign constitue le contrôle supply-chain équivalent.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Release signée (recommandée).** Les builds `aarch64` sont publiés sous `linux_arm64` :

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

**Paquets distros.** Pas de paquets first-party pour l'instant — suivez les archives de release ci-dessus.

**Podman rootless (production).** Voir [Déploiement](/fr/deployment/) pour la référence Quadlet. Le réseau `pasta` requiert Podman 5.x+ ; Debian 12 et Ubuntu 22.04 livrent 4.x et nécessitent un repli `slirp4netns` (roadmap).

<aside class="admonition" data-type="warning"><span class="admonition-title">Go de la distribution</span><p>Debian/Ubuntu livrent souvent un Go plus ancien que 1.26. Si <code>go version</code> rapporte &lt; 1.26, installez directement depuis <a href="https://go.dev/dl">go.dev/dl</a> ou utilisez l'archive de release signée — <code>go install</code> contre une toolchain ancienne échouera sur des fonctionnalités de module utilisées par rousseau.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau est une cible de build Windows de premier plan ; chaque transport fonctionne sous Windows sauf `signal` (nécessite le sous-processus JVM `signal-cli`) et `imessage` (nécessite macOS). Le déploiement de référence Podman + Quadlet est réservé à Linux — utilisez WSL 2 ou une VM Linux pour la voie conteneur.

**Release signée.** PowerShell :

```powershell
$Version = "<pin-a-tag>"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_windows_amd64.zip" -OutFile "rousseau.zip"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_checksums.txt" -OutFile "checksums.txt"
Get-FileHash rousseau.zip -Algorithm SHA256
Expand-Archive rousseau.zip -DestinationPath .
```

Comparez la sortie de `Get-FileHash` avec `checksums.txt` à l'œil, ou scriptez le contrôle via PowerShell.

**`go install`.** Fonctionne d'emblée sous Windows dès que Go est sur le PATH :

```powershell
winget install GoLang.Go
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

<aside class="admonition" data-type="warning"><span class="admonition-title">cosign sous Windows</span><p>La CLI <code>cosign</code> tourne sous Windows mais représente un gros téléchargement avec sa propre chaîne de dépendances. Pour une vérification sans friction, exécutez <code>cosign verify-blob</code> une fois depuis WSL 2 ou une VM Linux contre le même fichier de checksums, puis fiez-vous à la recette SHA-256 sous Windows.</p></aside>

<aside class="admonition" data-type="warning"><span class="admonition-title">Chemins du répertoire personnel</span><p>Rousseau écrit son état dans <code>%APPDATA%\rousseau\sessions.db</code> sous Windows (via <code>os.UserConfigDir()</code> dans <code>internal/config/config.go</code>). La documentation cite parfois le chemin Unix <code>~/.local/share/rousseau/</code> — le même fichier vit à l'emplacement adapté à la plateforme.</p></aside>

  </div>
</div>

## Vérifier une release signée

La commande `cosign verify-blob` effectue trois contrôles simultanés contre le journal de transparence public de Sigstore :

1. Le certificat embarqué dans la signature a été émis pour l'identité OIDC GitHub Actions correspondant à la regex.
2. La signature sur le fichier de checksums est valide.
3. Le certificat a été enregistré par le journal de transparence.

`sha256sum -c` confirme ensuite que chaque artefact du fichier de checksums correspond. C'est le contrôle supply-chain porteur — ne le sautez pas.

### Vérifier le SBOM

Chaque release livre `rousseau_<version>_sbom.cdx.json` (CycloneDX 1.5). Inspectez avec `cyclonedx-cli` :

```sh
cyclonedx-cli tree --input-file rousseau_<version>_sbom.cdx.json
cyclonedx-cli validate --input-file rousseau_<version>_sbom.cdx.json
```

### Vérifier la provenance SLSA-3

```sh
slsa-verifier verify-artifact \
  --provenance-path rousseau_<version>_provenance.intoto.jsonl \
  --source-uri github.com/sebastienrousseau/rousseau-agent \
  --source-tag <version> \
  rousseau_<version>_linux_amd64.tar.gz
```

Toute divergence entre l'artefact et ce que la CI atteste avoir construit fait sortir `slsa-verifier` en non-zero.

## macOS

### Release signée (recommandée)

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

Remplacez `arm64` par `amd64` sur les Mac Intel.

### Homebrew (prévu)

La formule Homebrew figure sur la roadmap. En attendant, la voie de l'archive de release ci-dessus reste l'installation recommandée pour macOS.

## Linux

### Release signée (recommandée)

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

Les builds `aarch64` sont publiés sous `linux_arm64`.

La regex certificate-identity verrouille l'identité du signataire. Ne l'affaiblissez pas : toute archive de release signée par une autre identité doit être rejetée d'emblée.

### Via `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

Le binaire est totalement statique (`CGO_ENABLED=0`) et embarque `modernc.org/sqlite`, donc aucune dépendance libc ou CGo à l'exécution n'est introduite. Le pinning de `go.sum` est appliqué par la base de données de checksums du proxy de modules Go.

## Windows

Les binaires Windows sont publiés selon la même disposition d'archive :

```powershell
$Version = "<pin-a-tag>"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_windows_amd64.zip" -OutFile "rousseau.zip"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_checksums.txt" -OutFile "checksums.txt"

# Verify SHA-256 (cosign verification is Linux/macOS-friendly; on Windows,
# checksum verification alone is usable but weaker than the full recipe).
Get-FileHash rousseau.zip -Algorithm SHA256
Expand-Archive rousseau.zip -DestinationPath .
```

Windows est une cible de build de premier plan mais est sous-testée — chaque transport de chat fonctionne, mais le déploiement de référence (Podman + Quadlet) suppose Linux. Signalez les problèmes spécifiques à Windows pour qu'ils soient couverts en CI.

## Depuis les sources

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` exécute la porte CI exacte : `go vet`, `golangci-lint` v2 (18 linters), `go test -race -count=1 -covermode=atomic ./...` et `govulncheck`.

Le job CI dédié `reproducible-build` vérifie une sortie bit-à-bit identique depuis un checkout neuf sur `ubuntu-latest`, donc un `make build` local sur la même toolchain Go produit un binaire dont le SHA-256 correspond à la release taggée.

## Podman / Docker

```sh
# Build locally from the tagged source.
podman build -t rousseau-agent:local -f docker/Dockerfile .

# Pull the pre-built image (once published).
podman pull ghcr.io/sebastienrousseau/rousseau-agent:<tag>
```

Docker fonctionne à l'identique : remplacez `podman` par `docker`. Le déploiement de référence ([Déploiement](/fr/deployment/)) utilise **Podman rootless** avec une unité Quadlet systemd car Quadlet fournit un durcissement déclaratif (`ReadOnly=true`, `DropCapability=all`, `NoNewPrivileges=true`, filtre seccomp, mapping user-namespace `keep-id`) que Docker classique n'offre pas.

L'image de runtime pèse ~550 Mo, construite en multi-étape avec un builder `golang:1.26-alpine` alimentant un runtime `node:22-alpine`. La couche Node n'existe que pour héberger le sous-processus CLI `claude` optionnel ; le daemon lui-même n'a aucune dépendance à un interpréteur.

## Vérifier une release signée

La commande `cosign verify-blob` effectue trois contrôles simultanés contre le journal de transparence public de Sigstore :

1. Le certificat embarqué dans la signature a été émis pour l'identité OIDC GitHub Actions correspondant à la regex.
2. La signature sur le fichier de checksums est valide.
3. Le certificat a été enregistré par le journal de transparence.

`sha256sum -c` confirme ensuite que chaque artefact du fichier de checksums correspond. C'est le contrôle supply-chain porteur — ne le sautez pas.

## Dépannage

### `go: module github.com/sebastienrousseau/rousseau-agent/cmd/rousseau: no matching versions`

Votre toolchain `go` est plus ancienne que 1.26. `go install` refuse les modules dont la directive `go` dépasse la version de la toolchain. Mettez Go à jour, ou utilisez l'archive de release signée.

### `sha256sum: WARNING: X computed checksums did NOT match`

L'archive a été corrompue en cours de téléchargement, ou (pire) altérée. Re-téléchargez et rejouez la recette depuis le début — `cosign verify-blob` aurait dû détecter une altération, mais fiez-vous toujours au verdict SHA-256 plutôt qu'à des hypothèses.

### `cosign: no matching signatures`

Vous avez `cosign` mais `--certificate-identity-regexp` ne correspond pas au signataire. Pour rousseau, utilisez `sebastienrousseau/rousseau-agent`. Si cela échoue toujours, exécutez `cosign initialize` pour rafraîchir la racine de confiance Sigstore — la racine tourne lentement.

### `rousseau version` affiche `dev / none / unknown`

Vous avez installé via `go install` et les stamps de version `-ldflags` dans `internal/cli/root.go` n'ont pas été peuplés. Purement cosmétique, mais l'archive de release signée corrige le problème.

### Gatekeeper macOS refuse d'ouvrir le binaire

Clic-droit sur le binaire dans le Finder, choisir <em>Ouvrir</em>, puis <em>Ouvrir</em> à nouveau dans la boîte de dialogue. Sinon, `xattr -d com.apple.quarantine ./rousseau` retire le bit de quarantaine. La release signée n'est pas notarisée — la vérification cosign constitue le contrôle supply-chain équivalent.

## Pages liées

- [Prise en main : Support de plateforme](/fr/getting-started/platform-support/) — matrice OS, architecture et authentification fournisseurs.
- [Prise en main : Premier transport](/fr/getting-started/first-transport/) — câbler WhatsApp de bout en bout.
- [Prise en main : Mise à jour](/fr/getting-started/updating/) — comment passer d'une version à l'autre sans risque.
- [Déploiement](/fr/deployment/) — le déploiement de référence Podman rootless + Quadlet.
- [Sécurité](/fr/security/) — frontières de confiance et durcissement supply-chain.

## Pour aller plus loin

- `README.md` — positionnement au niveau dépôt et matrice de capacités.
- `SECURITY.md` — divulgation de vulnérabilités et contrôles supply-chain.
- `Makefile` — la porte CI exacte, rejouée localement par `make check`.
- `docker/Dockerfile` — build multi-étape (`golang:1.26-alpine` &rarr; `node:22-alpine`).
