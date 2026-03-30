# Phase 4.2: Final Ablation Test

## Question

Does real Voynich text correlate with botanical illustrations while
synthetic text from the same generator does not?

## Method

1. Compute real ch-default rate per herbal page (slot1=empty, slot2=ch among 5-slot words)
2. Build Generator B (row-based): sample row signatures (S1,S2,S3,S5) jointly,
   then sample S4 sub-slots (S4a,S4b,S4c) independently
3. For each of 100 synthetic corpora, generate page-matched word counts
4. For each botanical feature, compute difference in mean ch-default rate
   between present/absent pages for both real and synthetic text
5. p_ablation: fraction of synthetic |diff| >= real |diff| (two-tailed)

- Herbal pages analyzed: 120
- Synthetic corpora: 100
- Seed: 42

## Results

| Feature | n_pres | n_abs | real_diff | synth_mean | synth_std | p_ablation | verdict |
|---------|--------|-------|-----------|------------|-----------|------------|---------|
| root_bulbous | 31 | 89 | -0.0470 | -0.000830 | 0.009571 | 0.0000 | CONTENT |
| root_visible | 104 | 16 | -0.0544 | +0.000462 | 0.010896 | 0.0000 | CONTENT |
| leaf_lobed | 50 | 70 | -0.0315 | -0.000403 | 0.007419 | 0.0000 | CONTENT |
| leaf_smooth | 65 | 55 | +0.0300 | +0.000056 | 0.007654 | 0.0000 | CONTENT |
| leaf_serrated | 47 | 73 | -0.0288 | -0.000449 | 0.008258 | 0.0000 | CONTENT |

## Interpretation

**All 5 features show CONTENT verdict.** The real botanical correlations
are NOT reproducible by the generator's statistical properties alone.
The synthetic text, despite being generated with the same row-signature
and S4 distributions as the real corpus, does not exhibit the same
page-level correlations with botanical illustrations.

This is the key positive result: the botanical-text correlation in the
Voynich manuscript reflects genuine page-level content variation passing
through the combinatorial encoding mechanism, not a statistical artifact
of the generation process itself.

## Ablation Logic

- **CONTENT**: Real diff is significant AND synthetic diffs are NOT as extreme
  (p_ablation < 0.05). The correlation is driven by page-level content variation,
  not by the generator mechanism.
- **SPURIOUS**: Synthetic diffs can match or exceed real diff (p_ablation >= 0.05).
  The generator mechanism alone can produce correlations this large, so the real
  correlation may not require a content explanation.
