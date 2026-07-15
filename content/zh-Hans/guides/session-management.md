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
description: "Full session lifecycle: list, search, show, delete, compression triggers, and restoration from the SQLite session store."
keywords: "session, lifecycle, list, search, delete, compression, sqlite"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/zh-Hans/guides/session-management/"
subtitle: "List, search, delete, compress, restore."
tags: "guides, session, sqlite, compression"
title: "指南：会话管理"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "session, lifecycle, list, search, delete, compression, sqlite"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "指南：会话管理"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/guides/session-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/session-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "指南：会话管理"
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
twitter_description: "Full session lifecycle: list, search, show, delete, compression triggers, and restoration from the SQLite session store."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "指南：会话管理"
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

## 会话生命周期

一个会话是持久化到 `sessions` 表（`internal/state/sqlite/schema.sql`）一行中的一个 `agent.Session` 值。它有一个 `id`、一个 `title`、按时间顺序排列的 `Message` 值切片，以及时间戳。一旦创建，直到您删除它才会消失。

会话在每个入口点按需创建：

- `rousseau chat` —— 每个 TUI 会话一个（每次调用 `chat` 都新建一个；如要复用现有会话，需要构建一个会话选择器）。
- 每种传输（`whatsapp`、`slack` 等）—— 通过 JID 映射（`internal/state/sqlite/jidmap.go`），每个 JID 一个会话。
- `rousseau cron` —— 每次触发都是被限定到本次运行的一次性会话。

## 枚举

```sh
rousseau session list --limit 10
```

输出（来自 `internal/cli/session.go` 的 `newSessionListCmd`）：

```
<short-id>  <messages>  <updated_at>  <title>
```

`--limit 0` 返回不限行数。

## 搜索

对每条已记录消息的 FTS5 搜索：

```sh
rousseau session search 'retry logic'
rousseau session search '"exponential backoff" AND anthropic'
rousseau session search 'retr*'                # 前缀
```

该命令用 `SearchOptions{Limit: N}` 包装 `Store.Search`（`internal/state/sqlite/search.go`）。排序是 BM25；片段被裁剪到约 200 字符。

## 显示

```sh
rousseau session show <session-id>
```

打印完整对话稿，在助手消息之间带有 `→ tool_use(name, input)` 与 `← tool_result` 标记。对审计无人值守守护进程的会话很有用。

## 删除

```sh
rousseau session delete <session-id> --yes
```

必须带 `--yes` flag（`newSessionDeleteCmd`）。删除会通过 FTS5 触发器级联，让回忆索引保持一致。

## 压缩触发条件

当 `config.yaml` 中 `agent.compression.enabled: true` 时，`LLMCompressor`（`internal/agent/compressor.go`）在每一轮之前检查两个条件：

- `len(s.Messages) >= trigger_messages`（默认 60）。
- `len(s.Messages) > keep_recent`（默认 8）。

如果两者都成立，压缩器把最老的一段摘要为单条以 `[rousseau-compressed]` 标记为前缀的合成用户消息，然后原样保留最后 `keep_recent` 条消息。重写的会话在内存中替换原始会话，并在下一次 `Store.Save` 时持久化。

除非会话增长到超过 `2 * trigger_messages`，否则对已压缩会话的第二次压缩会被跳过 —— 这在不为每轮重新摘要付费的情况下限定了失控增长。

日志行：

```
INFO agent.compressed messages=68
```

## 恢复

会话自动恢复。传输路由器（`internal/transport/router.go`）在入站时查找 JID → 会话 id 映射，然后 `Store.Load` 将 JSON 负载反序列化回一个 `agent.Session`。无需手动步骤。

如果映射过期 —— 会话 id 存在于 `jid_sessions` 但不存在于 `sessions` —— 您会看到 `router.stale_mapping`（WARN），路由器会新建一个会话。这是部分删除留下的历史残留；可以安全忽略。

## 从备份手动恢复

要从 `.backup` 快照回滚整个会话存储：

```sh
systemctl --user stop rousseau-agent
cp /backup/sessions.db.2026-07-12.bak ~/.local/share/rousseau/sessions.db
rm -f ~/.local/share/rousseau/sessions.db-wal ~/.local/share/rousseau/sessions.db-shm
systemctl --user start rousseau-agent
```

`-wal` 与 `-shm` 文件必须与主文件一起丢弃；SQLite 会在下次打开时重建它们。

