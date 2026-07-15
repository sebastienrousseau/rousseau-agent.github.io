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
description: "The exact JSON schemas for the five built-in tools rousseau ships: read, write, edit, grep, bash."
keywords: "tool schemas, read, write, edit, grep, bash, JSON Schema"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/reference/tool-schemas/"
subtitle: "JSON schemas for the five built-in tools, verbatim from internal/tools/builtin."
tags: "reference, tools, json-schema, read, write, edit, grep, bash"
title: "Reference: Tool Schemas"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "tool schemas, read, write, edit, grep, bash, JSON Schema"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Mon, 13 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Reference: Tool Schemas"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "reference"
order: 54
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/reference/tool-schemas/index.html"
item_link: "https://docs.rousseau-agent.dev/reference/tool-schemas/index.html"
item_pub_date: "Mon, 13 Jul 2026 00:00:00 GMT"
item_title: "Reference: Tool Schemas"
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
twitter_description: "The exact JSON schemas for the five built-in tools rousseau ships: read, write, edit, grep, bash."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Reference: Tool Schemas"
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

## What this page is

Every built-in tool in `internal/tools/builtin/*.go` publishes an `InputSchema()` method that returns a JSON Schema map. This page reproduces those schemas exactly, plus one paragraph on each tool's runtime contract.

The five built-in tools are: [`read`](#read), [`write`](#write), [`edit`](#edit), [`grep`](#grep), [`bash`](#bash). All five are constructed in the daemon wiring; the approver (`internal/agent/approver.go`) sits between the model's tool call and the tool's `Execute` method.

## read

Source: `internal/tools/builtin/read.go`.

**Description (surfaced to the model):** _Read the contents of a UTF-8 text file. Input: absolute path. Returns file contents or an error._

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

**Contract.** The `path` must be absolute (`filepath.IsAbs`). The tool reads the whole file into memory and rejects it if the first 512 bytes contain a NUL byte (`isLikelyText`). Returns the file contents as a string on success; an error otherwise. No line-count or size limit is enforced at the tool level — approval policies are the right place to bound file sizes.

## write

Source: `internal/tools/builtin/write.go`.

**Description (surfaced to the model):** _Write UTF-8 text to a file, replacing existing contents. Creates parent directories as needed. Input: absolute path + content._

**Input schema:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to write."
    },
    "content": {
      "type": "string",
      "description": "The complete file contents to write."
    }
  },
  "required": ["path", "content"]
}
```

**Contract.** Full-file overwrite. Creates parent directories with mode `0o755`. Writes with mode `0o644`. Absolute path required. Returns `"wrote N bytes to /path"`. There is deliberately no atomic-swap dance — pattern-mode approvers pin the write target to a specific directory tree; the tool itself does not try to be clever about filesystem safety.

## edit

Source: `internal/tools/builtin/edit.go`.

**Description (surfaced to the model):** _Replace exactly one occurrence of old_string with new_string in a file. old_string must be unique in the file; if it appears zero or multiple times the edit fails. Preserve indentation exactly._

**Input schema:**

```json
{
  "type": "object",
  "properties": {
    "path": {
      "type": "string",
      "description": "Absolute filesystem path to the file to edit."
    },
    "old_string": {
      "type": "string",
      "description": "Exact text to find. Must be unique in the file."
    },
    "new_string": {
      "type": "string",
      "description": "Text to replace old_string with."
    }
  },
  "required": ["path", "old_string", "new_string"]
}
```

**Contract.** Exact-string replacement, not regex. `old_string` must appear **exactly once** in the file — zero matches or multiple matches both fail with a descriptive error, which is intentional (borrowed from Claude Code's Edit tool). Prevents accidental mass-replace and forces the model to include enough surrounding context to disambiguate. `old_string == new_string` also errors. Returns `"edited /path (1 replacement)"`.

## grep

Source: `internal/tools/builtin/grep.go`.

**Description (surfaced to the model):** _Search files under a directory for a Go regular expression. Skips binary files and files larger than the configured limit. Returns 'path:line: matched_line' rows._

**Input schema:**

```json
{
  "type": "object",
  "properties": {
    "pattern": {
      "type": "string",
      "description": "Go RE2 regular expression to match."
    },
    "path": {
      "type": "string",
      "description": "Absolute directory to search under."
    },
    "include": {
      "type": "string",
      "description": "Optional filename glob (e.g. '*.go'). Applied to the base name."
    },
    "ignore_case": {
      "type": "boolean",
      "description": "Case-insensitive match. Defaults to false."
    }
  },
  "required": ["pattern", "path"]
}
```

**Contract.** RE2 regex, not PCRE. Case-insensitive when `ignore_case: true` (implemented by prefixing `(?i)`). Skips directories named `.git`, `node_modules`, `vendor`, `.venv`, `__pycache__`, `dist`, `build`. Skips files larger than `MaxFileBytes` (default 4 MiB). Truncates output at `MaxMatches` (default 200) and appends a `(truncated at N matches)` footer when it hits the cap. Skips files that contain a NUL byte on the current line (rough binary detection).

## bash

Source: `internal/tools/builtin/bash.go`.

**Description (surfaced to the model):** _Execute a shell command via `/bin/sh -c`. Returns combined stdout+stderr with exit status._

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

**Contract.** `/bin/sh -c <command>`. Combined stdout + stderr, capped at whatever fits in a `bytes.Buffer` (i.e. RAM). 60-second timeout by default (configurable at construction). On timeout: returns partial output plus a `bash: timed out after 60s` error. **No sandboxing at the tool level.** The daemon's OS user, filesystem view, network posture, and seccomp profile are the containment. Pattern-mode approvers are how you narrow the allowed commands — see [Tutorial: Harden the approver](/tutorials/harden-approver-policy/).

## MCP-exposed tools

Rousseau's stdio MCP server (`rousseau mcp`) exposes a **different** set of tools — read-only queries against the session store and cron jobs. See [MCP: Exposed tools](/mcp/exposed-tools/) for `rousseau_search_sessions`, `rousseau_list_sessions`, `rousseau_read_session`, `rousseau_cron_list`.

## Related

- [User Guide: Tools](/user-guide/tools/) — the operator-facing view.
- [Guides: File management](/guides/file-management/) — how `write`/`edit` interact with bind mounts and SELinux.
- [Guides: Audit + approval policies](/guides/audit-approval-policies/) — how pattern regexes constrain each tool's input.
- [Developer Guide: Add a tool](/developer-guide/add-a-tool/) — extend this set.
