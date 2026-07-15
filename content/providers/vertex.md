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
hreflang: "en"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "en-GB"
locale: "en_GB"
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
permalink: "https://docs.rousseau-agent.dev/providers/vertex/"
subtitle: "Anthropic's Claude models on Vertex AI."
tags: "providers, vertex, GCP"
title: "Google Vertex AI Provider"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Vertex, Google Cloud, GCP, Application Default Credentials, ADC, service account, aiplatform, endpoints, predict"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Google Vertex AI Provider"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 9
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/vertex/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/vertex/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Google Vertex AI Provider"
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
twitter_title: "Google Vertex AI Provider"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>Step-by-step service-account setup with <code>gcloud</code> commands, when to use Workload Identity Federation instead, the Vertex region matrix for Anthropic models, and the failure modes for 401/403/429 responses. Read <code>internal/llm/vertex/client.go</code> alongside this page.</p></aside>

## When to use Vertex

The `vertex` provider is the right choice when:

- You are on Google Cloud and want Claude billed through Vertex AI.
- You want to authenticate via a service-account JSON or Application Default Credentials (ADC).
- You need data residency inside a specific GCP region.
- You want to route via Private Google Access and never touch the public internet.
- You already have Workload Identity Federation set up for GKE workloads.

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

| Field | Default | Effect |
|---|---|---|
| `project` | *required* | GCP project ID (not the numeric project number). |
| `region` | *required* | Vertex region. Anthropic-on-Vertex is available in a subset of regions; check the GCP console. |
| `model` | *required* | Anthropic-on-Vertex model ID, e.g. `claude-sonnet-4-6@20260101`. Note the `@date` suffix. |
| `credentials_file` | *empty* | Path to a service-account or authorized-user JSON key. Empty uses ADC. |
| `max_tokens` | `4096` | Caps output tokens. |

## Endpoint layout

Requests hit:

```
https://<region>-aiplatform.googleapis.com/v1/
    projects/<project>/locations/<region>/publishers/anthropic/
    models/<model>:rawPredict
```

`rousseau` builds this URL from `project`, `region`, and `model`; do not override.

## Credentials

Two supported paths:

### 1. Explicit `credentials_file`

Point at a service-account JSON key or an authorized-user JSON (from `gcloud auth application-default login`):

```yaml
vertex:
  credentials_file: /home/rousseau/.config/gcloud/vertex-sa.json
```

The provider calls `google.CredentialsFromJSONWithParams` under the hood because the file may be either a `service_account` or an `authorized_user` shape. `CredentialsParams{Scopes: [cloud-platform]}` is fixed.

### 2. Application Default Credentials

Leave `credentials_file` empty and the provider walks ADC:

1. `GOOGLE_APPLICATION_CREDENTIALS` environment variable.
2. `~/.config/gcloud/application_default_credentials.json` (from `gcloud auth application-default login`).
3. GCE / GKE metadata server (Workload Identity is the recommended pattern in-cluster).

## Required IAM

Grant the calling identity `roles/aiplatform.user` — or the narrower `aiplatform.endpoints.predict` permission — on the project.

Workload Identity example for a GKE service account:

```sh
gcloud projects add-iam-policy-binding my-gcp-project \
  --member "serviceAccount:my-gcp-project.svc.id.goog[default/rousseau-sa]" \
  --role   "roles/aiplatform.user"
```

## Streaming

The provider implements `agent.StreamingProvider` using the same `rawPredict` endpoint with the SSE variant.

## Tool use

Tool definitions from the `Registry` are converted to Vertex's Anthropic-tool JSON in `internal/llm/vertex/client.go`. Approval policies apply.

## Service-account setup, step by step

<div class="tabs" data-tabs="vertex-auth">
  <div class="tab-list" role="tablist" aria-label="Vertex auth pattern">
    <button role="tab" aria-selected="true">Service-account JSON</button>
    <button role="tab" aria-selected="false">Workload Identity (GKE)</button>
    <button role="tab" aria-selected="false">WIF from AWS/Azure</button>
    <button role="tab" aria-selected="false">User ADC (dev)</button>
  </div>
  <div class="tab-panel" role="tabpanel">

The simplest pattern for on-prem or non-GKE hosts. Create a dedicated service account, grant the minimum role, download a JSON key, and point rousseau at the file.

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

<aside class="admonition" data-type="caution"><span class="admonition-title">Key rotation</span><p>Service-account JSON keys never expire. Rotate them at least every 90 days. Prefer Workload Identity Federation (below) so you never have to manage a static key.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

The recommended pattern for GKE. Bind a Kubernetes service account to a Google service account so pods inherit credentials via the metadata server — no JSON keys on disk.

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

Then leave `credentials_file` empty — ADC picks up credentials from the GKE metadata server automatically.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Workload Identity Federation lets AWS IAM roles or Azure managed identities call GCP APIs without a service-account key. Useful for multi-cloud deployments.

Create the federated identity:

```sh
gcloud iam workload-identity-pools create rousseau-pool \
  --location=global --project=$PROJECT

gcloud iam workload-identity-pools providers create-aws rousseau-aws \
  --location=global \
  --workload-identity-pool=rousseau-pool \
  --account-id=<AWS_ACCOUNT_ID>
```

