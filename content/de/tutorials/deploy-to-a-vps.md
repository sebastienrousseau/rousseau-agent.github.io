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
description: "Walk a fresh VPS from bare install to a hardened rousseau-agent daemon under rootless Podman and a systemd Quadlet unit."
keywords: "vps, podman, quadlet, systemd, rootless, deployment, hardening"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/tutorials/deploy-to-a-vps/"
subtitle: "Build a container, provision a VPS, install the Quadlet unit, verify the service."
tags: "tutorials, deployment, podman, quadlet, systemd, vps"
title: "Tutorial: auf einem VPS bereitstellen"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "vps, podman, quadlet, systemd, rootless, deployment, hardening"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: auf einem VPS bereitstellen"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/deploy-to-a-vps/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/deploy-to-a-vps/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: auf einem VPS bereitstellen"
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
twitter_title: "Tutorial: auf einem VPS bereitstellen"
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

## Was Sie bauen

Ein frischer Ubuntu-24.04-VPS, der den rousseau-agent-WhatsApp-Daemon unter einem rootless Podman-Container betreibt, gesteuert von der systemd-Quadlet-Unit unter `docker/rousseau-agent.container`. Read-only-Root-Dateisystem, alle Capabilities entzogen, `NoNewPrivileges=true`, seccomp an. Null eingehende Netzwerk-Ports.

Geschätzte Zeit: 45 Minuten.

## Voraussetzungen

- Ein VPS mit Ubuntu 24.04 (oder Debian 12+ / Fedora 40+). 1 GB RAM, 20 GB Disk reichen reichlich.
- SSH-Key-Zugriff auf einen Non-Root-Nutzer mit sudo.
- Ihr Anthropic-API-Schlüssel oder die Bereitschaft, `claudecli` zu betreiben — `claudecli` braucht `claude` auf dem VPS mit einer aktiven OAuth-Sitzung, was auf einem Headless-Server umständlich ist. Anthropic direkt oder Bedrock ist die praktikable Wahl.

## Schritt 1: Basis-OS-Setup

```sh
ssh admin@vps
sudo apt update && sudo apt -y upgrade
sudo apt -y install podman uidmap fuse-overlayfs slirp4netns curl git

# rootless podman needs subuid/subgid ranges for the user
grep rousseau /etc/subuid || sudo usermod --add-subuids 200000-265535 rousseau
grep rousseau /etc/subgid || sudo usermod --add-subgids 200000-265535 rousseau
```

Erstellen Sie den Service-Nutzer und dessen systemd-Nutzersitzung:

```sh
sudo useradd -m -s /bin/bash rousseau
sudo loginctl enable-linger rousseau     # keeps user services running when nobody is logged in
```

## Schritt 2: Source übertragen

Die Quadlet-Unit unter `docker/rousseau-agent.container` baut ein lokales Image. Auf dem VPS:

```sh
sudo -iu rousseau
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
podman build -t rousseau-agent:local -f docker/Dockerfile .
podman image inspect localhost/rousseau-agent:local | head
```

Das `Dockerfile` produziert ein statisches Go-Binary (`CGO_ENABLED=0`), kopiert es in eine minimale Basis und läuft als UID 1000. Siehe [Bereitstellung](/de/deployment/) für die Base-Image-Diskussion.

## Schritt 3: Konfiguration seeden

Rousseau liest `~/.config/rousseau/config.yaml`. Legen Sie es auf dem Host an — die Quadlet-Unit bind-mountet das `$HOME` des Containers zurück auf den Host.

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

Speichern Sie den Anthropic-API-Schlüssel in einer systemd-Umgebungsdatei — niemals in `config.yaml`:

```sh
mkdir -p /home/rousseau/.config/rousseau
cat > /home/rousseau/.config/rousseau/env <<'ENV'
ANTHROPIC_API_KEY=sk-ant-…
ENV
chmod 0600 /home/rousseau/.config/rousseau/env
```

Referenzieren Sie sie aus der Quadlet-Unit — siehe nächsten Schritt.

## Schritt 4: Quadlet-Unit installieren

