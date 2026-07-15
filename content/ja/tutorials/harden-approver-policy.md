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
description: "Go from bypassPermissions to a pattern-mode approver with default: deny and validate the audit trail through slog."
keywords: "approver, pattern mode, default deny, tool denied, audit, slog"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/tutorials/harden-approver-policy/"
subtitle: "From bypassPermissions to default-deny with slog-audited rule matching."
tags: "tutorials, approver, pattern-mode, security, audit"
title: "チュートリアル：Approver を強化する"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approver, pattern mode, default deny, tool denied, audit, slog"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "チュートリアル：Approver を強化する"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 46
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/tutorials/harden-approver-policy/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/harden-approver-policy/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "チュートリアル：Approver を強化する"
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
twitter_description: "Go from bypassPermissions to a pattern-mode approver with default: deny and validate the audit trail through slog."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "チュートリアル：Approver を強化する"
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

## 構築するもの

`claudecli` プロバイダーを `bypassPermissions` モード (無人デフォルト) で実行し始めた rousseau デーモンが、`default: deny` の `pattern` モード rousseau-agent 承認者の下に落ち着きます。すべてのツール呼び出しは明示的に allowlist に登録されているかブロックされます。すべての拒否は監査可能な `tool.denied` slog イベントを生成します。

想定時間: テスト付きの適切なルールパスで 30 分。

## 前提条件

- 任意のトランスポートブリッジ (WhatsApp、Slack、Signal — 無人のもの) が実行されている状態でインストールされた rousseau。
- 基本的な Go 正規表現の知識 — 承認者ルールは JSON ツール入力に対する Go RE2 正規表現です。

## 承認者の場所

2 つの独立した層がツール呼び出しを承認できます:

1. **プロバイダー独自のパーミッションモード。** `claudecli` プロバイダー (`internal/llm/claudecli/client.go`) は `claude --permission-mode` に委任します。値は `ClaudeCLIConfig.PermissionMode` (`internal/config/config.go`) で文書化されています: `acceptEdits`、`auto`、`bypassPermissions`、`default`、`dontAsk`、`plan`。無人デーモンは `setUnattendedPermissionDefault` で `bypassPermissions` を固定します。
2. **rousseau 独自の承認者。** `agent.approver` の下で設定 (`internal/config/config.go` の `ApproverConfig`。実装は `internal/agent/approver.go`)。3 つのモード: `allow_all`、`deny_all`、`pattern`。**deny が allow に勝ち、マッチしない呼び出しは `default` にフォールバックします。**

無人デーモンの場合、rousseau 承認者があなたが手動で設定する緩和策です。`claudecli` の独自モードはシートベルトです。

## ステップ 1: ベースライン監査

ルールを書く前に、`mode: allow_all` と `log.format: json` でいくつかの現実的なセッションを実行してください。すべてのツール呼び出しは `tool.execute` (`internal/agent/agent.go`) を発します:

```sh
jq -c 'select(.msg == "tool.execute") | {name, input: .input}' \
  < /var/log/rousseau.jsonl \
  | sort | uniq -c | sort -rn | head
```

これで、エージェントがどのツールをどのパスに対して使用するかの経験的分布が得られます。それが allowlist のシードです。

## ステップ 2: pattern ポリシーをドラフトする

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by pattern policy — ask the operator to loosen the rules"
    allow:
      # Read side: unrestricted within the daemon's filesystem view.
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

      # Editing pinned to /workspace.
      - {tool: edit,  match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}

      # Shell: whitelist of read-only utilities plus git status/diff/log.
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|grep|rg|find|wc|stat|file|which|pwd|env|git status|git diff|git log|go test|go vet|go build)\\b"}

    deny:
      # Absolute denies override any allow above.
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s|ncat"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}    # fork bomb
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit,  match: "\"path\":\"/etc/|/root/|/var/"}
```

デプロイし、slog ストリームを監視してください。関連イベント (`internal/agent/agent.go`):

- `tool.execute` — 呼び出しが実行された。フィールド: `name`、`id`。
- `tool.denied` — 承認者がブロックした。フィールド: `name`、`reason`。
- `tool.error` — 実行されて失敗した。フィールド: `name`、`err`。

## ステップ 3: イテレート

初日は false positive を表面化させます: 承認者がブロックした正当なツール呼び出し。grep してください:

```sh
jq -c 'select(.msg == "tool.denied") | {name, input}' \
  < /var/log/rousseau.jsonl \
  | sort | uniq -c | sort -rn | head
