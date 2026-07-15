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
description: "Worked example: lock down the bash tool with a pattern-mode approver, deny rules on destructive commands, and slog-driven audit trail."
keywords: "approval policy, pattern mode, bash tool, deny rules, audit trail, slog"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/audit-approval-policies/"
subtitle: "Pattern-mode approver with deny rules on the bash tool."
tags: "guides, audit, approval, pattern-mode, bash, deny"
title: "ガイド：監査と承認ポリシー"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approval policy, pattern mode, bash tool, deny rules, audit trail, slog"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：監査と承認ポリシー"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 34
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/audit-approval-policies/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/audit-approval-policies/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "ガイド：監査と承認ポリシー"
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
twitter_description: "Worked example: lock down the bash tool with a pattern-mode approver, deny rules on destructive commands, and slog-driven audit trail."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド：監査と承認ポリシー"
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

## 問題

無人のチャットトランスポートデーモンは、リアルタイムでツール呼び出しを承認する人間がターミナルにいません。モデルが `rm -rf /workspace/*` を実行しようとする場合、何かがそれを止める必要があります。rousseau の `pattern` モード承認者はそのレバーです。

脅威はモデルが暴走することではありません — トランスポートチャネル経由で侵害された、または方針から外れた指示がデーモンに到達することです。`default: deny` フォールバック付きのパターンモードポリシーは、リスクを境界付けて監査可能にします。

## 承認者モード

3 つの組み込みモードが出荷されます (`internal/agent/approver.go` を参照):

| モード | 動作 | 使用時 |
|---|---|---|
| `allow_all` | すべてのツール呼び出しが実行されます。 | `claudecli` プロバイダが独自の承認を行うインタラクティブな `rousseau chat`。 |
| `deny_all` | すべてのツール呼び出しがブロックされます。拒否理由は `tool_result` エラーとしてモデルに表面化され、適応できます。 | 読み取り専用検査姿勢、スモークテスト。 |
| `pattern` | ツールごとの正規表現許可 / 拒否ルール。**拒否が許可に勝ちます。** マッチしないリクエストは `default` にフォールバックします。 | プロダクションの無人デーモン全般。 |

## 作業例の設定

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by pattern policy — ask the operator"
    allow:
      # Read-side tools: no restriction inside the workspace.
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

      # Edit inside /workspace only.
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}

      # Write inside /workspace only.
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}

      # Shell commands: whitelist of safe read-side utilities plus git status/diff.
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|grep|rg|find|wc|stat|file|which|pwd|env|git status|git diff|git log|go test|go vet|go build)\\b"}

    deny:
      # Absolute deny rules override any allow above.
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s|ncat"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}   # fork bomb
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit, match: "\"path\":\"/etc/|/root/|/var/"}
```

`PatternApprover.Approve` から 2 つの重要な特性が導き出されます:

1. **拒否が勝つ。** すべての拒否ルールは、任意の許可ルールの前にチェックされます。これは逆よりも安全です。広い許可を追加するオペレーターは、拒否されていると思っていたカテゴリを誤って解除できません。
2. **マッチしない → 拒否。** `default: deny` では、オペレーターが列挙し忘れたツール呼び出しはすべてブロックされます。これは安全なデフォルトの傾向です。逆を望む場合は `default: allow` を設定してください。

## 監査証跡の読み方

すべてのツール呼び出しとすべての拒否は、slog ロガーを通じて発行されます:

```
INFO tool.execute name=read id=t_1
INFO tool.execute name=grep id=t_2
WARN tool.denied  name=bash reason="denied by pattern policy — ask the operator"
```

デーモンは設定可能なレベルとフォーマット (`log.level`、`log.format`) で `slog` を使用します。プロダクションでは、下流のツール (Loki、Vector、Datadog) がきれいにパースできるよう `format: json` を推奨します。パイプラインレシピについては [ガイド: 可観測性](/ja/guides/observability/) を参照してください。

すべての拒否は安定した構造化キーを持ちます:

- `tool.denied` — ツール呼び出しがブロックされました。フィールド: `name` (ツール識別子)、`reason` (`PatternApprover.DenyReason` または組み込みフォールバックから)。
- `tool.execute` — ツール呼び出しが実行されました。フィールド: `name`、`id` (相関のためにモデルが発行した呼び出し ID)。
- `tool.error` — ツールが実行されたが失敗しました。フィールド: `name`、`err`。

`tool.denied` に対する `slog` フィルタは、ほとんどのコンプライアンスフレームワークが要求する「ブロックされた試行」の監査ビューを提供します。

## ポリシーのテスト

ソースツリーの `internal/agent/approver_test.go` は、広いマトリックスで `PatternApprover` を行使します。独自のルールをスモークテストするには:

```sh
rousseau chat
> Run `rm -rf /tmp/foo` for me.
```

モデルは `bash` ツール呼び出しを試みます。デーモンは `tool.denied` をログし、`reason` 文字列をモデルに返します。モデルは通常、方向転換します (「それは実行できません — 何をしようとしていたか教えてくれますか?」)。

リファレンステストマトリックスについては、`internal/agent/approver_test.go` を参照してください — 同じルール形状がそこで行使されます。

## 手動オーバーライドの追加

時々、オペレーターは単一の危険な呼び出しを手動で承認したいことがあります。最もシンプルなパターン:

1. `rousseau chat` (インタラクティブ TUI) で `mode: allow_all` を設定します。`claudecli` プロバイダが独自の呼び出しごとの承認プロンプトを処理します。
2. すべての無人デーモンで `mode: pattern` を維持します。

現在、チャットトランスポート上に呼び出しごとのインタラクティブ承認 UI はありません — 安全性のストーリーは完全に正規表現 + slog です。

## ポリシーが行わないこと

- **ツールをサンドボックス化しません。** 承認者を通過した `bash` 呼び出しは、デーモンの UID とそのファイルシステム可視性で実行されます。下に rootless コンテナ ([デプロイ](/ja/deployment/)) を重ねてください。
- **レート制限しません。** 秒あたり 10 回の許可された `bash` 呼び出しが許可されます。レート制限が必要な場合は、ツールレジストリをラップしてください。
- **送信ネットワーク呼び出しを監査しません。** `bash` 呼び出しが何かを curl した場合、承認者は URL を見ません — 最初の `bash` `command` 文字列のみです。パターンレベルで `curl` と `wget` を完全に拒否してください。

## 一般的なパターン

### ディレクトリツリーへの編集ロック

```yaml
allow:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/[^\"]*\""}
  - {tool: write, match: "\"path\":\"/workspace/repo/[^\"]*\""}
