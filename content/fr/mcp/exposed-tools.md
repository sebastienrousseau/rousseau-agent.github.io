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
description: "The exact tool signatures exposed by rousseau's stdio MCP server, mirroring internal/mcp/tools.go."
keywords: "mcp, rousseau_search_sessions, rousseau_list_sessions, rousseau_read_session, rousseau_cron_list"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/mcp/exposed-tools/"
subtitle: "Every tool rousseau's MCP server advertises, with schemas."
tags: "mcp, tools, sessions, cron"
title: "MCP : outils exposés"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, rousseau_search_sessions, rousseau_list_sessions, rousseau_read_session, rousseau_cron_list"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP : outils exposés"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 72
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/exposed-tools/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/exposed-tools/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP : outils exposés"
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
twitter_description: "The exact tool signatures exposed by rousseau's stdio MCP server, mirroring internal/mcp/tools.go."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP : outils exposés"
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

## Enregistrement

`internal/cli/mcp.go` ouvre le magasin de sessions SQLite, construit un `NewCronStore`, enveloppe les deux dans `mcp.NewStoreBackend`, puis appelle `mcp.RegisterRousseauTools(s, backend)`. Les quatre outils ci-dessous sont attachés dans leur ordre d'insertion — `tools/list` les renvoie exactement dans cet ordre.

Chaque outil est en lecture seule. Il n'existe aujourd'hui aucune surface d'écriture sur MCP ; c'est voulu afin qu'un hôte MCP ne puisse pas muter l'état de rousseau.

## `rousseau_search_sessions`

**Description (exposée aux hôtes) :** _Recherche plein texte sur chaque session rousseau enregistrée. Utilise la syntaxe FTS5 de SQLite (phrases entre guillemets doubles, AND/OR/NOT, jokers de préfixe)._

**Schéma d'entrée :**

```json
{
  "type": "object",
  "properties": {
    "query": {
      "type": "string",
      "description": "FTS5 query"
    },
    "limit": {
      "type": "integer",
      "description": "Cap hits returned. Default 20."
    }
  },
  "required": ["query"]
}
```

**Comportement.** Passe `query` mot pour mot au moteur FTS5 de SQLite (`Store.Search` dans `internal/state/sqlite/search.go`). Les résultats sont triés par rang BM25 (plus bas = plus pertinent). Chaque hit est rendu sur trois lignes :

```
session <id> (rank 0.42)
    title:   <session title>
    snippet: <~200-char snippet with … ellipses>
```

**Erreurs.** Une requête vide renvoie `query is required`. Les erreurs de syntaxe FTS5 remontent comme des erreurs SQLite et sont exposées via `isError: true`.

## `rousseau_list_sessions`

**Description (exposée aux hôtes) :** _Liste les sessions rousseau, plus récentes d'abord._

**Schéma d'entrée :**

```json
{
  "type": "object",
  "properties": {
    "limit": {
      "type": "integer",
      "description": "Cap rows returned. Default 20."
    }
  }
}
```

**Comportement.** Appelle `Store.List` qui utilise l'index `idx_sessions_updated_at DESC`. Chaque ligne :

```
<session-id>  <title>  msgs=<count>  updated=<iso-8601>
```

Renvoie `(no sessions)` quand le magasin est vide.

## `rousseau_read_session`

**Description (exposée aux hôtes) :** _Renvoie la transcription complète d'une session rousseau par identifiant._

**Schéma d'entrée :**

```json
{
  "type": "object",
  "properties": {
    "id": {
      "type": "string",
      "description": "Session id"
    }
  },
  "required": ["id"]
}
```

**Comportement.** Appelle `Store.Load` pour récupérer la `agent.Session` complète. Rendu ainsi :

```
id: <session-id>
title: <session title>
created: <iso-8601>
updated: <iso-8601>
messages: <count>

[0] user
    <text content>
[1] assistant
    <text content>
    ...
```

Seul le contenu texte est rendu — les blocs tool_use et tool_result sont élidés dans la surface MCP (la CLI `rousseau session show` les inclut ; MCP ne le fait volontairement pas).

**Erreurs.** `id is required` sur entrée vide. `state.ErrNotFound` sur identifiant inconnu.

## `rousseau_cron_list`

**Description (exposée aux hôtes) :** _Liste les jobs cron planifiés de rousseau (nom, planning, prompt, cible de livraison)._

**Schéma d'entrée :**

```json
{
  "type": "object",
  "properties": {}
}
```

**Comportement.** Appelle `CronStore.List` — une ligne par entrée dans `cron_jobs` :

```
<name> [<on|off>] <cron-expr> → <deliver-to>  prompt="<prompt>"  deliver=<deliver-to>
```

Renvoie `(no jobs)` quand la table cron est vide. Renvoie aussi `(no jobs)` si le `CronStore` est nil à la construction (chemin défensif dans `storeBackend.CronList`).

## Ce qui n'est PAS exposé

Omissions délibérées :

| Surface | Pourquoi non |
|---|---|
| `rousseau_write_session` / `rousseau_delete_session` | La mutation via MCP permettrait à un hôte non fiable de remodeler la piste d'audit de rousseau. |
| `rousseau_add_cron` | Même raison — mutation. Ajoutez les jobs cron via `rousseau cron add`. |
| Les outils intégrés (`read`, `write`, `edit`, `grep`, `bash`) | Ce sont des outils tournés agent, destinés au LLM dans la boucle interne de rousseau, non tournés hôte. Les exposer donnerait à l'hôte MCP la capacité d'exécuter des commandes shell sur la machine faisant tourner rousseau — précisément l'inversion de confiance à éviter. |
| Consultation de la table JID | Expose des données personnelles (numéros de téléphone). Si nécessaire, interrogez SQLite directement sur la machine où tourne le démon. |

## Surface d'erreur

Les handlers MCP renvoient `([]Content, error)`. En cas d'erreur, le serveur (`handleToolsCall` dans `internal/mcp/server.go`) expose l'erreur comme `ToolsCallResult{Content: text of err, IsError: true}`. C'est la convention MCP : les échecs d'outil transitent par le canal content avec `isError=true`, non par le canal `error` JSON-RPC. Les hôtes doivent rendre le texte et poursuivre.

## Voir aussi

- [MCP](/fr/mcp/) — la référence globale.
- [MCP: Compatibility](/fr/mcp/compatibility/) — clients testés.
- [MCP: Exposed resources](/fr/mcp/exposed-resources/) — feuille de route.
- [Reference: Tool schemas](/fr/reference/tool-schemas/) — l'ensemble différent d'outils tournés agent.
