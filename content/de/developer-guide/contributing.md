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
description: "Contribution guide for rousseau-agent: conventional commits, PR process, reviewer checklist, release cadence."
keywords: "contributing, conventional commits, pr process, reviewer checklist, release"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/developer-guide/contributing/"
subtitle: "PR process, standards, review checklist."
tags: "developer-guide, contributing"
title: "Mitwirken"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "contributing, conventional commits, pr process, reviewer checklist, release"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Mitwirken"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 66
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/contributing/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/contributing/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Mitwirken"
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
twitter_description: "Contribution guide for rousseau-agent: conventional commits, PR process, reviewer checklist, release cadence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Mitwirken"
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

## Grundregeln

Beiträge werden von eingeladenen Mitwirkenden akzeptiert. Jeder PR wird an demselben Maßstab gemessen: grüne CI, untenstehende Code-Standards, Reviewer-Zustimmung. Grüne CI ist notwendig, aber nicht hinreichend.

Die maßgebliche Quelle ist die [`CONTRIBUTING.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/CONTRIBUTING.md) im Repo-Stammverzeichnis. Diese Seite spiegelt sie in der Docs-Site-Stimme.

## Entwicklungsumgebung

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make setup      # installiert golangci-lint (v2) und govulncheck
make check      # vet + lint + Race-Tests + govulncheck
```

Jede Prüfung, die in der CI läuft, ist lokal über das Makefile verfügbar. Wenn eine Änderung `make check` besteht, wird sie auch die CI bestehen.

## Commit-Standards

- **Conventional Commits** — `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `ci:`, `perf:`.
- Betreffzeile ≤ 72 Zeichen. Der Body erklärt das **Warum**, nicht das Was. Verweisen Sie auf die treibende Entscheidung, das Issue oder den Vorfall.
- Ändern Sie keine veröffentlichten Commits. Erstellen Sie einen neuen Commit; der Reviewer bevorzugt eine Serie, die er per Bisect durchgehen kann.
- Signieren Sie Ihre Commits, wenn Sie Signierung konfiguriert haben. Derzeit nicht erforderlich, aber für Release-Tag-Commits empfohlen.

## Code-Standards

- Jeder exportierte Identifier hat einen godoc-Kommentar, der mit dem Identifier-Namen beginnt.
- Kein `interface{}` / `any` in exportierten APIs ohne schriftliche Rechtfertigung im Doc-Kommentar.
- `context.Context` propagiert durch jeden I/O-Pfad. Keine versteckten Globals oder Ambient-Logger; übergeben Sie `*slog.Logger` explizit.
- Fehler werden nach oben mit `fmt.Errorf("...: %w", err)` verpackt. Sentinel-Fehler kommen in die `errors.go` des Pakets. Bevorzugen Sie `errors.Is` / `errors.As` an Aufrufstellen gegenüber String-Matching.
- Keine Panics außerhalb von `main` und Test-Helpern. `Must*`-Varianten, die bei Operator-Fehlern paniken (doppelte Registrierung, ungültiges statisches Schema), sind mit dokumentierter Begründung erlaubt.
- Kein `fmt.Print*` in Bibliothekscode. Verwenden Sie `slog` oder ein TUI-Modell. Der `forbidigo`-Linter erzwingt dies.

## Teststandards

- Unit-Tests leben neben dem Code: `foo.go` → `foo_test.go`.
- Tabellengesteuerte Tests bevorzugt. Verwenden Sie `require` für stoppende Assertions, `assert` für nicht-stoppende.
- Schnittstellen-basierte Test-Injektion statt globaler Patches. Jedes Transport-Paket definiert eine schmale Schnittstelle (`WSConn`, `IMAPClient`, `HTTPClient`, `Sender`), die Tests mit Fakes erfüllen.
- Coverage-Ziel: 85 % für reine Business-Logic-Pakete; 75 % insgesamt.
- Race-sicher: `go test -race` muss bestehen. Neuer nebenläufiger Code benötigt einen Race-Test, wenn er nicht-triviale Synchronisation einführt.
- Fuzz-Funktionen für jeden Parser (`FuzzParseFoo` neben `parseFoo`). `make fuzz` führt das Korpus aus.

Siehe [Tests](/de/developer-guide/testing/) für das Injektionsmuster.

## Pull-Request-Prozess

1. Öffnen Sie den PR gegen `main`. Rebasen Sie (nicht mergen), wenn `main` sich unter Ihnen bewegt.
2. Jeder PR erfordert:
   - Eine Begründung in der Beschreibung (2–3 Sätze, die auf die zugrundeliegende Entscheidung verweisen).
   - Grüne CI: `vet`, `lint`, `test-race` auf Linux + macOS, `govulncheck`, `codeql`, `reproducible-build`, Coverage-Untergrenze.
   - Reviewer-Zustimmung.
3. Nur Squash-Merges. Die Merge-Commit-Nachricht ist die finale Commit-Nachricht und landet als eine atomare Änderung auf `main`.
4. Wenn der PR eine neue Abhängigkeit hinzufügt, notieren Sie die Begründung in der Beschreibung. Bevorzugen Sie die Standardbibliothek gegenüber einer neuen Abhängigkeit; bevorzugen Sie eine bestehende Abhängigkeit gegenüber einer neuen.

## Reviewer-Checkliste

Reviewer verifizieren in dieser Reihenfolge:

1. **Notwendigkeit.** Ist die Änderung erforderlich, oder fügt sie Abstraktion / Feature-Fläche ohne treibende Anforderung hinzu?
2. **Umfang.** Bleibt die Änderung im angegebenen Zweck, oder bündelt sie unzusammenhängende Aufräumarbeiten?
3. **Grenz-Integrität.** Respektiert die Änderung die `agent → concrete`-Abhängigkeitsrichtung? Siehe [Architektur](/de/developer-guide/architecture/).
4. **Test-Coverage.** Sind neue Code-Pfade abgedeckt? Werden Randfälle geprüft?
5. **Fehlerbehandlung.** Werden Fehler mit Kontext verpackt? Sind Aufräum-Pfade ehrlich (`_ =` mit einer `//nolint:errcheck`-Begründung, nicht stillschweigend geschluckt)?
6. **Godoc + Linter sauber.** Jedes exportierte Symbol dokumentiert; Lint-Ausgabe ist 0 Issues.
7. **Sicherheit.** Berührt die Änderung das `bash`-Tool, die Freigaberichtlinie, die Transport-Auth oder die Container-Haltung? Wenn ja, kennzeichnet die PR-Beschreibung dies?

## Dokumentationsbeiträge

Die Dokumentation lebt in einem separaten Repository. Wenn ein Code-PR benutzersichtbare Oberfläche berührt (ein neues Flag, ein neues Feld, ein neues Tool), muss derselbe PR – oder ein unmittelbarer Folge-PR im Docs-Repo – die betroffenen Seiten aktualisieren.

- **CLI-Änderung** → [Benutzerleitfaden: CLI](/de/user-guide/cli/) und [Referenz: CLI-Befehle](/de/reference/cli-commands/).
- **Konfigurationsänderung** → [Konfiguration](/de/configuration/) und [Referenz: Konfigurationsschema](/de/reference/config-schema/).
- **Neues Tool** → [Benutzerleitfaden: Tools](/de/user-guide/tools/).
- **Neuer Transport** → `content/transports/<name>.md`.
- **Neuer Provider** → `content/providers/<name>.md`.
- **Verhaltensänderung** → [Changelog](/de/changelog/).

## Release-Prozess

Releases werden von `main` geschnitten:

1. Changelog-Einträge aktualisieren.
2. Als `vX.Y.Z` auf den Release-Commit taggen.
3. Der `release`-Workflow baut über GoReleaser, generiert eine CycloneDX-SBOM, veröffentlicht eine cosign-Signatur der Prüfsummen und generiert SLSA-3-Provenienz.
4. Konsumenten verifizieren gemäß dem Rezept in [Sicherheit](/de/security/) und [Installation](/de/getting-started/installation/).

Rousseau folgt [Semantic Versioning](/de/getting-started/updating/): Patch behebt Bugs, Minor fügt nicht-brechend Features hinzu, Major bricht – immer mit einem Migrationsrezept.

## Governance

`rousseau-agent` ist ein Ein-Maintainer-Projekt. Entscheidungsbefugnis liegt beim in `go.mod` und `LICENSE` aufgeführten Maintainer of Record. Mitwirkende schlagen Richtungsänderungen über PR-Diskussion oder per E-Mail an `sebastian.rousseau@gmail.com` vor.

## Sicherheitsmeldungen

**Öffnen Sie kein öffentliches Issue für eine Sicherheitsmeldung.** E-Mail an `sebastian.rousseau@gmail.com` gemäß der [Sicherheitsrichtlinie](/de/security/). Bestätigung innerhalb von 72 Stunden.

## Weiter

- [Architektur](/de/developer-guide/architecture/) — die Karte, bevor Sie sie ändern.
- [Tests](/de/developer-guide/testing/) — das Muster, das der Reviewer erwartet.
- [Sicherheit](/de/security/) — der Meldeweg.
