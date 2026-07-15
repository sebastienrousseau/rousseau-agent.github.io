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
description: "A checklist for platform teams adopting rousseau-agent: SBOM, cosign, seccomp, network egress, approval policy, at-rest encryption, security SLOs."
keywords: "enterprise, checklist, sbom, cosign, seccomp, egress, encryption, slo"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/guides/enterprise-onboarding/"
subtitle: "The platform-team checklist before rousseau ships beyond a proof-of-concept."
tags: "guides, enterprise, security, checklist, sbom, cosign"
title: "Guide : intégration entreprise"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "enterprise, checklist, sbom, cosign, seccomp, egress, encryption, slo"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : intégration entreprise"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/enterprise-onboarding/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/enterprise-onboarding/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide : intégration entreprise"
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
twitter_description: "A checklist for platform teams adopting rousseau-agent: SBOM, cosign, seccomp, network egress, approval policy, at-rest encryption, security SLOs."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide : intégration entreprise"
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

## Pour qui c'est fait

Une équipe plateforme évaluant rousseau-agent avant qu'il n'approche la production. Répond à la question « qu'avons-nous besoin de valider ? ». Chaque item renvoie à une chose concrète que rousseau livre pour que la validation soit objective, pas esthétique.

## Checklist

### 1. Chaîne d'approvisionnement

- [ ] **SBOM.** Confirmer que chaque release publie `rousseau_<v>_sbom.cdx.json` (CycloneDX 1.5). Importer dans votre scanner SCA. Actionnable : lancer `cyclonedx-cli tree` contre le SBOM et grep les exceptions de licence bannies par votre entreprise.
- [ ] **Provenance SLSA-3.** Chaque release publie `rousseau_<v>_provenance.intoto.jsonl`. Vérifier avec `slsa-verifier verify-artifact --source-uri github.com/sebastienrousseau/rousseau-agent …`.
- [ ] **Racine de confiance cosign.** Épinglez le regex d'identité du certificat : `sebastienrousseau/rousseau-agent`. Cachez la recette de vérification de checksum dans votre outillage de bootstrap ; voir [Quickstart](/fr/quickstart/) étape 5.
- [ ] **Build reproductible.** `make check` exécute `go test -race` plus `govulncheck`. Mettez en place un scan périodique des vulnérabilités de la version que vous exécutez.

### 2. Durcissement d'exécution

- [ ] **Conteneur rootless.** `docker/rousseau-agent.container` fait tourner l'unité Quadlet sous un utilisateur non privilégié dédié avec `loginctl enable-linger`. Confirmer que votre hôte est configuré de la même façon.
- [ ] **Toutes les capacités retirées.** `DropCapability=all`. `podman inspect | jq '.[0].EffectiveCaps'` doit afficher `[]`.
- [ ] **`NoNewPrivileges=true`.** Empêche les processus enfants de gagner des privilèges.
- [ ] **Système de fichiers racine en lecture seule.** `ReadOnly=true` + `Tmpfs=/tmp:rw,size=64m`.
- [ ] **Profil seccomp.** `SeccompProfile=/usr/share/containers/seccomp.json`. Auditer contre la baseline de votre hôte.
- [ ] **Cartographie d'espace de noms utilisateur.** `UserNS=keep-id`. Confirme que les fichiers bind-montés sont possédés correctement des deux côtés.

### 3. Posture réseau

- [ ] **Pas d'entrant.** Rousseau a zéro surface HTTP. `ss -tanp | grep rousseau` affiche uniquement des sockets sortants.
- [ ] **Allowlist de sortie.** Superposez nftables ou Cloudflare Zero-Trust hors du conteneur. Autorisez uniquement :
  - Le fournisseur LLM (`api.anthropic.com`, `bedrock-runtime.<region>.amazonaws.com`, `us-east1-aiplatform.googleapis.com`, etc.).
  - Le transport (`web.whatsapp.com`, `mtproto.telegram.org`, homeserver matrix, Slack `wss-*`).
- [ ] **Résolveur DNS verrouillé.** Optionnellement, exécutez un `unbound` dans un conteneur voisin qui ne résout que les noms allowlistés.

### 4. Politique d'approbation

- [ ] **`mode: pattern` pour chaque démon non-supervisé.** Vérifier `agent.approver.mode: pattern` dans la configuration pour chaque service de transport.
- [ ] **`default: deny`.** Aucun appel non correspondant ne passe.
- [ ] **Liste deny `bash`.** `rm\s+-rf`, `sudo`, `curl`, `wget`, `chmod`, `chown`, `nc`, `ncat`. Voir [Tutorial: Harden the approver](/fr/tutorials/harden-approver-policy/).
- [ ] **Épinglage de chemin `write` / `edit`.** Le regex restreint les écritures à `/workspace/...`.
- [ ] **Configuration dans le gestionnaire de sources.** Le YAML de l'approbateur est du code — révisez-le en PR.

