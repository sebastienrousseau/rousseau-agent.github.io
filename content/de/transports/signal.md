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
description: "Set up rousseau-agent's Signal transport: signal-cli subprocess in JSON-RPC mode, account registration out-of-band, E.164 allowlist, extra_args knob."
keywords: "Signal, signal-cli, JSON-RPC, subprocess, E.164, account registration, linked device"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/transports/signal/"
subtitle: "signal-cli subprocess in JSON-RPC daemon mode."
tags: "transports, Signal"
title: "Signal-Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Signal, signal-cli, JSON-RPC, subprocess, E.164, account registration, linked device"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Signal-Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 13
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/signal/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/signal/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Signal-Transport"
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
twitter_description: "Set up rousseau-agent's Signal transport: signal-cli subprocess in JSON-RPC mode, account registration out-of-band, E.164 allowlist, extra_args knob."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Signal-Transport"
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

## Überblick

Der Signal-Transport (`internal/transport/signal/`) ruft `signal-cli` (https://github.com/AsamK/signal-cli) im JSON-RPC-Daemon-Modus als Subprozess auf.

`signal-cli --output=json -a <account> jsonRpc` streamt JSON-RPC 2.0 über stdin/stdout: ausgehende `send`-Anfragen stellen Nachrichten zu; eingehende Ereignisse treffen als `receive`-Notifications ein.

## Voraussetzungen

Zwei Dinge müssen vorhanden sein, bevor rousseau mit Signal kommunizieren kann:

1. **`signal-cli` in `$PATH`** (oder ein expliziter `binary`-Konfigurationswert).
2. **Konto out-of-band registriert bzw. verknüpft.**

Die Kontoregistrierung liegt bewusst außerhalb des Scopes von rousseau. Zwei unterstützte Wege (laut `signal-cli`-Dokumentation):

- **Neue Nummer registrieren.** `signal-cli register` startet eine SMS- oder Sprachverifizierung. Abschluss mit `signal-cli verify <code>`. Die Nummer gehört anschließend dem Daemon.
- **Als Zweitgerät verknüpfen.** `signal-cli link` gibt eine `tsdevice://`-URI aus; diese in der mobilen Signal-App unter **Einstellungen → Verknüpfte Geräte** scannen. Die Nummer bleibt beim Telefon, der Daemon agiert als Zweitgerät.

Beide Verfahren persistieren den Zustand unter `~/.local/share/signal-cli/`. Dieses Verzeichnis bei einer Podman-Bereitstellung per Bind-Mount in den Container einhängen.

## Konfiguration

```yaml
signal:
  binary: signal-cli
  account: "+447900123456"
  extra_args:
    - --verbose
  reply_header: "*Rousseau Agent*\n\n"
  allowlist:
    - "+447900654321"
```

| Feld | Standard | Wirkung |
|---|---|---|
| `binary` | `signal-cli` | Aufzurufende ausführbare Datei. |
| `account` | *erforderlich* | Rufnummer im E.164-Format, unter der der Daemon läuft. |
| `extra_args` | `[]` | Wird zwischen `-a <account>` und `jsonRpc` eingefügt. Nützlich für `--config <path>` und `--verbose`. |
| `reply_header` | *leer* | Wird jeder ausgehenden Antwort vorangestellt. |
| `allowlist` | `[]` | E.164-Rufnummern, deren Nachrichten verarbeitet werden. Leer akzeptiert jeden Absender. |

## Kommandozeile

```sh
rousseau signal --account +447900123456 --allow +447900654321
```

Die Flags entsprechen dem Konfigurationsblock. `--allow` kann mehrfach angegeben werden.

## Nachrichtenfluss

- **Eingehend.** `signal-cli` sendet pro eingehender Nachricht eine `receive`-JSON-RPC-Notification. rousseau parst sie, verwirft alles, was nicht in der Allowlist steht, und übergibt den Inhalt an den `Handler`.
- **Ausgehend.** rousseau schreibt eine JSON-RPC-`send`-Anfrage in `signal-cli`s stdin. Zustellungs-ACKs treffen auf demselben Kanal ein.

## Timeouts

Der Transport erzwingt kein eigenes Timeout gegenüber dem Subprozess. Die Netzwerkschicht von `signal-cli` verwaltet Reconnects zum Signal-Server selbst. Beendet sich der Prozess, startet rousseau ihn nicht neu — ein systemd-`Restart=on-failure` (bereits im Referenz-Quadlet gesetzt) startet den gesamten rousseau-Daemon neu und nimmt `signal-cli` dabei mit.

## Fehlerbilder

| Symptom | Behebung |
|---|---|
| `signal-cli` beendet sich sofort | Konto ist nicht registriert oder verknüpft. Registrierung out-of-band abschließen. |
| Es treffen nie `receive`-Notifications ein | Prüfen, ob das Konto an einer anderen Stelle verknüpft ist, die die Queue leert. |
| Fehler beim JSON-Parsing | `signal-cli`-Version 0.13+ sicherstellen. Ältere Versionen verwendeten einen anderen Envelope. |
