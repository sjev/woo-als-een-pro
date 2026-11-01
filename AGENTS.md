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
4. `uitspraken/`: jurisprudentie per ECLI. Index in [`uitspraken/README.md`](uitspraken/README.md). Volledige teksten: `grep -rl "<term>" uitspraken/tekst/`.
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
- Bestandsnamen: kleine letters, koppeltekens, geen nummers vooraf. De volgorde staat in de TOC. `docs/` en `templates/` hebben ook `weight` in de front matter, gelijk aan de TOC: de site sorteert daarop.
- Wijzig `wetten/`, `bronnen/` en `uitspraken/tekst/` niet met de hand. Gebruik de tools in [`tools/`](tools/README.md).
- Draai `tools/check_links.py` na elke wijziging in `docs/`, `templates/` of `uitspraken/`.

## Uitspraak toevoegen

1. Haal de volledige tekst op: `tools/uitspraak.py <ECLI>`. Die komt in `uitspraken/tekst/<ECLI>.md`. Wijzig die niet met de hand.
2. Lees de volledige tekst. Neem alleen een uitspraak op die u in de bron hebt gelezen.
3. Schrijf `uitspraken/<ECLI>.md`. Naam: het ECLI met koppeltekens, bijv. `ECLI-NL-RVS-JJJJ-NNNN.md`. Formaat:

    ```markdown
    ---
    title: <korte kern, één zin>
    summary: <wat de uitspraak beslist, één of twee zinnen>
    ecli: ECLI:NL:RVS:JJJJ:NNNN
    datum: JJJJ-MM-DD
    instantie: ABRvS
    onderwerpen: [ingebrekestelling, zoekslag]
    source: https://uitspraken.rechtspraak.nl/details?id=ECLI:NL:RVS:JJJJ:NNNN
    ---

    ## Kern

    <de regel uit de uitspraak, in eigen woorden>

    ## Rechtsoverwegingen

    > r.o. 5.2: "<letterlijk citaat>"

    ## Gebruik

    <waarvoor en in welk stuk deze uitspraak bruikbaar is; link naar docs/>
    ```

4. Citeer rechtsoverwegingen letterlijk, met nummer.
5. Voeg een regel toe aan de index in [`uitspraken/README.md`](uitspraken/README.md). Staat de uitspraak onder "Gezocht"? Haal die regel weg.

## Brieven en termijnen

- Reken elke termijn uit met `tools/termijn.py`. Gebruik `day after` uit de uitvoer als datum voor de ingebrekestelling.
- Een brief is de tekst uit een sjabloon. Vul `[...]` in. Ontbreekt een gegeven? Vraag erom.
- Laat `{{datum}}` staan. `tools/build.py` vult die in en maakt van de kop (`afzender`, `aan`, `kenmerken`) het briefhoofd.

## Site

De site (woo.dasopen.nl) is voor juristen, niet voor ontwikkelaars. Zet in `docs/`, `templates/` en `uitspraken/` geen tools, commando's, bestandsformaten of werkinstructies voor agents. Die horen in dit bestand of in [`tools/README.md`](tools/README.md).

## Tools

Zie [`tools/README.md`](tools/README.md). Kort:

| Taak | Tool |
|---|---|
| Brief (markdown) naar PDF | `tools/build.py` |
| Wetstekst ophalen of bijwerken | `tools/wetten.py` |
| Termijn berekenen (Algemene termijnenwet) | `tools/termijn.py` |
| Uitspraak ophalen (volledige tekst) | `tools/uitspraak.py` |
| Links en ankers controleren | `tools/check_links.py` |
| Bronnen ophalen en omzetten | `tools/collect/` |
| Website bouwen en publiceren (woo.dasopen.nl) | `site/` (`inv build`, `inv deploy`) |
