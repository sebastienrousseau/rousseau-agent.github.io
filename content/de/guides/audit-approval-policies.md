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
description: "Worked example: lock down the bash tool with a pattern-mode approver, deny rules on destructive commands, and slog-driven audit trail."
keywords: "approval policy, pattern mode, bash tool, deny rules, audit trail, slog"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/guides/audit-approval-policies/"
subtitle: "Pattern-mode approver with deny rules on the bash tool."
tags: "guides, audit, approval, pattern-mode, bash, deny"
title: "Leitfaden: Audit + Genehmigungsrichtlinien"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approval policy, pattern mode, bash tool, deny rules, audit trail, slog"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: Audit + Genehmigungsrichtlinien"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 34
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/audit-approval-policies/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/audit-approval-policies/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: Audit + Genehmigungsrichtlinien"
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
twitter_description: "Worked example: lock down the bash tool with a pattern-mode approver, deny rules on destructive commands, and slog-driven audit trail."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Leitfaden: Audit + Genehmigungsrichtlinien"
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

## Das Problem

Ein unbeaufsichtigter Chat-Transport-Daemon hat keinen Menschen am Terminal, der Tool-Aufrufe in Echtzeit freigibt. Wenn das Modell `rm -rf /workspace/*` ausführen will, muss etwas es aufhalten. Der `pattern`-Modus-Approver von rousseau ist dieser Hebel.

Die Bedrohung ist nicht das Modell, das Amok läuft — es ist eine kompromittierte oder fehlausgerichtete Instruktion, die über den Transportkanal den Daemon erreicht. Eine Pattern-Modus-Richtlinie mit einem `default: deny`-Fallback macht das Risiko beschränkt und auditierbar.

## Approver-Modi

Drei eingebaute Modi sind enthalten (siehe `internal/agent/approver.go`):

| Modus | Verhalten | Wann verwenden |
|---|---|---|
| `allow_all` | Jeder Tool-Aufruf läuft. | Interaktiver `rousseau chat`, in dem der `claudecli`-Provider seine eigenen Freigaben durchführt. |
| `deny_all` | Jeder Tool-Aufruf wird blockiert. Ablehnungsgründe werden dem Modell als `tool_result`-Fehler zurückgemeldet, sodass es sich anpassen kann. | Read-only-Inspektionshaltung; Smoke-Tests. |
| `pattern` | Regex-Allow/Deny-Regeln je Tool. **Deny gewinnt gegen Allow.** Nicht getroffene Anfragen fallen auf `default` zurück. | Jeder unbeaufsichtigte Daemon in Produktion. |

