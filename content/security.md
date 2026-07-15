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
changefreq: "weekly"
description: "rousseau-agent security posture: SLSA-3 provenance, cosign signatures, CycloneDX SBOM, dropped capabilities, seccomp, trust model, cryptography inventory, disclosure SLA."
keywords: "security, SLSA-3, cosign, sigstore, SBOM, CycloneDX, seccomp, drop capabilities, trust model, disclosure, CVSS, coordinated disclosure"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/security/"
subtitle: "Supply chain, runtime, and trust boundaries — honestly stated."
tags: "security, supply-chain, disclosure"
title: "Security"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "security, SLSA-3, cosign, sigstore, SBOM, CycloneDX, seccomp, drop capabilities, trust model, disclosure, CVSS, coordinated disclosure"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Security"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "security"
order: 26
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/security/index.html"
item_link: "https://docs.rousseau-agent.dev/security/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Security"
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
twitter_title: "Security"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>rousseau's threat model in prose and ASCII diagram form, the load-bearing boundaries (approval policy, container isolation, supply chain), the reference seccomp filter and how to tighten it further, the network egress policy, and the audit trail that lands in <code>slog</code>. Cross-reference <code>SECURITY.md</code> in the source tree and <code>docker/rousseau-agent.container</code> for the ground truth.</p></aside>

## Threat model diagram

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

Everything inside the container box is under rousseau's control. The chat-transport ingress arrives already E2EE-encrypted (WhatsApp) or TLS-encrypted (Slack, Discord, Matrix, Telegram, Email, SMS). The LLM-provider egress is TLS. Bind mounts are the daemon's only access to the host filesystem.

## Trust model — what is in scope

`rousseau-agent` is a **local, container-native daemon**. Three load-bearing boundaries:

### 1. The user's shell

The `bash` built-in tool executes arbitrary commands with the user's privileges. **This is the primary security boundary.** Every tool call is surfaced before execution and is subject to the configured approval policy (`allow_all`, `deny_all`, or `pattern` mode with per-tool regex allow / deny rules and a configurable default).

Operators running unattended (chat-transport) daemons **must** either:

- enforce `pattern` mode with `default: deny` and explicit allow rules, or
- accept `bypassPermissions` posture with an explicit understanding of the exposure.

There is no middle ground where the model itself gates itself. If the daemon can shell out and the daemon is reachable from a chat transport, the reachable users can, in principle, drive the shell.

### 2. Container isolation

The reference deployment is a rootless Podman container with:

- `ReadOnly=true`
- `DropCapability=all`
- `NoNewPrivileges=true`
- Default seccomp filter (`/usr/share/containers/seccomp.json`)
- Non-root UID 1000
- `keep-id` user-namespace mapping
- `Network=pasta` (rootless, no inbound-from-host by default)

Only the workspace bind mount, the state directory, and `~/.claude` are visible from inside the container. See [/deployment/](/deployment/).

### 3. Supply chain

Every commit runs `govulncheck` and CodeQL. Every release ships:

- **SLSA Level 3 provenance** via `slsa-framework/slsa-github-generator`, signed through GitHub Actions OIDC.
- **cosign signature** on the checksum file, verifiable against the Sigstore transparency log.
- **CycloneDX JSON SBOM.**
- **Reproducible-build attestation** — a dedicated CI job verifies bit-identical output from a fresh checkout.

## Trust model — what is out of scope

- **Malicious model output.** The operator is responsible for reviewing tool calls before approving them. Approval policies make this less error-prone; they do not eliminate the need for human judgment.
- **Compromised Go toolchain, container runtime, or host OS.** A trustworthy build environment is assumed.
- **Physical access to the machine.**
- **Attacks against the LLM provider itself.** Provider vulnerabilities are that provider's responsibility.

## Supply-chain controls

| Control | Implementation |
|---|---|
| Direct dependency pinning | Exact versions in `go.mod`; transitive resolution frozen in `go.sum`. |
| Vulnerability scanning | `govulncheck ./...` on every CI build. Builds fail on any known vulnerability that reaches an imported symbol. |
| Static analysis | `golangci-lint` v2 (18 linters) + GitHub CodeQL (Go). |
| Dependency updates | Dependabot for `gomod` and `github-actions`, weekly cadence. |
| Build provenance | SLSA Level 3 via `slsa-framework/slsa-github-generator`; attested through GitHub Actions OIDC and published to the Sigstore transparency log. |
| Release signing | Release checksums are signed with cosign (keyless, via GitHub Actions OIDC). |
| Software bill of materials | CycloneDX JSON SBOM attached to every release artifact. |
| Reproducible builds | Dedicated `reproducible-build` CI job verifies bit-identical output. |

