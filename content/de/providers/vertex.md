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
description: "Configure the Vertex AI provider: Application Default Credentials or an explicit service-account JSON, region and model ID, required IAM roles."
keywords: "Vertex, Google Cloud, GCP, Application Default Credentials, ADC, service account, aiplatform, endpoints, predict"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/providers/vertex/"
subtitle: "Anthropic's Claude models on Vertex AI."
tags: "providers, vertex, GCP"
title: "Google-Vertex-AI-Anbieter"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Vertex, Google Cloud, GCP, Application Default Credentials, ADC, service account, aiplatform, endpoints, predict"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Google-Vertex-AI-Anbieter"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 9
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/vertex/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/vertex/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Google-Vertex-AI-Anbieter"
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
twitter_description: "Configure the Vertex AI provider: Application Default Credentials or an explicit service-account JSON, region and model ID, required IAM roles."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Google-Vertex-AI-Anbieter"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Schritt-für-Schritt-Einrichtung eines Service-Accounts mit <code>gcloud</code>-Befehlen, wann Sie stattdessen Workload Identity Federation nutzen sollten, die Vertex-Regionen-Matrix für Anthropic-Modelle sowie die Fehlermodi bei 401-/403-/429-Antworten. Lesen Sie <code>internal/llm/vertex/client.go</code> parallel zu dieser Seite.</p></aside>

## Wann Vertex verwenden

Der `vertex`-Provider ist die richtige Wahl, wenn:

- Sie auf Google Cloud sind und Claude über Vertex AI abrechnen wollen.
- Sie sich über ein Service-Account-JSON oder Application Default Credentials (ADC) authentifizieren wollen.
- Sie Datenresidenz innerhalb einer spezifischen GCP-Region benötigen.
- Sie über Private Google Access routen und das öffentliche Internet nie berühren wollen.
- Sie bereits Workload Identity Federation für GKE-Workloads eingerichtet haben.

## Konfiguration

```yaml
provider: vertex

vertex:
  project: my-gcp-project
  region: us-central1
  model: claude-sonnet-4-6@20260101
  credentials_file: ~/.config/gcloud/vertex-key.json
  max_tokens: 4096
```

| Feld | Standard | Wirkung |
|---|---|---|
| `project` | *erforderlich* | GCP-Projekt-ID (nicht die numerische Projekt-Nummer). |
| `region` | *erforderlich* | Vertex-Region. Anthropic-auf-Vertex ist in einer Teilmenge der Regionen verfügbar; prüfen Sie die GCP-Konsole. |
| `model` | *erforderlich* | Anthropic-auf-Vertex-Modell-ID, z.B. `claude-sonnet-4-6@20260101`. Beachten Sie das `@date`-Suffix. |
| `credentials_file` | *leer* | Pfad zu einem Service-Account- oder Authorized-User-JSON-Key. Leer nutzt ADC. |
| `max_tokens` | `4096` | Begrenzt Ausgabe-Tokens. |

## Endpoint-Layout

Anfragen gehen an:

```
https://<region>-aiplatform.googleapis.com/v1/
    projects/<project>/locations/<region>/publishers/anthropic/
    models/<model>:rawPredict
```

`rousseau` baut diese URL aus `project`, `region` und `model`; überschreiben Sie sie nicht.

## Credentials

Zwei unterstützte Wege:

### 1. Explizites `credentials_file`

Zeigen Sie auf einen Service-Account-JSON-Key oder ein Authorized-User-JSON (von `gcloud auth application-default login`):

```yaml
vertex:
  credentials_file: /home/rousseau/.config/gcloud/vertex-sa.json
```

Der Provider ruft intern `google.CredentialsFromJSONWithParams` auf, weil die Datei entweder eine `service_account`- oder `authorized_user`-Form haben kann. `CredentialsParams{Scopes: [cloud-platform]}` ist fest gesetzt.

### 2. Application Default Credentials

