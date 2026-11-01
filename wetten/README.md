# Wetten

Geldende wetstekst uit het [Basiswettenbestand](https://wetten.overheid.nl). EU-recht uit de [Cellar](https://op.europa.eu/) van het Publicatiebureau. Eén bestand per artikel.

| Map | Wet | BWB-ID |
|---|---|---|
| [`woo/`](woo/_wet.md) | Wet open overheid | BWBR0045754 |
| [`awb/`](awb/_wet.md) | Algemene wet bestuursrecht | BWBR0005537 |
| [`termijnenwet/`](termijnenwet/_wet.md) | Algemene termijnenwet | BWBR0002448 |
| [`archiefwet/`](archiefwet/_wet.md) | Archiefwet 1995 | BWBR0007376 |
| [`omgevingswet/`](omgevingswet/_wet.md) | Omgevingswet | BWBR0037885 |
| [`wm/`](wm/_wet.md) | Wet milieubeheer | BWBR0003245 |
| [`gemeentewet/`](gemeentewet/_wet.md) | Gemeentewet | BWBR0005416 |
| [`provinciewet/`](provinciewet/_wet.md) | Provinciewet | BWBR0005645 |
| [`uavg/`](uavg/_wet.md) | Uitvoeringswet AVG | BWBR0040940 |
| [`avg/`](avg/_wet.md) | Algemene verordening gegevensbescherming (EU 2016/679), tekst PB L 119; rectificaties niet verwerkt [niet geverifieerd] | CELEX:32016R0679 |
| [`aarhus/`](aarhus/_wet.md) | Verdrag van Aarhus (Nederlandse vertaling; authentiek is Engels en Frans) | BWBV0001700 |

## Indeling

- `<wet>/_wet.md`: front matter (`bwb_id`, `title`, `valid_from`, `fetched_at`, `source`) en inhoudsopgave.
- `<wet>/artikel_<nr>.md`: één artikel. Punt en dubbele punt worden een koppelteken: art. `5.1` → `artikel_5-1.md`, art. `6:12` → `artikel_6-12.md`, art. `15a` → `artikel_15a.md`.
- `<wet>/bijlage.md` of `bijlage_<n>.md`: een bijlage bij de wet. Voorbeeld: [bijlage Woo](woo/bijlage.md) (bijzondere openbaarmakingsregelingen, art. 8.8 Woo).

Citeer een artikel alleen uit deze bestanden. Noem `valid_from`.
