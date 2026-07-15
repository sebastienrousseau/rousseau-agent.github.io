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
description: "A checklist for platform teams adopting rousseau-agent: SBOM, cosign, seccomp, network egress, approval policy, at-rest encryption, security SLOs."
keywords: "enterprise, checklist, sbom, cosign, seccomp, egress, encryption, slo"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/guides/enterprise-onboarding/"
subtitle: "The platform-team checklist before rousseau ships beyond a proof-of-concept."
tags: "guides, enterprise, security, checklist, sbom, cosign"
title: "Leitfaden: Enterprise-Onboarding"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "enterprise, checklist, sbom, cosign, seccomp, egress, encryption, slo"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: Enterprise-Onboarding"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/enterprise-onboarding/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/enterprise-onboarding/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: Enterprise-Onboarding"
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
twitter_title: "Leitfaden: Enterprise-Onboarding"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Danke an jeden Operator, der seinen eigenen Coding-Agenten betreibt."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Für wen das ist

Ein Plattformteam, das rousseau-agent bewertet, bevor es in die Nähe der Produktion kommt. Beantwortet die „Was müssen wir abzeichnen?"-Frage. Jeder Punkt referenziert eine spezifische, konkrete Sache, die rousseau ausliefert, sodass die Abzeichnung objektiv, nicht ästhetisch ist.

## Checkliste

### 1. Lieferkette

- [ ] **SBOM.** Bestätigen Sie, dass jedes Release `rousseau_<v>_sbom.cdx.json` (CycloneDX 1.5) veröffentlicht. In Ihren SCA-Scanner importieren. Umsetzbar: `cyclonedx-cli tree` gegen das SBOM ausführen und nach Lizenz-Ausnahmen greppen, die Ihre Organisation verbietet.
- [ ] **SLSA-3-Provenienz.** Jedes Release veröffentlicht `rousseau_<v>_provenance.intoto.jsonl`. Verifizieren mit `slsa-verifier verify-artifact --source-uri github.com/sebastienrousseau/rousseau-agent …`.
- [ ] **cosign-Vertrauens-Root.** Pinnen Sie den Certificate-Identity-Regex: `sebastienrousseau/rousseau-agent`. Cachen Sie das Checksum-Verifikations-Rezept in Ihrem Bootstrap-Tooling; siehe [Schnellstart](/de/quickstart/) Schritt 5.
- [ ] **Reproduzierbarer Build.** `make check` führt `go test -race` plus `govulncheck` aus. Richten Sie einen periodischen Vulnerability-Scan der Version ein, die Sie betreiben.

### 2. Laufzeit-Härtung

- [ ] **Rootless Container.** `docker/rousseau-agent.container` führt die Quadlet-Unit unter einem dedizierten unprivilegierten Nutzer mit `loginctl enable-linger` aus. Bestätigen Sie, dass Ihr Host ebenso eingerichtet ist.
- [ ] **Alle Caps entzogen.** `DropCapability=all`. `podman inspect | jq '.[0].EffectiveCaps'` sollte `[]` zeigen.
- [ ] **`NoNewPrivileges=true`.** Verhindert, dass Kindprozesse Privilegien erlangen.
- [ ] **Read-only-Root-Dateisystem.** `ReadOnly=true` + `Tmpfs=/tmp:rw,size=64m`.
- [ ] **Seccomp-Profil.** `SeccompProfile=/usr/share/containers/seccomp.json`. Auditieren Sie es gegen die Baseline Ihres Hosts.
- [ ] **User-Namespace-Mapping.** `UserNS=keep-id`. Bestätigt, dass bind-gemountete Dateien auf beiden Seiten korrekt gehören.

### 3. Netzwerk-Haltung

- [ ] **Kein Inbound.** Rousseau hat null HTTP-Oberfläche. `ss -tanp | grep rousseau` zeigt nur Outbound-Sockets.
- [ ] **Egress-Allowlist.** Legen Sie nftables oder Cloudflare Zero-Trust außerhalb des Containers. Erlauben Sie nur:
  - Den LLM-Provider (`api.anthropic.com`, `bedrock-runtime.<region>.amazonaws.com`, `us-east1-aiplatform.googleapis.com`, etc.).
  - Den Transport (`web.whatsapp.com`, `mtproto.telegram.org`, Matrix-Homeserver, Slack `wss-*`).
- [ ] **DNS-Resolver eingesperrt.** Betreiben Sie optional einen `unbound` in einem benachbarten Container, der nur die allowlisteten Namen auflöst.

### 4. Freigaberichtlinie

- [ ] **`mode: pattern` für jeden unbeaufsichtigten Daemon.** Verifizieren Sie `agent.approver.mode: pattern` in der Konfiguration für jeden Transport-Dienst.
- [ ] **`default: deny`.** Kein nicht getroffener Aufruf kommt durch.
- [ ] **`bash`-Deny-Liste.** `rm\s+-rf`, `sudo`, `curl`, `wget`, `chmod`, `chown`, `nc`, `ncat`. Siehe [Tutorial: Approver härten](/de/tutorials/harden-approver-policy/).
- [ ] **`write` / `edit` Pfad-Pin.** Regex beschränkt Schreibvorgänge auf `/workspace/...`.
- [ ] **Konfiguration in der Versionskontrolle.** Die Approver-YAML ist Code — reviewen Sie sie im PR.

