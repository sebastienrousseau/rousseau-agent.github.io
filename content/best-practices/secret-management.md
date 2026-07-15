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
description: "Where API keys, bot tokens and IMAP passwords should live: environment variables, config files with 0600, systemd LoadCredential, or Vault."
keywords: "secrets, env, vault, loadcredential, credentials, best practices"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/best-practices/secret-management/"
subtitle: "Env vars, config files, LoadCredential, Vault."
tags: "best-practices, security, secrets"
title: "Secret Management"

news_genres: "Blog"
news_keywords: "secrets, env, vault"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Secret Management"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "best-practices"
order: 11
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/best-practices/secret-management/index.html"
item_link: "https://docs.rousseau-agent.dev/best-practices/secret-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Secret Management"
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
twitter_description: "Where API keys, bot tokens and IMAP passwords should live."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Secret Management"
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

Rousseau needs credentials for every backend it touches: API keys for LLM providers, bot tokens for chat transports, IMAP/SMTP passwords, cloud auth. This guide covers where they should live in production.

<aside class="admonition" data-type="tip"><span class="admonition-title">Precedence</span><p><code>config.Load</code> resolves values in the order flag &gt; env &gt; file &gt; default. Env vars beat the YAML file for the same key, so you can keep secrets out of the file entirely.</p></aside>

## Three postures

<div class="tabs" data-tabs="secret-posture">
  <div class="tab-list" role="tablist" aria-label="Posture">
    <button role="tab" aria-selected="true">Env vars</button>
    <button role="tab" aria-selected="false">Config file (0600)</button>
    <button role="tab" aria-selected="false">Vault / secrets manager</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Best for personal workstations and one-off daemons.

```sh
export ANTHROPIC_API_KEY='sk-ant-…'
export ROUSSEAU_SLACK_APP_TOKEN='xapp-…'
export ROUSSEAU_SLACK_BOT_TOKEN='xoxb-…'
```

Under systemd user units, the same idea in the `[Service]` section:

```ini
Environment=ROUSSEAU_LOG_FORMAT=json
EnvironmentFile=%h/.config/rousseau/secrets.env
```

Set `secrets.env` to `chmod 600`. Never commit it. Use `direnv` for shells.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Acceptable when the machine is single-tenant and the file is `0600`.

```sh
install -m 0600 /dev/null ~/.config/rousseau/config.yaml
$EDITOR ~/.config/rousseau/config.yaml
```

Never commit `config.yaml`. If versioning config, keep a `config.example.yaml` and gitignore the real one.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Best for shared/production infrastructure. Two common patterns:

1. **systemd LoadCredential** — put the secret in a manager (Vault, `sops`, GCP Secret Manager), fetch it in a pre-start unit, hand it to rousseau via `LoadCredential=` which exposes it under `${CREDENTIALS_DIRECTORY}`.

```ini
[Service]
LoadCredential=anthropic:%t/rousseau/anthropic
ExecStartPre=/usr/local/bin/fetch-secret anthropic > %t/rousseau/anthropic
ExecStart=/bin/sh -c 'export ANTHROPIC_API_KEY=$$(cat ${CREDENTIALS_DIRECTORY}/anthropic); exec rousseau slack'
```

2. **Vault agent template** — Vault Agent renders `secrets.env` and pushes SIGHUP to rousseau. Simpler and works with `EnvironmentFile=`.

  </div>
</div>

## Per-transport map

| Field | YAML | Env |
|---|---|---|
| Anthropic API key | `anthropic.api_key` | `ANTHROPIC_API_KEY` (magic) |
| Bedrock | AWS credential chain | `AWS_PROFILE`, `AWS_REGION` |
| Vertex | `vertex.credentials_file` | `GOOGLE_APPLICATION_CREDENTIALS` |
| Slack app token | `slack.app_token` | `ROUSSEAU_SLACK_APP_TOKEN` |
| Slack bot token | `slack.bot_token` | `ROUSSEAU_SLACK_BOT_TOKEN` |
| Discord | `discord.token` | `ROUSSEAU_DISCORD_TOKEN` |
| Telegram | `telegram.token` | `ROUSSEAU_TELEGRAM_TOKEN` |
| Matrix | `matrix.access_token` | `ROUSSEAU_MATRIX_ACCESS_TOKEN` |
| Email IMAP pw | `email.imap_password` | `ROUSSEAU_EMAIL_IMAP_PASSWORD` |
| Email SMTP pw | `email.smtp_password` | `ROUSSEAU_EMAIL_SMTP_PASSWORD` |
| SMS (Twilio) | `sms.auth_token` | `ROUSSEAU_SMS_AUTH_TOKEN` |
| iMessage | `imessage.password` | `ROUSSEAU_IMESSAGE_PASSWORD` |

## Rotation discipline

- Rotate LLM API keys quarterly. Bedrock/Vertex use the cloud IAM lifecycle instead.
- Rotate bot tokens whenever an operator leaves the org.
- After any suspected secret leak, revoke via the provider console *first*, then re-issue.

## Detection

- Enable `govulncheck` and secret-scanning in CI (`trufflehog`, `gitleaks`).
- Grep `journalctl -u rousseau-*.service` for `sk-ant-` fragments — rousseau logs mask sensitive fields (`mask()` in `internal/cli/doctor.go`), but callers should audit any custom code.

## Anti-patterns

- Committing `config.yaml` to a public repository.
- `export ANTHROPIC_API_KEY=sk-…` in `.bashrc` on a shared host.
- Storing secrets in the same directory as the workspace bind mount.
- Reusing a Slack app token across production and dev workspaces.

## Related pages

- [Reference: Config: Provider](/reference/config/provider/)
- [Deployment](/deployment/)
- [Security](/security/)
- [Best Practices: Multi-tenant](/best-practices/multi-tenant/)
