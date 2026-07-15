#!/usr/bin/env python3
"""Extract Q&A pairs from existing FAQ pages + build a lookup index.

Emits `/qa.json` — a compact `[{q, a, source}]` array — so the in-page
Ask-AI panel can return the closest deterministic Q/A match rather
than a generic snippet.

Also traverses the site for any `## Troubleshooting` / `## Common
failures` sections and extracts the H3 questions + following paragraph
as additional Q/A pairs. This gives us 250+ authoritative pairs
without any LLM call.
"""
from __future__ import annotations
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / "public"
FAQ_DIRS = [ROOT / "faq"]  # dedicated faq/* pages

H2_RE = re.compile(r"<h2[^>]*>([^<]+)</h2>", re.IGNORECASE)
H3_RE = re.compile(r"<h3[^>]*>([^<]+)</h3>", re.IGNORECASE)


def extract_pairs_from_html(text: str, source_url: str) -> list[dict]:
    """Extract Q/A pairs by walking H3 (question) → next paragraph (answer)."""
    pairs: list[dict] = []
    # Match `<h3>Question</h3><p>...</p>` shape
    for m in re.finditer(
        r'<h3[^>]*>([^<]+)</h3>\s*(?:<[^p][^>]*>.*?</[^>]+>)*\s*<p>([^<].{20,500})</p>',
        text, re.DOTALL,
    ):
        q, a = m.group(1).strip(), m.group(2).strip()
        # Clean nested tags in the answer
        a_clean = re.sub(r"<[^>]+>", " ", a)
        a_clean = re.sub(r"\s+", " ", a_clean).strip()
        if 20 <= len(a_clean) <= 500 and q.endswith("?"):
            pairs.append({"q": q, "a": a_clean, "src": source_url})
    return pairs


def extract_troubleshooting(text: str, source_url: str) -> list[dict]:
    """H3 in a Troubleshooting section, treat as a Q/A pair."""
    tshoot_start = re.search(r'<h2[^>]*>(?:Troubleshooting|Common\s+failures|FAQ)[^<]*</h2>', text, re.IGNORECASE)
    if not tshoot_start:
        return []
    tail = text[tshoot_start.end():]
    end = tail.find("<h2")
    section = tail if end < 0 else tail[:end]
    pairs: list[dict] = []
    for m in re.finditer(
        r'<h3[^>]*>([^<]+)</h3>\s*<p>([^<].{20,400})</p>',
        section, re.DOTALL,
    ):
        q_raw, a_raw = m.group(1).strip(), m.group(2).strip()
        q = q_raw if q_raw.endswith("?") else f"How do I handle: {q_raw}?"
        a = re.sub(r"<[^>]+>", " ", a_raw)
        a = re.sub(r"\s+", " ", a).strip()
        pairs.append({"q": q, "a": a, "src": source_url})
    return pairs


def main() -> None:
    pairs: list[dict] = []
    for html_file in ROOT.rglob("index.html"):
        rel = html_file.relative_to(ROOT).parent
        seg = str(rel).replace("\\", "/")
        # English canonical only
        if any(seg.startswith(p) for p in ("fr/", "de/", "es/", "ja/", "pt-BR/", "zh-Hans/")):
            continue
        if "_csp" in seg or "/tags/" in seg:
            continue
        url = "/" if seg == "." else f"/{seg}/"
        html = html_file.read_text(errors="ignore")

        # Isolate <main>
        main_m = re.search(r"<main[^>]*>(.*?)</main>", html, re.DOTALL)
        if not main_m:
            continue
        body = main_m.group(1)

        # FAQ pages: every H3 is a question
        if any(str(html_file).startswith(str(f)) for f in FAQ_DIRS):
            for m in re.finditer(r'<h3[^>]*>([^<]+)</h3>\s*(?:<[^p][^>]*>.*?</[^>]+>)*\s*<p>([^<].+?)</p>', body, re.DOTALL):
                q = m.group(1).strip()
                a = re.sub(r"<[^>]+>", " ", m.group(2))
                a = re.sub(r"\s+", " ", a).strip()
                if 20 <= len(a) <= 500:
                    pairs.append({"q": q if q.endswith("?") else q + "?", "a": a, "src": url})
        else:
            pairs.extend(extract_troubleshooting(body, url))

    # Dedup on question text
    seen = set()
    dedup: list[dict] = []
    for p in pairs:
        key = p["q"].lower()
        if key in seen:
            continue
        seen.add(key)
        dedup.append(p)

    out = ROOT / "qa.json"
    out.write_text(json.dumps({"pairs": dedup}, separators=(",", ":")))
    print(f"    qa:       {len(dedup)} Q/A pairs extracted, {out.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
