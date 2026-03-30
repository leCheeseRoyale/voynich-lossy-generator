"""
Phase 1.1: Stolfi-style positional slot decomposition of Voynich words.

Based on Stolfi (1997), Voynich words follow a quasi-regular structure:
  [prefix] [core-prefix] [gallows] [core-midfix] [core-suffix] [suffix]

We implement a data-driven slot decomposition using known EVA glyph classes:
  - Gallows: t, k, p, f (and their "bench" variants cth, ckh, cph, cfh)
  - Bench elements: ch, sh, (prefixed with c for gallows benches)
  - i-sequences: ii, iii, iiii, in, iin, iiin (right-side elements)
  - o-elements: o, qo (word-initial elements)
  - e-sequences: e, ee, eee, ey, eey
  - d/l/r/s/n: standalone or as connectors
  - a: usually precedes i-sequences
  - y: often word-final

Slot model (5 slots based on Stolfi's "crust-mantle-core"):
  SLOT 1 (initial):  q, qo, o, d, s, y (word-initial elements)
  SLOT 2 (prefix):   l, r, ch, sh, al, ol (pre-gallows)
  SLOT 3 (gallows):  k, t, p, f, ckh, cth, cph, cfh (or absent)
  SLOT 4 (mid):      h, ch, sh, o, a, e (post-gallows connective)
  SLOT 5 (suffix):   aiin, ain, air, al, am, an, ar, dy, edy, eedy,
                      ey, eey, ol, or, y, d, r, s (word-final)
"""

import re
import json
import sys
from collections import Counter, defaultdict
from parse_ivtff import parse_ivtff

# ---- Glyph-class regex patterns ----
# Order matters: longer patterns first to avoid partial matches.

# Known EVA "gallows" glyphs and their bench variants
GALLOWS = r'(?:ckh|cth|cph|cfh|kh|th|ph|fh|k|t|p|f)'

# Slot decomposition regex:
# This is the core structural hypothesis. We attempt to match Voynich words
# as a sequence of positional slots.
#
# Slot 1: Initial  — optional: q, qo, o, d, s, y (alone or combos)
# Slot 2: Prefix   — optional: ch, sh, l, r, ol, al, or
# Slot 3: Gallows  — optional: any gallows glyph
# Slot 4: Middle   — optional: e-sequences, o, a, ch, sh, h
# Slot 5: Suffix   — optional: aiin, ain, dy, ey, y, d, r, l, n, s, etc.

WORD_PATTERN = re.compile(
    r'^'
    r'(?P<slot1>(?:qo|[odsy]))?'           # Initial
    r'(?P<slot2>(?:ch|sh|[lr]|ol|al))?'     # Prefix
    r'(?P<slot3>' + GALLOWS + r')?'         # Gallows
    r'(?P<slot4>(?:eee|ee|e|o|a|ch|sh|h)*)' # Middle (repeatable)
    r'(?P<slot5>(?:ai+n|ai+r|ai+m|i+n|i+r|dy|edy|eedy|eey|ey|ol|or|al|am|an|ar|y|d|l|r|s|m|n))?'
    r'$'
)

# Fallback: try a simpler left-right decomposition
SIMPLE_PATTERN = re.compile(
    r'^'
    r'(?P<left>(?:qo|[odsy])?(?:ch|sh|[lr]|ol|al)?)'
    r'(?P<center>.*?)'
    r'(?P<right>(?:ai+n|ai+r|dy|edy|eedy|eey|ey|y|d|r|l|s|n)?)$'
)


def decompose_word(word):
    """Attempt slot decomposition. Returns dict of slot contents or None."""
    m = WORD_PATTERN.match(word)
    if m:
        return {k: v or '' for k, v in m.groupdict().items()}

    # Fallback
    m = SIMPLE_PATTERN.match(word)
    if m:
        return {
            'slot1': '', 'slot2': '', 'slot3': '',
            'left': m.group('left') or '',
            'center': m.group('center') or '',
            'right': m.group('right') or '',
            '_fallback': True
        }
    return None


