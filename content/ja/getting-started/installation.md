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
description: "Install rousseau-agent on macOS, Linux, or Windows. From-source build, go install, cosign-verified release archive, Podman / Docker image, checksum verification recipe."
keywords: "install, macos, linux, windows, homebrew, cosign, sha256, podman, docker, go install"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/getting-started/installation/"
subtitle: "Every supported install method with the verification recipe."
tags: "install, macos, linux, windows, cosign, docker"
title: "インストール"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "install, macos, linux, windows, homebrew, cosign, sha256, podman, docker, go install"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "インストール"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 21
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/getting-started/installation/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/installation/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "インストール"
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
twitter_description: "Install rousseau-agent on macOS, Linux, or Windows. From-source build, go install, cosign-verified release archive, Podman / Docker image, checksum verification recipe."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "インストール"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">このページで学べること</span><p>rousseau のサポートされたインストール方法すべて、OS 別コマンド、cosign / SHA-256 / SLSA-3 の検証手順、初回インストールでつまずきがちな失敗モードを扱います。以下の表を眺めて方法を選び、お使いの OS へ飛んでください。</p></aside>

## インストール方法の選択

| 方法 | 使用場面 | 検証可能 |
|---|---|---|
| 署名済みリリースアーカイブ | 本番、エアギャップ、規制環境全般。 | Yes — cosign + SHA-256 チェックサム + SLSA-3 プロビナンス。 |
| `go install` | Go モジュールプロキシのチェックサムデータベースを信頼する個人開発者。 | 部分的 — `pkg.go.dev` 経由の `go.sum` ピン留め。 |
| ソースから（`make build`） | 完全な CI ゲートをローカルで実行したいコントリビュータやレビュアー。 | Yes — CI の reproducible-build ジョブがビット同一の出力を確認します。 |
| コンテナイメージ | 他の systemd サービスと並べるデプロイや Kubernetes。 | Yes — イメージはタグ付けされたソースからビルドされ、プロビナンスが添付されます。 |
| Homebrew（予定） | macOS の利便性向上。 | 予定。未リリース。 |

<aside class="admonition" data-type="caution"><span class="admonition-title">検証スキップは危険</span><p>署名済みリリースの経路は、ソースコミットから GitHub Actions OIDC を経てディスク上のアーカイブまでの連鎖を得られる唯一の方法です。インターネットから拾った適当なバイナリを実行しないのであれば、<code>cosign verify-blob</code> + <code>sha256sum -c</code> をスキップしないでください。両コマンドは以下で OS 別に示します。</p></aside>

## OS 別インストール

<div class="tabs" data-tabs="install-os">
  <div class="tab-list" role="tablist" aria-label="Operating system">
    <button role="tab" aria-selected="true">macOS</button>
    <button role="tab" aria-selected="false">Linux</button>
    <button role="tab" aria-selected="false">Windows</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**署名済みリリース（推奨）。** Apple Silicon と Intel で動作します。Intel Mac では `arm64` を `amd64` に置き換えてください。

```sh
VERSION=<pin-a-tag>
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_darwin_arm64.tar.gz"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt.sig"

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature "rousseau_${VERSION}_checksums.txt.sig" \
  "rousseau_${VERSION}_checksums.txt"

shasum -a 256 -c "rousseau_${VERSION}_checksums.txt" --ignore-missing
tar -xzf "rousseau_${VERSION}_darwin_arm64.tar.gz"
sudo install -m 0755 rousseau /usr/local/bin/rousseau
rousseau version
```

**`go install`。** Go 1.26+ が既にあるなら最速です。

```sh
brew install go@1.26        # または https://go.dev/dl から
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

バイナリには `modernc.org/sqlite` が組み込まれているため（`internal/state/sqlite/store.go` を参照）、libc や CGo の依存関係はなく、Xcode Command Line Tools も不要です。

**Homebrew。** Homebrew formula はロードマップにあります。リリースまでは上記のリリースアーカイブ経路を使ってください。

<aside class="admonition" data-type="note"><span class="admonition-title">Gatekeeper</span><p>署名済みアーカイブは Apple の公証（notarisation）サービスの署名を持ちません（rousseau は Apple Developer ID を持ちません）。初回起動時に Gatekeeper のダイアログが出ることがあります。<em>システム設定 &gt; プライバシーとセキュリティ</em> で承認してください。cosign 署名の検証は同等のサプライチェーン検査です。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**署名済みリリース（推奨）。** `aarch64` ビルドは `linux_arm64` 配下で公開されます。

```sh
VERSION=<pin-a-tag>
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_linux_amd64.tar.gz"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt.sig"

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature "rousseau_${VERSION}_checksums.txt.sig" \
  "rousseau_${VERSION}_checksums.txt"

