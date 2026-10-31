"""Make a complete PDF clickable: references to bijlagen, blad, punt and bundelpagina, the bijlagenlijst and bookmarks."""

from __future__ import annotations

import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from bisect import bisect_right
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import pikepdf
from pikepdf import Array, Dictionary, Name

XHTML = "{http://www.w3.org/1999/xhtml}"
BIJLAGE = re.compile(r"[Bb]ijlagen? (\d+)(?:, blad (\d+))?")
BIJLAGE_EN = re.compile(r"[Bb]ijlagen \d+ en (\d+)")
PUNT = re.compile(r"punt (\d+)(?: onder \d+)?")
BUNDEL = re.compile(r"pagina (\d+) van de bundel (\d+)")
LABEL = re.compile(r"\d+\.")
LINE_GAP = 30.0  # points; a wrapped entry never leaves a bigger gap
OTHER_LETTER = "reactie op het verweer"  # "punt N" after this phrase points into another letter


@dataclass(frozen=True)
class Word:
    text: str
    page: int
    line: int
    x0: float
    y0: float
    x1: float
    y1: float


@dataclass(frozen=True)
class Link:
    words: list[Word]
    page: int  # absolute target page, zero-based
    y: float | None = None  # from the top of the target page; None shows the whole page


def read_words(pdf: Path, pages: int) -> list[Word]:
    xml = subprocess.run(["pdftotext", "-bbox-layout", "-l", str(pages), str(pdf), "-"],
                         capture_output=True, text=True, check=True).stdout
    words: list[Word] = []
    line_id = 0
    for number, page in enumerate(ET.fromstring(xml).iter(f"{XHTML}page")):
        for line in page.iter(f"{XHTML}line"):
            line_id += 1
            words += [Word(w.text or "", number, line_id, *(float(w.get(k)) for k in ("xMin", "yMin", "xMax", "yMax")))
                      for w in line.iter(f"{XHTML}word")]
    return words


def bundel_map(attachments: Path) -> dict[tuple[int, int], tuple[int, int]]:
    """(besluit, bundelpagina) -> (bijlage, blad), read from the toelichting of each uittreksel."""
    found: dict[tuple[int, int], tuple[int, int]] = {}
    for path in attachments.glob("bijlage-*a-toelichting.md"):
        text = path.read_text()
        bijlage = int(re.match(r"bijlage-(\d+)", path.name).group(1))
        besluit = int(re.search(r"besluit (\d+)", text).group(1))
        for blad, pagina in re.findall(r"^\| (\d+(?:-\d+)?) \| (\d+(?:-\d+)?) \|", text, re.M):
            b0, b1 = (list(map(int, blad.split("-"))) * 2)[:2]
            p0 = int(pagina.split("-")[0])
            found |= {(besluit, p0 + k): (bijlage, b0 + k) for k in range(b1 - b0 + 1)}
    return found


def spans(words: list[Word]) -> tuple[str, list[int]]:
    """Joined text and the start offset of each word in it."""
    starts, size = [], 0
    for w in words:
        starts.append(size)
        size += len(w.text) + 1
    return " ".join(w.text for w in words), starts


def words_in(words: list[Word], starts: list[int], begin: int, end: int) -> list[Word]:
    return words[bisect_right(starts, begin) - 1:bisect_right(starts, end - 1)]


def references(words: list[Word], first_page: dict[int, int], size: dict[int, int],
               punten: dict[int, Word], bundels: dict[tuple[int, int], tuple[int, int]]) -> list[Link]:
    text, starts = spans(words)

    def blad(nr: int, number: int = 1) -> int:
        return first_page[nr] + min(number, size[nr]) - 1

    links = []
    for m in BIJLAGE.finditer(text):
        if (nr := int(m[1])) in first_page:
            links.append(Link(words_in(words, starts, m.start(), m.end()), blad(nr, int(m[2] or 1))))
    for m in BIJLAGE_EN.finditer(text):
        if (nr := int(m[1])) in first_page:
            links.append(Link(words_in(words, starts, m.start(1), m.end(1)), blad(nr)))
    for m in PUNT.finditer(text):
        if int(m[1]) in punten and OTHER_LETTER not in text[max(0, m.start() - 40):m.start()]:
            target = punten[int(m[1])]
            links.append(Link(words_in(words, starts, m.start(), m.end()), target.page, target.y0))
    for m in BUNDEL.finditer(text):
        if (hit := bundels.get((int(m[2]), int(m[1])))) and hit[0] in first_page:
            links.append(Link(words_in(words, starts, m.start(), m.end()), blad(*hit)))
    return links


