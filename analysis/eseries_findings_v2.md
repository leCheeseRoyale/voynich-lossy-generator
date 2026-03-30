# E-Series Parametric Test Findings
**Date**: 2026-03-30
**Corpus**: IT2a-n.txt (37886 tokens, 8148 types, 225 pages)

## Hypothesis
The E-series sub-slot (S4b: empty, e, ee, eee, eeee) encodes a parametric value. If true, words identical except for S4b should co-occur on the same pages at rates higher than chance, representing the same concept with different parameter values.

## E-Family Construction
- Total E-families (2+ members): **630**
- Testable families (2+ members with freq >= 10): **97**

### Top 15 E-families by frequency
| Signature | Members | Total freq |
|-----------|---------|------------|
| d/\_/\_/\_/a/iin | daiin[empty]=863, deaiin[e]=1 | 864 |
| \_/ch/\_/\_/\_/dy | chdy[empty]=150, chedy[e]=501, cheedy[ee]=59 | 710 |
| \_/ch/\_/\_/\_/y | chy[empty]=155, chey[e]=344, cheey[ee]=174, cheeey[eee]=9 | 682 |
| qo/\_/k/\_/\_/y | qoky[empty]=147, qokey[e]=107, qokeey[ee]=308, qokeeey[eee]=26 | 588 |
| qo/\_/k/\_/\_/dy | qokdy[empty]=4, qokedy[e]=272, qokeedy[ee]=305, qokeeedy[eee]=5 | 586 |
| \_/ch/\_/\_/o/l | chol[empty]=396, cheol[e]=172, cheeol[ee]=9 | 577 |
| s/\_/\_/h/\_/dy | shdy[empty]=46, shedy[e]=426, sheedy[ee]=84 | 556 |
| s/\_/\_/h/\_/y | shy[empty]=104, shey[e]=283, sheey[ee]=144, sheeey[eee]=6 | 537 |
| o/\_/k/\_/\_/y | oky[empty]=102, okey[e]=63, okeey[ee]=177, okeeey[eee]=27 | 369 |
| o/r/\_/\_/\_/\_ | or[empty]=363, ore[e]=1 | 364 |
| \_/\_/\_/\_/a/r | ar[empty]=350, ear[e]=2, eear[ee]=1 | 353 |
| \_/ch/\_/\_/o/r | chor[empty]=219, cheor[e]=100, cheeor[ee]=14 | 333 |
| o/\_/t/\_/\_/y | oty[empty]=115, otey[e]=57, oteey[ee]=140, oteeey[eee]=8 | 320 |
| s/\_/\_/h/o/l | shol[empty]=186, sheol[e]=114, sheeol[ee]=14 | 314 |
| qo/\_/k/\_/a/in | qokain[empty]=279, qokeain[e]=3 | 282 |

## Co-occurrence Results
- Families with significant co-occurrence (p < 0.05): **72/97** (74.2%)
- Expected by chance at 5% level: **4.9**
- Median co-occurrence ratio (obs/expected): **3.876**
- Mean co-occurrence ratio: **5.585**

### Interpretation of co-occurrence ratio
- Ratio = 1.0: E-family members co-occur at chance levels
- Ratio > 1.0: E-family members co-occur MORE than chance (supports parametric hypothesis)
- Ratio < 1.0: E-family members co-occur LESS than chance (anti-correlation)

