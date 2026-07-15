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
changefreq: "weekly"
description: "rousseau-agent security posture: SLSA-3 provenance, cosign signatures, CycloneDX SBOM, dropped capabilities, seccomp, trust model, cryptography inventory, disclosure SLA."
keywords: "security, SLSA-3, cosign, sigstore, SBOM, CycloneDX, seccomp, drop capabilities, trust model, disclosure, CVSS, coordinated disclosure"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/security/"
subtitle: "Supply chain, runtime, and trust boundaries — honestly stated."
tags: "security, supply-chain, disclosure"
title: "Sicherheit"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "security, SLSA-3, cosign, sigstore, SBOM, CycloneDX, seccomp, drop capabilities, trust model, disclosure, CVSS, coordinated disclosure"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Sicherheit"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "security"
order: 26
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/security/index.html"
item_link: "https://docs.rousseau-agent.dev/security/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Sicherheit"
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
twitter_description: "rousseau-agent security posture: SLSA-3 provenance, cosign signatures, CycloneDX SBOM, dropped capabilities, seccomp, trust model, cryptography inventory, disclosure SLA."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Sicherheit"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Das Bedrohungsmodell von rousseau in Prosa- und ASCII-Diagrammform, die tragenden Grenzen (Approval-Richtlinie, Container-Isolation, Lieferkette), den Referenz-seccomp-Filter und dessen weitere Verschärfung, die Netzwerk-Egress-Richtlinie sowie den Audit-Trail in <code>slog</code>. Als Referenz vergleichen Sie <code>SECURITY.md</code> im Source-Tree und <code>docker/rousseau-agent.container</code> für die massgebliche Wahrheit.</p></aside>

## Bedrohungsmodell-Diagramm

```
                          ┌──────────────────────────────────┐
                          │        Chat transport user       │
                          │   (WhatsApp / Slack / Discord)   │
                          └──────────────────┬───────────────┘
                                             │ E2EE (WhatsApp)
                                             │ TLS   (Slack / Discord / …)
                        ─────────────────────┴─────────────────────
                                             │
                                             ▼
      ┌─────────────── rousseau-agent container ────────────────┐
      │                                                          │
      │   ┌─────────────┐    inbound     ┌──────────────────┐   │
      │   │  Transport  │ ───────────▶   │  Router          │   │
      │   │  adapter    │                │  + allowlist     │   │
      │   └─────────────┘                └────────┬─────────┘   │
      │                                           │             │
      │                                           ▼             │
      │                                   ┌─────────────┐       │
      │                                   │   Agent     │       │
      │                                   │  Turn loop  │       │
      │                                   └──────┬──────┘       │
      │                                          │              │
      │                            approver     │              │
      │                          ◀───────────────┤              │
      │                                          ▼              │
      │                                   ┌─────────────┐       │
      │                                   │  Registry   │       │
      │                                   │ read/edit/  │       │
      │                                   │ bash/…      │       │
      │                                   └──────┬──────┘       │
      │                                          │              │
      │  ROOTFS  ReadOnly=true  ─────────────────┤              │
      │  CAPS    DropCapability=all              │              │
      │  UID     1000, keep-id                   │              │
      │  SECCOMP default filter                  │              │
      │                                          │              │
      │            outbound TLS                  ▼              │
      └──────────────────┬───────────────────────┬──────────────┘
                         │                       │
                         ▼                       ▼
                ┌────────────────┐    ┌─────────────────────┐
                │  LLM provider  │    │  bind mounts        │
                │  (Anthropic /  │    │  ~/.local/share/    │
                │   Bedrock /    │    │    rousseau/  RW    │
                │   Vertex / …)  │    │  workspace/   RW    │
                └────────────────┘    │  ~/.claude/   RW    │
                                      └─────────────────────┘
```

Alles innerhalb der Container-Box steht unter Kontrolle von rousseau. Der Chat-Transport-Ingress trifft bereits E2EE-verschlüsselt (WhatsApp) oder TLS-verschlüsselt (Slack, Discord, Matrix, Telegram, Email, SMS) ein. Der LLM-Provider-Egress läuft über TLS. Bind-Mounts sind der einzige Zugriff des Daemons auf das Host-Dateisystem.

## Vertrauensmodell – was im Scope ist

`rousseau-agent` ist ein **lokaler, container-nativer Daemon**. Drei tragende Grenzen:

### 1. Die Shell des Benutzers

Das eingebaute Tool `bash` führt beliebige Befehle mit den Rechten des Benutzers aus. **Dies ist die primäre Sicherheitsgrenze.** Jeder Tool-Aufruf wird vor der Ausführung angezeigt und unterliegt der konfigurierten Approval-Richtlinie (`allow_all`, `deny_all` oder `pattern`-Modus mit Regex-Allow/Deny-Regeln pro Tool und einem konfigurierbaren Default).

Betreiber, die unbeaufsichtigte (Chat-Transport-)Daemons betreiben, **müssen** entweder:

- den `pattern`-Modus mit `default: deny` und expliziten Allow-Regeln erzwingen, oder
- die `bypassPermissions`-Posture mit explizitem Bewusstsein für die Angriffsfläche akzeptieren.

Es gibt keinen Mittelweg, bei dem sich das Modell selbst überprüft. Wenn der Daemon eine Shell öffnen kann und der Daemon von einem Chat-Transport aus erreichbar ist, können die erreichbaren Benutzer im Prinzip die Shell fernsteuern.

### 2. Container-Isolation

Die Referenz-Bereitstellung ist ein rootless Podman-Container mit:

- `ReadOnly=true`
- `DropCapability=all`
- `NoNewPrivileges=true`
- Standard-seccomp-Filter (`/usr/share/containers/seccomp.json`)
- Non-Root-UID 1000
- `keep-id`-User-Namespace-Mapping
- `Network=pasta` (rootless, standardmässig keine eingehenden Verbindungen vom Host)

Nur der Workspace-Bind-Mount, das State-Verzeichnis und `~/.claude` sind aus dem Container heraus sichtbar. Siehe [/deployment/](/de/deployment/).

### 3. Lieferkette

Jeder Commit führt `govulncheck` und CodeQL aus. Jedes Release enthält:

- **SLSA-Level-3-Provenance** über `slsa-framework/slsa-github-generator`, signiert über GitHub Actions OIDC.
- **cosign-Signatur** auf der Checksum-Datei, verifizierbar gegen das Sigstore-Transparenz-Log.
- **CycloneDX-JSON-SBOM.**
- **Reproducible-Build-Attestierung** – ein dedizierter CI-Job verifiziert bitidentische Ausgabe aus einem frischen Checkout.

## Vertrauensmodell – was ausserhalb des Scopes liegt

- **Bösartige Modell-Ausgaben.** Der Betreiber ist dafür verantwortlich, Tool-Aufrufe vor der Freigabe zu prüfen. Approval-Richtlinien reduzieren die Fehleranfälligkeit; sie ersetzen jedoch keine menschliche Beurteilung.
- **Kompromittierte Go-Toolchain, Container-Runtime oder Host-OS.** Eine vertrauenswürdige Build-Umgebung wird vorausgesetzt.
- **Physischer Zugriff auf die Maschine.**
- **Angriffe gegen den LLM-Provider selbst.** Provider-Schwachstellen liegen in der Verantwortung des jeweiligen Providers.

## Lieferketten-Kontrollen

| Kontrolle | Implementierung |
|---|---|
| Direkte Abhängigkeits-Pinning | Exakte Versionen in `go.mod`; transitive Auflösung eingefroren in `go.sum`. |
| Schwachstellen-Scanning | `govulncheck ./...` bei jedem CI-Build. Builds schlagen bei jeder bekannten Schwachstelle fehl, die ein importiertes Symbol erreicht. |
| Statische Analyse | `golangci-lint` v2 (18 Linter) plus GitHub CodeQL (Go). |
| Abhängigkeits-Updates | Dependabot für `gomod` und `github-actions`, wöchentlicher Rhythmus. |
| Build-Provenance | SLSA-Level 3 über `slsa-framework/slsa-github-generator`; attestiert über GitHub Actions OIDC und im Sigstore-Transparenz-Log veröffentlicht. |
| Release-Signierung | Release-Checksums werden mit cosign signiert (keyless, über GitHub Actions OIDC). |
| Software Bill of Materials | CycloneDX-JSON-SBOM ist jedem Release-Artefakt beigefügt. |
| Reproducible Builds | Dedizierter `reproducible-build`-CI-Job verifiziert bitidentische Ausgabe. |

