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
description: "Configure the AWS Bedrock provider: standard credential chain, region and model ID format, required IAM permissions."
keywords: "Bedrock, AWS, SigV4, IAM, InvokeModel, InvokeModelWithResponseStream, Claude on AWS"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/pt-BR/providers/bedrock/"
subtitle: "Anthropic's Claude models on AWS."
tags: "providers, bedrock, AWS"
title: "Provedor AWS Bedrock"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Bedrock, AWS, SigV4, IAM, InvokeModel, InvokeModelWithResponseStream, Claude on AWS"
news_language: "pt-BR"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Provedor AWS Bedrock"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 8
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS do rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/bedrock/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/bedrock/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Provedor AWS Bedrock"
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
twitter_description: "Configure the AWS Bedrock provider: standard credential chain, region and model ID format, required IAM permissions."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Provedor AWS Bedrock"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">O que você vai aprender</span><p>Como configurar o provider Bedrock com a cadeia de credenciais AWS, a política IAM de menor privilégio, assumption de role cross-account, endpoints VPC para conectividade privada e a matriz de disponibilidade de modelos por região. Leia <code>internal/llm/bedrock/client.go</code> junto a esta página.</p></aside>

## Quando usar o Bedrock

O provider `bedrock` é a escolha certa quando:

- Você está na AWS e quer Claude cobrado através do Bedrock em vez da API Anthropic.
- Você precisa de autenticação SigV4 via cadeia de credenciais AWS padrão (variáveis de ambiente, `~/.aws/credentials`, IMDS, IRSA no EKS).
- Você quer manter o tráfego do modelo dentro de uma única região AWS por razões de residência de dados.
- Você precisa rotear o tráfego do modelo através de um endpoint VPC para que ele nunca toque a internet pública.
- Você quer acesso cross-account via `sts:AssumeRole`.

## Configuração

```yaml
provider: bedrock

bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
  profile: default
  max_tokens: 4096
```

| Campo | Padrão | Efeito |
|---|---|---|
| `region` | *obrigatório* | Região AWS. A disponibilidade de modelos Bedrock é regional; verifique o console AWS. |
| `model` | *obrigatório* | ID do modelo Bedrock. IDs Anthropic Claude seguem o formato `anthropic.claude-<name>-<date>-<version>:<revision>`. |
| `profile` | *vazio* | Perfil de credenciais de `~/.aws/credentials`. Vazio recorre à cadeia de credenciais padrão. |
| `max_tokens` | padrão do SDK | Limita os tokens de saída por completion. |

## Cadeia de credenciais

O provider constrói um cliente Bedrock via `awsconfig.LoadDefaultConfig`, que percorre a cadeia padrão em ordem:

