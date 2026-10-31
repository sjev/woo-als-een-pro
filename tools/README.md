# Tools

Software for the knowledge base. Code and docs in this folder are in English.
Every script runs through `uv` (PEP 723 inline dependencies) unless noted.

| Tool | Purpose |
|---|---|
| [`build.py`](build.py) | Render a markdown letter from [`../templates/`](../templates/README.md) to PDF |
| [`links.py`](links.py) | Module for `build.py`: clickable references and bookmarks in the complete PDF |
| [`style.tex`](style.tex) | LaTeX house style for letters |
| [`wetten.py`](wetten.py) | Fetch current law text into [`../wetten/`](../wetten/README.md), one file per article |
| [`collect/`](collect/README.md) | Fetch secondary sources and convert them to markdown in [`../bronnen/`](../bronnen/README.md) |

## build.py

```bash
tools/build.py brief.md                                # brief.pdf
tools/build.py brief.md --sign handtekening.png        # + brief-digitaal.pdf
tools/build.py brief.md --bijlagen bijlagen/ --date 2026-11-01
```

| Option | Effect |
|---|---|
| `--bijlagen DIR` | Writes `<brief>-compleet.pdf`: letter + stamped attachments + clickable references and bookmarks |
| `--sign PNG` | Puts the signature in the space after "Hoogachtend," |
| `--date YYYY-MM-DD` | Fills `{{datum}}`; default today |
| `--out DIR` | Output folder; default `<letter folder>/out` |

Attachments (*bijlagen*):

- Name: `bijlage-NN[a-z]-<description>.md|pdf`. Parts `01a`, `01b` become one attachment.
- Each page gets the stamp "Bijlage N, blad x/y".
- `links.py` makes "bijlage N", "bijlage N, blad M" and "punt N" clickable. The letter must end with a heading `## Bijlagen` and a numbered list.

Known issue: an unfilled `[...]` directly after `\\` in the letter head breaks the LaTeX build.

Requires: `uv`, `pandoc`, `pdflatex` (TeX Live with KOMA-Script), `poppler-utils` (`pdfunite`, `pdfinfo`, `pdftotext`). `uv` installs `pikepdf`.

## wetten.py

```bash
tools/wetten.py update               # all laws
tools/wetten.py update woo           # one law
tools/wetten.py add BWBR0005537 awb  # new law
```

Source: the BWB XML repository (version in force today), resolved through the SRU service of zoekservice.overheid.nl. `update` replaces the folder of the law.
