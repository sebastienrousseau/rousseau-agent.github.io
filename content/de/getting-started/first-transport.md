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
description: "End-to-end walkthrough for wiring your first chat transport. Uses WhatsApp as the canonical example: pair, allowlist, send a test message, verify the reply."
keywords: "first transport, whatsapp, pairing, allowlist, e2e walkthrough, test message"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/getting-started/first-transport/"
subtitle: "End-to-end WhatsApp walkthrough: pair, allowlist, verify."
tags: "first-transport, whatsapp, walkthrough"
title: "Ihr erster Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "first transport, whatsapp, pairing, allowlist, e2e walkthrough, test message"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Ihr erster Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 25
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/first-transport/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/first-transport/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Ihr erster Transport"
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
twitter_description: "End-to-end walkthrough for wiring your first chat transport. Uses WhatsApp as the canonical example: pair, allowlist, send a test message, verify the reply."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Ihr erster Transport"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Wie Sie einen Chat-Transport mit dem rousseau-Daemon paaren, die steuernde JID/User-ID in die Allowlist aufnehmen, eine erste Testnachricht senden und die Antwort verifizieren. WhatsApp ist der kanonische Durchlauf, weil das Pairing am strengsten ist; die Tabs unten zeigen die parallelen Durchläufe für Slack und Discord.</p></aside>

## Ihren ersten Transport wählen

Jeder Transport ist ein dünner Adapter hinter demselben `transport.Transport`-Interface – Allowlisting, Sitzungs-Routing und Cron-Zustellung sind über alle hinweg identisch. Die Unterschiede liegen in der Pairing-UX und im transport-spezifischen Identifier-Format (JID, User-ID, Room-ID). Wählen Sie den, den Sie am schnellsten paaren können:

<div class="tabs" data-tabs="first-transport">
  <div class="tab-list" role="tablist" aria-label="First transport">
    <button role="tab" aria-selected="true">WhatsApp</button>
    <button role="tab" aria-selected="false">Slack</button>
    <button role="tab" aria-selected="false">Discord</button>
    <button role="tab" aria-selected="false">Telegram</button>
    <button role="tab" aria-selected="false">Signal</button>
  </div>
  <div class="tab-panel" role="tabpanel">

WhatsApp ist die Referenz – am schwierigsten zu paaren, am einfachsten zu testen (Sie haben die App bereits auf dem Handy).

**Voraussetzungen:** Ihr Handy mit WhatsApp, Ihre E.164-JID (z.B. `447900123456@s.whatsapp.net`).

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Scannen Sie den QR-Code aus **WhatsApp &gt; Einstellungen &gt; Verknüpfte Geräte &gt; Gerät verknüpfen**. Senden Sie `hello` an sich selbst; rousseau antwortet via WhatsApp. Siehe unten für den vollständigen Durchlauf.

