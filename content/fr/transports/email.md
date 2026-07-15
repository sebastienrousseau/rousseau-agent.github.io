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
description: "Set up rousseau-agent's email transport: IMAP inbound polling, SMTP submission, both over full TLS, PlainAuth on 587, UTF-8 RFC 5322 output."
keywords: "email, IMAP, SMTP, TLS, PlainAuth, INBOX, poll interval, RFC 5322, UTF-8"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/transports/email/"
subtitle: "IMAP inbound plus SMTP outbound over TLS."
tags: "transports, email"
title: "Transport e-mail"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "email, IMAP, SMTP, TLS, PlainAuth, INBOX, poll interval, RFC 5322, UTF-8"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Transport e-mail"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 20
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/email/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/email/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Transport e-mail"
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
twitter_description: "Set up rousseau-agent's email transport: IMAP inbound polling, SMTP submission, both over full TLS, PlainAuth on 587, UTF-8 RFC 5322 output."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Transport e-mail"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>Le parcours du mot de passe applicatif Gmail, comment configurer le transport pour Fastmail / Google Workspace / un serveur mail auto-hébergé, la voie de migration depuis des serveurs STARTTLS-uniquement, et l'arbitrage entre rendu texte et HTML. Lisez <code>internal/transport/email/client.go</code> en parallèle de cette page.</p></aside>

## Vue d'ensemble

Le transport email (`internal/transport/email/`) est une paire : **IMAP entrant** (via `github.com/emersion/go-imap/v2`) et **SMTP sortant** (via `net/smtp` de la bibliothèque standard Go).

Il sonde INBOX pour les messages `UNSEEN`, les marque `SEEN` après passage au handler, et répond via `net/smtp.SendMail`.

## Posture TLS

**Les deux extrémités sont en TLS complet.** Le transport utilise `imapclient.DialTLS` côté IMAP et `smtp.SendMail` avec `PlainAuth` sur une connexion déjà encapsulée en TLS côté SMTP. Les serveurs IMAP ou SMTP STARTTLS-uniquement ne sont **pas actuellement supportés** — le daemon refuse d'envoyer des credentials en clair sur un socket non chiffré.

Ports TLS standard :

- IMAP : `993`
- Soumission SMTP : `465` (TLS implicite) — TLS complet. **Pas `587`, sauf si votre fournisseur fait aussi du TLS implicite sur 587.**

Certains fournisseurs (Google Workspace, Fastmail) acceptent la soumission SMTP sur `465` en TLS implicite. Vérifiez votre fournisseur avant configuration.

## Configuration

```yaml
email:
  imap_addr: "imap.example.com:993"
  imap_username: "bot@example.com"
  imap_password: "..."
  mailbox: "INBOX"
  poll_interval: "30s"

  smtp_addr: "smtp.example.com:465"
  smtp_username: "bot@example.com"
  smtp_password: "..."

  from: "bot@example.com"
  reply_header: ""
```

| Champ | Défaut | Effet |
|---|---|---|
| `imap_addr` | *requis* | `host:port` pour IMAP en TLS. |
| `imap_username` | *requis* | Nom d'utilisateur IMAP. |
| `imap_password` | *requis* | Mot de passe IMAP. |
| `mailbox` | `INBOX` | Boîte à sonder. |
| `poll_interval` | `30s` | Fréquence de recherche des mails UNSEEN. |
| `smtp_addr` | *requis* | `host:port` pour la soumission SMTP. |
| `smtp_username` | *requis* | Nom d'utilisateur SMTP. |
| `smtp_password` | *requis* | Mot de passe SMTP. |
| `from` | *requis* | Adresse `From` en enveloppe et en en-tête. |
| `reply_header` | *vide* | Préfixé au corps de chaque message sortant. |

## Ligne de commande

```sh
rousseau email \
  --imap-addr imap.example.com:993 \
  --imap-username bot@example.com \
  --imap-password ... \
  --smtp-addr smtp.example.com:465 \
  --smtp-username bot@example.com \
  --smtp-password ... \
  --from bot@example.com
```

## Forme du message sortant

Les réponses sont conformes RFC 5322. rousseau écrit :

```
From: bot@example.com
To: sender@example.com
Subject: Re: <inbound subject>
Content-Type: text/plain; charset=utf-8
MIME-Version: 1.0

<reply_header><body>
```

