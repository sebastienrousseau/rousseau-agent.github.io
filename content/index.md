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
description: "The self-hosted, container-native coding agent. 9 chat transports, 5 LLM providers, SLSA-3 provenance, cosign-signed releases, MCP-native. Zero telemetry."
download: ""
format-detection: "telephone=no"
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
keywords: "coding agent, self-hosted, container-native, MCP server, SLSA-3, cosign, SBOM, LLM, WhatsApp, Signal, Slack, Discord, Matrix, iMessage, Email, SMS, whatsmeow, Anthropic, Bedrock, Vertex AI, OpenAI, Ollama"
language: "en-GB"
layout: "index"
locale: "en_GB"
logo_alt: "rousseau-agent logo"
logo_height: "33"
logo_width: "100"
logo: ""
name: "rousseau-agent"
permalink: "https://docs.rousseau-agent.dev/"
rating: "general"
referrer: "no-referrer"
revisit-after: "7 days"
robots: "index, follow"
short_name: "rousseau"
subtitle: "The self-hosted, container-native coding agent."
tags: "coding agent, self-hosted, container-native, MCP, SLSA-3, cosign, LLM, transports, WhatsApp, Slack"
theme-color: "26, 58, 138"
title: "rousseau-agent"
url: "https://docs.rousseau-agent.dev"
viewport: "width=device-width, initial-scale=1, shrink-to-fit=no"
changefreq: "weekly"

# News SiteMap
news_genres: "Blog"
news_keywords: "rousseau-agent, coding agent, self-hosted, MCP"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "rousseau-agent"

# RSS
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "welcome"
order: 1
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/index.html"
item_link: "https://docs.rousseau-agent.dev/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "rousseau-agent"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
ttl: "60"
type: "website"
webmaster: sebastian.rousseau@gmail.com (Sebastien Rousseau)

# Apple
apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "rousseau-agent"
apple-touch-fullscreen: "yes"

# MS Application
msapplication-navbutton-color: "rgb(26,58,138)"

# Twitter Card
twitter_card: "summary_large_image"
twitter_creator: "rousseauagent"
twitter_description: "The self-hosted, container-native coding agent. 9 chat transports, 5 LLM providers, SLSA-3, cosign, MCP-native."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "rousseau-agent — self-hosted coding agent"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<figure class="tui-demo tui-interactive" role="figure" aria-label="Interactive rousseau chat demo — type help to see commands"><header class="tui-demo-titlebar"><span class="tui-demo-dot r"></span><span class="tui-demo-dot y"></span><span class="tui-demo-dot g"></span><span class="tui-demo-title">rousseau chat · interactive demo</span></header><section class="tui-demo-body" id="tuiBody"><p class="tui-line tui-line-1 dim">$ <span style="color:#e6edf3">rousseau chat</span></p><p class="tui-line tui-line-2 dim">session bc4a-42d1 · provider=claudecli · workspace=~/team-rousseau</p><p class="tui-line tui-line-3 dim">type <kbd style="color:#7ce38b;background:#0f2a1e;padding:2px 8px;border-radius:3px;font-family:var(--font-mono)">help</kbd> or ask anything · <kbd>Ctrl</kbd>+<kbd>L</kbd> clears</p></section><form class="tui-input-form" id="tuiForm" autocomplete="off"><span class="tui-prompt">you ›</span><input id="tuiInput" type="text" class="tui-input" aria-label="Type a message to rousseau" placeholder="try: help, list transports, tell me about MCP" autocomplete="off" spellcheck="false"/><button type="submit" class="visually-hidden" aria-label="Send message">Send</button></form></figure>

