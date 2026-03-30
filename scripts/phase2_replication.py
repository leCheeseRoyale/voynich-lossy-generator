"""
Phase 2 Replication: Botanical correlation test with full annotation set (~120 herbal pages).

Merges pilot (batch1-4) and extended annotations, computes ch-default rates per page,
and tests correlations with botanical features via permutation tests, sign test,
Mantel test, and anomaly rate analysis.
"""

import json
import os
import re
import sys
import math
from collections import Counter, defaultdict

import numpy as np

# ---------------------------------------------------------------------------
# Add scripts dir to path so we can import parse_ivtff and decompose_word
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from parse_ivtff import parse_ivtff
from slot_analysis import decompose_word, WORD_PATTERN

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
FEATURES = [
    "root_visible", "root_bulbous", "root_fibrous",
    "leaf_serrated", "leaf_lobed", "leaf_smooth", "leaf_compound",
    "flower_visible", "flower_petals_few", "flower_petals_many",
    "stem_branching", "stem_single",
    "plant_tall", "plant_rosette", "has_fruit_seed"
]

DISTINCTIVE_FEATURES = [
    "root_bulbous", "root_fibrous", "leaf_serrated", "leaf_lobed",
    "leaf_compound", "flower_petals_many", "stem_branching", "has_fruit_seed"
]

DATA_DIR = os.path.join(PROJECT_DIR, "data")
ANALYSIS_DIR = os.path.join(PROJECT_DIR, "analysis")
TRANSCRIPTION = os.path.join(DATA_DIR, "IT2a-n.txt")


def load_annotations():
    """Load and merge all annotation files. Pilot batches take priority over extended."""
    combined = {}

    # Load pilot batches first (higher priority)
    for i in range(1, 5):
        path = os.path.join(ANALYSIS_DIR, f"annotations_batch{i}.json")
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
            combined.update(data)

    pilot_pages = set(combined.keys())

    # Load extended, skip duplicates
    ext_path = os.path.join(ANALYSIS_DIR, "annotations_extended.json")
    if os.path.exists(ext_path):
        with open(ext_path) as f:
            ext_data = json.load(f)
        for page, feats in ext_data.items():
            if page not in combined:
                combined[page] = feats

    extended_only = set(combined.keys()) - pilot_pages
    print(f"Loaded annotations: {len(pilot_pages)} pilot + {len(extended_only)} extended = {len(combined)} total")

    return combined


def get_feature_value(ann, feat):
    """Return 1, 0, or None (for '?' uncertain values)."""
    v = ann.get(feat)
    if v == "?" or v is None:
        return None
    return int(v)


def extract_folio(locus):
    """Extract folio id (e.g. 'f1r') from a locus string like 'f1r.3'."""
    m = re.match(r'^(f\d+[rv]\d?)', locus)
    return m.group(1) if m else None


def compute_page_stats(words):
    """
    For each page, compute:
    - ch_default_rate: proportion of 5-slot-matched words with slot1=empty, slot2=ch
    - overall_default_rate: proportion of all 5-slot words that are 'default' pattern
      (slot1=empty, slot2=ch, slot3=empty => the simplest ch-initial pattern)
    - word_count
    - anomaly_rate: proportion of words that are fallback-only or hapax
    """
    # Group words by folio
    page_words = defaultdict(list)
    for locus, word in words:
        folio = extract_folio(locus)
        if folio:
            page_words[folio].append(word)

    # Corpus-wide vocab for hapax detection
    all_words = [w for _, w in words]
    vocab = Counter(all_words)

    page_stats = {}
    for folio, wlist in page_words.items():
        total = len(wlist)
        if total == 0:
            continue

        matched_5slot = 0
        ch_default_count = 0
        fallback_or_hapax = 0

        # Per-page row frequencies (slot2 values for matched words)
        slot2_counts = Counter()

        for w in wlist:
            result = decompose_word(w)
            if result is None:
                fallback_or_hapax += 1
                continue

            if '_fallback' in result:
                fallback_or_hapax += 1
                # Also count hapax among fallback
                continue

            matched_5slot += 1
            s1 = result['slot1']
            s2 = result['slot2']
            s3 = result['slot3']

            slot2_counts[s2 if s2 else '(empty)'] += 1

            # ch-default: slot1 empty, slot2 = ch
            if not s1 and s2 == 'ch':
                ch_default_count += 1

        # Also count hapax among matched words
        for w in wlist:
            if vocab[w] == 1:
                fallback_or_hapax += 1

        # Avoid double-counting: hapax words that are also fallback
        # Recompute more carefully
        fallback_or_hapax = 0
        for w in wlist:
            result = decompose_word(w)
            is_fallback = (result is None) or ('_fallback' in result)
            is_hapax = (vocab[w] == 1)
            if is_fallback or is_hapax:
                fallback_or_hapax += 1

        ch_default_rate = ch_default_count / matched_5slot if matched_5slot > 0 else None
        anomaly_rate = fallback_or_hapax / total if total > 0 else None

        page_stats[folio] = {
            'word_count': total,
            'matched_5slot': matched_5slot,
            'ch_default_count': ch_default_count,
            'ch_default_rate': ch_default_rate,
            'anomaly_rate': anomaly_rate,
            'slot2_counts': dict(slot2_counts),
        }

    return page_stats


