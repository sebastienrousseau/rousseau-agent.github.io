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
description: "Configure the claudecli provider: PermissionMode values, model aliases, auth inheritance, and when to prefer this over the direct API."
keywords: "claudecli, claude CLI, subprocess, PermissionMode, bypassPermissions, acceptEdits, Claude Code"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/providers/claudecli/"
subtitle: "Subprocess against the local Claude Code CLI."
tags: "providers, claudecli"
title: "claudecli プロバイダ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "claudecli, claude CLI, subprocess, PermissionMode, bypassPermissions, acceptEdits, Claude Code"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "claudecli プロバイダ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 6
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/providers/claudecli/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/claudecli/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "claudecli プロバイダ"
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
twitter_description: "Configure the claudecli provider: PermissionMode values, model aliases, auth inheritance, and when to prefer this over the direct API."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "claudecli プロバイダ"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p><code>claudecli</code> プロバイダがローカルにインストールされた Claude Code から認証を継承する仕組み、完全な <code>PermissionMode</code> マトリクス、セッション相関のセマンティクス、モデルエイリアス、そして Anthropic API 直接よりこちらを選ぶべき場面を扱います。正典としてこのページと並行して <code>internal/llm/claudecli/client.go</code> を読んでください。</p></aside>

## claudecli を使う場面

`claudecli` は `claude` CLI（Claude Code）をサブプロセスとして起動します。**デフォルトのプロバイダ** であり、次の場合に最適です。

- Claude Code をローカルにインストールし認証済みの場合。
- API キーを配管するのではなく、サブスクリプションプランの Claude Code アカウントを再利用したい場合。
- モデルを `claude` 独自のツール使用ループ内で動作させたい場合（ファイル編集、思考、plan モードなどの機能はそのまま利用可能）。
- rousseau のコンフィグファイル内に一切のシークレット素材を置きたくない場合。

トレードオフ: rousseau のツール `Registry` はこのプロバイダでは **呼び出されません**。`claude` がサブプロセス内で自分のツールを実行します。レスポンスオブジェクトはターン終了時の単一のテキストメッセージとして返ります。`bash`/`edit`/`write` を rousseau の承認ポリシーでゲートしたい場合は、代わりに `anthropic`、`bedrock`、`vertex`、または OpenAI 互換プロバイダを使ってください。

## 認証の継承

`claude` CLI は認証情報を 3 箇所に保持します。

| 場所 | 内容 |
|---|---|
| `~/.claude/` | OAuth トークン（サブスクリプション）、API キーヘルパー出力、ワークスペースコンフィグ。 |
| システムキーチェーン | macOS では `claude` がリフレッシュトークンをログインキーチェーンにキャッシュすることがあります。 |
| `ANTHROPIC_API_KEY` 環境変数 | 設定されていれば、`claude` は OAuth の代わりに API キーモードで使用します。 |

`claudecli` はこれらを直接読みません。各呼び出しは `exec.CommandContext(binary, args...)` です。サブプロセスは親の環境とホームディレクトリを継承し、自分で認証情報を検索します。これが個人オペレーターにとっての「ゼロコンフィグ」の理由です。

<aside class="admonition" data-type="tip"><span class="admonition-title">コンテナのバインド</span><p>コンテナ内で rousseau を実行する場合は、<code>claude</code> がキャッシュされた OAuth トークンをその場でリフレッシュできるよう、<code>~/.claude</code> をコンテナに読み書き可能でバインドマウントしてください。</p></aside>

```ini
Volume=%h/.claude:/home/rousseau/.claude:rw,Z
```

SELinux ホストでは `Z` ラベルが重要です。完全な Quadlet ユニットは [デプロイ](/ja/deployment/) を参照してください。

## 設定

```yaml
provider: claudecli

claudecli:
  binary: claude
  model: sonnet
  permission_mode: bypassPermissions
  extra_args:
    - --add-dir
    - /workspace
```

