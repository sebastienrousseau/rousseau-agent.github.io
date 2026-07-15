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
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "en-GB"
locale: "en_GB"
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
permalink: "https://docs.rousseau-agent.dev/user-guide/voice-mode/"
subtitle: "Whisper-backed voice-note transcription for WhatsApp."
tags: "voice, whisper, whatsapp, transcription"
title: "Voice Mode"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "voice notes, whisper.cpp, transcription, whatsapp, opt-in, audio"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Voice Mode"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/voice-mode/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/voice-mode/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Voice Mode"
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
twitter_title: "Voice Mode"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## What voice mode does

When the WhatsApp transport receives a voice note, rousseau shells out to a locally installed `whisper.cpp` CLI to transcribe the audio into text, then feeds the text into the agent loop as if the user had typed it. The reply comes back as a normal WhatsApp text message.

The path lives in `internal/transport/whatsapp/whisper.go`. Every other transport is text-only today.

**Opt-in.** Voice mode is off by default, and `whisper.cpp` is not shipped with rousseau's container image — you install and configure the CLI yourself, then flip a single config flag.

## Prerequisites

- A working `rousseau whatsapp` bridge ([First transport](/getting-started/first-transport/)).
- The `whisper.cpp` CLI on the daemon's `$PATH`. Common binary names: `whisper`, `whisper-cli`, `whisper-cpp`.
- A model file. `base.en` is a good starting point for English-language notes; larger models trade latency for accuracy.

## Installing whisper.cpp

Whisper.cpp lives at [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp). Build recipe (host, not container):

```sh
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
make -j
bash ./models/download-ggml-model.sh base.en
sudo install -m 0755 main /usr/local/bin/whisper
sudo install -m 0644 models/ggml-base.en.bin /usr/local/share/whisper/ggml-base.en.bin
```

The binary name after `install` is `whisper`; rousseau's default binary lookup expects that name.

## Enabling in config

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

Every field in `VoiceConfig` (`internal/config/config.go`):

| Field | Type | Default | Notes |
|---|---|---|---|
| `enabled` | bool | `false` | Off by default. |
| `binary` | string | `whisper` | The CLI to invoke. Can be `whisper-cli`, `whisper-cpp`, etc. |
| `model` | string | — | Passed to `--model` (e.g. `base.en`, `small`, `medium`). Whisper's default resolution applies. |
| `model_path` | string | — | Explicit `.bin` path. **Takes precedence over `model`.** |
| `language` | string | — | Passed to `--language`. Empty auto-detects (slower). |
| `extra_args` | []string | — | Appended before the input filename. |

## What the daemon does on each voice note

1. WhatsApp delivers an audio message (Opus / OGG / MP3 / M4A / AAC / WAV — the extension is inferred from the mimetype).
2. Rousseau writes the payload to a temp file: `/tmp/rousseau-whisper-XXXX/input.<ext>` with permission `0o600`.
3. Invokes:
   ```
   whisper --output-txt --output-file /tmp/rousseau-whisper-XXXX/output [--model <path>] [--language <lang>] <extra_args...> <input.ext>
   ```
4. Reads `/tmp/rousseau-whisper-XXXX/output.txt` (falls back to `<input>.txt` for whisper.cpp variants that write next to the input).
5. Feeds the transcribed text into the agent loop as the user turn.
6. Temp directory is cleaned up with `os.RemoveAll` (deferred).

## Verifying with `rousseau doctor`

```sh
rousseau doctor
```

Look for:

```
✔ whatsapp.voice.binary     /usr/local/bin/whisper
```

or when disabled:

```
· whatsapp.voice           disabled
```

A `fail` on `whatsapp.voice.binary` means `enabled: true` but the CLI is not on the daemon's `$PATH`. Fix the install or turn it off.

## Testing end-to-end

1. Enable voice in config, restart `rousseau whatsapp`.
2. From your phone, record a short voice note ("what does the file main.go do?") and send it.
3. Watch the daemon log:
   ```
   whatsapp.voice_enabled binary=whisper model=/usr/local/share/whisper/ggml-base.en.bin
   ```
4. The daemon replies with a text answer to the transcribed question.

## Latency notes

Whisper is CPU-bound by default. Approximate latencies for a 10-second voice note on a modern laptop:

| Model | Approx. CPU latency |
|---|---|
| `tiny.en` | ~1s |
| `base.en` | ~3s |
| `small.en` | ~8s |
| `medium.en` | ~25s |

If you build whisper.cpp with `WHISPER_COREML=1` (macOS) or `WHISPER_CUBLAS=1` (Linux + NVIDIA), transcription can be 2–10x faster. Rousseau does not care — it just shells out.

## Container caveats

The rousseau container image (`docker/Dockerfile`) does **not** ship `whisper.cpp`. If you want voice mode inside the container, extend the image:

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

Or bind-mount `whisper` and the model from the host into the Quadlet unit.

## Errors surfaced to slog

| Event | Meaning |
|---|---|
| `whisper: empty audio payload` | The transport delivered a zero-byte audio message. Skipped. |
| `whisper: temp dir: <err>` | `/tmp` is not writable. Check the container's `Tmpfs=/tmp:rw` mount. |
| `whisper: write audio: <err>` | Disk full or permission denied. |
| `whisper: run <binary>: <err>: <stderr excerpt>` | The CLI exited non-zero. Excerpt is truncated to 400 chars. |
| `whisper: read transcript: <err>` | Whisper ran but did not produce the expected `.txt` file. Often a whisper.cpp variant that writes to a different path. |

## Privacy notes

Transcription runs **entirely on the host**. Audio never leaves the daemon. If you swap the CLI for a hosted transcription service (out of scope for the shipped code), you take on that vendor's data flow — verify against your own [privacy posture](/privacy/).

## Next

- [WhatsApp transport](/transports/whatsapp/) — the transport reference.
- [Configuration](/configuration/) — every field in `internal/config/config.go`.
- [Deployment](/deployment/) — how to bind-mount whisper into the container.
