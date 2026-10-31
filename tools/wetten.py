#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pyyaml"]
# ///
"""Fetch laws from the Basiswettenbestand and split them into one file per article.

    tools/wetten.py add BWBR0045754 woo    # add a law under wetten/woo/
    tools/wetten.py update                 # refetch every law in wetten/
    tools/wetten.py update woo awb         # refetch some laws
"""

from __future__ import annotations

import re
import sys
import urllib.parse
import urllib.request
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

import yaml

ROOT = Path(__file__).resolve().parent.parent / "wetten"
SRU_URL = "https://zoekservice.overheid.nl/sru/Search"
SECTIONS = ("titeldeel", "afdeling", "paragraaf", "sub-paragraaf")
NS = {
    "srw": "http://www.loc.gov/zing/srw/",
    "gzd": "http://standaarden.overheid.nl/sru",
    "bwb": "http://standaarden.overheid.nl/bwb/terms/",
    "dcterms": "http://purl.org/dc/terms/",
}


@dataclass
class Article:
    nr: str
    hoofdstuk: str
    secties: list[str]
    titel: str
    text: str


@dataclass
class Law:
    bwb_id: str
    title: str
    short_title: str
    valid_from: str
    source: str
    articles: list[Article] = field(default_factory=list)
    bijlagen: list[Article] = field(default_factory=list)


def get(url: str) -> str:
    with urllib.request.urlopen(url, timeout=60) as resp:
        return resp.read().decode("utf8")


def current_toestand(bwb_id: str) -> tuple[str, str, str]:
    """(url, title, valid_from) of the toestand with no end date."""
    # Awb has 200+ toestanden; one large page is simpler than paging.
    params = {
        "version": "1.2",
        "operation": "searchRetrieve",
        "x-connection": "BWB",
        "query": f"dcterms.identifier=={bwb_id}",
        "maximumRecords": "500",
    }
    root = ET.fromstring(get(f"{SRU_URL}?{urllib.parse.urlencode(params)}"))
    for record in root.iterfind(".//srw:record", NS):
        meta = record.find(".//gzd:bwbipm", NS)
        if meta is None or meta.findtext("bwb:geldigheidsperiode_einddatum", namespaces=NS) != "9999-12-31":
            continue
        url = record.findtext(".//bwb:locatie_toestand", namespaces=NS)
        if url:
            start = meta.findtext("bwb:geldigheidsperiode_startdatum", namespaces=NS) or ""
            return url, record.findtext(".//dcterms:title", namespaces=NS) or "", start
    raise LookupError(f"No current toestand for {bwb_id}.")


def words(el: ET.Element) -> str:
    parts = [el.text or ""]
    for child in el:
        if child.tag != "meta-data":
            parts.append(words(child))
        parts.append(child.tail or "")
    return "".join(parts)


def text(el: ET.Element | None) -> str:
    return " ".join(words(el).split()) if el is not None else ""


def content_text(children: Iterable[ET.Element], depth: int = 0) -> str:
    """Each <al> on its own line; nested list content one indent deeper."""
    pad = "   " * depth
    parts = []
    for child in children:
        if child.tag in ("al", "tussenkop"):
            parts.append(pad + text(child))
        elif child.tag == "lijst":
            for li in child.findall("li"):
                nr = (li.findtext("li.nr") or "-").replace("•", "-")
                body = [c for c in li if c.tag not in ("li.nr", "meta-data")]
                head = body.pop(0) if body and body[0].tag == "al" else None
                parts.append(f"{pad}{nr} {text(head)}".rstrip())
                parts.append(content_text(body, depth + 1))
    return "\n".join(p for p in parts if p.strip())


def article_text(artikel: ET.Element) -> str:
    blocks: list[str] = []
    run: list[ET.Element] = []
    for child in artikel:
        if child.tag != "lid":
            run.append(child)
            continue
        blocks.append(content_text(run))
        run = []
        nr = child.findtext("lidnr") or ""
        body = content_text(child)
        blocks.append(f"{nr}. {body}" if nr else body)
    blocks.append(content_text(run))
    return "\n\n".join(b for b in blocks if b)


def bijlage_text(el: ET.Element) -> str:
    """Appendices nest divisions and articles; each nested heading becomes ###."""
    blocks: list[str] = []
    for child in el:
        if child.tag == "kop" and el.tag != "bijlage":
            blocks.append("### " + text(child))
        elif child.tag in ("al", "tussenkop", "lijst"):
            blocks.append(content_text([child]))
        elif child.tag == "artikel":
            blocks.append(f"### {text(child.find('kop'))}\n\n{article_text(child)}")
        elif child.tag not in ("kop", "meta-data"):
            blocks.append(bijlage_text(child))
    return "\n\n".join(b for b in blocks if b)


def is_spent_amendment(artikel: ET.Element) -> bool:
    """An article that only amends another law. The change already sits in that law."""
    body = [c for c in artikel if c.tag not in ("kop", "meta-data")]
    if len(body) != 1 or body[0].tag != "al" or body[0].find("redactie") is None:
        return False
    return text(body[0]).startswith("Wijzigt")


