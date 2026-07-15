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
description: "Approval policy reference for rousseau-agent: allow_all, deny_all, and pattern-mode approvers with allow/deny regex rules and a configurable default."
keywords: "approval, approver, pattern mode, allow_all, deny_all, regex, safety, tool call"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/user-guide/approval-policies/"
subtitle: "Deep dive on approver modes with worked config."
tags: "approval, policy, pattern-mode, safety"
title: "Genehmigungsrichtlinien"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approval, approver, pattern mode, allow_all, deny_all, regex, safety, tool call"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Genehmigungsrichtlinien"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "security"
order: 43
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/approval-policies/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/approval-policies/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Genehmigungsrichtlinien"
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
twitter_description: "Approval policy reference for rousseau-agent: allow_all, deny_all, and pattern-mode approvers with allow/deny regex rules and a configurable default."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Genehmigungsrichtlinien"
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

## Der Vertrag

Jeder Tool-Aufruf durchläuft `Approver.Approve(ctx, ApprovalRequest)`, bevor er ausgeführt wird. Die Schnittstelle lebt in `internal/agent/approver.go`:

```go
type Decision string

const (
    DecisionAllow Decision = "allow"
    DecisionDeny  Decision = "deny"
)

type ApprovalRequest struct {
    ToolName  string
    Input     json.RawMessage
    SessionID string
}

type Approver interface {
    Approve(ctx context.Context, req ApprovalRequest) (Decision, string)
}
```

`Approve` wird synchron auf dem Hot Path aufgerufen; Implementierungen müssen zügig zurückkehren oder `ctx`-Abbruch respektieren.

Ein `DecisionDeny` mit einem nicht-leeren Grund macht den Grund dem Modell als `tool_result`-Fehler sichtbar. Das Modell kann sich dann anpassen (typischerweise, indem es den Operator um Klarstellung bittet), anstatt still zu scheitern. Dies ist eine bewusste Design-Entscheidung – stille Ablehnungen führen zu schlechterem Verhalten als annotierte.

## Drei ausgelieferte Modi

### `allow_all`

Jeder Tool-Aufruf läuft. Dies ist das Basisverhalten, wenn kein Approver konfiguriert ist.

```yaml
agent:
  approver:
    mode: allow_all
```

Verwenden Sie es bei:

- Interaktivem `rousseau chat` mit dem `claudecli`-Provider (Claude Code führt seine eigenen Pro-Aufruf-Freigaben durch).
- Entwicklungs-Smoke-Tests, bei denen Sie genau sehen wollen, was das Modell tun würde.

### `deny_all`

Blockiert jeden Tool-Aufruf mit einem einzigen Grund-String.

```yaml
agent:
  approver:
    mode: deny_all
    reason: "durch Richtlinie für diese Bereitstellung verweigert"
```

Verwenden Sie es bei:

- Smoke-Testen der Approver-Verdrahtung.
- Einer Erst-Inspektions-Haltung, bei der Sie sehen wollen, was das Modell *versucht hätte*, ohne es handeln zu lassen.

### `pattern`

Regex-Allow-/Deny-Regeln pro Tool. **Deny gewinnt über allow.** Nicht übereinstimmende Anfragen fallen auf `default` zurück (`allow` oder `deny`).

```yaml
agent:
  approver:
    mode: pattern
    default: deny         # sicher-by-default; nicht aufgeführte Anfragen werden blockiert
    reason: "durch Pattern-Richtlinie verweigert"
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
      - {tool: edit, match: "\"path\":\"/workspace/[^\"]*\""}
    deny:
      - {tool: bash, match: "rm -rf|sudo|chmod|chown"}
```

## Regel-Semantik

Jede `PatternRule` hat zwei Felder:

| Feld | Bedeutung |
|---|---|
| `tool` | Tool-Name (`read`, `write`, `edit`, `grep`, `bash` oder ein benutzerdefiniertes Tool). Leer trifft auf jedes Tool zu. |
| `match` | Go-RE2-Regex gegen die vom Modell produzierte rohe JSON-Eingabe. Leer trifft auf jede Eingabe zu. |

**Match-Reihenfolge:**

