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
hreflang: "pt-BR"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "pt-BR"
locale: "pt_BR"
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
permalink: "https://docs.rousseau-agent.dev/pt-BR/providers/vertex/"
subtitle: "Anthropic's Claude models on Vertex AI."
tags: "providers, vertex, GCP"
title: "Provedor Google Vertex AI"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Vertex, Google Cloud, GCP, Application Default Credentials, ADC, service account, aiplatform, endpoints, predict"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Provedor Google Vertex AI"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 9
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/vertex/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/vertex/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Provedor Google Vertex AI"
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
twitter_title: "Provedor Google Vertex AI"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Obrigado a cada operador que executa seu próprio agente de codificação."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>Configuração passo a passo de service account com comandos <code>gcloud</code>, quando usar Workload Identity Federation, a matriz de regiões Vertex para modelos Anthropic e os modos de falha para respostas 401/403/429. Leia <code>internal/llm/vertex/client.go</code> junto a esta página.</p></aside>

## Quando usar o Vertex

O provider `vertex` é a escolha certa quando:

- Você está no Google Cloud e quer Claude cobrado através do Vertex AI.
- Você quer autenticar via um JSON de service-account ou Application Default Credentials (ADC).
- Você precisa de residência de dados dentro de uma região GCP específica.
- Você quer rotear via Private Google Access e nunca tocar a internet pública.
- Você já tem Workload Identity Federation configurado para cargas de trabalho GKE.

## Configuração

```yaml
provider: vertex

vertex:
  project: my-gcp-project
  region: us-central1
  model: claude-sonnet-4-6@20260101
  credentials_file: ~/.config/gcloud/vertex-key.json
  max_tokens: 4096
```

| Campo | Padrão | Efeito |
|---|---|---|
| `project` | *obrigatório* | ID do projeto GCP (não o número numérico do projeto). |
| `region` | *obrigatório* | Região Vertex. Anthropic-on-Vertex está disponível em um subconjunto de regiões; verifique o console GCP. |
| `model` | *obrigatório* | ID do modelo Anthropic-on-Vertex, ex.: `claude-sonnet-4-6@20260101`. Note o sufixo `@date`. |
| `credentials_file` | *vazio* | Caminho para uma chave JSON de service-account ou authorized-user. Vazio usa ADC. |
| `max_tokens` | `4096` | Limita os tokens de saída. |

## Layout de endpoint

As requisições atingem:

```
https://<region>-aiplatform.googleapis.com/v1/
    projects/<project>/locations/<region>/publishers/anthropic/
    models/<model>:rawPredict
```

O `rousseau` constrói essa URL a partir de `project`, `region` e `model`; não sobrescreva.

## Credenciais

Dois caminhos suportados:

### 1. `credentials_file` explícito

Aponte para uma chave JSON de service-account ou um JSON de authorized-user (de `gcloud auth application-default login`):

```yaml
vertex:
  credentials_file: /home/rousseau/.config/gcloud/vertex-sa.json
```

O provider chama `google.CredentialsFromJSONWithParams` por baixo dos panos porque o arquivo pode ser tanto um `service_account` quanto um formato `authorized_user`. `CredentialsParams{Scopes: [cloud-platform]}` é fixo.

### 2. Application Default Credentials

Deixe `credentials_file` vazio e o provider percorre o ADC:

1. Variável de ambiente `GOOGLE_APPLICATION_CREDENTIALS`.
2. `~/.config/gcloud/application_default_credentials.json` (de `gcloud auth application-default login`).
3. Servidor de metadata do GCE / GKE (Workload Identity é o padrão recomendado in-cluster).

## IAM necessário

Conceda à identidade chamadora `roles/aiplatform.user` — ou a permissão mais estreita `aiplatform.endpoints.predict` — no projeto.

Exemplo de Workload Identity para uma service account GKE:

```sh
gcloud projects add-iam-policy-binding my-gcp-project \
  --member "serviceAccount:my-gcp-project.svc.id.goog[default/rousseau-sa]" \
  --role   "roles/aiplatform.user"
```

## Streaming

