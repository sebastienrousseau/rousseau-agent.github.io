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
description: "Troubleshoot rousseau-agent: WhatsApp QR won't scan, reconnect loops, cosign verify failures, SELinux bind-mount errors, cron not firing, approval policy denying everything."
keywords: "troubleshooting, WhatsApp QR, reconnect loop, cosign verify, SELinux, bind mount, cron, approval policy"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/troubleshooting/"
subtitle: "Häufige Fehlerbilder und ihre Behebung."
tags: "troubleshooting, support"
title: "Fehlerbehebung"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "troubleshooting, WhatsApp QR, reconnect loop, cosign verify, SELinux, bind mount, cron, approval policy"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Fehlerbehebung"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "support"
order: 27
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/troubleshooting/index.html"
item_link: "https://docs.rousseau-agent.dev/troubleshooting/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Fehlerbehebung"
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
twitter_description: "Troubleshoot rousseau-agent: WhatsApp QR won't scan, reconnect loops, cosign verify failures, SELinux bind-mount errors, cron not firing, approval policy denying everything."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Fehlerbehebung"
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

## WhatsApp: QR-Code lässt sich nicht scannen

Symptom: `rousseau whatsapp` gibt einen QR-Code aus, den die Handy-App ablehnt, oder der Pairing-Dialog zeigt "Dieses Gerät ist nicht mit WhatsApp verknüpft."

Lösungen:

1. **Container neu bauen.** Wenn Sie ein älteres Image betreiben, hat `whatsmeow` möglicherweise ein Protokoll-Update ausgeliefert. Neu bauen:
   ```sh
   podman build -t rousseau-agent:local -f docker/Dockerfile .
   systemctl --user restart rousseau-agent.service
   ```
2. **`whatsapp.db` löschen.** Ein teilweise abgeschlossenes Pairing hinterlässt die DB in einem Zustand, den whatsmeow nicht wiederverwenden kann. Löschen und neu pairen:
   ```sh
   rm ~/.local/share/rousseau/whatsapp.db
   ```
3. **Uhrzeitabweichung prüfen.** Der WhatsApp-Handshake ist zeitkritisch. Wenn die Container-Uhr um mehr als 30 Sekunden abweicht, schlägt das Pairing stillschweigend fehl.
   ```sh
   timedatectl status
   ```

## WhatsApp-Reconnect-Schleife

Symptom: In den Logs erscheinen wiederholt `whatsapp.connected` gefolgt von `whatsapp.disconnected` im Sekundenabstand.

Lösungen:

1. **Uhrzeitabweichung.** Gleiche Lösung wie oben.
2. **Allowlist falsch konfiguriert.** Jede eingehende Nachricht wird als unautorisiert verworfen; einige Server schliessen den Socket nach zu vielen stillen Verwerfungen. Fügen Sie die korrekten JIDs mit `--allow` hinzu.
3. **Meta-seitiger Bann.** Wenn die WhatsApp-Mobil-App "Dieses Gerät wurde abgemeldet" anzeigt, hat Meta das Pairing invalidiert. Erneut mit frischem QR-Code pairen. Passiert dies wiederholt mit derselben Nummer, verwenden Sie diese Nummer nicht mehr.

## cosign verify-blob schlägt fehl

Symptom:

```
Error: no matching signatures
```

Lösungen:

1. **Falsche certificate-identity-Regex.** Die Regex muss zum GitHub-Repository passen, das das Release signiert hat. Für rousseau-agent-Releases lautet der korrekte Wert:
   ```
   --certificate-identity-regexp 'sebastienrousseau/rousseau-agent'
   ```
   Verwenden Sie nicht `.*` – das würde eine cosign-Signatur aus jedem Repository akzeptieren.
2. **Falscher OIDC-Aussteller.** GitHub-Actions-cosign-Signaturen stammen von `https://token.actions.githubusercontent.com`. Andere CI-Provider (GitLab, Buildkite) stellen von anderen URLs aus.
3. **Falsche Signatur-Datei.** Prüfen Sie, dass `<version>_checksums.txt.sig` zur `_checksums.txt` gehört, die Sie verifizieren (keine veraltete Kopie eines anderen Release).
4. **Sigstore-Trust-Root geändert.** Aktualisieren Sie mit `cosign initialize`; die Trust-Root wird in langsamer Rotation aktualisiert.

## Container kann Bind-Mount nicht durchführen

Symptom: `podman play kube` oder `systemctl --user start rousseau-agent.service` schlägt mit `permission denied` an einem Bind-Mount fehl.

