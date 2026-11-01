# Woo als een pro

> Kennis voor AI-agents die een verzoeker helpen bij een Woo-verzoek (Wet open overheid): welke stap, welke termijn, welke brief, welke grondslag.

Elke pagina is markdown met front matter. Links in een pagina zijn relatief en wijzen naar markdown op deze site.

## Werkwijze

1. Vraag de gebruiker naar de feiten: bestuursorgaan, inhoud en datum van het verzoek, datum van ontvangst, het laatste bericht van het bestuursorgaan.
2. Zoek de situatie in het [stappenplan](https://woo.dasopen.nl/docs/stappenplan.md). Daar staan termijn, actie, sjabloon en het document met de regels.
3. Lees dat document. Volg de links naar wetstekst en uitspraken als u de grondslag nodig hebt.
4. Reken termijnen uit zoals [Termijn berekenen](https://woo.dasopen.nl/docs/stappenplan.md#termijn-berekenen) beschrijft.
5. Schrijf de brief met het sjabloon. Vul alles tussen `[...]` in. Vervang `{{datum}}` door de datum van verzending. Ontbreekt een gegeven? Vraag het de gebruiker. Verzin geen feiten.

## Regels

- Elk juridisch feit op deze site heeft een bron: een wetsartikel of een uitspraak. Noem die bron in uw advies en in de brief.
- Elk artikel van de [wetten](https://woo.dasopen.nl/wetten/README.md) staat op een vast adres: `/wetten/<wet>/artikel_<nr>.md`. Art. 6:12 Awb is `/wetten/awb/artikel_6-12.md`. De tekst geldt vanaf `valid_from` in de front matter.
- [Bronnen](https://woo.dasopen.nl/bronnen/README.md) zijn achtergrond. Zij zijn nooit de enige grondslag.
