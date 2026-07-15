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
description: "How rousseau-agent handles provider rate limits: 429s, exponential backoff, prompt-cache markers, and per-provider cost notes."
keywords: "rate limits, 429, backoff, retry, prompt cache, anthropic, bedrock, cost"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/rate-limits/"
subtitle: "429 handling, backoff, and cache-marker optimisation."
tags: "guides, rate limits, prompt cache, anthropic"
title: "指南：速率限制"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "rate limits, 429, backoff, retry, prompt cache, anthropic, bedrock, cost"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：速率限制"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 36
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/rate-limits/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/rate-limits/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "指南：速率限制"
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
twitter_description: "How rousseau-agent handles provider rate limits: 429s, exponential backoff, prompt-cache markers, and per-provider cost notes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "指南：速率限制"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">您将学到</span><p>按 provider 的速率限制、按 token 的成本、重试语义、缓存经济性，以及一份调用方侧带退避的重试配方。权威数字请见各 provider 的定价页 —— 下表是快照。</p></aside>

## 速率限制发生在哪里

Rousseau 不实现自己的速率限制处理。每个 provider 客户端委托给上游 SDK：

- **Anthropic direct** —— `anthropic-sdk-go` 处理 HTTP 重试，遵守 `Retry-After`，对 5xx 与 429 应用指数退避。见 `internal/llm/anthropic/client.go`。
- **Bedrock** —— `aws-sdk-go-v2` 用自适应重试处理限流错误。
- **Vertex** —— Google 认证库处理自己的重试。
- **OpenAI / OpenRouter / Ollama** —— Go OpenAI 兼容客户端处理 429。
- **claudecli** —— Claude Code 自己的 `claude` 二进制处理限制。Rousseau 只是 shell 出。

失败的请求以 `turn.failed`、`whatsapp.handler_failed` 或 `cron.run_failed` slog 事件浮现。消息文本会包括 provider 的错误字符串（通常是 `429 Too Many Requests` 及建议的退避）。

## 当您真的触发限制时

日志中的症状：

```jsonl
{"level":"ERROR","msg":"whatsapp.handler_failed","err":"anthropic: complete: 429 Too Many Requests"}
```

由于 rousseau 在遇到不可恢复错误时把该轮次视作失败，运维会在传输回复中看到失败 —— 守护进程不会静默吞掉。这是有意的。

## 降低速率限制压力

三个杠杆，按影响顺序排列：

### 1. 提示缓存标记（Anthropic direct）

`internal/llm/anthropic/client.go` 中的 `applyCacheMarkers` 会为 Anthropic 短时提示缓存标记消息的一个前导窗口。当 `CacheableMessages > 0` 时，系统提示也会被缓存标记。缓存输入 token 大约按标准输入费率的 10% 计费，缓存命中不消耗标准输入速率限制预算。

代理（`internal/agent/agent.go`）在多轮次会话中会选择启用它。如果您在 rousseau 的 Go API 之上构建自定义循环，请设置 `Request.CacheableMessages` 与 `Request.System` —— 即便浅层缓存命中也能同时削减成本与速率限制压力。

如今缓存标记只在 Anthropic direct 下有效。Bedrock、Vertex 与 OpenAI 兼容 provider 会忽略它们。

### 2. 压缩

对于按 token 计费 provider（Anthropic direct、Bedrock、Vertex、OpenRouter）上的长会话，启用压缩：

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60      # 来自 CompressionConfig 默认值
    keep_recent: 8
