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
description: "Use case narrative: a financial-services team running rousseau-agent in-tenant on AWS with Bedrock, pattern-mode approvals, and SLSA-3 supply-chain posture."
keywords: "regulated industry, financial services, bedrock, in-tenant, slsa, cosign, compliance"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/use-cases/regulated-industry/"
subtitle: "In-tenant Bedrock deployment for a financial-services team."
tags: "use-cases, bedrock, regulated, financial-services, slsa"
title: "Use Case: Regulated Industry"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "regulated industry, financial services, bedrock, in-tenant, slsa, cosign, compliance"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Use Case: Regulated Industry"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "use-cases"
order: 73
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/use-cases/regulated-industry/index.html"
item_link: "https://docs.rousseau-agent.dev/use-cases/regulated-industry/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Use Case: Regulated Industry"
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
twitter_title: "Use Case: Regulated Industry"
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

## The story

You are a platform engineer at a mid-sized bank. Compliance says any coding assistant your engineers use must:

1. Run inside the bank's AWS accounts, not on a SaaS control plane.
2. Route model traffic through a provider the bank has a contract and an audit trail with (Bedrock).
3. Have a documented supply-chain posture (SLSA-3, SBOM, signature verification).
4. Enforce approval policies with a machine-readable audit trail.
5. Not exfiltrate source code to a third party.

Rousseau's positioning maps onto every one of those requirements. You run it as a Kubernetes `Deployment` in the platform team's EKS cluster, driving a Slack Socket Mode transport into the engineering channel.

The engineering rollout is unremarkable — a `Deployment`, a `Secret`, a `ConfigMap`, a `PersistentVolumeClaim`. The story is what happens when the auditor arrives.

## The audit

An external auditor asks four questions.

**Q1: Where does model traffic go?**

You point them at `internal/llm/bedrock/`. The provider uses the standard AWS credential chain (via IRSA on EKS), so credentials are short-lived STS tokens. The traffic never leaves your AWS account.

**Q2: How do you verify the binary you're running?**

You show them `docker/Dockerfile` — a multi-stage build with a pinned `golang:1.26-alpine` base — and the `release-verify.sh` script the SRE team runs during image promotion:

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_${VERSION}_checksums.txt.sig \
  rousseau_${VERSION}_checksums.txt

sha256sum -c rousseau_${VERSION}_checksums.txt
```

You add: SLSA-3 provenance is attested through GitHub Actions OIDC. The Sigstore transparency log is a public trust anchor.

**Q3: How do you prevent the model from mutating production?**

You point them at the `agent.approver` config:

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

Deny wins over allow. Unmatched → deny. Every decision is logged as a structured slog event (`tool.execute`, `tool.denied`) and forwarded to the bank's Datadog tenant via a Vector daemonset.

**Q4: Where is the source code that a session references stored?**

You explain: session state lives on a PVC backed by EBS with encryption at rest. Model context stays within the compressed session (see [Compression + Recall](/user-guide/compression-recall/)). The FTS5 recall index runs on the same PVC. Nothing goes to `agentskills.io` or any external URL — [Skills](/skills/) are loaded from a bind-mounted directory, not a hosted registry.

The auditor asks a follow-up: "What about the model itself?" You explain that Bedrock is the model boundary; anything Bedrock does with prompts is governed by the bank's existing contract with AWS.

## What that requires

### The manifest

See [Guides: Kubernetes deployment](/guides/kubernetes-deployment/) for the full manifest. Key deviations for this use case:

- **Namespace `pod-security.kubernetes.io/enforce: restricted`.**
- **IRSA** for Bedrock credentials — no long-lived AWS keys in secrets.
- **NetworkPolicy** allowing egress to Bedrock regional endpoints and Slack WSS only.
- **Vector daemonset** shipping slog output to Datadog with the `msg` field parsed as a facet.

### The config

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

### The audit story

Every tool call is one slog line. Every denial is another. Datadog's monitor on `msg:tool.denied` alerts the SOC. Weekly, the platform team pulls a report:

```
# LogQL / Datadog / whichever
sum by (name) (
  count_over_time({job="rousseau-agent"} |= "tool.denied" [1w])
)
```

The report goes to the compliance drive. Because the slog schema is stable ([Observability](/guides/observability/)), the parsing does not break across rousseau upgrades.

## What the auditor might not ask but should

- **Reproducible builds.** Rousseau's CI includes a `reproducible-build` job that verifies bit-identical output on fresh checkouts. You can independently rebuild from a tagged source and compare SHA-256.
- **Dependency pinning.** `go.mod` pins exact versions; `go.sum` is frozen. Dependabot opens updates as reviewable PRs, not silent bumps.
- **`govulncheck` on every commit.** Any known vulnerability that reaches an imported symbol fails CI.
- **CodeQL** static analysis on every commit.

All of the above is in [Security](/security/) — the compliance file drawer already exists.

## The out-of-tenant boundary

Bedrock is the boundary. Traffic to `bedrock-runtime.eu-west-1.amazonaws.com` leaves the pod but stays inside AWS. The bank's data-flow diagram shows one arrow from the pod to Bedrock; no other outbound arrows exist for this deployment (Slack Socket Mode is outbound WSS to `wss-primary.slack.com`, which is documented as a separate allowed egress).

## Related pages

- [Guides: Kubernetes deployment](/guides/kubernetes-deployment/) — the manifests.
- [Guides: Audit + Approval Policies](/guides/audit-approval-policies/) — the compliance story.
- [Guides: Observability](/guides/observability/) — the slog pipeline.
- [Bedrock provider](/providers/bedrock/) — credential chain and region behaviour.
- [Security](/security/) — trust model and supply-chain controls.
