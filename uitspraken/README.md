# Uitspraken

Jurisprudentie over de Woo en de Awb. Eén bestand per uitspraak.

| Pad | Inhoud | Hoe |
|---|---|---|
| `<ECLI>.md` | Kern, letterlijke rechtsoverwegingen, gebruik | Met de hand, na lezing van de volledige tekst |
| [`tekst/<ECLI>.md`](tekst/) | Volledige tekst en metadata | `tools/uitspraak.py <ECLI>`. Niet met de hand wijzigen |

Zoek in de volledige teksten met `grep -rl "<term>" uitspraken/tekst/`.

## Bestand

Naam: het ECLI met koppeltekens, bijv. `ECLI-NL-RVS-JJJJ-NNNN.md`.

```markdown
---
title: <korte kern, één zin>
summary: <wat de uitspraak beslist, één of twee zinnen>
ecli: ECLI:NL:RVS:JJJJ:NNNN
datum: JJJJ-MM-DD
instantie: ABRvS
onderwerpen: [ingebrekestelling, zoekslag]
url: https://uitspraken.rechtspraak.nl/details?id=ECLI:NL:RVS:JJJJ:NNNN
---

## Kern

<de regel uit de uitspraak, in eigen woorden>

## Rechtsoverwegingen

> r.o. 5.2: "<letterlijk citaat>"

## Gebruik

<waarvoor en in welk stuk deze uitspraak bruikbaar is; link naar docs/>
```

Citeer rechtsoverwegingen letterlijk, met nummer. Neem alleen een uitspraak op die u in de bron hebt gelezen.

## Index

Handmatig bijgewerkt. Nieuwe uitspraak: voeg een regel toe.

| ECLI | Datum | Instantie | Kern |
|---|---|---|---|
| [ECLI:NL:RBNNE:2026:2349](ECLI-NL-RBNNE-2026-2349.md) | 2026-05-13 | Rechtbank Noord-Nederland | Precisering is geen wijziging; geen fatale termijn voor het verzoek om precisering |
| [ECLI:NL:RBZWB:2026:731](ECLI-NL-RBZWB-2026-731.md) | 2026-02-06 | Rechtbank Zeeland-West-Brabant | Beroep niet tijdig is niet-ontvankelijk na een te vroege ingebrekestelling |
| [ECLI:NL:RVS:2024:1066](ECLI-NL-RVS-2024-1066.md) | 2024-03-13 | ABRvS | De Woo verplicht niet tot het maken van documenten, ook niet als die er wettelijk hadden moeten zijn |
| [ECLI:NL:RVS:2024:480](ECLI-NL-RVS-2024-480.md) | 2024-02-07 | ABRvS | Zoekslag inzichtelijk: systemen, zoektermen, personen, schifting |
| [ECLI:NL:RVS:2024:470](ECLI-NL-RVS-2024-470.md) | 2024-02-07 | ABRvS | Staatsaandeelhouderschap alleen maakt een bedrijf niet "werkzaam onder verantwoordelijkheid van" de minister |
| [ECLI:NL:RVS:2023:4754](ECLI-NL-RVS-2023-4754.md) | 2023-12-20 | ABRvS | Openbaarmaking van beleidsopvattingen voor goede bestuursvoering is een bevoegdheid; de verzoeker moet het belang aannemelijk maken |
| [ECLI:NL:RVS:2023:4752](ECLI-NL-RVS-2023-4752.md) | 2023-12-20 | ABRvS | Het begrip persoonsgegevens is ruim; ook data die via koppeling herleidbaar zijn |
| [ECLI:NL:RVS:2022:3027](ECLI-NL-RVS-2022-3027.md) | 2022-10-19 | ABRvS | Het bestuursorgaan moet de zoekslag inzichtelijk maken; daarna moet de verzoeker aannemelijk maken dat er meer is |
| [ECLI:NL:RVS:2021:153](ECLI-NL-RVS-2021-153.md) | 2021-01-27 | ABRvS | Locatie van een emissiebron is een emissiegegeven; persoonlijke levenssfeer staat niet aan openbaarmaking in de weg |
| [ECLI:NL:RVS:2019:3975](ECLI-NL-RVS-2019-3975.md) | 2019-11-27 | ABRvS | Concepten en interne memo's zijn intern beraad; feiten die al in de definitieve versie staan, zijn al openbaar |
| [ECLI:NL:RVS:2019:899](ECLI-NL-RVS-2019-899.md) | 2019-03-20 | ABRvS | Sms- en WhatsApp-berichten over het werk zijn documenten, ook op een privételefoon |
| [ECLI:NL:RVS:2018:314](ECLI-NL-RVS-2018-314.md) | 2018-01-31 | ABRvS | Beoordeling per zelfstandig onderdeel (alinea), niet per zin |
| [ECLI:NL:RVS:2016:2273](ECLI-NL-RVS-2016-2273.md) | 2016-08-17 | ABRvS | Een Wob-verzoek is vormvrij; het bestuursorgaan mag geen formulier verplicht stellen |
| [ECLI:NL:RVS:2016:409](ECLI-NL-RVS-2016-409.md) | 2016-02-17 | ABRvS | Een ingebrekestelling vóór het einde van de (verdaagde) beslistermijn is prematuur |

## Gezocht

Uitspraken die de kennisbank nodig heeft. Haal een regel weg als het bestand er is.

- Art. 4:8 Awb (zienswijze derden) bij Woo-verzoeken.
- Verzoek om precisering (art. 4.1 lid 5 Woo) schort de beslistermijn op via art. 4:15 lid 1 onder a Awb (ABRvS). Nodig voor [procedure](../docs/procedure.md).
- Mag een bestuursorgaan onder de Woo een webformulier verplicht stellen (art. 4.1 lid 2 Woo)? Nodig voor [procedure](../docs/procedure.md).
- Art. 5.2 lid 2 en 3 Woo (formele bestuurlijke besluitvorming): eerste ABRvS-uitspraken onder de Woo. Nodig voor [beleidsopvattingen](../docs/beleidsopvattingen.md).
