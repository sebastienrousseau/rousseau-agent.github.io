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
description: "Architecture overview of rousseau-agent: agent loop, transport interface, tool registry, approval policies, SQLite session store, MCP server, cron scheduler, skills loader."
keywords: "architecture, agent loop, session, transport, tool registry, approval, MCP, cron, skills, compression, FTS5"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/concepts/"
subtitle: "Comment la boucle d'agent, les transports et le magasin de sessions s'articulent."
tags: "architecture, agent, session, mcp"
title: "Concepts"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "architecture, agent loop, session, transport, tool registry, approval, MCP, cron, skills, compression, FTS5"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Concepts"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "concepts"
order: 3
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/concepts/index.html"
item_link: "https://docs.rousseau-agent.dev/concepts/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Concepts"
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
twitter_description: "Architecture overview of rousseau-agent: agent loop, transport interface, tool registry, approval policies, SQLite session store, MCP server, cron scheduler, skills loader."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Concepts"
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

## Architecture en couches

```
+---------------------------------------------------------------+
|                             CLI                              |
|  chat  whatsapp  slack  discord  ...  mcp  cron  skills      |
+-------------------------+-------------------------------------+
                          |
+-------------------------v-------------------------------------+
|                          Router                              |
|          (per-JID session, allowlist, dispatch)              |
+-------------+---------------------------+---------------------+
              |                           |
     Transport interface           agent.Agent
     Start / Stop / Deliver        Turn / TurnStream
              |                           |
   +----------+----------+       +--------+--------+
   | 9 concrete adapters |       | Provider iface  |
   +---------------------+       | 5 concrete impls|
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 | Tools Registry  |
                                 | read/write/edit |
                                 | grep/bash + ext |
                                 +--------+--------+
                                          |
                                 +--------v--------+
                                 |  State (SQLite) |
                                 | sessions, cron, |
                                 | jidmap, FTS5    |
                                 +-----------------+
```

Le package `agent` ne dépend que des interfaces exposées par `tools`, de ses propres types `Provider` et de la bibliothèque standard. Les providers, stores et transports concrets dépendent d'`agent` — jamais l'inverse.

## La boucle d'agent

`Session → Turn → Provider → aller-retour tool-use`. Chaque message utilisateur devient un appel à `Agent.Turn` :

1. **Vérification de compression.** Le `Compressor` configuré a l'occasion de réécrire la session avant que le tour ne démarre. S'il agit, `Request.CacheableMessages` est positionné pour que le bloc de résumé soit mis en cache dès le tour suivant.
2. **Appendice skills.** Si un `SkillsProvider` est configuré, il inspecte le dernier message utilisateur et retourne du texte à insérer dans le system prompt.
3. **Appendice recall.** Si un `RecallProvider` est configuré, il interroge l'index FTS5 à travers les sessions passées et retourne du texte à insérer.
4. **Appel provider.** L'implémentation `Provider.Complete` retourne une `Response` avec un `StopReason`.
5. **Dispatch tool-use.** Si `StopReason == StopToolUse`, chaque appel d'outil demandé est envoyé à l'`Approver`. Les refus deviennent des erreurs `tool_result` pour que le modèle puisse s'adapter. Les appels autorisés sont exécutés contre le `Registry` et leurs sorties rejouées à l'itération suivante.
6. **Fin de tour.** Boucle jusqu'à `StopReason == StopEndTurn` ou l'atteinte de `MaxIterations` (32 par défaut).

`internal/agent/agent.go` est la référence canonique.

## Transports

Chaque transport implémente `transport.Transport` :

```go
type Transport interface {
    Name() string
    Start(ctx context.Context, handler Handler) error
    Stop() error
}
```

`Handler.Handle` reçoit un `IncomingMessage` (`From`, `Body`, `At`) et retourne le texte de la réponse. Le `Router` se place au-dessus du transport et prend en charge l'isolation des sessions par expéditeur, l'application de l'allowlist et le dispatch vers l'`Agent`.

Aucun des transports livrés n'expose de surface HTTP publique par défaut. Slack utilise Socket Mode (WebSocket sortant). Discord utilise Gateway (WebSocket sortant). Signal est un sous-processus. WhatsApp emploie le protocole Web de Meta sur TCP. Matrix, Telegram, iMessage et email fonctionnent par polling. SMS est en envoi uniquement car le côté entrant nécessiterait un webhook.