1. Ambiente (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`).
2. Arquivo de credenciais compartilhado (`~/.aws/credentials`), estreitado por `profile` se definido.
3. Arquivo de configuração compartilhado (`~/.aws/config`).
4. IAM Roles for Tasks (ECS) / IAM Roles Anywhere.
5. EC2 IMDS (v2).
6. IRSA — o IAM role anexado a uma service account do Kubernetes (EKS).

Nenhum desses é configurado através do rousseau; o SDK trata da resolução.

## Permissões IAM necessárias

A política mínima que o caller deve poder assumir:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-sonnet-4-6-*"
    }
  ]
}
```

Restrinja o `Resource` à família de modelo específica que você planeja invocar. Wildcards mais amplos funcionam mas geralmente são exagerados.

## Formato de wire

O provider envia o corpo JSON padrão de mensagens Anthropic (`anthropic_version`, `messages`, `system`, `tools`, `max_tokens`) para `bedrock:InvokeModel`, e recebe o mesmo formato de volta. Isso espelha a API direta da Anthropic — uso de tools, stop reasons e contadores de uso são os mesmos.

O streaming usa `bedrock:InvokeModelWithResponseStream` com o decoder de event-stream do SDK.

## Streaming

O provider implementa `agent.StreamingProvider`. O streaming é usado automaticamente no `rousseau chat`.

## Uso de tools

Definições de tools do `Registry` são convertidas para o JSON de tools do Bedrock em `internal/llm/bedrock/client.go`. Políticas de aprovação se aplicam.

## Padrão de autenticação por implantação

<div class="tabs" data-tabs="bedrock-auth">
  <div class="tab-list" role="tablist" aria-label="Bedrock auth deployment">
    <button role="tab" aria-selected="true">Laptop</button>
    <button role="tab" aria-selected="false">EC2</button>
    <button role="tab" aria-selected="false">EKS (IRSA)</button>
    <button role="tab" aria-selected="false">Cross-account</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Para dev local, use um perfil nomeado com SSO ou chaves de longa duração:

```sh
aws configure sso --profile rousseau-dev
aws sso login --profile rousseau-dev
```

```yaml
bedrock:
  region: us-east-1
  profile: rousseau-dev
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

O `profile:` é honrado porque o rousseau passa `awsconfig.WithSharedConfigProfile(cfg.Profile)` quando não-vazio (veja `internal/llm/bedrock/client.go` linha 63). Omita `profile` para recorrer à cadeia padrão.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Anexe um instance profile com permissão `bedrock:InvokeModel` (veja a política IAM abaixo), depois deixe `profile` vazio:

```yaml
bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

O SDK resolve credenciais do IMDS v2 automaticamente. Sem variáveis de ambiente, sem arquivo de perfil necessário.

<aside class="admonition" data-type="note"><span class="admonition-title">IMDS v2</span><p>Garanta que a instância esteja configurada para exigir IMDS v2 (hop limit 2, tokens obrigatórios). O AWS Go SDK v2 trata da dança de tokens de forma transparente, mas requer alcance de rede ao <code>169.254.169.254</code>.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

IAM Roles for Service Accounts (IRSA) é o padrão recomendado no EKS. Anexe um role à service account do pod:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rousseau
  namespace: agents
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/rousseau-bedrock
```

A trust policy do role o vincula ao OIDC provider do EKS e à service account. Veja [Guias: Implantação em Kubernetes](/pt-BR/guides/kubernetes-deployment/) para o exemplo completo.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

O rousseau vive na Conta A, o Bedrock vive na Conta B. Configure uma role assumption:

`~/.aws/config`:

```ini
[profile rousseau]
role_arn = arn:aws:iam::222222222222:role/rousseau-bedrock
source_profile = default
region = us-east-1
```

O role alvo na Conta B tem `bedrock:InvokeModel` no modelo, e uma trust policy permitindo que o principal da Conta A o assuma. Então:

```yaml
bedrock:
  region: us-east-1
  profile: rousseau
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

O SDK trata do roundtrip STS `AssumeRole` de forma transparente.

  </div>
</div>

## Política IAM de menor privilégio

A política mínima que o caller deve poder assumir:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-sonnet-4-6-*"
    }
  ]
}
```

Restrinja o `Resource` à família de modelo específica. Wildcards mais amplos funcionam mas concedem mais do que o necessário. Para throughput provisionado, adicione o ARN do seu modelo provisionado como um segundo recurso.

Trust policy para cross-account (Conta B, o lado que hospeda o modelo):

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "AWS": "arn:aws:iam::111111111111:role/rousseau-caller" },
    "Action": "sts:AssumeRole",
    "Condition": { "StringEquals": { "sts:ExternalId": "rousseau-prod" } }
  }]
}
```

`ExternalId` é exigido pelo guidance de segurança da AWS para acesso cross-account de terceiros.

## Endpoints VPC

Para implantações que não devem alcançar a internet pública, crie um endpoint VPC de interface para o Bedrock na sua VPC:

```sh
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-0123456789abcdef0 \
  --vpc-endpoint-type Interface \
  --service-name com.amazonaws.us-east-1.bedrock-runtime \
  --subnet-ids subnet-aaa subnet-bbb \
  --security-group-ids sg-xxx
```

O AWS SDK resolverá automaticamente através do endpoint se o security group e a route table permitirem. Nenhuma alteração de configuração no lado do rousseau é necessária — isto é transparente para o provider.

<aside class="admonition" data-type="warning"><span class="admonition-title">Políticas de endpoint</span><p>Anexe uma resource policy ao endpoint para restringir quais principals e ações ele aceita. Um endpoint totalmente aberto anula o benefício de isolamento.</p></aside>

## Disponibilidade de modelos por região

A disponibilidade muda conforme a AWS lança novos snapshots. Snapshot em meados de 2026:

