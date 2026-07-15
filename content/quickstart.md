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
description: "Install rousseau-agent, configure a provider, hold your first conversation, wire a transport, and verify the release supply chain in about five minutes."
keywords: "quickstart, install, first conversation, whatsapp, cosign, SLSA, SBOM, provider"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/quickstart/"
subtitle: "rousseau in five minutes: install, configure, converse, verify."
tags: "quickstart, install, provider, transport, supply-chain"
title: "Quickstart"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "quickstart, install, first conversation, whatsapp, cosign, SLSA, SBOM, provider"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Quickstart"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 0
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/quickstart/index.html"
item_link: "https://docs.rousseau-agent.dev/quickstart/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Quickstart"
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
twitter_description: "Install rousseau-agent, configure a provider, hold your first conversation, wire a transport, and verify the release supply chain in about five minutes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Quickstart"
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

## rousseau in 5 minutes


<video controls preload="metadata" poster="/assets/rousseau-chat-poster.png" width="820" style="max-width:100%;border-radius:12px;box-shadow:0 12px 40px rgba(0,0,0,.25);margin:16px 0" aria-label="A 7-second walkthrough of a rousseau chat session">
  <source src="/assets/rousseau-chat.webm" type="video/webm">
  <track kind="captions" src="/assets/rousseau-chat.vtt" srclang="en" label="English" default>
  Your browser does not support the video tag. <a href="/assets/rousseau-chat.webm">Download the WebM (27 KB)</a>.
</video>


Rousseau is a single static Go binary that ships with a Bubble Tea TUI, a SQLite session store at `~/.local/share/rousseau/sessions.db`, and nine chat transports (WhatsApp, Signal, Telegram, Slack, Discord, Matrix, iMessage, SMS, email). No SaaS control plane, no telemetry, no license server. You bring the LLM.

This page takes you end-to-end:

- [ ] **1. Install rousseau** — from source, `go install`, or a cosign-verified release.
- [ ] **2. Configure your LLM** — pick a provider (`claudecli` by default; Anthropic, Bedrock, Vertex, or any OpenAI-compatible endpoint).
- [ ] **3. Have your first conversation** — `rousseau chat` in your terminal.
- [ ] **4. Add a transport** — pair WhatsApp with an allowlisted JID.
- [ ] **5. Verify supply chain** — cosign-verify the checksums file, then read the CycloneDX SBOM and SLSA-3 provenance.

Most operators finish in under ten minutes.

## 1. Install rousseau

<aside class="admonition" data-type="tip"><span class="admonition-title">Recommended</span><p><code>go install</code> is the fastest path if you already have Go 1.26+. For production, use a signed release with <code>cosign verify-blob</code> so the supply-chain guarantees stick.</p></aside>

<div class="tabs" data-tabs="qs-install">
  <div class="tab-list" role="tablist" aria-label="Install method">
    <button role="tab" aria-selected="true">go install</button>
    <button role="tab" aria-selected="false">From source</button>
    <button role="tab" aria-selected="false">Signed release</button>
    <button role="tab" aria-selected="false">Container</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
rousseau version
```

The binary embeds `modernc.org/sqlite` (see `internal/state/sqlite/store.go`), so there is no libc or CGo dependency at runtime. Works identically on macOS, Linux, and Windows.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` runs `go vet`, `golangci-lint`, `go test -race`, and `govulncheck` — the same gates CI enforces.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Every tagged release publishes a checksummed archive, a CycloneDX SBOM, a SLSA-3 provenance attestation, and a cosign signature over the checksum file:

```sh
curl -LO https://github.com/sebastienrousseau/rousseau-agent/releases/download/v0.6.0/rousseau_0.6.0_linux_amd64.tar.gz
curl -LO https://github.com/sebastienrousseau/rousseau-agent/releases/download/v0.6.0/rousseau_0.6.0_checksums.txt
curl -LO https://github.com/sebastienrousseau/rousseau-agent/releases/download/v0.6.0/rousseau_0.6.0_checksums.txt.sig

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_0.6.0_checksums.txt.sig \
  rousseau_0.6.0_checksums.txt

sha256sum -c rousseau_0.6.0_checksums.txt --ignore-missing
tar -xzf rousseau_0.6.0_linux_amd64.tar.gz
sudo install -m 0755 rousseau /usr/local/bin/
```

