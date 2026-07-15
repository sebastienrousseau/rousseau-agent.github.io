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
description: "A checklist for platform teams adopting rousseau-agent: SBOM, cosign, seccomp, network egress, approval policy, at-rest encryption, security SLOs."
keywords: "enterprise, checklist, sbom, cosign, seccomp, egress, encryption, slo"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/enterprise-onboarding/"
subtitle: "The platform-team checklist before rousseau ships beyond a proof-of-concept."
tags: "guides, enterprise, security, checklist, sbom, cosign"
title: "指南：企业接入"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "enterprise, checklist, sbom, cosign, seccomp, egress, encryption, slo"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：企业接入"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/enterprise-onboarding/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/enterprise-onboarding/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "指南：企业接入"
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
twitter_description: "A checklist for platform teams adopting rousseau-agent: SBOM, cosign, seccomp, network egress, approval policy, at-rest encryption, security SLOs."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "指南：企业接入"
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

## 这是给谁的

在 rousseau-agent 靠近生产之前评估它的平台团队。回答"我们需要签字通过什么？"这个问题。每一项都交叉引用了 rousseau 提供的一个具体事实，因此签字通过是客观的，而不是主观的。

## 清单

### 1. 供应链

- [ ] **SBOM。** 确认每次 release 都发布 `rousseau_<v>_sbom.cdx.json`（CycloneDX 1.5）。导入到您的 SCA 扫描器。可操作：对 SBOM 运行 `cyclonedx-cli tree` 并 grep 您组织禁止的许可证例外。
- [ ] **SLSA-3 溯源。** 每次 release 都发布 `rousseau_<v>_provenance.intoto.jsonl`。用 `slsa-verifier verify-artifact --source-uri github.com/sebastienrousseau/rousseau-agent …` 校验。
- [ ] **cosign 信任根。** 固定证书身份正则：`sebastienrousseau/rousseau-agent`。把校验和验证配方缓存在您的 bootstrap 工具中；见 [快速开始](/zh-Hans/quickstart/) 第 5 步。
- [ ] **可复现构建。** `make check` 运行 `go test -race` 加 `govulncheck`。为您正在运行的版本设置周期性漏洞扫描。

### 2. 运行时加固

- [ ] **rootless 容器。** `docker/rousseau-agent.container` 在带 `loginctl enable-linger` 的专用非特权用户下运行 Quadlet 单元。确认您的主机以同样方式设置。
- [ ] **放弃所有 caps。** `DropCapability=all`。`podman inspect | jq '.[0].EffectiveCaps'` 应显示 `[]`。
- [ ] **`NoNewPrivileges=true`。** 阻止子进程获得特权。
- [ ] **只读根文件系统。** `ReadOnly=true` + `Tmpfs=/tmp:rw,size=64m`。
- [ ] **Seccomp 配置。** `SeccompProfile=/usr/share/containers/seccomp.json`。对照您主机的基线审计它。
- [ ] **用户命名空间映射。** `UserNS=keep-id`。确认 bind-mount 文件在两侧的属主正确。

### 3. 网络姿态

- [ ] **无入站。** Rousseau 零 HTTP 面。`ss -tanp | grep rousseau` 显示只出站 socket。
- [ ] **出站允许列表。** 在容器外叠加 nftables 或 Cloudflare Zero-Trust。只允许：
  - LLM provider（`api.anthropic.com`、`bedrock-runtime.<region>.amazonaws.com`、`us-east1-aiplatform.googleapis.com` 等）。
  - 传输（`web.whatsapp.com`、`mtproto.telegram.org`、matrix homeserver、Slack `wss-*`）。
- [ ] **DNS 解析器锁死。** 可选：在相邻容器中运行一个只解析允许列表内名称的 `unbound`。

### 4. 审批策略

- [ ] **每个无人值守守护进程都 `mode: pattern`。** 在每个传输服务的配置里核实 `agent.approver.mode: pattern`。
- [ ] **`default: deny`。** 未匹配的调用不得通过。
- [ ] **`bash` deny 列表。** `rm\s+-rf`、`sudo`、`curl`、`wget`、`chmod`、`chown`、`nc`、`ncat`。见 [教程：加固审批器](/zh-Hans/tutorials/harden-approver-policy/)。
- [ ] **`write` / `edit` 路径锚定。** 正则把写入限制到 `/workspace/...`。
- [ ] **配置进入源代码控制。** 审批器 YAML 是代码 —— 在 PR 中评审。

