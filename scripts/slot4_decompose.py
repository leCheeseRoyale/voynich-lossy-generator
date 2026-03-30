"""
Slot 4 sub-decomposition.

Hypothesis: Slot 4 is 2-3 adjacent table columns merged.
The 154 fragments are built from a small glyph alphabet: {ch, sh, h, e, o, a}

Candidate sub-slot model:
  Sub4a (bench):    (empty), ch, sh, h
  Sub4b (e-series): (empty), e, ee, eee, eeee
  Sub4c (terminal): (empty), o, a

Theoretical space: 4 * 5 * 3 = 60 combos.
But observed ordering suggests: bench can appear before OR after e-series,
and 'o'/'a' sometimes appear in unexpected positions.

Strategy: parse each slot4 fragment left-to-right using greedy matching
of known glyph elements, then test whether the parse decomposes cleanly
into positional sub-slots.
"""

import json
import re
import sys
from collections import Counter, defaultdict

# Load slot4 data
with open('analysis/slot_fragments.json') as f:
    data = json.load(f)

s4 = data.get('slot4', {})

# Greedy left-to-right tokenizer for slot4 internal glyphs
# Order: longest first
GLYPH_ORDER = ['ch', 'sh', 'ee', 'e', 'o', 'a', 'h']

def tokenize_slot4(fragment):
    """Break a slot4 fragment into glyph tokens."""
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


# Tokenize all slot4 fragments
print("=" * 70)
print("SLOT 4 SUB-DECOMPOSITION ANALYSIS")
print("=" * 70)

# First pass: tokenize and check coverage
glyph_counts = Counter()
unparseable = {}
all_tokenized = {}

for frag, count in sorted(s4.items(), key=lambda x: -x[1]):
    if frag == '(empty)':
        continue
    tokens = tokenize_slot4(frag)
    rejoined = ''.join(tokens)
    if rejoined != frag:
        unparseable[frag] = count
    else:
        all_tokenized[frag] = (tokens, count)
        for t in tokens:
            glyph_counts[t] += count

print(f"\nGlyph-level token frequencies within Slot 4:")
for g, c in glyph_counts.most_common():
    print(f"  {g:5s} {c:6d}")

print(f"\nUnparseable fragments: {len(unparseable)} "
      f"({sum(unparseable.values())} tokens)")
for f, c in sorted(unparseable.items(), key=lambda x: -x[1])[:10]:
    print(f"  {f:20s} {c:5d}")

# Second pass: test sub-slot decomposition
# Model: slot4 = [bench?] [e-series?] [terminal?]
# Where bench = {ch, sh, h}, e-series = {e+}, terminal = {o, a}
# But also test: bench can appear after e-series

BENCH = {'ch', 'sh', 'h'}
E_SERIES = {'e', 'ee'}  # tokenized 'ee' is one token
TERMINAL = {'o', 'a'}

def classify_sub_slots(tokens):
    """Try to assign each token to a sub-slot position.
    Returns (sub4a, sub4b, sub4c) or None if it doesn't fit."""
    # Track token-by-token classification
    classes = []
    for t in tokens:
        if t in BENCH:
            classes.append('B')
        elif t == 'e':
            classes.append('E')
        elif t == 'ee':
            classes.append('E')  # double-e still E-class
        elif t in TERMINAL:
            classes.append('T')
        else:
            classes.append('?')

    pattern = ''.join(classes)
    return pattern, classes


# Classify all tokenized fragments
pattern_counts = Counter()
pattern_examples = defaultdict(list)

for frag, (tokens, count) in all_tokenized.items():
    pattern, classes = classify_sub_slots(tokens)
    pattern_counts[pattern] += count
    if len(pattern_examples[pattern]) < 3:
        pattern_examples[pattern].append((frag, count))

print(f"\n--- Sub-slot patterns (B=bench, E=e-series, T=terminal) ---")
total_classified = sum(pattern_counts.values())
for pattern, count in sorted(pattern_counts.items(), key=lambda x: -x[1]):
    examples = ", ".join(f"{f}({c})" for f, c in pattern_examples[pattern])
    print(f"  {pattern:12s} {count:6d} ({100*count/total_classified:5.1f}%)  e.g. {examples}")

# Third pass: extract sub-slots cleanly
# For patterns that fit B?E*T? model, extract the three sub-components
print(f"\n--- Sub-slot fragment inventories ---")

sub4a_counts = Counter()  # Bench position
sub4b_counts = Counter()  # E-series position
sub4c_counts = Counter()  # Terminal position

clean_patterns = set()
for pattern in pattern_counts:
    # Check if pattern matches B?E*T? (possibly with repeats)
    if re.match(r'^B?E*T?$', pattern):
        clean_patterns.add(pattern)

clean_tokens = 0
for frag, (tokens, count) in all_tokenized.items():
    pattern, classes = classify_sub_slots(tokens)
    if pattern not in clean_patterns:
        continue
    clean_tokens += count

    # Extract sub-slots
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

    sub4a = ''.join(bench_parts) if bench_parts else '(empty)'
    sub4b = ''.join(e_parts) if e_parts else '(empty)'
    sub4c = ''.join(term_parts) if term_parts else '(empty)'

    sub4a_counts[sub4a] += count
    sub4b_counts[sub4b] += count
    sub4c_counts[sub4c] += count

# Add the (empty) slot4 cases
empty_count = s4.get('(empty)', 0)
sub4a_counts['(empty)'] += empty_count
sub4b_counts['(empty)'] += empty_count
sub4c_counts['(empty)'] += empty_count
clean_tokens += empty_count

print(f"\nClean B?E*T? patterns cover {clean_tokens}/{sum(s4.values())} "
      f"({100*clean_tokens/sum(s4.values()):.1f}%) of slot4 tokens")

print(f"\nSub4a (bench): {len(sub4a_counts)} unique")
for frag, c in sub4a_counts.most_common():
    print(f"  {frag:10s} {c:6d}")

print(f"\nSub4b (e-series): {len(sub4b_counts)} unique")
for frag, c in sub4b_counts.most_common():
    print(f"  {frag:10s} {c:6d}")

print(f"\nSub4c (terminal): {len(sub4c_counts)} unique")
for frag, c in sub4c_counts.most_common():
    print(f"  {frag:10s} {c:6d}")

# Fourth pass: test for non-BET patterns
# These are fragments where bench appears AFTER e-series (EB, EBT, BEB, etc.)
print(f"\n--- Non-B?E*T? patterns (potential column-order violations) ---")
non_clean = 0
non_clean_examples = []
for frag, (tokens, count) in sorted(all_tokenized.items(), key=lambda x: -x[1][1]):
    pattern, _ = classify_sub_slots(tokens)
    if pattern not in clean_patterns:
        non_clean += count
        if len(non_clean_examples) < 25:
            non_clean_examples.append((frag, pattern, count))

print(f"Non-clean tokens: {non_clean} ({100*non_clean/sum(s4.values()):.1f}%)")
for frag, pat, count in non_clean_examples:
    print(f"  {frag:20s} pattern={pat:10s} count={count}")

# Save decomposition results
results = {
    'sub4a': dict(sub4a_counts),
    'sub4b': dict(sub4b_counts),
    'sub4c': dict(sub4c_counts),
    'clean_coverage_pct': round(100 * clean_tokens / sum(s4.values()), 1),
    'pattern_distribution': {p: c for p, c in pattern_counts.most_common()},
}

with open('analysis/slot4_decomposition.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to analysis/slot4_decomposition.json")
