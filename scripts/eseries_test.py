"""
E-Series Parametric Test

Tests the hypothesis that E-series values (e, ee, eee, eeee) in sub-slot 4b
encode a parametric quantity. If true, words that differ ONLY in their S4b
value should co-occur on the same pages at elevated rates compared to chance.
"""

import os
import re
import sys
import json
import math
from collections import Counter, defaultdict

import numpy as np

# ---- Path setup ----
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, SCRIPT_DIR)

from parse_ivtff import parse_ivtff
from slot_analysis import decompose_word, WORD_PATTERN

# ---- Slot4 sub-decomposition (inlined from slot4_decompose.py) ----

GLYPH_ORDER = ['ch', 'sh', 'ee', 'e', 'o', 'a', 'h']
BENCH = {'ch', 'sh', 'h'}
TERMINAL = {'o', 'a'}


def tokenize_slot4(fragment):
    tokens = []
    i = 0
    while i < len(fragment):
        matched = False
        for g in GLYPH_ORDER:
            if fragment[i:].startswith(g):
                tokens.append(g)
                i += len(g)
                matched = True
                break
        if not matched:
            tokens.append(fragment[i])
            i += 1
    return tokens


def extract_sub_slots(tokens):
    """Extract sub4a (bench), sub4b (e-series), sub4c (terminal) from tokens.
    Returns (sub4a, sub4b, sub4c) or None if pattern is not B?E*T?."""
    classes = []
    for t in tokens:
        if t in BENCH:
            classes.append('B')
        elif t == 'e' or t == 'ee':
            classes.append('E')
        elif t in TERMINAL:
            classes.append('T')
        else:
            return None  # unknown token

    pattern = ''.join(classes)
    if not re.match(r'^B?E*T?$', pattern):
        return None

    bench_parts = []
    e_parts = []
    term_parts = []
    for tok, cls in zip(tokens, classes):
        if cls == 'B':
            bench_parts.append(tok)
        elif cls == 'E':
            e_parts.append(tok)
        elif cls == 'T':
            term_parts.append(tok)

    sub4a = ''.join(bench_parts) if bench_parts else ''
    sub4b = ''.join(['e' if t == 'e' else 'ee' for t in e_parts])  # normalize
    # Actually just rejoin the e tokens
    sub4b_raw = ''
    for t in e_parts:
        sub4b_raw += t
    sub4c = ''.join(term_parts) if term_parts else ''

    return sub4a, sub4b_raw, sub4c


def full_decompose(word):
    """Decompose word into (s1, s2, s3, s4a, s4b, s4c, s5) or None."""
    result = decompose_word(word)
    if result is None or '_fallback' in result:
        return None

    s1 = result['slot1'] or ''
    s2 = result['slot2'] or ''
    s3 = result['slot3'] or ''
    s4_raw = result['slot4'] or ''
    s5 = result['slot5'] or ''

    if s4_raw == '':
        s4a, s4b, s4c = '', '', ''
    else:
        tokens = tokenize_slot4(s4_raw)
        sub = extract_sub_slots(tokens)
        if sub is None:
            return None
        s4a, s4b, s4c = sub

    return (s1, s2, s3, s4a, s4b, s4c, s5)


# ---- Main analysis ----

def get_page(locus):
    """Extract page ID from locus (e.g., 'f1r.1' -> 'f1r')."""
    return locus.split('.')[0]


