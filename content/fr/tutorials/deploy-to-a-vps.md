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
description: "Walk a fresh VPS from bare install to a hardened rousseau-agent daemon under rootless Podman and a systemd Quadlet unit."
keywords: "vps, podman, quadlet, systemd, rootless, deployment, hardening"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/tutorials/deploy-to-a-vps/"
subtitle: "Build a container, provision a VPS, install the Quadlet unit, verify the service."
tags: "tutorials, deployment, podman, quadlet, systemd, vps"
title: "Tutoriel : déployer sur un VPS"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "vps, podman, quadlet, systemd, rootless, deployment, hardening"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutoriel : déployer sur un VPS"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/deploy-to-a-vps/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/deploy-to-a-vps/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutoriel : déployer sur un VPS"
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
twitter_description: "Walk a fresh VPS from bare install to a hardened rousseau-agent daemon under rootless Podman and a systemd Quadlet unit."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutoriel : déployer sur un VPS"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Ce que vous construisez

Un VPS Ubuntu 24.04 tout neuf exécutant le démon WhatsApp rousseau-agent dans un conteneur Podman rootless, piloté par l'unité Quadlet systemd `docker/rousseau-agent.container`. Système de fichiers racine en lecture seule, toutes les capacités retirées, `NoNewPrivileges=true`, seccomp actif. Zéro port réseau entrant.

Temps estimé : 45 minutes.

## Prérequis

- Un VPS sous Ubuntu 24.04 (ou Debian 12+ / Fedora 40+). 1 Go de RAM et 20 Go de disque suffisent largement.
- Accès SSH par clé à un utilisateur non root disposant de sudo.
- Votre clé API Anthropic, ou la volonté d'exécuter `claudecli` — `claudecli` nécessite `claude` installé sur le VPS avec une session OAuth active, ce qui est peu pratique sur un serveur sans tête. Anthropic direct ou Bedrock est le choix pratique.

## Étape 1 : configuration de base du système

```sh
ssh admin@vps
sudo apt update && sudo apt -y upgrade
sudo apt -y install podman uidmap fuse-overlayfs slirp4netns curl git

# podman rootless a besoin de plages subuid/subgid pour l'utilisateur
grep rousseau /etc/subuid || sudo usermod --add-subuids 200000-265535 rousseau
grep rousseau /etc/subgid || sudo usermod --add-subgids 200000-265535 rousseau
```

Créez l'utilisateur de service et sa session utilisateur systemd :

```sh
sudo useradd -m -s /bin/bash rousseau
sudo loginctl enable-linger rousseau     # maintient les services utilisateurs actifs quand personne n'est connecté
```

## Étape 2 : transférer le code source

L'unité Quadlet `docker/rousseau-agent.container` construit une image locale. Sur le VPS :

```sh
sudo -iu rousseau
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
podman build -t rousseau-agent:local -f docker/Dockerfile .
podman image inspect localhost/rousseau-agent:local | head
```

Le `Dockerfile` produit un binaire Go statique (`CGO_ENABLED=0`), le copie dans une base minimale et s'exécute sous l'UID 1000. Voir [Deployment](/fr/deployment/) pour la discussion sur l'image de base.

## Étape 3 : amorcer la configuration

Rousseau lit `~/.config/rousseau/config.yaml`. Créez-le sur l'hôte — l'unité Quadlet monte le `$HOME` du conteneur vers l'hôte.

```sh
mkdir -p /home/rousseau/.config/rousseau
cat > /home/rousseau/.config/rousseau/config.yaml <<'YAML'
provider: anthropic

anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096

whatsapp:
  reply_header: "*rousseau*\n\n"

agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

log:
  level: info
  format: json
YAML
chown -R rousseau:rousseau /home/rousseau/.config
```

Stockez la clé API Anthropic dans un fichier d'environnement systemd — jamais dans `config.yaml` :

```sh
mkdir -p /home/rousseau/.config/rousseau
cat > /home/rousseau/.config/rousseau/env <<'ENV'
ANTHROPIC_API_KEY=sk-ant-…
ENV
chmod 0600 /home/rousseau/.config/rousseau/env
```

