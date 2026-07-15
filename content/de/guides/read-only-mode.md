---

# Front Matter (YAML)

author: "sebastian.rousseau@gmail.com (Sebastien Rousseau) "
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
description: "Configure rousseau-agent as a read-only inspection agent: deny_all approver with a read/grep exception, plan-mode claudecli, read-only bind mounts."
keywords: "read-only, inspection, deny_all, plan mode, bind mount, ro mount, audit"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/guides/read-only-mode/"
subtitle: "An inspection posture that cannot mutate the workspace."
tags: "guides, read-only, deny_all, plan-mode"
title: "Leitfaden: Read-only-Modus"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "read-only, inspection, deny_all, plan mode, bind mount, ro mount, audit"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: Read-only-Modus"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 36
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/read-only-mode/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/read-only-mode/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: Read-only-Modus"
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
twitter_description: "Configure rousseau-agent as a read-only inspection agent: deny_all approver with a read/grep exception, plan-mode claudecli, read-only bind mounts."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Leitfaden: Read-only-Modus"
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

## Szenario

Sie möchten, dass rousseau ein Repository inspiziert, Fragen dazu beantwortet und Berichte erstellt — aber es darf nichts schreiben, editieren oder destruktive Shell-Befehle ausführen. Dies ist die Haltung, die Sie für einen First-Pass-Audit, eine Incident-Response-Inspektion oder einen Compliance-Rundgang bereitstellen würden.

Drei Schichten stapeln sich, um das schwierig zu machen:

1. **Freigaberichtlinie** — jedes mutierende Tool ablehnen.
2. **`claudecli`-Berechtigungsmodus** — Claude Code in den `plan`-Modus versetzen, sodass sein eigener Approver keine Dateien editiert.
3. **Dateisystem** — den Workspace read-only bind-mounten.

Gürtel, Hosenträger und ein zweiter Gürtel. Jede der drei Schichten fällt sicher aus.

## Schicht 1 — Approver

Die einfachste Read-only-Haltung verwendet den `pattern`-Approver mit einer Whitelist:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "read-only inspection posture — this deployment cannot mutate files"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|find|wc|stat|file|which|pwd|env|git status|git diff|git log|git show|git branch)\\b"}
    # No deny rules needed — default: deny catches everything else.
    # No edit, write, or unrestricted bash — the model can't reach them.
```

Eine noch strengere Variante verwendet `deny_all`, was jedes Tool einschließlich `read` und `grep` blockiert:

```yaml
agent:
  approver:
    mode: deny_all
    reason: "smoke test — no tool calls allowed"
```

`deny_all` ist nur als Smoke-Test nützlich; das Modell wird keine sinnvolle Arbeit leisten können.

## Schicht 2 — `claudecli`-Berechtigungsmodus

Wenn der Provider `claudecli` ist, führt Claude Code selbst die Tool-Aufrufe aus. `permission_mode: plan` zu setzen bringt Claude Code dazu, jeden Schreib- oder Bearbeitungsaufruf in seiner eigenen Schicht zu verweigern, selbst wenn der rousseau-Approver ihn erlaubt hätte:

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: plan
```

Gültige Werte (siehe `internal/config/config.go` und die Dokumentation von Claude Code): `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. `plan` ist der einzige Wert, der Claude Code konsistent in einer Read-only-Haltung hält.

## Schicht 3 — Dateisystem

Mounten Sie den Workspace read-only. Unter dem Referenz-Podman-Quadlet:

```
Volume=%h/team-rousseau-workspace:/workspace:ro,Z
```

`ro` macht den Mount aus Container-Sicht read-only; selbst wenn ein kompromittiertes Binary versucht, mit `O_WRONLY` `open(2)` aufzurufen, würde der Kernel `EROFS` zurückgeben.

Unter Kubernetes:

```yaml
volumeMounts:
  - name: workspace
    mountPath: /workspace
    readOnly: true