sha256sum -c "rousseau_${VERSION}_checksums.txt" --ignore-missing
tar -xzf "rousseau_${VERSION}_linux_amd64.tar.gz"
sudo install -m 0755 rousseau /usr/local/bin/rousseau
rousseau version
```

**ディストロパッケージ。** 一次配布のパッケージはまだありません。上記のリリースアーカイブを追跡してください。

**ルートレス Podman（本番）。** Quadlet リファレンスは [デプロイ](/ja/deployment/) を参照してください。`pasta` ネットワーキングには Podman 5.x+ が必要です。Debian 12 と Ubuntu 22.04 は 4.x を出荷しており、`slirp4netns` フォールバックが必要です（ロードマップ）。

<aside class="admonition" data-type="warning"><span class="admonition-title">ディストリビューションの Go</span><p>Debian/Ubuntu は 1.26 より古い Go を出荷することがよくあります。<code>go version</code> が &lt; 1.26 と表示される場合は、<a href="https://go.dev/dl">go.dev/dl</a> から直接インストールするか、署名済みリリースアーカイブを使ってください。古いツールチェーンに対する <code>go install</code> は、rousseau が使うモジュール機能で失敗します。</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau は Windows を第一級のビルドターゲットとしてサポートします。`signal`（`signal-cli` JVM サブプロセスが必要）と `imessage`（macOS が必要）を除き、すべてのトランスポートが Windows で動作します。リファレンスの Podman + Quadlet デプロイは Linux 専用です。コンテナ経路は WSL 2 や Linux VM を使ってください。

**署名済みリリース。** PowerShell:

```powershell
$Version = "<pin-a-tag>"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_windows_amd64.zip" -OutFile "rousseau.zip"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_checksums.txt" -OutFile "checksums.txt"
Get-FileHash rousseau.zip -Algorithm SHA256
Expand-Archive rousseau.zip -DestinationPath .
```

`Get-FileHash` の出力を `checksums.txt` と目視で比較するか、PowerShell をパイプしてチェックをスクリプト化してください。

**`go install`。** Go が PATH に入っていれば Windows でもそのまま動作します。

```powershell
winget install GoLang.Go
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

<aside class="admonition" data-type="warning"><span class="admonition-title">Windows での cosign</span><p><code>cosign</code> CLI は Windows でも動作しますが、ダウンロードサイズが大きく独自の依存チェーンを必要とします。摩擦の少ない検証には、同じチェックサムファイルに対し WSL 2 や Linux VM から一度 <code>cosign verify-blob</code> を実行し、Windows 上では SHA-256 の手順を信頼してください。</p></aside>

<aside class="admonition" data-type="warning"><span class="admonition-title">ホームディレクトリのパス</span><p>Rousseau は Windows では状態を <code>%APPDATA%\rousseau\sessions.db</code> に書き込みます（<code>internal/config/config.go</code> の <code>os.UserConfigDir()</code> 経由）。ドキュメントでは Unix パス <code>~/.local/share/rousseau/</code> を挙げることがありますが、同じファイルがプラットフォームに適した場所に置かれるということです。</p></aside>

  </div>
</div>

## 署名済みリリースの検証

`cosign verify-blob` コマンドは、Sigstore の公開透明性ログに対して 3 つのチェックを同時に行います。

1. 署名に埋め込まれた証明書が、正規表現に一致する GitHub Actions OIDC 身元に発行されている。
2. チェックサムファイルに対する署名が有効である。
3. 証明書が透明性ログにより witness されている。

続く `sha256sum -c` は、チェックサムファイル内のすべての成果物が一致することを確認します。これが荷重を支えるサプライチェーンチェックです。スキップしないでください。

