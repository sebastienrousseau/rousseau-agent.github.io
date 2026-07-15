---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "How the LLM compressor decides what to keep, the roles of trigger_messages and keep_recent, and a before/after diagram of a compressed session."
keywords: "compression, context, keep_recent, trigger_messages, summariser, marker"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/guides/context-management/"
subtitle: "trigger_messages, keep_recent, and the compressed-marker convention."
tags: "guides, context, compression, summariser"
title: "Guide : gestion du contexte"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "compression, context, keep_recent, trigger_messages, summariser, marker"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : gestion du contexte"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/context-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/context-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide : gestion du contexte"
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
twitter_description: "How the LLM compressor decides what to keep, the roles of trigger_messages and keep_recent, and a before/after diagram of a compressed session."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide : gestion du contexte"
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

## Le problème

Une session qui tourne des semaines accumule des centaines de messages. Chacun est renvoyé au fournisseur à chaque tour. Le coût croît linéairement avec le nombre de tours ; la latence aussi. Le `LLMCompressor` de rousseau (`internal/agent/compressor.go`) échange un petit coût ponctuel — un appel de résumé par compression — contre des économies permanentes sur chaque tour suivant.

La compression est **désactivée par défaut** car le déploiement de référence utilise `claudecli` sur un palier d'abonnement où le compte de jetons n'est pas facturé. Activez-la lorsque vous exécutez contre Anthropic direct, Bedrock, Vertex ou des fournisseurs compatibles OpenAI tarifés au jeton.

## Les paramètres

Depuis `CompressionConfig` dans `internal/config/config.go` :

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60        # zéro utilise la valeur par défaut 60
    keep_recent: 8              # zéro utilise la valeur par défaut 8
    prompt: ""                  # surcharge le prompt de résumé par défaut
```

Significations :

| Champ | Ce qu'il fait |
|---|---|
| `enabled` | Active la compression. Si false, l'agent utilise `NoopCompressor` et toute cette section est un no-op. |
| `trigger_messages` | La compression se déclenche dès que `len(session.Messages) >= trigger_messages`. |
| `keep_recent` | Nombre de messages les plus récents préservés tels quels après compression. |
| `prompt` | Surcharge le prompt de résumé par défaut. À définir uniquement si vous avez besoin d'instructions personnalisées (par ex. préserver la sortie JSON, toujours citer les chemins de fichiers). |

## Le prompt de résumé par défaut

```
Summarise the following conversation in <=200 words. Preserve every
commitment, TODO, credential, filename, and quoted output. Skip
pleasantries. Return only the summary — no preamble.
```

Défini comme `defaultSummaryPrompt` dans `internal/agent/compressor.go`. Surchargez avec `agent.compression.prompt` dans `config.yaml`.

## Avant / après

Une session de 68 messages, `trigger_messages: 60`, `keep_recent: 8` :

```
Avant compression :                        Après compression :

┌──────────────────────────┐              ┌──────────────────────────────┐
│ msg[0]  user             │              │ msg[0]  user (synthetic)     │
│ msg[1]  assistant        │              │   [rousseau-compressed]      │
│ msg[2]  user             │              │   (summary of prior 60       │
│  …  (60 messages)        │      →       │    messages): …              │
│ msg[59] assistant        │              ├──────────────────────────────┤
├──────────────────────────┤              │ msg[1]  user       — verbatim │
│ msg[60] user   verbatim  │              │ msg[2]  assistant  — verbatim │
│ msg[61] assistant        │              │ msg[3]  user       — verbatim │
│  …                       │              │ msg[4]  assistant  — verbatim │
│ msg[67] assistant        │              │ msg[5]  user       — verbatim │
└──────────────────────────┘              │ msg[6]  assistant  — verbatim │
                                          │ msg[7]  user       — verbatim │
                                          │ msg[8]  assistant  — verbatim │
                                          └──────────────────────────────┘
Total messages : 68                       Total messages : 9
Jetons d'entrée : ~5000 par tour          Jetons d'entrée : ~800 par tour
```

## Le marqueur

Le compresseur préfixe le message utilisateur synthétique par `[rousseau-compressed]` (constante `DefaultCompressorMarker` dans `internal/agent/compressor.go`). Aux tours suivants, `headAlreadyCompressed()` utilise le marqueur pour détecter un préfixe déjà compressé et saute la compression répétée sauf si la session a atteint `2 * trigger_messages`.

C'est ce qui borne la compression — vous ne payez pas pour re-résumer le résumé tous les 60 messages.

## Choisir les valeurs

| Situation | Recommandé |
|---|---|
| Démon de transport longue durée sur un fournisseur payant. | `trigger_messages: 60`, `keep_recent: 8`. Les valeurs par défaut sont calibrées pour cela. |
| TUI interactif où vous voulez tout dans le contexte. | `enabled: false`. |
| Sessions très techniques avec beaucoup de code / logs cités. | `trigger_messages: 40`, `keep_recent: 12`. Préservez davantage le contexte récent ; compressez plus tôt. |
| Résumés en batch critiques en coût (cron). | Chaque exécution cron est une session neuve, donc la compression se déclenche rarement. Laissez les valeurs par défaut. |

## Coût d'une passe de compression

Un appel de résumé par déclenchement. Le fournisseur utilisé est celui que sélectionne `Config.Provider` — le même que celui utilisé par l'agent. Cela signifie :

- Appel de compresseur de classe Sonnet : ~1-2 secondes, environ le coût de ~2 tours en jetons d'entrée.
- Rentabilisé après ~5-10 tours suivants selon la forme de session.

Pour un compresseur moins cher, exécutez rousseau selon le motif multi-fournisseur à deux démons avec un modèle de classe Haiku pour le démon compresseur. Voir [Guides: Multi-provider](/fr/guides/multi-provider/).

## Urgence : session trop grosse pour être chargée

Si la charge utile d'une session dépasse la fenêtre de contexte du modèle avant que la compression ne se déclenche — rare mais possible avec un `trigger_messages` très petit et de grosses sorties d'outils — le prochain tour échouera avec une erreur « context length exceeded » du fournisseur. Récupération :

```sh
rousseau session delete <id> --yes
```

Puis repartez à neuf. Ou réduisez manuellement via SQLite :

```sh
sqlite3 ~/.local/share/rousseau/sessions.db <<'SQL'
UPDATE sessions SET payload = json_set(payload, '$.messages',
  json_extract(payload, '$.messages[-8:]'))
WHERE id = '<session-id>';
SQL
```

Note : la syntaxe exacte du chemin JSON dépend de la version de SQLite. Confirmez avec un `SELECT payload` d'abord.

## Voir aussi

- [User Guide: Compression + Recall](/fr/user-guide/compression-recall/) — référence approfondie.
- [Guides: Rate limits](/fr/guides/rate-limits/) — implications de coût.
- [Guides: Session management](/fr/guides/session-management/) — cycle de vie des sessions.
- [Reference: Config schema](/fr/reference/config-schema/) — chaque champ.
