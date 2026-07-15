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
description: "Configure the AWS Bedrock provider: standard credential chain, region and model ID format, required IAM permissions."
keywords: "Bedrock, AWS, SigV4, IAM, InvokeModel, InvokeModelWithResponseStream, Claude on AWS"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/providers/bedrock/"
subtitle: "Anthropic's Claude models on AWS."
tags: "providers, bedrock, AWS"
title: "Fournisseur AWS Bedrock"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Bedrock, AWS, SigV4, IAM, InvokeModel, InvokeModelWithResponseStream, Claude on AWS"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Fournisseur AWS Bedrock"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 8
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/bedrock/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/bedrock/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Fournisseur AWS Bedrock"
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
twitter_title: "Fournisseur AWS Bedrock"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Ce que vous allez apprendre</span><p>Comment configurer le provider Bedrock avec la chaîne de credentials AWS, la politique IAM au moindre privilège, l'assomption de rôle cross-account, les endpoints VPC pour la connectivité privée, et la matrice de disponibilité des modèles par région. Lisez <code>internal/llm/bedrock/client.go</code> en parallèle de cette page.</p></aside>

## Quand utiliser Bedrock

Le provider `bedrock` est le bon choix quand :

- Vous êtes sur AWS et voulez faire facturer Claude via Bedrock plutôt que l'API Anthropic.
- Vous avez besoin d'une authentification SigV4 via la chaîne standard de credentials AWS (variables d'environnement, `~/.aws/credentials`, IMDS, IRSA sur EKS).
- Vous voulez maintenir le trafic modèle à l'intérieur d'une seule région AWS pour des raisons de résidence des données.
- Vous devez router le trafic modèle par un endpoint VPC pour qu'il ne sorte jamais sur l'internet public.
- Vous voulez un accès cross-account via `sts:AssumeRole`.

## Configuration

```yaml
provider: bedrock

bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
  profile: default
  max_tokens: 4096
```

| Champ | Défaut | Effet |
|---|---|---|
| `region` | *requis* | Région AWS. La disponibilité des modèles Bedrock est régionale ; vérifiez la console AWS. |
| `model` | *requis* | ID de modèle Bedrock. Les IDs Claude d'Anthropic suivent la forme `anthropic.claude-<nom>-<date>-<version>:<révision>`. |
| `profile` | *vide* | Profil de credentials depuis `~/.aws/credentials`. Vide, utilise la chaîne standard. |
| `max_tokens` | défaut SDK | Plafonne les tokens de sortie par complétion. |

## Chaîne de credentials

Le provider construit un client Bedrock via `awsconfig.LoadDefaultConfig`, qui parcourt la chaîne standard dans cet ordre :

