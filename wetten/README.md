# Wetten

Geldende wetstekst uit het [Basiswettenbestand](https://wetten.overheid.nl). Eén bestand per artikel.

| Map | Wet | BWB-ID |
|---|---|---|
| [`woo/`](woo/_wet.md) | Wet open overheid | BWBR0045754 |
| [`awb/`](awb/_wet.md) | Algemene wet bestuursrecht | BWBR0005537 |
| [`termijnenwet/`](termijnenwet/_wet.md) | Algemene termijnenwet | BWBR0002448 |
| [`archiefwet/`](archiefwet/_wet.md) | Archiefwet 1995 | BWBR0007376 |
| [`omgevingswet/`](omgevingswet/_wet.md) | Omgevingswet | BWBR0037885 |

## Indeling

- `<wet>/_wet.md`: front matter (`bwb_id`, `title`, `valid_from`, `fetched_at`, `source`) en inhoudsopgave.
- `<wet>/artikel_<N>-<M>.md`: één artikel. Art. `5.1` wordt `artikel_5-1.md`, art. `6:12` wordt `artikel_6-12.md`.

Citeer een artikel alleen uit deze bestanden. Noem `valid_from`.

## Bijwerken

```bash
wetten/fetch.py update               # alle wetten
wetten/fetch.py update woo           # één wet
wetten/fetch.py add BWBR0005537 awb  # nieuwe wet
```

`update` vervangt de map van de wet. Draait via `uv`; geen andere afhankelijkheden.
