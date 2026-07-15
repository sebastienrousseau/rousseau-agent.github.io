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
description: "Set up rousseau-agent's WhatsApp transport: QR pairing, E.164 allowlist, LID vs phone-JID normalisation, voice-note transcription with whisper.cpp."
keywords: "WhatsApp, whatsmeow, QR pairing, JID, LID, allowlist, voice notes, whisper, transcription"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/transports/whatsapp/"
subtitle: "Whatsmeow-backed WhatsApp bridge with QR pairing."
tags: "transports, WhatsApp"
title: "Transport WhatsApp"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "WhatsApp, whatsmeow, QR pairing, JID, LID, allowlist, voice notes, whisper, transcription"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transport WhatsApp"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 12
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/whatsapp/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/whatsapp/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transport WhatsApp"
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
twitter_description: "Set up rousseau-agent's WhatsApp transport: QR pairing, E.164 allowlist, LID vs phone-JID normalisation, voice-note transcription with whisper.cpp."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transport WhatsApp"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>Comment le transport WhatsApp s'appaire à votre téléphone, les règles de normalisation LID vs JID téléphonique, le flux de transcription des notes vocales, les téléchargements de médias, les motifs d'allowlist par regex, et les modes d'échec qui piègent les nouveaux opérateurs. Lisez <code>internal/transport/whatsapp/client.go</code>, <code>resolve.go</code> et <code>dispatch.go</code> en parallèle de cette page.</p></aside>

## Vue d'ensemble

Le transport WhatsApp (`internal/transport/whatsapp/`) s'appuie sur `go.mau.fi/whatsmeow` — un client WhatsApp Web multi-appareil rétro-ingénieré. Meta le considère comme un client non officiel ; ne l'exécutez pas sur un numéro personnel dont vous dépendez.

