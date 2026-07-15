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
description: "Configure OpenAI-compatible endpoints: OpenAI, OpenRouter, Ollama, self-hosted vLLM or LM Studio. BaseURL, model naming, streaming, and Ollama's not-required key."
keywords: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, base_url, chat completions, API key, streaming"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/providers/openai-compatible/"
subtitle: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, and any Chat Completions clone."
tags: "providers, openai, openrouter, ollama"
title: "OpenAI 兼容提供方"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "OpenAI, OpenRouter, Ollama, vLLM, LM Studio, base_url, chat completions, API key, streaming"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "OpenAI 兼容提供方"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 10
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/providers/openai-compatible/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/openai-compatible/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "OpenAI 兼容提供方"
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
twitter_description: "Configure OpenAI-compatible endpoints: OpenAI, OpenRouter, Ollama, self-hosted vLLM or LM Studio. BaseURL, model naming, streaming, and Ollama's not-required key."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "OpenAI 兼容提供方"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">你将学到</span><p>rousseau 的 <code>openai</code> 提供方如何用单一实现服务六种不同端点（OpenAI、OpenRouter、Ollama、vLLM、LM Studio、LiteLLM）、每种端点的精确 <code>base_url</code> 与 <code>model</code> 值，以及哪些端点支持工具使用。请对照阅读 <code>internal/llm/openai/client.go</code>。</p></aside>

## 单一实现，多种端点

`internal/llm/openai/` 讲的是 OpenAI Chat Completions API。由于 `base_url` 可配置，同一份代码服务每一个 OpenAI 兼容端点：OpenAI 本身、OpenRouter、together.ai、DeepInfra、自托管 vLLM、Ollama 的 OpenAI 兼容层、LM Studio 与 LiteLLM。

提供方名称为 `openai`、`openrouter` 或 `ollama` 之一——每个对应各自的配置块并预设 `base_url`（见 `internal/config/config.go` 中的 `setDefaults`）。当指向自托管后端时，请使用 `openai` 作为通用槽位并覆盖 `base_url`。

## 端点配方

<div class="tabs" data-tabs="openai-compat-endpoints">
  <div class="tab-list" role="tablist" aria-label="OpenAI-compatible endpoint">
    <button role="tab" aria-selected="true">OpenAI</button>
    <button role="tab" aria-selected="false">OpenRouter</button>
    <button role="tab" aria-selected="false">Ollama</button>
    <button role="tab" aria-selected="false">vLLM</button>
    <button role="tab" aria-selected="false">LM Studio</button>
    <button role="tab" aria-selected="false">LiteLLM</button>
  </div>
  <div class="tab-panel" role="tabpanel">

直连 OpenAI。SDK 默认为 `api.openai.com/v1`——无需覆盖 `base_url`。

```yaml
provider: openai

openai:
  api_key: sk-...
  model: gpt-5
  max_tokens: 4096
```

工具使用：支持（原生 `tools` 数组）。流式：支持（SSE）。

<aside class="admonition" data-type="note"><span class="admonition-title">模型命名</span><p>模型 ID 遵循 OpenAI 自身的命名（<code>gpt-4o</code>、<code>gpt-5</code>、<code>o1</code>、<code>o3-mini</code>）。生产中请固定精确 ID——别名可能在你不知情时变化。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

OpenRouter 在一个 API 后聚合数十个提供方。模型 ID 遵循 `provider/model` 约定：

```yaml
provider: openrouter

openrouter:
  api_key: sk-or-...
  model: anthropic/claude-sonnet-4-6
```

`base_url` 默认为 `https://openrouter.ai/api/v1`。工具使用取决于底层提供方——Anthropic 和 OpenAI 模型可用，大多数开源权重模型不可用。

<aside class="admonition" data-type="tip"><span class="admonition-title">免费层模型</span><p>OpenRouter 暴露免费层变体（<code>:free</code> 后缀）供试验。速率限制和每日配额适用。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

本地 Ollama 在 `http://localhost:11434/v1` 暴露一个兼容 Chat Completions 的层：

```yaml
provider: ollama

ollama:
  model: llama3.1:8b
```

`ollama.api_key` 默认为 `not-required`（该层会忽略它，但 SDK 拒绝空字符串——见 `internal/llm/openai/client.go` 中的 `New`）。`ollama.base_url` 默认为 `http://localhost:11434/v1`。

工具使用：Ollama 0.4+ 起支持（通过 Chat Completions 请求中的 `tools` 数组）。旧版本返回纯文本。

<aside class="admonition" data-type="warning"><span class="admonition-title">延迟</span><p>笔记本上仅 CPU 的 Ollama 每轮可能耗时数十秒。请将调用方 HTTP 超时设为 60 秒以上，或使用具备 GPU 的主机。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

vLLM 是生产级自托管引擎。若需要认证，可用 `--api-key` 启动：

```sh
python -m vllm.entrypoints.openai.api_server \
  --model mistralai/Mixtral-8x22B-Instruct-v0.1 \
  --host 0.0.0.0 --port 8000 \
  --api-key sk-vllm-secret
```

```yaml
provider: openai

openai:
  api_key: sk-vllm-secret
  base_url: http://vllm.internal:8000/v1
  model: mistralai/Mixtral-8x22B-Instruct-v0.1
  max_tokens: 4096
```

工具使用：对于具备 tool-use 聊天模板的模型支持（`Hermes-2-Pro`、`Mistral-Nemo`、`Llama-3.1-8B-Instruct` 及以上）。流式：支持。完整部署参见 [指南：自托管 vLLM](/zh-Hans/guides/self-hosted-vllm/)。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

LM Studio 在 `http://localhost:1234/v1` 提供 OpenAI 兼容服务器：

