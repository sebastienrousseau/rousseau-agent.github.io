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
hreflang: "de"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "de"
locale: "de_DE"
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
permalink: "https://docs.rousseau-agent.dev/de/transports/email/"
subtitle: "IMAP inbound plus SMTP outbound over TLS."
tags: "transports, email"
title: "E-Mail-Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "email, IMAP, SMTP, TLS, PlainAuth, INBOX, poll interval, RFC 5322, UTF-8"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "E-Mail-Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 20
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/email/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/email/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "E-Mail-Transport"
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
twitter_title: "E-Mail-Transport"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Den Gmail-App-Passwort-Durchlauf, wie Sie den Transport für Fastmail / Google Workspace / einen selbstgehosteten Mail-Server konfigurieren, den Migrationspfad von Nur-STARTTLS-Servern und den Trade-off zwischen Klartext- und HTML-Rendering. Lesen Sie <code>internal/transport/email/client.go</code> parallel zu dieser Seite.</p></aside>

## Überblick

Der Email-Transport (`internal/transport/email/`) ist ein Paar: **IMAP-Ingress** (über `github.com/emersion/go-imap/v2`) und **SMTP-Ausgang** (über Gos Standardbibliothek `net/smtp`).

Er pollt INBOX auf `UNSEEN`-Nachrichten, markiert sie nach Übergabe an den Handler als `SEEN` und antwortet über `net/smtp.SendMail`.

## TLS-Posture

**Beide Enden sind volles TLS.** Der Transport nutzt `imapclient.DialTLS` auf der IMAP-Seite und `smtp.SendMail` mit `PlainAuth` über eine bereits TLS-umhüllte Verbindung auf der SMTP-Seite. Nur-STARTTLS-IMAP- oder -SMTP-Server werden **derzeit nicht unterstützt** – der Daemon weigert sich, Klartext-Credentials über einen unverschlüsselten Socket zu senden.

Standard-TLS-Ports:

- IMAP: `993`
- SMTP-Submission: `465` (implizites TLS) – volles TLS. **Nicht `587`, es sei denn, Ihr Provider bietet implizites TLS ebenfalls auf 587 an.**

Einige Provider (Google Workspace, Fastmail) akzeptieren SMTP-Submission auf `465` mit implizitem TLS. Prüfen Sie Ihren Provider vor der Konfiguration.

## Konfiguration

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

| Feld | Standard | Wirkung |
|---|---|---|
| `imap_addr` | *erforderlich* | `host:port` für TLS-IMAP. |
| `imap_username` | *erforderlich* | IMAP-Benutzername. |
| `imap_password` | *erforderlich* | IMAP-Passwort. |
| `mailbox` | `INBOX` | Zu pollende Mailbox. |
| `poll_interval` | `30s` | Wie oft nach UNSEEN-Mails gesucht wird. |
| `smtp_addr` | *erforderlich* | `host:port` für SMTP-Submission. |
| `smtp_username` | *erforderlich* | SMTP-Benutzername. |
| `smtp_password` | *erforderlich* | SMTP-Passwort. |
| `from` | *erforderlich* | Envelope- und Header-Absenderadresse (`From`). |
| `reply_header` | *leer* | Wird dem Body jeder ausgehenden Nachricht vorangestellt. |

## Befehlszeile

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

## Form der ausgehenden Nachricht

Antworten sind RFC-5322-konform. rousseau schreibt:

```
From: bot@example.com
To: sender@example.com
Subject: Re: <eingehender Betreff>
Content-Type: text/plain; charset=utf-8
MIME-Version: 1.0

<reply_header><body>
```

UTF-8 ist verpflichtend. HTML-Ausgabe liegt ausserhalb des Scopes; es ist keine Template-Engine verdrahtet.

## Form der eingehenden Nachricht

`UNSEEN`-Nachrichten werden in eine `IncomingMessage` geparst mit:

- `From` = die geparste `From`-Header-Adresse.
- `Body` = die verketteten `text/plain`-Teile.
- `At` = das `INTERNALDATE` aus IMAP.

Anhänge, `text/html` und Inline-Bilder werden ignoriert.

