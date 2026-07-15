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
description: "Go from bypassPermissions to a pattern-mode approver with default: deny and validate the audit trail through slog."
keywords: "approver, pattern mode, default deny, tool denied, audit, slog"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/tutorials/harden-approver-policy/"
subtitle: "From bypassPermissions to default-deny with slog-audited rule matching."
tags: "tutorials, approver, pattern-mode, security, audit"
title: "Tutorial: den Approver härten"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "approver, pattern mode, default deny, tool denied, audit, slog"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: den Approver härten"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 46
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/harden-approver-policy/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/harden-approver-policy/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: den Approver härten"
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
twitter_description: "Go from bypassPermissions to a pattern-mode approver with default: deny and validate the audit trail through slog."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: den Approver härten"
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

## Was Sie bauen

Ein rousseau-Daemon, der ursprünglich den `claudecli`-Provider im `bypassPermissions`-Modus (dem unbeaufsichtigten Standard) betrieb, endet unter einem `pattern`-Modus-rousseau-agent-Approver mit `default: deny`. Jeder Tool-Aufruf ist entweder explizit allowlistet oder blockiert; jede Ablehnung produziert ein `tool.denied`-slog-Ereignis, das Sie auditieren können.

Geschätzte Zeit: 30 Minuten für einen ordentlichen Regeldurchlauf mit Tests.

## Voraussetzungen

- Rousseau installiert mit einer beliebigen laufenden Transport-Bridge (WhatsApp, Slack, Signal — irgendetwas Unbeaufsichtigtes).
- Grundlegende Go-Regex-Kenntnisse — Approver-Regeln sind Go-RE2-Regexe über den JSON-Tool-Input.

## Wo der Approver lebt

Zwei unabhängige Schichten können Tool-Aufrufe freigeben:

1. **Der eigene Berechtigungsmodus des Providers.** Der `claudecli`-Provider (`internal/llm/claudecli/client.go`) delegiert an `claude --permission-mode`. Werte dokumentiert in `ClaudeCLIConfig.PermissionMode` (`internal/config/config.go`): `acceptEdits`, `auto`, `bypassPermissions`, `default`, `dontAsk`, `plan`. Unbeaufsichtigte Daemons pinnen `bypassPermissions` in `setUnattendedPermissionDefault`.
2. **Der eigene Approver von rousseau.** Konfiguriert unter `agent.approver` (`internal/config/config.go` `ApproverConfig`; Implementierung in `internal/agent/approver.go`). Drei Modi: `allow_all`, `deny_all`, `pattern`. **Deny gewinnt gegen Allow, und nicht getroffene Aufrufe fallen auf `default` zurück.**

Für einen unbeaufsichtigten Daemon ist der rousseau-Approver die Mitigation, die Sie händisch konfigurieren. Der eigene Modus von `claudecli` ist der Sicherheitsgurt.

## Schritt 1: Baseline-Audit

Bevor Sie Regeln schreiben, führen Sie einige realistische Sitzungen mit `mode: allow_all` und `log.format: json` aus. Jeder Tool-Aufruf emittiert `tool.execute` (`internal/agent/agent.go`):

```sh
jq -c 'select(.msg == "tool.execute") | {name, input: .input}' \
  < /var/log/rousseau.jsonl \
  | sort | uniq -c | sort -rn | head
```

Sie haben nun eine empirische Verteilung darüber, welche Tools der Agent verwendet und gegen welche Pfade. Das ist die Saat für die Allowlist.

## Schritt 2: Pattern-Richtlinie entwerfen

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    reason: "denied by pattern policy — ask the operator to loosen the rules"
    allow:
      # Read side: unrestricted within the daemon's filesystem view.
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}

      # Editing pinned to /workspace.
      - {tool: edit,  match: "\"path\":\"/workspace/[^\"]*\""}
      - {tool: write, match: "\"path\":\"/workspace/[^\"]*\""}

      # Shell: whitelist of read-only utilities plus git status/diff/log.
      - {tool: bash, match: "^\\s*\"command\":\\s*\"(ls|cat|head|tail|grep|rg|find|wc|stat|file|which|pwd|env|git status|git diff|git log|go test|go vet|go build)\\b"}

    deny:
      # Absolute denies override any allow above.
      - {tool: bash, match: "rm\\s+-rf|sudo|curl|wget|chmod|chown|nc\\s|ncat"}
      - {tool: bash, match: ":\\(\\)\\{ :\\|:& \\};:"}    # fork bomb
      - {tool: write, match: "\"path\":\"/etc/|/root/|/var/"}
      - {tool: edit,  match: "\"path\":\"/etc/|/root/|/var/"}
