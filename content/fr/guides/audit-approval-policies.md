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
description: "Worked example: lock down the bash tool with a pattern-mode approver, deny rules on destructive commands, and slog-driven audit trail."
keywords: "approval policy, pattern mode, bash tool, deny rules, audit trail, slog"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/guides/audit-approval-policies/"
subtitle: "Pattern-mode approver with deny rules on the bash tool."
tags: "guides, audit, approval, pattern-mode, bash, deny"
title: "Guide : audit + politiques d'approbation"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approval policy, pattern mode, bash tool, deny rules, audit trail, slog"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : audit + politiques d'approbation"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 34
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/audit-approval-policies/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/audit-approval-policies/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guide : audit + politiques d'approbation"
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
twitter_description: "Worked example: lock down the bash tool with a pattern-mode approver, deny rules on destructive commands, and slog-driven audit trail."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide : audit + politiques d'approbation"
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

## Le problème

Un démon de transport chat non-supervisé n'a personne au terminal pour approuver les appels d'outils en temps réel. Si le modèle veut exécuter `rm -rf /workspace/*`, quelque chose doit l'arrêter. L'approbateur en mode `pattern` de rousseau est ce levier.

La menace n'est pas que le modèle devienne fou — c'est une instruction compromise ou mal alignée atteignant le démon via le canal de transport. Une politique en mode pattern avec un fallback `default: deny` rend le risque borné et auditable.

## Modes d'approbateur

Trois modes intégrés sont livrés (voir `internal/agent/approver.go`) :

| Mode | Comportement | Quand l'utiliser |
|---|---|---|
| `allow_all` | Chaque appel d'outil s'exécute. | `rousseau chat` interactif où le fournisseur `claudecli` fait ses propres approbations. |
| `deny_all` | Chaque appel d'outil est bloqué. Les raisons de refus sont remontées au modèle comme des erreurs `tool_result` pour qu'il puisse s'adapter. | Posture d'inspection read-only ; tests de fumée. |
| `pattern` | Règles regex allow / deny par outil. **Deny gagne sur allow.** Les requêtes non correspondantes retombent sur `default`. | Tout démon non-supervisé en production. |

## Configuration éprouvée

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by pattern policy — ask the operator"
    allow:
      # Outils lecture : aucune restriction dans le workspace.
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

      # Édition uniquement dans /workspace.
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}

      # Écriture uniquement dans /workspace.
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}

      # Commandes shell : whitelist d'utilitaires de lecture sûrs plus git status/diff.
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|grep|rg|find|wc|stat|file|which|pwd|env|git status|git diff|git log|go test|go vet|go build)\\b"}

    deny:
      # Règles de deny absolues qui prévalent sur tout allow ci-dessus.
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s|ncat"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}   # bombe fork
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit, match: "\"path\":\"/etc/|/root/|/var/"}
```

Deux propriétés importantes découlent de `PatternApprover.Approve` :

1. **Deny gagne.** Chaque règle deny est vérifiée avant toute règle allow. C'est plus sûr que l'inverse : un opérateur ajoutant un allow large ne peut jamais accidentellement débloquer une catégorie qu'il croyait refusée.
2. **Non-correspondance → deny.** Avec `default: deny`, tout appel d'outil que l'opérateur a oublié d'énumérer est bloqué. C'est la disposition sûre par défaut ; si vous voulez l'inverse, mettez `default: allow`.

## Lire la piste d'audit

Chaque appel d'outil et chaque refus est émis via le logger slog :

```
INFO tool.execute name=read id=t_1
INFO tool.execute name=grep id=t_2
WARN tool.denied  name=bash reason="denied by pattern policy — ask the operator"
```

Le démon utilise `slog` avec un niveau et un format configurables (`log.level`, `log.format`). Pour la production, préférez `format: json` afin que les outils en aval (Loki, Vector, Datadog) parsent proprement. Voir [Guides: Observability](/fr/guides/observability/) pour la recette de pipeline.

Chaque refus porte une clé structurée stable :

- `tool.denied` — l'appel d'outil a été bloqué. Champs : `name` (identifiant d'outil), `reason` (depuis `PatternApprover.DenyReason` ou le fallback intégré).
- `tool.execute` — l'appel d'outil s'est exécuté. Champs : `name`, `id` (l'ID d'appel émis par le modèle pour corrélation).
- `tool.error` — l'outil s'est exécuté mais a échoué. Champs : `name`, `err`.

Un filtre `slog` sur `tool.denied` vous donne la vue « tentatives bloquées » que la plupart des cadres de conformité demandent.

## Tester la politique

`internal/agent/approver_test.go` dans l'arborescence source exerce le `PatternApprover` avec une large matrice. Pour tester vos propres règles à vide :

```sh
rousseau chat
> Run `rm -rf /tmp/foo` for me.
```

Le modèle tentera l'appel d'outil `bash`. Le démon journalise `tool.denied` et renvoie la chaîne `reason` au modèle, qui pivotera habituellement (« Je ne peux pas exécuter ça — pourriez-vous me dire ce que vous cherchiez à faire ? »).

Pour la matrice de test de référence, voir `internal/agent/approver_test.go` — les mêmes formes de règles y sont exercées.

## Ajouter une surcharge manuelle

Parfois, un opérateur veut approuver manuellement un unique appel dangereux. Le motif le plus simple :

1. Définir `mode: allow_all` dans `rousseau chat` (TUI interactif). Le fournisseur `claudecli` gère ses propres prompts d'approbation par appel.
2. Garder `mode: pattern` dans chaque démon non-supervisé.

Il n'existe pas d'interface d'approbation interactive par appel sur les transports chat aujourd'hui — le récit de sécurité est entièrement regex + slog.

## Ce que la politique ne fait pas

- **Ne bac-à-sable pas l'outil.** Un appel `bash` qui survit à l'approbateur s'exécute avec l'UID du démon et sa visibilité du système de fichiers. Superposez un conteneur rootless ([Deployment](/fr/deployment/)) en dessous.
- **Ne limite pas le débit.** Dix appels `bash` autorisés par seconde sont permis. Si vous avez besoin de rate limiting, enveloppez le registre d'outils.
- **N'audite pas les appels réseau sortants.** Si une invocation `bash` fait un curl sortant, l'approbateur ne verra pas l'URL — uniquement la chaîne `command` initiale de `bash`. Refusez purement `curl` et `wget` au niveau pattern.

## Motifs courants

### Restreindre l'édition à une arborescence de répertoires

```yaml
allow:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/[^\"]*\""}
  - {tool: write, match: "\"path\":\"/workspace/repo/[^\"]*\""}
