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
hreflang: "zh-Hans"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "zh-Hans"
locale: "zh_CN"
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
permalink: "https://docs.rousseau-agent.dev/zh-Hans/getting-started/installation/"
subtitle: "Every supported install method with the verification recipe."
tags: "install, macos, linux, windows, cosign, docker"
title: "安装"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "install, macos, linux, windows, homebrew, cosign, sha256, podman, docker, go install"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "安装"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 21
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/getting-started/installation/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/installation/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "安装"
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
twitter_title: "安装"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "感谢每一位运行自有编码代理的运维者。"
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p>rousseau 支持的每一种安装方法、按操作系统的命令、cosign / SHA-256 / SLSA-3 的验证流程，以及首次安装容易踩的坑。请浏览下表选择一种方法，然后跳到你的操作系统。</p></aside>

## 选择安装方法

| 方法 | 何时使用 | 是否可验证 |
|---|---|---|
| 签名发布归档 | 生产环境、气隙、任何受监管环境。 | 是——cosign + SHA-256 校验和 + SLSA-3 溯源。 |
| `go install` | 信任 Go 模块代理校验和数据库的个人开发者。 | 部分——通过 `pkg.go.dev` 的 `go.sum` 固定。 |
| 从源码构建（`make build`） | 希望本地运行完整 CI 门槛的贡献者与审查者。 | 是——CI 的可复现构建任务确认位比特一致输出。 |
| 容器镜像 | 与其他 systemd 服务并列部署或在 Kubernetes 中部署。 | 是——镜像基于打标签的源码构建并附带溯源。 |
| Homebrew（计划中） | macOS 便利安装。 | 计划中；尚未发布。 |

<aside class="admonition" data-type="caution"><span class="admonition-title">跳过验证风险自负</span><p>签名发布路径是唯一能从源码提交经由 GitHub Actions OIDC 一直追溯到磁盘上归档的方法。如果你不会随便运行来自互联网的二进制，就不要跳过 <code>cosign verify-blob</code> + <code>sha256sum -c</code>。两个命令按操作系统在下方给出。</p></aside>

## 按操作系统安装

<div class="tabs" data-tabs="install-os">
  <div class="tab-list" role="tablist" aria-label="Operating system">
    <button role="tab" aria-selected="true">macOS</button>
    <button role="tab" aria-selected="false">Linux</button>
    <button role="tab" aria-selected="false">Windows</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**签名发布（推荐）。** 同时适用于 Apple Silicon 与 Intel——在 Intel Mac 上把 `arm64` 换成 `amd64`。

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

**`go install`。** 如果你已经安装了 Go 1.26+，这是最快的路径：

```sh
brew install go@1.26        # 或从 https://go.dev/dl 安装
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

该二进制内嵌 `modernc.org/sqlite`（见 `internal/state/sqlite/store.go`），因此没有 libc 或 CGo 依赖，也无需 Xcode 命令行工具。

**Homebrew。** Homebrew formula 已列入路线图。在其发布前请使用上方的发布归档路径。

<aside class="admonition" data-type="note"><span class="admonition-title">Gatekeeper</span><p>签名归档未经过 Apple 的公证服务（rousseau 不提供 Apple 开发者 ID）。首次启动可能出现 Gatekeeper 提示；请在 <em>系统设置 &gt; 隐私与安全性</em> 中批准。验证 cosign 签名是等效的供应链检查。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**签名发布（推荐）。** `aarch64` 构建在 `linux_arm64` 下发布：

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

**发行版软件包。** 尚无第一方软件包——请关注上述发布归档。

**无 root 权限 Podman（生产环境）。** Quadlet 参考请见 [部署](/zh-Hans/deployment/)。`pasta` 网络需要 Podman 5.x+；Debian 12 与 Ubuntu 22.04 出厂 4.x，需要 `slirp4netns` 回退（在路线图中）。

<aside class="admonition" data-type="warning"><span class="admonition-title">发行版 Go</span><p>Debian/Ubuntu 常常自带早于 1.26 的 Go。如果 <code>go version</code> 报告 &lt; 1.26，请直接从 <a href="https://go.dev/dl">go.dev/dl</a> 安装或使用签名发布归档——针对旧工具链的 <code>go install</code> 会在 rousseau 使用的模块特性上失败。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau 是一等的 Windows 构建目标；除 `signal`（需要 `signal-cli` 的 JVM 子进程）和 `imessage`（需要 macOS）外，所有传输都可在 Windows 上运行。参考的 Podman + Quadlet 部署仅限 Linux——容器路径请使用 WSL 2 或 Linux 虚拟机。

**签名发布。** PowerShell：

```powershell
$Version = "<pin-a-tag>"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_windows_amd64.zip" -OutFile "rousseau.zip"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_checksums.txt" -OutFile "checksums.txt"
Get-FileHash rousseau.zip -Algorithm SHA256
Expand-Archive rousseau.zip -DestinationPath .
```

用肉眼比较 `Get-FileHash` 输出与 `checksums.txt`，或用 PowerShell 管道脚本化检查。

**`go install`。** 只要 Go 在 PATH 中，在 Windows 上开箱即用：

```powershell
winget install GoLang.Go
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

