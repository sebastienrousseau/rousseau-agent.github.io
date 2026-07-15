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
description: "Bubble Tea TUI keybindings, panels, spinner and streaming semantics for rousseau-agent's rousseau chat command."
keywords: "tui, bubble tea, keybindings, viewport, textarea, spinner, streaming, session"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/user-guide/tui/"
subtitle: "Bubble Tea keybindings, panels, streaming."
tags: "tui, bubble-tea, keybindings"
title: "TUI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tui, bubble tea, keybindings, viewport, textarea, spinner, streaming, session"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "TUI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/tui/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/tui/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "TUI"
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
twitter_description: "Bubble Tea TUI keybindings, panels, spinner and streaming semantics for rousseau-agent's rousseau chat command."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "TUI"
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

## Vue d'ensemble

`rousseau chat` ouvre une TUI Bubble Tea à trois régions :

```
+------------------------------------------------------+
|                       Header                         |  titre de session
+------------------------------------------------------+
|                                                      |
|                                                      |
|                     Viewport                         |  historique défilable
|          (messages, aperçu de réponse streamée)      |
|                                                      |
|                                                      |
+------------------------------------------------------+
|                     Textarea                         |  saisie, Entrée pour envoyer
+------------------------------------------------------+
| statut : idle | spinner | streaming | error         |
+------------------------------------------------------+
```

Fonctionne en mode alt-screen de Bubble Tea — la TUI prend le contrôle du tampon terminal et le restaure à la sortie.

## Raccourcis clavier

La TUI de Rousseau garde un ensemble de raccourcis restreint. En cas de doute, les raccourcis standard de viewport / textarea Bubble Tea s'appliquent.

### Global

| Touche | Action |
|---|---|
| `Ctrl+C` | Quitter. Sauvegarde la session en cours, n'imprime rien à la sortie. |
| `Esc` | Quitter. Identique à `Ctrl+C`. |
| `Entrée` | Envoyer le contenu courant du textarea. Sans effet pendant que l'agent est occupé. |

### Textarea (saisie)

Comportement standard du textarea Bubble Tea :

| Touche | Action |
|---|---|
| Tout caractère imprimable | Insérer au curseur. |
| `Backspace` | Supprimer le caractère avant le curseur. |
| `Delete` | Supprimer le caractère sous le curseur. |
| Flèches | Déplacer le curseur. |
| `Home` / `End` | Aller au début / fin de ligne. |
| `Ctrl+A` / `Ctrl+E` | Aller au début / fin de ligne (bindings Emacs). |
| `Ctrl+U` | Effacer jusqu'au début de ligne. |
| `Ctrl+K` | Effacer jusqu'à la fin de ligne. |
| `Shift+Entrée` | (Dépend du terminal) saut de ligne sans soumettre ; souvent mappé comme `\n` littéral. |

Le textarea grandit verticalement quand le contenu se replie ; le viewport rétrécit pour s'adapter.

### Viewport (historique)

Le viewport supporte les raccourcis Bubble Tea usuels. Le focus est sur le viewport quand le textarea est vide ; taper redirige automatiquement vers le textarea.

| Touche | Action |
|---|---|
| `PgUp` / `PgDn` | Défiler d'une page. |
| `↑` / `↓` | Défiler d'une ligne. |
| `Home` / `End` | Aller en haut / en bas. |
| Molette souris | Défiler. |

## Sémantique des panneaux

### En-tête

`rousseau · <titre de session>`. Le titre vient de `--title` lors de la création de la session (défaut : `chat YYYY-MM-DD HH:MM`).

### Viewport

Historique rendu plus, pendant qu'un tour est en cours, un **aperçu streamé** en bas. L'aperçu reflète les deltas au fil du streaming du fournisseur ; quand le tour se termine, l'aperçu est remplacé par le message assistant final.

Chaque message est préfixé par son rôle (`you`, `rousseau`, `tool`) pour que le flux soit non-ambigu quand le modèle demande un appel d'outil.

### Textarea

Texte d'espace réservé : `Ask, or press Ctrl+C to quit…`. Entrée soumet ; le textarea se réinitialise à la soumission.

Pendant que l'agent est occupé, `Entrée` est sans effet pour que les doubles soumissions accidentelles n'empilent pas les tours.

### Ligne de statut

En dessous du textarea. Le contenu varie :

| État | Ligne |
|---|---|
| Inactif | Vide. |
| Occupé | Spinner + `thinking…`. Les ticks du spinner viennent de `bubbles/spinner`. |
| Streaming | Le spinner continue ; le delta streamé apparaît dans l'aperçu du viewport. |
| Erreur | Chaîne d'erreur en rouge. Le prochain tour réussi l'efface. |

## Persistance de session

Chaque tour est persisté dans `~/.local/share/rousseau/sessions.db` via `state.Store.Save`. Si le démon crashe en pleine session :

- Le tour utilisateur est déjà sauvegardé (il a été ajouté avant que `doTurn` ne se déclenche).
- La réponse assistant n'est sauvegardée qu'une fois le tour terminé.

Au redémarrage, `rousseau chat --session <id>` reprend depuis le dernier état sauvegardé avec succès.

## Commandes de session depuis la CLI

La TUI n'expose pas toutes les opérations de session. Gérez les sessions depuis un shell :

```sh
rousseau session list
rousseau session show <id>
rousseau session search "kubectl"
rousseau session delete <id>
```

## Sémantique de streaming

Les fournisseurs qui implémentent `StreamingProvider.ChatStream` (Anthropic, `claudecli`) streament les deltas dans l'aperçu du viewport. Les fournisseurs qui n'implémentent que `Provider.Chat` (Bedrock, Vertex, compatible OpenAI selon le shim) délivrent la réponse en un bloc unique à la fin du tour — l'aperçu reste vide et la réponse apparaît quand `busy` devient `false`.

## Quand ça tourne mal

- **La TUI se fige** — `Ctrl+C` deux fois. Le premier `Ctrl+C` signale `tea.Quit`, qui flush l'état. Le second est capté par l'OS.
- **Le viewport est vide et le textarea n'accepte pas la saisie** — l'alt-screen a peut-être été corrompu par un sous-processus émettant des séquences d'échappement (par ex. un appel d'outil qui imprime des codes ANSI). Redémarrez la TUI.
- **La ligne de statut reste sur `thinking…`** — le fournisseur n'a pas répondu. Vérifiez la stderr du démon (rousseau écrit slog sur stderr ; si vous l'avez redirigée, refaites-la remonter).

## Suite

- [Guide utilisateur : CLI](/fr/user-guide/cli/) — chaque commande hors TUI.
- [Concepts](/fr/concepts/) — la boucle d'agent sous-jacente.
- [Compression + Rappel](/fr/user-guide/compression-recall/) — comment les longues conversations restent utilisables.
