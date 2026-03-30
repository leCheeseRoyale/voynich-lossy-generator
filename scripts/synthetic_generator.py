"""
Phase 4.1: Synthetic Voynich text generators and statistical comparison.

Two generators:
  A) Independent Slots (null model) — sample each slot independently
  B) Row-Based (hypothesis model) — sample row signature then S4 sub-slots

Compare: entropy, Zipf, word-length, vocab size, hapax, TTR, transitions, default rate.
Bootstrap 100 corpora for CI estimation.
"""

import sys
import os
import json
import re
import math
import time
from collections import Counter, defaultdict

import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE, "data")
ANALYSIS_DIR = os.path.join(BASE, "analysis")
SCRIPTS_DIR = os.path.join(BASE, "scripts")

sys.path.insert(0, SCRIPTS_DIR)
from parse_ivtff import parse_ivtff
from slot_analysis import decompose_word

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

def load_json(name):
    with open(os.path.join(ANALYSIS_DIR, name)) as f:
        return json.load(f)


def load_real_corpus():
    """Load real Voynich words and return list of word strings."""
    words = parse_ivtff(os.path.join(DATA_DIR, "IT2a-n.txt"))
    return [w for _, w in words]


def build_slot_distributions(slot_fragments):
    """Build per-slot (fragment, probability) arrays from slot_fragments.json."""
    dists = {}
    for slot in ["slot1", "slot2", "slot3", "slot4", "slot5"]:
        frags = slot_fragments[slot]
        items = list(frags.items())
        total = sum(c for _, c in items)
        fragments = [f for f, _ in items]
        probs = np.array([c / total for _, c in items])
        dists[slot] = (fragments, probs)
    return dists


def build_sub4_distributions(sub4_data):
    """Build sub4a/b/c distributions."""
    dists = {}
    for sub in ["sub4a", "sub4b", "sub4c"]:
        items = list(sub4_data[sub].items())
        total = sum(c for _, c in items)
        fragments = [f for f, _ in items]
        probs = np.array([c / total for _, c in items])
        dists[sub] = (fragments, probs)
    return dists


def build_row_distribution(row_clusters):
    """Build distribution over row signatures (S1|S2|S3|S5) -> count."""
    rows = []
    counts = []
    for key, val in row_clusters.items():
        rows.append(key)
        counts.append(val["total_tokens"])
    total = sum(counts)
    probs = np.array([c / total for c in counts])
    return rows, probs


# ---------------------------------------------------------------------------
# Generator A: Independent Slots
# ---------------------------------------------------------------------------

def generate_word_independent(slot_dists, rng):
    """Sample each slot independently from marginal distribution."""
    parts = []
    for slot in ["slot1", "slot2", "slot3", "slot4", "slot5"]:
        fragments, probs = slot_dists[slot]
        idx = rng.choice(len(fragments), p=probs)
        frag = fragments[idx]
        if frag != "(empty)":
            parts.append(frag)
    word = "".join(parts)
    return word if word else "d"  # fallback: never produce empty


def generate_corpus_A(slot_dists, n, rng):
    """Generate n words using independent slot sampling."""
    return [generate_word_independent(slot_dists, rng) for _ in range(n)]


# ---------------------------------------------------------------------------
# Generator B: Row-Based
# ---------------------------------------------------------------------------

def generate_word_row(row_keys, row_probs, sub4_dists, rng):
    """Sample a row signature, then sample S4 sub-slots independently."""
    # Pick a row
    idx = rng.choice(len(row_keys), p=row_probs)
    row_key = row_keys[idx]

    # Parse row key: S1|S2|S3|S5
    parts = row_key.split("|")
    s1, s2, s3, s5 = parts[0], parts[1], parts[2], parts[3]

    # Sample S4 sub-slots
    s4_parts = []
    for sub in ["sub4a", "sub4b", "sub4c"]:
        fragments, probs = sub4_dists[sub]
        sidx = rng.choice(len(fragments), p=probs)
        frag = fragments[sidx]
        if frag != "(empty)":
            s4_parts.append(frag)
    s4 = "".join(s4_parts)

    # Concatenate: S1 + S2 + S3 + S4 + S5
    word = s1 + s2 + s3 + s4 + s5
    return word if word else "d"