## Durchgearbeitete Konfiguration

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by pattern policy — ask the operator"
    allow:
      # Read-side tools: no restriction inside the workspace.
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

      # Edit inside /workspace only.
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}

      # Write inside /workspace only.
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}

      # Shell commands: whitelist of safe read-side utilities plus git status/diff.
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|grep|rg|find|wc|stat|file|which|pwd|env|git status|git diff|git log|go test|go vet|go build)\\b"}

    deny:
      # Absolute deny rules override any allow above.
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s|ncat"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}   # fork bomb
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit, match: "\"path\":\"/etc/|/root/|/var/"}
```

Zwei wichtige Eigenschaften folgen aus `PatternApprover.Approve`:

1. **Deny gewinnt.** Jede Deny-Regel wird vor jeder Allow-Regel geprüft. Das ist sicherer als umgekehrt: Ein Operator, der ein breites Allow hinzufügt, kann niemals versehentlich eine Kategorie freischalten, die er als abgelehnt betrachtete.
2. **Nicht getroffen → deny.** Mit `default: deny` wird jeder Tool-Aufruf, den der Operator zu enumerieren vergaß, blockiert. Dies ist die sichere Standardhaltung; wollen Sie das Gegenteil, setzen Sie `default: allow`.

## Den Audit-Trail lesen

Jeder Tool-Aufruf und jede Ablehnung wird über den slog-Logger emittiert:

```
INFO tool.execute name=read id=t_1
INFO tool.execute name=grep id=t_2
WARN tool.denied  name=bash reason="denied by pattern policy — ask the operator"
```

Der Daemon verwendet `slog` mit konfigurierbarem Level und Format (`log.level`, `log.format`). Für Produktion bevorzugen Sie `format: json`, damit nachgelagerte Tools (Loki, Vector, Datadog) sauber parsen. Siehe [Leitfäden: Observability](/de/guides/observability/) für das Pipeline-Rezept.

Jede Ablehnung trägt einen stabilen strukturierten Schlüssel:

- `tool.denied` — der Tool-Aufruf wurde blockiert. Felder: `name` (Tool-Bezeichner), `reason` (aus `PatternApprover.DenyReason` oder dem eingebauten Fallback).
- `tool.execute` — der Tool-Aufruf lief. Felder: `name`, `id` (die vom Modell emittierte Aufruf-ID zur Korrelation).
- `tool.error` — das Tool lief, schlug aber fehl. Felder: `name`, `err`.

Ein `slog`-Filter auf `tool.denied` liefert Ihnen die Audit-Sicht „blockierte Versuche", nach der die meisten Compliance-Frameworks fragen.

## Die Richtlinie testen

`internal/agent/approver_test.go` im Source-Baum durchläuft den `PatternApprover` mit einer breiten Matrix. Um Ihre eigenen Regeln zu smoke-testen:

```sh
rousseau chat
> Run `rm -rf /tmp/foo` for me.
```

Das Modell wird den `bash`-Tool-Aufruf versuchen. Der Daemon protokolliert `tool.denied` und gibt den `reason`-String an das Modell zurück, das meist umschwenkt („I can't run that — could you tell me what you were trying to do?").

Für die Referenz-Testmatrix siehe `internal/agent/approver_test.go` — dort werden dieselben Regelformen exerziert.

## Manuellen Override hinzufügen

Manchmal möchte ein Operator einen einzelnen gefährlichen Aufruf manuell freigeben. Das einfachste Muster:

1. Setzen Sie `mode: allow_all` in `rousseau chat` (interaktives TUI). Der `claudecli`-Provider handhabt seine eigenen Per-Call-Freigabe-Prompts.
2. Behalten Sie `mode: pattern` in jedem unbeaufsichtigten Daemon.

Es gibt heute keine interaktive Per-Call-Freigabe-UI auf den Chat-Transporten — die Sicherheitsgeschichte ist vollständig Regex + slog.

## Was die Richtlinie nicht tut

- **Sandboxt das Tool nicht.** Ein `bash`-Aufruf, der den Approver überlebt, läuft mit der UID des Daemons und dessen Dateisystem-Sichtbarkeit. Legen Sie einen rootless Container ([Bereitstellung](/de/deployment/)) darunter.
- **Rate-Limiting entfällt.** Zehn erlaubte `bash`-Aufrufe pro Sekunde sind zulässig. Wenn Sie Rate-Limiting brauchen, wickeln Sie die Tool-Registry.
- **Auditiert keine ausgehenden Netzwerkaufrufe.** Wenn ein `bash`-Aufruf etwas nach draußen curlt, sieht der Approver die URL nicht — nur den initialen `bash`-`command`-String. Verbieten Sie `curl` und `wget` direkt auf Pattern-Ebene.

## Gebräuchliche Muster

### Editieren auf einen Verzeichnisbaum sperren

```yaml
allow:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/[^\"]*\""}
  - {tool: write, match: "\"path\":\"/workspace/repo/[^\"]*\""}
deny:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/(\\.git|node_modules|vendor)/"}
```

### Read-only-Auditor

```yaml
mode: pattern
default: deny
allow:
  - {tool: read, match: ".*"}
  - {tool: grep, match: ".*"}
