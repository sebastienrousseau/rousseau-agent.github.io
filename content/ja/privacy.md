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
description: "rousseau-agent is self-hosted. No telemetry endpoint, no SaaS control plane. LLM providers have their own retention policies; everything else stays in the operator's infrastructure."
keywords: "privacy, telemetry, self-hosted, data handling, retention, LLM providers"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/privacy/"
subtitle: "セルフホストとは自己制御の意 — LLM 呼び出し以外は基盤の外に出ません。"
tags: "privacy, legal, self-hosted"
title: "プライバシー"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "privacy, telemetry, self-hosted, data handling, retention, LLM providers"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "プライバシー"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "legal"
order: 30
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/privacy/index.html"
item_link: "https://docs.rousseau-agent.dev/privacy/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "プライバシー"
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
twitter_description: "rousseau-agent is self-hosted. No telemetry endpoint, no SaaS control plane. LLM providers have their own retention policies; everything else stays in the operator's infrastructure."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "プライバシー"
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

## データの取り扱い

`rousseau-agent` はセルフホストです。オペレーターが自身のインフラ上でデーモンを実行するとき、**LLM 呼び出し自体を除いて、そのインフラからデータが出ることはありません**。

以下のものは存在しません:

- **テレメトリエンドポイントなし。** rousseau は実行時に `rousseau-agent.dev` や、作者が管理するその他のサーバーへ一切の呼び出しを行いません。
- **SaaS コントロールプレーンなし。** ライセンスサーバー、クラウドダッシュボード、フォンホームはありません。
- **利用分析なし。** どのツールが呼ばれたか、何ターン実行されたか、どのモデルが呼ばれたかを、デーモンは報告しません。
- **クラッシュレポートなし。** クラッシュはローカルログ (`journalctl --user -u rousseau-agent.service`) に現れます。スタックトレースはどこにも送信されません。

## セッションデータの保管場所

| データ | 場所 | 保存時の暗号化 |
|---|---|---|
| セッション (メッセージ履歴) | `~/.local/share/rousseau/sessions.db` | ファイルシステムレベルのみ (オペレーターが設定していれば LUKS / FileVault)。 |
| Cron ジョブ | 同じ SQLite データベース | 同じ。 |
| WhatsApp デバイスペアリング | `~/.local/share/rousseau/whatsapp.db` | 同じ。 |
| ログ出力 | systemd journal (通常は `~/.local/state/`) | 同じ。 |
| 設定ファイル | `~/.config/rousseau/config.yaml` | 同じ。 |
| `claude` CLI の OAuth トークン | `~/.claude/` | 同じ。 |

これらはいずれもデーモンによってどこにも送信されません。

## LLM プロバイダ

LLM プロバイダは唯一の外部接点です。各プロバイダはそれぞれ独自のデータ取り扱いと保持ポリシーを持ちます — いずれも rousseau が制御するものではありません:

| プロバイダ | 保持ポリシー |
|---|---|
| [claudecli](/ja/providers/claudecli/) | ローカルの `claude` CLI が送信するよう設定されているもの。通常は Anthropic の標準保持ポリシー。 |
| [Anthropic 直接](/ja/providers/anthropic/) | https://www.anthropic.com/legal/aup を参照。 |
| [AWS Bedrock](/ja/providers/bedrock/) | 契約で定義される。Bedrock の推論トラフィックについては通常長期保持なし。 |
| [Google Vertex AI](/ja/providers/vertex/) | 契約で定義される。Vertex の推論については通常長期保持なし。 |
| [OpenAI 互換](/ja/providers/openai-compatible/) | エンドポイントに依存。Ollama とセルフホスト vLLM は外部に何も保持しません。OpenAI と OpenRouter はそれぞれ独自のポリシーを持ちます。 |

運用要件に合致する保持ポリシーを持つプロバイダを選択してください。最も厳格な姿勢を求めるなら、セルフホストの Ollama、vLLM、または LM Studio に対して実行してください — データはあなたのインフラから出ません。

## トランスポート側のデータ

チャットトランスポートは、ベンダーのサーバー (WhatsApp、Signal、Slack、Discord など) を通じてメッセージを送信します。各ベンダーはそれぞれ独自のデータ取り扱い姿勢を持ちます。rousseau はそれらの上に層を追加しません — ベンダーは基盤となるプロトコルが見せるものを見ます。それはプロトコル固有です:

- Signal と WhatsApp: エンドツーエンド暗号化。ベンダーはメタデータを見ますが、メッセージ内容は見ません。
- Slack、Discord: エンドツーエンド暗号化ではありません。ベンダーはメッセージ内容を見ます。
- Matrix: ルームが E2E 有効な場合はエンドツーエンド暗号化。それ以外はサーバーサイド。
- Email: PGP や S/MIME を上に重ねない限りエンドツーエンド暗号化ではありません (rousseau は行いません)。
- iMessage: エンドツーエンド暗号化。BlueBubbles が rousseau と Apple の間に位置します。

## セッションの削除

セッションは SQLite データベースの行です。以下で削除します:

```sh
rousseau session delete <session-id>
```

または、データベース全体を削除します:

```sh
rm ~/.local/share/rousseau/sessions.db
```

次回起動時に空のデータベースが再作成されます。これは FTS5 のクロスセッションリコールインデックスもパージします。

## サードパーティ依存関係

`go.mod` にすべての依存関係が列挙されています。フォンホームするよう設定されているものはありません。ビルド時依存関係 (リンタ、静的解析器) は CI でのみ実行されます。ランタイム依存関係は各リリースに添付される CycloneDX SBOM に列挙されています。
