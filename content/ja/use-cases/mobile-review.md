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
changefreq: "monthly"
description: "Use case narrative: reviewing pull requests from WhatsApp on the train, driven by rousseau-agent on a home box."
keywords: "mobile review, whatsapp, pr review, commute, use case, pull request"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/use-cases/mobile-review/"
subtitle: "Reviewing PRs from your phone on the train."
tags: "use-cases, whatsapp, mobile, pr"
title: "ユースケース：モバイルからの PR レビュー"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mobile review, whatsapp, pr review, commute, use case, pull request"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ユースケース：モバイルからの PR レビュー"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 72
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/use-cases/mobile-review/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/mobile-review/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "ユースケース：モバイルからの PR レビュー"
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
twitter_description: "Use case narrative: reviewing pull requests from WhatsApp on the train, driven by rousseau-agent on a home box."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ユースケース：モバイルからの PR レビュー"
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

## ストーリー

あなたは中規模企業のスタッフエンジニアです。受信箱にはあなたのレビュー待ちの 8 つの PR があります。あなたは 45 分の電車の中で、シグナルはあるがラップトップはありません。歴史的に、電話からの PR レビューは GitHub の diff ビューを目を細めて見て、空虚な「LGTM」コメントを打つことを意味しました。

rousseau はあなたの closet の小さな Intel NUC 上に住んでいます。あなたの JID への WhatsApp 接続、ローカル `claude` CLI 上の `bypassPermissions`、およびあなたがレビューする 3 つのリポのローカルチェックアウトへの読み取りアクセスを持っています。WhatsApp で DM:

> review PR #4821 in checkout-service

rousseau は `gh pr diff 4821` を実行し、コードを読み、返信します:

> PR #4821 adds retry-with-backoff to the Stripe webhook handler. Three observations:
>
> 1. The backoff is uncapped — if Stripe is truly down, we'll accumulate goroutines forever. Suggest a `context.WithTimeout` at the caller.
> 2. Test file adds two new tests but neither covers the timeout path.
> 3. `pkg/webhook.go:82` — the mutex is held across the network call. Minor.
>
> Should I draft a review comment stub?

あなたは返信:

> yes, with all three

rousseau は `--draft` の下で `gh pr review` を使用します (承認者が最終承認をブロックします。人間が依然として「submit review」をクリックする必要があります)。あなたが机に着く頃には、ドラフトコメントが待っています。

## それに必要なもの

### デーモン

NUC 上の rousseau、rootless Podman コンテナとして:

- **プロバイダー**: `claudecli` — あなたのローカル Claude Code 認証を継承。
- **トランスポート**: WhatsApp — モバイル到達のための選択のトランスポート。
- **状態**: `~/.local/share/rousseau/sessions.db`。

### Config

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: bypassPermissions

whatsapp:
  reply_header: "🚂 *rousseau*\n\n"

log:
  level: info
  format: text                # this is a single-user daemon; text logs are fine

agent:
  max_iterations: 32
  compression:
    enabled: true             # subscription-tier claudecli; compression is free
    trigger_messages: 60
    keep_recent: 8
  approver:
    mode: pattern
    default: deny
    reason: "denied — this daemon reviews code, it does not merge it"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(gh pr view|gh pr diff|gh pr list|gh pr review --draft|gh pr comment|git status|git diff|git log|git show) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(go test|go vet|go build|npm test|pnpm test|cargo check) "}
    deny:
      - {tool: bash, match: "gh pr merge|gh pr close|gh pr approve"}
      - {tool: bash, match: "git (push|reset --hard|clean)"}
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit,  match: "\"path\":\"/etc/|/root/|/var/"}
```

### バインドマウント

- `~/repos/checkout-service/` (読み取り専用)。
- `~/repos/payments-api/` (読み取り専用)。
- `~/repos/web-frontend/` (読み取り専用)。
- `~/.claude/` — Claude Code の OAuth トークン (読み書き、トークン更新のためのみ)。
- `~/.config/gh/` — GitHub CLI の OAuth トークン (読み書き、同じ理由)。

読み取り専用マウントは、モデルがあなたの作業コピーを誤って編集するのを防ぎます。レビューはあなたのチェックアウトではなく GitHub を通ります。

### 初回起動

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

QR コードを一度スキャンします。それ以降、デーモンは Quadlet ユニット内に住み、ホスト再起動時に起動します。あなたの allowlist はあなた自身の個人電話の JID です。

## セキュリティ姿勢

- **allowlist はトランスポートをロックします。** あなたの電話のみがデーモンを駆動できます。何らかの方法で電話番号を発見した他の誰かはサイレントにドロップされます。
- **pattern 承認者はすべての merge / push / close をブロックします。** rousseau はレビュー、ドラフト、コメントします — 人間が依然として「Merge」または「Approve」をクリックする必要があります。
- **読み取り専用マウント** はあなたの作業チェックアウトを保護します。
- **claudecli 上の `bypassPermissions`** は、承認者が安全性の作業をしているからこそ許容できます。`bypassPermissions` と `mode: allow_all` を決して組み合わせないでください。

## 到達

- **シグナルは地下鉄で切れます。** WhatsApp のバックプレッシャーは優雅です — あなたは質問を送信し、デーモンが返信するシグナルを持っているときに答えを取得します。rousseau はあなたの電話とのライブ TCP セッションを保持する必要はありません。
- **ボイスノートが動作します。** [ボイスモード](/ja/user-guide/voice-mode/) を有効化し、NUC に `whisper.cpp` をインストールすれば、「4821 の diff は何?」というボイスノートを口述してテキスト返信を取得できます。動く電車で電話にタイプするのが煩わしいときに便利です。
- **デーモンはあなたのハードウェアで実行されます。** あなたのレビュー推論に関するものはサードパーティの SaaS には行きません。唯一のアウトバウンド呼び出しは、既存のサブスクリプションを使用する `claude` CLI の Anthropic へのサブプロセスです。

## rousseau がここで行わないこと

- **「Merge」をクリックしません。** それは人間の決定であり、承認者が強制します。
- **あなたのレビュースタイルを学びません。** あなたのスタイルを捕捉する [スキル](/ja/skills/) を作成しない限り、次の PR は同じ汎用チェックリストを取得します。
- **レビューをキューイングしません。** 各リクエストは独立しています。「私のすべての開いた PR をレビュー」バックグラウンドジョブはありません ([cron](/ja/guides/scheduled-tasks/) 経由で 1 つを配線しない限り)。

## 負荷下で変更するもの

- 常にチェックする 6 つのことを体系化する `pr-review-checklist.md` という [スキル](/ja/skills/) を追加します。スキルは、マッチするトリガーがユーザーメッセージに出現するとシステムプロンプトにスプライスされます。
- 毎晩の cron を追加: `0 8 * * 1-5 rousseau ... deliver a summary of every open PR`。
- `claudecli` サブスクリプションレート制限がボトルネックになる場合、有料 Anthropic API パスに切り替えてください。下流の config 変更はゼロ。

## 関連ページ

- [WhatsApp トランスポート](/ja/transports/whatsapp/) — トランスポートリファレンス。
- [claudecli プロバイダー](/ja/providers/claudecli/) — 継承された認証。
- [スキル](/ja/skills/) — レビュースタイルを体系化する方法。
- [ボイスモード](/ja/user-guide/voice-mode/) — レビューを口述します。
