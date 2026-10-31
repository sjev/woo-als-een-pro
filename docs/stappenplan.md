---
title: Stappenplan
summary: Van situatie naar termijn, actie, sjabloon en achtergronddocument. Begin hier.
---

# Stappenplan

Begin hier. Zoek de situatie. Reken de termijn uit. Volg de actie. Lees het document voor de regels.

## Situaties

| Situatie | Termijn | Actie | Sjabloon | Lees |
|---|---|---|---|---|
| U wilt informatie | — | Zoek eerst of het al openbaar is. Vraag documenten, geen antwoorden. Nummer de onderdelen; noem bronnen, zoektermen, periode, concepten, vorm | [verzoek](../templates/verzoek.md) | [reikwijdte](reikwijdte.md), [zoekslag](zoekslag.md#wat-u-in-het-verzoek-vraagt), [beleidsopvattingen](beleidsopvattingen.md#zo-formuleert-u-het-verzoek) |
| Verzoek verstuurd | Beslistermijn: 4 weken na ontvangst | Noteer de ontvangstdatum. Reken de einddatum uit | — | [procedure](procedure.md#beslistermijn-art-44-lid-1-woo) |
| Verzoek om precisering | Bestuursorgaan: binnen 2 weken na ontvangst | Preciseer snel en schriftelijk. Bied een gesprek aan | [overleg](../templates/overleg.md) | [procedure](procedure.md#precisering-art-41-lid-5-6-woo) |
| Besluit "niet behandelen" (art. 4.1 lid 6 of 4.6 Woo) | Bezwaar: 6 weken | Bezwaar | [bezwaar](../templates/bezwaar.md) | [procedure](procedure.md#niet-behandelen-bij-ander-doel-art-46-woo) |
| Verzoek doorgezonden naar ander orgaan | Termijn loopt bij dat orgaan | Vraag de ontvangstdatum bij het andere orgaan | — | [procedure](procedure.md#doorzenden-en-vorderen-art-42-woo) |
| Bestuursorgaan verdaagt | Verdaagde termijn: 6 weken na ontvangst | Toets de vier eisen. Ongeldig? Leg de oude einddatum vast | [reactie-verdaging](../templates/reactie-verdaging.md) | [procedure](procedure.md#verdaging-art-44-lid-2-woo) |
| Bestuursorgaan vraagt overleg of inperking | Vóór einde beslistermijn (art. 4.2a) | Vraag inventaris, tijdpad, tranches. Geef alleen iets tegen een schriftelijke datum | [overleg](../templates/overleg.md) | [overleg](overleg.md) |
| Bestuursorgaan vraagt instemming met uitstel | — | Instemming alleen voorwaardelijk, met einddatum | [overleg](../templates/overleg.md) | [procedure](procedure.md#opschorting), [overleg](overleg.md#wat-u-geeft) |
| Mededeling: zienswijze derden (art. 4:8 Awb) | Opschorting vanaf de dag na de mededeling | Vraag wie, welke termijn, en verstrekking van de rest | [overleg](../templates/overleg.md) | [procedure](procedure.md#opschorting), [overleg](overleg.md#zienswijzen-van-derden) |
| Einde opschorting gemeld | Nieuwe einddatum in de mededeling | Reken na; leg de datum vast | — | [procedure](procedure.md#opschorting) |
| Aanbod vertrouwelijke voorinzage | — | Lees de geheimhoudingsverklaring; geen voorlegplicht | — | [overleg](overleg.md#vertrouwelijke-voorinzage) |
| Beslistermijn verstreken, geen besluit | Dag na de laatste dag | Ingebrekestelling. Niet eerder | [ingebrekestelling](../templates/ingebrekestelling.md) | [rechtsmiddelen](rechtsmiddelen.md#ingebrekestelling-art-612-awb) |
| Twee weken na ontvangst ingebrekestelling, geen besluit | Geen vaste termijn; niet onredelijk laat | Beroep niet tijdig bij de rechtbank | [beroep-niet-tijdig](../templates/beroep-niet-tijdig.md) | [rechtsmiddelen](rechtsmiddelen.md#beroep-niet-tijdig-art-612-855b-855d-awb-art-84-woo) |
| Besluit tijdens beroep niet tijdig | — | Beroep loopt door; voeg gronden tegen het besluit toe | [beroep](../templates/beroep.md) | [rechtsmiddelen](rechtsmiddelen.md#beroep-niet-tijdig-art-612-855b-855d-awb-art-84-woo) |
| Besluit ontvangen | Bezwaar: 6 weken na bekendmaking | Toets zoekslag, inventarislijst, lakken, gronden | — | [zoekslag](zoekslag.md), [weigeringsgronden](weigeringsgronden.md#toets-een-weigering-in-vijf-vragen), [praktijk](praktijk.md#besluit-controleren) |
| Besluit onvolledig of onjuist | Bezwaar: 6 weken | Bezwaar; zo nodig pro forma, gronden later | [bezwaar](../templates/bezwaar.md) | [rechtsmiddelen](rechtsmiddelen.md#bezwaar-tegen-het-besluit) |
| Beslissing op bezwaar uitgebleven | Beslistermijn bezwaar: 6 weken (12 met commissie) + max. 6 weken verdaging | Ingebrekestelling, daarna beroep niet tijdig | [ingebrekestelling](../templates/ingebrekestelling.md) | [rechtsmiddelen](rechtsmiddelen.md#bezwaar-tegen-het-besluit) |
| Beslissing op bezwaar onjuist | Beroep: 6 weken | Beroep bij de rechtbank | [beroep](../templates/beroep.md) | [rechtsmiddelen](rechtsmiddelen.md#beroep-bij-de-rechtbank) |
| Uitspraak rechtbank onjuist | Hoger beroep: 6 weken | Hoger beroep bij de ABRvS | — | [rechtsmiddelen](rechtsmiddelen.md#hoger-beroep-abrvs) |
| Weigering wegens geheimhouding of andere wet | — | Vraag welke bepaling uit de bijlage; vraag opheffing geheimhouding | — | [andere wetten](andere-wetten.md) |
| Behandeling stokt; u bent journalist of onderzoeker | — | Klacht bij het ACOI | — | [rechtsmiddelen](rechtsmiddelen.md#klacht-bij-het-acoi-art-72-73-woo) |

## Termijnen in één tabel

| Termijn | Duur | Begint | Grondslag | `tools/termijn.py` |
|---|---|---|---|---|
| Beslissen op verzoek | 4 weken | Dag na ontvangst | [art. 4.4 lid 1 Woo](../wetten/woo/artikel_4-4.md) | `<ontvangst> 4w` |
| Verdaging | + max. 2 weken | Mededeling vóór einde 4 weken | art. 4.4 lid 2 Woo | `<ontvangst> 4w 2w` |
| Opschorting zienswijze | Duur van de zienswijzeperiode | Dag na mededeling art. 4:8 Awb | art. 4.4 lid 3 Woo | `<ontvangst> 4w <n>d` |
| Verzoek om precisering | Bestuursorgaan: 2 weken | Dag na ontvangst | [art. 4.1 lid 5 Woo](../wetten/woo/artikel_4-1.md) | `<ontvangst> 2w` |
| Niet behandelen (ander doel) | Bestuursorgaan: 2 weken | Dag na ontvangst | [art. 4.6 Woo](../wetten/woo/artikel_4-6.md) | `<ontvangst> 2w` |
| Uitgestelde verstrekking | 2 weken | Dag na bekendmaking besluit | art. 4.4 lid 5 Woo | `<bekendmaking> 2w` |
| Beroep na ingebrekestelling | 2 weken | Dag na de ingebrekestelling | [art. 6:12 lid 2 Awb](../wetten/awb/artikel_6-12.md) | `<ontvangst ingebrekestelling> 2w` |
| Bezwaar, beroep, hoger beroep | 6 weken | Dag na bekendmaking | [art. 6:7](../wetten/awb/artikel_6-7.md), [6:8 Awb](../wetten/awb/artikel_6-8.md) | `<bekendmaking> 6w` |
| Beslissen op bezwaar | 6 weken (12 met commissie) + max. 6 weken verdaging | Dag na einde bezwaartermijn | [art. 7:10 Awb](../wetten/awb/artikel_7-10.md) | `<einde bezwaartermijn> 6w 6w` |
| Beslissen op bezwaar na ACOI-advies | 2 weken | Na advies of bericht "geen advies" | [art. 7.3 lid 3 Woo](../wetten/woo/artikel_7-3.md) | `<advies> 2w` |
| Rechter na gegrond beroep niet tijdig | 2 weken (groot verzoek: door rechter bepaald) | Dag na verzending uitspraak | [art. 8:55d Awb](../wetten/awb/artikel_8-55d.md), [art. 8.4 Woo](../wetten/woo/artikel_8-4.md) | `<verzending> 2w` |
| Griffierecht betalen | 4 weken | Verzending mededeling griffier | [art. 8:41 lid 5 Awb](../wetten/awb/artikel_8-41.md) | `<verzending> 4w` |

## Termijn berekenen

```bash
tools/termijn.py 2026-11-02 4w        # beslistermijn
tools/termijn.py 2026-11-02 4w 2w     # met verdaging
tools/termijn.py 2026-11-02 6w 12d    # plus 12 dagen opschorting
```

- De datum is de gebeurtenis (ontvangst, mededeling, bekendmaking). De termijn begint de dag erna.
- Valt het einde op een zaterdag, zondag of feestdag, dan schuift het naar de eerstvolgende werkdag ([art. 1 Algemene termijnenwet](../wetten/termijnenwet/artikel_1.md)). Feestdagen inclusief Goede Vrijdag en 5 mei ([art. 3](../wetten/termijnenwet/artikel_3.md)).
- Het tool telt eerst alle perioden op en past de Atw toe op het einde. Twijfel over een keten (verdaging, opschorting)? Neem de latere datum. Een te vroege ingebrekestelling telt niet.
- Gebruik `day after` uit de uitvoer als datum voor de ingebrekestelling.
