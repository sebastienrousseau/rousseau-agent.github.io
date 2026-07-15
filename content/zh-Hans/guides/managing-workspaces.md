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
description: "How rousseau's session store partitions by workspace, how to switch workspaces, share sessions across machines, and drop a workspace's history."
keywords: "workspace, session store, state path, sync, rsync, XDG_DATA_HOME"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/managing-workspaces/"
subtitle: "Partition state per project, share history across machines, drop history cleanly."
tags: "guides, workspace, session store, sqlite"
title: "指南：工作区管理"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "workspace, session store, state path, sync, rsync, XDG_DATA_HOME"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：工作区管理"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 38
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/managing-workspaces/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/managing-workspaces/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "指南：工作区管理"
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
twitter_description: "How rousseau's session store partitions by workspace, how to switch workspaces, share sessions across machines, and drop a workspace's history."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "指南：工作区管理"
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

## 约定

Rousseau 没有一等公民的"工作区"概念。它在 `internal/config/config.go`（`StateConfig`）中有一个 `state.path`，默认把每个进程指向 `~/.local/share/rousseau/sessions.db`。所有会话、cron 任务、JID 映射与 FTS5 回忆索引都在那一个文件中。

对大多数运维来说这正合适。想要隔离时 —— 按项目、按机器、按客户 —— 把 rousseau 指向不同的 SQLite 文件。那个文件**就是**工作区。

## 按调用切换工作区

两个旋钮，任一都可以：

```sh
# 1. 任何 rousseau 命令上的 flag
rousseau --config ~/.config/rousseau/acme.yaml chat

# 2. 环境变量（Viper 通过 ROUSSEAU_STATE_PATH 拾取）
ROUSSEAU_STATE_PATH=~/.local/share/rousseau/acme.db rousseau chat
```

在工作区之间切换时两种方式都不需要重启 rousseau —— 每个进程打开自己的文件。

## 按项目的工作区布局

```
~/.config/rousseau/
├── acme.yaml         # provider = anthropic, state.path = …/acme.db
├── personal.yaml     # provider = claudecli, state.path = …/personal.db
└── work.yaml         # provider = bedrock,    state.path = …/work.db
```

每个配置文件覆盖 `state.path`：

```yaml
state:
  path: /home/seb/.local/share/rousseau/acme.db
```

然后用正确的配置启动每个会话。TUI（`internal/tui/model.go`）在其状态栏显示会话 id + provider —— 直观确认您在正确的工作区。

## 跨机器共享历史

会话存储是单个 SQLite 文件。`internal/state/sqlite/store.go` 中的 `Open()` 启用了 WAL journaling，因此热快照是安全的：

```sh
# 从笔记本快照到桌面（都处于空闲）
rsync -avz --partial \
  ~/.local/share/rousseau/sessions.db \
  desktop:~/.local/share/rousseau/sessions.db
```

**同一时刻只能有一个写入者。** 不要在两台机器上通过 NFS 对同一 SQLite 文件运行 `rousseau whatsapp` —— 那是未定义的。在无人写入时同步，或者以单写入者加读副本方式运行。

一个更安全的替代是 `.backup` 快照：

```sh
sqlite3 ~/.local/share/rousseau/sessions.db ".backup '/tmp/sessions.snap.db'"
scp /tmp/sessions.snap.db desktop:~/.local/share/rousseau/sessions.db
```

`.backup` 使用 SQLite 的在线备份 API，产出一个一致的时间点文件。

## 迁移工作区

把整个目录移动；那就是工作区：

```sh
rsync -avz ~/.local/share/rousseau/ new-host:~/.local/share/rousseau/
```

`whatsapp.db`（设备凭据）是独立的 —— 您要么也带上（设备保持配对），要么留下它，在新主机上重新扫描 QR。

## 丢弃某个工作区的历史

```sh
rousseau session list                 # 确认您即将失去的内容
rm ~/.local/share/rousseau/acme.db*   # 包括 -wal 与 -shm 侧车
```

下一个打开该路径的进程会用 `internal/state/sqlite/schema.sql` 中的 schema 重新创建它。

如果您只想丢弃部分会话，使用 CLI：

```sh
rousseau session delete <id> --yes
```

`rousseau session delete`（`internal/cli/session.go`）调用 `Store.Delete`，通过 FTS5 触发器级联以保持回忆索引一致。必须带 `--yes` flag —— 没有它命令拒绝运行。

## 通过 SQL 部分删除

对于批量清理 —— 每个早于 90 天的会话：

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions WHERE updated_at < datetime('now', '-90 days');
SQL
```

FTS5 触发器（`internal/state/sqlite/search.go` 中的 `sessions_fts_ad`）在 DELETE 上触发，自动保持索引同步。

## 每个工作区的审批器

由于配置文件与状态文件都是按工作区的，审批器也是：

```yaml
# work.yaml —— 严格的 pattern 审批器
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

state:
  path: /home/seb/.local/share/rousseau/work.db
```

一份单独的 `personal.yaml` 可能为交互式工作保留 `mode: allow_all`。见 [教程：加固审批器](/zh-Hans/tutorials/harden-approver-policy/)。

## 相关

- [参考：会话存储](/zh-Hans/reference/session-store/) —— schema。
- [指南：多 provider](/zh-Hans/guides/multi-provider/) —— 双配置双 provider 模式。
- [参考：环境变量](/zh-Hans/reference/environment-variables/) —— 每个路径环境变量。
- [用户指南：CLI](/zh-Hans/user-guide/cli/) —— `rousseau session` 命令。
