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
description: "Transcribe WhatsApp voice notes to text with whisper.cpp before feeding them into the rousseau-agent agent loop. Opt-in; whisper.cpp not shipped in the container."
keywords: "voice notes, whisper.cpp, transcription, whatsapp, opt-in, audio"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/ja/user-guide/voice-mode/"
subtitle: "Whisper-backed voice-note transcription for WhatsApp."
tags: "voice, whisper, whatsapp, transcription"
title: "音声モード"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "voice notes, whisper.cpp, transcription, whatsapp, opt-in, audio"
news_language: "ja"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "音声モード"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent の RSS フィード
item_guid: "https://docs.rousseau-agent.dev/user-guide/voice-mode/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/voice-mode/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "音声モード"
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
twitter_description: "Transcribe WhatsApp voice notes to text with whisper.cpp before feeding them into the rousseau-agent agent loop. Opt-in; whisper.cpp not shipped in the container."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "音声モード"
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

## ボイスモードの機能

WhatsApp トランスポートがボイスノートを受信すると、rousseau はローカルにインストールされた `whisper.cpp` CLI にシェルアウトして音声をテキストに文字起こしし、そのテキストをユーザーがタイプしたかのようにエージェントループに投入します。返信は通常の WhatsApp テキストメッセージとして返ります。

そのパスは `internal/transport/whatsapp/whisper.go` にあります。他のすべてのトランスポートは今日、テキスト専用です。

**オプトイン。** ボイスモードはデフォルトでオフであり、`whisper.cpp` は rousseau のコンテナイメージに含まれません — CLI を自分でインストールして設定し、1 つの config フラグを切り替えてください。

## 前提条件

- 動作している `rousseau whatsapp` ブリッジ ([最初のトランスポート](/ja/getting-started/first-transport/))。
- デーモンの `$PATH` にある `whisper.cpp` CLI。一般的なバイナリ名: `whisper`、`whisper-cli`、`whisper-cpp`。
- モデルファイル。英語ノートには `base.en` が良い出発点です。より大きなモデルはレイテンシと引き換えに精度を得ます。

## whisper.cpp のインストール

Whisper.cpp は [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp) にあります。ビルドレシピ (ホスト、コンテナではない):

```sh
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
make -j
bash ./models/download-ggml-model.sh base.en
sudo install -m 0755 main /usr/local/bin/whisper
sudo install -m 0644 models/ggml-base.en.bin /usr/local/share/whisper/ggml-base.en.bin
```

`install` 後のバイナリ名は `whisper` です。rousseau のデフォルトバイナリルックアップはその名前を期待します。

## config での有効化

```yaml
whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
  voice:
    enabled: true
    binary: whisper                                # optional; defaults to "whisper"
    model_path: /usr/local/share/whisper/ggml-base.en.bin
    language: en                                   # optional; empty auto-detects
    extra_args: []                                 # appended before the input filename
```

`VoiceConfig` (`internal/config/config.go`) のすべてのフィールド:

| フィールド | 型 | デフォルト | 備考 |
|---|---|---|---|
| `enabled` | bool | `false` | デフォルトでオフ。 |
| `binary` | string | `whisper` | 呼び出す CLI。`whisper-cli`、`whisper-cpp` などにできます。 |
| `model` | string | — | `--model` に渡されます (例: `base.en`、`small`、`medium`)。Whisper のデフォルト解決が適用されます。 |
| `model_path` | string | — | 明示的な `.bin` パス。**`model` より優先されます。** |
| `language` | string | — | `--language` に渡されます。空は自動検出 (遅い)。 |
| `extra_args` | []string | — | 入力ファイル名の前に追加されます。 |

## ボイスノートごとにデーモンが行うこと

1. WhatsApp が音声メッセージを配信します (Opus / OGG / MP3 / M4A / AAC / WAV — 拡張子は mimetype から推論されます)。
2. rousseau がペイロードを一時ファイルに書き込みます: パーミッション `0o600` の `/tmp/rousseau-whisper-XXXX/input.<ext>`。
3. 呼び出します:
   ```
   whisper --output-txt --output-file /tmp/rousseau-whisper-XXXX/output [--model <path>] [--language <lang>] <extra_args...> <input.ext>
   ```
