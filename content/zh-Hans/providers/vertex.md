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
description: "Configure the Vertex AI provider: Application Default Credentials or an explicit service-account JSON, region and model ID, required IAM roles."
keywords: "Vertex, Google Cloud, GCP, Application Default Credentials, ADC, service account, aiplatform, endpoints, predict"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/providers/vertex/"
subtitle: "Anthropic's Claude models on Vertex AI."
tags: "providers, vertex, GCP"
title: "Google Vertex AI 提供方"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Vertex, Google Cloud, GCP, Application Default Credentials, ADC, service account, aiplatform, endpoints, predict"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Google Vertex AI 提供方"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 9
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/providers/vertex/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/vertex/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Google Vertex AI 提供方"
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
twitter_description: "Configure the Vertex AI provider: Application Default Credentials or an explicit service-account JSON, region and model ID, required IAM roles."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Google Vertex AI 提供方"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p>使用 <code>gcloud</code> 命令逐步设置服务账号、何时改用 Workload Identity Federation、Anthropic 模型的 Vertex 区域矩阵，以及 401/403/429 响应的失败模式。请对照阅读 <code>internal/llm/vertex/client.go</code>。</p></aside>

## 何时使用 Vertex

`vertex` 提供方在以下场景是正确选择：

- 你在 Google Cloud 上并希望通过 Vertex AI 为 Claude 计费。
- 你希望通过服务账号 JSON 或 Application Default Credentials（ADC）进行认证。
- 你需要在特定 GCP 区域内的数据驻留。
- 你希望经由 Private Google Access 路由且不接触公网。
- 你已经为 GKE 负载设置了 Workload Identity Federation。

## 配置

```yaml
provider: vertex

vertex:
  project: my-gcp-project
  region: us-central1
  model: claude-sonnet-4-6@20260101
  credentials_file: ~/.config/gcloud/vertex-key.json
  max_tokens: 4096
```

| 字段 | 默认值 | 作用 |
|---|---|---|
| `project` | *必填* | GCP 项目 ID（不是数字项目编号）。 |
| `region` | *必填* | Vertex 区域。Anthropic-on-Vertex 在部分区域可用；请查看 GCP 控制台。 |
| `model` | *必填* | Anthropic-on-Vertex 模型 ID，例如 `claude-sonnet-4-6@20260101`。注意 `@date` 后缀。 |
| `credentials_file` | *空* | 服务账号或授权用户 JSON key 的路径。为空则使用 ADC。 |
| `max_tokens` | `4096` | 输出 token 上限。 |

## 端点布局

请求指向：

```
https://<region>-aiplatform.googleapis.com/v1/
    projects/<project>/locations/<region>/publishers/anthropic/
    models/<model>:rawPredict
```

`rousseau` 根据 `project`、`region` 和 `model` 构造该 URL；请勿覆盖。

## 凭证

支持两种路径：

### 1. 显式 `credentials_file`

指向服务账号 JSON key 或授权用户 JSON（来自 `gcloud auth application-default login`）：

```yaml
vertex:
  credentials_file: /home/rousseau/.config/gcloud/vertex-sa.json
```

该提供方在底层调用 `google.CredentialsFromJSONWithParams`，因为文件可能是 `service_account` 或 `authorized_user` 之一的结构。`CredentialsParams{Scopes: [cloud-platform]}` 是固定的。

### 2. Application Default Credentials

将 `credentials_file` 留空，提供方会遍历 ADC：

1. `GOOGLE_APPLICATION_CREDENTIALS` 环境变量。
2. `~/.config/gcloud/application_default_credentials.json`（来自 `gcloud auth application-default login`）。
3. GCE / GKE 元数据服务器（集群内推荐使用 Workload Identity）。

## 所需 IAM

在项目上为调用者身份授予 `roles/aiplatform.user`——或更窄的 `aiplatform.endpoints.predict` 权限。

GKE 服务账号的 Workload Identity 示例：

```sh
gcloud projects add-iam-policy-binding my-gcp-project \
  --member "serviceAccount:my-gcp-project.svc.id.goog[default/rousseau-sa]" \
  --role   "roles/aiplatform.user"
```

## 流式传输

该提供方使用同一个 `rawPredict` 端点的 SSE 变体实现 `agent.StreamingProvider`。

## 工具使用

来自 `Registry` 的工具定义在 `internal/llm/vertex/client.go` 中转换为 Vertex 的 Anthropic-tool JSON。审批策略生效。

