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
description: "Use case narrative: reviewing pull requests from WhatsApp on the train, driven by rousseau-agent on a home box."
keywords: "mobile review, whatsapp, pr review, commute, use case, pull request"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/use-cases/mobile-review/"
subtitle: "Reviewing PRs from your phone on the train."
tags: "use-cases, whatsapp, mobile, pr"
title: "Anwendungsfall: mobile PR-Review"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "mobile review, whatsapp, pr review, commute, use case, pull request"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Anwendungsfall: mobile PR-Review"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 72
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/mobile-review/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/mobile-review/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Anwendungsfall: mobile PR-Review"
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
twitter_title: "Anwendungsfall: mobile PR-Review"
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

## Die Geschichte

Sie sind Staff-Engineer in einer mittelgroßen Firma. Ihr Posteingang hat acht offene PRs, die auf Ihr Review warten. Sie sind auf einer 45-minütigen Zugfahrt und haben Signal, aber keinen Laptop. Historisch bedeutet PR-Review vom Telefon: an GitHubs Diff-Ansicht zu schielen und hohle „LGTM"-Kommentare zu tippen.

Rousseau lebt auf dem kleinen Intel-NUC in Ihrem Schrank. Er hat eine WhatsApp-Verbindung zu Ihrer JID, `bypassPermissions` auf der lokalen `claude`-CLI und Read-Zugriff auf Ihre lokalen Checkouts der drei Repos, die Sie reviewen. Sie schreiben WhatsApp DM:

> review PR #4821 in checkout-service

Rousseau führt `gh pr diff 4821` aus, liest den Code und antwortet:

> PR #4821 fügt Retry-with-Backoff zum Stripe-Webhook-Handler hinzu. Drei Beobachtungen:
>
> 1. Das Backoff ist ungedeckelt — wenn Stripe wirklich down ist, akkumulieren wir für immer Goroutinen. Vorschlag: `context.WithTimeout` beim Aufrufer.
> 2. Die Testdatei fügt zwei neue Tests hinzu, aber keiner deckt den Timeout-Pfad ab.
> 3. `pkg/webhook.go:82` — der Mutex wird über den Netzwerkaufruf hinweg gehalten. Klein.
>
> Soll ich einen Review-Kommentar-Entwurf verfassen?

Sie antworten:

> ja, mit allen dreien

Rousseau verwendet `gh pr review` mit `--draft` (der Approver blockiert die finale Freigabe; ein Mensch muss noch auf „submit review" klicken). Wenn Sie an Ihrem Schreibtisch ankommen, wartet der Entwurfskommentar.

## Was das erfordert

### Der Daemon

Rousseau auf dem NUC als rootless Podman-Container:

- **Provider**: `claudecli` — erbt Ihre lokale Claude-Code-Auth.
- **Transport**: WhatsApp — der Transport der Wahl für mobile Reichweite.
- **State**: `~/.local/share/rousseau/sessions.db`.

### Konfiguration

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

### Die Bind-Mounts

- `~/repos/checkout-service/` (read-only).
- `~/repos/payments-api/` (read-only).
- `~/repos/web-frontend/` (read-only).
- `~/.claude/` — OAuth-Tokens von Claude Code (read-write, aber nur für Token-Refresh).
- `~/.config/gh/` — OAuth-Token der GitHub-CLI (read-write, gleicher Grund).

Read-only-Mounts verhindern, dass das Modell versehentlich Ihre Working-Copy editiert. Reviews gehen über GitHub, nicht über Ihren Checkout.

### Erster Start

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Sie scannen den QR-Code einmal. Von da an lebt der Daemon in der Quadlet-Unit und startet beim Host-Neustart. Ihre Allowlist ist die JID Ihres eigenen persönlichen Telefons.

## Die Sicherheitshaltung

- **Allowlist sperrt den Transport.** Nur Ihr Telefon kann den Daemon steuern. Jeder andere, der irgendwie die Telefonnummer entdeckt, wird stillschweigend abgewiesen.
- **Pattern-Approver blockiert jeden Merge / Push / Close.** Rousseau reviewt, entwirft und kommentiert — ein Mensch muss noch auf „Merge" oder „Approve" klicken.
- **Read-only-Mounts** schützen Ihre arbeitenden Checkouts.
- **`bypassPermissions` auf claudecli** ist nur tolerierbar, weil der Approver die Sicherheitsarbeit leistet. Kombinieren Sie `bypassPermissions` niemals mit `mode: allow_all`.

## Die Reichweite

- **Signal-Abbrüche in der U-Bahn.** Der Backpressure von WhatsApp ist elegant — Sie senden eine Frage, Sie bekommen eine Antwort, wenn der Daemon Signal zum Antworten hat. Rousseau muss keine Live-TCP-Sitzung mit Ihrem Telefon halten.
- **Sprachnotizen funktionieren.** Mit aktiviertem [Voice-Modus](/de/user-guide/voice-mode/) und `whisper.cpp` auf dem NUC installiert, können Sie eine Sprachnotiz „was ist der Diff auf 4821" diktieren und eine Textantwort erhalten. Nützlich, wenn das Tippen auf einem Telefon in einem fahrenden Zug ärgerlich ist.
- **Der Daemon läuft auf Ihrer Hardware.** Nichts an Ihrem Review-Räsonieren geht an eine Drittanbieter-SaaS. Der einzige Outbound-Aufruf ist der Subprozess der `claude`-CLI zu Anthropic, unter Verwendung Ihres bestehenden Abonnements.

## Was rousseau hier nicht tut

- **Es klickt nicht auf „Merge".** Das ist eine menschliche Entscheidung, und der Approver setzt sie durch.
- **Es lernt Ihren Review-Stil nicht.** Der nächste PR bekommt dieselbe generische Checkliste, es sei denn, Sie verfassen einen [Skill](/de/skills/), der Ihren Stil erfasst.
- **Es reiht Reviews nicht in eine Queue.** Jede Anfrage ist unabhängig; es gibt keinen „reviewe alle meine offenen PRs"-Hintergrundjob (es sei denn, Sie verdrahten einen via [Cron](/de/guides/scheduled-tasks/)).

## Was Sie unter Last ändern würden

- Fügen Sie einen [Skill](/de/skills/) namens `pr-review-checklist.md` hinzu, der die sechs Dinge kodifiziert, die Sie immer prüfen. Skills werden in den System-Prompt eingespleißt, wenn ein passender Trigger in der Nutzernachricht erscheint.
- Fügen Sie einen nächtlichen Cron hinzu: `0 8 * * 1-5 rousseau ... deliver a summary of every open PR`.
- Wechseln Sie auf einen kostenpflichtigen Anthropic-API-Pfad, wenn die `claudecli`-Abonnement-Rate-Limits zum Flaschenhals werden. Null Konfigurationsänderungen stromabwärts.

## Verwandte Seiten

- [WhatsApp-Transport](/de/transports/whatsapp/) — die Transport-Referenz.
- [claudecli-Provider](/de/providers/claudecli/) — geerbte Auth.
- [Skills](/de/skills/) — wie Sie Ihren Review-Stil kodifizieren.
- [Voice-Modus](/de/user-guide/voice-mode/) — Reviews diktieren.