Référencez-le depuis l'unité Quadlet — voir l'étape suivante.

## Étape 4 : installer l'unité Quadlet

```sh
mkdir -p /home/rousseau/.config/containers/systemd
cp docker/rousseau-agent.container /home/rousseau/.config/containers/systemd/
```

Éditez pour votre JID et le fichier de secrets :

```sh
sed -i 's|Exec=whatsapp --allow.*|Exec=whatsapp --allow YOUR_JID@s.whatsapp.net|' \
  /home/rousseau/.config/containers/systemd/rousseau-agent.container

cat >> /home/rousseau/.config/containers/systemd/rousseau-agent.container <<'EOF'
EnvironmentFile=%h/.config/rousseau/env
EOF
```

Rechargez et démarrez :

```sh
systemctl --user daemon-reload
systemctl --user enable --now rousseau-agent
systemctl --user status rousseau-agent
```

## Étape 5 : premier appairage

Le pont WhatsApp doit imprimer un QR code la première fois. Attachez-vous :

```sh
podman logs -f rousseau-agent
# scannez le QR depuis votre téléphone : WhatsApp > Paramètres > Appareils liés
```

Séquence de logs attendue (depuis `internal/transport/whatsapp/client.go`) :

```
INFO whatsapp.starting store=… allowlist=1
INFO whatsapp.qr_ready
INFO whatsapp.paired
INFO whatsapp.connected
```

Les identifiants de l'appareil persistent dans `/home/rousseau/.local/share/rousseau/whatsapp.db`. Les redémarrages ultérieurs sautent le QR.

## Étape 6 : vérifier

```sh
podman exec rousseau-agent rousseau status
```

Un code de sortie 0 signifie que le démon est sain. Toute autre valeur est un signal d'alerte — voir [Référence : codes de sortie](/fr/reference/exit-codes/).

Envoyez-vous un message de test depuis le téléphone autorisé. Les logs structurés affichent :

```
INFO whatsapp.incoming from=447900123456@s.whatsapp.net
INFO tool.execute name=read id=t_1
INFO whatsapp.handler_ok elapsed=…
```

## Étape 7 : revue de durcissement

L'unité Quadlet applique déjà :

- `ReadOnly=true` + `Tmpfs=/tmp` — aucune mutation de l'image à l'exécution.
- `DropCapability=all` — le binaire Go n'a besoin d'aucune capacité élevée.
- `NoNewPrivileges=true` — les processus enfants ne peuvent pas obtenir de privilèges.
- `SeccompProfile=/usr/share/containers/seccomp.json` — filtre d'appels système au niveau du noyau.
- `Network=pasta` — pile réseau rootless, bloque l'entrant par défaut.
- `UserNS=keep-id` — les fichiers montés appartiennent au bon utilisateur des deux côtés.

Pour la posture la plus stricte, encadrez le démon d'un pare-feu sortant uniquement (nftables ou Cloudflare Zero-Trust) qui n'autorise que les plages CDN vers lesquelles Anthropic + Meta se résolvent réellement. Voir [Guides : Enterprise Onboarding](/fr/guides/enterprise-onboarding/) pour la checklist.

## Étape 8 : sauvegarde

Tout l'état persistant tient dans un seul répertoire : `/home/rousseau/.local/share/rousseau/`. Sauvegardez-le chaque nuit avec `restic` ou `borg`.

```sh
sudo -iu rousseau -- restic backup /home/rousseau/.local/share/rousseau
```

Les bases SQLite peuvent être snapshotées à chaud sans risque car le journal WAL est activé par `Open()` dans `internal/state/sqlite/store.go`.

## Voir aussi

- [Deployment](/fr/deployment/) — référence complète de l'unité Quadlet.
- [Guides : déploiement en production](/fr/guides/production-deployment/) — expédition des logs, redémarrages progressifs.
- [Guides : Enterprise Onboarding](/fr/guides/enterprise-onboarding/) — vérification SBOM, audit seccomp.
- [Security](/fr/security/) — frontières de confiance.
