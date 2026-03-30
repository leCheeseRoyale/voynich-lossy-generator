"""
Phase 3: Classify Artifacts — Anomaly Detection and Distribution Analysis.

Tags every word token with one of:
  consistent, slot4_violation, fallback_only, repetition_artifact, hapax

Then analyzes per-page anomaly rates, section correlations, and clustering.
"""

import re
import sys
import os
import json
import math
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(__file__))
from parse_ivtff import parse_ivtff
from slot_analysis import WORD_PATTERN, SIMPLE_PATTERN, decompose_word

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

def slot4_fits_BET(fragment):
    """Return True if slot4 fragment matches B?E*T? pattern."""
    if not fragment:
        return True  # empty slot4 is fine
    tokens = tokenize_slot4(fragment)
    # Check rejoining
    if ''.join(tokens) != fragment:
        return False
    # Classify
    classes = []
    for t in tokens:
        if t in BENCH:
            classes.append('B')
        elif t in ('e', 'ee'):
            classes.append('E')
        elif t in TERMINAL:
            classes.append('T')
        else:
            classes.append('?')
    pattern = ''.join(classes)
    return bool(re.match(r'^B?E*T?$', pattern))


# ---- Section metadata parsing ----

def parse_sections(filepath):
    """Parse IVTFF headers to extract folio -> section mapping."""
    folio_section = {}
    with open(filepath, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')
            # Match folio headers like: <f1r>  <! $Q=A ... $I=T ...>
            m = re.match(r'^<(f\d+[rv]\d?)>\s+<!\s+(.*?)>', line)
            if m:
                folio = m.group(1)
                meta = m.group(2)
                # Extract $I=X
                im = re.search(r'\$I=(\w)', meta)
                if im:
                    folio_section[folio] = im.group(1)
                else:
                    folio_section[folio] = '?'
    return folio_section


# ---- Main classification ----

def classify_corpus(filepath):
    """Classify every token and return structured results."""
    words = parse_ivtff(filepath)
    folio_section = parse_sections(filepath)

    # Build vocabulary counts
    word_list = [w for _, w in words]
    vocab = Counter(word_list)
    hapax_types = {w for w, c in vocab.items() if c == 1}

    # Pre-classify each word type
    type_class = {}  # word -> base classification (before repetition/hapax)
    for word in vocab:
        result = decompose_word(word)
        if result is None:
            type_class[word] = 'fallback_only'  # shouldn't happen with SIMPLE_PATTERN
            continue
        if '_fallback' in result:
            type_class[word] = 'fallback_only'
        else:
            # Check slot4
            s4 = result.get('slot4', '')
            if slot4_fits_BET(s4):
                type_class[word] = 'consistent'
            else:
                type_class[word] = 'slot4_violation'

    # Now tag each token in order (need sequential scan for repetition)
    tagged = []  # list of (locus, word, tag)
    # Also track page info
    page_tokens = defaultdict(list)  # page -> list of (word, tag)

    for i, (locus, word) in enumerate(words):
        page = locus.split('.')[0]  # e.g. f1r
        tag = type_class.get(word, 'fallback_only')
        tagged.append((locus, word, tag, page))
        page_tokens[page].append((word, tag))

    # Mark repetition artifacts: 3+ consecutive identical tokens
    # Override tag for those tokens
    n = len(tagged)
    i = 0
    while i < n:
        j = i + 1
        while j < n and tagged[j][1] == tagged[i][1]:
            j += 1
        run_len = j - i
        if run_len >= 3:
            for k in range(i, j):
                locus, word, old_tag, page = tagged[k]
                tagged[k] = (locus, word, 'repetition_artifact', page)
        i = j

    # Mark hapax (if not already tagged as repetition_artifact)
    for i in range(n):
        locus, word, tag, page = tagged[i]
        if tag != 'repetition_artifact' and word in hapax_types:
            tagged[i] = (locus, word, 'hapax', page)

    return tagged, vocab, folio_section


def analyze(tagged, vocab, folio_section):
    """Compute all statistics and print results."""
    results = {}

    # ---- Task 3.1: Token and type counts per category ----
    tag_token_counts = Counter()
    tag_type_words = defaultdict(Counter)  # tag -> word -> count

    for locus, word, tag, page in tagged:
        tag_token_counts[tag] += 1
        tag_type_words[tag][word] += 1

    total_tokens = len(tagged)
    total_types = len(vocab)

    print("=" * 70)
    print("PHASE 3.1: ANOMALY CLASSIFICATION")
    print("=" * 70)

    print(f"\nCorpus: {total_tokens} tokens, {total_types} types\n")

    print(f"{'Category':<22s} {'Tokens':>8s} {'%':>7s}  {'Types':>7s} {'%':>7s}")
    print("-" * 55)
    for cat in ['consistent', 'slot4_violation', 'fallback_only', 'repetition_artifact', 'hapax']:
        tok = tag_token_counts[cat]
        typ = len(tag_type_words[cat])
        print(f"{cat:<22s} {tok:8d} {100*tok/total_tokens:6.1f}%  {typ:7d} {100*typ/total_types:6.1f}%")

    # Top 20 most frequent words per anomalous category
    anomalous_cats = ['slot4_violation', 'fallback_only', 'repetition_artifact', 'hapax']
    top20 = {}
    for cat in anomalous_cats:
        words_in_cat = tag_type_words[cat]
        top = words_in_cat.most_common(20)
        top20[cat] = top
        print(f"\nTop 20 words — {cat}:")
        for w, c in top:
            print(f"  {w:<25s} {c:5d}")

    results['token_counts'] = dict(tag_token_counts)
    results['type_counts'] = {cat: len(tag_type_words[cat]) for cat in tag_token_counts}
    results['top20'] = {cat: [(w, c) for w, c in top20[cat]] for cat in anomalous_cats}

    # ---- Task 3.2: Per-page anomaly rates ----
    print("\n" + "=" * 70)
    print("PHASE 3.2: ARTIFACT DISTRIBUTION ANALYSIS")
    print("=" * 70)

    page_tag_counts = defaultdict(Counter)
    page_total = Counter()
    for locus, word, tag, page in tagged:
        page_tag_counts[page][tag] += 1
        page_total[page] += 1

    pages = sorted(page_total.keys(), key=lambda p: (
        int(re.search(r'\d+', p).group()),
        p
    ))

    # Compute per-page rates
    page_rates = {}
    for page in pages:
        total_p = page_total[page]
        rates = {}
        for cat in ['slot4_violation', 'fallback_only', 'repetition_artifact', 'hapax']:
            rates[cat] = page_tag_counts[page].get(cat, 0) / total_p if total_p > 0 else 0
        rates['any_anomaly'] = sum(page_tag_counts[page].get(c, 0) for c in anomalous_cats) / total_p
        page_rates[page] = rates

    # Print top 10 pages by anomaly rate
    print("\nTop 15 pages by overall anomaly rate:")
    print(f"{'Page':<10s} {'Words':>6s} {'Anom%':>6s}  {'S4viol':>6s} {'Fallbk':>6s} {'Repet':>6s} {'Hapax':>6s}  {'Section':>7s}")
    print("-" * 70)
    for page in sorted(pages, key=lambda p: -page_rates[p]['any_anomaly'])[:15]:
        r = page_rates[page]
        sec = folio_section.get(page, '?')
        print(f"{page:<10s} {page_total[page]:6d} {100*r['any_anomaly']:5.1f}%  "
              f"{100*r['slot4_violation']:5.1f}% {100*r['fallback_only']:5.1f}% "
              f"{100*r['repetition_artifact']:5.1f}% {100*r['hapax']:5.1f}%  {sec:>7s}")

    # ---- Chi-squared test for clustering ----
    print("\n--- Chi-squared test: do anomalies cluster on specific pages? ---")

    for cat in anomalous_cats:
        # Observed: count of cat tokens per page
        # Expected: total_page * (global rate of cat)
        global_rate = tag_token_counts[cat] / total_tokens
        chi2 = 0
        df = 0
        for page in pages:
            total_p = page_total[page]
            if total_p < 5:
                continue  # skip very short pages
            observed = page_tag_counts[page].get(cat, 0)
            expected = total_p * global_rate
            if expected > 0:
                chi2 += (observed - expected) ** 2 / expected
                df += 1
        df = max(df - 1, 1)
        # Approximate p-value using Wilson-Hilferty normal approximation
        # For large df, chi2/df ~ N(1, 2/df)
        z = ((chi2 / df) ** (1/3) - (1 - 2 / (9 * df))) / math.sqrt(2 / (9 * df)) if df > 0 else 0
        # One-sided p-value from z
        # Use complementary error function approximation
        p_approx = 0.5 * math.erfc(z / math.sqrt(2))
        sig = "***" if p_approx < 0.001 else "**" if p_approx < 0.01 else "*" if p_approx < 0.05 else "n.s."
        print(f"  {cat:<22s}  chi2={chi2:10.1f}  df={df:4d}  z={z:6.2f}  p~{p_approx:.4f}  {sig}")

    # ---- Correlation with section ----
    print("\n--- Anomaly rates by manuscript section ---")
    section_tag_counts = defaultdict(Counter)
    section_total = Counter()
    for page in pages:
        sec = folio_section.get(page, '?')
        for cat in tag_token_counts:
            section_tag_counts[sec][cat] += page_tag_counts[page].get(cat, 0)
        section_total[sec] += page_total[page]

    section_names = {'H': 'Herbal', 'S': 'Stars', 'B': 'Biological',
                     'P': 'Pharmaceutical', 'Z': 'Zodiac', 'C': 'Cosmological',
                     'A': 'Astronomical', 'T': 'Text'}

    print(f"{'Section':<15s} {'Tokens':>7s} {'Consist%':>9s} {'S4viol%':>8s} {'Fallbk%':>8s} {'Repet%':>7s} {'Hapax%':>7s} {'AnyAnom%':>9s}")
    print("-" * 80)
    for sec in sorted(section_total.keys()):
        tot = section_total[sec]
        if tot == 0:
            continue
        name = section_names.get(sec, sec)
        cons = section_tag_counts[sec].get('consistent', 0)
        s4v = section_tag_counts[sec].get('slot4_violation', 0)
        fb = section_tag_counts[sec].get('fallback_only', 0)
        rep = section_tag_counts[sec].get('repetition_artifact', 0)
        hap = section_tag_counts[sec].get('hapax', 0)
        anom = s4v + fb + rep + hap
        print(f"{name:<15s} {tot:7d} {100*cons/tot:8.1f}% {100*s4v/tot:7.1f}% "
              f"{100*fb/tot:7.1f}% {100*rep/tot:6.1f}% {100*hap/tot:6.1f}% {100*anom/tot:8.1f}%")

    # ---- Correlation: page word count vs anomaly rate ----
    print("\n--- Correlation: page word count vs anomaly rate ---")
    page_sizes = []
    page_anom_rates = []
    for page in pages:
        tot = page_total[page]
        if tot < 5:
            continue
        anom = sum(page_tag_counts[page].get(c, 0) for c in anomalous_cats)
        page_sizes.append(tot)
        page_anom_rates.append(anom / tot)

    # Pearson correlation (manual, no numpy needed)
    n = len(page_sizes)
    mean_x = sum(page_sizes) / n
    mean_y = sum(page_anom_rates) / n
    cov_xy = sum((page_sizes[i] - mean_x) * (page_anom_rates[i] - mean_y) for i in range(n)) / n
    std_x = math.sqrt(sum((x - mean_x) ** 2 for x in page_sizes) / n)
    std_y = math.sqrt(sum((y - mean_y) ** 2 for y in page_anom_rates) / n)
    r_size = cov_xy / (std_x * std_y) if std_x * std_y > 0 else 0
    # t-test for significance
    t_stat = r_size * math.sqrt((n - 2) / (1 - r_size**2)) if abs(r_size) < 1 else float('inf')
    print(f"  r(page_size, anomaly_rate) = {r_size:.4f}  (n={n}, t={t_stat:.2f})")
    print(f"  {'Significant' if abs(t_stat) > 1.96 else 'Not significant'} at p<0.05")

    # Per-category correlations with page size
    for cat in anomalous_cats:
        cat_rates = []
        for page in pages:
            tot = page_total[page]
            if tot < 5:
                continue
            cat_rates.append(page_tag_counts[page].get(cat, 0) / tot)
        mean_cy = sum(cat_rates) / n
        cov_cxy = sum((page_sizes[i] - mean_x) * (cat_rates[i] - mean_cy) for i in range(n)) / n
        std_cy = math.sqrt(sum((y - mean_cy) ** 2 for y in cat_rates) / n)
        r_cat = cov_cxy / (std_x * std_cy) if std_x * std_cy > 0 else 0
        print(f"  r(page_size, {cat}) = {r_cat:.4f}")

    # ---- Correlation: fallback rate vs other anomaly rates ----
    print("\n--- Correlation: fallback rate vs other anomaly rates ---")
    fb_rates = []
    other_rates = []
    for page in pages:
        tot = page_total[page]
        if tot < 5:
            continue
        fb_r = page_tag_counts[page].get('fallback_only', 0) / tot
        other_r = sum(page_tag_counts[page].get(c, 0) for c in ['slot4_violation', 'repetition_artifact', 'hapax']) / tot
        fb_rates.append(fb_r)
        other_rates.append(other_r)

    mean_fb = sum(fb_rates) / n
    mean_ot = sum(other_rates) / n
    cov_fo = sum((fb_rates[i] - mean_fb) * (other_rates[i] - mean_ot) for i in range(n)) / n
    std_fb = math.sqrt(sum((y - mean_fb) ** 2 for y in fb_rates) / n)
    std_ot = math.sqrt(sum((y - mean_ot) ** 2 for y in other_rates) / n)
    r_fo = cov_fo / (std_fb * std_ot) if std_fb * std_ot > 0 else 0
    print(f"  r(fallback_rate, other_anomaly_rate) = {r_fo:.4f}")

    # ---- Correlation: default (fallback) rate vs hapax rate ----
    hapax_rates = []
    for page in pages:
        tot = page_total[page]
        if tot < 5:
            continue
        hapax_rates.append(page_tag_counts[page].get('hapax', 0) / tot)

    mean_hap = sum(hapax_rates) / n
    cov_fh = sum((fb_rates[i] - mean_fb) * (hapax_rates[i] - mean_hap) for i in range(n)) / n
    std_hap = math.sqrt(sum((y - mean_hap) ** 2 for y in hapax_rates) / n)
    r_fh = cov_fh / (std_fb * std_hap) if std_fb * std_hap > 0 else 0
    print(f"  r(fallback_rate, hapax_rate) = {r_fh:.4f}")

    return results, page_rates, section_tag_counts, section_total


def generate_findings(results, tagged, vocab, folio_section, page_rates,
                      section_tag_counts, section_total, outpath):
    """Generate phase3_findings.md."""
    tag_token_counts = Counter()
    tag_type_words = defaultdict(Counter)
    page_tag_counts = defaultdict(Counter)
    page_total = Counter()
    anomalous_cats = ['slot4_violation', 'fallback_only', 'repetition_artifact', 'hapax']

    for locus, word, tag, page in tagged:
        tag_token_counts[tag] += 1
        tag_type_words[tag][word] += 1
        page_tag_counts[page][tag] += 1
        page_total[page] += 1

    total_tokens = len(tagged)
    total_types = len(vocab)

    section_names = {'H': 'Herbal', 'S': 'Stars', 'B': 'Biological',
                     'P': 'Pharmaceutical', 'Z': 'Zodiac', 'C': 'Cosmological',
                     'A': 'Astronomical', 'T': 'Text'}

    lines = []
    lines.append("# Phase 3: Artifact Classification Findings\n")
    lines.append(f"Corpus: {total_tokens} tokens, {total_types} types\n")

    lines.append("## 3.1 Anomaly Classification\n")
    lines.append("### Token and type counts by category\n")
    lines.append("| Category | Tokens | % | Types | % |")
    lines.append("|----------|-------:|--:|------:|--:|")
    for cat in ['consistent', 'slot4_violation', 'fallback_only', 'repetition_artifact', 'hapax']:
        tok = tag_token_counts[cat]
        typ = len(tag_type_words[cat])
        lines.append(f"| {cat} | {tok} | {100*tok/total_tokens:.1f}% | {typ} | {100*typ/total_types:.1f}% |")

    for cat in anomalous_cats:
        lines.append(f"\n### Top 20 words: {cat}\n")
        lines.append("| Word | Count |")
        lines.append("|------|------:|")
        for w, c in tag_type_words[cat].most_common(20):
            lines.append(f"| {w} | {c} |")

    lines.append("\n## 3.2 Artifact Distribution Analysis\n")

    # Section table
    lines.append("### Anomaly rates by manuscript section\n")
    lines.append("| Section | Tokens | Consistent% | S4-viol% | Fallback% | Repet% | Hapax% | Any-anom% |")
    lines.append("|---------|-------:|------------:|---------:|----------:|-------:|-------:|----------:|")
    for sec in sorted(section_total.keys()):
        tot = section_total[sec]
        if tot == 0:
            continue
        name = section_names.get(sec, sec)
        cons = section_tag_counts[sec].get('consistent', 0)
        s4v = section_tag_counts[sec].get('slot4_violation', 0)
        fb = section_tag_counts[sec].get('fallback_only', 0)
        rep = section_tag_counts[sec].get('repetition_artifact', 0)
        hap = section_tag_counts[sec].get('hapax', 0)
        anom = s4v + fb + rep + hap
        lines.append(f"| {name} | {tot} | {100*cons/tot:.1f}% | {100*s4v/tot:.1f}% | "
                     f"{100*fb/tot:.1f}% | {100*rep/tot:.1f}% | {100*hap/tot:.1f}% | {100*anom/tot:.1f}% |")

    # Top anomalous pages
    pages = sorted(page_total.keys(), key=lambda p: (int(re.search(r'\d+', p).group()), p))
    lines.append("\n### Top 15 pages by anomaly rate\n")
    lines.append("| Page | Words | Anom% | S4-viol% | Fallback% | Repet% | Hapax% | Section |")
    lines.append("|------|------:|------:|---------:|----------:|-------:|-------:|---------|")
    for page in sorted(pages, key=lambda p: -page_rates[p]['any_anomaly'])[:15]:
        r = page_rates[page]
        sec = section_names.get(folio_section.get(page, '?'), '?')
        lines.append(f"| {page} | {page_total[page]} | {100*r['any_anomaly']:.1f}% | "
                     f"{100*r['slot4_violation']:.1f}% | {100*r['fallback_only']:.1f}% | "
                     f"{100*r['repetition_artifact']:.1f}% | {100*r['hapax']:.1f}% | {sec} |")

    # Chi-squared summary
    lines.append("\n### Chi-squared clustering tests\n")
    lines.append("Tests whether anomalous tokens cluster on specific pages vs. uniform distribution.\n")

    global_rates = {cat: tag_token_counts[cat] / total_tokens for cat in anomalous_cats}
    for cat in anomalous_cats:
        chi2 = 0
        df = 0
        for page in pages:
            tot = page_total[page]
            if tot < 5:
                continue
            obs = page_tag_counts[page].get(cat, 0)
            exp = tot * global_rates[cat]
            if exp > 0:
                chi2 += (obs - exp) ** 2 / exp
                df += 1
        df = max(df - 1, 1)
        z = ((chi2 / df) ** (1/3) - (1 - 2 / (9 * df))) / math.sqrt(2 / (9 * df)) if df > 0 else 0
        p_approx = 0.5 * math.erfc(z / math.sqrt(2))
        sig = "p<0.001" if p_approx < 0.001 else "p<0.01" if p_approx < 0.01 else "p<0.05" if p_approx < 0.05 else "n.s."
        lines.append(f"- **{cat}**: chi2={chi2:.1f}, df={df}, {sig}")

    # Correlation summary
    lines.append("\n### Correlations\n")

    # Recompute correlations for the report
    ps = []
    ar = []
    fb_r = []
    hap_r = []
    for page in pages:
        tot = page_total[page]
        if tot < 5:
            continue
        ps.append(tot)
        anom = sum(page_tag_counts[page].get(c, 0) for c in anomalous_cats)
        ar.append(anom / tot)
        fb_r.append(page_tag_counts[page].get('fallback_only', 0) / tot)
        hap_r.append(page_tag_counts[page].get('hapax', 0) / tot)

    def pearson(xs, ys):
        n = len(xs)
        mx = sum(xs) / n
        my = sum(ys) / n
        cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / n
        sx = math.sqrt(sum((x - mx)**2 for x in xs) / n)
        sy = math.sqrt(sum((y - my)**2 for y in ys) / n)
        return cov / (sx * sy) if sx * sy > 0 else 0

    r1 = pearson(ps, ar)
    r2 = pearson(fb_r, hap_r)
    lines.append(f"- Page word count vs. anomaly rate: r = {r1:.4f}")
    lines.append(f"- Fallback rate vs. hapax rate: r = {r2:.4f}")

    # Key findings
    lines.append("\n## Key Findings\n")

    consistent_pct = 100 * tag_token_counts['consistent'] / total_tokens
    lines.append(f"1. **{consistent_pct:.1f}% of tokens are fully consistent** with the 5-slot + B?E*T? model.")

    total_anom = sum(tag_token_counts[c] for c in anomalous_cats)
    lines.append(f"2. **{100*total_anom/total_tokens:.1f}% of tokens show some anomaly** "
                 f"({tag_token_counts['hapax']} hapax, "
                 f"{tag_token_counts['fallback_only']} fallback-only, "
                 f"{tag_token_counts['slot4_violation']} slot4 violations, "
                 f"{tag_token_counts['repetition_artifact']} repetition artifacts).")

    # Find most anomalous section
    worst_sec = max(section_total.keys(),
                    key=lambda s: sum(section_tag_counts[s].get(c, 0) for c in anomalous_cats) / section_total[s]
                    if section_total[s] > 0 else 0)
    worst_rate = sum(section_tag_counts[worst_sec].get(c, 0) for c in anomalous_cats) / section_total[worst_sec]
    lines.append(f"3. **Most anomalous section**: {section_names.get(worst_sec, worst_sec)} "
                 f"({100*worst_rate:.1f}% anomaly rate).")

    lines.append(f"4. **Page-size correlation**: r={r1:.4f} — "
                 f"{'longer pages tend to have lower anomaly rates (more regular text)' if r1 < -0.1 else 'longer pages tend to have higher anomaly rates' if r1 > 0.1 else 'no meaningful relationship between page length and anomaly rate'}.")

    lines.append(f"5. **Fallback-hapax correlation**: r={r2:.4f} — "
                 f"{'pages with more fallback words also have more hapaxes, suggesting shared source of irregularity' if r2 > 0.3 else 'fallback and hapax rates are only weakly related across pages'}.")

    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')
    print(f"\nFindings saved to {outpath}")


if __name__ == '__main__':
    basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath = os.path.join(basedir, 'data', 'IT2a-n.txt')
    outpath = os.path.join(basedir, 'analysis', 'phase3_findings.md')

    tagged, vocab, folio_section = classify_corpus(filepath)
    results, page_rates, section_tag_counts, section_total = analyze(tagged, vocab, folio_section)
    generate_findings(results, tagged, vocab, folio_section, page_rates,
                      section_tag_counts, section_total, outpath)
