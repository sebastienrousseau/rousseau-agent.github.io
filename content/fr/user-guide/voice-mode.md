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
hreflang: "fr"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "fr"
locale: "fr_FR"
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
permalink: "https://docs.rousseau-agent.dev/fr/user-guide/voice-mode/"
subtitle: "Whisper-backed voice-note transcription for WhatsApp."
tags: "voice, whisper, whatsapp, transcription"
title: "Mode vocal"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "voice notes, whisper.cpp, transcription, whatsapp, opt-in, audio"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Mode vocal"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/voice-mode/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/voice-mode/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Mode vocal"
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
twitter_title: "Mode vocal"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Ce que fait le mode vocal

Quand le transport WhatsApp reçoit une note vocale, rousseau appelle une CLI `whisper.cpp` installée localement pour transcrire l'audio en texte, puis alimente la boucle d'agent avec ce texte comme si l'utilisateur l'avait tapé. La réponse revient sous forme de message texte WhatsApp normal.

Le chemin vit dans `internal/transport/whatsapp/whisper.go`. Tous les autres transports sont texte uniquement aujourd'hui.

**Opt-in.** Le mode vocal est désactivé par défaut, et `whisper.cpp` n'est pas livré avec l'image conteneur de rousseau — vous installez et configurez la CLI vous-même, puis basculez un unique flag de config.

## Prérequis

- Un pont `rousseau whatsapp` fonctionnel ([First transport](/fr/getting-started/first-transport/)).
- La CLI `whisper.cpp` sur le `$PATH` du démon. Noms de binaires courants : `whisper`, `whisper-cli`, `whisper-cpp`.
- Un fichier modèle. `base.en` est un bon point de départ pour les notes en anglais ; les modèles plus grands échangent la latence contre la précision.

## Installer whisper.cpp

