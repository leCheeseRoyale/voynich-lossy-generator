"""
Phase 4.2: Final Ablation Test
Does real Voynich text correlate with botanical illustrations while
synthetic text from the same generator does not?

Method:
  1. Compute real ch-default rate per herbal page
  2. Build Generator B (row-based): joint row signature sampling + independent S4
  3. For each of 100 synthetic corpora, generate page-matched word counts,
     compute synthetic ch-default rates
  4. For each botanical feature, compare:
     - REAL difference in means (present vs absent)
     - Distribution of SYNTHETIC differences across 100 corpora
  5. p_ablation: fraction of synthetic |diff| >= real |diff|
"""

import json
import os
import re
import sys
from collections import Counter, defaultdict

import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from parse_ivtff import parse_ivtff
from slot_analysis import decompose_word

ANALYSIS_DIR = os.path.join(PROJECT_DIR, "analysis")
DATA_DIR = os.path.join(PROJECT_DIR, "data")
TRANSCRIPTION = os.path.join(DATA_DIR, "IT2a-n.txt")

N_SYNTH = 100
SEED = 42

# The 5 features that were significant in Phase 2 replication
TARGET_FEATURES = [
    "root_bulbous",   # p=0.003
    "root_visible",   # p=0.006
    "leaf_lobed",     # p=0.019
    "leaf_smooth",    # p=0.026 (inverse)
    "leaf_serrated",  # p=0.039
]


# ============================================================
# 1. Load annotations (pilot preferred over extended)
# ============================================================
def load_annotations():
    combined = {}
    for i in range(1, 5):
        path = os.path.join(ANALYSIS_DIR, f"annotations_batch{i}.json")
        if os.path.exists(path):
            with open(path) as f:
                combined.update(json.load(f))
    pilot_pages = set(combined.keys())

    ext_path = os.path.join(ANALYSIS_DIR, "annotations_extended.json")
    if os.path.exists(ext_path):
        with open(ext_path) as f:
            ext = json.load(f)
        for page, feats in ext.items():
            if page not in combined:
                combined[page] = feats

    extended_only = set(combined.keys()) - pilot_pages
    print(f"Annotations: {len(pilot_pages)} pilot + {len(extended_only)} extended = {len(combined)} total")
    return combined


def get_feature_value(ann, feat):
    v = ann.get(feat)
    if v == "?" or v is None:
        return None
    return int(v)


def extract_folio(locus):
    m = re.match(r'^(f\d+[rv]\d?)', locus)
    return m.group(1) if m else None


# ============================================================
# 2. Compute real per-page stats
# ============================================================
def compute_page_stats(words):
    """For each page: word_count, matched_5slot, ch_default_count, ch_default_rate."""
    page_words = defaultdict(list)
    for locus, word in words:
        folio = extract_folio(locus)
        if folio:
            page_words[folio].append(word)

    page_stats = {}
    for folio, wlist in page_words.items():
        total = len(wlist)
        if total == 0:
            continue

        matched_5slot = 0
        ch_default_count = 0

        for w in wlist:
            result = decompose_word(w)
            if result is None or '_fallback' in result:
                continue
            matched_5slot += 1
            s1 = result['slot1']
            s2 = result['slot2']
            if not s1 and s2 == 'ch':
                ch_default_count += 1

        ch_default_rate = ch_default_count / matched_5slot if matched_5slot > 0 else None

        page_stats[folio] = {
            'word_count': total,
            'matched_5slot': matched_5slot,
            'ch_default_count': ch_default_count,
            'ch_default_rate': ch_default_rate,
        }

    return page_stats


