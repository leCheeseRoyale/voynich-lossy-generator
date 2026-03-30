"""
Phase 2.2: Test whether herbal pages sharing botanical features share
row-selection profiles.

Input:
  - analysis/annotations_batch{1,2,3,4}.json  (botanical features per page)
  - analysis/row_clusters.json  (row signatures with page distributions)
  - data/IT2a-n_words.tsv  (word list with page provenance)

Method:
  For each binary botanical feature:
    1. Split pilot pages into feature-present vs feature-absent groups
    2. Compute per-page row-frequency profile (vector of row-signature counts)
    3. Compute between-group distance (mean cosine distance within vs between)
    4. Permutation test: shuffle group labels 1000x, compute null distribution
    5. Report p-value and effect size

Also test: overall similarity structure using Mantel test
(correlation between botanical feature distance matrix and
row-profile distance matrix).
"""

import json
import os
import sys
import re
import numpy as np
from collections import Counter, defaultdict

# ============================================================
# 1. Load annotations
# ============================================================
def load_annotations():
    annotations = {}
    for i in range(1, 5):
        path = f'analysis/annotations_batch{i}.json'
        if not os.path.exists(path):
            print(f"WARNING: {path} not found, skipping")
            continue
        with open(path) as f:
            batch = json.load(f)
        annotations.update(batch)
    print(f"Loaded annotations for {len(annotations)} pages")
    return annotations


# ============================================================
# 2. Build per-page row-frequency profiles
# ============================================================
def build_page_row_profiles(words_file, slot_module_path='.'):
    """For each page, count occurrences of each row signature."""
    sys.path.insert(0, slot_module_path)
    from parse_ivtff import parse_ivtff
    from slot_analysis import decompose_word

    words = parse_ivtff(words_file)

    # Extract folio from locus (e.g., "f1r.1" -> "f1r")
    page_rows = defaultdict(Counter)  # folio -> row_sig -> count

    for locus, word in words:
        folio = locus.split('.')[0]
        result = decompose_word(word)
        if result is None or '_fallback' in result:
            continue
        # Row signature = (S1, S2, S3, S5)
        row_sig = (
            result.get('slot1', '') or '',
            result.get('slot2', '') or '',
            result.get('slot3', '') or '',
            result.get('slot5', '') or ''
        )
        page_rows[folio][row_sig] += 1

    return page_rows


def profiles_to_matrix(page_rows, pages):
    """Convert per-page row counters to a matrix (pages x rows)."""
    # Get all row signatures that appear in the pilot pages
    all_sigs = set()
    for p in pages:
        all_sigs.update(page_rows.get(p, {}).keys())
    all_sigs = sorted(all_sigs)
    sig_idx = {s: i for i, s in enumerate(all_sigs)}

    matrix = np.zeros((len(pages), len(all_sigs)))
    for i, p in enumerate(pages):
        for sig, count in page_rows.get(p, {}).items():
            matrix[i, sig_idx[sig]] = count

    # Normalize to relative frequencies
    row_sums = matrix.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1
    matrix_norm = matrix / row_sums

    return matrix_norm, all_sigs


# ============================================================
# 3. Distance computations
# ============================================================
def cosine_distance_matrix(M):
    """Compute pairwise cosine distance matrix."""
    # Normalize rows to unit vectors
    norms = np.linalg.norm(M, axis=1, keepdims=True)
    norms[norms == 0] = 1
    M_norm = M / norms
    similarity = M_norm @ M_norm.T
    similarity = np.clip(similarity, -1, 1)
    return 1 - similarity


def feature_distance_matrix(annotations, pages, features):
    """Binary Hamming distance based on botanical features."""
    n = len(pages)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            ai = annotations[pages[i]]
            aj = annotations[pages[j]]
            diffs = 0
            valid = 0
            for feat in features:
                vi = ai.get(feat)
                vj = aj.get(feat)
                if vi == '?' or vj == '?' or vi is None or vj is None:
                    continue
                valid += 1
                if vi != vj:
                    diffs += 1
            D[i, j] = diffs / valid if valid > 0 else 0.5
            D[j, i] = D[i, j]
    return D


