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
# GitHub alert syntax: "> [!WARNING]" renders as a styled note; raw markdown stays a plain quote.
# The marker only sets the style; the author writes any heading below it.
ALERT = re.compile(r"<blockquote>\n<p>\[!(NOTE|WARNING)\](</p>\n|\s*)")


def slug(heading: str) -> str:
    """GitHub-style anchor, as in tools/check_links.py."""
    return re.sub(r"[^\w\- ]", "", heading.strip().lower()).replace(" ", "-")


MD = MarkdownIt("commonmark").enable("table").use(anchors_plugin, max_level=6, slug_func=slug)


GITHUB_ICON = (
    '<svg viewBox="0 0 16 16" width="20" height="20" fill="currentColor" aria-hidden="true" style="vertical-align:text-bottom">'
    '<path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49'
    "-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87"
    ".51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27"
    ".68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29"
    '.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/></svg>'
)


def to_html(text: str, title: str, source: str) -> str:
    def link(m: re.Match[str]) -> str:
        return m[1] + m[2][:-3] + ".html" if m[2].endswith(".md") and not SCHEME.match(m[2]) else m[0]

    body = MD.render(LINK.sub(link, text))
    body = ALERT.sub(lambda m: f'<blockquote class="{m[1].lower()}">\n' + ("" if m[2].startswith("</p>") else "<p>"), body)
    return f"""<!doctype html>
<html lang="nl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<link rel="stylesheet" href="/pico.min.css">
<title>{html.escape(title)}</title>
<link rel="alternate" type="text/markdown" href="{source}">
<style>
{CSS.read_text('utf8')}</style>
</head>
<body>
<header class="container"><nav>
<ul><li><a href="/"><strong>Woo als een pro</strong></a></li></ul>
<ul><li><a href="/termijn.html">Termijn berekenen</a></li><li><a href="{source}">llms.txt</a></li><li><a href="https://github.com/sjev/woo-als-een-pro" aria-label="GitHub" title="GitHub">{GITHUB_ICON}</a></li></ul>
</nav></header>
<main class="container">
{body}</main>
{LIVE_JS if LIVE else ''}
</body>
</html>
"""
