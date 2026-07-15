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
hreflang: "pt-BR"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "pt-BR"
locale: "pt_BR"
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
permalink: "https://docs.rousseau-agent.dev/pt-BR/user-guide/voice-mode/"
subtitle: "Whisper-backed voice-note transcription for WhatsApp."
tags: "voice, whisper, whatsapp, transcription"
title: "Modo de voz"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "voice notes, whisper.cpp, transcription, whatsapp, opt-in, audio"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Modo de voz"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/voice-mode/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/voice-mode/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Modo de voz"
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
twitter_title: "Modo de voz"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Obrigado a cada operador que executa seu próprio agente de codificação."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## O que o modo de voz faz

Quando o transporte WhatsApp recebe uma voice note, o rousseau faz shell-out para um CLI `whisper.cpp` instalado localmente para transcrever o áudio em texto, então alimenta o texto no agent loop como se o usuário tivesse digitado. A resposta volta como uma mensagem de texto WhatsApp normal.

O caminho vive em `internal/transport/whatsapp/whisper.go`. Todo outro transporte é somente texto hoje.

**Opt-in.** O modo de voz está desligado por padrão, e `whisper.cpp` não vem com a imagem de contêiner do rousseau — você instala e configura o CLI por conta própria, então vira uma única flag de config.

## Pré-requisitos

- Um bridge `rousseau whatsapp` funcionando ([Primeiro transporte](/pt-BR/getting-started/first-transport/)).
- O CLI `whisper.cpp` no `$PATH` do daemon. Nomes comuns de binário: `whisper`, `whisper-cli`, `whisper-cpp`.
- Um arquivo de modelo. `base.en` é um bom ponto de partida para notas em inglês; modelos maiores trocam latência por acurácia.

## Instalando whisper.cpp

Whisper.cpp vive em [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp). Receita de build (host, não contêiner):

```sh
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
make -j
bash ./models/download-ggml-model.sh base.en
sudo install -m 0755 main /usr/local/bin/whisper
sudo install -m 0644 models/ggml-base.en.bin /usr/local/share/whisper/ggml-base.en.bin
```

O nome do binário após `install` é `whisper`; a busca padrão de binário do rousseau espera esse nome.

## Habilitando na config

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

Cada campo em `VoiceConfig` (`internal/config/config.go`):

| Campo | Tipo | Padrão | Notas |
|---|---|---|---|
| `enabled` | bool | `false` | Desligado por padrão. |
| `binary` | string | `whisper` | O CLI a invocar. Pode ser `whisper-cli`, `whisper-cpp`, etc. |
| `model` | string | — | Passado para `--model` (por exemplo, `base.en`, `small`, `medium`). Resolução padrão do Whisper se aplica. |
| `model_path` | string | — | Caminho `.bin` explícito. **Tem precedência sobre `model`.** |
| `language` | string | — | Passado para `--language`. Vazio faz auto-detect (mais lento). |
| `extra_args` | []string | — | Anexado antes do nome do arquivo de entrada. |

## O que o daemon faz em cada voice note

1. WhatsApp entrega uma mensagem de áudio (Opus / OGG / MP3 / M4A / AAC / WAV — a extensão é inferida do mimetype).
2. O rousseau escreve o payload em um arquivo temp: `/tmp/rousseau-whisper-XXXX/input.<ext>` com permissão `0o600`.
3. Invoca:
   ```
   whisper --output-txt --output-file /tmp/rousseau-whisper-XXXX/output [--model <path>] [--language <lang>] <extra_args...> <input.ext>
   ```
4. Lê `/tmp/rousseau-whisper-XXXX/output.txt` (faz fallback para `<input>.txt` para variantes de whisper.cpp que escrevem ao lado da entrada).
5. Alimenta o texto transcrito no agent loop como o turno do usuário.
6. O diretório temp é limpo com `os.RemoveAll` (deferido).

## Verificando com `rousseau doctor`

```sh
rousseau doctor
```

Procure por:

```
✔ whatsapp.voice.binary     /usr/local/bin/whisper
```

ou quando desabilitado:

```
· whatsapp.voice           disabled
```

Um `fail` em `whatsapp.voice.binary` significa `enabled: true` mas o CLI não está no `$PATH` do daemon. Conserte a instalação ou desligue.

## Testando end-to-end

1. Habilite voz na config, reinicie `rousseau whatsapp`.
2. Do seu celular, grave uma voice note curta ("what does the file main.go do?") e envie.
3. Observe o log do daemon:
   ```
   whatsapp.voice_enabled binary=whisper model=/usr/local/share/whisper/ggml-base.en.bin
   ```
4. O daemon responde com uma resposta em texto à pergunta transcrita.

## Notas de latência

O Whisper é CPU-bound por padrão. Latências aproximadas para uma voice note de 10 segundos em um laptop moderno:

| Modelo | Latência CPU aproximada |
|---|---|
| `tiny.en` | ~1s |
| `base.en` | ~3s |
| `small.en` | ~8s |
| `medium.en` | ~25s |

Se você buildar whisper.cpp com `WHISPER_COREML=1` (macOS) ou `WHISPER_CUBLAS=1` (Linux + NVIDIA), a transcrição pode ser 2–10x mais rápida. O rousseau não liga — só faz shell-out.

## Ressalvas de contêiner

A imagem de contêiner do rousseau (`docker/Dockerfile`) **não** envia `whisper.cpp`. Se você quer modo de voz dentro do contêiner, estenda a imagem:

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

Ou faça bind-mount de `whisper` e do modelo do host para dentro da unidade Quadlet.

## Erros expostos ao slog

| Evento | Significado |
|---|---|
| `whisper: empty audio payload` | O transporte entregou uma mensagem de áudio de zero bytes. Pulada. |
| `whisper: temp dir: <err>` | `/tmp` não é gravável. Verifique o mount `Tmpfs=/tmp:rw` do contêiner. |
| `whisper: write audio: <err>` | Disco cheio ou permissão negada. |
| `whisper: run <binary>: <err>: <stderr excerpt>` | O CLI saiu com não-zero. Excerpt truncado em 400 chars. |
| `whisper: read transcript: <err>` | O Whisper rodou mas não produziu o arquivo `.txt` esperado. Frequentemente uma variante de whisper.cpp que escreve em um caminho diferente. |

## Notas de privacidade

A transcrição roda **inteiramente no host**. Áudio nunca deixa o daemon. Se você trocar o CLI por um serviço hospedado de transcrição (fora do escopo do código enviado), você assume o fluxo de dados daquele vendor — verifique contra sua própria [postura de privacidade](/pt-BR/privacy/).

## Próximo

- [Transporte WhatsApp](/pt-BR/transports/whatsapp/) — a referência do transporte.
- [Configuração](/pt-BR/configuration/) — cada campo em `internal/config/config.go`.
- [Implantação](/pt-BR/deployment/) — como bind-mountar whisper no contêiner.
