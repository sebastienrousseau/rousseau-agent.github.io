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
changefreq: "weekly"
description: "rousseau-agent's skills loader: Markdown + YAML frontmatter, discovery from skills_dir, trigger-based activation, composition into the system prompt."
keywords: "skills, agentskills.io, markdown, YAML frontmatter, triggers, system prompt, activation"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/skills/"
subtitle: "agentskills.io 互換の Markdown スキルファイル。"
tags: "skills, reference"
title: "スキル"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "skills, agentskills.io, markdown, YAML frontmatter, triggers, system prompt, activation"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "スキル"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 23
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/skills/index.html"
item_link: "https://docs.rousseau-agent.dev/skills/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "スキル"
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
twitter_description: "rousseau-agent's skills loader: Markdown + YAML frontmatter, discovery from skills_dir, trigger-based activation, composition into the system prompt."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "スキル"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "自らのコーディングエージェントを運用するすべてのオペレーターに感謝します。"
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## スキル形式

スキルは、任意の YAML フロントマターヘッダーを持つ Markdown ファイルです。フォーマットは意図的に [agentskills.io](https://agentskills.io) の慣習に近づけられており、他のツールでも移植可能です。

例 — `~/.local/share/rousseau/skills/git-rebase.md`:

```markdown
---
name: git-rebase
description: Guide the user through an interactive rebase safely.
triggers:
  - rebase
  - git rebase
  - squash
  - autosquash
---
When helping with a git rebase, first verify the current HEAD is
pushed to a remote branch. Prefer `git rebase -i --autosquash`
when the user has fixup commits. Never force-push to `main`.
```

## フロントマターのフィールド

| フィールド | 型 | 効果 |
|---|---|---|
| `name` | string | `^[a-z][a-z0-9-]*$` に一致する必要があります。`rousseau skills list` で表示されます。 |
| `description` | string | 1 行の要約。 |
| `triggers` | `[]string` | 大文字と小文字を区別しない部分文字列。いずれかがユーザーメッセージに現れれば、スキルが有効化されます。空の場合、スキルは自動的に有効化されません。 |

閉じる `---` 以降のすべてが、スキル本文としてそのまま扱われます。

## 検出

ローダーは `agent.skills_dir` を走査し、`*.md` ファイルを探します (再帰なし)。ディレクトリが存在しなくてもエラーにはなりません — Load は `nil` を返します。サブディレクトリは無視されます。

```yaml
agent:
  skills_dir: ~/.local/share/rousseau/skills
```

## 有効化

各ユーザーターンで、`SkillsProvider.SystemAppendix(session)` は最新のユーザーメッセージを調べ、各スキルの `triggers` に対して (大文字小文字を無視して) マッチングを行います。マッチしたものはすべて (読み込み順で) 連結され、そのターンのシステムプロンプトに挿入されます。

`triggers` が空のスキルは自動有効化されませんが、ライブラリを組み込む呼び出し側からプログラム的に組み込むことは可能です。

## CLI

```sh
# 検出されたスキルを一覧表示。
rousseau skills list

# 1 つのスキルの内容を表示。
rousseau skills show git-rebase
```

## 設計上の制約

- **コードは実行しない。** スキルは文字列であり、スクリプトやシェルコマンドを実行することはできません。自動化が必要な場合は、代わりに `Registry.Register` を通じて新しいツールを配線してください。
- **バージョン管理はない。** rousseau はスキルのバージョンを追跡しません。git で管理してください。`skills_dir` はリポジトリのワーキングコピーであることが期待されます。
- **決定的。** 同じセッションと同じユーザーメッセージは、同じ付録を生成します。ループ内に LLM は存在しません。

## 効果的なスキルの書き方

- 本文は短く保ってください (100–500 語)。有効化のたびにそのターンのシステムプロンプトの先頭に追加されます。
- 説明文よりも命令形の文章 (「ユーザーが X について尋ねた場合、Y を行う」) を優先してください。
- `triggers` には高精度のフレーズを使用してください。広範なトリガー (「code」、「help」など) はほぼすべてのターンで有効化され、他のスキルを埋もれさせます。
- チャットトランスポートのデーモンにロールアウトする前に TUI (`rousseau chat`) でテストしてください。ログ行 `agent.skills_activated` に、どのスキルが発火したかが記録されます。
