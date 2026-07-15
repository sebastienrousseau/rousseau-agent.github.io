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
description: "How rousseau's write and edit tools interact with the workspace bind mount, SELinux :Z labels, container UID mapping, and safe editing outside /workspace."
keywords: "workspace, bind mount, SELinux, :Z, UserNS, write, edit, permissions"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/guides/file-management/"
subtitle: "Workspace bind mount, SELinux :Z, UID mapping, and safe file edits."
tags: "guides, files, container, selinux, workspace"
title: "Leitfaden: Dateiverwaltung"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "workspace, bind mount, SELinux, :Z, UserNS, write, edit, permissions"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: Dateiverwaltung"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 37
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/file-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/file-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: Dateiverwaltung"
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
twitter_description: "How rousseau's write and edit tools interact with the workspace bind mount, SELinux :Z labels, container UID mapping, and safe editing outside /workspace."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Leitfaden: Dateiverwaltung"
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

## Die zwei Tools

Zwei Tools mutieren das Dateisystem:

- [`write`](/de/reference/tool-schemas/#write) — Vollständiges Datei-Überschreiben. `internal/tools/builtin/write.go` schreibt mit Modus `0o644` und `MkdirAll(dir, 0o755)`.
- [`edit`](/de/reference/tool-schemas/#edit) — Einzelne Exact-String-Ersetzung innerhalb einer existierenden Datei. `internal/tools/builtin/edit.go`.

Beide benötigen einen **absoluten Pfad** (sie rufen `filepath.IsAbs`). Beide führen keinen atomaren Swap-Tanz aus — sie verwenden direkt `os.WriteFile`.

## Die Container-Sicht der Welt

Die Referenz-Quadlet-Unit unter `docker/rousseau-agent.container` mountet drei Host-Verzeichnisse in den Container:

```
Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
Volume=%h/.claude:/home/rousseau/.claude:rw,Z
Volume=%h/team-rousseau-workspace:/workspace:rw,Z
```

Nichts anderes auf dem Host ist sichtbar. Aus dem Container heraus löst ein `edit`-Tool-Aufruf gegen `/workspace/repos/foo/main.go` auf `~/team-rousseau-workspace/repos/foo/main.go` auf dem Host auf.

### `:Z` — das SELinux-Label

Das `:Z`-Flag an jedem `Volume=` weist Podman an, den Mount mit einer **Container-privaten** SELinux-MCS-Kategorie neu zu labeln. Ohne dies, auf einem System mit SELinux im Enforcing-Modus:

- Lesevorgänge funktionieren die meiste Zeit noch (`container_file_t` ist breit lesbar).
- Schreibvorgänge scheitern mit `EACCES` und `avc: denied { write }` im Audit-Log.

Wenn Sie das Flag durch `:z` (Kleinbuchstabe) ersetzen, labelt Podman mit einer **geteilten** Kategorie neu — sicherer für Hosts, die Sie zwischen mehreren Container-Nutzern teilen, aber nicht der Standard.

Auf Systemen ohne SELinux (Debian, nicht gehärtetes Ubuntu) ist `:Z` ein stilles No-Op.

### `UserNS=keep-id` — UID-Mapping

Der Container läuft als UID/GID 1000. Ohne User-Namespace-Mapping würde rootless Podman 1000 in den subuid-Bereich (typischerweise `100000+`) remappen, und aus dem Container heraus geschriebene Dateien würden auf dem Host der gemappten UID gehören — für den Operator unbrauchbar.

`UserNS=keep-id` mappt Container-UID 1000 auf die UID des Host-Nutzers (im Referenz-Setup ebenfalls 1000). In `/workspace` geschriebene Dateien enden auf dem Host im Besitz von `seb:seb` — genau, was Sie möchten.

Wenn Ihr Host-Nutzer nicht UID 1000 ist, funktioniert das Mapping dennoch; `keep-id` verwendet die tatsächliche UID des aufrufenden Nutzers.

## Außerhalb von `/workspace` editieren

Da die Bind-Mounts die einzige Sicht des Containers auf das Host-Dateisystem sind, wird `write` oder `edit` gegen `/etc/nginx/nginx.conf` mit einem „Pfad nicht gefunden"-Fehler scheitern — der Pfad existiert im Container schlicht nicht. Das ist ein **Feature**: Die Approver-Richtlinie des Operators kann der Container-Grenze vertrauen.

Wenn Sie den Daemon wirklich einen anderen Host-Pfad berühren lassen müssen:

1. **Bevorzugt:** Fügen Sie eine neue `Volume=`-Zeile zur Quadlet-Unit hinzu. Wählen Sie die am wenigsten permissive Variante: `:ro` für read-only, `:Z` für privates SELinux-Labelling.
2. **Führen Sie** rousseau **nicht** außerhalb des Containers aus, um die Grenze zu umgehen — Sie verlieren seccomp, Drop-Caps und das Read-only-Root-Dateisystem.

## Außerhalb des Containers editieren

Wenn Sie rousseau direkt auf dem Host betreiben (kein Container), operieren die Tools gegen die Prozess-Sicht des Daemons — standardmäßig alles unter dem HOME des Nutzers. Der Approver ist die einzige Einschließungsschicht. Siehe [Leitfäden: Audit + Freigaberichtlinien](/de/guides/audit-approval-policies/) für das Pattern-Modus- + `default: deny`-Rezept.

## `write` vs. `edit` — wann welches verwenden

| Situation | Verwenden |
|---|---|
| Neue Datei erstellen. | `write`. |
| Datei vollständig neu schreiben. | `write`. |
| Einen Abschnitt einer großen Datei ändern. | `edit`. Scheitert sicher, wenn `old_string` nicht eindeutig ist. |
| Ein Symbol dateiübergreifend umbenennen. | Mehrere `edit`-Aufrufe mit progressiv mehr Umgebungskontext oder ein einzelnes `write` mit dem vollständig umgeschriebenen Inhalt. Verwenden Sie `edit` nicht mit `replace_all`-artiger Semantik — das Tool weigert sich. |

Die Exact-Uniqueness-Einschränkung von `edit` ist beabsichtigt. Sie ist direkt aus dem Edit-Tool von Claude Code entlehnt. Suchen Sie in `internal/tools/builtin/edit.go` nach dem Kommentarblock, der erklärt, warum.

## Häufige Fehlermodi

| Symptom | Ursache | Behebung |
|---|---|---|
| `edit: path must be absolute, got "…"` | Modell hat einen relativen Pfad übergeben. | Im Approver ablehnen oder umschreiben; das Modell bitten, absolute Pfade zu verwenden. |
| `edit: old_string not found in …` | Die Datei hat sich geändert, seit das Modell zuletzt gelesen hat, oder das Modell hat den Umgebungskontext halluziniert. | Das Modell wird typischerweise erneut lesen und wiederholen. |
| `edit: old_string is not unique in … (found 3 occurrences)` | Derselbe String erscheint mehrfach. | Das Modell muss mehr Umgebungszeilen liefern, um zu disambiguieren. |
| `write: permission denied` | SELinux-Label-Missmatch oder falsches UID-Mapping. | Verifizieren Sie `:Z` am Volume und `UserNS=keep-id` am Container. |
| `read: does not look like UTF-8 text` | Datei enthält NUL-Bytes in den ersten 512 Bytes (`isLikelyText` in `read.go`). | Binärlesungen auf Approver-Ebene ablehnen; verwenden Sie das `bash`-Tool mit `file`, wenn Identifikation nötig ist. |

## Backups vor großen Umschreibungen

Die Tools erstellen keine `.bak`-Kopien. Für risikoreiche Änderungen bringen Sie dem Modell bei, zuerst in einen Nachbarpfad zu schreiben, mit `bash` zu diffen und dann zu tauschen. Alternativ führen Sie alles durch einen git-Branch — rousseau lässt `git` komplett aus seinem Ausführungspfad heraus, sodass jede Versionierung über Ihren normalen Workflow läuft.

## Verwandt

- [Referenz: Tool-Schemata](/de/reference/tool-schemas/) — genaue Input-Schemata.
- [Benutzerleitfaden: Tools](/de/user-guide/tools/).
- [Bereitstellung](/de/deployment/) — die Quadlet-Unit, die die Bind-Mounts definiert.
- [Leitfäden: Audit + Freigaberichtlinien](/de/guides/audit-approval-policies/) — Schreibvorgänge an einen Verzeichnisbaum binden.