```

繰り返す `tool.denied` それぞれに判断が必要です:

- **本当に必要** — allow ルールを拡張してください。広い (オープンエンドの正規表現) より狭い (パス固定) を推奨します。
- **不要** — 拒否のままにしてください。モデルは別のアプローチにピボットします。

`default: deny` を弱めないでください。それが忘れられていないツールを安全にする性質です。

## ステップ 4: 監査ログの抜粋

見慣れないプロンプトによるプロダクション実行はこう見えました:

```jsonl
{"time":"2026-07-13T18:00:12Z","level":"INFO", "msg":"whatsapp.incoming","from":"447900123456@s.whatsapp.net"}
{"time":"2026-07-13T18:00:14Z","level":"INFO", "msg":"tool.execute","name":"grep","id":"t_1"}
{"time":"2026-07-13T18:00:15Z","level":"INFO", "msg":"tool.execute","name":"read","id":"t_2"}
{"time":"2026-07-13T18:00:17Z","level":"WARN", "msg":"tool.denied","name":"bash","reason":"denied by pattern policy — ask the operator to loosen the rules"}
{"time":"2026-07-13T18:00:18Z","level":"INFO", "msg":"tool.execute","name":"read","id":"t_3"}
{"time":"2026-07-13T18:00:20Z","level":"INFO", "msg":"whatsapp.handler_ok","elapsed":"7.4s"}
```

ここでの 1 つの `tool.denied` は `bash: "curl https://…"` でした。deny ルールがそれを捕捉し、モデルは `read` + `grep` に劣化し、返信はそれでも通りました。

## ステップ 5: ベイクイン

false positive レートが落ち着いたら、config をフリーズし、ソース管理にコミットし (シークレットを除外 — [ガイド: エンタープライズオンボーディング](/ja/guides/enterprise-onboarding/) を参照)、config 変更をコードレビュー越しにゲートしてください。ソースツリーの `internal/agent/approver_test.go` は、ルールセットに対するテストを書く方法のモデルです — CI が壊れたポリシーを捕捉することを望むなら、その形状を内部パッケージにコピーしてください。

## ポリシーが依然として行わないこと

最も厳格な pattern ルールでも:

- **サンドボックスなし。** 許可された `bash` 呼び出しは依然としてデーモンの UID とファイルシステム可視性で実行されます。下に rootless コンテナ ([デプロイ](/ja/deployment/)) を層状に配置してください。
- **レート制限なし。** 秒あたり 10 の許可された呼び出しはすべて許可されます。これが必要な場合はツールレジストリをラップしてください。
- **アウトバウンドネットワーク監査なし。** 承認者は最初の `bash` `command` 文字列を見ますが、それが curl するものは見ません。`curl` と `wget` を全面拒否してください — サンプル deny ルールはこれを行います。

より深い議論については [ガイド: 監査 + 承認ポリシー](/ja/guides/audit-approval-policies/) を参照してください。

## 関連

- [ユーザーガイド: 承認ポリシー](/ja/user-guide/approval-policies/) — すべてのモードのリファレンス。
- [ユーザーガイド: ツール](/ja/user-guide/tools/) — ツールスキーマ、正規表現を書くのに便利。
- [ガイド: 可観測性](/ja/guides/observability/) — `tool.denied` を Loki/Datadog にパイプします。
- [リファレンス: ログ](/ja/reference/logs/) — すべての既知の slog メッセージ。
