# Relaxed Parser Analysis: Fallback Hapax Legomena

## 1. Corpus Overview

- Total tokens: 37,886
- Total types: 8,148
- Hapax legomena: 5,645
- Strict-match hapax: 1,601 (28.4% of hapax)
- **Fallback hapax: 4,044 (71.6% of hapax)** -- words appearing once that fail the 5-slot regex

## 2. Failure Categorization

Why do these 4,044 words fail the strict 5-slot regex? Categories are non-exclusive (a word may appear in multiple).

| Category | Count | % of FB Hapax | Examples |
|----------|------:|:-------------:|----------|
| other (no specific pattern) | 2,528 | 62.5% | asa, ddl, apy, aky, oys |
| od/ok boundary overlap | 729 | 18.0% | doky, qoda, yoky, koky, kodl |
| prefix-gallows clash | 263 | 6.5% | qlky, kolky, cholp, echty, chrky |
| ck/ek boundary overlap | 194 | 4.8% | ek, eky, ckey, ocko, ckol |
| doubled gallows | 187 | 4.6% | epchy, tcfhy, akchy, cpchy, tchty |
| uncertain readings (?) | 118 | 2.9% | d?, ?s, o?, ra?, ?hy |
| non-standard EVA glyphs | 98 | 2.4% | dg, gm, ag, vs, vo, xor |
| repeated slot patterns | 33 | 0.8% | qopchedaiin, fchedypaiin |
| too short (1-2 chars) | 12 | 0.3% | q, dg, gm, ek |
| too long (>12 chars) | 12 | 0.3% | shapchedyfeey, chesokeeoteody |

### Analysis of the "other" category

The 2,528 "other" words mostly contain glyph sequences that fall outside all slot definitions. Common patterns include:
- Words using valid EVA glyphs in non-slot positions (e.g., "asa" has 'a' as initial, "mol" has 'm' as initial -- neither is a valid slot1 glyph)
- Words with connective 'd' in unexpected positions
- Words where slot4-like material (e, a, o) appears without preceding gallows

## 3. Relaxation Strategies

Four relaxation strategies were tested against the 4,044 fallback hapax:

1. **Merged onset**: Allow slot2+slot3 as a single complex onset (e.g., "chk"="ch+k", "tch"="t+ch", doubled prefixes like "ll", "lr")
2. **Expanded slot1**: Let slot1 absorb the following consonant (e.g., "ok" as slot1, "ot" as slot1)
3. **Suffix extension**: Allow extra slot4+slot5 material after the primary slot5 (compound-word structure)
4. **d-connector**: Allow optional 'd' glyph between any two adjacent slots

### Results per strategy

| Strategy | Captured | % of FB Hapax |
|----------|--------:|:-------------:|
| merged_onset | 192 | 4.7% |
| expanded_slot1 | 156 | 3.9% |
| suffix_extension | **1,690** | **41.8%** |
| d_connector | 498 | 12.3% |
| Union (individual) | 1,799 | 44.5% |
| **COMBINED (all)** | **1,965** | **48.6%** |

### Interpretation

- **Suffix extension is by far the most productive relaxation** (41.8%). This strongly suggests many fallback hapax are "compound" words -- two slot-sequences concatenated, or words with extra slot4/slot5 material appended. The strict regex fails because it allows only one slot5 terminus.
- **d-connector captures 12.3%**, confirming that 'd' frequently acts as an interstitial connector outside its nominal slot1 position.
- **Merged onset captures 4.7%**, showing doubled prefixes (ll, lr) and gallows+bench clusters (kch, tch) are real but relatively uncommon.
- **Expanded slot1 captures 3.9%**, validating that some slot1+slot3 fusions (ok, ot, of) exist.

### Uncaptured words

- Still uncaptured after all relaxations: **2,079 (51.4%)**
- Of these, 118 contain '?' (uncertain transcription)
- Clean uncaptured: 1,961

Sample clean uncaptured (shortest):
```
  q, dg, gm, ek, ag, oc, vs, vo, co, apy, aky, ylg, qef, xor,
  sai, org, aii, lgl, coy, oqo, dag, ais, qey, ocs, xsl, tco
```

Many of these contain rare/non-standard EVA glyphs (g, x, v, b, w, z) or start with glyphs that are never slot1-initial (a, c alone, m, n, i). These are likely transcription variants, damaged text, or genuinely anomalous tokens.

## 4. Section Distribution

| Section | Tokens | Hapax | FB Hapax | FB/Hapax% | FB/Token% |
|---------|-------:|------:|---------:|----------:|----------:|
| Herbal-A | 846 | 258 | 209 | **81.0%** | **24.7%** |
| Zodiac | 1,329 | 375 | 301 | **80.3%** | **22.6%** |
| Pharmaceutical | 2,567 | 474 | 376 | **79.3%** | **14.6%** |
| Text/Recipes | 2,306 | 309 | 229 | 74.1% | 9.9% |
| Cosmological | 1,681 | 325 | 240 | 73.8% | 14.3% |
| Stars/Astro | 11,413 | 1,652 | 1,156 | 70.0% | 10.1% |
| Herbal-B | 6,359 | 537 | 374 | 69.6% | 5.9% |
| Herbal-A/B | 11,385 | 1,715 | 1,159 | 67.6% | 10.2% |

### Key section observations

- **Herbal-A** has the highest FB/Hapax rate (81.0%) and the highest FB/Token rate (24.7%), despite being a small section. This suggests either more scribal variation or a different "dialect."
- **Zodiac** is similarly anomalous at 80.3% FB/Hapax and 22.6% FB/Token -- the zodiac labels may use different word-formation rules.
- **Pharmaceutical** also runs high (79.3%), possibly reflecting specialized vocabulary.
- **Herbal-A/B** and **Herbal-B** have the lowest FB/Hapax rates (~68-70%), suggesting the most regular word structure in the manuscript.

### Top folios by fallback hapax count

- f58r: 85 (Pharmaceutical)
- f114r: 74
- f105v: 63
- f111r: 54
- f105r: 51
- f107r: 51
- f115v: 51
- f106v: 49
- f66r: 48
- f113r: 48

Folio f58r stands out with 85 fallback hapax -- nearly double the next highest.

## 5. Key Findings

1. **The slot model is fundamentally sound but rigid at boundaries.** The combined relaxation captures 48.6% of fallback hapax, meaning nearly half of "failures" are structurally regular words that merely need flexible slot boundaries.

2. **Suffix extension is the dominant relaxation** (41.8%). Many Voynich words appear to be compounds or have repeated slot4+slot5 tails. This supports the hypothesis that the encoding mechanism can concatenate slot-sequences.

3. **The remaining 51.4% uncaptured words are genuinely anomalous** -- they contain rare EVA glyphs (g, x, v), start with non-standard initials (a, c, m, n), or have glyph combinations that no slot permutation can explain. Many likely represent transcription noise, damaged readings, or marginal annotations.

4. **Section clustering is significant.** Herbal-A, Zodiac, and Pharmaceutical sections have disproportionately high fallback hapax rates (>79%), while Herbal-A/B and Herbal-B are more regular (~68-70%). This pattern aligns with the hypothesis of multiple scribal hands or distinct text registers.

5. **Uncertain readings account for only 2.9%** of fallback hapax -- transcription ambiguity (?) is NOT the main driver of slot-model failure.
