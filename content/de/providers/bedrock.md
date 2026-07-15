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
description: "Configure the AWS Bedrock provider: standard credential chain, region and model ID format, required IAM permissions."
keywords: "Bedrock, AWS, SigV4, IAM, InvokeModel, InvokeModelWithResponseStream, Claude on AWS"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/de/providers/bedrock/"
subtitle: "Anthropic's Claude models on AWS."
tags: "providers, bedrock, AWS"
title: "AWS-Bedrock-Anbieter"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Bedrock, AWS, SigV4, IAM, InvokeModel, InvokeModelWithResponseStream, Claude on AWS"
news_language: "de"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "AWS-Bedrock-Anbieter"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 8
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS-Feed von rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/bedrock/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/bedrock/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "AWS-Bedrock-Anbieter"
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
twitter_title: "AWS-Bedrock-Anbieter"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">Was Sie lernen</span><p>Wie Sie den Bedrock-Provider mit der AWS-Credential-Kette konfigurieren, die Least-Privilege-IAM-Policy, Cross-Account-Role-Übernahme, VPC-Endpoints für private Konnektivität und die Modell-Verfügbarkeitsmatrix nach Region. Lesen Sie <code>internal/llm/bedrock/client.go</code> parallel zu dieser Seite.</p></aside>

## Wann Bedrock verwenden

Der `bedrock`-Provider ist die richtige Wahl, wenn:

- Sie auf AWS sind und Claude über Bedrock statt über die Anthropic-API abrechnen wollen.
- Sie SigV4-Auth über die Standard-AWS-Credential-Kette benötigen (Env-Variablen, `~/.aws/credentials`, IMDS, IRSA auf EKS).
- Sie den Modell-Traffic aus Gründen der Datenresidenz innerhalb einer einzigen AWS-Region halten wollen.
- Sie den Modell-Traffic durch einen VPC-Endpoint routen müssen, damit er nie das öffentliche Internet berührt.
- Sie Cross-Account-Zugriff über `sts:AssumeRole` wollen.

## Konfiguration

```yaml
provider: bedrock

bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
  profile: default
  max_tokens: 4096
```

| Feld | Standard | Wirkung |
|---|---|---|
| `region` | *erforderlich* | AWS-Region. Bedrock-Modell-Verfügbarkeit ist regional; prüfen Sie die AWS-Konsole. |
| `model` | *erforderlich* | Bedrock-Modell-ID. Anthropic-Claude-IDs folgen der Form `anthropic.claude-<name>-<datum>-<version>:<revision>`. |
| `profile` | *leer* | Credentials-Profil aus `~/.aws/credentials`. Leer nutzt die Standard-Credential-Kette. |
| `max_tokens` | SDK-Standard | Begrenzt Ausgabe-Tokens pro Completion. |

## Credential-Kette

Der Provider erstellt einen Bedrock-Client über `awsconfig.LoadDefaultConfig`, der die Standard-Kette der Reihe nach durchläuft:

