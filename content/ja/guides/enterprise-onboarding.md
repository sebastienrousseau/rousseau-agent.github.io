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
description: "A checklist for platform teams adopting rousseau-agent: SBOM, cosign, seccomp, network egress, approval policy, at-rest encryption, security SLOs."
keywords: "enterprise, checklist, sbom, cosign, seccomp, egress, encryption, slo"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/enterprise-onboarding/"
subtitle: "The platform-team checklist before rousseau ships beyond a proof-of-concept."
tags: "guides, enterprise, security, checklist, sbom, cosign"
title: "ガイド：エンタープライズ導入"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "enterprise, checklist, sbom, cosign, seccomp, egress, encryption, slo"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：エンタープライズ導入"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/enterprise-onboarding/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/enterprise-onboarding/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "ガイド：エンタープライズ導入"
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
twitter_description: "A checklist for platform teams adopting rousseau-agent: SBOM, cosign, seccomp, network egress, approval policy, at-rest encryption, security SLOs."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド：エンタープライズ導入"
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

## 対象読者

プロダクションに近づく前に rousseau-agent を評価するプラットフォームチーム。「何にサインオフする必要があるか?」という質問に答えます。すべての項目は rousseau が出荷する具体的なものと相互参照するため、サインオフは審美的ではなく客観的です。

## チェックリスト

### 1. サプライチェーン

- [ ] **SBOM。** すべてのリリースが `rousseau_<v>_sbom.cdx.json` (CycloneDX 1.5) を公開することを確認します。SCA スキャナにインポートします。アクション可能: SBOM に対して `cyclonedx-cli tree` を実行し、組織が禁止するライセンス例外を grep します。
- [ ] **SLSA-3 プロビナンス。** すべてのリリースが `rousseau_<v>_provenance.intoto.jsonl` を公開します。`slsa-verifier verify-artifact --source-uri github.com/sebastienrousseau/rousseau-agent …` で検証します。
- [ ] **cosign 信頼ルート。** 証明書 ID 正規表現を固定します: `sebastienrousseau/rousseau-agent`。ブートストラップツールにチェックサム検証レシピをキャッシュします。[クイックスタート](/ja/quickstart/) ステップ 5 を参照してください。
- [ ] **再現可能ビルド。** `make check` は `go test -race` と `govulncheck` を実行します。実行中のバージョンの定期的な脆弱性スキャンを設定します。

### 2. ランタイムハードニング

- [ ] **Rootless コンテナ。** `docker/rousseau-agent.container` は、`loginctl enable-linger` 付きの専用の非特権ユーザーの下で Quadlet ユニットを実行します。ホストが同じようにセットアップされていることを確認してください。
- [ ] **すべての capability を drop。** `DropCapability=all`。`podman inspect | jq '.[0].EffectiveCaps'` は `[]` を表示するはずです。
- [ ] **`NoNewPrivileges=true`。** 子プロセスが特権を獲得するのを防ぎます。
- [ ] **読み取り専用ルートファイルシステム。** `ReadOnly=true` + `Tmpfs=/tmp:rw,size=64m`。
- [ ] **Seccomp プロファイル。** `SeccompProfile=/usr/share/containers/seccomp.json`。ホストのベースラインに対して監査してください。
- [ ] **ユーザーネームスペースマッピング。** `UserNS=keep-id`。バインドマウントされたファイルが両側で正しく所有されることを確認します。

### 3. ネットワーク姿勢

- [ ] **インバウンドなし。** rousseau は HTTP 面がゼロです。`ss -tanp | grep rousseau` はアウトバウンド専用ソケットを表示します。
- [ ] **エグレス許可リスト。** コンテナの外側に nftables または Cloudflare Zero-Trust を重ねます。以下のみを許可します:
  - LLM プロバイダ (`api.anthropic.com`、`bedrock-runtime.<region>.amazonaws.com`、`us-east1-aiplatform.googleapis.com` など)。
  - トランスポート (`web.whatsapp.com`、`mtproto.telegram.org`、matrix ホームサーバー、Slack `wss-*`)。
- [ ] **DNS リゾルバをロックダウン。** オプションで、隣接するコンテナで許可リストの名前のみを解決する `unbound` を実行します。

### 4. 承認ポリシー

- [ ] **すべての無人デーモンに `mode: pattern`。** すべてのトランスポートサービスの設定で `agent.approver.mode: pattern` を確認します。
- [ ] **`default: deny`。** マッチしない呼び出しは通過しません。
- [ ] **`bash` 拒否リスト。** `rm\s+-rf`、`sudo`、`curl`、`wget`、`chmod`、`chown`、`nc`、`ncat`。[チュートリアル: 承認者の強化](/ja/tutorials/harden-approver-policy/) を参照してください。
- [ ] **`write` / `edit` パス固定。** 正規表現が書き込みを `/workspace/...` に制限します。
- [ ] **設定をソース管理下に。** 承認者 YAML はコードです — PR でレビューします。

