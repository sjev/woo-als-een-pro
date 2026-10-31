#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["pikepdf"]
# ///
"""Render a markdown letter to PDF, plus a complete PDF with stamped, linked bijlagen."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from datetime import date
from itertools import groupby
from pathlib import Path

from links import add_links

STYLE = Path(__file__).resolve().parent / "style.tex"
# The signature replaces the blank space between the closing and the name.
SIGN_GAP = re.compile(r"(?<=Hoogachtend,\n\n)\\vspace\{(\d+)mm\}")
MAANDEN = ("januari", "februari", "maart", "april", "mei", "juni",
           "juli", "augustus", "september", "oktober", "november", "december")

PANDOC_OPTS = [
    "--pdf-engine=pdflatex",
    "--from=markdown+hard_line_breaks",
    f"--include-in-header={STYLE}",
    "-V", "documentclass=scrartcl",
    "-V", "papersize=a4",
    "-V", "geometry:top=28mm,bottom=28mm,left=28mm,right=32mm",
    "-V", "lang=nl",
    "-V", "colorlinks=true",
    "-V", "linkcolor=black",
    "-V", "urlcolor=black",
]

# Shrink and lower each page so the stamp sits in a free strip, never over evidence.
STAMP_TEX = r"""\documentclass[a4paper]{article}
\usepackage{pdfpages,tikz}
\pagestyle{empty}
\begin{document}
\includepdf[pages=-,scale=0.93,offset=0 -6mm,pagecommand={\begin{tikzpicture}[remember picture,overlay]
\node[anchor=north east,draw,font=\sffamily\small,inner sep=2pt]
  at ([xshift=-10mm,yshift=-4mm]current page.north east) {LABEL, blad \thepage/TOTAL};
\end{tikzpicture}}]{SOURCE}
\end{document}
"""


def run(cmd: list[str], stdin: str | None = None) -> None:
    result = subprocess.run(cmd, input=stdin, capture_output=True, text=True)
    if result.returncode != 0:
        sys.exit(f"failed: {' '.join(cmd)}\n{result.stderr.strip()}")


def dutch_date(iso: str | None) -> str:
    day = date.fromisoformat(iso) if iso else date.today()
    return f"{day.day} {MAANDEN[day.month - 1]} {day.year}"


def render_markdown(source: Path, target: Path, datum: str, signature: Path | None = None,
                    fontsize: str = "10pt") -> None:
    text = source.read_text().replace("{{datum}}", datum)
    if signature:
        text = SIGN_GAP.sub(f"![]({signature}){{height=\\1mm}}", text)
    run(["pandoc", "-o", str(target), *PANDOC_OPTS, "-V", f"fontsize={fontsize}",
         "--resource-path", str(source.parent)], text)


def page_count(pdf: Path) -> str:
    result = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True)
    match = re.search(r"^Pages:\s+(\d+)", result.stdout, re.M)
    return match.group(1) if match else "?"


def report(pdf: Path) -> None:
    print(f"{pdf.name:48s} {page_count(pdf):>3s} p")


def number(path: Path) -> int:
    return int(re.match(r"bijlage-(\d+)", path.name).group(1))


def build_bijlagen(attachments: Path, out: Path, datum: str) -> list[Path]:
    """One PDF per bijlage number; parts named bijlage-01a, -01b are joined in order."""
    parts_dir = out / "parts"
    parts_dir.mkdir(parents=True, exist_ok=True)
    sources = sorted(p for p in attachments.glob("bijlage-*") if p.suffix in {".md", ".pdf"})
    built: list[Path] = []
    for nr, group in groupby(sources, key=number):
        parts = []
        for source in group:
            target = parts_dir / f"{source.stem}.pdf"
            if source.suffix == ".md":
                render_markdown(source, target, datum, fontsize="9pt")
            else:
                shutil.copyfile(source, target)
            parts.append(target)
        target = out / f"bijlage-{nr:02d}.pdf"
        if len(parts) == 1:
            shutil.copyfile(parts[0], target)
        else:
            run(["pdfunite", *map(str, parts), str(target)])
        report(target)
        built.append(target)
    return built


def stamp(pdf: Path) -> Path:
    """Mark each page with its bijlage number, since not every bijlage names itself."""
    stamped = pdf.parent / "stamped"
    stamped.mkdir(parents=True, exist_ok=True)
    tex = stamped / pdf.with_suffix(".tex").name
    tex.write_text(STAMP_TEX.replace("LABEL", f"Bijlage {number(pdf)}")
                   .replace("TOTAL", page_count(pdf)).replace("SOURCE", str(pdf)))
    for _ in range(2):  # tikz overlay positions resolve on the second pass
        run(["pdflatex", "-interaction=nonstopmode", f"-output-directory={stamped}", str(tex)])
    return tex.with_suffix(".pdf")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("letter", type=Path, help="markdown letter")
    parser.add_argument("--bijlagen", type=Path, help="folder with bijlage-NN[a-z]-*.md|pdf")
    parser.add_argument("--date", help="letter date JJJJ-MM-DD; default today")
    parser.add_argument("--sign", type=Path, help="signature image for the -digitaal.pdf")
    parser.add_argument("--out", type=Path, help="output folder; default <letter folder>/out")
    args = parser.parse_args()

    letter: Path = args.letter.resolve()
    out: Path = args.out or letter.parent / "out"
    out.mkdir(parents=True, exist_ok=True)
    datum = dutch_date(args.date)

    final = out / f"{letter.stem}.pdf"
    render_markdown(letter, final, datum)
    report(final)
    if args.sign:
        final = out / f"{letter.stem}-digitaal.pdf"
        render_markdown(letter, final, datum, signature=args.sign.resolve())
        report(final)
    if args.bijlagen:
        complete = out / f"{letter.stem}-compleet.pdf"
        parts = [final, *map(stamp, build_bijlagen(args.bijlagen, out, datum))]
        run(["pdfunite", *map(str, parts), str(complete)])
        add_links(complete, letter, args.bijlagen, parts)
        report(complete)


if __name__ == "__main__":
    main()