def permutation_test(group_present, group_absent, n_perm=5000, seed=42):
    """Two-tailed permutation test for difference in means."""
    rng = np.random.RandomState(seed)

    mean_p = np.mean(group_present)
    mean_a = np.mean(group_absent)
    obs_diff = mean_p - mean_a

    combined = np.concatenate([group_present, group_absent])
    n_p = len(group_present)
    n_total = len(combined)

    count_extreme = 0
    for _ in range(n_perm):
        perm = rng.permutation(n_total)
        perm_p = combined[perm[:n_p]]
        perm_a = combined[perm[n_p:]]
        perm_diff = np.mean(perm_p) - np.mean(perm_a)
        if abs(perm_diff) >= abs(obs_diff):
            count_extreme += 1

    p_value = count_extreme / n_perm
    return mean_p, mean_a, obs_diff, p_value


def sign_test_pvalue(n_lower, n_total):
    """Two-tailed sign test p-value using binomial distribution (exact)."""
    # P(X >= n_lower) under null p=0.5, two-tailed
    from math import comb
    if n_total == 0:
        return 1.0
    # One-tailed: P(X >= n_lower)
    p_one = sum(comb(n_total, k) for k in range(n_lower, n_total + 1)) / (2 ** n_total)
    # Two-tailed
    p_two = min(2 * p_one, 1.0)
    return p_two


def cosine_distance(a, b):
    """Cosine distance between two vectors."""
    dot = np.dot(a, b)
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 1.0
    return 1.0 - dot / (na * nb)


def hamming_distance(a, b):
    """Hamming distance for binary feature vectors."""
    return np.sum(a != b)


def mantel_test(dist_A, dist_B, n_perm=1000, seed=42):
    """Mantel test: correlation between two distance matrices. Returns r, p_value."""
    rng = np.random.RandomState(seed)
    n = dist_A.shape[0]

    # Extract upper triangle
    idx = np.triu_indices(n, k=1)
    a = dist_A[idx]
    b = dist_B[idx]

    obs_r = np.corrcoef(a, b)[0, 1]

    count_extreme = 0
    for _ in range(n_perm):
        perm = rng.permutation(n)
        perm_B = dist_B[np.ix_(perm, perm)]
        perm_b = perm_B[idx]
        perm_r = np.corrcoef(a, perm_b)[0, 1]
        if perm_r >= obs_r:
            count_extreme += 1

    p_value = count_extreme / n_perm
    return obs_r, p_value


