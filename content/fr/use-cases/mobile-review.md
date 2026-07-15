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
description: "Use case narrative: reviewing pull requests from WhatsApp on the train, driven by rousseau-agent on a home box."
keywords: "mobile review, whatsapp, pr review, commute, use case, pull request"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/use-cases/mobile-review/"
subtitle: "Reviewing PRs from your phone on the train."
tags: "use-cases, whatsapp, mobile, pr"
title: "Cas d'usage : revue de PR mobile"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mobile review, whatsapp, pr review, commute, use case, pull request"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Cas d'usage : revue de PR mobile"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 72
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/mobile-review/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/mobile-review/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Cas d'usage : revue de PR mobile"
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
twitter_description: "Use case narrative: reviewing pull requests from WhatsApp on the train, driven by rousseau-agent on a home box."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Cas d'usage : revue de PR mobile"
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

Vous êtes ingénieur staff dans une entreprise de taille moyenne. Votre boîte de réception compte huit PR ouvertes en attente de votre revue. Vous êtes dans un train pour 45 minutes, avec du réseau mais sans portable. Historiquement, réviser une PR depuis le téléphone signifie plisser les yeux devant la vue diff de GitHub et taper des commentaires creux « LGTM ».

Rousseau vit sur le petit Intel NUC dans votre placard. Il dispose d'une connexion WhatsApp vers votre JID, `bypassPermissions` sur la CLI `claude` locale, et un accès en lecture à vos checkouts locaux des trois dépôts que vous relisez. Vous écrivez en DM WhatsApp :

> review PR #4821 in checkout-service

Rousseau exécute `gh pr diff 4821`, lit le code et répond :

> PR #4821 adds retry-with-backoff to the Stripe webhook handler. Three observations:
>
> 1. The backoff is uncapped — if Stripe is truly down, we'll accumulate goroutines forever. Suggest a `context.WithTimeout` at the caller.
> 2. Test file adds two new tests but neither covers the timeout path.
> 3. `pkg/webhook.go:82` — the mutex is held across the network call. Minor.
>
> Should I draft a review comment stub?

Vous répondez :

> yes, with all three

Rousseau utilise `gh pr review` sous `--draft` (l'approbateur bloque l'approbation finale ; un humain doit toujours cliquer sur « submit review »). Le temps que vous soyez à votre bureau, le commentaire brouillon attend.

## Ce que cela requiert

### Le démon

Rousseau sur le NUC comme conteneur Podman rootless :

- **Fournisseur** : `claudecli` — hérite de votre authentification Claude Code locale.
- **Transport** : WhatsApp — le transport de prédilection pour la portée mobile.
- **État** : `~/.local/share/rousseau/sessions.db`.

### Configuration

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: bypassPermissions

whatsapp:
  reply_header: "🚂 *rousseau*\n\n"

log:
  level: info
  format: text                # this is a single-user daemon; text logs are fine

agent:
  max_iterations: 32
  compression:
    enabled: true             # subscription-tier claudecli; compression is free
    trigger_messages: 60
    keep_recent: 8
  approver:
    mode: pattern
    default: deny
    reason: "denied — this daemon reviews code, it does not merge it"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(gh pr view|gh pr diff|gh pr list|gh pr review --draft|gh pr comment|git status|git diff|git log|git show) "}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(go test|go vet|go build|npm test|pnpm test|cargo check) "}
    deny:
      - {tool: bash, match: "gh pr merge|gh pr close|gh pr approve"}
      - {tool: bash, match: "git (push|reset --hard|clean)"}
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit,  match: "\"path\":\"/etc/|/root/|/var/"}
```

### Les montages

- `~/repos/checkout-service/` (lecture seule).
- `~/repos/payments-api/` (lecture seule).
- `~/repos/web-frontend/` (lecture seule).
- `~/.claude/` — jetons OAuth de Claude Code (lecture-écriture, mais uniquement pour le rafraîchissement de jetons).
- `~/.config/gh/` — jeton OAuth de la CLI GitHub (lecture-écriture, même raison).

Les montages en lecture seule empêchent le modèle d'éditer accidentellement votre copie de travail. Les revues passent par GitHub, pas par votre checkout.

### Premier lancement

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Vous scannez le QR code une fois. Ensuite, le démon vit dans l'unité Quadlet et démarre au redémarrage de l'hôte. Votre allowlist est le JID de votre propre téléphone.

## La posture de sécurité

- L'**allowlist verrouille le transport.** Seul votre téléphone peut piloter le démon. Toute autre personne qui découvrirait le numéro se voit rejetée silencieusement.
- L'**approbateur pattern bloque chaque merge / push / close.** Rousseau relit, rédige des brouillons et commente — un humain doit toujours cliquer sur « Merge » ou « Approve ».
- Les **montages en lecture seule** protègent vos checkouts de travail.
- **`bypassPermissions` sur claudecli** n'est tolérable que parce que l'approbateur fait le travail de sécurité. Ne combinez jamais `bypassPermissions` avec `mode: allow_all`.

## La portée

- **Le signal chute dans le métro.** La backpressure de WhatsApp est gracieuse — vous envoyez une question, vous recevez une réponse quand le démon a du signal pour répondre. Rousseau n'a pas besoin de tenir une session TCP live avec votre téléphone.
- **Les notes vocales fonctionnent.** Avec le [mode vocal](/fr/user-guide/voice-mode/) activé et `whisper.cpp` installé sur le NUC, vous pouvez dicter une note vocale « what's the diff on 4821 » et obtenir une réponse texte. Utile quand taper sur un téléphone dans un train qui bouge est pénible.
- **Le démon tourne sur votre matériel.** Rien de votre raisonnement de revue ne part vers un SaaS tiers. Le seul appel sortant est le sous-processus de la CLI `claude` vers Anthropic, en utilisant votre abonnement existant.

## Ce que rousseau ne fait pas ici

- **Il ne clique pas sur « Merge ».** C'est une décision humaine, et l'approbateur l'impose.
- **Il n'apprend pas votre style de revue.** La prochaine PR reçoit la même checklist générique tant que vous n'avez pas rédigé un [skill](/fr/skills/) capturant votre style.
- **Il ne met pas les revues en file.** Chaque requête est indépendante ; il n'y a pas de tâche de fond « relire toutes mes PR ouvertes » (sauf si vous en câblez une via [cron](/fr/guides/scheduled-tasks/)).

## Ce que vous changeriez sous charge

- Ajoutez un [skill](/fr/skills/) nommé `pr-review-checklist.md` qui codifie les six choses que vous vérifiez toujours. Les skills sont insérés dans le prompt système quand un déclencheur correspondant apparaît dans le message utilisateur.
- Ajoutez un cron nocturne : `0 8 * * 1-5 rousseau ... deliver a summary of every open PR`.
- Basculez vers un chemin API Anthropic payant si les limites de débit de l'abonnement `claudecli` deviennent un goulot d'étranglement. Zéro changement de config en aval.

## Pages associées

- [Transport WhatsApp](/fr/transports/whatsapp/) — la référence du transport.
- [Fournisseur claudecli](/fr/providers/claudecli/) — authentification héritée.
- [Skills](/fr/skills/) — comment codifier votre style de revue.
- [Mode vocal](/fr/user-guide/voice-mode/) — dicter les revues.