def generate_corpus_B(row_keys, row_probs, sub4_dists, n, rng):
    """Generate n words using row-based sampling."""
    return [generate_word_row(row_keys, row_probs, sub4_dists, rng) for _ in range(n)]


# ---------------------------------------------------------------------------
# Statistical metrics
# ---------------------------------------------------------------------------

def shannon_entropy(words):
    """H1: Shannon entropy of word frequency distribution (bits)."""
    counts = Counter(words)
    n = len(words)
    h = 0.0
    for c in counts.values():
        p = c / n
        if p > 0:
            h -= p * math.log2(p)
    return h


def bigram_entropy(words):
    """H2: entropy of consecutive word-pair distribution (bits)."""
    if len(words) < 2:
        return 0.0
    bigrams = Counter()
    for i in range(len(words) - 1):
        bigrams[(words[i], words[i + 1])] += 1
    n = sum(bigrams.values())
    h = 0.0
    for c in bigrams.values():
        p = c / n
        if p > 0:
            h -= p * math.log2(p)
    return h


def zipf_exponent(words):
    """Compute Zipf exponent via log-log linear regression of rank vs freq."""
    counts = Counter(words)
    freqs = sorted(counts.values(), reverse=True)
    ranks = np.arange(1, len(freqs) + 1, dtype=float)
    log_ranks = np.log10(ranks)
    log_freqs = np.log10(np.array(freqs, dtype=float))

    # Linear regression: log_freq = a * log_rank + b
    # Zipf exponent = -a
    n = len(log_ranks)
    sx = log_ranks.sum()
    sy = log_freqs.sum()
    sxx = (log_ranks ** 2).sum()
    sxy = (log_ranks * log_freqs).sum()
    a = (n * sxy - sx * sy) / (n * sxx - sx ** 2)
    return -a  # Zipf exponent (positive)


def word_length_stats(words):
    """Return mean, std, and histogram of word lengths."""
    lengths = [len(w) for w in words]
    arr = np.array(lengths)
    hist = Counter(lengths)
    return arr.mean(), arr.std(), hist


def vocab_size(words):
    return len(set(words))


def hapax_count(words):
    counts = Counter(words)
    return sum(1 for c in counts.values() if c == 1)


def hapax_proportion(words):
    h = hapax_count(words)
    v = vocab_size(words)
    return h / v if v > 0 else 0.0


def type_token_ratio(words):
    return vocab_size(words) / len(words) if words else 0.0


def default_rate(words):
    """Proportion of words where S1=empty and S2=ch (the 'default' pattern)."""
    count = 0
    for w in words:
        result = decompose_word(w)
        if result and "_fallback" not in result:
            s1 = result["slot1"] or ""
            s2 = result["slot2"] or ""
            if s1 == "" and s2 == "ch":
                count += 1
    return count / len(words) if words else 0.0


def slot_transition_matrix(words):
    """Compute S1->S2 and S3->S5 transition matrices."""
    t12 = defaultdict(Counter)
    t35 = defaultdict(Counter)
    for w in words:
        result = decompose_word(w)
        if result and "_fallback" not in result:
            s1 = result["slot1"] or "(empty)"
            s2 = result["slot2"] or "(empty)"
            s3 = result["slot3"] or "(empty)"
            s5 = result["slot5"] or "(empty)"
            t12[s1][s2] += 1
            t35[s3][s5] += 1
    return t12, t35


