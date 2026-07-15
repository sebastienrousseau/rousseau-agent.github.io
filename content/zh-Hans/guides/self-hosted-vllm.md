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
description: "Worked example: point rousseau-agent at a self-hosted vLLM endpoint on your internal network via the OpenAI-compatible provider."
keywords: "vllm, self-hosted, openai-compatible, air-gapped, internal network, local llm"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/self-hosted-vllm/"
subtitle: "Point rousseau at a vLLM endpoint on your internal network."
tags: "guides, vllm, self-hosted, openai-compatible"
title: "指南：自托管 vLLM"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "vllm, self-hosted, openai-compatible, air-gapped, internal network, local llm"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：自托管 vLLM"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 32
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/self-hosted-vllm/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/self-hosted-vllm/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "指南：自托管 vLLM"
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
twitter_description: "Worked example: point rousseau-agent at a self-hosted vLLM endpoint on your internal network via the OpenAI-compatible provider."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "指南：自托管 vLLM"
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

## 场景

您在一台内部机器（`llm.internal:8000`）上有一个 vLLM 实例，为一个开源权重的编码模型提供服务。任何推理流量都不能离开网络。把 rousseau 指向它，并将该端点当作任何其他 OpenAI 兼容目标一样对待。

vLLM 实现了 OpenAI Chat Completions schema，因此 rousseau 的 `openai` provider 无需修改即可工作。LM Studio、Ollama 与 Text Generation Inference 是相同的模式。

## 先决条件

- vLLM 已在 `http://llm.internal:8000/v1` 上启动，`/v1/chat/completions` 对 curl 冒烟测试有响应。
- 您启动 vLLM 时使用的模型标签（例如 `Qwen/Qwen3-Coder-30B`）。

## 第 1 步 —— 确认 vLLM

```sh
curl -fsS http://llm.internal:8000/v1/models
curl -fsS http://llm.internal:8000/v1/chat/completions \
  -H 'content-type: application/json' \
  -d '{
    "model": "Qwen/Qwen3-Coder-30B",
    "messages": [{"role": "user", "content": "say hi"}]
  }' | jq .
```

两者都应无错误返回。如果第二个调用出现 4xx，先修复 vLLM —— rousseau 的客户端是一个薄的 JSON 垫片，会继承其错误表面。

## 第 2 步 —— 将 rousseau 接线到 vLLM

编辑 `~/.config/rousseau/config.yaml`：

```yaml
provider: openai

openai:
  base_url: http://llm.internal:8000/v1
  api_key: not-required        # vLLM ignores the key but the client sends one
  model: Qwen/Qwen3-Coder-30B
  max_tokens: 4096

log:
  level: info
  format: json
```

`openai` provider 与 `openrouter` 和 `ollama` 共享 schema；唯一的区别是预设的 `base_url`。显式设置 `base_url` 会覆盖默认值。

## 第 3 步 —— 在 TUI 中冒烟测试

```sh
rousseau chat
```

输入 `explain the difference between goroutines and threads in two paragraphs.` 并发送。如果回复以流式方式出现，接线就是正确的。

如果没有：

```sh
rousseau doctor
```

`provider.selected` 行会显示 `openai`；`provider.openai.base_url` 可达性上的 `fail` 表示 DNS 或内部网络路径被断开，而不是 rousseau。

## 第 4 步 —— 开启工具使用

编码模型在工具使用保真度上差异很大。rousseau 代理循环期望模型发出 `tool_use` 块，其 JSON 能够按工具的 `InputSchema` 通过校验。如果您的 vLLM 模型本身不支持 OpenAI 工具使用 schema：

- 从 `provider: openai` 开始，加上一个支持工具使用的模型（近期的 Qwen、Mistral、Llama 3.1 8B+ 变体宣称支持）。
- 或用一个垫片（例如 [vLLM 的 OpenAI 兼容 tool_choice 适配器](https://docs.vllm.ai/)）包裹 vLLM 并重新验证。

一旦工具使用生效，编码工具（read、write、edit、grep、bash）就像在任何其他 provider 下一样可用。

## 第 5 步 —— 考虑审批策略

自托管模型往往比前沿模型对风险的感知更弱。使用 `pattern` 模式审批器锁定 `bash` 工具是审慎之举：

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read,  match: ".*"}
      - {tool: grep,  match: ".*"}
      - {tool: edit,  match: "^./workspace/.*"}
      - {tool: bash,  match: "^(ls|cat|grep|rg|find|git status|git diff) "}
    deny:
      - {tool: bash,  match: "rm -rf|sudo|curl|wget|chmod|chown"}
```

更深入的演练见 [指南：审计 + 审批策略](/zh-Hans/guides/audit-approval-policies/)。

## 第 6 步 —— 关注性能

自托管端点通常受益于更高的 `max_iterations`（代理循环可能需要更多轮次才能得出相同结论），并且总是受益于启用会话压缩：

```yaml
agent:
  max_iterations: 48
  compression:
    enabled: true
    trigger_messages: 60
    keep_recent: 8
```

压缩默认关闭，因为它会用一个 LLM 轮次做摘要；在按 token 计费的公有 API 上这可能是浪费的。在自托管端点上 token 成本为零，所以保持开启。

## vLLM 的替代方案

同样的配方适用于：

- **Ollama** —— 使用 `provider: ollama`（`base_url` 默认为 `http://localhost:11434/v1`，`api_key` 默认为 `not-required`）。
- **LM Studio** —— 使用 `provider: openai` 并将 `base_url` 指向 LM Studio 服务器（`http://host:1234/v1`）。
- **TGI (Text Generation Inference)** —— 使用 `provider: openai` 并将 `base_url` 指向 TGI 的 OpenAI 兼容端点。
- **OpenRouter** —— 使用 `provider: openrouter`（`base_url` 默认为 `https://openrouter.ai/api/v1`）。

## 注意事项

- provider 不做流式时 rousseau 就不流式。某些 vLLM 构建默认禁用流式 —— 打开它以获得更好的 TUI 体验。
- 提示缓存（`internal/llm/anthropic` 使用 `cache_control` 标记）是 Anthropic 特有的，对 vLLM 无效。这主要在按 token 计费 provider 上的长寿命会话中有意义。
- [openai-compatible provider 页面](/zh-Hans/providers/openai-compatible/) 是每个旋钮的权威参考。

## 下一步

- [OpenAI 兼容 provider](/zh-Hans/providers/openai-compatible/) —— 每个配置字段。
- [审计 + 审批策略](/zh-Hans/guides/audit-approval-policies/) —— 面向对齐较弱模型的安全姿态。
- [离线](/zh-Hans/offline/) —— 在没有出站互联网的环境中运行 rousseau。
