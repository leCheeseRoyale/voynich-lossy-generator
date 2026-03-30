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
- Families with significant co-occurrence (p < 0.05): **33/97** (34.0%)
- Expected by chance at 5% level: **4.9**
- Median co-occurrence ratio (obs/expected): **1.353**
- Mean co-occurrence ratio: **1.707**

### Interpretation of co-occurrence ratio
- Ratio = 1.0: E-family members co-occur at chance levels
- Ratio > 1.0: E-family members co-occur MORE than chance (supports parametric hypothesis)
- Ratio < 1.0: E-family members co-occur LESS than chance (anti-correlation)

### Per-family results
| Signature | S4b values | Pages | Obs co-occur | Obs rate | Exp rate | Ratio | p-value |
|-----------|-----------|-------|-------------|----------|----------|-------|--------|
| \_/l/k/\_/\_/y | mt,ee | 24 | 8 | 0.333 | 0.060 | 5.57 | 0.0010\* |
| \_/l/k/\_/\_/dy | e,ee | 29 | 10 | 0.345 | 0.073 | 4.73 | 0.0010\* |
| s/\_/\_/h/a/l | mt,e | 23 | 5 | 0.217 | 0.051 | 4.24 | 0.0040\* |
| o/\_/t/ch/\_/dy | mt,e | 35 | 11 | 0.314 | 0.086 | 3.67 | 0.0010\* |
| \_/ch/\_/\_/a/l | mt,e | 33 | 9 | 0.273 | 0.075 | 3.64 | 0.0010\* |
| y/ch/\_/\_/o/l | mt,e | 20 | 3 | 0.150 | 0.043 | 3.47 | 0.0519 |
| qo/\_/t/\_/\_/dy | e,ee | 53 | 27 | 0.509 | 0.152 | 3.35 | 0.0010\* |
| qo/\_/p/ch/\_/dy | mt,e | 29 | 6 | 0.207 | 0.063 | 3.28 | 0.0110\* |
| qo/\_/t/ch/\_/dy | mt,e | 27 | 5 | 0.185 | 0.059 | 3.14 | 0.0170\* |
| y/\_/k/\_/o/dy | e,ee | 22 | 3 | 0.136 | 0.045 | 3.03 | 0.0729 |
| y/\_/t/\_/\_/dy | e,ee | 32 | 7 | 0.219 | 0.072 | 3.02 | 0.0020\* |
| qo/\_/k/\_/\_/dy | e,ee | 70 | 46 | 0.657 | 0.220 | 2.99 | 0.0010\* |
| o/\_/t/\_/o/\_ | e,ee | 21 | 3 | 0.143 | 0.049 | 2.94 | 0.0679 |
| \_/\_/k/\_/\_/dy | e,ee | 44 | 14 | 0.318 | 0.109 | 2.92 | 0.0010\* |
| \_/l/\_/ch/\_/dy | mt,e | 41 | 9 | 0.220 | 0.076 | 2.90 | 0.0030\* |
| qo/\_/t/\_/o/dy | mt,e | 18 | 2 | 0.111 | 0.039 | 2.85 | 0.1459 |
| qo/\_/\_/\_/\_/dy | mt,ee | 25 | 4 | 0.160 | 0.057 | 2.83 | 0.0519 |
| o/\_/t/\_/o/s | e,ee | 25 | 3 | 0.120 | 0.043 | 2.77 | 0.0869 |
| \_/l/\_/ch/\_/y | e,ee | 36 | 6 | 0.167 | 0.061 | 2.74 | 0.0170\* |
| y/\_/k/\_/\_/dy | e,ee | 38 | 9 | 0.237 | 0.087 | 2.73 | 0.0050\* |
| \_/sh/ckh/\_/\_/y | mt,e | 36 | 6 | 0.167 | 0.065 | 2.56 | 0.0210\* |
| o/l/k/\_/\_/dy | e,ee | 37 | 8 | 0.216 | 0.084 | 2.56 | 0.0090\* |
| o/\_/p/ch/\_/dy | mt,e | 41 | 8 | 0.195 | 0.078 | 2.51 | 0.0070\* |
| \_/\_/p/ch/\_/dy | mt,e | 34 | 5 | 0.147 | 0.059 | 2.49 | 0.0460\* |
| y/\_/k/\_/o/l | mt,e,ee | 30 | 6 | 0.200 | 0.086 | 2.32 | 0.0420\* |
| qo/\_/k/\_/o/dy | e,ee | 31 | 4 | 0.129 | 0.056 | 2.30 | 0.0849 |
| o/\_/k/\_/\_/dy | e,ee | 71 | 32 | 0.451 | 0.197 | 2.28 | 0.0010\* |
| o/\_/t/\_/\_/dy | e,ee | 69 | 29 | 0.420 | 0.185 | 2.27 | 0.0010\* |
| o/\_/k/\_/o/dy | mt,e,ee | 45 | 13 | 0.289 | 0.131 | 2.21 | 0.0010\* |
| o/\_/t/\_/o/dy | mt,e,ee | 41 | 9 | 0.220 | 0.112 | 1.97 | 0.0200\* |
| o/\_/k/\_/o/\_ | e,ee | 22 | 2 | 0.091 | 0.047 | 1.95 | 0.2697 |
| s/\_/\_/h/a/r | mt,e | 39 | 6 | 0.154 | 0.079 | 1.95 | 0.0769 |
| o/l/k/\_/\_/y | mt,e,ee | 41 | 9 | 0.220 | 0.114 | 1.92 | 0.0170\* |
| qo/\_/k/ch/\_/dy | mt,e | 48 | 9 | 0.188 | 0.100 | 1.88 | 0.0320\* |
| s/\_/\_/h/\_/dy | mt,e,ee | 88 | 49 | 0.557 | 0.304 | 1.83 | 0.0010\* |
| \_/\_/t/\_/\_/dy | e,ee | 38 | 4 | 0.105 | 0.060 | 1.75 | 0.2038 |
| o/\_/k/ch/\_/dy | mt,e | 33 | 4 | 0.121 | 0.069 | 1.75 | 0.1938 |
| y/\_/t/ch/\_/dy | mt,e | 17 | 1 | 0.059 | 0.034 | 1.71 | 0.4535 |
| \_/ch/\_/\_/o/m | mt,e | 17 | 1 | 0.059 | 0.035 | 1.69 | 0.4466 |
| y/\_/t/\_/\_/y | mt,e,ee | 43 | 9 | 0.209 | 0.126 | 1.66 | 0.0460\* |
| \_/\_/t/\_/\_/y | mt,e,ee | 34 | 5 | 0.147 | 0.094 | 1.56 | 0.2018 |
| qo/\_/t/\_/\_/y | mt,e,ee | 75 | 25 | 0.333 | 0.220 | 1.51 | 0.0050\* |
| \_/ch/\_/\_/\_/dy | mt,e,ee | 108 | 61 | 0.565 | 0.374 | 1.51 | 0.0010\* |
| qo/\_/p/ch/\_/y | mt,e | 19 | 1 | 0.053 | 0.037 | 1.44 | 0.5115 |
| \_/ch/ckh/\_/\_/y | mt,e | 85 | 17 | 0.200 | 0.139 | 1.44 | 0.0410\* |
| \_/ch/\_/\_/\_/s | mt,e,ee | 58 | 14 | 0.241 | 0.169 | 1.42 | 0.0759 |
| \_/ch/\_/\_/a/r | mt,e | 69 | 15 | 0.217 | 0.155 | 1.40 | 0.0879 |
| \_/ch/\_/\_/o/\_ | mt,e,ee | 76 | 23 | 0.303 | 0.222 | 1.36 | 0.0350\* |
| \_/ch/\_/\_/o/s | mt,e | 48 | 7 | 0.146 | 0.108 | 1.35 | 0.2478 |
| \_/\_/ckh/\_/\_/y | mt,e,ee | 53 | 10 | 0.189 | 0.145 | 1.30 | 0.1279 |
| \_/\_/t/ch/\_/dy | mt,e | 36 | 3 | 0.083 | 0.066 | 1.27 | 0.4256 |
| d/ch/\_/\_/\_/y | mt,e,ee | 48 | 8 | 0.167 | 0.132 | 1.26 | 0.2797 |
| \_/\_/cth/\_/o/l | mt,e | 46 | 3 | 0.065 | 0.052 | 1.24 | 0.4386 |
| \_/ch/ckh/\_/\_/dy | mt,e | 20 | 1 | 0.050 | 0.041 | 1.23 | 0.5574 |
| s/\_/\_/h/o/d | mt,e | 20 | 1 | 0.050 | 0.041 | 1.21 | 0.5634 |
| y/sh/\_/\_/\_/y | e,ee | 20 | 1 | 0.050 | 0.042 | 1.20 | 0.5854 |
| qo/\_/t/ch/\_/y | mt,e | 57 | 6 | 0.105 | 0.088 | 1.19 | 0.3806 |
| qo/\_/k/\_/o/r | mt,e,ee | 49 | 7 | 0.143 | 0.120 | 1.19 | 0.3556 |
| \_/ch/\_/\_/o/dy | mt,e,ee | 96 | 29 | 0.302 | 0.257 | 1.17 | 0.1309 |
| o/\_/k/\_/o/l | mt,e,ee | 89 | 25 | 0.281 | 0.239 | 1.17 | 0.1379 |
| o/\_/k/\_/a/l | mt,e | 85 | 6 | 0.071 | 0.060 | 1.17 | 0.4176 |
| qo/\_/k/\_/\_/y | mt,e,ee,eee | 117 | 59 | 0.504 | 0.431 | 1.17 | 0.0180\* |
| \_/ch/\_/\_/\_/y | mt,e,ee | 170 | 106 | 0.624 | 0.539 | 1.16 | 0.0030\* |
| s/\_/\_/h/\_/\_ | mt,e,ee | 42 | 5 | 0.119 | 0.105 | 1.13 | 0.4426 |
| \_/\_/t/\_/o/l | mt,e | 46 | 4 | 0.087 | 0.077 | 1.12 | 0.4875 |
| o/\_/t/\_/\_/y | mt,e,ee | 118 | 49 | 0.415 | 0.370 | 1.12 | 0.0969 |
| \_/\_/k/\_/\_/y | mt,e,ee,eee | 65 | 14 | 0.215 | 0.192 | 1.12 | 0.2987 |
| \_/\_/t/ch/\_/y | mt,e | 37 | 3 | 0.081 | 0.077 | 1.06 | 0.5694 |
| o/\_/t/\_/o/l | mt,e | 90 | 17 | 0.189 | 0.184 | 1.03 | 0.5045 |
| s/\_/\_/h/o/s | mt,e | 23 | 1 | 0.043 | 0.043 | 1.00 | 0.6503 |
| qo/\_/k/\_/o/l | mt,e,ee | 85 | 17 | 0.200 | 0.200 | 1.00 | 0.4925 |
| o/\_/t/\_/o/r | mt,e | 47 | 3 | 0.064 | 0.064 | 0.99 | 0.6004 |
| s/\_/\_/h/\_/y | mt,e,ee | 156 | 72 | 0.462 | 0.465 | 0.99 | 0.5195 |
| \_/ch/\_/\_/o/l | mt,e | 172 | 67 | 0.390 | 0.396 | 0.98 | 0.6573 |
| s/\_/\_/h/o/dy | mt,e | 68 | 10 | 0.147 | 0.150 | 0.98 | 0.5794 |
| qo/\_/ckh/\_/\_/y | mt,e | 32 | 2 | 0.062 | 0.065 | 0.96 | 0.6374 |
| o/\_/k/ch/\_/y | mt,e | 56 | 6 | 0.107 | 0.117 | 0.91 | 0.6603 |
| \_/\_/cth/\_/\_/y | mt,e,ee | 95 | 20 | 0.211 | 0.233 | 0.90 | 0.7223 |
| o/\_/k/\_/\_/y | mt,e,ee,eee | 138 | 52 | 0.377 | 0.418 | 0.90 | 0.8751 |
| qo/\_/k/ch/\_/y | mt,e | 69 | 7 | 0.101 | 0.113 | 0.90 | 0.6913 |
| o/\_/p/ch/\_/y | mt,e | 36 | 2 | 0.056 | 0.067 | 0.83 | 0.7273 |
| s/\_/\_/h/o/l | mt,e,ee | 135 | 36 | 0.267 | 0.324 | 0.82 | 0.9660 |
| y/ch/\_/\_/\_/y | e,ee | 35 | 2 | 0.057 | 0.070 | 0.81 | 0.7123 |
| \_/ch/\_/\_/o/r | mt,e,ee | 148 | 41 | 0.277 | 0.346 | 0.80 | 0.9880 |
| o/\_/k/\_/o/r | mt,e,ee | 53 | 5 | 0.094 | 0.124 | 0.76 | 0.7233 |
| y/\_/t/ch/\_/y | mt,e | 27 | 1 | 0.037 | 0.052 | 0.71 | 0.7612 |
| s/\_/\_/h/o/r | mt,e | 94 | 12 | 0.128 | 0.190 | 0.67 | 0.9770 |
| o/\_/t/ch/\_/y | mt,e | 62 | 5 | 0.081 | 0.121 | 0.67 | 0.8961 |
| s/\_/\_/h/o/\_ | mt,e | 105 | 13 | 0.124 | 0.194 | 0.64 | 0.9900 |
| o/l/\_/ch/\_/y | e,ee | 32 | 1 | 0.031 | 0.051 | 0.62 | 0.8322 |
| \_/\_/k/\_/o/r | mt,e | 31 | 1 | 0.032 | 0.053 | 0.60 | 0.8432 |
| \_/\_/k/ch/\_/y | mt,e | 45 | 2 | 0.044 | 0.087 | 0.51 | 0.9271 |
| \_/\_/k/\_/o/l | mt,e,ee | 61 | 4 | 0.066 | 0.138 | 0.48 | 0.9840 |
| \_/\_/k/ch/\_/dy | mt,e | 32 | 1 | 0.031 | 0.066 | 0.48 | 0.9131 |
| qo/\_/t/\_/o/l | mt,e | 43 | 1 | 0.023 | 0.057 | 0.41 | 0.9371 |
| y/\_/k/\_/\_/y | mt,ee | 60 | 2 | 0.033 | 0.092 | 0.36 | 0.9880 |
| \_/ch/k/\_/\_/y | mt,ee | 28 | 0 | 0.000 | 0.054 | 0.00 | 1.0000 |

### E-series pair analysis
Do certain E-series distance pairs show stronger co-occurrence?

| Pair | N families | Median ratio | % significant |
|------|-----------|-------------|---------------|
| e/ee | 48 | 1.513 | 43.8% |
| mt/e | 74 | 1.203 | 29.7% |
| mt/ee | 33 | 1.175 | 36.4% |
| mt/eee | 3 | 1.120 | 33.3% |
| e/eee | 3 | 1.120 | 33.3% |
| ee/eee | 3 | 1.120 | 33.3% |

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