## 按年龄批量删除

没有内置的"删除早于 X 的会话"CLI。通过 SQLite 处理：

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions WHERE updated_at < datetime('now', '-90 days');
SQL
```

FTS5 触发器会保持回忆索引一致。

## 保护隐私

由于会话内容以明文存储在 JSON blob 中，请把 `sessions.db` 视作敏感数据。选项：

- **文件系统级加密。** Linux 上的 LUKS、macOS 上的 FileVault。
- **加密备份。** `restic` 与 `borg` 都会在静态下加密。
- **一次性会话的完成即删除。** 对于 cron 驱动的守护进程，运行后 hook 可以 `rousseau session delete` 刚完成的会话 id。目前非内置；评审见 [指南：企业接入](/zh-Hans/guides/enterprise-onboarding/)。

## `rousseau session` 命令完整参考

<div class="tabs" data-tabs="session-commands">
  <div class="tab-list" role="tablist" aria-label="Session subcommand">
    <button role="tab" aria-selected="true">list</button>
    <button role="tab" aria-selected="false">show</button>
    <button role="tab" aria-selected="false">search</button>
    <button role="tab" aria-selected="false">delete</button>
    <button role="tab" aria-selected="false">export</button>
  </div>
  <div class="tab-panel" role="tabpanel">

列出会话，最新在前：

```sh
rousseau session list
rousseau session list --limit 100
rousseau session list --json
```

列：`ID`、`Title`、`Messages`、`UpdatedAt`。`--json` flag 每行发出一个对象，供脚本消费者使用。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

打印会话的完整对话稿：

```sh
rousseau session show <session-id>
rousseau session show <session-id> --raw
```

`--raw` 打印按原样存储的 JSON（对调试有用）。不带 `--raw` 时，工具调用渲染为 `→ tool_use(name, input)`，结果渲染为 `← tool_result`。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

跨所有会话的全文搜索：

```sh
rousseau session search "refactor login"
rousseau session search "TODO" --limit 10
```

使用 FTS5 索引（见 `internal/state/sqlite/`）。结果按相关性排序，并包含高亮匹配词的片段。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

删除会话及其 FTS5 条目：

```sh
rousseau session delete <session-id> --yes
```

必须带 `--yes` flag —— 没有交互确认。删除通过 SQL 触发器级联，让回忆索引保持一致。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

以 JSON 导出会话：

```sh
rousseau session export <session-id> > session.json
```

导出格式与磁盘上的 JSON blob 相匹配；重新导入尚未支持（路线图）。

  </div>
</div>

## 故障排除

### `session not found`

您传入的 ID 不存在。区分大小写。使用 `rousseau session list` 查看有效 ID。

### FTS5 搜索什么都没返回

在 FTS5 接线之前导入的旧会话上，索引可能已过期。运行任何改动内容的操作即可重建（删除会触发重新索引），或通过 SQLite 手动重新索引。

### 读时 `database is locked`

另一个守护进程持有 WAL 写锁。如果您只需要读，请使用只读 DSN（`?mode=ro`）。

### 会话存储增长过快

启用压缩（`agent.compression.enabled: true`）并定期对 SQLite 文件 `VACUUM` 以回收空间。

### 从备份恢复得到过期状态

确保在启动守护进程之前丢弃 `-wal` 与 `-shm`。如果 `-wal` 存在，SQLite 会重放 WAL，可能撤销您的恢复。

## 相关页面

- [参考：会话存储](/zh-Hans/reference/session-store/) —— schema 与 DDL。
- [指南：管理工作区](/zh-Hans/guides/managing-workspaces/) —— 每个工作区独立存储。
- [指南：上下文管理](/zh-Hans/guides/context-management/) —— 压缩如何决定保留什么。
- [用户指南：CLI](/zh-Hans/user-guide/cli/) —— 命令签名。
- [用户指南：压缩 &amp; 回忆](/zh-Hans/user-guide/compression-recall/) —— 压缩器与 FTS5 回忆的内部机制。

## 延伸阅读

- `internal/cli/session.go` —— CLI 接线。
- `internal/state/sqlite/store.go` —— DSN、WAL、索引。
- `internal/agent/session.go` —— `Session` 结构体。
- `internal/agent/compressor.go` —— `LLMCompressor`。
- `internal/agent/recall.go` —— `SQLiteRecall`。
