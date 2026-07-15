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
hreflang: "es"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "es"
locale: "es_ES"
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
permalink: "https://docs.rousseau-agent.dev/es/providers/vertex/"
subtitle: "Anthropic's Claude models on Vertex AI."
tags: "providers, vertex, GCP"
title: "Proveedor Google Vertex AI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Vertex, Google Cloud, GCP, Application Default Credentials, ADC, service account, aiplatform, endpoints, predict"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Proveedor Google Vertex AI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 9
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/vertex/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/vertex/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Proveedor Google Vertex AI"
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
twitter_title: "Proveedor Google Vertex AI"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Gracias a cada operador que ejecuta su propio agente de codificación."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">Qué aprenderás</span><p>Configuración paso a paso de cuenta de servicio con comandos <code>gcloud</code>, cuándo usar Workload Identity Federation en su lugar, la matriz de regiones de Vertex para modelos de Anthropic y los modos de fallo para respuestas 401/403/429. Lee <code>internal/llm/vertex/client.go</code> junto a esta página.</p></aside>

## Cuándo usar Vertex

El proveedor `vertex` es la elección correcta cuando:

- Estás en Google Cloud y quieres Claude facturado a través de Vertex AI.
- Quieres autenticar vía un JSON de cuenta de servicio o Application Default Credentials (ADC).
- Necesitas residencia de datos dentro de una región GCP específica.
- Quieres enrutar vía Private Google Access y nunca tocar Internet público.
- Ya tienes Workload Identity Federation configurada para cargas de trabajo GKE.

## Configuración

```yaml
provider: vertex

vertex:
  project: my-gcp-project
  region: us-central1
  model: claude-sonnet-4-6@20260101
  credentials_file: ~/.config/gcloud/vertex-key.json
  max_tokens: 4096
```

| Campo | Por defecto | Efecto |
|---|---|---|
| `project` | *requerido* | ID del proyecto GCP (no el número numérico del proyecto). |
| `region` | *requerido* | Región de Vertex. Anthropic en Vertex está disponible en un subconjunto de regiones; consulta la consola de GCP. |
| `model` | *requerido* | ID de modelo Anthropic en Vertex, por ejemplo `claude-sonnet-4-6@20260101`. Ten en cuenta el sufijo `@fecha`. |
| `credentials_file` | *vacío* | Ruta a una clave JSON de cuenta de servicio o de usuario autorizado. Vacío usa ADC. |
| `max_tokens` | `4096` | Limita los tokens de salida. |

## Diseño del endpoint

Las solicitudes llegan a:

```
https://<region>-aiplatform.googleapis.com/v1/
    projects/<project>/locations/<region>/publishers/anthropic/
    models/<model>:rawPredict
```

`rousseau` construye esta URL a partir de `project`, `region` y `model`; no la sobrescribas.

## Credenciales

Dos rutas soportadas:

### 1. `credentials_file` explícito

Apunta a una clave JSON de cuenta de servicio o un JSON de usuario autorizado (de `gcloud auth application-default login`):

```yaml
vertex:
  credentials_file: /home/rousseau/.config/gcloud/vertex-sa.json
```

El proveedor llama a `google.CredentialsFromJSONWithParams` internamente porque el archivo puede ser una forma `service_account` o `authorized_user`. `CredentialsParams{Scopes: [cloud-platform]}` es fijo.

### 2. Application Default Credentials

Deja `credentials_file` vacío y el proveedor recorre ADC:

1. Variable de entorno `GOOGLE_APPLICATION_CREDENTIALS`.
2. `~/.config/gcloud/application_default_credentials.json` (de `gcloud auth application-default login`).
3. Servidor de metadatos de GCE / GKE (Workload Identity es el patrón recomendado en clúster).

## IAM requerido

Otorga a la identidad llamadora `roles/aiplatform.user` — o el permiso más estrecho `aiplatform.endpoints.predict` — sobre el proyecto.

Ejemplo de Workload Identity para una cuenta de servicio de GKE:

```sh
gcloud projects add-iam-policy-binding my-gcp-project \
  --member "serviceAccount:my-gcp-project.svc.id.goog[default/rousseau-sa]" \
  --role   "roles/aiplatform.user"
```

## Streaming

