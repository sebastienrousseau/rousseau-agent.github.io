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
hreflang: "fr"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "fr"
locale: "fr_FR"
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
description: "rousseau-agent's slog output: message vocabulary, JSON vs text shape, and journalctl / jq recipes."
keywords: "slog, logs, json, text, journalctl, jq, observability"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/reference/logs/"
subtitle: "The full vocabulary of slog messages rousseau emits."
tags: "reference, logs, slog, observability, audit"
title: "Référence : journaux"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "slog, logs, json, text, journalctl, jq, observability"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Référence : journaux"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 52
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/logs/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/logs/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Référence : journaux"
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
twitter_description: "rousseau-agent's slog output: message vocabulary, JSON vs text shape, and journalctl / jq recipes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Référence : journaux"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Configuration du logger

`internal/cli/root.go` construit un `*slog.Logger` par processus — un `slog.NewTextHandler` quand `log.format` est vide ou `text`, un `slog.NewJSONHandler` quand il vaut `json`. Le niveau est mappé depuis `log.level` (`debug`, `info`, `warn`/`warning`, `error`) avec `info` par défaut. Le handler écrit sur stderr ; chaque démon en hérite.

Pour un déploiement en production, mettez toujours `log.format: json`. Les pipelines de logs en aval (journald + `journalctl -o json`, Loki, Vector, Datadog Agent) parsent la sortie structurée nativement.

## Forme de la sortie

### Texte

```
time=2026-07-13T18:00:14.202Z level=INFO msg=tool.execute name=grep id=t_1
```

Layout texte par défaut de slog : `time`, `level`, `msg`, puis paires clé=valeur.

### JSON

```json
{"time":"2026-07-13T18:00:14.202Z","level":"INFO","msg":"tool.execute","name":"grep","id":"t_1"}
```

Mêmes champs, encodés en JSON. Le champ `msg` est l'identifiant d'événement stable — filtrez et alertez dessus, pas sur du texte humain.

## Vocabulaire des messages

Chaque nom de message émis depuis `internal/**/*.go` est listé ci-dessous avec l'emplacement source et le niveau attendu. Groupé par sous-système ; alphabétisé au sein d'un groupe.

### Boucle d'agent (`internal/agent/`)

| Message | Niveau | Champs | Signification |
|---|---|---|---|
| `agent.compressed` | INFO | `messages` | Le compresseur LLM a réécrit une session ; le nouveau nombre de messages est `messages`. |
| `agent.compress_failed` | WARN | `err` | Le compresseur a retourné une erreur ; la session est laissée intacte. |
| `tool.denied` | WARN | `name`, `reason` | L'approbateur a bloqué un appel d'outil. Champs depuis `internal/agent/agent.go:179`. |
| `tool.execute` | INFO | `name`, `id` | L'approbateur a autorisé et l'outil s'est exécuté. |
| `tool.error` | WARN | `name`, `err` | L'outil s'est exécuté mais a renvoyé une erreur. |
| `turn.failed` | ERROR | `err` | Le tour TUI a échoué. Émis depuis `internal/tui/model.go`. |
| `session.save_failed` | WARN | `err` | La persistance d'une session a échoué post-tour. |

### Cron (`internal/cron/scheduler.go`)

| Message | Niveau | Champs | Signification |
|---|---|---|---|
| `cron.started` | INFO | `poll_interval` | Démarrage du planificateur. |
| `cron.scheduled` | INFO | `job`, `expr` | Tâche ajoutée au planning en mémoire. |
| `cron.schedule_failed` | WARN | `job`, `expr`, `err` | robfig/cron/v3 a rejeté l'expression. |
| `cron.sync_failed` | WARN | `err` | La passe de réconciliation contre `cron_jobs` a échoué. |
| `cron.firing` | INFO | `job` | La tâche va s'exécuter. |
| `cron.completed` | INFO | `job` | La tâche s'est terminée avec succès. |
| `cron.run_failed` | ERROR | `job`, `err` | L'appel fournisseur dans la tâche a échoué. |
| `cron.delivery_failed` | ERROR | `job`, `target`, `err` | La livraison au transport a échoué. |
| `cron.record_failed` | WARN | `job`, `err` | L'écriture de `last_run_at` a échoué. |

### MCP (`internal/mcp/server.go`)

