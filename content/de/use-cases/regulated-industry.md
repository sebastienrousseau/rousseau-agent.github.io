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
description: "Use case narrative: a financial-services team running rousseau-agent in-tenant on AWS with Bedrock, pattern-mode approvals, and SLSA-3 supply-chain posture."
keywords: "regulated industry, financial services, bedrock, in-tenant, slsa, cosign, compliance"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/use-cases/regulated-industry/"
subtitle: "In-tenant Bedrock deployment for a financial-services team."
tags: "use-cases, bedrock, regulated, financial-services, slsa"
title: "Anwendungsfall: regulierte Branche"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "regulated industry, financial services, bedrock, in-tenant, slsa, cosign, compliance"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Anwendungsfall: regulierte Branche"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 73
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/regulated-industry/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/regulated-industry/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Anwendungsfall: regulierte Branche"
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
twitter_title: "Anwendungsfall: regulierte Branche"
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

Sie sind Plattform-Ingenieur bei einer mittelgroßen Bank. Compliance verlangt, dass jeder Coding-Assistent, den Ihre Ingenieure verwenden, folgende Anforderungen erfüllt:

1. Läuft innerhalb der AWS-Konten der Bank, nicht auf einer SaaS-Control-Plane.
2. Leitet Modell-Traffic durch einen Provider, mit dem die Bank einen Vertrag und einen Audit-Trail hat (Bedrock).
3. Hat eine dokumentierte Lieferketten-Haltung (SLSA-3, SBOM, Signaturverifikation).
4. Erzwingt Freigaberichtlinien mit einem maschinenlesbaren Audit-Trail.
5. Exfiltriert keinen Quellcode an Dritte.

Die Positionierung von rousseau bildet jede dieser Anforderungen ab. Sie betreiben es als Kubernetes-`Deployment` im EKS-Cluster des Plattformteams und steuern einen Slack-Socket-Mode-Transport in den Engineering-Kanal.

Der Engineering-Rollout ist unspektakulär — ein `Deployment`, ein `Secret`, eine `ConfigMap`, ein `PersistentVolumeClaim`. Die Geschichte ist das, was passiert, wenn der Auditor kommt.

## Das Audit

Ein externer Auditor stellt vier Fragen.

**F1: Wohin geht der Modell-Traffic?**

Sie verweisen ihn auf `internal/llm/bedrock/`. Der Provider verwendet die standardmäßige AWS-Credential-Chain (via IRSA auf EKS), sodass Credentials kurzlebige STS-Tokens sind. Der Traffic verlässt niemals Ihr AWS-Konto.

**F2: Wie verifizieren Sie das Binary, das Sie ausführen?**

Sie zeigen ihm `docker/Dockerfile` — ein Multi-Stage-Build mit einer gepinnten `golang:1.26-alpine`-Basis — und das `release-verify.sh`-Skript, das das SRE-Team während der Image-Promotion ausführt:

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_${VERSION}_checksums.txt.sig \
  rousseau_${VERSION}_checksums.txt

