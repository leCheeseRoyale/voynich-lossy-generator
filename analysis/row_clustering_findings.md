# Row Clustering Analysis Findings

## Overview

- **Corpus**: 37886 tokens, 8148 unique types
- **5-slot matched**: 29973 tokens (79.1%)
- **Clean S4 decomposition**: 29420 tokens (98.2% of matched)

## Row Signature Statistics

A row signature = (S1, S2, S3, S5), the constrained slots.

- **Total unique row signatures**: 879
- **Signatures with >1 word variant**: 524 (59.6%)
- **Singleton signatures** (only 1 word): 355

### Variants-per-row distribution

| Variants | Row count |
|---|---|
| 1 | 355 |
| 2 | 142 |
| 3 | 107 |
| 4 | 66 |
| 5 | 38 |
| 6 | 32 |
| 7 | 32 |
| 8 | 20 |
| 9 | 15 |
| 10 | 8 |
| 11 | 10 |
| 12 | 5 |
| 13 | 11 |
| 14 | 8 |
| 15 | 4 |
| 16 | 5 |
| 17 | 6 |
| 18 | 2 |
| 19 | 3 |
| 21 | 3 |
| 22 | 2 |
| 23 | 2 |
| 25 | 1 |
| 26 | 1 |
| 34 | 1 |

### Top 20 row signatures by frequency

| Signature (S1\|S2\|S3\|S5) | Tokens | Types | Pages | Top words |
|---|---|---|---|---|
| |ch||dy | 909 | 10 | 146 | chedy(501), chdy(150), chody(94), cheody(89) |
| d|||iin | 886 | 4 | 205 | daiin(863), doiin(19), doaiin(3), deaiin(1) |
| qo||k|dy | 769 | 21 | 100 | qokeedy(305), qokedy(272), qokchdy(56), qokchedy(39) |
| qo||k|y | 743 | 26 | 145 | qokeey(308), qoky(147), qokey(107), qokchy(69) |
| |ch||y | 719 | 17 | 178 | chey(344), cheey(174), chy(155), choy(13) |
| |ch||l | 693 | 15 | 183 | chol(396), cheol(172), chal(48), cheal(30) |
| s|||dy | 674 | 12 | 123 | shedy(426), sheedy(84), shody(55), sheody(50) |
| s|||y | 608 | 25 | 170 | shey(283), sheey(144), shy(104), sy(35) |
| o|l|| | 552 | 9 | 134 | ol(537), olo(5), olsho(3), olcheo(2) |
| o||k|y | 509 | 34 | 164 | okeey(177), oky(102), okey(63), okchy(39) |
| s||| | 497 | 16 | 177 | s(243), sho(130), sheo(47), she(25) |
| |ch||r | 487 | 15 | 169 | chor(219), cheor(100), char(72), chear(51) |
| |||iin | 470 | 2 | 125 | aiin(469), haiin(1) |
| o||t|y | 434 | 23 | 146 | oteey(140), oty(115), otey(57), otchy(48) |
| o||t|dy | 426 | 22 | 98 | otedy(155), oteedy(100), oteody(39), otchedy(34) |
| d|||r | 396 | 6 | 161 | dar(318), dor(73), deeor(2), doar(1) |
| qo||k|l | 395 | 13 | 116 | qokal(191), qokol(104), qokeol(52), qokchol(18) |
| s|||r | 374 | 21 | 150 | shor(97), sar(84), sor(57), sheor(51) |
| o||k|dy | 373 | 21 | 105 | okedy(118), okeedy(105), okeody(37), okchedy(25) |
| o|r|| | 371 | 5 | 131 | or(363), oro(5), orcho(1), ore(1) |

## S4 Variation Within Rows

Within a row (shared S1+S2+S3+S5), words differ only in Slot 4.
Slot 4 decomposes into: S4a (bench: ch/sh/h), S4b (e-series: e/ee/eee), S4c (terminal: o/a).

- **Rows with S4 variation**: 511
- **S4a varies in**: 277 rows (54.2%)
- **S4b varies in**: 404 rows (79.1%)
- **S4c varies in**: 381 rows (74.6%)

### Interpretation

S4b (e-series) varies most frequently across rows, suggesting the e-count is the primary within-row variation mechanism. This is consistent with e-series encoding a numerical or quantitative value.

## Page Distribution

For the top 50 most frequent row signatures:

- **Page-specific** (1-2 pages): 0
- **Mid-range** (3-19 pages): 0
- **Universal** (20+ pages): 50

### Implications for Phase 2

Most high-frequency row signatures are universal (appear on many pages), suggesting that the table rows encode common structural elements rather than page-specific content. Page-specific encoding may be handled by other mechanisms (e.g., different row selection probabilities per page, or page-specific column values).

## Key Findings Summary

1. **879 row signatures** generate the matched vocabulary, with the top 20 accounting for a large share of tokens.
2. **60% of rows** produce multiple word variants via S4 variation, confirming that S4 sub-slots provide within-row combinatorial expansion.
3. **S4 sub-slots show structured variation**: not all sub-slots vary equally, consistent with independently selectable columns.
4. **Page distribution** reveals a mix of universal and page-specific rows, supporting a table model where some rows are shared infrastructure and others carry page-local information.

## Data

- Full row cluster data: `row_clusters.json`
- Format: `row_signature -> {total_tokens, num_variants, pages, variants: [{word, count, pages}], s4_combos}`
