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
description: "rousseau-agent's MCP server exposes its tools and sessions over stdio JSON-RPC. Compatible with Claude Desktop and any MCP host."
keywords: "MCP, Model Context Protocol, JSON-RPC, stdio, Claude Desktop, tools, sessions"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/mcp/"
subtitle: "JSON-RPC 2.0 sur stdio, révision de spéc. 2024-11-05."
tags: "MCP, reference"
title: "Serveur MCP"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "MCP, Model Context Protocol, JSON-RPC, stdio, Claude Desktop, tools, sessions"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Serveur MCP"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 21
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/mcp/index.html"
item_link: "https://docs.rousseau-agent.dev/mcp/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Serveur MCP"
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
twitter_description: "rousseau-agent's MCP server exposes its tools and sessions over stdio JSON-RPC. Compatible with Claude Desktop and any MCP host."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Serveur MCP"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>Le format filaire JSON-RPC 2.0 complet que parle rousseau, chaque méthode implémentée par le serveur MCP de rousseau avec des exemples de couples requête/réponse, la sémantique des codes d'erreur, et comment configurer Claude Desktop / Cursor / les hôtes MCP d'IDE pour atteindre le serveur. Lisez <code>internal/mcp/protocol.go</code> et <code>internal/mcp/server.go</code> en parallèle de cette page.</p></aside>

## Format filaire

