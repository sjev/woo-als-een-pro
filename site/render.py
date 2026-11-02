"""Render repo markdown as HTML for people; agents get the raw markdown."""

from __future__ import annotations

import html
import os
import re
from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.anchors import anchors_plugin

LINK = re.compile(r"(\]\()([^)\s#]+)")
SCHEME = re.compile(r"[a-z]+:")
# Dev only (site/app.py --reload): the server pushes on content changes.
# A reconnect means the server restarted after a code change: reload too.
LIVE = os.environ.get("WOO_LIVE") == "1"
LIVE_JS = """<script>
let up = false;
const es = new EventSource("/_live");
es.onmessage = () => location.reload();
es.onopen = () => { if (up) location.reload(); up = true; };
</script>"""
CSS = Path(__file__).with_name("style.css")


def slug(heading: str) -> str:
    """GitHub-style anchor, as in tools/check_links.py."""
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


MD = MarkdownIt("commonmark").enable("table").use(anchors_plugin, max_level=6, slug_func=slug)


def to_html(text: str, title: str, source: str) -> str:
    def link(m: re.Match[str]) -> str:
        return m[1] + m[2][:-3] + ".html" if m[2].endswith(".md") and not SCHEME.match(m[2]) else m[0]

    body = MD.render(LINK.sub(link, text))
    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="alternate" type="text/markdown" href="{source}">
<style>
{CSS.read_text('utf8')}</style>
</head>
<body>
<nav><a href="/">Woo als een pro</a> · <a href="/termijn.html">termijn berekenen</a> ·<a href="{source}">llms.txt</a></nav>
<main>
{body}</main>
{LIVE_JS if LIVE else ''}
</body>
</html>
"""
