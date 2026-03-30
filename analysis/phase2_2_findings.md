# Phase 2.2: Row-Frequency Profile Correlation with Botanical Features

**Pages analyzed:** 40
**Row signatures in profile:** 390
**Permutations:** 1000

## Per-Feature Group Separation

| Feature | n_present | n_absent | Within dist | Between dist | Effect | z-score | p-value | Sig? |
|---------|-----------|----------|-------------|-------------|--------|---------|---------|------|
| leaf_smooth | 17 | 23 | 0.6040 | 0.6168 | 0.0128 | 0.60 | 0.2370 |  |
| stem_single | 10 | 30 | 0.6127 | 0.6241 | 0.0114 | 0.42 | 0.2830 |  |
| plant_tall | 35 | 5 | 0.6165 | 0.6273 | 0.0108 | 0.38 | 0.3140 |  |
| root_fibrous | 26 | 14 | 0.6180 | 0.6240 | 0.0060 | 0.28 | 0.3360 |  |
| stem_branching | 30 | 10 | 0.6174 | 0.6241 | 0.0067 | 0.27 | 0.3640 |  |
| plant_rosette | 5 | 35 | 0.5944 | 0.5946 | 0.0002 | 0.02 | 0.4400 |  |
| flower_petals_few | 16 | 24 | 0.6197 | 0.6198 | 0.0001 | 0.04 | 0.4430 |  |
| flower_petals_many | 8 | 32 | 0.6488 | 0.6436 | -0.0052 | -0.16 | 0.5150 |  |
| flower_visible | 31 | 9 | 0.6273 | 0.6124 | -0.0149 | -0.54 | 0.6700 |  |
| root_visible | 37 | 3 | 0.6239 | 0.5946 | -0.0293 | -0.65 | 0.7020 |  |
| leaf_compound | 6 | 34 | 0.6516 | 0.6264 | -0.0252 | -0.64 | 0.7230 |  |
| leaf_lobed | 18 | 22 | 0.6361 | 0.6209 | -0.0152 | -0.62 | 0.7240 |  |
| has_fruit_seed | 4 | 36 | 0.6618 | 0.6033 | -0.0584 | -1.02 | 0.8630 |  |
| root_bulbous | 9 | 31 | 0.6641 | 0.6334 | -0.0308 | -1.04 | 0.8660 |  |
| leaf_serrated | 16 | 24 | 0.6678 | 0.6286 | -0.0392 | -1.62 | 0.9750 |  |

## Mantel Test

Correlation between botanical feature distance and row-profile distance:

- r = 0.0389
- null: 0.0026 +/- 0.0633
- z = 0.57
- p = 0.2660

## No individual features reached significance at p < 0.05


**OVERALL:** The Mantel test did not reach significance (r=0.0389, p=0.2660). The botanical feature distance and row-profile distance are not significantly correlated at this sample size.
