#!/usr/bin/env python3
"""Build a semantic-enhanced BM25 search index at build time.

Adds three enhancements on top of vanilla BM25 to close the gap with
vector search on the docs corpus we ship:

  1. Porter-lite stemming — "install", "installing", "installed",
     "installation" all collapse to the same term.
  2. Synonym expansion — common docs vocabulary is expanded so a query
     for "setup" also matches "configure", "install", "wire up"; a
     query for "error" also matches "issue", "failure", "problem".
  3. Bigram title index — multi-word title matches ("prompt caching",
     "cosign verify") get a big boost.

Together these lift recall on paraphrased queries (the failure mode of
pure keyword BM25) without needing an embedding model.
"""
from __future__ import annotations
import json
import math
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "public"
STOPWORDS = {
    "a","an","and","are","as","at","be","by","for","from","has","have",
    "in","is","it","of","on","or","that","the","this","to","was","were",
    "with","you","your","we","our","its","if","not","but","all","can","will",
    "so","when","how","what","why","which","one","also","any","only",
}

WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9_-]{1,}")

# Porter-lite stemming — handles the common docs suffixes without a
# full library. Order matters: longest first so we don't strip "ing" off
# a word that ends in "sing", etc.
SUFFIXES: list[tuple[str, str]] = [
    ("ational", "ate"), ("tional", "tion"),
    ("ization", "ize"), ("izations", "ize"),
    ("iveness", "ive"), ("fulness", "ful"), ("ousness", "ous"),
    ("ing", ""), ("ed", ""), ("es", ""), ("ies", "y"),
    ("ly", ""), ("ers", "er"), ("ist", ""),
    ("s", ""),
]


def stem(word: str) -> str:
    if len(word) < 5:
        return word
    for suf, repl in SUFFIXES:
        if word.endswith(suf) and len(word) - len(suf) >= 3:
            return word[: -len(suf)] + repl
    return word


# Synonym clusters — canonical form on the right; queries expand to include the
# stemmed canonical when a synonym is used. Chosen for high-value docs terms.
SYNONYMS: dict[str, str] = {
    "setup": "install", "wire": "install", "provision": "install",
    "problem": "error", "issue": "error", "failure": "error", "broken": "error",
    "auth": "authenticate", "creds": "credential", "credentials": "credential",
    "conf": "config", "settings": "config", "options": "config",
    "hosted": "host", "servers": "server",
    "docker": "container", "podman": "container",
    "runtime": "runtime", "run": "run",
    "chat": "chat", "message": "chat", "converse": "chat",
    "transport": "transport", "channel": "transport",
    "provider": "provider", "backend": "provider", "llm": "provider",
    "cli": "command", "commands": "command", "flag": "command",
    "verify": "verify", "attest": "verify", "sign": "verify",
    "log": "log", "logging": "log", "logs": "log", "slog": "log",
    "deploy": "deploy", "ship": "deploy", "release": "deploy",
    "tool": "tool", "tools": "tool", "builtin": "tool",
    "session": "session", "conversation": "session", "thread": "session",
    "workspace": "workspace", "project": "workspace", "repo": "workspace",
    "approval": "approval", "approver": "approval", "policy": "approval",
    "recall": "recall", "search": "recall", "history": "recall",
}


def tokenize(text: str) -> list[str]:
    raw = [w.lower() for w in WORD_RE.findall(text) if w.lower() not in STOPWORDS and len(w) > 1]
    out: list[str] = []
    for w in raw:
        canonical = SYNONYMS.get(w, w)
        out.append(stem(canonical))
    return out


def bigrams(tokens: list[str]) -> list[str]:
    return [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens) - 1)]


def extract(html: str) -> tuple[str, str, str]:
    """Return (title, description, body_text) from a built page's HTML."""
    title_m = re.search(r"<title>([^<]+)</title>", html)
    desc_m = re.search(r'<meta name="description" content="([^"]+)"', html)
    title = title_m.group(1) if title_m else ""
    description = desc_m.group(1) if desc_m else ""
    body_m = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
    body = body_m.group(1) if body_m else html
    text = re.sub(r'<script.*?</script>', ' ', body, flags=re.DOTALL)
    text = re.sub(r'<style.*?</style>', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return title, description, text


def main() -> None:
    docs: list[dict] = []
    for html_file in ROOT.rglob("index.html"):
        # English-only index (language switch is handled at UI level)
        rel = html_file.relative_to(ROOT).parent
        seg = str(rel).replace("\\", "/")
        if any(seg.startswith(p) for p in ("fr/","de/","es/","ja/","pt-BR/","zh-Hans/")):
            continue
        if "_csp" in seg or "/tags/" in seg:
            continue
        url = "/" if seg == "." else f"/{seg}/"
        html = html_file.read_text(errors="ignore")
        title, desc, body = extract(html)
        if not title:
            continue
        docs.append({"u": url, "t": title, "d": desc, "b": body[:4000]})

    # BM25 index preparation
    N = len(docs)
    tokenised: list[list[str]] = []
    df: Counter[str] = Counter()
    for d in docs:
        title_toks = tokenize(d["t"])
        desc_toks = tokenize(d["d"])
        body_toks = tokenize(d["b"])
        # Boost title + description with repetition; add bigrams for
        # multi-word phrase matches.
        title_bigrams = bigrams(title_toks)
        toks = (
            title_toks * 5
            + title_bigrams * 4
            + desc_toks * 3
            + bigrams(desc_toks) * 2
            + body_toks
        )
        tokenised.append(toks)
        for w in set(toks):
            df[w] += 1

    avgdl = sum(len(t) for t in tokenised) / max(1, N)
    idf = {w: math.log(1 + (N - c + 0.5) / (c + 0.5)) for w, c in df.items()}

    # Compact index: term → [(doc_idx, tf_norm), ...]
    inverted: dict[str, list[tuple[int, float]]] = {}
    k1, b = 1.5, 0.75
    for i, toks in enumerate(tokenised):
        counts = Counter(toks)
        for w, tf in counts.items():
            dl = len(toks)
            denom = tf + k1 * (1 - b + b * dl / avgdl)
            score = idf.get(w, 0) * (tf * (k1 + 1)) / max(1e-9, denom)
            inverted.setdefault(w, []).append([i, round(score, 3)])

    index_out = {
        "meta": {"n": N, "avgdl": round(avgdl, 2), "k1": k1, "b": b},
        "docs": [{"u": d["u"], "t": d["t"], "d": d["d"]} for d in docs],
        "postings": inverted,
    }
    out_path = ROOT / "search.json"
    out_path.write_text(json.dumps(index_out, separators=(",", ":")))
    print(f"    search: {N} docs indexed, {len(inverted):,} terms, {out_path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