<aside class="admonition" data-type="warning"><span class="admonition-title">Windows 上的 cosign</span><p><code>cosign</code> CLI 可以在 Windows 上运行，但下载体积大且有自己的依赖链。要减少验证摩擦，可以从 WSL 2 或 Linux 虚拟机对同一个校验和文件运行一次 <code>cosign verify-blob</code>，然后在 Windows 上信任 SHA-256 流程。</p></aside>

<aside class="admonition" data-type="warning"><span class="admonition-title">主目录路径</span><p>Rousseau 在 Windows 上将状态写入 <code>%APPDATA%\rousseau\sessions.db</code>（通过 <code>internal/config/config.go</code> 中的 <code>os.UserConfigDir()</code>）。文档有时引用 Unix 路径 <code>~/.local/share/rousseau/</code>——同一个文件位于平台相应的位置。</p></aside>

  </div>
</div>

## 验证签名发布

`cosign verify-blob` 命令针对 Sigstore 的公开透明日志一次执行三项检查：

1. 嵌入签名中的证书是签发给匹配正则的 GitHub Actions OIDC 身份的。
2. 对校验和文件的签名是有效的。
3. 该证书在透明日志中留有见证。

`sha256sum -c` 随后确认校验和文件中的每一项产物均匹配。这是承载安全的供应链检查——不要跳过。

### 验证 SBOM

每个发布都会附带 `rousseau_<version>_sbom.cdx.json`（CycloneDX 1.5）。用 `cyclonedx-cli` 查看：

```sh
cyclonedx-cli tree --input-file rousseau_<version>_sbom.cdx.json
cyclonedx-cli validate --input-file rousseau_<version>_sbom.cdx.json
```

### 验证 SLSA-3 溯源

```sh
slsa-verifier verify-artifact \
  --provenance-path rousseau_<version>_provenance.intoto.jsonl \
  --source-uri github.com/sebastienrousseau/rousseau-agent \
  --source-tag <version> \
  rousseau_<version>_linux_amd64.tar.gz
```

产物与 CI 证明所构建内容之间的任何偏差都会让 `slsa-verifier` 以非零状态退出。

## macOS

### 签名发布（推荐）

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

在 Intel Mac 上把 `arm64` 换成 `amd64`。

### Homebrew（计划中）

Homebrew formula 已列入路线图。在其发布前，上述发布归档路径是推荐的 macOS 安装方式。

## Linux

### 签名发布（推荐）

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

`aarch64` 构建在 `linux_arm64` 下发布。

certificate-identity 正则用于锁定签名者身份。切勿放宽：由不同身份签署的任何发布归档都应直接拒绝。

### 通过 `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

该二进制完全静态（`CGO_ENABLED=0`）并内嵌 `modernc.org/sqlite`，因此不引入 libc 或 CGo 运行时依赖。`go.sum` 固定由 Go 模块代理校验和数据库强制执行。

## Windows

Windows 二进制以相同的发布归档布局发布：

```powershell
$Version = "<pin-a-tag>"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_windows_amd64.zip" -OutFile "rousseau.zip"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_checksums.txt" -OutFile "checksums.txt"

# 验证 SHA-256（cosign 验证在 Linux/macOS 上更方便；在 Windows 上，
# 仅校验和验证可用，但弱于完整流程）。
Get-FileHash rousseau.zip -Algorithm SHA256
Expand-Archive rousseau.zip -DestinationPath .
```

Windows 是一等的构建目标，但测试相对较少——每个聊天传输都可用，但参考部署（Podman + Quadlet）假设 Linux 环境。请报告 Windows 特有问题以便在 CI 中捕获。

