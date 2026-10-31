# Tools

Bouw een brief uit [`../templates/`](../templates/) naar PDF.

## Gebruik

```bash
tools/build.py brief.md                                # brief.pdf
tools/build.py brief.md --sign handtekening.png        # + brief-digitaal.pdf
tools/build.py brief.md --bijlagen bijlagen/ --date 2026-11-01
```

| Optie | Effect |
|---|---|
| `--bijlagen DIR` | Maakt `<brief>-compleet.pdf`: brief + gestempelde bijlagen + klikbare verwijzingen en bladwijzers |
| `--sign PNG` | Zet de handtekening in de ruimte na "Hoogachtend," |
| `--date JJJJ-MM-DD` | Vult `{{datum}}`; standaard vandaag |
| `--out DIR` | Uitvoermap; standaard `<map van brief>/out` |

## Bijlagen

- Naam: `bijlage-NN[a-z]-<omschrijving>.md|pdf`. Delen `01a`, `01b` worden één bijlage.
- Elke pagina krijgt een stempel "Bijlage N, blad x/y".
- `links.py` maakt "bijlage N", "bijlage N, blad M" en "punt N" in de brief klikbaar. De brief moet eindigen met een kop `## Bijlagen` en een genummerde lijst.

## Vereisten

`uv`, `pandoc`, `pdflatex` (TeX Live met KOMA-Script), `poppler-utils` (`pdfunite`, `pdfinfo`, `pdftotext`). `uv` installeert `pikepdf`.