# ============================================================
# 3. Build Generator B (row-based)
# ============================================================
def build_generator_b():
    """
    Generator B: sample row signature (S1,S2,S3,S5) from observed joint
    distribution, then sample S4 sub-slots independently.

    Row signatures come from decomposing ALL corpus words (not from row_clusters.json,
    which groups by signature but doesn't give per-word counts conveniently).
    We'll build the distributions directly from the transcription.
    """
    # Load slot4 decomposition for sub-slot marginals
    s4_path = os.path.join(ANALYSIS_DIR, "slot4_decomposition.json")
    with open(s4_path) as f:
        s4_data = json.load(f)

    # Build S4 sub-slot distributions
    s4a_dist = s4_data["sub4a"]  # {fragment: count}
    s4b_dist = s4_data["sub4b"]
    s4c_dist = s4_data["sub4c"]

    def make_dist(d):
        items = list(d.items())
        labels = [k if k != "(empty)" else "" for k, _ in items]
        counts = np.array([v for _, v in items], dtype=float)
        probs = counts / counts.sum()
        return labels, probs

    s4a_labels, s4a_probs = make_dist(s4a_dist)
    s4b_labels, s4b_probs = make_dist(s4b_dist)
    s4c_labels, s4c_probs = make_dist(s4c_dist)

    # Build row signature distribution from corpus
    words = parse_ivtff(TRANSCRIPTION)
    row_sig_counts = Counter()
    for _, word in words:
        result = decompose_word(word)
        if result is None or '_fallback' in result:
            continue
        sig = (
            result['slot1'] or '',
            result['slot2'] or '',
            result['slot3'] or '',
            result['slot5'] or '',
        )
        row_sig_counts[sig] += 1

    row_sigs = list(row_sig_counts.keys())
    row_counts = np.array([row_sig_counts[s] for s in row_sigs], dtype=float)
    row_probs = row_counts / row_counts.sum()

    print(f"Generator B: {len(row_sigs)} unique row signatures, "
          f"{int(row_counts.sum())} total matched words")
    print(f"  S4a: {len(s4a_labels)} options, S4b: {len(s4b_labels)}, S4c: {len(s4c_labels)}")

    return {
        'row_sigs': row_sigs,
        'row_probs': row_probs,
        's4a_labels': s4a_labels, 's4a_probs': s4a_probs,
        's4b_labels': s4b_labels, 's4b_probs': s4b_probs,
        's4c_labels': s4c_labels, 's4c_probs': s4c_probs,
    }


def generate_words(gen, n_words, rng):
    """Generate n_words using Generator B. Returns list of (s1,s2,s3,s4,s5) tuples."""
    # Sample row signatures
    sig_indices = rng.choice(len(gen['row_sigs']), size=n_words, p=gen['row_probs'])

    # Sample S4 sub-slots independently
    s4a_indices = rng.choice(len(gen['s4a_labels']), size=n_words, p=gen['s4a_probs'])
    s4b_indices = rng.choice(len(gen['s4b_labels']), size=n_words, p=gen['s4b_probs'])
    s4c_indices = rng.choice(len(gen['s4c_labels']), size=n_words, p=gen['s4c_probs'])

    words = []
    for i in range(n_words):
        s1, s2, s3, s5 = gen['row_sigs'][sig_indices[i]]
        s4 = gen['s4a_labels'][s4a_indices[i]] + gen['s4b_labels'][s4b_indices[i]] + gen['s4c_labels'][s4c_indices[i]]
        words.append((s1, s2, s3, s4, s5))
    return words


def compute_synth_ch_default_rate(words):
    """
    Compute ch-default rate for synthetic words.
    ch-default = slot1 empty AND slot2 == 'ch'.
    All synthetic words are "5-slot matched" by construction.
    """
    if len(words) == 0:
        return None
    ch_default = sum(1 for s1, s2, s3, s4, s5 in words if s1 == '' and s2 == 'ch')
    return ch_default / len(words)