El proveedor implementa `agent.StreamingProvider` usando el mismo endpoint `rawPredict` con la variante SSE.

## Uso de herramientas

Las definiciones de herramientas del `Registry` se convierten al JSON de herramientas Anthropic de Vertex en `internal/llm/vertex/client.go`. Las políticas de aprobación aplican.

## Configuración de cuenta de servicio, paso a paso

<div class="tabs" data-tabs="vertex-auth">
  <div class="tab-list" role="tablist" aria-label="Vertex auth pattern">
    <button role="tab" aria-selected="true">JSON de cuenta de servicio</button>
    <button role="tab" aria-selected="false">Workload Identity (GKE)</button>
    <button role="tab" aria-selected="false">WIF desde AWS/Azure</button>
    <button role="tab" aria-selected="false">ADC de usuario (dev)</button>
  </div>
  <div class="tab-panel" role="tabpanel">

El patrón más simple para hosts on-prem o no-GKE. Crea una cuenta de servicio dedicada, otorga el rol mínimo, descarga una clave JSON y apunta rousseau al archivo.

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

<aside class="admonition" data-type="caution"><span class="admonition-title">Rotación de claves</span><p>Las claves JSON de cuenta de servicio nunca expiran. Rótalas al menos cada 90 días. Prefiere Workload Identity Federation (abajo) para no tener que gestionar nunca una clave estática.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

El patrón recomendado para GKE. Enlaza una cuenta de servicio de Kubernetes a una cuenta de servicio de Google para que los pods hereden credenciales vía el servidor de metadatos — sin claves JSON en disco.

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

Anota la cuenta de servicio de Kubernetes:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rousseau
  namespace: agents
  annotations:
    iam.gke.io/gcp-service-account: rousseau-vertex@my-gcp-project.iam.gserviceaccount.com
```

Luego deja `credentials_file` vacío — ADC toma las credenciales del servidor de metadatos de GKE automáticamente.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Workload Identity Federation permite que roles de IAM de AWS o identidades gestionadas de Azure llamen a APIs de GCP sin una clave de cuenta de servicio. Útil para despliegues multi-cloud.

Crea la identidad federada:

```sh
gcloud iam workload-identity-pools create rousseau-pool \
  --location=global --project=$PROJECT

gcloud iam workload-identity-pools providers create-aws rousseau-aws \
  --location=global \
  --workload-identity-pool=rousseau-pool \
  --account-id=<AWS_ACCOUNT_ID>
```

Enlaza el rol de AWS a la GSA:

```sh
gcloud iam service-accounts add-iam-policy-binding \
  "${GSA}@${PROJECT}.iam.gserviceaccount.com" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/rousseau-pool/attribute.aws_role/arn:aws:iam::${AWS_ACCOUNT_ID}:role/rousseau"