`rousseau mcp` démarre un serveur MCP qui parle JSON-RPC 2.0 sur stdio, conformément à la [spécification du Model Context Protocol](https://modelcontextprotocol.io) révision **2024-11-05** (déclarée dans `ProtocolVersion` de `internal/mcp/protocol.go`).

- Une requête par ligne sur stdin (`bufio.Scanner` lit jusqu'à 8 Mio par ligne).
- Une réponse par ligne sur stdout (`json.NewEncoder` émet du JSON délimité par des sauts de ligne).
- Le serveur bloque jusqu'à la fermeture de stdin ou l'annulation de `ctx`.

### Enveloppe JSON-RPC 2.0

Chaque requête, notification et réponse utilise cette enveloppe (depuis `internal/mcp/protocol.go` ligne 38) :

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list",
  "params": {}
}
```

Les champs présents dépendent du type d'enveloppe :

| Champ | Requête | Notification | Réponse |
|---|:---:|:---:|:---:|
| `jsonrpc` | toujours `"2.0"` | toujours `"2.0"` | toujours `"2.0"` |
| `id` | requis | absent | renvoyé depuis la requête |
| `method` | requis | requis | absent |
| `params` | optionnel | optionnel | absent |
| `result` | absent | absent | succès uniquement |
| `error` | absent | absent | échec uniquement |

Les notifications ne portent pas d'`id` et ne reçoivent pas de réponse. rousseau ne reçoit qu'une seule notification (`notifications/initialized`), acceptée silencieusement.

### Référence des méthodes

Le `Server.dispatch` de Rousseau (`internal/mcp/server.go` ligne 112) route ces méthodes :

| Méthode | Rôle | Réponse |
|---|---|---|
| `initialize` | Handshake. Le client déclare la version du protocole et ses capacités. | `InitializeResult` |
| `notifications/initialized` | Le client confirme qu'il est prêt. | (notification, sans réponse) |
| `ping` | Sonde de vivacité. | `{}` |
| `tools/list` | Énumère les outils enregistrés. | `ToolsListResult` |
| `tools/call` | Invoque un outil. | `ToolsCallResult` |
| `resources/list` | Placeholder. Retourne `{ "resources": [] }` aujourd'hui. | `{"resources": []}` |
| `prompts/list` | Placeholder. Retourne `{ "prompts": [] }`. | `{"prompts": []}` |
| `shutdown` | Arrêt initié par le client. | `{}` |

<aside class="admonition" data-type="note"><span class="admonition-title">Méthodes manquantes</span><p><code>resources/list</code> et <code>prompts/list</code> renvoient des tableaux vides pour que les hôtes qui les sondent n'échouent pas. Un support complet des ressources et prompts figure sur la feuille de route — voir <code>docs/GAP_ANALYSIS_2026.md</code>.</p></aside>

## Exemples requête/réponse

### 1. `initialize`

Le client envoie :

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","clientInfo":{"name":"claude-desktop","version":"0.7.0"}}}
```

Le serveur répond :

```json
{"jsonrpc":"2.0","id":1,"result":{"protocolVersion":"2024-11-05","serverInfo":{"name":"rousseau","version":"0.6.0"},"capabilities":{"tools":{"listChanged":false}}}}
```

`listChanged: false` car l'ensemble d'outils de rousseau est statique dès le démarrage du processus — aucun ajout/retrait à l'exécution.

### 2. `tools/list`

```json
{"jsonrpc":"2.0","id":2,"method":"tools/list"}
```

Le serveur répond avec les outils enregistrés dans l'ordre d'insertion :

```json
{"jsonrpc":"2.0","id":2,"result":{"tools":[
  {"name":"read","description":"Read a file...","inputSchema":{"type":"object","properties":{"path":{"type":"string"}},"required":["path"]}},
  {"name":"grep","description":"Search for a regex...","inputSchema":{"type":"object","properties":{"pattern":{"type":"string"},"path":{"type":"string"}},"required":["pattern"]}},
  {"name":"bash","description":"Execute a shell command...","inputSchema":{"type":"object","properties":{"command":{"type":"string"}},"required":["command"]}}
]}}
```

### 3. `tools/call`

```json
{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"read","arguments":{"path":"/etc/hostname"}}}
```

Succès :

```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"my-host.example.com\n"}]}}
```

Échec au niveau du handler (remonté sous forme de contenu, et non d'erreur JSON-RPC — c'est la convention MCP) :

```json
{"jsonrpc":"2.0","id":3,"result":{"content":[{"type":"text","text":"read: open /nope: no such file or directory"}],"isError":true}}
```

### 4. `ping`

```json
{"jsonrpc":"2.0","id":4,"method":"ping"}
```

```json
{"jsonrpc":"2.0","id":4,"result":{}}
```

## Codes d'erreur

Rousseau utilise la plage d'erreurs standard JSON-RPC 2.0 plus une extension MCP :

| Code | Constante | Signification | Quand émis |
|---|---|---|---|
| -32700 | `CodeParseError` | JSON invalide dans l'enveloppe. | L'enveloppe a échoué au `json.Unmarshal`. |
| -32600 | `CodeInvalidRequest` | Forme de l'enveloppe incorrecte. | Le champ `jsonrpc` ne vaut pas `"2.0"`. |
| -32601 | `CodeMethodNotFound` | Méthode non implémentée. | Le dispatch est tombé dans le cas par défaut. |
| -32602 | `CodeInvalidParams` | Échec du décodage des params. | `params` n'a pas pu être unmarshalé vers la forme attendue. |
| -32603 | `CodeInternalError` | Erreur au marshalling de la réponse. | Rare — indique un bug. |
| -32000 | `CodeToolNotFound` | Le nom d'outil n'est pas enregistré. | `tools/call` avec un `name` inconnu. |

<aside class="admonition" data-type="warning"><span class="admonition-title">Erreurs d'outil vs erreurs JSON-RPC</span><p>Les échecs au niveau du handler — commande <code>bash</code> retournant un code non nul, <code>read</code> sur un fichier manquant — sont retournés via <code>result.content</code> avec <code>isError: true</code>, et NON via le champ <code>error</code> JSON-RPC. Seuls les échecs de niveau protocole utilisent <code>error</code>. Les hôtes qui traitent les deux canaux comme équivalents mal classeront les échecs récupérables.</p></aside>

## Ce qui est exposé

Deux surfaces :

- **Outils.** Tout `mcp.ToolSpec` enregistré avant `Serve` est annoncé dans `tools/list` et appelable via `tools/call`. rousseau branche les mêmes implémentations d'outils que la boucle d'agent locale : `read`, `write`, `edit`, `grep`, `bash`.
- **Sessions.** Le store de sessions SQLite de rousseau est exposé pour qu'un hôte MCP puisse énumérer et lire les conversations passées. `resources/list` retourne une entrée par session.

Les échecs d'outils sont remontés via le canal `content` avec `isError=true`, et non via le canal d'erreur JSON-RPC. C'est la convention MCP.

## Configuration client — Claude Desktop

Ajoutez à `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) ou à l'équivalent sur votre plateforme :

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "rousseau",
      "args": ["mcp"],
      "env": {
        "HOME": "/Users/you"
      }
    }
  }
}
```

Redémarrez Claude Desktop. `rousseau` apparaîtra dans la palette d'outils ; chaque outil enregistré est invocable.

Pour un rousseau embarqué dans une image Podman, l'entrée devient :

```json
{
  "mcpServers": {
    "rousseau": {
      "command": "podman",
      "args": [
        "run", "--rm", "-i",
        "-v", "/Users/you/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z",
        "localhost/rousseau-agent:local",
        "mcp"
      ]
    }
  }
}
```

Effectuez un bind-mount du répertoire d'état afin que l'hôte MCP voie les mêmes sessions que le daemon.

## Enregistrer un outil personnalisé

Intégration du serveur MCP dans votre propre binaire :

```go
srv := mcp.NewServer("rousseau", "0.1.0", logger)

srv.MustRegister(mcp.ToolSpec{
    Name:        "count_files",
    Description: "Count files under a path.",
    InputSchema: json.RawMessage(`{
      "type": "object",
      "properties": {"path": {"type": "string"}},
      "required": ["path"]
    }`),
    Handler: func(ctx context.Context, args json.RawMessage) ([]mcp.Content, error) {
        var in struct{ Path string }
        if err := json.Unmarshal(args, &in); err != nil {
            return nil, fmt.Errorf("bad input: %w", err)
        }
        // ... count files ...
        return []mcp.Content{{Type: "text", Text: fmt.Sprintf("%d", n)}}, nil
    },
})

_ = srv.Serve(ctx, os.Stdin, os.Stdout)
```

Les enregistrements en double retournent une erreur ; `MustRegister` panique sur un doublon (réservé au câblage dans `main`).

## Concurrence

`Serve` peut être appelé de manière concurrente sur des transports indépendants (stdin/stdout pour l'hôte MCP, plus un canal de contrôle si vous le souhaitez). La table d'outils du serveur est protégée par un RWMutex ; l'exécution des handlers n'est pas sérialisée — les implémentations doivent être sûres pour une utilisation concurrente.

## Débogage

Chaque enveloppe requête/réponse est journalisée au niveau `debug` par défaut. Activez avec :

```yaml
log:
  level: debug
  format: text
```

Or:

```sh
ROUSSEAU_LOG_LEVEL=debug rousseau mcp 2>/tmp/mcp.log
```

L'hôte MCP consomme stdout ; conservez le flux de logs sur stderr.

## Dépannage

### Claude Desktop / Cursor n'affiche jamais les outils rousseau

Il s'agit presque toujours d'une erreur de câblage, et non d'un problème rousseau. Vérifiez : (1) que `command` et `args` dans la configuration hôte invoquent `rousseau mcp` (et non `rousseau chat`) ; (2) que le fichier de configuration a bien été sauvegardé et l'hôte redémarré ; (3) que `rousseau mcp </dev/null` depuis un shell ne plante pas — si oui, corrigez cela d'abord.

### `parse error` sur le tout premier message

L'hôte n'envoie pas de JSON délimité par des lignes. Certaines implémentations MCP précoces envoient des messages framés (`Content-Length: N\r\n\r\n<body>`) ; rousseau attend une délimitation par `\n`. Mettez à jour l'hôte vers une build utilisant le framing stdio (tous les hôtes majeurs actuels le font).

### `method not found: <foo>`

L'hôte appelle une méthode que rousseau n'implémente pas. `resources/list` et `prompts/list` vides sont fournis en no-op pour les sondes courantes ; toute autre méthode renvoie `-32601`. Consultez `dispatch()` dans `internal/mcp/server.go` pour la liste complète des méthodes.

### Les appels d'outils réussissent mais l'hôte les signale comme des erreurs

Le handler d'outil a retourné l'erreur par le mauvais canal. Les handlers doivent retourner `[]Content{{Type: "text", Text: err.Error()}}, err != nil` — rousseau capture l'erreur et l'enveloppe dans `isError: true`. Ne retournez pas l'erreur via le canal `error` JSON-RPC à moins qu'il ne s'agisse d'un échec de niveau protocole.

### Le MCP conteneurisé échoue avec `permission denied` sur le répertoire d'état

L'invocation `podman run` depuis Claude Desktop doit inclure un `-v` pour le répertoire d'état avec le bon label SELinux. Utilisez `:Z` (privé) à moins que le conteneur ne soit partagé avec d'autres charges Podman. Vérifiez également que l'UID hôte à l'intérieur du conteneur correspond aux propriétaires des fichiers.

## Pages liées

- [MCP : Outils exposés](/fr/mcp/exposed-tools/) — l'ensemble d'outils que rousseau publie.
- [MCP : Ressources exposées](/fr/mcp/exposed-resources/) — énumération et lecture de sessions.
- [MCP : Compatibilité](/fr/mcp/compatibility/) — matrice des hôtes testés.
- [Tutoriels : Exposer des outils via MCP](/fr/tutorials/expose-tools-via-mcp/) — parcours de bout en bout.
- [Boucle d'agent](/fr/agent-loop/) — comment les mêmes outils sont utilisés à l'intérieur de rousseau.

## Lectures complémentaires

- `internal/mcp/protocol.go` — enveloppe, noms de méthodes, codes d'erreur.
- `internal/mcp/server.go` — `Serve`, `dispatch`, registre d'outils.
- `internal/mcp/tools.go` — helpers pour enregistrer les outils intégrés de rousseau.
- `internal/cli/mcp.go` — câblage de la commande `rousseau mcp`.
- [Spécification du Model Context Protocol](https://modelcontextprotocol.io) — référence externe.