```

Deployen und den slog-Stream beobachten. Die relevanten Ereignisse (`internal/agent/agent.go`):

- `tool.execute` — der Aufruf lief. Felder: `name`, `id`.
- `tool.denied` — der Approver hat ihn blockiert. Felder: `name`, `reason`.
- `tool.error` — er lief und schlug fehl. Felder: `name`, `err`.

## Schritt 3: iterieren

Der erste Tag bringt False Positives zutage: legitime Tool-Aufrufe, die der Approver blockiert hat. Greppen Sie danach:

```sh
jq -c 'select(.msg == "tool.denied") | {name, input}' \
  < /var/log/rousseau.jsonl \
  | sort | uniq -c | sort -rn | head
```

Jedes wiederkehrende `tool.denied` verdient eine Entscheidung:

- **Wirklich benötigt** — erweitern Sie die Allow-Regel. Bevorzugen Sie eng (Pfad gepinnt) gegenüber breit (offener Regex).
- **Nicht benötigt** — abgelehnt lassen. Das Modell wird auf einen anderen Ansatz umschwenken.

Schwächen Sie `default: deny` nicht ab. Das ist die Eigenschaft, die ein nicht vergessenes Tool sicher macht.

## Schritt 4: Audit-Log-Auszug

Ein Produktionslauf mit einem unbekannten Prompt sah so aus:

```jsonl
{"time":"2026-07-13T18:00:12Z","level":"INFO", "msg":"whatsapp.incoming","from":"447900123456@s.whatsapp.net"}
{"time":"2026-07-13T18:00:14Z","level":"INFO", "msg":"tool.execute","name":"grep","id":"t_1"}
{"time":"2026-07-13T18:00:15Z","level":"INFO", "msg":"tool.execute","name":"read","id":"t_2"}
{"time":"2026-07-13T18:00:17Z","level":"WARN", "msg":"tool.denied","name":"bash","reason":"denied by pattern policy — ask the operator to loosen the rules"}
{"time":"2026-07-13T18:00:18Z","level":"INFO", "msg":"tool.execute","name":"read","id":"t_3"}
{"time":"2026-07-13T18:00:20Z","level":"INFO", "msg":"whatsapp.handler_ok","elapsed":"7.4s"}
```

Das eine `tool.denied` hier war `bash: "curl https://…"`. Die Deny-Regel hat es abgefangen, das Modell hat auf `read` + `grep` degradiert, und die Antwort ging trotzdem durch.

## Schritt 5: einbrennen

Sobald die False-Positive-Rate sich einpendelt, frieren Sie die Konfiguration ein, committen Sie sie in die Versionskontrolle (Secrets ausgeschlossen — siehe [Leitfäden: Enterprise-Onboarding](/de/guides/enterprise-onboarding/)) und gaten Sie Konfigurationsänderungen hinter einem Code-Review. `internal/agent/approver_test.go` im Source-Baum ist Ihr Vorbild dafür, wie Tests gegen den Regelsatz geschrieben werden — kopieren Sie seine Form in ein internes Paket, wenn Sie möchten, dass die CI eine kaputte Richtlinie abfängt.

## Was die Richtlinie dennoch nicht tut

Selbst mit den strengsten Pattern-Regeln:

- **Kein Sandboxing.** Ein erlaubter `bash`-Aufruf läuft weiterhin mit der UID und Dateisystem-Sichtbarkeit des Daemons. Legen Sie einen rootless Container ([Bereitstellung](/de/deployment/)) darunter.
- **Kein Rate-Limiting.** Zehn erlaubte Aufrufe pro Sekunde sind alle erlaubt. Wickeln Sie die Tool-Registry, wenn Sie dies benötigen.
- **Kein Outbound-Netzwerk-Audit.** Der Approver sieht den initialen `bash`-`command`-String, nicht das, was er curlt. Verbieten Sie `curl` und `wget` direkt — die Beispiel-Deny-Regeln tun dies.

Siehe [Leitfäden: Audit + Freigaberichtlinien](/de/guides/audit-approval-policies/) für die tiefere Diskussion.

## Verwandt

- [Benutzerleitfaden: Freigaberichtlinien](/de/user-guide/approval-policies/) — Referenz für jeden Modus.
- [Benutzerleitfaden: Tools](/de/user-guide/tools/) — Tool-Schemata, nützlich zum Schreiben von Regexen.
- [Leitfäden: Observability](/de/guides/observability/) — `tool.denied` an Loki/Datadog leiten.
- [Referenz: Logs](/de/reference/logs/) — jede wohlbekannte slog-Nachricht.