CI-Workflow-Dateien liegen im Source-Tree unter `.github/workflows/`: `ci.yml`, `codeql.yml`, `slsa.yml`, `release.yml`, `reproducible-build.yml`.

## Ein Release verifizieren

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_<version>_checksums.txt.sig \
  rousseau_<version>_checksums.txt

sha256sum -c rousseau_<version>_checksums.txt
```

Die beiden Flags, die die Identität festlegen:

- `--certificate-identity-regexp` passt zum GitHub-Repository, das das Signatur-Zertifikat ausstellt. Weiten Sie dies niemals auf `.*` aus; genau dies verhindert, dass eine cosign-Signatur aus einem anderen Repository gegen Ihre Checksum-Datei validiert.
- `--certificate-oidc-issuer` bindet den OIDC-Aussteller an GitHub Actions.

Der Sigstore-Transparenz-Log-Eintrag kann separat unter https://search.sigstore.dev/ abgefragt werden.

## Runtime-Kontrollen

Jede Einstellung unten ist in der Referenz-Quadlet-Unit gesetzt und gehört zur Baseline jedes Container-Betreibers:

- **Non-Root-Benutzer (UID 1000)** – keine Rechte, um innerhalb des Containers zu Root zu eskalieren.
- **`ReadOnly=true`** – das Image ist zur Laufzeit nicht beschreibbar; das Binary kann sich selbst oder seine Abhängigkeiten nicht verändern.
- **`Tmpfs=/tmp:rw,size=64m,mode=1777`** – der einzige beschreibbare Ort ausserhalb von Bind-Mounts.
- **`DropCapability=all`** – keine `CAP_*`-Bits gesetzt. Ausgehendes TCP benötigt keine.
- **`NoNewPrivileges=true`** – blockiert setuid-Eskalation.
- **Standard-seccomp-Filter** – Kernel-Level-Syscall-Gating.
- **`Network=pasta`** – rootless Netzwerkstack; standardmässig keine eingehenden Verbindungen vom Host.
- **Keine veröffentlichten Ports** – kein `PublishPort=` im Quadlet. Es gibt keine eingehende HTTP-Oberfläche zum Veröffentlichen.

## Kryptografie-Inventar

| Verwendung | Implementierung |
|---|---|
| TLS zu LLM-/Transport-Endpunkten | Go-Standardbibliothek `crypto/tls` mit dem System-Trust-Store. |
| WhatsApp | `whatsmeow` (Signal-Protokoll). |
| Matrix | Client-Server-API über HTTPS. |
| SMTP (Email-Transport) | Go-Standardbibliothek `net/smtp` mit `PlainAuth` über TLS. |
| Sitzungs-Store im Ruhezustand | **Nicht auf Anwendungsebene verschlüsselt.** Betreiber, die Verschlüsselung im Ruhezustand benötigen, sollten das State-Verzeichnis auf einem verschlüsselten Dateisystem (LUKS, FileVault) mounten. |

Es sind keine eigenen kryptografischen Primitive in diesem Projekt implementiert.

## Offenlegung

Melden Sie privat an **sebastian.rousseau@gmail.com**. Öffnen Sie **kein** öffentliches Issue für sicherheitsrelevante Meldungen.

Enthalten:

- Prägnante Beschreibung und CVSS-3.1-Vektor.
- Betroffene Komponente (Dateipfad + Zeilenbereich oder Modulpfad der Abhängigkeit).
- Umgebungsdetails (`rousseau version`, Go-Version, Betriebssystem, Container-Runtime).
- Minimale Reproduktion – idealerweise ein fehlschlagender Test.

### Antwort-Zusagen

| Ereignis | SLA |
|---|---|
| Bestätigung der Meldung | ≤ 72 Stunden |
| Triage-Entscheidung (annehmen / ablehnen / Rückfrage) | ≤ 7 Tage |
| Fix ausgeliefert für **Kritisch** (CVSS ≥ 9.0) | ≤ 14 Tage |
| Fix ausgeliefert für **Hoch** (7.0–8.9) | ≤ 30 Tage |
| Fix ausgeliefert für **Mittel / Niedrig** | eingeplant in einem regulären Release |
| Öffentliche Offenlegung (koordiniert) | nach Fix-Release |

## Unterstützte Versionen

Nur der `main`-Branch und das aktuellste getaggte Release erhalten Sicherheits-Fixes. Es gibt keine Long-Term-Support-Branches.

## Aufschlüsselung des Seccomp-Filters

Die Referenz-Quadlet-Unit verwendet das Standard-seccomp-Profil von Podman unter `/usr/share/containers/seccomp.json`. Es blockiert etwa 70 Syscalls, die kein korrekter rousseau-Aufruf benötigt, darunter:

| Syscall-Familie | Blockiert | Begründung |
|---|---|---|
| Kernel-Keyring (`add_key`, `keyctl`, `request_key`) | ja | rousseau berührt den Kernel-Keyring nicht. |
| Mount-Verwaltung (`mount`, `umount`, `pivot_root`, `chroot`) | ja | Keine dynamischen Mount-Änderungen zur Laufzeit. |
| Kernel-Module (`init_module`, `finit_module`, `delete_module`) | ja | Der Daemon kann keine Kernel-Module laden. |
| Namespace-Manipulation (`setns`, `unshare` mit bestimmten Flags) | gefiltert | Verhindert Container-Escape via Namespace-Wechsel. |
| Debug-Primitive (`ptrace`, `process_vm_readv`, `process_vm_writev`) | ja | Rousseau attacht sich nicht an andere Prozesse. |
| BPF (`bpf`) | ja | Keine eBPF-Programme aus dem Container heraus. |
| Reboot (`reboot`, `kexec_*`) | ja | Der Container hat keinen legitimen Grund, den Host neu zu starten. |
| Uhrzeit-Änderungen (`clock_settime`, `adjtimex`) | ja | Die Zeit wird vom Host verwaltet. |

Das Standard-Profil erlaubt genügend Syscalls für die Standardbibliothek, den SQLite-Treiber (`modernc.org/sqlite`), den whatsmeow-Client sowie die OpenAI-/Anthropic-SDKs. Wenn Sie weiter verschärfen möchten – z.B. `personality` entfernen, weil Sie nie andere ABIs emulieren – kopieren Sie das Standard-Profil, entfernen den Syscall und verweisen im Quadlet mit `SeccompProfile=/path/to/profile.json` auf die Kopie.

<aside class="admonition" data-type="caution"><span class="admonition-title">Test von strengeren Profilen</span><p>Jede seccomp-Anpassung benötigt Abdeckung in Ihrem Smoke-Test – ein Syscall, den Sie nicht als von rousseau benötigt erkannt haben, führt zur Laufzeit zu einem Completion- oder Transport-Fehler. Testen Sie mit einem echten Chat-Round-Trip, bevor Sie in Produktion rollen.</p></aside>

## Netzwerk-Egress-Richtlinie

Standardmässig hat der Container keinen Ingress und uneingeschränkten Egress (`Network=pasta`). Für Hochsicherheits-Bereitstellungen fügen Sie ein nftables-Regelwerk hinzu, das nur die von rousseau benötigten Domains zulässt:

```
# /etc/nftables.d/rousseau.nft — nur Beispiel, an Ihren Provider anpassen
table inet rousseau_out {
    chain output {
        type filter hook output priority 0; policy drop;

        # LLM-Provider
        ip daddr { 3.5.0.0/16, 15.230.0.0/16 } tcp dport 443 accept  # Anthropic + Bedrock
        ip daddr { 34.107.0.0/16 } tcp dport 443 accept              # Vertex

        # Chat-Transports
        ip daddr { 157.240.0.0/16 } tcp dport 443 accept             # Meta (WhatsApp)
        ip daddr { 3.208.0.0/16 } tcp dport 443 accept               # Slack

        # DNS
        udp dport 53 accept
        tcp dport 53 accept

        # NTP
        udp dport 123 accept
    }
}
```

CIDR-Bereiche ändern sich – betrachten Sie das Obige als Gerüst. Der entscheidende Punkt: Der Egress von rousseau ist endlich und aufzählbar; die Beispiel-Datei `docker/example-nftables.rules` im Source ist ein Ausgangs-Regelwerk.

## Audit-Trail über slog

Jedes sicherheitsrelevante Ereignis wird über Gos `log/slog` in strukturiertem JSON-Format geloggt (`log.format: json`). Die Ereignisse, die Sie in Produktion beobachten sollten:

| Ereignis | Level | Quelle | Was es Ihnen sagt |
|---|---|---|---|
| `tool.execute` | info | `internal/agent/agent.go` | Welches Tool das Modell in welcher Sitzung ausführen wollte. |
| `tool.denied` | warn | `internal/agent/agent.go` | Ein Approver hat einen Aufruf abgelehnt; enthält den Ablehnungsgrund. |
| `tool.error` | warn | `internal/agent/agent.go` | Das Tool lief, gab aber einen Fehler zurück. |
| `router.transport.rejected` | info | `internal/transport/router.go` | Eine eingehende Nachricht scheiterte an der Allowlist. |
| `whatsapp.logged_out` | error | `internal/transport/whatsapp/client.go` | Meta hat das Pairing invalidiert. |
| `mcp.tool_error` | warn | `internal/mcp/server.go` | Ein MCP-Tool-Handler hat einen Fehler zurückgegeben. |
| `cron.delivery_failed` | warn | `internal/cron/` | Die Transport-Zustellung eines geplanten Jobs schlug fehl. |

Leiten Sie den JSON-Stream in Loki / Datadog / Splunk / eine Vector-Pipeline; siehe [Guides: Observability](/de/guides/observability/).

<aside class="admonition" data-type="tip"><span class="admonition-title">Feldbenennung</span><p>Slog-Attribut-Keys sind per Punkt namespaced (<code>whatsapp.connected</code>, nicht <code>event=whatsapp_connected</code>). Fragen Sie mit dem Roh-Key in dem Log-Tool ab, das Sie verwenden.</p></aside>

## Fehlerbehebung

### Container weigert sich zu starten mit `mount: permission denied`

SELinux-Label-Konflikt. Stellen Sie sicher, dass jede Bind-Mount-Zeile mit `:Z` (privates Label) oder `:z` (Shared) endet. Ohne Label kann der Container-Prozess keine vom Host gelabelten Dateien lesen/schreiben.

### Seccomp blockiert einen von mir benötigten Syscall

Podman schreibt `syscall X blocked` ins Journal. Reproduzieren Sie mit `strace -f -e trace=X` ausserhalb des Containers, um zu bestätigen, was den Aufruf benötigt. Wenn er legitim ist, kopieren Sie das Standard-seccomp-Profil, ergänzen den Syscall in der Allow-Liste und verweisen mit `SeccompProfile=` auf das Profil.

### `cosign verify-blob` zeigt "certificate identity does not match"

Ihr `--certificate-identity-regexp` ist falsch. Verwenden Sie `sebastienrousseau/rousseau-agent`. Jede laxere Regex (`.*`, `.+`) hebelt den Sinn des Keyless-Signings aus.

### Provider-Egress schlägt unter nftables-Einschränkungen fehl

Ihr Regelwerk enthält den aktuellen IP-Bereich des Providers nicht. Provider rotieren CIDRs. Nutzen Sie DNS-basierten Egress mit einem ipset, das per Cron aufgelöst wird, oder einen Egress-Proxy, der Namen zur Connect-Zeit auflöst.

### Nichts in slog, wo ich Audit-Ereignisse erwarte

Log-Level zu hoch. Setzen Sie `log.level: info` (oder `debug` für Wire-Level-Details) und bestätigen Sie, dass der Daemon tatsächlich eine neue Sitzung startet – `slog.Default()` wird vor dem Config-Laden verwendet, weshalb frühe Boot-Meldungen unabhängig davon als Text auf stderr laufen.

## Verwandte Seiten

- [Bereitstellung](/de/deployment/) – die Referenz-Quadlet-Unit.
- [Benutzerhandbuch: Approval-Richtlinien](/de/user-guide/approval-policies/) – der primäre Sicherheitshebel.
- [Guides: Prompt-Injection](/de/guides/prompt-injection/) – Angriffe, die über Modell-Ausgaben kommen.
- [Guides: Read-Only-Modus](/de/guides/read-only-mode/) – wie man einen "Nur-Lese"-Daemon betreibt.
- [Guides: Observability](/de/guides/observability/) – slog- + Loki-/Datadog-Pipeline.

## Weiterführende Lektüre

- `SECURITY.md` – das kanonische Policy-Dokument.
- `docker/rousseau-agent.container` – die Referenz-Quadlet-Unit.
- `docker/example-nftables.rules` – Beispiel-Egress-Regelwerk.
- `internal/agent/agent.go` – wo die Ereignisse `tool.execute` und `tool.denied` emittiert werden.
- `internal/agent/approver.go` – Implementierungen der Approval-Richtlinien.