<section class="landing-features"><article class="landing-feature"><span class="landing-feature-icon" aria-hidden="true">✓</span><h3>Enterprise-hardened</h3><p>SLSA Level 3 provenance, cosign-signed checksums, CycloneDX SBOM, reproducible builds, rootless Podman with dropped capabilities.</p></article><article class="landing-feature"><span class="landing-feature-icon" aria-hidden="true">◐</span><h3>Multi-modal reach</h3><p>Nine chat transports behind one daemon — WhatsApp, Signal, Telegram, Matrix, Slack, Discord, iMessage, Email, SMS. No public HTTP surface required.</p></article><article class="landing-feature"><span class="landing-feature-icon" aria-hidden="true">⚙</span><h3>Model-agnostic</h3><p>Five LLM provider families behind one <code>agent.Provider</code> interface — claudecli, Anthropic, AWS Bedrock, Google Vertex AI, OpenAI-compatible.</p></article><article class="landing-feature"><span class="landing-feature-icon" aria-hidden="true">◇</span><h3>MCP-native</h3><p>Ships a Model Context Protocol server over stdio. Any MCP-compatible client — Claude Desktop, Continue, Codeium — can drive rousseau's tools and sessions.</p></article><article class="landing-feature"><span class="landing-feature-icon" aria-hidden="true">◎</span><h3>Zero telemetry</h3><p>No SaaS control plane, no license server, no analytics endpoint, no unique identifiers. The only outbound traffic is the LLM call and the transport you enabled.</p></article><article class="landing-feature"><span class="landing-feature-icon" aria-hidden="true">▤</span><h3>Single static binary</h3><p>Go 1.26+, <code>CGO_ENABLED=0</code>, embeds <code>modernc.org/sqlite</code>. No libc, no interpreter runtime. Runs identically on macOS, Linux, and Windows.</p></article></section>

## Get running in five minutes

<div class="tabs" data-tabs="landing-install">
  <div class="tab-list" role="tablist" aria-label="Install method">
    <button role="tab" aria-selected="true">go install</button>
    <button role="tab" aria-selected="false">Signed release</button>
    <button role="tab" aria-selected="false">Container</button>
  </div>
  <div class="tab-panel" role="tabpanel">

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
rousseau chat
```

That's the whole install. `go install` fetches the module, builds the static binary against your Go 1.26+ toolchain, and drops it in `$GOBIN`. `rousseau chat` launches the Bubble Tea TUI with your configured provider.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Every release ships a cosign signature and a CycloneDX SBOM:

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_checksums.txt.sig \
  rousseau_checksums.txt

sha256sum -c rousseau_checksums.txt
tar -xzf rousseau_*.tar.gz && sudo install -m 0755 rousseau /usr/local/bin/
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```sh
podman build -t rousseau-agent:local -f docker/Dockerfile .
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload && systemctl --user start rousseau-agent.service
```

Rootless Podman + systemd Quadlet. Read-only rootfs, dropped capabilities, seccomp filter, non-root UID.

  </div>
</div>

<nav class="landing-cta-row" aria-label="Primary calls to action"><a class="btn btn-primary btn-large" href="/quickstart/">Read the Quickstart →</a><a class="btn btn-outline btn-large" href="/getting-started/">Full getting-started guide</a><a class="btn btn-outline btn-large" href="https://github.com/sebastienrousseau/rousseau-agent">GitHub</a></nav>

## Where to next

<section class="landing-links"><a href="/quickstart/" class="landing-link-card"><h3>Quickstart</h3><p>Install, configure a provider, hold your first conversation, wire a transport, and verify the release supply chain in about five minutes.</p></a><a href="/concepts/" class="landing-link-card"><h3>Concepts</h3><p>Agent loop, session store, tool registry, approval policies, MCP server, cron scheduler, skills loader — how the daemon actually works.</p></a><a href="/configuration/" class="landing-link-card"><h3>Configuration</h3><p>Every field in <code>internal/config/config.go</code>, one page. Providers, transports, agent loop, compression, approver, state store.</p></a><a href="/deployment/" class="landing-link-card"><h3>Deployment</h3><p>Rootless Podman with Quadlet, systemd unit reference, Kubernetes note, secrets from Vault or cloud secret managers.</p></a><a href="/security/" class="landing-link-card"><h3>Security</h3><p>Supply-chain posture, trust model, cosign verify recipe, seccomp policy, network egress allowlist, disclosure SLA.</p></a><a href="/tutorials/" class="landing-link-card"><h3>Tutorials</h3><p>End-to-end walkthroughs — code review bot on Slack, nightly changelog on WhatsApp, MCP + Claude Desktop, hardened approver policy.</p></a></section>
