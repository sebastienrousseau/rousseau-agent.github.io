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
description: "How rousseau's write and edit tools interact with the workspace bind mount, SELinux :Z labels, container UID mapping, and safe editing outside /workspace."
keywords: "workspace, bind mount, SELinux, :Z, UserNS, write, edit, permissions"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/file-management/"
subtitle: "Workspace bind mount, SELinux :Z, UID mapping, and safe file edits."
tags: "guides, files, container, selinux, workspace"
title: "ガイド：ファイル管理"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "workspace, bind mount, SELinux, :Z, UserNS, write, edit, permissions"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：ファイル管理"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 37
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/file-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/file-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "ガイド：ファイル管理"
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
twitter_description: "How rousseau's write and edit tools interact with the workspace bind mount, SELinux :Z labels, container UID mapping, and safe editing outside /workspace."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド：ファイル管理"
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

## 2 つのツール

ファイルシステムを変更する 2 つのツール:

- [`write`](/ja/reference/tool-schemas/#write) — ファイル全体の上書き。`internal/tools/builtin/write.go` はモード `0o644` と `MkdirAll(dir, 0o755)` で書き込みます。
- [`edit`](/ja/reference/tool-schemas/#edit) — 既存ファイル内での単一の正確な文字列置換。`internal/tools/builtin/edit.go`。

どちらも **絶対パス** を必要とします (`filepath.IsAbs` を呼び出します)。どちらもアトミックスワップは行いません — 直接 `os.WriteFile` を使用します。

## コンテナから見た世界

`docker/rousseau-agent.container` のリファレンス Quadlet ユニットは、3 つのホストディレクトリをコンテナにマウントします:

```
Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
Volume=%h/.claude:/home/rousseau/.claude:rw,Z
Volume=%h/team-rousseau-workspace:/workspace:rw,Z
```

ホスト上の他のものは見えません。コンテナ内部からは、`/workspace/repos/foo/main.go` に対する `edit` ツール呼び出しは、ホスト上の `~/team-rousseau-workspace/repos/foo/main.go` に解決されます。

### `:Z` — SELinux ラベル

各 `Volume=` 上の `:Z` フラグは、Podman に **コンテナプライベート** の SELinux MCS カテゴリでマウントを再ラベル付けするよう指示します。SELinux が enforcing モードのシステムでは、これがないと:

- ほとんどの場合、読み取りは依然として機能します (`container_file_t` は広く読み取り可能)。
- 書き込みは `EACCES` と、監査ログの `avc: denied { write }` で失敗します。

フラグを `:z` (小文字) に変えると、Podman は **共有** カテゴリで再ラベル付けします — 複数のコンテナユーザー間で共有するホストではより安全ですが、デフォルトではありません。

SELinux のないシステム (Debian、非ハードニング Ubuntu) では、`:Z` はサイレントな no-op です。

### `UserNS=keep-id` — UID マッピング

コンテナは UID/GID 1000 で動作します。ユーザーネームスペースマッピングがないと、rootless Podman は 1000 を subuid 範囲 (通常 `100000+`) に再マップし、コンテナ内部から書き込まれたファイルはホスト上でその再マップされた UID によって所有されます — オペレーターには使えません。

`UserNS=keep-id` は、コンテナ UID 1000 をホストユーザーの UID (リファレンスセットアップでも 1000) にマップします。`/workspace` 内部から書き込まれたファイルは、ホスト上で `seb:seb` によって所有されます — まさに望むもの。

ホストユーザーが UID 1000 でない場合でも、マッピングは機能します。`keep-id` は呼び出し元ユーザーの実際の UID を使用します。

## `/workspace` の外での編集

バインドマウントがコンテナのホストファイルシステムに対する唯一のビューであるため、`/etc/nginx/nginx.conf` に対する `write` や `edit` は path-not-found エラーで失敗します — パスがコンテナ内部に単に存在しません。これは **機能** です: オペレーターの承認者ポリシーがコンテナ境界を信頼できることを意味します。

デーモンが別のホストパスに触れる必要が本当にある場合:

1. **推奨:** Quadlet ユニットに新しい `Volume=` 行を追加します。最も許容度の低い選択をしてください: 読み取り専用には `:ro`、プライベート SELinux ラベル付けには `:Z`。
2. 境界を回避するためにコンテナの外で rousseau を実行 **しないでください** — seccomp、drop-caps、読み取り専用ルートファイルシステムを失います。

## コンテナの外での編集

ホスト上で rousseau を直接実行する場合 (コンテナなし)、ツールはデーモンのプロセスビューに対して動作します — デフォルトではユーザーの HOME 下のすべて。承認者が唯一の封じ込め層です。パターンモード + `default: deny` レシピについては [ガイド: 監査 + 承認ポリシー](/ja/guides/audit-approval-policies/) を参照してください。

## `write` と `edit` — どちらを使うか

| 状況 | 使用 |
|---|---|
| 新しいファイルを作成する。 | `write`。 |
| ファイル全体を書き直す。 | `write`。 |
| 大きなファイルの 1 セクションを変更する。 | `edit`。`old_string` がユニークでない場合、安全に失敗します。 |
| ファイル全体でシンボルをリネームする。 | 徐々に周囲のコンテキストを増やした複数の `edit` 呼び出し、または書き直した完全な内容での単一の `write`。`replace_all` スタイルのセマンティクスで `edit` を使わないでください — ツールが拒否します。 |

`edit` の完全一意性制約は意図的です。Claude Code の Edit ツールから直接借用しています。理由を説明するコメントブロックについては `internal/tools/builtin/edit.go` を検索してください。

## 一般的な障害モード

| 症状 | 原因 | 修正 |
|---|---|---|
| `edit: path must be absolute, got "…"` | モデルが相対パスを渡した。 | 承認者で拒否または書き換え。モデルに絶対パスの使用を求めます。 |
| `edit: old_string not found in …` | モデルが最後に読み取ってからファイルが変更されたか、モデルが周囲のコンテキストを幻覚した。 | モデルは通常、再度読み取って再試行します。 |
| `edit: old_string is not unique in … (found 3 occurrences)` | 同じ文字列が複数回出現。 | モデルは曖昧さを解消するためにより多くの周囲の行を提供する必要があります。 |
| `write: permission denied` | SELinux ラベルの不一致、または UID マッピングが間違っている。 | ボリューム上の `:Z` とコンテナ上の `UserNS=keep-id` を確認してください。 |
| `read: does not look like UTF-8 text` | ファイルが最初の 512 バイトに NUL バイトを含む (`read.go` の `isLikelyText`)。 | 承認者レベルでバイナリ読み取りを拒否します。識別が必要な場合は `file` 付きの `bash` ツールを使用します。 |

## 大きな書き換え前のバックアップ

ツールは `.bak` コピーを作成しません。高リスクの変更については、モデルに最初に兄弟パスに書き込み、`bash` で diff し、その後入れ替えるように教えます。または、すべてを git ブランチ経由で実行してください — rousseau は `git` を完全に実行パスの外に置くため、任意のバージョニングは通常のワークフローで発生します。

## 関連

- [リファレンス: ツールスキーマ](/ja/reference/tool-schemas/) — 正確な入力スキーマ。
- [ユーザーガイド: ツール](/ja/user-guide/tools/)。
- [デプロイ](/ja/deployment/) — バインドマウントを定義する Quadlet ユニット。
- [ガイド: 監査 + 承認ポリシー](/ja/guides/audit-approval-policies/) — 書き込みをディレクトリツリーに固定します。
