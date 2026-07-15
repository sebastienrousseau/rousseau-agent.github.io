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
description: "Approval policy reference for rousseau-agent: allow_all, deny_all, and pattern-mode approvers with allow/deny regex rules and a configurable default."
keywords: "approval, approver, pattern mode, allow_all, deny_all, regex, safety, tool call"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/user-guide/approval-policies/"
subtitle: "Deep dive on approver modes with worked config."
tags: "approval, policy, pattern-mode, safety"
title: "Politiques d'approbation"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approval, approver, pattern mode, allow_all, deny_all, regex, safety, tool call"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Politiques d'approbation"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "security"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/approval-policies/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/approval-policies/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Politiques d'approbation"
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
twitter_description: "Approval policy reference for rousseau-agent: allow_all, deny_all, and pattern-mode approvers with allow/deny regex rules and a configurable default."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Politiques d'approbation"
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

## Le contrat

Chaque appel d'outil passe par `Approver.Approve(ctx, ApprovalRequest)` avant exécution. L'interface se trouve dans `internal/agent/approver.go` :

```go
type Decision string

const (
    DecisionAllow Decision = "allow"
    DecisionDeny  Decision = "deny"
)

type ApprovalRequest struct {
    ToolName  string
    Input     json.RawMessage
    SessionID string
}

type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

`Approve` est appelé de manière synchrone sur le chemin critique ; les implémentations doivent répondre rapidement ou honorer l'annulation de `ctx`.

Un `DecisionDeny` avec une raison non vide renvoie la raison au modèle sous forme d'erreur `tool_result`. Le modèle peut alors s'adapter (typiquement en demandant une clarification à l'opérateur) au lieu d'échouer silencieusement. C'est un choix de conception délibéré — les refus silencieux produisent un comportement pire que ceux annotés.

## Trois modes livrés

### `allow_all`

Chaque appel d'outil s'exécute. C'est le comportement par défaut lorsqu'aucun approbateur n'est configuré.

```yaml
agent:
  approver:
    mode: allow_all
```

À utiliser quand :

- `rousseau chat` interactif avec le fournisseur `claudecli` (Claude Code effectue ses propres approbations par appel).
- Tests de fumée en développement où vous voulez voir exactement ce que le modèle ferait.

### `deny_all`

Bloque tous les appels d'outils avec une chaîne de raison unique.

```yaml
agent:
  approver:
    mode: deny_all
    reason: "denied by policy for this deployment"
```

À utiliser quand :

- Test de fumée du câblage de l'approbateur.
- Posture d'inspection en première passe où vous voulez voir ce que le modèle *aurait* tenté, sans le laisser agir.

### `pattern`

Règles regex allow / deny par outil. **Le deny l'emporte sur le allow.** Les requêtes non correspondantes retombent sur `default` (`allow` ou `deny`).

```yaml
agent:
  approver:
    mode: pattern
    default: deny         # safe-by-default; unlisted requests are blocked
    reason: "denied by pattern policy"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
    deny:
      - {tool: bash, match: "rm -rf|sudo|chmod|chown"}
```

## Sémantique des règles

Chaque `PatternRule` a deux champs :

| Champ | Signification |
|---|---|
| `tool` | Nom de l'outil (`read`, `write`, `edit`, `grep`, `bash`, ou tout outil personnalisé). Vide correspond à tous les outils. |
| `match` | Regex RE2 Go appliquée sur l'entrée JSON brute produite par le modèle. Vide correspond à toute entrée. |

**Ordre d'évaluation :**

1. Chaque règle deny est testée contre la requête. Premier match → deny.
2. Chaque règle allow est testée. Premier match → allow.
3. Repli sur `default`. Un `default` vide est traité comme `deny` — sûr par défaut.

Le deny l'emporte toujours parce que la disposition la plus sûre est préférée. Un opérateur ajoutant un bloc `allow` large ne peut jamais déverrouiller accidentellement une catégorie qu'il avait refusée.

## Correspondance sur le JSON brut

La regex `match` s'applique sur l'**entrée JSON brute** émise par le modèle, pas sur les champs analysés. Cela a deux conséquences :

1. **Vous matchez sur la forme JSON.** Pour un appel `bash`, cela ressemble à `{"command":"ls /tmp"}`. Matchez `"command":\s*"ls\s`.
2. **Vous pouvez matcher tout champ.** L'outil `edit` reçoit `{"path":"/x","old_string":"...","new_string":"..."}` ; vous pouvez matcher sur `path`, sur `old_string`, ou sur les deux.

Échappez soigneusement les caractères significatifs en JSON :

- Les guillemets doubles sont littéraux dans le JSON brut — matchez avec `\"` dans votre regex si vous utilisez des chaînes YAML entre guillemets doubles.
- Les antislashs doivent être doublés en YAML : `\\` dans le fichier YAML devient `\` dans la regex compilée.

## Modèles de règles éprouvés

### Restreindre les éditions à une arborescence de répertoires

```yaml
allow:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/[^\"]*\""}
  - {tool: write, match: "\"path\":\"/workspace/repo/[^\"]*\""}
```

### Autoriser en liste blanche des commandes shell sûres

```yaml
allow:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|grep|rg|find|git status|git diff|go test) "}
```

### Refuser les commandes destructives indépendamment du allow

```yaml
deny:
  - {tool: bash, match: "rm\\s+-rf|sudo|:\\(\\)\\{ :\\|:& \\};:"}
