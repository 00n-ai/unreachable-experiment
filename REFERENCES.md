# References and how to use them

## Closest methodological foundations

1. **Saparov, Abulhair, and He He (2023). Language Models Are Greedy Reasoners: A Systematic Formal Analysis of Chain-of-Thought. ICLR.** [Paper](https://arxiv.org/abs/2210.01240). PrOntoQA generates synthetic worlds with formal logical structure, enabling analysis of generated proofs and proof-planning difficulties. Cite when motivating synthetic, formally verifiable reasoning tasks. Our current controlled-connectivity generator is not the original PrOntoQA benchmark, and these results are not directly comparable scores.

2. **Clark, Peter, Oyvind Tafjord, and Kyle Richardson (2020). Transformers as Soft Reasoners over Language. IJCAI, 3882–3890.** [Paper and proceedings](https://www.ijcai.org/proceedings/2020/537). RuleTaker supplies natural-language facts and rules and tests deduction over them, including reasoning depth. Cite for the natural-language rule-based task foundation. Its training/evaluation setup differs from our single-call inference study.

3. **Tafjord, Oyvind, Bhavana Dalvi, and Peter Clark (2021). ProofWriter: Generating Implications, Proofs, and Abductive Statements over Natural Language. Findings of ACL-IJCNLP, 3621–3634.** [Paper](https://aclanthology.org/2021.findings-acl.317/). Cite for explicit proof generation and distinguishing answer correctness from supporting proofs. Do not imply that our final-answer metric establishes proof validity or internal reasoning faithfulness.

## Statistical methods

4. **Clopper, C. J., and E. S. Pearson (1934). The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial. Biometrika, 26(4), 404–413.** [DOI](https://doi.org/10.1093/biomet/26.4.404). Cite for exact binomial confidence limits. Our analysis additionally applies the Bonferroni union-bound correction across 20 cells and a conservative envelope for unknown outcomes; those additions are not attributed to this paper.

5. **Holm, Sture (1979). A Simple Sequentially Rejective Multiple Test Procedure. Scandinavian Journal of Statistics, 6(2), 65–70.** [Original paper scan](https://www.ime.usp.br/~abe/lista/pdf4R8xPVzCnX.pdf). Optional background for familywise error control and multiple comparisons. **We did not use Holm's step-down procedure**: the current intervals use ordinary Bonferroni, with each tail set to 0.05/(2 × 20). Do not cite Holm as the procedure actually executed.

## Suggested positioning

Synthetic natural-language deduction, branching proof search, and proof evaluation already have substantial prior work. The present artifact studies successful correct rejection and matched reachable controls across selected depth–breadth settings, with explicit output-budget failure handling and a retrospective jointly corrected analysis. Whether that combination constitutes a publishable novelty requires a broader literature review; these citations are a starting set, not an exhaustive novelty search.

The evidence is specific to the prompt, generator, topology, provider/model versions and output budgets. It does not establish prompt-independent capacity, general hallucination rates, or real-world task safety. Links identify primary papers; no paper PDFs are included in this repository.
