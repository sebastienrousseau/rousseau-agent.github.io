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
description: "Install rousseau-agent, configure a provider, hold your first conversation, wire a transport, and verify the release supply chain in about five minutes."
keywords: "quickstart, install, first conversation, whatsapp, cosign, SLSA, SBOM, provider"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/quickstart/"
subtitle: "5 分で始める rousseau：インストール、設定、対話、検証。"
tags: "quickstart, install, provider, transport, supply-chain"
title: "クイックスタート"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "quickstart, install, first conversation, whatsapp, cosign, SLSA, SBOM, provider"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "クイックスタート"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 0
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/quickstart/index.html"
item_link: "https://docs.rousseau-agent.dev/quickstart/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "クイックスタート"
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
twitter_description: "Install rousseau-agent, configure a provider, hold your first conversation, wire a transport, and verify the release supply chain in about five minutes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "クイックスタート"
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

## 5 分で始める rousseau

Rousseau は、Bubble Tea TUI、`~/.local/share/rousseau/sessions.db` にある SQLite セッションストア、9 つのチャットトランスポート（WhatsApp、Signal、Telegram、Slack、Discord、Matrix、iMessage、SMS、Email）を同梱する単一の静的 Go バイナリです。SaaS コントロールプレーンなし、テレメトリなし、ライセンスサーバーなし。LLM は自分で用意します。

このページはエンドツーエンドで案内します：

- [ ] **1. rousseau をインストール** — ソースから、`go install`、または cosign 検証済みリリースから。
- [ ] **2. LLM を設定** — プロバイダーを選択（デフォルトは `claudecli`、Anthropic、Bedrock、Vertex、あるいは任意の OpenAI 互換エンドポイント）。
- [ ] **3. 最初の会話を行う** — ターミナルで `rousseau chat`。
- [ ] **4. トランスポートを追加** — 許可リスト JID を用いた WhatsApp のペアリング。
- [ ] **5. サプライチェーンを検証** — cosign でチェックサムファイルを検証し、CycloneDX SBOM と SLSA-3 プロヴェナンスを読む。

ほとんどのオペレーターは 10 分以内に完了します。

## 1. rousseau をインストール

<aside class="admonition" data-type="tip"><span class="admonition-title">推奨</span><p>すでに Go 1.26+ をお持ちであれば、<code>go install</code> が最速の経路です。本番環境では <code>cosign verify-blob</code> によって署名付きリリースを利用し、サプライチェーン保証を維持してください。</p></aside>

<div class="tabs" data-tabs="qs-install">
  <div class="tab-list" role="tablist" aria-label="Install method">
    <button role="tab" aria-selected="true">go install</button>
    <button role="tab" aria-selected="false">From source</button>
    <button role="tab" aria-selected="false">Signed release</button>
    <button role="tab" aria-selected="false">Container</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
rousseau version
```

バイナリは `modernc.org/sqlite` を埋め込むため（`internal/state/sqlite/store.go` を参照）、実行時に libc や CGo の依存関係はありません。macOS、Linux、Windows で同一に動作します。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` は `go vet`、`golangci-lint`、`go test -race`、`govulncheck` を実行します — CI が強制するのと同じゲートです。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

タグ付きリリースごとに、チェックサム付きアーカイブ、CycloneDX SBOM、SLSA-3 プロヴェナンス証明、およびチェックサムファイルに対する cosign 署名が公開されます：

```sh
curl -LO https://github.com/sebastienrousseau/rousseau-agent/releases/download/v0.6.0/rousseau_0.6.0_linux_amd64.tar.gz
curl -LO https://github.com/sebastienrousseau/rousseau-agent/releases/download/v0.6.0/rousseau_0.6.0_checksums.txt
curl -LO https://github.com/sebastienrousseau/rousseau-agent/releases/download/v0.6.0/rousseau_0.6.0_checksums.txt.sig

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_0.6.0_checksums.txt.sig \
  rousseau_0.6.0_checksums.txt

sha256sum -c rousseau_0.6.0_checksums.txt --ignore-missing
tar -xzf rousseau_0.6.0_linux_amd64.tar.gz
sudo install -m 0755 rousseau /usr/local/bin/
```