Lösungen:

1. **SELinux-Label.** Jede Volume-Zeile muss auf `:Z` (oder `:z` für Shared) enden, damit Podman das korrekte SELinux-Label anwendet:
   ```
   Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
   ```
   `:Z` (Grossbuchstabe) ist das private Label – geeignet für Single-Container-Mounts. `:z` (Kleinbuchstabe) teilt das Label über Container hinweg.
2. **`keep-id`-Mapping.** Ohne `UserNS=keep-id` wird die Container-UID 1000 in den subuid-Bereich des Hosts gemappt und kann keine Host-eigenen Dateien schreiben. Stellen Sie sicher, dass das Quadlet Folgendes enthält:
   ```
   UserNS=keep-id
   ```
3. **Fehlendes Verzeichnis.** Podman legt Bind-Mount-Quellen nicht automatisch an. Erstellen Sie das Verzeichnis vorab:
   ```sh
   mkdir -p ~/.local/share/rousseau
   ```

## Cron-Job wird nicht ausgelöst

Symptom: `rousseau cron list` zeigt den Job an, aber zur geplanten Zeit passiert nichts.

Lösungen:

1. **Status prüfen.** `rousseau status` meldet die Scheduler-Aktivität. Wenn der Scheduler nicht läuft, läuft der Daemon nicht, der ihn hostet.
2. **Zeitzone.** Zeitpläne verwenden die lokale Zeitzone des Servers. Bestätigen Sie mit `timedatectl`. Setzen Sie `TZ=UTC` im Quadlet, wenn Sie deterministisches Scheduling unabhängig vom Host-Locale wollen.
3. **PollInterval-Verzögerung.** Neue Jobs werden innerhalb von `PollInterval` (Standard 60s) aktiv. Warten Sie eine Minute.
4. **Zustellungsfehler.** Der Job wurde ausgelöst, aber die Zustellung ist fehlgeschlagen. Prüfen Sie die Logs auf `cron.delivery_failed`; das Zielformat ist transport-spezifisch (siehe [/cron/](/de/cron/)).

## Approval-Richtlinie lehnt alles ab

Symptom: Jeder Tool-Aufruf wird mit "denied by pattern policy" abgelehnt, und das Modell kann nicht fortfahren.

Lösungen:

1. **Fehlende Allow-Regel.** Im `pattern`-Modus mit `default: deny` benötigt jeder Tool-Aufruf eine passende Allow-Regel. Fügen Sie eine für die erlaubten Tools hinzu:
   ```yaml
   agent:
     approver:
       mode: pattern
       default: deny
       allow:
         - {tool: read, match: ".*"}
         - {tool: grep, match: ".*"}
         - {tool: edit, match: "^./workspace/.*"}
   ```
2. **Deny schlägt Allow.** Eine `deny`-Regel gewinnt immer gegen eine `allow`-Regel für dasselbe Tool. Prüfen Sie Ihre Deny-Liste auf ungewollte Überlappungen.
3. **Standard hochsetzen.** Für begleitete Sitzungen ist `default: allow` mit strengeren Deny-Regeln oft praktikabler:
   ```yaml
   agent:
     approver:
       mode: pattern
       default: allow
       deny:
         - {tool: bash, match: "rm -rf|sudo"}
   ```

## Provider gibt 401 zurück

Symptom: Der Agent meldet den Fehler `provider: unauthorized`.

Lösungen:

1. **Falscher API-Key.** Für den direkten Anthropic-Provider prüfen Sie, ob `ANTHROPIC_API_KEY` exportiert oder in `~/.config/rousseau/config.yaml` gesetzt ist.
2. **Falsche Credential-Kette.** Für Bedrock führen Sie `aws sts get-caller-identity` aus dem Container aus, um zu bestätigen, welches Principal das SDK auflöst.
3. **Vertex-Service-Account.** Für den Vertex-Provider prüfen Sie, dass die Datei unter `vertex.credentials_file` im Container lesbar ist und `roles/aiplatform.user` gewährt.

## Provider gibt 429 zurück

Symptom: Der Agent meldet den Fehler `provider: rate limited`.

Lösungen:

1. **`max_tokens` senken.** Kürzere Completions räumen das Rate-Fenster schneller frei.
2. **Kompression aktivieren.** Lange Transkripte erhöhen den Input-Token-Druck; `agent.compression.enabled: true` komprimiert alte Nachrichten.
3. **Abwarten.** rousseau wiederholt innerhalb von `Complete` nicht; der Aufrufer (Chat-Transport, Cron-Scheduler oder `rousseau chat`) entscheidet, ob und wie erneut versucht wird.

