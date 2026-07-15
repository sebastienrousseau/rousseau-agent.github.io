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
changefreq: "weekly"
description: "rousseau-agent security posture: SLSA-3 provenance, cosign signatures, CycloneDX SBOM, dropped capabilities, seccomp, trust model, cryptography inventory, disclosure SLA."
keywords: "security, SLSA-3, cosign, sigstore, SBOM, CycloneDX, seccomp, drop capabilities, trust model, disclosure, CVSS, coordinated disclosure"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/security/"
subtitle: "Supply chain, runtime, and trust boundaries — honestly stated."
tags: "security, supply-chain, disclosure"
title: "安全"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "security, SLSA-3, cosign, sigstore, SBOM, CycloneDX, seccomp, drop capabilities, trust model, disclosure, CVSS, coordinated disclosure"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "安全"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "security"
order: 26
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/security/index.html"
item_link: "https://docs.rousseau-agent.dev/security/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "安全"
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
twitter_description: "rousseau-agent security posture: SLSA-3 provenance, cosign signatures, CycloneDX SBOM, dropped capabilities, seccomp, trust model, cryptography inventory, disclosure SLA."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "安全"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p>rousseau 的威胁模型（散文与 ASCII 图形式）、承载安全的关键边界（审批策略、容器隔离、供应链）、参考 seccomp 过滤器及如何进一步收紧、网络出站策略，以及落入 <code>slog</code> 的审计轨迹。请对照源码树中的 <code>SECURITY.md</code> 与 <code>docker/rousseau-agent.container</code> 阅读真相。</p></aside>

## 威胁模型图

```
                          ┌──────────────────────────────────┐
                          │        Chat transport user       │
                          │   (WhatsApp / Slack / Discord)   │
                          └──────────────────┬───────────────┘
                                             │ E2EE (WhatsApp)
                                             │ TLS   (Slack / Discord / …)
                        ─────────────────────┴─────────────────────
                                             │
                                             ▼
      ┌─────────────── rousseau-agent container ────────────────┐
      │                                                          │
      │   ┌─────────────┐    inbound     ┌──────────────────┐   │
      │   │  Transport  │ ───────────▶   │  Router          │   │
      │   │  adapter    │                │  + allowlist     │   │
      │   └─────────────┘                └────────┬─────────┘   │
      │                                           │             │
      │                                           ▼             │
      │                                   ┌─────────────┐       │
      │                                   │   Agent     │       │
      │                                   │  Turn loop  │       │
      │                                   └──────┬──────┘       │
      │                                          │              │
      │                            approver     │              │
      │                          ◀───────────────┤              │
      │                                          ▼              │
      │                                   ┌─────────────┐       │
      │                                   │  Registry   │       │
      │                                   │ read/edit/  │       │
      │                                   │ bash/…      │       │
      │                                   └──────┬──────┘       │
      │                                          │              │
      │  ROOTFS  ReadOnly=true  ─────────────────┤              │
      │  CAPS    DropCapability=all              │              │
      │  UID     1000, keep-id                   │              │
      │  SECCOMP default filter                  │              │
      │                                          │              │
      │            outbound TLS                  ▼              │
      └──────────────────┬───────────────────────┬──────────────┘
                         │                       │
                         ▼                       ▼
                ┌────────────────┐    ┌─────────────────────┐
                │  LLM provider  │    │  bind mounts        │
                │  (Anthropic /  │    │  ~/.local/share/    │
                │   Bedrock /    │    │    rousseau/  RW    │
                │   Vertex / …)  │    │  workspace/   RW    │
                └────────────────┘    │  ~/.claude/   RW    │
                                      └─────────────────────┘
```

容器边界内的一切都在 rousseau 控制之下。聊天传输入口到达时已完成 E2EE 加密（WhatsApp）或 TLS 加密（Slack、Discord、Matrix、Telegram、Email、SMS）。LLM 提供方出站为 TLS。绑定挂载是守护进程访问宿主文件系统的唯一途径。

## 信任模型——在范围内的内容

`rousseau-agent` 是一个**本地、容器原生的守护进程**。三条承载安全的边界：

### 1. 用户 shell

内建的 `bash` 工具会以用户权限执行任意命令。**这是主要的安全边界。** 每次工具调用在执行前都会被暴露出来，并受配置的审批策略约束（`allow_all`、`deny_all`，或 `pattern` 模式——按工具的正则允许 / 拒绝规则加可配置的默认值）。