sha256sum -c rousseau_${VERSION}_checksums.txt
```

Sie ergänzen: SLSA-3-Provenienz wird über GitHub-Actions-OIDC attestiert. Das Sigstore-Transparenz-Log ist ein öffentlicher Vertrauensanker.

**F3: Wie verhindern Sie, dass das Modell Produktion mutiert?**

Sie verweisen ihn auf die `agent.approver`-Konfiguration:

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

Deny gewinnt gegen Allow. Nicht getroffen → deny. Jede Entscheidung wird als strukturiertes slog-Ereignis (`tool.execute`, `tool.denied`) protokolliert und über ein Vector-Daemonset an den Datadog-Tenant der Bank weitergeleitet.

**F4: Wo wird der Quellcode gespeichert, den eine Sitzung referenziert?**

Sie erklären: Der Sitzungszustand lebt auf einem PVC, das von EBS mit Encryption-at-Rest gestützt wird. Modell-Kontext bleibt innerhalb der komprimierten Sitzung (siehe [Komprimierung + Recall](/de/user-guide/compression-recall/)). Der FTS5-Recall-Index läuft auf demselben PVC. Nichts geht an `agentskills.io` oder eine externe URL — [Skills](/de/skills/) werden aus einem bind-gemounteten Verzeichnis geladen, nicht aus einer gehosteten Registry.

Der Auditor stellt eine Folgefrage: „Was ist mit dem Modell selbst?" Sie erklären, dass Bedrock die Modellgrenze ist; alles, was Bedrock mit Prompts tut, wird durch den bestehenden Vertrag der Bank mit AWS geregelt.

## Was das erfordert

### Das Manifest

Siehe [Leitfäden: Kubernetes-Bereitstellung](/de/guides/kubernetes-deployment/) für das vollständige Manifest. Wichtige Abweichungen für diesen Anwendungsfall:

- **Namespace `pod-security.kubernetes.io/enforce: restricted`.**
- **IRSA** für Bedrock-Credentials — keine langlebigen AWS-Schlüssel in Secrets.
- **NetworkPolicy**, die Egress nur zu Bedrock-Regionalendpunkten und Slack-WSS erlaubt.
- **Vector-Daemonset**, das slog-Ausgabe an Datadog liefert, wobei das `msg`-Feld als Facet geparst wird.

### Die Konfiguration

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

### Die Audit-Geschichte

Jeder Tool-Aufruf ist eine slog-Zeile. Jede Ablehnung eine weitere. Der Datadog-Monitor auf `msg:tool.denied` alarmiert das SOC. Wöchentlich zieht das Plattformteam einen Bericht:

```
# LogQL / Datadog / whichever
sum by (name) (
  count_over_time({job="rousseau-agent"} |= "tool.denied" [1w])
)
```

Der Bericht geht in das Compliance-Laufwerk. Weil das slog-Schema stabil ist ([Observability](/de/guides/observability/)), bricht das Parsen über rousseau-Upgrades hinweg nicht.

## Was der Auditor eventuell nicht fragt, aber sollte

- **Reproduzierbare Builds.** Die CI von rousseau enthält einen `reproducible-build`-Job, der bit-identische Ausgabe bei frischen Checkouts verifiziert. Sie können unabhängig aus einer getaggten Quelle neu bauen und SHA-256 vergleichen.
- **Dependency-Pinning.** `go.mod` pinnt exakte Versionen; `go.sum` ist eingefroren. Dependabot öffnet Updates als reviewbare PRs, nicht als stille Bumps.
- **`govulncheck` bei jedem Commit.** Jede bekannte Schwachstelle, die ein importiertes Symbol erreicht, lässt die CI fehlschlagen.
- **CodeQL**-Statikanalyse bei jedem Commit.

All das Obige steht in [Sicherheit](/de/security/) — die Compliance-Aktenschublade existiert bereits.

## Die Out-of-Tenant-Grenze

Bedrock ist die Grenze. Traffic zu `bedrock-runtime.eu-west-1.amazonaws.com` verlässt den Pod, bleibt aber innerhalb von AWS. Das Data-Flow-Diagramm der Bank zeigt einen Pfeil vom Pod zu Bedrock; keine weiteren Outbound-Pfeile existieren für diese Bereitstellung (Slack Socket Mode ist Outbound-WSS zu `wss-primary.slack.com`, was als separater erlaubter Egress dokumentiert ist).

## Verwandte Seiten

- [Leitfäden: Kubernetes-Bereitstellung](/de/guides/kubernetes-deployment/) — die Manifeste.
- [Leitfäden: Audit + Freigaberichtlinien](/de/guides/audit-approval-policies/) — die Compliance-Geschichte.
- [Leitfäden: Observability](/de/guides/observability/) — die slog-Pipeline.
- [Bedrock-Provider](/de/providers/bedrock/) — Credential-Chain und Regionsverhalten.
- [Sicherheit](/de/security/) — Vertrauensmodell und Lieferkettenkontrollen.
