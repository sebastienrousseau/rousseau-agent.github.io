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
description: "Run two rousseau daemons with different providers side-by-side — e.g. claudecli for interactive chat and Bedrock for scheduled reports."
keywords: "multi provider, claudecli, bedrock, config precedence, XDG_CONFIG_HOME"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/multi-provider/"
subtitle: "Two daemons, two providers, one operator."
tags: "guides, providers, multi-provider, deployment"
title: "指南：多提供方"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "multi provider, claudecli, bedrock, config precedence, XDG_CONFIG_HOME"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：多提供方"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 35
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/multi-provider/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/multi-provider/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "指南：多提供方"
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
twitter_description: "Run two rousseau daemons with different providers side-by-side — e.g. claudecli for interactive chat and Bedrock for scheduled reports."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "指南：多提供方"
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

## 为什么您可能需要这个

Rousseau 的 `provider` 字段是单一标量（`internal/config/config.go` 的 `Config.Provider`）。单个 rousseau 进程只与一个 provider 通话。当您需要不止一个时 —— 最常见的是 `claudecli` 用于交互式 TUI（因为它继承 OAuth 会话），以及付费 API provider（Bedrock、Anthropic direct、Vertex）用于后台守护进程（订阅层 `claude` OAuth 在此处不便）—— 您用不同的配置文件运行**两个 rousseau 进程**。

合理的搭配：

| 交互式 | 无人值守 | 为什么 |
|---|---|---|
| `claudecli` | `anthropic` 或 `bedrock` | 笔记本聊天用 OAuth，VPS 守护进程用 API key。 |
| `claudecli` | `vertex` | 同样，只是在 GCP 上。 |
| `anthropic` | `openai` 或 `ollama` | 比较答案，或为 cron 回退到更便宜/本地的模型。 |
| `claudecli` | `openai`（OpenRouter） | TUI 用 Claude，定时摘要用便宜的 OpenRouter 模型。 |

## Rousseau 如何解析配置

`config.Load`（在 `internal/config/config.go` 中）按 flag > env > 文件 > 默认 的顺序应用。它读取的文件默认是 `~/.config/rousseau/config.yaml`，但根命令（`internal/cli/root.go`）上的持久 `--config` flag 会覆盖它。这给了您一个干净的分割。

## 双配置布局

```sh
mkdir -p ~/.config/rousseau
cat > ~/.config/rousseau/chat.yaml <<'YAML'
provider: claudecli
claudecli:
  binary: claude
log:
  level: info
  format: text
YAML

cat > ~/.config/rousseau/cron.yaml <<'YAML'
provider: bedrock
bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
log:
  level: info
  format: json
YAML
```

用正确的文件运行每个命令：

```sh
rousseau --config ~/.config/rousseau/chat.yaml chat
rousseau --config ~/.config/rousseau/cron.yaml whatsapp --allow YOUR_JID@s.whatsapp.net
```

## 共享 vs 分区状态

两个进程默认都指向同一个 SQLite 会话存储（`~/.local/share/rousseau/sessions.db`）—— 这通常正是您想要的，让 WhatsApp 桥与您的 TUI 聊天共享历史。

要完全分区状态，按配置覆盖 `state.path`：

```yaml
state:
  path: /home/seb/.local/share/rousseau/chat.db
```

由于 `internal/state/sqlite/store.go` 中的 `Open()` 启用了 WAL journaling 与 15 秒的 `busy_timeout`，跨进程的 SQLite 访问是安全的。

## systemd 接线

两个 Quadlet 单元，每个配置一个。每个单元的 `Exec=` 包括 `--config /home/rousseau/.config/rousseau/<name>.yaml`：

```ini
Exec=--config /home/rousseau/.config/rousseau/cron.yaml whatsapp --allow ...
```

基础单元见 [部署](/zh-Hans/deployment/)。

## 每个配置的审批策略

不同 provider 值得不同审批。交互式 `claudecli` 可以安全保持 `mode: allow_all`，因为 Claude Code 有自己的每次调用审批 UI。Bedrock/Anthropic 守护进程应运行 `mode: pattern` + `default: deny`。把它们各自放在自己的 YAML 下。

## 测试

确认每个进程与正确的端点通话：

```sh
# 交互式在 strace / lsof 中显示 claudecli 子进程路径
lsof -c rousseau | grep -E 'claude|CLAUDE'

# 后台显示到 bedrock-runtime.<region>.amazonaws.com 的出站 HTTPS
ss -tanp | grep rousseau
```

## 这不给您什么

- **不做每请求路由。** Rousseau 不会在单个轮次内从一个 provider 回退到另一个。已配置 provider 的失败以 `whatsapp.handler_failed` / `turn.failed` 浮现，模型不会针对不同 provider 重试。那是路线图项。
- **不做共享缓存。** Anthropic 提示缓存（见 `internal/llm/anthropic/client.go` 中的 `applyCacheMarkers`）按端点分。Anthropic direct 下的命中不会算作 Bedrock 下的命中，即便是同一模型家族。

## 相关

- [Providers](/zh-Hans/providers/) —— 全部五种 provider 类型的比较。
- [配置](/zh-Hans/configuration/) —— 每个旋钮。
- [参考：环境变量](/zh-Hans/reference/environment-variables/) —— 基于环境变量的覆盖。
- [指南：生产部署](/zh-Hans/guides/production-deployment/)。