deny:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/(\\.git|node_modules|vendor)/"}
```

### 読み取り専用監査者

```yaml
mode: pattern
default: deny
allow:
  - {tool: read, match: ".*"}
  - {tool: grep, match: ".*"}
```

`provider.claudecli.permission_mode: plan` と組み合わせると、これは読み取り専用の検査姿勢になります — [ガイド: 読み取り専用モード](/ja/guides/read-only-mode/) を参照してください。

### Git ファーストワークフロー

```yaml
allow:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"git (status|diff|log|show|branch|stash|fetch|pull --ff-only)\\b"}
deny:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"git (push|reset --hard|clean -fd|checkout --)\\b"}
```

## 5 つのリファレンスルールセット

<div class="tabs" data-tabs="approval-rulesets">
  <div class="tab-list" role="tablist" aria-label="Reference ruleset">
    <button role="tab" aria-selected="true">Dev laptop</button>
    <button role="tab" aria-selected="false">Staging</button>
    <button role="tab" aria-selected="false">Production</button>
    <button role="tab" aria-selected="false">Oncall bot</button>
    <button role="tab" aria-selected="false">Read-only</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**開発用ラップトップ。** デフォルトで許容的、本当に危険なものを拒否します。有人ターミナルを前提とします。

```yaml
agent:
  approver:
    mode: pattern
    default: allow
    deny:
      - {tool: bash, match: "rm\\s+-rf\\s+/"}
      - {tool: bash, match: "sudo(?!\\s+-n)"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}
      - {tool: write, match: "\"path\":\"/etc/|/root/"}
      - {tool: edit, match: "\"path\":\"/etc/|/root/"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**ステージング。** ワークスペースの明示的な許可リスト、外側はすべて拒否。ブラスト半径が限られた共有ステージングデーモンに適しています。

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by staging policy — ping #platform for exceptions"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: bash, match: "^\\{\"command\":\"git (status|diff|log|show|branch|fetch|pull --ff-only)\\b"}
      - {tool: bash, match: "^\\{\"command\":\"(ls|cat|grep|rg|find)\\s"}
    deny:
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s"}
      - {tool: edit, match: "\"path\":\"/workspace/(\\.git|node_modules|vendor)/"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**プロダクション。** 拒否ファースト。すべての許可されたコマンドが明示的に列挙されます。顧客向けの質問に答えるプロダクションデーモンに適しています。

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by production policy — this daemon is read-mostly"
    allow:
      - {tool: read, match: "\"path\":\"/workspace/(runbooks|docs|src)/"}
      - {tool: grep, match: "\"path\":\"/workspace/(runbooks|docs|src)/"}
      - {tool: bash, match: "^\\{\"command\":\"(ls|cat|rg)\\s"}
    deny:
      # Layered denies just in case.
      - {tool: write, match: ".*"}
      - {tool: edit, match: ".*"}
      - {tool: bash, match: "\\b(rm|mv|cp|dd|mkfs|kill|killall)\\b"}
      - {tool: bash, match: "\\b(curl|wget|nc|ncat|ssh|scp|rsync)\\b"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**オンコールボット。** 監視のクエリ、ログの追跡は可能ですが、サービスの再起動やコードの編集はできません。Slack 向けのインシデントレスポンスヘルパーに適しています。

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied — oncall bot can query, not mutate"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\{\"command\":\"(kubectl|helm|argocd) (get|describe|logs|top|status)\\b"}
      - {tool: bash, match: "^\\{\"command\":\"(curl|http|wget) -[gsL]* https?://monitoring\\."}
      - {tool: bash, match: "^\\{\"command\":\"(pg_dump|psql -c 'SELECT|redis-cli GET)\\b"}
    deny:
      - {tool: write, match: ".*"}
      - {tool: edit, match: ".*"}
      - {tool: bash, match: "\\b(kubectl (apply|delete|edit|scale)|helm (install|upgrade|uninstall))\\b"}
      - {tool: bash, match: "\\b(systemctl (start|stop|restart|reload))\\b"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**読み取り専用監査者。** 書き込みなし、シェルなし。コードレビューボットやドキュメント解説デーモンに適しています。

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "read-only auditor — no side effects permitted"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
```

`provider.claudecli.permission_mode: plan` と `provider.claudecli.extra_args: ["--allowed-tools", "read,grep"]` を組み合わせて、二重の強制を行ってください — モデルは文字通り他のツールをリクエストできません。

  </div>
</div>

## トラブルシューティング

### 許可ルールがあるのにすべての呼び出しが拒否される

拒否が許可に勝ちます。拒否ルールのいずれかが意図せずマッチしていないか確認してください。ログ行 `tool.denied name=<X> reason=<Y>` に正確な理由が含まれています。

### パターン正規表現のコンパイルエラー

`PatternApprover` は最初の使用時にルールを遅延コンパイルします。コンパイルエラーは、理由 `approver: pattern compile: <err>` の `DecisionDeny` になります。正規表現を修正してください。Go フレーバーを選択した regex101.com が友です。

### 正規表現が JSON を意味的にではなく文字通りにマッチする

`match` 正規表現は、ツール呼び出しの生の JSON 入力に対して実行されます。引用符とバックスラッシュを適切にエスケープしてください: `"\"path\":\"/workspace/"` は `edit` または `write` 呼び出しの `path` フィールドにマッチします。

### `deny_all` が何もブロックしない

`mode: deny_all` (`mode: deny` ではない) を確認してください。有効なモードは `allow_all`、`deny_all`、`pattern` です。`allow` と `deny` 単独は `_all` バリアントのエイリアスとして扱われますが、正確な文字列の方が安全です。

### `bash` の許可ルールがマッチしない

`bash` 入力は `{"command":"ls -la"}` のような JSON です。シェルコマンド文字列だけでなく、その JSON リテラルに対してマッチさせてください。`^\\{\"command\":\"ls` のようなパターンを使用します。

## 関連ページ

- [ユーザーガイド: 承認ポリシー](/ja/user-guide/approval-policies/) — より深いリファレンスと作業例。
- [ユーザーガイド: ツール](/ja/user-guide/tools/) — すべての組み込みツールのスキーマ。
- [ガイド: 可観測性](/ja/guides/observability/) — 監査証跡を表面化します。
- [ガイド: 読み取り専用モード](/ja/guides/read-only-mode/) — 二重の強制。
- [セキュリティ](/ja/security/) — 信頼モデルの概要。

## 参考資料

- `internal/agent/approver.go` — `PatternApprover`、`AllowAllApprover`、`DenyAllApprover`。
- `internal/agent/approver_test.go` — テストマトリックス。
- `internal/cli/approver.go` — 設定 → 承認者の変換。
- `internal/config/config.go` — `ApproverConfig`、`PatternEntry`。