```

Der Session-Store (`~/.local/share/rousseau/`) muss weiterhin beschreibbar sein — der Daemon hängt bei jedem Turn daran an. Halten Sie diesen Mount `rw` und lassen Sie nur den Workspace read-only.

## Dry-Run-Haltung

Es gibt kein `--dry-run`-Flag am Daemon. Wenn Sie möchten, dass das Modell Änderungen *plant*, ohne sie auszuführen, erreicht die obige Kombination das Äquivalent:

- Der Approver blockiert jedes mutierende Tool → das Modell erhält einen `tool_result`-Fehler, der die Blockade erklärt.
- Der `plan`-Modus in `claudecli` hält Claude Code davon ab, seine eigenen destruktiven Tools auszuführen.
- Read-only-Mounts stoppen alles, was durchsickert.

Das Modell antwortet typischerweise mit einem Plandokument statt mit einem Diff. Das ist das Deliverable einer Read-only-Inspektion.

## Was weiterhin funktioniert

- Jeder `read`- und `grep`-Aufruf.
- `bash` für sichere Lese-Utilities, die Sie enumeriert haben.
- Sitzungspersistenz — der SQLite-Store zeichnet die Konversation weiterhin auf.
- Cross-Session-Recall via FTS5, MCP-Export, Skills — alles ohnehin read-only.

## Was (absichtlich) bricht

- `write` und `edit` — deny.
- Shell-Mutationsbefehle — deny.
- Cron-Jobs, deren Prompt Dateischreibvorgänge impliziert — das Modell versucht es, wird abgelehnt, antwortet mit einem Plan.
- `rousseau init` — die CLI ist vom Approver nicht betroffen, aber sie schreibt in `~/.config/rousseau/` außerhalb des Workspace. Führen Sie sie aus, bevor Sie den Read-only-Modus ausrollen.

## Die Haltung testen

```sh
rousseau chat
> Edit /workspace/README.md to add a footer.
```

Erwartete Log-Zeile:

```
WARN tool.denied name=edit reason="read-only inspection posture — this deployment cannot mutate files"
```

Erwartete Chat-Antwort: Das Modell entschuldigt sich, produziert einen Plan oder einen Diff-Patch als Text und bittet den Operator, ihn anzuwenden.

Für die `deny_all`-Variante wird jeder Tool-Aufruf blockiert — das Modell hat keine Möglichkeit, irgendetwas zu inspizieren, sodass diese Haltung nur als Smoke-Test nützlich ist.

## Schichtung mit anderen Transporten

Dieselben drei Schichten gelten für WhatsApp, Slack, Discord und jeden anderen Transport. Da der Approver innerhalb der Agent-Schleife läuft, kümmert es ihn nicht, welcher Transport den Nutzer-Turn geliefert hat. Ein Read-only-Slack-Agent ist einen `mode: pattern`-Block entfernt.

## Vorbehalte

- Die Read-only-Haltung wird vom Approver von rousseau und vom Dateisystem durchgesetzt — **nicht** vom LLM. Ein Modell kann weiterhin einen `edit`-Tool-Aufruf emittieren; der Approver blockiert ihn stillschweigend, aber der Versuch wird als `tool.denied` protokolliert. Das ist beabsichtigt, damit Audit-Trails aufzeichnen, was das Modell versucht hat, nicht nur was Erfolg hatte.
- Read-only-Bind-Mounts schützen nicht gegen Symlinks, die außerhalb des Mounts zeigen. Die Referenz-Podman-Haltung entzieht alle Capabilities, was die meisten Ausbruchswege verhindert, aber verlassen Sie sich nicht allein auf den Mount.
- Der `plan`-Modus des `claudecli`-Providers ist der Vertrag von Claude Code, nicht der von rousseau. Wenn Claude Code seine Permission-Mode-Semantik ändert, erbt die Read-only-Haltung von rousseau diese Änderung.

## Weiter

- [Benutzerleitfaden: Freigaberichtlinien](/de/user-guide/approval-policies/) — tiefere Referenz.
- [Audit + Freigaberichtlinien](/de/guides/audit-approval-policies/) — das mutierende Gegenstück.
- [Bereitstellung](/de/deployment/) — Mount- und Container-Flags.