### 5. Handhabung von Secrets

- [ ] **Keine API-Schlüssel in `config.yaml`.** Speichern Sie Secrets in einem `systemd`-`EnvironmentFile=` (`chmod 0600`) oder im Secret-Manager der Organisation.
- [ ] **`ANTHROPIC_API_KEY` per Env geliefert.** `config.Load` (`internal/config/config.go`) nimmt ihn auf.
- [ ] **Bedrock IRSA / Vertex ADC.** Bevorzugen Sie Identity-Federation gegenüber langlebigen API-Schlüsseln.
- [ ] **Rotationskadenz.** 90 Tage oder wie Ihre Richtlinie es verlangt. Rousseau cacht keine Credentials — ein rotierter Schlüssel wird beim nächsten Daemon-Neustart aufgenommen.

### 6. Daten at Rest

- [ ] **`sessions.db`-Verschlüsselung.** Vollverschlüsselung (LUKS unter Linux, FileVault unter macOS, EBS-verschlüsselte Volumes auf AWS). Rousseau implementiert keine Verschlüsselung auf Anwendungsebene für den Session-Store.
- [ ] **Backups verschlüsselt.** Restic oder borg verschlüsseln beide at rest mit einem Schlüssel, den Sie kontrollieren.
- [ ] **Retention-Richtlinie.** Massenlöschung von Sitzungen älter als `N` Tage — siehe [Leitfäden: Sitzungsverwaltung](/de/guides/session-management/) für das SQL.
- [ ] **JID-Map-Handling.** Die `jid_sessions`-Tabelle mappt Telefonnummern auf Session-IDs. Behandeln Sie sie als PII.

### 7. Logs und Audit

- [ ] **`log.format: json`.** Maschinen-parsbare Ausgabe.
- [ ] **Log-Shipping vom Host.** Vector / Promtail / Datadog. Siehe [Leitfäden: Observability](/de/guides/observability/).
- [ ] **Retention.** Mindestens 90 Tage in Cold Storage. Der Audit-Trail von rousseau ist vollständig in slog; Sie machen ihn dauerhaft.
- [ ] **`tool.denied`-Alerting.** Alarm bei jeder Ablehnung — sie kann gutartig oder ein versuchter Injection sein.
- [ ] **`whatsapp.logged_out`-Alerting.** Ein Auslösen von Metas Richtlinie bedeutet, dass das Konto außer Betrieb ist.

### 8. Change-Management

- [ ] **Konfigurationsänderungen sind Code.** PR-reviewt, in git versioniert.
- [ ] **Image-Bumps sind bewusst.** `AutoUpdate=disabled` in der Quadlet-Unit ist beabsichtigt.
- [ ] **Rollback-Plan.** Behalten Sie das vorherige Image getaggt und verfügbar. `podman tag localhost/rousseau-agent:local rousseau-agent:previous` vor jedem Build.

### 9. Incident-Response

- [ ] **On-Call-Rota.** Jemand kann `systemctl --user stop rousseau-agent` innerhalb Ihres MTTR-SLO ausführen.
- [ ] **Kompromittierungs-Playbook.** Schritte zum: Widerrufen des LLM-API-Schlüssels, Widerrufen des Transport-Tokens (z. B. Slack-Bot-Neuinstallation), Snapshot des Session-Stores, Imaging des Container-Dateisystems, WhatsApp-Gerät entkoppeln.
- [ ] **Sicherheits-Disclosure-Kanal.** Lesen Sie `SECURITY.md` im rousseau-agent-Repo für die Coordinated-Disclosure-Adresse.
- [ ] **SLO für Sicherheitsfixes.** Verfolgen Sie CVEs gegen die gepinnte rousseau-Version. `govulncheck` in `make check` fängt bekannte Go-Stdlib- und Abhängigkeits-Probleme ab.

### 10. Compliance-Mapping

- [ ] **SOC-2-Nachweise.** SLSA-3-Provenienz + cosign + SBOM deckt CC7.1 (System Operations) ab. Approver-Logs decken CC7.2 ab.
- [ ] **ISO 27001 A.12 Operations Security.** Freigaberichtlinien + Workspace-Scoping + Audit-Logs.
- [ ] **OWASP LLM Top-10.** Rousseau attestiert die LLM Top-10 heute nicht — das ist ein Roadmap-Punkt. Dokumentieren Sie Ihre kompensierenden Kontrollen (Approver + Container) in Ihrem Audit.

## Sign-off-Vorlage

Das Untenstehende ist eine leichte Vorlage, die Ihr Plattformteam in ein Runbook kopieren kann:

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

## Verwandt

- [Sicherheit](/de/security/) — die Vertrauensgrenzen, die diese Checkliste schützt.
- [Bereitstellung](/de/deployment/) — die Quadlet-Unit.
- [Tutorial: Auf einen VPS bereitstellen](/de/tutorials/deploy-to-a-vps/) — durchgearbeitetes Beispiel.
- [Leitfäden: Produktions-Bereitstellung](/de/guides/production-deployment/) — operative Spezifika.
