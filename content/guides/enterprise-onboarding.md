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
description: "A checklist for platform teams adopting rousseau-agent: SBOM, cosign, seccomp, network egress, approval policy, at-rest encryption, security SLOs."
keywords: "enterprise, checklist, sbom, cosign, seccomp, egress, encryption, slo"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/guides/enterprise-onboarding/"
subtitle: "The platform-team checklist before rousseau ships beyond a proof-of-concept."
tags: "guides, enterprise, security, checklist, sbom, cosign"
title: "Guide: Enterprise onboarding"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "enterprise, checklist, sbom, cosign, seccomp, egress, encryption, slo"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: Enterprise onboarding"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/enterprise-onboarding/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/enterprise-onboarding/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide: Enterprise onboarding"
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
twitter_title: "Guide: Enterprise onboarding"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Who this is for

A platform team assessing rousseau-agent before it goes near production. Answers the "what do we need to sign off on?" question. Every item cross-references a specific concrete thing rousseau ships so the sign-off is objective, not aesthetic.

## Checklist

### 1. Supply chain

- [ ] **SBOM.** Confirm every release publishes `rousseau_<v>_sbom.cdx.json` (CycloneDX 1.5). Import into your SCA scanner. Actionable: run `cyclonedx-cli tree` against the SBOM and grep for licence exceptions your org bans.
- [ ] **SLSA-3 provenance.** Every release publishes `rousseau_<v>_provenance.intoto.jsonl`. Verify with `slsa-verifier verify-artifact --source-uri github.com/sebastienrousseau/rousseau-agent …`.
- [ ] **cosign trust root.** Pin the certificate identity regex: `sebastienrousseau/rousseau-agent`. Cache the checksum verification recipe in your bootstrap tooling; see [Quickstart](/quickstart/) step 5.
- [ ] **Reproducible build.** `make check` runs `go test -race` plus `govulncheck`. Set up a periodic vulnerability scan of the version you're running.

### 2. Runtime hardening

- [ ] **Rootless container.** `docker/rousseau-agent.container` runs the Quadlet unit under a dedicated unprivileged user with `loginctl enable-linger`. Confirm your host is set up the same way.
- [ ] **All caps dropped.** `DropCapability=all`. `podman inspect | jq '.[0].EffectiveCaps'` should show `[]`.
- [ ] **`NoNewPrivileges=true`.** Prevents child processes from gaining privileges.
- [ ] **Read-only root filesystem.** `ReadOnly=true` + `Tmpfs=/tmp:rw,size=64m`.
- [ ] **Seccomp profile.** `SeccompProfile=/usr/share/containers/seccomp.json`. Audit it against your host's baseline.
- [ ] **User namespace mapping.** `UserNS=keep-id`. Confirms bind-mounted files own correctly on both sides.

### 3. Network posture

- [ ] **No inbound.** Rousseau has zero HTTP surface. `ss -tanp | grep rousseau` shows outbound-only sockets.
- [ ] **Egress allowlist.** Layer nftables or Cloudflare Zero-Trust outside the container. Allow only:
  - The LLM provider (`api.anthropic.com`, `bedrock-runtime.<region>.amazonaws.com`, `us-east1-aiplatform.googleapis.com`, etc.).
  - The transport (`web.whatsapp.com`, `mtproto.telegram.org`, matrix homeserver, Slack `wss-*`).
- [ ] **DNS resolver locked down.** Optionally run a `unbound` in an adjacent container that only resolves the allowlisted names.

### 4. Approval policy

- [ ] **`mode: pattern` for every unattended daemon.** Verify `agent.approver.mode: pattern` in the config for every transport service.
- [ ] **`default: deny`.** No unmatched call gets through.
- [ ] **`bash` deny list.** `rm\s+-rf`, `sudo`, `curl`, `wget`, `chmod`, `chown`, `nc`, `ncat`. See [Tutorial: Harden the approver](/tutorials/harden-approver-policy/).
- [ ] **`write` / `edit` path pin.** Regex restricts writes to `/workspace/...`.
- [ ] **Config in source control.** The approver YAML is code — review it in PR.

