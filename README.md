# Woo als een pro

Kennisbank en tools voor Woo-verzoeken. Doelgroep: LLM-agents en mensen.
Documenten zijn kort. Zij verwijzen naar wetstekst en jurisprudentie.

## Structuur

| Map | Inhoud |
|---|---|
| [`docs/`](docs/) | Kennisbank in markdown |
| [`templates/`](templates/) | Briefsjablonen: verzoek, reactie op verdaging, overleg, ingebrekestelling, beroep, bezwaar |
| [`tools/`](tools/) | Scripts om brieven te bouwen |
| [`wetten/`](wetten/) | Geldende wetstekst, één bestand per artikel |
| [`data-collection/`](data-collection/) | Bronnen ophalen en omzetten naar markdown |

## Inhoud (TOC)

1. [Overzicht](docs/01-overzicht.md) — de Woo in 4 stappen, van vraag tot document
2. [Procedure en termijnen](docs/02-procedure-termijnen.md) — beslistermijn, verdaging, opschorting, zienswijze derden
3. [Weigeringsgronden](docs/03-weigeringsgronden.md) — art. 5.1 en 5.2 Woo
4. [Rechtsmiddelen](docs/04-rechtsmiddelen.md) — ingebrekestelling, dwangsom, bezwaar, beroep
5. [Verhouding tot andere wetten](docs/05-andere-wetten.md) — Awb, Archiefwet, Omgevingswet, milieu-informatie
6. [Praktijk](docs/06-praktijk.md) — verzoek formuleren, precisering, opvolging, lessen uit eigen zaken
7. [Bronnen](docs/bronnen.md) — wetten, jurisprudentie, handreikingen

Sjablonen: zie [`templates/README.md`](templates/README.md). Tools: zie [`tools/README.md`](tools/README.md).

## Conventies

- Eén onderwerp per document. Doel: < 200 regels.
- Elk document begint met YAML front matter: `title`, `summary`.
- Verwijs naar artikelen met een link naar [wetten.overheid.nl](https://wetten.overheid.nl).
- Verwijs naar uitspraken met ECLI en een link naar [uitspraken.rechtspraak.nl](https://uitspraken.rechtspraak.nl).
