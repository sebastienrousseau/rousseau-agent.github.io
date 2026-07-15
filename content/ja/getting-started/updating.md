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
description: "How to update rousseau-agent: go install refresh, container tag rollover, config migration between minor versions, session-store compatibility policy."
keywords: "update, upgrade, go install, container tag, config migration, minor version"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/getting-started/updating/"
subtitle: "Move between versions without losing sessions or bricking the daemon."
tags: "update, upgrade, migration"
title: "アップデート"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "update, upgrade, go install, container tag, config migration, minor version"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "アップデート"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 24
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/getting-started/updating/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/updating/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "アップデート"
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
twitter_description: "How to update rousseau-agent: go install refresh, container tag rollover, config migration between minor versions, session-store compatibility policy."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "アップデート"
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

## バージョニングポリシー

rousseau は [セマンティックバージョニング](https://semver.org) に従います:

| バンプ | 変わるもの |
|---|---|
| パッチ (`0.1.2 → 0.1.3`) | バグ修正、セキュリティ修正、依存関係バンプ。設定またはオンディスク形式の変更なし。 |
| マイナー (`0.1.x → 0.2.0`) | 新機能。設定の追加は常に非破壊です。フィールドが削除される場合、少なくとも 1 マイナーバージョンはエイリアスフォールバックがカバーします。 |
| メジャー (`0.x → 1.0`) | 破壊的変更。[変更履歴](/ja/changelog/) に文書化された移行レシピが必要です。 |

[SECURITY.md ポリシー](https://github.com/sebastienrousseau/rousseau-agent/blob/main/SECURITY.md) は明示的です: `main` と最新のタグ付きリリースのみがセキュリティ修正を受け取ります。長期サポートブランチはありません。

## インストールパス別の更新方法

### 署名付きリリースアーカイブ

```sh
VERSION=<new-tag>
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

検証はオプションではありません。すべてのリリースには新しい cosign 署名が付属します。チェックをスキップすると、サプライチェーンの姿勢が損なわれます。

### `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

正確なタグを固定するには:

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@v0.4.2
```

新しいバイナリを優先させたい場合、`$GOBIN` (通常は `~/go/bin`) は `/usr/local/bin` より前に `$PATH` にある必要があります。

### コンテナイメージ

イメージ参照のタグを更新し、systemd サービスを再起動します。リファレンス Quadlet ユニットを使用している場合:

```sh
sed -i "s#Image=ghcr.io/sebastienrousseau/rousseau-agent:.*#Image=ghcr.io/sebastienrousseau/rousseau-agent:<new-tag>#" \
  ~/.config/containers/systemd/rousseau-agent.container
systemctl --user daemon-reload
systemctl --user restart rousseau-agent.service
journalctl --user -u rousseau-agent.service -f
```

サプライチェーンを意識したデプロイでは `:latest` に固定するのは安全ではありません — 常に不変のタグ (`:v0.4.2`) に固定し、リリースノートに対してイメージダイジェストを検証してください。

### ソースから

```sh
cd rousseau-agent
git fetch --tags
git checkout <new-tag>
make check          # runs the full CI gate locally
make build
sudo install -m 0755 bin/rousseau /usr/local/bin/rousseau
```

`make check` は CI が強制するのと同じ 18 リンタ + レース + govulncheck ゲートです — ローカル実行がパスすれば、reproducible-build ジョブもパスすることが保証されます。

## 設定の移行

設定スキーマの変更は、マイナーバージョンごとに [変更履歴](/ja/changelog/) に文書化されます。Viper のデフォルトは、1 マイナーサイクルの間、古いキーが動作するように保ちます。以下のパターンが適用されます:

- **新しいキーの追加**: 以前の動作を保持するデフォルトを取得します。アクションは不要です。
- **キーのリネーム**: 古いキーは 1 マイナーの間エイリアスされます。エイリアスがヒットするとログに警告が出力されます。
- **キーの削除**: ロード時にフェイルファストエラーが発行されます。変更履歴が代替を示します。

新しいバイナリに対して設定をドライランするには:

```sh
rousseau doctor --config ~/.config/rousseau/config.yaml
```

`rousseau doctor` は、すべてのランタイム依存とすべての設定選択を巡回します。`fail` 行は、どのキーが注意を必要とするかを正確に表面化します。

## セッションストアの互換性

`~/.local/share/rousseau/sessions.db` は、バージョン管理されたスキーマで SQLite を使用します。スキーマ移行は追加的で冪等です — デーモンは起動時に `CREATE TABLE IF NOT EXISTS` と `ALTER TABLE ADD COLUMN` を実行します。新しいスキーマが実行された後は、マイナーバージョンを **決してダウングレードしないでください**。SQLite はカラムを自動的に削除しませんが、アプリケーションコードはそれらの存在を仮定します。

クリーンな状態が必要な場合:

```sh
mv ~/.local/share/rousseau/sessions.db ~/.local/share/rousseau/sessions.db.bak
```

デーモンは次回起動時にストアを再作成します。WhatsApp デバイス認証情報は `whatsapp.db` に別途保存されているため、セッションストアのリセットは再ペアリングを強制しません。

## WhatsApp ストアの互換性

`whatsapp.db` (whatsmeow のデバイスストア) はセッションストアとは別です。これは、セッションスキーマ移行が WhatsApp ペアリングをブリックできないようにするためです。whatsmeow 自体が rousseau のアップグレードでオンディスク形式を変更する場合、変更履歴がフラグを立て、リカバリパスは以下です: `whatsapp.db` を削除し、再起動し、QR を再スキャンします。

## ロールバック

- **署名付きリリースアーカイブ / `go install`**: 同じレシピを使って以前のタグを再インストールします。
- **コンテナ**: イメージタグを元に戻して再起動します。
- **ソースから**: `git checkout <old-tag> && make build`。

古いバージョンのセッションストアスキーマが、新しいバージョンが書き込んだもののスーパーセットである限り、ロールバックは安全です。実際には、単一のマイナーシリーズ内では常に真であり、隣接するマイナー間では通常真です。メジャーアップグレードは、変更履歴に明示的なロールバックの免責事項付きで移行レシピを出荷します。

## 次に

- [変更履歴](/ja/changelog/) — リリースごとの詳細。
- [トラブルシューティング](/ja/troubleshooting/) — `rousseau doctor` が `fail` 行を表面化した場合。
