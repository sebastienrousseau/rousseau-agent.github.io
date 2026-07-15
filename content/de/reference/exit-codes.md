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
changefreq: "monthly"
description: "Exit codes and signal semantics for the rousseau-agent binary. What init systems can rely on."
keywords: "exit codes, signals, sigterm, sigint, systemd, restart policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/reference/exit-codes/"
subtitle: "Exit codes and signal semantics."
tags: "reference, exit-codes, signals"
title: "Exit-Codes"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "exit codes, signals, sigterm, sigint, systemd, restart policy"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Exit-Codes"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 51
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/exit-codes/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/exit-codes/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Exit-Codes"
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
twitter_description: "Exit codes and signal semantics for the rousseau-agent binary. What init systems can rely on."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Exit-Codes"
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

## Exit-Codes

Die CLI von rousseau ist bewusst konservativ — zwei Exit-Codes decken jeden Pfad ab.

| Code | Emittiert von | Bedeutung |
|---|---|---|
| 0 | `cmd/rousseau/main.go` via `cli.Execute` | Befehl erfolgreich abgeschlossen. Daemons beenden sich mit 0 bei einem sanften Shutdown (SIGINT / SIGTERM). |
| 1 | `cmd/rousseau/main.go` via `cli.Execute` | Befehl fehlgeschlagen. Der Fehlerstring wird nach stderr ausgegeben. Jeder Fehler — Config-Parse-Fehler, Provider-Auth-Fehler, Transport-Panic, Tool-Verdrahtungsfehler — wird auf diesen Code abgebildet. |

`rousseau doctor` folgt derselben Konvention: Exit 0, wenn jeder Check passt, Exit 1, wenn irgendein Check `fail` ist. Warnungen und Info-Level-Zeilen beeinflussen den Exit-Code nicht.

Zukünftige Releases könnten Fehler in distinkte Codes aufteilen (Config vs. Runtime vs. Netzwerk). Behandeln Sie heute jeden Nicht-Null-Exit als wiederholbar, aber Log-Inspektion erforderlich.

## Signal-Handling

`cmd/rousseau/main.go` installiert einen Signalhandler, der den Root-`context.Context` bei `SIGINT` und `SIGTERM` abbricht. Jede langlebige Komponente (Agent-Schleife, Transport, Cron-Scheduler, MCP-Server) honoriert Context-Cancellation, sodass der Shutdown-Pfad wie folgt aussieht:

1. `SIGINT` / `SIGTERM` empfangen.
2. Root-Context wird abgebrochen.
3. Transporte rufen `Stop()` auf sich selbst auf und leeren in-flight-Nachrichten.
4. Cron-Scheduler nimmt keine neuen Feuerungen mehr an; laufende Feuerungen werden abgeschlossen.
5. `Close()` des Session-Stores wird via `defer` aufgerufen, was das WAL checkpointet.
6. `Execute` gibt 0 zurück.

`SIGKILL` kann nicht abgefangen werden. Wenn der Daemon mitten im Turn `kill -9`'d wird, schützt das WAL des Session-Stores vor Korruption, aber der in-flight-Turn wird nicht persistiert. Der nächste Start setzt am letzten gespeicherten Zustand fort.

## systemd-Restart-Policy

Für die Referenz-Quadlet-Unit:

```
[Service]
Restart=on-failure
RestartSec=10
```

`on-failure` startet bei jedem Nicht-Null-Exit neu; kombiniert mit der Exit-Code-Konvention von rousseau bedeutet dies: Exit 0 (`SIGTERM` von `systemctl stop`) startet nicht neu, Exit 1 tut es.

Für Daemons, die auf persistente Fehler stoßen (falsche Config, falsche Provider-Auth), wird `on-failure` thrashen. Beobachten Sie `journalctl` auf den Fehlergrund, bevor Sie annehmen, dass die Retry-Schleife sich erholt.

## Kubernetes-Probe-Semantik

Rousseau liefert konstruktionsbedingt keinen HTTP-Liveness/Readiness-Endpunkt. Kubernetes-Probes müssen entweder:

- `exec`-Probes sein, die `rousseau doctor --config /etc/rousseau/config.yaml` ausführen (gibt 0 bei gesund, 1 bei Fehler zurück), oder
- Abwesend sein, wobei sich der Pod auf `restartPolicy: Always` und die eigene Fehlerbehandlung des Daemons verlässt.

`rousseau doctor` ist günstig (~50 ms), also eine gute Liveness-Probe. Verwenden Sie es nicht als Readiness-Probe — ein `fail` auf `provider.claudecli.binary` sollte den Pod nicht aus der Rotation nehmen, wenn sich der Fehler nicht selbst heilt.

## Behandelte Fehler

Fehler, die über die CLI-Fehleroberfläche Exit-Code 1 produzieren, umfassen:

- **Config-Ladefehler** — YAML-Parse-Fehler, unbekanntes Feld, ungültiger Typ.
- **Provider-Auth-Fehler** — fehlender API-Schlüssel, ungültige Credentials, ungültige Bedrock- / Vertex-Region.
- **Transport-Startfehler** — fehlendes Token, nicht erreichbarer IMAP/SMTP-Host, whatsmeow-Protokollfehler.
- **Store-Open-Fehler** — Permission denied auf `~/.local/share/rousseau/`, Disk full.
- **Doctor-Check-Fehler** — jede `fail`-Zeile lässt doctor Exit 1 zurückgeben.
- **Cron-Cron-Ausdruck-Parse-Fehler** — `rousseau cron add` validiert vor dem Persistieren.

## Unbehandelte Panics

`go test -race` läuft bei jedem CI-Build, sodass Panics extrem selten sind. Wenn sie doch auftreten, gibt die Go-Runtime den Panic + Stack-Trace nach stderr aus und beendet sich mit einem Nicht-Null-Code aus der Runtime — typischerweise 2, aber dies ist die Konvention von Go und nichts, was rousseau kontrolliert.

Für die Produktion wickeln Sie den Daemon in einen Supervisor, der stderr bei abnormalem Exit erfasst und den Trace meldet.

## Weiter

- [Benutzerleitfaden: CLI](/de/user-guide/cli/) — jeder Befehl.
- [Leitfäden: Observability](/de/guides/observability/) — das slog-Signal über den Exit-Code hinaus sichtbar machen.
- [Fehlerbehebung](/de/troubleshooting/) — was zu tun ist, wenn der Exit-Code nicht ausreicht.
