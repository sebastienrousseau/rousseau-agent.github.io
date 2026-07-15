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
description: "Contribution guide for rousseau-agent: conventional commits, PR process, reviewer checklist, release cadence."
keywords: "contributing, conventional commits, pr process, reviewer checklist, release"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/developer-guide/contributing/"
subtitle: "PR process, standards, review checklist."
tags: "developer-guide, contributing"
title: "コントリビュート"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "contributing, conventional commits, pr process, reviewer checklist, release"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "コントリビュート"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 66
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/developer-guide/contributing/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/contributing/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "コントリビュート"
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
twitter_description: "Contribution guide for rousseau-agent: conventional commits, PR process, reviewer checklist, release cadence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "コントリビュート"
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

## 基本ルール

コントリビューションは招待されたコラボレーターから受け付けます。すべての PR は同じ基準で評価されます: 緑の CI、以下のコード標準、レビュアー承認。緑の CI は必要ですが十分ではありません。

権威ある情報源は、リポジトリルートの [`CONTRIBUTING.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/CONTRIBUTING.md) です。このページはドキュメントサイトの声でそれをミラーリングしたものです。

## 開発環境

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make setup      # installs golangci-lint (v2) and govulncheck
make check      # vet + lint + race-tests + govulncheck
```

CI で実行されるすべてのチェックは、Makefile を通じてローカルで利用可能です。変更が `make check` をパスすれば、CI もパスします。

## コミット標準

- **Conventional Commits** — `feat:`、`fix:`、`refactor:`、`docs:`、`test:`、`chore:`、`ci:`、`perf:`。
- 件名は 72 文字以内。本文は何ではなく **なぜ** を説明します。動機となった決定、Issue、またはインシデントを参照してください。
- 公開されたコミットを amend しないでください。新しいコミットを作成します。レビュアーは二分検索できるシリーズを好みます。
- 署名を設定している場合はコミットに署名してください。現在必須ではありませんが、リリースタグコミットには推奨されます。

## コード標準

- すべてのエクスポート識別子には、識別子名で始まる godoc コメントがあります。
- ドキュメントコメントに書面での正当化なしに、エクスポート API で `interface{}` / `any` を使用しません。
- `context.Context` はすべての I/O パスを通じて伝播します。隠れたグローバルや周囲のロガーはありません。`*slog.Logger` を明示的に渡します。
- エラーは `fmt.Errorf("...: %w", err)` で上向きにラップします。センチネルエラーはパッケージの `errors.go` に配置します。呼び出し場所では文字列マッチングよりも `errors.Is` / `errors.As` を好みます。
- `main` とテストヘルパーの外ではパニックしません。オペレーターエラー (重複登録、無効な静的スキーマ) でパニックする `Must*` バリアントは、文書化された根拠付きで許可されます。
- ライブラリコードでは `fmt.Print*` を使いません。`slog` または TUI モデルを使用します。`forbidigo` リンタがこれを強制します。

## テスト標準

- ユニットテストはコードの隣に配置します: `foo.go` → `foo_test.go`。
- テーブル駆動テストが推奨されます。停止アサーションには `require`、非停止には `assert` を使用します。
- グローバルパッチではなくインターフェースベースのテスト注入。すべてのトランスポートパッケージは、テストがフェイクで満たす狭いインターフェース (`WSConn`、`IMAPClient`、`HTTPClient`、`Sender`) を定義します。
- カバレッジ目標: 純粋なビジネスロジックパッケージは 85%、全体で 75%。
- レースセーフ: `go test -race` はパスする必要があります。新しい並行コードが自明でない同期を導入する場合、レーステストが必要です。
- すべてのパーサーに Fuzz 関数 (`parseFoo` の隣に `FuzzParseFoo`)。`make fuzz` がコーパスを実行します。

注入パターンについては [テスト](/ja/developer-guide/testing/) を参照してください。

## プルリクエストプロセス

1. PR は `main` に対して開きます。`main` があなたの下で動いた場合はリベース (マージしないでください) してください。
2. すべての PR には以下が必要です:
   - 説明の根拠 (基礎となる決定にリンクする 2〜3 文)。
   - 緑の CI: `vet`、`lint`、Linux + macOS での `test-race`、`govulncheck`、`codeql`、`reproducible-build`、カバレッジ下限。
   - レビュアー承認。
3. スカッシュマージのみ。マージコミットメッセージは最終コミットメッセージであり、1 つの原子的な変更として `main` に到達します。
4. PR が新しい依存関係を追加する場合、説明にその正当化を記します。依存関係を追加するよりも標準ライブラリを好み、新しい依存関係を追加するよりも既存の依存関係を好んでください。

## レビュアーチェックリスト

レビュアーは順番に検証します:

1. **必要性。** 変更は必要か、それとも動機となる要件なしに抽象化 / 機能面を追加しているか?
2. **スコープ。** 変更は述べられた目的の範囲内に留まっているか、それとも無関係のクリーンアップをバンドルしているか?
3. **境界の完全性。** 変更は `agent → concrete` の依存方向を尊重しているか? [アーキテクチャ](/ja/developer-guide/architecture/) を参照してください。
4. **テストカバレッジ。** 新しいコードパスはカバーされているか? エッジケースは行使されているか?
5. **エラー処理。** エラーはコンテキストでラップされているか? クリーンアップパスは正直か (黙って飲み込むのではなく `//nolint:errcheck` 正当化付きの `_ =`)?
6. **godoc + リンタがクリーン。** すべてのエクスポートシンボルが文書化され、リント出力は 0 件。
7. **セキュリティ。** 変更は `bash` ツール、承認ポリシー、トランスポート認証、またはコンテナ姿勢に触れるか? はいの場合、PR 説明はそれをフラグしているか?

## ドキュメントの貢献

ドキュメントは別のリポジトリに存在します。コード PR がユーザーに見える面 (新しいフラグ、新しいフィールド、新しいツール) に触れる場合、同じ PR — またはドキュメントリポジトリへの即座のフォローアップ PR — は影響を受けるページを更新する必要があります。

- **CLI 変更** → [ユーザーガイド: CLI](/ja/user-guide/cli/) と [リファレンス: CLI コマンド](/ja/reference/cli-commands/)。
- **設定変更** → [設定](/ja/configuration/) と [リファレンス: 設定スキーマ](/ja/reference/config-schema/)。
- **新しいツール** → [ユーザーガイド: ツール](/ja/user-guide/tools/)。
- **新しいトランスポート** → `content/transports/<name>.md`。
- **新しいプロバイダ** → `content/providers/<name>.md`。
- **動作変更** → [変更履歴](/ja/changelog/)。

## リリースプロセス

リリースは `main` からカットされます:

1. 変更履歴エントリを更新します。
2. リリースコミットに `vX.Y.Z` としてタグを付けます。
3. `release` ワークフローは GoReleaser 経由でビルドし、CycloneDX SBOM を生成し、チェックサムの cosign 署名を公開し、SLSA-3 プロビナンスを生成します。
4. コンシューマは [セキュリティ](/ja/security/) と [インストール](/ja/getting-started/installation/) のレシピに従って検証します。

rousseau は [セマンティックバージョニング](/ja/getting-started/updating/) に従います: パッチはバグを修正し、マイナーは非破壊的に機能を追加し、メジャーは破壊します — 常に移行レシピ付きで。

## ガバナンス

`rousseau-agent` はシングルメンテナプロジェクトです。決定権限は `go.mod` と `LICENSE` に記載されている記録上のメンテナに帰属します。コントリビュータは PR ディスカッションまたは `sebastian.rousseau@gmail.com` へのメールで方向変更を提案します。

## セキュリティ開示

**セキュリティレポートについて公開 Issue を開かないでください。** [セキュリティポリシー](/ja/security/) に従って `sebastian.rousseau@gmail.com` にメールしてください。72 時間以内に受領します。

## 次に

- [アーキテクチャ](/ja/developer-guide/architecture/) — 変更する前の地図。
- [テスト](/ja/developer-guide/testing/) — レビュアーが期待するパターン。
- [セキュリティ](/ja/security/) — 開示パス。
