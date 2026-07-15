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
hreflang: "de"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "de"
locale: "de_DE"
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
permalink: "https://docs.rousseau-agent.dev/de/user-guide/voice-mode/"
subtitle: "Whisper-backed voice-note transcription for WhatsApp."
tags: "voice, whisper, whatsapp, transcription"
title: "Sprachmodus"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "voice notes, whisper.cpp, transcription, whatsapp, opt-in, audio"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Sprachmodus"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/voice-mode/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/voice-mode/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Sprachmodus"
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
twitter_title: "Sprachmodus"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Was der Sprachmodus tut

Wenn der WhatsApp-Transport eine Sprachnachricht empfängt, ruft rousseau eine lokal installierte `whisper.cpp`-CLI auf, um das Audio in Text zu transkribieren, und speist den Text dann in die Agent-Schleife, als hätte der Benutzer ihn getippt. Die Antwort kommt als normale WhatsApp-Textnachricht zurück.

Der Pfad lebt in `internal/transport/whatsapp/whisper.go`. Jeder andere Transport ist heute nur textbasiert.

**Opt-in.** Der Sprachmodus ist standardmäßig aus, und `whisper.cpp` wird nicht mit rousseaus Container-Image ausgeliefert – Sie installieren und konfigurieren die CLI selbst und schalten dann ein einziges Konfigurations-Flag um.

## Voraussetzungen

- Eine funktionierende `rousseau whatsapp`-Bridge ([Erster Transport](/de/getting-started/first-transport/)).
- Die `whisper.cpp`-CLI im `$PATH` des Daemons. Übliche Binary-Namen: `whisper`, `whisper-cli`, `whisper-cpp`.
- Eine Modelldatei. `base.en` ist ein guter Ausgangspunkt für englischsprachige Notizen; größere Modelle tauschen Latenz gegen Genauigkeit.

## whisper.cpp installieren

Whisper.cpp lebt unter [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp). Bau-Rezept (Host, nicht Container):

```sh
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
make -j
bash ./models/download-ggml-model.sh base.en
sudo install -m 0755 main /usr/local/bin/whisper
sudo install -m 0644 models/ggml-base.en.bin /usr/local/share/whisper/ggml-base.en.bin
```

Der Binary-Name nach `install` ist `whisper`; rousseaus Standard-Binary-Lookup erwartet diesen Namen.

## In der Konfiguration aktivieren

```yaml
whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
  voice:
    enabled: true
    binary: whisper                                # optional; Standard ist "whisper"
    model_path: /usr/local/share/whisper/ggml-base.en.bin
    language: en                                   # optional; leer bedeutet Auto-Erkennung
    extra_args: []                                 # vor den Eingabedateinamen angehängt
```

Jedes Feld in `VoiceConfig` (`internal/config/config.go`):

| Feld | Typ | Standardwert | Hinweise |
|---|---|---|---|
| `enabled` | bool | `false` | Standardmäßig aus. |
| `binary` | string | `whisper` | Die aufzurufende CLI. Kann `whisper-cli`, `whisper-cpp` usw. sein. |
| `model` | string | — | An `--model` übergeben (z. B. `base.en`, `small`, `medium`). Whispers Standardauflösung greift. |
| `model_path` | string | — | Expliziter `.bin`-Pfad. **Hat Vorrang vor `model`.** |
| `language` | string | — | An `--language` übergeben. Leer bedeutet Auto-Erkennung (langsamer). |
| `extra_args` | []string | — | Vor dem Eingabedateinamen angehängt. |

## Was der Daemon bei jeder Sprachnachricht tut

1. WhatsApp liefert eine Audio-Nachricht (Opus / OGG / MP3 / M4A / AAC / WAV – die Erweiterung wird aus dem MIME-Typ abgeleitet).
2. Rousseau schreibt die Nutzlast in eine Temp-Datei: `/tmp/rousseau-whisper-XXXX/input.<ext>` mit Berechtigung `0o600`.
3. Ruft auf:
   ```
   whisper --output-txt --output-file /tmp/rousseau-whisper-XXXX/output [--model <path>] [--language <lang>] <extra_args...> <input.ext>
   ```
