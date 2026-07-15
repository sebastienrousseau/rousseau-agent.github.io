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
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "en-GB"
locale: "en_GB"
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
permalink: "https://docs.rousseau-agent.dev/getting-started/installation/"
subtitle: "Every supported install method with the verification recipe."
tags: "install, macos, linux, windows, cosign, docker"
title: "Installation"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "install, macos, linux, windows, homebrew, cosign, sha256, podman, docker, go install"
news_language: "en"
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
item_description: RSS feed for rousseau-agent
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
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>Every supported install method for rousseau, per-OS commands, the cosign / SHA-256 / SLSA-3 verification recipe, and the failure modes that catch first-time installs. Skim the table below to pick a method, then jump to your OS.</p></aside>

## Picking an install method

| Method | When to use it | Verifiable |
|---|---|---|
| Signed release archive | Production, air-gapped, any regulated environment. | Yes — cosign + SHA-256 checksums + SLSA-3 provenance. |
| `go install` | Individual developers who trust the Go module proxy checksum database. | Partial — `go.sum` pin via `pkg.go.dev`. |
| From source (`make build`) | Contributors and reviewers who want to run the full CI gate locally. | Yes — reproducible-build job in CI confirms bit-identical output. |
| Container image | Deployments alongside other systemd services or in Kubernetes. | Yes — image is built from the tagged source, provenance is attached. |
| Homebrew (planned) | macOS convenience. | Planned; not yet shipped. |

<aside class="admonition" data-type="caution"><span class="admonition-title">Skip verification at your peril</span><p>The signed-release path is the only method that gives you a chain from the source commit through GitHub Actions OIDC to the archive on disk. If you would not run a random binary from the internet, do not skip <code>cosign verify-blob</code> + <code>sha256sum -c</code>. Both commands are shown per-OS below.</p></aside>

## Install by OS

<div class="tabs" data-tabs="install-os">
  <div class="tab-list" role="tablist" aria-label="Operating system">
    <button role="tab" aria-selected="true">macOS</button>
    <button role="tab" aria-selected="false">Linux</button>
    <button role="tab" aria-selected="false">Windows</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Signed release (recommended).** Works on Apple Silicon and Intel — swap `arm64` for `amd64` on Intel Macs.

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

**`go install`.** Fastest path if you already have Go 1.26+:

```sh
brew install go@1.26        # or from https://go.dev/dl
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

The binary embeds `modernc.org/sqlite` (see `internal/state/sqlite/store.go`), so there is no libc or CGo dependency and no Xcode Command Line Tools requirement.

**Homebrew.** The Homebrew formula is on the roadmap. Until it ships, use the release-archive path above.

<aside class="admonition" data-type="note"><span class="admonition-title">Gatekeeper</span><p>The signed archive is unsigned by Apple's notarisation service (rousseau does not ship an Apple Developer ID). The first launch may show a Gatekeeper prompt; approve it under <em>System Settings &gt; Privacy &amp; Security</em>. Verifying the cosign signature is the equivalent supply-chain check.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Signed release (recommended).** `aarch64` builds are published under `linux_arm64`:

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

**Distro packages.** No first-party packages yet — track the release archives above.

**Rootless Podman (production).** See [Deployment](/deployment/) for the Quadlet reference. `pasta` networking requires Podman 5.x+; Debian 12 and Ubuntu 22.04 ship 4.x and need a `slirp4netns` fallback (roadmap).

<aside class="admonition" data-type="warning"><span class="admonition-title">Distribution Go</span><p>Debian/Ubuntu often ship a Go older than 1.26. If <code>go version</code> reports &lt; 1.26, install directly from <a href="https://go.dev/dl">go.dev/dl</a> or use the signed release archive — <code>go install</code> against an old toolchain will fail on module features rousseau uses.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau is a first-class Windows build target; every transport works on Windows except `signal` (requires the `signal-cli` JVM subprocess) and `imessage` (requires macOS). The reference Podman + Quadlet deployment is Linux-only — use WSL 2 or a Linux VM for the container path.

**Signed release.** PowerShell:

```powershell
$Version = "<pin-a-tag>"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_windows_amd64.zip" -OutFile "rousseau.zip"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_checksums.txt" -OutFile "checksums.txt"
Get-FileHash rousseau.zip -Algorithm SHA256
Expand-Archive rousseau.zip -DestinationPath .
```

Compare `Get-FileHash` output against `checksums.txt` by eye, or pipe through PowerShell to script the check.

**`go install`.** Works out of the box on Windows once Go is on the PATH:

```powershell
winget install GoLang.Go
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

