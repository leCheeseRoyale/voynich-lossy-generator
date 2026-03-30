"""
Bridging Test: Phase 1 -> Phase 2
Do default fragment rates vary across manuscript sections?

Tests whether the slot-based "default filler" rates (identified in Phase 1.3)
differ significantly across the known section types (Herbal, Biological,
Zodiac, etc.), which would independently confirm Montemurro & Zanette (2013)
finding that vocabulary differs by section — using a purely structural metric.
"""

import sys
import os
import re
import math
from collections import Counter, defaultdict
from itertools import combinations

import numpy as np

# Allow importing sibling modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parse_ivtff import parse_ivtff
from slot_analysis import decompose_word

# --------------------------------------------------------------------------
# Config
# --------------------------------------------------------------------------
DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'IT2a-n.txt')
OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'analysis')

CANDIDATE_DEFAULTS = {
    'slot1': 'o',
    'slot2': 'ch',
    'slot3': 'k',
    'slot4': 'a',
    'slot5': 'y',
}

SECTION_NAMES = {
    'H': 'Herbal',
    'S': 'Stars/Pharma',
    'B': 'Biological',
    'P': 'Pharmaceutical',
    'Z': 'Zodiac',
    'C': 'Cosmological',
    'A': 'Astronomical',
    'T': 'Text-only',
}

MIN_WORDS_PER_PAGE = 10  # skip pages with very few words

# --------------------------------------------------------------------------
# 1. Parse section metadata from IVTFF headers
# --------------------------------------------------------------------------
def parse_section_metadata(filepath):
    """Parse $I= section labels from folio headers."""
    folio_section = {}
    with open(filepath, 'r', encoding='latin-1') as f:
        for line in f:
            # Match: <f1r>      <! $Q=A $P=A ... $I=T ...>
            m = re.match(r'^<(f\d+[rv]\d?)>\s+.*\$I=([A-Z])', line)
            if m:
                folio_section[m.group(1)] = m.group(2)
    return folio_section


# --------------------------------------------------------------------------
# 2. Load and decompose corpus with page provenance
# --------------------------------------------------------------------------
def load_corpus(filepath):
    """Load words, decompose into slots, return list of dicts with page info."""
    words = parse_ivtff(filepath)
    records = []
    failed = 0
    for locus, word in words:
        result = decompose_word(word)
        if result is None or '_fallback' in result:
            failed += 1
            continue
        page = re.match(r'(f\d+[rv]\d?)', locus).group(1)
        rec = {f'slot{i}': result[f'slot{i}'] or '' for i in range(1, 6)}
        rec['page'] = page
        rec['word'] = word
        records.append(rec)
    print(f"Loaded {len(records)} decomposed words ({failed} failed/fallback)")
    return records


# --------------------------------------------------------------------------
# 3. Compute per-page default rates
# --------------------------------------------------------------------------
def compute_page_rates(records, folio_section):
    """For each page, compute default rates for all 5 slots."""
    # Group by page
    pages = defaultdict(list)
    for rec in records:
        pages[rec['page']].append(rec)

    page_stats = []
    for page, recs in sorted(pages.items()):
        n = len(recs)
        if n < MIN_WORDS_PER_PAGE:
            continue
        section = folio_section.get(page, '?')
        if section == '?':
            continue

        stats = {'page': page, 'section': section, 'n_words': n}

        # For each slot, compute default rate
        for slot, default_frag in CANDIDATE_DEFAULTS.items():
            if slot == 'slot2':
                # ch-default: slot1 empty AND slot2 == ch
                count = sum(1 for r in recs if r['slot1'] == '' and r['slot2'] == 'ch')
            else:
                # General: slot contains the default fragment
                count = sum(1 for r in recs if r[slot] == default_frag)
            stats[f'{slot}_default_rate'] = count / n
            stats[f'{slot}_default_count'] = count

        # Overall default rate: average of all 5 slot default rates
        stats['overall_default_rate'] = np.mean([stats[f'{s}_default_rate'] for s in CANDIDATE_DEFAULTS])

        page_stats.append(stats)

    return page_stats