```sh
mkdir -p /home/rousseau/.config/containers/systemd
cp docker/rousseau-agent.container /home/rousseau/.config/containers/systemd/
```

Für Ihre JID und Secret-Datei bearbeiten:

```sh
sed -i 's|Exec=whatsapp --allow.*|Exec=whatsapp --allow YOUR_JID@s.whatsapp.net|' \
  /home/rousseau/.config/containers/systemd/rousseau-agent.container

cat >> /home/rousseau/.config/containers/systemd/rousseau-agent.container <<'EOF'
EnvironmentFile=%h/.config/rousseau/env
EOF
```

Reloaden und starten:

```sh
systemctl --user daemon-reload
systemctl --user enable --now rousseau-agent
systemctl --user status rousseau-agent
```

## Schritt 5: erste Kopplung

Die WhatsApp-Bridge muss beim ersten Mal einen QR-Code ausgeben. Attachen:

```sh
podman logs -f rousseau-agent
# scan the QR from your phone: WhatsApp > Settings > Linked devices
```

Erwartete Log-Sequenz (aus `internal/transport/whatsapp/client.go`):

```
INFO whatsapp.starting store=… allowlist=1
INFO whatsapp.qr_ready
INFO whatsapp.paired
INFO whatsapp.connected
```

Gerätedaten persistieren nach `/home/rousseau/.local/share/rousseau/whatsapp.db`. Nachfolgende Neustarts überspringen den QR.

## Schritt 6: verifizieren

```sh
podman exec rousseau-agent rousseau status
```

Exit-Code 0 bedeutet, der Daemon ist gesund. Jeder Nicht-Null-Wert ist ein Warnsignal — siehe [Referenz: Exit-Codes](/de/reference/exit-codes/).

Senden Sie sich eine Testnachricht vom Allowlist-Telefon. Strukturierte Logs zeigen:

```
INFO whatsapp.incoming from=447900123456@s.whatsapp.net
INFO tool.execute name=read id=t_1
INFO whatsapp.handler_ok elapsed=…
```

## Schritt 7: Härtungs-Review

Die Quadlet-Unit erzwingt bereits:

- `ReadOnly=true` + `Tmpfs=/tmp` — keine Image-Mutation zur Laufzeit.
- `DropCapability=all` — das Go-Binary braucht keine erhöhten Caps.
- `NoNewPrivileges=true` — Kindprozesse können keine Privilegien erlangen.
- `SeccompProfile=/usr/share/containers/seccomp.json` — Syscall-Filter auf Kernel-Ebene.
- `Network=pasta` — rootless Netzwerk-Stack, blockiert Inbound per Default.
- `UserNS=keep-id` — bind-gemountete Dateien gehören wie erwartet auf beiden Seiten.

Wenn Sie die dichteste Haltung möchten, wickeln Sie den Daemon in eine reine Outbound-Firewall (nftables oder Cloudflare Zero-Trust), die nur die CDN-Bereiche zulässt, zu denen Anthropic + Meta tatsächlich auflösen. Siehe [Leitfäden: Enterprise-Onboarding](/de/guides/enterprise-onboarding/) für die Checkliste.

## Schritt 8: Backup

Der gesamte persistente Zustand ist ein Verzeichnis: `/home/rousseau/.local/share/rousseau/`. `restic` oder `borg` es nächtlich.

```sh
sudo -iu rousseau -- restic backup /home/rousseau/.local/share/rousseau
```

Die SQLite-Datenbanken können sicher live gesnapshotet werden, weil WAL-Journaling durch `Open()` in `internal/state/sqlite/store.go` aktiviert ist.

## Verwandt

- [Bereitstellung](/de/deployment/) — vollständige Quadlet-Unit-Referenz.
- [Leitfäden: Produktions-Bereitstellung](/de/guides/production-deployment/) — Log-Shipping, rollierende Neustarts.
- [Leitfäden: Enterprise-Onboarding](/de/guides/enterprise-onboarding/) — SBOM-Verifikation, seccomp-Audit.
- [Sicherheit](/de/security/) — Vertrauensgrenzen.
