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
description: "Wire rousseau-agent's slog JSON output to Loki, Grafana, Datadog, or any log pipeline. OpenTelemetry roadmap notes."
keywords: "observability, slog, json logging, loki, grafana, datadog, opentelemetry"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/guides/observability/"
subtitle: "Slog JSON into your log pipeline. OTel on the roadmap."
tags: "guides, observability, slog, loki, grafana, datadog"
title: "Guide : observabilité"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "observability, slog, json logging, loki, grafana, datadog, opentelemetry"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide : observabilité"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 35
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/observability/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/observability/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Guide : observabilité"
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
twitter_description: "Wire rousseau-agent's slog JSON output to Loki, Grafana, Datadog, or any log pipeline. OpenTelemetry roadmap notes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide : observabilité"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>Les clés d'attributs slog que rousseau émet, les pipelines de logs qui fonctionnent bien avec du JSON structuré (Loki + Grafana, Datadog, Vector, OTel Collector), et une esquisse côté appelant pour le tracing quand l'item OTel de la feuille de route sera livré.</p></aside>

## Ce que rousseau émet

Chaque daemon utilise le package `log/slog` de la bibliothèque standard Go. Choisissez entre deux handlers via `log.format` :

| Valeur | Handler | Cas d'usage |
|---|---|---|
| `text` (défaut) | `slog.NewTextHandler` | `rousseau chat` interactif. Sans couleurs ; compatible grep. |
| `json` | `slog.NewJSONHandler` | Tout daemon en production. Chaque champ est une clé JSON. |

Niveaux : `debug`, `info`, `warn`, `error`.

Configuration en production :

```yaml
log:
  level: info
  format: json
```

## Clés structurées sur lesquelles vous pouvez compter

Les clés suivantes sont porteuses — parsez-les, ne les réécrivez pas. Elles apparaissent dans `internal/cli/` et `internal/agent/` :

| Clé | Émise depuis | Champs | Signification |
|---|---|---|---|
| `tool.execute` | `agent.runTools` | `name`, `id` | Un appel d'outil a été exécuté. |
| `tool.denied` | `agent.runTools` | `name`, `reason` | L'approver a bloqué l'appel. |
| `tool.error` | `agent.runTools` | `name`, `err` | L'outil a été exécuté mais a retourné une erreur. |
| `agent.compressed` | `agent.Turn` | `messages` | La compression de session s'est déclenchée. |
| `agent.compress_failed` | `agent.Turn` | `err` | Le fournisseur de compression a échoué ; la boucle a continué. |
| `whatsapp.starting` | `cli/whatsapp.go` | `store`, `allowlist` | Le bridge WhatsApp a démarré. |
| `whatsapp.voice_enabled` | `cli/whatsapp.go` | `binary`, `model` | Transcription vocale active. |
| `cron.fire` | `internal/cron/scheduler.go` | `name`, `job` | Une tâche cron s'est déclenchée. |
| `cron.deliver` | `internal/cron/scheduler.go` | `name`, `target`, `bytes` | Réponse cron délivrée. |

Chaque ligne de log porte les champs slog standard `time`, `level`, `msg`, ainsi que les attributs ci-dessus.

## Pipelines de logs — choisissez votre stack

<div class="tabs" data-tabs="observability-stack">
  <div class="tab-list" role="tablist" aria-label="Observability stack">
    <button role="tab" aria-selected="true">Loki + Grafana</button>
    <button role="tab" aria-selected="false">Datadog</button>
    <button role="tab" aria-selected="false">Vector</button>
    <button role="tab" aria-selected="false">OTel Collector</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Loki + Promtail + Grafana. Voir la configuration systemd + Promtail sous les onglets. Requête en LogQL :

```
sum by (level) (rate({job="rousseau-agent"} [5m]))
```

Alertes sur les refus d'approbation :

```
count_over_time({job="rousseau-agent"} |= "tool.denied" [15m]) > 5
```

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Datadog Agent avec la source journald ; le parser JSON intégré promeut chaque attribut slog en facette. Voir la configuration sous les onglets.

Monitors :

- `msg:tool.denied` — chaque appel d'outil bloqué.
- `msg:whatsapp.logged_out` — WhatsApp a perdu son pairing.
- `msg:cron.delivery_failed` — la livraison d'une tâche cron a échoué.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Vector en tant qu'agrégateur, avec n'importe quel puits en aval (S3, Kafka, Elasticsearch, etc.). Voir la configuration sous les onglets. Le langage `remap` de Vector permet d'écarter les événements bruyants ou d'ajouter des attributs dérivés sans toucher à rousseau.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Le OpenTelemetry Collector accepte les logs via journald et les transmet à n'importe quel backend OTLP :

```yaml
# otel-collector-config.yaml
receivers:
  journald:
    units: [rousseau-agent.service]

processors:
  transform:
    log_statements:
      - context: log
        statements:
          - merge_maps(cache, ParseJSON(body), "insert")

exporters:
  otlphttp:
    endpoint: https://otel-backend.internal:4318

service:
  pipelines:
    logs:
      receivers: [journald]
      processors: [transform]
      exporters: [otlphttp]
```

Une fois l'item de feuille de route « exporteur OTel » livré au sein de rousseau, on obtient du OTel de bout en bout sans passer par journald.

  </div>
</div>

## Pipeline de logs : Loki + Grafana

### Systemd + Promtail

Faites pointer Promtail sur le journal du service rousseau :

```yaml
# /etc/promtail/promtail.yaml
scrape_configs:
  - job_name: rousseau-agent
    journal:
      matches: _SYSTEMD_USER_UNIT=rousseau-agent.service
      labels: { job: rousseau-agent }
    relabel_configs:
      - source_labels: [__journal__systemd_user_unit]
        target_label: unit
    pipeline_stages:
      - json:
          expressions: { level: level, msg: msg }
      - labels: { level: "" }
```