Lassen Sie `credentials_file` leer, und der Provider läuft die ADC durch:

1. Umgebungsvariable `GOOGLE_APPLICATION_CREDENTIALS`.
2. `~/.config/gcloud/application_default_credentials.json` (aus `gcloud auth application-default login`).
3. GCE-/GKE-Metadata-Server (Workload Identity ist das empfohlene Muster im Cluster).

## Erforderliches IAM

Weisen Sie der aufrufenden Identität `roles/aiplatform.user` – oder die engere Berechtigung `aiplatform.endpoints.predict` – auf dem Projekt zu.

Workload-Identity-Beispiel für einen GKE-ServiceAccount:

```sh
gcloud projects add-iam-policy-binding my-gcp-project \
  --member "serviceAccount:my-gcp-project.svc.id.goog[default/rousseau-sa]" \
  --role   "roles/aiplatform.user"
```

## Streaming

Der Provider implementiert `agent.StreamingProvider` und nutzt denselben `rawPredict`-Endpoint mit der SSE-Variante.

## Tool-Use

Tool-Definitionen aus der `Registry` werden in `internal/llm/vertex/client.go` in Vertex' Anthropic-Tool-JSON konvertiert. Approval-Richtlinien greifen.

## Service-Account-Einrichtung, Schritt für Schritt

<div class="tabs" data-tabs="vertex-auth">
  <div class="tab-list" role="tablist" aria-label="Vertex auth pattern">
    <button role="tab" aria-selected="true">Service-Account-JSON</button>
    <button role="tab" aria-selected="false">Workload Identity (GKE)</button>
    <button role="tab" aria-selected="false">WIF aus AWS/Azure</button>
    <button role="tab" aria-selected="false">User-ADC (Entwicklung)</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Das einfachste Muster für On-Prem- oder Nicht-GKE-Hosts. Erstellen Sie einen dedizierten Service-Account, weisen Sie die minimale Rolle zu, laden Sie einen JSON-Key herunter und verweisen Sie rousseau auf die Datei.

```sh
PROJECT=my-gcp-project
SA_NAME=rousseau-vertex

gcloud iam service-accounts create $SA_NAME \
  --display-name "rousseau-agent Vertex caller" \
  --project $PROJECT

gcloud projects add-iam-policy-binding $PROJECT \
  --member "serviceAccount:${SA_NAME}@${PROJECT}.iam.gserviceaccount.com" \
  --role   "roles/aiplatform.user"

gcloud iam service-accounts keys create ~/vertex-sa.json \
  --iam-account "${SA_NAME}@${PROJECT}.iam.gserviceaccount.com"
```

```yaml
vertex:
  project: my-gcp-project
  region: europe-west4
  model: claude-sonnet-4-6@20260101
  credentials_file: /etc/rousseau/vertex-sa.json
```

<aside class="admonition" data-type="caution"><span class="admonition-title">Key-Rotation</span><p>Service-Account-JSON-Keys laufen nie ab. Rotieren Sie sie mindestens alle 90 Tage. Bevorzugen Sie Workload Identity Federation (unten), damit Sie nie einen statischen Key verwalten müssen.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Das empfohlene Muster für GKE. Binden Sie einen Kubernetes-ServiceAccount an einen Google-Service-Account, damit Pods Credentials über den Metadata-Server erben – keine JSON-Keys auf der Festplatte.

```sh
PROJECT=my-gcp-project
KSA=rousseau
GSA=rousseau-vertex
NAMESPACE=agents

# Der GSA existiert bereits aus dem vorherigen Schritt. KSA binden:
gcloud iam service-accounts add-iam-policy-binding \
  "${GSA}@${PROJECT}.iam.gserviceaccount.com" \
  --role "roles/iam.workloadIdentityUser" \
  --member "serviceAccount:${PROJECT}.svc.id.goog[${NAMESPACE}/${KSA}]"
```

