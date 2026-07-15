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
description: "Troubleshoot rousseau-agent: WhatsApp QR won't scan, reconnect loops, cosign verify failures, SELinux bind-mount errors, cron not firing, approval policy denying everything."
keywords: "troubleshooting, WhatsApp QR, reconnect loop, cosign verify, SELinux, bind mount, cron, approval policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/troubleshooting/"
subtitle: "よくある失敗パターンと解決方法。"
tags: "troubleshooting, support"
title: "トラブルシューティング"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "troubleshooting, WhatsApp QR, reconnect loop, cosign verify, SELinux, bind mount, cron, approval policy"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "トラブルシューティング"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "support"
order: 27
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/troubleshooting/index.html"
item_link: "https://docs.rousseau-agent.dev/troubleshooting/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "トラブルシューティング"
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
twitter_description: "Troubleshoot rousseau-agent: WhatsApp QR won't scan, reconnect loops, cosign verify failures, SELinux bind-mount errors, cron not firing, approval policy denying everything."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "トラブルシューティング"
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

## WhatsApp: QR がスキャンできない

症状: `rousseau whatsapp` が出力する QR を電話アプリが拒否する、またはペアリングダイアログに「This device is not paired with WhatsApp」と表示される。

修正:

1. **コンテナを再ビルドする。** 古いイメージを実行している場合、`whatsmeow` にプロトコル更新が入っていることがあります。再ビルドします。
   ```sh
   podman build -t rousseau-agent:local -f docker/Dockerfile .
   systemctl --user restart rousseau-agent.service
   ```
2. **`whatsapp.db` を削除する。** ペアリングが途中で終わると、whatsmeow が再利用できない状態で DB が残ります。削除して再ペアリングします。
   ```sh
   rm ~/.local/share/rousseau/whatsapp.db
   ```
3. **時計ズレを確認する。** WhatsApp のハンドシェイクは時刻に敏感です。コンテナの時計が 30 秒以上ずれていると、ペアリングは静かに失敗します。
   ```sh
   timedatectl status
   ```

## WhatsApp の再接続ループ

症状: ログに数秒ごとに `whatsapp.connected` と `whatsapp.disconnected` が繰り返し出力される。

修正:

1. **時計ズレ。** 上と同じ対策です。
2. **allowlist の設定誤り。** すべての受信メッセージが非認可として破棄されます。無視の連続が多いとサーバーによってはソケットを閉じます。`--allow` で正しい JID を追加してください。
3. **Meta 側の BAN。** WhatsApp モバイルアプリに「This device has been logged out」と表示される場合、Meta がペアリングを無効化しています。新しい QR で再ペアリングします。同じ番号で繰り返し発生する場合は、その番号の利用をやめてください。

## cosign verify-blob が失敗する

症状:

```
Error: no matching signatures
```

修正:

1. **certificate-identity 正規表現が誤り。** 正規表現はリリースに署名した GitHub リポジトリと一致する必要があります。rousseau-agent のリリースでは正しい値は次のとおりです:
   ```
   --certificate-identity-regexp 'sebastienrousseau/rousseau-agent'
   ```
   `.*` は使わないでください。あらゆるリポジトリの cosign 署名を受け入れてしまいます。
2. **OIDC 発行者が誤り。** GitHub Actions の cosign 署名は `https://token.actions.githubusercontent.com` から発行されます。他の CI プロバイダ（GitLab、Buildkite）は別 URL から発行します。
3. **署名ファイルが誤り。** `<version>_checksums.txt.sig` が検証対象の `_checksums.txt`（別リリースの古いコピーではない）に対応しているか確認してください。
4. **Sigstore の trust root が変更された。** `cosign initialize` でリフレッシュしてください。trust root はゆっくりとローテーションで更新されます。

## コンテナがバインドマウントに失敗する

症状: `podman play kube` または `systemctl --user start rousseau-agent.service` がバインドマウントで `permission denied` を返す。

修正:

