# Tools

Software for the knowledge base. Code and docs in this folder are in English.
Every script runs through `uv` (PEP 723 inline dependencies) unless noted.

| Tool | Purpose |
|---|---|
| [`build.py`](build.py) | Render a markdown letter from [`../templates/`](../templates/README.md) to PDF |
| [`links.py`](links.py) | Module for `build.py`: clickable references and bookmarks in the complete PDF |
| [`style.tex`](style.tex) | LaTeX house style for letters |
| [`wetten.py`](wetten.py) | Fetch current law text into [`../wetten/`](../wetten/README.md), one file per article |
| [`uitspraak.py`](uitspraak.py) | Fetch court rulings into [`../uitspraken/tekst/`](../uitspraken/README.md) |
| [`termijn.py`](termijn.py) | Compute the last day of a term under the Algemene termijnenwet |
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
tools/wetten.py add CELEX:32016R0679 avg  # EU act
```

Also fetches appendices (`bijlage*.md`). Source: the BWB XML repository (version in force today), resolved through the SRU service of zoekservice.overheid.nl. `update` replaces the folder of the law.
Treaties (BWBV): the Dutch translation. EU acts (`CELEX:` ids): Dutch XHTML from the Publications Office Cellar via [`eurlex.py`](eurlex.py); EUR-Lex itself blocks scripts. Set title and date of application in `EU_ACTS` in `wetten.py`.

## termijn.py

```bash
tools/termijn.py 2026-11-02 4w        # Woo decision term (art. 4.4 lid 1 Woo)
tools/termijn.py 2026-11-02 4w 2w     # with deferral (art. 4.4 lid 2 Woo)
tools/termijn.py 2026-11-02 6w 12d    # plus 12 days of suspension
```

- The date is the event: receipt, notice, decision. The term starts the next day.
- Periods add up first. The Atw then applies once, to the end of the total term. This is an assumption for chained terms; check it per case.
- Atw rules: weekend and holiday extension (art. 1), at least two workdays (art. 2), holidays incl. Good Friday and 5 May (art. 3), not for terms over twelve weeks or 90 days (art. 4).
- Not supported: terms counted backward (art. 1 lid 2), months, years before 2014.

Tests: `uv run --with pytest pytest tools/`.

## uitspraak.py

```bash
tools/uitspraak.py ECLI:NL:RVS:2022:3027 [ECLI...]
```

Source: the open data API of rechtspraak.nl (`data.rechtspraak.nl/uitspraken/content`). Writes metadata, *inhoudsindicatie* and full text to `uitspraken/tekst/<ECLI>.md` and prints it. The API has no full-text search; find ECLIs with a web search or on uitspraken.rechtspraak.nl.
