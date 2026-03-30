# Phase 3: Artifact Classification Findings

Corpus: 37886 tokens, 8148 types

## 3.1 Anomaly Classification

### Token and type counts by category

| Category | Tokens | % | Types | % |
|----------|-------:|--:|------:|--:|
| consistent | 28128 | 74.2% | 1529 | 18.8% |
| slot4_violation | 213 | 0.6% | 73 | 0.9% |
| fallback_only | 3869 | 10.2% | 901 | 11.1% |
| repetition_artifact | 31 | 0.1% | 8 | 0.1% |
| hapax | 5645 | 14.9% | 5645 | 69.3% |

### Top 20 words: slot4_violation

| Word | Count |
|------|------:|
| qokechy | 13 |
| choaiin | 7 |
| qokeechy | 6 |
| okechy | 6 |
| cheoar | 5 |
| shchy | 5 |
| otechdy | 5 |
| shoaiin | 4 |
| kechy | 4 |
| chochy | 4 |
| soaiin | 4 |
| kechdy | 4 |
| okechdy | 4 |
| otechy | 4 |
| qokechedy | 4 |
| okechedy | 4 |
| koaiin | 3 |
| doaiin | 3 |
| ykeechy | 3 |
| okeshy | 3 |

### Top 20 words: fallback_only

| Word | Count |
|------|------:|
| cheky | 65 |
| odaiin | 60 |
| checkhy | 47 |
| chodaiin | 44 |
| qodaiin | 42 |
| choky | 39 |
| choty | 37 |
| sheky | 36 |
| sheckhy | 35 |
| chedaiin | 32 |
| chedar | 30 |
| checthy | 28 |
| ary | 26 |
| chety | 25 |
| odar | 24 |
| cheeky | 24 |
| dary | 24 |
| chedal | 24 |
| okaly | 24 |
| shodaiin | 23 |

### Top 20 words: repetition_artifact

| Word | Count |
|------|------:|
| qokedy | 7 |
| chol | 6 |
| okaiin | 3 |
| ol | 3 |
| ytaiin | 3 |
| daiin | 3 |
| sheol | 3 |
| qokeedy | 3 |

### Top 20 words: hapax

| Word | Count |
|------|------:|
| fachys | 1 |
| ataiin | 1 |
| cthres | 1 |
| are | 1 |
| syaiir | 1 |
| cthoary | 1 |
| ooiin | 1 |
| roloty | 1 |
| cth?ar | 1 |
| cfhaiin | 1 |
| ydaraishy | 1 |
| oydar | 1 |
| cfhoaiin | 1 |
| shodary | 1 |
| oschy | 1 |
| cphesaiin | 1 |
| cphodales | 1 |
| kshoy | 1 |
| otairin | 1 |
| sckhey | 1 |

## 3.2 Artifact Distribution Analysis

### Anomaly rates by manuscript section

| Section | Tokens | Consistent% | S4-viol% | Fallback% | Repet% | Hapax% | Any-anom% |
|---------|-------:|------------:|---------:|----------:|-------:|-------:|----------:|
| Astronomical | 846 | 52.7% | 1.9% | 14.9% | 0.0% | 30.5% | 47.3% |
| Biological | 6359 | 83.8% | 0.2% | 7.4% | 0.2% | 8.4% | 16.2% |
| Cosmological | 1681 | 67.8% | 0.8% | 11.9% | 0.2% | 19.3% | 32.2% |
| Herbal | 11385 | 74.2% | 0.4% | 10.3% | 0.1% | 15.1% | 25.8% |
| Pharmaceutical | 2567 | 70.7% | 0.5% | 10.2% | 0.1% | 18.5% | 29.3% |
| Stars | 11413 | 74.0% | 0.8% | 10.7% | 0.1% | 14.5% | 26.0% |
| Text | 2306 | 77.1% | 0.4% | 9.1% | 0.0% | 13.4% | 22.9% |
| Zodiac | 1329 | 55.5% | 0.8% | 15.4% | 0.0% | 28.2% | 44.5% |

### Top 15 pages by anomaly rate

| Page | Words | Anom% | S4-viol% | Fallback% | Repet% | Hapax% | Section |
|------|------:|------:|---------:|----------:|-------:|-------:|---------|
| f67v2 | 61 | 59.0% | 3.3% | 4.9% | 0.0% | 50.8% | Cosmological |
| f72v3 | 121 | 57.0% | 0.0% | 14.9% | 0.0% | 42.1% | Zodiac |
| f68r2 | 81 | 56.8% | 4.9% | 14.8% | 0.0% | 37.0% | Astronomical |
| f67v1 | 71 | 56.3% | 2.8% | 18.3% | 0.0% | 35.2% | Astronomical |
| f72v1 | 102 | 52.9% | 0.0% | 14.7% | 0.0% | 38.2% | Zodiac |
| f73r | 96 | 51.0% | 0.0% | 25.0% | 0.0% | 26.0% | Zodiac |
| f72v2 | 110 | 50.9% | 0.0% | 14.5% | 0.0% | 36.4% | Zodiac |
| f68r1 | 65 | 50.8% | 1.5% | 16.9% | 0.0% | 32.3% | Astronomical |
| f67r2 | 176 | 50.0% | 2.3% | 14.2% | 0.0% | 33.5% | Astronomical |
| f67r1 | 155 | 46.5% | 1.3% | 19.4% | 0.0% | 25.8% | Astronomical |
| f58r | 367 | 45.5% | 0.5% | 17.7% | 0.0% | 27.2% | Stars |
| f70v1 | 86 | 45.3% | 3.5% | 12.8% | 0.0% | 29.1% | Zodiac |
| f96v | 61 | 44.3% | 0.0% | 11.5% | 0.0% | 32.8% | Herbal |
| f68v2 | 100 | 44.0% | 1.0% | 17.0% | 0.0% | 26.0% | Astronomical |
| f68v3 | 159 | 43.4% | 0.6% | 15.7% | 0.0% | 27.0% | Cosmological |

### Chi-squared clustering tests

Tests whether anomalous tokens cluster on specific pages vs. uniform distribution.

- **slot4_violation**: chi2=344.0, df=223, p<0.001
- **fallback_only**: chi2=485.7, df=223, p<0.001
- **repetition_artifact**: chi2=572.1, df=223, p<0.001
- **hapax**: chi2=1109.9, df=223, p<0.001

### Correlations

- Page word count vs. anomaly rate: r = -0.2262
- Fallback rate vs. hapax rate: r = 0.2424

## Key Findings

1. **74.2% of tokens are fully consistent** with the 5-slot + B?E*T? model.
2. **25.8% of tokens show some anomaly** (5645 hapax, 3869 fallback-only, 213 slot4 violations, 31 repetition artifacts).
3. **Most anomalous section**: Astronomical (47.3% anomaly rate).
4. **Page-size correlation**: r=-0.2262 — longer pages tend to have lower anomaly rates (more regular text).
5. **Fallback-hapax correlation**: r=0.2424 — fallback and hapax rates are only weakly related across pages.