### 5. Gestion des secrets

- [ ] **Pas de clés API dans `config.yaml`.** Stockez les secrets dans un `EnvironmentFile=` systemd (`chmod 0600`) ou le gestionnaire de secrets de l'entreprise.
- [ ] **`ANTHROPIC_API_KEY` transmise via env.** `config.Load` (`internal/config/config.go`) la capte.
- [ ] **Bedrock IRSA / Vertex ADC.** Préférez la fédération d'identités aux clés API longue durée.
- [ ] **Cadence de rotation.** 90 jours ou selon votre politique. Rousseau ne cache pas les identifiants — une clé rotatée est reprise au prochain redémarrage du démon.

### 6. Données au repos

- [ ] **Chiffrement de `sessions.db`.** Chiffrement de disque complet (LUKS sous Linux, FileVault sous macOS, volumes chiffrés EBS sous AWS). Rousseau n'implémente pas de chiffrement niveau applicatif sur le magasin de sessions.
- [ ] **Sauvegardes chiffrées.** Restic ou borg chiffrent tous deux au repos avec une clé que vous contrôlez.
- [ ] **Politique de rétention.** Suppression en masse des sessions de plus de `N` jours — voir [Guides: Session management](/fr/guides/session-management/) pour le SQL.
- [ ] **Gestion de la table JID.** La table `jid_sessions` mappe les numéros de téléphone aux identifiants de session. Traitez-la comme des données personnelles.

### 7. Logs et audit

- [ ] **`log.format: json`.** Sortie analysable par machine.
- [ ] **Expédition des logs hors hôte.** Vector / Promtail / Datadog. Voir [Guides: Observability](/fr/guides/observability/).
- [ ] **Rétention.** 90 jours minimum en stockage froid. La piste d'audit de rousseau est entièrement dans slog ; c'est vous qui la rendez durable.
- [ ] **Alerte sur `tool.denied`.** Alertez sur tout refus — cela peut être bénin ou une tentative d'injection.
- [ ] **Alerte sur `whatsapp.logged_out`.** Un déclenchement de la politique Meta signifie que le compte est hors service.

### 8. Gestion du changement

- [ ] **Les changements de configuration sont du code.** Revus en PR, versionnés dans git.
- [ ] **Les montées d'image sont délibérées.** `AutoUpdate=disabled` dans l'unité Quadlet est intentionnel.
- [ ] **Plan de rollback.** Gardez l'image précédente taguée et disponible. `podman tag localhost/rousseau-agent:local rousseau-agent:previous` avant chaque build.

### 9. Réponse à incident

- [ ] **Rotation d'astreinte.** Quelqu'un peut faire `systemctl --user stop rousseau-agent` dans votre SLO MTTR.
- [ ] **Playbook compromission.** Étapes pour : révoquer la clé API LLM, révoquer le jeton de transport (par ex. réinstallation du bot Slack), snapshotter le magasin de sessions, imager le système de fichiers du conteneur, délier l'appareil WhatsApp.
- [ ] **Canal de divulgation sécurité.** Lisez `SECURITY.md` dans le dépôt rousseau-agent pour l'adresse de divulgation coordonnée.
- [ ] **SLO pour les correctifs de sécurité.** Suivez les CVE contre la version rousseau épinglée. `govulncheck` dans `make check` attrape les problèmes connus de la stdlib Go et des dépendances.

### 10. Cartographie de conformité

- [ ] **Preuves SOC 2.** Provenance SLSA-3 + cosign + SBOM couvre CC7.1 (opérations système). Les logs d'approbateur couvrent CC7.2.
- [ ] **ISO 27001 A.12 Operations Security.** Politiques d'approbation + cloisonnement du workspace + logs d'audit.
- [ ] **OWASP LLM Top-10.** Rousseau ne s'atteste pas conforme au LLM Top-10 aujourd'hui — c'est un élément de feuille de route. Documentez vos contrôles compensatoires (approbateur + conteneur) dans votre audit.

## Modèle de validation

Ci-dessous un modèle léger que votre équipe plateforme peut copier dans un runbook :

```
Validation de déploiement Rousseau-agent
========================================
Version : <tag>            (vérifiée via cosign / SLSA verifier)
Fournisseur : <anthropic|bedrock|vertex|openai>
Transports activés : <liste>
Mode approbateur : pattern
Défaut approbateur : deny
Destination logs : <Loki / Datadog / etc>
Destination backups : <s3://... / dépôt restic>
Astreinte : <équipe>
Divulgation sécurité : <adresse interne>
```

## Voir aussi

- [Security](/fr/security/) — les frontières de confiance que cette checklist protège.
- [Deployment](/fr/deployment/) — l'unité Quadlet.
- [Tutorial: Deploy to a VPS](/fr/tutorials/deploy-to-a-vps/) — exemple pratique.
- [Guides: Production Deployment](/fr/guides/production-deployment/) — spécificités opérationnelles.