Le chiffrement de bout en bout du protocole Signal est préservé (whatsmeow utilise le même protocole que l'app mobile WhatsApp). Le daemon conserve les credentials d'appareil dans un fichier SQLite séparé du magasin de sessions, donc un ré-appairage d'appareil ne touche pas à l'historique des conversations.

<aside class="admonition" data-type="caution"><span class="admonition-title">Protocole non officiel</span><p>Meta bannit occasionnellement les numéros exécutant des clients non officiels. Même en respectant les limites de débit WhatsApp et en vous comportant raisonnablement, un numéro utilisé avec <code>whatsmeow</code> peut être banni sans préavis. Utilisez un numéro dédié, pas un numéro personnel.</p></aside>

## Appairage

Premier lancement :

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Un QR code s'affiche sur stdout via `mdp/qrterminal/v3`. Scannez-le avec l'app mobile WhatsApp (**Réglages → Appareils liés → Lier un appareil**). L'état d'appairage est écrit dans `whatsapp.db` sous le répertoire d'état (typiquement `~/.local/share/rousseau/whatsapp.db`).

Les lancements suivants réutilisent l'appareil appairé silencieusement. Si le QR réapparaît, l'appairage a été révoqué côté téléphone — supprimez `whatsapp.db` et ré-appairez.

## Allowlist

`--allow` restreint la prise en charge des messages entrants. Plusieurs flags s'accumulent :

```sh
rousseau whatsapp \
  --allow 447900123456@s.whatsapp.net \
  --allow 442071234567@s.whatsapp.net
```

La valeur est un **JID** WhatsApp — le numéro de téléphone E.164 (sans `+`) suivi de `@s.whatsapp.net`. Les JID de groupes (`<id>@g.us`) sont également supportés.

Une allowlist vide accepte tous les expéditeurs. Pour un daemon de transport chat, vous voulez toujours au moins une entrée.

## Normalisation LID vs JID téléphonique

WhatsApp utilise deux formats d'identifiants pour un utilisateur :

| Format | Exemple | Signification |
|---|---|---|
| JID téléphonique | `447900123456@s.whatsapp.net` | Numéro E.164, sans `+`, suivi de `@s.whatsapp.net`. Stable dans le temps ; expose le numéro. |
| LID | `1234567890@lid` | Location-Independent ID — chaîne d'apparence aléatoire qui ne révèle pas le numéro. Également stable, mais non directement rattachable à un numéro. |
| Suffixe d'appareil | `447900123456:5@s.whatsapp.net` | Tout JID peut porter un suffixe d'adresse d'appareil (`:N`). WhatsApp indique dans les messages quel appareil précis les a envoyés. |

Le handler entrant de rousseau (`ResolveInbound` dans `internal/transport/whatsapp/resolve.go`) normalise chaque événement vers une forme canonique avant le dispatch :

1. **Retirer le suffixe d'appareil.** `447900:5@s.whatsapp.net` devient `447900@s.whatsapp.net`. Cela permet aux allowlists écrites en JID d'utilisateur nu de matcher quel que soit l'appareil lié qui a envoyé le message.
2. **Substituer le LID par le JID téléphonique du titulaire en self-chat.** Quand le titulaire du compte est l'expéditeur (`IsFromMe=true`), WhatsApp indique l'expéditeur comme le LID du compte (un hash de confidentialité), pas le JID téléphonique. Rousseau substitue le JID propre du compte pour que les opérateurs puissent mettre `<téléphone>@s.whatsapp.net` en allowlist et que les tests self-chat routent correctement.
3. **Rejeter les expéditeurs non parsables.** Les champs `User` ou `Server` vides — découverts par `FuzzResolveInbound` — ne peuvent pas être routés en toute sécurité. Le message est silencieusement ignoré au lieu d'être passé au handler avec un From malformé.

### Piège du self-chat

Quand vous vous envoyez un message dans WhatsApp (pour tester le bot), le champ expéditeur arrive comme votre LID. Si vous avez mis en allowlist votre JID téléphonique, la recherche naïve raterait. La substitution de rousseau — `if evt.Info.IsFromMe && ownID != nil { from = ownID.ToNonAD() }` — corrige cela.

### Prévention des boucles

`IsFromMe=true` se déclenche aussi pour les messages émis par *cet* appareil lié (les réponses sortantes de rousseau qui reviennent en écho). Le transport les rejette quand l'ID d'appareil correspond :

```go
if evt.Info.IsFromMe && ownID != nil && evt.Info.Sender.Device == ownID.Device {
    return Resolved{Skip: SkipOwnDevice}
}
```

Les messages provenant des *autres* appareils liés du compte (ex. le téléphone principal testant « s'envoyer un message ») portent `IsFromMe=true` mais un ID d'appareil différent — ils sont traités normalement.

## Motifs regex pour l'allowlist

Le flag `--allow` prend des chaînes exactes, pas des regex — rousseau effectue une comparaison d'égalité insensible à la casse dans `router.go`. Pour du pattern matching, utilisez le fichier de configuration en mode `pattern` (comme pour les politiques d'approbation) :

```yaml
whatsapp:
  allowlist:
    - "447900123456@s.whatsapp.net"
    - "447900654321@s.whatsapp.net"
```

Pour les groupes (`<hash>@g.us`), ajoutez-les de la même manière. Pour autoriser tout le monde depuis un indicatif pays donné, il faudrait une implémentation `Router.Allow` custom — l'enforcer intégré ne fait pas de prefix matching par conception.

<aside class="admonition" data-type="warning"><span class="admonition-title">Allowlist vide</span><p>Une allowlist vide accepte tous les expéditeurs. N'exécutez pas un transport chat sans allowlist sur un numéro public — quiconque connaît le numéro devient opérateur de votre agent.</p></aside>

## En-tête de réponse

Chaque message sortant est préfixé d'un en-tête pour que l'expéditeur sache à quel bot il parle. Défaut :

```
💎 *Rousseau Agent*

<message body>
```

WhatsApp rend `*text*` en gras. Surchargez en config :

```yaml
whatsapp:
  reply_header: "🤖 *Coding bot*\n\n"
```

Positionnez à un espace unique `" "` pour désactiver totalement le préfixe.

## Transcription des notes vocales

Les notes vocales entrantes sont transcrites via `whisper.cpp` quand l'opérateur l'active. Désactivé par défaut car cela requiert la CLI `whisper` installée.

```yaml
whatsapp:
  voice:
    enabled: true
    binary: whisper
    model: base.en
    language: en
    extra_args:
      - --threads
      - "4"
```

| Champ | Effet |
|---|---|
| `enabled` | Bascule. Désactivé, les messages audio sont loggés et ignorés. |
| `binary` | Exécutable CLI Whisper. Vide, revient à `whisper`. |
| `model` | Transmis à `--model` (`base.en`, `small`, `medium`). |
| `model_path` | Chemin `.bin` explicite. Prioritaire sur `model`. |
| `language` | Transmis à `--language`. Vide, détection automatique. |
| `extra_args` | Ajouté à chaque invocation. |

Le texte transcrit est remis à l'agent comme si l'utilisateur l'avait tapé.

## Déploiement conteneur

L'unité Podman Quadlet de référence (`docker/rousseau-agent.container`) monte le répertoire d'état en lecture-écriture pour que l'appairage survive aux redémarrages :

```
Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
```

`Network=pasta` donne au conteneur une pile rootless en egress uniquement. Whatsmeow ne requiert aucune capability élevée ; `DropCapability=all` est sûr.

## Flux de transcription des notes vocales

Quand une note vocale arrive, le résolveur standard retourne `SkipEmptyText` (pas de contenu texte). `Dispatch` détecte spécifiquement ce cas pour les messages audio et — si un `Transcriber` est configuré — suit ce chemin :

```
Inbound audio message
  │
  ├── Downloader.Download(ctx, audioMsg)
  │     • bytes []byte, mimetype string, err error
  │     • Logs whatsapp.audio_downloaded on success
  │
  ├── Transcriber.Transcribe(ctx, audio, mimetype)
  │     • Returns plain-text transcription
  │     • Logs whatsapp.transcribed with duration
  │
  └── Re-enter handleTextMessage with the transcription as `Body`
```

Si aucun transcripteur n'est configuré, le daemon logue `whatsapp.audio_ignored reason=transcriber_not_configured` et jette le message. Les notes vocales ne déclenchent jamais de réponse « silence » — un entrant vide produit un sortant vide.

## Téléchargements de médias

L'interface `Downloader` est délibérément minimale :

```go
type Downloader interface {
    Download(ctx context.Context, msg DownloadableAudio) (bytes []byte, mimetype string, err error)
}
```

Seul le téléchargement audio est actuellement câblé. Les téléchargements image et vidéo figurent sur la roadmap — ils arrivent en `waProto.ImageMessage` / `VideoMessage` et nécessiteraient une interface `DownloadableMedia` correspondante. Suivez le plan dans [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md).

## Indicateurs de saisie

Le handler encadre chaque réponse par des appels `SendPresence(Composing, Paused)` pour que l'expéditeur voie l'indicateur « …est en train d'écrire » pendant que le modèle réfléchit. Les deux appels ont un timeout de 5 secondes et sont best-effort — un échec de présence ne bloque jamais la réponse elle-même.

## Modes d'échec

| Symptôme | Correctif |
|---|---|
| Le QR se réaffiche à chaque redémarrage | L'appairage a été révoqué côté téléphone ; supprimez `whatsapp.db` et ré-appairez. |
| Boucle de reconnexion WhatsApp | Vérifiez le décalage d'horloge contre `pool.ntp.org` — la poignée de main whatsmeow est sensible au temps. |
| Messages entrants ignorés | Vérifiez que l'expéditeur est dans la liste `--allow` ; cherchez `router.transport.rejected` dans les logs. |
| Meta bannit le numéro | N'utilisez pas un numéro personnel. Le protocole est non officiel. |
| Le « hello » de self-chat n'est pas routé | Le self-chat utilise le LID ; rousseau substitue au JID téléphonique pour matcher l'allowlist. Vérifiez que `ownID` est initialisé — le daemon logue `whatsapp.connected` quand c'est le cas. |
| Notes vocales silencieusement jetées | Soit `whatsapp.voice.enabled: false`, soit le binaire `whisper` est manquant. Ligne de log : `whatsapp.audio_ignored`. |
| Chaque réponse me revient deux fois | La prévention de boucle est désactivée. Assurez-vous d'utiliser un build récent ; le correctif a atterri dans `ResolveInbound` tôt dans le déploiement multi-appareil de whatsmeow. |

## Dépannage

### Le QR s'affiche mais l'app téléphone le rejette

Trois causes fréquentes : (1) un appairage partiellement abouti a laissé `whatsapp.db` dans un état inutilisable par whatsmeow — supprimez le fichier et rescannez ; (2) l'horloge est décalée de plus de 30 secondes (fréquent dans les conteneurs sans NTP) — vérifiez avec `timedatectl status` ; (3) une version ancienne de `whatsmeow` peut avoir raté une mise à jour de protocole Meta.

### `whatsapp.connected` puis `whatsapp.disconnected` en boucle

Décalage d'horloge, ou Meta a invalidé l'appairage. Cherchez les événements `whatsapp.logged_out` dans les logs — c'est le signal définitif.

### Les notes vocales arrivent mais ne sont jamais transcrites

Le binaire de transcription n'est pas résolvable. Vérifiez `whatsapp.voice.binary` et `whatsapp.voice.model_path` — les deux doivent pointer vers de vrais fichiers (ou `binary` doit être sur `PATH`).

### La regex d'allowlist ne matche pas

L'allowlist de rousseau est en chaîne exacte, pas en regex. Pour matcher une plage d'expéditeurs, listez chaque entrée explicitement ou ajoutez un router custom.

### L'en-tête de réponse s'affiche avec des `*` littéraux

Le client du destinataire ne rend pas le Markdown WhatsApp. Problème de rendu côté client ; utilisez du texte brut si vos destinataires sont sur des clients anciens.

## Pages liées

- [Prise en main : Premier transport](/fr/getting-started/first-transport/) — parcours de bout en bout.
- [Guide utilisateur : Mode vocal](/fr/user-guide/voice-mode/) — plongée sur les notes vocales.
- [Configuration](/fr/configuration/) — le bloc de config `whatsapp`.
- [Transports](/fr/transports/) — les huit autres transports.
- [Déploiement](/fr/deployment/) — exécuter WhatsApp dans un conteneur Podman.

## Pour aller plus loin

- `internal/transport/whatsapp/client.go` — connexion, appairage QR, pompe d'événements.
- `internal/transport/whatsapp/resolve.go` — normalisation LID/JID et gestion du self-chat.
- `internal/transport/whatsapp/dispatch.go` — dispatch des messages entrants avec branchement notes vocales.
- `internal/transport/whatsapp/whisper.go` — transcripteur whisper-cpp de référence.
- `internal/cli/whatsapp.go` — câblage CLI, DSN du store, sélection du transcripteur.
