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
description: "Set up rousseau-agent's Signal transport: signal-cli subprocess in JSON-RPC mode, account registration out-of-band, E.164 allowlist, extra_args knob."
keywords: "Signal, signal-cli, JSON-RPC, subprocess, E.164, account registration, linked device"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/transports/signal/"
subtitle: "signal-cli subprocess in JSON-RPC daemon mode."
tags: "transports, Signal"
title: "Signal 传输"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Signal, signal-cli, JSON-RPC, subprocess, E.164, account registration, linked device"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Signal 传输"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 13
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/transports/signal/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/signal/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Signal 传输"
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
twitter_description: "Set up rousseau-agent's Signal transport: signal-cli subprocess in JSON-RPC mode, account registration out-of-band, E.164 allowlist, extra_args knob."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Signal 传输"
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

## 概述

Signal 传输（`internal/transport/signal/`）通过 shell 调用 `signal-cli`（https://github.com/AsamK/signal-cli）的 JSON-RPC 守护模式。

`signal-cli --output=json -a <account> jsonRpc` 会在 stdin/stdout 上流式传输 JSON-RPC 2.0：出站 `send` 请求用于发送消息；入站到达的消息以 `receive` 通知形式到达。

## 先决条件

rousseau 与 Signal 通信之前必须具备两项前提：

1. **`signal-cli` 已在 `$PATH` 中**（或显式配置 `binary` 值）。
2. **账户已在带外完成注册或链接。**

账户注册刻意不在 rousseau 的职责范围之内。（参考 `signal-cli` 文档）支持两种方式：

- **注册新号码。** `signal-cli register` 会启动 SMS 或语音验证。用 `signal-cli verify <code>` 完成验证。号码最终归守护进程所有。
- **作为副设备链接。** `signal-cli link` 会打印一个 `tsdevice://` URI；在移动端 Signal 应用的 **设置 → 已链接的设备** 里扫描该链接。号码仍归手机所有；守护进程作为副设备工作。

这两种流程都会将状态持久化在 `~/.local/share/signal-cli/` 下。如果在 Podman 中部署，请将该目录挂载进容器。

## 配置

```yaml
signal:
  binary: signal-cli
  account: "+447900123456"
  extra_args:
    - --verbose
  reply_header: "*Rousseau Agent*\n\n"
  allowlist:
    - "+447900654321"
```

| 字段 | 默认值 | 作用 |
|---|---|---|
| `binary` | `signal-cli` | 要调用的可执行文件。 |
| `account` | *必填* | 守护进程使用的 E.164 电话号码。 |
| `extra_args` | `[]` | 插入到 `-a <account>` 与 `jsonRpc` 之间。用于 `--config <path>` 和 `--verbose`。 |
| `reply_header` | *空* | 前置到每条出站回复上。 |
| `allowlist` | `[]` | 允许处理消息的 E.164 号码。为空则接受所有发送者。 |

## 命令行

```sh
rousseau signal --account +447900123456 --allow +447900654321
```

命令行参数与配置块相对应。`--allow` 可重复使用。

## 消息流

- **入站。** `signal-cli` 每收到一条消息就发出一个 `receive` JSON-RPC 通知。rousseau 解析它，丢弃不在允许列表中的消息，然后将正文交给 `Handler`。
- **出站。** rousseau 向 `signal-cli` 的 stdin 写入一个 JSON-RPC `send` 请求。投递 ACK 会在同一通道上返回。

## 超时

该传输不会对子进程施加自身的超时。`signal-cli` 自己的网络层负责处理 Signal 服务器的重连。如果进程退出，rousseau 不会重启它 —— 参考 Quadlet 已经设置的 systemd `Restart=on-failure` 会重启整个 rousseau 守护进程，并连带重启 `signal-cli`。

## 失败模式

| 现象 | 解决方式 |
|---|---|
| `signal-cli` 立即退出 | 账户尚未注册或链接。请在带外完成注册。 |
| 从未收到 `receive` 通知 | 检查该账户是否被其他位置链接并在消费队列。 |
| JSON 解析错误 | 确认 `signal-cli` 版本为 0.13+。旧版本使用了不同的信封格式。 |
