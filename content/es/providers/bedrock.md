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
description: "Configure the AWS Bedrock provider: standard credential chain, region and model ID format, required IAM permissions."
keywords: "Bedrock, AWS, SigV4, IAM, InvokeModel, InvokeModelWithResponseStream, Claude on AWS"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/es/providers/bedrock/"
subtitle: "Anthropic's Claude models on AWS."
tags: "providers, bedrock, AWS"
title: "Proveedor AWS Bedrock"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Bedrock, AWS, SigV4, IAM, InvokeModel, InvokeModelWithResponseStream, Claude on AWS"
news_language: "es"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Proveedor AWS Bedrock"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 8
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Feed RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/bedrock/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/bedrock/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Proveedor AWS Bedrock"
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
twitter_title: "Proveedor AWS Bedrock"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Qué aprenderás</span><p>Cómo configurar el proveedor Bedrock con la cadena de credenciales de AWS, la política IAM de menor privilegio, la asunción de rol entre cuentas, endpoints VPC para conectividad privada y la matriz de disponibilidad de modelo por región. Lee <code>internal/llm/bedrock/client.go</code> junto a esta página.</p></aside>

## Cuándo usar Bedrock

El proveedor `bedrock` es la elección correcta cuando:

- Estás en AWS y quieres Claude facturado a través de Bedrock en lugar de la API de Anthropic.
- Necesitas autenticación SigV4 vía la cadena estándar de credenciales de AWS (variables de entorno, `~/.aws/credentials`, IMDS, IRSA en EKS).
- Quieres mantener el tráfico del modelo dentro de una sola región de AWS por razones de residencia de datos.
- Necesitas enrutar el tráfico del modelo a través de un endpoint VPC para que nunca toque Internet público.
- Quieres acceso entre cuentas vía `sts:AssumeRole`.

## Configuración

```yaml
provider: bedrock

bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
  profile: default
  max_tokens: 4096
```

| Campo | Por defecto | Efecto |
|---|---|---|
| `region` | *requerido* | Región de AWS. La disponibilidad de modelos en Bedrock es regional; revisa la consola de AWS. |
| `model` | *requerido* | ID de modelo de Bedrock. Los IDs de Anthropic Claude siguen la forma `anthropic.claude-<nombre>-<fecha>-<versión>:<revisión>`. |
| `profile` | *vacío* | Perfil de credenciales de `~/.aws/credentials`. Vacío usa la cadena estándar de credenciales. |
| `max_tokens` | por defecto del SDK | Limita los tokens de salida por completación. |

## Cadena de credenciales

El proveedor construye un cliente de Bedrock vía `awsconfig.LoadDefaultConfig`, que recorre la cadena estándar en orden:

