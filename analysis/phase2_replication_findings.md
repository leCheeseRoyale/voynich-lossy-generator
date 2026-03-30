# Phase 2 Replication: Botanical Correlation Test (Full Set)

**Date:** 2026-03-30
**Pages analyzed:** 120

## Ch-Default Rate Summary

- Mean: 0.1569
- Median: 0.1446
- Std: 0.0742
- Range: [0.0000, 0.4000]

## Permutation Tests (ch-default rate ~ botanical features)

5000 permutations, seed=42, two-tailed.

| Feature | n_present | n_absent | mean_present | mean_absent | diff | %diff | p-value | sig |
|---------|-----------|----------|-------------|------------|------|-------|---------|-----|
| root_visible | 104 | 16 | 0.1497 | 0.2041 | -0.0544 | -26.7% | 0.0058 | *** |
| root_bulbous | 31 | 89 | 0.1221 | 0.1691 | -0.0470 | -27.8% | 0.0030 | *** |
| root_fibrous | 69 | 49 | 0.1572 | 0.1557 | +0.0015 | +1.0% | 0.9176 |  |
| leaf_serrated | 47 | 73 | 0.1394 | 0.1682 | -0.0288 | -17.1% | 0.0394 | ** |
| leaf_lobed | 50 | 70 | 0.1385 | 0.1701 | -0.0315 | -18.5% | 0.0188 | ** |
| leaf_smooth | 65 | 55 | 0.1707 | 0.1406 | +0.0300 | +21.4% | 0.0256 | ** |
| leaf_compound | 18 | 102 | 0.1566 | 0.1570 | -0.0003 | -0.2% | 0.9864 |  |
| flower_visible | 96 | 20 | 0.1537 | 0.1682 | -0.0145 | -8.6% | 0.4222 |  |
| flower_petals_few | 59 | 51 | 0.1634 | 0.1536 | +0.0098 | +6.4% | 0.4972 |  |
| flower_petals_many | 30 | 82 | 0.1416 | 0.1664 | -0.0248 | -14.9% | 0.1192 |  |
| stem_branching | 69 | 51 | 0.1466 | 0.1709 | -0.0243 | -14.2% | 0.0786 | * |
| stem_single | 51 | 69 | 0.1709 | 0.1466 | +0.0243 | +16.6% | 0.0776 | * |
| plant_tall | 98 | 22 | 0.1520 | 0.1787 | -0.0267 | -14.9% | 0.1252 |  |
| plant_rosette | 26 | 94 | 0.1702 | 0.1532 | +0.0170 | +11.1% | 0.3014 |  |
| has_fruit_seed | 21 | 91 | 0.1458 | 0.1594 | -0.0136 | -8.5% | 0.4658 |  |

## Sign Test (Distinctive Features)

Distinctive features tested: root_bulbous, root_fibrous, leaf_serrated, leaf_lobed, leaf_compound, flower_petals_many, stem_branching, has_fruit_seed

- 7/8 show LOWER defaults when feature is present
- Sign test p-value (two-tailed): **0.0703**

Direction details:

- root_bulbous: LOWER (-0.0470, p=0.0030)
- root_fibrous: HIGHER (+0.0015, p=0.9176)
- leaf_serrated: LOWER (-0.0288, p=0.0394)
- leaf_lobed: LOWER (-0.0315, p=0.0188)
- leaf_compound: LOWER (-0.0003, p=0.9864)
- flower_petals_many: LOWER (-0.0248, p=0.1192)
- stem_branching: LOWER (-0.0243, p=0.0786)
- has_fruit_seed: LOWER (-0.0136, p=0.4658)

## Mantel Test

Botanical feature distance (Hamming) vs row-profile distance (cosine on slot2 frequencies).
1000 permutations, seed=42.

- Mantel r = **0.0345**
- Mantel p = **0.1730**
- Not significant at p<0.05.

## Anomaly Rate Correlation

Testing whether botanical features correlate with anomaly rate 
(proportion of fallback-only or hapax words per page).

| Feature | n_present | n_absent | mean_present | mean_absent | diff | p-value | sig |
|---------|-----------|----------|-------------|------------|------|---------|-----|
| root_visible | 104 | 16 | 0.2536 | 0.2344 | +0.0192 | 0.3348 |  |
| root_bulbous | 31 | 89 | 0.2585 | 0.2484 | +0.0101 | 0.5112 |  |
| root_fibrous | 69 | 49 | 0.2532 | 0.2483 | +0.0050 | 0.7248 |  |
| leaf_serrated | 47 | 73 | 0.2530 | 0.2498 | +0.0032 | 0.8224 |  |
| leaf_lobed | 50 | 70 | 0.2456 | 0.2549 | -0.0093 | 0.4992 |  |
| leaf_smooth | 65 | 55 | 0.2530 | 0.2487 | +0.0043 | 0.7488 |  |
| leaf_compound | 18 | 102 | 0.2643 | 0.2487 | +0.0156 | 0.4112 |  |
| flower_visible | 96 | 20 | 0.2482 | 0.2687 | -0.0204 | 0.2684 |  |
| flower_petals_few | 59 | 51 | 0.2515 | 0.2529 | -0.0013 | 0.9228 |  |
| flower_petals_many | 30 | 82 | 0.2436 | 0.2557 | -0.0121 | 0.4456 |  |
| stem_branching | 69 | 51 | 0.2527 | 0.2488 | +0.0039 | 0.7744 |  |
| stem_single | 51 | 69 | 0.2488 | 0.2527 | -0.0039 | 0.7760 |  |
| plant_tall | 98 | 22 | 0.2577 | 0.2215 | +0.0362 | 0.0406 | ** |
| plant_rosette | 26 | 94 | 0.2308 | 0.2566 | -0.0258 | 0.1182 |  |
| has_fruit_seed | 21 | 91 | 0.2613 | 0.2481 | +0.0132 | 0.4646 |  |

## Comparison to Pilot (40 pages)

Pilot findings (for comparison):
- leaf_lobed: p=0.0064, 32% lower defaults when present
- root_bulbous: p=0.012, 39% lower defaults when present
- 5/5 distinctive features trended lower (sign test p=0.031)

- leaf_lobed: REPLICATED (p=0.0188, diff=-0.0315)
- root_bulbous: REPLICATED (p=0.0030, diff=-0.0470)
- Sign test: NOT replicated (7/8, p=0.0703)

## Interpretation

Significant features (p<0.05): root_visible, root_bulbous, leaf_serrated, leaf_lobed, leaf_smooth
Marginal features (p<0.1): stem_branching, stem_single

The sign test is marginally significant, showing a trend consistent with the pilot.
The pattern of distinctive features having lower defaults persists but is weaker.
