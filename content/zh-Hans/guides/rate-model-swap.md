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
description: "Hot-swap the underlying model mid-session by editing config.yaml and restarting the daemon — the SQLite session store survives."
keywords: "model swap, hot swap, mid-session, restart, session store, sonnet, opus, haiku"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/rate-model-swap/"
subtitle: "Swap Sonnet for Opus mid-session; the session store survives the restart."
tags: "guides, model, swap, restart, session"
title: "指南：热切换模型"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "model swap, hot swap, mid-session, restart, session store, sonnet, opus, haiku"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：热切换模型"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/rate-model-swap/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/rate-model-swap/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "指南：热切换模型"
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
twitter_description: "Hot-swap the underlying model mid-session by editing config.yaml and restarting the daemon — the SQLite session store survives."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "指南：热切换模型"
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

## 为什么可行

Rousseau 在进程启动时从 `config.yaml` 读取一次它的 provider 与模型（`internal/config/config.go` 中的 `config.Load`）。会话状态在 SQLite 中。更换模型意味着编辑配置、重启守护进程，让下一条入站消息被新模型处理 —— 而先前模型参与过的每一个会话在 `sessions.db` 中都保持不变。

会话存储没有绑定到某个特定模型。`payload` 列（`internal/state/sqlite/schema.sql`）是 `agent.Session` 的普通 JSON blob；包含角色、内容、tool-use 块。任何说 Anthropic 内容块约定（或通过 `internal/llm/*/client.go` 中 SDK 适配器适配）的模型都能从上一个模型停下的地方接手。

## 在同一 provider 内互换

简单情形。编辑模型字段：

```yaml
# 之前：
anthropic:
  model: claude-sonnet-4-6

# 现在：
anthropic:
  model: claude-opus-4-6
```

重启：

```sh
systemctl --user restart rousseau-agent
# 或者，如果您在交互式运行 rousseau chat，退出并重新启动
```

发送下一条消息。回复来自 Opus；会话上下文不变。

## 跨 provider 互换

略微涉及更多，因为内容块形状各异。Rousseau 的适配器（`internal/llm/anthropic/client.go`、`internal/llm/openai/client.go`）在每一轮通过 SDK 的原生类型往返 `agent.Message` 值。这意味着：

- **`claudecli` → `anthropic`** —— 干净互换。两者使用相同的内容块形状。
- **`claudecli` → `bedrock` / `vertex`** —— 干净互换。Bedrock 上的 Anthropic 与 Vertex 上的 Anthropic 说相同的消息格式。
- **Anthropic 家族 → `openai` / `openrouter` / `ollama`** —— tool-use 块会被重塑为 OpenAI 的 function-call 格式。会话中之前的 tool_use / tool_result 对通过适配器往返。对于文本应无缝；边界情形（单轮多工具使用、流式部分内容）可能渲染有异。

如果会话有大量的 tool-use 历史且您在跨越 provider 家族，请先用一个新会话测试。

## 换部署 provider 而不动状态

同一会话存储，不同的守护进程配置：

```sh
cp ~/.config/rousseau/config.yaml ~/.config/rousseau/config.yaml.bak
$EDITOR ~/.config/rousseau/config.yaml   # 更改 provider + 模型
systemctl --user restart rousseau-agent
```

`state.path` 没有变，所以 JID→会话 映射（`internal/state/sqlite/jidmap.go` 中的 `jid_sessions` 表）仍然为每个 WhatsApp / Slack / Matrix 发送者指向同一条对话历史。

## 什么被保留

| 状态 | 重启后存活 | 说明 |
|---|---|---|
| 会话对话稿 | 是 | `sessions` 表。 |
| FTS5 回忆索引 | 是 | `sessions_fts` 虚拟表。回填时重新分词。 |
| JID → 会话映射 | 是 | `jid_sessions` 表。 |
| Cron 任务 | 是 | `cron_jobs` 表。 |
| WhatsApp 设备配对 | 是 | `whatsapp.db`（独立文件）。 |
| Anthropic 提示缓存命中 | **否** | 缓存按端点分。新模型或端点从冷启动开始。 |

## 什么丢失

Anthropic 提示缓存标记（`internal/llm/anthropic/client.go` 中的 `applyCacheMarkers`）位于模型的短时缓存内 —— 它们不会跨模型或 provider 的重启持久化。互换后接下来的几轮支付完整输入 token；后续轮次重建缓存。为成本预算了解这一点是有价值的，但对正确性无关。

## 何时互换 vs 从头开始

就地互换的时机：

- 会话值得保留，且内容以文本为主。
- 模型处于同一家族（都是 Anthropic，或通过 Bedrock/Vertex）。
- 您接受一次性的缓存未命中。

从头开始的时机：

- 会话有您不想让更聪明模型追逐的过时上下文。
- 您在跨越 provider 家族并想要确定性行为。
- token 计数无论如何都在压缩触发点 —— 一次搞定压缩与互换。

## 互换后测试

```sh
rousseau session list | head -3
rousseau session show <id> | tail -20
# 在 TUI 中或通过传输：
> what did we just decide about X?
```

如果回复连贯地引用了之前的对话，互换就在工作。如果模型为"没有上下文"道歉或者重复自己，适配器往返可能在丢失 tool-use 元数据 —— 提交 bug 或回退到先前模型。

## 相关

- [Providers](/zh-Hans/providers/) —— 每个支持的 provider。
- [配置](/zh-Hans/configuration/) —— 确切字段名。
- [指南：速率限制](/zh-Hans/guides/rate-limits/) —— 缓存标记讨论。
- [指南：会话管理](/zh-Hans/guides/session-management/) —— 完整生命周期。