1. Environnement (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`).
2. Fichier de credentials partagé (`~/.aws/credentials`), restreint par `profile` si renseigné.
3. Fichier de config partagé (`~/.aws/config`).
4. IAM Roles for Tasks (ECS) / IAM Roles Anywhere.
5. IMDS EC2 (v2).
6. IRSA — le rôle IAM attaché à un service account Kubernetes (EKS).

Aucun de ces éléments n'est configuré via rousseau ; le SDK gère la résolution.

## Permissions IAM requises

La politique minimale que l'appelant doit pouvoir endosser :

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

Cadrez le `Resource` sur la famille de modèles précise que vous comptez invoquer. Des wildcards plus larges fonctionnent mais sont généralement excessifs.

## Format wire

Le provider envoie le corps JSON standard des messages Anthropic (`anthropic_version`, `messages`, `system`, `tools`, `max_tokens`) à `bedrock:InvokeModel`, et reçoit la même forme en retour. Cela reflète l'API Anthropic directe — l'utilisation d'outils, les raisons d'arrêt et les compteurs d'usage sont identiques.

Le streaming utilise `bedrock:InvokeModelWithResponseStream` avec le décodeur d'event-stream du SDK.

## Streaming

Le provider implémente `agent.StreamingProvider`. Le streaming est utilisé automatiquement dans `rousseau chat`.

## Utilisation d'outils

Les définitions d'outils issues du `Registry` sont converties dans le JSON d'outils Bedrock via `internal/llm/bedrock/client.go`. Les politiques d'approbation s'appliquent.

## Patron d'authentification par déploiement

<div class="tabs" data-tabs="bedrock-auth">
  <div class="tab-list" role="tablist" aria-label="Bedrock auth deployment">
    <button role="tab" aria-selected="true">Laptop</button>
    <button role="tab" aria-selected="false">EC2</button>
    <button role="tab" aria-selected="false">EKS (IRSA)</button>
    <button role="tab" aria-selected="false">Cross-account</button>
  </div>
  <div class="tab-panel" role="tabpanel">

En dev local, utilisez un profil nommé avec SSO ou des clés long-lived :

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

`profile:` est honoré parce que rousseau passe `awsconfig.WithSharedConfigProfile(cfg.Profile)` quand non vide (voir `internal/llm/bedrock/client.go` ligne 63). Omettez `profile` pour retomber sur la chaîne par défaut.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Attachez un instance profile avec la permission `bedrock:InvokeModel` (voir la politique IAM plus bas), puis laissez `profile` vide :

```yaml
bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

Le SDK résout les credentials depuis IMDS v2 automatiquement. Aucune variable d'environnement ni fichier de profil requis.

<aside class="admonition" data-type="note"><span class="admonition-title">IMDS v2</span><p>Assurez-vous que l'instance est configurée pour exiger IMDS v2 (hop limit 2, tokens requis). Le SDK AWS Go v2 gère la mécanique des tokens de manière transparente mais requiert que <code>169.254.169.254</code> soit joignable.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

IAM Roles for Service Accounts (IRSA) est le pattern recommandé sur EKS. Attachez un rôle au service account du pod :

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rousseau
  namespace: agents
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/rousseau-bedrock
```

La politique de confiance du rôle le lie au provider OIDC EKS et au service account. Voir [Guides : Déploiement Kubernetes](/fr/guides/kubernetes-deployment/) pour l'exemple complet.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau vit dans le compte A, Bedrock dans le compte B. Configurez une assomption de rôle :

`~/.aws/config`:

```ini
[profile rousseau]
role_arn = arn:aws:iam::222222222222:role/rousseau-bedrock
source_profile = default
region = us-east-1
```

Le rôle cible dans le compte B dispose de `bedrock:InvokeModel` sur le modèle, avec une politique de confiance autorisant le principal du compte A à l'endosser. Ensuite :

```yaml
bedrock:
  region: us-east-1
  profile: rousseau
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

Le SDK gère l'aller-retour STS `AssumeRole` de manière transparente.

  </div>
</div>

## Politique IAM au moindre privilège

La politique minimale que l'appelant doit pouvoir endosser :

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

Cadrez le `Resource` sur la famille de modèles précise. Des wildcards plus larges fonctionnent mais accordent plus que nécessaire. Pour du provisioned throughput, ajoutez l'ARN de votre modèle provisionné en tant que deuxième ressource.

Politique de confiance pour le cross-account (compte B, côté hébergement du modèle) :

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

`ExternalId` est requis par les recommandations de sécurité AWS pour l'accès cross-account tiers.

## Endpoints VPC

Pour des déploiements qui ne doivent pas atteindre l'internet public, créez un endpoint VPC de type interface pour Bedrock dans votre VPC :

```sh
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-0123456789abcdef0 \
  --vpc-endpoint-type Interface \
  --service-name com.amazonaws.us-east-1.bedrock-runtime \
  --subnet-ids subnet-aaa subnet-bbb \
  --security-group-ids sg-xxx
```

Le SDK AWS résoudra automatiquement via l'endpoint si le security group et la table de routage l'autorisent. Aucun changement de config côté rousseau n'est nécessaire — c'est transparent pour le provider.

<aside class="admonition" data-type="warning"><span class="admonition-title">Politiques d'endpoint</span><p>Attachez une resource policy à l'endpoint pour restreindre les principals et les actions acceptés. Un endpoint grand ouvert annule le bénéfice d'isolation.</p></aside>

## Disponibilité des modèles par région

La disponibilité évolue au fil des déploiements AWS. Instantané à mi-2026 :

| Modèle | us-east-1 | us-west-2 | eu-west-2 | eu-central-1 | ap-southeast-1 | ap-northeast-1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Claude Sonnet 4.6 | oui | oui | oui | oui | oui | oui |
| Claude Opus 4.6 | oui | oui | limité | limité | non | non |
| Claude Haiku 4.6 | oui | oui | oui | oui | oui | oui |

<aside class="admonition" data-type="note"><span class="admonition-title">Vérifiez la console</span><p>La disponibilité change sans préavis. La source faisant foi est la console Bedrock à <em>Foundation models &gt; Model access</em> — où vous devez aussi demander explicitement l'accès avant que le modèle ne devienne appelable, même si la région le supporte.</p></aside>

## Points de vigilance

- **Les IDs de modèles changent selon la région.** `anthropic.claude-sonnet-4-6-20260101-v1:0` en `us-east-1` peut correspondre à un snapshot différent en `eu-west-2`. Vérifiez la console Bedrock.
- **L'accès doit être accordé par modèle.** Même si l'IAM autorise `InvokeModel`, Bedrock exige de passer par *Model access &gt; Request access* dans la console avant que le premier appel n'aboutisse.
- **Throttling.** Bedrock applique des limites de concurrence par compte et par modèle (tokens par minute et requêtes par minute). Réglez `max_tokens` de manière prudente.
- **Provisioned throughput.** Si vous disposez de provisioned throughput, passez l'ID de modèle provisionné (`arn:aws:bedrock:us-east-1:<compte>:provisioned-model/…`) dans `model`.
- **Échecs du décodeur streaming.** Le format d'event-stream a évolué subtilement entre versions de SDK. Épinglez `aws-sdk-go-v2/service/bedrockruntime` à une version connue et retestez à chaque bump.

## Dépannage

### `AccessDeniedException: You don't have access to the model`

Deux contrôles distincts : (1) la politique IAM de l'appelant autorise `bedrock:InvokeModel` sur l'ARN du modèle, et (2) le compte a explicitement demandé l'accès au modèle dans la console Bedrock. Le point 2 rattrape la plupart des débutants.

### `ValidationException: The model ID isn't valid`

La chaîne d'ID de modèle ne correspond à aucun modèle disponible dans la région configurée. Copiez l'ID exact depuis la console Bedrock (*Providers &gt; Anthropic &gt; Model catalog*) plutôt que de le taper — les suffixes de date et de version doivent correspondre exactement.

### `ThrottlingException`

Vous avez atteint un quota de tokens ou de requêtes par minute. Options : (1) demandez un relèvement de quota de service, (2) mettez les appels en file côté appelant avec backoff exponentiel, (3) basculez vers le provisioned throughput.

### `bedrock: parse response: json:` — JSON malformé

Le corps de réponse n'a pas la forme Anthropic-on-Bedrock attendue. Cela indique généralement qu'un modèle non-Anthropic a été passé dans `model` ; `buildBedrockBody` dans `internal/llm/bedrock/client.go` ne produit que le format wire Anthropic.

### Endpoint VPC injoignable — `dial tcp: no route to host`

Le pod/instance ne peut pas atteindre les ENI de l'endpoint. Vérifiez le security group de l'endpoint (doit autoriser le port 443 depuis le SG de l'appelant), la table de routage du subnet de l'endpoint et la résolution DNS (l'endpoint requiert que private DNS soit activé sur le VPC).

## Pages liées

- [Fournisseurs : Anthropic](/fr/providers/anthropic/) — même format wire, voie API directe.
- [Guides : Déploiement Kubernetes](/fr/guides/kubernetes-deployment/) — configuration IRSA.
- [Guides : Onboarding entreprise](/fr/guides/enterprise-onboarding/) — checklist équipe plateforme.
- [Guides : Limites de débit](/fr/guides/rate-limits/) — manuel du throttling.
- [Sécurité](/fr/security/) — frontières de confiance et trafic sortant.

## Pour aller plus loin

- `internal/llm/bedrock/client.go` — `Complete`, conversion de messages, types wire.
- `internal/config/config.go` — struct `BedrockConfig`.
- Docs AWS : [Permissions IAM Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html).
- Docs AWS : [Endpoints VPC interface Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html).
