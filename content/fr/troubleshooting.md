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
description: "Troubleshoot rousseau-agent: WhatsApp QR won't scan, reconnect loops, cosign verify failures, SELinux bind-mount errors, cron not firing, approval policy denying everything."
keywords: "troubleshooting, WhatsApp QR, reconnect loop, cosign verify, SELinux, bind mount, cron, approval policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/troubleshooting/"
subtitle: "Modes d'échec courants et comment y remédier."
tags: "troubleshooting, support"
title: "Dépannage"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "troubleshooting, WhatsApp QR, reconnect loop, cosign verify, SELinux, bind mount, cron, approval policy"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Dépannage"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "support"
order: 27
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/troubleshooting/index.html"
item_link: "https://docs.rousseau-agent.dev/troubleshooting/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Dépannage"
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
twitter_title: "Dépannage"
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

## WhatsApp : le QR ne se scanne pas

Symptôme : `rousseau whatsapp` affiche un QR que l'application refuse, ou la boîte de dialogue d'appairage indique « Cet appareil n'est pas jumelé à WhatsApp ».

Correctifs :

1. **Reconstruire le conteneur.** Sur une image ancienne, `whatsmeow` peut avoir livré une mise à jour de protocole. Reconstruisez :
   ```sh
   podman build -t rousseau-agent:local -f docker/Dockerfile .
   systemctl --user restart rousseau-agent.service
   ```
2. **Supprimer `whatsapp.db`.** Un appairage partiellement abouti laisse la base dans un état inutilisable par whatsmeow. Supprimez-la et ré-appairez :
   ```sh
   rm ~/.local/share/rousseau/whatsapp.db
   ```
3. **Vérifier le décalage d'horloge.** La poignée de main WhatsApp est sensible au temps. Un écart de plus de 30 secondes fait échouer l'appairage silencieusement.
   ```sh
   timedatectl status
   ```

## Boucle de reconnexion WhatsApp

Symptôme : les logs montrent des `whatsapp.connected` répétés suivis de `whatsapp.disconnected` toutes les quelques secondes.

Correctifs :

1. **Décalage d'horloge.** Même correctif que ci-dessus.
2. **Allowlist mal configurée.** Chaque message entrant est rejeté comme non autorisé ; certains serveurs ferment le socket après trop de rejets silencieux. Ajoutez les JID corrects avec `--allow`.
3. **Bannissement côté Meta.** Si l'app mobile WhatsApp affiche « Cet appareil a été déconnecté », Meta a invalidé l'appairage. Ré-appairez depuis un QR neuf. Si cela se reproduit sur le même numéro, cessez d'utiliser ce numéro.

## cosign verify-blob échoue

Symptôme :

```
Error: no matching signatures
```

Correctifs :

1. **Mauvaise regex certificate-identity.** La regex doit correspondre au dépôt GitHub qui a signé la release. Pour les releases rousseau-agent, la valeur correcte est :
   ```
   --certificate-identity-regexp 'sebastienrousseau/rousseau-agent'
   ```
   N'utilisez pas `.*` — cela accepterait une signature cosign de n'importe quel dépôt.
