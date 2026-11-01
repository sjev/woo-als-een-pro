# Woo als een pro

> Kennis voor AI-agents die een verzoeker helpen bij een Woo-verzoek (Wet open overheid): welke stap, welke termijn, welke brief, welke grondslag.

Elke pagina is markdown met front matter. Links in een pagina zijn relatief en wijzen naar markdown op deze site.

## Werkwijze

1. Vraag de gebruiker naar de feiten: bestuursorgaan, inhoud en datum van het verzoek, datum van ontvangst, het laatste bericht van het bestuursorgaan.
2. Zoek de situatie in het [stappenplan](/docs/stappenplan.md). Daar staan termijn, actie, sjabloon en het document met de regels.
3. Lees dat document. Volg de links naar wetstekst en uitspraken als u de grondslag nodig hebt.
4. Reken elke termijn uit met [`/termijn`](/termijn?datum=2026-11-02&duur=4w). `datum` is de gebeurtenis: ontvangst, mededeling of bekendmaking. `duur` is de termijn, met verdaging en opschorting erbij: `4w,2w,12d`. Gebruik `day after` als datum voor de ingebrekestelling. De regels staan in [Termijn berekenen](/docs/stappenplan.md#termijn-berekenen).
5. Schrijf de brief met het sjabloon. Vul alles tussen `[...]` in. Vervang `{{datum}}` door de datum van verzending. Ontbreekt een gegeven? Vraag het de gebruiker. Verzin geen feiten.

## Regels

- Elk juridisch feit op deze site heeft een bron: een wetsartikel of een uitspraak. Noem die bron in uw advies en in de brief.
- Elk artikel van de [wetten](/wetten/README.md) staat op een vast adres: `/wetten/<wet>/artikel_<nr>.md`. Art. 6:12 Awb is `/wetten/awb/artikel_6-12.md`. De tekst geldt vanaf `valid_from` in de front matter.
- [Bronnen](/bronnen/README.md) zijn achtergrond. Zij zijn nooit de enige grondslag.