```

Exporta `GOOGLE_APPLICATION_CREDENTIALS` a un archivo JSON de origen de credenciales que instruye al SDK a intercambiar el rol de AWS por un token de GCP. Consulta la [documentación de WIF de GCP](https://cloud.google.com/iam/docs/workload-identity-federation) para la forma del origen de credenciales.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Para desarrollo local, usa tus propias credenciales de usuario vía `gcloud`:

```sh
gcloud auth application-default login
gcloud auth application-default set-quota-project my-gcp-project
```

Esto escribe `~/.config/gcloud/application_default_credentials.json`. Deja `credentials_file` vacío y rousseau lo lee vía ADC.

<aside class="admonition" data-type="warning"><span class="admonition-title">Nunca en producción</span><p>El ADC de usuario enlaza las solicitudes a tu identidad y cuota personal. No despliegues un servicio con ADC de usuario en producción — cambia a una cuenta de servicio o Workload Identity.</p></aside>

  </div>
</div>

## Matriz de regiones

Los modelos de Anthropic en Vertex tienen alcance regional. La disponibilidad cambia a medida que Google despliega nuevos snapshots. A mediados de 2026:

| Modelo | us-central1 | us-east5 | europe-west1 | europe-west4 | asia-southeast1 |
|---|:---:|:---:|:---:|:---:|:---:|
| `claude-sonnet-4-6` | sí | sí | sí | sí | sí |
| `claude-opus-4-6` | sí | limitado | limitado | sí | no |
| `claude-haiku-4-6` | sí | sí | sí | sí | sí |

La fuente autoritativa es el Vertex Model Garden — *Model Garden &gt; Anthropic &gt; Region availability*. Solicitar acceso es instantáneo; no hay paso de aprobación manual (a diferencia de Bedrock).

## Conectividad privada

Para despliegues que no deben tener egress a Internet público, usa Private Google Access en la VPC y configura DNS para resolver `*-aiplatform.googleapis.com` a `restricted.googleapis.com`. La URL de endpoint de Vertex que rousseau construye sigue funcionando, pero el tráfico permanece en el backbone de Google.

Consulta la [documentación de Private Google Access de GCP](https://cloud.google.com/vpc/docs/private-google-access) para la configuración de la zona DNS.

## Gotchas

- **Formato del ID de modelo.** Vertex usa `@fecha` (`claude-sonnet-4-6@20260101`), Bedrock usa `-<fecha>-v1:0`, Anthropic directo usa `claude-sonnet-4-6`. No pegues uno en el otro.
- **Disponibilidad de región.** No todo modelo de Anthropic está en toda región. `us-central1` y `europe-west4` son las comunes.
- **Cuota.** La cuota de Vertex es por proyecto, por región, por modelo. Si tropiezas con una cuota, las solicitudes darán 429; habilita backoff exponencial en el llamador.
- **Cadena `anthropic_version`.** rousseau envía `vertex-2023-10-16` (consulta `buildVertexBody` en `internal/llm/vertex/client.go`). Si Anthropic actualiza la anthropic_version de Vertex, los builds antiguos de rousseau darán 400.
- **User-agent requerido.** Algunos endpoints de Vertex rechazan solicitudes sin User-Agent. El Go SDK establece uno automáticamente; si inyectas un `HTTPClient` personalizado, preserva el header User-Agent.

## Solución de problemas

### `vertex: HTTP 401 unauthorized`

La cadena de credenciales no devolvió credenciales válidas. Causas comunes: la ruta de `credentials_file` no legible dentro del contenedor, la variable `GOOGLE_APPLICATION_CREDENTIALS` apuntando a un archivo faltante, o `gcloud auth application-default login` nunca ejecutado. Verifica con `gcloud auth application-default print-access-token`.

### `vertex: HTTP 403 permission denied on resource`

La identidad está autenticada pero carece de `aiplatform.endpoints.predict` sobre el proyecto. Otorga `roles/aiplatform.user` (o el permiso más estrecho) y espera ~30 segundos para la propagación de IAM.

### `vertex: HTTP 404 not found`

El ID del modelo no existe en la región. Verifica el sufijo `@fecha` desde el Vertex Model Garden y confirma que la región muestre el modelo en la matriz de disponibilidad.

### `vertex: HTTP 429 resource exhausted`

Cuota excedida. Opciones: (1) solicitar un aumento de cuota vía la consola de IAM, (2) encolar llamadas en el llamador con backoff, (3) dividir el tráfico entre varias regiones.

### `vertex: credentials: could not find default credentials`

ADC no tiene nada que recorrer. O bien establece `credentials_file` explícitamente, `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json`, o (para GKE) confirma que Workload Identity esté habilitado en el clúster y que la KSA esté anotada correctamente.

## Páginas relacionadas

- [Proveedores: Anthropic](/es/providers/anthropic/) — mismo formato de cable, API directa.
- [Proveedores: Bedrock](/es/providers/bedrock/) — Claude gestionado por AWS.
- [Guías: Despliegue de Kubernetes](/es/guides/kubernetes-deployment/) — configuración de Workload Identity.
- [Guías: Onboarding empresarial](/es/guides/enterprise-onboarding/) — checklist para equipo de plataforma.
- [Seguridad](/es/security/) — fronteras de confianza y egress de red.

## Lectura adicional

- `internal/llm/vertex/client.go` — construcción de URL de endpoint, manejo de ADC, tipos de cable.
- `internal/llm/vertex/oauth2.go` — construcción del cliente HTTP OAuth2.
- `internal/config/config.go` — struct `VertexConfig`.
- Documentación de GCP: [Anthropic en Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude).
- Documentación de GCP: [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation).
