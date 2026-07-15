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
description: "How rousseau's write and edit tools interact with the workspace bind mount, SELinux :Z labels, container UID mapping, and safe editing outside /workspace."
keywords: "workspace, bind mount, SELinux, :Z, UserNS, write, edit, permissions"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/guides/file-management/"
subtitle: "Workspace bind mount, SELinux :Z, UID mapping, and safe file edits."
tags: "guides, files, container, selinux, workspace"
title: "Guide: File management"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "workspace, bind mount, SELinux, :Z, UserNS, write, edit, permissions"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Guide: File management"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "guides"
order: 37
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/guides/file-management/index.html"
item_link: "https://docs.rousseau-agent.dev/guides/file-management/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Guide: File management"
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
twitter_description: "How rousseau's write and edit tools interact with the workspace bind mount, SELinux :Z labels, container UID mapping, and safe editing outside /workspace."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Guide: File management"
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

## The two tools

Two tools mutate the filesystem:

- [`write`](/reference/tool-schemas/#write) — full-file overwrite. `internal/tools/builtin/write.go` writes with mode `0o644` and `MkdirAll(dir, 0o755)`.
- [`edit`](/reference/tool-schemas/#edit) — single exact-string replacement inside an existing file. `internal/tools/builtin/edit.go`.

Both require an **absolute path** (they call `filepath.IsAbs`). Both perform no atomic-swap dance — they use `os.WriteFile` directly.

## The container view of the world

The reference Quadlet unit at `docker/rousseau-agent.container` mounts three host directories into the container:

```
Volume=%h/.local/share/rousseau:/home/rousseau/.local/share/rousseau:rw,Z
Volume=%h/.claude:/home/rousseau/.claude:rw,Z
Volume=%h/team-rousseau-workspace:/workspace:rw,Z
```

Nothing else on the host is visible. From inside the container, an `edit` tool call against `/workspace/repos/foo/main.go` resolves to `~/team-rousseau-workspace/repos/foo/main.go` on the host.

### `:Z` — the SELinux label

The `:Z` flag on each `Volume=` tells Podman to relabel the mount with a **container-private** SELinux MCS category. Without it, on a system with SELinux in enforcing mode:

- Reads still work most of the time (`container_file_t` is broadly readable).
- Writes fail with `EACCES` and `avc: denied { write }` in the audit log.

If you swap the flag for `:z` (lowercase), Podman relabels with a **shared** category — safer for hosts you share between multiple container users, but not the default.

On systems without SELinux (Debian, non-hardened Ubuntu), `:Z` is a silent no-op.

### `UserNS=keep-id` — UID mapping

The container runs as UID/GID 1000. Without user-namespace mapping, rootless Podman would remap 1000 into the subuid range (typically `100000+`), and files written from inside the container would be owned by that mapped UID on the host — unusable for the operator.

`UserNS=keep-id` maps container UID 1000 to the host user's UID (also 1000 in the reference setup). Files written inside `/workspace` end up owned by `seb:seb` on the host — exactly what you want.

If your host user is not UID 1000, the mapping still works; `keep-id` uses the invoking user's actual UID.

## Editing outside `/workspace`

Because the bind mounts are the container's only view of the host filesystem, `write` or `edit` against `/etc/nginx/nginx.conf` will fail with a path-not-found error — the path simply doesn't exist inside the container. This is a **feature**: it means the operator's approver policy can trust the container boundary.

If you genuinely need the daemon to touch a different host path:

1. **Preferred:** add a new `Volume=` line to the Quadlet unit. Make the least-permissive choice: `:ro` for read-only, `:Z` for private SELinux labelling.
2. **Do not** run rousseau outside the container to bypass the boundary — you lose seccomp, drop-caps, and the read-only root filesystem.

## Editing outside the container

If you run rousseau directly on the host (no container), the tools operate against the daemon's process view — everything under the user's HOME by default. The approver is the only containment layer. See [Guides: Audit + approval policies](/guides/audit-approval-policies/) for the pattern-mode + `default: deny` recipe.

## `write` vs `edit` — when to use which

| Situation | Use |
|---|---|
| Creating a new file. | `write`. |
| Rewriting a file wholesale. | `write`. |
| Changing one section of a large file. | `edit`. It fails safely when `old_string` is not unique. |
| Renaming a symbol across the file. | Multiple `edit` calls with progressively more surrounding context, or a single `write` with the full rewritten contents. Do not use `edit` with `replace_all`-style semantics — the tool refuses. |

The exact-uniqueness constraint on `edit` is deliberate. It borrows directly from Claude Code's Edit tool. Search `internal/tools/builtin/edit.go` for the comment block that explains why.

## Common failure modes

| Symptom | Cause | Fix |
|---|---|---|
| `edit: path must be absolute, got "…"` | Model passed a relative path. | Reject or rewrite in the approver; ask the model to use absolute paths. |
| `edit: old_string not found in …` | The file changed since the model last read it, or the model hallucinated surrounding context. | The model will typically read again and retry. |
| `edit: old_string is not unique in … (found 3 occurrences)` | Same string appears multiple times. | Model must supply more surrounding lines to disambiguate. |
| `write: permission denied` | SELinux label mismatch or wrong UID mapping. | Verify `:Z` on the volume and `UserNS=keep-id` on the container. |
| `read: does not look like UTF-8 text` | File contains NUL bytes in first 512 bytes (`isLikelyText` in `read.go`). | Refuse binary reads at the approver level; use the `bash` tool with `file` if identification is needed. |

## Backups before big rewrites

The tools do not create `.bak` copies. For high-risk changes, teach the model to write to a sibling path first, `bash` diff it, then swap. Alternatively, run everything through a git branch — rousseau leaves `git` completely out of its execution path, so any versioning happens through your normal workflow.

## Related

- [Reference: Tool schemas](/reference/tool-schemas/) — exact input schemas.
- [User Guide: Tools](/user-guide/tools/).
- [Deployment](/deployment/) — the Quadlet unit that defines the bind mounts.
- [Guides: Audit + approval policies](/guides/audit-approval-policies/) — pinning writes to a directory tree.
