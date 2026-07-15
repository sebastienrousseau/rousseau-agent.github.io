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
description: "Configure the AWS Bedrock provider: standard credential chain, region and model ID format, required IAM permissions."
keywords: "Bedrock, AWS, SigV4, IAM, InvokeModel, InvokeModelWithResponseStream, Claude on AWS"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/providers/bedrock/"
subtitle: "Anthropic's Claude models on AWS."
tags: "providers, bedrock, AWS"
title: "AWS Bedrock Provider"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "Bedrock, AWS, SigV4, IAM, InvokeModel, InvokeModelWithResponseStream, Claude on AWS"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "AWS Bedrock Provider"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "providers"
order: 8
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/providers/bedrock/index.html"
item_link: "https://docs.rousseau-agent.dev/providers/bedrock/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "AWS Bedrock Provider"
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
twitter_title: "AWS Bedrock Provider"
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

<aside class="admonition" data-type="tip"><span class="admonition-title">What you'll learn</span><p>How to configure the Bedrock provider with the AWS credential chain, the least-privilege IAM policy, cross-account role assumption, VPC endpoints for private connectivity, and the model-availability matrix by region. Read <code>internal/llm/bedrock/client.go</code> alongside this page.</p></aside>

## When to use Bedrock

The `bedrock` provider is the right choice when:

- You are on AWS and want Claude billed through Bedrock rather than the Anthropic API.
- You need SigV4 auth via the standard AWS credential chain (env vars, `~/.aws/credentials`, IMDS, IRSA on EKS).
- You want to keep model traffic inside a single AWS region for data-residency reasons.
- You need to route model traffic through a VPC endpoint so it never touches the public internet.
- You want cross-account access via `sts:AssumeRole`.

## Configuration

```yaml
provider: bedrock

bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
  profile: default
  max_tokens: 4096
```

| Field | Default | Effect |
|---|---|---|
| `region` | *required* | AWS region. Bedrock model availability is regional; check the AWS console. |
| `model` | *required* | Bedrock model ID. Anthropic Claude IDs follow the shape `anthropic.claude-<name>-<date>-<version>:<revision>`. |
| `profile` | *empty* | Credentials profile from `~/.aws/credentials`. Empty falls through the standard credential chain. |
| `max_tokens` | SDK default | Caps output tokens per completion. |

## Credential chain

The provider constructs a Bedrock client via `awsconfig.LoadDefaultConfig`, which walks the standard chain in order:

1. Environment (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`).
2. Shared credentials file (`~/.aws/credentials`), narrowed by `profile` if set.
3. Shared config file (`~/.aws/config`).
4. IAM Roles for Tasks (ECS) / IAM Roles Anywhere.
5. EC2 IMDS (v2).
6. IRSA — the IAM role attached to a Kubernetes service account (EKS).

None of these are configured through rousseau; the SDK handles resolution.

## Required IAM permissions

The minimum policy the caller must be able to assume:

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

Scope the `Resource` to the specific model family you plan to invoke. Broader wildcards work but are usually overkill.

## Wire format

The provider sends the standard Anthropic messages JSON body (`anthropic_version`, `messages`, `system`, `tools`, `max_tokens`) to `bedrock:InvokeModel`, and receives the same shape back. This mirrors the Anthropic direct API — tool use, stop reasons, and usage counters are the same.

Streaming uses `bedrock:InvokeModelWithResponseStream` with the SDK's event-stream decoder.

## Streaming

The provider implements `agent.StreamingProvider`. Streaming is used automatically in `rousseau chat`.

## Tool use

Tool definitions from the `Registry` are converted to Bedrock's tool JSON in `internal/llm/bedrock/client.go`. Approval policies apply.

## Auth pattern by deployment

<div class="tabs" data-tabs="bedrock-auth">
  <div class="tab-list" role="tablist" aria-label="Bedrock auth deployment">
    <button role="tab" aria-selected="true">Laptop</button>
    <button role="tab" aria-selected="false">EC2</button>
    <button role="tab" aria-selected="false">EKS (IRSA)</button>
    <button role="tab" aria-selected="false">Cross-account</button>
  </div>
  <div class="tab-panel" role="tabpanel">

For local dev, use a named profile with SSO or long-lived keys:

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

`profile:` is honoured because rousseau passes `awsconfig.WithSharedConfigProfile(cfg.Profile)` when non-empty (see `internal/llm/bedrock/client.go` line 63). Omit `profile` to fall through the default chain.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Attach an instance profile with `bedrock:InvokeModel` permission (see the IAM policy below), then leave `profile` empty:

```yaml
bedrock:
  region: us-east-1
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

The SDK resolves credentials from IMDS v2 automatically. No env vars, no profile file needed.

<aside class="admonition" data-type="note"><span class="admonition-title">IMDS v2</span><p>Ensure the instance is configured to require IMDS v2 (hop limit 2, tokens required). The AWS Go SDK v2 handles the token dance transparently but requires network reachability to <code>169.254.169.254</code>.</p></aside>

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

IAM Roles for Service Accounts (IRSA) is the recommended pattern on EKS. Attach a role to the pod's service account:

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: rousseau
  namespace: agents
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::123456789012:role/rousseau-bedrock
```

The role's trust policy binds it to the EKS OIDC provider and the service account. See [Guides: Kubernetes deployment](/guides/kubernetes-deployment/) for the full example.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Rousseau lives in Account A, Bedrock lives in Account B. Configure a role assumption:

`~/.aws/config`:

```ini
[profile rousseau]
role_arn = arn:aws:iam::222222222222:role/rousseau-bedrock
source_profile = default
region = us-east-1
```

The target role in Account B has `bedrock:InvokeModel` on the model, and a trust policy allowing Account A's principal to assume it. Then:

```yaml
bedrock:
  region: us-east-1
  profile: rousseau
  model: anthropic.claude-sonnet-4-6-20260101-v1:0
```

The SDK handles the STS `AssumeRole` roundtrip transparently.

  </div>
</div>

## Least-privilege IAM policy

The minimum policy the caller must be able to assume:

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

Scope the `Resource` to the specific model family. Broader wildcards work but grant more than needed. For provisioned throughput, add the ARN of your provisioned model as a second resource.

Trust policy for cross-account (Account B, the model-hosting side):

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

`ExternalId` is required by AWS security guidance for third-party cross-account access.

## VPC endpoints

For deployments that must not reach the public internet, create an interface VPC endpoint for Bedrock in your VPC:

```sh
aws ec2 create-vpc-endpoint \
  --vpc-id vpc-0123456789abcdef0 \
  --vpc-endpoint-type Interface \
  --service-name com.amazonaws.us-east-1.bedrock-runtime \
  --subnet-ids subnet-aaa subnet-bbb \
  --security-group-ids sg-xxx
```

The AWS SDK will automatically resolve through the endpoint if the security group and route table allow it. No rousseau-side config change is needed — this is transparent to the provider.

<aside class="admonition" data-type="warning"><span class="admonition-title">Endpoint policies</span><p>Attach a resource policy to the endpoint to constrain which principals and actions it accepts. A wide-open endpoint negates the isolation benefit.</p></aside>

## Model availability by region

Availability shifts as AWS rolls out new snapshots. Snapshot as of mid-2026:

| Model | us-east-1 | us-west-2 | eu-west-2 | eu-central-1 | ap-southeast-1 | ap-northeast-1 |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Claude Sonnet 4.6 | yes | yes | yes | yes | yes | yes |
| Claude Opus 4.6 | yes | yes | limited | limited | no | no |
| Claude Haiku 4.6 | yes | yes | yes | yes | yes | yes |

<aside class="admonition" data-type="note"><span class="admonition-title">Check the console</span><p>Availability changes without notice. The authoritative source is the Bedrock console at <em>Foundation models &gt; Model access</em> — where you also have to explicitly request access before the model becomes callable, even if the region supports it.</p></aside>

## Gotchas

- **Model IDs change per region.** `anthropic.claude-sonnet-4-6-20260101-v1:0` in `us-east-1` may be a different snapshot in `eu-west-2`. Check the Bedrock console.
- **Access must be granted per model.** Even with IAM allowing `InvokeModel`, Bedrock requires you to click through *Model access &gt; Request access* in the console before the first call succeeds.
- **Throttling.** Bedrock enforces per-account and per-model concurrency limits (tokens-per-minute and requests-per-minute). Set `max_tokens` conservatively.
- **Provisioned throughput.** If you have provisioned throughput, pass the provisioned model ID (`arn:aws:bedrock:us-east-1:<account>:provisioned-model/…`) as `model`.
- **Streaming decoder failures.** The event-stream format changed subtly between SDK versions. Pin `aws-sdk-go-v2/service/bedrockruntime` to a known-good version and re-test on every bump.

## Troubleshooting

### `AccessDeniedException: You don't have access to the model`

Two separate checks: (1) the caller's IAM policy allows `bedrock:InvokeModel` on the model ARN, and (2) the account has explicitly requested access to the model in the Bedrock console. Item 2 catches most first-time users.

### `ValidationException: The model ID isn't valid`

The model ID string does not match a model available in the configured region. Copy the exact ID from the Bedrock console (*Providers &gt; Anthropic &gt; Model catalog*) rather than typing it — the date and version suffixes must match exactly.

### `ThrottlingException`

You hit a token or request-per-minute quota. Options: (1) request a service quota increase, (2) queue calls in the caller with exponential backoff, (3) switch to provisioned throughput.

### `bedrock: parse response: json:` — malformed JSON

The response body is not the expected Anthropic-on-Bedrock shape. Usually indicates a non-Anthropic model was passed as `model`; `buildBedrockBody` in `internal/llm/bedrock/client.go` only produces the Anthropic wire format.

### VPC endpoint unreachable — `dial tcp: no route to host`

The pod/instance cannot reach the endpoint's ENIs. Check the security group on the endpoint (must allow port 443 from the caller's SG), the endpoint's subnet route table, and DNS resolution (the endpoint requires private DNS enabled on the VPC).

## Related pages

- [Providers: Anthropic](/providers/anthropic/) — same wire format, direct API path.
- [Guides: Kubernetes deployment](/guides/kubernetes-deployment/) — IRSA setup.
- [Guides: Enterprise onboarding](/guides/enterprise-onboarding/) — platform-team checklist.
- [Guides: Rate limits](/guides/rate-limits/) — throttling handbook.
- [Security](/security/) — trust boundaries and network egress.

## Further reading

- `internal/llm/bedrock/client.go` — `Complete`, message conversion, wire types.
- `internal/config/config.go` — `BedrockConfig` struct.
- AWS docs: [Amazon Bedrock IAM permissions](https://docs.aws.amazon.com/bedrock/latest/userguide/security_iam_id-based-policy-examples.html).
- AWS docs: [Bedrock interface VPC endpoints](https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html).
