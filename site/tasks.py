#!/usr/bin/env python3
"""Build and deploy woo.dasopen.nl. Run `inv --list`."""

import re
import shutil
from pathlib import Path

from invoke import Context, task

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
PORT = 1315
# Caddy on bianco serves this folder. Config lives in the stek repo: caddy/sites/static.caddy.
REMOTE = "bianco:/srv/data/pub/www/woo.dasopen.nl"
# The site publishes only the law articles that these folders link to.
SCANNED = ("docs", "templates", "uitspraken")
LAWS = ROOT / "wetten"
LINK = re.compile(r"\]\(([^)\s#]+)")


def linked_laws() -> set[Path]:
    found = set()
    for folder in SCANNED:
        for md in (REPO / folder).glob("*.md"):
            for target in LINK.findall(md.read_text(encoding="utf8")):
                path = (md.parent / target).resolve()
                if path.is_relative_to(REPO / "wetten") and path.is_file():
                    found.add(path)
    return found


@task
def laws(c: Context) -> None:
    """Copy the linked law articles into site/wetten/."""
    shutil.rmtree(LAWS, ignore_errors=True)
    found = linked_laws()
    for src in found:
        dst = LAWS / src.relative_to(REPO / "wetten")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    print(f"{len(found)} law files")


@task(pre=[laws], help={"drafts": "Include draft content"})
def serve(c: Context, drafts: bool = True) -> None:
    """Run the dev server with live reload."""
    with c.cd(str(ROOT)):
        c.run(f"hugo server --port {PORT} {'-D' if drafts else ''}", pty=True)


@task
def clean(c: Context) -> None:
    """Remove build output."""
    shutil.rmtree(ROOT / "public", ignore_errors=True)


@task(pre=[clean, laws])
def build(c: Context) -> None:
    """Build the production site into public/."""
    with c.cd(str(ROOT)):
        c.run("hugo --gc --minify")


@task(help={"dry": "Show changes, copy nothing"})
def deploy(c: Context, dry: bool = False) -> None:
    """Build and copy the site to bianco."""
    build(c)
    flags = "-an --stats" if dry else "-a"
    c.run(f"rsync {flags} --delete --chmod=D755,F644 {ROOT / 'public'}/ {REMOTE}/")


@task
def update(c: Context) -> None:
    """Update the theme module to its latest version."""
    with c.cd(str(ROOT)):
        c.run("hugo mod get -u && hugo mod tidy")