### SBOM の検証

すべてのリリースには `rousseau_<version>_sbom.cdx.json`（CycloneDX 1.5）が同梱されています。`cyclonedx-cli` で確認します。

```sh
cyclonedx-cli tree --input-file rousseau_<version>_sbom.cdx.json
cyclonedx-cli validate --input-file rousseau_<version>_sbom.cdx.json
```

### SLSA-3 プロビナンスの検証

```sh
slsa-verifier verify-artifact \
  --provenance-path rousseau_<version>_provenance.intoto.jsonl \
  --source-uri github.com/sebastienrousseau/rousseau-agent \
  --source-tag <version> \
  rousseau_<version>_linux_amd64.tar.gz
```

成果物と CI がビルドしたと証明する内容の間に食い違いがあれば、`slsa-verifier` はゼロ以外で終了します。

## macOS

### 署名済みリリース（推奨）

```sh
VERSION=<pin-a-tag>
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_darwin_arm64.tar.gz"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt.sig"

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature "rousseau_${VERSION}_checksums.txt.sig" \
  "rousseau_${VERSION}_checksums.txt"

shasum -a 256 -c "rousseau_${VERSION}_checksums.txt" --ignore-missing
tar -xzf "rousseau_${VERSION}_darwin_arm64.tar.gz"
sudo install -m 0755 rousseau /usr/local/bin/rousseau
rousseau version
```

Intel Mac では `arm64` を `amd64` に置き換えてください。

### Homebrew（予定）

Homebrew formula はロードマップにあります。リリースまでは上記のリリースアーカイブ経路が macOS の推奨インストール方法です。

## Linux

### 署名済みリリース（推奨）

```sh
VERSION=<pin-a-tag>
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_linux_amd64.tar.gz"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt.sig"

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature "rousseau_${VERSION}_checksums.txt.sig" \
  "rousseau_${VERSION}_checksums.txt"

sha256sum -c "rousseau_${VERSION}_checksums.txt" --ignore-missing
tar -xzf "rousseau_${VERSION}_linux_amd64.tar.gz"
sudo install -m 0755 rousseau /usr/local/bin/rousseau
rousseau version
```

`aarch64` ビルドは `linux_arm64` 配下で公開されます。

certificate-identity 正規表現は署名者の身元を固定します。緩めないでください。別の身元で署名されたリリースアーカイブは即座に拒否すべきです。

### `go install` で

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

バイナリは完全静的リンク（`CGO_ENABLED=0`）で `modernc.org/sqlite` を組み込んでいるため、libc や CGo のランタイム依存関係は入りません。`go.sum` のピン留めは Go モジュールプロキシのチェックサムデータベースが強制します。

## Windows

Windows バイナリは同じリリースアーカイブレイアウトで公開されます。

```powershell
$Version = "<pin-a-tag>"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_windows_amd64.zip" -OutFile "rousseau.zip"
Invoke-WebRequest -Uri "https://github.com/sebastienrousseau/rousseau-agent/releases/download/$Version/rousseau_${Version}_checksums.txt" -OutFile "checksums.txt"

# Verify SHA-256 (cosign verification is Linux/macOS-friendly; on Windows,
# checksum verification alone is usable but weaker than the full recipe).
Get-FileHash rousseau.zip -Algorithm SHA256
Expand-Archive rousseau.zip -DestinationPath .
```

Windows は第一級のビルドターゲットですが、テストは十分ではありません。すべてのチャットトランスポートは動作しますが、リファレンスデプロイ（Podman + Quadlet）は Linux を前提とします。Windows 固有の問題は CI で捕捉できるよう報告してください。

## ソースから

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # ./bin/rousseau を生成
./bin/rousseau version
```

`make check` は CI と同じゲートを実行します: `go vet`、`golangci-lint` v2（18 リンター）、`go test -race -count=1 -covermode=atomic ./...`、`govulncheck`。

専用の `reproducible-build` CI ジョブは `ubuntu-latest` 上の新規チェックアウトからビット同一の出力を検証します。したがって、同じ Go ツールチェーンでのローカル `make build` は、SHA-256 がタグ付けされたリリースと一致するバイナリを生成します。

## Podman / Docker

```sh
# タグ付けされたソースからローカルビルド。
podman build -t rousseau-agent:local -f docker/Dockerfile .

