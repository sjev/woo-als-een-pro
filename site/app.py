#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["fastapi", "uvicorn", "markdown-it-py", "mdit-py-plugins", "pyyaml", "watchfiles"]
# ///
"""Serve woo.dasopen.nl: repo markdown for agents, the same pages as HTML for people.

    site/app.py               # http://localhost:8000
    site/app.py --port 8080
    site/app.py --reload      # dev: restart on code changes, refresh pages on content changes

/llms.txt is the agent entry point; / is the same content as HTML.
/<path>.md is the raw file; /<path>.html renders it. Files are read on each request.
A folder or extensionless path redirects to its file; a miss returns a markdown 404 with index links.
/termijn computes a deadline with tools/termijn.py.
"""

from __future__ import annotations

import argparse
import html
import logging
import os
import re
import sys
from collections.abc import AsyncIterator
from datetime import date
from pathlib import Path
from urllib.parse import quote

import uvicorn
import yaml
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, Response, StreamingResponse
from watchfiles import awatch

SITE = Path(__file__).resolve().parent
REPO = SITE.parent
sys.path[:0] = [str(SITE), str(REPO / "tools")]
from render import LINK, LIVE, SCHEME, to_html  # noqa: E402
from termijn import report  # noqa: E402

TERMIJN_USAGE = """Usage: /termijn?datum=YYYY-MM-DD&duur=4w[,2w,12d]

datum: the event (receipt, notice, decision). The term starts the day after.
duur:  one or more periods, comma-separated; w = weeks, d = days.
Chained periods: the Algemene termijnenwet is applied per step and at the end; the later date is given.
"""
TERMIJN_OPTIONS = {
    "2w": "2 weken",
    "4w": "4 weken",
    "4w,2w": "4 + 2 weken (verdaagd)",
    "6w": "6 weken",
    "8w": "8 weken",
    "12w": "12 weken",
}
GITHUB = "https://github.com/sjev/woo-als-een-pro/tree/main/"
RAW = "https://raw.githubusercontent.com/sjev/woo-als-een-pro/main/"
# Served in full, with the files they link to (full texts of rulings, sources).
# All law text is served too, so agents can fetch any article by its path.
SECTIONS = {"docs": "Kennisbank", "templates": "Sjablonen", "uitspraken": "Uitspraken"}
FRONT = re.compile(r"\A---\n(.*?)\n---\n", re.S)


def split(text: str) -> tuple[dict, str]:
    match = FRONT.match(text)
    return (yaml.safe_load(match[1]) or {}, text[match.end() :]) if match else ({}, text)


def linked() -> set[Path]:
    seeds = [md for folder in SECTIONS for md in (REPO / folder).glob("*.md")]
    return {(md.parent / t).resolve() for md in seeds for _, t in LINK.findall(md.read_text("utf8")) if not SCHEME.match(t)}


def served(path: Path, links: set[Path]) -> bool:
    if path.suffix != ".md" or not path.is_file() or not path.is_relative_to(REPO):
        return False
    parts = path.relative_to(REPO).parts
    return parts[0] == "wetten" or (len(parts) == 2 and parts[0] in SECTIONS) or path in links


def rewrite(src: Path, links: set[Path]) -> str:
    """A link to a repo file that is not served goes to the raw file on GitHub; a folder to its GitHub page."""

    def fix(m: re.Match[str]) -> str:
        path = (src.parent / m[2]).resolve()
        if SCHEME.match(m[2]) or not path.is_relative_to(REPO) or served(path, links):
            return m[0]
        return m[1] + (RAW if path.is_file() else GITHUB) + path.relative_to(REPO).as_posix()

    return LINK.sub(fix, src.read_text("utf8"))


def entry(md: Path, base: str) -> tuple[object, str]:
    """Sort key and index line. Rulings: newest first, title as description."""
    m, url = split(md.read_text("utf8"))[0], base + md.relative_to(REPO).as_posix()
    if "ecli" in m:
        return str(m["datum"]), f"- [{m['ecli']}]({url}) ({m['datum']}): {m['title']}"
    return -m.get("weight", 99), f"- [{m['title']}]({url}): {m['summary']}"


def llms(base: str) -> str:
    """site/llms.md links from the site root (`](/...`); base makes them absolute."""
    parts = [(SITE / "llms.md").read_text("utf8").rstrip().replace("](/", "](" + base)]
    for folder, name in SECTIONS.items():
        entries = sorted((entry(md, base) for md in (REPO / folder).glob("*.md") if md.name != "README.md"), reverse=True)
        parts.append(f"## {name}\n\n" + "\n".join(line for _, line in entries))
    return "\n\n".join(parts) + "\n"


NOT_FOUND = """# Niet gevonden

`/{path}` staat niet op deze site.

- Begin bij [llms.txt](/llms.txt): werkwijze en index van alle pagina's.
- Een wetsartikel staat op `/wetten/<wet>/artikel_<nr>.md`. Punt en dubbele punt worden een koppelteken: art. 6:12 Awb is `/wetten/awb/artikel_6-12.md`.
- Alle wetten: [wetten/README.md](/wetten/README.md).
"""


