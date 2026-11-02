"""Render repo markdown as HTML for people; agents get the raw markdown."""

from __future__ import annotations

import html
import re

from markdown_it import MarkdownIt
from mdit_py_plugins.anchors import anchors_plugin

LINK = re.compile(r"(\]\()([^)\s#]+)")
SCHEME = re.compile(r"[a-z]+:")
CSS = """
:root { color-scheme: light dark; }
body { font: 1rem/1.6 system-ui, sans-serif; max-width: 48rem; margin: 2rem auto; padding: 0 1rem; }
nav { font-size: .9rem; margin-bottom: 2rem; }
table { border-collapse: collapse; display: block; overflow-x: auto; }
th, td { border: 1px solid #8886; padding: .3rem .5rem; vertical-align: top; }
blockquote { margin: 1rem 0; padding: 0 1rem; border-left: 3px solid #8888; }
pre { overflow-x: auto; }
"""


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
<style>{CSS}</style>
</head>
<body>
<nav><a href="/">Woo als een pro</a> · <a href="/termijn.html">termijn berekenen</a> ·<a href="{source}">bron voor agents</a></nav>
<main>
{body}</main>
</body>
</html>
"""
