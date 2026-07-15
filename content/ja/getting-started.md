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
description: "Install rousseau-agent from source, go install, or a cosign-verified release. Run rousseau chat and configure the first chat transport."
keywords: "install, quickstart, rousseau chat, cosign verify, go install, systemd, podman"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/getting-started/"
subtitle: "rousseau-agent をインストールし、最初のトランスポートに到達する。"
tags: "install, quickstart, getting-started"
title: "はじめに"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "install, quickstart, rousseau chat, cosign verify, go install, systemd, podman"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "はじめに"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 2
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/getting-started/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "はじめに"
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
twitter_description: "Install rousseau-agent from source, go install, or a cosign-verified release. Run rousseau chat and configure the first chat transport."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "はじめに"
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

## 対象読者

- **個人開発者** — 自分のノートパソコン上で動作し、既存の `claude` CLI を駆動するコーディングアシスタントを求めている方。rousseau のコンフィグに API キーを組み込む必要はなく、間にクラウドブローカーも介在しません。
- **プラットフォームオペレーター** — 企業境界内でチーム共有のコーディングエージェントを運用する方。Rousseau は capability を drop したルートレスな Podman コンテナ上で動作する単一の静的 Go バイナリで、他の systemd サービスと並べてデプロイできます。
- **セキュリティレビュアー** — 導入前にエージェントを審査する方。SLSA-3 プロビナンス、cosign 署名済みのリリースチェックサム、CycloneDX SBOM、再現可能ビルド、あらゆる信頼境界は [セキュリティ](/ja/security/) にドキュメント化されています。

## 最短の道筋

1. **すでに `claude` CLI をインストールして認証済みの場合、** 最速のスタートはデフォルトの `claudecli` プロバイダを用いた `rousseau chat` です。認証は継承されるため、キーの受け渡しは不要です。以下の [初回起動](#first-run) に進んでください。
2. **自前のキーで直接 API を叩きたい場合、** `ANTHROPIC_API_KEY` を設定し、`~/.config/rousseau/config.yaml` で `provider: anthropic` に切り替えます。[Anthropic プロバイダ](/ja/providers/anthropic/) を参照してください。
3. **AWS Bedrock または Google Vertex を利用する企業環境の場合、** 該当するプロバイダを選択します。[Bedrock](/ja/providers/bedrock/) は標準の AWS 認証情報チェーンを使用し、[Vertex](/ja/providers/vertex/) はサービスアカウントの JSON を読み込みます。rousseau のコンフィグファイルにシークレットは残りません。
4. **エアギャップ環境または完全にセルフホストな推論を求める場合、** OpenAI 互換エンドポイント（Ollama、vLLM、LM Studio、その他のシム）に rousseau を向けます。[OpenAI 互換プロバイダ](/ja/providers/openai-compatible/) を参照してください。

## 最終的に得られるもの

- `$PATH` 上の `rousseau` バイナリ。cosign 署名（リリース経路）で検証済み、またはソースからビルド（`make check` は CI と同じ 18 リンター + race + govulncheck のゲートを実行）。
- 選択したプロバイダをバックエンドとする動作する `rousseau chat` TUI。
- `~/.local/share/rousseau/sessions.db` にある SQLite セッションストア — すべてのターンが永続化され、FTS5 によるセッション横断のリコールが利用可能です。
- オプションで、電話から到達可能なライブチャットトランスポート（WhatsApp、Slack、Signal など）を 1 つ。

## 動画で見たい場合は？

以下のフローの短いスクリーンキャストはロードマップにあります。それまでは、すべての手続きがこのページに収まっており、大半のオペレーターは 10 分以内に完了します。

## システム要件

| 要件 | バージョン | 備考 |
|---|---|---|
| Go ツールチェーン | 1.26+ | `CGO_ENABLED=0`。バイナリは完全静的リンクです。 |
| コンテナランタイム | Podman 4.4+ | リファレンスデプロイはルートレス Podman + systemd Quadlet ユニットを使用します。Docker も動作しますが Quadlet は Podman 固有です。 |
| `claude` CLI | latest | デフォルトの `claudecli` プロバイダを使う場合のみ。 |
| `signal-cli` | 0.13+ | Signal トランスポートを使う場合のみ。 |
| BlueBubbles server | 1.9+ | iMessage トランスポートを使う場合のみ（macOS ホストが必要）。 |
| `whisper.cpp` | 1.5+ | WhatsApp のボイスノート文字起こしを有効化する場合のみ。 |

## インストール

### ソースから

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` は vet、`golangci-lint`、`go test -race`、`govulncheck` を実行します。これは CI が強制するのと同じゲートです。

### `go install` を使用

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

バイナリには `modernc.org/sqlite` が組み込まれているため、実行時に libc や CGo の依存関係はありません。

### 署名済みリリースから

タグ付けされたすべてのリリースは、チェックサム付きアーカイブ、CycloneDX SBOM、SLSA-3 プロビナンス証明、およびチェックサムファイルの cosign 署名を公開しています。実行前に必ず検証してください。

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_<version>_checksums.txt.sig \
  rousseau_<version>_checksums.txt

sha256sum -c rousseau_<version>_checksums.txt
```

certificate-identity 正規表現は署名者の身元を固定するものです。緩めないでください。

## 初回起動

### ターミナルチャット

```sh
rousseau chat
```

Bubble Tea TUI です。Enter で送信、`Ctrl+C` で終了します。デフォルトのプロバイダは `claudecli` で、ローカルにインストールされた Claude Code から認証を継承します。rousseau のコンフィグに API キーは組み込まれません。

セッション履歴は `~/.local/share/rousseau/sessions.db`（WAL ジャーナリングとセッション横断リコール用の FTS5 を備えた SQLite）に永続化されます。

### はじめてのチャットトランスポート

WhatsApp はリファレンストランスポートです（ペアリングの UX が最も厳格なため）。初回起動時に、電話から QR をスキャンしてペアリングします。

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

E.164 JID（`<digits>@s.whatsapp.net`）は受信処理を制限します。それ以外の送信者は静かに破棄されます。ペアリング状態はセッションストアと並んで `whatsapp.db` に保存されます。

他のトランスポートも同じ形式に従います。

```sh
rousseau slack   --app-token xapp-... --bot-token xoxb-...
rousseau discord --token bot-token
rousseau telegram --token 12345:ABC
rousseau matrix  --homeserver-url https://matrix.org --access-token ... --user-id @bot:matrix.org
```

`rousseau <transport> --help` はそれぞれのフラグを一覧表示します。デフォルト値は `~/.config/rousseau/config.yaml` から取得されます。

## 状態が保存される場所

| パス | 用途 |
|---|---|
| `~/.config/rousseau/config.yaml` | ユーザーレベルのコンフィグファイル（Viper）。 |
| `~/.local/share/rousseau/sessions.db` | セッション、cron ジョブ、JID マップ、FTS5 リコールインデックス。 |
| `~/.local/share/rousseau/whatsapp.db` | Whatsmeow のデバイス認証情報（デバイスの再リンクが会話に触れないよう別ファイルに保持）。 |
| `~/.claude/` | `claude` CLI の OAuth トークン。`claudecli` プロバイダを使用する場合のみ。 |

## 次のステップ

- [コンセプト](/ja/concepts/) — エージェントループ、セッションストア、MCP、cron、スキル。
- [設定](/ja/configuration/) — すべてのノブ。
- [デプロイ](/ja/deployment/) — systemd 配下でのデーモン運用方法。
