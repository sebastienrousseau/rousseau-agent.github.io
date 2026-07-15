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
description: "Expose rousseau's session store and cron jobs to Claude Desktop as an MCP server that Claude can drive from its own tool interface."
keywords: "mcp, claude desktop, stdio, tools, rousseau_search_sessions, rousseau_read_session"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/tutorials/expose-tools-via-mcp/"
subtitle: "Wire rousseau mcp into Claude Desktop and let it query the session store."
tags: "tutorials, mcp, claude-desktop, stdio, sessions"
title: "Tutoriel : exposer des outils via MCP"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, claude desktop, stdio, tools, rousseau_search_sessions, rousseau_read_session"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutoriel : exposer des outils via MCP"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/expose-tools-via-mcp/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/expose-tools-via-mcp/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutoriel : exposer des outils via MCP"
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
twitter_description: "Expose rousseau's session store and cron jobs to Claude Desktop as an MCP server that Claude can drive from its own tool interface."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutoriel : exposer des outils via MCP"
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

Claude Desktop avec rousseau comme serveur MCP stdio. Depuis une conversation Claude Desktop, vous pouvez demander « trouve la session où nous avons discuté de la logique de retry » et Claude appellera `rousseau_search_sessions`, puis `rousseau_read_session` pour récupérer la transcription complète.

Temps estimé : 5 minutes.

## Prérequis

- Claude Desktop installé (macOS ou Windows). Sous Linux, on utilise la CLI Claude, pas Desktop — voir l'alternative en bas.
- Rousseau installé et présent dans `$PATH`.
- Un historique de sessions existant dans `~/.local/share/rousseau/sessions.db` — exécutez `rousseau chat` quelques fois si le fichier est vide.

## Étape 1 : comprendre ce qui est exposé

`rousseau mcp` (`internal/cli/mcp.go`) démarre un serveur JSON-RPC stdio qui parle le Model Context Protocol. `RegisterRousseauTools` (`internal/mcp/tools.go`) attache quatre outils en lecture seule :

| Outil | Objectif |
|---|---|
| `rousseau_search_sessions` | Recherche plein texte FTS5 sur toutes les sessions enregistrées (via `internal/state/sqlite/search.go`). |
| `rousseau_list_sessions` | Liste les sessions de la plus récente à la plus ancienne. |
| `rousseau_read_session` | Retourne la transcription complète d'une session par identifiant. |
| `rousseau_cron_list` | Liste les tâches cron planifiées de rousseau. |

Il n'y a aucun outil en écriture ; les hôtes MCP peuvent parcourir mais pas modifier. Voir [MCP : outils exposés](/fr/mcp/exposed-tools/) pour les schémas d'entrée exacts.

## Étape 2 : configurer Claude Desktop

Claude Desktop lit `claude_desktop_config.json` :

- **macOS :** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows :** `%APPDATA%\Claude\claude_desktop_config.json`

Ajoutez une entrée `mcpServers` pointant vers votre binaire `rousseau` :

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "/usr/local/bin/rousseau",
      "args": ["mcp"]
    }
  }
}
```

Redémarrez Claude Desktop.

## Étape 3 : vérifier

Ouvrez une conversation Claude Desktop et vérifiez que les outils apparaissent dans le sélecteur d'outils. Vous devez voir quatre outils préfixés par `rousseau_`. Essayez :

```
Use rousseau_list_sessions to show me my 5 most recent sessions,
then read the top one with rousseau_read_session.
```

Claude invoquera les deux outils, et le serveur MCP de rousseau (`internal/mcp/server.go`) traitera chaque enveloppe JSON-RPC via stdin/stdout. En coulisses :

1. Claude Desktop appelle `initialize`, puis `tools/list` — rousseau répond avec les quatre outils déclarés dans l'ordre d'insertion.
2. Claude choisit un outil et appelle `tools/call` avec les arguments — le gestionnaire de rousseau (depuis `internal/mcp/tools.go`) interroge SQLite et renvoie du contenu textuel.
3. En cas d'erreur, rousseau expose l'erreur via le canal de contenu (`isError=true`), jamais comme une erreur JSON-RPC — les hôtes MCP attendent ce comportement.

## Étape 4 : (optionnel) attacher à la CLI Claude ou à un autre hôte MCP

Le protocole stdio est indépendant de l'hôte. Pour la CLI Claude :

```sh
claude --mcp-config <(cat <<'JSON'
{ "mcpServers": { "rousseau": { "command": "rousseau", "args": ["mcp"] } } }
JSON
)
```

Pour Continue.dev, Codeium ou un autre hôte MCP, suivez leur processus d'enregistrement de serveur MCP avec `command: rousseau`, `args: [mcp]`. Voir [MCP : Compatibilité](/fr/mcp/compatibility/) pour les clients testés.

## Étape 5 : aide-mémoire syntaxe FTS5

Comme rousseau_search_sessions est un fin wrapper autour de SQLite FTS5 (`internal/state/sqlite/search.go`), le champ de requête accepte :

| Requête | Signification |
|---|---|
| `retry logic` | Tout document contenant les deux termes. |
| `"retry logic"` | Phrase exacte. |
| `retr*` | Correspondance par préfixe. |
| `retry OR backoff` | OR booléen. |
| `retry NOT retries` | Exclusion. |

Le classement utilise BM25 (rang plus bas = plus pertinent) ; l'appel `snippet()` dans `Search` renvoie un aperçu de 200 caractères par résultat.

## Dépannage

- **« outil inconnu » dans Claude Desktop.** Redémarrez l'application. La liste des outils n'est récupérée qu'au démarrage de la session.
- **Le serveur se ferme immédiatement.** `rousseau mcp` ouvre le fichier d'état SQLite ; si le chemin dans `state.path` n'est pas accessible en écriture, `Open()` échoue et le processus se termine avec un code non nul. Lancez-le depuis un shell pour voir l'erreur.
- **Résultats de recherche vides.** Confirmez que l'index FTS5 est peuplé : `sqlite3 ~/.local/share/rousseau/sessions.db "SELECT count(*) FROM sessions_fts"`. `EnsureSearch` dans `internal/state/sqlite/search.go` remplit l'index à chaque ouverture, mais un fichier d'état corrompu peut nécessiter une reconstruction manuelle.

## Voir aussi

- [MCP](/fr/mcp/) — la documentation de référence.
- [MCP : outils exposés](/fr/mcp/exposed-tools/) — schéma de chaque outil.
- [MCP : Compatibilité](/fr/mcp/compatibility/) — clients testés.
- [Référence : magasin de sessions](/fr/reference/session-store/) — schéma SQLite derrière les outils.
