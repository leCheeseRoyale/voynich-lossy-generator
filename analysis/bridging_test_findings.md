# Bridging Test: Default Fragment Rates Across Manuscript Sections

**Question:** Do the mechanical default-filler rates identified in Phase 1
differ across manuscript sections, independently recovering the
section-level vocabulary differences found by Montemurro & Zanette (2013)?

## 1. Pages Ranked by ch-Default Rate

The ch-default rate = proportion of words where slot1 is empty AND slot2 is `ch`.

### Top 15 Pages (highest ch-default rate)
| Rank | Page | Section | ch-Rate | Words |
|------|------|---------|---------|-------|
| 1 | f2v | H (Herbal) | 0.400 | 55 |
| 2 | f16v | H (Herbal) | 0.351 | 57 |
| 3 | f28v | H (Herbal) | 0.339 | 62 |
| 4 | f47v | H (Herbal) | 0.338 | 65 |
| 5 | f27r | H (Herbal) | 0.312 | 77 |
| 6 | f30r | H (Herbal) | 0.312 | 77 |
| 7 | f47r | H (Herbal) | 0.304 | 69 |
| 8 | f8v | H (Herbal) | 0.292 | 96 |
| 9 | f100v | P (Pharmaceutical) | 0.283 | 60 |
| 10 | f95r1 | H (Herbal) | 0.278 | 79 |
| 11 | f20r | H (Herbal) | 0.274 | 62 |
| 12 | f56r | H (Herbal) | 0.270 | 74 |
| 13 | f3r | H (Herbal) | 0.269 | 93 |
| 14 | f88r | P (Pharmaceutical) | 0.267 | 116 |
| 15 | f49r | H (Herbal) | 0.267 | 90 |

### Bottom 15 Pages (lowest ch-default rate)
| Rank | Page | Section | ch-Rate | Words |
|------|------|---------|---------|-------|
| 210 | f86v5 | T (Text-only) | 0.063 | 333 |
| 211 | f48r | H (Herbal) | 0.062 | 65 |
| 212 | f28r | H (Herbal) | 0.061 | 49 |
| 213 | f26r | H (Herbal) | 0.060 | 67 |
| 214 | f99v | P (Pharmaceutical) | 0.059 | 118 |
| 215 | f33r | H (Herbal) | 0.059 | 51 |
| 216 | f67v2 | C (Cosmological) | 0.059 | 34 |
| 217 | f11v | H (Herbal) | 0.050 | 40 |
| 218 | f79v | B (Biological) | 0.044 | 316 |
| 219 | f70v2 | Z (Zodiac) | 0.041 | 97 |
| 220 | f52r | H (Herbal) | 0.037 | 54 |
| 221 | f72v1 | Z (Zodiac) | 0.036 | 56 |
| 222 | f22r | H (Herbal) | 0.035 | 85 |
| 223 | f22v | H (Herbal) | 0.033 | 60 |
| 224 | f57v | C (Cosmological) | 0.000 | 124 |

## 2. Section-Level Default Rate Statistics


### ch-default (S1 empty & S2=ch)

| Section | N pages | Median | IQR | Min | Max |
|---------|---------|--------|-----|-----|-----|
| H (Herbal) | 128 | 0.141 | [0.102, 0.198] | 0.033 | 0.400 |
| S (Stars/Pharma) | 25 | 0.128 | [0.106, 0.150] | 0.070 | 0.215 |
| B (Biological) | 19 | 0.107 | [0.082, 0.125] | 0.044 | 0.183 |
| P (Pharmaceutical) | 16 | 0.177 | [0.101, 0.203] | 0.059 | 0.283 |
| Z (Zodiac) | 12 | 0.100 | [0.075, 0.121] | 0.036 | 0.129 |
| C (Cosmological) | 10 | 0.088 | [0.075, 0.095] | 0.000 | 0.167 |
| A (Astronomical) | 8 | 0.135 | [0.093, 0.146] | 0.066 | 0.174 |
| T (Text-only) | 6 | 0.111 | [0.090, 0.118] | 0.063 | 0.156 |

**Kruskal-Wallis:** H(7) = 30.31, p = 1.41e-05, epsilon-squared = 0.136
  -> Significant difference across sections (p < 0.05)

### slot1 default (o)

