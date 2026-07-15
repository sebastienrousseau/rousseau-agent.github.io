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
changefreq: "weekly"
description: "rousseau-agent security posture: SLSA-3 provenance, cosign signatures, CycloneDX SBOM, dropped capabilities, seccomp, trust model, cryptography inventory, disclosure SLA."
keywords: "security, SLSA-3, cosign, sigstore, SBOM, CycloneDX, seccomp, drop capabilities, trust model, disclosure, CVSS, coordinated disclosure"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/security/"
subtitle: "Supply chain, runtime, and trust boundaries — honestly stated."
tags: "security, supply-chain, disclosure"
title: "セキュリティ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "security, SLSA-3, cosign, sigstore, SBOM, CycloneDX, seccomp, drop capabilities, trust model, disclosure, CVSS, coordinated disclosure"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "セキュリティ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "security"
order: 26
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/security/index.html"
item_link: "https://docs.rousseau-agent.dev/security/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "セキュリティ"
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
twitter_description: "rousseau-agent security posture: SLSA-3 provenance, cosign signatures, CycloneDX SBOM, dropped capabilities, seccomp, trust model, cryptography inventory, disclosure SLA."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "セキュリティ"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p>rousseau の脅威モデルを散文と ASCII 図で示し、荷重を支える境界（承認ポリシー、コンテナ分離、サプライチェーン）、リファレンス seccomp フィルタとさらに強化する方法、ネットワーク送信ポリシー、<code>slog</code> に流れる監査トレイルを扱います。正典についてはソースツリーの <code>SECURITY.md</code> と <code>docker/rousseau-agent.container</code> を相互参照してください。</p></aside>

## 脅威モデル図

```
                          ┌──────────────────────────────────┐
                          │        Chat transport user       │
                          │   (WhatsApp / Slack / Discord)   │
                          └──────────────────┬───────────────┘
                                             │ E2EE (WhatsApp)
                                             │ TLS   (Slack / Discord / …)
                        ─────────────────────┴─────────────────────
                                             │
                                             ▼
      ┌─────────────── rousseau-agent container ────────────────┐
      │                                                          │
      │   ┌─────────────┐    inbound     ┌──────────────────┐   │
      │   │  Transport  │ ───────────▶   │  Router          │   │
      │   │  adapter    │                │  + allowlist     │   │
      │   └─────────────┘                └────────┬─────────┘   │
      │                                           │             │
      │                                           ▼             │
      │                                   ┌─────────────┐       │
      │                                   │   Agent     │       │
      │                                   │  Turn loop  │       │
      │                                   └──────┬──────┘       │
      │                                          │              │
      │                            approver     │              │
      │                          ◀───────────────┤              │
      │                                          ▼              │
      │                                   ┌─────────────┐       │
      │                                   │  Registry   │       │
      │                                   │ read/edit/  │       │
      │                                   │ bash/…      │       │
      │                                   └──────┬──────┘       │
      │                                          │              │
      │  ROOTFS  ReadOnly=true  ─────────────────┤              │
      │  CAPS    DropCapability=all              │              │
      │  UID     1000, keep-id                   │              │
      │  SECCOMP default filter                  │              │
      │                                          │              │
      │            outbound TLS                  ▼              │
      └──────────────────┬───────────────────────┬──────────────┘
                         │                       │
                         ▼                       ▼
                ┌────────────────┐    ┌─────────────────────┐
                │  LLM provider  │    │  bind mounts        │
                │  (Anthropic /  │    │  ~/.local/share/    │
                │   Bedrock /    │    │    rousseau/  RW    │
                │   Vertex / …)  │    │  workspace/   RW    │
                └────────────────┘    │  ~/.claude/   RW    │
                                      └─────────────────────┘
```