## Auswahl der Mailbox

`mailbox: "INBOX"` ist der Standard. Zeigen Sie auf ein Gmail-Label (`"[Gmail]/label"`) oder einen Fastmail-Ordner für feinere Filterung – alles, was der IMAP-Server exponiert, funktioniert.

## Provider-spezifische Einrichtung

<div class="tabs" data-tabs="email-provider">
  <div class="tab-list" role="tablist" aria-label="Email provider">
    <button role="tab" aria-selected="true">Gmail / Workspace</button>
    <button role="tab" aria-selected="false">Fastmail</button>
    <button role="tab" aria-selected="false">Outlook / M365</button>
    <button role="tab" aria-selected="false">Selbstgehostet</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Gmail-App-Passwort-Durchlauf.** Reguläre Gmail-Passwörter authentifizieren sich bei aktiviertem 2FA nicht über IMAP/SMTP. Erstellen Sie ein App-Passwort:

1. Öffnen Sie https://myaccount.google.com/security. Bestätigen Sie, dass **Bestätigung in zwei Schritten** aktiv ist.
2. Klicken Sie auf **App-Passwörter** (nur bei aktivem 2FA sichtbar).
3. Vergeben Sie den App-Namen "rousseau-agent", generieren. Kopieren Sie das 16-stellige Passwort (Leerzeichen optional).

Config:

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

<aside class="admonition" data-type="warning"><span class="admonition-title">Workspace-Admin-Sperre</span><p>Einige Workspace-Admins deaktivieren App-Passwörter organisationsweit. Fehlt <em>App-Passwörter</em> auf Ihrer Sicherheitsseite, bitten Sie Ihren Admin, "Zugriff durch weniger sichere Apps" zu erlauben oder OAuth zu konfigurieren – rousseau unterstützt Gmail-OAuth noch nicht (Roadmap).</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Fastmail unterstützt App-Passwörter unter *Settings &gt; Password &amp; Security &gt; App passwords*. Erstellen Sie ein Passwort mit Scope *Mail (IMAP/POP/SMTP)*:

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

Microsoft 365 hat Basic Authentication (Benutzername + Passwort) für die meisten Tenants abgekündigt. Rousseau unterstützt Modern Auth / OAuth noch nicht (Roadmap). Optionen:

1. *Authenticated SMTP* pro Postfach im M365-Admin-Center aktivieren (bei einigen Tenants möglich).
2. Einen Relay nutzen: Rousseau gegen ein selbstgehostetes IMAP+SMTP betreiben, das über SMTP mit einem App-Passwort durch M365 weiterleitet.
3. Auf OAuth-Support warten.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Jeder selbstgehostete Mail-Server, der IMAP über TLS auf 993 und SMTP-Submission über implizites TLS auf 465 spricht, funktioniert sofort. Postfix + Dovecot mit `smtpd_tls_wrappermode=yes` auf Port 465 ist ein klassisches Setup.

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

Ist Ihr Server nur-STARTTLS (Port 587 SMTP-Submission), verweigert rousseau die Authentifizierung – der Transport sendet keine Klartext-Credentials. Siehe den Migrationsabschnitt unten.

  </div>
</div>

## Migration von Nur-STARTTLS-Servern

Rousseau nutzt implizites TLS sowohl auf IMAP (993) als auch auf SMTP (465). Bietet Ihre bestehende Mail-Infrastruktur nur STARTTLS auf 143 (IMAP) oder 587 (SMTP-Submission), haben Sie drei Optionen:

1. **Implizites TLS auf Ihrem Server aktivieren.** Postfix unterstützt `smtpd_tls_wrappermode=yes` auf Port 465. Dovecot unterstützt den `imaps`-Service auf Port 993 out of the box.
2. **Server hinter einem TLS-terminierenden Proxy betreiben.** `stunnel` kann implizites TLS auf 465 annehmen und als STARTTLS auf 587 weiterleiten.
3. **Auf STARTTLS-Support warten.** Roadmap-Punkt; siehe `docs/GAP_ANALYSIS_2026.md`.

## Klartext vs. HTML-Rendering

