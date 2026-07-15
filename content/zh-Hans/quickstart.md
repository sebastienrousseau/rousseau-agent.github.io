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
description: "Install rousseau-agent, configure a provider, hold your first conversation, wire a transport, and verify the release supply chain in about five minutes."
keywords: "quickstart, install, first conversation, whatsapp, cosign, SLSA, SBOM, provider"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/quickstart/"
subtitle: "五分钟上手 rousseau：安装、配置、对话、验证。"
tags: "quickstart, install, provider, transport, supply-chain"
title: "快速开始"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "quickstart, install, first conversation, whatsapp, cosign, SLSA, SBOM, provider"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "快速开始"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 0
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/quickstart/index.html"
item_link: "https://docs.rousseau-agent.dev/quickstart/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "快速开始"
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
twitter_title: "快速开始"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "感谢每一位运行自有编码代理的运维者。"
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## 5 分钟上手 rousseau

Rousseau 是一个静态单文件 Go 二进制，内置 Bubble Tea TUI、位于 `~/.local/share/rousseau/sessions.db` 的 SQLite 会话存储，以及九种聊天传输（WhatsApp、Signal、Telegram、Slack、Discord、Matrix、iMessage、SMS、Email）。没有 SaaS 控制面，没有遥测，没有许可服务器。LLM 由您自备。

本页面带您端到端：

- [ ] **1. 安装 rousseau** — 通过源代码、`go install` 或经 cosign 验证的 release。
- [ ] **2. 配置您的 LLM** — 选择一个 provider（默认 `claudecli`；Anthropic、Bedrock、Vertex 或任何 OpenAI 兼容端点）。
- [ ] **3. 进行首次对话** — 在终端中运行 `rousseau chat`。
- [ ] **4. 添加一个传输** — 使用允许列表 JID 配对 WhatsApp。
- [ ] **5. 验证供应链** — 用 cosign 验证 checksums 文件，然后阅读 CycloneDX SBOM 和 SLSA-3 溯源。

大多数运维者在十分钟内即可完成。

## 1. 安装 rousseau

<aside class="admonition" data-type="tip"><span class="admonition-title">推荐</span><p>如果您已经安装了 Go 1.26+，<code>go install</code> 是最快的路径。生产环境请使用已签名的 release 并配合 <code>cosign verify-blob</code>，以保留供应链保障。</p></aside>

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

该二进制文件内嵌 `modernc.org/sqlite`（见 `internal/state/sqlite/store.go`），因此运行时无 libc 或 CGo 依赖。在 macOS、Linux 和 Windows 上表现一致。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` 会运行 `go vet`、`golangci-lint`、`go test -race` 与 `govulncheck` —— 与 CI 强制执行的门禁相同。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

每个打标签的 release 都会发布一个带 checksum 的归档、一份 CycloneDX SBOM、一份 SLSA-3 溯源证明，以及针对 checksums 文件的 cosign 签名：

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

<aside class="admonition" data-type="note"><span class="admonition-title">说明</span><p><code>cosign</code> 身份被限定在 <code>sebastienrousseau/rousseau-agent</code> 的 GitHub Actions OIDC。信任根请参见 <a href="/zh-Hans/security/">安全</a>。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau 在 `docker/Dockerfile` 提供一个 Podman 友好的 `Dockerfile`，并在 `docker/rousseau-agent.container` 提供一个 systemd Quadlet 单元。在 ghcr.io 发布镜像已列入路线图；在此之前请本地构建：

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
```

参见 [部署](/zh-Hans/deployment/) 获取具有加固运行时姿态（rootless、`DropCapability=all`、`NoNewPrivileges=true`、seccomp）的参考 Quadlet 单元。

  </div>
</div>

### 特定操作系统的先决条件

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

对于默认的 `claudecli` provider，请从 https://claude.ai/download 安装 Claude Code，并执行一次 `claude login`。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

通过包管理器或从 https://go.dev/dl 安装 Go 1.26+。对于容器路径，请使用 rootless Podman ≥ 5.x 并使用 `pasta` 网络模式。

