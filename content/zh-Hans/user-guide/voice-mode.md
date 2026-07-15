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
hreflang: "zh-Hans"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "zh-Hans"
locale: "zh_CN"
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
permalink: "https://docs.rousseau-agent.dev/zh-Hans/user-guide/voice-mode/"
subtitle: "Whisper-backed voice-note transcription for WhatsApp."
tags: "voice, whisper, whatsapp, transcription"
title: "语音模式"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "voice notes, whisper.cpp, transcription, whatsapp, opt-in, audio"
news_language: "zh-Hans"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "语音模式"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: rousseau-agent 的 RSS 订阅
item_guid: "https://docs.rousseau-agent.dev/user-guide/voice-mode/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/voice-mode/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "语音模式"
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
twitter_title: "语音模式"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "感谢每一位运行自有编码代理的运维者。"
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## 语音模式做什么

当 WhatsApp 传输接收到语音笔记时，rousseau shell 出到本地安装的 `whisper.cpp` CLI 把音频转写为文本，然后把文本喂进代理循环，就像用户打字一样。回复以常规 WhatsApp 文本消息形式返回。

该路径位于 `internal/transport/whatsapp/whisper.go`。今天其他每一种传输都是仅文本。

**默认关闭。** 语音模式默认关闭，rousseau 的容器镜像不包含 `whisper.cpp` —— 您自己安装并配置 CLI，然后翻一个配置开关。

## 先决条件

- 一个工作中的 `rousseau whatsapp` 桥（[首个传输](/zh-Hans/getting-started/first-transport/)）。
- 守护进程 `$PATH` 上的 `whisper.cpp` CLI。常见二进制名：`whisper`、`whisper-cli`、`whisper-cpp`。
- 一个模型文件。`base.en` 对英语笔记来说是好起点；更大的模型以延迟换准确性。

## 安装 whisper.cpp

Whisper.cpp 位于 [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp)。构建配方（主机而非容器）：

```sh
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
make -j
bash ./models/download-ggml-model.sh base.en
sudo install -m 0755 main /usr/local/bin/whisper
sudo install -m 0644 models/ggml-base.en.bin /usr/local/share/whisper/ggml-base.en.bin
```

`install` 之后的二进制名是 `whisper`；rousseau 的默认二进制查找就期望这个名字。

## 在配置中启用

```yaml
whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
  voice:
    enabled: true
    binary: whisper                                # 可选；默认 "whisper"
    model_path: /usr/local/share/whisper/ggml-base.en.bin
    language: en                                   # 可选；空则自动检测
    extra_args: []                                 # 在输入文件名之前追加
```

`VoiceConfig` 的每个字段（`internal/config/config.go`）：

| 字段 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `enabled` | bool | `false` | 默认关闭。 |
| `binary` | string | `whisper` | 要调用的 CLI。可以是 `whisper-cli`、`whisper-cpp` 等。 |
| `model` | string | — | 传给 `--model`（例如 `base.en`、`small`、`medium`）。Whisper 的默认解析适用。 |
| `model_path` | string | — | 显式 `.bin` 路径。**优先于 `model`。** |
| `language` | string | — | 传给 `--language`。空则自动检测（较慢）。 |
| `extra_args` | []string | — | 在输入文件名之前追加。 |

## 守护进程对每条语音笔记做什么

1. WhatsApp 交付一条音频消息（Opus / OGG / MP3 / M4A / AAC / WAV —— 扩展名从 mimetype 推断）。
2. Rousseau 把负载写入临时文件：`/tmp/rousseau-whisper-XXXX/input.<ext>`，权限 `0o600`。
3. 调用：
   ```
   whisper --output-txt --output-file /tmp/rousseau-whisper-XXXX/output [--model <path>] [--language <lang>] <extra_args...> <input.ext>
   ```
4. 读取 `/tmp/rousseau-whisper-XXXX/output.txt`（对写到输入旁边的 whisper.cpp 变体回退到 `<input>.txt`）。
5. 把转写后的文本作为用户轮次喂进代理循环。
6. 临时目录用 `os.RemoveAll` 清理（deferred）。

## 用 `rousseau doctor` 核实

```sh
rousseau doctor
```

查找：

```
✔ whatsapp.voice.binary     /usr/local/bin/whisper
```

或禁用时：

```
· whatsapp.voice           disabled
```

`whatsapp.voice.binary` 上的 `fail` 意味着 `enabled: true` 但 CLI 不在守护进程的 `$PATH` 上。修复安装或关掉它。

## 端到端测试

1. 在配置中启用语音，重启 `rousseau whatsapp`。
2. 从您的手机录一条简短语音笔记（"what does the file main.go do?"）并发送。
3. 观察守护进程日志：
   ```
   whatsapp.voice_enabled binary=whisper model=/usr/local/share/whisper/ggml-base.en.bin
   ```
4. 守护进程用文本回答转写后的问题。

## 延迟备注

Whisper 默认 CPU 密集型。在现代笔记本上，10 秒语音笔记的近似延迟：

| 模型 | 近似 CPU 延迟 |
|---|---|
| `tiny.en` | ~1s |
| `base.en` | ~3s |
| `small.en` | ~8s |
| `medium.en` | ~25s |

如果您用 `WHISPER_COREML=1`（macOS）或 `WHISPER_CUBLAS=1`（Linux + NVIDIA）构建 whisper.cpp，转写可快 2–10 倍。Rousseau 不在意 —— 它只是 shell 出。

## 容器注意事项

rousseau 容器镜像（`docker/Dockerfile`）**不**包含 `whisper.cpp`。如果您想在容器内使用语音模式，扩展镜像：

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

或从主机把 `whisper` 与模型 bind-mount 到 Quadlet 单元内。

## slog 中浮现的错误

| 事件 | 含义 |
|---|---|
| `whisper: empty audio payload` | 传输交付了零字节音频消息。跳过。 |
| `whisper: temp dir: <err>` | `/tmp` 不可写。检查容器的 `Tmpfs=/tmp:rw` 挂载。 |
| `whisper: write audio: <err>` | 磁盘满或权限被拒。 |
| `whisper: run <binary>: <err>: <stderr excerpt>` | CLI 非零退出。摘录截到 400 字符。 |
| `whisper: read transcript: <err>` | Whisper 运行了但没产出预期的 `.txt` 文件。通常是写到不同路径的 whisper.cpp 变体。 |

## 隐私备注

转写**完全在主机上**运行。音频永不离开守护进程。如果您把 CLI 换成托管转写服务（不在发布代码范围内），您就承担了那个供应商的数据流 —— 请与您自己的 [隐私姿态](/zh-Hans/privacy/) 对照核实。

## 下一步

- [WhatsApp 传输](/zh-Hans/transports/whatsapp/) —— 传输参考。
- [配置](/zh-Hans/configuration/) —— `internal/config/config.go` 中的每个字段。
- [部署](/zh-Hans/deployment/) —— 如何把 whisper bind-mount 到容器。
