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

## Gezocht

Uitspraken die de kennisbank nodig heeft. Haal een regel weg als het bestand er is.

- Zakelijke sms- en WhatsApp-berichten vallen onder de Woo (ABRvS).
- Zoekslag: aannemelijkheid dat er niet meer documenten zijn; bewijslast.
- Art. 4:8 Awb (zienswijze derden) bij Woo-verzoeken.
- Verzoek om precisering (art. 4.1 lid 5 Woo) schort de beslistermijn op via art. 4:15 lid 1 onder a Awb. Nodig voor [procedure](../docs/procedure.md).
- Misbruik van het recht op informatie wordt niet snel aangenomen (art. 4.6 Woo). Nodig voor [procedure](../docs/procedure.md).