2. **Mauvais émetteur OIDC.** Les signatures cosign de GitHub Actions sont émises depuis `https://token.actions.githubusercontent.com`. D'autres fournisseurs CI (GitLab, Buildkite) émettent depuis d'autres URL.
3. **Mauvais fichier de signature.** Vérifiez que `<version>_checksums.txt.sig` correspond au `_checksums.txt` que vous vérifiez (et non à une copie périmée d'une autre release).
4. **Racine de confiance Sigstore modifiée.** Rafraîchissez avec `cosign initialize` ; la racine de confiance tourne lentement.

## Le bind mount du conteneur échoue

Symptôme : `podman play kube` ou `systemctl --user start rousseau-agent.service` échoue avec `permission denied` sur un bind mount.

Correctifs :

1. **Label SELinux.** Chaque ligne de volume doit se terminer par `:Z` (ou `:z` en partagé) pour que Podman applique le bon label SELinux :
   ```
   Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
   ```
   `:Z` (majuscule) est le label privé — adapté aux montages mono-conteneur. `:z` (minuscule) partage le label entre plusieurs conteneurs.
2. **Mapping `keep-id`.** Sans `UserNS=keep-id`, l'UID 1000 du conteneur est remappé dans la plage subuid de l'hôte et ne peut pas écrire dans les fichiers appartenant à l'hôte. Assurez-vous que le Quadlet contient :
   ```
   UserNS=keep-id
   ```
3. **Répertoire manquant.** Podman ne crée pas automatiquement les sources de bind mount. Créez d'abord le répertoire :
   ```sh
   mkdir -p ~/.local/share/rousseau
   ```

## Le job cron ne se déclenche pas

Symptôme : `rousseau cron list` liste le job mais rien ne se passe à l'heure prévue.

Correctifs :

1. **Vérifier le statut.** `rousseau status` rapporte l'activité du scheduler. S'il n'est pas actif, le daemon qui l'héberge n'est pas actif.
2. **Fuseau horaire.** Les planifications utilisent le fuseau local du serveur. Confirmez avec `timedatectl`. Positionnez `TZ=UTC` dans le Quadlet pour une planification déterministe indépendamment du fuseau hôte.
3. **Délai PollInterval.** Les nouveaux jobs deviennent actifs sous `PollInterval` (60 s par défaut). Patientez une minute.
4. **Échec de livraison.** Le job s'est déclenché mais la livraison a échoué. Cherchez `cron.delivery_failed` dans les logs ; le format cible est spécifique au transport (voir [/cron/](/fr/cron/)).

## La politique d'approbation refuse tout

Symptôme : chaque appel d'outil est refusé avec « denied by pattern policy » et le modèle ne peut plus avancer.

Correctifs :

1. **Règle allow manquante.** En mode `pattern` avec `default: deny`, chaque appel d'outil requiert une règle allow correspondante. Ajoutez-en une pour les outils à autoriser :
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
2. **Deny l'emporte sur allow.** Une règle `deny` gagne toujours contre une règle `allow` pour le même outil. Vérifiez votre liste deny pour des correspondances trop larges.
3. **Relever le défaut.** Pour des sessions supervisées, `default: allow` avec des règles deny resserrées est souvent plus praticable :
   ```yaml
   agent:
     approver:
       mode: pattern
       default: allow
       deny:
         - {tool: bash, match: "rm -rf|sudo"}
   ```

## Le fournisseur retourne 401

Symptôme : l'agent échoue avec `provider: unauthorized`.

Correctifs :

1. **Mauvaise clé API.** Pour le fournisseur Anthropic direct, vérifiez que `ANTHROPIC_API_KEY` est exporté ou défini dans `~/.config/rousseau/config.yaml`.
2. **Mauvaise chaîne d'authentification.** Pour Bedrock, exécutez `aws sts get-caller-identity` depuis le conteneur pour vérifier quel principal le SDK résout.
3. **Compte de service Vertex.** Pour le fournisseur Vertex, confirmez que le fichier pointé par `vertex.credentials_file` est lisible dans le conteneur et accorde `roles/aiplatform.user`.

## Le fournisseur retourne 429

Symptôme : l'agent échoue avec `provider: rate limited`.

Correctifs :

1. **Réduire `max_tokens`.** Des complétions plus courtes libèrent la fenêtre de rate plus vite.
2. **Activer la compression.** Les longs transcripts alourdissent la pression en tokens d'entrée ; `agent.compression.enabled: true` condense les messages anciens.
3. **Attendre.** rousseau ne retente pas dans `Complete` ; l'appelant (transport chat, scheduler cron ou `rousseau chat`) décide s'il retente et comment.

## `rousseau chat` n'affiche qu'un TUI vide

Symptôme : le TUI Bubble Tea s'ouvre mais sans curseur ni viewport.

Correctifs :

1. **Environnement TERM.** rousseau exige un terminal capable ANSI. Positionnez `TERM=xterm-256color` (ou équivalent).
2. **stdin encapsulé.** Une exécution sous `nohup` ou dans un pipe supprime le terminal. Lancez en interactif.

## Slack : `invalid_auth` au démarrage

Symptôme : `slack.starting` immédiatement suivi de `invalid_auth`.

Correctifs :

1. **Jetons intervertis.** Rousseau exige les deux : `xapp-…` (app-level, `--app-token`) et `xoxb-…` (bot, `--bot-token`). Passer un app token là où un bot token est attendu produit cette erreur.
2. **App non installée.** Après la création des scopes, cliquez sur *Install to Workspace* dans la configuration de l'app Slack. Les jetons ne sont valides qu'après installation.
3. **Jeton régénéré.** Les jetons Slack peuvent être régénérés manuellement par un admin. Après régénération, tous les daemons qui l'utilisent doivent redémarrer avec la nouvelle valeur.

## Slack : le bot répond à ses propres messages (boucle)

Symptôme : le message sortant de rousseau déclenche un événement entrant auquel le daemon répond, provoquant une avalanche de réponses.

Correctifs :

1. **Renseignez `bot_user_id`.** Le flag `--bot-user-id` (ou `slack.bot_user_id` en config) indique au daemon d'ignorer les messages émis par cet ID utilisateur. Récupérez-le via `curl -H "Authorization: Bearer xoxb-..." https://slack.com/api/auth.test`.
2. **Vérifiez le filtre d'événements.** Le transport ignore les sous-types `bot_message` par défaut, mais une app Slack mal configurée peut contourner cela.

## Discord : le texte des messages arrive vide

Symptôme : `discord.incoming from=... body=` — les messages passent mais sans contenu.

Correctifs :

1. **Message Content Intent désactivé.** Dans le Discord Developer Portal sous <em>Bot &gt; Privileged Gateway Intents</em>, activez **Message Content Intent**. Sans cela, Discord retire le texte des messages des événements Gateway.
2. **Scopes manquants.** L'URL d'invitation doit avoir accordé au bot `Read Message History` et `Send Messages` pour le canal/DM utilisé.

## Discord : `disallowed intents`

Symptôme : erreurs de démarrage `Discord returned 4014 disallowed intents`.

Correctifs :

1. **Intents privilégiés.** Activez *Message Content Intent* (voir plus haut). Même sans demande, Discord retourne 4014 s'il est demandé sans approbation.
2. **Vérification.** Les bots présents dans 100+ serveurs doivent être vérifiés par Discord pour utiliser les intents privilégiés. Suivez le parcours du developer portal.

## Telegram : `unauthorized`

Symptôme : `telegram.starting` suivi de `getUpdates: 401`.

Correctifs :

1. **Mauvais jeton.** BotFather retourne le jeton une seule fois — n'incluez pas le point final. Le jeton a la forme `<bot_id>:<secret>`.
2. **Jeton révoqué.** `/revoke` dans BotFather invalide le jeton courant ; obtenez-en un neuf.

## Email : `dial tcp: i/o timeout`

Symptôme : la connexion IMAP ou SMTP n'aboutit jamais.

Correctifs :

1. **Mauvais port.** IMAP est `993` (TLS implicite). La soumission SMTP est `587` (STARTTLS) ou `465` (TLS implicite). Rousseau utilise le TLS implicite dans les deux — les serveurs STARTTLS-uniquement ne sont pas encore supportés. Voir [Transports : Email](/fr/transports/email/) pour la migration.
2. **Egress bloqué.** Les pare-feu d'entreprise bloquent souvent le SMTP sortant. Testez avec `openssl s_client -connect smtp.example.com:465` depuis le conteneur.
3. **Le fournisseur exige un mot de passe applicatif.** Gmail, Fastmail et similaires exigent un mot de passe applicatif (pas votre mot de passe de compte) lorsque la 2FA est activée. Générez-en un depuis les paramètres de sécurité du fournisseur.

## Vertex : `permission denied on resource`

Symptôme : `vertex: HTTP 403 permission denied on resource projects/.../models/claude-sonnet-4-6@…:rawPredict`.

Correctifs :

1. **Rôle manquant.** Accordez `roles/aiplatform.user` au compte de service ou à l'utilisateur qui appelle l'API. Les changements IAM prennent jusqu'à une minute à se propager.
2. **Mauvais projet.** Le `project` en config doit correspondre au projet qui détient le quota. Si la facturation est sur un autre projet, utilisez un quota-project via `gcloud auth application-default set-quota-project`.
3. **Mauvaise région.** Le modèle doit être disponible dans la région demandée — le Vertex Model Garden le liste.

## Bedrock : `You don't have access to the model`

Symptôme : `AccessDeniedException: You don't have access to the model with the specified model ID`.

Correctifs :

1. **Accès modèle non demandé.** Bedrock exige une demande d'accès explicite via la console (*Foundation models &gt; Model access*). Même avec un IAM autorisant `InvokeModel`, cette étape est requise.
2. **Mauvaise région.** La disponibilité des modèles est régionale. Vérifiez dans la console Bedrock.
3. **Mauvaise configuration cross-account.** En cas d'AssumeRole, vérifiez que la politique du rôle cible autorise `bedrock:InvokeModel` sur l'ARN exact du modèle.

## Ollama : `context deadline exceeded`

Symptôme : rousseau expire pendant qu'Ollama génère encore.

Correctifs :

1. **L'inférence CPU est lente.** Un modèle 70B sur CPU de laptop peut prendre plusieurs minutes par tour. Utilisez un modèle plus petit (`llama3.1:8b`) ou un hôte GPU.
2. **Héritage de timeout.** rousseau utilise le timeout HTTP par défaut du SDK. Si vous encapsulez le fournisseur, étendez le timeout à au moins 120 s.

## Notes vocales : transcripteur non configuré

Symptôme : `whatsapp.audio_ignored reason=transcriber_not_configured`.

Correctifs :

1. **Whisper désactivé.** Positionnez `whatsapp.voice.enabled: true` en config et vérifiez que le binaire `whisper` est sur `PATH` (ou renseignez `whatsapp.voice.binary` avec un chemin absolu).
2. **Fichier modèle manquant.** Renseignez `whatsapp.voice.model_path` avec un fichier `.bin` explicite. Les modèles Whisper.cpp se téléchargent à la main — la config pointe simplement là où ils vivent.

## Magasin de session : `database is locked`

Symptôme : l'écrivain WAL bloque ; les requêtes expirent.

Correctifs :

1. **Deux daemons, une BD.** SQLite en WAL autorise des lecteurs concurrents mais un seul écrivain. Si deux processus rousseau ciblent le même `state.path`, l'un bloque. Utilisez des chemins d'état distincts.
2. **`busy_timeout` trop faible.** Le DSN positionne `busy_timeout=15000`. Sous contention soutenue, augmentez-le — mais identifiez d'abord la cause racine.
3. **Fichier WAL périmé.** Un écrivain planté peut laisser `sessions.db-wal` verrouillé. Arrêtez tout, supprimez `sessions.db-wal` et `sessions.db-shm`, redémarrez.

## MCP : Claude Desktop ne voit pas les outils rousseau

Symptôme : rousseau lancé via `command: "rousseau"` dans `claude_desktop_config.json` mais aucun outil n'apparaît.

Correctifs :

1. **Config non sauvegardée.** Claude Desktop recharge à chaud à la sauvegarde ; si vous avez édité le fichier dans une instance en cours, redémarrez-la.
2. **`command` hors PATH.** Claude Desktop lance ses sous-processus depuis son propre environnement ; `/usr/local/bin/rousseau` peut ne pas être visible. Utilisez un chemin absolu.
3. **Bruit stderr.** rousseau écrit des logs structurés sur stderr ; un logger très bavard peut saturer l'hôte. Positionnez `log.level: warn` lors d'une exécution MCP contre un hôte strict.

## Skills : `skill loader: parse: yaml: line X`

Symptôme : rousseau échoue au démarrage sur une erreur de parse YAML.

Correctifs :

1. **Frontmatter mal formé.** Les skills utilisent un frontmatter YAML délimité par `---`. Vérifiez la présence des deux séparateurs et l'absence d'indentation par tabulation.
2. **Deux-points non quotés.** Un deux-points dans une valeur (`description: this: that`) est parsé comme une map imbriquée. Quotez la valeur : `description: "this: that"`.

## `rousseau doctor` rapporte des `warn`

Symptôme : doctor termine mais avec des lignes en orange.

Correctifs :

1. **Lisez le motif.** Chaque ligne warn contient un motif. Fréquents : `whatsapp.paired=false` (jamais appairé), `state.wal_size=large` (checkpoint en retard), `provider.claudecli.model=unset` (défaut claude utilisé).
2. **Les warns ne sont pas des échecs.** Le daemon démarrera ; la ligne signale quelque chose à examiner.

## Kubernetes : pod coincé en `CrashLoopBackOff`

Symptôme : le deployment n'atteint jamais Ready.

Correctifs :

1. **Lisez les logs.** `kubectl logs -p <pod>` affiche le stderr du conteneur précédent. Neuf fois sur dix, c'est une erreur de config ou de credentials.
2. **Volume d'état manquant.** Sans PVC pour `~/.local/share/rousseau`, l'appairage ne survit pas au redémarrage et le daemon peut boucler en tentant de ré-appairer.
3. **IRSA / Workload Identity mal configuré.** Vérifiez que l'annotation du service account correspond à un rôle IAM détenant les permissions du fournisseur. `kubectl exec` dans le pod et exécutez `aws sts get-caller-identity` (Bedrock) ou `gcloud auth print-access-token` (Vertex) pour confirmer.

## Le jeu de règles nftables bloque le trafic sortant du fournisseur

Symptôme : `dial tcp: i/o timeout` au premier appel fournisseur après application d'un jeu de règles egress.

Correctifs :

1. **CIDR ayant tourné.** Les plages IP fournisseurs changent. Utilisez un egress basé DNS via un ipset rafraîchi par cron, ou un proxy egress qui résout au moment de la connexion.
2. **DNS bloqué.** Le jeu de règles egress doit autoriser UDP/53 (ou TCP/53) vers votre résolveur DNS.

## Logs structurés : champs manquants

Symptôme : `whatsapp.incoming` apparaît avec `from` et aucun autre attribut.

Correctifs :

1. **Niveau de log trop haut.** Certains champs ne sont émis qu'en `debug`. Positionnez `log.level: debug` en config.
2. **Parser JSON qui avale des champs.** Une chaîne de filtres qui retire les champs inconnus peut supprimer `elapsed`, `bytes`, etc. Vérifiez contre le stdout brut.

## Pages liées

- [Prise en main : Premier transport](/fr/getting-started/first-transport/) — parcours bout en bout.
- [Fournisseurs](/fr/providers/) — dépannage par fournisseur.
- [Transports](/fr/transports/) — dépannage par transport.
- [Configuration](/fr/configuration/) — la source faisant foi pour chaque paramètre.
- [Sécurité](/fr/security/) — frontières de confiance et piste d'audit.

## Pour aller plus loin

- `internal/cli/doctor.go` — l'implémentation du doctor.
- `internal/state/sqlite/store.go` — DSN du magasin de sessions et gestion WAL.
- `internal/transport/router.go` — routage des événements entrants et allowlist.
- Référence des clés d'attributs slog — chaque `.info()`/`.warn()`/`.error()` dans l'arbre source.
