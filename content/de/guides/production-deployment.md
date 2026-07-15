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
description: "Beyond the Quadlet reference: log shipping, session-store backup, health checks, rolling restarts, and multi-transport coexistence."
keywords: "production, log shipping, backup, health check, rolling restart, systemd"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/guides/production-deployment/"
subtitle: "Everything the Quadlet reference doesn't already cover."
tags: "guides, production, deployment, backup, logs, health check"
title: "Leitfaden: Produktions-Bereitstellung"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "production, log shipping, backup, health check, rolling restart, systemd"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: Produktions-Bereitstellung"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 44
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/production-deployment/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/production-deployment/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: Produktions-Bereitstellung"
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
twitter_title: "Leitfaden: Produktions-Bereitstellung"
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

## Danach lesen

Die Referenz-Quadlet-Unit unter `docker/rousseau-agent.container` deckt die „Wie rousseau zu betreiben ist"-Geschichte ab. Dieser Leitfaden behandelt, was Sie darum herum ergänzen, bevor Sie es Produktion nennen: Logs, Backups, Gesundheit und Prozesshygiene.

## Log-Shipping

Rousseau schreibt strukturierte Logs via `log/slog` (`internal/cli/root.go`) nach stderr. Wenn Sie es unter systemd betreiben, landet dieses stderr im Journal. Optionen für das Ausschiffen vom Host:

| Werkzeug | Passung | Anmerkungen |
|---|---|---|
| Vector (`vector.dev`) | Bester Standard. | `journald`-Source + ein Filter, der DEBUG verwirft. Ausliefern nach Loki, Datadog, S3, was immer. |
| Promtail + Loki | Wenn Sie bereits Grafana betreiben. | Lokis `journal`-Source funktioniert direkt gegen `journalctl -o json`. |
| Datadog Agent | Wenn Datadog Org-Standard ist. | Der DD-Agent hat einen journald-Tail. Strukturiertes JSON parst nativ. |
| Fluent Bit | Alternative mit kleinem Footprint. | Setzen Sie `log.format: json` in `config.yaml`; der `systemd`-Input von Fluent Bit parst. |

Konfigurieren Sie `log.format: json` (`internal/config/config.go` `LogConfig.Format`) in Produktion bedingungslos. Text-Ausgabe ist für `less` gedacht, nicht für Maschinenparsing.

Siehe [Leitfäden: Observability](/de/guides/observability/) für ein vollständiges Loki-Pipeline-Rezept.

## Session-Store-Backup

Das State-Verzeichnis `~/.local/share/rousseau/` ist der einzige dauerhafte Zustand, den rousseau besitzt. Sichern Sie es nächtlich.

Zwei Ansätze:

**1. SQLite `.backup` (empfohlen).**

```sh
sqlite3 ~/.local/share/rousseau/sessions.db \
  ".backup '/backup/sessions.db.$(date +%Y%m%d).bak'"
sqlite3 ~/.local/share/rousseau/whatsapp.db \
  ".backup '/backup/whatsapp.db.$(date +%Y%m%d).bak'"
restic backup /backup
```

`.backup` verwendet die Online-API von SQLite — sicher, selbst während der Daemon schreibt. Siehe [Referenz: Session-Store](/de/reference/session-store/).

**2. Filesystem-Snapshot.**

Da WAL-Journaling an ist (`Open()` in `internal/state/sqlite/store.go`), können `restic` und `borg` die Rohdateien snapshotten, während der Daemon läuft. WAL garantiert ein konsistentes Point-in-Time-Image.

Nicht tun:

- Die `.db`-Datei mit `cp` kopieren, während der Daemon läuft, es sei denn, Sie kopieren auch `-wal` und `-shm`.
- Backups auf derselben Disk speichern.
- Die WhatsApp-Gerätedaten-Datei überspringen — sie zu verlieren bedeutet, den QR neu zu scannen.

## Health-Checks

`rousseau status` (`internal/cli/status.go`) beendet sich mit 0 bei gesund, mit Nicht-Null bei Problemen. Verwenden Sie es als systemd-Health-Probe:

```ini
[Service]
ExecStartPost=/usr/bin/timeout 30 podman exec rousseau-agent rousseau status
```