<aside class="admonition" data-type="note"><span class="admonition-title">Note</span><p>The <code>cosign</code> identity is scoped to <code>sebastienrousseau/rousseau-agent</code>'s GitHub Actions OIDC. See <a href="/security/">Security</a> for the trust root.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau ships with a Podman-friendly `Dockerfile` at `docker/Dockerfile` and a systemd Quadlet unit at `docker/rousseau-agent.container`. A published image on ghcr.io is on the roadmap; in the meantime, build locally:

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
```

See [Deployment](/deployment/) for the reference Quadlet unit with hardened runtime posture (rootless, `DropCapability=all`, `NoNewPrivileges=true`, seccomp).

  </div>
</div>

### OS-specific prerequisites

<div class="tabs" data-tabs="qs-os">
  <div class="tab-list" role="tablist" aria-label="Operating system">
    <button role="tab" aria-selected="true">macOS</button>
    <button role="tab" aria-selected="false">Linux</button>
    <button role="tab" aria-selected="false">Windows</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```sh
brew install go@1.26
# For the container path:
brew install podman
podman machine init && podman machine start
```

For the default `claudecli` provider, install Claude Code from https://claude.ai/download and run `claude login` once.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Install Go 1.26+ via your package manager or from https://go.dev/dl. For the container path, use rootless Podman ≥ 5.x with `pasta` network mode.

```sh
# Debian/Ubuntu
sudo apt install golang-1.26 podman

# Arch
sudo pacman -S go podman

# Fedora
sudo dnf install golang podman
```

Claude Code CLI (optional, for `claudecli` provider): download from https://claude.ai/download.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau runs natively on Windows via `go install`. The container reference deployment is Linux-only; on Windows use WSL 2 for the Podman path.

```powershell
winget install GoLang.Go
# Or: choco install golang
```

For `claudecli`, install Claude Code from https://claude.ai/download.

<aside class="admonition" data-type="warning"><span class="admonition-title">Windows note</span><p>Some transport packages call subprocesses (<code>signal-cli</code>) or open OS-specific paths (<code>~/.local/share/</code>). The <code>whatsapp</code>, <code>slack</code>, <code>discord</code>, <code>telegram</code>, <code>matrix</code>, <code>email</code>, <code>sms</code> transports are all cross-platform. <code>signal</code> and <code>imessage</code> require their respective host tooling.</p></aside>

  </div>
</div>

## 2. Configure your LLM

Config lives at `~/.config/rousseau/config.yaml` (override with `--config`) and every field is defined in `internal/config/config.go`. The default provider is `claudecli`, which shells out to your local `claude` CLI so no API keys leave your laptop.

### claudecli (default, zero keys)

If you already have Claude Code (`claude`) installed and authenticated, you're done. Rousseau inherits its OAuth session:

```yaml
provider: claudecli

claudecli:
  binary: claude              # optional; PATH lookup by default
  permission_mode: default    # or bypassPermissions for unattended daemons
```

See [Providers: claudecli](/providers/claudecli/).

### Anthropic API

Direct Anthropic. Uses the official `anthropic-sdk-go` in `internal/llm/anthropic/client.go`:

```sh
export ANTHROPIC_API_KEY=sk-ant-…
```

```yaml
provider: anthropic
anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096
```

`ANTHROPIC_API_KEY` is read directly from the environment (see `config.Load` in `internal/config/config.go`); the key never has to live on disk. See [Providers: Anthropic](/providers/anthropic/).

### AWS Bedrock

Uses the standard AWS credential chain (profile, IMDS, IRSA). Region and model come from `internal/config/config.go` `BedrockConfig`:

```yaml
provider: bedrock
bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
  profile: default            # optional named profile
  max_tokens: 4096
