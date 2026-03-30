# Phase 1.2: Table Structure Identification

## 1. Combinatorial Space

| Slot | Fragments (incl. empty) |
|------|------------------------|
| Slot 1 (Initial) | 6 |
| Slot 2 (Prefix) | 7 |
| Slot 3 (Gallows) | 12 |
| Slot 4 (Middle) | 155 |
| Slot 5 (Suffix) | 17 |

- **Theoretical combinatorial space**: 1,328,040 possible words
- **Observed vocabulary** (5-slot matched): 3,203 types
- **Coverage ratio**: 0.002412 (0.2412%)
- **Compression factor**: 415x

The observed vocabulary is a **tiny fraction** (0.2412%) of the
theoretical space. This is consistent with a constrained generation mechanism.

## 2. Can Frequency Weighting Explain the Gap?

Monte Carlo simulation: drawing tokens from independent slot marginals.

- With 37886 draws (full corpus): ~10815 distinct types expected
- Observed: 3203 types

**No** — independent sampling produces more types than observed. The vocabulary is MORE constrained than frequency alone predicts. Structural constraints must exist.

## 3. Chi-Squared Independence Tests

| Slot Pair | Chi² | df | p-value | Cramér's V | Verdict |
|-----------|------|-----|---------|------------|---------|
| slot1 x slot2 (adj) | 13390 | 30 | <1e-300 | 0.2989 | DEPENDENT |
| slot1 x slot3 (non-adj) | 14774 | 55 | <1e-300 | 0.3140 | DEPENDENT |
| slot1 x slot5 (non-adj) | 3316 | 80 | <1e-300 | 0.1488 | DEPENDENT |
| slot2 x slot5 (non-adj) | 7590 | 96 | <1e-300 | 0.2054 | DEPENDENT |
| slot3 x slot5 (semi) | 4392 | 176 | <1e-300 | 0.1154 | DEPENDENT |
| slot3 x slot4 (adj) | 13751 | 1694 | <1e-300 | 0.2042 | DEPENDENT |

**All tested slot pairs show statistically significant dependence** (p < 0.001).
Non-adjacent pairs (which should be independent if slots were free) show dependencies,
consistent with a table where row and column indices link multiple slots simultaneously.

## 4. Observed vs Possible Pair Combinations

- **slot1 x slot2**: 39/42 (93%) used
- **slot1 x slot3**: 54/72 (75%) used
- **slot2 x slot5**: 94/119 (79%) used
- **slot3 x slot5**: 123/204 (60%) used

## 5. Entropy Analysis — Effective Slot Sizes

- **slot1**: 6 fragments, 2.36 bits entropy, effective size = 5.1
- **slot2**: 7 fragments, 1.62 bits entropy, effective size = 3.1
- **slot3**: 12 fragments, 1.88 bits entropy, effective size = 3.7
- **slot4**: 155 fragments, 3.70 bits entropy, effective size = 13.0
- **slot5**: 17 fragments, 3.12 bits entropy, effective size = 8.7

Total marginal entropy: 12.67 bits => effective space of ~6514 combinations.

## 6. Minimum Table Dimensions

| Grouping | Rows | Cols | Max Words | Fill Ratio |
|----------|------|------|-----------|------------|
| [s1 x s2 x s3] x [s4 x s5] | 153 | 521 | 79713 | 4.0% |
| [s1 x s2] x [s3 x s4 x s5] | 39 | 1144 | 44616 | 7.2% |
| Square table | 56 | 57 | 3192 | 100.3% |

The [s1 x s2] x [s3 x s4 x s5] grouping gives 39 x 1144 = 44616 cells
with a fill ratio of 7.2%, suggesting a moderately sparse table.

## 7. GO/NO-GO Assessment

### Indicators

| Criterion | Result | Supports Table? |
|-----------|--------|----------------|
| Compression (obs/theoretical) | 0.2412% | YES |
| Frequency alone explains gap | NO | YES |
| Significant dependencies | 6/6 pairs | YES |
| Strong effect sizes (V>0.1) | 6/6 pairs | YES |

### Verdict: **GO**

The table hypothesis is **viable**. The Voynich vocabulary occupies a tiny, structured subset of the combinatorial space. Slot dependencies — including between non-adjacent slots — are consistent with a lookup table where selecting a row/column index determines multiple slot values simultaneously. The vocabulary size (~3203 types) fits naturally into a table of modest dimensions (~39 x ~1144).

**Next step (Phase 1.3)**: Test whether the specific constraint patterns match known cipher-table structures (Alberti disk, Vigenère tableau, grid cipher).
