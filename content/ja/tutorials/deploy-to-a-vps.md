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
description: "Walk a fresh VPS from bare install to a hardened rousseau-agent daemon under rootless Podman and a systemd Quadlet unit."
keywords: "vps, podman, quadlet, systemd, rootless, deployment, hardening"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/tutorials/deploy-to-a-vps/"
subtitle: "Build a container, provision a VPS, install the Quadlet unit, verify the service."
tags: "tutorials, deployment, podman, quadlet, systemd, vps"
title: "チュートリアル：VPS にデプロイする"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "vps, podman, quadlet, systemd, rootless, deployment, hardening"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "チュートリアル：VPS にデプロイする"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/tutorials/deploy-to-a-vps/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/deploy-to-a-vps/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "チュートリアル：VPS にデプロイする"
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
twitter_description: "Walk a fresh VPS from bare install to a hardened rousseau-agent daemon under rootless Podman and a systemd Quadlet unit."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "チュートリアル：VPS にデプロイする"
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

## 構築するもの

`docker/rousseau-agent.container` の systemd Quadlet ユニットで駆動される、rootless Podman コンテナ下で rousseau-agent の WhatsApp デーモンを実行する新規 Ubuntu 24.04 VPS。読み取り専用ルートファイルシステム、すべての capability を drop、`NoNewPrivileges=true`、seccomp オン。インバウンドネットワークポートはゼロ。

想定時間: 45 分。

## 前提条件

- Ubuntu 24.04 (または Debian 12+ / Fedora 40+) の VPS。1 GB RAM、20 GB ディスクで十分です。
- sudo 権限を持つ非 root ユーザーへの SSH キーアクセス。
- Anthropic API キー、または `claudecli` を実行する意志 — `claudecli` はアクティブな OAuth セッションを持つ `claude` が VPS にインストールされている必要があり、これはヘッドレスサーバーでは扱いにくいです。Anthropic 直接または Bedrock が実用的な選択肢です。

## ステップ 1: ベース OS のセットアップ

```sh
ssh admin@vps
sudo apt update && sudo apt -y upgrade
sudo apt -y install podman uidmap fuse-overlayfs slirp4netns curl git

# rootless podman needs subuid/subgid ranges for the user
grep rousseau /etc/subuid || sudo usermod --add-subuids 200000-265535 rousseau
grep rousseau /etc/subgid || sudo usermod --add-subgids 200000-265535 rousseau
```

サービスユーザーとその systemd ユーザーセッションを作成:

```sh
sudo useradd -m -s /bin/bash rousseau
sudo loginctl enable-linger rousseau     # keeps user services running when nobody is logged in
```

## ステップ 2: ソースを転送する

`docker/rousseau-agent.container` の Quadlet ユニットはローカルイメージをビルドします。VPS 上で:

```sh
sudo -iu rousseau
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
podman build -t rousseau-agent:local -f docker/Dockerfile .
podman image inspect localhost/rousseau-agent:local | head
```

`Dockerfile` は静的 Go バイナリ (`CGO_ENABLED=0`) を生成し、最小ベースにコピーし、UID 1000 として実行します。ベースイメージの議論については [デプロイ](/ja/deployment/) を参照してください。

## ステップ 3: 設定をシードする

rousseau は `~/.config/rousseau/config.yaml` を読み込みます。ホスト上に作成してください — Quadlet ユニットはコンテナの `$HOME` をホストにバインドマウントで戻します。

```sh
mkdir -p /home/rousseau/.config/rousseau
cat > /home/rousseau/.config/rousseau/config.yaml <<'YAML'
provider: anthropic

anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096

whatsapp:
  reply_header: "*rousseau*\n\n"

agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

log:
  level: info
  format: json
YAML
chown -R rousseau:rousseau /home/rousseau/.config
```

Anthropic API キーは systemd 環境ファイルに格納してください — 決して `config.yaml` には入れないでください:

```sh
mkdir -p /home/rousseau/.config/rousseau
cat > /home/rousseau/.config/rousseau/env <<'ENV'
ANTHROPIC_API_KEY=sk-ant-…
ENV
chmod 0600 /home/rousseau/.config/rousseau/env
```

