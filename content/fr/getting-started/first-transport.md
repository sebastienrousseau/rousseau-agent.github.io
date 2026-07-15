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
description: "End-to-end walkthrough for wiring your first chat transport. Uses WhatsApp as the canonical example: pair, allowlist, send a test message, verify the reply."
keywords: "first transport, whatsapp, pairing, allowlist, e2e walkthrough, test message"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/getting-started/first-transport/"
subtitle: "End-to-end WhatsApp walkthrough: pair, allowlist, verify."
tags: "first-transport, whatsapp, walkthrough"
title: "Votre premier transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "first transport, whatsapp, pairing, allowlist, e2e walkthrough, test message"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Votre premier transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 25
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/first-transport/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/first-transport/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Votre premier transport"
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
twitter_description: "End-to-end walkthrough for wiring your first chat transport. Uses WhatsApp as the canonical example: pair, allowlist, send a test message, verify the reply."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Votre premier transport"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>Comment appairer un transport de chat au daemon rousseau, ajouter à l'allowlist le JID ou user ID qui le pilote, envoyer un premier message de test et vérifier la réponse. WhatsApp sert de parcours canonique parce que l'appairage y est le plus exigeant ; les onglets ci-dessous présentent les parcours équivalents pour Slack et Discord.</p></aside>

## Choisir votre premier transport

Chaque transport est un adaptateur mince derrière la même interface `transport.Transport` — l'allowlist, le routage de session et la livraison cron sont identiques partout. Les différences sont l'UX d'appairage et le format d'identifiant par transport (JID, user ID, room ID). Choisissez celui que vous pouvez appairer le plus vite :

<div class="tabs" data-tabs="first-transport">
  <div class="tab-list" role="tablist" aria-label="First transport">
    <button role="tab" aria-selected="true">WhatsApp</button>
    <button role="tab" aria-selected="false">Slack</button>
    <button role="tab" aria-selected="false">Discord</button>
    <button role="tab" aria-selected="false">Telegram</button>
    <button role="tab" aria-selected="false">Signal</button>
  </div>
  <div class="tab-panel" role="tabpanel">

