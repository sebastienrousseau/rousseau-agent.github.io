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
description: "Install rousseau-agent from source, go install, or a cosign-verified release. Run rousseau chat and configure the first chat transport."
keywords: "install, quickstart, rousseau chat, cosign verify, go install, systemd, podman"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/getting-started/"
subtitle: "rousseau-agent installieren und den ersten Transport erreichen."
tags: "install, quickstart, getting-started"
title: "Erste Schritte"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "install, quickstart, rousseau chat, cosign verify, go install, systemd, podman"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Erste Schritte"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 2
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Erste Schritte"
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
twitter_description: "Install rousseau-agent from source, go install, or a cosign-verified release. Run rousseau chat and configure the first chat transport."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Erste Schritte"
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

## Für wen dies gedacht ist

- **Einzelne Entwickler**, die einen Coding-Assistenten wollen, der auf ihrem eigenen Laptop läuft und ihre bestehende `claude`-CLI ansteuert. Keine API-Schlüssel werden durch die Konfiguration von rousseau geführt, kein Cloud-Broker dazwischen.
- **Plattform-Operatoren**, die einen gemeinsamen Coding-Agenten für ein Team hinter einem Unternehmens-Perimeter betreiben. Rousseau ist ein einzelnes statisches Go-Binary in einem rootless Podman-Container mit abgelegten Capabilities — direkt neben jedem anderen systemd-Dienst bereitstellbar.
- **Sicherheitsprüfer**, die einen Agenten vor dem Rollout prüfen. SLSA-3-Provenienz, cosign-signierte Release-Checksummen, CycloneDX-SBOM, reproduzierbare Builds und jede Vertrauensgrenze sind in [Sicherheit](/de/security/) dokumentiert.

## Der schnellste Weg