### Per-family results
| Signature | S4b values | Pages | Obs co-occur | Obs rate | Exp rate | Ratio | p-value |
|-----------|-----------|-------|-------------|----------|----------|-------|--------|
| y/\_/k/\_/o/dy | e,ee | 22 | 3 | 0.136 | 0.003 | 43.48 | 0.0010\* |
| y/ch/\_/\_/o/l | mt,e | 20 | 3 | 0.150 | 0.007 | 20.55 | 0.0020\* |
| o/\_/t/\_/o/s | e,ee | 25 | 3 | 0.120 | 0.006 | 20.27 | 0.0030\* |
| \_/ch/\_/\_/o/m | mt,e | 17 | 1 | 0.059 | 0.003 | 18.18 | 0.0559 |
| y/\_/k/\_/o/l | mt,e,ee | 30 | 6 | 0.200 | 0.013 | 14.96 | 0.0010\* |
| y/\_/t/ch/\_/dy | mt,e | 17 | 1 | 0.059 | 0.004 | 14.71 | 0.0679 |
| qo/\_/t/\_/o/dy | mt,e | 18 | 2 | 0.111 | 0.009 | 12.50 | 0.0100\* |
| s/\_/\_/h/a/l | mt,e | 23 | 5 | 0.217 | 0.017 | 12.47 | 0.0010\* |
| o/\_/t/\_/o/\_ | e,ee | 21 | 3 | 0.143 | 0.012 | 12.40 | 0.0010\* |
| \_/\_/cth/\_/o/l | mt,e | 46 | 3 | 0.065 | 0.005 | 11.95 | 0.0020\* |
| \_/l/k/\_/\_/y | mt,ee | 24 | 8 | 0.333 | 0.031 | 10.77 | 0.0010\* |
| o/\_/k/\_/o/\_ | e,ee | 22 | 2 | 0.091 | 0.009 | 10.36 | 0.0150\* |
| qo/\_/\_/\_/\_/dy | mt,ee | 25 | 4 | 0.160 | 0.016 | 9.98 | 0.0020\* |
| y/\_/t/ch/\_/y | mt,e | 27 | 1 | 0.037 | 0.004 | 9.90 | 0.0989 |
| qo/\_/k/\_/o/dy | e,ee | 31 | 4 | 0.129 | 0.013 | 9.71 | 0.0020\* |
| y/\_/t/\_/\_/dy | e,ee | 32 | 7 | 0.219 | 0.024 | 9.22 | 0.0010\* |
| o/\_/t/ch/\_/dy | mt,e | 35 | 11 | 0.314 | 0.035 | 8.99 | 0.0010\* |
| qo/\_/t/ch/\_/dy | mt,e | 27 | 5 | 0.185 | 0.021 | 8.93 | 0.0010\* |
| \_/l/k/\_/\_/dy | e,ee | 29 | 10 | 0.345 | 0.040 | 8.57 | 0.0010\* |
| \_/ch/\_/\_/a/l | mt,e | 33 | 9 | 0.273 | 0.035 | 7.83 | 0.0010\* |
| o/\_/k/\_/o/dy | mt,e,ee | 45 | 13 | 0.289 | 0.038 | 7.57 | 0.0010\* |
| s/\_/\_/h/o/s | mt,e | 23 | 1 | 0.043 | 0.006 | 7.46 | 0.1269 |
| y/\_/k/\_/\_/dy | e,ee | 38 | 9 | 0.237 | 0.032 | 7.29 | 0.0010\* |
| y/\_/t/\_/\_/y | mt,e,ee | 43 | 9 | 0.209 | 0.029 | 7.25 | 0.0010\* |
| \_/\_/k/\_/o/r | mt,e | 31 | 1 | 0.032 | 0.005 | 6.99 | 0.1409 |
| \_/\_/ckh/\_/\_/y | mt,e,ee | 53 | 10 | 0.189 | 0.028 | 6.80 | 0.0010\* |
| qo/\_/p/ch/\_/dy | mt,e | 29 | 6 | 0.207 | 0.031 | 6.62 | 0.0010\* |
| \_/\_/t/\_/\_/y | mt,e,ee | 34 | 5 | 0.147 | 0.022 | 6.55 | 0.0010\* |
| o/\_/t/\_/o/dy | mt,e,ee | 41 | 9 | 0.220 | 0.034 | 6.41 | 0.0010\* |
| d/ch/\_/\_/\_/y | mt,e,ee | 48 | 8 | 0.167 | 0.026 | 6.30 | 0.0010\* |
| \_/sh/ckh/\_/\_/y | mt,e | 36 | 6 | 0.167 | 0.027 | 6.15 | 0.0010\* |
| o/\_/k/ch/\_/dy | mt,e | 33 | 4 | 0.121 | 0.021 | 5.84 | 0.0070\* |
| qo/\_/p/ch/\_/y | mt,e | 19 | 1 | 0.053 | 0.009 | 5.75 | 0.1678 |
| s/\_/\_/h/o/d | mt,e | 20 | 1 | 0.050 | 0.009 | 5.62 | 0.1688 |
| \_/\_/t/ch/\_/y | mt,e | 37 | 3 | 0.081 | 0.015 | 5.54 | 0.0120\* |
| \_/ch/ckh/\_/\_/dy | mt,e | 20 | 1 | 0.050 | 0.009 | 5.38 | 0.1778 |
| \_/\_/p/ch/\_/dy | mt,e | 34 | 5 | 0.147 | 0.029 | 5.08 | 0.0030\* |
| \_/\_/k/\_/\_/dy | e,ee | 44 | 14 | 0.318 | 0.065 | 4.93 | 0.0010\* |
| s/\_/\_/h/\_/\_ | mt,e,ee | 42 | 5 | 0.119 | 0.024 | 4.91 | 0.0040\* |
| \_/l/\_/ch/\_/y | e,ee | 36 | 6 | 0.167 | 0.035 | 4.75 | 0.0010\* |
| o/l/k/\_/\_/dy | e,ee | 37 | 8 | 0.216 | 0.046 | 4.69 | 0.0010\* |
| qo/\_/t/ch/\_/y | mt,e | 57 | 6 | 0.105 | 0.022 | 4.68 | 0.0020\* |
| \_/ch/\_/\_/o/s | mt,e | 48 | 7 | 0.146 | 0.031 | 4.67 | 0.0010\* |
| \_/l/\_/ch/\_/dy | mt,e | 41 | 9 | 0.220 | 0.048 | 4.58 | 0.0010\* |
| s/\_/\_/h/a/r | mt,e | 39 | 6 | 0.154 | 0.035 | 4.40 | 0.0010\* |
| y/sh/\_/\_/\_/y | e,ee | 20 | 1 | 0.050 | 0.012 | 4.22 | 0.2138 |
| o/\_/p/ch/\_/dy | mt,e | 41 | 8 | 0.195 | 0.046 | 4.21 | 0.0010\* |
| \_/\_/t/\_/\_/dy | e,ee | 38 | 4 | 0.105 | 0.026 | 4.12 | 0.0130\* |
| qo/\_/ckh/\_/\_/y | mt,e | 32 | 2 | 0.062 | 0.016 | 3.88 | 0.1019 |
| qo/\_/t/\_/\_/dy | e,ee | 53 | 27 | 0.509 | 0.133 | 3.84 | 0.0010\* |
| o/\_/t/\_/o/r | mt,e | 47 | 3 | 0.064 | 0.019 | 3.43 | 0.0380\* |
| \_/\_/t/ch/\_/dy | mt,e | 36 | 3 | 0.083 | 0.025 | 3.37 | 0.0450\* |
| \_/\_/t/\_/o/l | mt,e | 46 | 4 | 0.087 | 0.026 | 3.35 | 0.0250\* |
| o/l/k/\_/\_/y | mt,e,ee | 41 | 9 | 0.220 | 0.066 | 3.32 | 0.0010\* |
| qo/\_/k/ch/\_/dy | mt,e | 48 | 9 | 0.188 | 0.057 | 3.27 | 0.0010\* |
| \_/\_/k/ch/\_/y | mt,e | 45 | 2 | 0.044 | 0.014 | 3.25 | 0.1199 |
| qo/\_/k/\_/\_/dy | e,ee | 70 | 46 | 0.657 | 0.212 | 3.10 | 0.0010\* |
| \_/ch/\_/\_/\_/s | mt,e,ee | 58 | 14 | 0.241 | 0.079 | 3.05 | 0.0010\* |
| \_/\_/cth/\_/\_/y | mt,e,ee | 95 | 20 | 0.211 | 0.069 | 3.04 | 0.0010\* |
| o/\_/k/\_/\_/dy | e,ee | 71 | 32 | 0.451 | 0.152 | 2.97 | 0.0010\* |
| o/\_/k/\_/o/r | mt,e,ee | 53 | 5 | 0.094 | 0.034 | 2.80 | 0.0200\* |
| o/\_/t/\_/\_/dy | e,ee | 69 | 29 | 0.420 | 0.151 | 2.79 | 0.0010\* |
| o/\_/k/ch/\_/y | mt,e | 56 | 6 | 0.107 | 0.039 | 2.73 | 0.0130\* |
| \_/ch/\_/\_/o/\_ | mt,e,ee | 76 | 23 | 0.303 | 0.112 | 2.71 | 0.0010\* |
| qo/\_/k/\_/o/r | mt,e,ee | 49 | 7 | 0.143 | 0.054 | 2.66 | 0.0050\* |
| \_/ch/\_/\_/a/r | mt,e | 69 | 15 | 0.217 | 0.084 | 2.60 | 0.0010\* |
| y/ch/\_/\_/\_/y | e,ee | 35 | 2 | 0.057 | 0.023 | 2.51 | 0.1918 |
| o/\_/p/ch/\_/y | mt,e | 36 | 2 | 0.056 | 0.024 | 2.34 | 0.2238 |
| \_/\_/k/\_/\_/y | mt,e,ee,eee | 65 | 14 | 0.215 | 0.094 | 2.29 | 0.0010\* |
| s/\_/\_/h/o/dy | mt,e | 68 | 10 | 0.147 | 0.064 | 2.29 | 0.0050\* |
| qo/\_/t/\_/\_/y | mt,e,ee | 75 | 25 | 0.333 | 0.152 | 2.20 | 0.0010\* |
| \_/ch/ckh/\_/\_/y | mt,e | 85 | 17 | 0.200 | 0.092 | 2.16 | 0.0010\* |
| \_/ch/\_/\_/o/dy | mt,e,ee | 96 | 29 | 0.302 | 0.142 | 2.12 | 0.0010\* |
| o/\_/k/\_/o/l | mt,e,ee | 89 | 25 | 0.281 | 0.137 | 2.05 | 0.0010\* |
| qo/\_/k/ch/\_/y | mt,e | 69 | 7 | 0.101 | 0.051 | 2.00 | 0.0519 |
| s/\_/\_/h/\_/dy | mt,e,ee | 88 | 49 | 0.557 | 0.279 | 2.00 | 0.0010\* |
| o/\_/t/ch/\_/y | mt,e | 62 | 5 | 0.081 | 0.041 | 1.95 | 0.0999 |
| o/\_/t/\_/o/l | mt,e | 90 | 17 | 0.189 | 0.097 | 1.95 | 0.0030\* |
| o/l/\_/ch/\_/y | e,ee | 32 | 1 | 0.031 | 0.016 | 1.93 | 0.4316 |
| o/\_/k/\_/a/l | mt,e | 85 | 6 | 0.071 | 0.039 | 1.80 | 0.0699 |
| qo/\_/k/\_/o/l | mt,e,ee | 85 | 17 | 0.200 | 0.116 | 1.73 | 0.0040\* |
| \_/ch/\_/\_/\_/dy | mt,e,ee | 108 | 61 | 0.565 | 0.352 | 1.60 | 0.0010\* |
| \_/\_/k/\_/o/l | mt,e,ee | 61 | 4 | 0.066 | 0.042 | 1.57 | 0.2268 |
| \_/\_/k/ch/\_/dy | mt,e | 32 | 1 | 0.031 | 0.020 | 1.53 | 0.5085 |
| o/\_/t/\_/\_/y | mt,e,ee | 118 | 49 | 0.415 | 0.277 | 1.50 | 0.0010\* |
| s/\_/\_/h/o/\_ | mt,e | 105 | 13 | 0.124 | 0.087 | 1.42 | 0.0779 |
| qo/\_/k/\_/\_/y | mt,e,ee,eee | 117 | 59 | 0.504 | 0.381 | 1.32 | 0.0010\* |
| \_/ch/\_/\_/\_/y | mt,e,ee | 170 | 106 | 0.624 | 0.473 | 1.32 | 0.0010\* |
| s/\_/\_/h/o/r | mt,e | 94 | 12 | 0.128 | 0.098 | 1.30 | 0.1658 |
| qo/\_/t/\_/o/l | mt,e | 43 | 1 | 0.023 | 0.018 | 1.29 | 0.5564 |
| \_/ch/\_/\_/o/r | mt,e,ee | 148 | 41 | 0.277 | 0.222 | 1.25 | 0.0140\* |
| s/\_/\_/h/\_/y | mt,e,ee | 156 | 72 | 0.462 | 0.378 | 1.22 | 0.0020\* |
| \_/ch/\_/\_/o/l | mt,e | 172 | 67 | 0.390 | 0.323 | 1.20 | 0.0020\* |
| o/\_/k/\_/\_/y | mt,e,ee,eee | 138 | 52 | 0.377 | 0.321 | 1.18 | 0.0270\* |
| s/\_/\_/h/o/l | mt,e,ee | 135 | 36 | 0.267 | 0.248 | 1.07 | 0.2927 |
| y/\_/k/\_/\_/y | mt,ee | 60 | 2 | 0.033 | 0.032 | 1.06 | 0.5874 |
| \_/ch/k/\_/\_/y | mt,ee | 28 | 0 | 0.000 | 0.011 | 0.00 | 1.0000 |

