---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "Move rousseau-agent from bare-metal go install to rootless Podman + systemd Quadlet without losing conversation history."
keywords: "container migration, podman, quadlet, systemd, bare metal, bind mount"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/migrations/container-migration/"
subtitle: "Bare-metal to rootless Podman + systemd Quadlet."
tags: "migrations, container, podman, quadlet"
title: "Migration: Bare Metal → Podman"

news_genres: "Blog"
news_keywords: "container migration, podman, quadlet"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Migration: Bare Metal → Podman"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "migrations"
order: 13
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/migrations/container-migration/index.html"
item_link: "https://docs.rousseau-agent.dev/migrations/container-migration/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Migration: Bare Metal → Podman"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
ttl: "60"
type: "website"
webmaster: sebastian.rousseau@gmail.com (Sebastien Rousseau)

apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "rousseau-agent"
apple-touch-fullscreen: "yes"

msapplication-navbutton-color: "rgb(26,58,138)"

twitter_card: "summary"
twitter_creator: "rousseauagent"
twitter_description: "Move rousseau-agent from bare-metal go install to rootless Podman + systemd Quadlet without losing conversation history."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Migration: Bare Metal → Podman"
twitter_url: "https://docs.rousseau-agent.dev"

author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Overview

This guide moves a working `go install`-based rousseau setup into the reference production posture: a rootless Podman container managed by a systemd Quadlet unit, with a hardened runtime posture (read-only rootfs, dropped capabilities, seccomp, `NoNewPrivileges`, `keep-id` user namespace).

<aside class="admonition" data-type="tip"><span class="admonition-title">Preserve state</span><p>The migration keeps <code>sessions.db</code> and <code>whatsapp.db</code> on the host. The container mounts them read-write. WhatsApp pairing survives; conversation history survives.</p></aside>

## What changes

- Binary invocation moves from `rousseau whatsapp` on the host to `podman run` under a Quadlet-managed systemd service.
- File paths move from `~/.local/share/rousseau/*.db` on the host to bind-mounted volumes inside the container.
- The Claude CLI (`~/.claude`) is bind-mounted into the container so the `claudecli` provider keeps its OAuth token.
- Workspace access is scoped to a single bind mount — the container sees nothing else on the host.

## Config diff

The rousseau `config.yaml` does not change semantically. Only the file's location moves (from `~/.config/rousseau/config.yaml` on the host to a bind mount inside the container).

## Migration steps

### 1. Back up host state

```sh
tar -czf rousseau-state.tar.gz \
  -C "$HOME/.local/share" rousseau \
  -C "$HOME/.config" rousseau \
  -C "$HOME" .claude
```

### 2. Stop the host-side daemon

```sh
# If you started it manually, Ctrl+C. If under systemd (user unit):
systemctl --user stop rousseau-agent.service || true
```

### 3. Build the image

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
podman build -t rousseau-agent:local -f docker/Dockerfile .
```

### 4. Install the Quadlet unit

```sh
mkdir -p ~/.config/containers/systemd
cp docker/rousseau-agent.container ~/.config/containers/systemd/
systemctl --user daemon-reload
```

The unit ships with:

| Setting | Value | Rationale |
|---|---|---|
| `Network=pasta` | Rootless network stack | slirp4netns removed from recent Podman |
| `UserNS=keep-id` | Container UID 1000 → host UID 1000 | Bind-mounted files retain host ownership |
| `ReadOnly=true` | Root filesystem read-only | The binary can't mutate the image |
| `Tmpfs=/tmp:rw,size=64m,mode=1777` | Writable scratch | Anything the daemon writes lives on a bind mount |
| `DropCapability=all` + `NoNewPrivileges=true` | Least privilege | Outbound sockets need no elevated caps |
| `Volume=%h/.local/share/rousseau:…rw,Z` | State survives | Uses your existing sessions.db |
| `Volume=%h/.claude:…rw,Z` | Claude CLI auth | Reads / refreshes cached OAuth tokens |
| `Volume=%h/team-rousseau-workspace:/workspace:rw,Z` | Workspace | Nothing else on the host is mounted |

### 5. Start the container

```sh
systemctl --user start rousseau-agent.service
journalctl --user -u rousseau-agent.service -f
```

The first launch **inside the container** will see the existing pairing — no QR should print. If it does, the bind mount is not resolving to the host's `whatsapp.db`. Verify with `podman exec` (if privileges allow) or check the Quadlet mount paths.

## Downgrade path

Stop the container, restart the host binary:

```sh
systemctl --user stop rousseau-agent.service
rousseau whatsapp --allow '447900123456@s.whatsapp.net'
```

Because the container was reading/writing the same `sessions.db` and `whatsapp.db` on the host, the host binary picks up exactly where the container left off. No data migration required.

If you built up state exclusively inside the container:

```sh
# Ensure the container is stopped, then let the host binary use the same paths.
```

## Verification checklist

- [ ] `systemctl --user status rousseau-agent.service` is `active (running)`.
- [ ] `journalctl --user -u rousseau-agent.service | grep whatsapp.connected` fires within 10 s.
- [ ] Send yourself a WhatsApp message from an allowlisted JID; the reply lands.
- [ ] `rousseau session list --limit 5` (run on the host against the same sessions.db) shows the new session.
- [ ] `rousseau doctor` (host) reports green.

## Common failure modes

<aside class="admonition" data-type="warning"><span class="admonition-title">SELinux / :Z</span><p>On SELinux systems the <code>:Z</code> suffix on the volumes relabels files for the container user. Without it you'll see permission-denied on <code>sessions.db</code>.</p></aside>

- **Container starts, exits with `permission denied` on sessions.db** — missing `:Z` on the volume, or the host directory's owner does not match `keep-id`. `chown -R $(id -u):$(id -g) ~/.local/share/rousseau` and reload.
- **QR printed inside the container even though the host had a pairing** — the `whatsapp.db` bind mount is wrong; check the Quadlet unit's `Volume=` line.
- **`claudecli: exec: "claude": executable file not found`** — the runtime image ships the Node layer with the claude CLI. If a local override omits it, install claude inside the image or switch to `provider: anthropic`.

## Related pages

- [Deployment](/deployment/)
- [Security](/security/)
- [Migrations: Overview](/migrations/overview/)
- [Best Practices: Disaster recovery](/best-practices/disaster-recovery/)
- [Best Practices: Network egress](/best-practices/network-egress/)