<aside class="admonition" data-type="note"><span class="admonition-title">注</span><p><code>cosign</code> の ID は <code>sebastienrousseau/rousseau-agent</code> の GitHub Actions OIDC にスコープされています。信頼ルートについては <a href="/ja/security/">セキュリティ</a> を参照してください。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau は `docker/Dockerfile` に Podman フレンドリーな `Dockerfile`、`docker/rousseau-agent.container` に systemd Quadlet ユニットを同梱しています。ghcr.io で公開されるイメージはロードマップにあります。それまではローカルでビルドしてください：

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
```

ハードニング済みランタイム構成（rootless、`DropCapability=all`、`NoNewPrivileges=true`、seccomp）を備えたリファレンス Quadlet ユニットについては [デプロイ](/ja/deployment/) を参照してください。

  </div>
</div>

### OS 固有の前提条件

<div class="tabs" data-tabs="qs-os">
  <div class="tab-list" role="tablist" aria-label="Operating system">
    <button role="tab" aria-selected="true">macOS</button>
    <button role="tab" aria-selected="false">Linux</button>
    <button role="tab" aria-selected="false">Windows</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```sh
brew install go@1.26
# For the container path:
brew install podman
podman machine init && podman machine start
```

デフォルトの `claudecli` プロバイダーには、https://claude.ai/download から Claude Code をインストールし、`claude login` を一度実行してください。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Go 1.26+ をパッケージマネージャー、または https://go.dev/dl からインストールしてください。コンテナ経路では、`pasta` ネットワークモードで rootless Podman ≥ 5.x を使用します。

```sh
# Debian/Ubuntu
sudo apt install golang-1.26 podman

# Arch
sudo pacman -S go podman

# Fedora
sudo dnf install golang podman
```

Claude Code CLI（`claudecli` プロバイダー用、オプション）：https://claude.ai/download からダウンロード。

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau は `go install` により Windows でネイティブに動作します。コンテナリファレンスデプロイは Linux 専用です。Windows では Podman 経路に WSL 2 を使用してください。

```powershell
winget install GoLang.Go
# Or: choco install golang
```

`claudecli` の場合は、https://claude.ai/download から Claude Code をインストールしてください。

<aside class="admonition" data-type="warning"><span class="admonition-title">Windows に関する注意</span><p>一部のトランスポートパッケージはサブプロセス（<code>signal-cli</code>）を呼び出したり、OS 固有のパス（<code>~/.local/share/</code>）を開いたりします。<code>whatsapp</code>、<code>slack</code>、<code>discord</code>、<code>telegram</code>、<code>matrix</code>、<code>email</code>、<code>sms</code> トランスポートはすべてクロスプラットフォームです。<code>signal</code> と <code>imessage</code> は、それぞれのホストツールが必要です。</p></aside>

  </div>
</div>

## 2. LLM を設定する

コンフィグは `~/.config/rousseau/config.yaml` にあります（`--config` で上書き可能）。各フィールドは `internal/config/config.go` で定義されています。デフォルトプロバイダーは `claudecli` で、ローカルの `claude` CLI にシェルアウトするため、API キーがラップトップから外に出ることはありません。

### claudecli（デフォルト、キー不要）

Claude Code（`claude`）がすでにインストールされ、認証済みであれば、それで完了です。Rousseau はその OAuth セッションを継承します：

```yaml
provider: claudecli

claudecli:
  binary: claude              # optional; PATH lookup by default
  permission_mode: default    # or bypassPermissions for unattended daemons
```

[Providers: claudecli](/ja/providers/claudecli/) を参照してください。

### Anthropic API

直接 Anthropic。`internal/llm/anthropic/client.go` の公式 `anthropic-sdk-go` を使用します：

```sh
export ANTHROPIC_API_KEY=sk-ant-…
```

```yaml
provider: anthropic
anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096
```

`ANTHROPIC_API_KEY` は環境から直接読み込まれます（`internal/config/config.go` の `config.Load` を参照）。キーはディスクに置く必要は一切ありません。[Providers: Anthropic](/ja/providers/anthropic/) を参照してください。

### AWS Bedrock

標準の AWS 認証情報チェーン（プロファイル、IMDS、IRSA）を使用します。リージョンとモデルは `internal/config/config.go` の `BedrockConfig` から取得されます：

```yaml
provider: bedrock
bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
  profile: default            # optional named profile
  max_tokens: 4096
```

`config.yaml` に API キーは存在しません。[Providers: Bedrock](/ja/providers/bedrock/) を参照してください。

### Google Vertex AI

Anthropic on Vertex。サービスアカウント JSON ファイルを読み込みます。設定フィールドは `VertexConfig` で定義されています：

```yaml
provider: vertex
vertex:
  project: my-gcp-project
  region: europe-west4
  model: claude-sonnet-4-6@20250101
  credentials_file: /etc/rousseau/vertex.json
  max_tokens: 4096
