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
description: "rousseau-agent's slog output: message vocabulary, JSON vs text shape, and journalctl / jq recipes."
keywords: "slog, logs, json, text, journalctl, jq, observability"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/reference/logs/"
subtitle: "The full vocabulary of slog messages rousseau emits."
tags: "reference, logs, slog, observability, audit"
title: "リファレンス：ログ"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "slog, logs, json, text, journalctl, jq, observability"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "リファレンス：ログ"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 52
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/reference/logs/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/logs/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "リファレンス：ログ"
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
twitter_description: "rousseau-agent's slog output: message vocabulary, JSON vs text shape, and journalctl / jq recipes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "リファレンス：ログ"
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

## ロガーセットアップ

`internal/cli/root.go` はプロセスごとに 1 つの `*slog.Logger` を構築します — `log.format` が空または `text` のときは `slog.NewTextHandler`、`json` のときは `slog.NewJSONHandler`。レベルは `log.level` (`debug`、`info`、`warn`/`warning`、`error`) からマップされ、デフォルトは `info` です。ハンドラは stderr に書き込みます。すべてのデーモンがこれを継承します。

プロダクションデプロイメントでは、常に `log.format: json` を設定してください。下流のログパイプライン (journald + `journalctl -o json`、Loki、Vector、Datadog Agent) は構造化出力をネイティブにパースします。

## 出力形状

### テキスト

```
time=2026-07-13T18:00:14.202Z level=INFO msg=tool.execute name=grep id=t_1
```

slog のデフォルトテキストレイアウト: `time`、`level`、`msg`、そして key=value ペア。

### JSON

```json
{"time":"2026-07-13T18:00:14.202Z","level":"INFO","msg":"tool.execute","name":"grep","id":"t_1"}
```

同じフィールド、JSON エンコード。`msg` フィールドが安定したイベント識別子です — 人間向けテキストではなくそれでフィルタしアラートしてください。

## メッセージ語彙

`internal/**/*.go` から発行されるすべてのメッセージ名を、ソースの場所と期待されるレベルとともに以下に列挙します。サブシステム別にグループ化され、グループ内でアルファベット順です。

### エージェントループ (`internal/agent/`)

| メッセージ | レベル | フィールド | 意味 |
|---|---|---|---|
| `agent.compressed` | INFO | `messages` | LLM コンプレッサーがセッションを書き直した。新しいメッセージ数は `messages`。 |
| `agent.compress_failed` | WARN | `err` | コンプレッサーがエラーを返した。セッションは触れられないまま。 |
| `tool.denied` | WARN | `name`、`reason` | 承認者がツール呼び出しをブロック。`internal/agent/agent.go:179` のフィールド。 |
| `tool.execute` | INFO | `name`、`id` | 承認者が許可し、ツールが実行された。 |
| `tool.error` | WARN | `name`、`err` | ツールは実行されたがエラーを返した。 |
| `turn.failed` | ERROR | `err` | TUI ターンがエラーになった。`internal/tui/model.go` から発行される。 |
| `session.save_failed` | WARN | `err` | ターン後のセッション永続化が失敗した。 |

### Cron (`internal/cron/scheduler.go`)

| メッセージ | レベル | フィールド | 意味 |
|---|---|---|---|
| `cron.started` | INFO | `poll_interval` | スケジューラ起動。 |
| `cron.scheduled` | INFO | `job`、`expr` | ジョブがメモリ内スケジュールに追加された。 |
| `cron.schedule_failed` | WARN | `job`、`expr`、`err` | robfig/cron/v3 が式を拒否した。 |
| `cron.sync_failed` | WARN | `err` | `cron_jobs` に対する調停パスが失敗。 |
| `cron.firing` | INFO | `job` | ジョブが実行されようとしている。 |
| `cron.completed` | INFO | `job` | ジョブが正常に完了。 |
| `cron.run_failed` | ERROR | `job`、`err` | ジョブ内のプロバイダー呼び出しが失敗。 |
| `cron.delivery_failed` | ERROR | `job`、`target`、`err` | トランスポートへの配信が失敗。 |
| `cron.record_failed` | WARN | `job`、`err` | `last_run_at` の書き込みが失敗。 |

### MCP (`internal/mcp/server.go`)

| メッセージ | レベル | フィールド | 意味 |
|---|---|---|---|
| `mcp.encode_error` | WARN | `err` | レスポンスを JSON エンコードできなかった (稀)。 |
| `mcp.tool_error` | WARN | `tool`、`err` | ツールハンドラがエラーを返した。`isError=true` でホストに表面化される。 |

