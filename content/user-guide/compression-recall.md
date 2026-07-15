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
description: "Session compression triggers and FTS5 cross-session recall in rousseau-agent. How the agent loop keeps long sessions inside the model's context."
keywords: "compression, recall, fts5, session, context window, summarisation, trigger_messages, keep_recent"
layout: "page"
permalink: "https://docs.rousseau-agent.dev/user-guide/compression-recall/"
subtitle: "Session compression and FTS5 cross-session recall."
tags: "compression, recall, session, fts5"
title: "Compression + Recall"

# News - The News SiteMap front matter (YAML).
news_genres: "Blog"
news_keywords: "compression, recall, fts5, session, context window, summarisation, trigger_messages, keep_recent"
news_language: "en"
news_image_loc: ""
news_loc: "https://docs.rousseau-agent.dev"
news_publication_date: "Sun, 12 Jul 2026 00:00:00 GMT"
news_publication_name: "rousseau-agent"
news_title: "Compression + Recall"

# RSS - The RSS feed front matter (YAML).
atom_link: https://docs.rousseau-agent.dev/rss.xml
category: "concepts"
order: 45
schema: "doc"
docs: https://validator.w3.org/feed/docs/rss2.html
generator: "SSG (version 0.0.37)"
item_description: RSS feed for rousseau-agent
item_guid: "https://docs.rousseau-agent.dev/user-guide/compression-recall/index.html"
item_link: "https://docs.rousseau-agent.dev/user-guide/compression-recall/index.html"
item_pub_date: "Sun, 12 Jul 2026 00:00:00 GMT"
item_title: "Compression + Recall"
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
twitter_description: "Session compression triggers and FTS5 cross-session recall in rousseau-agent. How the agent loop keeps long sessions inside the model's context."
twitter_image: ""
twitter_image_alt: "rousseau-agent logo"
twitter_site: "rousseauagent"
twitter_title: "Compression + Recall"
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

## Two problems, two mechanisms

- A single long session can outgrow the model's context window. **Compression** collapses old messages into a summary block so the loop keeps working.
- A new session on a related topic loses the value of prior conversations. **Recall** queries the FTS5 index across sessions and splices excerpts into the system prompt.

Compression edits the current session in place. Recall never edits — it appends context to the system prompt for the current turn.

## Compression

`internal/agent/compressor.go` implements an LLM-backed summariser. The agent loop consults it at the start of every `Turn`:

```go
if changed, err := a.opts.Compressor.Compress(ctx, s); err != nil {
    a.logger.Warn("agent.compress_failed", slog.String("err", err.Error()))
} else if changed {
    a.logger.Info("agent.compressed", slog.Int("messages", len(s.Messages)))
}
```

If the session is short, nothing happens. Once the message count crosses `trigger_messages`, the compressor:

1. Isolates the tail of the session — the most recent `keep_recent` messages — and preserves them verbatim.
2. Feeds everything older to the provider with a summarisation prompt.
3. Replaces the older block with a single synthetic `RoleSystem` message containing the summary.
4. Marks the session so the summary block sits in the prompt-cache-eligible prefix on the very next provider call.

The loop then proceeds against the smaller message list. The user never sees the seam.

### Enabling compression

```yaml
agent:
  compression:
    enabled: true
    trigger_messages: 60      # zero → default 60
    keep_recent: 8            # zero → default 8
    prompt: ""                # zero → sensible default
```

| Field | Default | Meaning |
|---|---|---|
| `enabled` | `false` | Off by default. |
| `trigger_messages` | 60 | Message count above which compression fires. |
| `keep_recent` | 8 | How many recent messages to preserve verbatim. |
| `prompt` | built-in | Overrides the summarisation instruction. |

### When to leave it off

Compression uses one provider round-trip per fire. On a subscription-tier `claudecli` account, that trip is free — enable freely. On a pay-per-token API, every fire has a cost, so tune `trigger_messages` upward or keep it disabled for short-lived sessions.

### When to leave it on

- Long-lived chat-transport daemons where a WhatsApp thread grows over weeks.
- Cron-scheduled prompts whose replies feed a follow-up prompt.
- Self-hosted providers where token cost is zero.

### Semantics preserved across compression

- Tool-use / tool-result pairs are never split. If a `tool_use` is in the compressed region and its `tool_result` in the preserved region, both are collapsed into the summary.
- The compressor never rewrites the current in-flight user turn.
- Prompt caching (`internal/llm/anthropic` `cache_control` markers) is placed on the summary block so the next call reads it from the cache.

## Recall

`internal/state/sqlite/` maintains an FTS5 virtual table indexing every message. A `RecallProvider` runs a query against this table and returns a system-prompt appendix.

### The interface

```go
type RecallProvider interface {
    SystemAppendix(ctx context.Context, s *Session) string
}
```

The agent loop calls this once per iteration. When it returns non-empty text, the text is appended to the base system prompt for that iteration.

### The default provider

`internal/agent/recall.go` ships a heuristic that:

1. Extracts salient tokens from the current session's last user message.
2. Runs `MATCH` against the FTS5 index for those tokens across other sessions.
3. Formats the top N excerpts as a `Previously in another session:` block.
4. Bounds the appendix so it never exceeds a configured character budget.

### Enabling recall

Recall is wired at agent construction. See `internal/cli/chat.go` and `internal/cli/*.go` for how each transport wires it. In your own embedding:

```go
recall, err := sqlitestore.NewRecall(store)
if err != nil { /* ... */ }

ag := agent.New(provider, registry, logger, agent.Options{
    RecallProvider: recall,
})
```

### Interaction with the approver

Recall reads from the session store; it never fires a tool call. The approver is not consulted. The store contents themselves are the trust boundary.

### Session search from the CLI

Recall is a machine-facing feature. For humans, the same FTS5 index powers:

```sh
rousseau session search "kubectl"
rousseau session search "PVC not binding"
```

Same query engine, same results, minus the LLM re-ranking that a proper RecallProvider might add.

## Interaction with skills

Skills ([Skills](/skills/)) and recall both add to the system prompt. They are composed in a fixed order:

1. Base system prompt (from `agent.system_prompt` or the default).
2. Skills appendix (if any).
3. Recall appendix (if any).

Everything is separated by two newlines. If nothing needs adding, the base prompt goes through unchanged.

## Semantics of the summary block

The synthetic summary message is emitted with `RoleSystem`. It is not a user or assistant message, so it never appears in `rousseau session show` as a conversational turn — it shows as `[compressed summary]` metadata.

If you resume a compressed session with `rousseau chat --session <id>`, the summary is preserved. Deleting the summary block via a hypothetical schema edit is unsafe: the model may reference facts only known through it.

## Verifying compression is firing

```
INFO agent.compressed messages=12
```

`messages` is the new session length after the summary block replaced the compressed prefix. A `WARN agent.compress_failed err=...` means the summarisation provider errored; the loop continued against the uncompressed session.

## Caveats

- Compression is lossy. The summary is model-generated text; important details can be dropped. For audit trails, keep the full session in the store — compression only affects what the model sees, not what SQLite persists.
- Recall requires the FTS5 SQLite extension. `modernc.org/sqlite` builds it in by default; if you swap the store implementation, ensure FTS5 is available.
- Both features assume UTF-8 text. Voice-note transcripts (see [Voice mode](/user-guide/voice-mode/)) count as regular user messages once transcribed.

## Next

- [Concepts](/concepts/) — the agent loop overview.
- [Configuration](/configuration/) — every `agent.compression.*` knob.
- [Skills](/skills/) — the third system-prompt input.
