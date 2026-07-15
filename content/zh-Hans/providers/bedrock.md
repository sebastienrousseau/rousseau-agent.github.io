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
description: "Configure the AWS Bedrock provider: standard credential chain, region and model ID format, required IAM permissions."
keywords: "Bedrock, AWS, SigV4, IAM, InvokeModel, InvokeModelWithResponseStream, Claude on AWS"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/providers/bedrock/"
subtitle: "Anthropic's Claude models on AWS."
tags: "providers, bedrock, AWS"
title: "AWS Bedrock 提供方"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Bedrock, AWS, SigV4, IAM, InvokeModel, InvokeModelWithResponseStream, Claude on AWS"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "AWS Bedrock 提供方"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 8
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/providers/bedrock/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/bedrock/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "AWS Bedrock 提供方"
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
twitter_description: "Configure the AWS Bedrock provider: standard credential chain, region and model ID format, required IAM permissions."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "AWS Bedrock 提供方"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p>如何配置 Bedrock 提供方并使用 AWS 凭证链、最小权限 IAM 策略、跨账号角色假设、用于私有连接的 VPC 端点，以及按区域的模型可用性矩阵。请对照阅读 <code>internal/llm/bedrock/client.go</code>。</p></aside>

## 何时使用 Bedrock

`bedrock` 提供方在以下场景是正确选择：

- 你在 AWS 上并希望通过 Bedrock 而非 Anthropic API 为 Claude 计费。
- 你需要通过标准 AWS 凭证链（环境变量、`~/.aws/credentials`、IMDS、EKS 上的 IRSA）进行 SigV4 认证。
- 出于数据驻留原因，你希望将模型流量保留在单个 AWS 区域内。
- 你需要通过 VPC 端点路由模型流量，使其永不触及公网。
- 你希望通过 `sts:AssumeRole` 实现跨账号访问。

## 配置

```yaml
provider: bedrock

bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
  profile: default
  max_tokens: 4096
```

| 字段 | 默认值 | 作用 |
|---|---|---|
| `region` | *必填* | AWS 区域。Bedrock 模型可用性因区域而异；请查看 AWS 控制台。 |
| `model` | *必填* | Bedrock 模型 ID。Anthropic Claude ID 形如 `anthropic.claude-<name>-<date>-<version>:<revision>`。 |
| `profile` | *空* | 来自 `~/.aws/credentials` 的凭证 profile。为空则回退到标准凭证链。 |
| `max_tokens` | SDK 默认值 | 单次完成的输出 token 上限。 |

## 凭证链

该提供方通过 `awsconfig.LoadDefaultConfig` 构造 Bedrock 客户端，后者按顺序遍历标准凭证链：

1. 环境变量（`AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY`、`AWS_SESSION_TOKEN`）。
2. 共享凭证文件（`~/.aws/credentials`），若设置了 `profile` 则按其筛选。
3. 共享配置文件（`~/.aws/config`）。
4. IAM Roles for Tasks（ECS）/ IAM Roles Anywhere。
5. EC2 IMDS（v2）。
6. IRSA——附加到 Kubernetes 服务账号（EKS）上的 IAM 角色。

其中任一都不由 rousseau 配置；由 SDK 处理解析。

## 所需 IAM 权限

