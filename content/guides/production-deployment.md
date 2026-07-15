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
description: "Beyond the Quadlet reference: log shipping, session-store backup, health checks, rolling restarts, and multi-transport coexistence."
keywords: "production, log shipping, backup, health check, rolling restart, systemd"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/guides/production-deployment/"
subtitle: "Everything the Quadlet reference doesn't already cover."
tags: "guides, production, deployment, backup, logs, health check"
title: "Guide: Production deployment"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "production, log shipping, backup, health check, rolling restart, systemd"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: Production deployment"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/production-deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/production-deployment/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide: Production deployment"
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
twitter_description: "Beyond the Quadlet reference: log shipping, session-store backup, health checks, rolling restarts, and multi-transport coexistence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide: Production deployment"
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

## Read this after

The reference Quadlet unit at `docker/rousseau-agent.container` covers the "how to run rousseau" story. This guide covers what you add around it before calling it production: logs, backups, health, and process hygiene.

## Log shipping

Rousseau writes structured logs to stderr via `log/slog` (`internal/cli/root.go`). When you run it under systemd, that stderr lands in the journal. Options for shipping off the host:

| Tool | Fit | Notes |
|---|---|---|
| Vector (`vector.dev`) | Best default. | `journald` source + a filter dropping DEBUG. Ship to Loki, Datadog, S3, whatever. |
| Promtail + Loki | If you already run Grafana. | Loki's `journal` source works directly against `journalctl -o json`. |
| Datadog Agent | If Datadog is the org standard. | The DD agent has a journald tail. Structured JSON parses natively. |
| Fluent Bit | Small footprint alternative. | Set `log.format: json` in `config.yaml`; Fluent Bit's `systemd` input parses. |

Configure `log.format: json` (`internal/config/config.go` `LogConfig.Format`) unconditionally in production. Text output is designed for `less`, not machine parsing.

See [Guides: Observability](/guides/observability/) for a full Loki pipeline recipe.

## Session-store backup

The state directory `~/.local/share/rousseau/` is the only durable state rousseau owns. Back it up nightly.

Two approaches:

**1. SQLite `.backup` (recommended).**

```sh
sqlite3 ~/.local/share/rousseau/sessions.db \
  ".backup '/backup/sessions.db.$(date +%Y%m%d).bak'"
sqlite3 ~/.local/share/rousseau/whatsapp.db \
  ".backup '/backup/whatsapp.db.$(date +%Y%m%d).bak'"
restic backup /backup
```

`.backup` uses SQLite's online API — safe even while the daemon is writing. See [Reference: Session store](/reference/session-store/).

**2. Filesystem snapshot.**

Because WAL journaling is on (`Open()` in `internal/state/sqlite/store.go`), `restic` and `borg` can snapshot the raw files while the daemon runs. WAL guarantees a consistent point-in-time image.

Do not:

- Copy the `.db` file with `cp` while the daemon is running unless you also copy `-wal` and `-shm`.
- Store backups on the same disk.
- Skip the WhatsApp device credentials file — losing it means re-scanning the QR.

## Health checks

`rousseau status` (`internal/cli/status.go`) exits 0 on healthy, non-zero on trouble. Use it as a systemd health probe:

```ini
[Service]
ExecStartPost=/usr/bin/timeout 30 podman exec rousseau-agent rousseau status
```

For a richer probe, script a check that:

1. Runs `rousseau status`.
2. Confirms the session store's last write was recent (`stat sessions.db -c %Y` compared to now).
3. Checks the container's uptime via `podman inspect`.

Rousseau does not expose an HTTP `/healthz`. If your platform requires one (Kubernetes readiness probes), see [Guides: Kubernetes deployment](/guides/kubernetes-deployment/) — you wrap rousseau in a small `curl`-friendly sidecar.

## Rolling restart

Because state is a single SQLite file, the daemon is genuinely single-instance. A rolling restart is: stop, replace image, start. No warm-up required.

```sh
podman pull localhost/rousseau-agent:local     # or rebuild locally
systemctl --user restart rousseau-agent
podman logs -n 50 rousseau-agent | grep -E 'starting|connected'
```

Expected log sequence (from `internal/transport/whatsapp/client.go`):

```
INFO whatsapp.starting store=… allowlist=1
INFO whatsapp.connected
```

If the daemon does not emit `whatsapp.connected` within ~15 seconds, roll back.

## Multiple transports on one host

You may want the same session store shared by WhatsApp and Slack. Two ways:

- **Multiple Quadlet units** — one for each transport, each pointing at the same `state.path`. WAL + `busy_timeout` (see `Open()` in `internal/state/sqlite/store.go`) makes concurrent writers safe.
- **One binary, one transport per invocation.** Rousseau's transport commands are single-transport (`whatsapp`, `slack`, `signal`, …). To run two transports you run two processes.

## Zero-downtime configuration changes

Rousseau does not hot-reload `config.yaml`. Config changes require a restart. `SIGHUP` is not wired for reload.

Practical workflow:

1. Edit `~/.config/rousseau/config.yaml`.
2. `systemctl --user restart rousseau-agent`.
3. Verify from logs.

For most transports the reconnection is fast (~1-3 seconds). The main pause is on WhatsApp, where whatsmeow re-establishes the websocket.

## Log retention

`journald` retention is set by `SystemMaxUse=` in `/etc/systemd/journald.conf`. For an audit-friendly deployment, ship logs off-host and set journald to a shorter retention on the local disk (e.g. 7 days) so the audit trail lives in Loki/S3, not on a filesystem an intruder might rotate.

## Container image lifecycle

Rebuild the image on every rousseau release you want to adopt:

```sh
cd ~/rousseau-agent
git pull
podman build -t rousseau-agent:local -f docker/Dockerfile .
systemctl --user restart rousseau-agent
```

The Quadlet `AutoUpdate=disabled` line (in `docker/rousseau-agent.container`) prevents `podman auto-update` from touching the container. You control the update cadence.

## Related

- [Deployment](/deployment/) — the reference Quadlet unit.
- [Tutorial: Deploy to a VPS](/tutorials/deploy-to-a-vps/) — worked example.
- [Guides: Observability](/guides/observability/) — log pipeline.
- [Guides: Enterprise Onboarding](/guides/enterprise-onboarding/) — full checklist.