コンテナのボックス内はすべて rousseau の制御下にあります。チャットトランスポートの ingress は E2EE 暗号化済み（WhatsApp）または TLS 暗号化済み（Slack、Discord、Matrix、Telegram、Email、SMS）で到達します。LLM プロバイダへの egress は TLS です。バインドマウントがデーモンからホストファイルシステムへの唯一のアクセスです。

## 信頼モデル — スコープ内

`rousseau-agent` は **ローカル、コンテナネイティブなデーモン** です。荷重を支える境界は 3 つあります。

### 1. ユーザーのシェル

組み込み `bash` ツールはユーザー権限で任意のコマンドを実行します。**これが主要なセキュリティ境界です。** すべてのツール呼び出しは実行前に提示され、設定された承認ポリシー（`allow_all`、`deny_all`、またはツールごとの正規表現 allow / deny ルールと設定可能なデフォルトを持つ `pattern` モード）の対象となります。

無人稼働（チャットトランスポート）のデーモンを運用するオペレーターは、次のいずれかを **必ず** 行わなければなりません:

- `default: deny` と明示的な allow ルールを持つ `pattern` モードを強制する。
- 暴露の理解のうえで `bypassPermissions` 姿勢を受容する。

モデル自身がモデルをゲートする、という中庸はありません。デーモンがシェルアウトでき、チャットトランスポートから到達可能であれば、原理的に到達可能なユーザーがシェルを操作できてしまいます。

### 2. コンテナ分離

リファレンスデプロイは、以下を備えたルートレス Podman コンテナです。

- `ReadOnly=true`
- `DropCapability=all`
- `NoNewPrivileges=true`
- デフォルト seccomp フィルタ（`/usr/share/containers/seccomp.json`）
- 非 root UID 1000
- `keep-id` によるユーザー名前空間マッピング
- `Network=pasta`（ルートレス、デフォルトでホストからの受信なし）

コンテナ内から見えるのはワークスペースのバインドマウント、状態ディレクトリ、`~/.claude` のみです。[/deployment/](/ja/deployment/) を参照してください。

### 3. サプライチェーン

すべてのコミットが `govulncheck` と CodeQL を実行します。すべてのリリースは以下を出荷します。

- `slsa-framework/slsa-github-generator` による **SLSA レベル 3 プロビナンス**。GitHub Actions OIDC 経由で署名されます。
- チェックサムファイルの **cosign 署名**。Sigstore の透明性ログに対して検証可能です。
- **CycloneDX JSON SBOM。**
- **再現可能ビルド証明** — 専用の CI ジョブが新規チェックアウトからのビット同一の出力を検証します。

## 信頼モデル — スコープ外

- **悪意あるモデル出力。** ツール呼び出しの承認前レビューはオペレーターの責任です。承認ポリシーはミスを起こしにくくしますが、人間の判断の必要性を排除するものではありません。
- **侵害された Go ツールチェーン、コンテナランタイム、ホスト OS。** 信頼できるビルド環境を前提とします。
- **マシンへの物理アクセス。**
- **LLM プロバイダ自身への攻撃。** プロバイダの脆弱性はそのプロバイダの責任です。

## サプライチェーンの管理策

| 管理策 | 実装 |
|---|---|
| 直接依存のピン留め | `go.mod` に正確なバージョン。推移的解決は `go.sum` で凍結。 |
| 脆弱性スキャン | すべての CI ビルドで `govulncheck ./...`。インポートされたシンボルに到達する既知脆弱性があればビルド失敗。 |
| 静的解析 | `golangci-lint` v2（18 リンター）+ GitHub CodeQL（Go）。 |
| 依存関係の更新 | `gomod` と `github-actions` に対する Dependabot、週次。 |
| ビルドプロビナンス | `slsa-framework/slsa-github-generator` による SLSA レベル 3。GitHub Actions OIDC 経由で証明され、Sigstore 透明性ログに公開。 |
| リリース署名 | リリースチェックサムは cosign で署名（GitHub Actions OIDC を用いた keyless）。 |
| ソフトウェア部品表 | すべてのリリース成果物に CycloneDX JSON SBOM を添付。 |
| 再現可能ビルド | 専用の `reproducible-build` CI ジョブがビット同一の出力を検証。 |