| Section | N pages | Median | IQR | Min | Max |
|---------|---------|--------|-----|-----|-----|
| H (Herbal) | 128 | 0.160 | [0.104, 0.231] | 0.022 | 0.434 |
| S (Stars/Pharma) | 25 | 0.257 | [0.198, 0.285] | 0.096 | 0.376 |
| B (Biological) | 19 | 0.241 | [0.173, 0.284] | 0.090 | 0.374 |
| P (Pharmaceutical) | 16 | 0.225 | [0.176, 0.264] | 0.073 | 0.441 |
| Z (Zodiac) | 12 | 0.445 | [0.432, 0.508] | 0.369 | 0.542 |
| C (Cosmological) | 10 | 0.340 | [0.230, 0.378] | 0.198 | 0.438 |
| A (Astronomical) | 8 | 0.318 | [0.270, 0.400] | 0.222 | 0.541 |
| T (Text-only) | 6 | 0.238 | [0.172, 0.286] | 0.149 | 0.315 |

**Kruskal-Wallis:** H(7) = 70.71, p = 7.58e-14, epsilon-squared = 0.317
  -> Significant difference across sections (p < 0.05)

### slot3 default (k)

| Section | N pages | Median | IQR | Min | Max |
|---------|---------|--------|-----|-----|-----|
| H (Herbal) | 128 | 0.178 | [0.128, 0.247] | 0.000 | 0.479 |
| S (Stars/Pharma) | 25 | 0.309 | [0.244, 0.330] | 0.147 | 0.451 |
| B (Biological) | 19 | 0.304 | [0.263, 0.345] | 0.203 | 0.389 |
| P (Pharmaceutical) | 16 | 0.228 | [0.197, 0.283] | 0.147 | 0.424 |
| Z (Zodiac) | 12 | 0.170 | [0.134, 0.204] | 0.093 | 0.354 |
| C (Cosmological) | 10 | 0.198 | [0.147, 0.250] | 0.088 | 0.294 |
| A (Astronomical) | 8 | 0.234 | [0.193, 0.283] | 0.132 | 0.413 |
| T (Text-only) | 6 | 0.228 | [0.210, 0.252] | 0.184 | 0.304 |

**Kruskal-Wallis:** H(7) = 49.79, p = 1.62e-09, epsilon-squared = 0.223
  -> Significant difference across sections (p < 0.05)

### slot4 default (a)

| Section | N pages | Median | IQR | Min | Max |
|---------|---------|--------|-----|-----|-----|
| H (Herbal) | 128 | 0.208 | [0.156, 0.271] | 0.020 | 0.529 |
| S (Stars/Pharma) | 25 | 0.312 | [0.241, 0.390] | 0.205 | 0.494 |
| B (Biological) | 19 | 0.233 | [0.199, 0.263] | 0.157 | 0.355 |
| P (Pharmaceutical) | 16 | 0.157 | [0.115, 0.209] | 0.067 | 0.349 |
| Z (Zodiac) | 12 | 0.280 | [0.209, 0.344] | 0.123 | 0.403 |
| C (Cosmological) | 10 | 0.288 | [0.218, 0.322] | 0.129 | 0.360 |
| A (Astronomical) | 8 | 0.135 | [0.097, 0.217] | 0.054 | 0.363 |
| T (Text-only) | 6 | 0.294 | [0.266, 0.420] | 0.180 | 0.459 |

**Kruskal-Wallis:** H(7) = 38.45, p = 3.29e-07, epsilon-squared = 0.172
  -> Significant difference across sections (p < 0.05)

### slot5 default (y)

| Section | N pages | Median | IQR | Min | Max |
|---------|---------|--------|-----|-----|-----|
| H (Herbal) | 128 | 0.218 | [0.155, 0.287] | 0.047 | 0.587 |
| S (Stars/Pharma) | 25 | 0.171 | [0.161, 0.223] | 0.097 | 0.366 |
| B (Biological) | 19 | 0.208 | [0.160, 0.244] | 0.107 | 0.302 |
| P (Pharmaceutical) | 16 | 0.192 | [0.153, 0.221] | 0.133 | 0.333 |
| Z (Zodiac) | 12 | 0.219 | [0.190, 0.245] | 0.125 | 0.338 |
| C (Cosmological) | 10 | 0.177 | [0.141, 0.239] | 0.056 | 0.337 |
| A (Astronomical) | 8 | 0.235 | [0.190, 0.300] | 0.130 | 0.413 |
| T (Text-only) | 6 | 0.176 | [0.150, 0.222] | 0.131 | 0.250 |

**Kruskal-Wallis:** H(7) = 8.21, p = 3.15e-01, epsilon-squared = 0.037
  -> No significant difference (p >= 0.05)

### Overall default (mean of 5)

