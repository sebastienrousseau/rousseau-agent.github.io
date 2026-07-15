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
description: "Contribution guide for rousseau-agent: conventional commits, PR process, reviewer checklist, release cadence."
keywords: "contributing, conventional commits, pr process, reviewer checklist, release"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/developer-guide/contributing/"
subtitle: "PR process, standards, review checklist."
tags: "developer-guide, contributing"
title: "Contributing"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "contributing, conventional commits, pr process, reviewer checklist, release"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Contributing"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "developer-guide"
order: 66
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/developer-guide/contributing/index.html"
item_link: "https://docs.rousseau-agent.dev/developer-guide/contributing/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Contributing"
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
twitter_description: "Contribution guide for rousseau-agent: conventional commits, PR process, reviewer checklist, release cadence."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Contributing"
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

## Ground rules

Contributions accepted from invited collaborators. Every PR is held to the same bar: green CI, code standards below, reviewer approval. Green CI is necessary but not sufficient.

The authoritative source is the [`CONTRIBUTING.md`](https://github.com/sebastienrousseau/rousseau-agent/blob/main/CONTRIBUTING.md) in the repo root. This page mirrors it in the docs-site voice.

## Development environment

```sh
git clone https://github.com/sebastienrousseau/rousseau-agent
cd rousseau-agent
make setup      # installs golangci-lint (v2) and govulncheck
make check      # vet + lint + race-tests + govulncheck
```

Every check that runs in CI is available locally through the Makefile. If a change passes `make check`, it will pass CI.

## Commit standards

- **Conventional Commits** — `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `ci:`, `perf:`.
- Subject line ≤ 72 characters. Body explains **why**, not what. Reference the driving decision, issue, or incident.
- Do not amend published commits. Create a new commit; the reviewer prefers a series they can bisect.
- Sign your commits if you have signing configured. Not currently required, but recommended for release-tag commits.

## Code standards

- Every exported identifier has a godoc comment beginning with the identifier name.
- No `interface{}` / `any` in exported APIs without a written justification in the doc comment.
- `context.Context` propagates through every I/O path. No hidden globals or ambient loggers; pass `*slog.Logger` explicitly.
- Errors wrap upward with `fmt.Errorf("...: %w", err)`. Sentinel errors go in the package's `errors.go`. Prefer `errors.Is` / `errors.As` at call sites over string matching.
- No panics outside `main` and test helpers. `Must*` variants that panic on operator error (duplicate registration, invalid static schema) are allowed with a documented rationale.
- No `fmt.Print*` in library code. Use `slog` or a TUI model. The `forbidigo` linter enforces this.

## Test standards

- Unit tests live next to the code: `foo.go` → `foo_test.go`.
- Table-driven tests preferred. Use `require` for stopping assertions, `assert` for non-stopping ones.
- Interface-based test injection over global patching. Every transport package defines a narrow interface (`WSConn`, `IMAPClient`, `HTTPClient`, `Sender`) that tests satisfy with fakes.
- Coverage target: 85% for pure business-logic packages; 75% overall.
- Race-safe: `go test -race` must pass. New concurrent code needs a race test if it introduces non-trivial synchronisation.
- Fuzz functions for every parser (`FuzzParseFoo` next to `parseFoo`). `make fuzz` runs the corpus.

See [Testing](/developer-guide/testing/) for the injection pattern.

## Pull request process

1. Open the PR against `main`. Rebase (do not merge) if `main` moves under you.
2. Every PR requires:
   - A rationale in the description (2–3 sentences linking to the underlying decision).
   - Green CI: `vet`, `lint`, `test-race` on Linux + macOS, `govulncheck`, `codeql`, `reproducible-build`, coverage floor.
   - Reviewer approval.
3. Squash merges only. The merge commit message is the final commit message and lands on `main` as one atomic change.
4. If the PR adds a new dependency, note the justification in the description. Prefer standard library over adding a dependency; prefer an existing dependency over adding a new one.

## Reviewer checklist

Reviewers verify, in order:

1. **Necessity.** Is the change required, or does it add abstraction / feature surface without a driving requirement?
2. **Scope.** Does the change stay within its stated purpose, or does it bundle unrelated cleanups?
3. **Boundary integrity.** Does the change respect the `agent → concrete` dependency direction? See [Architecture](/developer-guide/architecture/).
4. **Test coverage.** Are new code paths covered? Are edge cases exercised?
5. **Error handling.** Are errors wrapped with context? Are cleanup paths honest (`_ =` with a `//nolint:errcheck` justification, not silently swallowed)?
6. **Godoc + linter clean.** Every exported symbol documented; lint output is 0 issues.
7. **Security.** Does the change touch the `bash` tool, approval policy, transport auth, or container posture? If yes, does the PR description flag it?

## Documentation contributions

Documentation lives in a separate repository. When a code PR touches user-visible surface (a new flag, a new field, a new tool), the same PR — or an immediate follow-up PR to the docs repo — must update the affected pages.

- **CLI change** → [User Guide: CLI](/user-guide/cli/) and [Reference: CLI Commands](/reference/cli-commands/).
- **Config change** → [Configuration](/configuration/) and [Reference: Config Schema](/reference/config-schema/).
- **New tool** → [User Guide: Tools](/user-guide/tools/).
- **New transport** → `content/transports/<name>.md`.
- **New provider** → `content/providers/<name>.md`.
- **Behavioural change** → [Changelog](/changelog/).

## Release process

Releases are cut from `main`:

1. Update changelog entries.
2. Tag as `vX.Y.Z` on the release commit.
3. The `release` workflow builds via GoReleaser, generates a CycloneDX SBOM, publishes a cosign signature of the checksums, and generates SLSA-3 provenance.
4. Consumers verify per the recipe in [Security](/security/) and [Installation](/getting-started/installation/).

Rousseau follows [Semantic Versioning](/getting-started/updating/): patch fixes bugs, minor adds features non-breakingly, major breaks — always with a migration recipe.

## Governance

`rousseau-agent` is a single-maintainer project. Decision authority rests with the maintainer of record listed in `go.mod` and `LICENSE`. Contributors propose direction changes via PR discussion or by email to `sebastian.rousseau@gmail.com`.

## Security disclosures

**Do not open a public issue for a security report.** Email `sebastian.rousseau@gmail.com` per the [Security policy](/security/). Acknowledgment within 72 hours.

## Next

- [Architecture](/developer-guide/architecture/) — the map before you change it.
- [Testing](/developer-guide/testing/) — the pattern the reviewer expects.
- [Security](/security/) — the disclosure path.
