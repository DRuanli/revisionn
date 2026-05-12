# Revision Checklist — PONE-D-26-07832
**Manuscript**: Best-First Search–Based Approach for Mining Top-K Closed Frequent Itemsets from Uncertain Databases
**Decision**: Major Revision
**Deadline**: May 22, 2026

Legend:  ✅ Done   🟡 Partially Done   ⬜ Not Done

---

## A. Editorial / Journal Requirements

| # | Requirement | Status | Notes |
|---|---|---|---|
| A1 | Apply PLOS ONE style template (main body) | ⬜ | Use `PLOSOne_formatting_sample_main_body.pdf` |
| A2 | Apply PLOS ONE style template (title/authors/affiliations) | ⬜ | Use `PLOSOne_formatting_sample_title_authors_affiliations.pdf` |
| A3 | Use "Fig" not "Figure" for figure citations | 🟡 | Audit current draft; current usage is mixed |
| A4 | Reference Table 3 in body text | ⬜ | Locate Table 3 (likely variants summary or vertical-DB table) and add textual reference |
| A5 | Audit ALL tables to ensure each is referenced | ⬜ | Cross-check all `\label{tab:...}` against `\ref{tab:...}` usage |
| A6 | Compliant file naming for resubmission | ⬜ | `Manuscript`, `Revised Manuscript with Track Changes`, `Response to Reviewers` |
| A7 | Generate latexdiff against initial submission | ⬜ | Required for tracked-changes file |

---

## B. Reviewer #1 — Critical Issues

| # | Issue | Severity | Status | Notes |
|---|---|---|---|---|
| B1 | TUFC1 vs TUFCII naming inconsistency audit | 🟡 MINOR | 🟡 | Code uses TUFCI consistently; do global find/replace verification on .tex source |
| B2 | Overstated novelty re: support-ordered exploration | 🟠 MAJOR | ✅ | Already softened in current revision; literature review explicitly cites TKO/kHMC/TFP |
| B3 | Lit review conflates deterministic/uncertain/utility mining | 🟠 MAJOR | ✅ | Already restructured into clean subsections in current revision |
| B4 | Excessive notation without intuitive explanation | 🟡 MINOR | ✅ | Intuitive paragraphs added before generating function and frequency function |
| B5 | Lemma 1 stochastic-dominance proof imprecision | 🔴 CRITICAL | ✅ | Already rewritten with explicit coupling argument using uniform random variables |
| B6 | Algorithm 1 uses undefined `min_sup`; LaTeX bug `\$\theta(\mathcal{H})\$` | 🟡 MINOR | 🟡 | LaTeX typo still in current revision (line: `Prune items with support $< \$\theta(\mathcal{H})$$`); fix syntax |
| B7 | Tie-breaking rules unjustified | 🟡 MINOR | 🟡 | Rationale paragraph added; supplementary 3-policy experiment claimed but NOT YET RUN — handle in writing per user instruction (remove Exp7) |
| B8 | $O(n^2)$ misleading without clarifying $n = m_X$ | 🟠 MAJOR | ⬜ | Add formal Complexity Analysis subsection |
| B9 | Algorithm 3 break logic flaw under unstable sort | 🔴 CRITICAL | ✅ | Lemma `closure_completeness` and "Remark on sort stability" added; algorithm uses strict `<` |
| B10 | Lemma 4 (early termination) circular re: PQ ordering cost | 🟠 MAJOR | ✅ | Rewritten to cite max-heap invariant + $O(\log\|Q\|)$ ops; add to complexity table |
| B11 | Standard pruning presented as novel; P4 (transaction trim) unreproducible | 🟠 MAJOR | 🟡 | Old P4 (Transaction Trimming) replaced by Subset Upper Bound — formally justified. Need pseudocode for each P-strategy |
| B12 | Synthetic uncertainty arbitrary; no sensitivity analysis | 🔴 CRITICAL | ⬜ | **Exp3** — vary $\alpha$, $\rho$, $P_{min}$, $P_{max}$; report Jaccard stability of top-k |
| B13 | No variance / significance testing in ablation | 🔴 CRITICAL | ⬜ | All experiments run with ≥5 reps; report mean ± std + Wilcoxon |

---

## C. Reviewer #2 — Major Concerns

| # | Issue | Severity | Status | Notes |
|---|---|---|---|---|
| C1 | Differentiate from prior B&B / best-first frameworks | 🟠 MAJOR | ✅ | Already addressed in revision; reinforce with comparison table |
| C2 | **No external baselines (only V1–V4 internal variants)** | 🔴 CRITICAL | ⬜ | **Exp1+2 combined** — add TopKPFIM (2017) and ITUFP (2023) |
| C3 | Synthetic uncertainty robustness | 🔴 CRITICAL | ⬜ | Same as B12 — Exp3 |
| C4 | Memory: PQ size + peak heap stats | 🟠 MAJOR | 🟡 | `maxPqSize` already tracked in V1; need to wire into reports + add JVM peak heap (Exp8) |
| C5 | Time and space complexity discussion | 🟠 MAJOR | ⬜ | Add Complexity Analysis subsection |
| C6 | P7 needs formal explanation + worked example | 🟡 MINOR | ✅ | Worked example already added in revision |
| C7 | Notation consistency ($\sigma$ vs $\theta$ vs `support()`) | 🟡 MINOR | 🟡 | Notation table added; cross-check usage in algorithms and prose |
| C8 | Grammatical revisions for clarity | 🟡 MINOR | 🟡 | Abstract still has typo "becauseprobabilistic" in old version (fixed in revision); needs final pass |
| C9 | Figure readability and labeling | 🟡 MINOR | ⬜ | Regenerate at 300 DPI with B&W-friendly line styles |
| C10 | Reproducibility info (runtime averaging, params, JVM config) | 🟡 MINOR | ⬜ | Add Reproducibility subsection (JVM flags, seed=42, git hash, dataset URLs, rep count) |