4. `/tmp/rousseau-whisper-XXXX/output.txt` を読み取ります (入力の隣に書き込む whisper.cpp バリアントの場合は `<input>.txt` にフォールバック)。
5. 文字起こしされたテキストをユーザーターンとしてエージェントループに投入します。
6. 一時ディレクトリは `os.RemoveAll` (deferred) でクリーンアップされます。

## `rousseau doctor` での検証

```sh
rousseau doctor
```

以下を探してください:

```
✔ whatsapp.voice.binary     /usr/local/bin/whisper
```

または無効化されているとき:

```
· whatsapp.voice           disabled
```

`whatsapp.voice.binary` の `fail` は `enabled: true` だが CLI がデーモンの `$PATH` にないことを意味します。インストールを修正するかオフにしてください。

## エンドツーエンドでのテスト

1. config でボイスを有効化し、`rousseau whatsapp` を再起動します。
2. 電話から短いボイスノート (「main.go ファイルは何をしますか?」) を録音し、送信します。
3. デーモンログを監視:
   ```
   whatsapp.voice_enabled binary=whisper model=/usr/local/share/whisper/ggml-base.en.bin
   ```
4. デーモンは文字起こしされた質問に対するテキスト回答で返信します。

## レイテンシに関する注意

Whisper はデフォルトで CPU バウンドです。モダンなラップトップでの 10 秒のボイスノートのおおよそのレイテンシ:

| モデル | 推定 CPU レイテンシ |
|---|---|
| `tiny.en` | ~1 秒 |
| `base.en` | ~3 秒 |
| `small.en` | ~8 秒 |
| `medium.en` | ~25 秒 |

whisper.cpp を `WHISPER_COREML=1` (macOS) または `WHISPER_CUBLAS=1` (Linux + NVIDIA) でビルドすると、文字起こしは 2–10 倍速くなり得ます。rousseau は気にしません — 単にシェルアウトするだけです。

## コンテナに関する注意事項

rousseau コンテナイメージ (`docker/Dockerfile`) は `whisper.cpp` を **出荷しません**。コンテナ内でボイスモードが欲しい場合は、イメージを拡張してください:

```dockerfile
# Add on top of the reference Dockerfile
RUN apk add --no-cache build-base git && \
    git clone https://github.com/ggerganov/whisper.cpp /tmp/whisper && \
    make -C /tmp/whisper -j && \
    mkdir -p /usr/local/share/whisper && \
    /tmp/whisper/models/download-ggml-model.sh base.en /usr/local/share/whisper && \
    install -m 0755 /tmp/whisper/main /usr/local/bin/whisper && \
    rm -rf /tmp/whisper
```

または、ホストから `whisper` とモデルを Quadlet ユニットにバインドマウントしてください。

## slog に表面化するエラー

| イベント | 意味 |
|---|---|
| `whisper: empty audio payload` | トランスポートがゼロバイトの音声メッセージを配信した。スキップされる。 |
| `whisper: temp dir: <err>` | `/tmp` が書き込み不可。コンテナの `Tmpfs=/tmp:rw` マウントを確認してください。 |
| `whisper: write audio: <err>` | ディスクフルまたはパーミッション拒否。 |
| `whisper: run <binary>: <err>: <stderr excerpt>` | CLI が 0 以外で終了した。抜粋は 400 文字に切り詰められる。 |
| `whisper: read transcript: <err>` | Whisper は実行されたが、期待される `.txt` ファイルを生成しなかった。しばしば異なるパスに書き込む whisper.cpp バリアント。 |

## プライバシーに関する注意

文字起こしは **完全にホスト上で** 実行されます。音声はデーモンから決して出ません。ホスト型文字起こしサービスに CLI をスワップする場合 (出荷コードの範囲外)、そのベンダーのデータフローを引き受けることになります — 独自の [プライバシー姿勢](/ja/privacy/) に対して検証してください。

## 次に

- [WhatsApp トランスポート](/ja/transports/whatsapp/) — トランスポートリファレンス。
- [設定](/ja/configuration/) — `internal/config/config.go` のすべてのフィールド。
- [デプロイ](/ja/deployment/) — whisper をコンテナにバインドマウントする方法。