```sh
# Debian/Ubuntu
sudo apt install golang-1.26 podman

# Arch
sudo pacman -S go podman

# Fedora
sudo dnf install golang podman
```

Claude Code CLI（可选，用于 `claudecli` provider）：从 https://claude.ai/download 下载。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau 通过 `go install` 在 Windows 上原生运行。容器参考部署仅支持 Linux；在 Windows 上，请使用 WSL 2 进行 Podman 路径。

```powershell
winget install GoLang.Go
# Or: choco install golang
```

对于 `claudecli`，请从 https://claude.ai/download 安装 Claude Code。

<aside class="admonition" data-type="warning"><span class="admonition-title">Windows 提示</span><p>某些传输包会调用子进程（<code>signal-cli</code>）或打开特定于操作系统的路径（<code>~/.local/share/</code>）。<code>whatsapp</code>、<code>slack</code>、<code>discord</code>、<code>telegram</code>、<code>matrix</code>、<code>email</code>、<code>sms</code> 传输均为跨平台。<code>signal</code> 和 <code>imessage</code> 需要各自的宿主工具。</p></aside>

  </div>
</div>

## 2. 配置您的 LLM

配置位于 `~/.config/rousseau/config.yaml`（可用 `--config` 覆盖），每个字段均在 `internal/config/config.go` 中定义。默认 provider 是 `claudecli`，它 shell out 到本地的 `claude` CLI，因此 API 密钥不会离开您的笔记本。

### claudecli（默认，无需密钥）

如果您已经安装并认证了 Claude Code（`claude`），那就完成了。Rousseau 会继承其 OAuth 会话：

```yaml
provider: claudecli

claudecli:
  binary: claude              # optional; PATH lookup by default
  permission_mode: default    # or bypassPermissions for unattended daemons
```

参见 [Providers: claudecli](/zh-Hans/providers/claudecli/)。

### Anthropic API

直接对接 Anthropic。使用 `internal/llm/anthropic/client.go` 中的官方 `anthropic-sdk-go`：

```sh
export ANTHROPIC_API_KEY=sk-ant-…
```

```yaml
provider: anthropic
anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096
```

`ANTHROPIC_API_KEY` 直接从环境变量读取（见 `internal/config/config.go` 中的 `config.Load`）；密钥永远不必落盘。参见 [Providers: Anthropic](/zh-Hans/providers/anthropic/)。

### AWS Bedrock

使用标准的 AWS 凭据链（profile、IMDS、IRSA）。区域和模型来自 `internal/config/config.go` 的 `BedrockConfig`：

```yaml
provider: bedrock
bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
  profile: default            # optional named profile
  max_tokens: 4096
```

`config.yaml` 中不含 API 密钥。参见 [Providers: Bedrock](/zh-Hans/providers/bedrock/)。

### Google Vertex AI

Anthropic on Vertex；读取一份 service account JSON 文件。配置字段在 `VertexConfig` 中定义：

```yaml
provider: vertex
vertex:
  project: my-gcp-project
  region: europe-west4
  model: claude-sonnet-4-6@20250101
  credentials_file: /etc/rousseau/vertex.json
  max_tokens: 4096
```

参见 [Providers: Vertex](/zh-Hans/providers/vertex/)。

### OpenAI 兼容（OpenRouter、Ollama、vLLM、LM Studio）

provider 名称 `openai`、`openrouter` 和 `ollama` 共用 `OpenAIConfig`。OpenRouter 和 Ollama 的 base URL 在 `setDefaults` 中有默认值（`https://openrouter.ai/api/v1` 和 `http://localhost:11434/v1`）；其他一切都通过显式的 `base_url` 落到 `openai` 块中：

```yaml
provider: ollama              # or: openai, openrouter
ollama:
  model: llama3.1:70b-instruct
  base_url: http://localhost:11434/v1
```

参见 [Providers: OpenAI 兼容](/zh-Hans/providers/openai-compatible/) 和 [Guides: 自托管 vLLM](/zh-Hans/guides/self-hosted-vllm/)。