调用方必须能承担的最小策略：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-sonnet-4-6-*"
    }
  ]
}
```

将 `Resource` 收窄到你计划调用的特定模型族。更宽松的通配符也能工作但通常过头。

## 线协议格式

该提供方向 `bedrock:InvokeModel` 发送标准的 Anthropic messages JSON 主体（`anthropic_version`、`messages`、`system`、`tools`、`max_tokens`），并收到相同结构。这与 Anthropic 直连 API 一致——工具使用、停止原因和用量计数器相同。

流式使用 `bedrock:InvokeModelWithResponseStream` 加 SDK 的 event-stream 解码器。

## 流式传输

该提供方实现了 `agent.StreamingProvider`。`rousseau chat` 中自动使用流式。

## 工具使用

来自 `Registry` 的工具定义在 `internal/llm/bedrock/client.go` 中转换为 Bedrock 的工具 JSON。审批策略生效。

## 按部署方式的认证模式

<div class="tabs" data-tabs="bedrock-auth">
  <div class="tab-list" role="tablist" aria-label="Bedrock auth deployment">
    <button role="tab" aria-selected="true">笔记本</button>
    <button role="tab" aria-selected="false">EC2</button>
    <button role="tab" aria-selected="false">EKS（IRSA）</button>
    <button role="tab" aria-selected="false">跨账号</button>
  </div>
  <div class="tab-panel" role="tabpanel">

在本地开发时，请使用具备 SSO 或长期密钥的命名 profile：

```sh
aws configure sso --profile rousseau-dev
aws sso login --profile rousseau-dev
```

```yaml
bedrock:
  region: us-east-1
  profile: rousseau-dev
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

`profile:` 会被采纳，因为当非空时 rousseau 会传入 `awsconfig.WithSharedConfigProfile(cfg.Profile)`（见 `internal/llm/bedrock/client.go` 第 63 行）。省略 `profile` 则回退到默认凭证链。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

附加一个带有 `bedrock:InvokeModel` 权限的实例 profile（见下文 IAM 策略），然后将 `profile` 留空：

```yaml
bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

SDK 会自动从 IMDS v2 解析凭证。无需环境变量、无需 profile 文件。

<aside class="admonition" data-type="note"><span class="admonition-title">IMDS v2</span><p>请确保实例配置为要求 IMDS v2（hop limit 2、要求 token）。AWS Go SDK v2 会透明处理 token 交换，但需要能网络到达 <code>169.254.169.254</code>。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

IAM Roles for Service Accounts（IRSA）是 EKS 上的推荐模式。将一个角色附加到 pod 的服务账号：

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rousseau
  namespace: agents
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/rousseau-bedrock
```

该角色的信任策略将其绑定到 EKS OIDC 提供方与服务账号。完整示例参见 [指南：Kubernetes 部署](/zh-Hans/guides/kubernetes-deployment/)。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau 位于账号 A，Bedrock 位于账号 B。配置角色假设：

`~/.aws/config`：

```ini
[profile rousseau]
role_arn = arn:aws:iam::222222222222:role/rousseau-bedrock
source_profile = default
region = us-east-1
```

账号 B 中的目标角色对模型拥有 `bedrock:InvokeModel`，并具备允许账号 A 主体承担的信任策略。然后：

```yaml
bedrock:
  region: us-east-1
  profile: rousseau
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

SDK 会透明处理 STS `AssumeRole` 往返。

  </div>
</div>

## 最小权限 IAM 策略

调用方必须能承担的最小策略：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-sonnet-4-6-*"
    }
  ]
}
```

将 `Resource` 收窄到特定模型族。更宽松的通配符也能工作但会授予过多权限。对于预置吞吐量，将预置模型的 ARN 作为第二个资源加入。

跨账号信任策略（账号 B，模型托管侧）：

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "AWS": "arn:aws:iam::111111111111:role/rousseau-caller" },
    "Action": "sts:AssumeRole",
    "Condition": { "StringEquals": { "sts:ExternalId": "rousseau-prod" } }
  }]
}
```

AWS 安全指南要求第三方跨账号访问必须使用 `ExternalId`。

## VPC 端点

对于不得访问公网的部署，请在你的 VPC 中为 Bedrock 创建接口 VPC 端点：

```sh
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-0123456789abcdef0 \
  --vpc-endpoint-type Interface \
  --service-name com.amazonaws.us-east-1.bedrock-runtime \
  --subnet-ids subnet-aaa subnet-bbb \
  --security-group-ids sg-xxx
