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
description: "Backup, restore, and integrity checks for rousseau's SQLite state stores: sessions.db and whatsapp.db."
keywords: "backup, restore, sqlite, wal, integrity, best practices"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/best-practices/disaster-recovery/"
subtitle: "Backup, restore, and integrity for the session store."
tags: "best-practices, dr, backup"
title: "Disaster Recovery"

news_genres: "Blog"
news_keywords: "backup, restore, sqlite"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Disaster Recovery"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "best-practices"
order: 16
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/best-practices/disaster-recovery/index.html"
item_link: "https://docs.rousseau-agent.dev/best-practices/disaster-recovery/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Disaster Recovery"
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
twitter_description: "Backup, restore, and integrity checks for rousseau's SQLite state stores."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Disaster Recovery"
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

Rousseau's entire operational state fits in two SQLite files:

- `sessions.db` — conversations, cron jobs, JID map, FTS5 index, claude cache.
- `whatsapp.db` — whatsmeow device credentials (WhatsApp only).

Every DR strategy here revolves around backing those files up and restoring them cleanly.

<aside class="admonition" data-type="tip"><span class="admonition-title">Prefer <code>.backup</code> to <code>cp</code></span><p>SQLite provides a hot-backup API. Under WAL mode, plain <code>cp</code> is generally fine, but <code>sqlite3 sessions.db ".backup /tmp/backup.db"</code> is guaranteed consistent.</p></aside>

## Backup

<div class="tabs" data-tabs="dr-backup">
  <div class="tab-list" role="tablist" aria-label="Backup style">
    <button role="tab" aria-selected="true">Ad-hoc</button>
    <button role="tab" aria-selected="false">Nightly cron</button>
    <button role="tab" aria-selected="false">Restic</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Before any upgrade, migration, or destructive command:

```sh
D=$(date -u +%Y%m%d-%H%M%SZ)
mkdir -p ~/backup/rousseau/$D
sqlite3 ~/.local/share/rousseau/sessions.db ".backup ~/backup/rousseau/$D/sessions.db"
cp ~/.local/share/rousseau/whatsapp.db ~/backup/rousseau/$D/whatsapp.db 2>/dev/null || true
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```ini
# ~/.config/systemd/user/rousseau-backup.service
[Service]
Type=oneshot
ExecStart=/usr/local/bin/rousseau-backup.sh

# ~/.config/systemd/user/rousseau-backup.timer
[Timer]
OnCalendar=daily
Persistent=true
[Install]
WantedBy=timers.target
```

```sh
# /usr/local/bin/rousseau-backup.sh
#!/usr/bin/env bash
set -euo pipefail
D=$(date -u +%Y%m%d-%H%M%SZ)
DEST="$HOME/backup/rousseau/$D"
mkdir -p "$DEST"
sqlite3 "$HOME/.local/share/rousseau/sessions.db" ".backup $DEST/sessions.db"
cp "$HOME/.local/share/rousseau/whatsapp.db" "$DEST/" 2>/dev/null || true
find "$HOME/backup/rousseau" -mindepth 1 -maxdepth 1 -mtime +30 -print0 | xargs -0 rm -rf --
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

```sh
export RESTIC_REPOSITORY=b2:rousseau-bucket:backups
export RESTIC_PASSWORD_FILE=/etc/rousseau/restic.pw

restic backup \
  ~/.local/share/rousseau/sessions.db \
  ~/.local/share/rousseau/whatsapp.db \
  --tag rousseau
```

  </div>
</div>

## Restore

```sh
# Stop any running rousseau processes first
systemctl --user stop 'rousseau-*.service'
pkill -TERM rousseau 2>/dev/null || true

# Restore
cp ~/backup/rousseau/<D>/sessions.db ~/.local/share/rousseau/
cp ~/backup/rousseau/<D>/whatsapp.db ~/.local/share/rousseau/ 2>/dev/null || true

# Verify
sqlite3 ~/.local/share/rousseau/sessions.db "PRAGMA integrity_check;"
# expect: ok

# Start
systemctl --user start 'rousseau-*.service'
```

## Integrity checks

Run monthly:

```sh
sqlite3 ~/.local/share/rousseau/sessions.db "PRAGMA integrity_check;"
sqlite3 ~/.local/share/rousseau/sessions.db "PRAGMA quick_check;"
sqlite3 ~/.local/share/rousseau/sessions.db "SELECT COUNT(*) FROM sessions;"
```

If `integrity_check` returns anything other than `ok`, restore from the latest good backup.

## What survives

| Backup | Restores | Notes |
|---|---|---|
| `sessions.db` | Conversations, cron jobs, JID map, FTS5, claude cache | Enough for full recovery of history + scheduled prompts |
| `whatsapp.db` | WhatsApp pairing | Without this, a QR re-pair is required |
| `~/.claude/` (for `claudecli`) | Claude Code OAuth | Not owned by rousseau; back up separately |
| `~/.config/rousseau/config.yaml` | Config | Also worth versioning |

## Failure modes

- **Backup taken during a heavy write** — WAL means readers see a consistent snapshot, but a plain `cp` might catch the WAL mid-checkpoint. Use `.backup` or stop the daemon.
- **Restore into a running daemon** — silent corruption. Always stop the process first.
- **Restore with mismatched user** — the file will be owned by the wrong user after container/host role changes. `chown` back to `rousseau:rousseau` (or your uid).

## Related pages

- [Reference: Session store](/reference/session-store/)
- [Reference: Config: State](/reference/config/state/)
- [Migrations: Overview](/migrations/overview/)
- [Best Practices: Session hygiene](/best-practices/session-hygiene/)
