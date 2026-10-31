#!/usr/bin/env python3
"""Check relative links and #anchors in the hand-written markdown of the knowledge base.

    tools/check_links.py            # docs/, templates/, uitspraken/*.md, top-level *.md
    tools/check_links.py FILE...    # only these files
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
CODE = re.compile(r"```.*?```", re.S)


def default_files() -> list[Path]:
    files = [*ROOT.glob("*.md"), *ROOT.glob("docs/*.md"), *ROOT.glob("templates/*.md"), *ROOT.glob("uitspraken/*.md")]
    return sorted(files)


def slug(heading: str) -> str:
    """GitHub-style anchor."""
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


def anchors(path: Path) -> set[str]:
    text = CODE.sub("", path.read_text(encoding="utf8"))
    return {slug(m) for m in re.findall(r"^#+\s+(.+)$", text, re.M)}


def check(path: Path) -> list[str]:
    errors: list[str] = []
    text = CODE.sub("", path.read_text(encoding="utf8"))
    for target in LINK.findall(text):
        if re.match(r"[a-z]+:", target):
            continue
        file_part, _, anchor = target.partition("#")
        dest = (path.parent / file_part).resolve() if file_part else path
        if not dest.exists():
            errors.append(f"{path.relative_to(ROOT)}: missing {target}")
        elif anchor and dest.suffix == ".md" and anchor not in anchors(dest):
            errors.append(f"{path.relative_to(ROOT)}: no anchor {target}")
    return errors


def main(argv: list[str]) -> None:
    files = [Path(a).resolve() for a in argv] or default_files()
    errors = [e for f in files for e in check(f)]
    print("\n".join(errors) or f"OK: {len(files)} files")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