Quadlet ユニットからそれを参照します — 次のステップを参照してください。

## ステップ 4: Quadlet ユニットをインストールする

```sh
mkdir -p /home/rousseau/.config/containers/systemd
cp docker/rousseau-agent.container /home/rousseau/.config/containers/systemd/
```

JID とシークレットファイル用に編集:

```sh
sed -i 's|Exec=whatsapp --allow.*|Exec=whatsapp --allow YOUR_JID@s.whatsapp.net|' \
  /home/rousseau/.config/containers/systemd/rousseau-agent.container

cat >> /home/rousseau/.config/containers/systemd/rousseau-agent.container <<'EOF'
EnvironmentFile=%h/.config/rousseau/env
EOF
```

リロードして起動:

```sh
systemctl --user daemon-reload
systemctl --user enable --now rousseau-agent
systemctl --user status rousseau-agent
```

## ステップ 5: 初回ペアリング

WhatsApp ブリッジは初回に QR コードを印刷する必要があります。アタッチ:

```sh
podman logs -f rousseau-agent
# scan the QR from your phone: WhatsApp > Settings > Linked devices
```

期待されるログシーケンス (`internal/transport/whatsapp/client.go` から):

```
INFO whatsapp.starting store=… allowlist=1
INFO whatsapp.qr_ready
INFO whatsapp.paired
INFO whatsapp.connected
```

デバイス資格情報は `/home/rousseau/.local/share/rousseau/whatsapp.db` に永続化されます。以降の再起動では QR をスキップします。

## ステップ 6: 検証

```sh
podman exec rousseau-agent rousseau status
```

終了コード 0 はデーモンが健全であることを意味します。0 以外はレッドフラッグです — [リファレンス: 終了コード](/ja/reference/exit-codes/) を参照してください。

allowlist に登録された電話からテストメッセージを自分に送信してください。構造化ログには次が表示されます:

```
INFO whatsapp.incoming from=447900123456@s.whatsapp.net
INFO tool.execute name=read id=t_1
INFO whatsapp.handler_ok elapsed=…
```

## ステップ 7: ハードニングレビュー

Quadlet ユニットは既に以下を強制しています:

- `ReadOnly=true` + `Tmpfs=/tmp` — 実行時のイメージ変更なし。
- `DropCapability=all` — Go バイナリは昇格された capability を必要としません。
- `NoNewPrivileges=true` — 子プロセスは特権を得られません。
- `SeccompProfile=/usr/share/containers/seccomp.json` — カーネルレベルの syscall フィルタ。
- `Network=pasta` — rootless ネットワークスタック、デフォルトでインバウンドをブロック。
- `UserNS=keep-id` — バインドマウントされたファイルは両側で期待通りに所有されます。

最も厳格な姿勢が欲しい場合は、Anthropic + Meta が実際に解決する CDN 範囲のみを許可するアウトバウンド専用ファイアウォール (nftables または Cloudflare Zero-Trust) でデーモンをラップしてください。チェックリストについては [ガイド: エンタープライズオンボーディング](/ja/guides/enterprise-onboarding/) を参照してください。

## ステップ 8: バックアップ

永続化された状態全体は 1 つのディレクトリです: `/home/rousseau/.local/share/rousseau/`。それを毎晩 `restic` または `borg` してください。

```sh
sudo -iu rousseau -- restic backup /home/rousseau/.local/share/rousseau
```

`internal/state/sqlite/store.go` の `Open()` によって WAL ジャーナリングが有効になっているため、SQLite データベースはライブでスナップショットしても安全です。

## 関連

- [デプロイ](/ja/deployment/) — 完全な Quadlet ユニットリファレンス。
- [ガイド: プロダクションデプロイ](/ja/guides/production-deployment/) — ログ配送、ローリングリスタート。
- [ガイド: エンタープライズオンボーディング](/ja/guides/enterprise-onboarding/) — SBOM 検証、seccomp 監査。
- [セキュリティ](/ja/security/) — 信頼境界。