## Registre d'outils

`internal/tools` définit l'interface `Tool` et un `Registry` sûr en concurrence. Les outils intégrés vivent dans `internal/tools/builtin/` :

- `read` — lecture de fichier.
- `write` — écriture de fichier.
- `edit` — remplacement de chaîne avec exigence de correspondance unique pour éviter les remplacements en masse accidentels.
- `grep` — recherche textuelle.
- `bash` — exécution de commande. **La frontière de sécurité porteuse.**

Chaque outil déclare un schéma JSON strict. Ajouter un outil se résume à un appel `registry.MustRegister(myTool)` au câblage ; le cœur de l'agent ne change pas.

## Politiques d'approbation

Chaque appel d'outil passe par `Approver.Approve` avant exécution. Trois politiques intégrées vivent dans `internal/agent/approver.go` :

| Mode | Comportement |
|---|---|
| `allow_all` | Tous les appels s'exécutent. Pertinent avec le provider `claudecli`, qui gère ses propres approbations. |
| `deny_all` | Tous les appels sont bloqués. Utile pour les smoke tests et les sessions en lecture seule. |
| `pattern` | Règles regex allow / deny par outil. Deny l'emporte sur allow. Les requêtes non couvertes retombent sur `Default` (`allow` ou `deny`). |

Les motifs de refus sont renvoyés au modèle sous forme d'erreurs `tool_result`, ce qui lui donne l'occasion de s'adapter au lieu d'échouer silencieusement.

## Magasin de sessions

`internal/state/sqlite/` implémente l'interface `state.Store` sur `modernc.org/sqlite` — Go pur, sans libc, sans CGo. Fonctionnalités :

- **Journalisation WAL** avec `busy_timeout=15s`.
- **Checkpoint WAL à la fermeture** pour que le fichier de base principal reste cohérent pour les sauvegardes.
- **Table de recall FTS5** qui indexe chaque message ; le `RecallProvider` effectue des lookups cross-sessions.
- **Table JID map** qui normalise les identités LID WhatsApp en JID téléphoniques.
- **Table cron** qui persiste les jobs planifiés à travers les redémarrages.

## Serveur MCP

`internal/mcp/server.go` est un serveur JSON-RPC 2.0 sur stdio, révision de spec **2024-11-05**. `rousseau mcp` le démarre. Enregistrez les outils avec `server.Register(mcp.ToolSpec{...})` et laissez un client (Claude Desktop, une extension IDE, un autre agent) les piloter.

Les échecs d'outils sont remontés via le canal `content` avec `isError=true`, pas via le canal d'erreur JSON-RPC — c'est ce qu'attendent les hôtes MCP.

## Scheduler cron

`internal/cron/scheduler.go` encapsule `robfig/cron/v3`. Les jobs sont stockés en SQLite pour survivre aux redémarrages. Chaque déclenchement appelle `Runner.RunOnce(ctx, prompt)` (un tour d'agent one-shot contre une session neuve), puis transmet la réponse à `Delivery` — une fonction indépendante du transport qui livre le message.

Les nouveaux jobs ajoutés via `rousseau cron add` deviennent actifs sous le prochain `PollInterval` (60 s par défaut).

## Loader de skills

`internal/skills/skills.go` parcourt `skills_dir` à la recherche de fichiers `*.md`. Chaque fichier peut porter un front-matter YAML déclarant `name`, `description` et `triggers`. Lorsqu'un trigger apparaît dans le message utilisateur courant, le corps du skill est inséré dans le system prompt pour ce tour. Le format est délibérément proche de la convention [agentskills.io](https://agentskills.io).

## Compression

`internal/agent/compressor.go` déclenche une synthèse par LLM dès que la session franchit `TriggerMessages` (60 par défaut). Les `KeepRecent` messages les plus récents (8 par défaut) sont conservés tels quels ; tout le reste plus ancien est condensé en un unique bloc de résumé. Désactivé par défaut car un compte `claudecli` en abonnement en a rarement besoin ; activez-la avec des fournisseurs facturés à l'usage.

## Où aller ensuite

- [Référence de configuration](/fr/configuration/) — chaque champ.
- [Référence agent-loop](/fr/agent-loop/) — contrat d'embarquement en bibliothèque.
- [MCP](/fr/mcp/) — câblage côté client.
