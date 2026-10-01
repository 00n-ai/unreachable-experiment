# Joint four model analysis of correct rejection

## Main conclusion

> Under the tested prompt, graph representation, and model-specific inference settings, each of the four models has measured settings with successful correct-rejection probability above 90% and settings below 90%, supported by jointly corrected 95% confidence intervals.

This is a retrospective joint analysis of completed confirmation cohorts, not a prospectively registered four-model experiment. It includes every correct-rejection setting in those cohorts, without selecting cells according to their outcomes. The original study analyses and sealed artifacts remain unchanged. No new model calls were made.

## Statistical method

The family contains 20 model–complexity settings: eight for GPT-5.6 Luna and four each for Gemma 4 31B, Hermes 3 Llama 3.1 405B, and DeepSeek V4.1 Flash. Each has 2,000 unreachable, non-negated queries from fresh world units. There are 40,000 primary observations; the audit also checks their 40,000 reachable controls, which are outside this inferential family.

Successful correct rejection requires an unambiguous final False without output-budget exhaustion. Wrong answers, no final answer, and budget exhaustion are failures. Infrastructure unknowns remain unknown. For C known successes and U unknowns among 2,000 planned cases, the interval runs from the exact lower bound for C successes to the exact upper bound for C+U successes. This is conservative under either assignment of missing outcomes.

Use two-sided Clopper-Pearson intervals with each tail alpha 0.05/(2×20) = 0.00125. Bonferroni gives at least 95% simultaneous coverage under the binomial sampling assumptions, without requiring independence between cells or models. A cell is above 90% only if its lower bound exceeds 0.90; below 90% only if its upper bound is below 0.90; otherwise unresolved. With no unknowns, 1,840/2,000 is the minimum count supporting above 90%.

The correction applies only to successful correct rejection. Explicit false-positive incidence, reachable accuracy, proof validity, model superiority, and production safety are not included. The original DeepInfra study jointly corrected rejection and false-positive endpoints; its original analysis remains valid separately and is not replaced by this narrower-endpoint retrospective family.

## All measured settings

| Model | Depth | Breadth | Correct / planned | Unknown | Joint 95% interval | Decision |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| Luna | 4 | 2 | 1994/2000 (99.70%) | 0 | 99.12–99.94% | Above 90% |
| Luna | 4 | 4 | 1990/2000 (99.50%) | 0 | 98.82–99.85% | Above 90% |
| Luna | 8 | 2 | 1980/2000 (99.00%) | 0 | 98.13–99.54% | Above 90% |
| Luna | 8 | 4 | 1952/2000 (97.60%) | 0 | 96.38–98.51% | Above 90% |
| Luna | 16 | 2 | 1933/2000 (96.65%) | 0 | 95.25–97.74% | Above 90% |
| Luna | 16 | 4 | 1880/2000 (94.00%) | 0 | 92.22–95.49% | Above 90% |
| Luna | 32 | 2 | 1838/2000 (91.90%) | 0 | 89.89–93.63% | Unresolved |
| Luna | 32 | 4 | 1707/2000 (85.35%) | 0 | 82.82–87.65% | Below 90% |
| Gemma 31B | 2 | 2 | 2000/2000 (100.00%) | 0 | 99.67–100.00% | Above 90% |
| Gemma 31B | 4 | 4 | 1891/2000 (94.55%) | 18 | 92.84–96.74% | Above 90% |
| Gemma 31B | 4 | 8 | 1637/2000 (81.85%) | 31 | 79.12–85.83% | Below 90% |
| Gemma 31B | 8 | 4 | 1126/2000 (56.30%) | 134 | 52.91–66.24% | Below 90% |
| Hermes 405B | 1 | 2 | 1937/2000 (96.85%) | 0 | 95.49–97.90% | Above 90% |
| Hermes 405B | 1 | 4 | 1831/2000 (91.55%) | 0 | 89.51–93.32% | Unresolved |
| Hermes 405B | 2 | 2 | 763/2000 (38.15%) | 0 | 34.88–41.49% | Below 90% |
| Hermes 405B | 2 | 4 | 171/2000 (8.55%) | 0 | 6.77–10.60% | Below 90% |
| DeepSeek V4.1 Flash | 4 | 2 | 1843/2000 (92.15%) | 0 | 90.17–93.86% | Above 90% |
| DeepSeek V4.1 Flash | 4 | 4 | 1699/2000 (84.95%) | 0 | 82.40–87.28% | Below 90% |
| DeepSeek V4.1 Flash | 16 | 2 | 1630/2000 (81.50%) | 0 | 78.75–84.05% | Below 90% |
| DeepSeek V4.1 Flash | 16 | 4 | 1178/2000 (58.90%) | 0 | 55.52–62.22% | Below 90% |

