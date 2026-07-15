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
changefreq: "weekly"
description: "rousseau-agent's skills loader: Markdown + YAML frontmatter, discovery from skills_dir, trigger-based activation, composition into the system prompt."
keywords: "skills, agentskills.io, markdown, YAML frontmatter, triggers, system prompt, activation"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/skills/"
subtitle: "Zu agentskills.io kompatible Markdown-Skill-Dateien."
tags: "skills, reference"
title: "Skills"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "skills, agentskills.io, markdown, YAML frontmatter, triggers, system prompt, activation"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Skills"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 23
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/skills/index.html"
item_link: "https://docs.rousseau-agent.dev/skills/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Skills"
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
twitter_description: "rousseau-agent's skills loader: Markdown + YAML frontmatter, discovery from skills_dir, trigger-based activation, composition into the system prompt."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Skills"
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

## Skill-Format

Ein Skill ist eine Markdown-Datei mit optionalem YAML-Frontmatter-Header. Das Format lehnt sich bewusst eng an die Konvention von [agentskills.io](https://agentskills.io) an, damit Dateien zu anderen Werkzeugen portierbar sind.

Beispiel — `~/.local/share/rousseau/skills/git-rebase.md`:

```markdown
---
name: git-rebase
description: Guide the user through an interactive rebase safely.
triggers:
  - rebase
  - git rebase
  - squash
  - autosquash
---
When helping with a git rebase, first verify the current HEAD is
pushed to a remote branch. Prefer `git rebase -i --autosquash`
when the user has fixup commits. Never force-push to `main`.
```

## Frontmatter-Felder

| Feld | Typ | Wirkung |
|---|---|---|
| `name` | string | Muss `^[a-z][a-z0-9-]*$` entsprechen. Wird von `rousseau skills list` angezeigt. |
| `description` | string | Einzeilige Zusammenfassung. |
| `triggers` | `[]string` | Case-insensitive Teilstrings. Erscheint einer davon in der Benutzernachricht, aktiviert sich der Skill. Leer bedeutet, dass der Skill sich nie automatisch aktiviert. |

Alles nach dem schließenden `---` bildet den Skill-Body, wortwörtlich übernommen.

## Discovery

Der Loader durchsucht `agent.skills_dir` nach `*.md`-Dateien (nicht rekursiv). Ein fehlendes Verzeichnis ist kein Fehler — Load liefert `nil`. Unterverzeichnisse werden ignoriert.

```yaml
agent:
  skills_dir: ~/.local/share/rousseau/skills
```

## Aktivierung

In jedem Benutzer-Turn prüft `SkillsProvider.SystemAppendix(session)` die aktuellste Benutzernachricht und matcht die `triggers` jedes Skills (case-insensitive). Jeder Treffer wird (in Ladereihenfolge) konkateniert und in den System-Prompt dieses Turns eingefügt.

Skills mit leeren `triggers` aktivieren sich nie automatisch, können aber programmgesteuert von Aufrufern eingebunden werden, die die Bibliothek einbetten.

## CLI

```sh
# Entdeckte Skills auflisten.
rousseau skills list

# Inhalt eines einzelnen Skills anzeigen.
rousseau skills show git-rebase
```

## Design-Constraints

- **Keine Code-Ausführung.** Skills sind Strings. Sie können weder Skripte noch Shell-Befehle ausführen. Für Automatisierung stattdessen ein neues Tool über `Registry.Register` verdrahten.
- **Keine Versionierung.** rousseau verwaltet keine Skill-Versionen. Dies in Git abbilden — das `skills_dir` sollte eine Working Copy eines Repositorys sein.
- **Deterministisch.** Dieselbe Session + Benutzernachricht erzeugt denselben Anhang. Es ist kein LLM in der Schleife.

## Effektive Skills schreiben

- Body kurz halten (100–500 Wörter). Jede Aktivierung wird dem System-Prompt dieses Turns vorangestellt.
- Imperative Sätze bevorzugen ("Wenn der Benutzer nach X fragt, tue Y") statt Erläuterungen.
- `triggers` für hochpräzise Phrasen nutzen; breite Trigger ("code", "help") aktivieren sich fast jedes Turn und verdrängen andere Skills.
- In der TUI (`rousseau chat`) testen, bevor Sie den Skill in einen Chat-Transport-Daemon übernehmen — die Log-Zeile `agent.skills_activated` listet die ausgelösten Skills auf.