<aside class="admonition" data-type="warning"><span class="admonition-title">cosign on Windows</span><p>The <code>cosign</code> CLI runs on Windows but is a large download and needs its own dependency chain. For low-friction verification, run <code>cosign verify-blob</code> once from WSL 2 or a Linux VM against the same checksum file, then trust the SHA-256 recipe on Windows.</p></aside>

<aside class="admonition" data-type="warning"><span class="admonition-title">Home directory paths</span><p>Rousseau writes state to <code>%APPDATA%\rousseau\sessions.db</code> on Windows (via <code>os.UserConfigDir()</code> in <code>internal/config/config.go</code>). Docs sometimes cite the Unix path <code>~/.local/share/rousseau/</code> — the same file lives at the platform-appropriate location.</p></aside>

  </div>
</div>

## Verifying a signed release

The `cosign verify-blob` command performs three checks at once against Sigstore's public transparency log:

1. The certificate embedded in the signature was issued to the GitHub Actions OIDC identity matching the regex.
2. The signature over the checksum file is valid.
3. The certificate was witnessed by the transparency log.

`sha256sum -c` then confirms every artefact in the checksum file matches. This is the load-bearing supply-chain check — do not skip it.

### Verifying the SBOM

Every release ships `rousseau_<version>_sbom.cdx.json` (CycloneDX 1.5). Inspect with `cyclonedx-cli`:

```sh
cyclonedx-cli tree --input-file rousseau_<version>_sbom.cdx.json
cyclonedx-cli validate --input-file rousseau_<version>_sbom.cdx.json
```

### Verifying SLSA-3 provenance

```sh
slsa-verifier verify-artifact \
  --provenance-path rousseau_<version>_provenance.intoto.jsonl \
  --source-uri github.com/sebastienrousseau/rousseau-agent \
  --source-tag <version> \
  rousseau_<version>_linux_amd64.tar.gz
```

Any deviation between the artefact and what CI attests to having built causes `slsa-verifier` to exit non-zero.

## macOS

### Signed release (recommended)

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

Replace `arm64` with `amd64` on Intel Macs.

### Homebrew (planned)

The Homebrew formula is on the roadmap. Until it ships, the release-archive path above is the recommended macOS install.

## Linux

### Signed release (recommended)

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

`aarch64` builds are published under `linux_arm64`.

The certificate-identity regex pins the signer identity. Do not weaken it: any release archive signed by a different identity should be rejected outright.

### Via `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

The binary is fully static (`CGO_ENABLED=0`) and embeds `modernc.org/sqlite`, so no libc or CGo runtime dependency is introduced. `go.sum` pins are enforced by the Go module proxy checksum database.

## Windows

Windows binaries are published in the same release archive layout:

```powershell
$Version = "<pin-a-tag>"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_windows_amd64.zip" -OutFile "rousseau.zip"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_checksums.txt" -OutFile "checksums.txt"

# Verify SHA-256 (cosign verification is Linux/macOS-friendly; on Windows,
# checksum verification alone is usable but weaker than the full recipe).
Get-FileHash rousseau.zip -Algorithm SHA256
Expand-Archive rousseau.zip -DestinationPath .
```

