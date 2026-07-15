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
description: "Use case narrative: a solo SRE running rousseau-agent over Slack to triage a 3 a.m. page from the couch, then hand off to full incident response."
keywords: "on-call, sre, slack, incident, page, triage, use case"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/use-cases/oncall-buddy/"
subtitle: "Triaging a 3 a.m. page from the couch over Slack."
tags: "use-cases, on-call, slack, sre"
title: "Cas d'usage : compagnon d'astreinte"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "on-call, sre, slack, incident, page, triage, use case"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Cas d'usage : compagnon d'astreinte"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 71
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/oncall-buddy/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/oncall-buddy/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Cas d'usage : compagnon d'astreinte"
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
twitter_description: "Use case narrative: a solo SRE running rousseau-agent over Slack to triage a 3 a.m. page from the couch, then hand off to full incident response."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Cas d'usage : compagnon d'astreinte"
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

## Le scénario

Il est 3 h du matin. Votre pager sonne. PagerDuty indique que le service de checkout renvoie des 502. Vous êtes l'un des deux SRE d'une petite entreprise, votre co-responsable est en vacances, et rejoindre votre portable implique de trouver vos lunettes, descendre les escaliers et déverrouiller un VPN. Avant tout cela, vous voulez une première réponse : quels tableaux de bord ont l'air mauvais, ce qui a changé dans les dernières 24 heures, quel runbook s'applique.

Rousseau vit sur la machine d'exploitation dans votre placard. Il dispose d'identifiants en lecture seule sur votre pile de logs, d'un kubectl en lecture seule sur un namespace et d'une connexion Slack Socket Mode vers `#incident-oncall`. Vous tapez la notification de DM sur votre téléphone :

> what changed in checkout in the last 24h?

Rousseau lit le git log du dépôt du service checkout, croise avec votre journal de déploiement (depuis un répertoire monté), et répond :

> Two changes: PR #4821 (payment retry logic, deployed 21:14 UTC) and a Helm value bump on `checkout-web` at 22:03 UTC. The payment retry change is the more suspicious — it touches the same code path the current 502s originate from.

Vous demandez :

> pull the last 100 error lines from checkout-web

Rousseau exécute `kubectl logs -n checkout deploy/checkout-web --tail=100 --previous` sous son kubeconfig en lecture seule, et vous colle les lignes saillantes. Vous repérez une trace de null-pointer. Vous répondez en DM :

> revert PR #4821 in staging first — call me when it's confirmed green

Rousseau poste dans `#incident-oncall` avec un plan, ouvre une PR de revert sur staging, et vous ping une fois que staging est vert. Vous vous levez et rejoignez votre portable.

## Ce que cela requiert

### Le démon

Rousseau tourne comme conteneur Podman rootless sur la machine d'exploitation :

- **Fournisseur** : `bedrock` — votre entreprise a déjà un engagement de dépense Bedrock ; aucune clé API par utilisateur requise.
- **Transport** : Slack Socket Mode — aucune surface HTTP entrante, WebSocket sortant uniquement.
- **État** : `~/.local/share/rousseau/sessions.db`, sur un disque chiffré LUKS.

### Configuration

```yaml
provider: bedrock

bedrock:
  region: us-east-1
  profile: rousseau-oncall
  model: anthropic.claude-sonnet-4-6-20250101-v1:0

log:
  level: info
  format: json

state:
  path: /var/lib/rousseau/sessions.db

agent:
  max_iterations: 32
  approver:
    mode: pattern
    default: deny
    reason: "read-only on-call posture — ask an operator to widen the scope"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(kubectl get|kubectl describe|kubectl logs|git log|git diff|git show|cat|grep|rg|head|tail|wc) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"gh pr (view|list|diff) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"gh pr create --draft "}   # allows opening a draft revert
    deny:
      - {tool: bash, match: "kubectl (delete|apply|edit|scale|rollout undo|exec)"}
      - {tool: bash, match: "gh pr merge|gh pr close --delete-branch"}

slack:
  app_token: xapp-<...>
  bot_token: xoxb-<...>
  allowlist:
    - U012ABCXYZ    # your Slack user ID
    - U012DEFGHI    # your co-lead's Slack user ID
```

### Les montages

- Checkouts de dépôts sous `/workspace/repos/` (lecture seule).
- Journal de déploiement sous `/workspace/deploys/` (lecture seule).
- kubeconfig à `/home/rousseau/.kube/config` — monté en lecture seule, le service account a un rôle cluster en lecture seule dans le namespace `checkout`.
- Identifiants AWS via IAM Role for Service Accounts (IRSA) si sur EKS, ou via un `~/.aws/` monté pour l'on-prem.

### L'unité Quadlet systemd

La `docker/rousseau-agent.container` de référence avec :

- `ReadOnly=true`
- `DropCapability=all`
- `NoNewPrivileges=true`
- `Restart=on-failure`

Démarre au redémarrage de l'hôte. Journal disponible via `journalctl --user -u rousseau-agent.service`.

## La posture de sécurité

- L'**allowlist Slack** garantit que seuls vous et votre co-responsable pouvez piloter le démon. Tout autre DM est rejeté silencieusement.
- L'**approbateur pattern avec `default: deny`** bloque tout ce qui sort de la whitelist. Si le modèle veut exécuter `kubectl delete pod`, il reçoit une erreur `tool_result` expliquant le blocage et se rabat sur un document de plan.
- Le **kubeconfig en lecture seule + les montages de dépôts en lecture seule** signifient que le démon *ne peut pas* muter la production même si l'approbateur échouait ouvert.
- **Ceinture, bretelles et une seconde ceinture** — chaque couche échoue en sécurité.

## Ce que rousseau ne fait pas ici

- **Il ne vous paginera pas.** PagerDuty est la source de vérité pour qui est d'astreinte.
- **Il ne merge pas les PR.** L'approbateur bloque `gh pr merge`. Rousseau peut ouvrir un revert en brouillon ; un humain doit toujours confirmer.
- **Il n'exécute pas `kubectl exec`.** Toute commande qui pourrait muter l'état du cluster est refusée.
- **Il n'apprend pas de l'incident.** Le rappel inter-session via FTS5 signifie que le rousseau du prochain incident trouvera des mots-clés de la session de ce soir ; les conclusions sémantiques restent le travail de l'opérateur.

## Ce que vous changeriez sous charge

Si deux pagers à 3 h par mois deviennent deux par semaine :

- Envisagez de promouvoir davantage de matchers `bash` dans `allow` à mesure que vous gagnez en confiance.
- Câblez la sortie slog vers [Loki](/fr/guides/observability/) pour que les revues post-mortem puissent citer les appels d'outils exacts effectués par rousseau.
- Ajoutez des [tâches planifiées](/fr/guides/scheduled-tasks/) pour que rousseau exécute un digest nocturne des incidents ouverts dans votre Slack du matin.

## Pages associées

- [Guides : Audit + politiques d'approbation](/fr/guides/audit-approval-policies/) — le levier de sécurité.
- [Guides : Mode lecture seule](/fr/guides/read-only-mode/) — la posture la plus stricte.
- [Transport Slack](/fr/transports/slack/) — câblage Socket Mode.
- [Fournisseur Bedrock](/fr/providers/bedrock/) — chaîne d'authentification.