1. **Wenn Sie die `claude`-CLI bereits installiert und authentifiziert haben,** ist der schnellste Start `rousseau chat` mit dem Standard-Provider `claudecli` — die Auth wird geerbt, keine Schlüssel zu verdrahten. Fahren Sie unten mit [Erster Start](#first-run) fort.
2. **Wenn Sie einen direkten API-Pfad mit Ihrem eigenen Schlüssel wollen,** setzen Sie `ANTHROPIC_API_KEY` und wechseln Sie zu `provider: anthropic` in `~/.config/rousseau/config.yaml`. Siehe [Anthropic-Provider](/de/providers/anthropic/).
3. **Wenn Sie in einem Unternehmen mit AWS Bedrock oder Google Vertex sind,** wählen Sie den passenden Provider — [Bedrock](/de/providers/bedrock/) verwendet die Standard-AWS-Credential-Chain; [Vertex](/de/providers/vertex/) liest ein Service-Account-JSON. Keine Geheimnisse liegen in der Konfigurationsdatei von rousseau.
4. **Wenn Sie air-gapped sind oder vollständig selbst gehostete Inferenz wollen,** richten Sie rousseau auf einen OpenAI-kompatiblen Endpunkt — Ollama, vLLM, LM Studio oder einen beliebigen Shim. Siehe [OpenAI-kompatibler Provider](/de/providers/openai-compatible/).

## Was Sie am Ende haben

- Ein `rousseau`-Binary in `$PATH`, verifiziert gegen eine cosign-Signatur (Release-Pfad) oder aus dem Quellcode gebaut (`make check` führt dieselben 18-Linter + race + govulncheck-Gates aus, die die CI erzwingt).
- Eine funktionierende `rousseau chat`-TUI mit dem von Ihnen gewählten Provider.
- Ein SQLite-Sitzungsspeicher unter `~/.local/share/rousseau/sessions.db` — jeder Turn wird persistiert, sitzungsübergreifender Recall via FTS5 ist verfügbar.
- Optional: ein Live-Chat-Transport (WhatsApp, Slack, Signal, ...) erreichbar von Ihrem Telefon.

## Lieber zuschauen?

Ein kurzer Screencast des Ablaufs ist auf der Roadmap. Bis dahin passt die gesamte Zeremonie auf diese Seite — die meisten Operatoren schließen dies in unter zehn Minuten ab.

## Systemanforderungen

| Anforderung | Version | Hinweise |
|---|---|---|
| Go-Toolchain | 1.26+ | `CGO_ENABLED=0`; das Binary ist vollständig statisch. |
| Container-Runtime | Podman 4.4+ | Referenzbereitstellung verwendet rootless Podman + eine systemd-Quadlet-Unit. Docker funktioniert, aber Quadlet ist Podman-spezifisch. |
| `claude`-CLI | latest | Nur wenn der Standard-Provider `claudecli` verwendet wird. |
| `signal-cli` | 0.13+ | Nur bei Verwendung des Signal-Transports. |
| BlueBubbles-Server | 1.9+ | Nur bei Verwendung des iMessage-Transports (macOS-Host erforderlich). |
| `whisper.cpp` | 1.5+ | Nur wenn Sie die WhatsApp-Sprachnachrichtentranskription aktivieren. |

## Installieren

### Aus dem Quellcode

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make build          # produces ./bin/rousseau
./bin/rousseau version
```

`make check` führt vet, `golangci-lint`, `go test -race` und `govulncheck` aus — dieselben Gates, die die CI erzwingt.

### Via `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

Das Binary bettet `modernc.org/sqlite` ein, daher gibt es zur Laufzeit keine libc- oder CGo-Abhängigkeit.

### Aus einem signierten Release

Jedes getaggte Release veröffentlicht ein Archiv mit Prüfsumme, eine CycloneDX-SBOM, ein SLSA-3-Provenienz-Attestat und eine cosign-Signatur der Prüfsummen-Datei. Verifizieren Sie immer vor der Ausführung:

```sh
cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature rousseau_<version>_checksums.txt.sig \
  rousseau_<version>_checksums.txt

sha256sum -c rousseau_<version>_checksums.txt
```

Die certificate-identity-Regex ist das, was die Signaturidentität festlegt; schwächen Sie sie nicht ab.

## Erster Start

### Terminal-Chat

```sh
rousseau chat
```

Bubble Tea TUI. Enter zum Senden, `Ctrl+C` zum Beenden. Der Standard-Provider ist `claudecli`, der die Authentifizierung von Ihrer lokalen Claude-Code-Installation erbt; keine API-Schlüssel werden durch die Konfiguration von rousseau geführt.

Der Sitzungsverlauf wird in `~/.local/share/rousseau/sessions.db` persistiert (SQLite mit WAL-Journaling und FTS5 für sitzungsübergreifenden Recall).

### Erster Chat-Transport

WhatsApp ist der Referenztransport (die Pairing-UX ist die strengste). Koppeln Sie beim ersten Start, indem Sie den QR-Code von Ihrem Telefon scannen:

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Die E.164-JID (`<digits>@s.whatsapp.net`) beschränkt die eingehende Behandlung; jeder andere Absender wird stillschweigend verworfen. Der Pairing-Zustand wird in `whatsapp.db` neben dem Sitzungsspeicher gespeichert.

Andere Transports folgen derselben Form:

```sh
rousseau slack   --app-token xapp-... --bot-token xoxb-...
rousseau discord --token bot-token
rousseau telegram --token 12345:ABC
rousseau matrix  --homeserver-url https://matrix.org --access-token ... --user-id @bot:matrix.org
```

Jedes `rousseau <transport> --help` listet seine Flags auf. Standardwerte kommen aus `~/.config/rousseau/config.yaml`.

## Wo der Zustand gespeichert wird

| Pfad | Zweck |
|---|---|
| `~/.config/rousseau/config.yaml` | Konfigurationsdatei auf Benutzerebene (Viper). |
| `~/.local/share/rousseau/sessions.db` | Sitzungen, Cron-Jobs, JID-Map, FTS5-Recall-Index. |
| `~/.local/share/rousseau/whatsapp.db` | Whatsmeow-Geräte-Credentials (getrennt gehalten, damit ein Geräte-Relink die Konversationen nicht berührt). |
| `~/.claude/` | OAuth-Tokens der `claude`-CLI, nur bei Verwendung des `claudecli`-Providers. |

## Nächste Schritte

- [Konzepte](/de/concepts/) — die Agent-Schleife, der Sitzungsspeicher, MCP, cron, Skills.
- [Konfiguration](/de/configuration/) — jeder Regler.
- [Bereitstellung](/de/deployment/) — wie man den Daemon unter systemd ausführt.