| Message | Niveau | Champs | Signification |
|---|---|---|---|
| `mcp.encode_error` | WARN | `err` | Impossible d'encoder une réponse en JSON (rare). |
| `mcp.tool_error` | WARN | `tool`, `err` | Un handler d'outil a renvoyé une erreur ; remontée à l'hôte avec `isError=true`. |

### Router (`internal/transport/router.go`)

| Message | Niveau | Champs | Signification |
|---|---|---|---|
| `transport.rejected` | WARN | `from` | Émetteur absent de l'allowlist ; message rejeté. |
| `router.save_failed` | WARN | `err` | La sauvegarde de session post-tour a échoué. |
| `router.stale_mapping` | WARN | `jid`, `err` | La correspondance JID→session pointait sur une session qui ne se charge plus. |

### WhatsApp (`internal/transport/whatsapp/`)

| Message | Niveau | Champs | Signification |
|---|---|---|---|
| `whatsapp.starting` | INFO | `store`, `allowlist` | Démarrage du pont ; `store` est le DSN. |
| `whatsapp.qr_ready` | INFO | — | QR affiché sur stdout ; scannez-le. |
| `whatsapp.qr_event` | WARN | `event` | Événement QR non réussi depuis whatsmeow. |
| `whatsapp.paired` | INFO | — | Le téléphone a accepté le QR. |
| `whatsapp.connected` | INFO | — | La WebSocket vers Meta est établie. |
| `whatsapp.disconnected` | WARN | — | Socket perdue. Retente automatiquement. |
| `whatsapp.logged_out` | ERROR | `reason` | Meta a déconnecté l'appareil — généralement un déclenchement de politique. |
| `whatsapp.voice_enabled` | INFO | `binary`, `model` | La transcription de notes vocales est activée. |
| `whatsapp.incoming` | INFO | `from` | Message entrant accepté. |
| `whatsapp.skipped` | DEBUG | `reason` | Le routeur a écarté un message (auto-écho, etc.). |
| `whatsapp.empty_reply` | INFO | `elapsed` | L'agent n'a produit aucun texte ce tour. |
| `whatsapp.handler_ok` | INFO | `elapsed`, `bytes` | Réponse livrée. |
| `whatsapp.handler_failed` | ERROR | `err` | Tour en erreur — généralement un échec de fournisseur ou d'outil. |
| `whatsapp.send_failed` | ERROR | `err` | Livraison à Meta échouée. |
| `whatsapp.presence_failed` | DEBUG | `err` | Écriture de présence « en train de taper » échouée (best-effort). |
| `whatsapp.audio_ignored` | INFO | `size` | Note vocale reçue mais transcription désactivée. |
| `whatsapp.audio_downloaded` | INFO | `size` | Octets de note vocale récupérés depuis Meta. |
| `whatsapp.transcribed` | INFO | `elapsed` | whisper.cpp a renvoyé une transcription. |
| `whatsapp.transcribe_failed` | ERROR | `err` | L'invocation whisper a échoué. |

### Slack (`internal/transport/slack/client.go`)

| Message | Niveau | Champs | Signification |
|---|---|---|---|
| `slack.starting` | INFO | `allowlist` | Démarrage du pont. |
| `slack.started` | INFO | — | Session Socket Mode acceptée. |
| `slack.session_failed` | WARN | `err` | Ouverture de la session Socket Mode échouée ; retente. |
| `slack.frame_failed` | WARN | `err` | Frame malformée depuis Slack. |
| `slack.incoming` | INFO | `from`, `channel`, `text` | Message accepté. |
| `slack.handler_failed` | ERROR | `err` | Tour en erreur. |

### Discord (`internal/transport/discord/client.go`)

| Message | Niveau | Champs | Signification |
|---|---|---|---|
| `discord.starting` | INFO | `allowlist` | Démarrage du pont. |
| `discord.ready` | INFO | `bot_id` | Gateway Discord prête. |
| `discord.started` | INFO | — | Session établie. |
| `discord.session_failed` | WARN | `err` | Ouverture de la Gateway échouée ; retente. |
| `discord.frame_failed` | WARN | `err` | Frame incorrecte depuis Discord. |
| `discord.incoming` | INFO | `from`, `channel` | Message accepté. |
| `discord.handler_failed` | ERROR | `err` | Tour en erreur. |

### Telegram (`internal/transport/telegram/client.go`)

