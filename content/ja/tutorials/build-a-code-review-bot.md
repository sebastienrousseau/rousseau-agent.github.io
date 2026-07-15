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
description: "Wire rousseau-agent to a Slack channel that runs read and grep over the workspace whenever an operator asks."
keywords: "slack, code review, socket mode, read tool, grep tool, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/tutorials/build-a-code-review-bot/"
subtitle: "A Slack channel that lets rousseau review a repo on demand."
tags: "tutorials, slack, code review, socket mode, read, grep"
title: "チュートリアル：コードレビュー Bot を作る"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "slack, code review, socket mode, read tool, grep tool, allowlist"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "チュートリアル：コードレビュー Bot を作る"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/tutorials/build-a-code-review-bot/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/build-a-code-review-bot/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "チュートリアル：コードレビュー Bot を作る"
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
twitter_description: "Wire rousseau-agent to a Slack channel that runs read and grep over the workspace whenever an operator asks."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "チュートリアル：コードレビュー Bot を作る"
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

## 作成するもの

チームメンバーが `@rousseau` にメンションし、リポジトリパスと質問を投稿するプライベート Slack チャンネルを構築します。Rousseau はワークスペースを参照し、`internal/tools/builtin/` の `read` と `grep` を実行して、引用付きの行参照を含む応答を投稿します。公開 HTTP サーフェスは不要です。Slack Socket Mode がすべてをアウトバウンドの WebSocket 経由で駆動します。

所要時間の目安: ワークスペースへの Slack 管理者アクセスを既に持っていることを前提として 20 分。

## 前提条件

- rousseau がインストールされ、プロバイダーが設定されていること ([Quickstart](/ja/quickstart/) を参照)。
- Slack ワークスペースの管理者権限。
- `$HOME` 配下のあるパスに既にチェックアウトされているリポジトリ。これがボットの `read` / `grep` の対象となる「ワークスペース」となります。

## ステップ 1: Slack アプリを作成

このボットを可能にしているのは Slack の Socket Mode です。デーモンが Slack へアウトバウンドの WebSocket を開くだけで、イングレスは不要です。

1. <https://api.slack.com/apps> にアクセスし、新しいアプリを **from scratch** で作成します。
2. **Socket Mode** で有効化し、`connections:write` 権限を持つ **app-level token** を生成します。`xapp-...` の値をコピーします。
3. **OAuth & Permissions** で、次の **Bot Token Scopes** を追加します。
   - `chat:write`
   - `app_mentions:read`
   - `channels:history` (プライベートチャンネルの場合は `groups:history`)
4. アプリをワークスペースにインストールします。**Bot User OAuth Token** (`xoxb-...` の値) をコピーします。
5. **Event Subscriptions** でイベントを有効化し、`app_mention` と `message.channels` (または `message.groups`) をボットに購読させます。
6. ボットをレビューチャンネルに招待します: `/invite @rousseau`。

## ステップ 2: rousseau を設定

`~/.config/rousseau/config.yaml` に追加します。関連フィールドは `internal/config/config.go` の `SlackConfig` から取得されます。

```yaml
provider: claudecli           # または anthropic — Quickstart で設定したもの

slack:
  app_token:  xapp-1-…
  bot_token:  xoxb-…
  bot_user_id: U0ROUSSEAU     # https://api.slack.com/methods/auth.test から取得
  reply_header: "*rousseau-agent*\n\n"
  allowlist:
    - U01ABC…                 # 自分の Slack ユーザー ID

agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
    # bash なし、write なし、edit なし — 読み取り専用のレビュアー
```

`allowlist` は、ルーターがメッセージを受け入れる相手を制限します。`internal/transport/router.go` のルーターは、それ以外の送信者に対して `transport.rejected` を出力します。

## ステップ 3: ブリッジを実行

```sh
rousseau slack \
  --app-token "$SLACK_APP_TOKEN" \
  --bot-token "$SLACK_BOT_TOKEN" \
  --bot-user-id "$SLACK_BOT_USER_ID"
```

`--bot-user-id` は、ボットが自身のメッセージに返信することを防ぎます。`internal/transport/slack/client.go` からの構造化ログは次のように表示されます。

```
INFO slack.started
INFO slack.incoming from=U01ABC channel=C01REVIEW text="…"
INFO tool.execute name=read id=t_1
INFO tool.execute name=grep id=t_2
```

## ステップ 4: 試す

レビューチャンネルで:

```
@rousseau look under /home/seb/repos/acme-api and tell me
where request logging is set up
```

`claudecli` プロバイダー (または選択した Anthropic) は、ワークスペースのバインドマウントに対して `internal/tools/builtin/` の `read` と `grep` を呼び出します。承認者が `pattern` モードで動作し、`read` と `grep` のみが allowlist に含まれているため、たとえ悪意あるプロンプトが要求してもモデルは書き込みやシェル実行を行えません。

## ステップ 5: 堅牢化

Pattern モードの承認者は、**JSON ツール入力に対する正規表現** として機能します。`read` と `grep` を特定のプロジェクトツリーに制限するには:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: "\"path\":\"/home/seb/repos/acme-api/[^\"]*\""}
      - {tool: grep, match: "\"path\":\"/home/seb/repos/acme-api\""}
```

`default: deny` と監査の完全なウォークスルーについては [Tutorial: Harden the approver](/ja/tutorials/harden-approver-policy/) を参照してください。

## systemd でのデプロイ

ラップトップセッションを超える運用では、`docker/rousseau-agent.container` にある Podman Quadlet ユニットで Slack ブリッジを実行してください。`Exec=whatsapp --allow …` を `Exec=slack --app-token … --bot-token …` に置き換えます。完全なユニットは [Deployment](/ja/deployment/) を参照してください。

## 関連

- [Transports: Slack](/ja/transports/slack/)
- [User Guide: Approval Policies](/ja/user-guide/approval-policies/)
- [User Guide: Tools](/ja/user-guide/tools/)
- [Tutorial: Harden the approver](/ja/tutorials/harden-approver-policy/)