def run_analysis():
    """Main analysis pipeline."""
    print("=" * 70)
    print("PHASE 2 REPLICATION: Botanical Correlation Test (Full Set)")
    print("=" * 70)

    # 1. Load and merge annotations
    annotations = load_annotations()

    # 2. Parse transcription and compute page stats
    print(f"\nParsing transcription: {TRANSCRIPTION}")
    words = parse_ivtff(TRANSCRIPTION)
    print(f"Total words parsed: {len(words)}")

    page_stats = compute_page_stats(words)
    print(f"Pages with stats: {len(page_stats)}")

    # Match annotated pages to stats
    matched_pages = []
    for page in sorted(annotations.keys()):
        if page in page_stats and page_stats[page]['ch_default_rate'] is not None:
            matched_pages.append(page)

    print(f"Annotated pages with valid stats: {len(matched_pages)}")

    # Summary of ch-default rates
    rates = [page_stats[p]['ch_default_rate'] for p in matched_pages]
    print(f"\nCh-default rate across {len(matched_pages)} pages:")
    print(f"  Mean:   {np.mean(rates):.4f}")
    print(f"  Median: {np.median(rates):.4f}")
    print(f"  Std:    {np.std(rates):.4f}")
    print(f"  Range:  [{np.min(rates):.4f}, {np.max(rates):.4f}]")

    # -------------------------------------------------------------------
    # 3. Permutation tests for each feature
    # -------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("PERMUTATION TESTS (5000 shuffles, seed=42)")
    print("=" * 70)

    results = {}
    for feat in FEATURES:
        present_rates = []
        absent_rates = []
        for p in matched_pages:
            val = get_feature_value(annotations[p], feat)
            if val is None:
                continue
            r = page_stats[p]['ch_default_rate']
            if val == 1:
                present_rates.append(r)
            else:
                absent_rates.append(r)

        if len(present_rates) < 3 or len(absent_rates) < 3:
            print(f"\n{feat}: SKIPPED (n_present={len(present_rates)}, n_absent={len(absent_rates)})")
            results[feat] = None
            continue

        present_arr = np.array(present_rates)
        absent_arr = np.array(absent_rates)

        mean_p, mean_a, diff, pval = permutation_test(present_arr, absent_arr)
        pct_diff = (diff / mean_a * 100) if mean_a != 0 else float('inf')

        results[feat] = {
            'n_present': len(present_rates),
            'n_absent': len(absent_rates),
            'mean_present': mean_p,
            'mean_absent': mean_a,
            'difference': diff,
            'pct_difference': pct_diff,
            'p_value': pval,
        }

        sig = " ***" if pval < 0.01 else (" **" if pval < 0.05 else (" *" if pval < 0.1 else ""))
        print(f"\n{feat}:")
        print(f"  Present: n={len(present_rates):3d}, mean={mean_p:.4f}")
        print(f"  Absent:  n={len(absent_rates):3d}, mean={mean_a:.4f}")
        print(f"  Diff:    {diff:+.4f} ({pct_diff:+.1f}%)")
        print(f"  p-value: {pval:.4f}{sig}")

    # -------------------------------------------------------------------
    # 4. Sign test on distinctive features
    # -------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SIGN TEST (Distinctive Features)")
    print("=" * 70)

    n_lower = 0
    n_tested = 0
    for feat in DISTINCTIVE_FEATURES:
        r = results.get(feat)
        if r is None:
            print(f"  {feat}: SKIPPED")
            continue
        n_tested += 1
        direction = "LOWER" if r['difference'] < 0 else "HIGHER"
        if r['difference'] < 0:
            n_lower += 1
        print(f"  {feat}: default when present is {direction} ({r['difference']:+.4f}, p={r['p_value']:.4f})")

    sign_p = sign_test_pvalue(n_lower, n_tested)
    print(f"\n  {n_lower}/{n_tested} distinctive features show LOWER defaults when present")
    print(f"  Sign test p-value (two-tailed): {sign_p:.4f}")

    # -------------------------------------------------------------------
    # 5. Mantel test
    # -------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("MANTEL TEST (Botanical distance vs Row-profile distance)")
    print("=" * 70)

    # Build feature matrix and row-profile matrix for matched pages
    # Only use pages where all features are known (no '?')
    mantel_pages = []
    feat_matrix = []
    profile_matrix = []

    # Get all slot2 values across matched pages for consistent profile vectors
    all_slot2_keys = set()
    for p in matched_pages:
        all_slot2_keys.update(page_stats[p]['slot2_counts'].keys())
    slot2_keys = sorted(all_slot2_keys)

    for p in matched_pages:
        ann = annotations[p]
        feat_vals = []
        skip = False
        for feat in FEATURES:
            v = get_feature_value(ann, feat)
            if v is None:
                skip = True
                break
            feat_vals.append(v)
        if skip:
            continue

        # Build row-profile vector (normalized slot2 frequencies)
        s2c = page_stats[p]['slot2_counts']
        total_s2 = sum(s2c.values())
        profile = np.array([s2c.get(k, 0) / total_s2 if total_s2 > 0 else 0 for k in slot2_keys])

        mantel_pages.append(p)
        feat_matrix.append(feat_vals)
        profile_matrix.append(profile)

    n_mantel = len(mantel_pages)
    print(f"Pages with complete features for Mantel test: {n_mantel}")

    if n_mantel >= 10:
        feat_matrix = np.array(feat_matrix)
        profile_matrix = np.array(profile_matrix)

        # Botanical distance matrix (Hamming on binary features)
        bot_dist = np.zeros((n_mantel, n_mantel))
        for i in range(n_mantel):
            for j in range(i + 1, n_mantel):
                d = hamming_distance(feat_matrix[i], feat_matrix[j])
                bot_dist[i, j] = d
                bot_dist[j, i] = d

        # Row-profile distance matrix (cosine distance)
        prof_dist = np.zeros((n_mantel, n_mantel))
        for i in range(n_mantel):
            for j in range(i + 1, n_mantel):
                d = cosine_distance(profile_matrix[i], profile_matrix[j])
                prof_dist[i, j] = d
                prof_dist[j, i] = d

        mantel_r, mantel_p = mantel_test(bot_dist, prof_dist, n_perm=1000, seed=42)
        print(f"  Mantel r = {mantel_r:.4f}")
        print(f"  Mantel p = {mantel_p:.4f}")
    else:
        mantel_r, mantel_p = None, None
        print("  Too few pages for Mantel test")

    # -------------------------------------------------------------------
    # 6. Anomaly rate correlation
    # -------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("ANOMALY RATE CORRELATION (Chimeric Illustration Prediction)")
    print("=" * 70)

    anomaly_rates = [page_stats[p]['anomaly_rate'] for p in matched_pages]
    print(f"\nAnomaly rate across {len(matched_pages)} pages:")
    print(f"  Mean:   {np.mean(anomaly_rates):.4f}")
    print(f"  Median: {np.median(anomaly_rates):.4f}")
    print(f"  Std:    {np.std(anomaly_rates):.4f}")

    anomaly_results = {}
    for feat in FEATURES:
        present_rates = []
        absent_rates = []
        for p in matched_pages:
            val = get_feature_value(annotations[p], feat)
            if val is None:
                continue
            r = page_stats[p]['anomaly_rate']
            if val == 1:
                present_rates.append(r)
            else:
                absent_rates.append(r)

        if len(present_rates) < 3 or len(absent_rates) < 3:
            anomaly_results[feat] = None
            continue

        present_arr = np.array(present_rates)
        absent_arr = np.array(absent_rates)

        mean_p, mean_a, diff, pval = permutation_test(present_arr, absent_arr)

        anomaly_results[feat] = {
            'n_present': len(present_rates),
            'n_absent': len(absent_rates),
            'mean_present': mean_p,
            'mean_absent': mean_a,
            'difference': diff,
            'p_value': pval,
        }

        sig = " ***" if pval < 0.01 else (" **" if pval < 0.05 else (" *" if pval < 0.1 else ""))
        if pval < 0.1:
            print(f"\n{feat} (ANOMALY RATE):")
            print(f"  Present: n={len(present_rates):3d}, mean={mean_p:.4f}")
            print(f"  Absent:  n={len(absent_rates):3d}, mean={mean_a:.4f}")
            print(f"  Diff:    {diff:+.4f}")
            print(f"  p-value: {pval:.4f}{sig}")

    # Print summary of anomaly features trending
    print("\nAnomaly rate summary (all features):")
    for feat in FEATURES:
        r = anomaly_results.get(feat)
        if r is None:
            continue
        direction = "+" if r['difference'] > 0 else "-"
        sig = "*" if r['p_value'] < 0.05 else ("~" if r['p_value'] < 0.1 else "")
        print(f"  {feat:25s} diff={r['difference']:+.4f}  p={r['p_value']:.4f} {sig}")

    # -------------------------------------------------------------------
    # 7. Save findings
    # -------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("SAVING FINDINGS")
    print("=" * 70)

    save_findings(results, sign_p, n_lower, n_tested, mantel_r, mantel_p,
                  anomaly_results, matched_pages, page_stats, annotations)


