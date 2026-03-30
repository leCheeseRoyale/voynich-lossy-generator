# Prior Work Review: Novelty Assessment of Voynich Lossy Generator Claims

**Reviewer role:** Skeptical academic reviewer
**Date:** 2026-03-30
**Purpose:** Determine whether each claimed contribution is genuinely novel, partially novel, or already established in prior literature.

---

## Methodology

Searched published literature (peer-reviewed and arXiv), community analyses (voynich.nu, voynich.ninja, Cipher Mysteries), and blog-form scholarship for prior work on each claimed contribution. Sources checked include:

- Stolfi (1997, 2000) -- word grammar and crust/mantle/core model
- Rugg (2004) and Rugg & Taylor (2017) -- Cardan grille hypothesis
- Schinner (2007) -- hoax statistical evidence
- Reddy & Knight (2011) -- HMM analysis
- Montemurro & Zanette (2013) -- information-theoretic keyword analysis
- Timm (2014) and Timm & Schinner (2020, 2023) -- self-citation algorithm
- Emma May Smith (2019) -- syllable rank ordering / "body rank order"
- Ponzi (2019) -- comparison of two word models
- Zandbergen (2021) -- extended Cardan grille with table structure
- Matlach et al. (2022) -- symbol roles revisited (autocorrelation)
- Zattera (2022) -- 12-slot decomposition (v4j framework)
- Bowern & Lindemann (2021) -- linguistic review
- Currier (1976) -- two "languages" A and B
- Earnhart (undated) -- "paper computer" hypothesis

---

## Claim 1: A 7-slot positional decomposition of Voynich words (building on Stolfi 1997)

**Verdict: PARTIALLY NOVEL**

### Prior work establishing the basic idea:

**Stolfi (1997, 2000)** proposed the foundational prefix-midfix-suffix and then crust-mantle-core decomposition. His grammar achieves 96.5% coverage. He identified three nested layers (crust, mantle, core) with specific character sets assigned to each. This is effectively a positional slot model, though expressed as a nested grammar rather than numbered slots.

**Emma May Smith (2019)** proposed a "body rank order" model with up to 3 syllable slots, achieving ~97% coverage. Her model imposes ordering constraints (rank must increase left to right).

**Zattera (2022)** proposed a 12-slot decomposition at the Malta Voynich conference, achieving 88-98% coverage depending on counting method. His slot alphabet assigns each glyph to one of 12 positional slots (numbered 0-11).

**Ponzi (2019)** compared Stolfi and Smith models side by side, noting both achieve ~91% accuracy and both impose positional constraints.

**Reddy & Knight (2011)** used a 2-state HMM that recovered an A*B word formula, essentially a 2-slot positional decomposition.

### What is novel in this project's version:

The specific 7-slot formulation (S1-Initial, S2-Prefix, S3-Gallows, S4a-Bench, S4b-E-series, S4c-Terminal, S5-Suffix) with the B?E*T? sub-decomposition of Slot 4 is a specific refinement not found in exactly this form elsewhere. However, it is one of many slot decompositions in a well-explored space. The sub-decomposition of S4 into bench/e-series/terminal sub-slots is a genuine contribution, as prior models either treated the middle as monolithic (Stolfi's mantle) or used finer-grained character-level slots (Zattera's 12 slots).

**The 98.2% coverage rate is competitive** but not clearly superior to Stolfi's 96.5% or Smith's ~97%.

### Required citations: Stolfi (1997, 2000), Smith (2019), Zattera (2022), Ponzi (2019), Reddy & Knight (2011)

---

## Claim 2: Statistical proof that all slot pairs are dependent (ruling out independent-column/Cardan grille)

**Verdict: PARTIALLY NOVEL -- the formal statistical proof is new, but the observation is not**

### Prior work:

**Stolfi (2000)** explicitly noted that his word paradigm "fails to notice" asymmetries like daiin (866 occurrences) vs deedy (3 occurrences), and stated "These dependencies are actually quite common in Voynichese." He recognized that independent slot selection was inadequate but did not perform formal statistical tests.

**Ponzi (2019)** discussed how both the Stolfi and Smith models impose ordering constraints that reflect dependencies, though no chi-squared or similar tests were performed.