# --------------------------------------------------------------------------
# 4. Statistical tests
# --------------------------------------------------------------------------
def rank_data(x):
    """Assign ranks to data (average ranks for ties)."""
    x = np.array(x)
    n = len(x)
    order = np.argsort(x)
    ranks = np.empty(n, dtype=float)
    i = 0
    while i < n:
        j = i
        while j < n and x[order[j]] == x[order[i]]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0  # 1-based average rank
        for k in range(i, j):
            ranks[order[k]] = avg_rank
        i = j
    return ranks


def kruskal_wallis(groups):
    """
    Kruskal-Wallis H test (non-parametric one-way ANOVA on ranks).
    groups: list of arrays, one per group.
    Returns H statistic and approximate p-value (chi2 with k-1 df).
    """
    all_data = np.concatenate(groups)
    N = len(all_data)
    ranks = rank_data(all_data)

    # Split ranks back into groups
    idx = 0
    group_ranks = []
    for g in groups:
        n_g = len(g)
        group_ranks.append(ranks[idx:idx + n_g])
        idx += n_g

    # H statistic
    H = 0.0
    for gr in group_ranks:
        n_g = len(gr)
        if n_g == 0:
            continue
        H += n_g * (np.mean(gr) - (N + 1) / 2.0) ** 2
    H = 12.0 / (N * (N + 1)) * H

    # Approximate p-value using chi2 distribution
    k = len(groups)
    df = k - 1
    p = chi2_sf(H, df)

    return H, df, p


def mann_whitney_u(x, y):
    """
    Mann-Whitney U test.
    Returns U statistic, z-score, p-value (two-sided), rank-biserial r.
    """
    nx, ny = len(x), len(y)
    combined = np.concatenate([x, y])
    ranks = rank_data(combined)
    R1 = np.sum(ranks[:nx])

    U1 = R1 - nx * (nx + 1) / 2.0
    U2 = nx * ny - U1
    U = min(U1, U2)

    # Normal approximation
    mu = nx * ny / 2.0
    sigma = math.sqrt(nx * ny * (nx + ny + 1) / 12.0)
    if sigma == 0:
        return U, 0, 1.0, 0.0
    z = (U - mu) / sigma
    p = 2.0 * normal_sf(abs(z))

    # Rank-biserial correlation (effect size)
    r_rb = 1.0 - 2.0 * U / (nx * ny)

    return U, z, p, r_rb


def chi2_sf(x, df):
    """Survival function for chi-squared distribution (upper tail p-value).
    Uses the regularized incomplete gamma function approximation."""
    if x <= 0:
        return 1.0
    return 1.0 - _regularized_gamma(df / 2.0, x / 2.0)


def normal_sf(x):
    """Survival function for standard normal (upper tail)."""
    return 0.5 * math.erfc(x / math.sqrt(2.0))


def _regularized_gamma(a, x, max_iter=200):
    """Regularized lower incomplete gamma function P(a, x) via series expansion."""
    if x < 0:
        return 0.0
    if x == 0:
        return 0.0
    # Use series expansion for P(a, x)
    if x < a + 1:
        # Series representation
        term = 1.0 / a
        total = term
        for n in range(1, max_iter):
            term *= x / (a + n)
            total += term
            if abs(term) < 1e-12 * abs(total):
                break
        return total * math.exp(-x + a * math.log(x) - math.lgamma(a))
    else:
        # Continued fraction (Lentz's method)
        f = 1e-30
        C = f
        D = 1.0 / (x + 1.0 - a)
        f = C * D
        for n in range(1, max_iter):
            an = n * (a - n)
            bn = x + 2.0 * n + 1.0 - a
            D = bn + an * D
            if abs(D) < 1e-30:
                D = 1e-30
            C = bn + an / C
            if abs(C) < 1e-30:
                C = 1e-30
            D = 1.0 / D
            delta = C * D
            f *= delta
            if abs(delta - 1.0) < 1e-12:
                break
        # Q(a, x) = 1 - P(a, x) via continued fraction
        Q = math.exp(-x + a * math.log(x) - math.lgamma(a)) * f
        return 1.0 - Q  # P(a, x)


