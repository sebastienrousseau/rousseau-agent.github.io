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
description: "Walk a fresh VPS from bare install to a hardened rousseau-agent daemon under rootless Podman and a systemd Quadlet unit."
keywords: "vps, podman, quadlet, systemd, rootless, deployment, hardening"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/tutorials/deploy-to-a-vps/"
subtitle: "Build a container, provision a VPS, install the Quadlet unit, verify the service."
tags: "tutorials, deployment, podman, quadlet, systemd, vps"
title: "Tutorial: Deploy to a VPS"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "vps, podman, quadlet, systemd, rootless, deployment, hardening"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: Deploy to a VPS"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/deploy-to-a-vps/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/deploy-to-a-vps/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: Deploy to a VPS"
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
twitter_description: "Walk a fresh VPS from bare install to a hardened rousseau-agent daemon under rootless Podman and a systemd Quadlet unit."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: Deploy to a VPS"
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

## What you build

A fresh Ubuntu 24.04 VPS running the rousseau-agent WhatsApp daemon under a rootless Podman container, driven by the systemd Quadlet unit at `docker/rousseau-agent.container`. Read-only root filesystem, all capabilities dropped, `NoNewPrivileges=true`, seccomp on. Zero inbound network ports.

Estimated time: 45 minutes.

## Prerequisites

- A VPS with Ubuntu 24.04 (or Debian 12+ / Fedora 40+). 1 GB RAM, 20 GB disk is plenty.
- SSH key access to a non-root user with sudo.
- Your Anthropic API key or willingness to run `claudecli` — `claudecli` needs `claude` installed on the VPS with an active OAuth session, which is awkward on a headless server. Anthropic direct or Bedrock is the practical choice.

## Step 1: base OS setup

```sh
ssh admin@vps
sudo apt update && sudo apt -y upgrade
sudo apt -y install podman uidmap fuse-overlayfs slirp4netns curl git

# rootless podman needs subuid/subgid ranges for the user
grep rousseau /etc/subuid || sudo usermod --add-subuids 200000-265535 rousseau
grep rousseau /etc/subgid || sudo usermod --add-subgids 200000-265535 rousseau
```

Create the service user and its systemd user session:

```sh
sudo useradd -m -s /bin/bash rousseau
sudo loginctl enable-linger rousseau     # keeps user services running when nobody is logged in
```

## Step 2: transfer the source

The Quadlet unit at `docker/rousseau-agent.container` builds a local image. On the VPS:

```sh
sudo -iu rousseau
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
podman build -t rousseau-agent:local -f docker/Dockerfile .
podman image inspect localhost/rousseau-agent:local | head
```

The `Dockerfile` produces a static Go binary (`CGO_ENABLED=0`), copies it into a minimal base, and runs as UID 1000. See [Deployment](/deployment/) for the base-image discussion.

## Step 3: seed configuration

Rousseau reads `~/.config/rousseau/config.yaml`. Create it on the host — the Quadlet unit bind-mounts the container's `$HOME` back to the host.

```sh
mkdir -p /home/rousseau/.config/rousseau
cat > /home/rousseau/.config/rousseau/config.yaml <<'YAML'
provider: anthropic

anthropic:
  model: claude-sonnet-4-6
  max_tokens: 4096

whatsapp:
  reply_header: "*rousseau*\n\n"

agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

log:
  level: info
  format: json
YAML
chown -R rousseau:rousseau /home/rousseau/.config
```

Store the Anthropic API key in a systemd environment file — never in `config.yaml`:

```sh
mkdir -p /home/rousseau/.config/rousseau
cat > /home/rousseau/.config/rousseau/env <<'ENV'
ANTHROPIC_API_KEY=sk-ant-…
ENV
chmod 0600 /home/rousseau/.config/rousseau/env
```

Reference it from the Quadlet unit — see the next step.

## Step 4: install the Quadlet unit

```sh
mkdir -p /home/rousseau/.config/containers/systemd
cp docker/rousseau-agent.container /home/rousseau/.config/containers/systemd/
```

Edit for your JID and secret file:

```sh
sed -i 's|Exec=whatsapp --allow.*|Exec=whatsapp --allow YOUR_JID@s.whatsapp.net|' \
  /home/rousseau/.config/containers/systemd/rousseau-agent.container

cat >> /home/rousseau/.config/containers/systemd/rousseau-agent.container <<'EOF'
EnvironmentFile=%h/.config/rousseau/env
EOF
```

Reload and start:

```sh
systemctl --user daemon-reload
systemctl --user enable --now rousseau-agent
systemctl --user status rousseau-agent
```

## Step 5: first pairing

The WhatsApp bridge needs to print a QR code the first time. Attach:

```sh
podman logs -f rousseau-agent
# scan the QR from your phone: WhatsApp > Settings > Linked devices
```

Expected log sequence (from `internal/transport/whatsapp/client.go`):

```
INFO whatsapp.starting store=… allowlist=1
INFO whatsapp.qr_ready
INFO whatsapp.paired
INFO whatsapp.connected
```

Device credentials persist to `/home/rousseau/.local/share/rousseau/whatsapp.db`. Subsequent restarts skip the QR.

## Step 6: verify

```sh
podman exec rousseau-agent rousseau status
```

Exit code 0 means the daemon is healthy. Any non-zero is a red flag — see [Reference: Exit codes](/reference/exit-codes/).

Send yourself a test message from the allowlisted phone. Structured logs show:

```
INFO whatsapp.incoming from=447900123456@s.whatsapp.net
INFO tool.execute name=read id=t_1
INFO whatsapp.handler_ok elapsed=…
```

## Step 7: hardening review

The Quadlet unit already enforces:

- `ReadOnly=true` + `Tmpfs=/tmp` — no image mutation at runtime.
- `DropCapability=all` — the Go binary needs no elevated caps.
- `NoNewPrivileges=true` — child processes cannot gain privileges.
- `SeccompProfile=/usr/share/containers/seccomp.json` — kernel-level syscall filter.
- `Network=pasta` — rootless network stack, blocks inbound by default.
- `UserNS=keep-id` — bind-mounted files owned as expected on both sides.

If you want the tightest posture, wrap the daemon in an outbound-only firewall (nftables or Cloudflare Zero-Trust) that only allows the CDN ranges Anthropic + Meta actually resolve to. See [Guides: Enterprise Onboarding](/guides/enterprise-onboarding/) for the checklist.

## Step 8: backup

The whole persistent state is one directory: `/home/rousseau/.local/share/rousseau/`. `restic` or `borg` it nightly.

```sh
sudo -iu rousseau -- restic backup /home/rousseau/.local/share/rousseau
```

The SQLite databases are safe to snapshot live because WAL journaling is enabled by `Open()` in `internal/state/sqlite/store.go`.

## Related

- [Deployment](/deployment/) — full Quadlet unit reference.
- [Guides: Production Deployment](/guides/production-deployment/) — log shipping, rolling restarts.
- [Guides: Enterprise Onboarding](/guides/enterprise-onboarding/) — SBOM verification, seccomp audit.
- [Security](/security/) — trust boundaries.
