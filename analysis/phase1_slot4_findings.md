# Slot 4 Sub-Decomposition Findings

## Result: CONFIRMED COMPOSITE — 3 sub-slots

Slot 4 (154 apparent fragments) decomposes into exactly 3 positional sub-slots:

| Sub-slot | Role | Options | Fill Rate |
|----------|------|---------|-----------|
| Sub4a | Bench | (empty), ch, h, sh | 21% filled |
| Sub4b | E-series | (empty), e, ee, eee, eeee | 37% filled |
| Sub4c | Terminal | (empty), a, o | 52% filled |

## Coverage
- **98.2%** of all slot 4 tokens fit the B?E*T? pattern
- Only 1.8% (553 tokens) violate the expected column order
- The 154 "unique fragments" reduce to 4 x 5 x 3 = 60 theoretical combinations
- Observed: ~46 of 60 possible combinations appear

## Revised Full Table Model (7 slots)

| Slot | Role | Unique | Fill Rate | Top entries |
|------|------|--------|-----------|-------------|
| S1 | Initial | 5+empty | 66% | o, qo, s, d, y |
| S2 | Prefix | 6+empty | 34% | ch, l, r, al, sh, ol |
| S3 | Gallows | 11+empty | 48% | k, t, p, cth, ckh, f |
| S4a | Bench | 3+empty | 21% | ch, h, sh |
| S4b | E-series | 4+empty | 37% | e, ee, eee, eeee |
| S4c | Terminal | 3+empty | 52% | (empty), a, o |
| S5 | Suffix | 16+empty | 88% | y, dy, r, l, iin, in |

Total: 6 x 7 x 12 x 4 x 5 x 3 x 17 = **513,360 theoretical combinations** (independent model)
Observed: **8,148 word types** = **1.6% of theoretical space**

## Column-order violations (the 1.8%)
The fragments that violate B?E*T? order (e.g., EB: "ech", TB: "och", TT: "oa")
represent either:
- Encoding errors (scribe mistakes or uncertain readings)
- Rare alternative access patterns in the generation mechanism
- Evidence that sub4a/sub4b/sub4c aren't perfectly positionally separated

The most common violation is TT ("oa" = 68 tokens), suggesting terminal+terminal
sequences where the table boundary between sub4b and sub4c is fuzzy.

## Implications for Table Hypothesis
With 7 effective slots and observed coverage of 1.6% of theoretical space,
the row-based model predicts approximately:
- If linear (row count = type count): ~8,148 rows (too many for a physical table)
- If row + sub-selection: e.g., 200 rows x ~40 slot4 variants = 8,000 (plausible)
- The low fill rates in S2 (34%) and S4a (21%) suggest many "empty" cells,
  consistent with a sparse table where not all cells are populated.