WhatsApp est la référence — le plus difficile à appairer, le plus simple à tester (vous avez déjà l'app sur votre téléphone).

**Prérequis :** votre téléphone avec WhatsApp, votre JID E.164 (ex. `447900123456@s.whatsapp.net`).

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Scannez le QR depuis **WhatsApp &gt; Réglages &gt; Appareils liés &gt; Lier un appareil**. Envoyez-vous `hello` ; rousseau répond via WhatsApp. Voir plus bas pour le parcours complet.

<aside class="admonition" data-type="warning"><span class="admonition-title">Protocole non officiel</span><p>Le support WhatsApp utilise <code>whatsmeow</code> — un client rétro-ingénieré. Meta bannit occasionnellement les numéros exécutant des clients non officiels. Ne l'utilisez pas sur un numéro dont vous dépendez.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Prérequis :** admin d'un workspace Slack, une app créée sur [api.slack.com/apps](https://api.slack.com/apps), Socket Mode activé.

1. Créez une app Slack, activez **Socket Mode** sous <em>Settings &gt; Socket Mode</em>.
2. Créez un **App-Level Token** avec `connections:write` — c'est le jeton `xapp-…`.
3. Sous <em>OAuth &amp; Permissions</em>, ajoutez les bot scopes `chat:write`, `im:history`, `im:read`, `im:write`, `mpim:history`, `mpim:read`. Installez sur le workspace pour obtenir le jeton bot `xoxb-…`.
4. Sous <em>Event Subscriptions</em>, abonnez-vous à `message.im` (DM) et à tout événement de canal souhaité.

```sh
rousseau slack --app-token xapp-... --bot-token xoxb-... --allow U01234567
```

Envoyez un DM au bot dans Slack ; rousseau répond dans le même DM. Voir [Transports : Slack](/fr/transports/slack/) pour le parcours complet, avec justification des scopes OAuth.

<aside class="admonition" data-type="tip"><span class="admonition-title">Pas de HTTP public</span><p>Socket Mode signifie que le daemon se connecte en sortant vers le WebSocket de Slack. Aucun webhook public, ngrok ou ingress requis.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Prérequis :** une application Discord sur [discord.com/developers/applications](https://discord.com/developers/applications), un utilisateur bot, l'intent **Message Content Intent** activé sous <em>Bot</em>.

1. Créez une application, ajoutez un bot, copiez le jeton de bot.
2. Sous <em>Bot &gt; Privileged Gateway Intents</em>, activez **Message Content Intent**. Sans cela, le texte des messages arrive vide.
3. Invitez le bot via <em>OAuth2 &gt; URL Generator</em> — scope `bot`, permissions `Send Messages`, `Read Message History`.

```sh
rousseau discord --token <bot-token> --allow 234567890123456789
```

Envoyez un DM au bot ; rousseau répond. Voir [Transports : Discord](/fr/transports/discord/) pour un plongée sur permissions et intents.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Prérequis :** un bot Telegram depuis [@BotFather](https://t.me/BotFather).

1. Messagez `@BotFather`, `/newbot`, suivez les prompts. Copiez le jeton.
2. Parlez au bot au moins une fois pour que Telegram crée un chat.

```sh
rousseau telegram --token 1234567890:AA... --allow 987654321
```

La valeur `--allow` est l'ID utilisateur numérique Telegram (pas le nom d'utilisateur). Récupérez-le en messageant [@userinfobot](https://t.me/userinfobot).

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Prérequis :** `signal-cli` installé et lié à un compte Signal. Voir la [documentation signal-cli](https://github.com/AsamK/signal-cli) pour le flux d'appairage.

```sh
rousseau signal --account +447900123456 --allow +447900654321
```

Rousseau lance `signal-cli` en sous-processus (voir `internal/cli/signal.go`) et communique avec lui via JSON-RPC. Voir [Transports : Signal](/fr/transports/signal/).

  </div>
</div>

## Pourquoi le parcours WhatsApp

La suite de cette page utilise WhatsApp comme exemple canonique — si vous saisissez le pattern ici, chaque autre transport en est une variation (mettre un ID stable en allowlist, effectuer une UX d'appairage une fois, envoyer un test, vérifier la réponse). Sautez à la page de transport concerné si vous avez déjà un jeton en main :

- [Slack](/fr/transports/slack/) — jetons Socket Mode et abonnements d'événements.
- [Discord](/fr/transports/discord/) — jeton de bot, intents, entiers de permission.
- [Telegram](/fr/transports/telegram/) — jeton BotFather.
- [Signal](/fr/transports/signal/) — sous-processus signal-cli.
- [Matrix](/fr/transports/matrix/) — URL du homeserver + access token.

## Prérequis

- `rousseau` sur `$PATH` (voir [Installation](/fr/getting-started/installation/)).
- Un provider fonctionnel — `claudecli` qui hérite de l'auth Claude Code est le défaut ; tout le reste requiert que sa configuration soit renseignée au préalable ([Configuration](/fr/configuration/)).
- Votre téléphone avec WhatsApp installé. Votre JID téléphonique E.164 (ex. `447900123456@s.whatsapp.net`).

## Étape 1 — Choisir le JID qui pilotera le daemon

Rousseau utilise une allowlist pour restreindre la prise en charge des messages entrants à un ensemble fixé de JID. Tout autre expéditeur est silencieusement rejeté. C'est un mécanisme porteur : sans allowlist, quiconque connaît le numéro peut piloter l'agent.

Votre JID E.164 est votre numéro de téléphone, chiffres uniquement, suivi de `@s.whatsapp.net` :

```
447900123456@s.whatsapp.net
```

Les JID de groupes se terminent par `@g.us` ; le daemon les supporte aussi, mais commencez par un JID personnel.

## Étape 2 — Premier lancement et appairage

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Au premier lancement, un QR code s'affiche sur stdout. Ouvrez WhatsApp sur votre téléphone, allez dans **Réglages → Appareils liés → Lier un appareil**, et scannez le QR.

Le daemon affiche quelque chose comme :

```
whatsapp.starting store=file:/home/you/.local/share/rousseau/whatsapp.db?_pragma=... allowlist=1
```

Une fois scanné, whatsmeow persiste les credentials d'appareil dans `whatsapp.db`. Les lancements suivants se connectent silencieusement — plus de QR.

## Étape 3 — Envoyer un message de test

Depuis votre téléphone, envoyez-vous `hello`. Le daemon journalise l'événement entrant, dispatche à l'agent et renvoie la réponse via WhatsApp avec l'en-tête configuré :

```
💎 *Rousseau Agent*

Hello — what would you like to work on?
```

L'en-tête de réponse se configure via `whatsapp.reply_header`. Mettez-le à un espace unique pour désactiver le préfixe.

## Étape 4 — Créer un `config.yaml` pour se passer des longs flags

Créez `~/.config/rousseau/config.yaml` :

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: bypassPermissions

whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
```

Désormais `rousseau whatsapp --allow 447900123456@s.whatsapp.net` récupère l'en-tête automatiquement. Chaque transport lit sa section depuis le même fichier — voir [Configuration](/fr/configuration/) pour la liste complète.

`bypassPermissions` est le défaut pour les daemons non supervisés parce qu'il n'y a personne à l'autre bout du terminal pour approuver les appels d'outils de manière interactive. **Mettez en place une politique d'approbation** ([Guide utilisateur : Politiques d'approbation](/fr/user-guide/approval-policies/)) avant de pointer le daemon vers quoi que ce soit d'important.

## Étape 5 — Confirmer de bout en bout

Envoyez une question de code depuis votre téléphone :

```
Read the file at /workspace/README.md and summarise it in 3 bullets.
```

Le daemon exécute un appel d'outil `read`, transmet le fichier au modèle et vous répond avec la synthèse. Vous venez de fermer la boucle :

- Téléphone → WhatsApp → WebSocket whatsmeow
- rousseau-agent → boucle d'agent → appel d'outil → appel provider
- réponse → whatsmeow → WhatsApp → téléphone

Rien n'a franchi votre périmètre réseau à l'exception de l'appel provider — et si le provider était `claudecli` sur votre installation locale Claude Code, même pas cela.

## Vérifier avec `rousseau doctor`

```sh
rousseau doctor
```

Chaque contrôle du chemin WhatsApp est couvert :

- `provider.claudecli.binary`, `provider.claudecli.version` — le chemin LLM.
- `state.path`, `state.db_size`, `state.sessions` — magasin de sessions SQLite.
- `whatsapp.store`, `whatsapp.paired` — credentials d'appareil.
- `whatsapp.voice` — posture de transcription des notes vocales.

Une ligne `fail` est un arrêt franc ; une ligne `warn` mérite d'être investiguée avant déploiement.

## Dépannage

### Le QR s'affiche mais le téléphone le rejette

Trois causes fréquentes. Premièrement, un appairage partiellement abouti a laissé `whatsapp.db` dans un état inutilisable par whatsmeow — supprimez `~/.local/share/rousseau/whatsapp.db` et rescannez. Deuxièmement, l'horloge est décalée de plus de 30 secondes (fréquent dans les conteneurs sans client NTP fonctionnel) — la poignée de main WhatsApp est sensible au temps. Troisièmement, une version ancienne de `whatsmeow` peut avoir raté une mise à jour de protocole Meta ; mettez rousseau à jour.

### J'ai envoyé un message mais le daemon logue `router.transport.rejected`

Votre JID ne correspond pas à l'allowlist. La valeur passée à `--allow` doit être le JID de l'expéditeur exactement tel que WhatsApp le rapporte (`447900123456@s.whatsapp.net`, sans `+`, sans espace). Notez que le test en self-chat fonctionne car rousseau substitue le JID du compte au hash LID de confidentialité (voir `internal/transport/whatsapp/resolve.go`).

### Aucun QR ne s'affiche et le daemon se termine avec `no rows`

Le store whatsmeow n'a jamais été initialisé. Vérifiez que le répertoire parent (`~/.local/share/rousseau/`) existe et est accessible en écriture. `rousseau doctor` le signale sous `whatsapp.store`.

### Rousseau répond mais la sortie modèle est vide

Vérifiez `provider.claudecli.binary` et `provider.claudecli.version` dans `rousseau doctor`. La cause la plus fréquente d'une réponse vide est une invocation `claudecli` qui retourne `is_error: true` — le daemon logue l'erreur tronquée au niveau `warn`. Basculez sur `anthropic` ou `bedrock` pour isoler le sous-processus.

### Slack/Discord : "invalid_auth" ou "401 Unauthorized"

Pour Slack, `xapp-…` (app token) et `xoxb-…` (bot token) sont différents — les intervertir produit `invalid_auth`. Pour Discord, le jeton affiché sur <em>Bot &gt; Reset Token</em> est one-shot ; si vous l'avez copié une fois et perdu, vous devez le régénérer.

## Pages liées

- [Transports](/fr/transports/) — chaque transport, son protocole wire et son format d'allowlist.
- [Guide utilisateur : CLI](/fr/user-guide/cli/) — chaque commande et chaque flag.
- [Guide utilisateur : Politiques d'approbation](/fr/user-guide/approval-policies/) — le levier de sécurité principal.
- [Déploiement](/fr/deployment/) — passer du `rousseau whatsapp` au premier plan à une unité systemd.
- [Mode vocal](/fr/user-guide/voice-mode/) — transformer les notes vocales WhatsApp en tours d'agent.

## Pour aller plus loin

- `internal/transport/whatsapp/client.go` — connexion, QR, pompe d'événements.
- `internal/transport/whatsapp/resolve.go` — normalisation LID/JID et gestion du self-chat.
- `internal/cli/whatsapp.go` — câblage CLI, DSN du store, sélection du transcripteur.
- `internal/cli/slack.go`, `internal/cli/discord.go` — CLI des transports voisins.
- `internal/transport/router.go` — application de l'allowlist.
