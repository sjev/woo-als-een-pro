#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Fetch court rulings from the open data of rechtspraak.nl.

    tools/uitspraak.py ECLI:NL:RVS:2022:3027 [ECLI...]

Saves the full text to uitspraken/tekst/<ECLI-with-dashes>.md and prints it.
The curated file uitspraken/<ECLI>.md (kern, citaten, gebruik) is written by hand.
"""

from __future__ import annotations

import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

import yaml

OUT = Path(__file__).resolve().parent.parent / "uitspraken" / "tekst"
API = "https://data.rechtspraak.nl/uitspraken/content?id="
PUBLIC = "https://uitspraken.rechtspraak.nl/details?id="
RDF = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}"
RS = "{http://www.rechtspraak.nl/schema/rechtspraak-1.0}"
DC = "{http://purl.org/dc/terms/}"
PSI = "{http://psi.rechtspraak.nl/}"


def flat(el: ET.Element) -> str:
    return " ".join("".join(el.itertext()).split())


def blocks(el: ET.Element) -> list[str]:
    """Titles and innermost paragraphs, in document order."""
    out: list[str] = []
    for node in el.iter():
        tag = node.tag.removeprefix(RS)
        if tag == "title":
            out.append("## " + flat(node))
        elif tag == "para" and node.find(f".//{RS}para") is None and flat(node):
            out.append(flat(node))
    return out


def file_name(ecli: str) -> str:
    return ecli.replace(":", "-") + ".md"


def fetch(ecli: str) -> str:
    with urllib.request.urlopen(API + ecli, timeout=60) as resp:
        root = ET.fromstring(resp.read())
    desc = root.find(f"{RDF}RDF/{RDF}Description")
    if desc is None:
        raise LookupError(f"No metadata for {ecli}.")
    meta = {
        "ecli": ecli,
        "datum": desc.findtext(f"{DC}date"),
        "instantie": desc.findtext(f"{DC}creator"),
        "zaaknummer": desc.findtext(f"{PSI}zaaknummer"),
        "procedure": desc.findtext(f"{PSI}procedure"),
        "url": PUBLIC + ecli,
        "fetched_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }
    indicatie = root.find(f"{RS}inhoudsindicatie")
    body = root.find(f"{RS}uitspraak")
    if body is None:
        body = root.find(f"{RS}conclusie")
    if body is None:
        raise LookupError(f"No text for {ecli}.")
    parts = ["## Inhoudsindicatie", "\n\n".join(blocks(indicatie)) if indicatie is not None else ""]
    parts += ["## Uitspraak", "\n\n".join(blocks(body))]
    text = "\n\n".join(p for p in parts if p)
    dumped = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False)
    return f"---\n{dumped}---\n\n{text}\n"


def main(argv: list[str]) -> None:
    if not argv or not all(re.fullmatch(r"ECLI:[A-Z]{2}:[A-Z]+:\d{4}:[\w.]+", e) for e in argv):
        sys.exit(__doc__)
    OUT.mkdir(parents=True, exist_ok=True)
    for ecli in argv:
        doc = fetch(ecli)
        path = OUT / file_name(ecli)
        path.write_text(doc, encoding="utf8")
        print(doc)
        print(f"saved: {path.relative_to(OUT.parent.parent)}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:])
