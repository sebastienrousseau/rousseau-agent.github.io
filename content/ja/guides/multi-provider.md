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
description: "Run two rousseau daemons with different providers side-by-side — e.g. claudecli for interactive chat and Bedrock for scheduled reports."
keywords: "multi provider, claudecli, bedrock, config precedence, XDG_CONFIG_HOME"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/multi-provider/"
subtitle: "Two daemons, two providers, one operator."
tags: "guides, providers, multi-provider, deployment"
title: "ガイド：マルチプロバイダ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "multi provider, claudecli, bedrock, config precedence, XDG_CONFIG_HOME"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：マルチプロバイダ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 35
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/multi-provider/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/multi-provider/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "ガイド：マルチプロバイダ"
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
twitter_description: "Run two rousseau daemons with different providers side-by-side — e.g. claudecli for interactive chat and Bedrock for scheduled reports."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド：マルチプロバイダ"
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

## これを求める理由

rousseau の `provider` フィールドは単一のスカラーです (`internal/config/config.go` `Config.Provider`)。単一の rousseau プロセスはちょうど 1 つのプロバイダと通信します。複数が必要な場合 — 最も一般的には、OAuth セッションを継承するためインタラクティブ TUI 用に `claudecli`、そしてサブスクリプション階層の `claude` OAuth が不便なバックグラウンドデーモン用に有料 API プロバイダ (Bedrock、Anthropic 直接、Vertex) — 異なる設定ファイルで **2 つの rousseau プロセス** を実行します。

妥当な組み合わせ:

| インタラクティブ | 無人 | 理由 |
|---|---|---|
| `claudecli` | `anthropic` または `bedrock` | ラップトップチャット用の OAuth、VPS デーモン用の API キー。 |
| `claudecli` | `vertex` | 同じ、GCP 上。 |
| `anthropic` | `openai` または `ollama` | 回答を比較する、または cron 用により安価な / ローカルモデルにフォールバック。 |
| `claudecli` | `openai` (OpenRouter) | TUI では Claude、スケジュールされた要約のために安価な OpenRouter モデル。 |

## rousseau が設定を解決する方法

`config.Load` (`internal/config/config.go` 内) は flag > env > file > default を適用します。読み取るファイルはデフォルトで `~/.config/rousseau/config.yaml` ですが、ルートコマンド (`internal/cli/root.go`) の `--config` 永続フラグがそれを上書きします。これによりクリーンな分割が得られます。

## 2 設定レイアウト

```sh
mkdir -p ~/.config/rousseau
cat > ~/.config/rousseau/chat.yaml <<'YAML'
provider: claudecli
claudecli:
  binary: claude
log:
  level: info
  format: text
YAML

cat > ~/.config/rousseau/cron.yaml <<'YAML'
provider: bedrock
bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
log:
  level: info
  format: json
YAML
```

正しいファイルで各コマンドを実行します:

```sh
rousseau --config ~/.config/rousseau/chat.yaml chat
rousseau --config ~/.config/rousseau/cron.yaml whatsapp --allow YOUR_JID@s.whatsapp.net
```

## 共有ステートとパーティション化されたステート

両方のプロセスはデフォルトで同じ SQLite セッションストア (`~/.local/share/rousseau/sessions.db`) を指します — 通常はこれが望むもので、WhatsApp ブリッジと TUI チャットが履歴を共有します。

ステートを完全にパーティション化するには、設定ごとに `state.path` を上書きします:

```yaml
state:
  path: /home/seb/.local/share/rousseau/chat.db
```

クロスプロセスの SQLite アクセスは、WAL ジャーナリングと `internal/state/sqlite/store.go` の `Open()` によって設定される 15 秒の `busy_timeout` により安全です。

## systemd 配線

2 つの Quadlet ユニット、設定ごとに 1 つ。各ユニットの `Exec=` には `--config /home/rousseau/.config/rousseau/<name>.yaml` が含まれます:

```ini
Exec=--config /home/rousseau/.config/rousseau/cron.yaml whatsapp --allow ...
```

ベースユニットについては [デプロイ](/ja/deployment/) を参照してください。

## 設定ごとの承認者ポリシー

異なるプロバイダは異なる承認に値します。インタラクティブな `claudecli` は、Claude Code が独自の呼び出しごとの承認 UI を持つため、安全に `mode: allow_all` のままにできます。Bedrock/Anthropic デーモンは `default: deny` 付きの `mode: pattern` を実行するべきです。それぞれを独自の YAML の下に置いてください。

## テスト

各プロセスが正しいエンドポイントと通信することを確認します:

```sh
# Interactive shows the claudecli subprocess path in strace / lsof
lsof -c rousseau | grep -E 'claude|CLAUDE'

# Background shows outbound HTTPS to bedrock-runtime.<region>.amazonaws.com
ss -tanp | grep rousseau
```

## これでは得られないもの

- **リクエストごとのルーティングではない。** rousseau は単一のターン内で 1 つのプロバイダから別のプロバイダにフォールバックしません。設定されたプロバイダの失敗は `whatsapp.handler_failed` / `turn.failed` として現れ、モデルは別のプロバイダに対してリトライしません。これはロードマップ項目です。
- **共有キャッシングではない。** Anthropic プロンプトキャッシュ (`internal/llm/anthropic/client.go` の `applyCacheMarkers` を参照) はエンドポイントごとです。同じモデルファミリでも、Anthropic 直接でのヒットは Bedrock に対するヒットではありません。

## 関連

- [プロバイダ](/ja/providers/) — 5 種類のプロバイダタイプすべての比較。
- [設定](/ja/configuration/) — すべてのノブ。
- [リファレンス: 環境変数](/ja/reference/environment-variables/) — env ベースの上書き。
- [ガイド: プロダクションデプロイ](/ja/guides/production-deployment/)。