### E-series pair analysis
Do certain E-series distance pairs show stronger co-occurrence?

| Pair | N families | Median ratio | % significant |
|------|-----------|-------------|---------------|
| mt/e | 74 | 3.335 | 73.0% |
| e/ee | 48 | 3.074 | 89.6% |
| mt/ee | 33 | 2.289 | 87.9% |
| mt/eee | 3 | 1.325 | 100.0% |
| e/eee | 3 | 1.325 | 100.0% |
| ee/eee | 3 | 1.325 | 100.0% |

## E-Series Ordering Test
On pages where multiple E-series variants co-occur, do they appear in order?

- Total position pairs checked: **28695**
- Concordant (lower E before higher E): **6392**
- Discordant (higher E before lower E): **5784**
- Tied (same rank): **16519**
- Kendall's tau: **0.0499**
- Z-score: **5.510**, p-value: **0.000000**
- Direction: Lower E-values tend to appear BEFORE higher E-values

Per-family tau statistics (71 families with 5+ non-tied pairs):
- Median tau: **0.0321**
- Mean tau: **0.0606**
- Positive (ordered): 44, Negative: 23

## Conclusions
**STRONG SUPPORT** for the parametric hypothesis. E-family members co-occur on the same pages significantly more than chance, suggesting that E-series variants represent parametric modifications of the same base concept.

The ordering test shows a positive tendency (tau=0.0499, p=0.000000), suggesting E-series values may track a sequential or ordered quantity within pages.
