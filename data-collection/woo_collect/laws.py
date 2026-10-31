import re
from datetime import date
from pathlib import Path

import httpx
from lxml import etree

SRU = "https://zoekservice.overheid.nl/sru/Search"

CONTAINERS = {"boek", "deel", "hoofdstuk", "titeldeel", "afdeling", "paragraaf", "sub-paragraaf", "bijlage"}
SKIP = {
    "meta-data", "bwb-inputbestand", "bwb-wijzigingen", "redactionele-correcties",
    "kop", "lidnr", "li.nr", "wetsluiting", "aanhef", "redactie",
}


def resolve_law_url(bwb: str, http: httpx.Client) -> str:
    """Return the XML url of the version in force today."""
    params = {
        "operation": "searchRetrieve", "version": "2.0", "x-connection": "BWB",
        "query": f"dcterms.identifier=={bwb}", "maximumRecords": "1000",
    }
    root = etree.fromstring(http.get(SRU, params=params).content)
    today = date.today().isoformat()
    for record in root.iter("{*}record"):
        start = record.findtext(".//{*}geldigheidsperiode_startdatum") or ""
        end = record.findtext(".//{*}geldigheidsperiode_einddatum") or ""
        if start <= today <= end:
            return record.findtext(".//{*}locatie_toestand")
    raise LookupError(f"no version of {bwb} in force on {today}")


def text(el: etree._Element) -> str:
    parts = [el.text or ""]
    for child in el:
        if child.tag not in SKIP:
            parts.append(text(child))
        parts.append(child.tail or "")
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def heading(el: etree._Element) -> str:
    kop = el.find("kop")
    if kop is None:
        return el.tag.capitalize()
    parts = (kop.find(x) for x in ("label", "nr", "titel"))
    return " ".join(text(p) for p in parts if p is not None and text(p))


def render(el: etree._Element, depth: int, out: list[str]) -> None:
    tag = el.tag
    if tag in SKIP or not isinstance(tag, str):
        return
    if tag in CONTAINERS:
        out.append(f"\n{'#' * min(depth, 5)} {heading(el)}\n")
        for child in el:
            render(child, depth + 1, out)
    elif tag == "artikel":
        out.append(f"\n{'#' * min(depth, 6)} {heading(el)}\n")
        for child in el:
            render(child, depth + 1, out)
    elif tag == "lid":
        nr = el.findtext("lidnr", "").strip()
        body: list[str] = []
        for child in el:
            render(child, depth, body)
        first, *rest = body or [""]
        out.append(f"\n{nr} {first.lstrip()}" if nr else first)
        out.extend(rest)
    elif tag == "li":
        nr = el.findtext("li.nr", "").strip()
        indent = "  " * (sum(1 for _ in el.iterancestors("lijst")) - 1)
        line = " ".join(text(c) for c in el if c.tag == "al")
        out.append(f"{indent}- {nr} {line}".rstrip())
        for child in el:
            if child.tag == "lijst":
                render(child, depth, out)
    elif tag == "al":
        out.append(f"\n{text(el)}")
    elif tag == "lijst":
        out.append("")
        for child in el:
            render(child, depth, out)
    else:
        for child in el:
            render(child, depth, out)


def law_to_markdown(xml_path: Path, chapters: list[str]) -> str:
    root = etree.parse(str(xml_path)).getroot()
    regeling = next(root.iter("wettekst", "regeling-tekst"), root)
    out: list[str] = []
    for child in regeling:
        if chapters and child.tag == "hoofdstuk" and heading_nr(child) not in chapters:
            continue
        render(child, 2, out)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip() + "\n"


def heading_nr(el: etree._Element) -> str:
    return (el.findtext("kop/nr") or "").strip().rstrip(".")
