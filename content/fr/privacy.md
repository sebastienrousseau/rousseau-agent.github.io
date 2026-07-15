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
description: "rousseau-agent is self-hosted. No telemetry endpoint, no SaaS control plane. LLM providers have their own retention policies; everything else stays in the operator's infrastructure."
keywords: "privacy, telemetry, self-hosted, data handling, retention, LLM providers"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/privacy/"
subtitle: "Auto-hébergé signifie auto-contrôlé — rien ne quitte votre infrastructure sauf l'appel LLM."
tags: "privacy, legal, self-hosted"
title: "Confidentialité"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "privacy, telemetry, self-hosted, data handling, retention, LLM providers"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Confidentialité"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "legal"
order: 30
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/privacy/index.html"
item_link: "https://docs.rousseau-agent.dev/privacy/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Confidentialité"
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
twitter_description: "rousseau-agent is self-hosted. No telemetry endpoint, no SaaS control plane. LLM providers have their own retention policies; everything else stays in the operator's infrastructure."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Confidentialité"
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

## Traitement des données

`rousseau-agent` est auto-hébergé. Quand l'opérateur exécute le démon sur sa propre infrastructure, **aucune donnée ne quitte cette infrastructure hormis l'appel LLM lui-même**.

Il n'y a :

- **Aucun endpoint de télémétrie.** rousseau n'effectue aucun appel vers `rousseau-agent.dev` ni aucun autre serveur contrôlé par l'auteur à l'exécution.
- **Aucun plan de contrôle SaaS.** Pas de serveur de licences, pas de tableau de bord cloud, pas de phone-home.
- **Aucune analytique d'usage.** Le démon ne rapporte pas quels outils ont été invoqués, combien de tours ont tourné, ni quels modèles ont été appelés.
- **Aucun rapport de crash.** Les crashes remontent dans les logs locaux (`journalctl --user -u rousseau-agent.service`). Aucune stack trace n'est expédiée où que ce soit.

## Où vivent les données de session

| Donnée | Emplacement | Chiffrement au repos |
|---|---|---|
| Sessions (historique de messages) | `~/.local/share/rousseau/sessions.db` | Uniquement au niveau système de fichiers (LUKS / FileVault si l'opérateur l'a configuré). |
| Tâches cron | Même base SQLite | Idem. |
| Appairage d'appareil WhatsApp | `~/.local/share/rousseau/whatsapp.db` | Idem. |
| Sortie de logs | Journal systemd (typiquement `~/.local/state/`) | Idem. |
| Fichier de config | `~/.config/rousseau/config.yaml` | Idem. |
| Jetons OAuth de la CLI `claude` | `~/.claude/` | Idem. |

Aucune de ces données n'est transmise ailleurs par le démon.

## Fournisseurs LLM

Le fournisseur LLM est le seul point de contact externe. Chaque fournisseur a sa propre politique de traitement et de rétention des données — dont rousseau ne contrôle rien :

| Fournisseur | Politique de rétention |
|---|---|
| [claudecli](/fr/providers/claudecli/) | Ce que la CLI `claude` locale est configurée pour envoyer. Typiquement la rétention standard d'Anthropic. |
| [Anthropic direct](/fr/providers/anthropic/) | Voir https://www.anthropic.com/legal/aup |
| [AWS Bedrock](/fr/providers/bedrock/) | Défini par contrat ; typiquement aucune rétention à long terme pour le trafic d'inférence sur Bedrock. |
| [Google Vertex AI](/fr/providers/vertex/) | Défini par contrat ; typiquement aucune rétention à long terme pour l'inférence Vertex. |
| [Compatible OpenAI](/fr/providers/openai-compatible/) | Dépend de l'endpoint. Ollama et vLLM auto-hébergé ne retiennent rien d'externe ; OpenAI et OpenRouter ont leurs propres politiques. |

Choisissez le fournisseur dont la politique de rétention correspond à vos exigences opérationnelles. Pour la posture la plus stricte, exécutez contre Ollama, vLLM ou LM Studio auto-hébergé — aucune donnée ne quitte votre infrastructure.

## Données côté transport

Les transports chat envoient les messages via les serveurs du fournisseur (WhatsApp, Signal, Slack, Discord, etc.). Chacun a sa propre posture de traitement des données. rousseau n'ajoute pas de couche par-dessus — le fournisseur voit ce que le protocole sous-jacent lui montre, ce qui est spécifique au protocole :

- Signal et WhatsApp : chiffrement de bout en bout ; le fournisseur voit les métadonnées mais pas le contenu des messages.
- Slack, Discord : pas de chiffrement de bout en bout ; le fournisseur voit le contenu des messages.
- Matrix : chiffrement de bout en bout quand le salon est E2E-activé ; côté serveur sinon.
- Email : pas chiffré de bout en bout sauf si vous ajoutez PGP ou S/MIME par-dessus (ce que rousseau ne fait pas).
- iMessage : chiffrement de bout en bout ; BlueBubbles se place entre rousseau et Apple.

## Supprimer une session

Les sessions sont des lignes dans une base SQLite. Supprimez avec :

```sh
rousseau session delete <session-id>
```

Ou détruisez toute la base :

```sh
rm ~/.local/share/rousseau/sessions.db
```

Le prochain démarrage en recréera une vide. Cela purge également l'index de rappel inter-session FTS5.

## Dépendances tierces

`go.mod` liste chaque dépendance. Aucune n'est configurée pour phone-home. Les dépendances de build (linters, analyseurs statiques) ne tournent qu'en CI. Les dépendances d'exécution sont énumérées dans le SBOM CycloneDX joint à chaque release.