```

No API key sits in `config.yaml`. See [Providers: Bedrock](/providers/bedrock/).

### Google Vertex AI

Anthropic-on-Vertex; reads a service-account JSON file. Config fields defined in `VertexConfig`:

```yaml
provider: vertex
vertex:
  project: my-gcp-project
  region: europe-west4
  model: claude-sonnet-4-6@20250101
  credentials_file: /etc/rousseau/vertex.json
  max_tokens: 4096
```

See [Providers: Vertex](/providers/vertex/).

### OpenAI-compatible (OpenRouter, Ollama, vLLM, LM Studio)

The `openai`, `openrouter`, and `ollama` provider names share `OpenAIConfig`. Base URLs for OpenRouter and Ollama have defaults in `setDefaults` (`https://openrouter.ai/api/v1` and `http://localhost:11434/v1`); anything else lands in the `openai` block with an explicit `base_url`:

```yaml
provider: ollama              # or: openai, openrouter
ollama:
  model: llama3.1:70b-instruct
  base_url: http://localhost:11434/v1
```

See [Providers: OpenAI-compatible](/providers/openai-compatible/) and [Guides: Self-hosted vLLM](/guides/self-hosted-vllm/).

## 3. Have your first conversation

```sh
rousseau chat
```

You'll see a Bubble Tea TUI (`internal/tui/model.go`):

- A **viewport** at the top scrolls the transcript. Assistant text streams in as it arrives.
- A **textarea** at the bottom takes your input. Press `Enter` to send, `Ctrl+C` to quit.
- A **spinner** shows during LLM turns; a small streaming indicator appears while tokens arrive.
- Every turn is persisted to SQLite at `~/.local/share/rousseau/sessions.db`. WAL journaling is enabled by `Open()` in `internal/state/sqlite/store.go`, so you can safely run other rousseau commands (`rousseau session list`, `rousseau mcp`) against the same database while the TUI is open.

Ask something small first — e.g. "list the files under `internal/tools/builtin`" — and rousseau will call the `read`, `grep`, `edit`, `write`, or `bash` built-in tools (`internal/tools/builtin/*.go`) as needed. See [User Guide: TUI](/user-guide/tui/) for keybindings and [User Guide: Tools](/user-guide/tools/) for the schemas.

Screenshot placeholder: the TUI shows a two-line status bar (session id and provider), the viewport with assistant + user messages colour-tinted, and the textarea in focus at the bottom.

## 4. Add a transport (WhatsApp)

WhatsApp is the reference transport because pairing is the most stringent. Every other transport (`slack`, `discord`, `telegram`, `matrix`, `signal`, `sms`, `imessage`, `email`) follows the same shape.

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

On first launch, `rousseau` prints a QR code to stdout. Scan it in **WhatsApp > Settings > Linked devices** on your phone. The whatsmeow client (`internal/transport/whatsapp/client.go`) emits three structured log events:

- `whatsapp.qr_ready` — QR was rendered.
- `whatsapp.paired` — phone accepted the QR.
- `whatsapp.connected` — websocket to Meta is up.

Device credentials are cached to `~/.local/share/rousseau/whatsapp.db` (a separate SQLite database, so relinking a device does not touch conversation history). The `--allow` flag pins an allowlist of E.164 JIDs; every other sender is silently dropped by `router.transport.rejected`.

Rousseau uses the **unofficial** WhatsApp Web protocol. Meta occasionally bans numbers running unofficial clients — do not run this on a number you rely on. See [Transports: WhatsApp](/transports/whatsapp/) for the risk analysis.

## 5. Verify supply chain

Every tagged release ships:

| Artefact | Purpose |
|---|---|
| `rousseau_<v>_checksums.txt` | SHA-256 of every archive in the release. |
| `rousseau_<v>_checksums.txt.sig` | cosign signature (keyless, OIDC-issued from GitHub Actions). |
| `rousseau_<v>_sbom.cdx.json` | CycloneDX 1.5 SBOM of the Go module graph. |
| `rousseau_<v>_provenance.intoto.jsonl` | SLSA-3 provenance attestation. |