def main():
    data_path = os.path.join(PROJECT_DIR, 'data', 'IT2a-n.txt')
    words = parse_ivtff(data_path)

    print("=" * 70)
    print("E-SERIES PARAMETRIC TEST")
    print("=" * 70)

    # Step 1: Decompose all words, build page-level data
    # word_pages[word] = set of pages it appears on
    # page_words[page] = list of (position_index, word) in order
    word_pages = defaultdict(set)
    page_words = defaultdict(list)
    word_decomp = {}  # word -> decomposition tuple
    decomp_success = 0
    decomp_fail = 0
    word_freq = Counter()

    for idx, (locus, word) in enumerate(words):
        page = get_page(locus)
        page_words[page].append((idx, word))
        word_freq[word] += 1
        word_pages[word].add(page)

        if word not in word_decomp:
            d = full_decompose(word)
            if d is not None:
                word_decomp[word] = d

    for w, c in word_freq.items():
        if w in word_decomp:
            decomp_success += c
        else:
            decomp_fail += c

    total_tokens = sum(word_freq.values())
    print(f"\nCorpus: {total_tokens} tokens, {len(word_freq)} types, {len(page_words)} pages")
    print(f"Decomposed: {decomp_success} tokens ({100*decomp_success/total_tokens:.1f}%)")
    print(f"Failed decomposition: {decomp_fail} tokens ({100*decomp_fail/total_tokens:.1f}%)")

    # Step 2: Build E-families
    # Family signature: (s1, s2, s3, s4a, s4c, s5) — everything EXCEPT s4b
    family_members = defaultdict(dict)  # signature -> {s4b_value: word}

    for word, decomp in word_decomp.items():
        s1, s2, s3, s4a, s4b, s4c, s5 = decomp
        sig = (s1, s2, s3, s4a, s4c, s5)
        # Multiple words could map to same (sig, s4b) if decomposition is ambiguous
        # Keep the more frequent one
        if s4b in family_members[sig]:
            existing = family_members[sig][s4b]
            if word_freq[word] > word_freq[existing]:
                family_members[sig][s4b] = word
        else:
            family_members[sig][s4b] = word

    # Filter: families with 2+ distinct E-series values
    e_families = {}
    for sig, members in family_members.items():
        if len(members) >= 2:
            e_families[sig] = members

    print(f"\nE-families with 2+ members: {len(e_families)}")

    # Show top families
    print(f"\n--- Top 30 E-families by total frequency ---")
    family_stats = []
    for sig, members in e_families.items():
        total_f = sum(word_freq[w] for w in members.values())
        family_stats.append((sig, members, total_f))
    family_stats.sort(key=lambda x: -x[2])

    for sig, members, total_f in family_stats[:30]:
        sig_str = f"({'/'.join(s if s else '_' for s in sig)})"
        member_strs = []
        for s4b in sorted(members.keys(), key=lambda x: len(x)):
            w = members[s4b]
            s4b_label = s4b if s4b else 'empty'
            member_strs.append(f"{w}[{s4b_label}]={word_freq[w]}")
        print(f"  {sig_str:30s} total={total_f:5d}  {', '.join(member_strs)}")

    # Step 3: Co-occurrence analysis with permutation test
    print(f"\n{'=' * 70}")
    print("CO-OCCURRENCE ANALYSIS")
    print("=" * 70)

    # Filter families where at least 2 members have freq >= 10
    testable_families = []
    for sig, members, total_f in family_stats:
        qualified = {s4b: w for s4b, w in members.items() if word_freq[w] >= 10}
        if len(qualified) >= 2:
            testable_families.append((sig, qualified))

    print(f"\nTestable families (2+ members with freq >= 10): {len(testable_families)}")

    # For each testable family, compute observed co-occurrence rate
    all_pages = sorted(page_words.keys())
    page_word_sets = {p: set(w for _, w in wlist) for p, wlist in page_words.items()}

    N_PERM = 1000
    rng = np.random.default_rng(42)

    results = []
    for sig, members in testable_families:
        member_words = list(members.values())
        member_set = set(member_words)

        # Pages where any family member appears
        relevant_pages = set()
        for w in member_words:
            relevant_pages |= word_pages[w]

        if len(relevant_pages) == 0:
            continue

        # Observed: pages with 2+ distinct family members
        obs_cooccur = 0
        for p in relevant_pages:
            present = member_set & page_word_sets[p]
            if len(present) >= 2:
                obs_cooccur += 1

        obs_rate = obs_cooccur / len(relevant_pages)

        # Permutation test: for each member word, shuffle its page assignments
        # while preserving frequency and page-size distribution.
        # FIXED: compare co-occurrence COUNTS over a FIXED page set (relevant_pages)
        # to avoid denominator mismatch between observed and null.
        page_sizes = np.array([len(page_words[p]) for p in all_pages], dtype=float)
        page_probs = page_sizes / page_sizes.sum()

        # Convert relevant_pages to a list for iteration
        relevant_pages_list = sorted(relevant_pages)

        perm_counts = np.zeros(N_PERM)
        for perm_i in range(N_PERM):
            # For each member word, randomly assign it to pages
            perm_pages = {}  # word -> set of pages
            for w in member_words:
                n_pages = len(word_pages[w])
                # Sample pages weighted by page size (without replacement)
                chosen_idx = rng.choice(len(all_pages), size=min(n_pages, len(all_pages)),
                                        replace=False, p=page_probs)
                perm_pages[w] = set(all_pages[i] for i in chosen_idx)

            # Count co-occurrences over the FIXED relevant_pages set
            cooccur = 0
            for p in relevant_pages_list:
                present = sum(1 for w in member_words if p in perm_pages[w])
                if present >= 2:
                    cooccur += 1
            perm_counts[perm_i] = cooccur

        expected_count = perm_counts.mean()
        expected_rate = expected_count / len(relevant_pages) if len(relevant_pages) > 0 else 0
        ratio = obs_rate / expected_rate if expected_rate > 0 else float('inf')
        p_value = (np.sum(perm_counts >= obs_cooccur) + 1) / (N_PERM + 1)

        s4b_values = sorted(members.keys(), key=lambda x: len(x))
        results.append({
            'sig': sig,
            'members': members,
            's4b_values': s4b_values,
            'n_relevant_pages': len(relevant_pages),
            'obs_cooccur': obs_cooccur,
            'obs_rate': obs_rate,
            'expected_rate': expected_rate,
            'ratio': ratio,
            'p_value': p_value,
        })

    # Sort by ratio
    results.sort(key=lambda x: -x['ratio'])

    print(f"\n--- Per-family results (sorted by obs/expected ratio) ---")
    print(f"{'Signature':35s} {'S4b values':20s} {'Pages':>5s} {'Obs':>5s} {'ObsR':>6s} {'ExpR':>6s} {'Ratio':>6s} {'p':>7s}")
    sig_count = 0
    significant_count = 0
    for r in results:
        sig_str = '/'.join(s if s else '_' for s in r['sig'])
        s4b_str = ','.join(s if s else 'mt' for s in r['s4b_values'])
        flag = '*' if r['p_value'] < 0.05 else ' '
        if r['p_value'] < 0.05:
            significant_count += 1
        print(f"  {sig_str:33s} {s4b_str:20s} {r['n_relevant_pages']:5d} {r['obs_cooccur']:5d} "
              f"{r['obs_rate']:6.3f} {r['expected_rate']:6.3f} {r['ratio']:6.2f} {r['p_value']:7.4f} {flag}")
        sig_count += 1

    # Step 4: Aggregate statistics
    print(f"\n{'=' * 70}")
    print("AGGREGATE RESULTS")
    print("=" * 70)

    ratios = [r['ratio'] for r in results if np.isfinite(r['ratio'])]
    p_values = [r['p_value'] for r in results]

    print(f"\nTotal testable families: {len(results)}")
    print(f"Significant (p < 0.05): {significant_count} ({100*significant_count/len(results):.1f}%)")
    print(f"Expected by chance (5%): {0.05 * len(results):.1f}")
    if ratios:
        print(f"\nCo-occurrence ratio (obs/expected):")
        print(f"  Median: {np.median(ratios):.3f}")
        print(f"  Mean:   {np.mean(ratios):.3f}")
        print(f"  Min:    {np.min(ratios):.3f}")
        print(f"  Max:    {np.max(ratios):.3f}")

    # E-series pair analysis: which pairs co-occur most?
    print(f"\n--- E-series pair analysis ---")
    E_VALUES = ['', 'e', 'ee', 'eee', 'eeee']
    pair_ratios = defaultdict(list)
    pair_pvals = defaultdict(list)

    for r in results:
        s4b_vals = r['s4b_values']
        # For each pair of s4b values in this family
        for i in range(len(s4b_vals)):
            for j in range(i + 1, len(s4b_vals)):
                pair_key = (s4b_vals[i] if s4b_vals[i] else 'mt', s4b_vals[j] if s4b_vals[j] else 'mt')
                pair_ratios[pair_key].append(r['ratio'])
                pair_pvals[pair_key].append(r['p_value'])

    print(f"{'Pair':20s} {'N':>4s} {'Med ratio':>10s} {'%sig':>6s}")
    for pair in sorted(pair_ratios.keys(), key=lambda x: -np.median(pair_ratios[x])):
        rats = pair_ratios[pair]
        pvs = pair_pvals[pair]
        n_sig = sum(1 for p in pvs if p < 0.05)
        if len(rats) >= 2:
            print(f"  {pair[0]+'/'+pair[1]:18s} {len(rats):4d} {np.median(rats):10.3f} {100*n_sig/len(rats):6.1f}%")

    # Step 5: E-series ordering test
    print(f"\n{'=' * 70}")
    print("E-SERIES ORDERING TEST")
    print("=" * 70)

    # For each testable family, on pages where 2+ variants co-occur,
    # check if they appear in order (lower E-series value before higher)
    e_rank = {'': 0, 'e': 1, 'ee': 2, 'eee': 3, 'eeee': 4}

    concordant = 0
    discordant = 0
    tied = 0
    total_pairs_checked = 0

    # Also collect Kendall's tau per family
    family_taus = []

    for r in results:
        members = r['members']
        member_words = list(members.values())
        member_set = set(member_words)
        word_to_rank = {}
        for s4b, w in members.items():
            word_to_rank[w] = e_rank.get(s4b, -1)

        family_conc = 0
        family_disc = 0
        family_tied = 0

        for page in page_words:
            # Find positions of family members on this page
            positions = []  # (position_in_page, e_rank)
            for pos_idx, (global_idx, w) in enumerate(page_words[page]):
                if w in member_set:
                    positions.append((pos_idx, word_to_rank[w]))

            if len(positions) < 2:
                continue

            # Check all pairs
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    pos_i, rank_i = positions[i]
                    pos_j, rank_j = positions[j]
                    # Position is already ordered (i < j means pos_i < pos_j)
                    if rank_i < rank_j:
                        concordant += 1
                        family_conc += 1
                    elif rank_i > rank_j:
                        discordant += 1
                        family_disc += 1
                    else:
                        tied += 1
                        family_tied += 1
                    total_pairs_checked += 1

        total_non_tied = family_conc + family_disc
        if total_non_tied >= 5:
            tau = (family_conc - family_disc) / total_non_tied
            family_taus.append(tau)

    print(f"\nPositional ordering of E-series variants within pages:")
    print(f"  Total pairs checked: {total_pairs_checked}")
    print(f"  Concordant (lower E before higher E): {concordant}")
    print(f"  Discordant (higher E before lower E): {discordant}")
    print(f"  Tied (same E-rank): {tied}")
    non_tied = concordant + discordant
    if non_tied > 0:
        overall_tau = (concordant - discordant) / non_tied
        print(f"\n  Overall Kendall's tau: {overall_tau:.4f}")
        # Significance test for tau using normal approximation
        # Under null, E[tau] = 0, Var(tau) ~ 2(2n+5)/(9n(n-1)) but we use
        # simpler approach: binomial test on concordant vs discordant
        # Under null, P(concordant) = 0.5
        from math import sqrt
        z = (concordant - discordant) / sqrt(non_tied)
        p_ordering = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / sqrt(2))))
        print(f"  Z-score: {z:.3f}")
        print(f"  p-value (two-sided): {p_ordering:.6f}")
        if overall_tau > 0:
            print(f"  Direction: Lower E-values tend to appear BEFORE higher E-values")
        elif overall_tau < 0:
            print(f"  Direction: Higher E-values tend to appear BEFORE lower E-values")
        else:
            print(f"  Direction: No clear ordering tendency")

    if family_taus:
        print(f"\n  Per-family Kendall's tau (families with 5+ non-tied pairs):")
        print(f"  N families: {len(family_taus)}")
        print(f"  Median tau: {np.median(family_taus):.4f}")
        print(f"  Mean tau:   {np.mean(family_taus):.4f}")
        positive = sum(1 for t in family_taus if t > 0)
        negative = sum(1 for t in family_taus if t < 0)
        zero = sum(1 for t in family_taus if t == 0)
        print(f"  Positive (ordered): {positive}, Negative: {negative}, Zero: {zero}")

    # ---- Save findings ----
    print(f"\n{'=' * 70}")
    print("SAVING FINDINGS")
    print("=" * 70)

    analysis_dir = os.path.join(PROJECT_DIR, 'analysis')
    os.makedirs(analysis_dir, exist_ok=True)

    findings = []
    findings.append("# E-Series Parametric Test Findings\n")
    findings.append(f"**Date**: 2026-03-30\n")
    findings.append(f"**Corpus**: IT2a-n.txt ({total_tokens} tokens, {len(word_freq)} types, {len(page_words)} pages)\n")

    findings.append("\n## Hypothesis\n")
    findings.append("The E-series sub-slot (S4b: empty, e, ee, eee, eeee) encodes a parametric value. ")
    findings.append("If true, words identical except for S4b should co-occur on the same pages at rates ")
    findings.append("higher than chance, representing the same concept with different parameter values.\n")

    findings.append("\n## E-Family Construction\n")
    findings.append(f"- Total E-families (2+ members): **{len(e_families)}**\n")
    findings.append(f"- Testable families (2+ members with freq >= 10): **{len(testable_families)}**\n")

    findings.append("\n### Top 15 E-families by frequency\n")
    findings.append("| Signature | Members | Total freq |\n")
    findings.append("|-----------|---------|------------|\n")
    for sig, members, total_f in family_stats[:15]:
        sig_str = '/'.join(s if s else '\\_' for s in sig)
        member_strs = ', '.join(f"{members[s4b]}[{s4b if s4b else 'empty'}]={word_freq[members[s4b]]}"
                                for s4b in sorted(members.keys(), key=len))
        findings.append(f"| {sig_str} | {member_strs} | {total_f} |\n")

    findings.append("\n## Co-occurrence Results\n")
    findings.append(f"- Families with significant co-occurrence (p < 0.05): **{significant_count}/{len(results)}** ")
    findings.append(f"({100*significant_count/len(results):.1f}%)\n")
    findings.append(f"- Expected by chance at 5% level: **{0.05 * len(results):.1f}**\n")
    if ratios:
        findings.append(f"- Median co-occurrence ratio (obs/expected): **{np.median(ratios):.3f}**\n")
        findings.append(f"- Mean co-occurrence ratio: **{np.mean(ratios):.3f}**\n")

    findings.append("\n### Interpretation of co-occurrence ratio\n")
    findings.append("- Ratio = 1.0: E-family members co-occur at chance levels\n")
    findings.append("- Ratio > 1.0: E-family members co-occur MORE than chance (supports parametric hypothesis)\n")
    findings.append("- Ratio < 1.0: E-family members co-occur LESS than chance (anti-correlation)\n")

    findings.append("\n### Per-family results\n")
    findings.append("| Signature | S4b values | Pages | Obs co-occur | Obs rate | Exp rate | Ratio | p-value |\n")
    findings.append("|-----------|-----------|-------|-------------|----------|----------|-------|--------|\n")
    for r in results:
        sig_str = '/'.join(s if s else '\\_' for s in r['sig'])
        s4b_str = ','.join(s if s else 'mt' for s in r['s4b_values'])
        flag = '\\*' if r['p_value'] < 0.05 else ''
        findings.append(f"| {sig_str} | {s4b_str} | {r['n_relevant_pages']} | {r['obs_cooccur']} | "
                        f"{r['obs_rate']:.3f} | {r['expected_rate']:.3f} | {r['ratio']:.2f} | {r['p_value']:.4f}{flag} |\n")

    findings.append("\n### E-series pair analysis\n")
    findings.append("Do certain E-series distance pairs show stronger co-occurrence?\n\n")
    findings.append("| Pair | N families | Median ratio | % significant |\n")
    findings.append("|------|-----------|-------------|---------------|\n")
    for pair in sorted(pair_ratios.keys(), key=lambda x: -np.median(pair_ratios[x])):
        rats = pair_ratios[pair]
        pvs = pair_pvals[pair]
        if len(rats) >= 2:
            n_sig = sum(1 for p in pvs if p < 0.05)
            findings.append(f"| {pair[0]}/{pair[1]} | {len(rats)} | {np.median(rats):.3f} | {100*n_sig/len(rats):.1f}% |\n")

    findings.append("\n## E-Series Ordering Test\n")
    findings.append("On pages where multiple E-series variants co-occur, do they appear in order?\n\n")
    findings.append(f"- Total position pairs checked: **{total_pairs_checked}**\n")
    findings.append(f"- Concordant (lower E before higher E): **{concordant}**\n")
    findings.append(f"- Discordant (higher E before lower E): **{discordant}**\n")
    findings.append(f"- Tied (same rank): **{tied}**\n")
    if non_tied > 0:
        findings.append(f"- Kendall's tau: **{overall_tau:.4f}**\n")
        findings.append(f"- Z-score: **{z:.3f}**, p-value: **{p_ordering:.6f}**\n")
        if overall_tau > 0:
            findings.append(f"- Direction: Lower E-values tend to appear BEFORE higher E-values\n")
        elif overall_tau < 0:
            findings.append(f"- Direction: Higher E-values tend to appear BEFORE lower E-values\n")
        else:
            findings.append(f"- Direction: No clear ordering tendency\n")
    if family_taus:
        findings.append(f"\nPer-family tau statistics ({len(family_taus)} families with 5+ non-tied pairs):\n")
        findings.append(f"- Median tau: **{np.median(family_taus):.4f}**\n")
        findings.append(f"- Mean tau: **{np.mean(family_taus):.4f}**\n")
        positive = sum(1 for t in family_taus if t > 0)
        negative = sum(1 for t in family_taus if t < 0)
        findings.append(f"- Positive (ordered): {positive}, Negative: {negative}\n")

    findings.append("\n## Conclusions\n")
    # Will be filled by the actual numbers
    if ratios:
        median_r = np.median(ratios)
        if significant_count / len(results) > 0.15 and median_r > 1.2:
            findings.append("**STRONG SUPPORT** for the parametric hypothesis. E-family members co-occur ")
            findings.append("on the same pages significantly more than chance, suggesting that E-series variants ")
            findings.append("represent parametric modifications of the same base concept.\n")
        elif significant_count / len(results) > 0.08 and median_r > 1.05:
            findings.append("**MODERATE SUPPORT** for the parametric hypothesis. Some E-families show elevated ")
            findings.append("co-occurrence, but the effect is not universal across all families.\n")
        elif significant_count / len(results) <= 0.08 and median_r <= 1.05:
            findings.append("**NO SUPPORT** for the parametric hypothesis. E-family co-occurrence rates are ")
            findings.append("consistent with chance, suggesting E-series values do not encode a parametric quantity ")
            findings.append("that varies across instances of the same base word.\n")
        else:
            findings.append("**MIXED EVIDENCE**. The co-occurrence patterns show some deviation from chance but ")
            findings.append("the signal is not strong enough for definitive conclusions.\n")

    if non_tied > 0:
        if p_ordering < 0.01:
            findings.append(f"\nThe ordering test shows a {'positive' if overall_tau > 0 else 'negative'} ")
            findings.append(f"tendency (tau={overall_tau:.4f}, p={p_ordering:.6f}), suggesting E-series values ")
            findings.append("may track a sequential or ordered quantity within pages.\n")
        else:
            findings.append(f"\nThe ordering test shows no significant positional ordering of E-series variants ")
            findings.append(f"within pages (tau={overall_tau:.4f}, p={p_ordering:.6f}).\n")

    outpath = os.path.join(analysis_dir, 'eseries_findings.md')
    with open(outpath, 'w', encoding='utf-8') as f:
        f.writelines(findings)
    print(f"Findings saved to {outpath}")


if __name__ == '__main__':
    main()
