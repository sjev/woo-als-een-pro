import json
import re
from collections import Counter
from pathlib import Path

import mammoth
import pymupdf4llm
import yaml
from bs4 import BeautifulSoup
from markdownify import markdownify

from woo_collect.laws import law_to_markdown
from woo_collect.sources import Source

NOISE_TAGS = ["script", "style", "nav", "header", "footer", "aside", "form", "noscript", "svg", "button"]
MAIN_SELECTORS = ["main", "article", "[role=main]", "#content", "body"]


def tidy(md: str) -> str:
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def drop_repeated_lines(md: str, pages: int) -> str:
    """Remove page headers/footers: short lines that recur on many pages."""
    if pages < 3:
        return md
    lines = md.splitlines()
    key = lambda s: re.sub(r"\d+", "#", s.strip())
    counts = Counter(key(s) for s in lines if s.strip() and len(s) < 120)
    noise = {k for k, n in counts.items() if n >= max(3, pages // 2) and not k.startswith(("|", "-", "#"))}
    return "\n".join(s for s in lines if key(s) not in noise)


PICTURE = re.compile(r"<!-- Start of picture text -->(.*?)<!-- End of picture text -->", re.S)


def picture_text(m: re.Match[str]) -> str:
    """Keep OCR text from diagrams; drop logos and chart axes that OCR turns into noise."""
    tokens = m.group(1).replace("<br>", " ").split()
    words = [t for t in tokens if re.fullmatch(r"[A-Za-zÀ-ÿ'’-]{3,}[.,:;?]?", t)]
    if len(words) < 8 or len(words) < 0.6 * len(tokens):
        return ""
    return "\n" + m.group(1).replace("<br>", "\n") + "\n"


def pdf_to_md(path: Path) -> str:
    chunks = pymupdf4llm.to_markdown(str(path), page_chunks=True, show_progress=False)
    md = "\n\n".join(c["text"] for c in chunks)
    md = PICTURE.sub(picture_text, md)
    md = re.sub(r"</?(mark|sup|sub|u)>", "", md)
    md = re.sub(r"^(#+) \*\*(.+?)\*\*\s*$", r"\1 \2", md, flags=re.M)
    return drop_repeated_lines(md, len(chunks))


def html_to_md(path: Path) -> str:
    soup = BeautifulSoup(path.read_bytes(), "lxml")
    for tag in soup(NOISE_TAGS):
        tag.decompose()
    main = next(el for sel in MAIN_SELECTORS if (el := soup.select_one(sel)) is not None)
    return markdownify(str(main), heading_style="ATX", strip=["img"])


def docx_to_md(path: Path) -> str:
    with path.open("rb") as f:
        html = mammoth.convert_to_html(f).value
    return markdownify(html, heading_style="ATX")


def extract(source: Source) -> str:
    if not source.raw_path.exists():
        return "missing raw"
    match source.format:
        case "pdf":
            body = pdf_to_md(source.raw_path)
        case "html":
            body = html_to_md(source.raw_path)
        case "docx":
            body = docx_to_md(source.raw_path)
        case "law":
            body = law_to_markdown(source.raw_path, source.chapters)
        case other:
            raise ValueError(f"unknown format {other}")

    meta = json.loads(source.meta_path.read_text()) if source.meta_path.exists() else {"url": source.url, "fetched_at": "manual"}
    front = {"id": source.id, "title": source.title, "section": source.section, "format": source.format, **meta}
    source.clean_path.parent.mkdir(parents=True, exist_ok=True)
    body = tidy(body)
    source.clean_path.write_text(f"---\n{yaml.safe_dump(front, allow_unicode=True, sort_keys=False)}---\n\n{body}")
    return f"ok ({len(body.split())} words)"