Annotieren Sie den Kubernetes-ServiceAccount:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rousseau
  namespace: agents
  annotations:
    iam.gke.io/gcp-service-account: rousseau-vertex@my-gcp-project.iam.gserviceaccount.com
```

Lassen Sie dann `credentials_file` leer – ADC übernimmt die Credentials automatisch vom GKE-Metadata-Server.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Workload Identity Federation ermöglicht AWS-IAM-Rollen oder Azure-Managed-Identities, GCP-APIs ohne Service-Account-Key aufzurufen. Nützlich für Multi-Cloud-Bereitstellungen.

Erstellen Sie die föderierte Identität:

```sh
gcloud iam workload-identity-pools create rousseau-pool \
  --location=global --project=$PROJECT

gcloud iam workload-identity-pools providers create-aws rousseau-aws \
  --location=global \
  --workload-identity-pool=rousseau-pool \
  --account-id=<AWS_ACCOUNT_ID>
```

Binden Sie die AWS-Rolle an den GSA:

```sh
gcloud iam service-accounts add-iam-policy-binding \
  "${GSA}@${PROJECT}.iam.gserviceaccount.com" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/rousseau-pool/attribute.aws_role/arn:aws:iam::${AWS_ACCOUNT_ID}:role/rousseau"
```

Exportieren Sie `GOOGLE_APPLICATION_CREDENTIALS` mit dem Verweis auf eine Credential-Source-JSON-Datei, die das SDK anweist, die AWS-Rolle gegen ein GCP-Token zu tauschen. Siehe die [GCP-WIF-Dokumentation](https://cloud.google.com/iam/docs/workload-identity-federation) für die Form der Credential-Source.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Für lokale Entwicklung nutzen Sie Ihre eigenen Benutzer-Credentials via `gcloud`:

```sh
gcloud auth application-default login
gcloud auth application-default set-quota-project my-gcp-project
```

Dies schreibt `~/.config/gcloud/application_default_credentials.json`. Lassen Sie `credentials_file` leer, und rousseau liest sie via ADC.

<aside class="admonition" data-type="warning"><span class="admonition-title">Niemals in Produktion</span><p>User-ADC bindet Anfragen an Ihre persönliche Identität und Ihr Kontingent. Betreiben Sie keinen Daemon mit User-ADC in Produktion – wechseln Sie auf einen Service-Account oder Workload Identity.</p></aside>

  </div>
</div>

## Regionen-Matrix

Anthropic-Modelle auf Vertex sind regionsgebunden. Die Verfügbarkeit ändert sich, während Google neue Snapshots ausrollt. Stand Mitte 2026:

| Modell | us-central1 | us-east5 | europe-west1 | europe-west4 | asia-southeast1 |
|---|:---:|:---:|:---:|:---:|:---:|
| `claude-sonnet-4-6` | ja | ja | ja | ja | ja |
| `claude-opus-4-6` | ja | limitiert | limitiert | ja | nein |
| `claude-haiku-4-6` | ja | ja | ja | ja | ja |

Die massgebliche Quelle ist der Vertex Model Garden – *Model Garden &gt; Anthropic &gt; Region availability*. Der Zugriff wird sofort gewährt; es gibt keinen manuellen Freigabeschritt (anders als bei Bedrock).

## Private Konnektivität

Für Bereitstellungen, die nicht ins öffentliche Internet gehen dürfen, nutzen Sie Private Google Access auf der VPC und konfigurieren DNS so, dass `*-aiplatform.googleapis.com` auf `restricted.googleapis.com` aufgelöst wird. Die von rousseau gebaute Vertex-Endpoint-URL funktioniert weiter, aber der Traffic bleibt auf Googles Backbone.

Siehe die [GCP-Private-Google-Access-Dokumentation](https://cloud.google.com/vpc/docs/private-google-access) für die Einrichtung der DNS-Zone.

## Fallstricke

- **Modell-ID-Format.** Vertex nutzt `@date` (`claude-sonnet-4-6@20260101`), Bedrock nutzt `-<date>-v1:0`, direktes Anthropic nutzt `claude-sonnet-4-6`. Verwechseln Sie diese nicht.
- **Regionsverfügbarkeit.** Nicht jedes Anthropic-Modell ist in jeder Region. `us-central1` und `europe-west4` sind die gängigen.
- **Kontingent.** Vertex-Kontingente sind pro Projekt, pro Region und pro Modell. Wird ein Kontingent gerissen, ergibt sich ein 429; aktivieren Sie exponentiellen Backoff im Aufrufer.
- **`anthropic_version`-String.** rousseau sendet `vertex-2023-10-16` (siehe `buildVertexBody` in `internal/llm/vertex/client.go`). Bumpt Anthropic die Vertex-`anthropic_version`, geben ältere rousseau-Builds 400 zurück.
- **User-Agent erforderlich.** Einige Vertex-Endpunkte lehnen Anfragen ohne User-Agent ab. Das Go-SDK setzt automatisch einen; wenn Sie einen eigenen `HTTPClient` injizieren, erhalten Sie den User-Agent-Header.

## Fehlerbehebung

### `vertex: HTTP 401 unauthorized`

Die Credential-Kette hat keine gültigen Credentials geliefert. Häufige Ursachen: `credentials_file`-Pfad im Container nicht lesbar, `GOOGLE_APPLICATION_CREDENTIALS`-Env verweist auf eine fehlende Datei, oder `gcloud auth application-default login` wurde nie ausgeführt. Verifizieren mit `gcloud auth application-default print-access-token`.

### `vertex: HTTP 403 permission denied on resource`

Die Identität ist authentifiziert, hat aber kein `aiplatform.endpoints.predict` auf dem Projekt. Gewähren Sie `roles/aiplatform.user` (oder die engere Berechtigung) und warten Sie ~30 Sekunden auf die IAM-Propagation.

### `vertex: HTTP 404 not found`

Die Modell-ID existiert in der Region nicht. Prüfen Sie das `@date`-Suffix im Vertex Model Garden und bestätigen Sie, dass die Region das Modell in der Verfügbarkeitsmatrix führt.

### `vertex: HTTP 429 resource exhausted`

Kontingent überschritten. Optionen: (1) Kontingent-Erhöhung über die IAM-Konsole anfordern, (2) Aufrufe im Aufrufer mit Backoff in eine Warteschlange, (3) Traffic über mehrere Regionen splitten.

### `vertex: credentials: could not find default credentials`

ADC hat nichts zu durchlaufen. Setzen Sie entweder `credentials_file` explizit, exportieren Sie `GOOGLE_APPLICATION_CREDENTIALS=/pfad/zu/sa.json` oder (für GKE) bestätigen Sie, dass Workload Identity im Cluster aktiviert ist und der KSA korrekt annotiert wurde.

## Verwandte Seiten

- [Providers: Anthropic](/de/providers/anthropic/) – gleiches Wire-Format, direkte API.
- [Providers: Bedrock](/de/providers/bedrock/) – AWS-verwaltetes Claude.
- [Guides: Kubernetes-Bereitstellung](/de/guides/kubernetes-deployment/) – Workload-Identity-Setup.
- [Guides: Enterprise-Onboarding](/de/guides/enterprise-onboarding/) – Checkliste für das Plattform-Team.
- [Sicherheit](/de/security/) – Vertrauensgrenzen und Netzwerk-Egress.

## Weiterführende Lektüre

- `internal/llm/vertex/client.go` – Aufbau der Endpoint-URL, ADC-Handling, Wire-Typen.
- `internal/llm/vertex/oauth2.go` – OAuth2-HTTP-Client-Aufbau.
- `internal/config/config.go` – `VertexConfig`-Struktur.
- GCP-Dokumentation: [Anthropic on Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude).
- GCP-Dokumentation: [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation).
