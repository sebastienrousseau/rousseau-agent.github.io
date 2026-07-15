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
description: "Set up rousseau-agent's WhatsApp transport: QR pairing, E.164 allowlist, LID vs phone-JID normalisation, voice-note transcription with whisper.cpp."
keywords: "WhatsApp, whatsmeow, QR pairing, JID, LID, allowlist, voice notes, whisper, transcription"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/transports/whatsapp/"
subtitle: "Whatsmeow-backed WhatsApp bridge with QR pairing."
tags: "transports, WhatsApp"
title: "WhatsApp-Transport"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "WhatsApp, whatsmeow, QR pairing, JID, LID, allowlist, voice notes, whisper, transcription"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "WhatsApp-Transport"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "transports"
order: 12
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/transports/whatsapp/index.html"
item_link: "https://docs.rousseau-agent.dev/transports/whatsapp/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "WhatsApp-Transport"
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
twitter_description: "Set up rousseau-agent's WhatsApp transport: QR pairing, E.164 allowlist, LID vs phone-JID normalisation, voice-note transcription with whisper.cpp."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "WhatsApp-Transport"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Wie sich der WhatsApp-Transport mit Ihrem Handy paart, die Normalisierungsregeln für LID vs. Telefon-JID, den Ablauf der Sprachnachrichten-Transkription, Medien-Downloads, Allowlist-Regex-Muster und die Fehlermodi, die Erstbetreiber abfangen. Lesen Sie <code>internal/transport/whatsapp/client.go</code>, <code>resolve.go</code> und <code>dispatch.go</code> parallel zu dieser Seite.</p></aside>

## Überblick

Der WhatsApp-Transport (`internal/transport/whatsapp/`) basiert auf `go.mau.fi/whatsmeow` – einem reverse-engineerten WhatsApp-Web-Multi-Device-Client. Meta betrachtet dies als inoffiziellen Client; nutzen Sie ihn nicht auf einer persönlichen Nummer, auf die Sie für Wichtiges angewiesen sind.

Die End-to-End-Verschlüsselung des Signal-Protokolls bleibt erhalten (whatsmeow nutzt dasselbe Protokoll wie die WhatsApp-Mobil-App). Der Daemon hält die Geräte-Credentials in einer SQLite-Datei getrennt vom Session-Store, weshalb ein Geräte-Relink die Konversationshistorie nicht berührt.

<aside class="admonition" data-type="caution"><span class="admonition-title">Inoffizielles Protokoll</span><p>Meta sperrt gelegentlich Nummern, die inoffizielle Clients betreiben. Selbst wenn Sie WhatsApps Rate-Limits einhalten und verantwortungsvoll agieren, kann eine mit <code>whatsmeow</code> genutzte Rufnummer ohne Vorwarnung gesperrt werden. Nutzen Sie eine dedizierte Nummer, keine persönliche.</p></aside>

## Pairing

Erster Start:

```sh
rousseau whatsapp --allow 447900123456@s.whatsapp.net
```

Ein QR-Code wird über `mdp/qrterminal/v3` nach stdout ausgegeben. Scannen Sie ihn mit der WhatsApp-Mobil-App (**Einstellungen → Verknüpfte Geräte → Gerät verknüpfen**). Der Pairing-Zustand wird nach `whatsapp.db` im State-Verzeichnis geschrieben (typischerweise `~/.local/share/rousseau/whatsapp.db`).

Folge-Starts nutzen das gepaarte Gerät stillschweigend weiter. Erscheint der QR erneut, wurde das Pairing seitens des Handys widerrufen – löschen Sie `whatsapp.db` und paaren Sie erneut.

## Allowlist

`--allow` beschränkt die Verarbeitung eingehender Nachrichten. Mehrere Flags akkumulieren:

```sh
rousseau whatsapp \
  --allow 447900123456@s.whatsapp.net \
  --allow 442071234567@s.whatsapp.net
```

Der Wert ist eine WhatsApp-**JID** – die E.164-Telefonnummer (ohne `+`) gefolgt von `@s.whatsapp.net`. Gruppen-JIDs (`<id>@g.us`) werden ebenfalls unterstützt.

Eine leere Allowlist akzeptiert jeden Absender. Für einen Chat-Transport-Daemon wollen Sie stets mindestens einen Eintrag.

## LID- vs. Telefon-JID-Normalisierung

