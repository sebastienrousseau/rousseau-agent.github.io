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
description: "Wire rousseau-agent to a Slack channel that runs read and grep over the workspace whenever an operator asks."
keywords: "slack, code review, socket mode, read tool, grep tool, allowlist"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/tutorials/build-a-code-review-bot/"
subtitle: "A Slack channel that lets rousseau review a repo on demand."
tags: "tutorials, slack, code review, socket mode, read, grep"
title: "Tutorial: Build a code-review bot"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "slack, code review, socket mode, read tool, grep tool, allowlist"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Tutorial: Build a code-review bot"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "tutorials"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/tutorials/build-a-code-review-bot/index.html"
item_link: "https://docs.rousseau-agent.dev/tutorials/build-a-code-review-bot/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Tutorial: Build a code-review bot"
last_build_date: "Mon, 13 Jul 2026 00:00:00 GMT"
managing_editor: sebastian.rousseau@gmail.com (Sebastien Rousseau)
pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
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
twitter_description: "Wire rousseau-agent to a Slack channel that runs read and grep over the workspace whenever an operator asks."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Tutorial: Build a code-review bot"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Thanks to every operator running their own coding agent."
site_last_updated: "2026-07-13"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## What you build

A private Slack channel where team members mention `@rousseau` with a repo path and a question. Rousseau checks out the workspace, runs `read` and `grep` from `internal/tools/builtin/`, and posts a reply with quoted line references. No public HTTP surface — Slack Socket Mode drives everything from outbound WebSocket.

Estimated time: 20 minutes assuming you already have Slack admin access to a workspace.

## Prerequisites

- Rousseau installed and a provider configured (see [Quickstart](/quickstart/)).
- Slack workspace admin.
- A repository already checked out at some path under your `$HOME` — that becomes the "workspace" the bot can `read`/`grep` over.

## Step 1: create a Slack app

Slack's Socket Mode is what makes this bot possible: your daemon opens an outbound WebSocket to Slack, no ingress required.

1. Head to <https://api.slack.com/apps> and create a new app **from scratch**.
2. Under **Socket Mode**, enable it and generate an **app-level token** with `connections:write`. Copy the `xapp-...` value.
3. Under **OAuth & Permissions**, add these **Bot Token Scopes**:
   - `chat:write`
   - `app_mentions:read`
   - `channels:history` (or `groups:history` for private channels)
4. Install the app to your workspace. Copy the **Bot User OAuth Token** — the `xoxb-...` value.
5. Under **Event Subscriptions**, enable events and subscribe the bot to `app_mention` and `message.channels` (or `message.groups`).
6. Invite the bot to the review channel: `/invite @rousseau`.

## Step 2: configure rousseau

Add to `~/.config/rousseau/config.yaml`. The relevant fields come from `SlackConfig` in `internal/config/config.go`:

```yaml
provider: claudecli           # or anthropic — whatever you set in Quickstart

slack:
  app_token:  xapp-1-…
  bot_token:  xoxb-…
  bot_user_id: U0ROUSSEAU     # from https://api.slack.com/methods/auth.test
  reply_header: "*rousseau-agent*\n\n"
  allowlist:
    - U01ABC…                 # your Slack user IDs

agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: ".*"}
      - {tool: grep, match: ".*"}
    # no bash, no write, no edit — read-only reviewer
```

The `allowlist` restricts who the router will accept messages from. The `internal/transport/router.go` router emits `transport.rejected` for any other sender.

## Step 3: run the bridge

```sh
rousseau slack \
  --app-token "$SLACK_APP_TOKEN" \
  --bot-token "$SLACK_BOT_TOKEN" \
  --bot-user-id "$SLACK_BOT_USER_ID"
```

`--bot-user-id` prevents the bot from replying to its own messages. Structured logs from `internal/transport/slack/client.go` will show:

```
INFO slack.started
INFO slack.incoming from=U01ABC channel=C01REVIEW text="…"
INFO tool.execute name=read id=t_1
INFO tool.execute name=grep id=t_2
```

## Step 4: try it

In the review channel:

```
@rousseau look under /home/seb/repos/acme-api and tell me
where request logging is set up
```

The `claudecli` provider (or Anthropic — whichever you chose) will call `read` and `grep` from `internal/tools/builtin/` against the workspace bind mount. Because the approver runs `pattern` mode with only `read` and `grep` allowlisted, the model cannot write or shell out — even if a compromised prompt asks it to.

## Step 5: harden

Pattern-mode approvers are **regex over the JSON tool-input**. To restrict `read` and `grep` to a specific project tree:

```yaml
agent:
  approver:
    mode: pattern
    default: deny
    allow:
      - {tool: read, match: "\"path\":\"/home/seb/repos/acme-api/[^\"]*\""}
      - {tool: grep, match: "\"path\":\"/home/seb/repos/acme-api\""}
```

See [Tutorial: Harden the approver](/tutorials/harden-approver-policy/) for the full walkthrough of `default: deny` + audit.

## Deploying under systemd

For anything beyond a laptop session, run the Slack bridge under the Podman Quadlet unit at `docker/rousseau-agent.container` — swap `Exec=whatsapp --allow …` for `Exec=slack --app-token … --bot-token …`. See [Deployment](/deployment/) for the full unit.

## Related

- [Transports: Slack](/transports/slack/)
- [User Guide: Approval Policies](/user-guide/approval-policies/)
- [User Guide: Tools](/user-guide/tools/)
- [Tutorial: Harden the approver](/tutorials/harden-approver-policy/)
