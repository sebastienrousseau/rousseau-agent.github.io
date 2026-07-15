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
description: "Configure the Vertex AI provider: Application Default Credentials or an explicit service-account JSON, region and model ID, required IAM roles."
keywords: "Vertex, Google Cloud, GCP, Application Default Credentials, ADC, service account, aiplatform, endpoints, predict"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/providers/vertex/"
subtitle: "Anthropic's Claude models on Vertex AI."
tags: "providers, vertex, GCP"
title: "Fournisseur Google Vertex AI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Vertex, Google Cloud, GCP, Application Default Credentials, ADC, service account, aiplatform, endpoints, predict"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Fournisseur Google Vertex AI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 9
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/vertex/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/vertex/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Fournisseur Google Vertex AI"
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
twitter_title: "Fournisseur Google Vertex AI"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>Configuration pas-à-pas d'un compte de service avec les commandes <code>gcloud</code>, quand privilégier la Workload Identity Federation, la matrice des régions Vertex pour les modèles Anthropic, et les modes d'échec pour les réponses 401/403/429. Lisez <code>internal/llm/vertex/client.go</code> en parallèle de cette page.</p></aside>

## Quand utiliser Vertex

Le provider `vertex` est le bon choix quand :

- Vous êtes sur Google Cloud et voulez faire facturer Claude via Vertex AI.
- Vous voulez vous authentifier via un JSON de compte de service ou Application Default Credentials (ADC).
- Vous avez besoin de résidence des données dans une région GCP précise.
- Vous voulez router par Private Google Access et ne jamais toucher l'internet public.
- Vous avez déjà de la Workload Identity Federation configurée pour vos workloads GKE.

## Configuration

```yaml
provider: vertex

vertex:
  project: my-gcp-project
  region: us-central1
  model: claude-sonnet-4-6@20260101
  credentials_file: ~/.config/gcloud/vertex-key.json
  max_tokens: 4096
```

| Champ | Défaut | Effet |
|---|---|---|
| `project` | *requis* | ID de projet GCP (pas le numéro de projet numérique). |
| `region` | *requis* | Région Vertex. Anthropic-on-Vertex n'est disponible que dans un sous-ensemble de régions ; vérifiez la console GCP. |
| `model` | *requis* | ID de modèle Anthropic-on-Vertex, ex. `claude-sonnet-4-6@20260101`. Notez le suffixe `@date`. |
| `credentials_file` | *vide* | Chemin vers une clé JSON de compte de service ou d'utilisateur autorisé. Vide, utilise ADC. |
| `max_tokens` | `4096` | Plafonne les tokens de sortie. |

## Disposition des endpoints

Les requêtes visent :

```
https://<region>-aiplatform.googleapis.com/v1/
    projects/<project>/locations/<region>/publishers/anthropic/
    models/<model>:rawPredict
```

`rousseau` construit cette URL depuis `project`, `region` et `model` ; ne la surchargez pas.

## Credentials

Deux voies supportées :

### 1. `credentials_file` explicite

Pointez vers une clé JSON de compte de service ou vers un JSON d'utilisateur autorisé (issu de `gcloud auth application-default login`) :

```yaml
vertex:
  credentials_file: /home/rousseau/.config/gcloud/vertex-sa.json
```

Le provider appelle `google.CredentialsFromJSONWithParams` en interne car le fichier peut être soit un `service_account`, soit un `authorized_user`. `CredentialsParams{Scopes: [cloud-platform]}` est fixe.

### 2. Application Default Credentials

Laissez `credentials_file` vide et le provider parcourt ADC :

1. Variable d'environnement `GOOGLE_APPLICATION_CREDENTIALS`.
2. `~/.config/gcloud/application_default_credentials.json` (via `gcloud auth application-default login`).
3. Serveur de métadonnées GCE / GKE (Workload Identity est le pattern recommandé en cluster).

## IAM requis

Accordez à l'identité appelante `roles/aiplatform.user` — ou la permission plus étroite `aiplatform.endpoints.predict` — sur le projet.

Exemple Workload Identity pour un service account GKE :

```sh
gcloud projects add-iam-policy-binding my-gcp-project \
  --member "serviceAccount:my-gcp-project.svc.id.goog[default/rousseau-sa]" \
  --role   "roles/aiplatform.user"
```

## Streaming

Le provider implémente `agent.StreamingProvider` via le même endpoint `rawPredict` en variante SSE.