<aside class="admonition" data-type="warning"><span class="admonition-title">Inoffizielles Protokoll</span><p>Der WhatsApp-Support nutzt <code>whatsmeow</code> – einen reverse-engineerten Client. Meta sperrt gelegentlich Nummern, die inoffizielle Clients betreiben. Nutzen Sie dies nicht auf einer Nummer, auf die Sie angewiesen sind.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Voraussetzungen:** Admin in einem Slack-Workspace, eine unter [api.slack.com/apps](https://api.slack.com/apps) erstellte App, Socket Mode aktiviert.

1. Erstellen Sie eine Slack-App, aktivieren Sie **Socket Mode** unter <em>Settings &gt; Socket Mode</em>.
2. Erstellen Sie ein **App-Level-Token** mit `connections:write` – dies ist der `xapp-…`-Token.
3. Unter <em>OAuth &amp; Permissions</em> fügen Sie die Bot-Scopes `chat:write`, `im:history`, `im:read`, `im:write`, `mpim:history`, `mpim:read` hinzu. Installieren Sie in den Workspace, um den `xoxb-…`-Bot-Token zu erhalten.
4. Unter <em>Event Subscriptions</em> abonnieren Sie `message.im` (DMs) und jedes gewünschte Channel-Ereignis.

```sh
rousseau slack --app-token xapp-... --bot-token xoxb-... --allow U01234567
```

Senden Sie dem Bot eine DM in Slack; rousseau antwortet in derselben DM. Siehe [Transports: Slack](/de/transports/slack/) für den vollständigen Durchlauf mit Begründung der OAuth-Scopes.

<aside class="admonition" data-type="tip"><span class="admonition-title">Kein öffentliches HTTP</span><p>Socket Mode bedeutet, dass der Daemon ausgehend zum WebSocket von Slack verbindet. Sie benötigen keinen öffentlichen Webhook, kein ngrok und keinen Ingress.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Voraussetzungen:** eine Discord-Application unter [discord.com/developers/applications](https://discord.com/developers/applications), ein Bot-Benutzer, das **Message Content Intent** unter <em>Bot</em> aktiviert.

1. Erstellen Sie eine Application, fügen Sie einen Bot hinzu, kopieren Sie den Bot-Token.
2. Unter <em>Bot &gt; Privileged Gateway Intents</em> aktivieren Sie **Message Content Intent**. Ohne dies kommen Nachrichtentexte leer an.
3. Laden Sie den Bot über <em>OAuth2 &gt; URL Generator</em> ein – Scope `bot`, Berechtigungen `Send Messages`, `Read Message History`.

```sh
rousseau discord --token <bot-token> --allow 234567890123456789
```

Senden Sie dem Bot eine DM; rousseau antwortet. Siehe [Transports: Discord](/de/transports/discord/) für ein Deep-Dive zu Berechtigungen und Intents.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Voraussetzungen:** ein Telegram-Bot von [@BotFather](https://t.me/BotFather).

1. Schreiben Sie `@BotFather`, `/newbot`, folgen Sie den Anweisungen. Kopieren Sie den Token.
2. Sprechen Sie Ihren Bot mindestens einmal an, damit Telegram einen Chat anlegt.

```sh
rousseau telegram --token 1234567890:AA... --allow 987654321
```

Der `--allow`-Wert ist die numerische Telegram-User-ID (nicht der Benutzername). Sie erhalten sie durch Anschreiben von [@userinfobot](https://t.me/userinfobot).

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

**Voraussetzungen:** `signal-cli` installiert und mit einem Signal-Konto verknüpft. Siehe die [signal-cli-Dokumentation](https://github.com/AsamK/signal-cli) für den Pairing-Flow.

```sh
rousseau signal --account +447900123456 --allow +447900654321
```

Rousseau startet `signal-cli` als Subprozess (siehe `internal/cli/signal.go`) und kommuniziert damit via JSON-RPC. Siehe [Transports: Signal](/de/transports/signal/).

  </div>
</div>

## Warum der WhatsApp-Durchlauf

Der Rest dieser Seite verwendet WhatsApp als kanonisches Beispiel – wenn Sie das Muster hier beherrschen, ist jeder andere Transport eine Variation davon (stabile ID auf die Allowlist setzen, Pairing-UX einmal durchführen, Test senden, Antwort verifizieren). Springen Sie zur passenden Transport-Seite, wenn Sie bereits einen Token in der Hand haben:

- [Slack](/de/transports/slack/) – Socket-Mode-Tokens und Event-Subscriptions.
- [Discord](/de/transports/discord/) – Bot-Token, Intents, Permission-Integers.
- [Telegram](/de/transports/telegram/) – BotFather-Token.
- [Signal](/de/transports/signal/) – signal-cli-Subprozess.
- [Matrix](/de/transports/matrix/) – Homeserver-URL + Access-Token.

## Voraussetzungen

- `rousseau` auf `$PATH` (siehe [Installation](/de/getting-started/installation/)).
- Ein funktionierender Provider – `claudecli` erbt die Claude-Code-Auth und ist der Standard; alles andere muss zunächst konfiguriert werden ([Konfiguration](/de/configuration/)).
- Ihr Handy mit installiertem WhatsApp. Ihre E.164-Telefon-JID (z.B. `447900123456@s.whatsapp.net`).

## Schritt 1 – Wählen Sie die JID, die den Daemon steuert

Rousseau nutzt eine Allowlist, um die Verarbeitung eingehender Nachrichten auf eine feste Menge von JIDs zu beschränken. Jeder andere Absender wird stillschweigend verworfen. Dies ist tragend: Ohne Allowlist könnte jeder mit Kenntnis der Nummer den Agenten steuern.

Ihre E.164-JID ist Ihre Telefonnummer, nur Ziffern, gefolgt von `@s.whatsapp.net`:

```
447900123456@s.whatsapp.net
```

Gruppen-JIDs enden auf `@g.us`; der Daemon unterstützt diese ebenfalls, aber beginnen Sie mit einer persönlichen JID.

## Schritt 2 – Erster Start und Pairing

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Beim ersten Start wird ein QR-Code auf stdout ausgegeben. Öffnen Sie WhatsApp auf Ihrem Handy, gehen Sie zu **Einstellungen → Verknüpfte Geräte → Gerät verknüpfen** und scannen Sie den QR-Code.

Der Daemon gibt etwa Folgendes aus:

```
whatsapp.starting store=file:/home/you/.local/share/rousseau/whatsapp.db?_pragma=... allowlist=1
```

Sobald Sie gescannt haben, persistiert whatsmeow die Geräte-Credentials in `whatsapp.db`. Folge-Starts verbinden sich stillschweigend – kein weiterer QR-Code.

## Schritt 3 – Eine Testnachricht senden

Senden Sie von Ihrem Handy `hello` an sich selbst. Der Daemon loggt das eingehende Ereignis, leitet an den Agenten weiter und stellt die Antwort über WhatsApp mit dem konfigurierten Header zu:

```
💎 *Rousseau Agent*

Hallo – woran möchten Sie arbeiten?
```

Der Reply-Header ist über `whatsapp.reply_header` konfigurierbar. Setzen Sie ihn auf ein einzelnes Leerzeichen, um das Präfix zu deaktivieren.

## Schritt 4 – Eine `config.yaml` einrichten, damit lange Flags entfallen

Erstellen Sie `~/.config/rousseau/config.yaml`:

```yaml
provider: claudecli

claudecli:
  binary: claude
  permission_mode: bypassPermissions

whatsapp:
  reply_header: "💎 *Rousseau Agent*\n\n"
```

Nun übernimmt `rousseau whatsapp --allow 447900123456@s.whatsapp.net` den Header automatisch. Jeder Transport liest seinen Block aus derselben Datei – siehe [Konfiguration](/de/configuration/) für die vollständige Liste.

`bypassPermissions` ist der Standard für unbeaufsichtigte Daemons, weil am anderen Ende des Terminals kein Mensch sitzt, der Tool-Aufrufe interaktiv freigibt. **Richten Sie eine Approval-Richtlinie ein** ([Benutzerhandbuch: Approval-Richtlinien](/de/user-guide/approval-policies/)), bevor Sie den Daemon auf etwas Wichtiges loslassen.

## Schritt 5 – End-to-End bestätigen

Senden Sie eine Coding-Frage von Ihrem Handy:

```
Lies die Datei /workspace/README.md und fasse sie in 3 Punkten zusammen.
```

Der Daemon führt einen `read`-Tool-Aufruf aus, füttert die Datei an das Modell und schreibt Ihnen die Zusammenfassung zurück. Sie haben soeben den Kreis geschlossen:

- Handy → WhatsApp → whatsmeow-WebSocket
- rousseau-agent → Agent-Schleife → Tool-Aufruf → Provider-Aufruf
- Antwort → whatsmeow → WhatsApp → Handy

Nichts hat Ihren Netzwerk-Perimeter verlassen ausser dem Provider-Aufruf – und wenn der Provider `claudecli` auf Ihrer lokalen Claude-Code-Installation war, nicht einmal das.

## Verifikation mit `rousseau doctor`

```sh
rousseau doctor
```

Jede Prüfung für den WhatsApp-Pfad ist abgedeckt:

- `provider.claudecli.binary`, `provider.claudecli.version` – der LLM-Pfad.
- `state.path`, `state.db_size`, `state.sessions` – SQLite-Session-Store.
- `whatsapp.store`, `whatsapp.paired` – Geräte-Credentials.
- `whatsapp.voice` – Posture der Sprachnachrichten-Transkription.

Eine `fail`-Zeile ist ein Hard-Stop; eine `warn`-Zeile sollten Sie vor dem Rollout untersuchen.

## Fehlerbehebung

### QR-Code wird ausgegeben, aber das Handy lehnt ihn ab

Drei häufige Ursachen. Erstens: Ein teilweise abgeschlossenes vorheriges Pairing hat `whatsapp.db` in einem Zustand hinterlassen, den whatsmeow nicht wiederverwenden kann – löschen Sie `~/.local/share/rousseau/whatsapp.db` und scannen Sie erneut. Zweitens: Die Uhr weicht um mehr als 30 Sekunden ab (häufig in Containern ohne funktionierenden NTP-Client) – der WhatsApp-Handshake ist zeitkritisch. Drittens: Eine ältere `whatsmeow`-Version kann ein Meta-Protokoll-Update verpasst haben; aktualisieren Sie rousseau.

### Ich habe eine Nachricht gesendet, aber der Daemon loggt `router.transport.rejected`

Ihre JID passt nicht zur Allowlist. Der an `--allow` übergebene Wert muss die JID des Absenders exakt so lauten, wie WhatsApp sie meldet (`447900123456@s.whatsapp.net`, ohne `+`, ohne Leerzeichen). Beachten Sie, dass Selbst-Chat-Tests funktionieren, weil rousseau die eigene JID des Kontos für den LID-Privacy-Hash ersetzt (siehe `internal/transport/whatsapp/resolve.go`).

### Es wird kein QR-Code ausgegeben und der Daemon beendet mit `no rows`

Der whatsmeow-Store wurde nie initialisiert. Stellen Sie sicher, dass das übergeordnete Verzeichnis (`~/.local/share/rousseau/`) existiert und beschreibbar ist. `rousseau doctor` meldet dies unter `whatsapp.store`.

### Rousseau antwortet, aber die Modell-Ausgabe ist leer

Prüfen Sie `provider.claudecli.binary` und `provider.claudecli.version` in `rousseau doctor`. Die häufigste Ursache für leere Antworten ist ein `claudecli`-Aufruf, der `is_error: true` zurückgibt – der Daemon loggt den gekürzten Fehler auf `warn`-Level. Wechseln Sie den Provider auf `anthropic` oder `bedrock`, um den Subprozess zu isolieren.

### Slack/Discord: "invalid_auth" oder "401 Unauthorized"

Für Slack sind `xapp-…` (App-Token) und `xoxb-…` (Bot-Token) verschieden – ihre Verwechslung führt zu `invalid_auth`. Für Discord ist der unter <em>Bot &gt; Reset Token</em> angezeigte Token einmalig; wenn Sie ihn einmal kopiert und verloren haben, müssen Sie erneut resetten.

## Verwandte Seiten

- [Transports](/de/transports/) – jeder Transport, sein Wire-Protokoll und sein Allowlist-Format.
- [Benutzerhandbuch: CLI](/de/user-guide/cli/) – jeder Befehl und jedes Flag.
- [Benutzerhandbuch: Approval-Richtlinien](/de/user-guide/approval-policies/) – der primäre Sicherheitshebel.
- [Bereitstellung](/de/deployment/) – Übergabe vom Vordergrund-`rousseau whatsapp` an eine systemd-Unit.
- [Voice-Modus](/de/user-guide/voice-mode/) – WhatsApp-Sprachnachrichten in Agent-Turns umwandeln.

## Weiterführende Lektüre

- `internal/transport/whatsapp/client.go` – Connect, QR, Event-Pump.
- `internal/transport/whatsapp/resolve.go` – LID/JID-Normalisierung und Selbst-Chat-Handling.
- `internal/cli/whatsapp.go` – CLI-Verdrahtung, Store-DSN, Auswahl des Transkribierers.
- `internal/cli/slack.go`, `internal/cli/discord.go` – Geschwister-Transport-CLIs.
- `internal/transport/router.go` – Durchsetzung der Allowlist.
