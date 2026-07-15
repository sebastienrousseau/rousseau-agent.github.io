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
description: "How to update rousseau-agent: go install refresh, container tag rollover, config migration between minor versions, session-store compatibility policy."
keywords: "update, upgrade, go install, container tag, config migration, minor version"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/getting-started/updating/"
subtitle: "Move between versions without losing sessions or bricking the daemon."
tags: "update, upgrade, migration"
title: "Updating"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "update, upgrade, go install, container tag, config migration, minor version"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Updating"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "getting-started"
order: 24
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/getting-started/updating/index.html"
item_link: "https://docs.rousseau-agent.dev/getting-started/updating/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Updating"
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
twitter_description: "How to update rousseau-agent: go install refresh, container tag rollover, config migration between minor versions, session-store compatibility policy."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Updating"
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

## Versioning policy

Rousseau follows [Semantic Versioning](https://semver.org):

| Bump | What changes |
|---|---|
| Patch (`0.1.2 → 0.1.3`) | Bug fixes, security fixes, dependency bumps. No config or on-disk format changes. |
| Minor (`0.1.x → 0.2.0`) | New features. Config additions are always non-breaking; if a field is removed, an aliased fallback covers at least one minor version. |
| Major (`0.x → 1.0`) | Breaking changes. Requires a documented migration recipe in the [changelog](/changelog/). |

The [SECURITY.md policy](https://github.com/sebastienrousseau/rousseau-agent/blob/main/SECURITY.md) is explicit: only `main` and the most recent tagged release receive security fixes. There is no long-term support branch.

## Update method by install path

### Signed release archive

```sh
VERSION=<new-tag>
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_linux_amd64.tar.gz"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt"
curl -fsSLO "https://github.com/sebastienrousseau/rousseau-agent/releases/download/${VERSION}/rousseau_${VERSION}_checksums.txt.sig"

cosign verify-blob \
  --certificate-identity-regexp 'sebastienrousseau/rousseau-agent' \
  --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
  --signature "rousseau_${VERSION}_checksums.txt.sig" \
  "rousseau_${VERSION}_checksums.txt"

sha256sum -c "rousseau_${VERSION}_checksums.txt" --ignore-missing
tar -xzf "rousseau_${VERSION}_linux_amd64.tar.gz"
sudo install -m 0755 rousseau /usr/local/bin/rousseau
rousseau version
```

Verification is not optional. Every release ships a fresh cosign signature; skipping the check defeats the supply-chain posture.

### `go install`

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@latest
```

To pin an exact tag:

```sh
go install github.com/sebastienrousseau/rousseau-agent/cmd/rousseau@v0.4.2
```

`$GOBIN` (typically `~/go/bin`) needs to be on `$PATH` before `/usr/local/bin` if you want the fresh binary to take precedence.

### Container image

Roll the tag on the image reference and restart the systemd service. If you use the reference Quadlet unit:

```sh
sed -i "s#Image=ghcr.io/sebastienrousseau/rousseau-agent:.*#Image=ghcr.io/sebastienrousseau/rousseau-agent:<new-tag>#" \
  ~/.config/containers/systemd/rousseau-agent.container
systemctl --user daemon-reload
systemctl --user restart rousseau-agent.service
journalctl --user -u rousseau-agent.service -f
```

Pinning to `:latest` is unsafe in a supply-chain-conscious deployment — always pin an immutable tag (`:v0.4.2`) and verify the image digest against the release notes.

### From source

```sh
cd rousseau-agent
git fetch --tags
git checkout <new-tag>
make check          # runs the full CI gate locally
make build
sudo install -m 0755 bin/rousseau /usr/local/bin/rousseau
```

`make check` is the same 18-linter + race + govulncheck gate CI enforces — a passing local run guarantees the reproducible-build job will also pass.

## Config migration

Config schema changes are documented in the [changelog](/changelog/) for every minor version. The Viper defaults keep old keys working across one minor cycle; the following pattern applies:

- **New key added**: gets a default that preserves prior behaviour. No action required.
- **Key renamed**: the old key is aliased for one minor. A warning is logged when the alias is hit.
- **Key removed**: a fail-fast error is emitted at load time. The changelog names the replacement.

To dry-run a config against a new binary:

```sh
rousseau doctor --config ~/.config/rousseau/config.yaml
```

`rousseau doctor` walks every runtime dependency and every config choice; a `fail` row surfaces exactly which key needs attention.

## Session-store compatibility

`~/.local/share/rousseau/sessions.db` uses SQLite with a versioned schema. Schema migrations are additive and idempotent — the daemon runs `CREATE TABLE IF NOT EXISTS` and `ALTER TABLE ADD COLUMN` on startup. **Never downgrade** across a minor version once the new schema has run; SQLite will not remove columns automatically, but application code assumes their presence.

If you need a clean slate:

```sh
mv ~/.local/share/rousseau/sessions.db ~/.local/share/rousseau/sessions.db.bak
```

The daemon recreates the store on next launch. WhatsApp device credentials are stored separately in `whatsapp.db`, so a session-store reset does not force a re-pairing.

## WhatsApp store compatibility

`whatsapp.db` (whatsmeow's device store) is separate from the session store precisely so a session-schema migration cannot brick the WhatsApp pairing. If whatsmeow itself changes on-disk format across a rousseau upgrade, the changelog will flag it and the recovery path is: delete `whatsapp.db`, restart, re-scan the QR.

## Rolling back

- **Signed release archive / `go install`**: reinstall the previous tag using the same recipe.
- **Container**: change the image tag back and restart.
- **From source**: `git checkout <old-tag> && make build`.

Rollbacks are safe as long as the session-store schema in the older version is a superset of what the newer version wrote. In practice this is always true within a single minor series and usually true across adjacent minors. Major upgrades ship a migration recipe with an explicit rollback disclaimer in the changelog.

## Next

- [Changelog](/changelog/) — release-by-release breakdown.
- [Troubleshooting](/troubleshooting/) — if `rousseau doctor` surfaces a `fail` row.