## `rousseau chat` zeigt nur eine leere TUI

Symptom: Die Bubble-Tea-TUI öffnet sich, aber ohne Cursor, ohne Viewport.

Lösungen:

1. **TERM-Umgebung.** rousseau benötigt ein ANSI-fähiges Terminal. Setzen Sie `TERM=xterm-256color` (oder ähnlich).
2. **Gekapseltes stdin.** Das Ausführen unter `nohup` oder Pipes entfernt das Terminal. Interaktiv ausführen.

## Slack: `invalid_auth` beim Start

Symptom: `slack.starting` unmittelbar gefolgt von `invalid_auth`.

Lösungen:

1. **Falscher Token verwechselt.** Rousseau benötigt sowohl `xapp-…` (App-Level, `--app-token`) als auch `xoxb-…` (Bot, `--bot-token`). Wird ein App-Token dort übergeben, wo ein Bot-Token erwartet wird, ergibt sich dieser Fehler.
2. **App nicht installiert.** Nach dem Anlegen der Scopes klicken Sie in der Slack-App-Konfiguration auf *Install to Workspace*. Tokens sind erst nach der Installation gültig.
3. **Token rotiert.** Slack-Tokens können von einem Admin manuell rotiert werden. Wenn Sie einen rotiert haben, müssen alle Daemons, die ihn verwenden, mit dem neuen Wert neu gestartet werden.

## Slack: Bot antwortet auf eigene Nachrichten (Schleife)

Symptom: Die ausgehende Nachricht von rousseau löst ein eingehendes Ereignis aus, auf das der Daemon antwortet, was zu Endlos-Antworten führt.

Lösungen:

1. **`bot_user_id` setzen.** Das Flag `--bot-user-id` (oder `slack.bot_user_id` in der Config) weist den Daemon an, Nachrichten dieser User-ID zu ignorieren. Ermitteln Sie sie mit `curl -H "Authorization: Bearer xoxb-..." https://slack.com/api/auth.test`.
2. **Event-Filter verifizieren.** Der Transport ignoriert `bot_message`-Subtypes standardmässig, aber eine schlecht konfigurierte Slack-App kann dies umgehen.

## Discord: Nachrichtentext trifft leer ein

Symptom: `discord.incoming from=... body=` – Nachrichten kommen durch, aber ohne Inhalt.

Lösungen:

1. **Message Content Intent deaktiviert.** Im Discord Developer Portal unter <em>Bot &gt; Privileged Gateway Intents</em> aktivieren Sie **Message Content Intent**. Ohne diesen entfernt Discord Nachrichtentexte aus Gateway-Ereignissen.
2. **Fehlende Scopes.** Die Invite-URL muss dem Bot `Read Message History` und `Send Messages` für den verwendeten Channel/DM gewährt haben.

## Discord: `disallowed intents`

Symptom: Beim Start Fehlermeldung `Discord returned 4014 disallowed intents`.

Lösungen:

1. **Privilegierte Intents.** Aktivieren Sie *Message Content Intent* (siehe oben). Selbst wenn Sie es nie anfragen, liefert Discord 4014, wenn Sie es ohne Freigabe anfordern.
2. **Verifizierung.** Bots in 100+ Servern müssen von Discord verifiziert werden, um privilegierte Intents nutzen zu können. Folgen Sie dem Walkthrough im Developer Portal.

## Telegram: `unauthorized`

Symptom: `telegram.starting` gefolgt von `getUpdates: 401`.

Lösungen:

1. **Falscher Token.** BotFather gibt den Token einmalig aus – ohne den abschliessenden Punkt. Der Token hat die Form `<bot_id>:<secret>`.
2. **Token widerrufen.** `/revoke` im BotFather invalidiert den aktuellen Token; holen Sie sich einen frischen.

## Email: `dial tcp: i/o timeout`

Symptom: Die IMAP- oder SMTP-Verbindung kommt nie zustande.

Lösungen:

1. **Falscher Port.** IMAP läuft auf `993` (implizites TLS). SMTP-Submission auf `587` (STARTTLS) oder `465` (implizites TLS). Rousseau nutzt implizites TLS auf beiden – Nur-STARTTLS-Server werden noch nicht unterstützt. Siehe [Transports: Email](/de/transports/email/) für die Migration.
2. **Egress blockiert.** Unternehmensfirewalls blockieren häufig ausgehendes SMTP. Testen Sie mit `openssl s_client -connect smtp.example.com:465` aus dem Container.
3. **Provider erfordert App-Passwort.** Gmail, Fastmail und ähnliche erfordern ein App-Passwort (nicht Ihr Account-Passwort), wenn 2FA aktiv ist. Erstellen Sie eines in den Sicherheitseinstellungen des Providers.