| Modelo | us-east-1 | us-west-2 | eu-west-2 | eu-central-1 | ap-southeast-1 | ap-northeast-1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Claude Sonnet 4.6 | sim | sim | sim | sim | sim | sim |
| Claude Opus 4.6 | sim | sim | limitado | limitado | não | não |
| Claude Haiku 4.6 | sim | sim | sim | sim | sim | sim |

<aside class="admonition" data-type="note"><span class="admonition-title">Verifique o console</span><p>A disponibilidade muda sem aviso. A fonte autoritativa é o console do Bedrock em <em>Foundation models &gt; Model access</em> — onde você também precisa solicitar acesso explicitamente antes de o modelo se tornar chamável, mesmo que a região o suporte.</p></aside>

## Armadilhas

- **IDs de modelo mudam por região.** `anthropic.claude-sonnet-4-6-20260101-v1:0` em `us-east-1` pode ser um snapshot diferente em `eu-west-2`. Verifique o console do Bedrock.
- **O acesso deve ser concedido por modelo.** Mesmo com o IAM permitindo `InvokeModel`, o Bedrock requer que você clique em *Model access &gt; Request access* no console antes de a primeira chamada ter sucesso.
- **Throttling.** O Bedrock impõe limites de concorrência por conta e por modelo (tokens por minuto e requisições por minuto). Defina `max_tokens` conservadoramente.
- **Throughput provisionado.** Se você tem throughput provisionado, passe o ID do modelo provisionado (`arn:aws:bedrock:us-east-1:<account>:provisioned-model/…`) como `model`.
- **Falhas no decoder de streaming.** O formato de event-stream mudou sutilmente entre versões do SDK. Fixe `aws-sdk-go-v2/service/bedrockruntime` em uma versão conhecida como boa e re-teste a cada bump.

## Solução de problemas

### `AccessDeniedException: You don't have access to the model`

Duas checagens separadas: (1) a política IAM do caller permite `bedrock:InvokeModel` no ARN do modelo, e (2) a conta solicitou explicitamente acesso ao modelo no console do Bedrock. O item 2 pega a maioria dos usuários de primeira vez.

### `ValidationException: The model ID isn't valid`

A string do ID do modelo não corresponde a um modelo disponível na região configurada. Copie o ID exato do console do Bedrock (*Providers &gt; Anthropic &gt; Model catalog*) em vez de digitá-lo — os sufixos de data e versão devem casar exatamente.

### `ThrottlingException`

Você atingiu uma cota de tokens ou requisições por minuto. Opções: (1) solicite um aumento de cota de serviço, (2) enfileire chamadas no caller com backoff exponencial, (3) mude para throughput provisionado.

### `bedrock: parse response: json:` — JSON mal-formado

O corpo da resposta não está no formato esperado Anthropic-on-Bedrock. Geralmente indica que um modelo não-Anthropic foi passado como `model`; `buildBedrockBody` em `internal/llm/bedrock/client.go` só produz o formato de wire da Anthropic.

### Endpoint VPC inalcançável — `dial tcp: no route to host`

O pod/instância não consegue alcançar as ENIs do endpoint. Verifique o security group no endpoint (deve permitir a porta 443 do SG do caller), a route table da subnet do endpoint e a resolução DNS (o endpoint requer DNS privado habilitado na VPC).

## Páginas relacionadas

- [Providers: Anthropic](/pt-BR/providers/anthropic/) — mesmo formato de wire, caminho de API direta.
- [Guias: Implantação em Kubernetes](/pt-BR/guides/kubernetes-deployment/) — configuração de IRSA.
- [Guias: Enterprise onboarding](/pt-BR/guides/enterprise-onboarding/) — checklist de time de plataforma.
- [Guias: Rate limits](/pt-BR/guides/rate-limits/) — manual de throttling.
- [Segurança](/pt-BR/security/) — limites de confiança e egresso de rede.

## Leitura complementar

- `internal/llm/bedrock/client.go` — `Complete`, conversão de mensagem, tipos de wire.
- `internal/config/config.go` — struct `BedrockConfig`.
- Docs AWS: [Amazon Bedrock IAM permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html).
- Docs AWS: [Bedrock interface VPC endpoints](https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html).
