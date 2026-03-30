# Phase 1.3: Default Fragment Detection

**Corpus:** 29973 decomposed word tokens

## 1. Candidate Default Fragments

A 'default' fragment is the most frequent non-empty value in a slot,
hypothesized to be the filler entry selected when no content is encoded.

| Slot | Default | Count | Share (all) | Share (non-empty) | Dominance | Runner-up |
|------|---------|-------|-------------|-------------------|-----------|-----------|
| slot1 | `o` | 6925 | 23.1% | 35.0% | 1.4x | qo(4789) |
| slot2 | `ch` | 4537 | 15.1% | 44.6% | 1.6x | l(2923) |
| slot3 | `k` | 7593 | 25.3% | 52.7% | 1.8x | t(4326) |
| slot4 | `a` | 7872 | 26.3% | 32.1% | 2.6x | o(2998) |
| slot5 | `y` | 6240 | 20.8% | 23.8% | 1.1x | dy(5666) |

**Interpretation:** Slots 1-3 have very strong single dominants (with 'empty' being
the most common overall). Slot 4's `a` at 26% and slot 5's `y` at 21% are the
leading non-empty candidates. Slot 4 is notably diverse (155 unique fragments),
making `a` a plausible default despite its moderate share.

## 2. Positional Constraint

Does each candidate default appear exclusively in its slot, or also elsewhere?

- **slot1** `o`: Also in slot4(2998)
- **slot2** `ch`: Also in slot4(797)
- **slot3** `k`: EXCLUSIVE to this slot
- **slot4** `a`: EXCLUSIVE to this slot
- **slot5** `y`: Also in slot1(1556)

## 3. Conditional Frequency (Adjacency Effects)

If a fragment is a 'default filler', its frequency should increase when
adjacent slots are empty (no content to encode there means more filler).

### slot1 = `o`

| Adjacent Slot | Rate (adj empty) | Rate (adj filled) | Rate Ratio | Chi2 | Cramer's V | Interpretation |
|---------------|------------------|--------------------|-----------:|-----:|-----------:|----------------|
| slot2 | 0.244 | 0.206 | 1.18 | 54.6 | 0.043 | DEFAULT-LIKE: rate rises when neighbor empty |

### slot2 = `ch`

| Adjacent Slot | Rate (adj empty) | Rate (adj filled) | Rate Ratio | Chi2 | Cramer's V | Interpretation |
|---------------|------------------|--------------------|-----------:|-----:|-----------:|----------------|
| slot1 | 0.391 | 0.028 | 14.03 | 6905.2 | 0.480 | DEFAULT-LIKE: rate rises when neighbor empty |
| slot3 | 0.250 | 0.044 | 5.66 | 2476.9 | 0.287 | DEFAULT-LIKE: rate rises when neighbor empty |

### slot3 = `k`

| Adjacent Slot | Rate (adj empty) | Rate (adj filled) | Rate Ratio | Chi2 | Cramer's V | Interpretation |
|---------------|------------------|--------------------|-----------:|-----:|-----------:|----------------|
| slot2 | 0.329 | 0.106 | 3.11 | 1770.2 | 0.243 | DEFAULT-LIKE: rate rises when neighbor empty |
| slot4 | 0.083 | 0.291 | 0.29 | 1016.5 | 0.184 | ANTI-DEFAULT: rate drops when neighbor empty |

### slot4 = `a`

| Adjacent Slot | Rate (adj empty) | Rate (adj filled) | Rate Ratio | Chi2 | Cramer's V | Interpretation |
|---------------|------------------|--------------------|-----------:|-----:|-----------:|----------------|
| slot3 | 0.260 | 0.266 | 0.98 | 1.4 | 0.007 | weak/no effect |
| slot5 | 0.009 | 0.299 | 0.03 | 1415.7 | 0.217 | ANTI-DEFAULT: rate drops when neighbor empty |

### slot5 = `y`

| Adjacent Slot | Rate (adj empty) | Rate (adj filled) | Rate Ratio | Chi2 | Cramer's V | Interpretation |
|---------------|------------------|--------------------|-----------:|-----:|-----------:|----------------|
| slot4 | 0.357 | 0.175 | 2.04 | 894.3 | 0.173 | DEFAULT-LIKE: rate rises when neighbor empty |

## 4. Per-Page Variation

If default rates are uniform across pages, the mechanism is intrinsic.
If they vary, pages may encode different amounts of content.

| Slot | Default | Overall Rate | Page Mean +/- SD | CV | Range | Chi2 | Perm p | Verdict |
|------|---------|-------------|------------------|-----|-------|------|--------|---------|
| slot1 | `o` | 0.231 | 0.222 +/- 0.113 | 0.51 | 0.02-0.54 | 1147.2 | 0.000 | HIGHLY VARIABLE |
| slot2 | `ch` | 0.151 | 0.165 +/- 0.072 | 0.44 | 0.00-0.40 | 779.4 | 0.000 | HIGHLY VARIABLE |
| slot3 | `k` | 0.253 | 0.221 +/- 0.094 | 0.43 | 0.00-0.48 | 947.7 | 0.000 | HIGHLY VARIABLE |
| slot4 | `a` | 0.263 | 0.237 +/- 0.101 | 0.43 | 0.02-0.53 | 1074.5 | 0.000 | HIGHLY VARIABLE |
| slot5 | `y` | 0.208 | 0.219 +/- 0.089 | 0.41 | 0.05-0.59 | 801.9 | 0.000 | HIGHLY VARIABLE |

