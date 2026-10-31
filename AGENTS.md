# AGENTS.md

Werkinstructie voor agents (en mensen) die deze kennisbank gebruiken of aanvullen.

## Doel en grens

- Deze repo geeft praktische kennis over Woo-verzoeken: wat mag, wat werkt, welke brief, welke termijn.
- Deze repo bevat **geen zaakgegevens**. Zaakbeheer (dossier, log, termijnen per zaak) gebeurt in een apart systeem, zoals ODAS. Verwijs niet naar paden of formaten van zo'n systeem.
- Zet nooit persoonsgegevens in de repo: geen namen, adressen, zaaknummers of kenmerken van echte zaken. Lessen uit zaken komen geanonimiseerd in [`docs/praktijk.md`](docs/praktijk.md).

## Taal

| Onderwerp | Taal | Waar |
|---|---|---|
| Juridisch werk: kennis, uitleg, brieven, wetten, uitspraken, bronnen | Nederlands | `docs/`, `templates/`, `wetten/`, `uitspraken/`, `bronnen/`, dit bestand |
| Software: code, docstrings, commentaar, tool-README's, foutmeldingen | Engels | `tools/` |

Schrijfstijl in beide talen: ASD-STE100. Korte zinnen, één gedachte per zin, actieve vorm.

## Zoekvolgorde

1. [`docs/stappenplan.md`](docs/stappenplan.md): welke situatie, welke actie, welk sjabloon.
2. `docs/<onderwerp>.md`: de regel en de praktijk. TOC in [`README.md`](README.md).
3. `wetten/<wet>/artikel_<nr>.md`: de wetstekst zelf. Zoek met `grep -rl "<term>" wetten/<wet>/`.
4. `uitspraken/`: jurisprudentie per ECLI.
5. `bronnen/`: handreikingen en achtergrond. Secundair; nooit de enige grondslag.

## Bronregels

- Elk juridisch feit heeft een bron: een artikel uit `wetten/` of een uitspraak uit `uitspraken/`.
- Citeer wetstekst alleen uit `wetten/`. Noem `valid_from` als de datum ertoe doet.
- Link naar een artikel met een relatief pad, bijv. [art. 4.4 Woo](wetten/woo/artikel_4-4.md). Het bestand bevat de bron-URL.
- Link naar een uitspraak met het ECLI en het bestand in `uitspraken/`.
- Niet gecontroleerd? Zet `[niet geverifieerd]` direct achter de bewering. Zoek open punten met `grep -rn "niet geverifieerd"`.
- Een juridisch feit staat op één plek in `docs/`. Sjablonen en andere documenten linken ernaar. Zij herhalen het niet.

## Conventies voor documenten

- Eén onderwerp per document. Doel: < 200 regels.
- Documenten in `docs/`, `templates/` en `uitspraken/` beginnen met YAML front matter: minimaal `title` en `summary`.
- Bestandsnamen: kleine letters, koppeltekens, geen nummers vooraf. De volgorde staat in de TOC.
- Wijzig `wetten/` en `bronnen/` niet met de hand. Gebruik de tools in [`tools/`](tools/README.md).

## Tools

Zie [`tools/README.md`](tools/README.md). Kort:

| Taak | Tool |
|---|---|
| Brief (markdown) naar PDF | `tools/build.py` |
| Wetstekst ophalen of bijwerken | `tools/wetten.py` |
| Termijn berekenen (Algemene termijnenwet) | `tools/termijn.py` |
| Bronnen ophalen en omzetten | `tools/collect/` |