**Matlach et al. (2022)** found that 90.4% of tested autocorrelation lags for Voynich symbols are significant, demonstrating symbol placement depends on prior context. This is a different kind of dependency test (sequential autocorrelation rather than within-word slot-pair dependency) but establishes that Voynich text is far from positionally independent.

**Zandbergen (2021)** acknowledged that his extended grille model needed to account for word structure but did not test slot independence formally.

**Rugg & Taylor (2017)** showed their grille output was "very sensitive to tweaks in the initial parameters" but did not address whether the grille model could reproduce observed slot dependencies.

### What is novel:

The **formal chi-squared testing of all pairwise slot dependencies** with explicit Cramer's V effect sizes (V = 0.12-0.48) and demonstration that even non-adjacent slots show significant dependence (p < 1e-300) appears to be genuinely new. No prior work has published pairwise chi-squared tests between word-position slots. This is the rigorous statistical version of an observation Stolfi made qualitatively 25+ years ago.

**The specific argument that this rules out independent-column models** is a valid inference from the data, but the conceptual point (Voynich words are not random concatenations of independently chosen fragments) was already widely appreciated in the community.

### Required citations: Stolfi (2000) for qualitative dependency observation, Matlach et al. (2022) for symbol autocorrelation, Rugg & Taylor (2017) for grille sensitivity

---

## Claim 3: Discovery of a "ch-default" mechanism (14x rate spike, V=0.48)

**Verdict: NOVEL (the specific quantitative finding is new; the general observation about ch is not)**

### Prior work:

**Stolfi (2000)** classified ch as a "bench" letter in the mantle layer and noted its high frequency and specific positional behavior, but did not identify it as a "default" for empty cells.

**Rugg (2004) and Rugg's blog posts (2014)** discussed how his table-and-grille method produces blank cells and that "a comparatively high proportion of 'blank' words can be produced where the card shows only empty cells on the table." However, he did not identify specific characters as defaults for blank cells.

**The Voynich community** has long noted ch's special behavior -- its high frequency, its positional regularity, and its tendency to appear in certain contexts. The voynich.nu writing system analysis and multiple forum discussions note ch's peculiarities. However, no one has framed it as a "default fragment" that fills empty table cells with a measured conditional rate.

### What is novel:

The **specific finding that ch appears at 14x its baseline rate when adjacent slots are empty (V=0.48)** is a new quantitative result. The interpretation as a "blank-cell default" in a lookup table is a novel mechanistic explanation. No prior publication frames ch's behavior this way or provides comparable statistics.

### Required citations: Stolfi (2000) for ch as mantle/bench letter, Rugg (2004, 2014) for blank-cell concept in grille tables

---

## Claim 4: The "lossy generation" framework -- real content through a mechanical encoder producing hallucinations

**Verdict: NOVEL as a unified framework; constituent ideas have precedents**

### Prior work:

**Zandbergen (2021)** explicitly stated that the grille method "could not only be used to create meaningless text, but also to encode meaningful text." This directly anticipates the idea that a mechanical table encodes real content.

**Rugg (2004)** proposed pure hoax (no content). **Montemurro & Zanette (2013)** argued for genuine semantic content. **Timm (2014)** proposed pure self-citation (no content). The field has been polarized between "all content" and "no content" camps.

**Earnhart (undated)** proposed the manuscript as a "paper computer" or "pasigraphic engine" encoding procedures, which shares conceptual overlap with the idea of a mechanical encoding device.

**The "lossy number cipher" idea** has been discussed in Voynich forums, with some noting that "just because the encoding is lossy, that doesn't mean it's completely meaningless."

### What is novel:

The **specific framework that unifies these observations** -- a mechanical device that encodes real content but produces systematic "hallucinations" (unparseable words, defaults, hapax words) as generation artifacts -- appears to be genuinely new. The analogy to a lossy codec (real signal + predictable noise) is a fresh framing. No prior work has explicitly modeled the coexistence of content and noise as natural consequences of a single generation mechanism, with the noise being diagnostically useful.

However, **Zandbergen (2021) came close** to this idea by noting the table could encode meaningful text. The gap is that Zandbergen did not model the noise/artifact side or propose that artifacts are diagnostically useful.

### Required citations: Zandbergen (2021) for "table can encode meaningful text," Montemurro & Zanette (2013) for content evidence, Timm (2014) for generation mechanism, Rugg (2004) for table-based generation

---

## Claim 5: Default rates recovering manuscript sections independently of vocabulary analysis