O provider implementa `agent.StreamingProvider` usando o mesmo endpoint `rawPredict` com a variante SSE.

## Uso de tools

Definições de tools do `Registry` são convertidas para o JSON de Anthropic-tool do Vertex em `internal/llm/vertex/client.go`. Políticas de aprovação se aplicam.

## Configuração de service account, passo a passo

<div class="tabs" data-tabs="vertex-auth">
  <div class="tab-list" role="tablist" aria-label="Vertex auth pattern">
    <button role="tab" aria-selected="true">JSON de service-account</button>
    <button role="tab" aria-selected="false">Workload Identity (GKE)</button>
    <button role="tab" aria-selected="false">WIF de AWS/Azure</button>
    <button role="tab" aria-selected="false">ADC de usuário (dev)</button>
  </div>
  <div class="tab-panel" role="tabpanel">

O padrão mais simples para hosts on-prem ou não-GKE. Crie uma service account dedicada, conceda o role mínimo, baixe uma chave JSON e aponte o rousseau para o arquivo.

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

<aside class="admonition" data-type="caution"><span class="admonition-title">Rotação de chave</span><p>Chaves JSON de service-account nunca expiram. Rotacione-as pelo menos a cada 90 dias. Prefira Workload Identity Federation (abaixo) para nunca precisar gerenciar uma chave estática.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

O padrão recomendado para GKE. Vincule uma service account Kubernetes a uma service account Google para que os pods herdem credenciais via servidor de metadata — sem chaves JSON em disco.

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

Faça a annotation da service account Kubernetes:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rousseau
  namespace: agents
  annotations:
    iam.gke.io/gcp-service-account: rousseau-vertex@my-gcp-project.iam.gserviceaccount.com
```

Depois deixe `credentials_file` vazio — o ADC pega credenciais do servidor de metadata GKE automaticamente.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Workload Identity Federation permite que roles IAM AWS ou identidades gerenciadas Azure chamem APIs GCP sem uma chave de service-account. Útil para implantações multi-cloud.

Crie a identidade federada:

```sh
gcloud iam workload-identity-pools create rousseau-pool \
  --location=global --project=$PROJECT

gcloud iam workload-identity-pools providers create-aws rousseau-aws \
  --location=global \
  --workload-identity-pool=rousseau-pool \
  --account-id=<AWS_ACCOUNT_ID>
```

Vincule o role AWS à GSA:

```sh
gcloud iam service-accounts add-iam-policy-binding \
  "${GSA}@${PROJECT}.iam.gserviceaccount.com" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/rousseau-pool/attribute.aws_role/arn:aws:iam::${AWS_ACCOUNT_ID}:role/rousseau"
