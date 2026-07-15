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
description: "How to update rousseau-agent: go install refresh, container tag rollover, config migration between minor versions, session-store compatibility policy."
keywords: "update, upgrade, go install, container tag, config migration, minor version"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/getting-started/updating/"
subtitle: "Move between versions without losing sessions or bricking the daemon."
tags: "update, upgrade, migration"
title: "Mise à jour"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "update, upgrade, go install, container tag, config migration, minor version"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Mise à jour"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 24
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/updating/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/updating/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Mise à jour"
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
twitter_description: "How to update rousseau-agent: go install refresh, container tag rollover, config migration between minor versions, session-store compatibility policy."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Mise à jour"
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

## Politique de versionnage

Rousseau suit le [Semantic Versioning](https://semver.org) :

| Incrément | Ce qui change |
|---|---|
| Patch (`0.1.2 → 0.1.3`) | Corrections de bugs, correctifs de sécurité, mises à jour de dépendances. Aucun changement de configuration ni de format sur disque. |
| Mineur (`0.1.x → 0.2.0`) | Nouvelles fonctionnalités. Les ajouts de configuration ne cassent jamais la compatibilité ; si un champ est retiré, un fallback aliasé couvre au moins une version mineure. |
| Majeur (`0.x → 1.0`) | Changements cassants. Nécessite une recette de migration documentée dans le [changelog](/fr/changelog/). |

La [politique SECURITY.md](https://github.com/sebastienrousseau/rousseau-agent/blob/main/SECURITY.md) est explicite : seuls `main` et la release taguée la plus récente reçoivent des correctifs de sécurité. Il n'existe pas de branche de support à long terme.

## Méthode de mise à jour par chemin d'installation

### Archive de release signée

```sh
VERSION=<new-tag>
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_linux_amd64.tar.gz"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt.sig"

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature "rousseau_${VERSION}_checksums.txt.sig" \
  "rousseau_${VERSION}_checksums.txt"

sha256sum -c "rousseau_${VERSION}_checksums.txt" --ignore-missing
tar -xzf "rousseau_${VERSION}_linux_amd64.tar.gz"
sudo install -m 0755 rousseau /usr/local/bin/rousseau
rousseau version
```

La vérification n'est pas optionnelle. Chaque release embarque une nouvelle signature cosign ; sauter la vérification annule la posture de chaîne d'approvisionnement.

### `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

Pour épingler un tag exact :

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@v0.4.2
```

`$GOBIN` (typiquement `~/go/bin`) doit figurer sur `$PATH` avant `/usr/local/bin` si vous voulez que le nouveau binaire prenne le pas.

### Image de conteneur

Faites rouler le tag sur la référence d'image et redémarrez le service systemd. Si vous utilisez l'unité Quadlet de référence :

```sh
sed -i "s#Image=ghcr.io/sebastienrousseau/rousseau-agent:.*#Image=ghcr.io/sebastienrousseau/rousseau-agent:<new-tag>#" \
  ~/.config/containers/systemd/rousseau-agent.container
systemctl --user daemon-reload
systemctl --user restart rousseau-agent.service
journalctl --user -u rousseau-agent.service -f
```

Épingler à `:latest` n'est pas sûr dans un déploiement soucieux de la chaîne d'approvisionnement — épinglez toujours un tag immuable (`:v0.4.2`) et vérifiez le digest de l'image contre les notes de release.

### Depuis les sources

```sh
cd rousseau-agent
git fetch --tags
git checkout <new-tag>
make check          # exécute localement l'intégralité de la porte CI
make build
sudo install -m 0755 bin/rousseau /usr/local/bin/rousseau
```

`make check` correspond à la même porte 18-linters + race + govulncheck qu'impose la CI — un passage local réussi garantit que le job de build reproductible passera aussi.

## Migration de configuration

Les changements du schéma de configuration sont documentés dans le [changelog](/fr/changelog/) pour chaque version mineure. Les valeurs par défaut Viper maintiennent les anciennes clés fonctionnelles sur un cycle mineur ; le motif suivant s'applique :

- **Nouvelle clé ajoutée** : reçoit une valeur par défaut qui préserve le comportement antérieur. Aucune action requise.
- **Clé renommée** : l'ancienne clé est aliasée pendant une mineure. Un avertissement est journalisé quand l'alias est utilisé.
- **Clé retirée** : une erreur fail-fast est émise au chargement. Le changelog nomme le remplacement.

Pour tester à vide une configuration contre un nouveau binaire :

```sh
rousseau doctor --config ~/.config/rousseau/config.yaml
```

`rousseau doctor` parcourt chaque dépendance runtime et chaque choix de configuration ; une ligne `fail` fait remonter exactement la clé qui nécessite attention.

## Compatibilité du magasin de sessions

`~/.local/share/rousseau/sessions.db` utilise SQLite avec un schéma versionné. Les migrations de schéma sont additives et idempotentes — le démon exécute `CREATE TABLE IF NOT EXISTS` et `ALTER TABLE ADD COLUMN` au démarrage. **Ne rétrogradez jamais** entre versions mineures une fois le nouveau schéma appliqué ; SQLite ne retire pas automatiquement les colonnes, mais le code applicatif suppose leur présence.

Si vous avez besoin d'un état vierge :

```sh
mv ~/.local/share/rousseau/sessions.db ~/.local/share/rousseau/sessions.db.bak
```

Le démon recrée le magasin au prochain lancement. Les identifiants d'appareil WhatsApp sont stockés séparément dans `whatsapp.db`, donc une réinitialisation du magasin de sessions n'oblige pas à ré-appairer.

## Compatibilité du magasin WhatsApp

`whatsapp.db` (le magasin d'appareils de whatsmeow) est séparé du magasin de sessions précisément pour qu'une migration du schéma de sessions ne puisse pas casser l'appairage WhatsApp. Si whatsmeow lui-même change de format sur disque lors d'une montée de version de rousseau, le changelog le signalera et le chemin de récupération est : supprimer `whatsapp.db`, redémarrer, rescanner le QR.

## Retour arrière

- **Archive de release signée / `go install`** : réinstaller le tag précédent avec la même recette.
- **Conteneur** : remettre l'ancien tag d'image et redémarrer.
- **Depuis les sources** : `git checkout <old-tag> && make build`.

Les retours arrière sont sûrs tant que le schéma du magasin de sessions dans l'ancienne version est un sur-ensemble de ce qu'a écrit la nouvelle. En pratique, c'est toujours vrai au sein d'une même série mineure et généralement vrai entre mineures adjacentes. Les montées de version majeures livrent une recette de migration avec une clause explicite de non-retour dans le changelog.

## Suite

- [Changelog](/fr/changelog/) — décomposition version par version.
- [Troubleshooting](/fr/troubleshooting/) — si `rousseau doctor` fait remonter une ligne `fail`.
