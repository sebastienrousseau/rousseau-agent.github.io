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
hreflang: "ja"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "ja"
locale: "ja_JP"
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
permalink: "https://docs.rousseau-agent.dev/ja/guides/managing-workspaces/"
subtitle: "Partition state per project, share history across machines, drop history cleanly."
tags: "guides, workspace, session store, sqlite"
title: "ガイド：ワークスペース管理"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "workspace, session store, state path, sync, rsync, XDG_DATA_HOME"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：ワークスペース管理"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 38
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/managing-workspaces/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/managing-workspaces/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "ガイド：ワークスペース管理"
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
twitter_title: "ガイド：ワークスペース管理"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "自らのコーディングエージェントを運用するすべてのオペレーターに感謝します。"
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## 慣例

rousseau にはファーストクラスの「ワークスペース」概念はありません。`internal/config/config.go` (`StateConfig`) に 1 つの `state.path` があり、デフォルトではすべてのプロセスが `~/.local/share/rousseau/sessions.db` を指します。すべてのセッション、cron ジョブ、JID マッピング、FTS5 リコールインデックスがその単一ファイルに存在します。

ほとんどのオペレーターにとってこれが正解です。分離が必要な場合 — プロジェクトごと、マシンごと、クライアントごと — rousseau を別の SQLite ファイルに向けます。そのファイル **が** ワークスペースです。

## 呼び出しごとにワークスペースを切り替える

2 つのノブ、どちらでも動作します:

```sh
# 1. flag on any rousseau command
rousseau --config ~/.config/rousseau/acme.yaml chat

# 2. env var (Viper picks it up via ROUSSEAU_STATE_PATH)
ROUSSEAU_STATE_PATH=~/.local/share/rousseau/acme.db rousseau chat
```

ワークスペース間を移動するとき、どちらのアプローチも rousseau の再起動を必要としません — 各プロセスは独自のファイルを開きます。

## プロジェクトごとのワークスペースレイアウト

```
~/.config/rousseau/
├── acme.yaml         # provider = anthropic, state.path = …/acme.db
├── personal.yaml     # provider = claudecli, state.path = …/personal.db
└── work.yaml         # provider = bedrock,    state.path = …/work.db
```

各設定ファイルが `state.path` を上書きします:

```yaml
state:
  path: /home/seb/.local/share/rousseau/acme.db
```

その後、正しい設定で各セッションを起動します。TUI (`internal/tui/model.go`) はステータスバーにセッション ID + プロバイダを表示します — 正しいワークスペースにいることを視覚的に確認できます。

## マシン間で履歴を共有する

セッションストアは単一の SQLite ファイルです。WAL ジャーナリングは `internal/state/sqlite/store.go` の `Open()` によって有効化されるため、ライブスナップショットは安全です:

```sh
# Snapshot laptop-to-desktop (both idle)
rsync -avz --partial \
  ~/.local/share/rousseau/sessions.db \
  desktop:~/.local/share/rousseau/sessions.db
```

**一度に 1 つのライターのみ。** NFS 上の同じ SQLite ファイルに対して 2 台のマシンで `rousseau whatsapp` を実行しないでください — それは未定義です。何も書き込んでいないときに同期するか、リードレプリカ付きで単一のライターを実行してください。

より安全な代替は `.backup` スナップショットです:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db ".backup '/tmp/sessions.snap.db'"
scp /tmp/sessions.snap.db desktop:~/.local/share/rousseau/sessions.db
```

`.backup` は SQLite のオンラインバックアップ API を使用し、一貫したポイントインタイムファイルを生成します。

## ワークスペースの移行

ディレクトリ全体を移動します。それがワークスペースです:

```sh
rsync -avz ~/.local/share/rousseau/ new-host:~/.local/share/rousseau/
```

`whatsapp.db` (デバイス認証情報) は別です — それも持ってくる (デバイスはペアリングされたまま) か、置いていって新しいホストで QR を再スキャンします。

## ワークスペースの履歴を削除する

```sh
rousseau session list                 # confirm what you're about to lose
rm ~/.local/share/rousseau/acme.db*   # includes -wal and -shm sidecars
```

パスを開く次のプロセスは、`internal/state/sqlite/schema.sql` のスキーマでそれを再作成します。

セッションのサブセットのみを削除したい場合は、CLI を使用します:

```sh
rousseau session delete <id> --yes
```

`rousseau session delete` (`internal/cli/session.go`) は `Store.Delete` を呼び出し、それが FTS5 トリガを通じてカスケードし、リコールインデックスを一貫させます。`--yes` フラグが必要です — なしではコマンドは実行を拒否します。

## SQL による部分削除

一括クリーンアップ — 90 日より古いすべてのセッション:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
DELETE FROM sessions WHERE updated_at < datetime('now', '-90 days');
SQL
```

FTS5 トリガ (`internal/state/sqlite/search.go` の `sessions_fts_ad`) は DELETE で発火し、インデックスを自動的に同期します。

## ワークスペースごとの承認者

設定ファイルとステートファイルがどちらもワークスペースごとであるため、承認者もそうです:

```yaml
# work.yaml — strict pattern approver
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

別の `personal.yaml` はインタラクティブな作業用に `mode: allow_all` を維持するかもしれません。[チュートリアル: 承認者の強化](/ja/tutorials/harden-approver-policy/) を参照してください。

## 関連

- [リファレンス: セッションストア](/ja/reference/session-store/) — スキーマ。
- [ガイド: マルチプロバイダ](/ja/guides/multi-provider/) — 2 設定、2 プロバイダのパターン。
- [リファレンス: 環境変数](/ja/reference/environment-variables/) — すべてのパス環境変数。
- [ユーザーガイド: CLI](/ja/user-guide/cli/) — `rousseau session` コマンド。