1. Jede Deny-Regel wird gegen die Anfrage getestet. Erster Treffer → deny.
2. Jede Allow-Regel wird getestet. Erster Treffer → allow.
3. Rückfall auf `default`. Leeres `default` wird als `deny` behandelt – sicher-by-default.

Deny gewinnt immer, weil die sicherere Disposition bevorzugt wird. Ein Operator, der einen breiten `allow`-Block hinzufügt, kann niemals versehentlich eine Kategorie freischalten, die er verweigert hatte.

## Matching gegen rohes JSON

Der `match`-Regex läuft gegen die **rohe JSON-Eingabe**, die das Modell ausgegeben hat, nicht gegen geparste Felder. Das hat zwei Konsequenzen:

1. **Sie matchen gegen die JSON-Form.** Für einen `bash`-Aufruf sieht das aus wie `{"command":"ls /tmp"}`. Matchen Sie `"command":\s*"ls\s`.
2. **Sie können jedes Feld matchen.** Das `edit`-Tool empfängt `{"path":"/x","old_string":"...","new_string":"..."}`; Sie können auf `path`, auf `old_string` oder beides matchen.

Escapen Sie JSON-relevante Zeichen sorgfältig:

- Doppelte Anführungszeichen sind im rohen JSON literal – matchen Sie mit `\"` in Ihrem Regex, wenn Sie YAML-Doppelquote-Strings verwenden.
- Backslashes müssen in YAML verdoppelt werden: `\\` in der YAML-Datei wird zu `\` im kompilierten Regex.

## Durchgearbeitete Matcher-Patterns

### Bearbeitungen auf einen Verzeichnisbaum einschränken

```yaml
allow:
  - {tool: edit,  match: "\"path\":\"/workspace/repo/[^\"]*\""}
  - {tool: write, match: "\"path\":\"/workspace/repo/[^\"]*\""}
```

### Sichere Shell-Befehle auf eine Whitelist setzen

```yaml
allow:
  - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|grep|rg|find|git status|git diff|go test) "}
```

### Destruktive Befehle unabhängig von allow ablehnen

```yaml
deny:
  - {tool: bash, match: "rm\\s+-rf|sudo|:\\(\\)\\{ :\\|:& \\};:"}
```

### Schreibvorgänge in Systemverzeichnisse ablehnen

```yaml
deny:
  - {tool: write, match: "\"path\":\"/(etc|root|var|usr)/"}
  - {tool: edit,  match: "\"path\":\"/(etc|root|var|usr)/"}
```

## Das `Default`-Feld

`default: deny` ist die sicherere Disposition und der empfohlene Wert für jeden unbeaufsichtigten Daemon. `default: allow` invertiert das Modell – jeder nicht aufgeführte Aufruf läuft, und `deny`-Regeln werden zum primären Hebel.

Wann `default: allow` verwenden:

- Der Daemon läuft in einem stark abgeschotteten Container ([Bereitstellung](/de/deployment/)) und der Container ist Ihre primäre Grenze.
- Sie experimentieren und wollen das Verhalten des Modells sehen, bevor Sie entscheiden, was zu blockieren ist.

Überall sonst bevorzugen Sie `default: deny`.

## Das `Reason`-Feld

`reason` ist der String, der dem Modell bei jeder Ablehnung (oder `default: deny`-Rückfall) zurückgegeben wird. Leer fällt auf `denied by pattern policy` zurück (oder `denied by policy` für `deny_all`).

Ein hilfreicher Grund verbessert die Modell-Erholung – statt `denied by pattern policy` versuchen Sie `verweigert – diese Bereitstellung erlaubt nur Lesevorgänge innerhalb von /workspace; bitten Sie den Operator, den Umfang zu erweitern` und beobachten Sie, wie das Modell mit einer umsetzbaren Klärung antwortet.

## Interaktion mit `claudecli`

Wenn `provider: claudecli`, führt Claude Code die Tool-Aufrufe aus, und sein eigener Berechtigungsmodus (`bypassPermissions`, `plan`, `default`) gated ebenfalls jede Aktion. Das effektive Verhalten ist der Schnitt: **Beide**, der rousseau-Approver und Claude Codes Approver, müssen den Aufruf erlauben, damit er läuft.

Halten Sie beide möglichst abgestimmt:

- Unbeaufsichtigt: `bypassPermissions` auf Claude Code, `mode: pattern` + `default: deny` auf rousseau.
- Nur-Lese-Inspektion: `plan` auf Claude Code, `mode: pattern` erlaubt auf rousseau nur `read`/`grep`. Siehe [Leitfäden: Read-only-Modus](/de/guides/read-only-mode/).

## Audit-Trail

Jede Approver-Entscheidung wird über slog ausgegeben:

| Ereignis | Bedeutung |
|---|---|
| `tool.execute` (INFO) | Aufruf genehmigt, läuft. |
| `tool.denied` (WARN) | Aufruf blockiert. Enthält Tool-Namen und Grund. |
| `tool.error` (WARN) | Aufruf lief, aber fehlgeschlagen. |

Siehe [Leitfäden: Observability](/de/guides/observability/) für Pipeline-Rezepte.

## Benutzerdefinierte Approver

Jeder Typ, der `Approver` erfüllt, funktioniert. Verdrahten Sie Ihren eigenen beim Einbetten der Agent-Schleife:

```go
myApprover := agent.ApproverFunc(func(ctx context.Context, req agent.ApprovalRequest) (agent.Decision, string) {
    // Eine externe Policy-Engine konsultieren, den Operator befragen, ...
    return agent.DecisionAllow, ""
})