```

`LLMCompressor`（`internal/agent/compressor.go`）在消息计数越过 `trigger_messages` 时，把会话最老的一段摘要为单条合成的用户消息，并原样保留最后 `keep_recent` 条消息。每轮 token 更少 = 速率限制压力更小。

压缩默认关闭，因为参考部署在订阅层使用 `claudecli`，那里不按 token 计费。

### 3. 更慢的 cron 频率

对于纯后台守护进程，把 cron 频率减半就把请求减半。`rousseau cron` 频率是 cron 表达式 —— 如果新鲜度要求允许，可从每 15 分钟改为每小时。

## 各 provider 的近似成本

速率限制与按 token 成本各自独立，但通常相关（付费层限制更高）。截至 2026-07 的粗略指南：

| Provider | 输入 $/MTok（Sonnet 级） | 输出 $/MTok | 缓存读取 $/MTok |
|---|---|---|---|
| `anthropic` direct | ~3 | ~15 | ~0.30 |
| `bedrock` (Sonnet-4.6) | ~3 | ~15 | 撰写时缓存：N/A |
| `vertex` (Anthropic on Vertex) | ~3 | ~15 | 撰写时缓存：N/A |
| `openrouter` | 视模型而定 | 视模型而定 | 视 provider 而定 |
| `ollama` 自托管 | $0 | $0 | $0（您承担算力） |
| `claudecli` | 订阅层计费 | 含 | N/A |

请从各 provider 的定价页获取当前数字。

## 当 SDK 用尽重试时

如果 provider 的 SDK 放弃，rousseau 会浮现最终错误。该轮次丢失 —— 没有队列，也没有磁盘上的重试。两种缓解：

- **通过同一通道消息通知运维。** 传输回复中可见轮次失败；运维可以重述。
- **手动回退到第二个 provider。** 双守护进程模式见 [指南：多 provider](/zh-Hans/guides/multi-provider/)。

跨 provider 的自动故障转移是路线图项。

## 调试速率限制问题

1. 在 `config.yaml` 中设置 `log.level: debug`。SDK 调试输出会显示确切的 `Retry-After` 值。
2. 在日志中查找 `turn.failed`、`whatsapp.handler_failed`、`cron.run_failed`。
3. 在 provider 仪表盘（Anthropic Console、AWS CloudWatch、GCP Cloud Monitoring）中检查实际配额消耗。
4. 如果您在订阅层，请关注每日配额重置 —— SDK 错误通常包括重置时间。

## 各 provider 快速参考

<aside class="admonition" data-type="warning"><span class="admonition-title">注明来源</span><p>定价与限制会不加通知地变化。表中数字为 2026 年中期时的说明性数字。始终链接到 provider 的当前定价页以获取权威值。</p></aside>

| Provider | 重试行为 | 速率信号 | 每 1M 输入成本 | 每 1M 输出成本 | 缓存读取成本 |
|---|---|---|---|---|---|
| `anthropic` direct | SDK 重试 5xx；遵守带 `Retry-After` 的 429 | `429 Too Many Requests` 头携带重置时间 | ~$3 (Sonnet) | ~$15 (Sonnet) | ~$0.30 |
| `bedrock` | AWS SDK 自适应重试 | `ThrottlingException` | ~$3 (Sonnet) | ~$15 (Sonnet) | 尚无 |
| `vertex` | Google SDK 指数重试 | `429 RESOURCE_EXHAUSTED` | ~$3 (Sonnet) | ~$15 (Sonnet) | 尚无 |
| `openai` | SDK 重试 5xx；遵守 429 | `429 Too Many Requests` | 视模型而定 | 视模型而定 | 视模型而定 |
| `openrouter` | 透传给底层 provider | 视 provider 而定 | 视模型而定 | 视模型而定 | 视 provider 而定 |
| `ollama` | SDK 重试；本地几乎不触发 | 无 | $0（算力成本） | $0（算力成本） | N/A |
| `claudecli` | 子进程错误浮现；rousseau 侧无重试 | 不透明 | 订阅 | 订阅 | 不透明 |

权威来源：

- [Anthropic pricing](https://www.anthropic.com/pricing)
- [AWS Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)
- [Vertex AI pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing)
- [OpenAI pricing](https://openai.com/pricing)
- [OpenRouter model list](https://openrouter.ai/models)

## 调用方侧重试配方

Rousseau 在 `Complete` 内部不做重试。如果您嵌入代理库，用您自己的带指数退避与抖动的重试循环包装 `Turn`：

```go
func retryTurn(ctx context.Context, ag *agent.Agent, sess *agent.Session, maxRetries int) (agent.Message, error) {
    var lastErr error
    for attempt := 0; attempt < maxRetries; attempt++ {
        m, err := ag.Turn(ctx, sess)
        if err == nil {
            return m, nil
        }
        if !isRateLimit(err) {
            return agent.Message{}, err // 不可重试
        }
        lastErr = err
        // 带抖动的指数退避：1s、2s、4s、8s、……
        backoff := time.Duration(1<<attempt) * time.Second
        jitter := time.Duration(rand.Int63n(int64(backoff / 2)))
        select {
        case <-time.After(backoff + jitter):
        case <-ctx.Done():
            return agent.Message{}, ctx.Err()
        }
    }
    return agent.Message{}, fmt.Errorf("giving up after %d retries: %w", maxRetries, lastErr)
}

func isRateLimit(err error) bool {
    s := err.Error()
    return strings.Contains(s, "429") || strings.Contains(s, "rate limit") || strings.Contains(s, "ThrottlingException")
}
```

## 故障排除

### 每次请求都是 `429 Too Many Requests`

您处于低层级，或另一个工作负载正消耗配额。选项：(1) 申请提升限制，(2) 在多 provider 之间拆分负载，(3) 对仅订阅型工作负载运行 `claudecli`。

### 间歇性 `529 Overloaded`

Anthropic 系统已达容量。不是账户级别的限流 —— 整个区域都在负载。带退避重试。

### 已设缓存标记但看不到成本节省

确认 `CacheableMessages` 确实已设。`internal/llm/anthropic/cache.go` 中的 `applyCacheMarkers` 在为零时是 no-op。也要确认前缀是稳定的 —— 每轮重新生成的系统提示会破坏缓存。

### 低量下 Bedrock 出现 `ThrottlingException`

Bedrock 配额是按账户、按模型、按区域计的。有些模型的默认配额非常低（每分钟 2–5 次请求）。在 Service Quotas 控制台申请提升。

### 使用量很低但 API 响应慢

一些 provider 在全局负载下会降低低层级账户的优先级。Anthropic 的 `x-ratelimit-*` 响应头指示当前 bucket 状态 —— 如果您有 SDK 访问权限就检查它们。

## 相关页面

- [Providers：Anthropic](/zh-Hans/providers/anthropic/) —— 缓存标记细节。
- [配置](/zh-Hans/configuration/) —— 每个压缩旋钮。
- [用户指南：压缩 + 回忆](/zh-Hans/user-guide/compression-recall/) —— 更深入的压缩讨论。
- [指南：多 provider](/zh-Hans/guides/multi-provider/) —— 在端点之间拆分负载。
- [指南：速率/模型互换](/zh-Hans/guides/rate-model-swap/) —— 在失败时热切换 provider。

## 延伸阅读

- `internal/llm/anthropic/client.go` —— SDK 调用。
- `internal/llm/anthropic/cache.go` —— 缓存标记助手。
- `internal/agent/agent.go` —— 轮次失败浮现之处。
- 以上所链接的 provider 定价页。
