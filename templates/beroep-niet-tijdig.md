---
title: Beroep niet tijdig beslissen
summary: Beroepschrift bij de rechtbank als het bestuursorgaan twee weken na de ingebrekestelling nog niet heeft beslist.
---

# Beroep niet tijdig beslissen

Bouw met `tools/build.py <brief>.md --bijlagen bijlagen/ --sign handtekening.png`. Algemene schrijfregels: [beroep.md](beroep.md).

## Regels

1. Instellen kan twee weken na ontvangst van de ingebrekestelling (art. 6:12 lid 2 Awb). Er is geen uiterste termijn, maar wacht niet lang.
2. Meerdere verzoeken over hetzelfde onderwerp: één beroepschrift, vraag voeging (art. 8:14 Awb).
3. Het procesverloop is een tabel met data. Elke regel heeft een bijlage.
4. Toon in 3.1 dat de termijn **niet** is opgeschort: geen mededeling over art. 4:8 Awb (art. 4.4 lid 3 Woo) en geen onvoorwaardelijke instemming (art. 4:15 lid 2 onder a Awb).
5. Groot verzoek: de rechter kan een andere termijn bepalen (art. 8.4 lid 1 Woo). Stel zelf een fasering voor (art. 8:55d lid 3 Awb). Toon uw medewerking; zonder medewerking kan de rechter de proceskosten weigeren (art. 8.4 lid 3 Woo).
6. Dwangsom: standaard volgens de beleidsregels van de rechtbanken. Vraag een hoger bedrag alleen als u weigerachtigheid met citaten kunt tonen.
7. Beslist het bestuursorgaan tijdens het beroep, dan loopt het beroep door tegen dat besluit (art. 6:20 lid 3 Awb). Zie [bezwaar.md](bezwaar.md) en [beroep.md](beroep.md).
8. Een zitting is meestal niet nodig (art. 8:55b Awb).

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

\noindent Rechtbank [Naam]\\
Team bestuursrecht\\
Postbus [Nummer]\\
[Postcode Plaats]

\vspace{7mm}

\noindent\begin{tabular}{@{}p{42mm}p{104mm}@{}}
\textsf{\small Plaats en datum} & [Plaats], {{datum}}\\[0.6ex]
\textsf{\small Betreft} & Beroep wegens niet tijdig beslissen\\[0.6ex]
\textsf{\small Verweerder} & [Bestuursorgaan]\\[0.6ex]
\textsf{\small Kenmerk verweerder} & [zaaknummer]
\end{tabular}

\vspace{3mm}
```

Edelachtbare,

## 1. Inleiding

Eiser stelt beroep in tegen het niet tijdig beslissen door verweerder op het Woo-verzoek van [datum], kenmerk [nummer] (bijlage 1). [Bij meer verzoeken: tabel met zaak, onderwerp, ingebrekestelling; verzoek om voeging (artikel 8:14 Awb).]

## 2. Procesverloop

| Datum | Gebeurtenis |
| ----- | ----------- |
| [datum] | Eiser dient het Woo-verzoek in (bijlage 1). |
| [datum] | Verweerder verdaagt de beslistermijn wegens [reden] (bijlage [X]). |
| [datum] | De verdaagde beslistermijn eindigt. |
| [datum] | Eiser stelt verweerder in gebreke (bijlage [X]). |
| [datum] | Twee weken na de ingebrekestelling, zonder besluit. |

Verweerder heeft tot op heden geen documenten verstrekt.

## 3. Beoordeling

### 3.1 Beslistermijn

De verdaagde termijn eindigde op [datum] (artikel 4.4, eerste en tweede lid, Woo). De termijn is niet opgeschort. Verweerder heeft niet meegedeeld dat hij artikel 4:8 Awb toepast (artikel 4.4, derde lid, Woo). Eiser heeft niet onvoorwaardelijk ingestemd met uitstel (artikel 4:15, tweede lid, onder a, Awb).

### 3.2 Ontvankelijkheid

Eiser heeft verweerder op [datum] in gebreke gesteld. Twee weken later was geen besluit genomen. Artikel 6:12, tweede lid, Awb staat niet aan het beroep in de weg.

### 3.3 Nadere beslistermijn

[Klein verzoek:] Gelet op de beperkte omvang bestaat geen aanleiding voor een andere termijn (artikel 8.4, eerste lid, Woo).
[Groot verzoek:] Eiser stelt een gefaseerde termijn voor (artikel 8.4, eerste lid, Woo, en artikel 8:55d, derde lid, Awb).

**Medewerking van eiser (artikel 8.4, derde lid, Woo).** Eiser heeft steeds meegewerkt:

* op [datum] [voorstel tot fasering / zoektermen / inperking] (bijlage [X]);
* op [datum] [...].

### 3.4 Dwangsom

[Standaard bedrag volgens de beleidsregels van de rechtbanken. Bij weigerachtigheid: citaat van verweerder met bijlage, en verzoek om een sterkere prikkel.]

## 4. Verzoek

Eiser verzoekt de rechtbank:

1. het beroep gegrond te verklaren;
2. verweerder op te dragen binnen [twee weken / de termijnen hieronder] na verzending van de uitspraak alsnog te beslissen;

   | Fase | Onderdelen | Termijn na verzending uitspraak |
   | ---- | ---------- | ------------------------------- |
   | 1 | [nummers] | [X] weken |
   | 2 | [nummers] | [X] weken |

3. aan deze termijn(en) een dwangsom te verbinden van € [bedrag] per dag, met een maximum van € [bedrag] (artikel 8:55d, tweede lid, Awb);
4. te bepalen dat verweerder bij ieder (deel)besluit een inventarislijst verstrekt en de documenten verstrekt in de gevraagde vorm (artikel 4.5, eerste lid, Woo);
5. verweerder te veroordelen in de proceskosten en tot vergoeding van het griffierecht (artikelen 8:74 en 8:75 Awb).

Eiser acht een onderzoek ter zitting niet nodig (artikel 8:55b, eerste lid, Awb).

Hoogachtend,

\vspace{16mm}

[Naam]

## Bijlagen

1. Woo-verzoek van [datum] met ontvangstbevestiging
2. Verdaging van [datum]
3. [Correspondentie over prioritering]
4. Ingebrekestelling van [datum]
````