| Section | N pages | Median | IQR | Min | Max |
|---------|---------|--------|-----|-----|-----|
| H (Herbal) | 128 | 0.191 | [0.173, 0.217] | 0.112 | 0.304 |
| S (Stars/Pharma) | 25 | 0.235 | [0.216, 0.259] | 0.188 | 0.304 |
| B (Biological) | 19 | 0.216 | [0.198, 0.232] | 0.169 | 0.261 |
| P (Pharmaceutical) | 16 | 0.204 | [0.189, 0.211] | 0.158 | 0.258 |
| Z (Zodiac) | 12 | 0.247 | [0.235, 0.260] | 0.207 | 0.272 |
| C (Cosmological) | 10 | 0.216 | [0.205, 0.230] | 0.116 | 0.265 |
| A (Astronomical) | 8 | 0.218 | [0.208, 0.247] | 0.200 | 0.267 |
| T (Text-only) | 6 | 0.216 | [0.204, 0.238] | 0.169 | 0.256 |

**Kruskal-Wallis:** H(7) = 47.87, p = 4.00e-09, epsilon-squared = 0.215
  -> Significant difference across sections (p < 0.05)

## 3. Pairwise Comparisons: ch-Default Rate

Mann-Whitney U tests with Bonferroni correction.

Number of comparisons: 28, Bonferroni alpha: 0.0018

| Pair | n1 | n2 | Median1 | Median2 | U | z | p | p_bonf | r_rb | Sig? |
|------|----|----|---------|---------|---|---|---|--------|------|------|
| H vs S | 128 | 25 | 0.141 | 0.128 | 1321 | -1.38 | 1.69e-01 | 1.00e+00 | 0.174 | no |
| H vs B | 128 | 19 | 0.141 | 0.107 | 689 | -3.04 | 2.34e-03 | 6.56e-02 | 0.433 | no |
| H vs P | 128 | 16 | 0.141 | 0.177 | 912 | -0.71 | 4.78e-01 | 1.00e+00 | 0.109 | no |
| H vs Z | 128 | 12 | 0.141 | 0.100 | 343 | -3.16 | 1.56e-03 | 4.36e-02 | 0.553 | YES |
| H vs C | 128 | 10 | 0.141 | 0.088 | 282 | -2.94 | 3.24e-03 | 9.07e-02 | 0.560 | no |
| H vs A | 128 | 8 | 0.141 | 0.135 | 386 | -1.16 | 2.46e-01 | 1.00e+00 | 0.245 | no |
| H vs T | 128 | 6 | 0.141 | 0.111 | 221 | -1.75 | 7.95e-02 | 1.00e+00 | 0.424 | no |
| S vs B | 25 | 19 | 0.128 | 0.107 | 149 | -2.10 | 3.60e-02 | 1.00e+00 | 0.373 | no |
| S vs P | 25 | 16 | 0.128 | 0.177 | 143 | -1.52 | 1.28e-01 | 1.00e+00 | 0.285 | no |
| S vs Z | 25 | 12 | 0.128 | 0.100 | 67 | -2.69 | 7.08e-03 | 1.98e-01 | 0.553 | no |
| S vs C | 25 | 10 | 0.128 | 0.088 | 56 | -2.52 | 1.18e-02 | 3.29e-01 | 0.552 | no |
| S vs A | 25 | 8 | 0.128 | 0.135 | 97 | -0.13 | 9.00e-01 | 1.00e+00 | 0.030 | no |
| S vs T | 25 | 6 | 0.128 | 0.111 | 46 | -1.45 | 1.47e-01 | 1.00e+00 | 0.387 | no |
| B vs P | 19 | 16 | 0.107 | 0.177 | 71 | -2.68 | 7.31e-03 | 2.05e-01 | 0.533 | no |
| B vs Z | 19 | 12 | 0.107 | 0.100 | 95 | -0.77 | 4.41e-01 | 1.00e+00 | 0.167 | no |
| B vs C | 19 | 10 | 0.107 | 0.088 | 77 | -0.83 | 4.09e-01 | 1.00e+00 | 0.189 | no |
| B vs A | 19 | 8 | 0.107 | 0.135 | 52 | -1.27 | 2.03e-01 | 1.00e+00 | 0.316 | no |
| B vs T | 19 | 6 | 0.107 | 0.111 | 57 | 0.00 | 1.00e+00 | 1.00e+00 | 0.000 | no |
| P vs Z | 16 | 12 | 0.177 | 0.100 | 36 | -2.79 | 5.35e-03 | 1.50e-01 | 0.625 | no |
| P vs C | 16 | 10 | 0.177 | 0.088 | 26 | -2.85 | 4.43e-03 | 1.24e-01 | 0.675 | no |
| P vs A | 16 | 8 | 0.177 | 0.135 | 38 | -1.62 | 1.05e-01 | 1.00e+00 | 0.414 | no |
| P vs T | 16 | 6 | 0.177 | 0.111 | 25 | -1.70 | 9.00e-02 | 1.00e+00 | 0.479 | no |
| Z vs C | 12 | 10 | 0.100 | 0.088 | 54 | -0.40 | 6.92e-01 | 1.00e+00 | 0.100 | no |
| Z vs A | 12 | 8 | 0.100 | 0.135 | 23 | -1.93 | 5.38e-02 | 1.00e+00 | 0.521 | no |
| Z vs T | 12 | 6 | 0.100 | 0.111 | 31 | -0.47 | 6.40e-01 | 1.00e+00 | 0.139 | no |
| C vs A | 10 | 8 | 0.088 | 0.135 | 22 | -1.55 | 1.20e-01 | 1.00e+00 | 0.438 | no |
| C vs T | 10 | 6 | 0.088 | 0.111 | 21 | -0.98 | 3.29e-01 | 1.00e+00 | 0.300 | no |
| A vs T | 8 | 6 | 0.135 | 0.111 | 16 | -1.03 | 3.02e-01 | 1.00e+00 | 0.333 | no |