Les dashboards Grafana peuvent alors filtrer sur `level=WARN` et `msg="tool.denied"` pour construire le panneau « appels d'outils bloqués ».

### Kubernetes

Déployez le Grafana Agent (ou Loki + Alloy) en tant que DaemonSet. Comme rousseau écrit sur stdout dans le conteneur, aucun scraping de fichier n'est requis.

## Pipeline de logs : Datadog

```
# /etc/datadog-agent/conf.d/rousseau.d/conf.yaml
logs:
  - type: journald
    include_units:
      - rousseau-agent.service
    service: rousseau-agent
    source: rousseau-agent
```

Comme rousseau émet du JSON, le parser JSON intégré à Datadog promeut `level`, `msg` et chaque attribut en facettes de premier plan. Configurez un monitor sur `msg:tool.denied` pour les alertes de politique d'approbation.

## Pipeline de logs : Vector

```toml
# /etc/vector/vector.toml
[sources.rousseau_journal]
type = "journald"
include_units = ["rousseau-agent.service"]

[transforms.rousseau_parse]
type = "remap"
inputs = ["rousseau_journal"]
source = '''
. = merge(., parse_json(.message) ?? {})
'''

[sinks.loki]
type = "loki"
inputs = ["rousseau_parse"]
endpoint = "https://loki.internal:3100"
labels = { job = "rousseau-agent", level = "{{ level }}" }
```

## Métriques clés à tracer

Il n'y a pas d'endpoint Prometheus aujourd'hui. Les métriques qui vous intéressent transitent par le flux de logs :

| Métrique | Comment la dériver |
|---|---|
| Débit d'appels d'outils | comptage de `msg:tool.execute` |
| Taux de refus | comptage de `msg:tool.denied` |
| Taux d'erreurs | comptage de `msg:tool.error` |
| Événements de compression | comptage de `msg:agent.compressed` |
| Déclenchements cron | comptage de `msg:cron.fire` |
| Octets délivrés par cron | somme de `bytes` où `msg:cron.deliver` |

Loki + LogQL : `sum by (name) (count_over_time({job="rousseau-agent"} |= "tool.denied" [1h]))`.

## Feuille de route OpenTelemetry

Une intégration OpenTelemetry figure sur la feuille de route. Une fois livrée, attendez-vous à :

- Propagation du contexte `otel.trace` à travers la boucle d'agent (un span par `Turn`, spans enfants par appel d'outil).
- Exporteur de métriques pour les compteurs qui transitent aujourd'hui via les logs.
- Endpoint OTLP configurable via variables d'environnement.

D'ici là, traitez la sortie slog structurée comme le substrat d'observabilité. Chaque événement pour lequel vous voudriez une métrique ou une trace est déjà là — les métadonnées sont complètes, seul le format filaire diffère.

## Débogage sans pipeline de logs

Interactif :

```sh
rousseau --config /etc/rousseau/config.yaml whatsapp \
  --allow 447900123456@s.whatsapp.net 2>&1 | jq
```

Le daemon écrit slog sur stderr ; passer par `jq` fournit un filtre interactif. `jq 'select(.msg == "tool.denied")'` affiche chaque appel bloqué.

`rousseau doctor` est l'autre levier d'observabilité — un instantané de chaque dépendance et de chaque choix de configuration à un instant donné.

## Dépannage

### `journal has no entries`

Le daemon n'a encore rien écrit, ou le matcher journald est incorrect. Confirmez avec `journalctl --user -u rousseau-agent.service --no-pager`.

### Erreurs de parsing JSON dans le pipeline

Rousseau émet une ligne par événement. Si le `msg` d'un événement de log contient un saut de ligne (rare — certains transports incluent des chaînes d'erreur multi-lignes), le pipeline peut le scinder en deux événements. Filtrez avec une regex ou utilisez un parsing structuré qui respecte les sauts de ligne intégrés.

### Attributs manquants en aval

Loki écarte les attributs qu'il ne peut pas mapper à des labels. Utilisez `line_format` en LogQL pour projeter les attributs dans la sortie rendue, ou indexez-les comme labels avec `pipeline_stages.labels`.

### Le tag `service` Datadog est absent

Datadog utilise le champ `service` pour le filtrage. La source journald le renseigne depuis la configuration ; assurez-vous que `service: rousseau-agent` est présent.

### Les dashboards Grafana n'affichent aucune donnée

Vérifiez que la requête LogQL correspond à vos labels. Le label `job` par défaut de Promtail est défini par la configuration de scrape — si vous l'avez modifié, mettez à jour chaque requête de dashboard.

## Pages liées

- [Configuration](/fr/configuration/) — `log.level` et `log.format`.
- [Guides : Audit &amp; politiques d'approbation](/fr/guides/audit-approval-policies/) — les signaux d'alerte les plus utiles.
- [Référence : Codes de sortie](/fr/reference/exit-codes/) — comment le daemon signale un échec aux init systems.
- [Sécurité](/fr/security/) — piste d'audit via slog.
- [Référence : Logs](/fr/reference/logs/) — chaque clé slog émise par rousseau.

## Lectures complémentaires

- `internal/cli/root.go` — `newLogger` positionne le handler slog.
- `internal/agent/agent.go` — événements `tool.execute`, `tool.denied`, `agent.compressed`.
- `internal/transport/whatsapp/dispatch.go` — émission d'événements côté transport.
- Documentation Grafana LogQL et documentation de traitement des logs Datadog (externes).