# --------------------------------------------------------------------------
# 5. Run analysis and produce report
# --------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("BRIDGING TEST: Default Rates Across Manuscript Sections")
    print("=" * 70)

    folio_section = parse_section_metadata(DATA_FILE)
    print(f"\nSection metadata: {len(folio_section)} folios")
    sec_counts = Counter(folio_section.values())
    for s, c in sorted(sec_counts.items(), key=lambda x: -x[1]):
        print(f"  {s} ({SECTION_NAMES.get(s, '?')}): {c} pages")

    records = load_corpus(DATA_FILE)
    page_stats = compute_page_rates(records, folio_section)
    print(f"\nPages with >= {MIN_WORDS_PER_PAGE} words: {len(page_stats)}")

    # ---- Results collector for markdown output ----
    report = []
    report.append("# Bridging Test: Default Fragment Rates Across Manuscript Sections\n")
    report.append("**Question:** Do the mechanical default-filler rates identified in Phase 1")
    report.append("differ across manuscript sections, independently recovering the")
    report.append("section-level vocabulary differences found by Montemurro & Zanette (2013)?\n")

    # ---- 3a. Rank all pages by ch-default rate ----
    sorted_by_ch = sorted(page_stats, key=lambda x: -x['slot2_default_rate'])

    report.append("## 1. Pages Ranked by ch-Default Rate\n")
    report.append("The ch-default rate = proportion of words where slot1 is empty AND slot2 is `ch`.\n")
    report.append("### Top 15 Pages (highest ch-default rate)")
    report.append("| Rank | Page | Section | ch-Rate | Words |")
    report.append("|------|------|---------|---------|-------|")
    for i, ps in enumerate(sorted_by_ch[:15]):
        report.append(f"| {i+1} | {ps['page']} | {ps['section']} ({SECTION_NAMES.get(ps['section'],'?')}) "
                      f"| {ps['slot2_default_rate']:.3f} | {ps['n_words']} |")

    report.append("\n### Bottom 15 Pages (lowest ch-default rate)")
    report.append("| Rank | Page | Section | ch-Rate | Words |")
    report.append("|------|------|---------|---------|-------|")
    for i, ps in enumerate(sorted_by_ch[-15:]):
        report.append(f"| {len(sorted_by_ch)-14+i} | {ps['page']} | {ps['section']} ({SECTION_NAMES.get(ps['section'],'?')}) "
                      f"| {ps['slot2_default_rate']:.3f} | {ps['n_words']} |")

    # ---- 4. Section-level statistics for each default ----
    report.append("\n## 2. Section-Level Default Rate Statistics\n")

    # For each metric, compute per-section stats
    metrics = [('slot2_default_rate', 'ch-default (S1 empty & S2=ch)')]
    for slot, frag in CANDIDATE_DEFAULTS.items():
        if slot != 'slot2':
            metrics.append((f'{slot}_default_rate', f'{slot} default ({frag})'))
    metrics.append(('overall_default_rate', 'Overall default (mean of 5)'))

    # Group pages by section
    section_pages = defaultdict(list)
    for ps in page_stats:
        section_pages[ps['section']].append(ps)

    sections_ordered = sorted(section_pages.keys(), key=lambda s: -len(section_pages[s]))

    for metric_key, metric_name in metrics:
        report.append(f"\n### {metric_name}\n")
        report.append("| Section | N pages | Median | IQR | Min | Max |")
        report.append("|---------|---------|--------|-----|-----|-----|")

        groups = []
        group_labels = []
        for sec in sections_ordered:
            vals = np.array([ps[metric_key] for ps in section_pages[sec]])
            groups.append(vals)
            group_labels.append(sec)
            med = np.median(vals)
            q25, q75 = np.percentile(vals, [25, 75])
            report.append(f"| {sec} ({SECTION_NAMES.get(sec,'?')}) | {len(vals)} "
                          f"| {med:.3f} | [{q25:.3f}, {q75:.3f}] "
                          f"| {np.min(vals):.3f} | {np.max(vals):.3f} |")

        # Kruskal-Wallis test
        valid_groups = [g for g in groups if len(g) >= 2]
        if len(valid_groups) >= 2:
            H, df, p = kruskal_wallis(valid_groups)
            # Epsilon-squared effect size
            N = sum(len(g) for g in valid_groups)
            eps2 = H / (N - 1) if N > 1 else 0
            report.append(f"\n**Kruskal-Wallis:** H({df}) = {H:.2f}, p = {p:.2e}, "
                          f"epsilon-squared = {eps2:.3f}")

            if p < 0.05:
                report.append(f"  -> Significant difference across sections (p < 0.05)")
            else:
                report.append(f"  -> No significant difference (p >= 0.05)")

    # ---- 5. Pairwise Mann-Whitney for ch-default (the flagship metric) ----
    report.append("\n## 3. Pairwise Comparisons: ch-Default Rate\n")
    report.append("Mann-Whitney U tests with Bonferroni correction.\n")

    ch_groups = {}
    for sec in sections_ordered:
        vals = np.array([ps['slot2_default_rate'] for ps in section_pages[sec]])
        if len(vals) >= 3:  # need at least 3 pages
            ch_groups[sec] = vals

    pairs = list(combinations(ch_groups.keys(), 2))
    n_comparisons = len(pairs)
    alpha_bonf = 0.05 / n_comparisons if n_comparisons > 0 else 0.05

    report.append(f"Number of comparisons: {n_comparisons}, "
                  f"Bonferroni alpha: {alpha_bonf:.4f}\n")
    report.append("| Pair | n1 | n2 | Median1 | Median2 | U | z | p | p_bonf | r_rb | Sig? |")
    report.append("|------|----|----|---------|---------|---|---|---|--------|------|------|")

    significant_pairs = []
    for s1, s2 in pairs:
        g1, g2 = ch_groups[s1], ch_groups[s2]
        U, z, p, r_rb = mann_whitney_u(g1, g2)
        p_bonf = min(p * n_comparisons, 1.0)
        sig = "YES" if p_bonf < 0.05 else "no"
        if p_bonf < 0.05:
            significant_pairs.append((s1, s2, r_rb, p_bonf))
        report.append(f"| {s1} vs {s2} | {len(g1)} | {len(g2)} "
                      f"| {np.median(g1):.3f} | {np.median(g2):.3f} "
                      f"| {U:.0f} | {z:.2f} | {p:.2e} | {p_bonf:.2e} "
                      f"| {r_rb:.3f} | {sig} |")

    # ---- 6. Interpretation ----
    report.append("\n## 4. Interpretation\n")

    if significant_pairs:
        report.append(f"**{len(significant_pairs)} of {n_comparisons} pairwise comparisons "
                      f"are significant** after Bonferroni correction:\n")
        for s1, s2, r_rb, p_bonf in significant_pairs:
            higher = s1 if np.median(ch_groups[s1]) > np.median(ch_groups[s2]) else s2
            lower = s2 if higher == s1 else s1
            report.append(f"- **{SECTION_NAMES.get(higher, higher)}** has significantly higher "
                          f"ch-default rate than **{SECTION_NAMES.get(lower, lower)}** "
                          f"(|r_rb| = {abs(r_rb):.3f}, p_bonf = {p_bonf:.2e})")
    else:
        report.append("No pairwise comparisons reached significance after Bonferroni correction.")

    # Comparison with Montemurro & Zanette
    report.append("\n## 5. Comparison with Montemurro & Zanette (2013)\n")
    report.append("M&Z found that Voynich vocabulary differs significantly across sections,")
    report.append("using information-theoretic measures (semantic content clustering).")
    report.append("Their key finding: Herbal, Biological, and Pharmaceutical/Stars sections")
    report.append("have distinct vocabulary profiles.\n")

    # Compute a summary statistic: range of median ch-default rates
    medians = {sec: np.median([ps['slot2_default_rate'] for ps in section_pages[sec]])
               for sec in sections_ordered}
    report.append("**Section median ch-default rates:**\n")
    for sec in sorted(medians, key=lambda s: -medians[s]):
        report.append(f"- {sec} ({SECTION_NAMES.get(sec, '?')}): {medians[sec]:.3f}")

    report.append("\n**Assessment:** The ch-default rate (a purely structural metric derived from")
    report.append("slot decomposition) is a novel measure independent of vocabulary/semantics.")

    ch_valid = [g for g in [np.array([ps['slot2_default_rate'] for ps in section_pages[sec]])
                            for sec in sections_ordered] if len(g) >= 2]
    if len(ch_valid) >= 2:
        H, df, p = kruskal_wallis(ch_valid)
        if p < 0.05:
            report.append(f"The Kruskal-Wallis test confirms significant variation (p = {p:.2e}),")
            report.append("independently recovering section-level structural differences that")
            report.append("parallel M&Z's semantic findings. This supports the hypothesis that")
            report.append("sections differ not just in *what* glyphs are used, but in the")
            report.append("*combinatorial structure* -- specifically, the rate at which default")
            report.append("fillers appear. This is consistent with a table-based generator whose")
            report.append("parameters (table contents or selection rules) vary by section.")
        else:
            report.append(f"The Kruskal-Wallis test does NOT show significant variation (p = {p:.2e}).")
            report.append("The default rate metric does not independently recover section differences.")
            report.append("This could mean: (a) defaults are globally uniform, which would still be")
            report.append("consistent with a single generator, or (b) the metric lacks power.")

    # ---- 7. Section-specific extreme pages ----
    report.append("\n## 6. Extreme Pages by Section\n")
    report.append("Pages with unusually high or low ch-default rates within their section.\n")
    for sec in sections_ordered:
        vals = [(ps['page'], ps['slot2_default_rate'], ps['n_words']) for ps in section_pages[sec]]
        if len(vals) < 5:
            continue
        vals_sorted = sorted(vals, key=lambda x: -x[1])
        report.append(f"### {sec} ({SECTION_NAMES.get(sec, '?')}) -- {len(vals)} pages")
        rates = [v[1] for v in vals]
        med = np.median(rates)
        report.append(f"Median: {med:.3f}\n")
        report.append(f"**Highest:** {vals_sorted[0][0]} ({vals_sorted[0][1]:.3f}, n={vals_sorted[0][2]}), "
                      f"{vals_sorted[1][0]} ({vals_sorted[1][1]:.3f}, n={vals_sorted[1][2]})")
        report.append(f"**Lowest:** {vals_sorted[-1][0]} ({vals_sorted[-1][1]:.3f}, n={vals_sorted[-1][2]}), "
                      f"{vals_sorted[-2][0]} ({vals_sorted[-2][1]:.3f}, n={vals_sorted[-2][2]})")
        report.append("")

    # ---- Print and save ----
    report_text = "\n".join(report) + "\n"
    print("\n" + report_text)

    os.makedirs(OUT_DIR, exist_ok=True)
    out_path = os.path.join(OUT_DIR, 'bridging_test_findings.md')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    print(f"\nReport saved to {out_path}")


if __name__ == '__main__':
    main()