| Message | Niveau | Champs | Signification |
|---|---|---|---|
| `telegram.starting` | INFO | `allowlist` | Démarrage du pont. |
| `telegram.started` | INFO | — | Premier long-poll réussi. |
| `telegram.poll_failed` | WARN | `err` | HTTP long-poll échoué. |
| `telegram.incoming` | INFO | `from` | Message accepté. |
| `telegram.handler_failed` | ERROR | `err` | Tour en erreur. |
| `telegram.send_failed` | ERROR | `err` | HTTP sortant échoué. |

### Matrix (`internal/transport/matrix/client.go`)

| Message | Niveau | Champs | Signification |
|---|---|---|---|
| `matrix.starting` | INFO | `homeserver`, `allowlist` | Démarrage du pont. |
| `matrix.started` | INFO | `homeserver` | Premier `/sync` accepté. |
| `matrix.sync_failed` | WARN | `err` | HTTP `/sync` échoué. |
| `matrix.incoming` | INFO | `from`, `room` | Message accepté. |
| `matrix.handler_failed` | ERROR | `err` | Tour en erreur. |
| `matrix.send_failed` | ERROR | `err` | HTTP sortant échoué. |

### Signal (`internal/transport/signal/`)

| Message | Niveau | Champs | Signification |
|---|---|---|---|
| `signal.starting` | INFO | `account`, `allowlist` | Démarrage du sous-processus JSON-RPC signal-cli. |
| `signal.started` | INFO | — | Sous-processus prêt. |
| `signal.frame_failed` | WARN | `err` | Frame JSON malformée depuis signal-cli. |
| `signal.stderr` | WARN | `line` | Passthrough de stderr signal-cli. |
| `signal.incoming` | INFO | `from` | Message accepté. |
| `signal.handler_failed` | ERROR | `err` | Tour en erreur. |

### iMessage (`internal/transport/imessage/client.go`)

| Message | Niveau | Champs | Signification |
|---|---|---|---|
| `imessage.starting` | INFO | `base` | URL du serveur BlueBubbles loggée. |
| `imessage.started` | INFO | `server` | Premier polling réussi. |
| `imessage.prime_failed` | WARN | `err` | Récupération d'amorçage échouée ; retentes. |
| `imessage.poll_failed` | WARN | `err` | HTTP de polling échoué. |
| `imessage.incoming` | INFO | `from` | Message accepté. |
| `imessage.handler_failed` | ERROR | `err` | Tour en erreur. |
| `imessage.send_failed` | ERROR | `err` | HTTP sortant échoué. |

### Email + SMS (`internal/transport/email/`, `internal/transport/sms/`)

Suit la même forme `<transport>.starting / .started / .poll_failed / .incoming / .handler_failed / .send_failed` que les transports par polling ci-dessus.

## Recettes

### Afficher chaque appel d'outil échoué aujourd'hui

```sh
journalctl --user -u rousseau-agent --since today -o json \
  | jq -c 'select(.MESSAGE | fromjson? | .msg == "tool.denied")'
```

### Suivre en direct une session de transport unique

```sh
journalctl --user -u rousseau-agent -f -o cat \
  | grep -E 'whatsapp\.|tool\.|cron\.'
```

### Alerter sur les échecs cron

Esquisse de règle Prometheus/alertmanager (via le pipeline `promtail` → Loki → alerte dans [Guides : Observabilité](/fr/guides/observability/)) :

```yaml
- alert: RousseauCronFailure
  expr: |
    sum by (job) (
      count_over_time({app="rousseau-agent"} |= "cron.run_failed" [5m])
    ) > 0
```

### Rédaction

`slog` ne rédige pas par défaut. Configurez un processeur en aval pour rédiger les champs `err` sur `whatsapp.send_failed`, `tool.error`, etc. — les erreurs de fournisseurs peuvent occasionnellement inclure des fragments de prompt. Voir [Guides : Observabilité](/fr/guides/observability/) pour le pipeline.

## Voir aussi

- [Guide utilisateur : politiques d'approbation](/fr/user-guide/approval-policies/) — la source de `tool.denied`.
- [Guides : Observabilité](/fr/guides/observability/) — recette de pipeline complète.
- [Guides : Audit + politiques d'approbation](/fr/guides/audit-approval-policies/) — traiter ces logs comme une piste d'audit.