1. **SELinux ラベル。** Podman が正しい SELinux ラベルを付与するよう、すべてのボリューム行は `:Z`（共有の場合は `:z`）で終える必要があります。
   ```
   Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
   ```
   `:Z`（大文字）は private ラベルで、単一コンテナのマウントに適しています。`:z`（小文字）はコンテナ間でラベルを共有します。
2. **`keep-id` マッピング。** `UserNS=keep-id` がないとコンテナ UID 1000 がホストの subuid レンジに再マッピングされ、ホスト所有のファイルに書き込めません。Quadlet に以下があることを確認してください:
   ```
   UserNS=keep-id
   ```
3. **ディレクトリが存在しない。** Podman はバインドマウント元を自動作成しません。事前に作成してください。
   ```sh
   mkdir -p ~/.local/share/rousseau
   ```

## cron ジョブが発火しない

症状: `rousseau cron list` にジョブが表示されるが、スケジュール時刻になっても何も起こらない。

修正:

1. **ステータスを確認。** `rousseau status` はスケジューラの活動を報告します。スケジューラが動作していない場合、それをホストするデーモンも動作していません。
2. **タイムゾーン。** スケジュールはサーバーのローカルタイムゾーンを使用します。`timedatectl` で確認してください。ホストのロケールに依存しない決定的なスケジューリングが必要なら、Quadlet で `TZ=UTC` を設定します。
3. **PollInterval による遅延。** 新規ジョブは `PollInterval`（デフォルト 60 秒）以内に有効になります。1 分待ってください。
4. **配信失敗。** ジョブは発火したが配信に失敗しました。ログで `cron.delivery_failed` を確認してください。宛先のフォーマットはトランスポート依存です（[/cron/](/ja/cron/) を参照）。

## 承認ポリシーがすべてを拒否する

症状: すべてのツール呼び出しが「denied by pattern policy」で拒否され、モデルが前進できない。

修正:

1. **allow ルールが欠落。** `default: deny` の `pattern` モードでは、すべてのツール呼び出しに一致する allow ルールが必要です。許可したいツールに対して追加してください。
   ```yaml
   agent:
     approver:
       mode: pattern
       default: deny
       allow:
         - {tool: read, match: ".*"}
         - {tool: grep, match: ".*"}
         - {tool: edit, match: "^./workspace/.*"}
   ```
2. **deny が allow に勝つ。** 同じツールでは `deny` ルールは常に `allow` に勝ちます。deny リストに意図しない広範なマッチがないか確認してください。
3. **デフォルトを緩める。** 対面セッションでは、絞った deny ルールと組み合わせた `default: allow` の方が扱いやすいことが多いです。
   ```yaml
   agent:
     approver:
       mode: pattern
       default: allow
       deny:
         - {tool: bash, match: "rm -rf|sudo"}
   ```

## プロバイダが 401 を返す

症状: エージェントが `provider: unauthorized` でエラーを返す。

修正:

1. **API キーが誤り。** Anthropic 直接プロバイダの場合、`ANTHROPIC_API_KEY` がエクスポートされているか、`~/.config/rousseau/config.yaml` に設定されているか確認してください。
2. **認証情報チェーンが誤り。** Bedrock の場合、コンテナ内から `aws sts get-caller-identity` を実行して、SDK が解決するプリンシパルを確認してください。
3. **Vertex のサービスアカウント。** Vertex プロバイダの場合、`vertex.credentials_file` のファイルがコンテナ内から読み取り可能で、`roles/aiplatform.user` が付与されていることを確認してください。

## プロバイダが 429 を返す

症状: エージェントが `provider: rate limited` でエラーを返す。

修正:

1. **`max_tokens` を下げる。** 補完が短いほどレートウィンドウを早くクリアします。
2. **圧縮を有効化する。** 長いトランスクリプトは入力トークン圧を増します。`agent.compression.enabled: true` で古いメッセージを畳み込みます。
3. **待つ。** rousseau は `Complete` 内でリトライしません。呼び出し側（チャットトランスポート、cron スケジューラ、`rousseau chat`）がリトライの可否と方法を決めます。

