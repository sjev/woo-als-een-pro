#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Build woo.dasopen.nl: the repo markdown as-is, indexed by llms.txt.

    site/build.py               # build into site/public/
    site/build.py deploy        # build and copy to bianco
    site/build.py deploy --dry  # show changes, copy nothing
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path

import yaml

SITE = Path(__file__).resolve().parent
REPO = SITE.parent
OUT = SITE / "public"
BASE = "https://woo.dasopen.nl/"
GITHUB = "https://github.com/sjev/woo-als-een-pro/tree/main/"
RAW = "https://raw.githubusercontent.com/sjev/woo-als-een-pro/main/"
# Caddy on bianco serves this folder. Config: stek repo, caddy/sites/static.caddy.
REMOTE = "bianco:/srv/data/pub/www/woo.dasopen.nl"
# Published in full, with the files they link to (full texts of rulings, sources).
# All law text is published too, so agents can fetch any article by its path.
SECTIONS = {"docs": "Kennisbank", "templates": "Sjablonen", "uitspraken": "Uitspraken"}
LINK = re.compile(r"(\]\()([^)\s#]+)")
FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)
SCHEME = re.compile(r"[a-z]+:")


def targets(md: Path) -> set[Path]:
    found = LINK.findall(md.read_text(encoding="utf8"))
    return {(md.parent / t).resolve() for _, t in found if not SCHEME.match(t)}


def pages() -> set[Path]:
    seeds = {md for folder in SECTIONS for md in (REPO / folder).glob("*.md")}
    linked = {p for md in seeds for p in targets(md)}
    linked = {p for p in linked if p.is_file() and p.suffix == ".md" and p.is_relative_to(REPO)}
    return seeds | linked | set((REPO / "wetten").rglob("*.md"))


def rewrite(md: Path, published: set[Path]) -> str:
    """A link to a file that is not on the site goes to the raw file on GitHub; a folder to its GitHub page."""

    def fix(m: re.Match[str]) -> str:
        path = (md.parent / m[2]).resolve()
        if SCHEME.match(m[2]) or path in published or not path.is_relative_to(REPO):
            return m[0]
        return m[1] + (RAW if path.is_file() else GITHUB) + path.relative_to(REPO).as_posix()

    return LINK.sub(fix, md.read_text(encoding="utf8"))


def meta(md: Path) -> dict:
    match = FRONT.match(md.read_text(encoding="utf8"))
    return yaml.safe_load(match[1]) if match else {}


def entry(md: Path) -> tuple[object, str]:
    """Sort key and index line. Rulings: newest first, title as description."""
    m, url = meta(md), BASE + md.relative_to(REPO).as_posix()
    if "ecli" in m:
        return str(m["datum"]), f"- [{m['ecli']}]({url}) ({m['datum']}): {m['title']}"
    return -m.get("weight", 99), f"- [{m['title']}]({url}): {m['summary']}"


def llms() -> str:
    parts = [(SITE / "llms.md").read_text(encoding="utf8").rstrip()]
    for folder, name in SECTIONS.items():
        entries = sorted((entry(md) for md in (REPO / folder).glob("*.md") if md.name != "README.md"), reverse=True)
        parts.append(f"## {name}\n\n" + "\n".join(line for _, line in entries))
    return "\n\n".join(parts) + "\n"


def build() -> None:
    shutil.rmtree(OUT, ignore_errors=True)
    published = pages()
    for md in published:
        dst = OUT / md.relative_to(REPO)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(rewrite(md, published), encoding="utf8")
    shutil.copy2(SITE / "index.html", OUT / "index.html")
    (OUT / "llms.txt").write_text(llms(), encoding="utf8")
    print(f"{len(published)} pages in {OUT}")


def deploy(dry: bool) -> None:
    build()
    flags = ["-an", "--stats"] if dry else ["-a"]
    subprocess.run(["rsync", *flags, "--delete", "--chmod=D755,F644", f"{OUT}/", f"{REMOTE}/"], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", nargs="?", choices=["build", "deploy"], default="build")
    parser.add_argument("--dry", action="store_true", help="deploy: show changes, copy nothing")
    args = parser.parse_args()
    deploy(args.dry) if args.command == "deploy" else build()


if __name__ == "__main__":
    main()
