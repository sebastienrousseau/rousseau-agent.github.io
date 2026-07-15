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
description: "MCP clients tested against rousseau's stdio server: Claude Desktop, Claude CLI, Continue, Codeium, plus setup snippets."
keywords: "mcp, compatibility, claude desktop, continue, codeium, stdio, claude_desktop_config"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/mcp/compatibility/"
subtitle: "Which MCP clients talk to rousseau's stdio server."
tags: "mcp, compatibility, claude, continue, stdio"
title: "MCP : compatibilité"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mcp, compatibility, claude desktop, continue, codeium, stdio, claude_desktop_config"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "MCP : compatibilité"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "mcp"
order: 71
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/compatibility/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/compatibility/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "MCP : compatibilité"
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
twitter_description: "MCP clients tested against rousseau's stdio server: Claude Desktop, Claude CLI, Continue, Codeium, plus setup snippets."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "MCP : compatibilité"
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

## Le contrat protocolaire

Le serveur MCP de rousseau (`internal/mcp/server.go`) parle JSON-RPC 2.0 sur stdio et annonce les outils déclarés dans `internal/mcp/tools.go`. Il gère les méthodes suivantes :

- `initialize` — renvoie `ServerCapabilities.Tools`.
- `initialized` — notification, sans réponse.
- `ping` — renvoie `{}`.
- `tools/list` — renvoie les quatre outils dans leur ordre d'insertion.
- `tools/call` — invoque un handler d'outil, renvoie `ToolsCallResult` avec `content` et `isError`.
- `resources/list`, `prompts/list` — renvoient des tableaux vides (voir les notes de feuille de route ci-dessous).
- `shutdown` — renvoie `{}`.

Tout hôte MCP qui parle JSON-RPC sur stdio et appelle les quatre méthodes ci-dessus est compatible.

## Clients testés

| Client | Statut | Comment enregistrer |
|---|---|---|
| Claude Desktop (macOS / Windows) | Fonctionne. | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) ou `%APPDATA%\Claude\claude_desktop_config.json` (Windows). |
| Claude CLI (`claude`) | Fonctionne. | `--mcp-config <file>` ou un bloc `[mcp]` dans `~/.claude/config.json`. |
| Continue.dev (VS Code / JetBrains) | Fonctionne. | Bloc `mcpServers` dans `~/.continue/config.json`. |
| Codeium (extensions IDE) | Fonctionne quand Codeium expose le mode hôte MCP (versions récentes). La configuration varie selon l'IDE. |
| Cursor (versions récentes) | Fonctionne. Enregistrer via l'interface Settings > MCP de Cursor. |
| Tout SDK hôte MCP Go / TypeScript / Python | Fonctionne. Instancier avec `command: "rousseau", args: ["mcp"]`. |

Inconnus / non testés mais probablement compatibles : `zed`, `windsurf`, `aider`. Si votre hôte supporte la spécification MCP stdio, rousseau fonctionnera.

## Claude Desktop

Éditez `claude_desktop_config.json` (chemin ci-dessus) et ajoutez :

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

Redémarrez Claude Desktop. Les quatre outils `rousseau_*` apparaissent dans le sélecteur d'outils lors de la prochaine session de chat.

Pour un état par workspace, ajoutez une surcharge d'environnement :

```json
{
  "mcpServers": {
    "rousseau-work": {
      "command": "/usr/local/bin/rousseau",
      "args": ["--config", "/home/seb/.config/rousseau/work.yaml", "mcp"]
    }
  }
}
```

## Claude CLI

Pointez la CLI vers une configuration :

```sh
claude --mcp-config <(cat <<'JSON'
{
  "mcpServers": {
    "rousseau": {
      "command": "rousseau",
      "args": ["mcp"]
    }
  }
}
JSON
)
```

Ou inscrivez-le dans `~/.claude/config.json` sous un bloc `mcpServers` avec la même forme.

## Continue.dev

Ajoutez à `~/.continue/config.json` :

```json
{
  "mcpServers": [
    {
      "name": "rousseau",
      "command": "rousseau",
      "args": ["mcp"]
    }
  ]
}
```

Continue capte les outils au prochain appel modèle.

## Cursor

Cursor expose l'enregistrement MCP dans son interface Settings > MCP. Enregistrez un nouveau serveur nommé `rousseau` avec la commande `rousseau` et les args `mcp`. Aucune édition de fichier de configuration requise.

## Codeium

Le support MCP de Codeium est livré derrière un feature flag dans les versions récentes de l'extension IDE. Consultez la documentation de l'extension — l'enregistrement est là encore une paire `command / args`.

## Variables d'environnement et secrets

Comme la surface MCP de rousseau est en lecture seule sur le magasin de sessions, elle n'a pas besoin d'identifiants de fournisseur. `ANTHROPIC_API_KEY` et consorts ne sont pas utilisés par `rousseau mcp` — uniquement par les démons transport / chat qui _génèrent_ les sessions.

## Problèmes courants

- **« Le serveur s'est arrêté immédiatement. »** La commande `mcp` de rousseau ouvre `state.path`. Si le fichier n'est pas inscriptible, le processus sort en non-zéro. Exécutez `rousseau mcp` depuis un shell pour voir l'erreur exacte.
- **« Outil inconnu : rousseau_search_sessions. »** L'hôte a mis en cache une ancienne liste d'outils. Redémarrez l'hôte.
- **Enregistrement dupliqué.** Si deux serveurs rousseau sont enregistrés sous le même nom, seul le dernier l'emporte.

## Ressources et prompts

`resources/list` et `prompts/list` renvoient actuellement du vide. La page [Exposed resources](/fr/mcp/exposed-resources/) suit la feuille de route pour exposer les sessions en tant que ressources MCP.

## Voir aussi

- [MCP](/fr/mcp/) — la référence globale.
- [MCP: Exposed tools](/fr/mcp/exposed-tools/) — chaque signature d'outil.
- [MCP: Exposed resources](/fr/mcp/exposed-resources/) — feuille de route.
- [Tutorial: Expose tools via MCP](/fr/tutorials/expose-tools-via-mcp/) — exemple pratique.