UTF-8 est inconditionnel. La sortie HTML est hors périmètre ; aucun moteur de template n'est câblé.

## Forme du message entrant

Les messages `UNSEEN` sont parsés en `IncomingMessage` avec :

- `From` = adresse parsée depuis l'en-tête `From`.
- `Body` = concaténation des parties `text/plain`.
- `At` = `INTERNALDATE` depuis IMAP.

Les pièces jointes, `text/html` et images inline sont ignorées.

## Choix de la boîte

`mailbox: "INBOX"` est le défaut. Pointez vers une étiquette Gmail (`"[Gmail]/étiquette"`) ou un dossier Fastmail pour un filtrage plus fin — tout ce que le serveur IMAP expose fonctionne.

## Configuration par fournisseur

<div class="tabs" data-tabs="email-provider">
  <div class="tab-list" role="tablist" aria-label="Email provider">
    <button role="tab" aria-selected="true">Gmail / Workspace</button>
    <button role="tab" aria-selected="false">Fastmail</button>
    <button role="tab" aria-selected="false">Outlook / M365</button>
    <button role="tab" aria-selected="false">Auto-hébergé</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Parcours mot de passe applicatif Gmail.** Les mots de passe Gmail classiques ne s'authentifient pas en IMAP/SMTP quand la 2FA est activée. Générez un mot de passe applicatif :

1. Rendez-vous sur https://myaccount.google.com/security. Confirmez que la **validation en 2 étapes** est activée.
2. Cliquez sur **Mots de passe des applications** (visible uniquement quand la 2FA est activée).
3. Nommez l'application « rousseau-agent », générez. Copiez le mot de passe de 16 caractères (les espaces sont optionnels).

Configuration :

```yaml
email:
  imap_addr: imap.gmail.com:993
  imap_username: your.address@gmail.com
  imap_password: "aaaa bbbb cccc dddd"

  smtp_addr: smtp.gmail.com:465
  smtp_username: your.address@gmail.com
  smtp_password: "aaaa bbbb cccc dddd"

  from: your.address@gmail.com
```

<aside class="admonition" data-type="warning"><span class="admonition-title">Verrouillage admin Google Workspace</span><p>Certains admins Workspace désactivent les mots de passe applicatifs à l'échelle de l'organisation. Si <em>Mots de passe des applications</em> n'apparaît pas sur votre page de sécurité, demandez à votre admin d'autoriser « Accès aux applications moins sécurisées » ou de configurer OAuth — rousseau ne supporte pas encore OAuth Gmail (roadmap).</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Fastmail supporte les mots de passe applicatifs sous *Settings &gt; Password &amp; Security &gt; App passwords*. Créez un mot de passe scopé sur *Mail (IMAP/POP/SMTP)* :

```yaml
email:
  imap_addr: imap.fastmail.com:993
  imap_username: your.address@fastmail.com
  imap_password: "..."

  smtp_addr: smtp.fastmail.com:465
  smtp_username: your.address@fastmail.com
  smtp_password: "..."

  from: your.address@fastmail.com
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Microsoft 365 a déprécié l'authentification basique (nom d'utilisateur + mot de passe) pour la plupart des tenants. Rousseau ne supporte pas encore Modern Auth / OAuth (roadmap). Options :

1. Activez *Authenticated SMTP* par boîte dans l'admin M365 (possible sur certains tenants).
2. Utilisez un relai : faites tourner rousseau contre un IMAP+SMTP auto-hébergé qui transfère par M365 en SMTP avec un mot de passe applicatif.
3. Attendez l'arrivée du support OAuth.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Tout serveur de messagerie auto-hébergé parlant IMAP sur TLS en 993 et soumission SMTP en TLS implicite en 465 fonctionne d'emblée. Postfix + Dovecot avec `smtpd_tls_wrappermode=yes` sur le port 465 est un classique.

```yaml
email:
  imap_addr: mail.internal:993
  imap_username: rousseau
  imap_password: "..."

  smtp_addr: mail.internal:465
  smtp_username: rousseau
  smtp_password: "..."

  from: rousseau@internal