def split_body(words: list[Word]) -> tuple[list[Word], list[Word]]:
    """The letter body and the bijlagenlijst below the last heading 'Bijlagen', by position on the page."""
    per_line = Counter(w.line for w in words)
    head = [w for w in words if w.text == "Bijlagen" and per_line[w.line] == 1][-1]
    above = [w for w in words if (w.page, w.y0) < (head.page, head.y0)]
    below = [w for w in words if (w.page, w.y0) > (head.page, head.y0)]
    return above, below


def labels(words: list[Word], margin: float, headings: set[tuple[int, str]]) -> dict[int, Word]:
    """The first number at the margin for each n; a section heading '1. Title' is not a label."""
    found: dict[int, Word] = {}
    for w, after in zip(words, words[1:] + [None]):
        n = int(w.text[:-1]) if LABEL.fullmatch(w.text) else 0
        if n and w.x0 <= margin + 1 and n not in found and (after is None or (n, after.text) not in headings):
            found[n] = w
    return found


def entries(listing: list[Word], found: dict[int, Word]) -> dict[int, list[Word]]:
    """The words of each listed bijlage: from its label down to the next label."""
    order = sorted(found.items(), key=lambda item: (item[1].page, item[1].y0))
    result: dict[int, list[Word]] = {}
    for (n, label), nxt in zip(order, order[1:] + [(0, None)]):
        end = (nxt[1].page, nxt[1].y0) if nxt[1] else (10**6, 0.0)
        inside = sorted((w for w in listing if (label.page, label.y0 - 2) <= (w.page, w.y0) < end),
                        key=lambda w: (w.page, round(w.y0), w.x0))
        previous = label.y0
        for i, w in enumerate(inside):
            if w.page != label.page or w.y0 - previous > LINE_GAP:  # the page number in the foot is no entry
                inside = inside[:i]
                break
            previous = w.y0
        result[n] = inside
    return result


def annotate(pdf: pikepdf.Pdf, link: Link) -> None:
    target = pdf.pages[link.page]
    top = float(target.mediabox[3])
    dest = Array([target.obj, Name.Fit]) if link.y is None else Array([target.obj, Name.XYZ, None, top - link.y + 6, None])
    for page_no in {w.page for w in link.words}:
        page = pdf.pages[page_no]
        height = float(page.mediabox[3])
        for line in {w.line for w in link.words if w.page == page_no}:
            ws = [w for w in link.words if w.line == line]
            rect = [min(w.x0 for w in ws) - 1, height - max(w.y1 for w in ws) - 1,
                    max(w.x1 for w in ws) + 1, height - min(w.y0 for w in ws) + 1]
            annot = pdf.make_indirect(Dictionary(Type=Name.Annot, Subtype=Name.Link, Rect=rect, Border=Array([0, 0, 0.6]),
                                                 C=Array([0.1, 0.3, 0.8]), F=0, Dest=dest))
            if "/Annots" not in page.obj:
                page.obj.Annots = Array()
            page.obj.Annots.append(annot)


def add_links(complete: Path, letter: Path, attachments: Path, parts: list[Path]) -> None:
    """parts: the letter PDF first, then one stamped PDF per bijlage, in the order they were joined."""
    sizes = [len(pikepdf.open(p).pages) for p in parts]
    letter_pages = sizes[0]
    numbers = [int(re.match(r"bijlage-(\d+)", p.name).group(1)) for p in parts[1:]]
    first_page = {nr: sum(sizes[:i + 1]) for i, nr in enumerate(numbers)}
    size = dict(zip(numbers, sizes[1:]))

    words = read_words(complete, letter_pages)
    margin = min(w.x0 for w in words)
    headings = {(int(n), first) for n, first in re.findall(r"^#+ (\d+)\. (\S+)", letter.read_text(), re.M)}
    body, listing = split_body(words)
    punten = labels(body, margin, headings)
    links = references(body, first_page, size, punten, bundel_map(attachments))
    listed = entries(listing, labels(listing, margin, set()))
    links += [Link(ws, first_page[n]) for n, ws in listed.items() if n in first_page]

    with pikepdf.open(complete, allow_overwriting_input=True) as pdf:
        for link in links:
            annotate(pdf, link)
        with pdf.open_outline() as outline:
            outline.root.append(pikepdf.OutlineItem("Brief", 0))
            for n, ws in listed.items():
                if n in first_page:
                    title = " ".join(w.text for w in ws).replace(". ", ": ", 1)
                    outline.root.append(pikepdf.OutlineItem(f"Bijlage {title}", first_page[n]))
        pdf.Root.PageMode = Name.UseOutlines
        pdf.save()
    print(f"{complete.name}: {len(links)} links, {len(listed)} bijlagen in the bookmarks")
