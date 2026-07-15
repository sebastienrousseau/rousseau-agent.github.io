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
description: "Go from bypassPermissions to a pattern-mode approver with default: deny and validate the audit trail through slog."
keywords: "approver, pattern mode, default deny, tool denied, audit, slog"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/tutorials/harden-approver-policy/"
subtitle: "From bypassPermissions to default-deny with slog-audited rule matching."
tags: "tutorials, approver, pattern-mode, security, audit"
title: "Tutoriel : durcir l'approbateur"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approver, pattern mode, default deny, tool denied, audit, slog"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutoriel : durcir l'approbateur"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 46
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/harden-approver-policy/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/harden-approver-policy/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutoriel : durcir l'approbateur"
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
twitter_description: "Go from bypassPermissions to a pattern-mode approver with default: deny and validate the audit trail through slog."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutoriel : durcir l'approbateur"
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

Un démon rousseau qui a démarré en exécutant le fournisseur `claudecli` en mode `bypassPermissions` (le défaut sans surveillance) se retrouve sous un approbateur rousseau-agent en mode `pattern` avec `default: deny`. Chaque appel d'outil est soit explicitement autorisé, soit bloqué ; chaque refus produit un événement slog `tool.denied` que vous pouvez auditer.

Temps estimé : 30 minutes pour une passe de règles correcte avec tests.

## Prérequis

- Rousseau installé avec n'importe quel pont de transport en marche (WhatsApp, Slack, Signal — n'importe quoi sans surveillance).
- Familiarité de base avec les regex Go — les règles d'approbateur sont des regex RE2 Go sur le JSON d'entrée d'outil.

## Où vit l'approbateur

Deux couches indépendantes peuvent approuver les appels d'outils :

1. **Le mode de permission propre au fournisseur.** Le fournisseur `claudecli` (`internal/llm/claudecli/client.go`) délègue à `claude --permission-mode`. Valeurs documentées dans `ClaudeCLIConfig.PermissionMode` (`internal/config/config.go`) : `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. Les démons sans surveillance épinglent `bypassPermissions` dans `setUnattendedPermissionDefault`.
2. **L'approbateur propre à Rousseau.** Configuré sous `agent.approver` (`internal/config/config.go` `ApproverConfig` ; implémentation dans `internal/agent/approver.go`). Trois modes : `allow_all`, `deny_all`, `pattern`. **Le deny l'emporte sur le allow, et les appels non correspondants retombent sur `default`.**

Pour un démon sans surveillance, l'approbateur rousseau est la mitigation que vous configurez à la main. Le propre mode de `claudecli` est la ceinture de sécurité.

## Étape 1 : audit de base

Avant d'écrire des règles, exécutez quelques sessions réalistes avec `mode: allow_all` et `log.format: json`. Chaque appel d'outil émet `tool.execute` (`internal/agent/agent.go`) :

```sh
jq -c 'select(.msg == "tool.execute") | {name, input: .input}' \
  < /var/log/rousseau.jsonl \
  | sort | uniq -c | sort -rn | head
```

Vous avez maintenant une distribution empirique des outils que l'agent utilise et contre quels chemins. C'est la graine de l'allowlist.

## Étape 2 : ébaucher une politique pattern

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by pattern policy — ask the operator to loosen the rules"
    allow:
      # Read side: unrestricted within the daemon's filesystem view.
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

      # Editing pinned to /workspace.
      - {tool: edit,  match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}

      # Shell: whitelist of read-only utilities plus git status/diff/log.
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|grep|rg|find|wc|stat|file|which|pwd|env|git status|git diff|git log|go test|go vet|go build)\\b"}

    deny:
      # Absolute denies override any allow above.
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s|ncat"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}    # fork bomb
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit,  match: "\"path\":\"/etc/|/root/|/var/"}
```

Déployez et observez le flux slog. Les événements pertinents (`internal/agent/agent.go`) :

