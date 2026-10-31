---
title: Beroepschrift
summary: Regels en sjabloon voor een beroepschrift bij de rechtbank.
---

# Beroepschrift

- **Stijl:** Beknopt, zakelijk, 'headlines-first'. Geen vultekst. Korte zinnen, één gedachte per zin.
- **Regels:**
  1. Nummering: hoofdstukken `## 1.`, `## 2.` …; gronden `### 3.1`, `### 3.2` …; doorlopende randnummers (1, 2, 3 …) over het hele stuk; onderdelen van het verzoek I, II, III …. Geen letters of `1e`. De rechter en verweerder verwijzen naar randnummers ("punt 17").
  2. Scheid achtergrond strikt van gronden. De achtergrond geeft alleen wat de rechter nodig heeft om de gronden te volgen.
  3. Begin de gronden met een samenvatting: één regel per grond. Elke regel is gelijk aan het kopje van die grond.
  4. Het kopje van een grond is de stelling: "Verweerder heeft miskend dat …", "Het besluit is onzorgvuldig voorbereid doordat …".
  5. Elke grond volgt: standpunt verweerder (citaat met paginanummer van het besluit) → standpunt eiser → juridisch kader (artikel, ECLI met r.o.) → uitwerking → conclusie.
  6. Lange grond: deel de uitwerking op met tussenkopjes per deelargument. Sluit af met een eigen conclusie.
  7. Elke feitelijke bewering heeft een vindplaats: bijlage X, p. Y. Een externe bron (handreiking, beleid) staat in een voetnoot met URL.
  8. Detail (lijsten, tijdlijnen, vindplaatsen per stuk) gaat naar een overzichtsbijlage. In de tekst staan alleen het aantal en twee of drie voorbeelden.
  9. Is er een eerder stuk (bezwaar, zienswijze)? Verklaar het "herhaald en ingelast". Herhaal het niet.
  10. Nummer bijlagen door vanaf het vorige stuk in dezelfde procedure.
  11. Vul variabelen tussen `[...]` in of vraag erom. `{{datum}}` blijft staan; die vult `tools/build.py`. Verzind geen feiten.

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
\textsf{\small Betreft} & Beroepschrift\\[0.6ex]
\textsf{\small Bestreden besluit} & [datum], kenmerk [kenmerk]\\[0.6ex]
\textsf{\small Verweerder} & [Bestuursorgaan, bijv. college van B\&W van [gemeente]]\\[0.6ex]
\textsf{\small Uw kenmerk} & [zaaknummer rechtbank / nader te bepalen]
\end{tabular}

\vspace{3mm}
```

Edelachtbare,

## 1. Inleiding

1. Eiser stelt beroep in tegen het besluit van [verweerder] (hierna: verweerder) van [datum], kenmerk [kenmerk] (bijlage [X]).

2. [Optioneel] Eiser diende op [datum] [bezwaar / een zienswijze] in (bijlage [X]). Dat stuk geldt hier als herhaald en ingelast.

## 2. Achtergrond

3. [Het verzoek of de aanvraag: wat, wanneer, door wie (bijlage [X]).]

4. [Wat verweerder besliste, in één zin (bijlage [X]).]

5. [Alleen de feiten die nodig zijn om de gronden te volgen.]

## 3. Gronden van beroep

6. Samengevat gelden de volgende gronden:

   - verweerder heeft miskend dat [stelling grond 1];
   - het besluit is [onzorgvuldig voorbereid / onvoldoende gemotiveerd] doordat [stelling grond 2];
   - [stelling grond 3].

### 3.1 Verweerder heeft miskend dat [stelling grond 1]

7. Op p. [Y] van het besluit stelt verweerder:

   > [citaat uit het besluit]

8. Dit is onjuist. [Standpunt eiser in één of twee zinnen.]

9. [Juridisch kader: artikel [X] [wet]. ECLI:NL:RVS:[JJJJ]:[XXXX], r.o. [N]:]

   > [citaat uit de uitspraak]

10. [Uitwerking, met vindplaats per feit: bijlage [X], p. [Y].]

#### [Tussenkopje deelargument, bij een lange grond]

11. [Uitwerking deelargument.]

12. Conclusie: [het besluit is in strijd met artikel [X] [wet]].

### 3.2 Het besluit is [onzorgvuldig voorbereid] doordat [stelling grond 2]

13. [Uitwerking volgens hetzelfde schema.]

14. Conclusie: het besluit is in strijd met [artikel 3:2 / 3:46 Awb].

## 4. Procedurele verzoeken

15. [Optioneel. Bijv. behandeling ter zitting; opdracht tot overlegging van stukken of inlichtingen (artikelen 8:42 en 8:45 Awb); kennisneming alleen door de rechtbank (artikel 8:29 Awb).]

## 5. Verzoek

16. Eiser verzoekt de rechtbank:

    I.   het beroep gegrond te verklaren;
    II.  het besluit van [datum] (kenmerk [kenmerk]) te vernietigen;
    III. [Optie A] zelf in de zaak te voorzien door [bijv. de documenten openbaar te maken];
         [Optie B] verweerder op te dragen binnen [X] weken een nieuw besluit te nemen, met inachtneming van de uitspraak en [eisen aan het nieuwe besluit], op straffe van een dwangsom (artikel 8:72, zesde lid, Awb);
    IV.  verweerder te veroordelen in de proceskosten en tot vergoeding van het griffierecht (artikelen 8:74 en 8:75 Awb).

17. [Optioneel] Subsidiair verzoekt eiser de rechtbank verweerder in de gelegenheid te stellen de gebreken te herstellen (artikel 8:51a Awb).

Hoogachtend,

\vspace{16mm}

[Naam]

## Bijlagen

[Bijlagen 1 tot en met X zijn eerder ingediend, bij (stuk).]

[X]. Bestreden besluit van [datum], kenmerk [kenmerk]
[X]. [Verzoek / aanvraag] van [datum]
[X]. [Bezwaar / zienswijze] van [datum]
[X]. [Overzicht / aanvullend bewijs]
````
