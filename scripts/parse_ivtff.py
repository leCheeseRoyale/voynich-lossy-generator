"""
Parse IVTFF transcription files and extract Voynich words with page metadata.
Returns clean word list in EVA notation with folio/line provenance.
"""
import re
import sys
from collections import Counter

def parse_ivtff(filepath):
    """Parse IVTFF file, return list of (folio, line_num, word) tuples."""
    words = []
    current_folio = None

    with open(filepath, 'r', encoding='latin-1') as f:
        for line in f:
            line = line.rstrip('\n')

            # Skip comments and empty lines
            if line.startswith('#') or not line.strip():
                continue

            # Folio header: <f1r>
            folio_match = re.match(r'^<(f\d+[rv]\d?)>\s', line)
            if folio_match:
                current_folio = folio_match.group(1)
                continue

            # Text line: <f1r.1,@P0>  text...
            line_match = re.match(r'^<(f\d+[rv]\d?\.\d+),[^>]+>\s+(.*)', line)
            if not line_match:
                continue

            locus = line_match.group(1)
            text = line_match.group(2)

            # Remove IVTFF markers: <%> paragraph start, <$> paragraph end,
            # <-> line break within text, {curly} uncertain readings
            text = re.sub(r'<%>', '', text)
            text = re.sub(r'<\$>', '', text)
            text = re.sub(r'<->', '.', text)  # treat line breaks as word separators
            text = re.sub(r'[{}]', '', text)  # remove uncertainty brackets
            text = re.sub(r'<[^>]*>', '', text)  # remove any remaining tags

            # Split on dots (EVA word separator)
            raw_words = text.split('.')

            for w in raw_words:
                w = w.strip()
                if not w:
                    continue
                # Skip words that are only uncertainty markers or spaces
                if re.match(r'^[\?\s\*]+$', w):
                    continue
                words.append((locus, w))

    return words


def basic_stats(words):
    """Print basic corpus statistics."""
    word_list = [w for _, w in words]
    vocab = Counter(word_list)

    print(f"Total word tokens: {len(word_list)}")
    print(f"Unique word types: {len(vocab)}")
    print(f"Type-token ratio:  {len(vocab)/len(word_list):.4f}")
    print(f"Hapax legomena:    {sum(1 for c in vocab.values() if c == 1)}")
    print(f"Top 30 words:")
    for word, count in vocab.most_common(30):
        print(f"  {word:20s} {count:5d}")

    # Word length distribution
    lengths = Counter(len(w) for w in word_list)
    print(f"\nWord length distribution:")
    for l in sorted(lengths):
        print(f"  len={l:2d}: {lengths[l]:5d} ({100*lengths[l]/len(word_list):.1f}%)")

    return vocab


if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'data/IT2a-n.txt'
    words = parse_ivtff(filepath)
    vocab = basic_stats(words)

    # Save word list for downstream analysis
    outpath = filepath.replace('.txt', '_words.tsv')
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write("locus\tword\n")
        for locus, word in words:
            f.write(f"{locus}\t{word}\n")
    print(f"\nWord list saved to {outpath}")