## Vertex: `permission denied on resource`

Symptom: `vertex: HTTP 403 permission denied on resource projects/.../models/claude-sonnet-4-6@…:rawPredict`.

Lösungen:

1. **Fehlende Rolle.** Weisen Sie `roles/aiplatform.user` dem Service-Account oder Benutzer zu, der die API aufruft. IAM-Änderungen benötigen bis zu einer Minute zur Propagation.
2. **Falsches Projekt.** Das `project` in der Config muss zum Projekt passen, das die Quota hält. Läuft das Billing über ein anderes Projekt, verwenden Sie ein Quota-Project via `gcloud auth application-default set-quota-project`.
3. **Region stimmt nicht überein.** Das Modell muss in der angefragten Region verfügbar sein – der Vertex Model Garden listet dies auf.

## Bedrock: `You don't have access to the model`

Symptom: `AccessDeniedException: You don't have access to the model with the specified model ID`.

Lösungen:

1. **Modell-Zugriff nicht beantragt.** Bedrock erfordert einen expliziten Modell-Zugriffsantrag über die Konsole (*Foundation models &gt; Model access*). Selbst wenn IAM `InvokeModel` erlaubt, ist dieser Schritt erforderlich.
2. **Falsche Region.** Die Modellverfügbarkeit ist regional. Prüfen Sie die Bedrock-Konsole.
3. **Cross-Account-Fehlkonfiguration.** Bei Verwendung von AssumeRole prüfen Sie, ob die Policy der Ziel-Rolle `bedrock:InvokeModel` auf dem exakten Modell-ARN erlaubt.

## Ollama: `context deadline exceeded`

Symptom: rousseau läuft in ein Timeout, während Ollama noch generiert.

Lösungen:

1. **CPU-Inferenz ist langsam.** Ein 70B-Modell auf einer Laptop-CPU kann Minuten pro Turn benötigen. Nutzen Sie ein kleineres Modell (`llama3.1:8b`) oder einen GPU-Host.
2. **Timeout-Vererbung.** rousseau verwendet den Standard-HTTP-Timeout des SDK. Wenn Sie den Provider selbst wrappen, verlängern Sie den Timeout auf mindestens 120 s.

## Sprachnachrichten: Transkribierer nicht konfiguriert

Symptom: `whatsapp.audio_ignored reason=transcriber_not_configured`.

Lösungen:

1. **Whisper deaktiviert.** Setzen Sie `whatsapp.voice.enabled: true` in der Config und stellen Sie sicher, dass das `whisper`-Binary auf `PATH` liegt (oder setzen Sie `whatsapp.voice.binary` auf einen absoluten Pfad).
2. **Modell-Datei fehlt.** Setzen Sie `whatsapp.voice.model_path` auf eine explizite `.bin`-Datei. Whisper.cpp-Modelle werden manuell heruntergeladen – die Config verweist auf ihren Speicherort.

## Session-Store: `database is locked`

Symptom: Der WAL-Schreiber blockiert; Anfragen laufen in einen Timeout.

Lösungen:

1. **Zwei Daemons, eine DB.** SQLite mit WAL unterstützt gleichzeitige Leser, aber nur einen Schreiber. Wenn Sie zwei rousseau-Prozesse gegen denselben `state.path` betreiben, blockiert einer. Nutzen Sie unterschiedliche State-Pfade.
2. **`busy_timeout` zu niedrig.** Der DSN setzt `busy_timeout=15000`. Bei anhaltender Contention erhöhen – aber die Grundursache zuerst untersuchen.
3. **Verwaiste WAL-Datei.** Ein abgestürzter Schreiber kann `sessions.db-wal` gesperrt hinterlassen. Alles stoppen, `sessions.db-wal` und `sessions.db-shm` löschen, neu starten.

## MCP: Claude Desktop sieht keine rousseau-Tools

Symptom: rousseau wurde per `command: "rousseau"` in `claude_desktop_config.json` gestartet, aber es erscheinen keine Tools.

Lösungen:

1. **Config nicht gespeichert.** Claude Desktop lädt beim Speichern neu; wenn Sie die Datei in einer laufenden Instanz bearbeitet haben, starten Sie sie neu.
2. **`command` nicht auf PATH.** Claude Desktop startet Subprozesse aus der eigenen Umgebung; `/usr/local/bin/rousseau` ist möglicherweise nicht sichtbar. Verwenden Sie einen absoluten Pfad.
3. **stderr-Rauschen.** rousseau schreibt strukturierte Logs nach stderr; ein sehr geschwätziger Logger kann den Host überfluten. Setzen Sie `log.level: warn`, wenn Sie MCP gegen einen strengen Host betreiben.

## Skills: `skill loader: parse: yaml: line X`

Symptom: rousseau bricht beim Start mit einem YAML-Parse-Fehler ab.

Lösungen:

1. **Fehlerhaftes Frontmatter.** Skills verwenden `---`-getrenntes YAML-Frontmatter. Stellen Sie sicher, dass beide Fences vorhanden sind und keine Tab-Einrückung existiert.
2. **Nicht gequotete Doppelpunkte.** Ein Doppelpunkt innerhalb eines Wertes (`description: this: that`) wird als verschachtelte Map geparst. Wert quoten: `description: "this: that"`.

## `rousseau doctor` meldet `warn`

Symptom: doctor läuft durch, jedoch mit gelben Zeilen.

Lösungen:

1. **Grund lesen.** Jede Warn-Zeile enthält einen Grund. Häufige: `whatsapp.paired=false` (nie verknüpft), `state.wal_size=large` (Checkpoint überfällig), `provider.claudecli.model=unset` (nutzt Claudes Standard).
2. **Warnungen sind keine Fehler.** Der Daemon startet; die Zeile weist auf etwas hin, das Sie prüfen sollten.

## Kubernetes: Pod bleibt in `CrashLoopBackOff`

Symptom: Das Deployment erreicht nie Ready.

Lösungen:

1. **Logs lesen.** `kubectl logs -p <pod>` zeigt den stderr des vorherigen Containers. Neun von zehn Fällen sind Config- oder Credential-Fehler.
2. **Fehlendes State-Volume.** Ohne PVC für `~/.local/share/rousseau` übersteht das Pairing keinen Neustart, und der Daemon versucht möglicherweise in Schleife, sich neu zu pairen.
3. **IRSA-/Workload-Identity-Fehlkonfiguration.** Prüfen Sie, dass die Service-Account-Annotation zu einer IAM-Rolle mit Provider-Rechten passt. `kubectl exec` in den Pod und `aws sts get-caller-identity` (Bedrock) bzw. `gcloud auth print-access-token` (Vertex) zur Bestätigung ausführen.

## nftables-Regelwerk blockiert Provider-Egress

Symptom: `dial tcp: i/o timeout` beim ersten Provider-Aufruf nach Anwendung eines Egress-Regelwerks.

Lösungen:

1. **CIDR rotiert.** Provider-IP-Bereiche ändern sich. Nutzen Sie DNS-basierten Egress über ein ipset, das per Cron aktualisiert wird, oder einen Egress-Proxy, der zur Connect-Zeit auflöst.
2. **DNS blockiert.** Das Egress-Regelwerk muss UDP/53 (oder TCP/53) zu Ihrem DNS-Resolver zulassen.

## Strukturierten Logs fehlen Felder

Symptom: `whatsapp.incoming` erscheint mit `from`, aber ohne weitere Attribute.

Lösungen:

1. **Log-Level zu hoch.** Einige Felder werden nur bei `debug` emittiert. Setzen Sie `log.level: debug` in der Config.
2. **JSON-Parser verschluckt Felder.** Durch einen Filter geleitet, der unbekannte Felder entfernt, können `elapsed`, `bytes` usw. verloren gehen. Gegen den rohen stdout prüfen.

## Verwandte Seiten

- [Getting Started: Erster Transport](/de/getting-started/first-transport/) – End-to-End-Durchlauf.
- [Provider](/de/providers/) – Fehlerbehebung pro Provider.
- [Transports](/de/transports/) – Fehlerbehebung pro Transport.
- [Konfiguration](/de/configuration/) – die Source of Truth für jeden Regler.
- [Sicherheit](/de/security/) – Vertrauensgrenzen und Audit-Trail.

## Weiterführende Lektüre

- `internal/cli/doctor.go` – die Doctor-Implementierung.
- `internal/state/sqlite/store.go` – DSN des Session-Stores und WAL-Handling.
- `internal/transport/router.go` – Routing eingehender Ereignisse und Allowlist.
- Referenz der Slog-Attribut-Keys – jedes `.info()`/`.warn()`/`.error()` im Source-Tree.