Windows is a first-class build target but is under-tested — every chat transport works, but the reference deployment (Podman + Quadlet) assumes Linux. Report Windows-specific issues so they can be caught in CI.

## From source

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` runs the exact CI gate: `go vet`, `golangci-lint` v2 (18 linters), `go test -race -count=1 -covermode=atomic ./...`, and `govulncheck`.

The dedicated `reproducible-build` CI job verifies bit-identical output from a fresh checkout on `ubuntu-latest`, so a local `make build` on the same Go toolchain will produce a binary whose SHA-256 matches the tagged release.

## Podman / Docker

```sh
# Build locally from the tagged source.
podman build -t rousseau-agent:local -f docker/Dockerfile .

# Pull the pre-built image (once published).
podman pull ghcr.io/sebastienrousseau/rousseau-agent:<tag>
```

Docker works identically: swap `podman` for `docker`. The reference deployment ([Deployment](/deployment/)) uses **rootless Podman** with a systemd Quadlet unit because Quadlet provides declarative hardening (`ReadOnly=true`, `DropCapability=all`, `NoNewPrivileges=true`, seccomp filter, `keep-id` user-namespace mapping) that plain Docker does not.

The runtime image is ~550 MB, built as a multi-stage `golang:1.26-alpine` builder feeding a `node:22-alpine` runtime. The Node layer exists only so the optional `claude` CLI subprocess has a home; the daemon itself has no interpreter dependency.

## Verifying a signed release

The `cosign verify-blob` command performs three checks at once against Sigstore's public transparency log:

1. The certificate embedded in the signature was issued to the GitHub Actions OIDC identity matching the regex.
2. The signature over the checksum file is valid.
3. The certificate was witnessed by the transparency log.

`sha256sum -c` then confirms every artefact in the checksum file matches. This is the load-bearing supply-chain check — do not skip it.

## Troubleshooting

### `go: module github.com/sebastienrousseau/rousseau-agent/cmd/rousseau: no matching versions`

Your `go` toolchain is older than 1.26. `go install` refuses modules with a `go` directive above the toolchain version. Upgrade Go, or use the signed-release archive.

### `sha256sum: WARNING: X computed checksums did NOT match`

The archive was corrupted mid-download, or (worse) tampered with. Re-download and re-run the recipe from the top — `cosign verify-blob` should have caught tampering, but always trust the SHA-256 outcome over any assumption.

### `cosign: no matching signatures`

You have `cosign` but the `--certificate-identity-regexp` does not match the signer. For rousseau, use `sebastienrousseau/rousseau-agent`. If it still fails, run `cosign initialize` to refresh Sigstore's trust root — the root rotates on a slow cadence.

### `rousseau version` prints `dev / none / unknown`

You installed via `go install` and the `-ldflags` version stamps in `internal/cli/root.go` were not populated. Cosmetic only, but the signed-release archive is the fix.

### macOS Gatekeeper refuses to open the binary

Right-click the binary in Finder, choose <em>Open</em>, then <em>Open</em> again in the dialog. Alternatively `xattr -d com.apple.quarantine ./rousseau` removes the quarantine bit. The signed release is not notarised — cosign verification is the equivalent supply-chain check.

## Related pages

- [Getting Started: Platform Support](/getting-started/platform-support/) — OS, architecture, and provider auth matrix.
- [Getting Started: First Transport](/getting-started/first-transport/) — wire WhatsApp end-to-end.
- [Getting Started: Updating](/getting-started/updating/) — how to move between versions safely.
- [Deployment](/deployment/) — the rootless Podman + Quadlet reference deployment.
- [Security](/security/) — trust boundaries and supply-chain hardening.

## Further reading

- `README.md` — repository-level positioning and capability matrix.
- `SECURITY.md` — vulnerability disclosure and supply-chain controls.
- `Makefile` — the exact CI gate reproduced locally by `make check`.
- `docker/Dockerfile` — multi-stage build (`golang:1.26-alpine` &rarr; `node:22-alpine`).
