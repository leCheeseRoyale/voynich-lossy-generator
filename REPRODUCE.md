# Reproducing the Voynich Lossy Generator Analysis

This document walks through every step needed to reproduce the results reported in the paper, from raw transcription data to the final ablation test. All scripts are in `scripts/`, all outputs land in `analysis/`, and the transcription data is in `data/`.

## Prerequisites

- Python 3.10+ (tested on 3.13)
- NumPy (`pip install numpy`)
- No other dependencies. Everything uses Python stdlib + NumPy.

## Data Setup

The two transcription files should already be in `data/`:

```
data/IT2a-n.txt    # Takahashi EVA transcription (primary)
data/ZL3b-n.txt    # Zandbergen-Landini transcription (cross-validation)
```

If missing, download from https://www.voynich.nu/data/:

```bash
curl -o data/IT2a-n.txt https://www.voynich.nu/data/IT2a-n.txt
curl -o data/ZL3b-n.txt https://www.voynich.nu/data/ZL3b-n.txt
```

## Step-by-Step Reproduction

All commands assume you are in the `voynich2/` project root.

---

### Phase 1: Reconstruct the Generator

**Step 1 — Parse the transcription and get corpus stats:**

```bash
python scripts/parse_ivtff.py data/IT2a-n.txt
```

Outputs: `data/IT2a-n_words.tsv` (word list with folio provenance), plus corpus statistics printed to stdout (37,886 tokens, 8,148 types, 5,645 hapax).

**Step 2 — Run the 5-slot decomposition (Task 1.1):**

```bash
python scripts/slot_analysis.py data/IT2a-n.txt
```

Outputs: `analysis/slot_fragments.json`, `analysis/transitions_s1_s2.json`, `analysis/transitions_s3_s5.json`. Prints per-slot fragment inventories and transition matrices.

**Step 3 — Decompose Slot 4 into 3 sub-slots (Task 1.1+):**

```bash
python scripts/slot4_decompose.py
```

Outputs: `analysis/slot4_decomposition.json`. Prints the B?E*T? pattern analysis showing 98.2% coverage.

**Step 4 — Test table structure hypothesis (Task 1.2):**

```bash
python scripts/table_structure.py data/IT2a-n.txt
```

Outputs: `analysis/phase1_2_findings_v2.md`. Prints chi-squared independence tests (all p < 1e-300), Monte Carlo comparison, and entropy analysis.

**Step 5 — Detect default fragments (Task 1.3):**

```bash
python scripts/default_fragments.py data/IT2a-n.txt
```

Outputs: `analysis/phase1_3_findings.md`. Prints the ch-default signature (14x ratio, V=0.48) and per-page variation analysis.

---

### Bridging Tests

**Step 6 — Default rates vs manuscript sections:**

```bash
python scripts/bridging_test.py
```

Outputs: `analysis/bridging_test_findings.md`. Prints Kruskal-Wallis tests showing section-level default rate variation (p=4e-9 overall).

**Step 7 — Row signature clustering:**

```bash
python scripts/row_clustering.py
```

Outputs: `analysis/row_clusters.json`, `analysis/row_clustering_findings.md`. Identifies 879 row signatures, shows S4 variation hierarchy and page distribution.

**Step 8 — E-series parametric test:**

```bash
python scripts/eseries_test.py
```

Outputs: `analysis/eseries_findings_v2.md`. Tests E-family co-occurrence (74.2% significant) and within-page ordering (tau=0.05, p<1e-6).

---

### Phase 2: Anchor to Ground Truth

**Step 9 — Build folio-to-image mapping:**

```bash
python scripts/build_folio_map.py
```

Outputs: `data/folio_image_map.json`, `data/pilot_pages.json`. Downloads the IIIF manifest from Yale Beinecke and maps folio labels to image IDs.

**Step 10 — Download herbal page scans:**

This is done automatically by the annotation scripts, but to download manually:

```python
# In Python — downloads 800x800 JPEG for each herbal folio
import json, urllib.request, os, time
with open('data/folio_image_map.json') as f:
    fmap = json.load(f)
os.makedirs('data/scans', exist_ok=True)
for folio, img_id in fmap.items():
    url = f'https://collections.library.yale.edu/iiif/2/{img_id}/full/!800,800/0/default.jpg'
    outpath = f'data/scans/{folio}.jpg'
    if not os.path.exists(outpath):
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            with open(outpath, 'wb') as out:
                out.write(resp.read())
        time.sleep(0.5)  # polite rate limiting
```

**Step 11 — Botanical annotation:**

The annotation JSON files in `analysis/` contain the botanical feature labels for all 120 herbal pages:

- `analysis/annotations_batch1.json` through `annotations_batch4.json` (40 pilot pages)
- `analysis/annotations_extended.json` (80 additional pages)

These were produced by AI-assisted vision annotation of the IIIF scans. To reproduce from scratch, each page image must be inspected and 15 binary features recorded (see the feature definitions in `scripts/phase2_replication.py`). The provided JSON files are the annotations used in the paper.

**Step 12 — Run Phase 2 botanical correlation (pilot):**

