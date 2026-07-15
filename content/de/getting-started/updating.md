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
description: "How to update rousseau-agent: go install refresh, container tag rollover, config migration between minor versions, session-store compatibility policy."
keywords: "update, upgrade, go install, container tag, config migration, minor version"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/getting-started/updating/"
subtitle: "Move between versions without losing sessions or bricking the daemon."
tags: "update, upgrade, migration"
title: "Aktualisieren"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "update, upgrade, go install, container tag, config migration, minor version"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Aktualisieren"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 24
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/updating/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/updating/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Aktualisieren"
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
twitter_description: "How to update rousseau-agent: go install refresh, container tag rollover, config migration between minor versions, session-store compatibility policy."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Aktualisieren"
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

## Versionierungsrichtlinie

Rousseau folgt [Semantic Versioning](https://semver.org):

| Sprung | Was sich ändert |
|---|---|
| Patch (`0.1.2 → 0.1.3`) | Bugfixes, Sicherheits-Fixes, Dependency-Bumps. Keine Änderungen an Konfiguration oder On-Disk-Format. |
| Minor (`0.1.x → 0.2.0`) | Neue Features. Konfigurations-Erweiterungen sind immer nicht-brechend; wenn ein Feld entfernt wird, deckt ein Alias-Fallback mindestens eine Minor-Version ab. |
| Major (`0.x → 1.0`) | Breaking Changes. Erfordert ein dokumentiertes Migrationsrezept im [Changelog](/de/changelog/). |

Die [SECURITY.md-Richtlinie](https://github.com/sebastienrousseau/rousseau-agent/blob/main/SECURITY.md) ist explizit: Nur `main` und das aktuellste getaggte Release erhalten Sicherheits-Fixes. Es gibt keinen Long-Term-Support-Branch.

## Update-Methode nach Installationspfad

### Signiertes Release-Archiv

```sh
VERSION=<new-tag>
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_linux_amd64.tar.gz"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt.sig"

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature "rousseau_${VERSION}_checksums.txt.sig" \
  "rousseau_${VERSION}_checksums.txt"

sha256sum -c "rousseau_${VERSION}_checksums.txt" --ignore-missing
tar -xzf "rousseau_${VERSION}_linux_amd64.tar.gz"
sudo install -m 0755 rousseau /usr/local/bin/rousseau
rousseau version
```

Verifikation ist nicht optional. Jedes Release liefert eine frische cosign-Signatur; die Prüfung zu überspringen hebelt die Lieferketten-Haltung aus.

### `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

Um ein exaktes Tag zu pinnen:

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@v0.4.2
```

`$GOBIN` (typischerweise `~/go/bin`) muss in `$PATH` vor `/usr/local/bin` stehen, wenn das frische Binary Vorrang haben soll.

### Container-Image

Rollen Sie das Tag der Image-Referenz und starten Sie den systemd-Dienst neu. Wenn Sie die Referenz-Quadlet-Unit verwenden:

```sh
sed -i "s#Image=ghcr.io/sebastienrousseau/rousseau-agent:.*#Image=ghcr.io/sebastienrousseau/rousseau-agent:<new-tag>#" \
  ~/.config/containers/systemd/rousseau-agent.container
systemctl --user daemon-reload
systemctl --user restart rousseau-agent.service
journalctl --user -u rousseau-agent.service -f
```

Auf `:latest` zu pinnen ist in einer lieferkettenbewussten Bereitstellung unsicher – pinnen Sie immer ein unveränderliches Tag (`:v0.4.2`) und verifizieren Sie den Image-Digest gegen die Release-Notes.

### Aus dem Quellcode

```sh
cd rousseau-agent
git fetch --tags
git checkout <new-tag>
make check          # führt das vollständige CI-Gate lokal aus
make build
sudo install -m 0755 bin/rousseau /usr/local/bin/rousseau
```

`make check` ist dasselbe 18-Linter- + race- + govulncheck-Gate, das die CI erzwingt – ein bestandener lokaler Lauf garantiert, dass auch der Reproducible-Build-Job bestehen wird.

## Konfigurationsmigration

Änderungen am Konfigurationsschema werden für jede Minor-Version im [Changelog](/de/changelog/) dokumentiert. Die Viper-Defaults halten alte Schlüssel über einen Minor-Zyklus lauffähig; das folgende Muster gilt:

- **Neuer Schlüssel hinzugefügt**: erhält einen Standardwert, der das vorherige Verhalten bewahrt. Keine Aktion erforderlich.
- **Schlüssel umbenannt**: Der alte Schlüssel wird für einen Minor als Alias geführt. Eine Warnung wird protokolliert, wenn der Alias getroffen wird.
- **Schlüssel entfernt**: Ein Fail-fast-Fehler wird zur Ladezeit ausgegeben. Das Changelog nennt den Ersatz.

Um eine Konfiguration mit einem neuen Binary im Trockenlauf zu prüfen:

```sh
rousseau doctor --config ~/.config/rousseau/config.yaml
```

`rousseau doctor` geht jede Laufzeit-Abhängigkeit und jede Konfigurationswahl durch; eine `fail`-Zeile zeigt genau, welcher Schlüssel Aufmerksamkeit benötigt.

## Sitzungsspeicher-Kompatibilität

`~/.local/share/rousseau/sessions.db` verwendet SQLite mit einem versionierten Schema. Schema-Migrationen sind additiv und idempotent – der Daemon führt beim Start `CREATE TABLE IF NOT EXISTS` und `ALTER TABLE ADD COLUMN` aus. **Führen Sie niemals ein Downgrade** über eine Minor-Version hinweg durch, sobald das neue Schema gelaufen ist; SQLite entfernt Spalten nicht automatisch, aber der Anwendungscode setzt deren Vorhandensein voraus.

Wenn Sie einen sauberen Neustart benötigen:

```sh
mv ~/.local/share/rousseau/sessions.db ~/.local/share/rousseau/sessions.db.bak
```

Der Daemon erstellt den Speicher beim nächsten Start neu. WhatsApp-Gerätedaten werden separat in `whatsapp.db` gespeichert, sodass ein Reset des Sitzungsspeichers keine erneute Kopplung erzwingt.

## WhatsApp-Store-Kompatibilität

`whatsapp.db` (whatsmeows Gerätespeicher) ist vom Sitzungsspeicher getrennt, gerade damit eine Sitzungsschema-Migration die WhatsApp-Kopplung nicht kaputtmachen kann. Wenn whatsmeow selbst das On-Disk-Format über ein rousseau-Upgrade hinweg ändert, wird das Changelog dies markieren, und der Wiederherstellungspfad ist: `whatsapp.db` löschen, neu starten, den QR-Code erneut scannen.

## Rollback

- **Signiertes Release-Archiv / `go install`**: Installieren Sie das vorherige Tag mit demselben Rezept neu.
- **Container**: Ändern Sie das Image-Tag zurück und starten Sie neu.
- **Aus dem Quellcode**: `git checkout <old-tag> && make build`.

Rollbacks sind sicher, solange das Sitzungsspeicher-Schema der älteren Version eine Obermenge dessen ist, was die neuere Version geschrieben hat. In der Praxis stimmt dies innerhalb einer einzelnen Minor-Serie immer und über benachbarte Minors hinweg meist. Major-Upgrades liefern ein Migrationsrezept mit einem expliziten Rollback-Disclaimer im Changelog.

## Weiter

- [Changelog](/de/changelog/) — Aufschlüsselung Release für Release.
- [Fehlerbehebung](/de/troubleshooting/) — wenn `rousseau doctor` eine `fail`-Zeile ausgibt.