Whisper.cpp vit à [ggerganov/whisper.cpp](https://github.com/ggerganov/whisper.cpp). Recette de build (hôte, pas conteneur) :

```sh
git clone https://github.com/ggerganov/whisper.cpp
cd whisper.cpp
make -j
bash ./models/download-ggml-model.sh base.en
sudo install -m 0755 main /usr/local/bin/whisper
sudo install -m 0644 models/ggml-base.en.bin /usr/local/share/whisper/ggml-base.en.bin
```

Le nom du binaire après `install` est `whisper` ; la recherche par défaut de rousseau attend ce nom.

## Activer dans la config

```yaml
whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
  voice:
    enabled: true
    binary: whisper                                # optionnel ; défaut « whisper »
    model_path: /usr/local/share/whisper/ggml-base.en.bin
    language: en                                   # optionnel ; vide → auto-détection
    extra_args: []                                 # ajouté avant le nom du fichier d'entrée
```

Chaque champ dans `VoiceConfig` (`internal/config/config.go`) :

| Champ | Type | Défaut | Notes |
|---|---|---|---|
| `enabled` | bool | `false` | Désactivé par défaut. |
| `binary` | string | `whisper` | La CLI à invoquer. Peut être `whisper-cli`, `whisper-cpp`, etc. |
| `model` | string | — | Passé à `--model` (par ex. `base.en`, `small`, `medium`). La résolution par défaut de whisper s'applique. |
| `model_path` | string | — | Chemin `.bin` explicite. **Prend le pas sur `model`.** |
| `language` | string | — | Passé à `--language`. Vide → auto-détection (plus lent). |
| `extra_args` | []string | — | Ajouté avant le nom du fichier d'entrée. |

## Ce que fait le démon à chaque note vocale

1. WhatsApp délivre un message audio (Opus / OGG / MP3 / M4A / AAC / WAV — l'extension est inférée depuis le mimetype).
2. Rousseau écrit le payload dans un fichier temporaire : `/tmp/rousseau-whisper-XXXX/input.<ext>` avec permission `0o600`.
3. Invoque :
   ```
   whisper --output-txt --output-file /tmp/rousseau-whisper-XXXX/output [--model <path>] [--language <lang>] <extra_args...> <input.ext>
   ```
4. Lit `/tmp/rousseau-whisper-XXXX/output.txt` (bascule sur `<input>.txt` pour les variantes de whisper.cpp qui écrivent à côté de l'entrée).
5. Alimente la boucle d'agent avec le texte transcrit comme tour utilisateur.
6. Le répertoire temporaire est nettoyé avec `os.RemoveAll` (différé).

## Vérifier avec `rousseau doctor`

```sh
rousseau doctor
```

Cherchez :

```
✔ whatsapp.voice.binary     /usr/local/bin/whisper
```

ou quand désactivé :

```
· whatsapp.voice           disabled
```

Un `fail` sur `whatsapp.voice.binary` signifie `enabled: true` mais la CLI n'est pas sur le `$PATH` du démon. Corrigez l'installation ou désactivez-le.

## Test de bout en bout

1. Activez la voix dans la config, redémarrez `rousseau whatsapp`.
2. Depuis votre téléphone, enregistrez une courte note vocale (« what does the file main.go do? ») et envoyez-la.
3. Observez le log du démon :
   ```
   whatsapp.voice_enabled binary=whisper model=/usr/local/share/whisper/ggml-base.en.bin
   ```
4. Le démon répond par une réponse textuelle à la question transcrite.

## Notes sur la latence

Whisper est CPU-bound par défaut. Latences approximatives pour une note vocale de 10 secondes sur un portable moderne :

| Modèle | Latence CPU approx. |
|---|---|
| `tiny.en` | ~1s |
| `base.en` | ~3s |
| `small.en` | ~8s |
| `medium.en` | ~25s |

Si vous compilez whisper.cpp avec `WHISPER_COREML=1` (macOS) ou `WHISPER_CUBLAS=1` (Linux + NVIDIA), la transcription peut être 2 à 10 fois plus rapide. Rousseau s'en moque — il ne fait qu'un appel de sous-processus.

## Précautions conteneur

L'image conteneur rousseau (`docker/Dockerfile`) ne livre **pas** `whisper.cpp`. Si vous voulez le mode vocal dans le conteneur, étendez l'image :

```dockerfile
# À ajouter par-dessus le Dockerfile de référence
RUN apk add --no-cache build-base git && \
    git clone https://github.com/ggerganov/whisper.cpp /tmp/whisper && \
    make -C /tmp/whisper -j && \
    mkdir -p /usr/local/share/whisper && \
    /tmp/whisper/models/download-ggml-model.sh base.en /usr/local/share/whisper && \
    install -m 0755 /tmp/whisper/main /usr/local/bin/whisper && \
    rm -rf /tmp/whisper
```

Ou montez `whisper` et le modèle depuis l'hôte dans l'unité Quadlet.

## Erreurs remontées vers slog

| Événement | Signification |
|---|---|
| `whisper: empty audio payload` | Le transport a délivré un message audio de zéro octet. Sauté. |
| `whisper: temp dir: <err>` | `/tmp` n'est pas accessible en écriture. Vérifiez le montage `Tmpfs=/tmp:rw` du conteneur. |
| `whisper: write audio: <err>` | Disque plein ou permission refusée. |
| `whisper: run <binary>: <err>: <extrait stderr>` | La CLI est sortie non nulle. L'extrait est tronqué à 400 caractères. |
| `whisper: read transcript: <err>` | Whisper s'est exécuté mais n'a pas produit le fichier `.txt` attendu. Souvent une variante de whisper.cpp qui écrit à un autre chemin. |

## Notes de confidentialité

La transcription tourne **entièrement sur l'hôte**. L'audio ne quitte jamais le démon. Si vous remplacez la CLI par un service de transcription hébergé (hors périmètre du code livré), vous prenez à votre charge le flux de données de ce fournisseur — vérifiez contre votre propre [posture de confidentialité](/fr/privacy/).

## Suite

- [Transport WhatsApp](/fr/transports/whatsapp/) — la référence du transport.
- [Configuration](/fr/configuration/) — chaque champ dans `internal/config/config.go`.
- [Deployment](/fr/deployment/) — comment monter whisper dans le conteneur.