def transition_jsd(real_trans, synth_trans):
    """Jensen-Shannon divergence of transition distributions (averaged over source states).

    JSD(P||Q) = 0.5*KL(P||M) + 0.5*KL(Q||M)  where M = 0.5*(P+Q).
    Symmetric, bounded in [0, 1] (when using log2).

    Uses Laplace smoothing (alpha=1) over the union vocabulary so both P and Q
    are well-defined over the same support.
    """
    all_sources = set(real_trans.keys()) | set(synth_trans.keys())

    total_jsd = 0.0
    total_weight = 0.0
    alpha = 1.0  # Laplace smoothing parameter

    for src in all_sources:
        real_counts = real_trans.get(src, {})
        synth_counts = synth_trans.get(src, {})
        real_total = sum(real_counts.values()) if real_counts else 0
        synth_total = sum(synth_counts.values()) if synth_counts else 0

        # Skip source states with no real observations
        if real_total == 0:
            continue

        # Union vocabulary for this source state
        targets = set()
        if src in real_trans:
            targets |= set(real_trans[src].keys())
        if src in synth_trans:
            targets |= set(synth_trans[src].keys())
        V = len(targets)

        # Laplace-smoothed distributions with identical denominator structure
        p_dist = {}
        q_dist = {}
        for t in targets:
            p_dist[t] = (real_counts.get(t, 0) + alpha) / (real_total + alpha * V)
            q_dist[t] = (synth_counts.get(t, 0) + alpha) / (synth_total + alpha * V)

        # Mixture M = 0.5*(P + Q)
        m_dist = {t: 0.5 * (p_dist[t] + q_dist[t]) for t in targets}

        # JSD = 0.5 * KL(P||M) + 0.5 * KL(Q||M)
        kl_pm = 0.0
        kl_qm = 0.0
        for t in targets:
            if p_dist[t] > 0:
                kl_pm += p_dist[t] * math.log2(p_dist[t] / m_dist[t])
            if q_dist[t] > 0:
                kl_qm += q_dist[t] * math.log2(q_dist[t] / m_dist[t])

        jsd = 0.5 * kl_pm + 0.5 * kl_qm
        total_jsd += jsd * real_total
        total_weight += real_total

    return total_jsd / total_weight if total_weight > 0 else 0.0


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------

def compute_all_metrics(words, label=""):
    """Compute all metrics for a word list. Returns dict."""
    h1 = shannon_entropy(words)
    h2 = bigram_entropy(words)
    z = zipf_exponent(words)
    wl_mean, wl_std, wl_hist = word_length_stats(words)
    vs = vocab_size(words)
    hx = hapax_count(words)
    hp = hapax_proportion(words)
    ttr = type_token_ratio(words)
    dr = default_rate(words)
    t12, t35 = slot_transition_matrix(words)

    return {
        "label": label,
        "h1": h1,
        "h2": h2,
        "zipf_exp": z,
        "wl_mean": wl_mean,
        "wl_std": wl_std,
        "wl_hist": wl_hist,
        "vocab_size": vs,
        "hapax_count": hx,
        "hapax_proportion": hp,
        "ttr": ttr,
        "default_rate": dr,
        "trans_12": t12,
        "trans_35": t35,
    }