## Utilisation d'outils

Les définitions d'outils issues du `Registry` sont converties dans le JSON d'outils Anthropic de Vertex via `internal/llm/vertex/client.go`. Les politiques d'approbation s'appliquent.

## Mise en place du compte de service, pas à pas

<div class="tabs" data-tabs="vertex-auth">
  <div class="tab-list" role="tablist" aria-label="Vertex auth pattern">
    <button role="tab" aria-selected="true">JSON de compte de service</button>
    <button role="tab" aria-selected="false">Workload Identity (GKE)</button>
    <button role="tab" aria-selected="false">WIF depuis AWS/Azure</button>
    <button role="tab" aria-selected="false">ADC utilisateur (dev)</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Le pattern le plus simple pour des hôtes on-prem ou hors GKE. Créez un compte de service dédié, accordez le rôle minimum, téléchargez une clé JSON et faites pointer rousseau vers le fichier.

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

<aside class="admonition" data-type="caution"><span class="admonition-title">Rotation des clés</span><p>Les clés JSON de compte de service n'expirent jamais. Rotationnez-les au moins tous les 90 jours. Préférez la Workload Identity Federation (ci-dessous) pour ne jamais avoir à gérer de clé statique.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Le pattern recommandé pour GKE. Liez un service account Kubernetes à un service account Google pour que les pods héritent des credentials via le serveur de métadonnées — aucune clé JSON sur disque.

```sh
PROJECT=my-gcp-project
KSA=rousseau
GSA=rousseau-vertex
NAMESPACE=agents

# GSA already exists from the previous step. Bind the KSA:
gcloud iam service-accounts add-iam-policy-binding \
  "${GSA}@${PROJECT}.iam.gserviceaccount.com" \
  --role "roles/iam.workloadIdentityUser" \
  --member "serviceAccount:${PROJECT}.svc.id.goog[${NAMESPACE}/${KSA}]"
```

Annotate the Kubernetes service account:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rousseau
  namespace: agents
  annotations:
    iam.gke.io/gcp-service-account: rousseau-vertex@my-gcp-project.iam.gserviceaccount.com
```

Puis laissez `credentials_file` vide — ADC récupère les credentials automatiquement depuis le serveur de métadonnées GKE.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

La Workload Identity Federation permet aux rôles AWS IAM ou aux managed identities Azure d'appeler les API GCP sans clé de compte de service. Utile pour les déploiements multi-cloud.

Créez l'identité fédérée :

```sh
gcloud iam workload-identity-pools create rousseau-pool \
  --location=global --project=$PROJECT

gcloud iam workload-identity-pools providers create-aws rousseau-aws \
  --location=global \
  --workload-identity-pool=rousseau-pool \
  --account-id=<AWS_ACCOUNT_ID>
```

Liez le rôle AWS au GSA :

```sh
gcloud iam service-accounts add-iam-policy-binding \
  "${GSA}@${PROJECT}.iam.gserviceaccount.com" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/rousseau-pool/attribute.aws_role/arn:aws:iam::${AWS_ACCOUNT_ID}:role/rousseau"
