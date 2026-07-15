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
description: "Configure the claudecli provider: PermissionMode values, model aliases, auth inheritance, and when to prefer this over the direct API."
keywords: "claudecli, claude CLI, subprocess, PermissionMode, bypassPermissions, acceptEdits, Claude Code"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/providers/claudecli/"
subtitle: "Subprocess against the local Claude Code CLI."
tags: "providers, claudecli"
title: "claudecli-Anbieter"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "claudecli, claude CLI, subprocess, PermissionMode, bypassPermissions, acceptEdits, Claude Code"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "claudecli-Anbieter"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 6
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/claudecli/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/claudecli/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "claudecli-Anbieter"
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
twitter_description: "Configure the claudecli provider: PermissionMode values, model aliases, auth inheritance, and when to prefer this over the direct API."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "claudecli-Anbieter"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Wie der <code>claudecli</code>-Provider die Authentifizierung von Ihrer lokal installierten Claude Code erbt, die vollständige <code>PermissionMode</code>-Matrix, die Semantik der Sitzungs-Korrelation, Modell-Aliase und wann Sie diese Variante der direkten Anthropic-API vorziehen sollten. Lesen Sie <code>internal/llm/claudecli/client.go</code> parallel zu dieser Seite für die massgebliche Wahrheit.</p></aside>

## Wann claudecli verwenden

`claudecli` startet die `claude`-CLI (Claude Code) als Subprozess. Dies ist der **Standard-Provider** und die richtige Wahl, wenn:

- Sie Claude Code bereits lokal installiert und authentifiziert haben.
- Sie ein Abonnement-Konto von Claude Code wiederverwenden wollen, statt API-Keys zu verlegen.
- Sie das Modell innerhalb der eigenen Tool-Use-Schleife von `claude` laufen lassen wollen (dessen Datei-Bearbeitung, Thinking und Plan-Mode-Features bleiben intakt).
- Sie kein Secret-Material in der rousseau-Config wollen.

Der Kompromiss: Die Tool-`Registry` von rousseau wird für diesen Provider **nicht** aufgerufen – `claude` führt seine eigenen Tools im Subprozess aus. Response-Objekte kommen als einzelne Textnachricht am Turn-Ende zurück. Wenn Sie rousseau benötigen, um `bash`/`edit`/`write` über die Approval-Richtlinie zu regulieren, verwenden Sie stattdessen `anthropic`, `bedrock`, `vertex` oder einen OpenAI-kompatiblen Provider.

## Auth-Vererbung

Die `claude`-CLI hält die Authentifizierung an drei Orten:

| Ort | Inhalt |
|---|---|
| `~/.claude/` | OAuth-Tokens (Abonnement), API-Key-Helper-Output, Workspace-Config. |
| System-Keychain | Auf macOS kann `claude` Refresh-Tokens im Login-Keychain zwischenspeichern. |
| `ANTHROPIC_API_KEY`-Env | Falls gesetzt, nutzt `claude` diesen für den API-Key-Modus anstelle von OAuth. |

`claudecli` liest diese nie direkt. Jeder Aufruf ist `exec.CommandContext(binary, args...)` – der Subprozess erbt Umgebung und Home-Verzeichnis des Parents und ermittelt seine eigenen Credentials. Das macht die Konfiguration für einzelne Betreiber praktisch überflüssig.

<aside class="admonition" data-type="tip"><span class="admonition-title">Container-Bind-Mounts</span><p>Wenn Sie rousseau in einem Container betreiben, mounten Sie <code>~/.claude</code> lesend/schreibend in den Container, damit <code>claude</code> zwischengespeicherte OAuth-Tokens an Ort und Stelle auffrischen kann:</p></aside>

```ini
Volume=%h/.claude:/home/rousseau/.claude:rw,Z
```

Das `Z`-Label ist auf SELinux-Hosts entscheidend; siehe [Bereitstellung](/de/deployment/) für die vollständige Quadlet-Unit.

## Konfiguration

```yaml
provider: claudecli

claudecli:
  binary: claude
  model: sonnet
  permission_mode: bypassPermissions
  extra_args:
    - --add-dir
    - /workspace
```