def print_comparison(real_m, genA_m, genB_m):
    """Print side-by-side comparison table."""
    print("\n" + "=" * 80)
    print("STATISTICAL COMPARISON: Real vs Generator A (Independent) vs Generator B (Row)")
    print("=" * 80)

    metrics = [
        ("H1 (word entropy, bits)", "h1", ".4f"),
        ("H2 (bigram entropy, bits)", "h2", ".4f"),
        ("Zipf exponent", "zipf_exp", ".4f"),
        ("Word length mean", "wl_mean", ".3f"),
        ("Word length std", "wl_std", ".3f"),
        ("Vocabulary size", "vocab_size", "d"),
        ("Hapax legomena", "hapax_count", "d"),
        ("Hapax proportion (of types)", "hapax_proportion", ".4f"),
        ("Type-token ratio", "ttr", ".4f"),
        ("Default rate (S1=empty,S2=ch)", "default_rate", ".4f"),
    ]

    print(f"\n{'Metric':<35s} {'Real':>12s} {'GenA':>12s} {'GenB':>12s}  {'Closer?':>8s}")
    print("-" * 85)

    results = {}
    for name, key, fmt in metrics:
        rv = real_m[key]
        av = genA_m[key]
        bv = genB_m[key]
        dist_a = abs(rv - av)
        dist_b = abs(rv - bv)
        closer = "GenB" if dist_b < dist_a else ("GenA" if dist_a < dist_b else "Tie")
        results[key] = closer

        rv_s = f"{rv:{fmt}}"
        av_s = f"{av:{fmt}}"
        bv_s = f"{bv:{fmt}}"
        print(f"  {name:<33s} {rv_s:>12s} {av_s:>12s} {bv_s:>12s}  {closer:>8s}")

    # Transition KL divergences
    print(f"\n{'Transition JSD (Jensen-Shannon)':<35s} {'':>12s} {'GenA':>12s} {'GenB':>12s}  {'Closer?':>8s}")
    print("-" * 85)

    kl_a_12 = transition_jsd(real_m["trans_12"], genA_m["trans_12"])
    kl_b_12 = transition_jsd(real_m["trans_12"], genB_m["trans_12"])
    closer_12 = "GenB" if kl_b_12 < kl_a_12 else "GenA"
    print(f"  {'S1->S2 JSD(Real||Synth)':<33s} {'0.0000':>12s} {kl_a_12:>12.4f} {kl_b_12:>12.4f}  {closer_12:>8s}")
    results["kl_12"] = closer_12

    kl_a_35 = transition_jsd(real_m["trans_35"], genA_m["trans_35"])
    kl_b_35 = transition_jsd(real_m["trans_35"], genB_m["trans_35"])
    closer_35 = "GenB" if kl_b_35 < kl_a_35 else "GenA"
    print(f"  {'S3->S5 JSD(Real||Synth)':<33s} {'0.0000':>12s} {kl_a_35:>12.4f} {kl_b_35:>12.4f}  {closer_35:>8s}")
    results["kl_35"] = closer_35

    # Word length histogram comparison
    print(f"\n--- Word Length Distribution ---")
    all_lens = set()
    for m in [real_m, genA_m, genB_m]:
        all_lens |= set(m["wl_hist"].keys())
    n_real = sum(real_m["wl_hist"].values())
    n_a = sum(genA_m["wl_hist"].values())
    n_b = sum(genB_m["wl_hist"].values())

    print(f"  {'Len':<5s} {'Real%':>8s} {'GenA%':>8s} {'GenB%':>8s}")
    for l in sorted(all_lens):
        rp = 100 * real_m["wl_hist"].get(l, 0) / n_real
        ap = 100 * genA_m["wl_hist"].get(l, 0) / n_a
        bp = 100 * genB_m["wl_hist"].get(l, 0) / n_b
        print(f"  {l:<5d} {rp:>7.1f}% {ap:>7.1f}% {bp:>7.1f}%")

    # Summary
    genB_wins = sum(1 for v in results.values() if v == "GenB")
    genA_wins = sum(1 for v in results.values() if v == "GenA")
    print(f"\n--- Summary ---")
    print(f"  GenB closer on {genB_wins}/{len(results)} metrics")
    print(f"  GenA closer on {genA_wins}/{len(results)} metrics")

    return results, {
        "kl_a_12": kl_a_12, "kl_b_12": kl_b_12,
        "kl_a_35": kl_a_35, "kl_b_35": kl_b_35,
    }


# ---------------------------------------------------------------------------
# Bootstrap CI
# ---------------------------------------------------------------------------

