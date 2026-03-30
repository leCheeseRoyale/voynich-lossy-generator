# Phase 1.1 Findings: Slot Decomposition

## Corpus Stats
- 37,886 tokens, 8,148 types (TTR: 0.215)
- 5,645 hapax legomena (69.3% of vocabulary)
- Word length peaks at 5 chars (25.4%), strong unimodal distribution

## 5-Slot Model Coverage
- **79.1%** of tokens match the 5-slot regex decomposition
- 20.9% require fallback (3-slot left/center/right)
- 0% total failures — the regex is too permissive; need to tighten

## Fragment Inventory Per Slot

| Slot | Role | Unique Frags | Fill Rate | Top Fragments |
|------|------|-------------|-----------|---------------|
| S1 | Initial | 5 | 66.0% | o(23%), qo(16%), s(11%), d(11%), y(5%) |
| S2 | Prefix | 6 | 34.0% | ch(15%), l(10%), r(3%), al(3%), sh(2%) |
| S3 | Gallows | 11 | 48.1% | k(25%), t(14%), p(3%), cth(2%), ckh(2%) |
| S4 | Middle | 154 | 81.8% | a(26%), o(10%), e(9%), ee(8%), eo(5%) |
| S5 | Suffix | 16 | 87.6% | y(21%), dy(19%), r(12%), l(12%), iin(11%) |

## Key Observations
1. **Slot 4 has too many fragments (154)** — likely over-segmenting. The "middle"
   slot absorbs too much variation. Needs sub-decomposition or tighter grammar.
2. **Slots 1, 2, 3, 5 are remarkably constrained**: 5, 6, 11, 16 fragments respectively.
   This is consistent with a table with ~5-11 columns.
3. **High empty rates in S1-S3** mean many words skip initial/prefix/gallows slots,
   consistent with a system where some table rows/columns yield empty contributions.
4. **Transition constraints exist**: qo almost never precedes ch/sh in slot2 (only 26/4789),
   while (empty) slot1 strongly associates with ch slot2 (3986/10195). This is NOT
   independent slot selection — there are structural dependencies.
5. **Gallows-suffix transitions**: k and t have similar suffix distributions, but cth/ckh
   strongly prefer 'y' suffix (50-67%). Different gallows types access different suffix
   rows/columns.

## Assessment
The 5-slot model is viable but slot 4 needs refinement. The transition constraints
between slots 1-2 and 3-5 are strong evidence AGAINST independent column selection
and FOR constrained access patterns (grille, linked wheels, or row-based lookup).

**Go/No-Go for Phase 1.2**: GO — sufficient structure to test table hypothesis.