deny:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/(\\.git|node_modules|vendor)/"}
```

### Auditeur en lecture seule

```yaml
mode: pattern
default: deny
allow:
  - {tool: read, match: ".*"}
  - {tool: grep, match: ".*"}
```

Combiné avec `provider.claudecli.permission_mode: plan`, cela donne une posture d'inspection read-only — voir [Guides: Read-only Mode](/fr/guides/read-only-mode/).

### Flux de travail git-first

```yaml
allow:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"git (status|diff|log|show|branch|stash|fetch|pull --ff-only)\\b"}
deny:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"git (push|reset --hard|clean -fd|checkout --)\\b"}
```

## Cinq jeux de règles de référence

<div class="tabs" data-tabs="approval-rulesets">
  <div class="tab-list" role="tablist" aria-label="Reference ruleset">
    <button role="tab" aria-selected="true">Poste dev</button>
    <button role="tab" aria-selected="false">Staging</button>
    <button role="tab" aria-selected="false">Production</button>
    <button role="tab" aria-selected="false">Bot d'astreinte</button>
    <button role="tab" aria-selected="false">Lecture seule</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Poste dev.** Permissif par défaut, refuse les vraies dangers. Suppose un terminal supervisé.

```yaml
agent:
  approver:
    mode: pattern
    default: allow
    deny:
      - {tool: bash, match: "rm\\s+-rf\\s+/"}
      - {tool: bash, match: "sudo(?!\\s+-n)"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}
      - {tool: write, match: "\"path\":\"/etc/|/root/"}
      - {tool: edit, match: "\"path\":\"/etc/|/root/"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Staging.** Liste allow explicite pour le workspace, refus de tout le reste. Adapté à un démon staging partagé avec un rayon d'explosion limité.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by staging policy — ping #platform for exceptions"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: bash, match: "^\\{\"command\":\"git (status|diff|log|show|branch|fetch|pull --ff-only)\\b"}
      - {tool: bash, match: "^\\{\"command\":\"(ls|cat|grep|rg|find)\\s"}
    deny:
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s"}
      - {tool: edit, match: "\"path\":\"/workspace/(\\.git|node_modules|vendor)/"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Production.** Deny-first. Chaque commande autorisée est énumérée explicitement. Adapté à un démon de production répondant à des questions client.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by production policy — this daemon is read-mostly"
    # Ce démon est presque exclusivement en lecture.
    allow:
      - {tool: read, match: "\"path\":\"/workspace/(runbooks|docs|src)/"}
      - {tool: grep, match: "\"path\":\"/workspace/(runbooks|docs|src)/"}
      - {tool: bash, match: "^\\{\"command\":\"(ls|cat|rg)\\s"}
    deny:
      # Refus superposés par sécurité.
      - {tool: write, match: ".*"}
      - {tool: edit, match: ".*"}
      - {tool: bash, match: "\\b(rm|mv|cp|dd|mkfs|kill|killall)\\b"}
      - {tool: bash, match: "\\b(curl|wget|nc|ncat|ssh|scp|rsync)\\b"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Bot d'astreinte.** Peut interroger le monitoring, tailer les logs, mais pas redémarrer les services ni éditer du code. Adapté à un assistant de réponse à incident tourné Slack.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied — oncall bot can query, not mutate"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\{\"command\":\"(kubectl|helm|argocd) (get|describe|logs|top|status)\\b"}
      - {tool: bash, match: "^\\{\"command\":\"(curl|http|wget) -[gsL]* https?://monitoring\\."}
      - {tool: bash, match: "^\\{\"command\":\"(pg_dump|psql -c 'SELECT|redis-cli GET)\\b"}
    deny:
      - {tool: write, match: ".*"}
      - {tool: edit, match: ".*"}
      - {tool: bash, match: "\\b(kubectl (apply|delete|edit|scale)|helm (install|upgrade|uninstall))\\b"}
      - {tool: bash, match: "\\b(systemctl (start|stop|restart|reload))\\b"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Auditeur en lecture seule.** Pas d'écritures, pas de shell. Adapté à un bot de revue de code ou à un démon d'explication de documentation.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "read-only auditor — no side effects permitted"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
```

Combinez avec `provider.claudecli.permission_mode: plan` et `provider.claudecli.extra_args: ["--allowed-tools", "read,grep"]` pour une application ceinture-bretelles — le modèle ne peut littéralement pas demander d'autres outils.

  </div>
</div>

## Dépannage

### Chaque appel est refusé alors que j'ai des règles allow

Deny gagne sur allow. Vérifiez si l'une de vos règles deny correspond involontairement. La ligne de log `tool.denied name=<X> reason=<Y>` inclut la raison exacte.

### Erreur de compilation d'un regex pattern

`PatternApprover` compile paresseusement les règles à la première utilisation. Une erreur de compilation devient un `DecisionDeny` avec la raison `approver: pattern compile: <err>`. Corrigez le regex ; regex101.com avec la saveur Go sélectionnée est votre ami.

### Le regex correspond au JSON littéralement, pas sémantiquement

Le regex `match` s'exécute contre l'entrée JSON brute de l'appel d'outil. Échappez les guillemets et les barres obliques inverses de manière appropriée : `"\"path\":\"/workspace/"` correspond au champ `path` d'un appel `edit` ou `write`.

### `deny_all` ne bloque rien

Confirmez `mode: deny_all` (pas `mode: deny`). Les modes valides sont `allow_all`, `deny_all`, `pattern`. `allow` et `deny` seuls sont traités comme alias des variantes `_all` mais les chaînes exactes sont plus sûres.

### Une règle allow pour `bash` ne correspond jamais

L'entrée `bash` est du JSON comme `{"command":"ls -la"}`. Faites correspondre contre ce littéral JSON, pas seulement la chaîne de commande shell. Utilisez un motif comme `^\\{\"command\":\"ls`.

## Pages liées

- [User Guide: Approval Policies](/fr/user-guide/approval-policies/) — référence approfondie et exemples pratiques.
- [User Guide: Tools](/fr/user-guide/tools/) — schéma de chaque outil intégré.
- [Guides: Observability](/fr/guides/observability/) — faire remonter la piste d'audit.
- [Guides: Read-only mode](/fr/guides/read-only-mode/) — application ceinture-bretelles.
- [Security](/fr/security/) — vue d'ensemble du modèle de confiance.

## Lecture complémentaire

- `internal/agent/approver.go` — `PatternApprover`, `AllowAllApprover`, `DenyAllApprover`.
- `internal/agent/approver_test.go` — matrice de tests.
- `internal/cli/approver.go` — traduction configuration → approbateur.
- `internal/config/config.go` — `ApproverConfig`, `PatternEntry`.
