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
hreflang: "pt-BR"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "pt-BR"
locale: "pt_BR"
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
permalink: "https://docs.rousseau-agent.dev/pt-BR/getting-started/installation/"
subtitle: "Every supported install method with the verification recipe."
tags: "install, macos, linux, windows, cosign, docker"
title: "Instalação"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "install, macos, linux, windows, homebrew, cosign, sha256, podman, docker, go install"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Instalação"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 21
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/installation/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/installation/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Instalação"
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
twitter_title: "Instalação"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Obrigado a cada operador que executa seu próprio agente de codificação."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>Cada método de instalação suportado do rousseau, comandos por OS, a receita de verificação cosign / SHA-256 / SLSA-3 e os modos de falha que pegam instalações de primeira vez. Passe os olhos pela tabela abaixo para escolher um método, depois vá para seu OS.</p></aside>

## Escolhendo um método de instalação

| Método | Quando usar | Verificável |
|---|---|---|
| Archive de release assinada | Produção, air-gapped, qualquer ambiente regulado. | Sim — cosign + checksums SHA-256 + proveniência SLSA-3. |
| `go install` | Desenvolvedores individuais que confiam no banco de checksums do proxy de módulos Go. | Parcial — fixação via `go.sum` no `pkg.go.dev`. |
| Do código-fonte (`make build`) | Contribuidores e revisores que querem executar o gate completo do CI localmente. | Sim — job de reproducible-build no CI confirma saída bit-idêntica. |
| Imagem de contêiner | Implantações junto a outros serviços systemd ou em Kubernetes. | Sim — a imagem é construída a partir do código-fonte com tag, a proveniência é anexada. |
| Homebrew (planejado) | Conveniência no macOS. | Planejado; ainda não entregue. |

<aside class="admonition" data-type="caution"><span class="admonition-title">Pule a verificação por sua conta e risco</span><p>O caminho de release assinada é o único método que lhe dá uma cadeia do commit-fonte, passando pelo OIDC do GitHub Actions, até o arquivo em disco. Se você não executaria um binário aleatório da internet, não pule <code>cosign verify-blob</code> + <code>sha256sum -c</code>. Ambos os comandos são mostrados por OS abaixo.</p></aside>

## Instalação por OS

<div class="tabs" data-tabs="install-os">
  <div class="tab-list" role="tablist" aria-label="Operating system">
    <button role="tab" aria-selected="true">macOS</button>
    <button role="tab" aria-selected="false">Linux</button>
    <button role="tab" aria-selected="false">Windows</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Release assinada (recomendada).** Funciona em Apple Silicon e Intel — troque `arm64` por `amd64` em Macs Intel.

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

**`go install`.** Caminho mais rápido se você já tem Go 1.26+:

```sh
brew install go@1.26        # or from https://go.dev/dl
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

O binário incorpora `modernc.org/sqlite` (veja `internal/state/sqlite/store.go`), então não há dependência de libc ou CGo e nenhuma exigência de Xcode Command Line Tools.

**Homebrew.** A fórmula Homebrew está no roadmap. Até ser lançada, use o caminho de archive de release acima.

<aside class="admonition" data-type="note"><span class="admonition-title">Gatekeeper</span><p>O archive assinado não é assinado pelo serviço de notarização da Apple (o rousseau não entrega um Apple Developer ID). O primeiro lançamento pode mostrar um prompt do Gatekeeper; aprove em <em>System Settings &gt; Privacy &amp; Security</em>. Verificar a assinatura cosign é a checagem equivalente da cadeia de suprimentos.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Release assinada (recomendada).** Builds `aarch64` são publicados sob `linux_arm64`:

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

**Pacotes de distro.** Ainda não há pacotes first-party — acompanhe os archives de release acima.

**Podman rootless (produção).** Veja [Implantação](/pt-BR/deployment/) para a referência do Quadlet. A rede `pasta` requer Podman 5.x+; Debian 12 e Ubuntu 22.04 entregam 4.x e precisam de um fallback `slirp4netns` (roadmap).

<aside class="admonition" data-type="warning"><span class="admonition-title">Go de distribuição</span><p>Debian/Ubuntu frequentemente entregam um Go mais antigo que 1.26. Se <code>go version</code> reportar &lt; 1.26, instale diretamente de <a href="https://go.dev/dl">go.dev/dl</a> ou use o archive de release assinada — <code>go install</code> contra um toolchain antigo vai falhar em recursos de módulo que o rousseau usa.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

O rousseau é um alvo de build de primeira classe do Windows; cada transporte funciona no Windows exceto `signal` (requer o subprocesso JVM do `signal-cli`) e `imessage` (requer macOS). A implantação de referência Podman + Quadlet é somente Linux — use WSL 2 ou uma VM Linux para o caminho de contêiner.

**Release assinada.** PowerShell:

```powershell
$Version = "<pin-a-tag>"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_windows_amd64.zip" -OutFile "rousseau.zip"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_checksums.txt" -OutFile "checksums.txt"
Get-FileHash rousseau.zip -Algorithm SHA256
Expand-Archive rousseau.zip -DestinationPath .
```

Compare a saída de `Get-FileHash` contra `checksums.txt` a olho, ou canalize pelo PowerShell para automatizar a verificação.

**`go install`.** Funciona de saída no Windows assim que o Go está no PATH:

```powershell
winget install GoLang.Go
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