```

### Refuser les écritures dans les répertoires système

```yaml
deny:
  - {tool: write, match: "\"path\":\"/(etc|root|var|usr)/"}
  - {tool: edit,  match: "\"path\":\"/(etc|root|var|usr)/"}
```

## Le champ `Default`

`default: deny` est la disposition la plus sûre et la valeur recommandée pour tout démon sans surveillance. `default: allow` inverse le modèle — chaque appel non listé s'exécute, et les règles `deny` deviennent le levier principal.

Quand utiliser `default: allow` :

- Le démon tourne dans un conteneur fortement verrouillé ([Deployment](/fr/deployment/)) et le conteneur est votre frontière principale.
- Vous expérimentez et voulez observer le comportement du modèle avant de décider quoi bloquer.

Partout ailleurs, préférez `default: deny`.

## Le champ `Reason`

`reason` est la chaîne retournée au modèle à chaque refus (ou repli `default: deny`). Vide, elle retombe sur `denied by pattern policy` (ou `denied by policy` pour `deny_all`).

Définir une raison utile améliore la récupération du modèle — au lieu de `denied by pattern policy`, essayez `denied — this deployment only allows reads inside /workspace; ask the operator to widen the scope` et observez le modèle répondre par une clarification actionnable.

## Interaction avec `claudecli`

Quand `provider: claudecli`, Claude Code exécute les appels d'outils, et son propre mode de permission (`bypassPermissions`, `plan`, `default`) filtre également chaque action. Le comportement effectif est l'intersection : l'approbateur rousseau **et** l'approbateur de Claude Code doivent tous deux autoriser l'appel pour qu'il s'exécute.

Préférez garder les deux alignés :

- Sans surveillance : `bypassPermissions` sur Claude Code, `mode: pattern` + `default: deny` sur rousseau.
- Inspection en lecture seule : `plan` sur Claude Code, `mode: pattern` n'autorisant que `read`/`grep` sur rousseau. Voir [Guides : Mode lecture seule](/fr/guides/read-only-mode/).

## Piste d'audit

Chaque décision d'approbateur est émise via slog :

| Événement | Signification |
|---|---|
| `tool.execute` (INFO) | Appel approuvé, en cours d'exécution. |
| `tool.denied` (WARN) | Appel bloqué. Inclut le nom de l'outil et la raison. |
| `tool.error` (WARN) | L'appel s'est exécuté mais a échoué. |

Voir [Guides : Observabilité](/fr/guides/observability/) pour les recettes de pipeline.

## Approbateurs personnalisés

Tout type satisfaisant `Approver` fonctionne. Câblez le vôtre lors de l'intégration de la boucle d'agent :

```go
myApprover := agent.ApproverFunc(func(ctx context.Context, req agent.ApprovalRequest) (agent.Decision, string) {
    // Consulter un moteur de politiques externe, solliciter l'opérateur, ...
    return agent.DecisionAllow, ""
})

ag := agent.New(provider, registry, logger, agent.Options{Approver: myApprover})
```

L'interface est délibérément minimale (`Approve` est la seule méthode) donc intégrer un moteur de politiques externe (OPA, Cedar, ou un moteur de règles sur mesure) tient dans un petit adaptateur.

## Dépannage

### Chaque appel refusé même avec un allow correspondant

Le deny l'emporte sur le allow. `PatternApprover.Approve` dans `internal/agent/approver.go` ligne 152 itère d'abord sur les règles deny. Cherchez la chaîne `reason` exacte dans les logs `tool.denied`.

### Erreur de compilation de regex au démarrage

`PatternApprover` compile les regex paresseusement au premier `Approve`. Une erreur de compilation entraîne un `DecisionDeny` avec la raison `approver: pattern compile: <err>`. Testez vos regex sur [regex101.com](https://regex101.com) avec la saveur Go.

### `mode: pattern` mais `default:` est ignoré

Seules `allow` et `deny` sont des valeurs valides pour `default:`. Les valeurs vides ou inconnues retombent sur `DecisionDeny` (défaut sûr) sans afficher d'avertissement.

### La règle allow correspond littéralement au JSON

La regex s'applique sur le JSON brut d'entrée de l'appel d'outil. Pour matcher un champ `path`, échappez les guillemets : `"\"path\":\"/workspace/"`.

### Les appels refusés n'apparaissent pas dans les logs

Si — sous forme de `tool.denied` au niveau `warn`. Si vous filtrez par niveau, assurez-vous que `warn` est inclus.

## Pages associées

- [Guides : Audit + politiques d'approbation](/fr/guides/audit-approval-policies/) — exemple concret avec piste d'audit slog.
- [Guides : Mode lecture seule](/fr/guides/read-only-mode/) — la posture d'inspection.
- [Guide utilisateur : outils](/fr/user-guide/tools/) — les outils que l'approbateur filtre.
- [Security](/fr/security/) — vue d'ensemble des frontières de confiance.
- [Boucle d'agent](/fr/agent-loop/) — où l'approbateur est appelé.

## Pour aller plus loin

- `internal/agent/approver.go` — `PatternApprover`, `AllowAllApprover`, `DenyAllApprover`.
- `internal/agent/approver_test.go` — la matrice de tests.
- `internal/cli/approver.go` — traduction config → approbateur.
- `internal/config/config.go` — `ApproverConfig`, `PatternEntry`.