Für eine reichhaltigere Probe skripten Sie einen Check, der:

1. `rousseau status` ausführt.
2. Bestätigt, dass der letzte Schreibvorgang des Session-Stores kürzlich war (`stat sessions.db -c %Y` verglichen mit jetzt).
3. Die Uptime des Containers via `podman inspect` prüft.

Rousseau exponiert keine HTTP-`/healthz`. Wenn Ihre Plattform eine benötigt (Kubernetes-Readiness-Probes), siehe [Leitfäden: Kubernetes-Bereitstellung](/de/guides/kubernetes-deployment/) — Sie wickeln rousseau in einen kleinen `curl`-freundlichen Sidecar.

## Rollierender Neustart

Weil der Zustand eine einzige SQLite-Datei ist, ist der Daemon wirklich Single-Instance. Ein rollierender Neustart ist: stoppen, Image ersetzen, starten. Kein Warm-up erforderlich.

```sh
podman pull localhost/rousseau-agent:local     # or rebuild locally
systemctl --user restart rousseau-agent
podman logs -n 50 rousseau-agent | grep -E 'starting|connected'
```

Erwartete Log-Sequenz (aus `internal/transport/whatsapp/client.go`):

```
INFO whatsapp.starting store=… allowlist=1
INFO whatsapp.connected
```

Wenn der Daemon `whatsapp.connected` nicht innerhalb von ~15 Sekunden emittiert, zurückrollen.

## Mehrere Transporte auf einem Host

Sie möchten möglicherweise, dass sich denselben Session-Store zwischen WhatsApp und Slack teilen. Zwei Wege:

- **Mehrere Quadlet-Units** — eine für jeden Transport, jede auf denselben `state.path` zeigend. WAL + `busy_timeout` (siehe `Open()` in `internal/state/sqlite/store.go`) macht gleichzeitige Schreiber sicher.
- **Ein Binary, ein Transport pro Aufruf.** Die Transport-Befehle von rousseau sind Single-Transport (`whatsapp`, `slack`, `signal`, …). Um zwei Transporte zu betreiben, führen Sie zwei Prozesse aus.

## Zero-Downtime-Konfigurationsänderungen

Rousseau lädt `config.yaml` nicht hot. Konfigurationsänderungen erfordern einen Neustart. `SIGHUP` ist nicht für Reload verdrahtet.

Praktischer Workflow:

1. `~/.config/rousseau/config.yaml` bearbeiten.
2. `systemctl --user restart rousseau-agent`.
3. Aus den Logs verifizieren.

Für die meisten Transporte ist die Wiederverbindung schnell (~1–3 Sekunden). Die Hauptpause liegt bei WhatsApp, wo whatsmeow den Websocket neu etabliert.

## Log-Retention

Die `journald`-Retention wird durch `SystemMaxUse=` in `/etc/systemd/journald.conf` gesetzt. Für eine audit-freundliche Bereitstellung schiffen Sie Logs vom Host aus und setzen journald auf eine kürzere Retention auf der lokalen Disk (z. B. 7 Tage), damit der Audit-Trail in Loki/S3 lebt, nicht auf einem Dateisystem, das ein Eindringling rotieren könnte.

## Container-Image-Lebenszyklus

Bauen Sie das Image bei jedem rousseau-Release neu, den Sie übernehmen möchten:

```sh
cd ~/rousseau-agent
git pull
podman build -t rousseau-agent:local -f docker/Dockerfile .
systemctl --user restart rousseau-agent
```

Die Quadlet-Zeile `AutoUpdate=disabled` (in `docker/rousseau-agent.container`) verhindert, dass `podman auto-update` den Container berührt. Sie kontrollieren die Update-Kadenz.

## Verwandt

- [Bereitstellung](/de/deployment/) — die Referenz-Quadlet-Unit.
- [Tutorial: Auf einen VPS bereitstellen](/de/tutorials/deploy-to-a-vps/) — durchgearbeitetes Beispiel.
- [Leitfäden: Observability](/de/guides/observability/) — Log-Pipeline.
- [Leitfäden: Enterprise-Onboarding](/de/guides/enterprise-onboarding/) — vollständige Checkliste.