# ============================================================
# 4. Permutation tests
# ============================================================
def test_feature_group_separation(row_dist, group_mask, n_perms=1000):
    """Test whether pages with a feature are more similar to each other
    in row-profile space than to pages without the feature.

    Returns observed effect, p-value, and null distribution stats.
    """
    n = len(group_mask)
    in_group = np.where(group_mask)[0]
    out_group = np.where(~group_mask)[0]

    if len(in_group) < 3 or len(out_group) < 3:
        return None  # too few for meaningful test

    # Observed: mean within-group distance minus mean between-group distance
    within = []
    between = []
    for i in in_group:
        for j in in_group:
            if i < j:
                within.append(row_dist[i, j])
    for i in in_group:
        for j in out_group:
            between.append(row_dist[i, j])

    if not within or not between:
        return None

    obs_within = np.mean(within)
    obs_between = np.mean(between)
    obs_effect = obs_between - obs_within  # positive = group is clustered

    # Permutation null
    rng = np.random.default_rng(42)
    null_effects = []
    for _ in range(n_perms):
        perm = rng.permutation(n)
        perm_in = perm[:len(in_group)]
        perm_out = perm[len(in_group):]
        w = [row_dist[perm_in[i], perm_in[j]]
             for i in range(len(perm_in)) for j in range(i+1, len(perm_in))]
        b = [row_dist[perm_in[i], perm_out[j]]
             for i in range(len(perm_in)) for j in range(len(perm_out))]
        if w and b:
            null_effects.append(np.mean(b) - np.mean(w))

    null_effects = np.array(null_effects)
    p_value = np.mean(null_effects >= obs_effect)

    return {
        'obs_within': float(obs_within),
        'obs_between': float(obs_between),
        'obs_effect': float(obs_effect),
        'null_mean': float(np.mean(null_effects)),
        'null_std': float(np.std(null_effects)),
        'p_value': float(p_value),
        'n_present': int(len(in_group)),
        'n_absent': int(len(out_group)),
        'effect_z': float((obs_effect - np.mean(null_effects)) / max(np.std(null_effects), 1e-10))
    }


def mantel_test(D1, D2, n_perms=1000):
    """Mantel test: correlation between two distance matrices."""
    n = D1.shape[0]
    # Extract upper triangular
    idx = np.triu_indices(n, k=1)
    v1 = D1[idx]
    v2 = D2[idx]

    obs_r = np.corrcoef(v1, v2)[0, 1]

    rng = np.random.default_rng(42)
    null_rs = []
    for _ in range(n_perms):
        perm = rng.permutation(n)
        D2_perm = D2[np.ix_(perm, perm)]
        v2_perm = D2_perm[idx]
        null_rs.append(np.corrcoef(v1, v2_perm)[0, 1])

    null_rs = np.array(null_rs)
    p_value = np.mean(null_rs >= obs_r)

    return {
        'obs_r': float(obs_r),
        'null_mean': float(np.mean(null_rs)),
        'null_std': float(np.std(null_rs)),
        'p_value': float(p_value),
        'effect_z': float((obs_r - np.mean(null_rs)) / max(np.std(null_rs), 1e-10))
    }


