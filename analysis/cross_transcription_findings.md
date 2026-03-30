# Cross-Transcription Analysis: IT vs ZL

**Question:** Is the 5-slot decomposition transcription-dependent?
Does the 71.6% hapax-fallback rate in IT reflect transcription noise or real generator behavior?

## 1. Corpus Statistics

| Metric | IT (Takahashi) | ZL (Zandbergen-Landini) |
|--------|---------------|------------------------|
| Total tokens | 37,886 | 35,744 |
| Unique types | 8,148 | 9,207 |
| Hapax legomena | 5,645 (69.3%) | 6,699 (72.8%) |
| Type-token ratio | 0.2151 | 0.2576 |

## 2. Type Overlap

- **Shared types:** 6,519 (60.2% of union)
- **IT-only types:** 1,629 (of which 1577 = 96.8% are IT hapax)
- **ZL-only types:** 2,688 (of which 2617 = 97.4% are ZL hapax)

**Interpretation:** Transcription-unique types are overwhelmingly hapax -- most vocabulary disagreement is in rare words.

## 3. Locus-Level Agreement

- **Shared loci:** 5,205
- **Token agreement rate:** 70.2% (24,995 agree, 10,610 disagree)

## 4. 5-Slot Decomposition Comparison

| Metric | IT | ZL |
|--------|----|----|
| 5-slot match (tokens) | 79.1% | 74.1% |
| Fallback (tokens) | 20.9% | 25.9% |
| 5-slot match (types) | 39.3% | 33.4% |
| Hapax fallback rate | 71.6% | 76.9% |

## 5. Critical Test: IT Hapax-Fallback vs ZL

Of 4044 IT hapax-fallback word types, checked 4044 locus occurrences:

- **ZL missing at locus:** 289
- **Same reading in both:** 2341 (62.3%)
- **Different reading:** 1414 (37.7%)
  - ZL reading NOW parses (5-slot): **586** (41.4% of disagreements)
  - ZL reading still fallback/fail: 828 (58.6%)

**Key finding:** 37.7% of IT hapax-fallback words have a *different* ZL reading. 
Of those disagreements, 41.4% produce a word that parses under the 5-slot model.
This means only ~15.6% of IT hapax-fallback could be 'rescued' by switching transcriptions.

## 6. Consensus Words (Transcription-Robust)

Words where IT and ZL agree at the same locus (24,995 tokens, 5,633 types):

- **5-slot match (tokens):** 79.9%
- **5-slot match (types):** 44.0%
- **Consensus hapax fallback rate:** 68.0%

## 7. Conclusions

1. **Slot match rates differ meaningfully** (IT 79.1% vs ZL 74.1%, delta=5.0pp). Transcription choice affects the model.
2. **Only 62% of IT hapax-fallback words agree in ZL.** Transcription uncertainty is a significant factor.
3. **Hapax fallback rates:** IT=71.6% vs ZL=76.9% (delta=5.2pp).
4. **Consensus words parse at similar rate** (79.9% vs IT-full 79.1%), suggesting transcription disagreement is evenly distributed.