## 服务账号设置，逐步演示

<div class="tabs" data-tabs="vertex-auth">
  <div class="tab-list" role="tablist" aria-label="Vertex auth pattern">
    <button role="tab" aria-selected="true">服务账号 JSON</button>
    <button role="tab" aria-selected="false">Workload Identity（GKE）</button>
    <button role="tab" aria-selected="false">来自 AWS/Azure 的 WIF</button>
    <button role="tab" aria-selected="false">用户 ADC（开发）</button>
  </div>
  <div class="tab-panel" role="tabpanel">

对于本地或非 GKE 主机最简单的模式。创建专用服务账号、授予最小角色、下载 JSON key，然后让 rousseau 指向该文件。

```sh
PROJECT=my-gcp-project
SA_NAME=rousseau-vertex

gcloud iam service-accounts create $SA_NAME \
  --display-name "rousseau-agent Vertex caller" \
  --project $PROJECT

gcloud projects add-iam-policy-binding $PROJECT \
  --member "serviceAccount:${SA_NAME}@${PROJECT}.iam.gserviceaccount.com" \
  --role   "roles/aiplatform.user"

gcloud iam service-accounts keys create ~/vertex-sa.json \
  --iam-account "${SA_NAME}@${PROJECT}.iam.gserviceaccount.com"
```

```yaml
vertex:
  project: my-gcp-project
  region: europe-west4
  model: claude-sonnet-4-6@20260101
  credentials_file: /etc/rousseau/vertex-sa.json
```

<aside class="admonition" data-type="caution"><span class="admonition-title">密钥轮换</span><p>服务账号 JSON key 永不过期。请至少每 90 天轮换一次。优先使用 Workload Identity Federation（下文），这样你就无需管理静态密钥。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

GKE 上的推荐模式。将 Kubernetes 服务账号绑定到 Google 服务账号，使 pod 通过元数据服务器继承凭证——磁盘上无 JSON key。

```sh
PROJECT=my-gcp-project
KSA=rousseau
GSA=rousseau-vertex
NAMESPACE=agents

# GSA already exists from the previous step. Bind the KSA:
gcloud iam service-accounts add-iam-policy-binding \
  "${GSA}@${PROJECT}.iam.gserviceaccount.com" \
  --role "roles/iam.workloadIdentityUser" \
  --member "serviceAccount:${PROJECT}.svc.id.goog[${NAMESPACE}/${KSA}]"
```

为 Kubernetes 服务账号添加注解：

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rousseau
  namespace: agents
  annotations:
    iam.gke.io/gcp-service-account: rousseau-vertex@my-gcp-project.iam.gserviceaccount.com
```

然后将 `credentials_file` 留空——ADC 会自动从 GKE 元数据服务器获取凭证。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Workload Identity Federation 让 AWS IAM 角色或 Azure 托管身份无需服务账号 key 即可调用 GCP API。对多云部署很有用。

创建联邦身份：

```sh
gcloud iam workload-identity-pools create rousseau-pool \
  --location=global --project=$PROJECT

gcloud iam workload-identity-pools providers create-aws rousseau-aws \
  --location=global \
  --workload-identity-pool=rousseau-pool \
  --account-id=<AWS_ACCOUNT_ID>
```

将 AWS 角色绑定到 GSA：

```sh
gcloud iam service-accounts add-iam-policy-binding \
  "${GSA}@${PROJECT}.iam.gserviceaccount.com" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/rousseau-pool/attribute.aws_role/arn:aws:iam::${AWS_ACCOUNT_ID}:role/rousseau"