def not_found(path: str) -> Response:
    """Markdown 404 that points an agent back to an index."""
    text = NOT_FOUND.format(path=path)
    parts = path.split("/")
    if len(parts) > 2 and parts[0] == "wetten" and (REPO / "wetten" / parts[1] / "_wet.md").is_file():
        text += f"- Alle artikelen van deze wet: [wetten/{parts[1]}/_wet.md](/wetten/{parts[1]}/_wet.md).\n"
    return Response(text, status_code=404, media_type="text/markdown; charset=utf-8")


def canonical(path: str, links: set[Path]) -> str | None:
    """Served file for a folder or an extensionless path: wetten/woo/ is wetten/woo/_wet.md, docs/ is llms.txt."""
    src = (REPO / path).resolve()
    if path.strip("/") in SECTIONS and not (src / "README.md").is_file():
        return "llms.txt"
    if src.is_dir():
        candidates = [src / "_wet.md", src / "README.md"]
    elif not src.suffix:
        candidates = [src.with_name(src.name + ".md")]
    else:
        return None
    hit = next((c for c in candidates if served(c, links)), None)
    return hit.relative_to(REPO).as_posix() if hit else None


app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


@app.api_route("/llms.txt", methods=["GET", "HEAD"], response_class=PlainTextResponse)
def llms_txt(request: Request) -> str:
    return llms(str(request.base_url))


@app.api_route("/termijn", methods=["GET", "HEAD"], response_class=PlainTextResponse)
def termijn(datum: str = "", duur: str = "") -> PlainTextResponse:
    try:
        return PlainTextResponse(report(date.fromisoformat(datum), duur.split(",")))
    except ValueError as e:
        return PlainTextResponse(f"Error: {e}\n\n{TERMIJN_USAGE}", status_code=400)


@app.api_route("/termijn.html", methods=["GET", "HEAD"], response_class=HTMLResponse)
def termijn_form(datum: str = "", duur: str = "4w") -> str:
    datum = datum or date.today().isoformat()
    try:
        result = report(date.fromisoformat(datum), duur.split(","))
    except ValueError as e:
        result = f"Error: {e}\n"
    options = "".join(
        f'<option value="{v}"{" selected" if v == duur else ""}>{label}</option>' for v, label in TERMIJN_OPTIONS.items()
    )
    form = (
        '<form action="/termijn.html">'
        f'<label>Datum gebeurtenis <input type="date" name="datum" value="{html.escape(datum)}" required></label> '
        f'<label>Termijn <select name="duur">{options}</select></label> '
        "<button>Bereken</button></form>"
    )
    text = (
        "# Termijn berekenen\n\nDe termijn begint de dag na de gebeurtenis. "
        "De regels staan in [Termijn berekenen](/docs/stappenplan.md#termijn-berekenen).\n\n"
        f"{form}\n\n```\n{result}```\n"
    )
    return to_html(text, "Termijn berekenen", f"/termijn?datum={quote(datum)}&duur={quote(duur)}")


if LIVE:
    logging.getLogger("uvicorn.access").addFilter(lambda r: "/_live" not in r.getMessage())

    @app.get("/_live")
    async def live() -> StreamingResponse:
        async def events() -> AsyncIterator[str]:
            yield "retry: 500\n\n"
            async for _ in awatch(REPO, watch_filter=lambda _, p: p.endswith(".md")):
                yield "data: reload\n\n"

        return StreamingResponse(events(), media_type="text/event-stream")


@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
def home() -> str:
    return to_html(llms("/"), "Woo als een pro", "/llms.txt")


@app.api_route("/{path:path}", methods=["GET", "HEAD"])
def page(path: str) -> Response:
    is_html = path.endswith(".html")
    src = (REPO / (path[:-5] + ".md" if is_html else path)).resolve()
    links = linked()
    if not served(src, links):
        target = canonical(path, links) if src.is_relative_to(REPO) else None
        return RedirectResponse("/" + target, status_code=308) if target else not_found(path)
    text = rewrite(src, links)
    if not is_html:
        return Response(text, media_type="text/markdown; charset=utf-8")
    meta, body = split(text)
    title = str(meta.get("title", src.stem))
    if not re.search(r"^# ", body, re.M):
        body = f"# {title}\n\n{body}"
    if "source" in meta:
        body += f"\n\nBron: <{meta['source']}>\n"
    return HTMLResponse(to_html(body, title, "/" + path[:-5] + ".md"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true", help="dev: restart on code changes, refresh pages on content changes")
    args = parser.parse_args()
    if args.reload:
        os.environ["WOO_LIVE"] = "1"  # inherited by the reloader's worker process
        uvicorn.run(
            "app:app",
            app_dir=str(SITE),
            host=args.host,
            port=args.port,
            reload=True,
            reload_dirs=[str(SITE), str(REPO / "tools")],
            timeout_graceful_shutdown=1,  # open /_live streams would block a restart
        )
        return
    # Behind Caddy: take scheme and host for llms.txt from the forwarded headers.
    uvicorn.run(app, host=args.host, port=args.port, proxy_headers=True, forwarded_allow_ips="*")


if __name__ == "__main__":
    main()
