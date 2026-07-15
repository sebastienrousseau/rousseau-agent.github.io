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
description: "How to contribute to rousseau-agent: commit style, quality gates, adding a transport or provider, docs contributions."
keywords: "contributing, patches, conventional commits, quality gates"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/community/contributing/"
subtitle: "Sending patches, adding features, filing bugs."
tags: "community, contributing"
title: "Contributing"

news_genres: "Blog"
news_keywords: "contributing, patches"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Contributing"

atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "community"
order: 12
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/community/contributing/index.html"
item_link: "https://docs.rousseau-agent.dev/community/contributing/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Contributing"
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
twitter_description: "How to contribute to rousseau-agent."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Contributing"
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

The authoritative contributor guide lives at [`CONTRIBUTING.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/CONTRIBUTING.md) in the source tree. This page is a docs-flavoured summary and the entry point when you're reading docs first, code second.

<aside class="admonition" data-type="tip"><span class="admonition-title">Start small</span><p>Filing a good bug report is a contribution. So is fixing a typo in the docs. Ambitious patches (new transport, new provider) are welcome but they have a higher review bar.</p></aside>

## Ground rules

- Commit style: [Conventional Commits](https://www.conventionalcommits.org/). `feat(slack): …`, `fix(whatsapp): …`, `docs(concepts): …`, `refactor: …`.
- Every exported identifier has a godoc comment.
- No `interface{}` / `any` in exported APIs without a written justification.
- Every fact in the docs is code-truthful. Cite the file when possible.

## Quality gates (run locally before opening a PR)

`make check` mirrors the CI matrix:

```sh
make check
```

Under the hood:

- `go vet ./...`
- `golangci-lint run` (18 linters)
- `go test -race -count=1 -covermode=atomic ./...`
- `govulncheck ./...`

Coverage floor is 75% total. Core packages sit 85–100% — keep them there.

## Sending a patch

```sh
git clone git@github.com:<you>/rousseau-agent
cd rousseau-agent
git checkout -b feat/awesome
# … edit …
make check
git commit -m "feat(<area>): <what changed>"
git push -u origin feat/awesome
# open PR against sebastienrousseau/rousseau-agent:main
```

CI runs the same gates. Every commit must pass.

## Contribution shapes

<div class="tabs" data-tabs="contrib-shape">
  <div class="tab-list" role="tablist" aria-label="Shape">
    <button role="tab" aria-selected="true">Bug fix</button>
    <button role="tab" aria-selected="false">Docs</button>
    <button role="tab" aria-selected="false">New transport</button>
    <button role="tab" aria-selected="false">New provider</button>
  </div>
  <div class="tab-panel" role="tabpanel">

Reproduce first. Add a failing test. Fix. Verify the test passes. Send the PR with both the fix and the test in the same commit.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

Docs live in a separate repo (`rousseau-agent-docs`). English content lives under `content/`; language variants under `content/<lang>/`.

- Use the frontmatter template from an existing page.
- Prefer editing over creating; new pages need an owner willing to keep them fresh.
- Cross-link with absolute paths.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

A transport lives at `internal/transport/<name>/`. It needs:

- A `New` constructor and `Config` struct.
- Implementation of the `transport.Transport` interface (`Start`, `Stop`, `Deliver`).
- Table-driven tests.
- A CLI wire-up at `internal/cli/<name>.go`.
- A config struct on `Config` in `internal/config/config.go`.
- A docs page under `content/transports/<name>.md`.

The Slack + Discord PR history is a good template.

  </div>
  <div class="tab-panel" role="tabpanel" hidden>

A provider lives at `internal/llm/<name>/`. It needs:

- A `New` constructor and `Config` struct.
- Implementation of `agent.Provider` (`Chat`) and, ideally, `agent.StreamingProvider` (`ChatStream`).
- Table-driven tests.
- A config struct on `Config`.
- A docs page under `content/providers/<name>.md`.

The Bedrock and Vertex commit history is a good template.

  </div>
</div>

## Filing a bug

Include, at minimum:

- `rousseau version` output.
- `rousseau doctor` output.
- The exact command you ran.
- The stderr you got.
- What you expected.

Use the GitHub Issues bug-report template — it prompts for exactly this.

## Related pages

- [Community: Overview](/community/overview/)
- [Community: Code of Conduct](/community/code-of-conduct/)
- [Developer Guide](/developer-guide/)
- [Reference: CLI Commands](/reference/cli-commands/)
- [Security](/security/)
