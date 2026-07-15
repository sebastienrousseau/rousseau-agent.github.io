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
description: "Use case narrative: a financial-services team running rousseau-agent in-tenant on AWS with Bedrock, pattern-mode approvals, and SLSA-3 supply-chain posture."
keywords: "regulated industry, financial services, bedrock, in-tenant, slsa, cosign, compliance"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/use-cases/regulated-industry/"
subtitle: "In-tenant Bedrock deployment for a financial-services team."
tags: "use-cases, bedrock, regulated, financial-services, slsa"
title: "Cas d'usage : secteur réglementé"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "regulated industry, financial services, bedrock, in-tenant, slsa, cosign, compliance"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Cas d'usage : secteur réglementé"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 73
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/regulated-industry/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/regulated-industry/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Cas d'usage : secteur réglementé"
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
twitter_description: "Use case narrative: a financial-services team running rousseau-agent in-tenant on AWS with Bedrock, pattern-mode approvals, and SLSA-3 supply-chain posture."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Cas d'usage : secteur réglementé"
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

Vous êtes ingénieur plateforme dans une banque de taille moyenne. La conformité exige que tout assistant de codage utilisé par vos ingénieurs doive :

1. Tourner à l'intérieur des comptes AWS de la banque, pas sur un plan de contrôle SaaS.
2. Router le trafic modèle via un fournisseur avec lequel la banque a un contrat et une piste d'audit (Bedrock).
3. Avoir une posture chaîne d'approvisionnement documentée (SLSA-3, SBOM, vérification de signature).
4. Appliquer des politiques d'approbation avec une piste d'audit lisible par machine.
5. Ne pas exfiltrer le code source vers un tiers.

Le positionnement de Rousseau répond à chacune de ces exigences. Vous l'exécutez comme un `Deployment` Kubernetes dans le cluster EKS de l'équipe plateforme, pilotant un transport Slack Socket Mode vers le canal d'ingénierie.

Le déploiement en ingénierie est banal — un `Deployment`, un `Secret`, un `ConfigMap`, un `PersistentVolumeClaim`. L'histoire commence quand l'auditeur arrive.

## L'audit

Un auditeur externe pose quatre questions.

**Q1 : Où va le trafic modèle ?**

Vous le pointez vers `internal/llm/bedrock/`. Le fournisseur utilise la chaîne d'identifiants AWS standard (via IRSA sur EKS), donc les identifiants sont des jetons STS de courte durée. Le trafic ne quitte jamais votre compte AWS.

**Q2 : Comment vérifiez-vous le binaire exécuté ?**

Vous lui montrez `docker/Dockerfile` — un build multi-étapes avec une base `golang:1.26-alpine` épinglée — et le script `release-verify.sh` que l'équipe SRE exécute lors de la promotion de l'image :

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_${VERSION}_checksums.txt.sig \
  rousseau_${VERSION}_checksums.txt

sha256sum -c rousseau_${VERSION}_checksums.txt
```

Vous ajoutez : la provenance SLSA-3 est attestée via GitHub Actions OIDC. Le journal de transparence Sigstore est une ancre de confiance publique.

**Q3 : Comment empêchez-vous le modèle de muter la production ?**

Vous le pointez vers la config `agent.approver` :

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied — this deployment does not permit destructive operations without operator confirmation"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|grep|rg|find|git status|git diff|git log|go test|go build) "}
    deny:
      - {tool: bash, match: "rm -rf|sudo|curl|wget|chmod|chown"}
      - {tool: bash, match: "kubectl (delete|apply|edit|scale|exec)"}
      - {tool: bash, match: "aws (s3 rm|iam|kms delete)"}
      - {tool: write, match: "\"path\":\"/(etc|root|var|usr)/"}
      - {tool: edit,  match: "\"path\":\"/(etc|root|var|usr)/"}
```

Deny l'emporte sur allow. Non correspondant → deny. Chaque décision est loggée comme un événement slog structuré (`tool.execute`, `tool.denied`) et transmise au tenant Datadog de la banque via un daemonset Vector.

**Q4 : Où est stocké le code source qu'une session référence ?**