# 事前ビルドされたイメージを pull（公開後）。
podman pull ghcr.io/sebastienrousseau/rousseau-agent:<tag>
```

Docker も同じ動作です。`podman` を `docker` に置き換えてください。リファレンスデプロイ（[デプロイ](/ja/deployment/)）は **ルートレス Podman** に systemd Quadlet ユニットを使用します。Quadlet が素の Docker にはない宣言的な堅牢化（`ReadOnly=true`、`DropCapability=all`、`NoNewPrivileges=true`、seccomp フィルタ、`keep-id` によるユーザー名前空間マッピング）を提供するためです。

実行時イメージは約 550 MB で、マルチステージの `golang:1.26-alpine` ビルダーが `node:22-alpine` ランタイムに供給する形式で構築されます。Node レイヤーはオプションの `claude` CLI サブプロセスのために存在するのみで、デーモン自体にインタプリタの依存関係はありません。

## 署名済みリリースの検証

`cosign verify-blob` コマンドは Sigstore の公開透明性ログに対して 3 つのチェックを同時に行います。

1. 署名に埋め込まれた証明書が、正規表現に一致する GitHub Actions OIDC 身元に発行されている。
2. チェックサムファイルへの署名が有効である。
3. 証明書が透明性ログにより witness されている。

続く `sha256sum -c` はチェックサムファイル内のすべての成果物が一致することを確認します。これが荷重を支えるサプライチェーンチェックです。スキップしないでください。

## トラブルシューティング

### `go: module github.com/sebastienrousseau/rousseau-agent/cmd/rousseau: no matching versions`

`go` ツールチェーンが 1.26 より古いです。`go install` はツールチェーンバージョンより上の `go` ディレクティブを持つモジュールを拒否します。Go をアップグレードするか、署名済みリリースアーカイブを使ってください。

### `sha256sum: WARNING: X computed checksums did NOT match`

アーカイブがダウンロード中に破損したか、（悪ければ）改ざんされています。再ダウンロードし、手順を最初からやり直してください。改ざんは `cosign verify-blob` が検知しているはずですが、SHA-256 の結果はどんな前提よりも信頼してください。

### `cosign: no matching signatures`

`cosign` はあるが `--certificate-identity-regexp` が署名者と一致していません。rousseau では `sebastienrousseau/rousseau-agent` を使用してください。それでも失敗する場合は `cosign initialize` を実行して Sigstore の trust root をリフレッシュしてください。trust root はゆっくりとローテートされます。

### `rousseau version` が `dev / none / unknown` を表示する

`go install` でインストールしたため、`internal/cli/root.go` の `-ldflags` バージョンスタンプが埋め込まれていません。表示上の問題だけですが、署名済みリリースアーカイブが解決策です。

### macOS Gatekeeper がバイナリを開かない

Finder でバイナリを右クリックし <em>開く</em> を選び、ダイアログでもう一度 <em>開く</em> をクリックします。代替として `xattr -d com.apple.quarantine ./rousseau` で quarantine ビットを外せます。署名済みリリースは公証されていません。cosign 検証が同等のサプライチェーン検査になります。

## 関連ページ

- [はじめに: プラットフォームサポート](/ja/getting-started/platform-support/) — OS、アーキテクチャ、プロバイダ認証マトリクス。
- [はじめに: はじめてのトランスポート](/ja/getting-started/first-transport/) — WhatsApp をエンドツーエンドで配線。
- [はじめに: 更新](/ja/getting-started/updating/) — バージョン間の安全な移行方法。
- [デプロイ](/ja/deployment/) — ルートレス Podman + Quadlet のリファレンスデプロイ。
- [セキュリティ](/ja/security/) — 信頼境界とサプライチェーン堅牢化。

## さらに読む

- `README.md` — リポジトリレベルの立ち位置と機能マトリクス。
- `SECURITY.md` — 脆弱性開示とサプライチェーン管理策。
- `Makefile` — `make check` でローカル再現される正確な CI ゲート。
- `docker/Dockerfile` — マルチステージビルド（`golang:1.26-alpine` &rarr; `node:22-alpine`）。
