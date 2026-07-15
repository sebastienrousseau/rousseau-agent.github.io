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
date: "July 13, 2026"
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
description: "Run rousseau against AWS Bedrock across multiple accounts using AWS profile-based routing and per-project state directories."
keywords: "bedrock, aws, sts, profile, multi-account, recipes"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/recipes/bedrock-multi-account/"
subtitle: "One rousseau, multiple AWS accounts on Bedrock."
tags: "recipes, bedrock, aws"
title: "Recipe: Bedrock Multi-Account"

news_genres: "Blog"
news_keywords: "bedrock, aws, multi-account"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Recipe: Bedrock Multi-Account"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "recipes"
order: 20
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/recipes/bedrock-multi-account/index.html"
item_link: "https://docs.rousseau-agent.dev/recipes/bedrock-multi-account/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Recipe: Bedrock Multi-Account"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
ttl: "60"
type: "website"
webmaster: sebastian.rousseau@gmail.com (Sebastien Rousseau)

apple_mobile_web_app_orientations: "portrait"
apple_touch_icon_sizes: "192x192"
apple-mobile-web-app-capable: "yes"
apple-mobile-web-app-status-bar-inset: "black"
apple-mobile-web-app-status-bar-style: "black-translucent"
apple-mobile-web-app-title: "rousseau-agent"
apple-touch-fullscreen: "yes"

msapplication-navbutton-color: "rgb(26,58,138)"

twitter_card: "summary"
twitter_creator: "rousseauagent"
twitter_description: "Run rousseau against AWS Bedrock across multiple accounts using AWS profile-based routing."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Recipe: Bedrock Multi-Account"
twitter_url: "https://docs.rousseau-agent.dev"

author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## Overview

A platform team runs rousseau on shared infrastructure. Each project has its own AWS account for Bedrock (compliance, chargeback, model access). Use one rousseau binary with per-project config files, each pinning a `bedrock.profile` and its own `state.path`.

## Prerequisites

- AWS SSO (or IAM Identity Center) with roles pre-configured in `~/.aws/config`.
- Bedrock model access approved in each account for the target model.
- A directory-per-project layout on the host.

## Layout

```text
/etc/rousseau/
├── projects/
│   ├── alpha/
│   │   └── config.yaml
│   ├── bravo/
│   │   └── config.yaml
│   └── charlie/
│       └── config.yaml
└── shared/
    └── skills/
```

## Per-project config

`/etc/rousseau/projects/alpha/config.yaml`:

```yaml
provider: bedrock

bedrock:
  region: eu-west-2
  model: anthropic.claude-sonnet-4-6-20250101-v1:0
  profile: alpha-dev

state:
  path: /var/lib/rousseau/alpha/sessions.db

agent:
  skills_dir: /etc/rousseau/shared/skills
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
```

`~/.aws/config`:

```ini
[profile alpha-dev]
sso_start_url = https://acme.awsapps.com/start
sso_region    = eu-west-2
sso_account_id = 111111111111
sso_role_name = BedrockOperator
region        = eu-west-2

[profile bravo-dev]
# …
```

## Launch

```sh
# Refresh SSO once
aws sso login --profile alpha-dev

# Alpha WhatsApp bridge
rousseau --config /etc/rousseau/projects/alpha/config.yaml whatsapp \
  --allow 447900123456@s.whatsapp.net

# Bravo Slack bridge
rousseau --config /etc/rousseau/projects/bravo/config.yaml slack
```

Under systemd, one unit per project.

## Verification

- [ ] `AWS_PROFILE=alpha-dev aws bedrock list-foundation-models` returns the approved model.
- [ ] `rousseau --config /etc/rousseau/projects/alpha/config.yaml doctor` reports the provider as `bedrock` with the right region.
- [ ] Session-store paths are distinct per project (`/var/lib/rousseau/alpha/`, `/bravo/`, …).

## Failure modes

- **`AccessDeniedException`** — role lacks `bedrock:InvokeModelWithResponseStream`. Grant in the SCP or the role's policy.
- **`ModelNotReady`** — model access not approved for this account. Request in the Bedrock console.
- **Cross-account STS refresh loops** — SSO session expired. Add a systemd timer that runs `aws sso login --profile X` weekly.
- **State bleed** — two projects share a state.path. Always use distinct paths.

## Related pages

- [Reference: Config: Provider](/reference/config/provider/)
- [Providers: Bedrock](/providers/bedrock/)
- [Best Practices: Multi-tenant](/best-practices/multi-tenant/)
- [Best Practices: Cost control](/best-practices/cost-control/)