4. Liest `/tmp/rousseau-whisper-XXXX/output.txt` (fällt auf `<input>.txt` zurück für whisper.cpp-Varianten, die neben die Eingabe schreiben).
5. Speist den transkribierten Text als Benutzer-Turn in die Agent-Schleife.
6. Das Temp-Verzeichnis wird mit `os.RemoveAll` (verzögert) aufgeräumt.

## Verifikation mit `rousseau doctor`

```sh
rousseau doctor
```

Achten Sie auf:

```
✔ whatsapp.voice.binary     /usr/local/bin/whisper
```

oder wenn deaktiviert:

```
· whatsapp.voice           disabled
```

Ein `fail` bei `whatsapp.voice.binary` bedeutet `enabled: true`, aber die CLI ist nicht im `$PATH` des Daemons. Reparieren Sie die Installation oder schalten Sie es aus.

## End-to-End testen

1. Sprache in der Konfiguration aktivieren, `rousseau whatsapp` neu starten.
2. Nehmen Sie vom Telefon eine kurze Sprachnachricht auf ("was macht die Datei main.go?") und senden Sie sie.
3. Beobachten Sie das Daemon-Log:
   ```
   whatsapp.voice_enabled binary=whisper model=/usr/local/share/whisper/ggml-base.en.bin
   ```
4. Der Daemon antwortet mit einer Textantwort auf die transkribierte Frage.

## Latenz-Hinweise

Whisper ist standardmäßig CPU-gebunden. Ungefähre Latenzen für eine 10-Sekunden-Sprachnachricht auf einem modernen Laptop:

| Modell | Ungefähre CPU-Latenz |
|---|---|
| `tiny.en` | ~1s |
| `base.en` | ~3s |
| `small.en` | ~8s |
| `medium.en` | ~25s |

Wenn Sie whisper.cpp mit `WHISPER_COREML=1` (macOS) oder `WHISPER_CUBLAS=1` (Linux + NVIDIA) bauen, kann die Transkription 2–10x schneller sein. Rousseau ist das egal – es ruft nur die Shell auf.

## Container-Vorbehalte

Das rousseau-Container-Image (`docker/Dockerfile`) liefert `whisper.cpp` **nicht** aus. Wenn Sie den Sprachmodus im Container wollen, erweitern Sie das Image:

```dockerfile
# Über das Referenz-Dockerfile hinzufügen
RUN apk add --no-cache build-base git && \
    git clone https://github.com/ggerganov/whisper.cpp /tmp/whisper && \
    make -C /tmp/whisper -j && \
    mkdir -p /usr/local/share/whisper && \
    /tmp/whisper/models/download-ggml-model.sh base.en /usr/local/share/whisper && \
    install -m 0755 /tmp/whisper/main /usr/local/bin/whisper && \
    rm -rf /tmp/whisper
```

Oder binden Sie `whisper` und das Modell vom Host in die Quadlet-Unit ein.

## An slog gemeldete Fehler

| Ereignis | Bedeutung |
|---|---|
| `whisper: empty audio payload` | Der Transport lieferte eine Audio-Nachricht mit null Byte. Übersprungen. |
| `whisper: temp dir: <err>` | `/tmp` ist nicht beschreibbar. Prüfen Sie den `Tmpfs=/tmp:rw`-Mount des Containers. |
| `whisper: write audio: <err>` | Disk voll oder Berechtigung verweigert. |
| `whisper: run <binary>: <err>: <stderr excerpt>` | Die CLI endete mit einem Wert ungleich null. Auszug ist auf 400 Zeichen gekürzt. |
| `whisper: read transcript: <err>` | Whisper lief, produzierte aber nicht die erwartete `.txt`-Datei. Oft eine whisper.cpp-Variante, die an einen anderen Pfad schreibt. |

## Datenschutz-Hinweise

Die Transkription läuft **vollständig auf dem Host**. Audio verlässt den Daemon nie. Wenn Sie die CLI durch einen gehosteten Transkriptionsdienst ersetzen (außerhalb des Rahmens des ausgelieferten Codes), übernehmen Sie den Datenfluss dieses Anbieters – verifizieren Sie gegen Ihre eigene [Datenschutz-Haltung](/de/privacy/).

## Weiter

- [WhatsApp-Transport](/de/transports/whatsapp/) — die Transport-Referenz.
- [Konfiguration](/de/configuration/) — jedes Feld in `internal/config/config.go`.
- [Bereitstellung](/de/deployment/) — wie whisper in den Container gebunden wird.