def save_findings(results, sign_p, n_lower, n_tested, mantel_r, mantel_p,
                  anomaly_results, matched_pages, page_stats, annotations):
    """Write findings to markdown file."""
    out_path = os.path.join(ANALYSIS_DIR, "phase2_replication_findings.md")

    lines = []
    lines.append("# Phase 2 Replication: Botanical Correlation Test (Full Set)")
    lines.append("")
    lines.append(f"**Date:** 2026-03-30")
    lines.append(f"**Pages analyzed:** {len(matched_pages)}")
    lines.append("")

    # Summary stats
    rates = [page_stats[p]['ch_default_rate'] for p in matched_pages]
    lines.append("## Ch-Default Rate Summary")
    lines.append("")
    lines.append(f"- Mean: {np.mean(rates):.4f}")
    lines.append(f"- Median: {np.median(rates):.4f}")
    lines.append(f"- Std: {np.std(rates):.4f}")
    lines.append(f"- Range: [{np.min(rates):.4f}, {np.max(rates):.4f}]")
    lines.append("")

    # Permutation test results table
    lines.append("## Permutation Tests (ch-default rate ~ botanical features)")
    lines.append("")
    lines.append("5000 permutations, seed=42, two-tailed.")
    lines.append("")
    lines.append("| Feature | n_present | n_absent | mean_present | mean_absent | diff | %diff | p-value | sig |")
    lines.append("|---------|-----------|----------|-------------|------------|------|-------|---------|-----|")

    for feat in FEATURES:
        r = results.get(feat)
        if r is None:
            lines.append(f"| {feat} | - | - | - | - | - | - | - | skipped |")
            continue
        sig = "***" if r['p_value'] < 0.01 else ("**" if r['p_value'] < 0.05 else ("*" if r['p_value'] < 0.1 else ""))
        lines.append(
            f"| {feat} | {r['n_present']} | {r['n_absent']} | "
            f"{r['mean_present']:.4f} | {r['mean_absent']:.4f} | "
            f"{r['difference']:+.4f} | {r['pct_difference']:+.1f}% | "
            f"{r['p_value']:.4f} | {sig} |"
        )

    lines.append("")

    # Sign test
    lines.append("## Sign Test (Distinctive Features)")
    lines.append("")
    lines.append(f"Distinctive features tested: {', '.join(DISTINCTIVE_FEATURES)}")
    lines.append("")
    lines.append(f"- {n_lower}/{n_tested} show LOWER defaults when feature is present")
    lines.append(f"- Sign test p-value (two-tailed): **{sign_p:.4f}**")
    lines.append("")

    # Direction details
    lines.append("Direction details:")
    lines.append("")
    for feat in DISTINCTIVE_FEATURES:
        r = results.get(feat)
        if r is None:
            lines.append(f"- {feat}: skipped (insufficient data)")
            continue
        direction = "LOWER" if r['difference'] < 0 else "HIGHER"
        lines.append(f"- {feat}: {direction} ({r['difference']:+.4f}, p={r['p_value']:.4f})")
    lines.append("")

    # Mantel test
    lines.append("## Mantel Test")
    lines.append("")
    lines.append("Botanical feature distance (Hamming) vs row-profile distance (cosine on slot2 frequencies).")
    lines.append("1000 permutations, seed=42.")
    lines.append("")
    if mantel_r is not None:
        lines.append(f"- Mantel r = **{mantel_r:.4f}**")
        lines.append(f"- Mantel p = **{mantel_p:.4f}**")
        if mantel_p < 0.05:
            lines.append("- **Significant**: pages with similar botanical features have similar row profiles.")
        elif mantel_p < 0.1:
            lines.append("- *Marginally significant*: weak trend toward botanical-row profile correspondence.")
        else:
            lines.append("- Not significant at p<0.05.")
    else:
        lines.append("- Could not run (too few pages with complete features).")
    lines.append("")

    # Anomaly rate
    lines.append("## Anomaly Rate Correlation")
    lines.append("")
    lines.append("Testing whether botanical features correlate with anomaly rate ")
    lines.append("(proportion of fallback-only or hapax words per page).")
    lines.append("")
    lines.append("| Feature | n_present | n_absent | mean_present | mean_absent | diff | p-value | sig |")
    lines.append("|---------|-----------|----------|-------------|------------|------|---------|-----|")

    for feat in FEATURES:
        r = anomaly_results.get(feat)
        if r is None:
            lines.append(f"| {feat} | - | - | - | - | - | - | skipped |")
            continue
        sig = "***" if r['p_value'] < 0.01 else ("**" if r['p_value'] < 0.05 else ("*" if r['p_value'] < 0.1 else ""))
        lines.append(
            f"| {feat} | {r['n_present']} | {r['n_absent']} | "
            f"{r['mean_present']:.4f} | {r['mean_absent']:.4f} | "
            f"{r['difference']:+.4f} | {r['p_value']:.4f} | {sig} |"
        )
    lines.append("")

    # Comparison to pilot
    lines.append("## Comparison to Pilot (40 pages)")
    lines.append("")
    lines.append("Pilot findings (for comparison):")
    lines.append("- leaf_lobed: p=0.0064, 32% lower defaults when present")
    lines.append("- root_bulbous: p=0.012, 39% lower defaults when present")
    lines.append("- 5/5 distinctive features trended lower (sign test p=0.031)")
    lines.append("")

    # Check which pilot findings replicate
    leaf_lobed = results.get('leaf_lobed')
    root_bulbous = results.get('root_bulbous')

    if leaf_lobed:
        rep = "REPLICATED" if leaf_lobed['p_value'] < 0.05 and leaf_lobed['difference'] < 0 else "NOT replicated"
        lines.append(f"- leaf_lobed: {rep} (p={leaf_lobed['p_value']:.4f}, diff={leaf_lobed['difference']:+.4f})")
    if root_bulbous:
        rep = "REPLICATED" if root_bulbous['p_value'] < 0.05 and root_bulbous['difference'] < 0 else "NOT replicated"
        lines.append(f"- root_bulbous: {rep} (p={root_bulbous['p_value']:.4f}, diff={root_bulbous['difference']:+.4f})")

    sign_rep = "REPLICATED" if sign_p < 0.05 else "NOT replicated"
    lines.append(f"- Sign test: {sign_rep} ({n_lower}/{n_tested}, p={sign_p:.4f})")
    lines.append("")

    # Interpretation
    lines.append("## Interpretation")
    lines.append("")

    sig_features = [f for f in FEATURES if results.get(f) and results[f]['p_value'] < 0.05]
    marginal_features = [f for f in FEATURES if results.get(f) and 0.05 <= results[f]['p_value'] < 0.1]

    lines.append(f"Significant features (p<0.05): {', '.join(sig_features) if sig_features else 'none'}")
    lines.append(f"Marginal features (p<0.1): {', '.join(marginal_features) if marginal_features else 'none'}")
    lines.append("")

    if sign_p < 0.05:
        lines.append("The sign test replicates: morphologically distinctive features consistently show ")
        lines.append("lower ch-default rates. This supports the hypothesis that botanical content ")
        lines.append("influences the combinatorial encoding of Voynich text.")
    elif sign_p < 0.1:
        lines.append("The sign test is marginally significant, showing a trend consistent with the pilot.")
        lines.append("The pattern of distinctive features having lower defaults persists but is weaker.")
    else:
        lines.append("The sign test does not replicate at conventional significance levels.")
        lines.append("The pilot finding may have been a false positive or the effect is weaker in the full set.")

    lines.append("")

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"Findings saved to: {out_path}")


if __name__ == '__main__':
    run_analysis()