The displayed correct/planned fraction is the lower observed success fraction where outcomes are unknown, not an assertion that unknowns were incorrect. All 183 infrastructure unknowns belong to Gemma. The decisions incorporate their best- and worst-case assignments. Ten cells are above 90%, eight below, and two unresolved.

## Supported boundary brackets

| Model | Above 90% setting | Below 90% setting | Fixed coordinate |
| --- | --- | --- | --- |
| Luna | 16 × 4 | 32 × 4 | breadth 4 |
| Gemma 31B | 4 × 4 | 4 × 8 | depth 4 |
| Hermes 405B | 1 × 2 | 2 × 2 | breadth 2 |
| DeepSeek V4.1 Flash | 4 × 2 | 4 × 4 | depth 4 |

Coordinates are depth × breadth. These are measured passing/failing anchor pairs, not a unique continuous frontier. We do not assume monotonicity or infer outcomes at untested intermediate settings. Gemma also has a supported depth bracket from 4×4 to 8×4.

## What changed for Luna

Luna at 32×2 remains 1,838/2,000 correct (91.90%), but its joint interval is now 89.89–93.63%. It is unresolved under this family, whereas the original eight-cell correction placed its lower bound just above 90%. Consequently, do not use 32×2 to 32×4 as a jointly supported breadth bracket. The supported joint bracket instead runs from 16×4 (94.00%, interval 92.22–95.49%) to 32×4 (85.35%, interval 82.82–87.65%). No observations or scores changed; only the multiplicity correction changed.

## Interpretation and limits

The data support the existence of observed high- and low-reliability settings for each model in this benchmark. They do not establish an intrinsic, prompt-independent reasoning limit or a production-safe context size. The fixed topology is two disconnected spines with distractor leaves; breadth is the generator branching factor. Failures include inability to finish within the output budget, not only explicit incorrect conclusions.

Luna used native OpenAI Batch with medium reasoning effort; the other three used DeepInfra Batch with their recorded settings. Cells, providers, generation seeds, and model settings differ. Common DeepInfra worlds are paired across models, while Luna uses a separate cohort. Do not read these brackets as a controlled cross-model ranking or a causal decomposition of depth and breadth.

The cell selections were informed by earlier exploratory cohorts, followed by fresh confirmation worlds. The joint family was chosen after those confirmations completed. Report it transparently as retrospective; this correction does not cover an unrestricted search over alternative endpoints, thresholds, prompts, or historical cohorts, and it does not make earlier interim monitoring an anytime-valid test.

## Reproducibility

Run `python3 scripts/analyze_joint_rejection90.py` from experiment-1. The script verifies both completed execution seals and outcome hashes, checks exact manifest coverage and identities, replays the frozen final-answer classifications for all 80,000 outcomes, and computes fresh intervals from the outcome rows rather than relying on summary reports. It only writes separate report artifacts.

The companion `reports/joint_four_model_rejection90_20261001.json` records full-precision intervals, counts, cohort seals, input hashes, and analysis-source hashes. Original study files are never rewritten. Existing output reports can only be regenerated identically; differing output is rejected.