### ルーター (`internal/transport/router.go`)

| メッセージ | レベル | フィールド | 意味 |
|---|---|---|---|
| `transport.rejected` | WARN | `from` | 送信者が allowlist にない。メッセージはドロップされた。 |
| `router.save_failed` | WARN | `err` | ターン後のセッション保存が失敗。 |
| `router.stale_mapping` | WARN | `jid`、`err` | JID→セッションマッピングが、もうロードされないセッションを指していた。 |

### WhatsApp (`internal/transport/whatsapp/`)

| メッセージ | レベル | フィールド | 意味 |
|---|---|---|---|
| `whatsapp.starting` | INFO | `store`、`allowlist` | ブリッジ起動中。`store` は DSN。 |
| `whatsapp.qr_ready` | INFO | — | QR が stdout にレンダリングされた。スキャンしてください。 |
| `whatsapp.qr_event` | WARN | `event` | whatsmeow からの非成功 QR イベント。 |
| `whatsapp.paired` | INFO | — | 電話が QR を受け入れた。 |
| `whatsapp.connected` | INFO | — | Meta への WebSocket が起動。 |
| `whatsapp.disconnected` | WARN | — | ソケットを失った。自動的にリトライ。 |
| `whatsapp.logged_out` | ERROR | `reason` | Meta がデバイスをログアウトさせた — 通常はポリシー違反。 |
| `whatsapp.voice_enabled` | INFO | `binary`、`model` | ボイスノート文字起こしがオン。 |
| `whatsapp.incoming` | INFO | `from` | インバウンドメッセージが受け入れられた。 |
| `whatsapp.skipped` | DEBUG | `reason` | ルーターがメッセージを破棄した (セルフエコーなど)。 |
| `whatsapp.empty_reply` | INFO | `elapsed` | エージェントがこのターンでテキストを生成しなかった。 |
| `whatsapp.handler_ok` | INFO | `elapsed`、`bytes` | 返信が配信された。 |
| `whatsapp.handler_failed` | ERROR | `err` | ターンがエラーになった — 通常はプロバイダーまたはツール障害。 |
| `whatsapp.send_failed` | ERROR | `err` | Meta への配信が失敗。 |
| `whatsapp.presence_failed` | DEBUG | `err` | 入力プレゼンスの書き込みが失敗 (ベストエフォート)。 |
| `whatsapp.audio_ignored` | INFO | `size` | ボイスノートを受信したが、文字起こしは無効。 |
| `whatsapp.audio_downloaded` | INFO | `size` | ボイスノートのバイトを Meta から取得。 |
| `whatsapp.transcribed` | INFO | `elapsed` | whisper.cpp が文字起こしを返した。 |
| `whatsapp.transcribe_failed` | ERROR | `err` | whisper 呼び出しが失敗。 |

### Slack (`internal/transport/slack/client.go`)

| メッセージ | レベル | フィールド | 意味 |
|---|---|---|---|
| `slack.starting` | INFO | `allowlist` | ブリッジ起動中。 |
| `slack.started` | INFO | — | Socket Mode セッションが受け入れられた。 |
| `slack.session_failed` | WARN | `err` | Socket Mode セッションのオープンに失敗。リトライ。 |
| `slack.frame_failed` | WARN | `err` | Slack からの不正なフレーム。 |
| `slack.incoming` | INFO | `from`、`channel`、`text` | メッセージが受け入れられた。 |
| `slack.handler_failed` | ERROR | `err` | ターンがエラーになった。 |

### Discord (`internal/transport/discord/client.go`)

| メッセージ | レベル | フィールド | 意味 |
|---|---|---|---|
| `discord.starting` | INFO | `allowlist` | ブリッジ起動中。 |
| `discord.ready` | INFO | `bot_id` | Discord ゲートウェイ準備完了。 |
| `discord.started` | INFO | — | セッション起動。 |
| `discord.session_failed` | WARN | `err` | ゲートウェイオープンが失敗。リトライ。 |
| `discord.frame_failed` | WARN | `err` | Discord からの不正フレーム。 |
| `discord.incoming` | INFO | `from`、`channel` | メッセージが受け入れられた。 |
| `discord.handler_failed` | ERROR | `err` | ターンがエラーになった。 |

### Telegram (`internal/transport/telegram/client.go`)