<aside class="admonition" data-type="warning"><span class="admonition-title">cosign no Windows</span><p>O CLI <code>cosign</code> roda no Windows, mas é um download grande e precisa de sua própria cadeia de dependências. Para verificação com baixa fricção, execute <code>cosign verify-blob</code> uma vez do WSL 2 ou de uma VM Linux contra o mesmo arquivo de checksum, depois confie na receita SHA-256 no Windows.</p></aside>

<aside class="admonition" data-type="warning"><span class="admonition-title">Caminhos do diretório home</span><p>O rousseau grava estado em <code>%APPDATA%\rousseau\sessions.db</code> no Windows (via <code>os.UserConfigDir()</code> em <code>internal/config/config.go</code>). A documentação às vezes cita o caminho Unix <code>~/.local/share/rousseau/</code> — o mesmo arquivo vive na localização apropriada para a plataforma.</p></aside>

  </div>
</div>

## Verificando uma release assinada

O comando `cosign verify-blob` realiza três checagens de uma só vez contra o log de transparência público do Sigstore:

1. O certificado embutido na assinatura foi emitido para a identidade OIDC do GitHub Actions que casa com a regex.
2. A assinatura sobre o arquivo de checksum é válida.
3. O certificado foi testemunhado pelo log de transparência.

`sha256sum -c` então confirma que cada artefato no arquivo de checksum corresponde. Esta é a checagem crítica da cadeia de suprimentos — não pule.

### Verificando o SBOM

Cada release entrega `rousseau_<version>_sbom.cdx.json` (CycloneDX 1.5). Inspecione com `cyclonedx-cli`:

```sh
cyclonedx-cli tree --input-file rousseau_<version>_sbom.cdx.json
cyclonedx-cli validate --input-file rousseau_<version>_sbom.cdx.json
```

### Verificando a proveniência SLSA-3

```sh
slsa-verifier verify-artifact \
  --provenance-path rousseau_<version>_provenance.intoto.jsonl \
  --source-uri github.com/sebastienrousseau/rousseau-agent \
  --source-tag <version> \
  rousseau_<version>_linux_amd64.tar.gz
```

Qualquer desvio entre o artefato e o que o CI atesta ter construído faz o `slsa-verifier` sair com código diferente de zero.

## macOS

### Release assinada (recomendada)

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

Substitua `arm64` por `amd64` em Macs Intel.

### Homebrew (planejado)

A fórmula Homebrew está no roadmap. Até ser lançada, o caminho do archive de release acima é a instalação recomendada no macOS.

## Linux

### Release assinada (recomendada)

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

Builds `aarch64` são publicados sob `linux_arm64`.

A regex de certificate-identity fixa a identidade do assinante. Não a enfraqueça: qualquer archive de release assinado por uma identidade diferente deve ser rejeitado sumariamente.

### Via `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

O binário é totalmente estático (`CGO_ENABLED=0`) e incorpora `modernc.org/sqlite`, então nenhuma dependência de libc ou CGo em runtime é introduzida. As fixações do `go.sum` são impostas pelo banco de checksums do proxy de módulos Go.

## Windows

Binários Windows são publicados no mesmo layout de archive de release:

```powershell
$Version = "<pin-a-tag>"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_windows_amd64.zip" -OutFile "rousseau.zip"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_checksums.txt" -OutFile "checksums.txt"

# Verify SHA-256 (cosign verification is Linux/macOS-friendly; on Windows,
# checksum verification alone is usable but weaker than the full recipe).
Get-FileHash rousseau.zip -Algorithm SHA256
Expand-Archive rousseau.zip -DestinationPath .
```

O Windows é um alvo de build de primeira classe, mas é subtestado — cada transporte de chat funciona, mas a implantação de referência (Podman + Quadlet) assume Linux. Reporte problemas específicos do Windows para que possam ser detectados no CI.