WhatsApp nutzt für einen Benutzer zwei ID-Formate:

| Format | Beispiel | Bedeutung |
|---|---|---|
| Telefon-JID | `447900123456@s.whatsapp.net` | Die E.164-Telefonnummer ohne `+`, gefolgt von `@s.whatsapp.net`. Zeitlich stabil; verrät die Rufnummer. |
| LID | `1234567890@lid` | Location-Independent ID – ein zufällig wirkender String, der die Rufnummer nicht preisgibt. Ebenfalls stabil, aber nicht direkt einer Nummer zuordenbar. |
| Device-Suffix | `447900123456:5@s.whatsapp.net` | Jede JID kann ein Geräte-Adress-Suffix (`:N`) tragen. WhatsApp meldet Nachrichten mit dem konkreten Gerät, das sie gesendet hat. |

Der Inbound-Handler von rousseau (`ResolveInbound` in `internal/transport/whatsapp/resolve.go`) normalisiert jedes Ereignis vor der Weitergabe auf eine kanonische Form:

1. **Device-Suffix entfernen.** `447900:5@s.whatsapp.net` wird zu `447900@s.whatsapp.net`. Damit passen Allowlists, die als reine Benutzer-JIDs geschrieben sind, unabhängig davon, welches gekoppelte Gerät die Nachricht gesendet hat.
2. **LID gegen die Telefon-JID des Konto-Inhabers im Selbst-Chat ersetzen.** Ist der Konto-Inhaber der Absender (`IsFromMe=true`), meldet WhatsApp den Absender als die LID des Kontos (einen Privacy-Hash), nicht als Telefon-JID. Rousseau setzt die eigene JID des Kontos ein, damit Betreiber `<phone>@s.whatsapp.net` auf die Allowlist setzen können und Selbst-Chat-Tests korrekt geroutet werden.
3. **Nicht parsbare Absender verwerfen.** Leere `User`- oder `Server`-Felder – entdeckt durch `FuzzResolveInbound` – lassen sich nicht sicher routen. Die Nachricht wird stillschweigend übersprungen, statt mit einer defekten From-Angabe an den Handler zu gehen.

### Selbst-Chat-Falle

Wenn Sie sich in WhatsApp selbst eine Nachricht schicken (um den Bot zu testen), kommt das Sender-Feld als Ihre LID. Wenn Sie Ihre Telefon-JID auf die Allowlist gesetzt haben, würde die naive Prüfung fehlschlagen. Die Ersetzung von rousseau – `if evt.Info.IsFromMe && ownID != nil { from = ownID.ToNonAD() }` – behebt dies.

### Schleifen-Verhinderung

`IsFromMe=true` feuert auch für Nachrichten, die von *diesem* gekoppelten Gerät gesendet wurden (rousseaus ausgehende Antworten, die zurückkehren). Der Transport verwirft diese, wenn die Geräte-ID passt:

```go
if evt.Info.IsFromMe && ownID != nil && evt.Info.Sender.Device == ownID.Device {
    return Resolved{Skip: SkipOwnDevice}
}
```

Nachrichten von *anderen* gekoppelten Geräten des Kontos (z.B. das Primärhandy, das "Nachricht an dich selbst" testet) tragen `IsFromMe=true`, aber eine andere Geräte-ID – diese werden regulär verarbeitet.

## Allowlist-Regex-Muster

Das `--allow`-Flag akzeptiert exakte Strings, keine Regex – rousseau führt einen Case-Insensitive-Gleichheitsvergleich in `router.go` durch. Wenn Sie Muster-Matching wollen, nutzen Sie die Config-Datei mit `pattern`-Modus (analog zu Approval-Richtlinien):

```yaml
whatsapp:
  allowlist:
    - "447900123456@s.whatsapp.net"
    - "447900654321@s.whatsapp.net"
```

Für Gruppen (`<hash>@g.us`) fügen Sie diese analog hinzu. Um alle aus einer bestimmten Ländervorwahl zuzulassen, benötigen Sie eine eigene `Router.Allow`-Implementierung – der eingebaute Enforcer führt bewusst kein Präfix-Matching durch.

<aside class="admonition" data-type="warning"><span class="admonition-title">Leere Allowlist</span><p>Eine leere Allowlist akzeptiert jeden Absender. Betreiben Sie keinen Chat-Transport ohne Allowlist auf einer öffentlichen Nummer – jeder, der die Nummer kennt, wird zum Operator Ihres Agenten.</p></aside>

