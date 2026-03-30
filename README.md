# The Voynich Manuscript as Lossy Generation

Evidence for a combinatorial encoding device from positional slot analysis, synthetic text comparison, and botanical correlation.

## What This Is

Quantitative evidence that the Voynich Manuscript's text was produced by a physical combinatorial generation device -- a lookup table with ~879 row signatures and 7 positional columns. The device encoded real botanical and pharmaceutical knowledge through a constrained combinatorial process, producing text that is structurally valid but semantically degraded -- an effect analogous to hallucination in modern language models.

## Five Convergent Lines of Evidence

1. **Mechanical structure**: 7-slot word decomposition with all slot pairs statistically dependent (chi-squared p < 1e-300, Cramer's V 0.12-0.31)
2. **Default-filler signature**: `ch` in slot 2 shows a 14x frequency spike when adjacent slots are empty (V = 0.48)
3. **Section recovery**: Default rates independently recover manuscript section boundaries (Kruskal-Wallis p = 4e-9)
4. **Computational falsification**: Row-based synthetic generator reproduces real transition statistics with 9-15x less divergence (Jensen-Shannon) than an independent-slot generator, falsifying the Cardan grille hypothesis (Rugg 2004)
5. **Content ablation**: Real text correlates with botanical illustration features (p = 0.003) while synthetic text does not (p_ablation < 0.0001 for all 5 features)

## Quick Start

```bash
# Requirements: Python 3.10+, NumPy
pip install numpy

# Run the full analysis pipeline (see REPRODUCE.md for details)
python scripts/parse_ivtff.py data/IT2a-n.txt        # Parse transcription
python scripts/slot_analysis.py data/IT2a-n.txt       # 7-slot decomposition
python scripts/slot4_decompose.py                      # Slot 4 sub-decomposition
python scripts/table_structure.py data/IT2a-n.txt      # Chi-squared tests
python scripts/default_fragments.py data/IT2a-n.txt    # Default detection
python scripts/bridging_test.py                        # Section recovery
python scripts/row_clustering.py                       # Row signatures
python scripts/eseries_test.py                         # E-series parametric test
python scripts/phase2_replication.py                   # Botanical correlation
python scripts/anomaly_detection.py                    # Anomaly classification
python scripts/synthetic_generator.py                  # GenA vs GenB
python scripts/phase4_2_ablation.py                    # Content ablation
```

See [REPRODUCE.md](REPRODUCE.md) for the complete 18-step reproduction guide.

## Repository Structure

```
scripts/          14 analysis scripts (Python + NumPy only)
analysis/         All findings reports (.md) and data outputs (.json)
data/             EVA transcriptions (Takahashi IT, Zandbergen-Landini ZL)
paper/            LaTeX manuscript targeting Cryptologia
STATUS.md         Complete research status with decision log
REPRODUCE.md      Step-by-step reproduction guide
```

## Key Results

| Claim | Evidence |
|-------|----------|
| 7-slot table structure | 98.2% token coverage, 1.6% of combinatorial space used |
| Row-based generation | GenB 9-15x better than independent on JSD |
| ch-default mechanism | 14x rate spike, V=0.48 (largest effect in analysis) |
| E-series parametric | 74.2% of families show elevated co-occurrence |
| Real content encoding | All 5 botanical features: p_ablation < 0.0001 |
| Cardan grille (Rugg 2004) | Computationally falsified |

## Data Sources

- **Primary transcription**: Takahashi EVA (IT2a-n), IVTFF 2.0 format, from [voynich.nu](http://www.voynich.nu/data/)
- **Cross-validation**: Zandbergen-Landini (ZL3b-n) transcription
- **Manuscript scans**: Yale Beinecke Library IIIF service (downloaded automatically by scripts)
- **Botanical annotations**: AI-assisted annotation of 120 herbal pages (included in `analysis/`)

## Author

**Showerhead** -- @Formershowerhead on YouTube

## Methodology Note

This research was conducted with AI-assisted analysis (Claude, Anthropic). AI tools were used for coding, botanical annotation, and code review. The research program, hypothesis, and all interpretive decisions were human-directed. A systematic code review found three critical bugs, all conservative -- the corrected analysis is stronger than the original. Full disclosure in the paper (Section 2.7).

## License

The analysis code and findings are released for academic use. The EVA transcription data is a community resource maintained at voynich.nu. Manuscript scans are courtesy of the Yale Beinecke Rare Book and Manuscript Library.