## 3. 进行首次对话

```sh
rousseau chat
```

您将看到一个 Bubble Tea TUI（`internal/tui/model.go`）：

- 顶部的 **viewport** 滚动显示会话记录。助手文本在到达时以流式方式呈现。
- 底部的 **textarea** 接收您的输入。按 `Enter` 发送，`Ctrl+C` 退出。
- LLM 轮次期间会显示一个 **spinner**；当 tokens 到达时会出现一个小的流式指示器。
- 每个轮次都被持久化到 `~/.local/share/rousseau/sessions.db` 的 SQLite。`internal/state/sqlite/store.go` 中的 `Open()` 启用了 WAL 日志，因此您可以在 TUI 打开的同时安全地对同一数据库运行其他 rousseau 命令（`rousseau session list`、`rousseau mcp`）。

先从小事问起 —— 例如 "列出 `internal/tools/builtin` 下的文件" —— rousseau 会根据需要调用内建工具 `read`、`grep`、`edit`、`write` 或 `bash`（`internal/tools/builtin/*.go`）。键位映射参见 [用户指南: TUI](/zh-Hans/user-guide/tui/)，schemas 参见 [用户指南: 工具](/zh-Hans/user-guide/tools/)。

截图占位符：TUI 显示两行状态栏（会话 id 与 provider）、着色的助手 + 用户消息 viewport，以及底部聚焦的 textarea。

## 4. 添加一个传输（WhatsApp）

WhatsApp 是参考传输，因为配对最为严格。所有其他传输（`slack`、`discord`、`telegram`、`matrix`、`signal`、`sms`、`imessage`、`email`）遵循相同的形式。

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

首次启动时，`rousseau` 将 QR 码打印到 stdout。在您的手机上通过 **WhatsApp > 设置 > 已连接的设备** 扫描它。whatsmeow 客户端（`internal/transport/whatsapp/client.go`）会发出三个结构化日志事件：

- `whatsapp.qr_ready` — QR 已渲染。
- `whatsapp.paired` — 手机接受了 QR。
- `whatsapp.connected` — 通往 Meta 的 websocket 已连通。

设备凭据被缓存到 `~/.local/share/rousseau/whatsapp.db`（独立的 SQLite 数据库，因此重新连接设备不会影响会话历史）。`--allow` 标志固定一份 E.164 JID 的允许列表；其他任何发送者都会被 `router.transport.rejected` 静默丢弃。

Rousseau 使用 **非官方** WhatsApp Web 协议。Meta 偶尔会封禁运行非官方客户端的号码 —— 请不要在您依赖的号码上运行。风险分析参见 [Transports: WhatsApp](/zh-Hans/transports/whatsapp/)。

## 5. 验证供应链

每个打标签的 release 会交付：

| 制品 | 用途 |
|---|---|
| `rousseau_<v>_checksums.txt` | release 中每个归档的 SHA-256。 |
| `rousseau_<v>_checksums.txt.sig` | cosign 签名（keyless，来自 GitHub Actions 的 OIDC 颁发）。 |
| `rousseau_<v>_sbom.cdx.json` | Go 模块图的 CycloneDX 1.5 SBOM。 |
| `rousseau_<v>_provenance.intoto.jsonl` | SLSA-3 溯源证明。 |

在信任 checksums 之前，请验证签名身份：

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_0.6.0_checksums.txt.sig \
  rousseau_0.6.0_checksums.txt