## Reply-Header

Jede ausgehende Nachricht wird mit einem Header versehen, damit der Absender weiss, mit welchem Bot er spricht. Der Standard:

```
💎 *Rousseau Agent*

<Nachrichtentext>
```

WhatsApp rendert `*text*` als fett. Überschreiben in der Config:

```yaml
whatsapp:
  reply_header: "🤖 *Coding-Bot*\n\n"
```

Setzen Sie ihn auf ein einzelnes Leerzeichen `" "`, um das Präfix vollständig zu deaktivieren.

## Sprachnachrichten-Transkription

Eingehende Sprachnachrichten werden über `whisper.cpp` transkribiert, wenn der Betreiber sich dafür entscheidet. Standardmässig aus, da die Installation der `whisper`-CLI erforderlich ist.

```yaml
whatsapp:
  voice:
    enabled: true
    binary: whisper
    model: base.en
    language: en
    extra_args:
      - --threads
      - "4"
```

| Feld | Wirkung |
|---|---|
| `enabled` | Schalter. Aus bedeutet: Audio-Nachrichten werden geloggt und übersprungen. |
| `binary` | Whisper-CLI-Executable. Leer nutzt Standard `whisper`. |
| `model` | Übergeben an `--model` (`base.en`, `small`, `medium`). |
| `model_path` | Expliziter `.bin`-Pfad. Hat Vorrang vor `model`. |
| `language` | Übergeben an `--language`. Leer erkennt automatisch. |
| `extra_args` | Wird an jeden Aufruf angehängt. |

Der transkribierte Text wird dem Agenten übergeben, als hätte der Benutzer ihn getippt.

## Container-Bereitstellung

Die Referenz-Podman-Quadlet-Unit (`docker/rousseau-agent.container`) mountet das State-Verzeichnis lesend/schreibend, damit das Pairing Neustarts übersteht:

```
Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
```

`Network=pasta` gibt dem Container einen rootless nur-ausgehenden Stack. Whatsmeow benötigt keine erhöhten Capabilities; `DropCapability=all` ist unproblematisch.

## Ablauf der Sprachnachrichten-Transkription

Wenn eine Sprachnachricht eintrifft, gibt der Standard-Resolver `SkipEmptyText` zurück (kein Text-Inhalt). `Dispatch` erkennt dies speziell für Audio-Nachrichten und – falls ein `Transcriber` konfiguriert ist – durchläuft folgenden Pfad:

```
Eingehende Audio-Nachricht
  │
  ├── Downloader.Download(ctx, audioMsg)
  │     • bytes []byte, mimetype string, err error
  │     • Loggt whatsapp.audio_downloaded bei Erfolg
  │
  ├── Transcriber.Transcribe(ctx, audio, mimetype)
  │     • Gibt Klartext-Transkription zurück
  │     • Loggt whatsapp.transcribed mit Dauer
  │
  └── Wiedereintritt in handleTextMessage mit der Transkription als `Body`
```

Ist kein Transkribierer konfiguriert, loggt der Daemon `whatsapp.audio_ignored reason=transcriber_not_configured` und verwirft die Nachricht. Sprachnachrichten lösen nie eine "Stille"-Antwort aus – ein leerer Eingang erzeugt einen leeren Ausgang.

## Medien-Downloads

Die `Downloader`-Schnittstelle ist absichtlich klein:

```go
type Downloader interface {
    Download(ctx context.Context, msg DownloadableAudio) (bytes []byte, mimetype string, err error)
}
```