# ============================================================
# 5. Main
# ============================================================
if __name__ == '__main__':
    # Load data
    annotations = load_annotations()
    if not annotations:
        print("ERROR: No annotations found. Run annotation agents first.")
        sys.exit(1)

    # Build row profiles
    print("Building per-page row-frequency profiles...")
    page_rows = build_page_row_profiles('data/IT2a-n.txt', 'scripts')

    # Get pages that have both annotations and row profiles
    pages = sorted([p for p in annotations if p in page_rows])
    print(f"Pages with both annotations and row data: {len(pages)}")

    if len(pages) < 10:
        print("ERROR: Too few pages for meaningful analysis.")
        sys.exit(1)

    # Feature list
    features = [
        'root_visible', 'root_bulbous', 'root_fibrous',
        'leaf_serrated', 'leaf_lobed', 'leaf_smooth', 'leaf_compound',
        'flower_visible', 'flower_petals_few', 'flower_petals_many',
        'stem_branching', 'stem_single',
        'plant_tall', 'plant_rosette', 'has_fruit_seed'
    ]

    # Build matrices
    M, row_sigs = profiles_to_matrix(page_rows, pages)
    row_dist = cosine_distance_matrix(M)
    feat_dist = feature_distance_matrix(annotations, pages, features)

    print(f"Row profile matrix: {M.shape} (pages x row signatures)")
    print(f"Row distance matrix: {row_dist.shape}")

    # ---- Per-feature permutation tests ----
    print("\n" + "=" * 70)
    print("PER-FEATURE GROUP SEPARATION TESTS")
    print("=" * 70)

    results = {}
    for feat in features:
        # Build binary mask (treating ? as absent)
        mask = np.array([annotations[p].get(feat, 0) == 1 for p in pages])
        n_present = mask.sum()
        n_absent = (~mask).sum()

        if n_present < 3 or n_absent < 3:
            print(f"\n{feat}: SKIPPED (n_present={n_present}, n_absent={n_absent})")
            continue

        result = test_feature_group_separation(row_dist, mask, n_perms=1000)
        if result:
            results[feat] = result
            sig = "*" if result['p_value'] < 0.05 else ""
            strong = "**" if result['p_value'] < 0.01 else ""
            marker = strong or sig
            print(f"\n{feat} (n={n_present}/{n_absent}):")
            print(f"  within={result['obs_within']:.4f}  between={result['obs_between']:.4f}  "
                  f"effect={result['obs_effect']:.4f}  z={result['effect_z']:.2f}  "
                  f"p={result['p_value']:.4f} {marker}")

    # ---- Mantel test ----
    print("\n" + "=" * 70)
    print("MANTEL TEST: Botanical features vs Row profiles")
    print("=" * 70)

    mantel = mantel_test(feat_dist, row_dist, n_perms=1000)
    print(f"  r = {mantel['obs_r']:.4f}")
    print(f"  null: {mantel['null_mean']:.4f} +/- {mantel['null_std']:.4f}")
    print(f"  z = {mantel['effect_z']:.2f}")
    print(f"  p = {mantel['p_value']:.4f}")

    # ---- Save results ----
    output = {
        'per_feature': results,
        'mantel_test': mantel,
        'n_pages': len(pages),
        'n_row_signatures': len(row_sigs),
        'pages_used': pages
    }
    with open('analysis/phase2_2_results.json', 'w') as f:
        json.dump(output, f, indent=2)

    # ---- Write findings report ----
    with open('analysis/phase2_2_findings.md', 'w', encoding='utf-8') as f:
        f.write("# Phase 2.2: Row-Frequency Profile Correlation with Botanical Features\n\n")
        f.write(f"**Pages analyzed:** {len(pages)}\n")
        f.write(f"**Row signatures in profile:** {len(row_sigs)}\n")
        f.write(f"**Permutations:** 1000\n\n")

        f.write("## Per-Feature Group Separation\n\n")
        f.write("| Feature | n_present | n_absent | Within dist | Between dist | Effect | z-score | p-value | Sig? |\n")
        f.write("|---------|-----------|----------|-------------|-------------|--------|---------|---------|------|\n")

        sorted_feats = sorted(results.items(), key=lambda x: x[1]['p_value'])
        for feat, r in sorted_feats:
            sig = "**" if r['p_value'] < 0.01 else ("*" if r['p_value'] < 0.05 else "")
            f.write(f"| {feat} | {r['n_present']} | {r['n_absent']} | "
                    f"{r['obs_within']:.4f} | {r['obs_between']:.4f} | "
                    f"{r['obs_effect']:.4f} | {r['effect_z']:.2f} | "
                    f"{r['p_value']:.4f} | {sig} |\n")

        f.write(f"\n## Mantel Test\n\n")
        f.write(f"Correlation between botanical feature distance and row-profile distance:\n\n")
        f.write(f"- r = {mantel['obs_r']:.4f}\n")
        f.write(f"- null: {mantel['null_mean']:.4f} +/- {mantel['null_std']:.4f}\n")
        f.write(f"- z = {mantel['effect_z']:.2f}\n")
        f.write(f"- p = {mantel['p_value']:.4f}\n\n")

        sig_feats = [feat for feat, r in results.items() if r['p_value'] < 0.05]
        if sig_feats:
            f.write(f"## Significant Features (p < 0.05)\n\n")
            for feat in sig_feats:
                r = results[feat]
                f.write(f"- **{feat}**: Pages with this feature use more similar "
                        f"row-selection profiles (effect z={r['effect_z']:.2f}, p={r['p_value']:.4f})\n")
        else:
            f.write("## No individual features reached significance at p < 0.05\n\n")

        if mantel['p_value'] < 0.05:
            f.write(f"\n**OVERALL:** The Mantel test shows significant correlation between "
                    f"botanical similarity and row-profile similarity (r={mantel['obs_r']:.4f}, "
                    f"p={mantel['p_value']:.4f}). Pages with similar botanical illustrations "
                    f"tend to use similar word-generation patterns.\n")
        else:
            f.write(f"\n**OVERALL:** The Mantel test did not reach significance "
                    f"(r={mantel['obs_r']:.4f}, p={mantel['p_value']:.4f}). "
                    f"The botanical feature distance and row-profile distance are not "
                    f"significantly correlated at this sample size.\n")

    print("\nResults saved to analysis/phase2_2_results.json and analysis/phase2_2_findings.md")
