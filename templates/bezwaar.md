---
title: Pro-forma bezwaar
summary: Bezwaar dat de termijn veiligstelt; gronden volgen later of staan in een lopend beroep.
---

# Pro-forma bezwaar

Bouw met `tools/build.py`. Algemene schrijfregels: [beroep.md](beroep.md).

## Regels

1. Bezwaartermijn: zes weken na bekendmaking van het besluit (art. 6:7 Awb). Pro-forma bezwaar houdt die termijn open. Het bestuursorgaan geeft dan een termijn om de gronden aan te vullen (art. 6:6 Awb).
2. Loopt er al beroep wegens niet tijdig beslissen? Dan is dat beroep mede gericht tegen het latere besluit (art. 6:20 lid 3 Awb). Bezwaar is dan niet de juiste weg, ook als de rechtsmiddelenclausule dat zegt. Maak toch pro-forma bezwaar en vraag doorzending naar de rechtbank (art. 2:3 Awb). Gebruik blok A.
3. Zonder lopend beroep: vraag zo nodig rechtstreeks beroep (art. 7:1a Awb). Gebruik blok B.
4. Noem de gronden in het kort. Gangbare gronden bij Woo-besluiten:
   - onvolledige zoekslag: documenten die bij het bestuursorgaan berusten maar ontbreken;
   - zoekverantwoording ontbreekt: geen systemen, zoektermen of periode per onderdeel;
   - onjuist weggelakt: dezelfde informatie hier gelakt en daar niet; feiten of emissiegegevens gelakt;
   - inventarislijst te summier: geen datum, afzender of geadresseerde (art. 3:46 Awb).
5. Kies blok A of B en nummer de punten opnieuw.

## Template

````markdown
```{=latex}
\thispagestyle{empty}
\vspace*{-14mm}
\hfill\begin{minipage}[t]{58mm}
[Naam]\\
[Straat en huisnummer]\\
[Postcode Plaats]\\[1ex]
{\small [Telefoon]\\
[E-mail]}
\end{minipage}

\vspace{7mm}

\noindent [Bestuursorgaan]\\
Postbus [Nummer]\\
[Postcode Plaats]

\vspace{7mm}

\noindent\begin{tabular}{@{}p{42mm}p{104mm}@{}}
\textsf{\small Plaats en datum} & [Plaats], {{datum}}\\[0.6ex]
\textsf{\small Betreft} & Pro-forma bezwaar tegen het besluit van [datum]\\[0.6ex]
\textsf{\small Uw kenmerk} & [zaaknummer]
\end{tabular}

\vspace{3mm}
```

Geacht [college],

1. Op [datum] heeft u besloten op mijn Woo-verzoek [nummer]. Tegen dit besluit maak ik bezwaar.

[Blok A: beroep niet tijdig loopt]

2. Bij de rechtbank [naam] loopt mijn beroep wegens niet tijdig beslissen ([zaaknummer rechtbank]). Op grond van artikel 6:20, derde lid, Awb is dat beroep mede gericht tegen dit besluit. De rechtsmiddelenclausule noemt ten onrechte bezwaar.
3. Ik maak dit bezwaar alleen ter bescherming van mijn rechten. Ik verzoek u dit geschrift onverwijld door te zenden aan de rechtbank (artikel 2:3 Awb), ter voeging bij [zaaknummer rechtbank].

[Blok B: geen lopend beroep]

2. Ik verzoek u in te stemmen met rechtstreeks beroep bij de rechtbank (artikel 7:1a Awb).

[Gemeenschappelijk]

4. De gronden zijn in het kort:
   a. [grond];
   b. [grond].
5. Ik verzoek u mij een termijn te geven om de gronden aan te vullen (artikel 6:6 Awb).

Hoogachtend,

\vspace{16mm}

[Naam]
````