Derzeit ist nur der Audio-Download verdrahtet. Bild- und Video-Downloads sind auf der Roadmap – sie treffen als `waProto.ImageMessage` / `VideoMessage` ein und benötigten eine korrespondierende `DownloadableMedia`-Schnittstelle. Verfolgen Sie den Plan unter [`docs/GAP_ANALYSIS_2026.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/docs/GAP_ANALYSIS_2026.md).

## Tipp-Indikatoren

Der Handler umhüllt jede Antwort mit `SendPresence(Composing, Paused)`-Aufrufen, damit der Absender den "…schreibt"-Indikator sieht, während das Modell nachdenkt. Beide Aufrufe haben ein 5-Sekunden-Timeout und sind Best-Effort – ein Presence-Fehler blockiert die Antwort nie.

## Fehlermodi

| Symptom | Lösung |
|---|---|
| QR wird bei jedem Neustart erneut ausgegeben | Das Pairing wurde vom Handy widerrufen; `whatsapp.db` löschen und neu paaren. |
| WhatsApp-Reconnect-Schleife | Uhrzeitabweichung gegen `pool.ntp.org` prüfen – der whatsmeow-Handshake ist zeitkritisch. |
| Eingehende Nachrichten werden ignoriert | Prüfen, ob der Absender in der `--allow`-Liste steht; Logs auf `router.transport.rejected` durchsuchen. |
| Meta sperrt die Nummer | Nicht auf einer persönlichen Nummer betreiben. Das Protokoll ist inoffiziell. |
| Selbst-Chat-"hello" wird nicht geroutet | Selbst-Chat nutzt LID; rousseau ersetzt für die Allowlist-Prüfung durch die Telefon-JID. Verifizieren Sie, dass `ownID` initialisiert ist – der Daemon loggt `whatsapp.connected`, sobald dies der Fall ist. |
| Sprachnachrichten werden stillschweigend verworfen | Entweder `whatsapp.voice.enabled: false` oder das `whisper`-Binary fehlt. Log-Zeile: `whatsapp.audio_ignored`. |
| Jede Antwort kommt doppelt zurück | Schleifen-Verhinderung ist deaktiviert. Stellen Sie sicher, dass Sie einen aktuellen Build betreiben; der Fix ist in `ResolveInbound` früh im whatsmeow-Multi-Device-Rollout gelandet. |

## Fehlerbehebung

### QR wird ausgegeben, aber die Handy-App lehnt ihn ab

Drei häufige Ursachen: (1) Ein teilweise abgeschlossenes vorheriges Pairing hat `whatsapp.db` in einem Zustand hinterlassen, den whatsmeow nicht wiederverwenden kann – Datei löschen und neu scannen; (2) die Uhr weicht um mehr als 30 Sekunden ab (häufig in Containern ohne NTP) – prüfen mit `timedatectl status`; (3) eine ältere `whatsmeow`-Version kann ein Meta-Protokoll-Update verpasst haben.

### `whatsapp.connected` dann `whatsapp.disconnected` in Schleife

Uhrzeitabweichung, oder Meta hat das Pairing invalidiert. Prüfen Sie `whatsapp.logged_out`-Ereignisse im Log – das ist das definitive Signal.

### Sprachnachrichten kommen an, werden aber nie transkribiert

Das Transkribierer-Binary ist nicht auflösbar. Prüfen Sie `whatsapp.voice.binary` und `whatsapp.voice.model_path` – beide müssen auf existierende Dateien zeigen (oder `binary` muss auf `PATH` liegen).

### Allowlist-Regex passt nicht

Die Allowlist von rousseau ist Exact-String, nicht Regex. Um einen Bereich von Absendern zu matchen, listen Sie jeden explizit oder fügen Sie einen eigenen Router hinzu.

### Reply-Header erscheint als literales `*`-Zeichen

Der Client des Empfängers rendert kein WhatsApp-Markdown. Dies ist ein Client-seitiges Rendering-Problem; nutzen Sie Klartext, wenn Ihre Empfänger auf älteren Clients sind.

## Verwandte Seiten

- [Getting Started: Erster Transport](/de/getting-started/first-transport/) – End-to-End-Durchlauf.
- [Benutzerhandbuch: Voice-Modus](/de/user-guide/voice-mode/) – Deep-Dive Sprachnachrichten.
- [Konfiguration](/de/configuration/) – der `whatsapp`-Config-Block.
- [Transports](/de/transports/) – die anderen acht Transports.
- [Bereitstellung](/de/deployment/) – WhatsApp in einem Podman-Container betreiben.

## Weiterführende Lektüre

- `internal/transport/whatsapp/client.go` – Connect, QR-Pairing, Event-Pump.
- `internal/transport/whatsapp/resolve.go` – LID/JID-Normalisierung und Selbst-Chat-Handling.
- `internal/transport/whatsapp/dispatch.go` – Dispatch eingehender Nachrichten mit Sprachnachrichten-Verzweigung.
- `internal/transport/whatsapp/whisper.go` – Referenz-Transkribierer whisper-cpp.
- `internal/cli/whatsapp.go` – CLI-Verdrahtung, Store-DSN, Transkribierer-Auswahl.
