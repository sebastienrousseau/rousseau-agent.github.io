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
description: "Rousseau's SQLite session store: sessions table, FTS5 recall index, JID mapping table, cron jobs, and WAL journaling."
keywords: "sqlite, fts5, session store, sessions, jid, cron, WAL, schema"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/reference/session-store/"
subtitle: "The SQLite schema at the heart of rousseau's state."
tags: "reference, sqlite, fts5, session, wal"
title: "参考：会话存储"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "sqlite, fts5, session store, sessions, jid, cron, WAL, schema"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "参考：会话存储"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 53
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/reference/session-store/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/session-store/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "参考：会话存储"
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
twitter_description: "Rousseau's SQLite session store: sessions table, FTS5 recall index, JID mapping table, cron jobs, and WAL journaling."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "参考：会话存储"
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

## 位置与驱动

会话存储是位于 `state.path` 的单一 SQLite 数据库（默认 `~/.local/share/rousseau/sessions.db`，参见 `internal/config/config.go` 中的 `setDefaults`）。

Rousseau 使用 `modernc.org/sqlite` —— 一个纯 Go SQLite 驱动。**不依赖 CGO 或 libsqlite3**。`bin/rousseau` 中的 Go 二进制是完全静态的。

`internal/state/sqlite/store.go` 的 `Open()` 在每次打开时应用四条 pragma：

| PRAGMA | 用途 |
|---|---|
| `journal_mode=WAL` | Write-ahead logging。允许并发读者、安全的在线备份。 |
| `foreign_keys=ON` | 标准完整性保障。 |
| `busy_timeout=15000` | 锁竞争时等待 15 秒 —— 一旦多个传输并发写入时至关重要。 |
| — | 随后 `EnsureSearch` 运行以安装 FTS5 schema。 |

存储在每个进程中打开一次。得益于 busy-timeout + WAL 组合，支持多个守护进程指向同一 DB 文件 —— WhatsApp 桥、`rousseau mcp` 和 `rousseau session list` 可以安全共享该文件。

## Schema 巡览

### 表：`sessions`

定义于 `internal/state/sqlite/schema.sql`：

```sql
CREATE TABLE IF NOT EXISTS sessions (
    id             TEXT PRIMARY KEY,
    title          TEXT NOT NULL,
    payload        TEXT NOT NULL,        -- JSON blob of the full agent.Session
    message_count  INTEGER NOT NULL DEFAULT 0,
    created_at     TEXT NOT NULL,
    updated_at     TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sessions_updated_at
    ON sessions(updated_at DESC);
```

**Payload 形态。** `payload` 列存储完整的 `agent.Session` JSON —— 角色、内容块、tool-use 与 tool-result 块、时间戳。参见 `internal/state/sqlite/store.go` 中的 `Save`/`Load`。将整个会话作为单个 JSON blob 保存可让 schema 迁移变得罕见；针对内部的查询走下方的 FTS5 索引。

**时间戳** 为 ISO-8601 毫秒精度（Go time 语法为 `2006-01-02T15:04:05.000Z`），UTC。

**排序。** `idx_sessions_updated_at` 为 `List` 与 `RecentSessions`（都位于 `store.go` / `search.go`）供能。

### 虚拟表：`sessions_fts`（FTS5）

由 `internal/state/sqlite/search.go` 的 `searchSchema` 安装：

```sql
CREATE VIRTUAL TABLE IF NOT EXISTS sessions_fts USING fts5(
    session_id UNINDEXED,
    title,
    body,
    tokenize = 'porter unicode61'
);
```

三个触发器驱动的写入使其与 `sessions` 保持一致：

- `sessions_fts_ai` —— 在 `sessions` INSERT 后，镜像该行。
- `sessions_fts_au` —— 在 UPDATE 后，删除 + 重新插入。
- `sessions_fts_ad` —— 在 DELETE 后，丢弃 FTS 行。

**回填。** `EnsureSearch` 在每次 `Open()` 时运行一次 `LEFT JOIN`，插入 FTS 索引尚未拥有的任何 `sessions` 行。这让索引可以安全地添加到既有数据库 —— 无需手动迁移。