| Feld | Standard | Wirkung |
|---|---|---|
| `binary` | `claude` | Ausführbare Datei, aufgelöst über `$PATH`. Nutzen Sie einen absoluten Pfad, wenn Sie mehrere `claude`-Versionen haben. |
| `model` | *leer* | Übergeben als `--model <wert>`. Leer nutzt Claudes Standard. |
| `permission_mode` | *leer* | Übergeben als `--permission-mode <wert>`. Siehe Tabelle unten. |
| `extra_args` | `[]` | Wird vor `-p <prompt>` bei jedem Aufruf vorangestellt. |

Jedes Feld ist auf `ClaudeCLIConfig` in `internal/config/config.go` abgebildet. Die bei jedem Turn zusammengebaute Subprozess-Befehlszeile lautet:

```sh
claude --print --output-format json \
  --session-id <sessionID> \
  --system-prompt <systemPrompt> \
  --model <model> \
  --permission-mode <permissionMode> \
  <extra_args...> \
  <prompt>
```

<aside class="admonition" data-type="warning"><span class="admonition-title">STDOUT-Parsing</span><p>Rousseau erwartet, dass <code>claude</code> ein JSON-Envelope auf stdout ausgibt. Wenn Sie <code>claude</code> in ein Shell-Skript wrappen (für Audit, Redaktion oder Rate-Limiting), muss der Wrapper stdout unverändert weiterleiten. Der Parser toleriert eine führende Log-Zeile vor dem ersten <code>{</code> – siehe <code>parseResult</code> in <code>internal/llm/claudecli/client.go</code> – aber Müll nach dem JSON-Envelope führt zu Fehlern.</p></aside>

## PermissionMode-Matrix

Das `PermissionMode`-Flag spiegelt Claudes eigenes `--permission-mode`. Der Subprozess erzwingt den Wert; rousseau prüft nicht doppelt nach.

<div class="tabs" data-tabs="claudecli-permission-modes">
  <div class="tab-list" role="tablist" aria-label="PermissionMode selector">
    <button role="tab" aria-selected="true">Begleitet</button>
    <button role="tab" aria-selected="false">Unbeaufsichtigt</button>
    <button role="tab" aria-selected="false">Nur-Lesen</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Interaktive TUI-Sitzungen, in denen ein Mensch am Terminal sitzt und Tool-Aufrufe freigeben kann.

| Modus | Verhalten |
|---|---|
| `default` | Claude Code fragt für jeden Tool-Aufruf interaktiv nach. Ideal für explorative Sitzungen. |
| `acceptEdits` | Datei-Edits laufen ohne Nachfrage; andere Tools fragen weiter nach. Sinnvoll, wenn Sie der Edit-Oberfläche vertrauen. |
| `auto` | Automatisch anhand des Tools. Nutzen Sie es, wenn Claudes eingebaute Heuristik entscheiden soll. |

```yaml
claudecli:
  permission_mode: acceptEdits
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Chat-Transports (WhatsApp, Slack, Discord, Signal, …) haben keinen Menschen am Terminal, der Nachfragen beantwortet.

| Modus | Verhalten |
|---|---|
| `bypassPermissions` | Jeder Tool-Aufruf läuft ohne Nachfrage. Akzeptiert den vollen Blast-Radius. |
| `dontAsk` | Alias, ähnlich wie Bypass behandelt. |

```yaml
claudecli:
  permission_mode: bypassPermissions
```

Die CLI setzt `bypassPermissions` automatisch für unbeaufsichtigte Daemons, wenn der Betreiber keinen Modus angegeben hat – siehe `setUnattendedPermissionDefault` in `internal/cli`.

<aside class="admonition" data-type="caution"><span class="admonition-title">Blast-Radius</span><p><code>bypassPermissions</code> gibt dem Modell direkten <code>bash</code>-Zugriff mit den Rechten des Daemons. Kombinieren Sie dies mit (a) einem gehärteten Container, (b) einer Allowlist und (c) einem Pattern-Mode-Approver auf rousseau-Seite – oder nutzen Sie einen Nicht-<code>claudecli</code>-Provider, der es rousseau erlaubt, Freigaben vor der Tool-Ausführung durchzusetzen.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Explorationsmodus für grosse Refactorings oder Code-Reviews, in denen Sie keine Schreibvorgänge wollen.

| Modus | Verhalten |
|---|---|
| `plan` | Planner-Modus. Read und grep sind erlaubt; Schreibvorgänge werden unterbunden. |

```yaml
claudecli:
  permission_mode: plan
```

Kombinieren Sie es mit rousseaus eigenem Read-Only-Modus (siehe [Guides: Read-Only-Modus](/de/guides/read-only-mode/)) für doppelte Absicherung.

  </div>
</div>

## Sitzungs-Korrelation

`claudecli` hält den Konversationszustand innerhalb des Subprozesses. Rousseau korreliert seine eigenen Session-IDs mit denen von `claude` über zwei Flags:

- `claude -p --session-id <uuid>` erstellt eine neue Sitzung. Existiert die UUID bereits, meldet `claude` den Fehler `already in use`.
- `claude -p --resume <uuid>` setzt eine bestehende Sitzung fort. Ist sie unbekannt, meldet `claude` einen Fehler.

Rousseau wählt das Flag über einen In-Memory-`SessionCache` (standardmässig `InMemorySessionCache`). Bei einem Cold-Start-Cache-Miss, bei dem `claude` noch State aus einem früheren rousseau-Lauf hält, versucht der Provider optimistisch `--session-id`, fängt den `already in use`-Fehler ab und wiederholt mit `--resume`. Siehe den Kommentar zu `(*Provider).Complete` in `internal/llm/claudecli/client.go`.

Aufrufer, die den Provider einbetten, können einen persistenten Cache via `provider.WithCache(store)` einbringen – der `state.sqlite`-Store implementiert dieselbe Schnittstelle und übersteht Daemon-Neustarts, was den Cold-Start-Round-Trip beim ersten Turn nach einem Neustart vermeidet.

## Modell-Aliase

Die Modell-Aliase von `claude` werden vom Subprozess unverändert übernommen:

| Alias | Zeigt auf |
|---|---|
| `sonnet` | Das aktuelle Standardmodell der Sonnet-Klasse. |
| `opus` | Das aktuelle Standardmodell der Opus-Klasse. |
| `haiku` | Das aktuelle Standardmodell der Haiku-Klasse. |

Für Reproduzierbarkeit über Daemon-Neustarts hinweg (Skill-Benchmarks, Cron-Jobs, Batch-Läufe) pinnen Sie eine exakte Modell-ID:

```yaml
claudecli:
  model: claude-sonnet-4-6
```

<aside class="admonition" data-type="note"><span class="admonition-title">Aliase folgen Releases</span><p>Aliase verschieben sich, wenn Anthropic ein neues Modell ausliefert. Der <code>sonnet</code>-Alias im Juli 2026 zeigt nicht auf dieselben Gewichte wie im April 2026. Wenn Ihr Workflow auf ein bestimmtes Verhalten angewiesen ist, pinnen Sie die exakte ID.</p></aside>

## Kombination mit Skills

`claudecli` sendet den System-Prompt bei der Sitzungs-Erstellung über `--system-prompt`. `claude` übernimmt ihn wortgetreu und ignoriert folgende `--system-prompt`-Werte bei `--resume` – was zur Art passt, wie rousseau ihn nutzt. Die Ausgabe des `SkillsProvider` wird vor dem Aufruf eingefügt:

```
<agent.SystemPrompt>

<Skill-1-Markdown>

<Skill-2-Markdown>

<RecallProvider-Anhang>
```

Siehe `internal/agent/agent.go` `systemPrompt()`. Skills funktionieren über jeden Provider identisch; die Mechanik der Komposition passiert in `agent.Agent`, nicht im Provider.

<aside class="admonition" data-type="tip"><span class="admonition-title">Prompt-Caching</span><p>Der direkte Anthropic-Provider markiert den System-Prompt für den ephemeren Prompt-Cache (siehe <code>internal/llm/anthropic/cache.go</code>). <code>claudecli</code> tut dies nicht – <code>claude</code> verwaltet den eigenen Cache intern. Wenn Sie messbare Prompt-Cache-Einsparungen wollen, nutzen Sie <code>provider: anthropic</code>.</p></aside>

## Fallstricke

- **Keine anbieterübergreifende Portabilität.** Eine gegen `claudecli` erstellte Sitzung ist nicht auf `anthropic` portierbar – der modellseitige State liegt innerhalb von `claude`. Ein Provider-Wechsel mitten in der Sitzung erzwingt eine neue Sitzung.
- **Tool-Registry wird nicht aufgerufen.** `bash`, `edit`, `write`, `grep`, `read` werden von `claude` ausgeführt, nicht von `rousseau`. Rousseaus `agent.Approver` kann diese Aufrufe nicht regulieren. Nutzen Sie einen Nicht-`claudecli`-Provider, wenn Sie rousseau-seitige Freigabe-Erzwingung benötigen.
- **`--add-dir`-Scoping.** Standardmässig weigert sich `claude`, ausserhalb seines eigenen Workspace zu lesen. Übergeben Sie `--add-dir /workspace` (oder wo immer Ihre Quellen liegen) via `extra_args`, um den Bereich zu erweitern. Kombinieren Sie dies mit der Approval-Richtlinie von rousseau auf Transport-Ebene, wenn Sie den Kontrollverlust kompensieren wollen.
- **Streaming.** `claudecli` nutzt `claude -p --output-format json` (nicht-streamend). Der Streaming-Pfad in `internal/llm/claudecli/stream.go` liest `--output-format stream-json`; aktivieren Sie ihn per `StreamingProvider` aus einer Embedding-Integration.
- **Umgebungs-Leakage.** Der Subprozess erbt jede Umgebungsvariable des Parents. Ist `ANTHROPIC_API_KEY` in der rousseau-Umgebung gesetzt, bevorzugt `claude` diesen gegenüber gecachtem OAuth. Das ist meist in Ordnung, ändert jedoch das Billing.

## Fehlerbehebung

### `claudecli: run: exec: "claude": executable file not found in $PATH`

`claude` ist nicht auf `PATH` (oder das Container-Image liefert es nicht aus). Zwei Lösungen:

1. Setzen Sie `claudecli.binary` auf einen absoluten Pfad.
2. Fügen Sie Claude Code zur Runtime-Schicht des Containers hinzu – die Referenz-`docker/Dockerfile` verwendet aus diesem Grund `node:22-alpine`.

### `claudecli: model error: session id already in use`

Sie betreiben zwei rousseau-Prozesse gegen dieselbe Session-ID gegen dieselbe `claude`-Installation, oder der In-Memory-Cache hat eine Sitzung verworfen, an die sich `claude` noch erinnert. Der oben beschriebene optimistische Retry behandelt den zweiten Fall; der erste bedeutet, dass Sie gleichzeitige Daemons haben, die sich in die Quere kommen.

### `claudecli: no JSON in output`

`claude` hat Non-JSON auf stdout ausgegeben oder wurde vor dem Envelope beendet. Häufige Ursachen: ein ungültiger API-Key auf Claude-Code-Seite, eine `claude`-Version, die `--output-format json` nicht kennt, oder ein Shell-Wrapper, der Fortschritts-Marker schreibt. Führen Sie `claude -p --output-format json 'hello'` direkt aus, um dies zu isolieren.

### Die Antwort bricht mitten im Satz ab

Die Ausgabe von `claude` ist durch `--max-turns` und sein eigenes internes Token-Budget begrenzt. Rousseau setzt `--max-turns` nicht; wenn Sie es via `extra_args` setzen, erhöhen Sie es. Für lange Generierungen ziehen Sie einen direkten API-Provider in Betracht, bei dem Sie `MaxTokens` aus `internal/llm/anthropic/client.go` steuern.

### Der Abonnement-Plan wird rate-limited, aber die API funktioniert

Die `claude`-CLI auf einem Abonnement-Plan hat versteckte pro-Konversations- und pro-Zeitfenster-Limits. Wenn Sie diese erreichen, wechseln Sie zu `provider: anthropic` mit einem API-Key – die direkte API hat explizite, veröffentlichte Limits (siehe [Guides: Rate-Limits](/de/guides/rate-limits/)).

## Verwandte Seiten

- [Providers: Anthropic](/de/providers/anthropic/) – direkte API mit Prompt-Caching und Streaming.
- [Providers: Bedrock](/de/providers/bedrock/) – AWS-verwaltetes Claude.
- [Benutzerhandbuch: Approval-Richtlinien](/de/user-guide/approval-policies/) – wie Sie Tool-Aufrufe auf rousseau-Ebene regulieren.
- [Skills](/de/skills/) – wie der System-Prompt-Anhang zusammengesetzt wird.
- [Konfiguration](/de/configuration/) – der `claudecli`-Block im Kontext.

## Weiterführende Lektüre

- `internal/llm/claudecli/client.go` – Subprozess-Aufruf, Sitzungs-Korrelation, JSON-Parsing.
- `internal/llm/claudecli/stream.go` – Streaming-Variante mit `--output-format stream-json`.
- `internal/config/config.go` – `ClaudeCLIConfig`-Struktur.
- `internal/cli/root.go` – wie `setUnattendedPermissionDefault` `bypassPermissions` für Chat-Transports wählt.