## `rousseau chat` が空白の TUI しか表示しない

症状: Bubble Tea TUI は開くがカーソルもビューポートも表示されない。

修正:

1. **TERM 環境。** rousseau は ANSI 対応ターミナルを必要とします。`TERM=xterm-256color`（または類似）を設定してください。
2. **stdin がラップされている。** `nohup` やパイプで実行するとターミナルが剥がれます。対話的に実行してください。

## Slack: 起動時に `invalid_auth`

症状: `slack.starting` の直後に `invalid_auth`。

修正:

1. **トークンの取り違え。** Rousseau は `xapp-…`（アプリレベル、`--app-token`）と `xoxb-…`（ボット、`--bot-token`）の両方を必要とします。ボットトークンが期待される場所にアプリトークンを渡すとこのエラーが出ます。
2. **アプリ未インストール。** スコープを作成したら、Slack アプリ設定で *Install to Workspace* をクリックしてください。トークンはインストール後にのみ有効になります。
3. **トークンがローテートされた。** Slack のトークンは管理者が手動でローテートできます。ローテートした場合は、それを使うすべてのデーモンを新しい値で再起動する必要があります。

## Slack: ボットが自分のメッセージに返信する（ループ）

症状: rousseau の送信メッセージが受信イベントを引き起こし、デーモンがそれに応答して返信が暴走する。

修正:

1. **`bot_user_id` を設定する。** `--bot-user-id` フラグ（またはコンフィグの `slack.bot_user_id`）は、そのユーザー ID が送ったメッセージを無視するようデーモンに指示します。`curl -H "Authorization: Bearer xoxb-..." https://slack.com/api/auth.test` で取得できます。
2. **イベントフィルタを確認する。** トランスポートはデフォルトで `bot_message` サブタイプを無視しますが、設定の悪い Slack アプリがこれをバイパスすることがあります。

## Discord: メッセージ本文が空で届く

症状: `discord.incoming from=... body=` — メッセージは通るが内容がない。

修正:

1. **Message Content Intent が無効。** Discord Developer Portal の <em>Bot &gt; Privileged Gateway Intents</em> で **Message Content Intent** を有効化してください。これがないと Discord は Gateway イベントからメッセージ本文を削除します。
2. **スコープ不足。** 招待 URL は、使用するチャンネル/DM に対するボットの `Read Message History` と `Send Messages` を付与している必要があります。

## Discord: `disallowed intents`

症状: 起動時に `Discord returned 4014 disallowed intents` でエラー。

修正:

1. **特権 intent。** *Message Content Intent* を有効化してください（上記参照）。要求しない場合でも、承認なく要求すると Discord は 4014 を返します。
2. **検証（Verification）。** 100 サーバー以上に参加しているボットは特権 intent を使うために Discord 検証が必要です。Developer Portal のウォークスルーに従ってください。

## Telegram: `unauthorized`

症状: `telegram.starting` の後に `getUpdates: 401`。

修正:

1. **トークンが誤り。** BotFather はトークンを一度だけ返します。末尾のピリオドを含めないでください。トークンの形式は `<bot_id>:<secret>` です。
2. **トークンが失効。** BotFather の `/revoke` は現在のトークンを無効化します。新しいものを取得してください。

## Email: `dial tcp: i/o timeout`

症状: IMAP または SMTP の接続が完了しない。

修正:

1. **ポートが誤り。** IMAP は `993`（implicit TLS）。SMTP submission は `587`（STARTTLS）または `465`（implicit TLS）です。Rousseau は両方で implicit TLS を使用します。STARTTLS のみのサーバーはまだサポートしていません。移行については [トランスポート: Email](/ja/transports/email/) を参照してください。
2. **egress ブロック。** 企業ファイアウォールは送信 SMTP をブロックすることがよくあります。コンテナから `openssl s_client -connect smtp.example.com:465` でテストしてください。
3. **プロバイダがアプリパスワードを要求する。** Gmail、Fastmail などは 2FA が有効な場合、アカウントパスワードではなくアプリパスワードを要求します。プロバイダのセキュリティ設定から生成してください。