### 5. Secret 处理

- [ ] **不要把 API key 放进 `config.yaml`。** 把 secret 存在 `systemd` 的 `EnvironmentFile=`（`chmod 0600`）中或组织的 secret 管理器里。
- [ ] **`ANTHROPIC_API_KEY` 通过环境变量传入。** `config.Load`（`internal/config/config.go`）会拾取它。
- [ ] **Bedrock IRSA / Vertex ADC。** 偏好身份联邦而非长寿命 API key。
- [ ] **轮换节奏。** 90 天或按您的策略。Rousseau 不缓存凭据 —— 轮换后的 key 在下次守护进程重启时被拾取。

### 6. 静态数据

- [ ] **`sessions.db` 加密。** 全盘加密（Linux 上的 LUKS、macOS 上的 FileVault、AWS 上加密的 EBS 卷）。Rousseau 不在会话存储上实现应用层加密。
- [ ] **备份加密。** Restic 或 borg 都用您控制的密钥在静态下加密。
- [ ] **保留策略。** 批量删除早于 `N` 天的会话 —— SQL 见 [指南：会话管理](/zh-Hans/guides/session-management/)。
- [ ] **JID 映射处理。** `jid_sessions` 表把电话号码映射到会话 ID。视其为 PII。

### 7. 日志与审计

- [ ] **`log.format: json`。** 机器可解析输出。
- [ ] **日志转运出主机。** Vector / Promtail / Datadog。见 [指南：可观测性](/zh-Hans/guides/observability/)。
- [ ] **保留。** 冷存储中至少 90 天。Rousseau 的审计轨迹完全在 slog 中；您让它变得持久。
- [ ] **`tool.denied` 告警。** 对任何拒绝告警 —— 可能是良性也可能是尝试注入。
- [ ] **`whatsapp.logged_out` 告警。** Meta 策略触发意味着账号停摆。

### 8. 变更管理

- [ ] **配置变更是代码。** 经 PR 评审、在 git 中版本化。
- [ ] **镜像升级是刻意的。** Quadlet 单元中的 `AutoUpdate=disabled` 是有意的。
- [ ] **回滚计划。** 保留先前镜像已打标签且可用。每次构建前 `podman tag localhost/rousseau-agent:local rousseau-agent:previous`。

### 9. 事件响应

- [ ] **on-call 值班表。** 有人可在您的 MTTR SLO 内 `systemctl --user stop rousseau-agent`。
- [ ] **入侵剧本。** 步骤：吊销 LLM API key，吊销传输 token（例如 Slack 机器人重新安装），快照会话存储，映像化容器文件系统，解绑 WhatsApp 设备。
- [ ] **安全披露通道。** 读 rousseau-agent 仓库中的 `SECURITY.md` 获取协调披露地址。
- [ ] **安全修复的 SLO。** 针对固定的 rousseau 版本跟踪 CVE。`make check` 中的 `govulncheck` 抓取已知 Go 标准库与依赖问题。

### 10. 合规映射

- [ ] **SOC 2 证据。** SLSA-3 溯源 + cosign + SBOM 覆盖 CC7.1（系统运营）。审批器日志覆盖 CC7.2。
- [ ] **ISO 27001 A.12 运营安全。** 审批策略 + 工作区范围化 + 审计日志。
- [ ] **OWASP LLM Top-10。** Rousseau 今天不对 LLM Top-10 做认证 —— 这是路线图项。在您的审计中记录您的补偿性控制（审批器 + 容器）。

## 签字模板

以下是一份您平台团队可以复制到 runbook 的轻量模板：

```
Rousseau-agent deployment sign-off
=================================
Version: <tag>            (verified via cosign / SLSA verifier)
Provider: <anthropic|bedrock|vertex|openai>
Transports enabled: <list>
Approver mode: pattern
Approver default: deny
Log destination: <Loki / Datadog / etc>
Backup destination: <s3://... / restic repo>
On-call: <team>
Security disclosure: <internal address>
```

## 相关

- [安全](/zh-Hans/security/) —— 本清单保护的信任边界。
- [部署](/zh-Hans/deployment/) —— Quadlet 单元。
- [教程：部署到 VPS](/zh-Hans/tutorials/deploy-to-a-vps/) —— 可行示例。
- [指南：生产部署](/zh-Hans/guides/production-deployment/) —— 运营细节。