CI workflow files live under `.github/workflows/` in the source tree: `ci.yml`, `codeql.yml`, `slsa.yml`, `release.yml`, `reproducible-build.yml`.

## Verifying a release

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_<version>_checksums.txt.sig \
  rousseau_<version>_checksums.txt

sha256sum -c rousseau_<version>_checksums.txt
```

The two flags that pin identity:

- `--certificate-identity-regexp` matches the GitHub repository issuing the signing certificate. Never widen this to `.*`; it is what stops another repository's cosign signature from validating against your checksum file.
- `--certificate-oidc-issuer` pins the OIDC issuer to GitHub Actions.

The Sigstore transparency log entry can be queried separately at https://search.sigstore.dev/.

## Runtime controls

Every setting below is set on the reference Quadlet unit and belongs in any container operator's baseline:

- **Non-root user (UID 1000)** — no privilege to escalate to root inside the container.
- **`ReadOnly=true`** — the image is not writable at runtime; the binary cannot mutate itself or its dependencies.
- **`Tmpfs=/tmp:rw,size=64m,mode=1777`** — the only writable location outside bind mounts.
- **`DropCapability=all`** — no `CAP_*` bits set. Outbound TCP does not require any.
- **`NoNewPrivileges=true`** — blocks setuid escalation.
- **Default seccomp filter** — kernel-level syscall gating.
- **`Network=pasta`** — rootless network stack; no inbound from the host by default.
- **No published ports** — no `PublishPort=` in the Quadlet. There is no inbound HTTP surface to publish.

## Cryptography inventory

| Use | Implementation |
|---|---|
| TLS to LLM / transport endpoints | Go standard library `crypto/tls` with the system trust store. |
| WhatsApp | `whatsmeow` (Signal protocol). |
| Matrix | Client-server API over HTTPS. |
| SMTP (email transport) | Go standard library `net/smtp` with `PlainAuth` over TLS. |
| Session store at rest | **Not encrypted at the application layer.** Operators requiring encryption at rest should mount the state directory on an encrypted filesystem (LUKS, FileVault). |

No custom cryptographic primitives are implemented in this project.

## Disclosure

Report privately to **sebastian.rousseau@gmail.com**. Do **not** open a public issue for security-affecting reports.

Include:

- Concise description and CVSS 3.1 vector.
- Affected component (file path + line range, or dependency module path).
- Environment details (`rousseau version`, Go version, OS, container runtime).
- Minimal reproduction — ideally a failing test.

### Response commitments

| Event | SLA |
|---|---|
| Acknowledgment of report | ≤ 72 hours |
| Triage decision (accept / decline / need-info) | ≤ 7 days |
| Fix landed for **Critical** (CVSS ≥ 9.0) | ≤ 14 days |
| Fix landed for **High** (7.0–8.9) | ≤ 30 days |
| Fix landed for **Medium / Low** | scheduled in a routine release |
| Public disclosure (coordinated) | after fix release |

## Supported versions

Only the `main` branch and the most recent tagged release receive security fixes. There are no long-term support branches.

## Seccomp filter breakdown

The reference Quadlet unit uses Podman's default seccomp profile at `/usr/share/containers/seccomp.json`. It blocks about 70 syscalls that no correct rousseau invocation needs, including:

| Syscall family | Blocked | Rationale |
|---|---|---|
| Kernel keyring (`add_key`, `keyctl`, `request_key`) | yes | rousseau does not touch the kernel keyring. |
| Mount management (`mount`, `umount`, `pivot_root`, `chroot`) | yes | No dynamic mount changes at runtime. |
| Kernel modules (`init_module`, `finit_module`, `delete_module`) | yes | The daemon cannot load kernel modules. |
| Namespace fun (`setns`, `unshare` with certain flags) | filtered | Prevents container-escape via namespace swap. |
| Debug primitives (`ptrace`, `process_vm_readv`, `process_vm_writev`) | yes | Rousseau does not attach to other processes. |
| BPF (`bpf`) | yes | No eBPF programs from inside the container. |
| Reboot (`reboot`, `kexec_*`) | yes | Container has no legitimate reason to reboot the host. |
| Clock changes (`clock_settime`, `adjtimex`) | yes | Time is host-managed. |

The default profile allows enough syscalls for the standard library, the SQLite driver (`modernc.org/sqlite`), the whatsmeow client, and the OpenAI/Anthropic SDKs. If you need to tighten further — e.g. drop `personality` because you never emulate other ABIs — copy the default profile, remove the syscall, and reference the copy via `SeccompProfile=/path/to/profile.json` in the Quadlet.

<aside class="admonition" data-type="caution"><span class="admonition-title">Tighter profile testing</span><p>Every seccomp adjustment needs coverage in your smoke test — a syscall you didn't know rousseau needed will cause a completion or transport to fail at runtime. Test with an actual chat round-trip before rolling into production.</p></aside>

## Network egress policy

By default the container has no ingress and unrestricted egress (`Network=pasta`). For high-security deployments, add an nftables ruleset that only permits the domains rousseau needs:

```
# /etc/nftables.d/rousseau.nft — example only, adjust to your provider
table inet rousseau_out {
    chain output {
        type filter hook output priority 0; policy drop;

        # LLM providers
        ip daddr { 3.5.0.0/16, 15.230.0.0/16 } tcp dport 443 accept  # Anthropic + Bedrock
        ip daddr { 34.107.0.0/16 } tcp dport 443 accept              # Vertex

        # Chat transports
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

CIDR ranges shift — treat the above as scaffolding. The point is that rousseau's egress is finite and enumerable; the sample `docker/example-nftables.rules` in the source is a starting-point ruleset.

## Audit trail via slog

Every security-relevant event is logged via Go's `log/slog` at structured JSON level (`log.format: json`). The events you should be tailing in production:

| Event | Level | Source | What it tells you |
|---|---|---|---|
| `tool.execute` | info | `internal/agent/agent.go` | Which tool the model asked to run, in which session. |
| `tool.denied` | warn | `internal/agent/agent.go` | An approver denied a call; contains the reason string. |
| `tool.error` | warn | `internal/agent/agent.go` | The tool ran but returned an error. |
| `router.transport.rejected` | info | `internal/transport/router.go` | An inbound message failed the allowlist. |
| `whatsapp.logged_out` | error | `internal/transport/whatsapp/client.go` | Meta invalidated the pairing. |
| `mcp.tool_error` | warn | `internal/mcp/server.go` | An MCP tool handler returned an error. |
| `cron.delivery_failed` | warn | `internal/cron/` | A scheduled job's transport delivery errored. |

Feed the JSON stream into Loki / Datadog / Splunk / a Vector pipeline; see [Guides: Observability](/guides/observability/).

<aside class="admonition" data-type="tip"><span class="admonition-title">Field naming</span><p>Slog attribute keys are namespaced by dot (<code>whatsapp.connected</code>, not <code>event=whatsapp_connected</code>). Query with the raw key in whichever log tool you use.</p></aside>

## Troubleshooting

### Container refuses to start with `mount: permission denied`

SELinux label mismatch. Ensure every bind-mount line ends with `:Z` (private label) or `:z` (shared). Without a label, the container process cannot read/write files that were labelled by the host.

### Seccomp is killing a syscall I need

Podman prints `syscall X blocked` to the journal. Reproduce with `strace -f -e trace=X` outside the container to confirm what needs the call. If it is legitimate, copy the default seccomp profile, add the syscall to the allow-list, and reference the profile via `SeccompProfile=`.

### `cosign verify-blob` shows "certificate identity does not match"

Your `--certificate-identity-regexp` is wrong. Use `sebastienrousseau/rousseau-agent`. Any looser regex (`.*`, `.+`) defeats the point of keyless signing.

### Provider egress fails under nftables restrictions

Your ruleset does not include the provider's current IP range. Providers rotate CIDRs. Use DNS-based egress with an ipset that resolves on a cron, or use an egress proxy that resolves names at connect time.

### Nothing in slog when I expect audit events

Log level too high. Set `log.level: info` (or `debug` for wire-level detail) and confirm the daemon actually starts a new session — `slog.Default()` is used before config loads, so early boot messages route to stderr in text form regardless.

## Related pages

- [Deployment](/deployment/) — the reference Quadlet unit.
- [User Guide: Approval Policies](/user-guide/approval-policies/) — the primary safety lever.
- [Guides: Prompt Injection](/guides/prompt-injection/) — attacks that come through model output.
- [Guides: Read-only mode](/guides/read-only-mode/) — how to run a "look, don't touch" daemon.
- [Guides: Observability](/guides/observability/) — slog + Loki / Datadog pipeline.

## Further reading

- `SECURITY.md` — the canonical policy document.
- `docker/rousseau-agent.container` — the reference Quadlet unit.
- `docker/example-nftables.rules` — sample egress ruleset.
- `internal/agent/agent.go` — where the `tool.execute` and `tool.denied` events are emitted.
- `internal/agent/approver.go` — approval-policy implementations.