运行无人值守（聊天传输）守护进程的运维人员**必须**二选一：

- 强制使用 `pattern` 模式并设置 `default: deny` 及明确的允许规则，或
- 在明确理解风险敞口的前提下接受 `bypassPermissions` 姿态。

不存在由模型自我把关的中间地带。如果守护进程能够执行 shell 命令，并且可通过聊天传输访问，那么可访问它的用户原则上就能驱动 shell。

### 2. 容器隔离

参考部署是无 root 权限的 Podman 容器，具备：

- `ReadOnly=true`
- `DropCapability=all`
- `NoNewPrivileges=true`
- 默认 seccomp 过滤器（`/usr/share/containers/seccomp.json`）
- 非 root UID 1000
- `keep-id` 用户命名空间映射
- `Network=pasta`（无 root 权限，默认不接受来自主机的入站）

容器内仅可见工作区绑定挂载、状态目录与 `~/.claude`。参见 [/deployment/](/zh-Hans/deployment/)。

### 3. 供应链

每次提交都会运行 `govulncheck` 与 CodeQL。每个发布都会附带：

- **SLSA Level 3 溯源**，通过 `slsa-framework/slsa-github-generator` 提供，由 GitHub Actions OIDC 签名。
- **cosign 签名**，签名对象是校验和文件，可对照 Sigstore 透明日志验证。
- **CycloneDX JSON SBOM。**
- **可复现构建证明**——专门的 CI 任务在全新检出上验证输出位比特一致。

## 信任模型——不在范围内的内容

- **恶意模型输出。** 运维人员负责在批准前审查工具调用。审批策略让这一过程不易出错，但不能消除人类判断的必要性。
- **被入侵的 Go 工具链、容器运行时或主机操作系统。** 假定构建环境可信。
- **对机器的物理访问。**
- **对 LLM 提供方本身的攻击。** 提供方漏洞由该提供方负责。

## 供应链控制

| 控制 | 实现方式 |
|---|---|
| 直接依赖固定 | `go.mod` 中的精确版本；`go.sum` 中冻结的传递解析。 |
| 漏洞扫描 | 每次 CI 构建都会执行 `govulncheck ./...`。任何触及已导入符号的已知漏洞都会导致构建失败。 |
| 静态分析 | `golangci-lint` v2（18 个 linter）+ GitHub CodeQL（Go）。 |
| 依赖更新 | `gomod` 与 `github-actions` 的 Dependabot，按周更新。 |
| 构建溯源 | 通过 `slsa-framework/slsa-github-generator` 实现 SLSA Level 3；经由 GitHub Actions OIDC 证明并发布到 Sigstore 透明日志。 |
| 发布签名 | 使用 cosign（无密钥，通过 GitHub Actions OIDC）对发布校验和签名。 |
| 软件物料清单 | 每个发布产物都附带 CycloneDX JSON SBOM。 |
| 可复现构建 | 专门的 `reproducible-build` CI 任务验证位比特一致的输出。 |

CI 工作流文件位于源码树的 `.github/workflows/` 下：`ci.yml`、`codeql.yml`、`slsa.yml`、`release.yml`、`reproducible-build.yml`。

## 验证发布

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_<version>_checksums.txt.sig \
  rousseau_<version>_checksums.txt