```

Exportez `GOOGLE_APPLICATION_CREDENTIALS` vers un fichier JSON credential-source qui indique au SDK d'échanger le rôle AWS contre un token GCP. Voir la [doc GCP WIF](https://cloud.google.com/iam/docs/workload-identity-federation) pour la forme du credential-source.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

En dev local, utilisez vos propres credentials utilisateur via `gcloud` :

```sh
gcloud auth application-default login
gcloud auth application-default set-quota-project my-gcp-project
```

Cela écrit `~/.config/gcloud/application_default_credentials.json`. Laissez `credentials_file` vide et rousseau le lit via ADC.

<aside class="admonition" data-type="warning"><span class="admonition-title">Jamais en production</span><p>L'ADC utilisateur lie les requêtes à votre identité personnelle et à votre quota. Ne déployez pas un daemon avec un ADC utilisateur en production — basculez sur un compte de service ou Workload Identity.</p></aside>

  </div>
</div>

## Matrice des régions

Les modèles Anthropic sur Vertex sont scopés par région. La disponibilité évolue au fil des déploiements Google. À mi-2026 :

| Modèle | us-central1 | us-east5 | europe-west1 | europe-west4 | asia-southeast1 |
|---|:---:|:---:|:---:|:---:|:---:|
| `claude-sonnet-4-6` | oui | oui | oui | oui | oui |
| `claude-opus-4-6` | oui | limité | limité | oui | non |
| `claude-haiku-4-6` | oui | oui | oui | oui | oui |

La source faisant foi est le Vertex Model Garden — *Model Garden &gt; Anthropic &gt; Region availability*. La demande d'accès est instantanée ; aucune étape d'approbation manuelle (contrairement à Bedrock).

## Connectivité privée

Pour les déploiements qui ne doivent pas sortir sur l'internet public, activez Private Google Access sur le VPC et configurez le DNS pour que `*-aiplatform.googleapis.com` résolve vers `restricted.googleapis.com`. L'URL d'endpoint Vertex construite par rousseau reste valide, mais le trafic reste sur le backbone de Google.

Voir la [documentation Private Google Access de GCP](https://cloud.google.com/vpc/docs/private-google-access) pour la configuration de la zone DNS.

## Points de vigilance

- **Format d'ID de modèle.** Vertex utilise `@date` (`claude-sonnet-4-6@20260101`), Bedrock utilise `-<date>-v1:0`, Anthropic direct utilise `claude-sonnet-4-6`. Ne collez pas l'un à la place de l'autre.
- **Disponibilité régionale.** Tous les modèles Anthropic ne sont pas dans toutes les régions. `us-central1` et `europe-west4` sont les plus courants.
- **Quota.** Le quota Vertex s'applique par projet, par région et par modèle. Un quota atteint provoque des 429 ; activez le backoff exponentiel côté appelant.
- **Chaîne `anthropic_version`.** rousseau envoie `vertex-2023-10-16` (voir `buildVertexBody` dans `internal/llm/vertex/client.go`). Si Anthropic incrémente la version Vertex anthropic_version, les anciens builds de rousseau retourneront 400.
- **User-Agent requis.** Certains endpoints Vertex refusent les requêtes sans User-Agent. Le SDK Go en fixe un automatiquement ; si vous injectez un `HTTPClient` custom, préservez l'en-tête User-Agent.

## Dépannage

### `vertex: HTTP 401 unauthorized`

La chaîne de credentials n'a rien renvoyé de valide. Causes fréquentes : chemin de `credentials_file` illisible depuis le conteneur, variable `GOOGLE_APPLICATION_CREDENTIALS` pointant vers un fichier absent, ou `gcloud auth application-default login` jamais exécuté. Vérifiez avec `gcloud auth application-default print-access-token`.

### `vertex: HTTP 403 permission denied on resource`

L'identité est authentifiée mais n'a pas `aiplatform.endpoints.predict` sur le projet. Accordez `roles/aiplatform.user` (ou la permission plus étroite) et attendez ~30 secondes pour la propagation IAM.

### `vertex: HTTP 404 not found`

L'ID de modèle n'existe pas dans la région. Revérifiez le suffixe `@date` depuis Vertex Model Garden et confirmez que la région liste le modèle dans la matrice de disponibilité.

### `vertex: HTTP 429 resource exhausted`

Quota dépassé. Options : (1) demandez un relèvement de quota via la console IAM, (2) mettez les appels en file côté appelant avec backoff, (3) répartissez le trafic sur plusieurs régions.

### `vertex: credentials: could not find default credentials`

ADC n'a rien à parcourir. Renseignez `credentials_file` explicitement, `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json`, ou (pour GKE) confirmez que Workload Identity est activé sur le cluster et que le KSA est correctement annoté.

## Pages liées

- [Fournisseurs : Anthropic](/fr/providers/anthropic/) — même format wire, API directe.
- [Fournisseurs : Bedrock](/fr/providers/bedrock/) — Claude géré par AWS.
- [Guides : Déploiement Kubernetes](/fr/guides/kubernetes-deployment/) — configuration Workload Identity.
- [Guides : Onboarding entreprise](/fr/guides/enterprise-onboarding/) — checklist équipe plateforme.
- [Sécurité](/fr/security/) — frontières de confiance et trafic sortant.

## Pour aller plus loin

- `internal/llm/vertex/client.go` — construction d'URL d'endpoint, gestion ADC, types wire.
- `internal/llm/vertex/oauth2.go` — construction du client HTTP OAuth2.
- `internal/config/config.go` — struct `VertexConfig`.
- Docs GCP : [Anthropic sur Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude).
- Docs GCP : [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation).