```

[Providers: Vertex](/ja/providers/vertex/) を参照してください。

### OpenAI 互換（OpenRouter、Ollama、vLLM、LM Studio）

プロバイダー名 `openai`、`openrouter`、`ollama` は `OpenAIConfig` を共有します。OpenRouter と Ollama のベース URL は `setDefaults` にデフォルト値があります（`https://openrouter.ai/api/v1` と `http://localhost:11434/v1`）。それ以外は明示的な `base_url` を持つ `openai` ブロックに入ります：

```yaml
provider: ollama              # or: openai, openrouter
ollama:
  model: llama3.1:70b-instruct
  base_url: http://localhost:11434/v1
```

[Providers: OpenAI 互換](/ja/providers/openai-compatible/) と [Guides: セルフホスト vLLM](/ja/guides/self-hosted-vllm/) を参照してください。

## 3. 最初の会話を行う

```sh
rousseau chat
```

Bubble Tea TUI（`internal/tui/model.go`）が表示されます：

- 上部の **ビューポート** がトランスクリプトをスクロールします。アシスタントのテキストは到着するにつれてストリーミングされます。
- 下部の **テキストエリア** が入力を受け取ります。送信は `Enter`、終了は `Ctrl+C`。
- LLM ターン中に **スピナー** が表示されます。トークンが到着すると小さなストリーミングインジケーターが表示されます。
- すべてのターンは `~/.local/share/rousseau/sessions.db` の SQLite に永続化されます。WAL ジャーナリングは `internal/state/sqlite/store.go` の `Open()` によって有効化されるため、TUI を開いたまま同じデータベースに対して他の rousseau コマンド（`rousseau session list`、`rousseau mcp`）を安全に実行できます。

まずは小さなことを尋ねてみてください — 例えば「`internal/tools/builtin` の下のファイルをリストして」など — すると rousseau は必要に応じて組み込みツール `read`、`grep`、`edit`、`write`、`bash`（`internal/tools/builtin/*.go`）を呼び出します。キーバインドについては [ユーザーガイド: TUI](/ja/user-guide/tui/)、スキーマについては [ユーザーガイド: ツール](/ja/user-guide/tools/) を参照してください。

スクリーンショットのプレースホルダー: TUI は 2 行のステータスバー（セッション ID とプロバイダー）、色付けされたアシスタント + ユーザーメッセージのビューポート、そしてフォーカスされた下部のテキストエリアを表示します。

## 4. トランスポートを追加（WhatsApp）

WhatsApp はペアリングが最も厳格であるため、リファレンストランスポートです。その他のすべてのトランスポート（`slack`、`discord`、`telegram`、`matrix`、`signal`、`sms`、`imessage`、`email`）は同じ形に従います。

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

初回起動時に、`rousseau` は QR コードを stdout に出力します。電話で **WhatsApp > 設定 > リンク済みデバイス** でスキャンしてください。whatsmeow クライアント（`internal/transport/whatsapp/client.go`）は 3 つの構造化ログイベントを発行します：

- `whatsapp.qr_ready` — QR がレンダリングされた。
- `whatsapp.paired` — 電話が QR を受け入れた。
- `whatsapp.connected` — Meta への websocket が接続されている。

デバイスの認証情報は `~/.local/share/rousseau/whatsapp.db` にキャッシュされます（別の SQLite データベースなので、デバイスを再リンクしても会話履歴には影響しません）。`--allow` フラグは E.164 JID の許可リストを固定します。それ以外の送信者は `router.transport.rejected` によって黙って破棄されます。

Rousseau は **非公式の** WhatsApp Web プロトコルを使用します。Meta は非公式クライアントを実行する番号を時折 BAN します — 依存している番号では実行しないでください。リスク分析については [Transports: WhatsApp](/ja/transports/whatsapp/) を参照してください。

## 5. サプライチェーンを検証する

タグ付きリリースごとに以下が出荷されます：

| アーティファクト | 目的 |
|---|---|
| `rousseau_<v>_checksums.txt` | リリース内の各アーカイブの SHA-256。 |
| `rousseau_<v>_checksums.txt.sig` | cosign 署名（キーレス、GitHub Actions から OIDC 発行）。 |
| `rousseau_<v>_sbom.cdx.json` | Go モジュールグラフの CycloneDX 1.5 SBOM。 |
| `rousseau_<v>_provenance.intoto.jsonl` | SLSA-3 プロヴェナンス証明。 |

チェックサムを信頼する前に、署名 ID を検証してください：

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_0.6.0_checksums.txt.sig \
  rousseau_0.6.0_checksums.txt
