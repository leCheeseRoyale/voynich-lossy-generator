"""
Cross-transcription comparison: IT (Takahashi) vs ZL (Zandbergen-Landini).

Tests whether the 5-slot decomposition results are transcription-dependent
by comparing slot match rates, hapax behavior, and locus-level agreement.
"""

import re
import sys
import os
from collections import Counter, defaultdict

# Add scripts dir to path so we can import existing modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from slot_analysis import decompose_word, WORD_PATTERN


def parse_ivtff_clean(filepath):
    """Parse IVTFF file with extra cleaning for ZL-style annotations.

    Returns list of (locus, word) tuples.
    ZL uses commas within words for uncertain glyph boundaries,
    [x:y] for alternative readings, and <!...> for inline comments.
    """
    words = []

    with open(filepath, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')

            if line.startswith('#') or not line.strip():
                continue

            # Folio header
            if re.match(r'^<(f\d+[rv]\d?)>\s', line):
                continue

            # Text line
            line_match = re.match(r'^<(f\d+[rv]\d?\.\d+),[^>]+>\s+(.*)', line)
            if not line_match:
                continue

            locus = line_match.group(1)
            text = line_match.group(2)

            # Remove inline comments <!...>
            text = re.sub(r'<![^>]*>', '', text)

            # Remove IVTFF markers
            text = re.sub(r'<%>', '', text)
            text = re.sub(r'<\$>', '', text)
            text = re.sub(r'<->', '.', text)

            # Handle alternative readings [x:y] — take first reading
            # Also handles [{x}:y] patterns
            text = re.sub(r'\[\{?([^:\]]*?)\}?:[^\]]*\]', r'\1', text)

            # Remove remaining tags
            text = re.sub(r'<[^>]*>', '', text)

            # Remove uncertainty brackets
            text = re.sub(r'[{}]', '', text)

            # Remove commas within words (ZL uses these for uncertain boundaries)
            text = re.sub(r',', '', text)

            # Remove @ references that may remain (e.g., @254;)
            text = re.sub(r'@\d+;?', '', text)

            # Split on dots
            raw_words = text.split('.')
            for w in raw_words:
                w = w.strip()
                if not w:
                    continue
                if re.match(r'^[\?\s\*]+$', w):
                    continue
                # Skip words containing ? (uncertain readings)
                # Keep them but mark — actually, keep them for comparison
                words.append((locus, w))

    return words


def basic_corpus_stats(words, label):
    """Compute and print basic corpus statistics."""
    word_list = [w for _, w in words]
    vocab = Counter(word_list)
    hapax = sum(1 for c in vocab.values() if c == 1)

    stats = {
        'label': label,
        'total_tokens': len(word_list),
        'unique_types': len(vocab),
        'hapax_count': hapax,
        'hapax_pct': 100 * hapax / len(vocab) if vocab else 0,
        'ttr': len(vocab) / len(word_list) if word_list else 0,
        'vocab': vocab,
    }

    print(f"\n{'='*60}")
    print(f"  Corpus: {label}")
    print(f"{'='*60}")
    print(f"  Total tokens:    {stats['total_tokens']:,}")
    print(f"  Unique types:    {stats['unique_types']:,}")
    print(f"  Hapax legomena:  {stats['hapax_count']:,} ({stats['hapax_pct']:.1f}% of types)")
    print(f"  Type-token ratio: {stats['ttr']:.4f}")

    return stats


def slot_decomposition_stats(vocab, label):
    """Run 5-slot decomposition on a vocabulary, return stats."""
    match_tokens = 0
    fallback_tokens = 0
    fail_tokens = 0

    match_types = 0
    fallback_types = 0
    fail_types = 0

    matched_words = set()
    fallback_words = set()
    failed_words = set()

    for word, count in vocab.items():
        result = decompose_word(word)
        if result is None:
            fail_tokens += count
            fail_types += 1
            failed_words.add(word)
        elif '_fallback' in result:
            fallback_tokens += count
            fallback_types += 1
            fallback_words.add(word)
        else:
            match_tokens += count
            match_types += 1
            matched_words.add(word)

    total_tokens = match_tokens + fallback_tokens + fail_tokens
    total_types = match_types + fallback_types + fail_types

    print(f"\n--- 5-Slot Decomposition: {label} ---")
    print(f"  By tokens: matched={match_tokens} ({100*match_tokens/total_tokens:.1f}%), "
          f"fallback={fallback_tokens} ({100*fallback_tokens/total_tokens:.1f}%), "
          f"fail={fail_tokens} ({100*fail_tokens/total_tokens:.1f}%)")
    print(f"  By types:  matched={match_types} ({100*match_types/total_types:.1f}%), "
          f"fallback={fallback_types} ({100*fallback_types/total_types:.1f}%), "
          f"fail={fail_types} ({100*fail_types/total_types:.1f}%)")

    return {
        'match_tokens': match_tokens, 'fallback_tokens': fallback_tokens, 'fail_tokens': fail_tokens,
        'match_types': match_types, 'fallback_types': fallback_types, 'fail_types': fail_types,
        'total_tokens': total_tokens, 'total_types': total_types,
        'matched_words': matched_words, 'fallback_words': fallback_words, 'failed_words': failed_words,
        'match_token_pct': 100*match_tokens/total_tokens,
        'fallback_token_pct': 100*fallback_tokens/total_tokens,
        'match_type_pct': 100*match_types/total_types,
    }


def hapax_fallback_analysis(vocab, label):
    """Analyze what fraction of hapax legomena are fallback-only."""
    hapax_words = [w for w, c in vocab.items() if c == 1]

    hapax_match = 0
    hapax_fallback = 0
    hapax_fail = 0
    fb_hapax_list = []

    for word in hapax_words:
        result = decompose_word(word)
        if result is None:
            hapax_fail += 1
        elif '_fallback' in result:
            hapax_fallback += 1
            fb_hapax_list.append(word)
        else:
            hapax_match += 1

    total = len(hapax_words)
    print(f"\n--- Hapax Fallback Analysis: {label} ---")
    print(f"  Total hapax: {total}")
    print(f"  Hapax matched 5-slot: {hapax_match} ({100*hapax_match/total:.1f}%)")
    print(f"  Hapax fallback-only:  {hapax_fallback} ({100*hapax_fallback/total:.1f}%)")
    print(f"  Hapax failed:         {hapax_fail} ({100*hapax_fail/total:.1f}%)")

    return {
        'total_hapax': total,
        'hapax_match': hapax_match,
        'hapax_fallback': hapax_fallback,
        'hapax_fail': hapax_fail,
        'hapax_fallback_pct': 100*hapax_fallback/total if total else 0,
        'fb_hapax_list': fb_hapax_list,
    }


def locus_comparison(it_words, zl_words):
    """Compare IT and ZL at the locus level."""
    # Build locus -> word list mappings
    # A locus can have multiple words; we need word position within locus
    it_locus = defaultdict(list)
    zl_locus = defaultdict(list)

    for locus, word in it_words:
        it_locus[locus].append(word)
    for locus, word in zl_words:
        zl_locus[locus].append(word)

    shared_loci = set(it_locus.keys()) & set(zl_locus.keys())

    # Token-level agreement: for each shared locus, compare word by word
    agree = 0
    disagree = 0
    it_only_tokens = 0
    zl_only_tokens = 0
    disagreement_pairs = []

    for locus in shared_loci:
        it_ws = it_locus[locus]
        zl_ws = zl_locus[locus]
        min_len = min(len(it_ws), len(zl_ws))

        for i in range(min_len):
            # Strip ? from both for comparison (uncertain glyphs)
            it_clean = it_ws[i].replace('?', '')
            zl_clean = zl_ws[i].replace('?', '')
            if it_clean == zl_clean:
                agree += 1
            else:
                disagree += 1
                disagreement_pairs.append((locus, i, it_ws[i], zl_ws[i]))

        it_only_tokens += max(0, len(it_ws) - min_len)
        zl_only_tokens += max(0, len(zl_ws) - min_len)

    total_compared = agree + disagree
    agreement_rate = 100 * agree / total_compared if total_compared else 0

    print(f"\n{'='*60}")
    print(f"  Locus-Level Comparison")
    print(f"{'='*60}")
    print(f"  IT loci:     {len(it_locus)}")
    print(f"  ZL loci:     {len(zl_locus)}")
    print(f"  Shared loci: {len(shared_loci)}")
    print(f"  IT-only loci: {len(it_locus) - len(shared_loci)}")
    print(f"  ZL-only loci: {len(zl_locus) - len(shared_loci)}")
    print(f"\n  Token-level comparison (shared loci, aligned positions):")
    print(f"  Agree:    {agree:,} ({agreement_rate:.1f}%)")
    print(f"  Disagree: {disagree:,} ({100*disagree/total_compared:.1f}%)")
    print(f"  IT extra tokens: {it_only_tokens}")
    print(f"  ZL extra tokens: {zl_only_tokens}")

    # Show sample disagreements
    print(f"\n  Sample disagreements (first 20):")
    for locus, idx, it_w, zl_w in disagreement_pairs[:20]:
        print(f"    {locus}[{idx}]: IT={it_w:20s} ZL={zl_w}")

    return {
        'shared_loci': len(shared_loci),
        'agree': agree,
        'disagree': disagree,
        'agreement_rate': agreement_rate,
        'disagreement_pairs': disagreement_pairs,
        'it_locus': it_locus,
        'zl_locus': zl_locus,
    }


def critical_test_hapax_fallback(it_words, zl_words, it_vocab):
    """The critical test: for IT hapax-fallback words, what does ZL say at same locus?"""

    # Find IT hapax words that are fallback-only
    it_hapax = {w for w, c in it_vocab.items() if c == 1}
    it_hapax_fb = set()
    for w in it_hapax:
        result = decompose_word(w)
        if result and '_fallback' in result:
            it_hapax_fb.add(w)

    # Build locus -> position -> word maps
    it_locus_pos = {}
    for locus, word in it_words:
        if locus not in it_locus_pos:
            it_locus_pos[locus] = []
        it_locus_pos[locus].append(word)

    zl_locus_pos = {}
    for locus, word in zl_words:
        if locus not in zl_locus_pos:
            zl_locus_pos[locus] = []
        zl_locus_pos[locus].append(word)

    # For each IT hapax-fb occurrence, find ZL reading at same locus+position
    total_checked = 0
    same_reading = 0
    diff_reading = 0
    diff_now_parses = 0
    diff_still_fails = 0
    zl_missing = 0

    examples_rescued = []
    examples_still_bad = []

    for locus in it_locus_pos:
        for idx, it_word in enumerate(it_locus_pos[locus]):
            if it_word not in it_hapax_fb:
                continue

            total_checked += 1

            # Check if ZL has this locus and position
            if locus not in zl_locus_pos or idx >= len(zl_locus_pos[locus]):
                zl_missing += 1
                continue

            zl_word = zl_locus_pos[locus][idx]
            it_clean = it_word.replace('?', '')
            zl_clean = zl_word.replace('?', '')

            if it_clean == zl_clean:
                same_reading += 1
            else:
                diff_reading += 1
                # Does the ZL reading parse under 5-slot?
                zl_result = decompose_word(zl_clean)
                if zl_result and '_fallback' not in zl_result:
                    diff_now_parses += 1
                    examples_rescued.append((locus, idx, it_word, zl_word))
                else:
                    diff_still_fails += 1
                    examples_still_bad.append((locus, idx, it_word, zl_word))

    print(f"\n{'='*60}")
    print(f"  CRITICAL TEST: IT Hapax-Fallback vs ZL Readings")
    print(f"{'='*60}")
    print(f"  IT hapax-fallback words: {len(it_hapax_fb)}")
    print(f"  Locus occurrences checked: {total_checked}")
    print(f"  ZL missing at that locus/position: {zl_missing}")
    print(f"  Same reading in both: {same_reading} ({100*same_reading/(total_checked-zl_missing):.1f}% of found)")
    found = total_checked - zl_missing
    print(f"  Different reading: {diff_reading} ({100*diff_reading/found:.1f}% of found)")
    if diff_reading > 0:
        print(f"    -> ZL reading NOW parses (5-slot): {diff_now_parses} ({100*diff_now_parses/diff_reading:.1f}% of disagreements)")
        print(f"    -> ZL reading still fails:         {diff_still_fails} ({100*diff_still_fails/diff_reading:.1f}% of disagreements)")

    print(f"\n  Examples where ZL 'rescues' the word (first 20):")
    for locus, idx, it_w, zl_w in examples_rescued[:20]:
        print(f"    {locus}[{idx}]: IT={it_w:20s} -> ZL={zl_w}")

    print(f"\n  Examples where both fail (first 20):")
    for locus, idx, it_w, zl_w in examples_still_bad[:20]:
        print(f"    {locus}[{idx}]: IT={it_w:20s} -> ZL={zl_w}")

    return {
        'it_hapax_fb_count': len(it_hapax_fb),
        'total_checked': total_checked,
        'zl_missing': zl_missing,
        'same_reading': same_reading,
        'diff_reading': diff_reading,
        'diff_now_parses': diff_now_parses,
        'diff_still_fails': diff_still_fails,
        'examples_rescued': examples_rescued,
        'examples_still_bad': examples_still_bad,
    }


def consensus_analysis(it_words, zl_words):
    """Compute 5-slot match rate for consensus words (same word at same locus in both)."""

    # Build aligned pairs
    it_by_locus = defaultdict(list)
    zl_by_locus = defaultdict(list)
    for locus, word in it_words:
        it_by_locus[locus].append(word)
    for locus, word in zl_words:
        zl_by_locus[locus].append(word)

    consensus_words = []
    for locus in it_by_locus:
        if locus not in zl_by_locus:
            continue
        it_ws = it_by_locus[locus]
        zl_ws = zl_by_locus[locus]
        for i in range(min(len(it_ws), len(zl_ws))):
            it_clean = it_ws[i].replace('?', '')
            zl_clean = zl_ws[i].replace('?', '')
            if it_clean == zl_clean:
                consensus_words.append(it_clean)

    consensus_vocab = Counter(consensus_words)
    consensus_hapax = {w for w, c in consensus_vocab.items() if c == 1}

    # Slot decomposition on consensus
    match_tok = 0
    fb_tok = 0
    fail_tok = 0

    match_types = 0
    fb_types = 0
    fail_types = 0

    hapax_match = 0
    hapax_fb = 0
    hapax_fail = 0

    for word, count in consensus_vocab.items():
        result = decompose_word(word)
        is_hapax = word in consensus_hapax

        if result is None:
            fail_tok += count
            fail_types += 1
            if is_hapax:
                hapax_fail += 1
        elif '_fallback' in result:
            fb_tok += count
            fb_types += 1
            if is_hapax:
                hapax_fb += 1
        else:
            match_tok += count
            match_types += 1
            if is_hapax:
                hapax_match += 1

    total_tok = match_tok + fb_tok + fail_tok
    total_types = match_types + fb_types + fail_types
    total_hapax = hapax_match + hapax_fb + hapax_fail

    print(f"\n{'='*60}")
    print(f"  CONSENSUS ANALYSIS (words agreed at same locus)")
    print(f"{'='*60}")
    print(f"  Consensus tokens: {len(consensus_words):,}")
    print(f"  Consensus types:  {len(consensus_vocab):,}")
    print(f"  Consensus hapax:  {total_hapax:,}")
    print(f"\n  5-slot match by tokens: {match_tok:,} ({100*match_tok/total_tok:.1f}%)")
    print(f"  Fallback by tokens:     {fb_tok:,} ({100*fb_tok/total_tok:.1f}%)")
    print(f"  Fail by tokens:         {fail_tok:,} ({100*fail_tok/total_tok:.1f}%)")
    print(f"\n  5-slot match by types: {match_types:,} ({100*match_types/total_types:.1f}%)")
    print(f"  Fallback by types:     {fb_types:,} ({100*fb_types/total_types:.1f}%)")
    print(f"  Fail by types:         {fail_types:,} ({100*fail_types/total_types:.1f}%)")
    if total_hapax > 0:
        print(f"\n  Consensus hapax matched:  {hapax_match} ({100*hapax_match/total_hapax:.1f}%)")
        print(f"  Consensus hapax fallback: {hapax_fb} ({100*hapax_fb/total_hapax:.1f}%)")
        print(f"  Consensus hapax fail:     {hapax_fail} ({100*hapax_fail/total_hapax:.1f}%)")

    return {
        'consensus_tokens': len(consensus_words),
        'consensus_types': len(consensus_vocab),
        'consensus_hapax': total_hapax,
        'match_tok': match_tok, 'fb_tok': fb_tok, 'fail_tok': fail_tok,
        'match_tok_pct': 100*match_tok/total_tok,
        'match_types': match_types, 'fb_types': fb_types, 'fail_types': fail_types,
        'match_type_pct': 100*match_types/total_types,
        'hapax_match': hapax_match, 'hapax_fb': hapax_fb, 'hapax_fail': hapax_fail,
        'hapax_fb_pct': 100*hapax_fb/total_hapax if total_hapax else 0,
    }


def type_overlap(it_vocab, zl_vocab):
    """Compute type overlap between IT and ZL."""
    it_types = set(it_vocab.keys())
    zl_types = set(zl_vocab.keys())
    shared = it_types & zl_types
    it_only = it_types - zl_types
    zl_only = zl_types - it_types

    print(f"\n{'='*60}")
    print(f"  Type Overlap")
    print(f"{'='*60}")
    print(f"  IT types:     {len(it_types):,}")
    print(f"  ZL types:     {len(zl_types):,}")
    print(f"  Shared types: {len(shared):,} ({100*len(shared)/len(it_types|zl_types):.1f}% of union)")
    print(f"  IT-only:      {len(it_only):,}")
    print(f"  ZL-only:      {len(zl_only):,}")

    # Of IT-only types, how many are hapax in IT?
    it_only_hapax = sum(1 for w in it_only if it_vocab[w] == 1)
    zl_only_hapax = sum(1 for w in zl_only if zl_vocab[w] == 1)
    print(f"  IT-only that are IT-hapax: {it_only_hapax} ({100*it_only_hapax/len(it_only):.1f}%)")
    print(f"  ZL-only that are ZL-hapax: {zl_only_hapax} ({100*zl_only_hapax/len(zl_only):.1f}%)")

    return {
        'shared': len(shared),
        'it_only': len(it_only),
        'zl_only': len(zl_only),
        'it_only_hapax': it_only_hapax,
        'zl_only_hapax': zl_only_hapax,
    }


def generate_report(it_stats, zl_stats, it_slot, zl_slot, it_hapax, zl_hapax,
                     overlap, locus, critical, consensus):
    """Generate markdown findings report."""

    report = []
    report.append("# Cross-Transcription Analysis: IT vs ZL")
    report.append("")
    report.append("**Question:** Is the 5-slot decomposition transcription-dependent?")
    report.append("Does the 71.6% hapax-fallback rate in IT reflect transcription noise or real generator behavior?")
    report.append("")

    report.append("## 1. Corpus Statistics")
    report.append("")
    report.append("| Metric | IT (Takahashi) | ZL (Zandbergen-Landini) |")
    report.append("|--------|---------------|------------------------|")
    report.append(f"| Total tokens | {it_stats['total_tokens']:,} | {zl_stats['total_tokens']:,} |")
    report.append(f"| Unique types | {it_stats['unique_types']:,} | {zl_stats['unique_types']:,} |")
    report.append(f"| Hapax legomena | {it_stats['hapax_count']:,} ({it_stats['hapax_pct']:.1f}%) | {zl_stats['hapax_count']:,} ({zl_stats['hapax_pct']:.1f}%) |")
    report.append(f"| Type-token ratio | {it_stats['ttr']:.4f} | {zl_stats['ttr']:.4f} |")
    report.append("")

    report.append("## 2. Type Overlap")
    report.append("")
    report.append(f"- **Shared types:** {overlap['shared']:,} ({100*overlap['shared']/(overlap['shared']+overlap['it_only']+overlap['zl_only']):.1f}% of union)")
    report.append(f"- **IT-only types:** {overlap['it_only']:,} (of which {overlap['it_only_hapax']} = {100*overlap['it_only_hapax']/overlap['it_only']:.1f}% are IT hapax)")
    report.append(f"- **ZL-only types:** {overlap['zl_only']:,} (of which {overlap['zl_only_hapax']} = {100*overlap['zl_only_hapax']/overlap['zl_only']:.1f}% are ZL hapax)")
    report.append("")
    report.append("**Interpretation:** Transcription-unique types are overwhelmingly hapax -- most vocabulary disagreement is in rare words.")
    report.append("")

    report.append("## 3. Locus-Level Agreement")
    report.append("")
    report.append(f"- **Shared loci:** {locus['shared_loci']:,}")
    report.append(f"- **Token agreement rate:** {locus['agreement_rate']:.1f}% ({locus['agree']:,} agree, {locus['disagree']:,} disagree)")
    report.append("")

    report.append("## 4. 5-Slot Decomposition Comparison")
    report.append("")
    report.append("| Metric | IT | ZL |")
    report.append("|--------|----|----|")
    report.append(f"| 5-slot match (tokens) | {it_slot['match_token_pct']:.1f}% | {zl_slot['match_token_pct']:.1f}% |")
    report.append(f"| Fallback (tokens) | {it_slot['fallback_token_pct']:.1f}% | {zl_slot['fallback_token_pct']:.1f}% |")
    report.append(f"| 5-slot match (types) | {it_slot['match_type_pct']:.1f}% | {zl_slot['match_type_pct']:.1f}% |")
    report.append(f"| Hapax fallback rate | {it_hapax['hapax_fallback_pct']:.1f}% | {zl_hapax['hapax_fallback_pct']:.1f}% |")
    report.append("")

    report.append("## 5. Critical Test: IT Hapax-Fallback vs ZL")
    report.append("")
    report.append(f"Of {critical['it_hapax_fb_count']} IT hapax-fallback word types, checked {critical['total_checked']} locus occurrences:")
    report.append("")
    found = critical['total_checked'] - critical['zl_missing']
    report.append(f"- **ZL missing at locus:** {critical['zl_missing']}")
    report.append(f"- **Same reading in both:** {critical['same_reading']} ({100*critical['same_reading']/found:.1f}%)")
    report.append(f"- **Different reading:** {critical['diff_reading']} ({100*critical['diff_reading']/found:.1f}%)")
    if critical['diff_reading'] > 0:
        report.append(f"  - ZL reading NOW parses (5-slot): **{critical['diff_now_parses']}** ({100*critical['diff_now_parses']/critical['diff_reading']:.1f}% of disagreements)")
        report.append(f"  - ZL reading still fallback/fail: {critical['diff_still_fails']} ({100*critical['diff_still_fails']/critical['diff_reading']:.1f}%)")
    report.append("")

    # Compute the key diagnostic
    if found > 0 and critical['diff_reading'] > 0:
        rescue_rate = 100 * critical['diff_now_parses'] / found
        noise_fraction = 100 * critical['diff_reading'] / found
        report.append(f"**Key finding:** {noise_fraction:.1f}% of IT hapax-fallback words have a *different* ZL reading. ")
        report.append(f"Of those disagreements, {100*critical['diff_now_parses']/critical['diff_reading']:.1f}% produce a word that parses under the 5-slot model.")
        report.append(f"This means only ~{rescue_rate:.1f}% of IT hapax-fallback could be 'rescued' by switching transcriptions.")
        report.append("")

    report.append("## 6. Consensus Words (Transcription-Robust)")
    report.append("")
    report.append(f"Words where IT and ZL agree at the same locus ({consensus['consensus_tokens']:,} tokens, {consensus['consensus_types']:,} types):")
    report.append("")
    report.append(f"- **5-slot match (tokens):** {consensus['match_tok_pct']:.1f}%")
    report.append(f"- **5-slot match (types):** {consensus['match_type_pct']:.1f}%")
    report.append(f"- **Consensus hapax fallback rate:** {consensus['hapax_fb_pct']:.1f}%")
    report.append("")

    report.append("## 7. Conclusions")
    report.append("")

    # Determine conclusions based on data
    slot_diff = abs(it_slot['match_token_pct'] - zl_slot['match_token_pct'])
    if slot_diff < 3:
        report.append(f"1. **Slot match rates are stable across transcriptions** (IT {it_slot['match_token_pct']:.1f}% vs ZL {zl_slot['match_token_pct']:.1f}%, delta={slot_diff:.1f}pp). The 5-slot model is NOT an artifact of one transcription.")
    else:
        report.append(f"1. **Slot match rates differ meaningfully** (IT {it_slot['match_token_pct']:.1f}% vs ZL {zl_slot['match_token_pct']:.1f}%, delta={slot_diff:.1f}pp). Transcription choice affects the model.")

    if found > 0:
        same_pct = 100 * critical['same_reading'] / found
        if same_pct > 70:
            report.append(f"2. **Most IT hapax-fallback words ({same_pct:.0f}%) have the SAME reading in ZL.** The fallback-hapax problem is real, not transcription noise.")
        else:
            report.append(f"2. **Only {same_pct:.0f}% of IT hapax-fallback words agree in ZL.** Transcription uncertainty is a significant factor.")

    hapax_diff = abs(it_hapax['hapax_fallback_pct'] - zl_hapax['hapax_fallback_pct'])
    report.append(f"3. **Hapax fallback rates:** IT={it_hapax['hapax_fallback_pct']:.1f}% vs ZL={zl_hapax['hapax_fallback_pct']:.1f}% (delta={hapax_diff:.1f}pp).")

    consensus_vs_full = consensus['match_tok_pct'] - it_slot['match_token_pct']
    if consensus_vs_full > 1:
        report.append(f"4. **Consensus words parse better** ({consensus['match_tok_pct']:.1f}% vs IT-full {it_slot['match_token_pct']:.1f}%), confirming that transcription disagreements concentrate in hard-to-parse words.")
    else:
        report.append(f"4. **Consensus words parse at similar rate** ({consensus['match_tok_pct']:.1f}% vs IT-full {it_slot['match_token_pct']:.1f}%), suggesting transcription disagreement is evenly distributed.")

    report.append("")

    return "\n".join(report)


def main():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    it_path = os.path.join(base, 'data', 'IT2a-n.txt')
    zl_path = os.path.join(base, 'data', 'ZL3b-n.txt')

    print("Parsing IT (Takahashi)...")
    it_words = parse_ivtff_clean(it_path)
    print("Parsing ZL (Zandbergen-Landini)...")
    zl_words = parse_ivtff_clean(zl_path)

    # 1. Basic stats
    it_stats = basic_corpus_stats(it_words, "IT (Takahashi)")
    zl_stats = basic_corpus_stats(zl_words, "ZL (Zandbergen-Landini)")

    # 2. Type overlap
    overlap = type_overlap(it_stats['vocab'], zl_stats['vocab'])

    # 3. Locus-level agreement
    locus = locus_comparison(it_words, zl_words)

    # 4. Slot decomposition comparison
    it_slot = slot_decomposition_stats(it_stats['vocab'], "IT")
    zl_slot = slot_decomposition_stats(zl_stats['vocab'], "ZL")

    # 5. Hapax fallback analysis
    it_hapax = hapax_fallback_analysis(it_stats['vocab'], "IT")
    zl_hapax = hapax_fallback_analysis(zl_stats['vocab'], "ZL")

    # 6. Critical test
    critical = critical_test_hapax_fallback(it_words, zl_words, it_stats['vocab'])

    # 7. Consensus analysis
    consensus = consensus_analysis(it_words, zl_words)

    # Generate report
    report = generate_report(it_stats, zl_stats, it_slot, zl_slot,
                              it_hapax, zl_hapax, overlap, locus, critical, consensus)

    outdir = os.path.join(base, 'analysis')
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, 'cross_transcription_findings.md')
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"\n\nReport saved to {outpath}")


if __name__ == '__main__':
    main()