### 5. Secret handling

- [ ] **No API keys in `config.yaml`.** Store secrets in a `systemd` `EnvironmentFile=` (`chmod 0600`) or the org's secret manager.
- [ ] **`ANTHROPIC_API_KEY` piped via env.** `config.Load` (`internal/config/config.go`) picks it up.
- [ ] **Bedrock IRSA / Vertex ADC.** Prefer identity federation over long-lived API keys.
- [ ] **Rotation cadence.** 90 days or as your policy demands. Rousseau does not cache credentials — a rotated key is picked up on the next daemon restart.

### 6. Data at rest

- [ ] **`sessions.db` encryption.** Full-disk encryption (LUKS on Linux, FileVault on macOS, EBS-encrypted volumes on AWS). Rousseau does not implement application-level encryption on the session store.
- [ ] **Backups encrypted.** Restic or borg both encrypt at rest with a key you control.
- [ ] **Retention policy.** Bulk-delete sessions older than `N` days — see [Guides: Session management](/guides/session-management/) for the SQL.
- [ ] **JID map handling.** `jid_sessions` table maps phone numbers to session IDs. Treat it as PII.

### 7. Logs and audit

- [ ] **`log.format: json`.** Machine-parsable output.
- [ ] **Log shipping off-host.** Vector / Promtail / Datadog. See [Guides: Observability](/guides/observability/).
- [ ] **Retention.** 90 days minimum in cold storage. Rousseau's audit trail is entirely in slog; you make it durable.
- [ ] **`tool.denied` alerting.** Alert on any denial — it may be benign or an attempted injection.
- [ ] **`whatsapp.logged_out` alerting.** Meta policy trip means the account is out of action.

### 8. Change management

- [ ] **Config changes are code.** PR-reviewed, versioned in git.
- [ ] **Image bumps are deliberate.** `AutoUpdate=disabled` in the Quadlet unit is intentional.
- [ ] **Rollback plan.** Keep the previous image tagged and available. `podman tag localhost/rousseau-agent:local rousseau-agent:previous` before every build.

### 9. Incident response

- [ ] **On-call rota.** Someone can `systemctl --user stop rousseau-agent` within your MTTR SLO.
- [ ] **Compromise playbook.** Steps to: revoke the LLM API key, revoke the transport token (e.g. Slack bot re-install), snapshot the session store, image the container filesystem, unlink WhatsApp device.
- [ ] **Security disclosure channel.** Read `SECURITY.md` in the rousseau-agent repo for the coordinated disclosure address.
- [ ] **SLO for security fixes.** Track CVEs against the pinned rousseau version. `govulncheck` in `make check` catches known Go stdlib and dependency issues.

### 10. Compliance mapping

- [ ] **SOC 2 evidence.** SLSA-3 provenance + cosign + SBOM covers CC7.1 (system operations). Approver logs cover CC7.2.
- [ ] **ISO 27001 A.12 Operations Security.** Approval policies + workspace scoping + audit logs.
- [ ] **OWASP LLM Top-10.** Rousseau does not attest to LLM Top-10 today — this is a roadmap item. Document your compensating controls (approver + container) in your audit.

## Sign-off template

The below is a lightweight template your platform team can copy into a runbook:

```
Rousseau-agent deployment sign-off
=================================
Version: <tag>            (verified via cosign / SLSA verifier)
Provider: <anthropic|bedrock|vertex|openai>
Transports enabled: <list>
Approver mode: pattern
Approver default: deny
Log destination: <Loki / Datadog / etc>
Backup destination: <s3://... / restic repo>
On-call: <team>
Security disclosure: <internal address>
```

## Related

- [Security](/security/) — the trust boundaries this checklist protects.
- [Deployment](/deployment/) — the Quadlet unit.
- [Tutorial: Deploy to a VPS](/tutorials/deploy-to-a-vps/) — worked example.
- [Guides: Production Deployment](/guides/production-deployment/) — operational specifics.