```

`--certificate-identity-regexp` 将签名者身份钉在 Sebastien 命名空间下的 rousseau-agent 仓库。**请勿放宽。** 通配符身份会使 keyless 签名失去意义。

签名验证通过后，`sha256sum -c` 证明您下载的 tarball 就是 CI 构建的那个。用 `cyclonedx-cli tree` 阅读 SBOM，用 `slsa-verifier verify-artifact` 验证 SLSA-3 溯源，然后再解压归档。

完整信任边界参见 [安全](/zh-Hans/security/)，平台团队清单参见 [Guides: 企业入门](/zh-Hans/guides/enterprise-onboarding/)。

## 故障排除

<aside class="admonition" data-type="tip"><span class="admonition-title">推荐的首站</span><p>在提 issue 之前，请运行 <code>rousseau doctor</code>。它会锻炼每一个子系统 —— provider 认证、状态存储、传输凭据 —— 并输出结构化的 pass/warn/fail 行。</p></aside>

### `go install` 之后 `rousseau version` 输出 "dev"

`version`、`commit`、`buildDate` 的值由 release 工具链通过 `internal/cli/root.go` 中的 `-ldflags` 加以打标。`go install` 会跳过这些 flag，因此二进制会报告 `dev / none / unknown`。若需要稳定的版本字符串，请使用已签名 release 路径；`dev` 字符串在运行时无害。

### `claudecli: exec: "claude": executable file not found`

`provider: claudecli` shell out 到 `claude` 二进制。请将 Claude Code 放入您的 `$PATH`（参见 [Providers: claudecli](/zh-Hans/providers/claudecli/)），或切换 provider —— 最快的替代方案是 `provider: anthropic` 并导出 `ANTHROPIC_API_KEY`。

### WhatsApp QR 已显示但从未被接受

三种常见原因：（1）容器时钟偏差超过 30 秒 —— WhatsApp 握手对时间敏感；（2）部分完成的配对使 `whatsapp.db` 处于不可重用状态 —— 删除 `~/.local/share/rousseau/whatsapp.db` 并重新扫描；（3）Meta 已使该号码失效 —— 尝试一个新号码。参见 [Transports: WhatsApp](/zh-Hans/transports/whatsapp/)。

### `cosign verify-blob` 报错 "no matching signatures"

`--certificate-identity-regexp` 必须匹配签名者的 GitHub 仓库。对于 rousseau-agent，正确值是 `sebastienrousseau/rousseau-agent`。通配符会使 keyless 签名失去意义 —— 请勿放宽。如果正则表达式正确，请用 `cosign initialize` 刷新 Sigstore 的信任根。

### 每次工具调用都被 "denied by pattern policy" 拒绝

您运行在 `pattern` 模式且 `default: deny`，没有匹配的 allow 规则。为该工具添加一条 allow 条目，或者反转为 `default: allow` 并添加狭窄的 deny 规则。工作示例参见 [用户指南: 审批策略](/zh-Hans/user-guide/approval-policies/)。

## 相关页面

- [入门: 安装](/zh-Hans/getting-started/installation/) —— 每种安装方法及验证配方。
- [入门: 首个传输](/zh-Hans/getting-started/first-transport/) —— WhatsApp/Slack/Discord 的端到端演练。
- [配置](/zh-Hans/configuration/) —— `~/.config/rousseau/config.yaml` 的每个旋钮。
- [概念](/zh-Hans/concepts/) —— 代理循环、会话存储、MCP、cron、skills。
- [故障排除](/zh-Hans/troubleshooting/) —— 完整的故障模式目录。

## 延伸阅读

- `README.md` —— 仓库级定位与能力矩阵。
- `SECURITY.md` —— 信任边界与供应链加固。
- `internal/config/config.go` —— 权威配置 struct。
- `internal/cli/root.go` —— Cobra 命令树接线。

## 后续步骤

| 去哪里 | 为什么 |
|---|---|
| [配置](/zh-Hans/configuration/) | `~/.config/rousseau/config.yaml` 的每个旋钮及默认值。 |
| [概念](/zh-Hans/concepts/) | 代理循环、会话存储、MCP、cron、skills。 |
| [部署](/zh-Hans/deployment/) | Rootless Podman + systemd Quadlet 单元。 |
| [安全](/zh-Hans/security/) | 信任边界、SLSA-3 溯源、seccomp 姿态。 |
| [教程](/zh-Hans/tutorials/) | 完整的端到端演练。 |
| [参考](/zh-Hans/reference/cli-commands/) | 每一个 CLI flag、退出码与配置字段。 |
