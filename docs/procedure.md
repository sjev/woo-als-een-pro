---
title: Procedure en termijnen
summary: Van ontvangst tot verstrekking. Beslistermijn, verdaging, opschorting, precisering, overleg, zienswijze derden, vorm.
---

# Procedure en termijnen

Wetstekst: Woo geldig vanaf 2026-08-15, Awb geldig vanaf 2026-08-15. Reken elke termijn uit met `tools/termijn.py` (zie [termijn berekenen](stappenplan.md#termijn-berekenen)).

## Tijdlijn

| Dag | Gebeurtenis | Grondslag |
|---|---|---|
| 0 | Verzoek ontvangen. Termijnen lopen vanaf de dag erna | [art. 4.4 lid 1 Woo](../wetten/woo/artikel_4-4.md) |
| ≤ 2 weken | Verzoek om precisering, of besluit "niet behandelen" bij ander doel | [art. 4.1 lid 5](../wetten/woo/artikel_4-1.md), [art. 4.6 Woo](../wetten/woo/artikel_4-6.md) |
| < 4 weken | Overleg bij omvangrijk verzoek; mededeling verdaging | [art. 4.2a](../wetten/woo/artikel_4-2a.md), [art. 4.4 lid 2 Woo](../wetten/woo/artikel_4-4.md) |
| 4 weken | Einde beslistermijn | art. 4.4 lid 1 Woo |
| 6 weken | Einde verdaagde termijn | art. 4.4 lid 2 Woo |
| + opschorting | Dagen van zienswijze, instemming met uitstel, toerekenbare vertraging | art. 4.4 lid 3 Woo, [art. 4:15 Awb](../wetten/awb/artikel_4-15.md) |
| Besluit + 2 weken | Verstrekking als een derde naar verwachting bezwaar heeft | art. 4.4 lid 5 Woo |

Daarna: [rechtsmiddelen](rechtsmiddelen.md).

## Indienen

- Iedereen kan een verzoek doen. Mondeling of schriftelijk, ook elektronisch op de aangegeven wijze ([art. 4.1 lid 1-2 Woo](../wetten/woo/artikel_4-1.md)).
- U hoeft geen belang te stellen (art. 4.1 lid 3). U noemt de aangelegenheid of het document (art. 4.1 lid 4).
- Een verzoek aan een instelling, dienst of bedrijf onder verantwoordelijkheid van een bestuursorgaan: het verantwoordelijke bestuursorgaan beslist (art. 4.1 lid 1).
- Vanaf ontvangst moet het bestuursorgaan de gevraagde documenten bewaren ([art. 4.1a Woo](../wetten/woo/artikel_4-1a.md)). Noem dit artikel als u vreest dat berichten of mailboxen worden gewist.
- Vraag schriftelijk. Bij een schriftelijk verzoek volgt een gehele of gedeeltelijke afwijzing altijd schriftelijk ([art. 4.3 lid 2 onder a Woo](../wetten/woo/artikel_4-3.md)). Alleen een schriftelijk besluit is een vast startpunt voor bezwaar.

## Precisering (art. 4.1 lid 5-6 Woo)

- Is het verzoek te algemeen? Dan vraagt het bestuursorgaan binnen twee weken om precisering. Het moet u daarbij helpen ([art. 4.1 lid 5 Woo](../wetten/woo/artikel_4-1.md)).
- Werkt u niet mee, dan kan het besluiten het verzoek niet te behandelen. Dat besluit komt binnen twee weken na de precisering of na afloop van de gestelde termijn (art. 4.1 lid 6).
- Een verzoek om precisering schort de beslistermijn op tot het verzoek voldoende is gepreciseerd. Bron: instructie § 3.3.1, via [art. 4:15 lid 1 onder a](../wetten/awb/artikel_4-15.md) en [art. 4:5 Awb](../wetten/awb/artikel_4-5.md). [niet geverifieerd]
- Praktijk: antwoord snel en concreet. Vraag om een gesprek als de vraag vaag is. Leg de precisering schriftelijk vast.
- Komt het verzoek om precisering na meer dan twee weken? Dan is het te laat volgens art. 4.1 lid 5. Wijs daarop, maar preciseer toch. Zo voorkomt u discussie over opschorting.

## Niet behandelen bij ander doel (art. 4.6 Woo)

- Het bestuursorgaan kan een verzoek niet behandelen als u kennelijk een ander doel hebt dan publieke informatie, of als het verzoek evident geen bestuurlijke aangelegenheid betreft ([art. 4.6 Woo](../wetten/woo/artikel_4-6.md)).
- Termijn: binnen twee weken na ontvangst, of onverwijld nadat het andere doel is gebleken.
- Een geschil met het bestuursorgaan is op zich geen misbruik. De rechter neemt misbruik niet snel aan. Bron: instructie § 3.3.3. [niet geverifieerd]

## Doorzenden en vorderen (art. 4.2 Woo)

- Berust de informatie bij een ander bestuursorgaan? Dan zendt het bestuursorgaan een schriftelijk verzoek onverwijld door en meldt dat aan u ([art. 4.2 lid 1 Woo](../wetten/woo/artikel_4-2.md)). Uw termijnen lopen dan bij het andere orgaan.
- Had de informatie volgens een wettelijk voorschrift bij het bestuursorgaan moeten berusten? Dan vordert het de informatie van wie haar heeft (art. 4.2 lid 2). Het kan dat afdwingen met een last onder dwangsom ([art. 8.5 Woo](../wetten/woo/artikel_8-5.md)).
- Praktijk: stukken van andere bestuursorganen hebben meestal geen zienswijze nodig. Vraag om die stukken eerst te verstrekken ([praktijk](praktijk.md#overleg-en-prioritering)).

## Beslistermijn (art. 4.4 lid 1 Woo)

- Zo spoedig mogelijk, uiterlijk vier weken vanaf de dag na ontvangst ([art. 4.4 lid 1 Woo](../wetten/woo/artikel_4-4.md)).
- Eindigt de termijn op een zaterdag, zondag of algemeen erkende feestdag? Dan schuift het einde naar de eerstvolgende werkdag ([art. 1 Algemene termijnenwet](../wetten/termijnenwet/artikel_1.md); feestdagen: [art. 3](../wetten/termijnenwet/artikel_3.md)).
- Voorbeeld: `tools/termijn.py 2026-11-02 4w` geeft maandag 2026-11-30.

## Verdaging (art. 4.4 lid 2 Woo)

Een verdaging is alleen geldig als zij aan alle eisen voldoet ([art. 4.4 lid 2 Woo](../wetten/woo/artikel_4-4.md)):

| Eis | Toets |
|---|---|
| Ten hoogste twee weken | Langer kan alleen via opschorting |
| Grond: omvang of gecompliceerdheid **van de informatie** | Vakantie, reces, werkdruk en interne afstemming gaan niet over de informatie |
| Schriftelijk en gemotiveerd | Een losse zin zonder reden is geen motivering |
| Voor afloop van de eerste termijn | Komt de mededeling na vier weken? Dan is de termijn al verstreken |

- Is de verdaging ongeldig? Dan eindigt de termijn na vier weken. Leg dat schriftelijk vast. Sjabloon: [reactie-verdaging](../templates/reactie-verdaging.md).
- Twijfelt u? Reken met de latere datum. Een te vroege ingebrekestelling telt niet ([rechtsmiddelen](rechtsmiddelen.md)).

## Opschorting

De termijn staat stil. De dagen tellen niet mee. Gronden:

| Grond | Begin | Einde | Bron |
|---|---|---|---|
| Zienswijze van derden | Dag na de mededeling aan u dat art. 4:8 Awb wordt toegepast | Dag waarop de zienswijze binnen is, of de termijn ongebruikt is verstreken | [art. 4.4 lid 3 Woo](../wetten/woo/artikel_4-4.md) |
| U stemt schriftelijk in met uitstel | Volgens de instemming | Einde van de periode waarmee u instemde | [art. 4:15 lid 2 onder a Awb](../wetten/awb/artikel_4-15.md) |
| Vertraging is aan u toe te rekenen | Begin vertraging | Einde vertraging | art. 4:15 lid 2 onder b Awb |
| Overmacht | Mededeling van overmacht | Einde overmacht | art. 4:15 lid 2 onder c, lid 3 Awb |

- Een losse aankondiging van een zienswijze is niet genoeg. Het bestuursorgaan moet meedelen dat art. 4:8 Awb wordt toegepast (art. 4.4 lid 3 Woo).
- Eindigt de opschorting voor de zienswijze? Dan meldt het bestuursorgaan dat zo spoedig mogelijk, met de nieuwe einddatum (art. 4.4 lid 4 Woo). Vraag die datum als de mededeling uitblijft.
- Instemming met uitstel is een ruilmiddel. Geef haar alleen tegen een schriftelijk tijdpad. Zonder instemming loopt de termijn door ([praktijk](praktijk.md#verdaging-en-opschorting)).
- Weigert u bij een groot verzoek redelijk uitstel? Dan kan de rechter later de proceskosten weigeren ([art. 8.4 lid 3 Woo](../wetten/woo/artikel_8-4.md)). Weeg dat af.

## Overleg bij een omvangrijk verzoek (art. 4.2a Woo)

- Is een voldoende gespecificeerd verzoek te groot voor vier weken? Dan overlegt het bestuursorgaan **voor het einde van die termijn** met u over de prioritering ([art. 4.2a Woo](../wetten/woo/artikel_4-2a.md)).
- Het verstrekt de documenten zo veel mogelijk in de volgorde die u wilt (art. 4.2a).
- Overleg zelf schort de termijn niet op. Alleen uw schriftelijke instemming met uitstel doet dat (art. 4:15 lid 2 onder a Awb).
- Een eerste deel (bijv. de vijftig belangrijkste documenten) laat uw recht op de rest intact. Bron: instructie § 3.3.2.
- Wat u in het overleg vraagt: [praktijk](praktijk.md#overleg-en-prioritering). Sjabloon: [overleg](../templates/overleg.md).

## Zienswijze van derden (art. 4:8 Awb)

- Het bestuursorgaan vraagt een zienswijze aan een belanghebbende die naar verwachting bedenkingen heeft, als het besluit steunt op gegevens over die belanghebbende die hij niet zelf heeft verstrekt ([art. 4:8 lid 1 Awb](../wetten/awb/artikel_4-8.md)).
- Niet iedereen die in een document staat, heeft bedenkingen. Vraag welke derden zijn aangeschreven en waarom.
- De wet noemt geen termijn voor de zienswijze. Gebruikelijk is twee weken. Bron: instructie § 3.5.
- Vraag om stukken zonder zienswijze alvast te verstrekken. Dat mag: uitgestelde verstrekking geldt alleen voor de stukken waartegen een derde bezwaar heeft (art. 4.4 lid 5 Woo).

## Besluit en verstrekking

- Besluit het bestuursorgaan tot openbaarmaking? Dan verstrekt het de informatie tegelijk met het besluit ([art. 4.4 lid 5 Woo](../wetten/woo/artikel_4-4.md)).
- Heeft een belanghebbende naar verwachting bezwaar? Dan volgt de verstrekking twee weken na bekendmaking. Vraagt die belanghebbende een voorlopige voorziening, dan wacht de verstrekking op de voorzieningenrechter (art. 4.4 lid 5).
- Gaat informatie over een derde of komt zij van een derde? Dan krijgt die derde het besluit tegelijk (art. 4.4 lid 6).

## Vorm van verstrekking (art. 4.5 Woo)

- U krijgt de informatie in de vorm die u vraagt, tenzij dat redelijkerwijs niet kan ([art. 4.5 lid 1 Woo](../wetten/woo/artikel_4-5.md)).
- Anders geldt de rangorde van [art. 2.4 lid 3 Woo](../wetten/woo/artikel_2-4.md): (a) herbruikbaar, machineleesbaar open formaat; (b) andere elektronisch doorzoekbare vorm; (c) kopie in andere vorm; (d) uittreksel, samenvatting, inlichtingen of inzage.
- Een scan zonder doorzoekbare tekst is geen (a) of (b). Vraag in het verzoek om losse, doorzoekbare bestanden en een inventarislijst als spreadsheet.
- Is de informatie al openbaar en gemakkelijk toegankelijk? Dan wijst het bestuursorgaan u daarop (art. 4.5 lid 2).
