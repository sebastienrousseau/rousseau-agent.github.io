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
description: "Hot-swap the underlying model mid-session by editing config.yaml and restarting the daemon — the SQLite session store survives."
keywords: "model swap, hot swap, mid-session, restart, session store, sonnet, opus, haiku"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/guides/rate-model-swap/"
subtitle: "Swap Sonnet for Opus mid-session; the session store survives the restart."
tags: "guides, model, swap, restart, session"
title: "Guide : échange à chaud du modèle"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "model swap, hot swap, mid-session, restart, session store, sonnet, opus, haiku"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : échange à chaud du modèle"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 41
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/rate-model-swap/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/rate-model-swap/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide : échange à chaud du modèle"
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
twitter_description: "Hot-swap the underlying model mid-session by editing config.yaml and restarting the daemon — the SQLite session store survives."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide : échange à chaud du modèle"
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

## Pourquoi ça marche

Rousseau lit son fournisseur et son modèle depuis `config.yaml` une seule fois au démarrage du processus (`config.Load` dans `internal/config/config.go`). L'état de session vit dans SQLite. Changer de modèle revient à éditer la configuration, redémarrer le démon et laisser le nouveau modèle traiter le prochain message entrant — tandis que chaque session à laquelle le modèle précédent a participé demeure intacte dans `sessions.db`.

Rien dans le magasin de sessions n'est lié à un modèle particulier. La colonne `payload` (`internal/state/sqlite/schema.sql`) est un simple blob JSON d'`agent.Session` : rôle, contenu, blocs tool-use. Tout modèle qui parle la convention des blocs de contenu Anthropic (ou qui est adapté via les adaptateurs SDK dans `internal/llm/*/client.go`) peut reprendre là où le précédent s'est arrêté.

## Basculer au sein du même fournisseur

Le cas facile. Éditez le champ modèle :

```yaml
# avant :
anthropic:
  model: claude-sonnet-4-6

# maintenant :
anthropic:
  model: claude-opus-4-6
```

Redémarrez :

```sh
systemctl --user restart rousseau-agent
# ou, si vous exécutez rousseau chat en interactif, quittez et relancez
```

Envoyez le message suivant. La réponse vient d'Opus ; le contexte de session est inchangé.

## Basculer entre fournisseurs

Un peu plus complexe car les formes des blocs de contenu varient. Les adaptateurs de rousseau (`internal/llm/anthropic/client.go`, `internal/llm/openai/client.go`) font l'aller-retour des valeurs `agent.Message` via les types natifs du SDK à chaque tour. Cela signifie :

- **`claudecli` → `anthropic`** — bascule propre. Les deux utilisent la même forme de bloc de contenu.
- **`claudecli` → `bedrock` / `vertex`** — bascule propre. Anthropic-sur-Bedrock et Anthropic-sur-Vertex parlent le même format de messages.
- **Famille Anthropic → `openai` / `openrouter` / `ollama`** — Les blocs tool-use sont reformatés vers le format function-call d'OpenAI. Les paires tool_use / tool_result antérieures dans la session font l'aller-retour via l'adaptateur. Devrait être transparent pour le texte ; les cas limites (multi-tool-use dans un même tour, partiels de streaming) peuvent s'afficher différemment.

Si la session a un lourd historique tool-use et que vous traversez des familles de fournisseurs, testez d'abord avec une session neuve.

## Changer le fournisseur de déploiement sans toucher à l'état

Même magasin de sessions, configuration démon différente :

```sh
cp ~/.config/rousseau/config.yaml ~/.config/rousseau/config.yaml.bak
$EDITOR ~/.config/rousseau/config.yaml   # change provider + model
systemctl --user restart rousseau-agent
```

`state.path` n'a pas changé, donc la cartographie JID→session (table `jid_sessions` dans `internal/state/sqlite/jidmap.go`) pointe toujours sur le même historique de conversation pour chaque expéditeur WhatsApp / Slack / Matrix.

## Ce qui est préservé

| État | Survit au redémarrage | Notes |
|---|---|---|
| Transcriptions de session | Oui | Table `sessions`. |
| Index de recall FTS5 | Oui | Table virtuelle `sessions_fts`. Re-tokenisée au backfill. |
| Cartographie JID → session | Oui | Table `jid_sessions`. |
| Jobs cron | Oui | Table `cron_jobs`. |
| Appairage d'appareil WhatsApp | Oui | `whatsapp.db` (fichier séparé). |
| Hit du cache de prompt Anthropic | **Non** | Le cache est par endpoint. Un nouveau modèle ou endpoint démarre à froid. |

## Ce qui est perdu

Les marqueurs de prompt-cache Anthropic (`applyCacheMarkers` dans `internal/llm/anthropic/client.go`) vivent dans le cache éphémère du modèle — ils ne persistent pas au redémarrage du modèle ou du fournisseur. Les quelques tours suivant une bascule paient les jetons d'entrée pleins ; les tours suivants reconstruisent le cache. Bon à savoir pour la budgétisation des coûts, mais pas pour la correction.

## Quand basculer vs. repartir à neuf

Basculez en place quand :

- La session vaut la peine d'être préservée et le contenu est majoritairement textuel.
- Les modèles sont dans la même famille (les deux Anthropic, ou via Bedrock/Vertex).
- Vous acceptez un miss de cache ponctuel.

Repartez à neuf quand :

- La session a un contexte périmé que vous ne voulez pas voir un modèle plus intelligent poursuivre.
- Vous traversez des familles de fournisseurs et voulez un comportement déterministe.
- Le compte de jetons atteint de toute façon le seuil de compression — compressez et basculez en un seul geste.

## Tester après une bascule

```sh
rousseau session list | head -3
rousseau session show <id> | tail -20
# dans la TUI ou via un transport :
> qu'avons-nous décidé au sujet de X ?
```

Si la réponse référence la conversation précédente de manière cohérente, la bascule fonctionne. Si le modèle s'excuse de « ne pas avoir de contexte » ou se répète, l'aller-retour de l'adaptateur perd peut-être des métadonnées tool-use — ouvrez un bug ou revenez au modèle précédent.

## Voir aussi

- [Providers](/fr/providers/) — chaque fournisseur supporté.
- [Configuration](/fr/configuration/) — les noms de champs exacts.
- [Guides: Rate limits](/fr/guides/rate-limits/) — discussion des marqueurs de cache.
- [Guides: Session management](/fr/guides/session-management/) — cycle de vie complet.