ag := agent.New(provider, registry, logger, agent.Options{Approver: myApprover})
```

Die Schnittstelle ist absichtlich minimal (`Approve` ist die einzige Methode), sodass die Integration mit einer externen Policy-Engine (OPA, Cedar oder einer maßgeschneiderten Rules-Engine) ein kleiner Adapter ist.

## Fehlerbehebung

### Jeder Aufruf verweigert, obwohl ein passendes allow vorhanden ist

Deny gewinnt über allow. `PatternApprover.Approve` in `internal/agent/approver.go` Zeile 152 iteriert zuerst über die Deny-Regeln. Suchen Sie nach dem genauen `reason`-String in den `tool.denied`-Logs.

### Regex-Kompilierungsfehler beim Start

`PatternApprover` kompiliert Regexes lazy beim ersten `Approve`. Ein Kompilierungsfehler führt zu `DecisionDeny` mit dem Grund `approver: pattern compile: <err>`. Testen Sie Regexes unter [regex101.com](https://regex101.com) mit der Go-Variante.

### `mode: pattern`, aber `default:` wird ignoriert

Nur `allow` und `deny` sind gültige Werte für `default:`. Leere oder unbekannte Werte fallen auf `DecisionDeny` zurück (sicherer Standardwert) und geben keine Warnung aus.

### Allow-Regel matcht das JSON literal

Der Regex läuft gegen die rohe Tool-Call-Eingabe-JSON. Um ein `path`-Feld zu matchen, escapen Sie die Anführungszeichen: `"\"path\":\"/workspace/"`.

### Abgelehnte Aufrufe erscheinen nicht in den Logs

Doch – als `tool.denied` auf `warn`-Level. Wenn Sie nach Level filtern, stellen Sie sicher, dass `warn` enthalten ist.

## Verwandte Seiten

- [Leitfäden: Audit + Freigaberichtlinien](/de/guides/audit-approval-policies/) — durchgearbeitetes Beispiel mit slog-Audit-Trail.
- [Leitfäden: Read-only-Modus](/de/guides/read-only-mode/) — die Inspektions-Haltung.
- [Benutzerleitfaden: Tools](/de/user-guide/tools/) — die Tools, die der Approver gated.
- [Sicherheit](/de/security/) — Übersicht über Vertrauensgrenzen.
- [Agent-Schleife](/de/agent-loop/) — wo der Approver aufgerufen wird.

## Weiterführende Lektüre

- `internal/agent/approver.go` — `PatternApprover`, `AllowAllApprover`, `DenyAllApprover`.
- `internal/agent/approver_test.go` — die Test-Matrix.
- `internal/cli/approver.go` — Konfiguration → Approver-Übersetzung.
- `internal/config/config.go` — `ApproverConfig`, `PatternEntry`.