- `tool.execute` — l'appel s'est exécuté. Champs : `name`, `id`.
- `tool.denied` — l'approbateur l'a bloqué. Champs : `name`, `reason`.
- `tool.error` — s'est exécuté et a échoué. Champs : `name`, `err`.

## Étape 3 : itérer

Le premier jour fait remonter les faux positifs : les appels d'outils légitimes que l'approbateur a bloqués. Grepez-les :

```sh
jq -c 'select(.msg == "tool.denied") | {name, input}' \
  < /var/log/rousseau.jsonl \
  | sort | uniq -c | sort -rn | head
```

Chaque `tool.denied` récurrent mérite une décision :

- **Réellement nécessaire** — étendez la règle allow. Préférez restreint (chemin épinglé) plutôt que large (regex ouverte).
- **Pas nécessaire** — laissez refusé. Le modèle pivotera vers une autre approche.

N'affaiblissez pas `default: deny`. C'est la propriété qui rend sûr un outil oublié.

## Étape 4 : extrait de journal d'audit

Une exécution en production avec un prompt inhabituel ressemblait à ça :

```jsonl
{"time":"2026-07-13T18:00:12Z","level":"INFO", "msg":"whatsapp.incoming","from":"447900123456@s.whatsapp.net"}
{"time":"2026-07-13T18:00:14Z","level":"INFO", "msg":"tool.execute","name":"grep","id":"t_1"}
{"time":"2026-07-13T18:00:15Z","level":"INFO", "msg":"tool.execute","name":"read","id":"t_2"}
{"time":"2026-07-13T18:00:17Z","level":"WARN", "msg":"tool.denied","name":"bash","reason":"denied by pattern policy — ask the operator to loosen the rules"}
{"time":"2026-07-13T18:00:18Z","level":"INFO", "msg":"tool.execute","name":"read","id":"t_3"}
{"time":"2026-07-13T18:00:20Z","level":"INFO", "msg":"whatsapp.handler_ok","elapsed":"7.4s"}
```

Le seul `tool.denied` ici était `bash: "curl https://…"`. La règle deny l'a attrapé, le modèle a dégradé vers `read` + `grep`, et la réponse est passée quand même.

## Étape 5 : figer

Une fois le taux de faux positifs stabilisé, gelez la config, commitez-la dans le contrôle de source (secrets exclus — voir [Guides : Enterprise Onboarding](/fr/guides/enterprise-onboarding/)), et conditionnez les changements de config à une revue de code. `internal/agent/approver_test.go` dans l'arborescence source est votre modèle pour écrire des tests contre l'ensemble de règles — copiez sa forme dans un package interne si vous voulez que la CI attrape une politique cassée.

## Ce que la politique ne fait toujours pas

Même avec les règles pattern les plus strictes :

- **Pas de sandboxing.** Un appel `bash` autorisé s'exécute toujours avec l'UID du démon et sa visibilité du système de fichiers. Superposez un conteneur rootless ([Deployment](/fr/deployment/)) en dessous.
- **Pas de rate limiting.** Dix appels autorisés par seconde sont tous autorisés. Wrappez le registre d'outils si vous en avez besoin.
- **Pas d'audit réseau sortant.** L'approbateur voit la chaîne initiale `command` de `bash`, pas ce qu'elle curl. Refusez `curl` et `wget` d'emblée — les règles deny d'exemple le font.

Voir [Guides : Audit + politiques d'approbation](/fr/guides/audit-approval-policies/) pour la discussion approfondie.

## Voir aussi

- [Guide utilisateur : politiques d'approbation](/fr/user-guide/approval-policies/) — référence de chaque mode.
- [Guide utilisateur : outils](/fr/user-guide/tools/) — schémas d'outils, utile pour écrire des regex.
- [Guides : Observabilité](/fr/guides/observability/) — envoyer `tool.denied` vers Loki/Datadog.
- [Référence : logs](/fr/reference/logs/) — chaque message slog connu.