def heading(el: ET.Element, word: str) -> str:
    return f"{word} {text(el.find('kop/nr'))}. {text(el.find('kop/titel'))}".strip(". ").strip()


def collect(el: ET.Element, hoofdstuk: str, secties: list[str], out: list[Article]) -> None:
    for child in el:
        if child.tag == "hoofdstuk":
            collect(child, heading(child, ""), secties, out)
        elif child.tag in SECTIONS:
            word = text(child.find("kop/label")) or child.tag.capitalize()
            collect(child, hoofdstuk, [*secties, heading(child, word)], out)
        elif child.tag == "artikel" and not is_spent_amendment(child):
            # Repealed articles may lack <nr>; the label still carries the number.
            nr = text(child.find("kop/nr")) or child.get("label", "").removeprefix("Artikel ").strip()
            titel = text(child.find("kop/titel"))
            out.append(Article(nr, hoofdstuk, secties, titel, article_text(child)))


def fetch(bwb_id: str) -> Law:
    url, title, valid_from = current_toestand(bwb_id)
    root = ET.fromstring(get(url))
    law = Law(bwb_id, title, text(root.find(".//citeertitel")) or title, valid_from, url)
    wettekst = root.find(".//wettekst")
    if wettekst is not None:
        collect(wettekst, "", [], law.articles)
    for el in root.iterfind(".//wetgeving/*/bijlage"):
        label = el.get("label") or "Bijlage"
        law.bijlagen.append(Article(label, "", [], text(el.find("kop/titel")), bijlage_text(el)))
    return law


def frontmatter(meta: dict[str, str], body: str) -> str:
    dumped = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False)
    return f"---\n{dumped}---\n\n{body.strip()}\n"


def article_file(a: Article) -> str:
    return "artikel_" + a.nr.replace(".", "-").replace(":", "-") + ".md"


def bijlage_file(b: Article) -> str:
    return b.nr.lower().replace(" ", "_") + ".md"


def toc(articles: list[Article]) -> str:
    lines: list[str] = []
    last_h: str | None = None
    last_s: list[str] = []
    for a in articles:
        if a.hoofdstuk != last_h:
            if a.hoofdstuk:
                lines.append(f"\n## Hoofdstuk {a.hoofdstuk}\n")
            last_h, last_s = a.hoofdstuk, []
        for depth, sectie in enumerate(a.secties):
            if depth >= len(last_s) or last_s[depth] != sectie:
                lines.append(f"\n### {sectie}\n")
        last_s = a.secties
        link = f"- [Artikel {a.nr}]({article_file(a)})"
        lines.append(f"{link} — {a.titel}" if a.titel else link)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines))


def write(slug: str, law: Law) -> None:
    """Replace wetten/<slug>/ with `_wet.md` and one `artikel_*.md` per article."""
    folder = ROOT / slug
    folder.mkdir(exist_ok=True)
    for old in folder.glob("*.md"):
        old.unlink()
    fetched_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    wet = {
        "bwb_id": law.bwb_id,
        "title": law.title,
        "short_title": law.short_title,
        "valid_from": law.valid_from,
        "fetched_at": fetched_at,
        "source": law.source,
    }
    bijlagen = "".join(f"\n- [{b.nr}]({bijlage_file(b)}) {b.titel}".rstrip() for b in law.bijlagen)
    body = toc(law.articles) + (f"\n\n## Bijlagen\n{bijlagen}" if bijlagen else "")
    (folder / "_wet.md").write_text(frontmatter(wet, body), encoding="utf8")
    for b in law.bijlagen:
        meta = {"wet": law.title, "bijlage": b.nr, "titel": b.titel, "valid_from": law.valid_from, "source": law.source}
        (folder / bijlage_file(b)).write_text(frontmatter(meta, b.text), encoding="utf8")
    for a in law.articles:
        meta = {"wet": law.title, "artikel": a.nr}
        if a.hoofdstuk:
            meta["hoofdstuk"] = a.hoofdstuk
        meta |= {"valid_from": law.valid_from, "source": law.source}
        (folder / article_file(a)).write_text(frontmatter(meta, a.text), encoding="utf8")


def add(bwb_id: str, slug: str) -> None:
    law = fetch(bwb_id)
    write(slug, law)
    print(f"{slug}: {law.title}, {len(law.articles)} artikelen, geldig vanaf {law.valid_from}")


def bwb_id_of(slug: str) -> str:
    raw = (ROOT / slug / "_wet.md").read_text(encoding="utf8")
    return yaml.safe_load(raw.split("---")[1])["bwb_id"]


def main(argv: list[str]) -> None:
    match argv:
        case ["add", bwb_id, slug]:
            add(bwb_id, slug)
        case ["update", *slugs]:
            for slug in slugs or sorted(p.parent.name for p in ROOT.glob("*/_wet.md")):
                add(bwb_id_of(slug), slug)
        case _:
            sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