## 从源码构建

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # 产出 ./bin/rousseau
./bin/rousseau version
```

`make check` 运行与 CI 相同的门槛：`go vet`、`golangci-lint` v2（18 个 linter）、`go test -race -count=1 -covermode=atomic ./...` 与 `govulncheck`。

专门的 `reproducible-build` CI 任务在 `ubuntu-latest` 上从全新检出验证位比特一致的输出，因此在相同 Go 工具链下本地执行 `make build` 会产出与打标签发布 SHA-256 相同的二进制。

## Podman / Docker

```sh
# 从打标签的源码本地构建。
podman build -t rousseau-agent:local -f docker/Dockerfile .

# 拉取预构建镜像（一旦发布）。
podman pull ghcr.io/sebastienrousseau/rousseau-agent:<tag>
```

Docker 用法相同：把 `podman` 换成 `docker`。参考部署（[部署](/zh-Hans/deployment/)）使用 **无 root 权限 Podman** + systemd Quadlet 单元，因为 Quadlet 提供了普通 Docker 所没有的声明式加固（`ReadOnly=true`、`DropCapability=all`、`NoNewPrivileges=true`、seccomp 过滤器、`keep-id` 用户命名空间映射）。

运行时镜像约 550 MB，采用多阶段构建：`golang:1.26-alpine` 构建器输出到 `node:22-alpine` 运行时。Node 层的存在只是为了让可选的 `claude` CLI 子进程有运行环境；守护进程本身没有解释器依赖。

## 验证签名发布

`cosign verify-blob` 命令针对 Sigstore 的公开透明日志一次执行三项检查：

1. 嵌入签名中的证书是签发给匹配正则的 GitHub Actions OIDC 身份的。
2. 对校验和文件的签名是有效的。
3. 该证书在透明日志中留有见证。

`sha256sum -c` 随后确认校验和文件中的每一项产物均匹配。这是承载安全的供应链检查——不要跳过。

## 故障排查

### `go: module github.com/sebastienrousseau/rousseau-agent/cmd/rousseau: no matching versions`

你的 `go` 工具链早于 1.26。`go install` 会拒绝声明高于工具链版本的 `go` 指令的模块。请升级 Go，或使用签名发布归档。

### `sha256sum: WARNING: X computed checksums did NOT match`

归档在下载过程中损坏，或（更糟）被篡改。请重新下载并从头执行一遍——`cosign verify-blob` 本应捕获篡改，但请总是相信 SHA-256 结果而非任何假设。

### `cosign: no matching signatures`

你有 `cosign`，但 `--certificate-identity-regexp` 与签名者不匹配。对于 rousseau，请使用 `sebastienrousseau/rousseau-agent`。若仍失败，请运行 `cosign initialize` 刷新 Sigstore 的信任根——信任根按缓慢节奏轮换。

### `rousseau version` 打印 `dev / none / unknown`

你通过 `go install` 安装，`internal/cli/root.go` 中的 `-ldflags` 版本戳未被填充。仅影响外观，但签名发布归档是修复方式。

### macOS Gatekeeper 拒绝打开二进制

在 Finder 中右键点击二进制，选择 <em>打开</em>，然后在对话框中再点一次 <em>打开</em>。或者执行 `xattr -d com.apple.quarantine ./rousseau` 移除隔离位。签名发布未经过公证——cosign 验证是等效的供应链检查。

## 相关页面

- [快速入门：平台支持](/zh-Hans/getting-started/platform-support/)——操作系统、架构与提供方认证矩阵。
- [快速入门：第一个传输](/zh-Hans/getting-started/first-transport/)——端到端接入 WhatsApp。
- [快速入门：更新](/zh-Hans/getting-started/updating/)——如何在版本间安全迁移。
- [部署](/zh-Hans/deployment/)——无 root 权限 Podman + Quadlet 参考部署。
- [安全](/zh-Hans/security/)——信任边界与供应链加固。

## 延伸阅读

- `README.md`——仓库级别的定位与能力矩阵。
- `SECURITY.md`——漏洞披露与供应链控制。
- `Makefile`——由 `make check` 在本地复现的精确 CI 门槛。
- `docker/Dockerfile`——多阶段构建（`golang:1.26-alpine` &rarr; `node:22-alpine`）。