## 4. Interpretation

**1 of 28 pairwise comparisons are significant** after Bonferroni correction:

- **Herbal** has significantly higher ch-default rate than **Zodiac** (|r_rb| = 0.553, p_bonf = 4.36e-02)

## 5. Comparison with Montemurro & Zanette (2013)

M&Z found that Voynich vocabulary differs significantly across sections,
using information-theoretic measures (semantic content clustering).
Their key finding: Herbal, Biological, and Pharmaceutical/Stars sections
have distinct vocabulary profiles.

**Section median ch-default rates:**

- P (Pharmaceutical): 0.177
- H (Herbal): 0.141
- A (Astronomical): 0.135
- S (Stars/Pharma): 0.128
- T (Text-only): 0.111
- B (Biological): 0.107
- Z (Zodiac): 0.100
- C (Cosmological): 0.088

**Assessment:** The ch-default rate (a purely structural metric derived from
slot decomposition) is a novel measure independent of vocabulary/semantics.
The Kruskal-Wallis test confirms significant variation (p = 1.41e-05),
independently recovering section-level structural differences that
parallel M&Z's semantic findings. This supports the hypothesis that
sections differ not just in *what* glyphs are used, but in the
*combinatorial structure* -- specifically, the rate at which default
fillers appear. This is consistent with a table-based generator whose
parameters (table contents or selection rules) vary by section.

## 6. Extreme Pages by Section

Pages with unusually high or low ch-default rates within their section.

### H (Herbal) -- 128 pages
Median: 0.141

**Highest:** f2v (0.400, n=55), f16v (0.351, n=57)
**Lowest:** f22v (0.033, n=60), f22r (0.035, n=85)

### S (Stars/Pharma) -- 25 pages
Median: 0.128

**Highest:** f115r (0.215, n=354), f111v (0.200, n=480)
**Lowest:** f105v (0.070, n=287), f58v (0.071, n=269)

### B (Biological) -- 19 pages
Median: 0.107

**Highest:** f83v (0.183, n=224), f77r (0.151, n=279)
**Lowest:** f79v (0.044, n=316), f78v (0.067, n=267)

### P (Pharmaceutical) -- 16 pages
Median: 0.177

**Highest:** f100v (0.283, n=60), f88r (0.267, n=116)
**Lowest:** f99v (0.059, n=118), f102r1 (0.081, n=74)

### Z (Zodiac) -- 12 pages
Median: 0.100

**Highest:** f71v (0.129, n=70), f72r2 (0.125, n=72)
**Lowest:** f72v1 (0.036, n=56), f70v2 (0.041, n=97)

### C (Cosmological) -- 10 pages
Median: 0.088

**Highest:** f69v (0.167, n=102), f70r2 (0.145, n=186)
**Lowest:** f57v (0.000, n=124), f67v2 (0.059, n=34)

### A (Astronomical) -- 8 pages
Median: 0.135

**Highest:** f68r2 (0.174, n=46), f67v1 (0.167, n=36)
**Lowest:** f67r2 (0.066, n=106), f67r1 (0.088, n=91)

### T (Text-only) -- 6 pages
Median: 0.111

**Highest:** f76r (0.156, n=488), f1r (0.118, n=152)
**Lowest:** f86v5 (0.063, n=333), f86v6 (0.085, n=388)

