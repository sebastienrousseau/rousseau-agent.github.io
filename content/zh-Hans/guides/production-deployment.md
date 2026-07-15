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
description: "Beyond the Quadlet reference: log shipping, session-store backup, health checks, rolling restarts, and multi-transport coexistence."
keywords: "production, log shipping, backup, health check, rolling restart, systemd"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/production-deployment/"
subtitle: "Everything the Quadlet reference doesn't already cover."
tags: "guides, production, deployment, backup, logs, health check"
title: "指南：生产部署"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "production, log shipping, backup, health check, rolling restart, systemd"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：生产部署"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/production-deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/production-deployment/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "指南：生产部署"
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
twitter_description: "Beyond the Quadlet reference: log shipping, session-store backup, health checks, rolling restarts, and multi-transport coexistence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "指南：生产部署"
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

## 请在此之后阅读

`docker/rousseau-agent.container` 的参考 Quadlet 单元覆盖"如何运行 rousseau"的故事。本指南覆盖您在称其为生产之前需要在它周围加什么：日志、备份、健康与进程卫生。

## 日志转运

Rousseau 通过 `log/slog`（`internal/cli/root.go`）向 stderr 写入结构化日志。在 systemd 下运行时，该 stderr 落入 journal。转运出主机的选项：

| 工具 | 适配 | 说明 |
|---|---|---|
| Vector（`vector.dev`） | 最佳默认。 | `journald` 源 + 一个丢弃 DEBUG 的过滤器。发到 Loki、Datadog、S3，随您意。 |
| Promtail + Loki | 如果您已经运行 Grafana。 | Loki 的 `journal` 源直接对着 `journalctl -o json` 工作。 |
| Datadog Agent | 如果 Datadog 是组织标准。 | DD agent 有一个 journald 尾追。结构化 JSON 原生解析。 |
| Fluent Bit | 小体积替代方案。 | 在 `config.yaml` 中设置 `log.format: json`；Fluent Bit 的 `systemd` 输入解析。 |

在生产环境中无条件配置 `log.format: json`（`internal/config/config.go` 的 `LogConfig.Format`）。文本输出为 `less` 设计，而不是为机器解析。

完整 Loki 管道配方见 [指南：可观测性](/zh-Hans/guides/observability/)。

## 会话存储备份

状态目录 `~/.local/share/rousseau/` 是 rousseau 拥有的唯一持久状态。每晚备份它。

两种方式：

**1. SQLite `.backup`（推荐）。**

```sh
sqlite3 ~/.local/share/rousseau/sessions.db \
  ".backup '/backup/sessions.db.$(date +%Y%m%d).bak'"
sqlite3 ~/.local/share/rousseau/whatsapp.db \
  ".backup '/backup/whatsapp.db.$(date +%Y%m%d).bak'"
restic backup /backup
```

`.backup` 使用 SQLite 的在线 API —— 即使守护进程在写入也安全。见 [参考：会话存储](/zh-Hans/reference/session-store/)。

**2. 文件系统快照。**

由于 WAL journaling 开启（`internal/state/sqlite/store.go` 中的 `Open()`），`restic` 与 `borg` 可以在守护进程运行时快照原始文件。WAL 保证一个一致的时间点镜像。

不要：

- 在守护进程运行时用 `cp` 复制 `.db` 文件，除非您同时复制 `-wal` 与 `-shm`。
- 把备份存在同一块盘。
- 跳过 WhatsApp 设备凭据文件 —— 丢失它意味着重新扫描 QR。

## 健康检查

`rousseau status`（`internal/cli/status.go`）在健康时退出 0，出问题时非零。把它用作 systemd 健康探针：

```ini
[Service]
ExecStartPost=/usr/bin/timeout 30 podman exec rousseau-agent rousseau status
```

对于更丰富的探针，脚本一个检查：

1. 运行 `rousseau status`。
2. 确认会话存储的最后写入是近期的（`stat sessions.db -c %Y` 与当前时间比较）。
3. 通过 `podman inspect` 检查容器的运行时长。

Rousseau 不暴露 HTTP `/healthz`。如果您的平台需要一个（Kubernetes readiness 探针），见 [指南：Kubernetes 部署](/zh-Hans/guides/kubernetes-deployment/) —— 您把 rousseau 包在一个小的、对 `curl` 友好的 sidecar 中。

## 滚动重启

由于状态是单个 SQLite 文件，守护进程真正意义上是单实例。一次滚动重启是：停止、替换镜像、启动。无需预热。

```sh
podman pull localhost/rousseau-agent:local     # or rebuild locally
systemctl --user restart rousseau-agent
podman logs -n 50 rousseau-agent | grep -E 'starting|connected'
```

预期日志序列（来自 `internal/transport/whatsapp/client.go`）：

```
INFO whatsapp.starting store=… allowlist=1
INFO whatsapp.connected
```

如果守护进程在约 15 秒内没有发出 `whatsapp.connected`，回滚。

## 一台主机上的多个传输

您可能想让 WhatsApp 与 Slack 共享同一个会话存储。两种方式：

- **多个 Quadlet 单元** —— 每个传输一个，各自指向相同的 `state.path`。WAL + `busy_timeout`（见 `internal/state/sqlite/store.go` 中的 `Open()`）让并发写入者安全。
- **一份二进制，每次调用一个传输。** Rousseau 的传输命令是单传输的（`whatsapp`、`slack`、`signal`、……）。要运行两个传输就运行两个进程。

## 零停机配置变更

Rousseau 不热重载 `config.yaml`。配置变更需要重启。`SIGHUP` 没有接线到重载。

实用工作流：

1. 编辑 `~/.config/rousseau/config.yaml`。
2. `systemctl --user restart rousseau-agent`。
3. 从日志核实。

对大多数传输，重新连接很快（约 1–3 秒）。主要停顿在 WhatsApp 上，whatsmeow 会重新建立 websocket。

## 日志保留

`journald` 保留由 `/etc/systemd/journald.conf` 中的 `SystemMaxUse=` 设定。对于对审计友好的部署，把日志转运出主机，并把本地磁盘上的 journald 设为较短保留（例如 7 天），这样审计轨迹存在于 Loki/S3 中，而不是入侵者可能轮换的文件系统上。

## 容器镜像生命周期

对您想采用的每次 rousseau release 重建镜像：

```sh
cd ~/rousseau-agent
git pull
podman build -t rousseau-agent:local -f docker/Dockerfile .
systemctl --user restart rousseau-agent
```

Quadlet 的 `AutoUpdate=disabled` 行（在 `docker/rousseau-agent.container` 中）阻止 `podman auto-update` 触碰该容器。您控制更新节奏。

## 相关

- [部署](/zh-Hans/deployment/) —— 参考 Quadlet 单元。
- [教程：部署到 VPS](/zh-Hans/tutorials/deploy-to-a-vps/) —— 可行示例。
- [指南：可观测性](/zh-Hans/guides/observability/) —— 日志管道。
- [指南：企业接入](/zh-Hans/guides/enterprise-onboarding/) —— 完整清单。