**分词。** `porter unicode61` —— Porter 词干 + Unicode 感知的大小写折叠。大小写不敏感，处理英语形态（`retry`/`retries`/`retried`）。

**排名。** `Search()` 按 `bm25(sessions_fts)` 排序（更低更相关）。`SearchHit.Rank` 会暴露它。

**查询语法。** 原样透传给 FTS5。运维者速查表参见 [教程：通过 MCP 暴露工具](/zh-Hans/tutorials/expose-tools-via-mcp/)。

### 表：`jid_sessions`

持久化平台发送者到会话 id 的映射；由 `internal/state/sqlite/jidmap.go` 的 `NewJIDMap` 安装：

```sql
CREATE TABLE IF NOT EXISTS jid_sessions (
    jid         TEXT PRIMARY KEY,
    session_id  TEXT NOT NULL,
    created_at  TEXT NOT NULL
);
```

每个长生命周期传输都使用 JID 映射，以便同一个电话号码、Matrix 用户或 Slack 用户在重启之间接续同一会话。`Router.Handle`（`internal/transport/router.go`）在入站时查询它；`Put` 在 `Save` 之后写入。

JID 空间是传输相关的 —— WhatsApp 为 `447900123456@s.whatsapp.net`，Matrix 为 `@user:matrix.org`，Slack 为 `U01ABC…`。传输负责规范化。

### 表：`cron_jobs`

由 `internal/state/sqlite/cron.go` 的 `NewCronStore` 安装：

```sql
CREATE TABLE IF NOT EXISTS cron_jobs (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    cron_expr   TEXT NOT NULL,
    prompt      TEXT NOT NULL,
    deliver_to  TEXT NOT NULL,
    enabled     INTEGER NOT NULL DEFAULT 1,
    created_at  TEXT NOT NULL,
    last_run_at TEXT
);
```

`UNIQUE(name)` 防止重复。`rousseau cron add/list/remove/enable/disable`（源自 `internal/cli/cron.go`）都会通过此表往返。`internal/cron/scheduler.go` 的调度器每个 `poll_interval` 从中对账。MCP 通过 `rousseau_cron_list` 以只读方式暴露它。

## 并发姿态

- **WAL** 允许无限并发读者与单一写者并存。
- **`busy_timeout=15000`** 意味着遭遇竞争的写者最多等待 15 秒，而不是快速失败。实践中，WhatsApp 桥承担写者角色，而 `rousseau mcp` 与 `rousseau session list` 是只读访客。
- 存储不为跨机并发设计。两台主机通过 NFS 同时写入同一文件属于未定义行为 —— 使用单一写者，并对 DB 使用 rsync 到其他地方以获得只读副本。

## 备份

最安全的方法是在线 `sqlite3 .backup`：

```sh
sqlite3 ~/.local/share/rousseau/sessions.db ".backup '/backup/sessions.db.$(date -I).bak'"
```

`.backup` 使用 SQLite 的在线备份 API，在主库仍被写入时也能工作。基于 WAL，`restic` / `borg` 对原始文件的快照也是安全的 —— 备份能获得读取文件那一刻的一致快照。

`whatsapp.db` 文件（whatsmeow 设备凭据）是一个单独的数据库；如果您想避免恢复后重新配对，请以同样方式备份它。

## 重建 FTS 索引

若 FTS5 索引失去同步（极其罕见 —— 触发器会保持一致），可重建它：

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions_fts;
INSERT INTO sessions_fts (session_id, title, body)
SELECT id, title, payload FROM sessions;
SQL
```

Rousseau 的 `EnsureSearch` 不会撤销此操作；触发器会从一个干净状态继续运行。

## 相关

- [概念](/zh-Hans/concepts/) —— 存储在整体架构中的位置。
- [用户指南：压缩 + 召回](/zh-Hans/user-guide/compression-recall/) —— FTS 索引如何暴露给模型。
- [MCP：暴露的工具](/zh-Hans/mcp/exposed-tools/) —— 此 schema 之上的只读面。
- [指南：管理工作区](/zh-Hans/guides/managing-workspaces/) —— 跨机器共享 / 分区存储。