## A partir do código-fonte

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` executa o gate exato do CI: `go vet`, `golangci-lint` v2 (18 linters), `go test -race -count=1 -covermode=atomic ./...` e `govulncheck`.

O job dedicado `reproducible-build` do CI verifica saída bit-idêntica a partir de um checkout novo em `ubuntu-latest`, então um `make build` local no mesmo toolchain Go produzirá um binário cujo SHA-256 casa com a release taggada.

## Podman / Docker

```sh
# Build locally from the tagged source.
podman build -t rousseau-agent:local -f docker/Dockerfile .

# Pull the pre-built image (once published).
podman pull ghcr.io/sebastienrousseau/rousseau-agent:<tag>
```

O Docker funciona de forma idêntica: troque `podman` por `docker`. A implantação de referência ([Implantação](/pt-BR/deployment/)) usa **Podman rootless** com uma unidade Quadlet do systemd porque o Quadlet oferece hardening declarativo (`ReadOnly=true`, `DropCapability=all`, `NoNewPrivileges=true`, filtro seccomp, mapeamento de user-namespace `keep-id`) que o Docker puro não oferece.

A imagem de runtime tem ~550 MB, construída como um builder multi-stage `golang:1.26-alpine` alimentando um runtime `node:22-alpine`. A camada Node existe apenas para que o subprocesso opcional do CLI `claude` tenha um lar; o próprio daemon não tem dependência de interpretador.

## Verificando uma release assinada

O comando `cosign verify-blob` realiza três checagens de uma só vez contra o log de transparência público do Sigstore:

1. O certificado embutido na assinatura foi emitido para a identidade OIDC do GitHub Actions que casa com a regex.
2. A assinatura sobre o arquivo de checksum é válida.
3. O certificado foi testemunhado pelo log de transparência.

`sha256sum -c` então confirma que cada artefato no arquivo de checksum corresponde. Esta é a checagem crítica da cadeia de suprimentos — não pule.

## Solução de problemas

### `go: module github.com/sebastienrousseau/rousseau-agent/cmd/rousseau: no matching versions`

Seu toolchain `go` é mais antigo que 1.26. `go install` recusa módulos com uma diretiva `go` acima da versão do toolchain. Atualize o Go ou use o archive de release assinada.

### `sha256sum: WARNING: X computed checksums did NOT match`

O archive foi corrompido durante o download, ou (pior) adulterado. Baixe novamente e execute a receita a partir do topo — o `cosign verify-blob` deveria ter pego a adulteração, mas sempre confie no resultado do SHA-256 sobre qualquer suposição.

### `cosign: no matching signatures`

Você tem `cosign` mas a `--certificate-identity-regexp` não casa com o assinante. Para rousseau, use `sebastienrousseau/rousseau-agent`. Se ainda falhar, execute `cosign initialize` para atualizar o trust root do Sigstore — o root rotaciona em uma cadência lenta.

### `rousseau version` imprime `dev / none / unknown`

Você instalou via `go install` e os stamps de versão `-ldflags` em `internal/cli/root.go` não foram populados. Apenas cosmético, mas o archive de release assinada é a correção.

### O Gatekeeper do macOS recusa a abrir o binário

Clique com o botão direito no binário no Finder, escolha <em>Abrir</em>, depois <em>Abrir</em> novamente no diálogo. Alternativamente, `xattr -d com.apple.quarantine ./rousseau` remove o bit de quarentena. A release assinada não é notarizada — a verificação cosign é a checagem equivalente da cadeia de suprimentos.

## Páginas relacionadas

- [Começando: Suporte a plataformas](/pt-BR/getting-started/platform-support/) — matriz de OS, arquitetura e autenticação de provider.
- [Começando: Seu primeiro transporte](/pt-BR/getting-started/first-transport/) — configure o WhatsApp de ponta a ponta.
- [Começando: Atualização](/pt-BR/getting-started/updating/) — como mover entre versões com segurança.
- [Implantação](/pt-BR/deployment/) — a implantação de referência Podman rootless + Quadlet.
- [Segurança](/pt-BR/security/) — limites de confiança e hardening da cadeia de suprimentos.

## Leitura complementar

- `README.md` — posicionamento e matriz de capacidades no nível do repositório.
- `SECURITY.md` — divulgação de vulnerabilidades e controles da cadeia de suprimentos.
- `Makefile` — o gate exato do CI reproduzido localmente por `make check`.
- `docker/Dockerfile` — build multi-stage (`golang:1.26-alpine` &rarr; `node:22-alpine`).