1. Umgebung (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`).
2. Shared-Credentials-Datei (`~/.aws/credentials`), auf `profile` eingeschränkt, falls gesetzt.
3. Shared-Config-Datei (`~/.aws/config`).
4. IAM Roles for Tasks (ECS) / IAM Roles Anywhere.
5. EC2 IMDS (v2).
6. IRSA – die IAM-Rolle, die einem Kubernetes-ServiceAccount zugeordnet ist (EKS).

Keine davon wird über rousseau konfiguriert; das SDK übernimmt die Auflösung.

## Erforderliche IAM-Berechtigungen

Die minimale Policy, die der Aufrufer übernehmen können muss:

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

Beschränken Sie die `Resource` auf die konkrete Modellfamilie, die Sie aufrufen wollen. Weitere Wildcards funktionieren, sind aber meist überzogen.

## Wire-Format

Der Provider sendet den Standard-JSON-Body für Anthropic-Nachrichten (`anthropic_version`, `messages`, `system`, `tools`, `max_tokens`) an `bedrock:InvokeModel` und erhält dieselbe Form zurück. Dies spiegelt die direkte Anthropic-API – Tool-Use, Stop-Reasons und Usage-Counter sind identisch.

Streaming nutzt `bedrock:InvokeModelWithResponseStream` mit dem Event-Stream-Decoder des SDKs.

## Streaming

Der Provider implementiert `agent.StreamingProvider`. Streaming wird in `rousseau chat` automatisch verwendet.

## Tool-Use

Tool-Definitionen aus der `Registry` werden in Bedrocks Tool-JSON in `internal/llm/bedrock/client.go` konvertiert. Approval-Richtlinien greifen.

## Auth-Muster pro Bereitstellung

<div class="tabs" data-tabs="bedrock-auth">
  <div class="tab-list" role="tablist" aria-label="Bedrock auth deployment">
    <button role="tab" aria-selected="true">Laptop</button>
    <button role="tab" aria-selected="false">EC2</button>
    <button role="tab" aria-selected="false">EKS (IRSA)</button>
    <button role="tab" aria-selected="false">Cross-Account</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Für lokale Entwicklung nutzen Sie ein benanntes Profil mit SSO oder langlebigen Keys:

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

`profile:` wird berücksichtigt, weil rousseau `awsconfig.WithSharedConfigProfile(cfg.Profile)` übergibt, wenn nicht leer (siehe `internal/llm/bedrock/client.go` Zeile 63). Lassen Sie `profile` weg, um die Standard-Kette zu nutzen.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Hängen Sie ein Instanz-Profil mit der Berechtigung `bedrock:InvokeModel` an (siehe die IAM-Policy unten), und lassen Sie dann `profile` leer:

```yaml
bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

Das SDK löst Credentials automatisch aus IMDS v2 auf. Keine Env-Variablen, keine Profil-Datei nötig.

<aside class="admonition" data-type="note"><span class="admonition-title">IMDS v2</span><p>Stellen Sie sicher, dass die Instanz IMDS v2 verlangt (Hop-Limit 2, Tokens erforderlich). Das AWS Go SDK v2 handhabt den Token-Tanz transparent, benötigt aber Netzwerk-Erreichbarkeit zu <code>169.254.169.254</code>.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

IAM Roles for Service Accounts (IRSA) ist das empfohlene Muster auf EKS. Ordnen Sie dem ServiceAccount des Pods eine Rolle zu:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rousseau
  namespace: agents
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/rousseau-bedrock
```

Die Trust-Policy der Rolle bindet sie an den EKS-OIDC-Provider und den ServiceAccount. Siehe [Guides: Kubernetes-Bereitstellung](/de/guides/kubernetes-deployment/) für das vollständige Beispiel.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau lebt in Konto A, Bedrock lebt in Konto B. Konfigurieren Sie eine Role-Übernahme:

`~/.aws/config`:

```ini
[profile rousseau]
role_arn = arn:aws:iam::222222222222:role/rousseau-bedrock
source_profile = default
region = us-east-1
```

Die Ziel-Rolle in Konto B hat `bedrock:InvokeModel` auf dem Modell und eine Trust-Policy, die dem Principal von Konto A das Übernehmen erlaubt. Anschliessend:

```yaml
bedrock:
  region: us-east-1
  profile: rousseau
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

Das SDK übernimmt den STS-`AssumeRole`-Round-Trip transparent.

  </div>
</div>

## Least-Privilege-IAM-Policy

Die minimale Policy, die der Aufrufer übernehmen können muss:

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

Beschränken Sie die `Resource` auf die konkrete Modellfamilie. Weitere Wildcards funktionieren, erteilen aber mehr Rechte als nötig. Für Provisioned Throughput fügen Sie das ARN Ihres provisionierten Modells als zweite Resource hinzu.

Trust-Policy für Cross-Account (Konto B, die modell-hostende Seite):

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

`ExternalId` ist gemäss AWS-Sicherheitsleitfaden für Drittanbieter-Cross-Account-Zugriffe erforderlich.

## VPC-Endpoints

Für Bereitstellungen, die das öffentliche Internet nicht erreichen dürfen, erstellen Sie einen Interface-VPC-Endpoint für Bedrock in Ihrer VPC:

```sh
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-0123456789abcdef0 \
  --vpc-endpoint-type Interface \
  --service-name com.amazonaws.us-east-1.bedrock-runtime \
  --subnet-ids subnet-aaa subnet-bbb \
  --security-group-ids sg-xxx
```

Das AWS-SDK löst automatisch über den Endpoint auf, wenn Security-Group und Route-Table dies erlauben. Es ist keine Config-Änderung auf rousseau-Seite nötig – dies ist für den Provider transparent.

<aside class="admonition" data-type="warning"><span class="admonition-title">Endpoint-Policies</span><p>Hängen Sie eine Resource-Policy an den Endpoint, um einzuschränken, welche Principals und Aktionen er akzeptiert. Ein weit geöffneter Endpoint hebt den Isolations-Vorteil auf.</p></aside>

## Modell-Verfügbarkeit nach Region

Die Verfügbarkeit ändert sich, während AWS neue Snapshots ausrollt. Momentaufnahme Stand Mitte 2026:

| Modell | us-east-1 | us-west-2 | eu-west-2 | eu-central-1 | ap-southeast-1 | ap-northeast-1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Claude Sonnet 4.6 | ja | ja | ja | ja | ja | ja |
| Claude Opus 4.6 | ja | ja | limitiert | limitiert | nein | nein |
| Claude Haiku 4.6 | ja | ja | ja | ja | ja | ja |

<aside class="admonition" data-type="note"><span class="admonition-title">Konsole prüfen</span><p>Die Verfügbarkeit ändert sich ohne Vorankündigung. Die massgebliche Quelle ist die Bedrock-Konsole unter <em>Foundation models &gt; Model access</em> – wo Sie den Zugriff auch explizit anfordern müssen, bevor das Modell aufrufbar wird, selbst wenn die Region es unterstützt.</p></aside>

## Fallstricke

- **Modell-IDs ändern sich pro Region.** `anthropic.claude-sonnet-4-6-20260101-v1:0` in `us-east-1` kann in `eu-west-2` ein anderer Snapshot sein. Prüfen Sie die Bedrock-Konsole.
- **Der Zugriff muss pro Modell gewährt werden.** Selbst wenn IAM `InvokeModel` erlaubt, müssen Sie in der Konsole *Model access &gt; Request access* durchklicken, bevor der erste Aufruf gelingt.
- **Throttling.** Bedrock erzwingt Konto- und modell-bezogene Concurrency-Limits (Tokens pro Minute und Requests pro Minute). Setzen Sie `max_tokens` konservativ.
- **Provisioned Throughput.** Wenn Sie Provisioned Throughput haben, übergeben Sie die provisionierte Modell-ID (`arn:aws:bedrock:us-east-1:<konto>:provisioned-model/…`) als `model`.
- **Streaming-Decoder-Fehler.** Das Event-Stream-Format hat sich zwischen SDK-Versionen subtil geändert. Pinnen Sie `aws-sdk-go-v2/service/bedrockruntime` auf eine bekannt-funktionierende Version und testen Sie bei jedem Bump neu.

## Fehlerbehebung

### `AccessDeniedException: You don't have access to the model`

Zwei getrennte Prüfungen: (1) Die IAM-Policy des Aufrufers erlaubt `bedrock:InvokeModel` auf dem Modell-ARN, und (2) das Konto hat den Zugriff auf das Modell in der Bedrock-Konsole explizit angefragt. Punkt 2 trifft die meisten Erstnutzer.

### `ValidationException: The model ID isn't valid`

Der Modell-ID-String passt zu keinem in der konfigurierten Region verfügbaren Modell. Kopieren Sie die exakte ID aus der Bedrock-Konsole (*Providers &gt; Anthropic &gt; Model catalog*), anstatt sie zu tippen – Datum und Versions-Suffixe müssen exakt übereinstimmen.

### `ThrottlingException`

Sie erreichen ein Token- oder Requests-pro-Minute-Quota. Optionen: (1) Service-Quota-Erhöhung anfordern, (2) Aufrufe im Aufrufer mit exponentiellem Backoff in eine Warteschlange, (3) Wechsel zu Provisioned Throughput.

### `bedrock: parse response: json:` – fehlerhaftes JSON

Der Response-Body hat nicht die erwartete Anthropic-auf-Bedrock-Form. Meist deutet das darauf hin, dass ein Nicht-Anthropic-Modell als `model` übergeben wurde; `buildBedrockBody` in `internal/llm/bedrock/client.go` erzeugt nur das Anthropic-Wire-Format.

### VPC-Endpoint nicht erreichbar – `dial tcp: no route to host`

Der Pod bzw. die Instanz kann die ENIs des Endpoints nicht erreichen. Prüfen Sie die Security-Group am Endpoint (muss Port 443 aus der SG des Aufrufers erlauben), die Route-Table des Endpoint-Subnetzes und die DNS-Auflösung (der Endpoint erfordert Private DNS für die VPC).

## Verwandte Seiten

- [Providers: Anthropic](/de/providers/anthropic/) – gleiches Wire-Format, direkter API-Pfad.
- [Guides: Kubernetes-Bereitstellung](/de/guides/kubernetes-deployment/) – IRSA-Setup.
- [Guides: Enterprise-Onboarding](/de/guides/enterprise-onboarding/) – Checkliste für das Plattform-Team.
- [Guides: Rate-Limits](/de/guides/rate-limits/) – Throttling-Handbuch.
- [Sicherheit](/de/security/) – Vertrauensgrenzen und Netzwerk-Egress.

## Weiterführende Lektüre

- `internal/llm/bedrock/client.go` – `Complete`, Nachrichtenkonvertierung, Wire-Typen.
- `internal/config/config.go` – `BedrockConfig`-Struktur.
- AWS-Dokumentation: [Amazon Bedrock IAM permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html).
- AWS-Dokumentation: [Bedrock interface VPC endpoints](https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html).