```

Exporte `GOOGLE_APPLICATION_CREDENTIALS` para um arquivo JSON de credential-source que instrua o SDK a trocar o role AWS por um token GCP. Veja a [documentação do WIF do GCP](https://cloud.google.com/iam/docs/workload-identity-federation) para o formato do credential-source.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Para desenvolvimento local, use suas próprias credenciais de usuário via `gcloud`:

```sh
gcloud auth application-default login
gcloud auth application-default set-quota-project my-gcp-project
```

Isto grava `~/.config/gcloud/application_default_credentials.json`. Deixe `credentials_file` vazio e o rousseau o lerá via ADC.

<aside class="admonition" data-type="warning"><span class="admonition-title">Nunca em produção</span><p>O ADC de usuário vincula requisições à sua identidade e cota pessoais. Não implante um daemon com ADC de usuário em produção — mude para uma service account ou Workload Identity.</p></aside>

  </div>
</div>

## Matriz de regiões

Modelos Anthropic no Vertex são escopados por região. A disponibilidade muda conforme o Google lança novos snapshots. Em meados de 2026:

| Modelo | us-central1 | us-east5 | europe-west1 | europe-west4 | asia-southeast1 |
|---|:---:|:---:|:---:|:---:|:---:|
| `claude-sonnet-4-6` | sim | sim | sim | sim | sim |
| `claude-opus-4-6` | sim | limitado | limitado | sim | não |
| `claude-haiku-4-6` | sim | sim | sim | sim | sim |

A fonte autoritativa é o Vertex Model Garden — *Model Garden &gt; Anthropic &gt; Region availability*. Solicitar acesso é instantâneo; não há passo manual de aprovação (ao contrário do Bedrock).

## Conectividade privada

Para implantações que não devem fazer egresso à internet pública, use Private Google Access na VPC e configure o DNS para resolver `*-aiplatform.googleapis.com` para `restricted.googleapis.com`. A URL do endpoint Vertex que o rousseau constrói ainda funciona, mas o tráfego permanece no backbone do Google.

Veja [documentação do Private Google Access do GCP](https://cloud.google.com/vpc/docs/private-google-access) para a configuração da zona DNS.

## Armadilhas

- **Formato do ID de modelo.** O Vertex usa `@date` (`claude-sonnet-4-6@20260101`), o Bedrock usa `-<date>-v1:0`, a Anthropic direta usa `claude-sonnet-4-6`. Não cole um no outro.
- **Disponibilidade de região.** Nem todo modelo Anthropic está em toda região. `us-central1` e `europe-west4` são as comuns.
- **Cota.** A cota Vertex é por projeto, por região, por modelo. Ultrapasse uma cota e requisições retornarão 429; habilite backoff exponencial no caller.
- **String `anthropic_version`.** O rousseau envia `vertex-2023-10-16` (veja `buildVertexBody` em `internal/llm/vertex/client.go`). Se a Anthropic subir a anthropic_version do Vertex, builds mais antigas do rousseau darão 400.
- **User-agent obrigatório.** Alguns endpoints Vertex rejeitam requisições sem um User-Agent. O Go SDK define um automaticamente; se você injetar um `HTTPClient` customizado, preserve o header User-Agent.

## Solução de problemas

### `vertex: HTTP 401 unauthorized`

A cadeia de credenciais não retornou credenciais válidas. Causas comuns: caminho de `credentials_file` ilegível dentro do contêiner, env `GOOGLE_APPLICATION_CREDENTIALS` apontando para um arquivo ausente, ou `gcloud auth application-default login` nunca executado. Verifique com `gcloud auth application-default print-access-token`.

### `vertex: HTTP 403 permission denied on resource`

A identidade está autenticada, mas não tem `aiplatform.endpoints.predict` no projeto. Conceda `roles/aiplatform.user` (ou a permissão mais estreita) e espere ~30 segundos pela propagação do IAM.

### `vertex: HTTP 404 not found`

O ID do modelo não existe na região. Verifique novamente o sufixo `@date` no Vertex Model Garden e confirme que a região mostra o modelo na matriz de disponibilidade.

### `vertex: HTTP 429 resource exhausted`

Cota excedida. Opções: (1) solicite um aumento de cota via console IAM, (2) enfileire chamadas no caller com backoff, (3) divida o tráfego entre múltiplas regiões.

### `vertex: credentials: could not find default credentials`

O ADC não tem nada por onde caminhar. Ou defina `credentials_file` explicitamente, `export GOOGLE_APPLICATION_CREDENTIALS=/path/to/sa.json`, ou (para GKE) confirme que o Workload Identity está habilitado no cluster e a KSA está anotada corretamente.

## Páginas relacionadas

- [Providers: Anthropic](/pt-BR/providers/anthropic/) — mesmo formato de wire, API direta.
- [Providers: Bedrock](/pt-BR/providers/bedrock/) — Claude gerenciado pela AWS.
- [Guias: Implantação em Kubernetes](/pt-BR/guides/kubernetes-deployment/) — configuração de Workload Identity.
- [Guias: Enterprise onboarding](/pt-BR/guides/enterprise-onboarding/) — checklist de time de plataforma.
- [Segurança](/pt-BR/security/) — limites de confiança e egresso de rede.

## Leitura complementar

- `internal/llm/vertex/client.go` — construção de URL de endpoint, tratamento de ADC, tipos de wire.
- `internal/llm/vertex/oauth2.go` — construção de HTTP-client OAuth2.
- `internal/config/config.go` — struct `VertexConfig`.
- Docs GCP: [Anthropic on Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-claude).
- Docs GCP: [Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation).
