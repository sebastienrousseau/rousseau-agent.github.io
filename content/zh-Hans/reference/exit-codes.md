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
description: "Exit codes and signal semantics for the rousseau-agent binary. What init systems can rely on."
keywords: "exit codes, signals, sigterm, sigint, systemd, restart policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/reference/exit-codes/"
subtitle: "Exit codes and signal semantics."
tags: "reference, exit-codes, signals"
title: "退出码"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "exit codes, signals, sigterm, sigint, systemd, restart policy"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "退出码"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 51
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/reference/exit-codes/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/exit-codes/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "退出码"
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
twitter_description: "Exit codes and signal semantics for the rousseau-agent binary. What init systems can rely on."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "退出码"
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

## 退出码

Rousseau 的 CLI 刻意保守 —— 两个退出码覆盖每一条路径。

| 码 | 由谁发出 | 含义 |
|---|---|---|
| 0 | `cmd/rousseau/main.go` 经由 `cli.Execute` | 命令成功完成。守护进程在优雅关停（SIGINT / SIGTERM）时以 0 退出。 |
| 1 | `cmd/rousseau/main.go` 经由 `cli.Execute` | 命令失败。错误字符串会打印到 stderr。每一种失败 —— 配置解析错误、provider 认证失败、传输 panic、工具接线错误 —— 都会映射到该码。 |

`rousseau doctor` 遵循同一惯例：所有检查通过时退出 0，任何一个检查为 `fail` 时退出 1。警告和 info 级别的行不影响退出码。

未来 release 可能会将失败拆分为不同的码（配置、运行时、网络）。目前，把任何非零退出视为可重试但需要日志检查。

## 信号处理

`cmd/rousseau/main.go` 安装了一个信号处理器，在 `SIGINT` 和 `SIGTERM` 时取消根 `context.Context`。每个长生命周期组件（代理循环、传输、cron 调度器、MCP 服务器）都会遵循 context 取消，因此关停路径是：

1. 收到 `SIGINT` / `SIGTERM`。
2. 根 context 被取消。
3. 传输对自己调用 `Stop()`，冲刷正在传输中的消息。
4. Cron 调度器停止接受新的触发；正在运行的触发完成。
5. 经由 `defer` 调用会话存储的 `Close()`，checkpoint WAL。
6. `Execute` 返回 0。

`SIGKILL` 无法被捕获。若在轮次中间对守护进程执行 `kill -9`，会话存储的 WAL 可防止损坏，但正在进行的轮次不会被持久化。下次启动会从上一次保存的状态恢复。

## systemd 重启策略

参考 Quadlet 单元采用：

```
[Service]
Restart=on-failure
RestartSec=10
```

`on-failure` 在任何非零退出时重启；结合 rousseau 的退出码惯例，意味着：退出 0（来自 `systemctl stop` 的 `SIGTERM`）不重启，退出 1 会重启。

对于持续遭遇错误（错误配置、错误 provider 认证）的守护进程，`on-failure` 会造成抖动。在假定重试循环能恢复之前，请先查看 `journalctl` 中的失败原因。

## Kubernetes 探针语义

出于设计，Rousseau 不提供 HTTP liveness/readiness 端点。Kubernetes 探针必须是：

- 运行 `rousseau doctor --config /etc/rousseau/config.yaml` 的 `exec` 探针（健康时返回 0，失败时返回 1），或
- 无探针，pod 依赖 `restartPolicy: Always` 与守护进程自身的错误处理。

`rousseau doctor` 开销很低（~50ms），因此适合做 liveness 探针。不要把它做成 readiness 探针 —— 如果失败无法自愈，`provider.claudecli.binary` 上的 `fail` 不应把 pod 从轮转中撤下。

## 已处理的错误

经由 CLI 错误面产生退出码 1 的错误包括：

- **配置加载失败** —— YAML 解析错误、未知字段、无效类型。
- **Provider 认证失败** —— 缺失 API 密钥、无效凭据、无效 Bedrock / Vertex 区域。
- **传输启动失败** —— 缺失 token、IMAP/SMTP 主机不可达、whatsmeow 协议错误。
- **存储打开失败** —— `~/.local/share/rousseau/` 权限拒绝、磁盘已满。
- **Doctor 检查失败** —— 任一 `fail` 行都会让 doctor 返回退出 1。
- **Cron 表达式解析失败** —— `rousseau cron add` 在持久化前校验。

## 未处理的 panic

`go test -race` 在每次 CI 构建中运行，因此 panic 极为罕见。当发生时，Go 运行时会将 panic + 堆栈跟踪打印到 stderr，并以运行时返回的非零码退出 —— 通常为 2，但这是 Go 的惯例，rousseau 无法控制。

生产环境请用一个 supervisor 包裹守护进程，在异常退出时捕获 stderr 并报告堆栈。

## 下一步

- [用户指南：CLI](/zh-Hans/user-guide/cli/) —— 每个命令。
- [指南：可观测性](/zh-Hans/guides/observability/) —— 让 slog 信号超越退出码。
- [故障排除](/zh-Hans/troubleshooting/) —— 当退出码不足以说明问题时怎么办。
