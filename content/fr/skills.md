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
changefreq: "weekly"
description: "rousseau-agent's skills loader: Markdown + YAML frontmatter, discovery from skills_dir, trigger-based activation, composition into the system prompt."
keywords: "skills, agentskills.io, markdown, YAML frontmatter, triggers, system prompt, activation"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/skills/"
subtitle: "Fichiers de compétences Markdown compatibles agentskills.io."
tags: "skills, reference"
title: "Compétences"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "skills, agentskills.io, markdown, YAML frontmatter, triggers, system prompt, activation"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Compétences"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 23
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/skills/index.html"
item_link: "https://docs.rousseau-agent.dev/skills/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Compétences"
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
twitter_description: "rousseau-agent's skills loader: Markdown + YAML frontmatter, discovery from skills_dir, trigger-based activation, composition into the system prompt."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Compétences"
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

## Format d'une compétence

Une compétence est un fichier Markdown avec un en-tête YAML front-matter optionnel. Le format est délibérément proche de la convention [agentskills.io](https://agentskills.io) afin que les fichiers soient portables vers d'autres outils.

Exemple — `~/.local/share/rousseau/skills/git-rebase.md` :

```markdown
---
name: git-rebase
description: Guide the user through an interactive rebase safely.
triggers:
  - rebase
  - git rebase
  - squash
  - autosquash
---
When helping with a git rebase, first verify the current HEAD is
pushed to a remote branch. Prefer `git rebase -i --autosquash`
when the user has fixup commits. Never force-push to `main`.
```

## Champs du frontmatter

| Champ | Type | Effet |
|---|---|---|
| `name` | string | Correspond à `^[a-z][a-z0-9-]*$`. Affiché par `rousseau skills list`. |
| `description` | string | Résumé sur une ligne. |
| `triggers` | `[]string` | Sous-chaînes insensibles à la casse. Si l'une apparaît dans le message utilisateur, la compétence est activée. Vide signifie que la compétence ne s'active jamais automatiquement. |

Tout ce qui suit le `---` de fermeture constitue le corps de la compétence, tel quel.

## Découverte

Le loader parcourt `agent.skills_dir` à la recherche de fichiers `*.md` (non récursif). Un répertoire manquant n'est pas une erreur — Load retourne `nil`. Les sous-répertoires sont ignorés.

```yaml
agent:
  skills_dir: ~/.local/share/rousseau/skills
```

## Activation

À chaque tour utilisateur, `SkillsProvider.SystemAppendix(session)` inspecte le message utilisateur le plus récent et met en correspondance les `triggers` de chaque compétence (sans distinction de casse). Chaque correspondance est concaténée (dans l'ordre de chargement) et intégrée au prompt système pour ce tour.

Les compétences avec des `triggers` vides ne s'activent jamais automatiquement, mais peuvent être incluses par programmation par les appelants intégrant la bibliothèque.

## CLI

```sh
# Lister les compétences découvertes.
rousseau skills list

# Afficher le contenu d'une compétence unique.
rousseau skills show git-rebase
```

## Contraintes de conception

- **Aucune exécution de code.** Les compétences sont des chaînes. Elles ne peuvent pas exécuter de scripts ni de commandes shell. Si vous souhaitez de l'automatisation, câblez plutôt un nouvel outil via `Registry.Register`.
- **Aucun versioning.** rousseau ne suit pas les versions des compétences. Gérez cela avec git — le `skills_dir` est censé être une copie de travail d'un dépôt.
- **Déterministe.** Une même session + message utilisateur produit la même annexe. Aucun LLM n'intervient dans la boucle.

## Rédiger des compétences efficaces

- Gardez le corps court (100–500 mots). Chaque activation est préfixée au prompt système pour ce tour.
- Privilégiez les phrases impératives (« Lorsque l'utilisateur demande X, fais Y ») plutôt que l'exposé.
- Utilisez des `triggers` pour des expressions de haute précision ; des triggers larges (« code », « aide ») s'activent à presque chaque tour et noient les autres compétences.
- Testez dans la TUI (`rousseau chat`) avant de déployer dans un daemon de transport de chat — la ligne de log `agent.skills_activated` indique quelles compétences ont été déclenchées.
