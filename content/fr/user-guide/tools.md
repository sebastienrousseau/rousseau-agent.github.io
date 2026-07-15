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
hreflang: "fr"
icon: ""
id: "https://docs.rousseau-agent.dev"
image_alt: "rousseau-agent logo"
image_height: "630"
image_width: "1200"
image: ""
language: "fr"
locale: "fr_FR"
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
description: "The five built-in tools shipped with rousseau-agent: read, write, edit, grep, bash. JSON schemas, execution semantics, safety notes."
keywords: "tools, read, write, edit, grep, bash, json schema, tool registry"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/fr/user-guide/tools/"
subtitle: "The five built-in tools, with schemas and safety notes."
tags: "tools, reference, read, write, edit, grep, bash"
title: "Outils intégrés"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tools, read, write, edit, grep, bash, json schema, tool registry"
news_language: "fr"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Outils intégrés"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 42
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: Flux RSS de rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/tools/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/tools/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Outils intégrés"
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
twitter_description: "The five built-in tools shipped with rousseau-agent: read, write, edit, grep, bash. JSON schemas, execution semantics, safety notes."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Outils intégrés"
twitter_url: "https://docs.rousseau-agent.dev"

# Humans.txt - The Humans.txt front matter (YAML).
author_website: "https://docs.rousseau-agent.dev"
author_twitter: "@rousseauagent"
author_location: "London, UK"
thanks: "Merci à chaque opérateur qui exploite son propre agent de codage."
site_last_updated: "2026-07-12"
site_standards: "HTML5, CSS3, RSS, Atom, JSON, XML, YAML, Markdown, TOML"
site_components: "SSG, rousseau-agent documentation"
site_software: "SSG, Rust"

---

## What ships

`internal/tools/builtin/` provides the five tools that every rousseau daemon wires up by default (see `internal/cli/chat.go` for the wiring):

| Tool | Purpose | Mutates? |
|---|---|:---:|
| `read` | UTF-8 text file read. | No |
| `write` | UTF-8 text file overwrite. Creates parents. | Yes |
| `edit` | Exact-string replacement, unique-match required. | Yes |
| `grep` | RE2 regex search under a directory. | No |
| `bash` | `/bin/sh -c <cmd>` with a timeout. | Yes |

Each is registered via `registry.MustRegister(builtin.NewXTool())`. Register additional tools without touching the agent core — see [Developer Guide: Add a Tool](/fr/developer-guide/add-a-tool/).

## `read`

Read a UTF-8 text file from the local filesystem.

