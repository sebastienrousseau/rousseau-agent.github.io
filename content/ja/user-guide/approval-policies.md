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
description: "Approval policy reference for rousseau-agent: allow_all, deny_all, and pattern-mode approvers with allow/deny regex rules and a configurable default."
keywords: "approval, approver, pattern mode, allow_all, deny_all, regex, safety, tool call"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/user-guide/approval-policies/"
subtitle: "Deep dive on approver modes with worked config."
tags: "approval, policy, pattern-mode, safety"
title: "承認ポリシー"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approval, approver, pattern mode, allow_all, deny_all, regex, safety, tool call"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "承認ポリシー"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "security"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/user-guide/approval-policies/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/approval-policies/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "承認ポリシー"
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
twitter_description: "Approval policy reference for rousseau-agent: allow_all, deny_all, and pattern-mode approvers with allow/deny regex rules and a configurable default."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "承認ポリシー"
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

## コントラクト

すべてのツール呼び出しは、実行前に `Approver.Approve(ctx, ApprovalRequest)` を通過します。インターフェースは `internal/agent/approver.go` にあります:

```go
type Decision string

const (
    DecisionAllow Decision = "allow"
    DecisionDeny  Decision = "deny"
)

type ApprovalRequest struct {
    ToolName  string
    Input     json.RawMessage
    SessionID string
}

type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

`Approve` はホットパス上で同期的に呼び出されます。実装は速やかに戻るか、`ctx` のキャンセレーションを尊重する必要があります。

空でない reason を伴う `DecisionDeny` は、`tool_result` エラーとしてその理由をモデルに返します。モデルはそれから (通常はオペレーターに明確化を求めることで) 適応でき、静かに失敗するのではありません。これは意図的な設計判断です — サイレントな拒否は、注釈付きの拒否より悪い挙動を生みます。

## 出荷される 3 つのモード

### `allow_all`

すべてのツール呼び出しが実行されます。これは承認者が設定されていないときのベースライン挙動です。

```yaml
agent:
  approver:
    mode: allow_all
```

使う場面:

- `claudecli` プロバイダーによる対話的な `rousseau chat` (Claude Code が独自の呼び出しごとの承認を行っている)。
- モデルが何をするかを正確に見たい開発用スモークテスト。

### `deny_all`

すべてのツール呼び出しを単一の理由文字列でブロックします。

```yaml
agent:
  approver:
    mode: deny_all
    reason: "denied by policy for this deployment"
```

使う場面:

- 承認者の配線のスモークテスト。
- モデルが何を試みる *だろうか* を、実際に行動させずに見たい初回検査姿勢。

### `pattern`

ツールごとの正規表現による allow / deny ルール。**deny が allow に勝ちます。** マッチしないリクエストは `default` (`allow` または `deny`) にフォールバックします。

```yaml
agent:
  approver:
    mode: pattern
    default: deny         # safe-by-default; unlisted requests are blocked
    reason: "denied by pattern policy"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
    deny:
      - {tool: bash, match: "rm -rf|sudo|chmod|chown"}
```

## ルールセマンティクス

各 `PatternRule` には 2 つのフィールドがあります:

| フィールド | 意味 |
|---|---|
| `tool` | ツール名 (`read`、`write`、`edit`、`grep`、`bash`、または任意のカスタムツール)。空はすべてのツールにマッチ。 |
| `match` | モデルが生成した生の JSON 入力に対する Go RE2 正規表現。空はすべての入力にマッチ。 |

**マッチ順序:**

1. すべての deny ルールがリクエストに対してテストされます。最初のマッチ → deny。
2. すべての allow ルールがテストされます。最初のマッチ → allow。
3. `default` にフォールバック。空の `default` は `deny` として扱われます — safe-by-default。

より安全な処分が好まれるため、常に deny が勝ちます。広範な `allow` ブロックを追加するオペレーターは、拒否していたカテゴリを誤ってアンロックすることはありません。

## 生の JSON に対するマッチング

`match` 正規表現は、パースされたフィールドに対してではなく、モデルが発した **生の JSON 入力** に対して実行されます。これには 2 つの結果があります:

1. **JSON の形状に対してマッチします。** `bash` 呼び出しの場合、それは `{"command":"ls /tmp"}` のようになります。`"command":\s*"ls\s` にマッチさせてください。
2. **任意のフィールドにマッチできます。** `edit` ツールは `{"path":"/x","old_string":"...","new_string":"..."}` を受け取ります。`path`、`old_string`、または両方にマッチさせられます。

JSON 関連文字を注意深くエスケープしてください:

- ダブルクォートは生の JSON ではリテラルです — YAML のダブルクォート文字列を使う場合、正規表現内で `\"` としてマッチさせてください。
- バックスラッシュは YAML では二重化が必要です: YAML ファイル内の `\\` はコンパイル済み正規表現の `\` になります。

## マッチャーパターンの作業例

### ディレクトリツリーへの編集を制限する

```yaml
allow:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/[^\"]*\""}
  - {tool: write, match: "\"path\":\"/workspace/repo/[^\"]*\""}
```

### 安全なシェルコマンドをホワイトリスト化する

```yaml
allow:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|grep|rg|find|git status|git diff|go test) "}
```

### allow に関係なく破壊的なコマンドを拒否する

```yaml
deny:
  - {tool: bash, match: "rm\\s+-rf|sudo|:\\(\\)\\{ :\\|:& \\};:"}
