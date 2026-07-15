#!/usr/bin/env python3
"""Verify every `internal/…/foo.go` reference in the docs resolves
against the rousseau-agent source tree.

Runs on every build. Catches stale file paths introduced when the code
is refactored but a doc still cites the old name.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path


DOCS_ROOT = Path(__file__).resolve().parents[1] / "content"
SRC_ROOT = Path("/home/seb/team-rousseau-workspace/repos/private/go/rousseau-agent")
KNOWN_HYPOTHETICALS = {"internal/cli/xmpp.go", "internal/transport/xmpp/client.go"}


def main() -> int:
    if not SRC_ROOT.exists():
        print(f"    source root missing ({SRC_ROOT}); skipping", file=sys.stderr)
        return 0

    src_files = {str(p.relative_to(SRC_ROOT)) for p in SRC_ROOT.rglob("*.go")}
    missing: list[tuple[str, str]] = []
    for md in DOCS_ROOT.rglob("*.md"):
        text = md.read_text(errors="ignore")
        for pth in re.findall(r"`(internal/[a-zA-Z0-9/_.-]+\.go)`", text):
            if pth not in src_files and pth not in KNOWN_HYPOTHETICALS:
                missing.append((str(md.relative_to(DOCS_ROOT)), pth))

    print(f"    content: {len(missing)} stale source references")
    if missing:
        for f, p in missing[:20]:
            print(f"      {p} in {f}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