| メッセージ | レベル | フィールド | 意味 |
|---|---|---|---|
| `telegram.starting` | INFO | `allowlist` | ブリッジ起動中。 |
| `telegram.started` | INFO | — | 最初のロングポールが成功。 |
| `telegram.poll_failed` | WARN | `err` | ロングポール HTTP が失敗。 |
| `telegram.incoming` | INFO | `from` | メッセージが受け入れられた。 |
| `telegram.handler_failed` | ERROR | `err` | ターンがエラーになった。 |
| `telegram.send_failed` | ERROR | `err` | アウトバウンド HTTP が失敗。 |

### Matrix (`internal/transport/matrix/client.go`)

| メッセージ | レベル | フィールド | 意味 |
|---|---|---|---|
| `matrix.starting` | INFO | `homeserver`、`allowlist` | ブリッジ起動中。 |
| `matrix.started` | INFO | `homeserver` | 最初の `/sync` が受け入れられた。 |
| `matrix.sync_failed` | WARN | `err` | `/sync` HTTP が失敗。 |
| `matrix.incoming` | INFO | `from`、`room` | メッセージが受け入れられた。 |
| `matrix.handler_failed` | ERROR | `err` | ターンがエラーになった。 |
| `matrix.send_failed` | ERROR | `err` | アウトバウンド HTTP が失敗。 |

### Signal (`internal/transport/signal/`)

| メッセージ | レベル | フィールド | 意味 |
|---|---|---|---|
| `signal.starting` | INFO | `account`、`allowlist` | signal-cli JSON-RPC サブプロセス起動中。 |
| `signal.started` | INFO | — | サブプロセスが ready を報告。 |
| `signal.frame_failed` | WARN | `err` | signal-cli からの不正な JSON フレーム。 |
| `signal.stderr` | WARN | `line` | signal-cli の stderr のパススルー。 |
| `signal.incoming` | INFO | `from` | メッセージが受け入れられた。 |
| `signal.handler_failed` | ERROR | `err` | ターンがエラーになった。 |

### iMessage (`internal/transport/imessage/client.go`)

| メッセージ | レベル | フィールド | 意味 |
|---|---|---|---|
| `imessage.starting` | INFO | `base` | BlueBubbles サーバー URL がログされた。 |
| `imessage.started` | INFO | `server` | 最初のポーリングが成功。 |
| `imessage.prime_failed` | WARN | `err` | プライミング状態のフェッチが失敗。リトライ。 |
| `imessage.poll_failed` | WARN | `err` | ポーリング HTTP が失敗。 |
| `imessage.incoming` | INFO | `from` | メッセージが受け入れられた。 |
| `imessage.handler_failed` | ERROR | `err` | ターンがエラーになった。 |
| `imessage.send_failed` | ERROR | `err` | アウトバウンド HTTP が失敗。 |

### Email + SMS (`internal/transport/email/`、`internal/transport/sms/`)

上記のポーリングトランスポートと同じ `<transport>.starting / .started / .poll_failed / .incoming / .handler_failed / .send_failed` 形状に従います。

## レシピ

### 今日失敗したすべてのツール呼び出しを表示

```sh
journalctl --user -u rousseau-agent --since today -o json \
  | jq -c 'select(.MESSAGE | fromjson? | .msg == "tool.denied")'
```

### 単一のトランスポートセッションをライブで追跡

```sh
journalctl --user -u rousseau-agent -f -o cat \
  | grep -E 'whatsapp\.|tool\.|cron\.'
```

### cron 失敗でアラート

Prometheus/alertmanager ルールのスケッチ ([ガイド: 可観測性](/ja/guides/observability/) の `promtail` → Loki → アラートパイプライン経由):

```yaml
- alert: RousseauCronFailure
  expr: |
    sum by (job) (
      count_over_time({app="rousseau-agent"} |= "cron.run_failed" [5m])
    ) > 0
```

### 秘匿化

`slog` はデフォルトでは秘匿化しません。`whatsapp.send_failed`、`tool.error` などの `err` フィールドを秘匿化するように下流プロセッサを設定してください — プロバイダーエラーは時折プロンプト断片を含む可能性があります。パイプラインについては [ガイド: 可観測性](/ja/guides/observability/) を参照してください。

## 関連

- [ユーザーガイド: 承認ポリシー](/ja/user-guide/approval-policies/) — `tool.denied` の源。
- [ガイド: 可観測性](/ja/guides/observability/) — 完全なパイプラインレシピ。
- [ガイド: 監査 + 承認ポリシー](/ja/guides/audit-approval-policies/) — これらのログを監査証跡として扱います。