```

将 `GOOGLE_APPLICATION_CREDENTIALS` 导出为一个 credential-source JSON 文件，用于指示 SDK 用 AWS 角色兑换 GCP 令牌。credential-source 结构参见 [GCP WIF 文档](https://cloud.google.com/iam/docs/workload-identity-federation)。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

在本地开发时，通过 `gcloud` 使用你自己的用户凭证：

```sh
gcloud auth application-default login
gcloud auth application-default set-quota-project my-gcp-project
```

这会写入 `~/.config/gcloud/application_default_credentials.json`。将 `credentials_file` 留空，rousseau 会通过 ADC 读取。

<aside class="admonition" data-type="warning"><span class="admonition-title">切勿用于生产</span><p>用户 ADC 将请求绑定到你的个人身份与配额。切勿在生产环境部署使用用户 ADC 的守护进程——请切换到服务账号或 Workload Identity。</p></aside>

  </div>
</div>

## 区域矩阵

Vertex 上的 Anthropic 模型按区域限定。可用性随 Google 发布新快照而变化。以 2026 年中为准：

| 模型 | us-central1 | us-east5 | europe-west1 | europe-west4 | asia-southeast1 |
|---|:---:|:---:|:---:|:---:|:---:|
| `claude-sonnet-4-6` | 是 | 是 | 是 | 是 | 是 |
| `claude-opus-4-6` | 是 | 有限 | 有限 | 是 | 否 |
| `claude-haiku-4-6` | 是 | 是 | 是 | 是 | 是 |

权威来源是 Vertex Model Garden——*Model Garden &gt; Anthropic &gt; Region availability*。申请访问即时生效；没有人工审批步骤（不同于 Bedrock）。

## 私有连接

对于不得出站到公网的部署，请在 VPC 上使用 Private Google Access，并配置 DNS 将 `*-aiplatform.googleapis.com` 解析为 `restricted.googleapis.com`。rousseau 构造的 Vertex 端点 URL 仍然有效，但流量保留在 Google 骨干上。

DNS 区域设置参见 [GCP Private Google Access 文档](https://cloud.google.com/vpc/docs/private-google-access)。

## 注意事项

- **模型 ID 格式。** Vertex 使用 `@date`（`claude-sonnet-4-6@20260101`），Bedrock 使用 `-<date>-v1:0`，Anthropic 直连使用 `claude-sonnet-4-6`。请勿将一种粘贴为另一种。
- **区域可用性。** 并非每个 Anthropic 模型都在每个区域可用。`us-central1` 和 `europe-west4` 是常见的。
- **配额。** Vertex 配额按项目、区域、模型计。触发配额则请求会 429；请在调用方启用指数退避。
- **`anthropic_version` 字符串。** rousseau 发送 `vertex-2023-10-16`（见 `internal/llm/vertex/client.go` 中的 `buildVertexBody`）。若 Anthropic 升级 Vertex anthropic_version，旧的 rousseau 构建会 400。
- **需要 User-Agent。** 某些 Vertex 端点会拒绝没有 User-Agent 的请求。Go SDK 会自动设置；如果你注入自定义 `HTTPClient`，请保留 User-Agent 首部。

## 故障排查

### `vertex: HTTP 401 unauthorized`

凭证链未返回有效凭证。常见原因：容器内 `credentials_file` 路径不可读、`GOOGLE_APPLICATION_CREDENTIALS` 环境变量指向不存在的文件，或从未运行过 `gcloud auth application-default login`。用 `gcloud auth application-default print-access-token` 验证。

### `vertex: HTTP 403 permission denied on resource`

身份已认证但缺少项目上的 `aiplatform.endpoints.predict`。授予 `roles/aiplatform.user`（或更窄的权限），等待约 30 秒 IAM 传播。

### `vertex: HTTP 404 not found`

模型 ID 在该区域不存在。请从 Vertex Model Garden 复核 `@date` 后缀，并确认该区域的可用性矩阵中显示该模型。

### `vertex: HTTP 429 resource exhausted`

配额超限。选项：(1) 通过 IAM 控制台申请配额提升，(2) 在调用方以退避排队请求，(3) 将流量分散到多个区域。

### `vertex: credentials: could not find default credentials`

ADC 没有可遍历的内容。要么显式设置 `credentials_file`、`export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json`，要么（对 GKE）确认集群启用了 Workload Identity 且 KSA 注解正确。

## 相关页面

- [提供方：Anthropic](/zh-Hans/providers/anthropic/)——相同的线协议格式，直连 API。
- [提供方：Bedrock](/zh-Hans/providers/bedrock/)——AWS 托管的 Claude。
- [指南：Kubernetes 部署](/zh-Hans/guides/kubernetes-deployment/)——Workload Identity 设置。
- [指南：企业入驻](/zh-Hans/guides/enterprise-onboarding/)——平台团队检查清单。
- [安全](/zh-Hans/security/)——信任边界与网络出站。

## 延伸阅读

- `internal/llm/vertex/client.go`——端点 URL 构造、ADC 处理、线协议类型。
- `internal/llm/vertex/oauth2.go`——OAuth2 HTTP 客户端构造。
- `internal/config/config.go`——`VertexConfig` 结构体。
- GCP 文档：[Vertex AI 上的 Anthropic](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude)。
- GCP 文档：[Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation)。