## Vertex: `permission denied on resource`

症状: `vertex: HTTP 403 permission denied on resource projects/.../models/claude-sonnet-4-6@…:rawPredict`。

修正:

1. **ロール不足。** API を呼び出すサービスアカウントまたはユーザーに `roles/aiplatform.user` を付与してください。IAM 変更の反映には最大 1 分かかります。
2. **プロジェクトが誤り。** コンフィグの `project` はクォータを持つプロジェクトと一致する必要があります。課金が別プロジェクトなら、`gcloud auth application-default set-quota-project` で quota-project を使用してください。
3. **リージョン不一致。** モデルは要求したリージョンで利用可能である必要があります。Vertex Model Garden で確認できます。

## Bedrock: `You don't have access to the model`

症状: `AccessDeniedException: You don't have access to the model with the specified model ID`。

修正:

1. **モデルアクセスが未申請。** Bedrock はコンソール経由の明示的なモデルアクセス申請（*Foundation models &gt; Model access*）を要求します。IAM で `InvokeModel` を許可していてもこのステップは必要です。
2. **リージョンが誤り。** モデルの可用性はリージョン単位です。Bedrock コンソールで確認してください。
3. **クロスアカウントの設定ミス。** AssumeRole を使う場合、ターゲットロールのポリシーが正確なモデル ARN に対して `bedrock:InvokeModel` を許可しているか確認してください。

## Ollama: `context deadline exceeded`

症状: Ollama が生成中に rousseau がタイムアウトする。

修正:

1. **CPU 推論が遅い。** ノートパソコン CPU 上の 70B モデルは 1 ターン数分かかります。より小さいモデル（`llama3.1:8b`）や GPU ホストを使ってください。
2. **タイムアウトの継承。** rousseau は SDK デフォルトの HTTP タイムアウトを使用します。自前でプロバイダをラップする場合、タイムアウトを最低 120 秒に延長してください。

## ボイスノート: 文字起こしツールが未設定

症状: `whatsapp.audio_ignored reason=transcriber_not_configured`。

修正:

1. **Whisper が無効。** コンフィグで `whatsapp.voice.enabled: true` を設定し、`whisper` バイナリが `PATH` にあることを確認してください（または `whatsapp.voice.binary` に絶対パスを設定）。
2. **モデルファイルが欠落。** `whatsapp.voice.model_path` に明示的な `.bin` ファイルを設定してください。Whisper.cpp モデルは手動でダウンロードします。コンフィグはその配置先を指します。

## セッションストア: `database is locked`

症状: WAL ライタがブロックされ、リクエストがタイムアウトする。

修正:

1. **2 つのデーモン、1 つの DB。** WAL 付き SQLite は複数の読み手をサポートしますが、書き手は 1 つだけです。同じ `state.path` に対して 2 つの rousseau プロセスを走らせると、一方がブロックされます。異なる state パスを使ってください。
2. **`busy_timeout` が低すぎる。** DSN は `busy_timeout=15000` を設定します。持続する競合下では引き上げてください。ただし、まず根本原因を調査してください。
3. **古い WAL ファイル。** クラッシュしたライタが `sessions.db-wal` をロックしたまま残すことがあります。すべて停止し、`sessions.db-wal` と `sessions.db-shm` を削除し、再起動してください。

## MCP: Claude Desktop に rousseau のツールが見えない

症状: `claude_desktop_config.json` で `command: "rousseau"` を用いて rousseau を起動したが、ツールが表示されない。

修正:

1. **コンフィグが保存されていない。** Claude Desktop は保存時にホットリロードします。実行中のインスタンスでファイルを編集した場合は再起動してください。
2. **`command` が PATH にない。** Claude Desktop は自分の環境からサブプロセスを起動します。`/usr/local/bin/rousseau` が見えないことがあります。絶対パスを使ってください。
3. **stderr のノイズ。** rousseau は構造化ログを stderr に書き込みます。非常に饒舌なロガーはホストを圧倒することがあります。厳格なホストに対して MCP を実行する際は `log.level: warn` を設定してください。

## Skills: `skill loader: parse: yaml: line X`

症状: rousseau が起動時に YAML パースエラーで失敗する。

修正:

1. **フロントマターの形式が誤り。** Skills は `---` で区切られた YAML フロントマターを使用します。両方のフェンスがあり、タブインデントがないことを確認してください。
2. **クォートされていないコロン。** 値の中のコロン（`description: this: that`）はネストされたマップとしてパースされます。値をクォートしてください: `description: "this: that"`。

## `rousseau doctor` が `warn` を報告する

症状: doctor は完了するが黄色の行がある。

修正:

1. **理由を読む。** すべての warn 行には理由が含まれます。よくあるもの: `whatsapp.paired=false`（一度もリンクしていない）、`state.wal_size=large`（チェックポイント遅延）、`provider.claudecli.model=unset`（claude のデフォルトを使用）。
2. **warn は失敗ではない。** デーモンは起動します。その行はレビュー価値のあるものを示唆しているだけです。

## Kubernetes: Pod が `CrashLoopBackOff` から抜けない

症状: Deployment が Ready にならない。

修正:

1. **ログを読む。** `kubectl logs -p <pod>` で前のコンテナの stderr が表示されます。10 回中 9 回はコンフィグまたは認証情報のエラーです。
2. **状態ボリュームが欠落。** `~/.local/share/rousseau` の PVC がないと、ペアリングは再起動を越えて残らず、デーモンは再ペアリングしようとしてループします。
3. **IRSA / Workload Identity の設定ミス。** サービスアカウントアノテーションが、プロバイダ権限を持つ IAM ロールと一致することを確認してください。Pod に `kubectl exec` して `aws sts get-caller-identity`（Bedrock）または `gcloud auth print-access-token`（Vertex）を実行して確認します。

## nftables ルールセットがプロバイダ egress をブロックする

症状: 送信ルールセットを適用した直後の最初のプロバイダ呼び出しで `dial tcp: i/o timeout`。

修正:

1. **CIDR がローテートされた。** プロバイダの IP レンジは変わります。cron でリフレッシュされる ipset を用いた DNS ベースの egress を使うか、接続時に解決する egress プロキシを使ってください。
2. **DNS がブロックされている。** 送信ルールセットは DNS リゾルバへの UDP/53（または TCP/53）を許可する必要があります。

## 構造化ログのフィールド欠落

症状: `whatsapp.incoming` が `from` だけを持ち、他の属性を含まない。

修正:

1. **ログレベルが高すぎる。** 一部フィールドは `debug` でしか出力されません。コンフィグで `log.level: debug` を設定してください。
2. **JSON パーサがフィールドを食っている。** 未知フィールドを削るフィルタを通すと `elapsed`、`bytes` などが落ちます。生の stdout に対して検証してください。

## 関連ページ

- [はじめに: はじめてのトランスポート](/ja/getting-started/first-transport/) — エンドツーエンドのウォークスルー。
- [プロバイダ](/ja/providers/) — プロバイダ別のトラブルシューティング。
- [トランスポート](/ja/transports/) — トランスポート別のトラブルシューティング。
- [設定](/ja/configuration/) — すべてのノブの正典。
- [セキュリティ](/ja/security/) — 信頼境界と監査トレイル。

## さらに読む

- `internal/cli/doctor.go` — doctor の実装。
- `internal/state/sqlite/store.go` — セッションストアの DSN と WAL 処理。
- `internal/transport/router.go` — 受信イベントのルーティングと allowlist。
- slog 属性キーリファレンス — ソースツリー内のすべての `.info()` / `.warn()` / `.error()`。