def analyze_slots(words):
    """Run slot decomposition across corpus, collect statistics."""
    slot_fragments = defaultdict(Counter)  # slot_name -> fragment -> count
    match_count = 0
    fallback_count = 0
    fail_count = 0
    failed_words = Counter()

    word_list = [w for _, w in words]
    vocab = Counter(word_list)

    for word, count in vocab.items():
        result = decompose_word(word)
        if result is None:
            fail_count += count
            failed_words[word] += count
            continue

        if '_fallback' in result:
            fallback_count += count
            for slot in ['left', 'center', 'right']:
                if result[slot]:
                    slot_fragments[f'fb_{slot}'][result[slot]] += count
        else:
            match_count += count
            for slot in ['slot1', 'slot2', 'slot3', 'slot4', 'slot5']:
                fragment = result[slot]
                if fragment:
                    slot_fragments[slot][fragment] += count
                else:
                    slot_fragments[slot]['(empty)'] += count

    total = len(word_list)
    print("=" * 70)
    print("PHASE 1.1: SLOT DECOMPOSITION RESULTS")
    print("=" * 70)
    print(f"\nCorpus: {total} tokens, {len(vocab)} types")
    print(f"Matched (5-slot):  {match_count:6d} ({100*match_count/total:.1f}%)")
    print(f"Fallback (3-slot): {fallback_count:6d} ({100*fallback_count/total:.1f}%)")
    print(f"Failed:            {fail_count:6d} ({100*fail_count/total:.1f}%)")

    print(f"\n--- Per-Slot Fragment Inventory ---")
    for slot in ['slot1', 'slot2', 'slot3', 'slot4', 'slot5']:
        frags = slot_fragments[slot]
        total_slot = sum(frags.values())
        non_empty = {k: v for k, v in frags.items() if k != '(empty)'}
        empty_count = frags.get('(empty)', 0)
        print(f"\n{slot.upper()} ({total_slot} tokens, "
              f"{len(non_empty)} unique fragments, "
              f"empty in {100*empty_count/total_slot:.1f}% of words):")
        for frag, cnt in sorted(non_empty.items(), key=lambda x: -x[1])[:20]:
            print(f"  {frag:15s} {cnt:6d} ({100*cnt/total_slot:.1f}%)")

    # Transition analysis: which slot2 values follow which slot1 values?
    print(f"\n--- Slot Transition Matrix (slot1 -> slot2) ---")
    transitions_12 = defaultdict(Counter)
    for word, count in vocab.items():
        result = decompose_word(word)
        if result and '_fallback' not in result:
            s1 = result['slot1'] or '(empty)'
            s2 = result['slot2'] or '(empty)'
            transitions_12[s1][s2] += count

    for s1 in sorted(transitions_12, key=lambda x: -sum(transitions_12[x].values())):
        top = transitions_12[s1].most_common(8)
        pairs = ", ".join(f"{s2}:{c}" for s2, c in top)
        print(f"  {s1:5s} -> {pairs}")

    # Transition: slot3 -> slot5 (gallows to suffix)
    print(f"\n--- Slot Transition Matrix (slot3 -> slot5) ---")
    transitions_35 = defaultdict(Counter)
    for word, count in vocab.items():
        result = decompose_word(word)
        if result and '_fallback' not in result:
            s3 = result['slot3'] or '(empty)'
            s5 = result['slot5'] or '(empty)'
            transitions_35[s3][s5] += count

    for s3 in sorted(transitions_35, key=lambda x: -sum(transitions_35[x].values())):
        top = transitions_35[s3].most_common(8)
        pairs = ", ".join(f"{s5}:{c}" for s5, c in top)
        print(f"  {s3:8s} -> {pairs}")

    # Failed words (top 20)
    if failed_words:
        print(f"\n--- Top 20 Failed Words ---")
        for w, c in failed_words.most_common(20):
            print(f"  {w:20s} {c:5d}")

    return slot_fragments, transitions_12, transitions_35, failed_words


def save_results(slot_fragments, transitions_12, transitions_35, outdir='analysis'):
    """Save results as JSON for downstream tasks."""
    import os
    os.makedirs(outdir, exist_ok=True)

    # Convert Counters to dicts for JSON
    sf = {slot: dict(frags) for slot, frags in slot_fragments.items()}
    t12 = {s1: dict(t) for s1, t in transitions_12.items()}
    t35 = {s3: dict(t) for s3, t in transitions_35.items()}

    with open(f'{outdir}/slot_fragments.json', 'w') as f:
        json.dump(sf, f, indent=2, ensure_ascii=False)
    with open(f'{outdir}/transitions_s1_s2.json', 'w') as f:
        json.dump(t12, f, indent=2)
    with open(f'{outdir}/transitions_s3_s5.json', 'w') as f:
        json.dump(t35, f, indent=2)

    print(f"\nResults saved to {outdir}/")


if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'data/IT2a-n.txt'
    words = parse_ivtff(filepath)
    sf, t12, t35, failed = analyze_slots(words)
    save_results(sf, t12, t35)
