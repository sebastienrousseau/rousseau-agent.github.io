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
description: "Rousseau-agent ships zero telemetry. No analytics endpoint, no crash-report upload, no license server, no unique identifiers."
keywords: "telemetry, privacy, no phone home, no analytics, no license server"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/guides/telemetry/"
subtitle: "Keine Analytik, kein Phone-home. Verifizierbar."
tags: "guides, telemetry, privacy, security"
title: "Leitfaden: Telemetrie"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "telemetry, privacy, no phone home, no analytics, no license server"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Leitfaden: Telemetrie"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 40
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/telemetry/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/telemetry/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Leitfaden: Telemetrie"
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
twitter_description: "Rousseau-agent ships zero telemetry. No analytics endpoint, no crash-report upload, no license server, no unique identifiers."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Leitfaden: Telemetrie"
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

## Die Zusage

Rousseau-agent liefert keinerlei Telemetrie aus. Die Liste der Dinge, die rousseau explizit **nicht** tut:

- Kein Analytics-Endpunkt. Es gibt kein `metrics.rousseau-agent.dev` oder Äquivalent.
- Kein Crash-Report-Upload. Panics landen in stderr; nichts wird irgendwohin hochgeladen.
- Kein Lizenzserver. Es gibt keinen periodischen Check-in und keine Sitzplatzverifikation.
- Kein eindeutiger Installationsbezeichner. Das Binary ist byteidentisch über jede Installation desselben Tags.
- Kein Feature-Flag-Dienst. Jeder Schalter in rousseau steht in `config.yaml` oder ist ein CLI-Flag.
- Kein Update-Ping. `rousseau version` ist eine lokale Abfrage; es gibt keinen „Nach Updates suchen"-Roundtrip.

## Wie verifizieren

Das rousseau-Binary ist Open Source (MIT, siehe `LICENSE`). Jeder Netzwerkaufruf ist grep-bar:

```sh
grep -rn 'http.Get\|http.Post\|http.Client\|http.NewRequest\|net/http' \
  /path/to/rousseau-agent/internal/ | head
```

Jeder Treffer landet in einer dieser Kategorien:

| Paket | Zweck |
|---|---|
| `internal/llm/anthropic/` | Anthropic-API-Aufrufe (via offizielles SDK). |
| `internal/llm/openai/` | OpenAI-kompatible Endpunkt-Aufrufe. |
| `internal/transport/telegram/` | Telegram-Bot-API. |
| `internal/transport/matrix/` | Matrix-Client-Server-API. |
| `internal/transport/whatsapp/` | Whatsmeow-Websockets zu Meta. |
| `internal/transport/slack/`, `discord/` | Socket Mode / Discord Gateway. |
| `internal/transport/imessage/` | BlueBubbles-Server (in Ihrem LAN). |
| `internal/transport/sms/` | Twilio / Vonage. |
| `internal/transport/email/` | IMAP + SMTP. |

Keine davon ist ein Analytics-Endpunkt. Jeder einzelne ist entweder der von Ihnen konfigurierte LLM-Provider oder der von Ihnen aktivierte Transport.

Betreiben Sie den Daemon unter `strace -e network` oder beobachten Sie ihn mit `ss -tanp` — die einzigen Sockets, die Sie sehen werden, gehen zu den oben aufgeführten Endpunkten.

## Strukturierte Protokollierung ist lokal

Rousseau verwendet `log/slog` (`internal/cli/root.go`). Standardmäßig schreibt der Handler nach stderr, was unter der Quadlet-Unit im systemd-Journal landet. Nichts wird vom Host weggestreamt. Wenn Sie Logs an Loki, Datadog oder anderswohin ausliefern möchten, konfigurieren Sie diese Pipeline selbst — siehe [Leitfäden: Observability](/de/guides/observability/).

## Vergleich

| Produkt | Analytics | Crash-Upload | Lizenzserver |
|---|---|---|---|
| rousseau-agent | keine | keiner | keiner |
| Anbieter A (typischer SaaS-Coding-Assistent) | ja | ja | ja |
| Anbieter B (verwaltete Control Plane) | ja | opt-out | ja |

Das Betriebsmodell von rousseau lautet: Sie bringen den LLM-Schlüssel mit, Sie hosten den Daemon. Es gibt kein Teilstück von rousseau, das auf von Sebastien kontrollierten Servern läuft.

## Was rousseau _tatsächlich_ an LLM-Provider sendet

Per Definition sieht dieser Provider den Nachrichteninhalt, wenn Sie Nachrichten durch Anthropic, Bedrock, Vertex, OpenAI oder eine andere API leiten. Das ist der Natur der LLM-Inferenz eigen — rousseau ist ein Client, kein Shim.

Zwei Mitigationen, falls Ihnen die Datenhandhabung des Providers wichtig ist:

1. **Betreiben Sie gegen ein selbst gehostetes Modell.** Ollama, vLLM, LM Studio oder jeden OpenAI-kompatiblen Endpunkt. Nichts verlässt Ihre Maschine. Siehe [Leitfäden: Selbst gehostetes vLLM](/de/guides/self-hosted-vllm/).
2. **Verwenden Sie Bedrock oder Vertex in einer Region mit einem Data-Processing-Addendum.** Sowohl AWS als auch GCP veröffentlichen regionsspezifische Datenaufenthaltsgarantien.

## Was die WhatsApp-Bridge sieht

Das inoffizielle WhatsApp-Web-Protokoll, das von whatsmeow implementiert wird, spricht mit Metas Servern — dieser Datenverkehr liegt außerhalb der Kontrolle von rousseau. Meta sieht Ihre Nachrichten auf dieselbe Weise wie beim WhatsApp-Web-Zugriff aus einem Browser. Wenn es nicht akzeptabel ist, dass Meta Ihre Nachrichten sieht, betreiben Sie die WhatsApp-Bridge nicht.

Der whatsmeow-Client ist öffentlich auditierbar — jedes Paket ist dokumentiert; es sind keine rousseau-spezifischen Netzwerkaufrufe darüber gelegt.

## Verwandt

- [Sicherheit](/de/security/) — Vertrauensgrenzen und Audit-Haltung.
- [Datenschutz](/de/privacy/) — Datenschutzhaltung auf Site-Ebene.
- [Provider: OpenAI-kompatibel](/de/providers/openai-compatible/) — selbst gehostete Inferenz.
- [Leitfäden: Selbst gehostetes vLLM](/de/guides/self-hosted-vllm/) — ein durchgearbeitetes Beispiel.