CI ワークフローファイルはソースツリーの `.github/workflows/` 配下にあります: `ci.yml`、`codeql.yml`、`slsa.yml`、`release.yml`、`reproducible-build.yml`。

## リリースの検証

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_<version>_checksums.txt.sig \
  rousseau_<version>_checksums.txt

sha256sum -c rousseau_<version>_checksums.txt
```

身元を固定する 2 つのフラグ:

- `--certificate-identity-regexp` は署名証明書を発行した GitHub リポジトリと一致します。これを `.*` などに広げないでください。これが別リポジトリの cosign 署名で自分のチェックサムファイルを検証されるのを防いでいます。
- `--certificate-oidc-issuer` は OIDC 発行者を GitHub Actions に固定します。

Sigstore の透明性ログエントリは https://search.sigstore.dev/ で個別に照会できます。

## 実行時の管理策

以下の設定はすべてリファレンス Quadlet ユニットで設定されており、コンテナオペレーターのベースラインに含めるべきものです。

- **非 root ユーザー（UID 1000）** — コンテナ内で root へ昇格する特権を持たない。
- **`ReadOnly=true`** — イメージは実行時に書き込み不可。バイナリは自身や依存関係を変更できません。
- **`Tmpfs=/tmp:rw,size=64m,mode=1777`** — バインドマウント外で唯一書き込み可能な場所。
- **`DropCapability=all`** — `CAP_*` ビットを一切設定しない。送信 TCP には不要です。
- **`NoNewPrivileges=true`** — setuid 昇格をブロック。
- **デフォルト seccomp フィルタ** — カーネルレベルのシステムコールゲート。
- **`Network=pasta`** — ルートレスネットワークスタック。デフォルトでホストからの受信なし。
- **公開ポートなし** — Quadlet に `PublishPort=` はありません。公開すべき受信 HTTP サーフェスは存在しません。

## 暗号インベントリ

| 用途 | 実装 |
|---|---|
| LLM / トランスポートエンドポイントへの TLS | Go 標準ライブラリの `crypto/tls` とシステムトラストストア。 |
| WhatsApp | `whatsmeow`（Signal プロトコル）。 |
| Matrix | HTTPS 上のクライアント/サーバー API。 |
| SMTP（メールトランスポート） | Go 標準ライブラリ `net/smtp` を TLS 上の `PlainAuth` と共に使用。 |
| セッションストアの静止データ | **アプリ層で暗号化していません。** 静止時暗号化が必要なオペレーターは、状態ディレクトリを暗号化ファイルシステム（LUKS、FileVault）上にマウントしてください。 |

このプロジェクトでは独自の暗号プリミティブは実装していません。

## 脆弱性開示

**sebastian.rousseau@gmail.com** まで非公開で報告してください。セキュリティ影響のある報告について、公開 issue を開かないでください。

含めるべき内容:

- 簡潔な説明と CVSS 3.1 ベクトル。
- 影響を受けるコンポーネント（ファイルパスと行範囲、または依存モジュールパス）。
- 環境詳細（`rousseau version`、Go バージョン、OS、コンテナランタイム）。
- 最小再現手順 — 理想的には失敗するテスト。

### 対応コミットメント

| イベント | SLA |
|---|---|
| 報告の受領確認 | 72 時間以内 |
| トリアージ判断（受理 / 却下 / 情報不足） | 7 日以内 |
| **Critical**（CVSS ≥ 9.0）修正の投入 | 14 日以内 |
| **High**（7.0–8.9）修正の投入 | 30 日以内 |
| **Medium / Low** 修正の投入 | 通常リリースに組み込み |
| 公開開示（協調的） | 修正リリース後 |

## サポート対象バージョン

セキュリティ修正は `main` ブランチと最新のタグ付きリリースにのみ提供されます。長期サポートブランチはありません。

## Seccomp フィルタの内訳

リファレンス Quadlet ユニットは `/usr/share/containers/seccomp.json` にある Podman のデフォルト seccomp プロファイルを使用します。これは、rousseau の正しい呼び出しには不要な約 70 のシステムコールをブロックします。例:

| システムコールファミリ | ブロック | 根拠 |
|---|---|---|
| カーネル keyring（`add_key`、`keyctl`、`request_key`） | あり | rousseau はカーネル keyring に触れません。 |
| マウント管理（`mount`、`umount`、`pivot_root`、`chroot`） | あり | 実行時の動的なマウント変更はありません。 |
| カーネルモジュール（`init_module`、`finit_module`、`delete_module`） | あり | デーモンはカーネルモジュールを読み込めません。 |
| 名前空間関連（`setns`、特定フラグ付き `unshare`） | フィルタ | 名前空間スワップによるコンテナエスケープを防止。 |
| デバッグプリミティブ（`ptrace`、`process_vm_readv`、`process_vm_writev`） | あり | Rousseau は他プロセスにアタッチしません。 |
| BPF（`bpf`） | あり | コンテナ内から eBPF プログラムは動作させません。 |
| リブート（`reboot`、`kexec_*`） | あり | コンテナがホストを再起動する正当な理由はありません。 |
| 時刻変更（`clock_settime`、`adjtimex`） | あり | 時刻はホスト管理です。 |

デフォルトプロファイルは標準ライブラリ、SQLite ドライバ（`modernc.org/sqlite`）、whatsmeow クライアント、OpenAI/Anthropic SDK に十分なシステムコールを許可します。さらに厳しくする必要がある場合（例: 他 ABI をエミュレートしないので `personality` を落とす）、デフォルトプロファイルをコピーし、システムコールを削除して、Quadlet で `SeccompProfile=/path/to/profile.json` としてコピーを参照します。

<aside class="admonition" data-type="caution"><span class="admonition-title">厳格プロファイルのテスト</span><p>seccomp を調整するたびにスモークテストでカバーが必要です。rousseau が使うと知らなかったシステムコールが、実行時に補完やトランスポートを失敗させます。本番投入前に実際のチャットのラウンドトリップでテストしてください。</p></aside>

## ネットワーク送信ポリシー

デフォルトではコンテナに ingress はなく、egress は無制限（`Network=pasta`）です。高セキュリティのデプロイでは、rousseau が必要とするドメインだけを許可する nftables ルールセットを追加します。

```
# /etc/nftables.d/rousseau.nft — example only, adjust to your provider
table inet rousseau_out {
    chain output {
        type filter hook output priority 0; policy drop;

        # LLM providers
        ip daddr { 3.5.0.0/16, 15.230.0.0/16 } tcp dport 443 accept  # Anthropic + Bedrock
        ip daddr { 34.107.0.0/16 } tcp dport 443 accept              # Vertex

        # Chat transports
        ip daddr { 157.240.0.0/16 } tcp dport 443 accept             # Meta (WhatsApp)
        ip daddr { 3.208.0.0/16 } tcp dport 443 accept               # Slack

        # DNS
        udp dport 53 accept
        tcp dport 53 accept

        # NTP
        udp dport 123 accept
    }
}
```

CIDR レンジは変動します。上記は足場として扱ってください。要点は、rousseau の送信は有限で列挙可能であるということです。ソースにある `docker/example-nftables.rules` は出発点となるルールセットです。

## slog による監査トレイル

セキュリティ関連のイベントは、すべて Go の `log/slog` を用いて構造化 JSON レベルで記録されます（`log.format: json`）。本番でテールすべきイベント:

| イベント | レベル | 出所 | 何を伝えるか |
|---|---|---|---|
| `tool.execute` | info | `internal/agent/agent.go` | どのセッションでモデルがどのツールを実行しようとしたか。 |
| `tool.denied` | warn | `internal/agent/agent.go` | approver が呼び出しを拒否した。reason 文字列を含みます。 |
| `tool.error` | warn | `internal/agent/agent.go` | ツールが実行されたがエラーを返した。 |
| `router.transport.rejected` | info | `internal/transport/router.go` | 受信メッセージが allowlist に失敗した。 |
| `whatsapp.logged_out` | error | `internal/transport/whatsapp/client.go` | Meta がペアリングを無効化した。 |
| `mcp.tool_error` | warn | `internal/mcp/server.go` | MCP ツールハンドラがエラーを返した。 |
| `cron.delivery_failed` | warn | `internal/cron/` | スケジュールされたジョブのトランスポート配信でエラーが発生した。 |

JSON ストリームを Loki / Datadog / Splunk / Vector パイプラインに流し込みます。[ガイド: 可観測性](/ja/guides/observability/) を参照してください。

<aside class="admonition" data-type="tip"><span class="admonition-title">フィールド命名</span><p>slog の属性キーはドット区切りで名前空間化されています（<code>event=whatsapp_connected</code> ではなく <code>whatsapp.connected</code>）。利用するログツールでは生のキーで照会してください。</p></aside>

## トラブルシューティング

### コンテナが `mount: permission denied` で起動を拒否する

SELinux ラベルの不整合です。バインドマウント行がすべて `:Z`（private ラベル）または `:z`（共有）で終わっているか確認してください。ラベルがないと、コンテナプロセスはホストがラベル付けしたファイルを読み書きできません。

### seccomp が必要なシステムコールを殺している

Podman はジャーナルに `syscall X blocked` を出力します。コンテナ外で `strace -f -e trace=X` を用いて再現し、その呼び出しが必要か確認してください。正当な場合は、デフォルト seccomp プロファイルをコピーし、そのシステムコールを許可リストに追加し、`SeccompProfile=` でプロファイルを参照させます。

### `cosign verify-blob` が「certificate identity does not match」を表示する

`--certificate-identity-regexp` が誤っています。`sebastienrousseau/rousseau-agent` を使用してください。より緩い正規表現（`.*`、`.+`）は keyless 署名の要点を無効化します。

### nftables 制限下でプロバイダ egress が失敗する

ルールセットがプロバイダの現在の IP レンジを含んでいません。プロバイダは CIDR をローテートします。cron で解決される ipset を用いた DNS ベースの egress を使うか、接続時に名前を解決する egress プロキシを利用してください。

### 監査イベントを期待しているのに slog に何も出ない

ログレベルが高すぎます。`log.level: info`（ワイヤレベルの詳細が欲しければ `debug`）を設定し、実際に新しいセッションが開始されていることを確認してください。設定ロード前に `slog.Default()` が使われるため、起動初期のメッセージはいずれにせよテキスト形式で stderr へルーティングされます。

## 関連ページ

- [デプロイ](/ja/deployment/) — リファレンス Quadlet ユニット。
- [ユーザーガイド: 承認ポリシー](/ja/user-guide/approval-policies/) — 主要な安全レバー。
- [ガイド: プロンプトインジェクション](/ja/guides/prompt-injection/) — モデル出力を経由した攻撃。
- [ガイド: 読み取り専用モード](/ja/guides/read-only-mode/) — 「見るだけ、触らない」デーモンの運用方法。
- [ガイド: 可観測性](/ja/guides/observability/) — slog + Loki / Datadog パイプライン。

## さらに読む

- `SECURITY.md` — 正典のポリシードキュメント。
- `docker/rousseau-agent.container` — リファレンス Quadlet ユニット。
- `docker/example-nftables.rules` — サンプル送信ルールセット。
- `internal/agent/agent.go` — `tool.execute` と `tool.denied` イベントが発せられる場所。
- `internal/agent/approver.go` — 承認ポリシーの実装。
