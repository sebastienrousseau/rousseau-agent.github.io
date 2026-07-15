---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "Configure rousseau-agent as a read-only inspection agent: deny_all approver with a read/grep exception, plan-mode claudecli, read-only bind mounts."
keywords: "read-only, inspection, deny_all, plan mode, bind mount, ro mount, audit"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/guides/read-only-mode/"
subtitle: "An inspection posture that cannot mutate the workspace."
tags: "guides, read-only, deny_all, plan-mode"
title: "ガイド：読み取り専用モード"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "read-only, inspection, deny_all, plan mode, bind mount, ro mount, audit"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "ガイド：読み取り専用モード"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 36
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/guides/read-only-mode/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/read-only-mode/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "ガイド：読み取り専用モード"
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
twitter_description: "Configure rousseau-agent as a read-only inspection agent: deny_all approver with a read/grep exception, plan-mode claudecli, read-only bind mounts."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "ガイド：読み取り専用モード"
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

## シナリオ

rousseau にリポジトリを検査させ、それに関する質問に回答させ、レポートを生成させたい — しかし、書き込み、編集、または破壊的なシェルコマンドの実行はできてはいけません。これは、初回監査、インシデントレスポンスの検査、またはコンプライアンスウォークスルーのためにデプロイする姿勢です。

これを困難にするために 3 つの層が積み重なります:

1. **承認ポリシー** — 変更するすべてのツールを拒否します。
2. **`claudecli` パーミッションモード** — Claude Code を `plan` モードにして、その独自の承認者がファイルを編集しないようにします。
3. **ファイルシステム** — ワークスペースを読み取り専用でバインドマウントします。

ベルト、サスペンダー、そしてもう 1 本のベルト。3 つのうちどれか 1 つでも安全にフェイルします。

## 層 1 — 承認者

最も単純な読み取り専用姿勢は、ホワイトリスト付きの `pattern` 承認者を使用します:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "read-only inspection posture — this deployment cannot mutate files"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|find|wc|stat|file|which|pwd|env|git status|git diff|git log|git show|git branch)\\b"}
    # No deny rules needed — default: deny catches everything else.
    # No edit, write, or unrestricted bash — the model can't reach them.
```

さらに厳格なバリアントは `deny_all` を使用し、`read` や `grep` を含むすべてのツールをブロックします:

```yaml
agent:
  approver:
    mode: deny_all
    reason: "smoke test — no tool calls allowed"
```

`deny_all` はスモークテストとしてのみ有用です。モデルは意味のある作業ができません。

## 層 2 — `claudecli` パーミッションモード

プロバイダーが `claudecli` の場合、Claude Code 自体がツール呼び出しを実行します。`permission_mode: plan` を設定すると、rousseau の承認者が許可したはずでも、Claude Code が独自の層で書き込みまたは編集側のすべての呼び出しを拒否します:

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: plan
```

有効な値 (`internal/config/config.go` と Claude Code のドキュメントを参照): `acceptEdits`、`auto`、`bypassPermissions`、`default`、`dontAsk`、`plan`。`plan` は Claude Code を一貫して読み取り専用姿勢に保つ唯一の値です。

## 層 3 — ファイルシステム

ワークスペースを読み取り専用でマウントします。参照 Podman Quadlet の下では:

```
Volume=%h/team-rousseau-workspace:/workspace:ro,Z
```

`ro` はコンテナの視点からマウントを読み取り専用にします。侵害されたバイナリが `O_WRONLY` で `open(2)` しようとしても、カーネルは `EROFS` を返します。

Kubernetes の下では:

```yaml
volumeMounts:
  - name: workspace
    mountPath: /workspace
    readOnly: true
```

セッションストア (`~/.local/share/rousseau/`) は書き込み可能である必要があります — デーモンはターンごとにそこに追記します。そのマウントは `rw` のままにし、ワークスペースのみを読み取り専用にしてください。

## ドライラン姿勢

デーモンには `--dry-run` フラグはありません。モデルに変更を実行せずに *計画* させたい場合、上記の組み合わせで同等のことが達成できます:

- 承認者が変更するすべてのツールをブロック → モデルはブロックを説明する `tool_result` エラーを受け取ります。
- `claudecli` の `plan` モードが Claude Code に独自の破壊的ツールを実行させません。
- 読み取り専用マウントが漏れたものを止めます。

モデルは通常、diff ではなく計画ドキュメントで応答します。それが読み取り専用検査の成果物です。

## それでも動作するもの

- すべての `read` および `grep` 呼び出し。
- あなたが列挙した安全な読み取り側ユーティリティのための `bash`。
- セッション永続化 — SQLite ストアは引き続き会話を記録します。
- FTS5、MCP エクスポート、スキル経由のクロスセッション再呼び出し — いずれも読み取り専用です。

## (意図的に) 壊れるもの

- `write` と `edit` — 拒否。
- シェルの変更コマンド — 拒否。
- プロンプトがファイル書き込みを暗示する cron ジョブ — モデルが試み、拒否され、計画で応答します。
- `rousseau init` — CLI は承認者の影響を受けませんが、ワークスペースの外の `~/.config/rousseau/` に書き込みます。読み取り専用モードを展開する前に実行してください。

## 姿勢のテスト

```sh
rousseau chat
> Edit /workspace/README.md to add a footer.
```

期待されるログ行:

```
WARN tool.denied name=edit reason="read-only inspection posture — this deployment cannot mutate files"
```

期待されるチャット返信: モデルは謝罪し、テキストとして計画または diff パッチを生成し、オペレーターに適用を求めます。

`deny_all` バリアントでは、すべてのツール呼び出しがブロックされます — モデルは何も検査する手段がないため、この姿勢はスモークテストとしてのみ有用です。

## 他のトランスポートとのレイヤリング

同じ 3 層が WhatsApp、Slack、Discord、およびその他のすべてのトランスポートに適用されます。承認者はエージェントループ内で実行されるため、どのトランスポートがユーザーターンを配送したかは気にしません。読み取り専用の Slack エージェントは 1 つの `mode: pattern` ブロックの距離です。

## 注意事項

- 読み取り専用姿勢は rousseau の承認者とファイルシステムによって強制されます — LLM によってでは **ありません**。モデルは依然として `edit` ツール呼び出しを発することができます。承認者はそれをサイレントにブロックしますが、試行は `tool.denied` としてログに記録されます。これは監査証跡がモデルが試みたことを記録するようにするための意図的なもので、成功したものだけではありません。
- 読み取り専用のバインドマウントは、マウントの外を指すシンボリックリンクからは保護しません。参照 Podman 姿勢はすべての capability を drop するため、ほとんどの脱出パスを防止しますが、マウントだけに頼らないでください。
- `claudecli` プロバイダーの `plan` モードは Claude Code のコントラクトであり、rousseau のものではありません。Claude Code がその permission-mode セマンティクスを変更すると、rousseau の読み取り専用姿勢もその変更を継承します。

## 次に

- [ユーザーガイド: 承認ポリシー](/ja/user-guide/approval-policies/) — より深いリファレンス。
- [監査 + 承認ポリシー](/ja/guides/audit-approval-policies/) — 変更対応版。
- [デプロイ](/ja/deployment/) — マウントとコンテナのフラグ。