# ============================================================
# 4. Main analysis
# ============================================================
def main():
    print("=" * 70)
    print("PHASE 4.2: FINAL ABLATION TEST")
    print("=" * 70)

    # Load annotations
    annotations = load_annotations()

    # Parse transcription
    print(f"\nParsing transcription...")
    words = parse_ivtff(TRANSCRIPTION)
    print(f"Total words: {len(words)}")

    # Compute real page stats
    page_stats = compute_page_stats(words)

    # Get herbal pages with both annotations and valid stats
    herbal_pages = sorted([
        p for p in annotations
        if p in page_stats and page_stats[p]['ch_default_rate'] is not None
    ])
    print(f"Herbal pages with annotations and valid stats: {len(herbal_pages)}")

    # Build generator
    print("\nBuilding Generator B...")
    gen = build_generator_b()

    # ---------------------------------------------------------------
    # Generate 100 synthetic corpora
    # ---------------------------------------------------------------
    print(f"\nGenerating {N_SYNTH} synthetic corpora...")
    rng = np.random.default_rng(SEED)

    # For each synthetic corpus, compute ch-default rate per page
    # synth_rates[corpus_idx][page] = rate
    synth_rates = []
    for corpus_idx in range(N_SYNTH):
        page_rates = {}
        for page in herbal_pages:
            n_words = page_stats[page]['word_count']
            synth_words = generate_words(gen, n_words, rng)
            rate = compute_synth_ch_default_rate(synth_words)
            page_rates[page] = rate
        synth_rates.append(page_rates)
        if (corpus_idx + 1) % 20 == 0:
            print(f"  Generated {corpus_idx + 1}/{N_SYNTH} corpora")

    # ---------------------------------------------------------------
    # Compute real and synthetic differences for each feature
    # ---------------------------------------------------------------
    print("\n" + "=" * 70)
    print("ABLATION RESULTS")
    print("=" * 70)

    results = {}
    for feat in TARGET_FEATURES:
        # Split pages into present/absent groups
        present_pages = []
        absent_pages = []
        for p in herbal_pages:
            val = get_feature_value(annotations[p], feat)
            if val is None:
                continue
            if val == 1:
                present_pages.append(p)
            else:
                absent_pages.append(p)

        if len(present_pages) < 3 or len(absent_pages) < 3:
            print(f"\n{feat}: SKIPPED (n_present={len(present_pages)}, n_absent={len(absent_pages)})")
            results[feat] = None
            continue

        # REAL difference
        real_present = np.array([page_stats[p]['ch_default_rate'] for p in present_pages])
        real_absent = np.array([page_stats[p]['ch_default_rate'] for p in absent_pages])
        real_diff = np.mean(real_present) - np.mean(real_absent)

        # SYNTHETIC differences (100 values)
        synth_diffs = []
        for corpus_idx in range(N_SYNTH):
            sp = np.array([synth_rates[corpus_idx][p] for p in present_pages])
            sa = np.array([synth_rates[corpus_idx][p] for p in absent_pages])
            synth_diffs.append(np.mean(sp) - np.mean(sa))
        synth_diffs = np.array(synth_diffs)

        synth_mean = np.mean(synth_diffs)
        synth_std = np.std(synth_diffs)

        # p_ablation: fraction of synthetic |diff| >= real |diff| (two-tailed)
        p_ablation = np.mean(np.abs(synth_diffs) >= np.abs(real_diff))

        # Verdict
        if p_ablation < 0.05:
            verdict = "CONTENT"
        else:
            verdict = "SPURIOUS"

        results[feat] = {
            'n_present': len(present_pages),
            'n_absent': len(absent_pages),
            'real_mean_present': float(np.mean(real_present)),
            'real_mean_absent': float(np.mean(real_absent)),
            'real_diff': float(real_diff),
            'synth_mean_diff': float(synth_mean),
            'synth_std_diff': float(synth_std),
            'synth_min_diff': float(np.min(synth_diffs)),
            'synth_max_diff': float(np.max(synth_diffs)),
            'p_ablation': float(p_ablation),
            'verdict': verdict,
        }

        print(f"\n{feat}:")
        print(f"  Groups: present={len(present_pages)}, absent={len(absent_pages)}")
        print(f"  Real:   mean_present={np.mean(real_present):.4f}, mean_absent={np.mean(real_absent):.4f}")
        print(f"  Real diff:     {real_diff:+.4f}")
        print(f"  Synth diffs:   mean={synth_mean:+.6f}, std={synth_std:.6f}")
        print(f"  Synth range:   [{np.min(synth_diffs):+.4f}, {np.max(synth_diffs):+.4f}]")
        print(f"  p_ablation:    {p_ablation:.4f}")
        print(f"  Verdict:       {verdict}")

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SUMMARY TABLE")
    print("=" * 70)
    print(f"{'Feature':<18s} {'real_diff':>10s} {'synth_mean':>11s} {'synth_std':>10s} {'p_ablation':>11s} {'verdict':>9s}")
    print("-" * 70)
    for feat in TARGET_FEATURES:
        r = results.get(feat)
        if r is None:
            print(f"{feat:<18s} {'SKIPPED':>10s}")
            continue
        print(f"{feat:<18s} {r['real_diff']:>+10.4f} {r['synth_mean_diff']:>+11.6f} "
              f"{r['synth_std_diff']:>10.6f} {r['p_ablation']:>11.4f} {r['verdict']:>9s}")

    # Count verdicts
    content_count = sum(1 for f in TARGET_FEATURES if results.get(f) and results[f]['verdict'] == 'CONTENT')
    spurious_count = sum(1 for f in TARGET_FEATURES if results.get(f) and results[f]['verdict'] == 'SPURIOUS')
    total_tested = content_count + spurious_count

    print(f"\nVerdicts: {content_count}/{total_tested} CONTENT, {spurious_count}/{total_tested} SPURIOUS")

    # ---------------------------------------------------------------
    # Save findings
    # ---------------------------------------------------------------
    save_findings(results, herbal_pages, content_count, spurious_count, total_tested)

    return results


