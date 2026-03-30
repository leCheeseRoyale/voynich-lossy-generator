# Phase 1.2: Table Structure Identification (v2 — corrected)

## Bug Fixes Applied

| ID | Issue | Fix |
|----|-------|-----|
| HIGH-1 | Chi-squared included cells with expected < 5 | Mask changed from `expected > 0` to `expected >= 5` |
| HIGH-2 | Degrees of freedom used full table dimensions | df now reflects only rows/cols contributing cells with expected >= 5 |
| HIGH-3 | Cramer's V inflated by bloated chi2 | Fixed by HIGH-1 + using filtered dimensions for V denominator |
| HIGH-7 | Total entropy used `+ 1e-30` epsilon; per-slot used `> 0` filter | Both now use consistent `probs > 0` filter |

## Comparison: Old (v1) vs Corrected (v2)

| Slot Pair | Old Chi2 | New Chi2 | Old df | New df | Old V | New V | Old p | New p |
|-----------|----------|----------|--------|--------|-------|-------|-------|-------|
| slot1 x slot2 (adj) | 13390 | 13390 | 30 | 30 | 0.2989 | 0.2989 | <1e-300 | <1e-300 |
| slot1 x slot3 (non-adj) | 14774 | 14707 | 55 | 40 | 0.3140 | 0.3133 | <1e-300 | <1e-300 |
| slot1 x slot5 (non-adj) | 3316 | 3283 | 80 | 70 | 0.1488 | 0.1480 | <1e-300 | <1e-300 |
| slot2 x slot5 (non-adj) | 7590 | 7556 | 96 | 90 | 0.2054 | 0.2050 | <1e-300 | <1e-300 |
| slot3 x slot5 (semi) | 4392 | 4320 | 176 | 120 | 0.1154 | 0.1342 | <1e-300 | <1e-300 |
| slot3 x slot4 (adj) | 13751 | 10723 | 1694 | 352 | 0.2042 | 0.2115 | <1e-300 | <1e-300 |

**Key observations:**
- **slot1 x slot2**: Unchanged (all 42 cells had expected >= 5).
- **slot3 x slot4**: Largest change — chi2 dropped from 13751 to 10723, df from 1694 to 352. Many cells in the 12x155 matrix had expected < 5. Cramer's V actually *increased* from 0.204 to 0.212 because the denominator shrank more than the numerator.
- **slot3 x slot5**: V increased from 0.115 to 0.134 (same reason — filtered dims tighter).
- **All p-values remain < 1e-300** — the dependencies are overwhelming regardless of fix.
- **All Cramer's V values remain > 0.1** — key conclusion holds.
- **Entropy**: Unchanged at 12.67 bits (no slots had zero-probability fragments in practice).

**Conclusion: The key finding (all slot pairs dependent, Cramer's V > 0.1) is CONFIRMED after correction.** The fixes actually *strengthened* some V values by removing noise from low-expected cells.

---

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
| slot1 x slot3 (non-adj) | 14707 | 40 | <1e-300 | 0.3133 | DEPENDENT |
| slot1 x slot5 (non-adj) | 3283 | 70 | <1e-300 | 0.1480 | DEPENDENT |
| slot2 x slot5 (non-adj) | 7556 | 90 | <1e-300 | 0.2050 | DEPENDENT |
| slot3 x slot5 (semi) | 4320 | 120 | <1e-300 | 0.1342 | DEPENDENT |
| slot3 x slot4 (adj) | 10723 | 352 | <1e-300 | 0.2115 | DEPENDENT |

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