```yaml
provider: openai

openai:
  api_key: not-required
  base_url: http://localhost:1234/v1
  model: lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF
```

工具使用：当前构建**不**支持（截至 2026 年中）。端点接受 `tools` 数组但会忽略并返回纯文本。请仅用于纯聊天工作负载，或等待该特性落地。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

LiteLLM 是一个在一个 API 后代理许多提供方的代理。将 rousseau 指向它：

```yaml
provider: openai

openai:
  api_key: sk-litellm-...
  base_url: http://litellm.internal:4000
  model: bedrock/anthropic.claude-sonnet-4-6-20260101-v1:0
```

注意：LiteLLM 的默认端口是 4000，其 `/v1` 前缀视部署方式可选。请参考你所用版本的 LiteLLM 文档。

工具使用：透传到底层提供方。流式：支持。适合希望为 LLM 流量提供单一节流点（限流、预算追踪、审计）的团队。

  </div>
</div>

## 配置参考

| 字段 | 默认值 | 作用 |
|---|---|---|
| `api_key` | *必填* | Bearer 令牌。对忽略认证的本地端点使用 `not-required`。 |
| `model` | *必填* | 模型标识符。跨端点没有统一默认值。 |
| `base_url` | *依提供方名称而定* | 覆盖端点。预设见 `setDefaults`。 |
| `max_tokens` | SDK 默认值 | 单次完成的输出 token 上限。 |

`openai`、`openrouter` 与 `ollama` 提供方名称各自映射到自己的配置块（`OpenAIConfig`、`OpenAIConfig`、`OpenAIConfig`）；它们结构相同，但让你能在一个 `config.yaml` 中配置多个端点，并通过修改 `provider:` 在它们之间切换。

## 流式传输

该提供方通过 SSE 实现 `agent.StreamingProvider`。上述所有端点都支持流式；Ollama 的兼容层需要较新的构建（0.5+）。

## 工具使用

来自 `Registry` 的工具定义在 `internal/llm/openai/client.go` 中被转换为 OpenAI 的 `tools` 数组。并非所有 OpenAI 兼容端点都支持工具使用——启用前请检查你的后端。Ollama 自 0.4 起支持；较旧的 LM Studio 不支持。

对于确实返回 `tool_calls` 的端点，审批策略生效。不支持工具使用的端点会返回纯文本，且不会调用 `Registry`。

## 注意事项

- **模型命名。** 每个端点都有自己的约定：OpenAI（`gpt-5`）、OpenRouter（`anthropic/claude-sonnet-4-6`）、Ollama（`llama3.1:8b`）、vLLM（HuggingFace 名称）。跨端点不可互相移植。
- **空 API 密钥。** SDK 拒绝空字符串；对不需要认证的本地端点，请传入 `not-required`（或任意占位符）。
- **BaseURL 结尾斜杠。** 请包含 `/v1` 路径段。不要包含结尾斜杠。
- **超时。** CPU 上的本地 Ollama 每轮可能耗时数十秒——若你自己封装提供方请增加 HTTP 客户端超时。`rousseau` 使用 SDK 默认值。
- **工具使用差异。** OpenAI 与 OpenRouter 后面的 Anthropic 稳定支持工具。Ollama 需要较新构建以及具有 tool-use 聊天模板的模型。LM Studio 不支持工具。若 tool_calls 以纯文本到达，`Registry` 不会被调用。
- **推理模型。** OpenAI o1/o3 系列表现不同：`max_tokens` 被替换为 `max_completion_tokens`，系统提示受限。SDK 会处理这些，但需预期更长的单轮延迟。

## 故障排查

### `openai: complete: 401 Unauthorized`

API 密钥错误或缺失。对于 OpenRouter，使用 `sk-or-…` 令牌。对于本地端点，即使端点忽略也请确保 `api_key` 非空。

### `openai: complete: 404 model not found`

`model` 字符串未匹配端点识别的任何值。对于 OpenRouter，请包含提供方前缀（`anthropic/claude-sonnet-4-6`，而非 `claude-sonnet-4-6`）。对于 Ollama，请确保已拉取模型（`ollama pull llama3.1:8b`）。

### 模型忽略我的 `tools`

该端点对此模型不支持工具使用。请通过已知可用端点（OpenAI、Anthropic 直连、OpenRouter 配 Anthropic 模型）指向同一模型验证。参见上文配方中的工具使用列。

### 本地 Ollama 出现 `context deadline exceeded`

CPU 推理很慢。选项：(1) 增加调用方超时，(2) 在 GPU 主机上运行 Ollama，(3) 切换为更小模型（`llama3.1:8b` 而非 `70b`）。

### 流在响应中途停滞

某些代理（LiteLLM、企业出站代理）会缓冲 SSE。请将代理设置为对 `text/event-stream` 禁用缓冲，或让 rousseau 与端点在同一网段。

## 相关页面

- [指南：自托管 vLLM](/zh-Hans/guides/self-hosted-vllm/)——生产部署。
- [提供方：Anthropic](/zh-Hans/providers/anthropic/)——Claude 的直连 API 备选方案。
- [指南：多提供方](/zh-Hans/guides/multi-provider/)——按传输运行不同提供方。
- [指南：速率限制](/zh-Hans/guides/rate-limits/)——按提供方的重试手册。
- [配置](/zh-Hans/configuration/)——上下文中的 `openai`/`openrouter`/`ollama` 配置块。

## 延伸阅读

- `internal/llm/openai/client.go`——`Complete`、消息转换、工具 schema。
- `internal/llm/openai/client.go`——流式实现。
- `internal/config/config.go`——`OpenAIConfig` 结构体，用于 `base_url` 预设的 `setDefaults`。