Bind the AWS role to the GSA:

```sh
gcloud iam service-accounts add-iam-policy-binding \
  "${GSA}@${PROJECT}.iam.gserviceaccount.com" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/rousseau-pool/attribute.aws_role/arn:aws:iam::${AWS_ACCOUNT_ID}:role/rousseau"
```

Export `GOOGLE_APPLICATION_CREDENTIALS` to a credential-source JSON file that instructs the SDK to exchange the AWS role for a GCP token. See the [GCP WIF docs](https://cloud.google.com/iam/docs/workload-identity-federation) for the credential-source shape.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

For local development, use your own user credentials via `gcloud`:

```sh
gcloud auth application-default login
gcloud auth application-default set-quota-project my-gcp-project
```

This writes `~/.config/gcloud/application_default_credentials.json`. Leave `credentials_file` empty and rousseau reads it via ADC.

<aside class="admonition" data-type="warning"><span class="admonition-title">Never in production</span><p>User ADC binds requests to your personal identity and quota. Do not deploy a daemon with user ADC in production — switch to a service account or Workload Identity.</p></aside>

  </div>
</div>

## Region matrix

Anthropic models on Vertex are region-scoped. Availability shifts as Google rolls out new snapshots. As of mid-2026:

| Model | us-central1 | us-east5 | europe-west1 | europe-west4 | asia-southeast1 |
|---|:---:|:---:|:---:|:---:|:---:|
| `claude-sonnet-4-6` | yes | yes | yes | yes | yes |
| `claude-opus-4-6` | yes | limited | limited | yes | no |
| `claude-haiku-4-6` | yes | yes | yes | yes | yes |

The authoritative source is the Vertex Model Garden — *Model Garden &gt; Anthropic &gt; Region availability*. Requesting access is instant; there is no manual approval step (unlike Bedrock).

## Private connectivity

For deployments that must not egress to the public internet, use Private Google Access on the VPC and configure DNS to resolve `*-aiplatform.googleapis.com` to `restricted.googleapis.com`. The Vertex endpoint URL rousseau builds still works, but traffic stays on Google's backbone.

See [GCP Private Google Access docs](https://cloud.google.com/vpc/docs/private-google-access) for the DNS zone setup.

## Gotchas

- **Model ID format.** Vertex uses `@date` (`claude-sonnet-4-6@20260101`), Bedrock uses `-<date>-v1:0`, direct Anthropic uses `claude-sonnet-4-6`. Do not paste one into the other.
- **Region availability.** Not every Anthropic model is in every region. `us-central1` and `europe-west4` are the common ones.
- **Quota.** Vertex quota is per-project per-region per-model. Trip a quota and requests will 429; enable exponential backoff at the caller.
- **`anthropic_version` string.** rousseau sends `vertex-2023-10-16` (see `buildVertexBody` in `internal/llm/vertex/client.go`). If Anthropic bumps the Vertex anthropic_version, older rousseau builds will 400.
- **User-agent required.** Some Vertex endpoints reject requests without a User-Agent. The Go SDK sets one automatically; if you inject a custom `HTTPClient`, preserve the User-Agent header.

## Troubleshooting

### `vertex: HTTP 401 unauthorized`

The credential chain returned no valid credentials. Common causes: `credentials_file` path unreadable inside the container, `GOOGLE_APPLICATION_CREDENTIALS` env pointing at a missing file, or `gcloud auth application-default login` never run. Verify with `gcloud auth application-default print-access-token`.

### `vertex: HTTP 403 permission denied on resource`

The identity is authenticated but lacks `aiplatform.endpoints.predict` on the project. Grant `roles/aiplatform.user` (or the narrower permission) and wait ~30 seconds for IAM propagation.

### `vertex: HTTP 404 not found`

The model ID does not exist in the region. Double-check the `@date` suffix from Vertex Model Garden and confirm the region shows the model in the availability matrix.

### `vertex: HTTP 429 resource exhausted`

Quota exceeded. Options: (1) request a quota increase via the IAM console, (2) queue calls in the caller with backoff, (3) split traffic across multiple regions.

### `vertex: credentials: could not find default credentials`

ADC has nothing to walk. Either set `credentials_file` explicitly, `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json`, or (for GKE) confirm Workload Identity is enabled on the cluster and the KSA is annotated correctly.

## Related pages

- [Providers: Anthropic](/providers/anthropic/) — same wire format, direct API.
- [Providers: Bedrock](/providers/bedrock/) — AWS-managed Claude.
- [Guides: Kubernetes deployment](/guides/kubernetes-deployment/) — Workload Identity setup.
- [Guides: Enterprise onboarding](/guides/enterprise-onboarding/) — platform-team checklist.
- [Security](/security/) — trust boundaries and network egress.

## Further reading

- `internal/llm/vertex/client.go` — endpoint URL construction, ADC handling, wire types.
- `internal/llm/vertex/oauth2.go` — OAuth2 HTTP-client construction.
- `internal/config/config.go` — `VertexConfig` struct.
- GCP docs: [Anthropic on Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude).
- GCP docs: [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation).