**Verdict: NOVEL**

### Prior work:

**Currier (1976)** identified "languages" A and B and noted statistical differences across sections, but his analysis was vocabulary-based (letter-group frequencies).

**Montemurro & Zanette (2013)** showed that keyword distributions distinguish manuscript sections, but this was explicitly vocabulary/word-based analysis using information-theoretic measures.

**Bowern & Lindemann (2021)** reviewed section-level differences but through standard linguistic/statistical measures (entropy, vocabulary).

**Various researchers** have noted section differences in word frequencies, character distributions, and statistical properties, but always through vocabulary-level metrics.

### What is novel:

The finding that **structural default rates** (a purely mechanical metric -- the rate at which specific fragments appear as blank-cell fillers) independently recover section structure (Kruskal-Wallis H up to 70.71, p < 1e-13) appears to be genuinely new. This is a vocabulary-independent structural metric that recovers the same section boundaries. No prior work has used generation-mechanism parameters (as opposed to vocabulary) to distinguish sections.

This is a strong novelty claim because it validates Montemurro & Zanette's content finding "through an entirely different analytical lens," as the project states.

### Required citations: Currier (1976), Montemurro & Zanette (2013), Bowern & Lindemann (2021)

---

## Claim 6: E-series as parametric encoding (74.2% co-occurrence, ordering effect)

**Verdict: PARTIALLY NOVEL**

### Prior work:

**Stolfi (2000)** extensively analyzed the e/ee/eee patterns in his mantle layer. He noted the parsing rule: "A string of two or more e letters following a gallows letter is parsed from right to left, into zero or more ee pairs (mantle) and possibly a single e (core)." He recognized e-sequences as structurally significant but did not propose a parametric encoding interpretation.

**The Voynich community** has long discussed e-sequences as one of the most distinctive features of Voynichese. The observation that e, ee, eee, eeee form a graded series is not new.

**Zandbergen (2021)** included e-variants as part of his column structure in the extended grille table, treating them as distinct table entries.

### What is novel:

The **statistical evidence for parametric encoding** is new: 74.2% of e-families showing significant co-occurrence (vs 5% expected by chance), the ordering effect (Kendall's tau = 0.05, p < 0.000001 showing lower E-values tend to precede higher ones within pages), and the interpretation that e-series encode a graded parameter (quantity, intensity). The formal co-occurrence analysis and ordering test have not been published before.

However, the **observation itself** (that e/ee/eee form a series) is decades old. The novelty is in the statistical validation and parametric interpretation.

### Required citations: Stolfi (2000) for e-series structure, Zandbergen (2021) for e-variants in table

---

## Claim 7: Computational falsification of Rugg (2004) via synthetic generator comparison (JSD 9-15x)

**Verdict: PARTIALLY NOVEL**

### Prior work:

**Timm (2014) and Timm & Schinner (2020)** built synthetic Voynich text generators and compared statistical properties to the real manuscript. Their self-citation algorithm achieved <10% relative error on Zipf's laws, word length distribution, and entropy. This is a direct precedent for synthetic-vs-real comparison.

**Rugg & Taylor (2017)** themselves showed their grille output was "very sensitive to tweaks" and that the method could reproduce Zipf's distribution, word length distribution, and non-homogeneous word distribution.

**Schinner (2007)** compared Voynich statistical properties to random text and natural languages.

**The anachronism argument** against Rugg (Cardan grille not invented until 1550, manuscript dated to early 15th century) has been widely noted.

### What is novel:

The **specific head-to-head comparison** between an independent-slot generator (GenA, modeling Rugg) and a row-based generator (GenB) using Jensen-Shannon Divergence on slot-transition distributions is a new methodology. The 9-15x JSD advantage for GenB on transition distributions is a new quantitative finding.

However, the **conceptual conclusion** (the Cardan grille model is inadequate) was already widely held in the research community for multiple reasons: anachronism, failure to capture higher-order statistics, and the known slot dependencies. The project provides rigorous computational evidence for a conclusion many researchers had already reached.

**Important caveat:** Timm's self-citation model is a third alternative to both GenA and GenB. The project appears to test only the Rugg-style independent model (GenA) against row-based (GenB), but does not compare against the Timm self-citation model. This is a gap that reviewers will note.

### Required citations: Timm (2014), Timm & Schinner (2020), Rugg & Taylor (2017), Schinner (2007)

---

## Claim 8: Botanical feature correlation with default rates (ablation confirmed at p<0.0001)

**Verdict: NOVEL**

### Prior work:

**Montemurro & Zanette (2013)** showed that semantic word networks align with manuscript sections and that sections sharing illustration types (plants) share vocabulary. However, they worked at the section level, not the individual page/illustration level, and used vocabulary distributions, not generation-mechanism parameters.

**Tucker & Talbert (2014)** attempted to identify specific plants in the manuscript but did not correlate text properties with botanical features.

**No prior work** has correlated specific visual features of botanical illustrations (leaf shape, root type) with statistical properties of the accompanying text at the individual page level.

### What is novel:

The finding that **pages with distinctive botanical features (lobed leaves, bulbous roots, serrated edges) have significantly lower default rates** -- meaning more table slots filled with content -- is entirely new. The ablation test showing that zero of 100 synthetic corpora produce correlations as extreme as the real data (p < 0.0001 for all 5 features) is a powerful novel finding.

This is arguably the project's strongest novelty claim, as it provides the first direct statistical link between illustration content and text-generation parameters at the individual page level.

### Required citations: Montemurro & Zanette (2013) for section-level content argument, Tucker & Talbert (2014) for plant identification attempts

---

## Claim 9: The analogy between Voynich generation artifacts and LLM hallucination

**Verdict: NOVEL as a formal analogy; casual comparisons exist**

### Prior work:

**LessWrong (2023)** published a post noting that "humanity is essentially in the same relationship to the Voynich Manuscript as AI large language models (LLMs) are to the entire textual output of humans on the Internet." However, this is a philosophical/conceptual comparison, not a technical analogy about generation mechanisms.

**Various blog discussions** have noted parallels between AI-generated text and Voynich text in passing, typically in the context of AI "decipherment" attempts.

### What is novel:

The **specific technical analogy** -- that a mechanical encoder produces "hallucinations" (unparseable words from empty cells) in the same way that LLMs produce hallucinations (plausible-sounding but unfounded text) as a byproduct of the generation mechanism -- appears to be a new framing. The key insight is that in both cases, the artifacts are systematic and diagnostically useful (they reveal properties of the generation mechanism).

However, this is primarily a **rhetorical/pedagogical contribution**, not a research finding. It helps explain the framework but does not constitute independent evidence.

### Required citations: General LLM hallucination literature; note this is an analogy, not a finding

---

## Claim 10: Row-based lookup as the generation mechanism (vs Cardan grille)

**Verdict: PARTIALLY NOVEL**

### Prior work:

**Rugg (2004)** proposed movement of a grille across a table -- which is fundamentally a column-selection mechanism where each word is assembled from independently chosen column entries.

**Zandbergen (2021)** extended the grille model to a multi-table system (3 tables x 4 column-sets x 42 rows = 504 entries) and explicitly proposed that rows contain word fragments. His model is table-based with rows and columns. However, he did not formally distinguish between row-based joint selection and independent column selection, nor did he test one against the other.

**Stolfi's paradigm** implicitly encodes something like row structure -- his observation that certain prefix/suffix combinations are far more common than others (daiin vs deedy) describes exactly the row-based constraint.

**Timm (2014)** proposed self-citation (copying and modifying nearby words) as the mechanism, which is neither row-based nor column-based but sequential.

### What is novel:

The **explicit distinction between independent-column selection and row-based joint selection**, formalized as two competing generators (GenA vs GenB) and tested quantitatively, is a new contribution. The demonstration that row-based generation better reproduces observed transition structures (by 9-15x on JSD) provides the first formal evidence favoring joint selection over independent selection.

However, the **concept of a lookup table with rows** is not new -- Zandbergen proposed essentially this structure. The novelty is in the formal comparison and the evidence that row-based selection is necessary.

### Required citations: Zandbergen (2021) for table structure with rows, Rugg (2004) for column-based model, Stolfi (2000) for implicit row constraints

---

## Summary Table

| # | Claim | Verdict | Key Prior Work |
|---|-------|---------|----------------|
| 1 | 7-slot decomposition | PARTIALLY NOVEL | Stolfi (1997/2000), Smith (2019), Zattera (2022) |
| 2 | All slot pairs dependent | PARTIALLY NOVEL | Stolfi (2000) qualitative observation; chi-squared tests are new |
| 3 | ch-default mechanism (14x, V=0.48) | NOVEL | ch's special behavior known; quantitative default finding is new |
| 4 | Lossy generation framework | NOVEL (as unified framework) | Zandbergen (2021) closest; field was polarized content vs hoax |
| 5 | Default rates recover sections | NOVEL | No prior vocabulary-independent structural section recovery |
| 6 | E-series parametric encoding | PARTIALLY NOVEL | e-series structure known since Stolfi; statistical tests are new |
| 7 | Rugg falsification via synthetic comparison | PARTIALLY NOVEL | Timm (2014) did synthetic comparison; JSD method is new |
| 8 | Botanical feature correlation | NOVEL | First page-level illustration-text correlation study |
| 9 | LLM hallucination analogy | NOVEL (rhetorical) | Casual comparisons exist; formal technical analogy is new |
| 10 | Row-based lookup mechanism | PARTIALLY NOVEL | Zandbergen (2021) proposed tables with rows; formal test is new |

---

## Critical Gaps and Risks

### 1. The Timm self-citation model is not addressed
Timm's self-citation algorithm is a serious alternative generation mechanism that reproduces many Voynich statistical properties. The project compares only independent-slot (GenA) vs row-based (GenB) but does not test against Timm's model. A reviewer familiar with Timm's work will ask: "How does your row-based model compare to self-citation?" This must be addressed.

### 2. Zattera's 12-slot model is not cited
Zattera presented a 12-slot decomposition at the Malta 2022 conference with high coverage. The paper must explain why 7 slots were chosen over 12 (or other numbers) and how the decompositions relate.

### 3. Zandbergen (2021) is dangerously close on several claims
Zandbergen proposed: (a) a table with rows and columns of word fragments, (b) that the method could encode meaningful text, (c) a specific table structure (3 tables x 4 column-sets x 42 rows). The paper must clearly delineate what Zandbergen proposed versus what this project adds (formal statistical testing, default mechanism, botanical correlation).

### 4. The Montemurro & Zanette (2013) section-level finding
The paper correctly notes it validates M&Z through a different lens, but must be careful not to overclaim the botanical correlation as wholly unprecedented -- M&Z already showed text content tracks illustrations at the section level.

### 5. Matlach et al. (2022) autocorrelation findings
The symbol autocorrelation results from this paper are relevant to Claim 2 and should be discussed.

### 6. Smith (2019) and Ponzi (2019) on positional structure
These more recent word-structure analyses should be cited alongside Stolfi.

---

## Recommended Citation Additions

The paper **must cite** the following works that appear to be missing or under-cited based on the claims made:

1. **Zattera (2022)** -- 12-slot decomposition, v4j framework
2. **Timm (2014) and Timm & Schinner (2020, 2023)** -- self-citation generation model, synthetic comparison
3. **Matlach et al. (2022)** -- symbol autocorrelation / positional dependencies
4. **Emma May Smith (2019)** -- syllable rank ordering model
5. **Ponzi (2019)** -- two word models comparison
6. **Rugg & Taylor (2017)** -- refined grille with syllable tables
7. **Bowern & Lindemann (2021)** -- comprehensive linguistic review
8. **Earnhart (undated)** -- "paper computer" concept (if available as citable source)

---

## Overall Assessment

Of the 10 claimed contributions, **3 are genuinely novel** (claims 3, 5, 8), **1 is novel as a framework** (claim 4), **5 are partially novel** (claims 1, 2, 6, 7, 10), and **1 is primarily rhetorical** (claim 9).

The project's strongest novelty claims are:
- The ch-default quantitative finding (claim 3)
- Default rates as a vocabulary-independent section discriminator (claim 5)
- Botanical feature correlation at the page level (claim 8)
- The lossy generation framework unifying content and noise (claim 4)

The project's weakest novelty claims are:
- The 7-slot decomposition (claim 1) -- one of many in a crowded field
- Rugg falsification (claim 7) -- conclusion was already widely held; Timm's alternative model is not addressed
- The LLM analogy (claim 9) -- interesting framing but not a research finding

The paper should be restructured to **lead with the genuinely novel findings** (botanical correlation, ch-default, section recovery via defaults, lossy framework) and **frame the slot decomposition and Rugg falsification as enabling methodology** rather than headline contributions.