---

## D. Reviewer #3 — Minor Concerns

| # | Issue | Severity | Status | Notes |
|---|---|---|---|---|
| D1 | "Late-appearing items" pruning concern (milk-bread-beer-wine example) | 🟠 MAJOR | ⬜ | **Address in writing only** (per user instruction) — add pedagogical paragraph + math note in Phase 1 description; clarify single-scan vertical DB construction guarantees no item is missed |

---

## E. New Manuscript Sections / Subsections to Write

| # | Section | Status | Notes |
|---|---|---|---|
| E1 | Complexity Analysis subsection (time + space) | ⬜ | Per-candidate $O(m_X^2)$ + $O(m_X \log m_X)$; whole-algorithm $O(\|C_k\| \cdot M^2)$; heap ops $O(\log\|Q\|)$ |
| E2 | Pedagogical paragraph addressing R3 concern | ⬜ | Show that single Phase-1 vertical-DB scan registers ALL items regardless of position |
| E3 | External-baseline adaptation paragraph | ⬜ | Document modifications to TopKPFIM and ITUFP for fair comparison |
| E4 | Reproducibility subsection | ⬜ | JVM, seed, hardware, dataset URLs, repetition count, code repo URL |
| E5 | Updated novelty positioning paragraph | 🟡 | Already partly written; reinforce with comparison table |
| E6 | Pruning-group taxonomy (G1–G4) for restructured ablation | ⬜ | Group P1+P2 (frontier), P3 (item), P4+P5 (upper bound), P6+P7 (tidset) |

---

## F. New Experiments (Java implementation + raw results)

| # | Experiment | File | Status | Reviewer mapping |
|---|---|---|---|---|
| F1 | Main comparison: V1–V4 + TopKPFIM + ITUFP | `Exp1_MainComparisonAndBaselines.java` | ⬜ | C2 (CRITICAL), B13 |
| F2 | Uncertainty sensitivity ($\alpha$, $\rho$, $P_{min/max}$) | `Exp3_UncertaintySensitivity.java` | ⬜ | B12, C3 (CRITICAL) |
| F3 | Group ablation (G1, G2, G3, G4) | `Exp4a_GroupAblation.java` | ⬜ | B13, C5 |
| F4 | Group dominance heatmap | `Exp4b_GroupDominance.java` | ⬜ | B13 |
| F5 | Group synergy / pairwise interaction | `Exp4c_GroupSynergy.java` | ⬜ | B13 |
| F6 | Scalability in $k$ | `Exp5_ScalabilityK.java` | ⬜ | C5 |
| F7 | Memory profile (max PQ size + peak heap) | `Exp8_MemoryProfile.java` | ⬜ | C4 |

REMOVED PER USER INSTRUCTION:
- ~~Exp6_LateItemRobustness.java~~ → addressed in writing (D1)
- ~~Exp7_TieBreakingSensitivity.java~~ → addressed in writing (B7)
- ~~Exp9_ComplexityValidation.java~~ → handled by E1 + Exp5

---

## G. External Baseline Implementations

| # | Baseline | DOI | Year | Status |
|---|---|---|---|---|
| G1 | TopKPFIM (Li, Zhang, Zhang) | 10.1016/j.procs.2017.11.483 | 2017 | ⬜ |
| G2 | ITUFP (Davashi) | 10.1016/j.eswa.2022.119156 | 2023 | ⬜ |

Adaptations needed:
- Both: post-filter for closedness on output (fair-comparison adaptation)
- ITUFP: disable interactive re-mining (run as one-shot top-k)
- Both: use same uncertain-DB injection method as TUFCI for fairness
- Both: same tau, k, datasets

---

## H. Response-to-Reviewers Letter

| # | Item | Status |
|---|---|---|
| H1 | Skeleton draft mapping every reviewer point to a change | ⬜ |
| H2 | Reviewer #1 detailed responses (13 points) | ⬜ |
| H3 | Reviewer #2 detailed responses (10 points) | ⬜ |
| H4 | Reviewer #3 detailed responses (1 point) | ⬜ |
| H5 | Editorial requirements responses (Table 3, style, etc.) | ⬜ |
| H6 | Final proofreading pass | ⬜ |

---

## I. Final Submission Checklist

| # | Item | Status |
|---|---|---|
| I1 | Manuscript (clean) PDF compiled | ⬜ |
| I2 | Revised Manuscript with Track Changes (latexdiff) PDF | ⬜ |
| I3 | Response to Reviewers letter | ⬜ |
| I4 | All figures uploaded as separate files (PLOS ONE requirement) | ⬜ |
| I5 | Cover letter (mention any new financial disclosure if changed) | ⬜ |
| I6 | All co-author ORCIDs verified in submission system | ⬜ |
| I7 | Code repository public + DOI (Zenodo or similar) | ⬜ |
| I8 | Dataset access documented in Data Availability statement | ⬜ |

---

## Status Summary

- **Total items**: 60+
- **✅ Done**: 9
- **🟡 Partially Done**: 9
- **⬜ Not Done**: 42+

**Remaining critical-path items (🔴)**: B12, B13, C2, C3 — all addressed by F1, F2, F3.