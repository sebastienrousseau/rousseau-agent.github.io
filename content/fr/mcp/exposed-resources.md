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
description: "MCP resources exposed by rousseau's stdio server today (none) and the roadmap for sessions-as-resources."
keywords: "mcp, resources, roadmap, sessions, resources/list"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/mcp/exposed-resources/"
subtitle: "What resources rousseau exposes today, and what is planned."
tags: "mcp, resources, roadmap"
title: "MCP : ressources exposées"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, resources, roadmap, sessions, resources/list"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP : ressources exposées"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 73
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/exposed-resources/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/exposed-resources/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP : ressources exposées"
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
twitter_description: "MCP resources exposed by rousseau's stdio server today (none) and the roadmap for sessions-as-resources."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP : ressources exposées"
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

## État actuel

Le serveur MCP de rousseau (`internal/mcp/server.go`) déclare la capacité `Tools` uniquement. Il renvoie une liste vide sur `resources/list` :

```
MethodResourcesList → okResponse(env.ID, map[string]any{"resources": []any{}})
```

L'intention est délibérée. Chaque cas d'usage qui ressemblerait à une ressource MCP — une session sauvegardée, une description de job cron — est aujourd'hui exposé via un outil (`rousseau_read_session`, `rousseau_cron_list`) afin que l'hôte puisse demander exactement les données dont il a besoin, quand il en a besoin, plutôt que de pré-lister chaque session.

## Pourquoi pas de ressources aujourd'hui

Les ressources MCP brillent quand un hôte veut énumérer un ensemble modeste et bien défini d'URIs (fichiers, pages) et les déréférencer paresseusement. Le magasin de sessions de rousseau peut croître jusqu'à des milliers de lignes ; énumérer chaque session à chaque appel `resources/list` ferait exploser le contexte de l'hôte. La surface d'outils (search / list / read) est une meilleure forme pour un état à forte cardinalité.

## Feuille de route

Deux candidats méritent d'être exposés comme ressources MCP, une fois que la spécification MCP supportera robustement l'énumération paginée des ressources :

### Candidat : `rousseau://sessions/<id>`

Chaque session rousseau comme ressource. Les URIs ressembleraient à :

```
rousseau://sessions/1a2b3c4d-…
```

Le déréférencement renverrait la même transcription que `rousseau_read_session` renvoie aujourd'hui. Cela permettrait à l'hôte d'attacher une session spécifique à une conversation comme un citoyen de première classe (« attacher la session 1a2b3c… », glisser-déposer), plutôt que d'obliger le modèle à se rappeler d'appeler l'outil.

Condition préalable : la liste de ressources devrait être paginée. Les versions récentes de la spécification MCP proposent une pagination par curseur ; une fois disponible et implémentée par les hôtes, cela devient viable.

### Candidat : `rousseau://cron/<name>`

Chaque job cron comme ressource. Inspection en lecture seule du prompt, du planning, de la cible de livraison et de l'horodatage de dernière exécution. Petite liste — probablement sans risque d'énumération aujourd'hui, mais pas assez utile pour l'exposer séparément de `rousseau_cron_list` avant que la forme sessions-comme-ressources ait fait ses preuves.

## Capacité prompts

Non exposée aujourd'hui non plus. `MethodPromptsList` renvoie `{"prompts": []any{}}` dans le `dispatch` de `internal/mcp/server.go`. Rousseau n'a pas de bibliothèque de prompts organisée à exposer ; le mécanisme des skills (`internal/skills/skills.go`) est le concept interne équivalent, et il n'est pas actuellement exposé sur MCP.

Si la feuille de route des skills converge vers des prompts partageables, les exposer en tant que prompts MCP est l'étape naturelle suivante. Voir [Skills](/fr/skills/).

## Comment contourner cette absence aujourd'hui

Si votre hôte MCP exige des ressources pour une affordance UI spécifique (par ex. le glisser-déposer d'une session), la solution de contournement est :

1. Demander à l'hôte d'invoquer `rousseau_list_sessions` au début du chat.
2. Copier l'identifiant de session à référencer.
3. Invoquer `rousseau_read_session` avec cet identifiant.

Moins ergonomique que le déréférencement natif de ressources, mais fonctionnellement équivalent.

## Demander une surface de ressources

Tous les opérateurs n'ont pas besoin de ressources sur MCP. Si votre équipe en a besoin, le chemin constructif est d'ouvrir une issue avec :

- L'hôte MCP spécifique avec lequel vous vous intégrez.
- L'action utilisateur qui serait plus agréable avec des ressources.
- Les attentes de trafic approximatives (combien de sessions, à quelle fréquence).

## Voir aussi

- [MCP](/fr/mcp/) — la référence globale.
- [MCP: Exposed tools](/fr/mcp/exposed-tools/) — ce qui est exposé aujourd'hui.
- [MCP: Compatibility](/fr/mcp/compatibility/) — clients testés.
- [Skills](/fr/skills/) — le concept interne qui pourrait devenir prompts MCP.
