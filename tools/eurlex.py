"""Fetch an EU act (Dutch text) from the Publications Office Cellar and split it into articles.

Used by wetten.py for ids like CELEX:32016R0679. EUR-Lex itself blocks scripts; the Cellar
serves the same XHTML through content negotiation.
"""

from __future__ import annotations

import re
import urllib.request
from xml.etree import ElementTree as ET

CELLAR = "http://publications.europa.eu/resource/celex/"
X = "{http://www.w3.org/1999/xhtml}"


def get_xhtml(celex: str) -> tuple[str, ET.Element]:
    req = urllib.request.Request(CELLAR + celex, headers={"Accept": "application/xhtml+xml", "Accept-Language": "nld"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.geturl(), ET.fromstring(resp.read())


def flat(el: ET.Element) -> str:
    return " ".join("".join(el.itertext()).split())


def cls(el: ET.Element) -> str:
    return el.get("class", "")


def render(el: ET.Element, depth: int = 0) -> list[str]:
    """Paragraph <p> per line; list tables (label cell + body cell) as 'a) text', nested one indent deeper."""
    pad = "   " * depth
    lines: list[str] = []
    for child in el:
        tag = child.tag.removeprefix(X)
        if tag == "p" and "oj-normal" in cls(child):
            lines.append(pad + flat(child))
        elif tag == "table":
            for row in child.iter(f"{X}tr"):
                cells = row.findall(f"{X}td")
                if len(cells) != 2:
                    continue
                body = render(cells[1], depth + 1)
                head = body.pop(0).strip() if body else ""
                lines.append(f"{pad}{flat(cells[0])} {head}".rstrip())
                lines.extend(body)
        elif tag == "div":
            block = render(child, depth)
            if block:
                lines.extend(["", *block] if lines else block)
    return lines


def article(div: ET.Element) -> tuple[str, str, str]:
    """(nr, title, text) of one <div id="art_N">."""
    nr = div.get("id", "").removeprefix("art_")
    title_el = div.find(f".//{X}p[@class='oj-sti-art']")
    body = [c for c in div if not cls(c).startswith("eli-title") and "oj-ti-art" not in cls(c)]
    holder = ET.Element("div")
    holder.extend(body)
    text = "\n".join(render(holder))
    return nr, flat(title_el) if title_el is not None else "", re.sub(r"\n{3,}", "\n\n", text).strip()


def fetch_act(celex: str) -> tuple[str, str, list[tuple[str, str, str, str]]]:
    """(title, source url, [(nr, chapter, title, text)]) for an EU act."""
    url, root = get_xhtml(celex)
    doc_title = next((flat(p) for p in root.iter(f"{X}p") if "oj-doc-ti" in cls(p)), celex)
    out: list[tuple[str, str, str, str]] = []
    for cpt in root.iter(f"{X}div"):
        if not re.fullmatch(r"cpt_[IVXLC]+", cpt.get("id", "")):
            continue
        roman = cpt.get("id", "").removeprefix("cpt_")
        tit = cpt.find(f"{X}div[@class='eli-title']")
        chapter = f"{roman}. {flat(tit)}" if tit is not None else roman
        for div in cpt.iter(f"{X}div"):
            if re.fullmatch(r"art_\d+", div.get("id", "")):
                nr, title, text = article(div)
                out.append((nr, chapter, title, text))
    return doc_title, url, out