Der Ausgang ist `text/plain; charset=utf-8`. Kein HTML-Template. Das ist bewusst – Klartext wird universell gerendert, enthält keine Tracking-Pixel und bricht in keinem Text-only-Mail-Client. Wenn Sie HTML-Ausgabe wollen, wrappen Sie den Transport und schreiben `SendMail` um:

```go
// Custom-Transport, der multipart/alternative emittiert.
type MyEmailClient struct{ email.Client }

func (c *MyEmailClient) Deliver(ctx context.Context, to, body string) error {
    html := markdown.ToHTML([]byte(body), nil, nil)
    // ... multipart/alternative-Nachricht bauen, net/smtp.SendMail aufrufen ...
}
```

Der Kern von rousseau bleibt Klartext; HTML ist Sache des Aufrufers.

## Fehlermodi

| Symptom | Lösung |
|---|---|
| `imapclient.DialTLS`-Fehler | Prüfen, dass Port 993 ausgehend offen ist und das TLS-Zertifikat gültig ist. |
| `SMTP AUTH failed` | `PlainAuth` erfordert, dass der Auth-Server-Hostname mit `smtp_addr` übereinstimmt. Provider mit Load-Balancern können einen anderen Namen präsentieren. |
| Nachrichten werden nie SEEN markiert | Handler hat einen Fehler zurückgegeben. Ursache beheben; rousseau wiederholt nicht endlos. |
| Doppelte Antworten | Zwei rousseau-Instanzen auf derselben Mailbox; nur eine sollte laufen. |
| `AUTHENTICATE failed: Application-specific password required` | Gmail mit aktivem 2FA, und das Konto-Passwort wurde statt eines App-Passworts verwendet. Siehe Gmail-Durchlauf oben. |

## Fehlerbehebung

### `dial tcp: connect: connection refused`

Falscher Port. Stellen Sie sicher, dass `imap_addr` `:993` nutzt (nicht `:143`) und `smtp_addr` `:465` (nicht `:587` für Nur-STARTTLS-Server).

### Bot antwortet auf Spam

Jede Nachricht in INBOX mit `UNSEEN` wird verarbeitet. Filtern Sie Spam auf Mailbox-Ebene (serverseitige Regeln, Gmail-Spam-Filter) oder konfigurieren Sie ein `mailbox:` ungleich INBOX und leiten Sie Mails mit einer serverseitigen Regel dorthin.

### `SendMail` gelingt, aber die Nachricht kommt nie an

Prüfen Sie das Mail-Log des SMTP-Servers. Häufige Ursachen: DKIM-Signaturfehler (die `From:`-Domain passt zu keiner Domain, die Ihr Server signieren kann), Reverse-DNS-Diskrepanz, SPF der Empfängerdomain blockiert Ihre IP.

### Unicode im Nachrichten-Body wird als `?????` gerendert

Etwas auf dem Pfad hat UTF-8 entfernt. Stellen Sie sicher, dass `Content-Type: text/plain; charset=utf-8` in der gesendeten Nachricht steht (rousseau setzt es immer) und dass kein Relay transkodiert.

### Poll dauert Sekunden, auch nach Config-Änderung

`poll_interval` wird nur beim Daemon-Start neu gelesen. Neu starten, um den neuen Wert zu übernehmen.

## Verwandte Seiten

- [Getting Started: Erster Transport](/de/getting-started/first-transport/) – End-to-End-Durchlauf.
- [Konfiguration](/de/configuration/) – der `email`-Config-Block.
- [Transports](/de/transports/) – Geschwister-Transports.
- [Bereitstellung](/de/deployment/) – Email in einem Podman-Container betreiben.
- [Cron](/de/cron/) – geplante Digests per Email versenden.

## Weiterführende Lektüre

- `internal/transport/email/client.go` – IMAP-Poll, SMTP-Send, Nachrichten-Parsing.
- `internal/cli/email.go` – CLI-Verdrahtung.
- `internal/config/config.go` – `EmailConfig`-Struktur.
- [emersion/go-imap-Dokumentation](https://github.com/emersion/go-imap) – die IMAP-Bibliothek.