```bash
python scripts/phase2_correlate.py
```

Outputs: `analysis/phase2_2_findings.md`, `analysis/phase2_2_results.json`. Tests row-profile and default-rate correlations for the 40 pilot pages.

**Step 13 — Run Phase 2 replication (full 120 pages):**

```bash
python scripts/phase2_replication.py
```

Outputs: `analysis/phase2_replication_findings.md`. Replicates with all annotations: root_bulbous p=0.003, leaf_lobed p=0.019. Also runs the Mantel test (null) and anomaly-rate correlation.

---

### Phase 3: Classify Artifacts

**Step 14 — Anomaly detection and distribution:**

```bash
python scripts/anomaly_detection.py
```

Outputs: `analysis/phase3_findings.md`. Tags all tokens as consistent/hapax/fallback/slot4_violation/repetition. Reports section-level and page-level anomaly rates.

---

### Phase 4: Validate or Kill

**Step 15 — Synthetic generator comparison (Task 4.1):**

```bash
python scripts/synthetic_generator.py
```

Outputs: `analysis/phase4_1_findings_v2.md`. Builds GenA (independent) and GenB (row-based), generates 37,886 tokens from each, compares 12 metrics. Runs 100-corpus bootstrap. GenB wins 8/12, JSD 9-15x better on transitions.

**Step 16 — Content ablation test (Task 4.2):**

```bash
python scripts/phase4_2_ablation.py
```

Outputs: `analysis/phase4_2_findings.md`. Generates 100 synthetic corpora from GenB with page-matched token counts, tests whether synthetic default rates correlate with botanical features. All 5 features: p_ablation < 0.0001 (CONTENT verdict).

---

### Robustness Checks

**Step 17 — Cross-transcription validation:**

```bash
python scripts/cross_transcription.py
```

Outputs: `analysis/cross_transcription_findings.md`. Compares IT vs ZL transcriptions: 62.3% of fallback-hapax have identical readings in both, confirming the phenomenon is real.

**Step 18 — Relaxed parser for fallback hapax:**

```bash
python scripts/relaxed_parser.py
```

Outputs: `analysis/relaxed_parser_findings.md`. Tests four boundary-loosening strategies: suffix extension captures 41.8%, combined 48.6%. The remaining 51.4% are genuinely anomalous.

---

## Expected Runtime

On a modern machine, the entire pipeline runs in under 10 minutes:

| Step | Script | Approximate time |
|------|--------|-----------------|
| 1-5 | Phase 1 (all) | ~15 seconds |
| 6-8 | Bridging tests | ~30 seconds |
| 9-10 | Image download | ~2 minutes (network) |
| 12-13 | Phase 2 | ~20 seconds |
| 14 | Phase 3 | ~10 seconds |
| 15 | Phase 4.1 (with bootstrap) | ~2 minutes |
| 16 | Phase 4.2 (100 synthetic corpora) | ~3 minutes |
| 17-18 | Robustness checks | ~30 seconds |

Step 11 (botanical annotation) is the only manual/semi-manual step. The provided annotation files allow full reproduction without re-annotating.

## Key Output Files

After running all steps, these files contain the paper's key results:

| File | Contains |
|------|----------|
| `analysis/slot_fragments.json` | Fragment inventories per slot |
| `analysis/slot4_decomposition.json` | Sub-slot inventories (B?E*T?) |
| `analysis/row_clusters.json` | 879 row signatures with variants |
| `analysis/phase1_2_findings_v2.md` | Chi-squared tests (corrected) |
| `analysis/phase1_3_findings.md` | Default fragment analysis |
| `analysis/bridging_test_findings.md` | Section-level default rates |
| `analysis/eseries_findings_v2.md` | E-series co-occurrence (corrected) |
| `analysis/phase2_replication_findings.md` | Botanical correlation (n=120) |
| `analysis/phase3_findings.md` | Anomaly classification |
| `analysis/phase4_1_findings_v2.md` | Synthetic generator comparison (corrected) |
| `analysis/phase4_2_findings.md` | Content ablation (decisive result) |
| `analysis/cross_transcription_findings.md` | IT vs ZL comparison |
| `analysis/relaxed_parser_findings.md` | Fallback hapax analysis |

## Verifying Key Claims

To quickly verify the paper's five headline claims:

1. **"All slot pairs dependent, V=0.12-0.31"** — Check `phase1_2_findings_v2.md`, Table: Chi-squared tests
2. **"ch default 14x spike, V=0.48"** — Check `phase1_3_findings.md`, Section 3: Conditional Frequency
3. **"Section recovery p=4e-9"** — Check `bridging_test_findings.md`, Section 2: ch-default Kruskal-Wallis
4. **"GenB 9-15x better on JSD"** — Check `phase4_1_findings_v2.md`, transition divergence rows
5. **"Ablation p<0.0001 all features"** — Check `phase4_2_findings.md`, Results table

## Seed Reproducibility

All randomized analyses use `seed=42` via `numpy.random.default_rng(42)`. Results should be exactly reproducible across runs on the same platform. Minor floating-point differences may occur across different NumPy versions or OS architectures but should not affect any conclusion.
