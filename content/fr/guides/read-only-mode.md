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
description: "Configure rousseau-agent as a read-only inspection agent: deny_all approver with a read/grep exception, plan-mode claudecli, read-only bind mounts."
keywords: "read-only, inspection, deny_all, plan mode, bind mount, ro mount, audit"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/guides/read-only-mode/"
subtitle: "An inspection posture that cannot mutate the workspace."
tags: "guides, read-only, deny_all, plan-mode"
title: "Guide : mode lecture seule"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "read-only, inspection, deny_all, plan mode, bind mount, ro mount, audit"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : mode lecture seule"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 36
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/read-only-mode/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/read-only-mode/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guide : mode lecture seule"
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
twitter_description: "Configure rousseau-agent as a read-only inspection agent: deny_all approver with a read/grep exception, plan-mode claudecli, read-only bind mounts."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide : mode lecture seule"
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

## Scénario

Vous voulez que rousseau inspecte un dépôt, réponde aux questions le concernant et produise des rapports — mais il ne doit pas pouvoir écrire, éditer ni exécuter de commandes shell destructrices. C'est la posture que vous déploieriez pour un audit en première passe, une inspection de réponse à incident ou une revue de conformité.

Trois couches s'empilent pour rendre cela difficile :

1. **Politique d'approbation** — refuser chaque outil mutant.
2. **Mode de permission `claudecli`** — placer Claude Code en mode `plan` afin que son propre approbateur n'édite jamais de fichier.
3. **Système de fichiers** — bind-mount du workspace en lecture seule.

Ceinture, bretelles et une seconde ceinture. Chacune des trois échoue en sécurité.

## Couche 1 — Approbateur

La posture read-only la plus simple utilise l'approbateur `pattern` avec une whitelist :

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "read-only inspection posture — this deployment cannot mutate files"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|find|wc|stat|file|which|pwd|env|git status|git diff|git log|git show|git branch)\\b"}
    # Aucune règle deny nécessaire — default: deny attrape tout le reste.
    # Pas d'edit, de write ni de bash sans restriction — le modèle n'y accède pas.
```

Une variante encore plus stricte utilise `deny_all`, qui bloque chaque outil y compris `read` et `grep` :

```yaml
agent:
  approver:
    mode: deny_all
    reason: "smoke test — no tool calls allowed"
```

`deny_all` n'est utile qu'en tant que test de fumée ; le modèle ne pourra pas produire de travail utile.

## Couche 2 — Mode de permission `claudecli`

Quand le fournisseur est `claudecli`, c'est Claude Code lui-même qui exécute les appels d'outils. Définir `permission_mode: plan` fait refuser à Claude Code chaque appel d'écriture ou d'édition dans sa propre couche, même si l'approbateur rousseau l'aurait autorisé :

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: plan
```

Valeurs valides (voir `internal/config/config.go` et la documentation de Claude Code) : `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. `plan` est la seule valeur qui maintient de manière fiable Claude Code en posture read-only.

## Couche 3 — Système de fichiers

Montez le workspace en lecture seule. Sous le Quadlet Podman de référence :

```
Volume=%h/team-rousseau-workspace:/workspace:ro,Z
```

`ro` rend le montage en lecture seule du point de vue du conteneur ; même si un binaire compromis tentait d'`open(2)` avec `O_WRONLY`, le noyau renverrait `EROFS`.

Sous Kubernetes :

```yaml
volumeMounts:
  - name: workspace
    mountPath: /workspace
    readOnly: true
```

Le magasin de sessions (`~/.local/share/rousseau/`) doit rester inscriptible — le démon y ajoute des entrées à chaque tour. Gardez ce montage en `rw` et ne laissez que le workspace en lecture seule.

## Posture dry-run

Il n'existe pas de flag `--dry-run` sur le démon. Si vous voulez que le modèle *planifie* des modifications sans les exécuter, la combinaison ci-dessus atteint l'équivalent :

- L'approbateur bloque chaque outil mutant → le modèle reçoit une erreur `tool_result` expliquant le blocage.
- Le mode `plan` dans `claudecli` empêche Claude Code d'exécuter ses propres outils destructeurs.
- Les montages read-only arrêtent tout ce qui passerait au travers.

Le modèle répondra typiquement par un document de plan plutôt qu'un diff. C'est le livrable d'inspection read-only.

## Ce qui fonctionne encore

- Chaque appel `read` et `grep`.
- `bash` pour les utilitaires de lecture sûrs que vous avez énumérés.
- La persistance de session — le magasin SQLite continue d'enregistrer la conversation.
- Le recall inter-session via FTS5, l'export MCP, les skills — tous en lecture seule de toute façon.

## Ce qui casse (intentionnellement)

- `write` et `edit` — refusés.
- Commandes shell de mutation — refusées.
- Jobs cron dont le prompt implique des écritures fichier — le modèle essaie, est refusé, répond par un plan.
- `rousseau init` — la CLI n'est pas affectée par l'approbateur, mais elle écrit dans `~/.config/rousseau/` hors workspace. Exécutez-la avant de déployer le mode read-only.

## Tester la posture

```sh
rousseau chat
> Edit /workspace/README.md to add a footer.
```

Ligne de log attendue :

```
WARN tool.denied name=edit reason="read-only inspection posture — this deployment cannot mutate files"
```

Réponse chat attendue : le modèle s'excuse, produit un plan ou un patch diff en texte, et demande à l'opérateur de l'appliquer.

Pour la variante `deny_all`, chaque appel d'outil est bloqué — le modèle n'a aucun moyen d'inspecter quoi que ce soit, donc cette posture n'est utile qu'en test de fumée.

## Superposition avec d'autres transports

Les trois mêmes couches s'appliquent à WhatsApp, Slack, Discord et tout autre transport. Puisque l'approbateur tourne à l'intérieur de la boucle d'agent, il ne se soucie pas de quel transport a livré le tour utilisateur. Un agent Slack read-only est à un bloc `mode: pattern` près.

## Précautions

- La posture read-only est appliquée par l'approbateur de rousseau et par le système de fichiers — **pas** par le LLM. Un modèle peut toujours émettre un appel `edit` ; l'approbateur le bloque silencieusement, mais la tentative est journalisée comme `tool.denied`. C'est intentionnel afin que les pistes d'audit consignent ce que le modèle a tenté, pas seulement ce qui a réussi.
- Les bind mounts en lecture seule ne protègent pas contre les liens symboliques pointant hors du mount. La posture Podman de référence retire toutes les capacités, ce qui empêche la plupart des chemins d'évasion, mais ne comptez pas sur le seul mount.
- Le mode `plan` du fournisseur `claudecli` est un contrat de Claude Code, pas de rousseau. Si Claude Code change la sémantique de son mode de permission, la posture read-only de rousseau hérite de ce changement.

## Suite

- [User Guide: Approval Policies](/fr/user-guide/approval-policies/) — référence approfondie.
- [Audit + approval policies](/fr/guides/audit-approval-policies/) — le pendant mutant.
- [Deployment](/fr/deployment/) — flags de mount et de conteneur.
