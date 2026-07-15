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
description: "Use case narrative: a financial-services team running rousseau-agent in-tenant on AWS with Bedrock, pattern-mode approvals, and SLSA-3 supply-chain posture."
keywords: "regulated industry, financial services, bedrock, in-tenant, slsa, cosign, compliance"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/use-cases/regulated-industry/"
subtitle: "In-tenant Bedrock deployment for a financial-services team."
tags: "use-cases, bedrock, regulated, financial-services, slsa"
title: "用例：受监管行业"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "regulated industry, financial services, bedrock, in-tenant, slsa, cosign, compliance"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "用例：受监管行业"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 73
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/use-cases/regulated-industry/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/regulated-industry/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "用例：受监管行业"
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
twitter_description: "Use case narrative: a financial-services team running rousseau-agent in-tenant on AWS with Bedrock, pattern-mode approvals, and SLSA-3 supply-chain posture."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "用例：受监管行业"
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

## 故事

您是一家中型银行的平台工程师。合规部说您的工程师使用的任何编码助手必须：

1. 运行在银行的 AWS 账户内，而不是 SaaS 控制面。
2. 通过银行有合同与审计轨迹的 provider（Bedrock）路由模型流量。
3. 拥有已文档化的供应链姿态（SLSA-3、SBOM、签名校验）。
4. 以机器可读的审计轨迹执行审批策略。
5. 不向第三方外泄源代码。

Rousseau 的定位对应上述每一条要求。您在平台团队的 EKS 集群中把它作为 Kubernetes `Deployment` 运行，驱动一个 Slack Socket Mode 传输进入工程频道。

工程上的部署平平无奇 —— 一个 `Deployment`、一个 `Secret`、一个 `ConfigMap`、一个 `PersistentVolumeClaim`。故事在审计员到来时才开始。

## 审计

一位外部审计员问四个问题。

**Q1：模型流量去哪里？**

您把他们指向 `internal/llm/bedrock/`。provider 使用标准 AWS 凭据链（在 EKS 上通过 IRSA），所以凭据是短寿命的 STS token。流量绝不离开您的 AWS 账户。

**Q2：您如何校验正在运行的二进制？**

您向他们展示 `docker/Dockerfile` —— 多阶段构建，固定 `golang:1.26-alpine` 基础镜像 —— 以及 SRE 团队在镜像升级期间运行的 `release-verify.sh` 脚本：

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_${VERSION}_checksums.txt.sig \
  rousseau_${VERSION}_checksums.txt

sha256sum -c rousseau_${VERSION}_checksums.txt
```

您补充：SLSA-3 溯源通过 GitHub Actions OIDC 证明。Sigstore 透明日志是公开的信任锚。

**Q3：您如何防止模型改动生产？**

您把他们指向 `agent.approver` 配置：

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied — this deployment does not permit destructive operations without operator confirmation"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|grep|rg|find|git status|git diff|git log|go test|go build) "}
    deny:
      - {tool: bash, match: "rm -rf|sudo|curl|wget|chmod|chown"}
      - {tool: bash, match: "kubectl (delete|apply|edit|scale|exec)"}
      - {tool: bash, match: "aws (s3 rm|iam|kms delete)"}
      - {tool: write, match: "\"path\":\"/(etc|root|var|usr)/"}
      - {tool: edit,  match: "\"path\":\"/(etc|root|var|usr)/"}
```

deny 优先于 allow。未匹配 → deny。每次决定都记录为结构化 slog 事件（`tool.execute`、`tool.denied`）并通过 Vector daemonset 转发到银行的 Datadog 租户。

**Q4：会话引用的源代码存在哪里？**

您解释：会话状态存在一个由 EBS 加密静态支撑的 PVC 上。模型上下文停留在压缩会话之内（见 [压缩 + 回忆](/zh-Hans/user-guide/compression-recall/)）。FTS5 回忆索引运行在同一个 PVC 上。没有东西发到 `agentskills.io` 或任何外部 URL —— [Skills](/zh-Hans/skills/) 从一个 bind-mount 的目录加载，而不是托管的 registry。

审计员接着问："模型本身呢？"您解释 Bedrock 是模型边界；Bedrock 对提示做的一切都由银行与 AWS 已有的合同管辖。

## 这需要什么

### manifest

完整 manifest 见 [指南：Kubernetes 部署](/zh-Hans/guides/kubernetes-deployment/)。该用例的关键偏差：

- **Namespace `pod-security.kubernetes.io/enforce: restricted`。**
- 用 **IRSA** 提供 Bedrock 凭据 —— 秘密中不放长寿命 AWS key。
- **NetworkPolicy** 只允许出站到 Bedrock 区域端点与 Slack WSS。
- **Vector daemonset** 把 slog 输出发到 Datadog，并把 `msg` 字段解析为 facet。

### 配置

```yaml
provider: bedrock

bedrock:
  region: eu-west-1
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
  max_tokens: 4096

log:
  level: info
  format: json

state:
  path: /var/lib/rousseau/sessions.db

agent:
  max_iterations: 32
  compression:
    enabled: true
    trigger_messages: 40
    keep_recent: 6
  approver:
    mode: pattern
    default: deny
    reason: "denied — this deployment does not permit destructive operations without operator confirmation"
    allow: [...as above...]
    deny:  [...as above...]

slack:
  app_token: xapp-<from-Secret>
  bot_token: xoxb-<from-Secret>
  allowlist:
    - U012ABC   # 平台团队 on-call
    - U012DEF   # 平台团队负责人
```

### 审计故事

每次工具调用就是一行 slog。每次拒绝也是。Datadog 对 `msg:tool.denied` 的监视器告警到 SOC。每周，平台团队拉取一份报告：

```
# LogQL / Datadog / whichever
sum by (name) (
  count_over_time({job="rousseau-agent"} |= "tool.denied" [1w])
)
```

报告归到合规盘。由于 slog schema 稳定（[可观测性](/zh-Hans/guides/observability/)），解析不会因 rousseau 升级而破坏。

## 审计员可能不问但应该问的

- **可复现构建。** Rousseau 的 CI 包含一个 `reproducible-build` 任务，校验在新 checkout 上产出按位相同的输出。您可以独立地从打标签的源代码重建并比较 SHA-256。
- **依赖固定。** `go.mod` 固定精确版本；`go.sum` 被冻结。Dependabot 把升级作为可评审的 PR 打开，而不是静默的 bump。
- **每次 commit 上的 `govulncheck`。** 任何触达导入符号的已知漏洞都会让 CI 失败。
- **每次 commit 上的 CodeQL** 静态分析。

以上所有都在 [安全](/zh-Hans/security/) 中 —— 合规文件抽屉已经存在。

## 离租户边界

Bedrock 就是边界。到 `bedrock-runtime.eu-west-1.amazonaws.com` 的流量离开 Pod 但保留在 AWS 内。银行的数据流图显示一条从 Pod 到 Bedrock 的箭头；该部署没有其他出站箭头（Slack Socket Mode 是到 `wss-primary.slack.com` 的出站 WSS，被文档化为单独允许的出站）。

## 相关页面

- [指南：Kubernetes 部署](/zh-Hans/guides/kubernetes-deployment/) —— manifest。
- [指南：审计 + 审批策略](/zh-Hans/guides/audit-approval-policies/) —— 合规故事。
- [指南：可观测性](/zh-Hans/guides/observability/) —— slog 管道。
- [Bedrock provider](/zh-Hans/providers/bedrock/) —— 凭据链与区域行为。
- [安全](/zh-Hans/security/) —— 信任模型与供应链控制。