Verify the signature identity before trusting the checksums:

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_0.6.0_checksums.txt.sig \
  rousseau_0.6.0_checksums.txt
```

The `--certificate-identity-regexp` pins the signer identity to the rousseau-agent repository under Sebastien's namespace. **Do not weaken it.** A wildcard identity defeats the point of keyless signing.

Once the signature is verified, `sha256sum -c` proves the tarball you downloaded is the one CI built. Read the SBOM with `cyclonedx-cli tree`, verify the SLSA-3 provenance with `slsa-verifier verify-artifact`, and only then extract the archive.

See [Security](/security/) for the full trust boundaries and [Guides: Enterprise Onboarding](/guides/enterprise-onboarding/) for the platform-team checklist.

## Troubleshooting

<aside class="admonition" data-type="tip"><span class="admonition-title">Recommended first stop</span><p>Run <code>rousseau doctor</code> before opening an issue. It exercises every subsystem — provider auth, state store, transport credentials — and prints structured pass/warn/fail rows.</p></aside>

### `rousseau version` prints "dev" after `go install`

The `version`, `commit`, and `buildDate` values are stamped by the release toolchain via `-ldflags` in `internal/cli/root.go`. `go install` skips those flags, so the binary reports `dev / none / unknown`. Use the signed-release path if you need a stable version string; the `dev` string is harmless at runtime.

### `claudecli: exec: "claude": executable file not found`

`provider: claudecli` shells out to the `claude` binary. Either put Claude Code on your `$PATH` (see [Providers: claudecli](/providers/claudecli/)) or switch provider — the fastest alternative is `provider: anthropic` with `ANTHROPIC_API_KEY` exported.

### WhatsApp QR is displayed but never accepted

Three common causes: (1) the container clock is skewed by more than 30 seconds — WhatsApp's handshake is time-sensitive; (2) a partially-completed pairing left `whatsapp.db` in an unreusable state — delete `~/.local/share/rousseau/whatsapp.db` and re-scan; (3) Meta invalidated the number — try a fresh phone number. See [Transports: WhatsApp](/transports/whatsapp/).

### `cosign verify-blob` errors with "no matching signatures"

The `--certificate-identity-regexp` must match the signer's GitHub repository. For rousseau-agent, the correct value is `sebastienrousseau/rousseau-agent`. A wildcard defeats the point of keyless signing — do not weaken it. If the regex is correct, refresh Sigstore's trust root with `cosign initialize`.

### Every tool call is denied with "denied by pattern policy"

You are running in `pattern` mode with `default: deny` and no matching allow rule. Add an allow entry for the tool, or flip `default: allow` and add narrow deny rules instead. See [User Guide: Approval Policies](/user-guide/approval-policies/) for worked examples.

## Related pages

- [Getting Started: Installation](/getting-started/installation/) — every install method with the verification recipe.
- [Getting Started: First Transport](/getting-started/first-transport/) — end-to-end WhatsApp/Slack/Discord walkthrough.
- [Configuration](/configuration/) — every knob in `~/.config/rousseau/config.yaml`.
- [Concepts](/concepts/) — the agent loop, session store, MCP, cron, skills.
- [Troubleshooting](/troubleshooting/) — the full failure-mode catalogue.

## Further reading

- `README.md` — repository-level positioning and capability matrix.
- `SECURITY.md` — trust boundaries and supply-chain hardening.
- `internal/config/config.go` — the authoritative config struct.
- `internal/cli/root.go` — Cobra command tree wiring.

## Next steps

| Where to go | Why |
|---|---|
| [Configuration](/configuration/) | Every knob in `~/.config/rousseau/config.yaml` with defaults. |
| [Concepts](/concepts/) | The agent loop, session store, MCP, cron, skills. |
| [Deployment](/deployment/) | Rootless Podman + systemd Quadlet unit. |
| [Security](/security/) | Trust boundaries, SLSA-3 provenance, seccomp posture. |
| [Tutorials](/tutorials/) | Full end-to-end walkthroughs. |
| [Reference](/reference/cli-commands/) | Every CLI flag, exit code, and config field. |
