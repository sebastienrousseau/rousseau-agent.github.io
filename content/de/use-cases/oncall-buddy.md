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
description: "Use case narrative: a solo SRE running rousseau-agent over Slack to triage a 3 a.m. page from the couch, then hand off to full incident response."
keywords: "on-call, sre, slack, incident, page, triage, use case"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/use-cases/oncall-buddy/"
subtitle: "Triaging a 3 a.m. page from the couch over Slack."
tags: "use-cases, on-call, slack, sre"
title: "Anwendungsfall: On-Call-Buddy"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "on-call, sre, slack, incident, page, triage, use case"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Anwendungsfall: On-Call-Buddy"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 71
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/oncall-buddy/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/oncall-buddy/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Anwendungsfall: On-Call-Buddy"
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
twitter_title: "Anwendungsfall: On-Call-Buddy"
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

Es ist 3 Uhr morgens. Ihr Pager feuert. PagerDuty sagt, der Checkout-Dienst wirft 502s. Sie sind einer von zwei SREs in einer kleinen Firma, Ihr Co-Lead ist im Urlaub, und zu Ihrem Laptop zu kommen heißt, Ihre Brille zu finden, herunter zu gehen und ein VPN zu entsperren. Vor all dem möchten Sie eine erste Antwort: welche Dashboards schlecht aussehen, was sich in den letzten 24 Stunden geändert hat, welches Runbook zutrifft.

Rousseau lebt auf der Ops-Box in Ihrem Schrank. Er hat Read-only-Credentials für Ihren Logging-Stack, Read-only-kubectl in einem Namespace und eine Slack-Socket-Mode-Verbindung in `#incident-oncall`. Sie tippen auf die DM-Benachrichtigung auf Ihrem Telefon:

> was hat sich in checkout in den letzten 24h geändert?

Rousseau liest das git-Log für das Checkout-Service-Repo, kreuzreferenziert gegen Ihr Deploy-Log (aus einem bind-gemounteten Verzeichnis) und antwortet:

> Zwei Änderungen: PR #4821 (Payment-Retry-Logik, um 21:14 UTC deployt) und ein Helm-Value-Bump auf `checkout-web` um 22:03 UTC. Die Payment-Retry-Änderung ist die verdächtigere — sie berührt denselben Codepfad, aus dem die aktuellen 502s stammen.

Sie fragen:

> zieh die letzten 100 Fehlerzeilen von checkout-web

Rousseau führt `kubectl logs -n checkout deploy/checkout-web --tail=100 --previous` unter seinem Read-only-kubeconfig aus und fügt die wesentlichen Zeilen zurück ein. Sie entdecken einen Null-Pointer-Trace. Sie schreiben DM zurück:

> revertiere PR #4821 zuerst in staging — ruf mich, wenn es bestätigt grün ist

Rousseau postet in `#incident-oncall` einen Plan, öffnet einen Revert-PR gegen Staging und pingt zurück, sobald Staging grün ist. Sie stehen auf und gehen zu Ihrem Laptop.

## Was das erfordert

### Der Daemon

Rousseau läuft als rootless Podman-Container auf der Ops-Box:

- **Provider**: `bedrock` — Ihre Firma hat bereits ein Bedrock-Spend-Commitment; keine per-Nutzer-API-Schlüssel erforderlich.
- **Transport**: Slack Socket Mode — keine Inbound-HTTP-Oberfläche, nur Outbound-WebSocket.
- **State**: `~/.local/share/rousseau/sessions.db`, auf einer LUKS-verschlüsselten Disk.

### Konfiguration

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

### Die Bind-Mounts

- Repo-Checkouts unter `/workspace/repos/` (read-only).
- Deploy-Log unter `/workspace/deploys/` (read-only).
- kubeconfig unter `/home/rousseau/.kube/config` — read-only gemountet, Service-Account hat Read-only-Cluster-Rolle im `checkout`-Namespace.
- AWS-Credentials über IAM Role for Service Accounts (IRSA), wenn auf EKS, oder über ein gemountetes `~/.aws/` für On-Prem.

### Die systemd-Quadlet-Unit

Die Referenz `docker/rousseau-agent.container` mit:

- `ReadOnly=true`
- `DropCapability=all`
- `NoNewPrivileges=true`
- `Restart=on-failure`

Startet beim Host-Neustart. Journal verfügbar via `journalctl --user -u rousseau-agent.service`.

## Die Sicherheitshaltung

- **Slack-Allowlist** stellt sicher, dass nur Sie und Ihr Co-Lead den Daemon steuern können. Jeder andere DM wird stillschweigend abgewiesen.
- **Pattern-Approver mit `default: deny`** blockiert alles außerhalb der Whitelist. Wenn das Modell `kubectl delete pod` ausführen möchte, erhält es einen `tool_result`-Fehler, der die Blockade erklärt, und leitet auf ein Plandokument um.
- **Read-only-kubeconfig + Read-only-Repo-Mounts** bedeuten, dass der Daemon Produktion *nicht* mutieren kann, selbst wenn der Approver offen ausfällt.
- **Gürtel, Hosenträger und ein zweiter Gürtel** — jede Schicht fällt sicher aus.

## Was rousseau hier nicht tut

- **Es pagt Sie nicht.** PagerDuty ist die Quelle der Wahrheit dafür, wer on-call ist.
- **Es merged keine PRs.** Der Approver blockiert `gh pr merge`. Rousseau kann einen Entwurfs-Revert öffnen; ein Mensch muss noch bestätigen.
- **Es führt kein `kubectl exec` aus.** Jeder Befehl, der Cluster-Zustand mutieren könnte, wird abgelehnt.
- **Es lernt nicht aus dem Vorfall.** Cross-Session-Recall via FTS5 bedeutet, dass das rousseau des nächsten Vorfalls Keywords aus der heutigen Sitzung findet; die semantischen Schlussfolgerungen sind weiterhin Aufgabe des Operators.

## Was Sie unter Last ändern würden

Wenn zwei 3-Uhr-morgens-Pages pro Monat zu zwei pro Woche werden:

- Erwägen Sie, mehr `bash`-Matcher in `allow` hochzustufen, während Sie Vertrauen gewinnen.
- Verdrahten Sie die slog-Ausgabe in [Loki](/de/guides/observability/), damit Post-mortem-Reviews die exakten Tool-Aufrufe zitieren können, die rousseau gemacht hat.
- Fügen Sie [geplante Aufgaben](/de/guides/scheduled-tasks/) hinzu, damit rousseau einen nächtlichen Digest offener Vorfälle in Ihr morgendliches Slack ausführt.

## Verwandte Seiten

- [Leitfäden: Audit + Freigaberichtlinien](/de/guides/audit-approval-policies/) — der Sicherheitshebel.
- [Leitfäden: Read-only-Modus](/de/guides/read-only-mode/) — die strengste Haltung.
- [Slack-Transport](/de/transports/slack/) — Socket-Mode-Verdrahtung.
- [Bedrock-Provider](/de/providers/bedrock/) — Auth-Chain.