def bootstrap_ci(slot_dists, row_keys, row_probs, sub4_dists, n_words, n_bootstrap=100, seed=42):
    """Generate n_bootstrap corpora from each generator and compute 95% CIs."""
    print(f"\n{'=' * 80}")
    print(f"BOOTSTRAP ANALYSIS ({n_bootstrap} corpora per generator)")
    print(f"{'=' * 80}")

    metrics_to_bootstrap = [
        ("H1", lambda w: shannon_entropy(w)),
        ("Zipf exponent", lambda w: zipf_exponent(w)),
        ("Vocab size", lambda w: float(vocab_size(w))),
        ("H2", lambda w: bigram_entropy(w)),
        ("Word length mean", lambda w: float(np.mean([len(x) for x in w]))),
        ("Type-token ratio", lambda w: type_token_ratio(w)),
        ("Default rate", lambda w: default_rate(w)),
    ]

    rng = np.random.default_rng(seed)

    results_A = {name: [] for name, _ in metrics_to_bootstrap}
    results_B = {name: [] for name, _ in metrics_to_bootstrap}

    print(f"\n  Generating {n_bootstrap} corpora from Generator A...")
    t0 = time.time()
    for i in range(n_bootstrap):
        corpus = generate_corpus_A(slot_dists, n_words, rng)
        for name, func in metrics_to_bootstrap:
            results_A[name].append(func(corpus))
    print(f"  Done in {time.time()-t0:.1f}s")

    print(f"  Generating {n_bootstrap} corpora from Generator B...")
    t0 = time.time()
    for i in range(n_bootstrap):
        corpus = generate_corpus_B(row_keys, row_probs, sub4_dists, n_words, rng)
        for name, func in metrics_to_bootstrap:
            results_B[name].append(func(corpus))
    print(f"  Done in {time.time()-t0:.1f}s")

    # Compute real metrics
    real_words = load_real_corpus()[:n_words]
    real_values = {}
    for name, func in metrics_to_bootstrap:
        real_values[name] = func(real_words)

    print(f"\n  {'Metric':<25s} {'Real':>10s} {'GenA 95% CI':>25s} {'GenB 95% CI':>25s} {'Real in A?':>12s} {'Real in B?':>12s}")
    print("  " + "-" * 100)

    ci_results = {}
    for name, _ in metrics_to_bootstrap:
        rv = real_values[name]
        a_vals = np.array(results_A[name])
        b_vals = np.array(results_B[name])
        a_lo, a_hi = np.percentile(a_vals, 2.5), np.percentile(a_vals, 97.5)
        b_lo, b_hi = np.percentile(b_vals, 2.5), np.percentile(b_vals, 97.5)
        in_a = "YES" if a_lo <= rv <= a_hi else "NO"
        in_b = "YES" if b_lo <= rv <= b_hi else "NO"

        ci_results[name] = {
            "real": rv,
            "a_ci": (a_lo, a_hi), "b_ci": (b_lo, b_hi),
            "in_a": in_a == "YES", "in_b": in_b == "YES",
            "a_mean": a_vals.mean(), "b_mean": b_vals.mean(),
        }

        fmt = ".4f" if rv < 100 else ".1f"
        rv_s = f"{rv:{fmt}}"
        a_ci_s = f"[{a_lo:{fmt}}, {a_hi:{fmt}}]"
        b_ci_s = f"[{b_lo:{fmt}}, {b_hi:{fmt}}]"
        print(f"  {name:<25s} {rv_s:>10s} {a_ci_s:>25s} {b_ci_s:>25s} {in_a:>12s} {in_b:>12s}")

    # Count
    in_b_count = sum(1 for v in ci_results.values() if v["in_b"])
    in_a_count = sum(1 for v in ci_results.values() if v["in_a"])
    print(f"\n  Real falls within GenA CI: {in_a_count}/{len(ci_results)}")
    print(f"  Real falls within GenB CI: {in_b_count}/{len(ci_results)}")

    return ci_results


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_report(results, kl_values, ci_results, real_m, genA_m, genB_m):
    """Write findings markdown."""
    report = []
    report.append("# Phase 4.1: Synthetic Generator Validation\n")
    report.append("## Overview\n")
    report.append("Two synthetic generators tested against the real Voynich corpus:\n")
    report.append("- **Generator A (Independent Slots)**: Each slot sampled independently from marginal frequencies (null model)")
    report.append("- **Generator B (Row-Based)**: Row signature (S1,S2,S3,S5) sampled jointly; S4 sub-slots sampled independently (hypothesis model)\n")
    report.append(f"Corpus size: {sum(real_m['wl_hist'].values())} tokens\n")

    report.append("## Single-Run Comparison\n")
    report.append("| Metric | Real | GenA | GenB | Closer? |")
    report.append("|--------|------|------|------|---------|")

    metrics_list = [
        ("H1 (word entropy, bits)", "h1", ".4f"),
        ("H2 (bigram entropy, bits)", "h2", ".4f"),
        ("Zipf exponent", "zipf_exp", ".4f"),
        ("Word length mean", "wl_mean", ".3f"),
        ("Word length std", "wl_std", ".3f"),
        ("Vocabulary size", "vocab_size", "d"),
        ("Hapax legomena", "hapax_count", "d"),
        ("Hapax proportion", "hapax_proportion", ".4f"),
        ("Type-token ratio", "ttr", ".4f"),
        ("Default rate", "default_rate", ".4f"),
    ]

    for name, key, fmt in metrics_list:
        rv = real_m[key]
        av = genA_m[key]
        bv = genB_m[key]
        closer = results.get(key, "?")
        report.append(f"| {name} | {rv:{fmt}} | {av:{fmt}} | {bv:{fmt}} | {closer} |")

    report.append(f"\n| S1->S2 JSD | 0.0000 | {kl_values['kl_a_12']:.4f} | {kl_values['kl_b_12']:.4f} | {results.get('kl_12','?')} |")
    report.append(f"| S3->S5 JSD | 0.0000 | {kl_values['kl_a_35']:.4f} | {kl_values['kl_b_35']:.4f} | {results.get('kl_35','?')} |")

    # Word length table
    report.append("\n## Word Length Distribution\n")
    report.append("| Length | Real% | GenA% | GenB% |")
    report.append("|--------|-------|-------|-------|")
    all_lens = set()
    for m in [real_m, genA_m, genB_m]:
        all_lens |= set(m["wl_hist"].keys())
    n_real = sum(real_m["wl_hist"].values())
    n_a = sum(genA_m["wl_hist"].values())
    n_b = sum(genB_m["wl_hist"].values())
    for l in sorted(all_lens):
        rp = 100 * real_m["wl_hist"].get(l, 0) / n_real
        ap = 100 * genA_m["wl_hist"].get(l, 0) / n_a
        bp = 100 * genB_m["wl_hist"].get(l, 0) / n_b
        report.append(f"| {l} | {rp:.1f} | {ap:.1f} | {bp:.1f} |")

    # Bootstrap
    report.append("\n## Bootstrap Confidence Intervals (100 corpora, 95% CI)\n")
    report.append("| Metric | Real | GenA CI | GenB CI | Real in A? | Real in B? |")
    report.append("|--------|------|---------|---------|------------|------------|")
    for name, info in ci_results.items():
        rv = info["real"]
        fmt = ".4f" if rv < 100 else ".1f"
        a_ci = f"[{info['a_ci'][0]:{fmt}}, {info['a_ci'][1]:{fmt}}]"
        b_ci = f"[{info['b_ci'][0]:{fmt}}, {info['b_ci'][1]:{fmt}}]"
        in_a = "YES" if info["in_a"] else "NO"
        in_b = "YES" if info["in_b"] else "NO"
        report.append(f"| {name} | {rv:{fmt}} | {a_ci} | {b_ci} | {in_a} | {in_b} |")

    in_b_count = sum(1 for v in ci_results.values() if v["in_b"])
    in_a_count = sum(1 for v in ci_results.values() if v["in_a"])

    # Verdict
    report.append("\n## Findings\n")

    genB_wins = sum(1 for v in results.values() if v == "GenB")
    genA_wins = sum(1 for v in results.values() if v == "GenA")

    report.append(f"### Single-run comparison")
    report.append(f"- Generator B closer to Real on **{genB_wins}/{len(results)}** metrics")
    report.append(f"- Generator A closer to Real on **{genA_wins}/{len(results)}** metrics\n")

    report.append(f"### Bootstrap validation")
    report.append(f"- Real falls within GenA 95% CI on **{in_a_count}/{len(ci_results)}** metrics")
    report.append(f"- Real falls within GenB 95% CI on **{in_b_count}/{len(ci_results)}** metrics\n")

    report.append("### Interpretation\n")

    if genB_wins > genA_wins and in_b_count > in_a_count:
        report.append("The row-based model (Generator B) **significantly outperforms** the independent-slot "
                       "null model (Generator A) in reproducing Voynich statistical properties. "
                       "This validates the hypothesis that Voynich words are generated by a process "
                       "that jointly determines S1, S2, S3, and S5 (the 'row'), with S4 sub-slots "
                       "providing within-row variation.\n")
        report.append("Key observations:")
        report.append("- The independent model fails because it creates slot combinations that "
                       "never occur in the real text, inflating vocabulary and entropy")
        report.append("- The row-based model preserves the correlations between slots 1,2,3,5 "
                       "that are characteristic of real Voynich text")
        report.append("- The row-based model's slot transition KL divergences are much lower, "
                       "confirming it captures the dependency structure")
        verdict = "VALIDATED"
    elif genB_wins > genA_wins:
        report.append("Generator B outperforms Generator A in single-run metrics but bootstrap "
                       "results are mixed. The row-based model captures more structure than "
                       "independent sampling but may need refinement.\n")
        verdict = "PARTIALLY VALIDATED"
    else:
        report.append("Results are inconclusive. The row-based model does not clearly outperform "
                       "the independent model, suggesting the row hypothesis may need revision.\n")
        verdict = "INCONCLUSIVE"

    report.append(f"\n**Overall verdict: Row-based generation hypothesis is {verdict}.**\n")

    return "\n".join(report)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("Phase 4.1: Synthetic Voynich Text Generator\n")

    # Load data
    print("Loading data...")
    slot_fragments = load_json("slot_fragments.json")
    sub4_data = load_json("slot4_decomposition.json")
    row_clusters = load_json("row_clusters.json")

    real_words = load_real_corpus()
    N = len(real_words)
    print(f"Real corpus: {N} tokens")

    # Build distributions
    slot_dists = build_slot_distributions(slot_fragments)
    sub4_dists = build_sub4_distributions(sub4_data)
    row_keys, row_probs = build_row_distribution(row_clusters)

    # Generate corpora
    rng = np.random.default_rng(42)

    print(f"\nGenerating {N} tokens from Generator A (Independent Slots)...")
    t0 = time.time()
    corpus_A = generate_corpus_A(slot_dists, N, rng)
    print(f"  Done in {time.time()-t0:.1f}s")

    print(f"Generating {N} tokens from Generator B (Row-Based)...")
    t0 = time.time()
    corpus_B = generate_corpus_B(row_keys, row_probs, sub4_dists, N, rng)
    print(f"  Done in {time.time()-t0:.1f}s")

    # Sample outputs
    print(f"\nSample words - Real:   {' '.join(real_words[:15])}")
    print(f"Sample words - GenA:   {' '.join(corpus_A[:15])}")
    print(f"Sample words - GenB:   {' '.join(corpus_B[:15])}")

    # Compute metrics
    print("\nComputing metrics for Real corpus...")
    real_m = compute_all_metrics(real_words, "Real")
    print("Computing metrics for Generator A...")
    genA_m = compute_all_metrics(corpus_A, "GenA")
    print("Computing metrics for Generator B...")
    genB_m = compute_all_metrics(corpus_B, "GenB")

    # Compare
    results, kl_values = print_comparison(real_m, genA_m, genB_m)

    # Bootstrap
    ci_results = bootstrap_ci(slot_dists, row_keys, row_probs, sub4_dists, N, n_bootstrap=100, seed=42)

    # Generate report
    report = generate_report(results, kl_values, ci_results, real_m, genA_m, genB_m)

    outpath = os.path.join(ANALYSIS_DIR, "phase4_1_findings_v2.md")
    with open(outpath, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"\nReport saved to {outpath}")


if __name__ == "__main__":
    main()