```

Kombiniert mit `provider.claudecli.permission_mode: plan` ergibt dies eine Read-only-Inspektionshaltung — siehe [Leitfäden: Read-only-Modus](/de/guides/read-only-mode/).

### Git-first-Workflows

```yaml
allow:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"git (status|diff|log|show|branch|stash|fetch|pull --ff-only)\\b"}
deny:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"git (push|reset --hard|clean -fd|checkout --)\\b"}
```

## Fünf Referenz-Regelsätze

<div class="tabs" data-tabs="approval-rulesets">
  <div class="tab-list" role="tablist" aria-label="Reference ruleset">
    <button role="tab" aria-selected="true">Dev-Laptop</button>
    <button role="tab" aria-selected="false">Staging</button>
    <button role="tab" aria-selected="false">Produktion</button>
    <button role="tab" aria-selected="false">Oncall-Bot</button>
    <button role="tab" aria-selected="false">Read-only</button>
  </div>
  <div class="tab-panel" role="tabpanel">

**Dev-Laptop.** Permissiv per Default, wirklich Gefährliches ablehnen. Setzt ein beaufsichtigtes Terminal voraus.

```yaml
agent:
  approver:
    mode: pattern
    default: allow
    deny:
      - {tool: bash, match: "rm\\s+-rf\\s+/"}
      - {tool: bash, match: "sudo(?!\\s+-n)"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}
      - {tool: write, match: "\"path\":\"/etc/|/root/"}
      - {tool: edit, match: "\"path\":\"/etc/|/root/"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Staging.** Explizite Allowlist für den Workspace, alles außerhalb ablehnen. Geeignet für einen geteilten Staging-Daemon mit begrenztem Blast-Radius.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by staging policy — ping #platform for exceptions"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: bash, match: "^\\{\"command\":\"git (status|diff|log|show|branch|fetch|pull --ff-only)\\b"}
      - {tool: bash, match: "^\\{\"command\":\"(ls|cat|grep|rg|find)\\s"}
    deny:
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s"}
      - {tool: edit, match: "\"path\":\"/workspace/(\\.git|node_modules|vendor)/"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Produktion.** Deny-first. Jeder erlaubte Befehl ist explizit enumeriert. Geeignet für einen Produktions-Daemon, der kundenzugewandte Fragen beantwortet.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by production policy — this daemon is read-mostly"
    allow:
      - {tool: read, match: "\"path\":\"/workspace/(runbooks|docs|src)/"}
      - {tool: grep, match: "\"path\":\"/workspace/(runbooks|docs|src)/"}
      - {tool: bash, match: "^\\{\"command\":\"(ls|cat|rg)\\s"}
    deny:
      # Layered denies just in case.
      - {tool: write, match: ".*"}
      - {tool: edit, match: ".*"}
      - {tool: bash, match: "\\b(rm|mv|cp|dd|mkfs|kill|killall)\\b"}
      - {tool: bash, match: "\\b(curl|wget|nc|ncat|ssh|scp|rsync)\\b"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Oncall-Bot.** Kann Monitoring abfragen, Logs verfolgen, aber keine Dienste neu starten oder Code editieren. Geeignet für einen Slack-orientierten Incident-Response-Helfer.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied — oncall bot can query, not mutate"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: bash, match: "^\\{\"command\":\"(kubectl|helm|argocd) (get|describe|logs|top|status)\\b"}
      - {tool: bash, match: "^\\{\"command\":\"(curl|http|wget) -[gsL]* https?://monitoring\\."}
      - {tool: bash, match: "^\\{\"command\":\"(pg_dump|psql -c 'SELECT|redis-cli GET)\\b"}
    deny:
      - {tool: write, match: ".*"}
      - {tool: edit, match: ".*"}
      - {tool: bash, match: "\\b(kubectl (apply|delete|edit|scale)|helm (install|upgrade|uninstall))\\b"}
      - {tool: bash, match: "\\b(systemctl (start|stop|restart|reload))\\b"}
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Read-only-Auditor.** Keine Schreibvorgänge, keine Shell. Geeignet für einen Code-Review-Bot oder einen Docs-Erklärer-Daemon.

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "read-only auditor — no side effects permitted"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
```

Kombinieren Sie mit `provider.claudecli.permission_mode: plan` und `provider.claudecli.extra_args: ["--allowed-tools", "read,grep"]` für Gürtel-und-Hosenträger-Durchsetzung — das Modell kann buchstäblich keine anderen Tools anfordern.

  </div>
</div>

## Fehlerbehebung

### Jeder Aufruf wird abgelehnt, obwohl ich Allow-Regeln habe

Deny gewinnt gegen Allow. Prüfen Sie, ob eine Ihrer Deny-Regeln unbeabsichtigt trifft. Die Log-Zeile `tool.denied name=<X> reason=<Y>` enthält den genauen Grund.

### Pattern-Regex-Compile-Fehler

`PatternApprover` kompiliert Regeln lazy bei der ersten Verwendung. Ein Compile-Fehler wird zu einem `DecisionDeny` mit Grund `approver: pattern compile: <err>`. Korrigieren Sie den Regex; regex101.com mit ausgewähltem Go-Flavor ist Ihr Freund.

### Regex trifft JSON wörtlich, nicht semantisch

Der `match`-Regex läuft gegen die rohe JSON-Eingabe des Tool-Aufrufs. Escape Anführungszeichen und Backslashes angemessen: `"\"path\":\"/workspace/"` trifft das `path`-Feld eines `edit`- oder `write`-Aufrufs.

### `deny_all` blockiert nichts

Bestätigen Sie `mode: deny_all` (nicht `mode: deny`). Die gültigen Modi sind `allow_all`, `deny_all`, `pattern`. `allow` und `deny` allein werden als Aliase für die `_all`-Varianten behandelt, aber exakte Strings sind sicherer.

### Allow-Regel für `bash` trifft nie

Die `bash`-Eingabe ist JSON wie `{"command":"ls -la"}`. Matchen Sie gegen dieses JSON-Literal, nicht nur gegen den Shell-Befehlsstring. Verwenden Sie ein Pattern wie `^\\{\"command\":\"ls`.

## Verwandte Seiten

- [Benutzerleitfaden: Freigaberichtlinien](/de/user-guide/approval-policies/) — tiefere Referenz und durchgearbeitete Beispiele.
- [Benutzerleitfaden: Tools](/de/user-guide/tools/) — das Schema jedes eingebauten Tools.
- [Leitfäden: Observability](/de/guides/observability/) — den Audit-Trail sichtbar machen.
- [Leitfäden: Read-only-Modus](/de/guides/read-only-mode/) — Gürtel-und-Hosenträger-Durchsetzung.
- [Sicherheit](/de/security/) — Übersicht über das Vertrauensmodell.

## Weiterführende Lektüre

- `internal/agent/approver.go` — `PatternApprover`, `AllowAllApprover`, `DenyAllApprover`.
- `internal/agent/approver_test.go` — Testmatrix.
- `internal/cli/approver.go` — Konfiguration → Approver-Übersetzung.
- `internal/config/config.go` — `ApproverConfig`, `PatternEntry`.