def save_findings(results, herbal_pages, content_count, spurious_count, total_tested):
    out_path = os.path.join(ANALYSIS_DIR, "phase4_2_findings.md")

    lines = []
    lines.append("# Phase 4.2: Final Ablation Test")
    lines.append("")
    lines.append("## Question")
    lines.append("")
    lines.append("Does real Voynich text correlate with botanical illustrations while")
    lines.append("synthetic text from the same generator does not?")
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append("1. Compute real ch-default rate per herbal page (slot1=empty, slot2=ch among 5-slot words)")
    lines.append("2. Build Generator B (row-based): sample row signatures (S1,S2,S3,S5) jointly,")
    lines.append("   then sample S4 sub-slots (S4a,S4b,S4c) independently")
    lines.append("3. For each of 100 synthetic corpora, generate page-matched word counts")
    lines.append("4. For each botanical feature, compute difference in mean ch-default rate")
    lines.append("   between present/absent pages for both real and synthetic text")
    lines.append("5. p_ablation: fraction of synthetic |diff| >= real |diff| (two-tailed)")
    lines.append("")
    lines.append(f"- Herbal pages analyzed: {len(herbal_pages)}")
    lines.append(f"- Synthetic corpora: {N_SYNTH}")
    lines.append(f"- Seed: {SEED}")
    lines.append("")
    lines.append("## Results")
    lines.append("")
    lines.append("| Feature | n_pres | n_abs | real_diff | synth_mean | synth_std | p_ablation | verdict |")
    lines.append("|---------|--------|-------|-----------|------------|-----------|------------|---------|")

    for feat in TARGET_FEATURES:
        r = results.get(feat)
        if r is None:
            lines.append(f"| {feat} | - | - | - | - | - | - | SKIPPED |")
            continue
        lines.append(
            f"| {feat} | {r['n_present']} | {r['n_absent']} | "
            f"{r['real_diff']:+.4f} | {r['synth_mean_diff']:+.6f} | "
            f"{r['synth_std_diff']:.6f} | {r['p_ablation']:.4f} | "
            f"{r['verdict']} |"
        )

    lines.append("")
    lines.append("## Interpretation")
    lines.append("")

    if content_count == total_tested:
        lines.append(f"**All {total_tested} features show CONTENT verdict.** The real botanical correlations")
        lines.append("are NOT reproducible by the generator's statistical properties alone.")
        lines.append("The synthetic text, despite being generated with the same row-signature")
        lines.append("and S4 distributions as the real corpus, does not exhibit the same")
        lines.append("page-level correlations with botanical illustrations.")
        lines.append("")
        lines.append("This is the key positive result: the botanical-text correlation in the")
        lines.append("Voynich manuscript reflects genuine page-level content variation passing")
        lines.append("through the combinatorial encoding mechanism, not a statistical artifact")
        lines.append("of the generation process itself.")
    elif content_count > spurious_count:
        lines.append(f"**{content_count}/{total_tested} features show CONTENT verdict.**")
        lines.append("The majority of botanical correlations are driven by content, not by the")
        lines.append("generator's statistical properties. However, some features may reflect")
        lines.append("spurious correlations that the generator can reproduce by chance.")
        lines.append("")
        content_feats = [f for f in TARGET_FEATURES if results.get(f) and results[f]['verdict'] == 'CONTENT']
        spurious_feats = [f for f in TARGET_FEATURES if results.get(f) and results[f]['verdict'] == 'SPURIOUS']
        lines.append(f"Content-driven: {', '.join(content_feats)}")
        lines.append(f"Potentially spurious: {', '.join(spurious_feats)}")
    elif spurious_count == total_tested:
        lines.append(f"**All {total_tested} features show SPURIOUS verdict.** The generator's")
        lines.append("statistical properties alone can reproduce the real botanical correlations.")
        lines.append("The Phase 2 findings may be artifacts of the generation mechanism rather")
        lines.append("than evidence of content.")
    else:
        lines.append(f"Mixed results: {content_count} CONTENT, {spurious_count} SPURIOUS.")

    lines.append("")
    lines.append("## Ablation Logic")
    lines.append("")
    lines.append("- **CONTENT**: Real diff is significant AND synthetic diffs are NOT as extreme")
    lines.append("  (p_ablation < 0.05). The correlation is driven by page-level content variation,")
    lines.append("  not by the generator mechanism.")
    lines.append("- **SPURIOUS**: Synthetic diffs can match or exceed real diff (p_ablation >= 0.05).")
    lines.append("  The generator mechanism alone can produce correlations this large, so the real")
    lines.append("  correlation may not require a content explanation.")
    lines.append("")

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"\nFindings saved to: {out_path}")


if __name__ == '__main__':
    main()