```

### システムディレクトリへの書き込みを拒否する

```yaml
deny:
  - {tool: write, match: "\"path\":\"/(etc|root|var|usr)/"}
  - {tool: edit,  match: "\"path\":\"/(etc|root|var|usr)/"}
```

## `Default` フィールド

`default: deny` はより安全な処分であり、無人デーモンに推奨される値です。`default: allow` はモデルを反転させます — リストにないすべての呼び出しが実行され、`deny` ルールが主要なレバーになります。

`default: allow` を使う場面:

- デーモンが厳重にロックダウンされたコンテナ ([デプロイ](/ja/deployment/)) 内で実行されており、コンテナがプライマリ境界である場合。
- 何をブロックするかを決める前に、モデルの挙動を見たい実験中。

それ以外のところでは、`default: deny` を選んでください。

## `Reason` フィールド

`reason` は、あらゆる拒否 (または `default: deny` フォールバック) 時にモデルに返される文字列です。空の場合は `denied by pattern policy` (または `deny_all` の場合は `denied by policy`) にフォールバックします。

有用な reason を設定するとモデルの回復が改善します — `denied by pattern policy` の代わりに `denied — this deployment only allows reads inside /workspace; ask the operator to widen the scope` を試してみてください。モデルが実行可能な明確化で返信するのが見られます。

## `claudecli` との相互作用

`provider: claudecli` の場合、Claude Code がツール呼び出しを実行しており、その独自の permission-mode (`bypassPermissions`、`plan`、`default`) もあらゆる動作をゲートします。実効的な挙動は交差です: rousseau の承認者と Claude Code の承認者の **両方** が呼び出しの実行を許可する必要があります。

両者を揃えたままにするのが望ましいです:

- 無人: Claude Code で `bypassPermissions`、rousseau で `mode: pattern` + `default: deny`。
- 読み取り専用検査: Claude Code で `plan`、rousseau で `read`/`grep` のみを許可する `mode: pattern`。[ガイド: 読み取り専用モード](/ja/guides/read-only-mode/) を参照。

## 監査証跡

すべての承認者の判定は slog を通じて発行されます:

| イベント | 意味 |
|---|---|
| `tool.execute` (INFO) | 呼び出しが承認され、実行中。 |
| `tool.denied` (WARN) | 呼び出しがブロックされた。ツール名と reason を含む。 |
| `tool.error` (WARN) | 呼び出しは実行されたが失敗した。 |

パイプラインレシピについては [ガイド: 可観測性](/ja/guides/observability/) を参照してください。

## カスタム承認者

`Approver` を満たす任意の型が動作します。エージェントループを組み込む際に独自のものを配線してください:

```go
myApprover := agent.ApproverFunc(func(ctx context.Context, req agent.ApprovalRequest) (agent.Decision, string) {
    // Consult an external policy engine, prompt the operator, ...
    return agent.DecisionAllow, ""
})

ag := agent.New(provider, registry, logger, agent.Options{Approver: myApprover})
```

インターフェースは意図的に最小限にされている (`Approve` が唯一のメソッド) ため、外部ポリシーエンジン (OPA、Cedar、または特注のルールエンジン) との統合は小さなアダプタで済みます。

## トラブルシューティング

### マッチする allow があっても、すべての呼び出しが拒否される

deny が allow に勝ちます。`internal/agent/approver.go` の 152 行目の `PatternApprover.Approve` は deny ルールを最初にイテレートします。`tool.denied` ログ内で正確な `reason` 文字列を探してください。

### 起動時の正規表現コンパイルエラー

`PatternApprover` は最初の `Approve` で正規表現を遅延コンパイルします。コンパイルエラーは reason `approver: pattern compile: <err>` を伴う `DecisionDeny` になります。Go フレーバーで [regex101.com](https://regex101.com) にて正規表現をテストしてください。

### `mode: pattern` だが `default:` が無視される

`default:` に有効な値は `allow` と `deny` のみです。空または未知の値は `DecisionDeny` (安全なデフォルト) にフォールバックし、警告は出力されません。

### allow ルールが JSON にリテラルにマッチする

正規表現は生のツール呼び出し入力 JSON に対して実行されます。`path` フィールドにマッチさせるには、クォートをエスケープしてください: `"\"path\":\"/workspace/"`。

### 拒否された呼び出しがログに現れない

現れています — `warn` レベルで `tool.denied` として。レベルでフィルタしている場合は、`warn` が含まれることを確認してください。

## 関連ページ

- [ガイド: 監査 + 承認ポリシー](/ja/guides/audit-approval-policies/) — slog 監査証跡を伴う作業例。
- [ガイド: 読み取り専用モード](/ja/guides/read-only-mode/) — 検査姿勢。
- [ユーザーガイド: ツール](/ja/user-guide/tools/) — 承認者がゲートするツール。
- [セキュリティ](/ja/security/) — 信頼境界の概要。
- [エージェントループ](/ja/agent-loop/) — 承認者が呼び出される場所。

## さらに読む

- `internal/agent/approver.go` — `PatternApprover`、`AllowAllApprover`、`DenyAllApprover`。
- `internal/agent/approver_test.go` — テストマトリックス。
- `internal/cli/approver.go` — config → approver 変換。
- `internal/config/config.go` — `ApproverConfig`、`PatternEntry`。