Vous expliquez : l'état de session vit sur un PVC adossé à EBS avec chiffrement au repos. Le contexte modèle reste dans la session compressée (voir [Compression + Rappel](/fr/user-guide/compression-recall/)). L'index de rappel FTS5 tourne sur le même PVC. Rien ne part vers `agentskills.io` ni aucune URL externe — les [Skills](/fr/skills/) sont chargés depuis un répertoire monté, pas depuis un registre hébergé.

L'auditeur enchaîne : « Et le modèle lui-même ? » Vous expliquez que Bedrock est la frontière du modèle ; tout ce que Bedrock fait avec les prompts est régi par le contrat existant de la banque avec AWS.

## Ce que cela requiert

### Le manifest

Voir [Guides : déploiement Kubernetes](/fr/guides/kubernetes-deployment/) pour le manifest complet. Écarts clés pour ce cas d'usage :

- **Namespace `pod-security.kubernetes.io/enforce: restricted`.**
- **IRSA** pour les identifiants Bedrock — pas de clés AWS de longue durée dans les secrets.
- **NetworkPolicy** autorisant l'egress vers les endpoints régionaux Bedrock et Slack WSS uniquement.
- **Daemonset Vector** expédiant la sortie slog vers Datadog avec le champ `msg` analysé comme une facette.

### La configuration

```yaml
provider: bedrock

bedrock:
  region: eu-west-1
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
  max_tokens: 4096

log:
  level: info
  format: json

state:
  path: /var/lib/rousseau/sessions.db

agent:
  max_iterations: 32
  compression:
    enabled: true
    trigger_messages: 40
    keep_recent: 6
  approver:
    mode: pattern
    default: deny
    reason: "denied — this deployment does not permit destructive operations without operator confirmation"
    allow: [...as above...]
    deny:  [...as above...]

slack:
  app_token: xapp-<from-Secret>
  bot_token: xoxb-<from-Secret>
  allowlist:
    - U012ABC   # platform team on-call
    - U012DEF   # platform team lead
```

### Le récit d'audit

Chaque appel d'outil est une ligne slog. Chaque refus en est une autre. Le monitor Datadog sur `msg:tool.denied` alerte le SOC. Chaque semaine, l'équipe plateforme extrait un rapport :

```
# LogQL / Datadog / autre
sum by (name) (
  count_over_time({job="rousseau-agent"} |= "tool.denied" [1w])
)
```

Le rapport rejoint le drive conformité. Parce que le schéma slog est stable ([Observabilité](/fr/guides/observability/)), le parsing ne casse pas d'une mise à jour rousseau à l'autre.

## Ce que l'auditeur ne demandera peut-être pas mais devrait

- **Builds reproductibles.** La CI de Rousseau inclut un job `reproducible-build` qui vérifie une sortie bit-identique sur des checkouts frais. Vous pouvez reconstruire indépendamment depuis une source taggée et comparer les SHA-256.
- **Épinglage des dépendances.** `go.mod` épingle les versions exactes ; `go.sum` est figé. Dependabot ouvre les mises à jour comme PR relisables, pas comme bumps silencieux.
- **`govulncheck` à chaque commit.** Toute vulnérabilité connue atteignant un symbole importé fait échouer la CI.
- Analyse statique **CodeQL** à chaque commit.

Tout ce qui précède se trouve dans [Security](/fr/security/) — le tiroir des dossiers de conformité existe déjà.

## La frontière hors-tenant

Bedrock est la frontière. Le trafic vers `bedrock-runtime.eu-west-1.amazonaws.com` quitte le pod mais reste dans AWS. Le diagramme de flux de données de la banque montre une flèche du pod vers Bedrock ; aucune autre flèche sortante n'existe pour ce déploiement (Slack Socket Mode est un WSS sortant vers `wss-primary.slack.com`, documenté comme une egress autorisée séparée).

## Pages associées

- [Guides : déploiement Kubernetes](/fr/guides/kubernetes-deployment/) — les manifests.
- [Guides : Audit + politiques d'approbation](/fr/guides/audit-approval-policies/) — le récit de conformité.
- [Guides : Observabilité](/fr/guides/observability/) — le pipeline slog.
- [Fournisseur Bedrock](/fr/providers/bedrock/) — chaîne d'identifiants et comportement régional.
- [Security](/fr/security/) — modèle de confiance et contrôles chaîne d'approvisionnement.