### 5. シークレット処理

- [ ] **`config.yaml` に API キーなし。** シークレットは `systemd` の `EnvironmentFile=` (`chmod 0600`) または組織のシークレットマネージャに保存します。
- [ ] **`ANTHROPIC_API_KEY` は env 経由でパイプ。** `config.Load` (`internal/config/config.go`) がそれを取得します。
- [ ] **Bedrock IRSA / Vertex ADC。** 長寿命の API キーよりも ID フェデレーションを推奨します。
- [ ] **ローテーション頻度。** 90 日、またはポリシーが要求するもの。rousseau は認証情報をキャッシュしません — ローテーションされたキーは次のデーモン再起動時に取得されます。

### 6. 保存データ

- [ ] **`sessions.db` の暗号化。** フルディスク暗号化 (Linux では LUKS、macOS では FileVault、AWS では EBS 暗号化ボリューム)。rousseau はセッションストア上でアプリケーションレベルの暗号化を実装しません。
- [ ] **バックアップの暗号化。** Restic と borg のどちらも、あなたが管理するキーで保存時に暗号化します。
- [ ] **保持ポリシー。** `N` 日より古いセッションを一括削除します — SQL については [ガイド: セッション管理](/ja/guides/session-management/) を参照してください。
- [ ] **JID マップの処理。** `jid_sessions` テーブルは電話番号をセッション ID にマッピングします。PII として扱ってください。

### 7. ログと監査

- [ ] **`log.format: json`。** マシンパース可能な出力。
- [ ] **オフホストログ配送。** Vector / Promtail / Datadog。[ガイド: 可観測性](/ja/guides/observability/) を参照してください。
- [ ] **保持。** コールドストレージで最低 90 日。rousseau の監査証跡は完全に slog 内にあります。あなたがそれを永続的にします。
- [ ] **`tool.denied` アラート。** 拒否のたびにアラート — 良性かもしれないし、注入試行かもしれません。
- [ ] **`whatsapp.logged_out` アラート。** Meta ポリシーのトリップは、アカウントが動作不能であることを意味します。

### 8. 変更管理

- [ ] **設定変更はコード。** PR レビュー済み、git でバージョン管理。
- [ ] **イメージバンプは意図的。** Quadlet ユニットの `AutoUpdate=disabled` は意図的です。
- [ ] **ロールバック計画。** 以前のイメージをタグ付けして利用可能に保ちます。すべてのビルドの前に `podman tag localhost/rousseau-agent:local rousseau-agent:previous`。

### 9. インシデントレスポンス

- [ ] **オンコールローテーション。** 誰かが MTTR SLO 内に `systemctl --user stop rousseau-agent` できます。
- [ ] **侵害プレイブック。** 手順: LLM API キーの取り消し、トランスポートトークンの取り消し (例: Slack ボットの再インストール)、セッションストアのスナップショット、コンテナファイルシステムのイメージ化、WhatsApp デバイスのリンク解除。
- [ ] **セキュリティ開示チャネル。** 調整開示アドレスについては、rousseau-agent リポジトリの `SECURITY.md` を読んでください。
- [ ] **セキュリティ修正の SLO。** 固定された rousseau バージョンに対する CVE を追跡します。`make check` の `govulncheck` は既知の Go stdlib および依存関係の問題をキャッチします。

### 10. コンプライアンスマッピング

- [ ] **SOC 2 の証拠。** SLSA-3 プロビナンス + cosign + SBOM は CC7.1 (システム運用) をカバーします。承認者ログは CC7.2 をカバーします。
- [ ] **ISO 27001 A.12 運用セキュリティ。** 承認ポリシー + ワークスペーススコーピング + 監査ログ。
- [ ] **OWASP LLM Top-10。** rousseau は今日 LLM Top-10 を証明しません — これはロードマップ項目です。補償的な統制 (承認者 + コンテナ) を監査に文書化してください。

## サインオフテンプレート

以下は、プラットフォームチームがランブックにコピーできる軽量なテンプレートです:

```
Rousseau-agent deployment sign-off
=================================
Version: <tag>            (verified via cosign / SLSA verifier)
Provider: <anthropic|bedrock|vertex|openai>
Transports enabled: <list>
Approver mode: pattern
Approver default: deny
Log destination: <Loki / Datadog / etc>
Backup destination: <s3://... / restic repo>
On-call: <team>
Security disclosure: <internal address>
```

## 関連

- [セキュリティ](/ja/security/) — このチェックリストが保護する信頼境界。
- [デプロイ](/ja/deployment/) — Quadlet ユニット。
- [チュートリアル: VPS にデプロイ](/ja/tutorials/deploy-to-a-vps/) — 作業例。
- [ガイド: プロダクションデプロイ](/ja/guides/production-deployment/) — 運用の詳細。