| フィールド | デフォルト | 効果 |
|---|---|---|
| `binary` | `claude` | `$PATH` から解決される実行ファイル。複数バージョンの `claude` がある場合は絶対パスを指定してください。 |
| `model` | *空* | `--model <value>` として渡されます。空の場合は `claude` のデフォルトを使用。 |
| `permission_mode` | *空* | `--permission-mode <value>` として渡されます。以下の表を参照。 |
| `extra_args` | `[]` | 各呼び出しで `-p <prompt>` の前に追加されます。 |

各フィールドは `internal/config/config.go` の `ClaudeCLIConfig` にマップされます。各ターンで組み立てられるサブプロセスコマンドラインは次のとおりです。

```sh
claude --print --output-format json \
  --session-id <sessionID> \
  --system-prompt <systemPrompt> \
  --model <model> \
  --permission-mode <permissionMode> \
  <extra_args...> \
  <prompt>
```

<aside class="admonition" data-type="warning"><span class="admonition-title">STDOUT のパース</span><p>Rousseau は <code>claude</code> が stdout に JSON エンベロープを出力することを期待します。（監査、赤字化、レート制限のために）<code>claude</code> をシェルスクリプトでラップする場合、ラッパは stdout を無改変で転送しなければなりません。パーサは最初の <code>{</code> より前の先頭ログ行を許容します（<code>internal/llm/claudecli/client.go</code> の <code>parseResult</code> を参照）が、JSON エンベロープの後にゴミがあると失敗します。</p></aside>

## PermissionMode マトリクス

`PermissionMode` フラグは `claude` 自身の `--permission-mode` を反映します。値を強制するのはサブプロセスであり、rousseau は二重チェックしません。

<div class="tabs" data-tabs="claudecli-permission-modes">
  <div class="tab-list" role="tablist" aria-label="PermissionMode selector">
    <button role="tab" aria-selected="true">Attended</button>
    <button role="tab" aria-selected="false">Unattended</button>
    <button role="tab" aria-selected="false">Read-only</button>
  </div>
  <div class="tab-panel" role="tabpanel">

ターミナルの前に人間がいてツール呼び出しを承認できる対話的 TUI セッション。

| モード | 挙動 |
|---|---|
| `default` | Claude Code はすべてのツール呼び出しで対話的に問い合わせます。探索的なセッションに最適。 |
| `acceptEdits` | ファイル編集は問い合わせなしで進みます。他のツールは問い合わせを継続します。編集面を信頼できる場合に有用。 |
| `auto` | ツールに基づいて自動判断します。claude の組み込みヒューリスティックに任せたい場合に使用します。 |

```yaml
claudecli:
  permission_mode: acceptEdits
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

チャットトランスポート（WhatsApp、Slack、Discord、Signal など）には、プロンプトに応答する人間がターミナル前にいません。

| モード | 挙動 |
|---|---|
| `bypassPermissions` | すべてのツール呼び出しが問い合わせなしで実行されます。完全な影響範囲を受容します。 |
| `dontAsk` | bypass と類似に扱われるエイリアス。 |

```yaml
claudecli:
  permission_mode: bypassPermissions
```

CLI は、オペレーターが明示しない場合、無人稼働のデーモンに対して自動的に `bypassPermissions` を設定します（`internal/cli` の `setUnattendedPermissionDefault` を参照）。

<aside class="admonition" data-type="caution"><span class="admonition-title">影響範囲</span><p><code>bypassPermissions</code> はモデルにデーモンの権限で直接 <code>bash</code> アクセスを与えます。(a) 堅牢化されたコンテナ、(b) allowlist、(c) rousseau 側の pattern モード approver と組み合わせるか、rousseau がツール実行前に承認を強制できる <code>claudecli</code> 以外のプロバイダを使ってください。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

書き込みを一切行わせたくない大規模リファクタリングやコードレビューのための探索モード。

| モード | 挙動 |
|---|---|
| `plan` | プランナモード。read と grep は許可され、書き込みは抑止されます。 |

```yaml
claudecli:
  permission_mode: plan
```

二重の安全策として rousseau 自身の読み取り専用モード（[ガイド: 読み取り専用モード](/ja/guides/read-only-mode/) を参照）と組み合わせてください。

  </div>
</div>

## セッション相関

`claudecli` は会話状態をサブプロセス内で維持します。Rousseau は自身のセッション ID を `claude` のセッション ID と 2 つのフラグで相関させます。

- `claude -p --session-id <uuid>` は新しいセッションを作成します。UUID が既に存在すると `claude` は `already in use` エラーを返します。
- `claude -p --resume <uuid>` は既存のセッションを再開します。未知のものだと `claude` はエラーを返します。

Rousseau はインメモリの `SessionCache`（デフォルトは `InMemorySessionCache`）を用いてフラグを選択します。`claude` が以前の rousseau 実行の状態をすでに持っているコールドスタートでのキャッシュミス時、プロバイダは楽観的に `--session-id` を試し、`already in use` エラーを捕捉して `--resume` でリトライします。`internal/llm/claudecli/client.go` の `(*Provider).Complete` のコメントを参照してください。

プロバイダを組み込む呼び出し側は、`provider.WithCache(store)` で永続キャッシュに差し替えられます。`state.sqlite` ストアは同じインタフェースを実装し、デーモン再起動を越えて生き残るため、再起動後の最初のターンでのコールドスタートラウンドトリップを回避できます。

## モデルエイリアス

`claude` のモデルエイリアスはサブプロセスによってそのまま尊重されます。

| エイリアス | 指す先 |
|---|---|
| `sonnet` | 現在デフォルトの Sonnet 帯モデル。 |
| `opus` | 現在デフォルトの Opus 帯モデル。 |
| `haiku` | 現在デフォルトの Haiku 帯モデル。 |

デーモン再起動をまたぐ再現性（スキルベンチマーク、cron ジョブ、バッチ実行）のためには、正確なモデル ID を固定してください。

```yaml
claudecli:
  model: claude-sonnet-4-6
```

<aside class="admonition" data-type="note"><span class="admonition-title">エイリアスはリリースに追従する</span><p>Anthropic が新しいモデルをリリースするとエイリアスは移ります。2026 年 7 月の <code>sonnet</code> エイリアスは、2026 年 4 月の <code>sonnet</code> エイリアスと同じ重みを指しません。ワークフローが特定の挙動に依存するなら、正確な ID を固定してください。</p></aside>

## スキルとの組み合わせ

`claudecli` はセッション作成時に `--system-prompt` でシステムプロンプトを送信します。`claude` はこれをそのまま尊重し、`--resume` 時の後続の `--system-prompt` 値は無視します。これは rousseau の使い方と一致します。`SkillsProvider` の出力は呼び出し前に挿入されます。

```
<agent.SystemPrompt>

<skill 1 markdown>

<skill 2 markdown>

<RecallProvider appendix>
```

`internal/agent/agent.go` の `systemPrompt()` を参照してください。スキルはどのプロバイダでも同じように動作します。合成の仕組みはプロバイダではなく `agent.Agent` にあります。

<aside class="admonition" data-type="tip"><span class="admonition-title">プロンプトキャッシュ</span><p>Anthropic 直接プロバイダはシステムプロンプトを ephemeral プロンプトキャッシュ用にマークします（<code>internal/llm/anthropic/cache.go</code> を参照）。<code>claudecli</code> はマークしません。<code>claude</code> が独自に内部でキャッシュを管理するためです。プロンプトキャッシュによる測定可能な節約が欲しい場合は <code>provider: anthropic</code> を使ってください。</p></aside>

## 注意点

- **プロバイダ横断のポータビリティなし。** `claudecli` に対して作成されたセッションは `anthropic` にはポータブルではありません。モデル側の状態は `claude` 内部にあります。途中でプロバイダを切り替えると新しいセッションが強制されます。
- **ツールレジストリは呼び出されない。** `bash`、`edit`、`write`、`grep`、`read` は `rousseau` ではなく `claude` によって実行されます。Rousseau の `agent.Approver` はこれらの呼び出しをゲートできません。rousseau 側での承認強制が必要なら `claudecli` 以外のプロバイダを使ってください。
- **`--add-dir` のスコープ。** デフォルトでは `claude` は自身のワークスペース外の読み取りを拒否します。`extra_args` で `--add-dir /workspace`（またはソースがある場所）を渡して広げてください。制御の失われを補いたい場合は、rousseau の承認ポリシーをトランスポート層で組み合わせます。
- **ストリーミング。** `claudecli` は `claude -p --output-format json`（非ストリーミング）を使用します。`internal/llm/claudecli/stream.go` のストリーミング経路は `--output-format stream-json` を読みます。組み込み統合から `StreamingProvider` を使うことでオプトインできます。
- **環境変数の漏出。** サブプロセスは親のすべての環境変数を継承します。rousseau の環境で `ANTHROPIC_API_KEY` が設定されていると、`claude` はキャッシュされた OAuth より API キーを優先します。通常は問題ありませんが、課金先が変わります。

## トラブルシューティング

### `claudecli: run: exec: "claude": executable file not found in $PATH`

`claude` が `PATH` にありません（またはコンテナイメージにバンドルされていません）。修正は 2 つ:

1. `claudecli.binary` に絶対パスを設定する。
2. Claude Code をコンテナのランタイム層に追加する。リファレンスの `docker/Dockerfile` はこの理由で `node:22-alpine` を使用しています。

### `claudecli: model error: session id already in use`

同じ `claude` インストールに対して同じセッション ID で 2 つの rousseau プロセスを実行しているか、インメモリキャッシュが `claude` がまだ覚えているセッションを破棄しました。前述の楽観的リトライは後者のケースを扱います。前者は並行するデーモンが競合していることを意味します。

### `claudecli: no JSON in output`

`claude` が stdout に JSON 以外を出力したか、エンベロープを出す前に終了しました。よくある原因: Claude Code 側の API キーが無効、`--output-format json` より古い `claude` バージョン、進捗マーカーを出力するシェルラッパ。切り分けには `claude -p --output-format json 'hello'` を直接実行してください。

### 返信が文中で途切れる

`claude` の出力は `--max-turns` と自身の内部トークンバジェットで制限されます。Rousseau は `--max-turns` を設定しません。`extra_args` で設定している場合は引き上げてください。長い生成には、`internal/llm/anthropic/client.go` から `MaxTokens` を制御できる直接 API プロバイダの利用を検討してください。

### サブスクリプションプランはレート制限されているが API は問題ない

サブスクリプションプランの `claude` CLI には、隠された会話単位・ウィンドウ単位のリミットがあります。それに当たった場合、API キーを持つ `provider: anthropic` に切り替えてください。直接 API には明示された公開リミットがあります（[ガイド: レート制限](/ja/guides/rate-limits/) を参照）。

## 関連ページ

- [プロバイダ: Anthropic](/ja/providers/anthropic/) — プロンプトキャッシュとストリーミングを持つ直接 API。
- [プロバイダ: Bedrock](/ja/providers/bedrock/) — AWS マネージドの Claude。
- [ユーザーガイド: 承認ポリシー](/ja/user-guide/approval-policies/) — rousseau 層でツール呼び出しをゲートする方法。
- [スキル](/ja/skills/) — システムプロンプト付録の合成方法。
- [設定](/ja/configuration/) — 文脈内の `claudecli` スタンザ。

## さらに読む

- `internal/llm/claudecli/client.go` — サブプロセス起動、セッション相関、JSON パース。
- `internal/llm/claudecli/stream.go` — `--output-format stream-json` を用いるストリーミング版。
- `internal/config/config.go` — `ClaudeCLIConfig` 構造体。
- `internal/cli/root.go` — チャットトランスポート向けに `setUnattendedPermissionDefault` が `bypassPermissions` を選ぶ方法。
