## Úvod do sportovního sázení

Sportovní sázení je hra dvou hráčů: bookmakera a sázkaře. Úlohou bookmakera je nabizet sázkařům příležitosti k sázkám s cílem maximalizovat svůj vlastní získ. Blíží-li se tedy například nějaké fotbalové utkání dvou týmů, bookmaker vypíše tzv. kurzy na možné výsledky. Sázkař si může zvolit, na které zápasy a výsledky by si chtěl vsadit. V případě, že si sázkař vsadí na výsledek, který nastane, vyhrává sázkař vloženou sázku vynásobenou kurzem bookmakera. Pokud daný výsledek nenastane, sázkař svou sázku prohrál. Příklad: pro zápas Slavia - Sparta vypíše bookmaker kurzy 1.6 na výhru domácích (Slavia), 3.75 na remízu a 6.6 na vítězství Sparty. Sázkař, který má k dispozici 1000 Kč, se rozhodne vsadit 100 Kč na vítězství Slavie a 40 Kč na remízu. Po vsazení vkladů má na svém kontě 860 Kč. Předpokládejmě, že utkání skončí remízou. Sázkař vyhrává 3.75 x 40 = 150 Kč. Jeho sázka na výhru domácích propadá bookmakerovi. Ve finále má sázkař na kontě 1010 Kč. 

## Zadání

Vaším úkolem bude naprogramovat co nejúspešnějšího sázkaře. V naší soutěži však nebude rozhodovat počet shédnutých fotbalových zápasů, nýbrž vaše schopnost navrhnout, implementovat a otestovat model, který se naučí predikovat výsledky nadcházejících zápasů z historických dat. 

Konkrétně se jedná o fotbalové zápasy z ligových soutěží z celého světa. Jelikož jednotlivé ročníky ligových soutěží (sezóny) trvají několik měsíců, bude se váš model v průběhu sezóny adaptovat na nová data. 

Každý den, kdy jsou na trhu nějaké sázkařské příležitosti, obdržíte inkrement dat, sázkařské příležitosti a shrnutí. Od vás budeme očekávat sázky, které si přejete uskutečnit.

### DataFrame se shrnutím

Ve shrnutí se dozvíte aktuální datum a jaké prostředky máte k dispozici.

|    |   Bankroll | Date                |   min_bet |   max_bet |
|---:|-----------:|:--------------------|----------:|----------:|
|  0 |    1000    | 2003-09-14 00:00:00 |         5 |       100 |

- bankroll - Aktuální stav vašeho konta
- date - Aktuální datum 
- min_bet - Minimální možná nenulová sázka
- max_bet - Maximální možná sázka

### DataFrame inkrementálních dat

Inkrementální data obsahují výsledky, které jste doposud neviděli (jedná se o nově odehrané zápasy). Počítejte s tím, že první inkrement který uvidíte, bude obsahovat i zápasy staršího data (z předcházejících sezón). 

|   MatchID |   Sea | Date       |   LID |   HID |   AID |   OddsH |   OddsD |   OddsA |   HSC |   ASC |   H |   D |   A |     BetH |     BetD |     BetA |
|----------:|------:|:-----------|------:|------:|------:|--------:|--------:|--------:|------:|------:|----:|----:|----:|---------:|---------:|---------:|
|     27433 |  2003 | 2003-09-13 |     A1 |    48 |    35 |    2.28 |    3.82 |    3.34 |     1 |     0 |   1 |   0 |   0 | 0 | 0 | 0 |
|     27431 |  2003 | 2003-09-13 |     A1 |    46 |    28 |    2.65 |    3.76 |    2.8  |     3 |     1 |   1 |   0 |   0 | 0 | 0 | 0 |
|     27429 |  2003 | 2003-09-13 |     A1 |    42 |    14 |    1.48 |    5.12 |    7.67 |     2 |     1 |   1 |   0 |   0 | 0 | 0 | 0 |
|     27428 |  2003 | 2003-09-13 |     A1 |    36 |    13 |    1.98 |    4.00 |    4.09 |     0 |     2 |   0 |   0 |   1 | 0 | 0 | 0 |
|     27426 |  2003 | 2003-09-13 |     A1 |    30 |     8 |    1.86 |    4.13 |    4.56 |     2 |     0 |   1 |   0 |   0 | 0   | 0 | 0 |

- MatchID - Unikátní identifikátor zápasu (MatchID je index DataFramu)
- Date - Den kdy bude zápas odehrán 
- LID - Unikátní identifikátor ligy
- HID - Unikátní identifikátor domácího týmu
- AID - Unikátní identifikátor týmu hostí
- OddsH/D/A - Bookmakerovy kurzy pro daný výsledek
- HSC - Výsledné skóre domácích
- ASC - Výsledné skóre hostí
- H/D/A - Binární idikátor výhry domácích/remízy/prohry domácích
- BetH/D/A - Celkový objem vašich sázek na daný výsledek

### DataFrame sázkařských příležitostí

Sázkařské příležitosti obsahují zápasy hrané v nadcházejících dnech. Příležitosti jsou platné do data konání zápasu (včetně). Je tedy možné vsadit na dannou příležitost vícekrát.

|   MatchID |   Sea | Date       |   LID |   HID |   AID |   OddsH |   OddsD |   OddsA |     BetH |     BetD |     BetA |
|----------:|------:|:-----------|------:|------:|------:|--------:|--------:|--------:|---------:|---------:|---------:|
|     27435 |  2003 | 2003-09-16 |     A1 |     8 |    31 |    3.56 |    3.88 |    2.17 | 0 | 0 | 0 |
|     27444 |  2003 | 2003-09-16 |     A1 |    41 |    42 |    6.5  |    4.76 |    1.57 | 0 | 0 | 0 |
|     27437 |  2003 | 2003-09-16 |     A1 |    14 |     6 |    1.77 |    4.26 |    4.96 | 0 | 0 | 0 |
|     27438 |  2003 | 2003-09-16 |     A1 |    18 |    30 |    2.8  |    3.77 |    2.65 | 0 | 0 | 0 |
|     27439 |  2003 | 2003-09-16 |     A1 |    21 |    45 |    1.8  |    4.22 |    4.83 | 0 | 0 | 0 |

### DataFrame sázek

Tento DataFrame očekáváme jako vaší odpověď. I pokud nechcete pokládat žádné sázky, musíte poslat (alespoň prázdný) DataFrame.

|   MatchID |     BetH |     BetD |     BetA |
|----------:|---------:|---------:|---------:|
|     27435 | 5.5 | 0 | 0 |
|     27444 | 0 | 15 | 21.7 |
|     27437 | 23.7 | 0 | 0 |
|     27438 | 0 | 0 | 0 |
|     27439 | 0 | 0 | 7.91 |

### Technické náležitosti

- Veškerá data kolující mezi vaším modelem a bookmakerem jsou uložená v pandas.DataFrame.
- Komunikace mezi vámi a bookmakerem probíhá přes std in/out, avšak nemusíte se ničeho obávat, serializaci jsme vyřešili za vás.
- Pokud bookmakerovi pošlete sázky na jiné příležitosti, než které vám přisly, budou ignorovány.
- Pokud nebudete mít dostatek prostředků pro vaše sázky, budou ignorovány.
- Sázky > max_bet a sázky < min_bet budou ignorovány.