sha256sum -c rousseau_<version>_checksums.txt
```

锁定身份的两个参数：

- `--certificate-identity-regexp` 匹配签发签名证书的 GitHub 仓库。切勿放宽到 `.*`；正是这一项阻止其他仓库的 cosign 签名验证你的校验和文件。
- `--certificate-oidc-issuer` 将 OIDC 发行方锁定为 GitHub Actions。

Sigstore 透明日志条目可以在 https://search.sigstore.dev/ 单独查询。

## 运行时控制

下列每一项均在参考 Quadlet 单元中设置，属于任何容器运维人员的基线：

- **非 root 用户（UID 1000）**——容器内无提权到 root 的权限。
- **`ReadOnly=true`**——运行时镜像不可写；二进制无法修改自身或其依赖。
- **`Tmpfs=/tmp:rw,size=64m,mode=1777`**——绑定挂载之外唯一的可写位置。
- **`DropCapability=all`**——不设置任何 `CAP_*` 位。出站 TCP 不需要任何能力。
- **`NoNewPrivileges=true`**——阻止 setuid 提权。
- **默认 seccomp 过滤器**——内核级系统调用管控。
- **`Network=pasta`**——无 root 权限网络栈；默认不接受来自主机的入站。
- **未发布端口**——Quadlet 中没有 `PublishPort=`。没有需要发布的入站 HTTP 面。

## 密码学清单

| 用途 | 实现 |
|---|---|
| 到 LLM / 传输端点的 TLS | Go 标准库 `crypto/tls` + 系统信任存储。 |
| WhatsApp | `whatsmeow`（Signal 协议）。 |
| Matrix | 基于 HTTPS 的 Client-Server API。 |
| SMTP（邮件传输） | Go 标准库 `net/smtp`，`PlainAuth` 运行在 TLS 之上。 |
| 静态会话存储 | **应用层不加密。** 需要静态加密的运维人员应将状态目录挂载在加密文件系统（LUKS、FileVault）上。 |

本项目未实现任何自研密码学原语。

## 漏洞披露

请私下报告至 **sebastian.rousseau@gmail.com**。**不要**为影响安全的报告创建公开 issue。

内容包括：

- 简要描述与 CVSS 3.1 向量。
- 受影响组件（文件路径 + 行范围，或依赖模块路径）。
- 环境详情（`rousseau version`、Go 版本、操作系统、容器运行时）。
- 最小复现——最好是一个失败的测试。

### 响应承诺

| 事件 | SLA |
|---|---|
| 报告确认 | ≤ 72 小时 |
| 分诊决定（接受 / 拒绝 / 需要信息） | ≤ 7 天 |
| **严重**级修复上线（CVSS ≥ 9.0） | ≤ 14 天 |
| **高**级修复上线（7.0–8.9） | ≤ 30 天 |
| **中 / 低**级修复上线 | 排入常规发布 |
| 公开披露（协调） | 修复发布后 |

## 支持版本

仅 `main` 分支和最新的打标签发布会收到安全修复。没有长期支持分支。

## Seccomp 过滤器解析

参考 Quadlet 单元使用 Podman 位于 `/usr/share/containers/seccomp.json` 的默认 seccomp 配置。它屏蔽了约 70 个 rousseau 正确调用永远不需要的系统调用，包括：

| 系统调用族 | 屏蔽 | 原理 |
|---|---|---|
| 内核 keyring（`add_key`、`keyctl`、`request_key`） | 是 | rousseau 不接触内核 keyring。 |
| 挂载管理（`mount`、`umount`、`pivot_root`、`chroot`） | 是 | 运行时不进行动态挂载变更。 |
| 内核模块（`init_module`、`finit_module`、`delete_module`） | 是 | 守护进程无法加载内核模块。 |
| 命名空间（`setns`、带某些标志的 `unshare`） | 过滤 | 防止通过命名空间切换逃逸容器。 |
| 调试原语（`ptrace`、`process_vm_readv`、`process_vm_writev`） | 是 | rousseau 不附加到其他进程。 |
| BPF（`bpf`） | 是 | 不允许容器内运行 eBPF 程序。 |
| 重启（`reboot`、`kexec_*`） | 是 | 容器没有正当理由重启主机。 |
| 时钟更改（`clock_settime`、`adjtimex`） | 是 | 时间由主机管理。 |

默认配置允许标准库、SQLite 驱动（`modernc.org/sqlite`）、whatsmeow 客户端以及 OpenAI/Anthropic SDK 所需的足够系统调用。若需进一步收紧——例如因你从不模拟其他 ABI 而移除 `personality`——请复制默认配置、删除该系统调用，并在 Quadlet 中通过 `SeccompProfile=/path/to/profile.json` 引用副本。

<aside class="admonition" data-type="caution"><span class="admonition-title">收紧配置的测试</span><p>每一次 seccomp 调整都需要在冒烟测试中覆盖——一个你不知道 rousseau 需要的系统调用会在运行时导致对话或传输失败。上线生产前请用真实聊天回环测试。</p></aside>

## 网络出站策略

容器默认无入站且不限制出站（`Network=pasta`）。对于高安全部署，请添加一套只允许 rousseau 所需域名的 nftables 规则：

```
# /etc/nftables.d/rousseau.nft — example only, adjust to your provider
table inet rousseau_out {
    chain output {
        type filter hook output priority 0; policy drop;

        # LLM providers
        ip daddr { 3.5.0.0/16, 15.230.0.0/16 } tcp dport 443 accept  # Anthropic + Bedrock
        ip daddr { 34.107.0.0/16 } tcp dport 443 accept              # Vertex

        # Chat transports
        ip daddr { 157.240.0.0/16 } tcp dport 443 accept             # Meta (WhatsApp)
        ip daddr { 3.208.0.0/16 } tcp dport 443 accept               # Slack

        # DNS
        udp dport 53 accept
        tcp dport 53 accept

        # NTP
        udp dport 123 accept
    }
}
```

CIDR 范围会变化——请把上述内容当作脚手架。要点在于 rousseau 的出站是有限且可枚举的；源码中的示例 `docker/example-nftables.rules` 是一份起始规则集。

## 通过 slog 的审计轨迹

每一个与安全相关的事件都通过 Go 的 `log/slog` 以结构化 JSON 级别（`log.format: json`）记录。生产中你应该跟踪的事件：

| 事件 | 级别 | 来源 | 表达含义 |
|---|---|---|---|
| `tool.execute` | info | `internal/agent/agent.go` | 模型请求运行的工具及所处会话。 |
| `tool.denied` | warn | `internal/agent/agent.go` | 审批器拒绝了一次调用；包含理由字符串。 |
| `tool.error` | warn | `internal/agent/agent.go` | 工具运行但返回错误。 |
| `router.transport.rejected` | info | `internal/transport/router.go` | 入站消息未通过允许列表。 |
| `whatsapp.logged_out` | error | `internal/transport/whatsapp/client.go` | Meta 使配对失效。 |
| `mcp.tool_error` | warn | `internal/mcp/server.go` | MCP 工具处理器返回错误。 |
| `cron.delivery_failed` | warn | `internal/cron/` | 定时任务的传输投递出错。 |

将 JSON 流馈入 Loki / Datadog / Splunk / Vector 管道；参见 [指南：可观测性](/zh-Hans/guides/observability/)。

<aside class="admonition" data-type="tip"><span class="admonition-title">字段命名</span><p>Slog 属性键按点号分组（<code>whatsapp.connected</code>，而非 <code>event=whatsapp_connected</code>）。在你所用的日志工具中直接以原始键查询。</p></aside>

## 故障排查

### 容器因 `mount: permission denied` 拒绝启动

SELinux 标签不匹配。确保每一行绑定挂载都以 `:Z`（私有标签）或 `:z`（共享）结尾。没有标签，容器进程无法读写被主机打过标签的文件。

### Seccomp 杀掉了我需要的系统调用

Podman 会向 journal 打印 `syscall X blocked`。在容器外用 `strace -f -e trace=X` 复现以确认调用需求。如果合理，请复制默认 seccomp 配置、将该系统调用加入允许列表，并通过 `SeccompProfile=` 引用该配置。

### `cosign verify-blob` 显示 "certificate identity does not match"

你的 `--certificate-identity-regexp` 错误。请使用 `sebastienrousseau/rousseau-agent`。任何更宽松的正则（`.*`、`.+`）都会破坏无密钥签名的意义。

### 在 nftables 限制下提供方出站失败

你的规则集不包含提供方当前的 IP 范围。提供方会轮换 CIDR。请使用基于 DNS 的出站——由定时任务解析的 ipset，或使用在连接时解析名称的出站代理。

### 期待审计事件但 slog 中没有

日志级别过高。设置 `log.level: info`（或 `debug` 以查看线级细节），并确认守护进程确实启动了新会话——`slog.Default()` 在配置加载前被使用，因此早期启动消息无论如何都以文本形式路由到 stderr。

## 相关页面

- [部署](/zh-Hans/deployment/)——参考 Quadlet 单元。
- [用户指南：审批策略](/zh-Hans/user-guide/approval-policies/)——主要的安全杠杆。
- [指南：提示注入](/zh-Hans/guides/prompt-injection/)——通过模型输出发起的攻击。
- [指南：只读模式](/zh-Hans/guides/read-only-mode/)——如何运行"只看不改"的守护进程。
- [指南：可观测性](/zh-Hans/guides/observability/)——slog + Loki / Datadog 管道。

## 延伸阅读

- `SECURITY.md`——规范策略文档。
- `docker/rousseau-agent.container`——参考 Quadlet 单元。
- `docker/example-nftables.rules`——示例出站规则集。
- `internal/agent/agent.go`——`tool.execute` 与 `tool.denied` 事件的发出位置。
- `internal/agent/approver.go`——审批策略实现。