```

Si votre serveur est STARTTLS-uniquement (soumission SMTP sur 587), rousseau refusera de s'authentifier — le transport n'envoie pas de credentials en clair. Voir la section migration ci-dessous.

  </div>
</div>

## Migrer depuis des serveurs STARTTLS-uniquement

Rousseau utilise le TLS implicite en IMAP (993) et SMTP (465). Si votre infrastructure mail existante n'offre que STARTTLS en 143 (IMAP) ou 587 (soumission SMTP), vous avez trois options :

1. **Activez le TLS implicite sur votre serveur.** Postfix supporte `smtpd_tls_wrappermode=yes` en écoute sur le port 465. Dovecot supporte le service `imaps` sur le port 993 d'emblée.
2. **Placez un proxy de terminaison TLS devant le serveur.** `stunnel` peut accepter du TLS implicite en 465 et le forwarder en STARTTLS en 587.
3. **Attendez le support STARTTLS.** Élément de roadmap ; voir `docs/GAP_ANALYSIS_2026.md`.

## Rendu texte vs HTML

Le sortant est `text/plain; charset=utf-8`. Aucun template HTML. C'est délibéré — le texte brut est rendu universellement, n'embarque pas de pixels de tracking, et ne casse jamais dans un client mail texte-only. Pour une sortie HTML, encapsulez le transport et réécrivez `SendMail` :

```go
// Custom transport that emits multipart/alternative.
type MyEmailClient struct{ email.Client }

func (c *MyEmailClient) Deliver(ctx context.Context, to, body string) error {
    html := markdown.ToHTML([]byte(body), nil, nil)
    // ... construct multipart/alternative message, call net/smtp.SendMail ...
}
```

Le cœur de rousseau reste en texte brut ; le HTML relève de l'appelant.

## Modes d'échec

| Symptôme | Correctif |
|---|---|
| Erreurs `imapclient.DialTLS` | Vérifiez que le port 993 est ouvert en sortie et que le certificat TLS est valide. |
| `SMTP AUTH failed` | `PlainAuth` exige que le hostname du serveur d'authentification corresponde à `smtp_addr`. Les fournisseurs avec load balancers peuvent présenter un nom différent. |
| Les messages ne sont jamais marqués SEEN | Le handler a renvoyé une erreur. Corrigez la cause racine ; rousseau ne retente pas indéfiniment. |
| Réponses en double | Deux instances de rousseau sur la même boîte ; une seule doit tourner. |
| `AUTHENTICATE failed: Application-specific password required` | Gmail avec 2FA activée, et le mot de passe du compte a été utilisé au lieu d'un mot de passe applicatif. Voir le parcours Gmail plus haut. |

## Dépannage

### `dial tcp: connect: connection refused`

Mauvais port. Assurez-vous que `imap_addr` utilise `:993` (pas `:143`) et que `smtp_addr` utilise `:465` (pas `:587` pour les serveurs STARTTLS-uniquement).

### Le bot répond au spam

Tout message dans INBOX en `UNSEEN` est traité. Filtrez le spam au niveau de la boîte (règles côté serveur, filtre spam Gmail), ou configurez un `mailbox:` différent d'INBOX et routez-y les mails avec une règle côté serveur.

### `SendMail` réussit mais le message n'arrive jamais

Consultez le mail log du serveur SMTP. Causes fréquentes : échec de signature DKIM (le domaine du `From:` ne correspond pas à un domaine que votre serveur peut signer), reverse DNS non concordant, SPF du domaine destinataire bloque votre IP.

### L'unicode dans le corps s'affiche en `?????`

Un maillon du chemin a supprimé l'UTF-8. Vérifiez la présence de `Content-Type: text/plain; charset=utf-8` dans le message envoyé (rousseau la positionne toujours) et qu'aucun relai ne transcode.

### Le polling prend des secondes même après un changement de config

`poll_interval` n'est relu qu'au démarrage du daemon. Redémarrez pour prendre en compte la nouvelle valeur.

## Pages liées

- [Prise en main : Premier transport](/fr/getting-started/first-transport/) — parcours de bout en bout.
- [Configuration](/fr/configuration/) — le bloc de config `email`.
- [Transports](/fr/transports/) — transports voisins.
- [Déploiement](/fr/deployment/) — exécuter Email dans un conteneur Podman.
- [Cron](/fr/cron/) — envoyer des synthèses planifiées par email.

## Pour aller plus loin

- `internal/transport/email/client.go` — polling IMAP, envoi SMTP, parsing des messages.
- `internal/cli/email.go` — câblage CLI.
- `internal/config/config.go` — struct `EmailConfig`.
- [Docs emersion/go-imap](https://github.com/emersion/go-imap) — la bibliothèque IMAP.
