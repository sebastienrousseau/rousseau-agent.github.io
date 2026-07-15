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
description: "Run two rousseau daemons with different providers side-by-side — e.g. claudecli for interactive chat and Bedrock for scheduled reports."
keywords: "multi provider, claudecli, bedrock, config precedence, XDG_CONFIG_HOME"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/guides/multi-provider/"
subtitle: "Two daemons, two providers, one operator."
tags: "guides, providers, multi-provider, deployment"
title: "Guide : multi-fournisseur"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "multi provider, claudecli, bedrock, config precedence, XDG_CONFIG_HOME"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : multi-fournisseur"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 35
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/multi-provider/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/multi-provider/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide : multi-fournisseur"
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
twitter_description: "Run two rousseau daemons with different providers side-by-side — e.g. claudecli for interactive chat and Bedrock for scheduled reports."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide : multi-fournisseur"
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

## Pourquoi vous en auriez besoin

Le champ `provider` de rousseau est un scalaire unique (`Config.Provider` dans `internal/config/config.go`). Un unique processus rousseau parle à exactement un fournisseur. Quand vous en voulez plusieurs — le plus souvent, `claudecli` pour l'usage TUI interactif car il hérite d'une session OAuth, et un fournisseur d'API payant (Bedrock, Anthropic direct, Vertex) pour les démons d'arrière-plan où l'OAuth `claude` de palier d'abonnement est peu pratique — vous exécutez **deux processus rousseau** avec des fichiers de configuration différents.

Appariements raisonnables :

| Interactif | Non-supervisé | Pourquoi |
|---|---|---|
| `claudecli` | `anthropic` ou `bedrock` | OAuth pour le chat sur laptop, clé API pour un démon sur VPS. |
| `claudecli` | `vertex` | Même chose, sur GCP. |
| `anthropic` | `openai` ou `ollama` | Comparer les réponses, ou basculer sur un modèle moins cher/local pour le cron. |
| `claudecli` | `openai` (OpenRouter) | Claude en TUI, modèle OpenRouter bon marché pour les résumés planifiés. |

## Comment rousseau résout la configuration

`config.Load` (dans `internal/config/config.go`) applique flag > env > fichier > défaut. Le fichier lu vaut par défaut `~/.config/rousseau/config.yaml`, mais le flag persistant `--config` de la commande racine (`internal/cli/root.go`) le surcharge. Cela vous donne une séparation propre.

## Disposition à deux configs

```sh
mkdir -p ~/.config/rousseau
cat > ~/.config/rousseau/chat.yaml <<'YAML'
provider: claudecli
claudecli:
  binary: claude
log:
  level: info
  format: text
YAML

cat > ~/.config/rousseau/cron.yaml <<'YAML'
provider: bedrock
bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
log:
  level: info
  format: json
YAML
```

Lancez chaque commande avec le bon fichier :

```sh
rousseau --config ~/.config/rousseau/chat.yaml chat
rousseau --config ~/.config/rousseau/cron.yaml whatsapp --allow YOUR_JID@s.whatsapp.net
```

## État partagé vs partitionné

Les deux processus pointent par défaut sur le même magasin de sessions SQLite (`~/.local/share/rousseau/sessions.db`) — et c'est généralement ce que vous voulez, afin que le pont WhatsApp et votre chat TUI partagent l'historique.

Pour partitionner complètement l'état, surchargez `state.path` par configuration :

```yaml
state:
  path: /home/seb/.local/share/rousseau/chat.db
```

L'accès SQLite inter-processus est sûr grâce au journal WAL et au `busy_timeout` de 15 secondes défini par `Open()` dans `internal/state/sqlite/store.go`.

## Câblage systemd

Deux unités Quadlet, une par configuration. L'`Exec=` de chaque unité inclut `--config /home/rousseau/.config/rousseau/<name>.yaml` :

```ini
Exec=--config /home/rousseau/.config/rousseau/cron.yaml whatsapp --allow ...
```

Voir [Deployment](/fr/deployment/) pour l'unité de base.

## Politiques d'approbation par configuration

Des fournisseurs différents méritent des approbations différentes. Le `claudecli` interactif peut sereinement rester en `mode: allow_all` car Claude Code possède sa propre interface d'approbation par appel. Le démon Bedrock/Anthropic devrait fonctionner en `mode: pattern` avec `default: deny`. Placez chacun sous son propre YAML.

## Tests

Confirmez que chaque processus parle au bon endpoint :

```sh
# L'interactif montre le chemin du sous-processus claudecli dans strace / lsof
lsof -c rousseau | grep -E 'claude|CLAUDE'

# L'arrière-plan montre le HTTPS sortant vers bedrock-runtime.<region>.amazonaws.com
ss -tanp | grep rousseau
```

## Ce que cela ne vous donne PAS

- **Pas de routage par requête.** Rousseau ne basculera pas d'un fournisseur à l'autre au sein d'un même tour. Une défaillance du fournisseur configuré remonte comme `whatsapp.handler_failed` / `turn.failed` et le modèle ne réessaie pas contre un fournisseur différent. C'est un élément de feuille de route.
- **Pas de cache partagé.** Le cache de prompt Anthropic (voir `applyCacheMarkers` dans `internal/llm/anthropic/client.go`) est par endpoint. Un hit sous Anthropic direct n'est pas un hit contre Bedrock, même pour la même famille de modèles.

## Voir aussi

- [Providers](/fr/providers/) — comparaison des cinq types de fournisseurs.
- [Configuration](/fr/configuration/) — chaque paramètre.
- [Reference: Environment Variables](/fr/reference/environment-variables/) — surcharges par variables d'environnement.
- [Guides: Production Deployment](/fr/guides/production-deployment/).
