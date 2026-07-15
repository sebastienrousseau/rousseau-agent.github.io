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
description: "Use case narrative: a solo SRE running rousseau-agent over Slack to triage a 3 a.m. page from the couch, then hand off to full incident response."
keywords: "on-call, sre, slack, incident, page, triage, use case"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/use-cases/oncall-buddy/"
subtitle: "Triaging a 3 a.m. page from the couch over Slack."
tags: "use-cases, on-call, slack, sre"
title: "ユースケース：オンコールの相棒"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "on-call, sre, slack, incident, page, triage, use case"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ユースケース：オンコールの相棒"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 71
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/use-cases/oncall-buddy/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/oncall-buddy/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "ユースケース：オンコールの相棒"
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
twitter_description: "Use case narrative: a solo SRE running rousseau-agent over Slack to triage a 3 a.m. page from the couch, then hand off to full incident response."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ユースケース：オンコールの相棒"
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

午前 3 時。ポケベルが鳴る。PagerDuty は checkout サービスが 502 を投げていると言っています。あなたは小さな会社の 2 人の SRE の 1 人で、共同リードは休暇中、ラップトップに到達するには眼鏡を見つけ、階段を降りて、VPN のロックを解除する必要があります。それらすべての前に、初回の答えが欲しい: どのダッシュボードが悪く見えるか、過去 24 時間で何が変わったか、どのランブックが適用されるか。

rousseau はあなたの closet の ops box 上に住んでいます。ロギングスタックへの読み取り専用資格情報、1 つの名前空間の読み取り専用 kubectl、および `#incident-oncall` への Slack Socket Mode 接続を持っています。あなたは電話で DM 通知をタップします:

> what changed in checkout in the last 24h?

rousseau は checkout サービスリポの git log を読み、デプロイログ (バインドマウントされたディレクトリから) と相互参照し、返信します:

> Two changes: PR #4821 (payment retry logic, deployed 21:14 UTC) and a Helm value bump on `checkout-web` at 22:03 UTC. The payment retry change is the more suspicious — it touches the same code path the current 502s originate from.

あなたは尋ねる:

> pull the last 100 error lines from checkout-web

rousseau は読み取り専用の kubeconfig の下で `kubectl logs -n checkout deploy/checkout-web --tail=100 --previous` を実行し、目立つ行を貼り付けて戻します。null ポインタトレースを見つけます。DM で返信:

> revert PR #4821 in staging first — call me when it's confirmed green

rousseau は計画とともに `#incident-oncall` に投稿し、staging に対する revert PR を開き、staging が green になったら ping で返します。あなたは起き上がってラップトップに向かいます。

## それに必要なもの

### デーモン

rousseau は ops box 上で rootless Podman コンテナとして実行されます:

- **プロバイダー**: `bedrock` — あなたの会社にはすでに Bedrock spend コミットメントがあります。ユーザーごとの API キーは不要。
- **トランスポート**: Slack Socket Mode — インバウンド HTTP 表面なし、WebSocket アウトバウンドのみ。
- **状態**: `~/.local/share/rousseau/sessions.db`、LUKS 暗号化ディスク上。

### Config

```yaml
provider: bedrock

bedrock:
  region: us-east-1
  profile: rousseau-oncall
  model: anthropic.claude-sonnet-4-6-20250101-v1:0

log:
  level: info
  format: json

state:
  path: /var/lib/rousseau/sessions.db

agent:
  max_iterations: 32
  approver:
    mode: pattern
    default: deny
    reason: "read-only on-call posture — ask an operator to widen the scope"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(kubectl get|kubectl describe|kubectl logs|git log|git diff|git show|cat|grep|rg|head|tail|wc) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"gh pr (view|list|diff) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"gh pr create --draft "}   # allows opening a draft revert
    deny:
      - {tool: bash, match: "kubectl (delete|apply|edit|scale|rollout undo|exec)"}
      - {tool: bash, match: "gh pr merge|gh pr close --delete-branch"}

slack:
  app_token: xapp-<...>
  bot_token: xoxb-<...>
  allowlist:
    - U012ABCXYZ    # your Slack user ID
    - U012DEFGHI    # your co-lead's Slack user ID
```

### バインドマウント

- `/workspace/repos/` の下のリポチェックアウト (読み取り専用)。
- `/workspace/deploys/` の下のデプロイログ (読み取り専用)。
- `/home/rousseau/.kube/config` の kubeconfig — 読み取り専用でマウント、サービスアカウントは `checkout` 名前空間に読み取り専用クラスターロールを持つ。
- EKS 上なら IAM Role for Service Accounts (IRSA) 経由、オンプレなら マウントされた `~/.aws/` 経由の AWS 資格情報。

### systemd Quadlet ユニット

以下を持つ参照 `docker/rousseau-agent.container`:

- `ReadOnly=true`
- `DropCapability=all`
- `NoNewPrivileges=true`
- `Restart=on-failure`

ホスト再起動時にブート。ジャーナルは `journalctl --user -u rousseau-agent.service` 経由で利用可能。

## セキュリティ姿勢

- **Slack allowlist** はあなたと共同リードのみがデーモンを駆動できることを保証します。他のすべての DM はサイレントにドロップされます。
- **`default: deny` を持つ pattern 承認者** はホワイトリスト外のあらゆるものをブロックします。モデルが `kubectl delete pod` を実行したい場合、ブロックを説明する `tool_result` エラーを取得し、計画ドキュメントにルートを変更します。
- **読み取り専用 kubeconfig + 読み取り専用リポマウント** は、承認者が fail open してもデーモンがプロダクションを変更 *できない* ことを意味します。
- **ベルト、サスペンダー、そしてもう 1 本のベルト** — 各層は安全にフェイルします。

## rousseau がここで行わないこと

- **あなたにページしません。** PagerDuty は誰がオンコールかの真実のソースです。
- **PR をマージしません。** 承認者は `gh pr merge` をブロックします。rousseau はドラフト revert を開けます。人間が依然として確認する必要があります。
- **`kubectl exec` を実行しません。** クラスタ状態を変更する可能性のある任意のコマンドは拒否されます。
- **インシデントから学習しません。** FTS5 経由のクロスセッション再呼び出しは、次のインシデントの rousseau が今夜のセッションからのキーワードを見つけることを意味します。セマンティックな結論は依然としてオペレーターの仕事です。

## 負荷下で変更するもの

月 2 回の午前 3 時のページが週 2 回になる場合:

- 自信がついたら、より多くの `bash` マッチャーを `allow` に昇格することを検討してください。
- slog 出力を [Loki](/ja/guides/observability/) に配線して、ポストモーテムレビューが rousseau が行った正確なツール呼び出しを引用できるようにします。
- [スケジュールタスク](/ja/guides/scheduled-tasks/) を追加して、rousseau が開いているインシデントの毎晩ダイジェストを朝の Slack に実行するようにします。

## 関連ページ

- [ガイド: 監査 + 承認ポリシー](/ja/guides/audit-approval-policies/) — セーフティレバー。
- [ガイド: 読み取り専用モード](/ja/guides/read-only-mode/) — 最も厳格な姿勢。
- [Slack トランスポート](/ja/transports/slack/) — Socket Mode 配線。
- [Bedrock プロバイダー](/ja/providers/bedrock/) — 認証チェーン。