**Input schema:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to the file to read."
    }
  },
  "required": ["path"]
}
```

**Semantics:**

- `path` must be absolute; relative paths are rejected.
- Rejects binary content via a `\x00` sniff over the first 512 bytes.
- Returns the file contents verbatim as a string.

**Errors:** missing path, relative path, unreadable file, non-text content.

## `write`

Write UTF-8 text to a file, replacing existing contents. Creates parent directories as needed.

**Input schema:**

```json
{
  "type": "object",
  "properties": {
    "path":    { "type": "string", "description": "Absolute filesystem path to write." },
    "content": { "type": "string", "description": "The complete file contents to write." }
  },
  "required": ["path", "content"]
}
```

**Semantics:**

- Overwrites the file (not append). Use `edit` for incremental changes.
- `MkdirAll(dir, 0o755)` on the parent directory.
- File written with permission `0o644`.
- Returns `wrote <n> bytes to <path>` on success.

**Errors:** missing path, relative path, mkdir failure, write failure.

## `edit`

Exact-string replacement with a **unique-match constraint**. Borrowed from Claude Code's Edit tool.

**Input schema:**

```json
{
  "type": "object",
  "properties": {
    "path":       { "type": "string", "description": "Absolute filesystem path to the file to edit." },
    "old_string": { "type": "string", "description": "Exact text to find. Must be unique in the file." },
    "new_string": { "type": "string", "description": "Text to replace old_string with." }
  },
  "required": ["path", "old_string", "new_string"]
}
```

**Semantics:**

- `old_string` must appear **exactly once** in the file. Zero occurrences → error. Two or more → error (asks the model to provide more surrounding context).
- `old_string == new_string` → error (no-op edits are rejected).
- Preserves indentation and whitespace verbatim.
- Returns `edited <path> (1 replacement)` on success.

The unique-match rule is deliberate: it prevents the model from performing accidental mass-replacement. When the model wants to change every occurrence, it has to author multiple `edit` calls, each with enough surrounding context to disambiguate.

**Errors:** missing / relative path, missing `old_string`, no match, non-unique match, identical strings, read / write failure.

## `grep`

Regex search under a directory. Deliberately simpler than ripgrep — no dependency, runs in-process.

**Input schema:**

```json
{
  "type": "object",
  "properties": {
    "pattern":     { "type": "string",  "description": "Go RE2 regular expression to match." },
    "path":        { "type": "string",  "description": "Absolute directory to search under." },
    "include":     { "type": "string",  "description": "Optional filename glob (e.g. '*.go'). Applied to the base name." },
    "ignore_case": { "type": "boolean", "description": "Case-insensitive match. Defaults to false." }
  },
  "required": ["pattern", "path"]
}
```

**Semantics:**

- Go [RE2](https://github.com/google/re2/wiki/Syntax) syntax — no backreferences, no lookaround.
- Recursively walks `path`. Skips `.git`, `node_modules`, `vendor`, `.venv`, `__pycache__`, `dist`, `build`.
- Skips files larger than `MaxFileBytes` (default 4 MiB) and binary content.
- Caps output at `MaxMatches` (default 200); truncation is annotated inline.
- Returns `<path>:<line>: <matching-line>` rows.
- Returns the string `no matches` when nothing matched.

**Errors:** missing pattern / path, relative path, invalid regex, invalid include glob.

## `bash`

Execute a shell command via `/bin/sh -c`. **The load-bearing security boundary.**

**Input schema:**

```json
{
  "type": "object",
  "properties": {
    "command": {
      "type": "string",
      "description": "The shell command to execute."
    }
  },
  "required": ["command"]
}
```

**Semantics:**

- Runs under `/bin/sh -c <command>`. Not bash-specific — POSIX shell.
- Combined stdout+stderr is returned.
- Default timeout: 60 seconds. Configurable at registration via `NewBashTool(timeout)`.
- Timeout returns a `bash: timed out after <duration>` error along with any output produced before the deadline.
- Non-zero exit yields an error whose string wraps the exit status; the output is still returned for the model to inspect.

**Safety:**

- The tool has no built-in allowlist. The [Approver](/fr/user-guide/approval-policies/) is the load-bearing gate. **Always** enable pattern-mode approval on unattended daemons.
- The command runs with the daemon's UID and filesystem visibility. Layer a rootless container underneath ([Deployment](/fr/deployment/)).

## Tool errors and the loop

When a tool returns an error, the agent converts it into a `tool_result` block with `isError: true` and feeds it back to the model on the next iteration:

```
[user] make the change
[assistant] tool_use: edit {"path": "/tmp/foo", "old_string": "x", "new_string": "y"}
[user]      tool_result: "edit: old_string not found in /tmp/foo" (isError=true)
[assistant] I couldn't find "x" in /tmp/foo. Could you confirm the path?
```

This is the same channel used for approver denials — see [Approval Policies](/fr/user-guide/approval-policies/).

## Registering additional tools

```go
registry := tools.NewRegistry()
registry.MustRegister(builtin.NewReadTool())
registry.MustRegister(builtin.NewWriteTool())
registry.MustRegister(builtin.NewEditTool())
registry.MustRegister(builtin.NewGrepTool(0, 0))    // zero → defaults
registry.MustRegister(builtin.NewBashTool(60 * time.Second))
registry.MustRegister(myCustomTool)                  // any tools.Tool
```

`tools.Registry` is concurrency-safe; registration is thread-safe.

## Security implications at a glance

| Tool | Blast radius | When NOT to use |
|---|---|---|
| `read` | Read files with daemon's FS visibility. Can exfiltrate any readable file. | If any secret material is on disk in the workspace. Restrict via approver `match` regex. |
| `grep` | Same as read plus a regex CPU cost. | If matching untrusted patterns — ReDoS is possible with pathological regex. |
| `edit` | Modifies file contents in-place. | If the daemon's FS visibility extends beyond the intended workspace. Combine with a container bind mount. |
| `write` | Creates/overwrites files. | Same as edit, plus can create files anywhere the daemon can write. |
| `bash` | Arbitrary command execution. | On any unattended daemon without a pattern-mode approver. **The primary security boundary.** |

## Troubleshooting

### `read: read /path: is a directory`

The `read` tool is file-only. Use `grep` with a path pattern or `bash` (with `ls`) if you need directory contents.

### `edit: old_string not found`

The model's proposed `old_string` did not match the file's contents byte-for-byte. Common causes: whitespace/newline drift, wrong line-ending style, the file was edited between the model's read and the edit call.

### `edit: old_string is not unique`

Rousseau's `edit` tool refuses ambiguous edits — the model must include enough surrounding context to make `old_string` a unique substring. This prevents accidental multi-site replacement.

### `bash: timed out after 1m0s`

Default 60s timeout. Long-running commands (build, test) will fail. Either raise the timeout with `NewBashTool(2*time.Minute)` when embedding, or split into faster steps.

### `grep` returns nothing but the pattern is definitely there

Rousseau's `grep` uses Go's `regexp` package (RE2), which does not support all PCRE features. Backreferences and lookarounds will silently fail. Rewrite the pattern for RE2.

## Related pages

- [User Guide: Approval Policies](/fr/user-guide/approval-policies/) — the gate on every tool call.
- [Developer Guide: Add a Tool](/fr/developer-guide/add-a-tool/) — build your own.
- [Concepts](/fr/concepts/) — how tools fit into the agent loop.
- [Agent loop](/fr/agent-loop/) — how tool results feed back into the next turn.
- [Reference: Tool schemas](/fr/reference/tool-schemas/) — machine-readable schemas.

## Further reading

- `internal/tools/builtin/read.go` — file read with truncation.
- `internal/tools/builtin/write.go` — file write.
- `internal/tools/builtin/edit.go` — the unique-string constraint enforcer.
- `internal/tools/builtin/grep.go` — recursive regex search.
- `internal/tools/builtin/bash.go` — `/bin/sh -c` shell wrapper.