1. Entorno (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`).
2. Archivo de credenciales compartidas (`~/.aws/credentials`), acotado por `profile` si está establecido.
3. Archivo de configuración compartida (`~/.aws/config`).
4. IAM Roles for Tasks (ECS) / IAM Roles Anywhere.
5. EC2 IMDS (v2).
6. IRSA — el rol de IAM adjunto a una cuenta de servicio de Kubernetes (EKS).

Nada de esto se configura a través de rousseau; el SDK gestiona la resolución.

## Permisos IAM requeridos

La política mínima que el llamador debe poder asumir:

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

Acota el `Resource` a la familia de modelos específica que planeas invocar. Los comodines más amplios funcionan pero suelen ser excesivos.

## Formato de cable

El proveedor envía el cuerpo JSON de mensajes estándar de Anthropic (`anthropic_version`, `messages`, `system`, `tools`, `max_tokens`) a `bedrock:InvokeModel`, y recibe la misma forma. Esto refleja la API directa de Anthropic — el uso de herramientas, los motivos de parada y los contadores de uso son iguales.

El streaming usa `bedrock:InvokeModelWithResponseStream` con el decodificador de flujo de eventos del SDK.

## Streaming

El proveedor implementa `agent.StreamingProvider`. El streaming se usa automáticamente en `rousseau chat`.

## Uso de herramientas

Las definiciones de herramientas del `Registry` se convierten al JSON de herramientas de Bedrock en `internal/llm/bedrock/client.go`. Las políticas de aprobación aplican.

## Patrón de autenticación por despliegue

<div class="tabs" data-tabs="bedrock-auth">
  <div class="tab-list" role="tablist" aria-label="Bedrock auth deployment">
    <button role="tab" aria-selected="true">Portátil</button>
    <button role="tab" aria-selected="false">EC2</button>
    <button role="tab" aria-selected="false">EKS (IRSA)</button>
    <button role="tab" aria-selected="false">Entre cuentas</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Para desarrollo local, usa un perfil con nombre con SSO o claves de larga duración:

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

`profile:` se respeta porque rousseau pasa `awsconfig.WithSharedConfigProfile(cfg.Profile)` cuando no está vacío (consulta `internal/llm/bedrock/client.go` línea 63). Omite `profile` para caer a la cadena por defecto.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Adjunta un perfil de instancia con permiso `bedrock:InvokeModel` (consulta la política IAM más abajo), luego deja `profile` vacío:

```yaml
bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

El SDK resuelve las credenciales desde IMDS v2 automáticamente. Sin variables de entorno, sin archivo de perfil necesarios.

<aside class="admonition" data-type="note"><span class="admonition-title">IMDS v2</span><p>Asegúrate de que la instancia esté configurada para requerir IMDS v2 (hop limit 2, tokens requeridos). El AWS Go SDK v2 gestiona el intercambio de tokens de forma transparente pero requiere accesibilidad de red a <code>169.254.169.254</code>.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

IAM Roles for Service Accounts (IRSA) es el patrón recomendado en EKS. Adjunta un rol a la cuenta de servicio del pod:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rousseau
  namespace: agents
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/rousseau-bedrock
```

La política de confianza del rol lo enlaza al proveedor OIDC de EKS y a la cuenta de servicio. Consulta [Guías: Despliegue de Kubernetes](/es/guides/kubernetes-deployment/) para el ejemplo completo.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau vive en la Cuenta A, Bedrock vive en la Cuenta B. Configura una asunción de rol:

`~/.aws/config`:

```ini
[profile rousseau]
role_arn = arn:aws:iam::222222222222:role/rousseau-bedrock
source_profile = default
region = us-east-1
```

El rol destino en la Cuenta B tiene `bedrock:InvokeModel` sobre el modelo, y una política de confianza permitiendo al principal de la Cuenta A asumirlo. Luego:

```yaml
bedrock:
  region: us-east-1
  profile: rousseau
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

El SDK gestiona la ida y vuelta STS `AssumeRole` de forma transparente.

  </div>
</div>

## Política IAM de menor privilegio

La política mínima que el llamador debe poder asumir:

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

Acota el `Resource` a la familia de modelos específica. Los comodines más amplios funcionan pero otorgan más de lo necesario. Para throughput provisionado, añade el ARN de tu modelo provisionado como segundo recurso.

Política de confianza para entre cuentas (Cuenta B, el lado que hospeda el modelo):

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

`ExternalId` es requerido por la guía de seguridad de AWS para acceso entre cuentas de terceros.

## Endpoints VPC

Para despliegues que no deben alcanzar Internet público, crea un endpoint VPC de interfaz para Bedrock en tu VPC:

```sh
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-0123456789abcdef0 \
  --vpc-endpoint-type Interface \
  --service-name com.amazonaws.us-east-1.bedrock-runtime \
  --subnet-ids subnet-aaa subnet-bbb \
  --security-group-ids sg-xxx
```

El AWS SDK resolverá automáticamente a través del endpoint si el security group y la tabla de rutas lo permiten. No se necesita ningún cambio de configuración del lado de rousseau — esto es transparente para el proveedor.

<aside class="admonition" data-type="warning"><span class="admonition-title">Políticas de endpoint</span><p>Adjunta una política de recurso al endpoint para restringir qué principales y acciones acepta. Un endpoint abierto de par en par anula el beneficio de aislamiento.</p></aside>

## Disponibilidad de modelo por región

La disponibilidad cambia a medida que AWS despliega nuevos snapshots. Instantánea a mediados de 2026:

| Modelo | us-east-1 | us-west-2 | eu-west-2 | eu-central-1 | ap-southeast-1 | ap-northeast-1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Claude Sonnet 4.6 | sí | sí | sí | sí | sí | sí |
| Claude Opus 4.6 | sí | sí | limitado | limitado | no | no |
| Claude Haiku 4.6 | sí | sí | sí | sí | sí | sí |

<aside class="admonition" data-type="note"><span class="admonition-title">Consulta la consola</span><p>La disponibilidad cambia sin aviso. La fuente autoritativa es la consola de Bedrock en <em>Foundation models &gt; Model access</em> — donde también tienes que solicitar acceso explícitamente antes de que el modelo se vuelva invocable, incluso si la región lo admite.</p></aside>

## Gotchas

- **Los IDs de modelo cambian por región.** `anthropic.claude-sonnet-4-6-20260101-v1:0` en `us-east-1` puede ser un snapshot diferente en `eu-west-2`. Consulta la consola de Bedrock.
- **El acceso debe otorgarse por modelo.** Incluso con IAM permitiendo `InvokeModel`, Bedrock requiere que hagas clic en *Model access &gt; Request access* en la consola antes de que la primera llamada tenga éxito.
- **Throttling.** Bedrock impone límites de concurrencia por cuenta y por modelo (tokens por minuto y solicitudes por minuto). Establece `max_tokens` de forma conservadora.
- **Throughput provisionado.** Si tienes throughput provisionado, pasa el ID del modelo provisionado (`arn:aws:bedrock:us-east-1:<account>:provisioned-model/…`) como `model`.
- **Fallos del decodificador de streaming.** El formato de flujo de eventos cambió sutilmente entre versiones del SDK. Fija `aws-sdk-go-v2/service/bedrockruntime` a una versión conocida como buena y vuelve a probar en cada bump.

## Solución de problemas

### `AccessDeniedException: You don't have access to the model`

Dos comprobaciones separadas: (1) la política IAM del llamador permite `bedrock:InvokeModel` sobre el ARN del modelo, y (2) la cuenta ha solicitado explícitamente acceso al modelo en la consola de Bedrock. El punto 2 atrapa a la mayoría de usuarios primerizos.

### `ValidationException: The model ID isn't valid`

La cadena del ID de modelo no coincide con un modelo disponible en la región configurada. Copia el ID exacto desde la consola de Bedrock (*Providers &gt; Anthropic &gt; Model catalog*) en lugar de escribirlo — los sufijos de fecha y versión deben coincidir exactamente.

### `ThrottlingException`

Alcanzaste una cuota de tokens o solicitudes por minuto. Opciones: (1) solicitar un aumento de cuota de servicio, (2) encolar llamadas en el llamador con backoff exponencial, (3) cambiar a throughput provisionado.

### `bedrock: parse response: json:` — JSON malformado

El cuerpo de la respuesta no es la forma esperada de Anthropic sobre Bedrock. Normalmente indica que un modelo no-Anthropic se pasó como `model`; `buildBedrockBody` en `internal/llm/bedrock/client.go` solo produce el formato de cable de Anthropic.

### Endpoint VPC inalcanzable — `dial tcp: no route to host`

El pod/instancia no puede alcanzar las ENIs del endpoint. Comprueba el security group del endpoint (debe permitir el puerto 443 desde el SG del llamador), la tabla de rutas de la subred del endpoint y la resolución DNS (el endpoint requiere DNS privado habilitado en la VPC).

## Páginas relacionadas

- [Proveedores: Anthropic](/es/providers/anthropic/) — mismo formato de cable, ruta de API directa.
- [Guías: Despliegue de Kubernetes](/es/guides/kubernetes-deployment/) — configuración de IRSA.
- [Guías: Onboarding empresarial](/es/guides/enterprise-onboarding/) — checklist para equipo de plataforma.
- [Guías: Límites de tasa](/es/guides/rate-limits/) — manual de throttling.
- [Seguridad](/es/security/) — fronteras de confianza y egress de red.

## Lectura adicional

- `internal/llm/bedrock/client.go` — `Complete`, conversión de mensajes, tipos de cable.
- `internal/config/config.go` — struct `BedrockConfig`.
- Documentación de AWS: [Permisos IAM de Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html).
- Documentación de AWS: [Endpoints VPC de interfaz para Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html).