```

如果安全组和路由表允许，AWS SDK 会自动通过该端点解析。无需修改 rousseau 侧配置——对提供方而言是透明的。

<aside class="admonition" data-type="warning"><span class="admonition-title">端点策略</span><p>为端点附加资源策略以限制其接受的主体与动作。开放的端点会抵消隔离的好处。</p></aside>

## 按区域的模型可用性

可用性随 AWS 发布新快照而变化。以 2026 年中为准的快照：

| 模型 | us-east-1 | us-west-2 | eu-west-2 | eu-central-1 | ap-southeast-1 | ap-northeast-1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Claude Sonnet 4.6 | 是 | 是 | 是 | 是 | 是 | 是 |
| Claude Opus 4.6 | 是 | 是 | 有限 | 有限 | 否 | 否 |
| Claude Haiku 4.6 | 是 | 是 | 是 | 是 | 是 | 是 |

<aside class="admonition" data-type="note"><span class="admonition-title">请查看控制台</span><p>可用性会在无通知的情况下变化。权威来源是 Bedrock 控制台的 <em>Foundation models &gt; Model access</em>——即使区域支持该模型，你也必须在此明确申请访问权，之后才能调用。</p></aside>

## 注意事项

- **模型 ID 因区域而异。** `us-east-1` 中的 `anthropic.claude-sonnet-4-6-20260101-v1:0` 在 `eu-west-2` 可能是不同快照。请查看 Bedrock 控制台。
- **必须按模型授予访问权。** 即使 IAM 允许 `InvokeModel`，Bedrock 也要求你在控制台点击 *Model access &gt; Request access*，之后首次调用才会成功。
- **限流。** Bedrock 对每个账号与每个模型强制执行并发限制（每分钟 token 数与每分钟请求数）。请保守设置 `max_tokens`。
- **预置吞吐量。** 如果你拥有预置吞吐量，请将预置模型 ID（`arn:aws:bedrock:us-east-1:<account>:provisioned-model/…`）作为 `model` 传入。
- **流式解码失败。** event-stream 格式在 SDK 版本间有细微变化。将 `aws-sdk-go-v2/service/bedrockruntime` 固定到已知良好版本，并在每次升级时重新测试。

## 故障排查

### `AccessDeniedException: You don't have access to the model`

两项独立检查：(1) 调用方 IAM 策略允许对模型 ARN 执行 `bedrock:InvokeModel`，(2) 账号已在 Bedrock 控制台明确申请该模型的访问权。第 2 项是大多数首次使用者的坑。

### `ValidationException: The model ID isn't valid`

模型 ID 字符串与配置区域中的模型不匹配。请从 Bedrock 控制台（*Providers &gt; Anthropic &gt; Model catalog*）复制精确 ID，不要手打——日期和版本后缀必须完全一致。

### `ThrottlingException`

你触及了每分钟 token 或请求配额。选项：(1) 申请服务配额提升，(2) 在调用方以指数退避排队请求，(3) 切换到预置吞吐量。

### `bedrock: parse response: json:` —— JSON 格式错误

响应体不是预期的 Anthropic-on-Bedrock 结构。通常表明传入的 `model` 不是 Anthropic 模型；`internal/llm/bedrock/client.go` 中的 `buildBedrockBody` 只生成 Anthropic 线协议格式。

### VPC 端点不可达 —— `dial tcp: no route to host`

pod/实例无法到达端点的 ENI。检查端点上的安全组（必须允许来自调用方 SG 的 443 端口）、端点子网的路由表以及 DNS 解析（端点要求在 VPC 上启用私有 DNS）。

## 相关页面

- [提供方：Anthropic](/zh-Hans/providers/anthropic/)——相同的线协议格式，直连 API 路径。
- [指南：Kubernetes 部署](/zh-Hans/guides/kubernetes-deployment/)——IRSA 设置。
- [指南：企业入驻](/zh-Hans/guides/enterprise-onboarding/)——平台团队检查清单。
- [指南：速率限制](/zh-Hans/guides/rate-limits/)——限流手册。
- [安全](/zh-Hans/security/)——信任边界与网络出站。

## 延伸阅读

- `internal/llm/bedrock/client.go`——`Complete`、消息转换、线协议类型。
- `internal/config/config.go`——`BedrockConfig` 结构体。
- AWS 文档：[Amazon Bedrock IAM 权限](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html)。
- AWS 文档：[Bedrock 接口 VPC 端点](https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html)。
