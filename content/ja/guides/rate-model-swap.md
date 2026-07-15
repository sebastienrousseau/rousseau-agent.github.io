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
description: "Hot-swap the underlying model mid-session by editing config.yaml and restarting the daemon — the SQLite session store survives."
keywords: "model swap, hot swap, mid-session, restart, session store, sonnet, opus, haiku"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/rate-model-swap/"
subtitle: "Swap Sonnet for Opus mid-session; the session store survives the restart."
tags: "guides, model, swap, restart, session"
title: "ガイド：モデルのホットスワップ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "model swap, hot swap, mid-session, restart, session store, sonnet, opus, haiku"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：モデルのホットスワップ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/rate-model-swap/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/rate-model-swap/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "ガイド：モデルのホットスワップ"
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
twitter_description: "Hot-swap the underlying model mid-session by editing config.yaml and restarting the daemon — the SQLite session store survives."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド：モデルのホットスワップ"
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

## なぜ動作するか

rousseau はプロセス起動時に一度 `config.yaml` からプロバイダーとモデルを読み取ります (`internal/config/config.go` の `config.Load`)。セッション状態は SQLite にあります。モデルを変更するには、config を編集し、デーモンを再起動し、次のインバウンドメッセージを新しいモデルに処理させます — 前のモデルが参加したすべてのセッションは `sessions.db` にそのまま残ります。

セッションストアに関する何も特定のモデルに結びついていません。`payload` カラム (`internal/state/sqlite/schema.sql`) は `agent.Session` のプレーン JSON ブロブです。役割、コンテンツ、tool-use ブロック。Anthropic の content-block 慣習を話す (あるいは `internal/llm/*/client.go` の SDK アダプタを通じて適応された) 任意のモデルは、前のモデルが中断したところから続けることができます。

## 同じプロバイダー内でのスワップ

簡単なケース。model フィールドを編集:

```yaml
# was:
anthropic:
  model: claude-sonnet-4-6

# now:
anthropic:
  model: claude-opus-4-6
```

再起動:

```sh
systemctl --user restart rousseau-agent
# or, if you're running rousseau chat interactively, quit and relaunch
```

次のメッセージを送信してください。返信は Opus から来ます。セッションコンテキストは変わりません。

## プロバイダー間のスワップ

コンテンツブロック形状が異なるため、少し複雑です。rousseau のアダプタ (`internal/llm/anthropic/client.go`、`internal/llm/openai/client.go`) は各ターンで `agent.Message` 値を SDK のネイティブ型を通じてラウンドトリップします。これは:

- **`claudecli` → `anthropic`** — クリーンスワップ。両者は同じコンテンツブロック形状を使用します。
- **`claudecli` → `bedrock` / `vertex`** — クリーンスワップ。Anthropic-on-Bedrock と Anthropic-on-Vertex は同じメッセージ形式を話します。
- **Anthropic ファミリー → `openai` / `openrouter` / `ollama`** — tool-use ブロックは OpenAI の function-call 形式に再形成されます。セッション内の以前の tool_use / tool_result ペアはアダプタを通じてラウンドトリップします。テキストにはシームレスなはずですが、エッジケース (単一ターン内の複数 tool-use、ストリーミング部分) は異なってレンダリングされる可能性があります。

セッションに tool-use 履歴が多くあり、プロバイダーファミリーを越える場合は、まず新しいセッションでテストしてください。

## 状態に触れずにデプロイプロバイダーをスワップする

同じセッションストア、異なるデーモン config:

```sh
cp ~/.config/rousseau/config.yaml ~/.config/rousseau/config.yaml.bak
$EDITOR ~/.config/rousseau/config.yaml   # change provider + model
systemctl --user restart rousseau-agent
```

`state.path` は変わっていないため、JID→セッションマッピング (`internal/state/sqlite/jidmap.go` の `jid_sessions` テーブル) は依然としてすべての WhatsApp / Slack / Matrix 送信者に対して同じ会話履歴を指しています。

## 保持されるもの

| 状態 | 再起動を生き延びる | 備考 |
|---|---|---|
| セッショントランスクリプト | はい | `sessions` テーブル。 |
| FTS5 再呼び出しインデックス | はい | `sessions_fts` 仮想テーブル。バックフィルで再トークン化。 |
| JID → セッションマッピング | はい | `jid_sessions` テーブル。 |
| cron ジョブ | はい | `cron_jobs` テーブル。 |
| WhatsApp デバイスペアリング | はい | `whatsapp.db` (別ファイル)。 |
| Anthropic プロンプトキャッシュヒット | **いいえ** | キャッシュはエンドポイントごとです。新しいモデルまたはエンドポイントは cold で始まります。 |

## 失われるもの

Anthropic のプロンプトキャッシュマーカー (`internal/llm/anthropic/client.go` の `applyCacheMarkers`) はモデルの ephemeral キャッシュ内に存在します — モデルまたはプロバイダーの再起動を超えて永続化しません。スワップ後の次の数ターンはフル入力トークンを支払います。以降のターンでキャッシュを再構築します。これはコスト予算のために知っておく価値がありますが、正しさのためではありません。

## スワップか、始め直すか

以下の場合に in-place でスワップ:

- セッションが保存する価値があり、コンテンツがテキスト重視である。
- モデルが同じファミリー内 (両方 Anthropic、または Bedrock/Vertex 経由) にある。
- 一回限りのキャッシュミスを受け入れる。

以下の場合に新規で始める:

- スマートなモデルに追いかけさせたくない古いコンテキストをセッションが持っている。
- プロバイダーファミリーを越えており、決定論的な挙動が欲しい。
- トークン数がとにかく圧縮トリガーにある — 圧縮とスワップを一気に行う。

## スワップ後のテスト

```sh
rousseau session list | head -3
rousseau session show <id> | tail -20
# in TUI or via a transport:
> what did we just decide about X?
```

返信が以前の会話を一貫して参照するなら、スワップは動作しています。モデルが「コンテキストがない」ことを謝罪したり、自分を繰り返したりする場合、アダプタのラウンドトリップが tool-use メタデータを失っている可能性があります — バグを報告するか、以前のモデルにフォールバックしてください。

## 関連

- [プロバイダー](/ja/providers/) — サポートされるすべてのプロバイダー。
- [設定](/ja/configuration/) — 正確なフィールド名。
- [ガイド: レート制限](/ja/guides/rate-limits/) — キャッシュマーカーの議論。
- [ガイド: セッション管理](/ja/guides/session-management/) — 完全ライフサイクル。
