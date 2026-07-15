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
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "en-GB"
locale: "en_GB"
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
permalink: "https://docs.rousseau-agent.dev/transports/email/"
subtitle: "IMAP inbound plus SMTP outbound over TLS."
tags: "transports, email"
title: "Email Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "email, IMAP, SMTP, TLS, PlainAuth, INBOX, poll interval, RFC 5322, UTF-8"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Email Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 20
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/email/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/email/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Email Transport"
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
twitter_title: "Email Transport"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>The Gmail app-password walkthrough, how to configure the transport for Fastmail / Google Workspace / a self-hosted mail server, the migration path from STARTTLS-only servers, and the plain-vs-HTML rendering trade-off. Read <code>internal/transport/email/client.go</code> alongside this page.</p></aside>

## Overview

The email transport (`internal/transport/email/`) is a pair: **IMAP inbound** (via `github.com/emersion/go-imap/v2`) and **SMTP outbound** (via Go's standard-library `net/smtp`).

It polls INBOX for `UNSEEN` messages, flags them `SEEN` after handoff to the handler, and replies via `net/smtp.SendMail`.

## TLS posture

**Both ends are full TLS.** The transport uses `imapclient.DialTLS` on the IMAP side and `smtp.SendMail` with `PlainAuth` over an already-TLS-wrapped connection on the SMTP side. STARTTLS-only IMAP or SMTP servers are **not currently supported** — the daemon refuses to send plaintext credentials over an unencrypted socket.

Standard TLS ports:

- IMAP: `993`
- SMTP submission: `465` (implicit TLS) — full TLS. **Not `587` unless your provider does implicit TLS on 587 as well.**

Some providers (Google Workspace, Fastmail) accept SMTP submission on `465` with implicit TLS. Verify your provider before configuring.

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

| Field | Default | Effect |
|---|---|---|
| `imap_addr` | *required* | `host:port` for TLS IMAP. |
| `imap_username` | *required* | IMAP username. |
| `imap_password` | *required* | IMAP password. |
| `mailbox` | `INBOX` | Mailbox to poll. |
| `poll_interval` | `30s` | How often to look for UNSEEN mail. |
| `smtp_addr` | *required* | `host:port` for SMTP submission. |
| `smtp_username` | *required* | SMTP username. |
| `smtp_password` | *required* | SMTP password. |
| `from` | *required* | Envelope + header `From` address. |
| `reply_header` | *empty* | Prepended to every outbound message body. |

## Command-line

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

## Outbound message shape

Replies are RFC 5322-compliant. rousseau writes:

```
From: bot@example.com
To: sender@example.com
Subject: Re: <inbound subject>
Content-Type: text/plain; charset=utf-8
MIME-Version: 1.0

<reply_header><body>
```

UTF-8 is unconditional. HTML output is out of scope; there is no template engine wired in.

## Inbound message shape

`UNSEEN` messages are parsed into an `IncomingMessage` with:

- `From` = the parsed `From` header address.
- `Body` = the concatenated `text/plain` parts.
- `At` = the `INTERNALDATE` from IMAP.

Attachments, `text/html`, and inline images are ignored.

## Mailbox choice

`mailbox: "INBOX"` is the default. Point at a Gmail label (`"[Gmail]/label"`) or a Fastmail folder for finer filtering — anything the IMAP server exposes works.

## Provider-specific setup

<div class="tabs" data-tabs="email-provider">
  <div class="tab-list" role="tablist" aria-label="Email provider">
    <button role="tab" aria-selected="true">Gmail / Workspace</button>
    <button role="tab" aria-selected="false">Fastmail</button>
    <button role="tab" aria-selected="false">Outlook / M365</button>
    <button role="tab" aria-selected="false">Self-hosted</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Gmail app password walkthrough.** Regular Gmail passwords will not authenticate over IMAP/SMTP when 2FA is on. Generate an app password:

1. Visit https://myaccount.google.com/security. Confirm **2-Step Verification** is on.
2. Click **App passwords** (only visible with 2FA enabled).
3. Name the app "rousseau-agent", generate. Copy the 16-character password (spaces optional).

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

<aside class="admonition" data-type="warning"><span class="admonition-title">Google Workspace admin lock</span><p>Some Workspace admins disable app passwords org-wide. If <em>App passwords</em> is missing from your security page, ask your admin to allow "Less secure app access" or configure OAuth — rousseau does not yet support Gmail OAuth (roadmap).</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Fastmail supports app passwords under *Settings &gt; Password &amp; Security &gt; App passwords*. Create a password scoped to *Mail (IMAP/POP/SMTP)*:

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

Microsoft 365 has deprecated basic authentication (username + password) for most tenants. Rousseau does not yet support Modern Auth / OAuth (roadmap). Options:

1. Enable *Authenticated SMTP* per-mailbox in the M365 admin center (possible on some tenants).
2. Use a relay: run rousseau against a self-hosted IMAP+SMTP that forwards through M365 via SMTP with an app password.
3. Wait for OAuth support to land.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Any self-hosted mail server that speaks IMAP over TLS on 993 and SMTP submission over implicit TLS on 465 works out of the box. Postfix + Dovecot with `smtpd_tls_wrappermode=yes` on port 465 is a classic setup.

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

If your server is STARTTLS-only (port 587 SMTP submission), rousseau will refuse to authenticate — the transport does not send plaintext credentials. See the migration section below.

  </div>
</div>

## Migrating from STARTTLS-only servers

Rousseau uses implicit TLS on both IMAP (993) and SMTP (465). If your existing mail infrastructure only offers STARTTLS on 143 (IMAP) or 587 (SMTP submission), you have three options:

1. **Enable implicit TLS on your server.** Postfix supports `smtpd_tls_wrappermode=yes` bound to port 465. Dovecot supports `imaps` service on port 993 out of the box.
2. **Front the server with a TLS-terminating proxy.** `stunnel` can accept implicit TLS on 465 and forward as STARTTLS on 587.
3. **Wait for STARTTLS support.** Roadmap item; see `docs/GAP_ANALYSIS_2026.md`.

## Plain vs HTML rendering

Outbound is `text/plain; charset=utf-8`. No HTML template. This is deliberate — plain text is universally rendered, does not embed tracking pixels, and never breaks in a text-only email client. If you want HTML output, wrap the transport and rewrite `SendMail`:

```go
// Custom transport that emits multipart/alternative.
type MyEmailClient struct{ email.Client }

func (c *MyEmailClient) Deliver(ctx context.Context, to, body string) error {
    html := markdown.ToHTML([]byte(body), nil, nil)
    // ... construct multipart/alternative message, call net/smtp.SendMail ...
}
```

Rousseau's core stays plain-text; HTML is a caller concern.

## Failure modes

| Symptom | Fix |
|---|---|
| `imapclient.DialTLS` errors | Confirm port 993 is open outbound, TLS certificate is valid. |
| `SMTP AUTH failed` | `PlainAuth` requires the auth server hostname to match `smtp_addr`. Providers with load balancers may present a different name. |
| Messages never flagged SEEN | Handler returned an error. Fix the underlying issue; rousseau does not retry indefinitely. |
| Duplicate replies | Two rousseau instances on the same mailbox; only one should run. |
| `AUTHENTICATE failed: Application-specific password required` | Gmail with 2FA on, and the account password was used instead of an app password. See Gmail walkthrough above. |

## Troubleshooting

### `dial tcp: connect: connection refused`

Wrong port. Ensure `imap_addr` uses `:993` (not `:143`) and `smtp_addr` uses `:465` (not `:587` for STARTTLS-only servers).

### Bot replies to spam

Any message in INBOX with `UNSEEN` is handled. Filter spam at the mailbox level (server-side rules, Gmail spam filter) or configure a `mailbox:` different from INBOX and route mail into it with a server-side rule.

### `SendMail` succeeds but the message never arrives

Check the SMTP server's mail log. Common causes: DKIM signing failure (the `From:` domain does not match a domain your server can sign), reverse DNS mismatch, receiving domain's SPF blocks your IP.

### Unicode in message body renders as `?????`

Something along the path stripped UTF-8. Verify `Content-Type: text/plain; charset=utf-8` is in the sent message (rousseau always sets it) and that no relay is transcoding.

### Poll takes seconds even after config change

`poll_interval` is only re-read at daemon start. Restart to pick up the new value.

## Related pages

- [Getting Started: First Transport](/getting-started/first-transport/) — end-to-end walkthrough.
- [Configuration](/configuration/) — the `email` config block.
- [Transports](/transports/) — sibling transports.
- [Deployment](/deployment/) — running Email in a Podman container.
- [Cron](/cron/) — send scheduled digests via email.

## Further reading

- `internal/transport/email/client.go` — IMAP poll, SMTP send, message parsing.
- `internal/cli/email.go` — CLI wiring.
- `internal/config/config.go` — `EmailConfig` struct.
- [emersion/go-imap docs](https://github.com/emersion/go-imap) — the IMAP library.
