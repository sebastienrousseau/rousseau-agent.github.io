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
description: "Contribution guide for rousseau-agent: conventional commits, PR process, reviewer checklist, release cadence."
keywords: "contributing, conventional commits, pr process, reviewer checklist, release"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/developer-guide/contributing/"
subtitle: "PR process, standards, review checklist."
tags: "developer-guide, contributing"
title: "Contribuer"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "contributing, conventional commits, pr process, reviewer checklist, release"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Contribuer"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 66
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/contributing/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/contributing/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Contribuer"
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
twitter_description: "Contribution guide for rousseau-agent: conventional commits, PR process, reviewer checklist, release cadence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Contribuer"
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

## Règles de base

Les contributions sont acceptées uniquement de la part des collaborateurs invités. Chaque PR est tenue au même niveau : CI verte, standards de code ci-dessous, approbation d'un relecteur. Une CI verte est nécessaire mais pas suffisante.

La source faisant autorité est le [`CONTRIBUTING.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/CONTRIBUTING.md) à la racine du dépôt. Cette page en est le miroir dans la voix du site de documentation.

## Environnement de développement

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make setup      # installe golangci-lint (v2) et govulncheck
make check      # vet + lint + tests race + govulncheck
```

Chaque contrôle exécuté en CI est disponible en local via le Makefile. Si un changement passe `make check`, il passera la CI.

## Standards de commit

- **Conventional Commits** — `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `ci:`, `perf:`.
- Ligne d'objet ≤ 72 caractères. Le corps explique le **pourquoi**, pas le quoi. Référencez la décision motrice, le ticket ou l'incident.
- N'amendez pas les commits publiés. Créez un nouveau commit ; le relecteur préfère une série qu'il peut bisecter.
- Signez vos commits si vous avez la signature configurée. Non obligatoire actuellement, mais recommandé pour les commits de tags de release.

## Standards de code

- Chaque identifiant exporté porte un commentaire godoc commençant par le nom de l'identifiant.
- Pas de `interface{}` / `any` dans les API exportées sans justification écrite dans le commentaire.
- `context.Context` se propage à travers chaque chemin d'E/S. Pas de globales cachées ni de loggers ambiants ; passez `*slog.Logger` explicitement.
- Les erreurs sont wrappées vers le haut avec `fmt.Errorf("...: %w", err)`. Les erreurs sentinelles vont dans le `errors.go` du package. Préférez `errors.Is` / `errors.As` sur les sites d'appel au matching par chaîne.
- Pas de panics hors de `main` et des helpers de test. Les variantes `Must*` qui panic sur erreur opérateur (double enregistrement, schéma statique invalide) sont autorisées avec justification documentée.
- Pas de `fmt.Print*` dans le code de bibliothèque. Utilisez `slog` ou un modèle TUI. Le linter `forbidigo` l'impose.

## Standards de tests

- Les tests unitaires vivent à côté du code : `foo.go` → `foo_test.go`.
- Tests table-driven préférés. Utilisez `require` pour les assertions bloquantes, `assert` pour les non-bloquantes.
- Injection de tests basée sur interface plutôt que monkey-patching global. Chaque package de transport définit une interface étroite (`WSConn`, `IMAPClient`, `HTTPClient`, `Sender`) que les tests satisfont avec des fakes.
- Cible de couverture : 85 % pour les packages de logique métier pure ; 75 % au global.
- Race-safe : `go test -race` doit passer. Le nouveau code concurrent nécessite un test race s'il introduit une synchronisation non triviale.
- Fonctions fuzz pour chaque parseur (`FuzzParseFoo` à côté de `parseFoo`). `make fuzz` exécute le corpus.

Voir [Testing](/fr/developer-guide/testing/) pour le motif d'injection.

## Processus de pull request

1. Ouvrez la PR contre `main`. Rebasez (ne mergez pas) si `main` bouge sous vous.
2. Chaque PR requiert :
   - Une justification dans la description (2–3 phrases reliant à la décision sous-jacente).
   - CI verte : `vet`, `lint`, `test-race` sur Linux + macOS, `govulncheck`, `codeql`, `reproducible-build`, plancher de couverture.
   - Approbation d'un relecteur.
3. Merges en squash uniquement. Le message de commit de merge est le message final et atterrit sur `main` comme un unique changement atomique.
4. Si la PR ajoute une nouvelle dépendance, notez la justification dans la description. Préférez la bibliothèque standard à l'ajout d'une dépendance ; préférez une dépendance existante à l'ajout d'une nouvelle.

## Checklist du relecteur

Les relecteurs vérifient, dans l'ordre :

1. **Nécessité.** Le changement est-il requis, ou ajoute-t-il une surface d'abstraction / fonctionnalité sans exigence motrice ?
2. **Portée.** Le changement reste-t-il dans son objectif déclaré, ou empaquette-t-il des nettoyages sans rapport ?
3. **Intégrité des frontières.** Le changement respecte-t-il la direction de dépendance `agent → concret` ? Voir [Architecture](/fr/developer-guide/architecture/).
4. **Couverture de tests.** Les nouveaux chemins de code sont-ils couverts ? Les cas limites sont-ils exercés ?
5. **Gestion d'erreurs.** Les erreurs sont-elles wrappées avec du contexte ? Les chemins de nettoyage sont-ils honnêtes (`_ =` avec justification `//nolint:errcheck`, pas avalés silencieusement) ?
6. **Godoc + linter propres.** Chaque symbole exporté documenté ; sortie du lint à 0 problème.
7. **Sécurité.** Le changement touche-t-il l'outil `bash`, la politique d'approbation, l'authentification de transport ou la posture conteneur ? Si oui, la description de la PR le signale-t-elle ?

## Contributions à la documentation

La documentation vit dans un dépôt séparé. Quand une PR de code touche une surface visible par l'utilisateur (un nouveau flag, un nouveau champ, un nouvel outil), la même PR — ou une PR immédiate de suivi sur le dépôt docs — doit mettre à jour les pages affectées.

- **Changement CLI** → [Guide utilisateur : CLI](/fr/user-guide/cli/) et [Référence : commandes CLI](/fr/reference/cli-commands/).
- **Changement de config** → [Configuration](/fr/configuration/) et [Référence : schéma de config](/fr/reference/config-schema/).
- **Nouvel outil** → [Guide utilisateur : outils](/fr/user-guide/tools/).
- **Nouveau transport** → `content/transports/<name>.md`.
- **Nouveau fournisseur** → `content/providers/<name>.md`.
- **Changement comportemental** → [Changelog](/fr/changelog/).

## Processus de release

Les releases sont taillées depuis `main` :

1. Mettre à jour les entrées du changelog.
2. Taguer en `vX.Y.Z` sur le commit de release.
3. Le workflow `release` build via GoReleaser, génère un SBOM CycloneDX, publie une signature cosign des checksums et génère une provenance SLSA-3.
4. Les consommateurs vérifient selon la recette dans [Security](/fr/security/) et [Installation](/fr/getting-started/installation/).

Rousseau suit [Semantic Versioning](/fr/getting-started/updating/) : patch corrige les bugs, minor ajoute des fonctionnalités sans casser, major casse — toujours avec une recette de migration.

## Gouvernance

`rousseau-agent` est un projet à mainteneur unique. L'autorité décisionnelle appartient au mainteneur officiel listé dans `go.mod` et `LICENSE`. Les contributeurs proposent des changements de direction via discussion de PR ou par courriel à `sebastian.rousseau@gmail.com`.

## Divulgations de sécurité

**N'ouvrez pas de ticket public pour un rapport de sécurité.** Écrivez à `sebastian.rousseau@gmail.com` selon la [Politique de sécurité](/fr/security/). Accusé de réception sous 72 heures.

## Suite

- [Architecture](/fr/developer-guide/architecture/) — la carte avant de la modifier.
- [Testing](/fr/developer-guide/testing/) — le motif que le relecteur attend.
- [Security](/fr/security/) — le canal de divulgation.