### Pages with Extreme Default Rates

**slot1 = `o`** (overall rate 0.231):
- High: f68r1(0.54, n=37), f71r(0.54, n=59), f72r1(0.48, n=65), f72r3(0.50, n=110), f72v1(0.54, n=56)

**slot2 = `ch`** (overall rate 0.151):
- High: f16v(0.37, n=57), f20r(0.40, n=62), f27r(0.36, n=77), f28v(0.34, n=62), f2v(0.40, n=55)
- Low: f57v(0.00, n=124)

**slot3 = `k`** (overall rate 0.253):
- High: f107v(0.45, n=384), f108r(0.43, n=391), f40r(0.42, n=83), f50r(0.48, n=71), f50v(0.44, n=81)
- Low: f20r(0.03, n=62), f4r(0.02, n=54), f96v(0.00, n=44)

**slot4 = `a`** (overall rate 0.263):
- High: f107r(0.45, n=397), f107v(0.45, n=384), f25r(0.45, n=38), f33r(0.53, n=51), f55v(0.49, n=87)
- Low: f90r1(0.02, n=51)

**slot5 = `y`** (overall rate 0.208):
- High: f11v(0.50, n=40), f14v(0.59, n=46), f16v(0.40, n=57), f27r(0.44, n=77), f44r(0.49, n=57)

## 5. Synthesis and Conclusions

### Strongest Default Candidates

1. **Slot 2 `ch`** (15% overall, 45% of non-empty): The most compelling default.
   When slot 1 is empty, `ch` skyrockets to 39% (vs 2.8% when slot1 filled) --
   a 14x rate ratio with Cramer's V=0.48, the largest effect in the entire analysis.
   Similarly, when slot 3 is empty, `ch` rises to 25% (vs 4.4%). This is exactly
   what a default/filler entry would look like: it fills the gap when neighboring
   slots carry no content.

2. **Slot 3 `k`** (25% overall, 53% of non-empty): When slot 2 is empty, `k`
   rises to 33% (vs 11% when slot2 filled), a 3.1x ratio (V=0.24). However, `k`
   shows ANTI-default behavior relative to slot 4: when slot4 is empty, `k` drops
   to 8%. This means `k` and slot4 content tend to co-occur, suggesting `k` may
   encode something rather than being pure filler.

3. **Slot 5 `y`** (21% overall, 24% of non-empty): When slot 4 is empty, `y`
   rises to 36% (vs 18%), a 2x ratio (V=0.17). This is consistent with `y` being
   a default suffix selected when the middle of the word is sparse.

4. **Slot 4 `a`** (26% overall, 32% of non-empty): Despite being the most frequent
   fragment, `a` shows ANTI-default behavior. When slot 5 is empty, `a` drops to
   0.9% (vs 30%), meaning `a` almost never appears without a suffix. This makes
   `a` look like a structural connector (linking gallows to suffixes) rather than
   an independent default.

5. **Slot 1 `o`** (23% overall, 35% of non-empty): Only a weak default signal.
   When slot2 is empty, `o` rises slightly (24% vs 21%), a 1.18x ratio with
   tiny effect size (V=0.04). Not compelling as a default.

### Key Adjacency Findings

The adjacency analysis reveals a striking structural pattern:

- **`ch` is a strong left-side filler** (V=0.48 and 0.29 for its two neighbors).
  It dominates when slot1 and slot3 are both absent, consistent with `ch` being
  the default entry for the "prefix" column of a lookup table.

- **`a` is NOT a default -- it is a structural bridge.** Its near-zero rate when
  slot5 is empty (0.9% vs 30%) means `a` almost obligatorily precedes a suffix.
  In a table model, `a` would be part of the slot4-slot5 compound, not an
  independent filler.

- **`k` has mixed signals**: default-like relative to slot2 (left neighbor) but
  anti-default relative to slot4 (right neighbor). This may indicate that `k`
  serves as a structural anchor that attracts right-side content.

### Per-Page Variation

All five candidate defaults are **HIGHLY VARIABLE** across pages (all p < 0.001
by permutation test). The coefficients of variation range from 0.41 to 0.51,
meaning page-to-page rates fluctuate by roughly half the mean value. This rules
out a purely mechanical/fixed default rate and indicates:

1. Different pages/sections encode different amounts or types of content.
2. The "default rate" may track information density -- pages with more defaults
   could represent sparser source material or more padding.
3. Some folios cluster: f72 pages show high `o` rates, f107 pages show high `k`
   and `a` rates, suggesting section-level encoding differences.

### Mechanism Implications

- **Positional constraint** confirms that slot identities are real: `k` and `a`
  are exclusive to their slots, while `o`, `ch`, and `y` appear in multiple slots
  (but with very different frequencies), consistent with a slotted generator
  where the same glyph has different roles in different positions.

- **The `ch` default pattern is the strongest evidence for table-based generation.**
  A 14x frequency increase when the neighboring slot is empty is hard to explain
  by linguistic mechanisms but follows naturally if `ch` is the "blank" entry in
  a lookup column that gets selected by default.

- **Page-level variation** argues against a single fixed table and in favor of
  either (a) multiple tables for different sections, (b) a table with
  variable "default probability" parameters, or (c) source material that
  varies in density across the manuscript.