```

`--certificate-identity-regexp` は、署名者の ID を Sebastien の名前空間下の rousseau-agent リポジトリに固定します。**弱めないでください。** ワイルドカード ID はキーレス署名の意義を損ないます。

署名が検証されると、`sha256sum -c` はダウンロードした tarball が CI がビルドしたものと同一であることを証明します。SBOM は `cyclonedx-cli tree` で読み、SLSA-3 プロヴェナンスは `slsa-verifier verify-artifact` で検証し、その後にのみアーカイブを展開してください。

信頼境界の全体像については [セキュリティ](/ja/security/)、プラットフォームチーム向けチェックリストについては [Guides: エンタープライズオンボーディング](/ja/guides/enterprise-onboarding/) を参照してください。

## トラブルシューティング

<aside class="admonition" data-type="tip"><span class="admonition-title">最初に推奨</span><p>Issue を開く前に <code>rousseau doctor</code> を実行してください。プロバイダー認証、状態ストア、トランスポート認証情報など、あらゆるサブシステムを動作させ、構造化された pass/warn/fail 行を出力します。</p></aside>

### `go install` 後に `rousseau version` が「dev」を出力する

`version`、`commit`、`buildDate` の値は、`internal/cli/root.go` の `-ldflags` によりリリースツールチェーンでスタンプされます。`go install` はこれらのフラグをスキップするため、バイナリは `dev / none / unknown` を報告します。安定したバージョン文字列が必要な場合は、署名付きリリース経路を使用してください。`dev` 文字列は実行時には無害です。

### `claudecli: exec: "claude": executable file not found`

`provider: claudecli` は `claude` バイナリにシェルアウトします。Claude Code を `$PATH` に配置する（[Providers: claudecli](/ja/providers/claudecli/) を参照）か、プロバイダーを切り替えてください — 最速の代替は `ANTHROPIC_API_KEY` をエクスポートした `provider: anthropic` です。

### WhatsApp QR は表示されるが受理されない

一般的な 3 つの原因: (1) コンテナクロックが 30 秒以上ずれている — WhatsApp のハンドシェイクは時間に敏感です。(2) 部分的に完了したペアリングが `whatsapp.db` を再利用不能な状態のままにしている — `~/.local/share/rousseau/whatsapp.db` を削除して再スキャンしてください。(3) Meta が番号を無効化した — 新しい電話番号を試してください。[Transports: WhatsApp](/ja/transports/whatsapp/) を参照してください。

### `cosign verify-blob` が「no matching signatures」でエラーになる

`--certificate-identity-regexp` は署名者の GitHub リポジトリと一致する必要があります。rousseau-agent の場合、正しい値は `sebastienrousseau/rousseau-agent` です。ワイルドカードはキーレス署名の意義を損ないます — 弱めないでください。正規表現が正しい場合は、`cosign initialize` で Sigstore の信頼ルートを更新してください。

### すべてのツール呼び出しが「denied by pattern policy」で拒否される

`default: deny` の `pattern` モードで実行しており、一致する許可ルールがありません。ツールに対する許可エントリを追加するか、`default: allow` に切り替えて代わりに狭い拒否ルールを追加してください。詳細な例については [ユーザーガイド: 承認ポリシー](/ja/user-guide/approval-policies/) を参照してください。

## 関連ページ

- [はじめに: インストール](/ja/getting-started/installation/) — 検証レシピを備えたすべてのインストール方法。
- [はじめに: 最初のトランスポート](/ja/getting-started/first-transport/) — WhatsApp/Slack/Discord のエンドツーエンドウォークスルー。
- [設定](/ja/configuration/) — `~/.config/rousseau/config.yaml` のすべてのノブ。
- [概念](/ja/concepts/) — エージェントループ、セッションストア、MCP、cron、スキル。
- [トラブルシューティング](/ja/troubleshooting/) — 完全な障害モードカタログ。

## さらなる資料

- `README.md` — リポジトリレベルのポジショニングと機能マトリックス。
- `SECURITY.md` — 信頼境界とサプライチェーンのハードニング。
- `internal/config/config.go` — 権威ある config 構造体。
- `internal/cli/root.go` — Cobra コマンドツリーの配線。

## 次のステップ

| 行き先 | 理由 |
|---|---|
| [設定](/ja/configuration/) | `~/.config/rousseau/config.yaml` のすべてのノブとデフォルト。 |
| [概念](/ja/concepts/) | エージェントループ、セッションストア、MCP、cron、スキル。 |
| [デプロイ](/ja/deployment/) | Rootless Podman + systemd Quadlet ユニット。 |
| [セキュリティ](/ja/security/) | 信頼境界、SLSA-3 プロヴェナンス、seccomp 構成。 |
| [チュートリアル](/ja/tutorials/) | 完全なエンドツーエンドウォークスルー。 |
| [リファレンス](/ja/reference/cli-commands/) | すべての CLI フラグ、終了コード、設定フィールド。 |
