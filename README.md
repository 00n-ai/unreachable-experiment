# Directed graph reasoning: a reliability study

**Sheraz Mahmood** · Research snapshot, 1 October 2026

Open [index.html](index.html) for the interactive experiment explainer. It works offline, with no API key, build step, or external JavaScript dependency.

## What this release contains

This is the completed **Condition A, four-model confirmation analysis**, not every historical exploratory experiment. It contains 80,000 scored observations: 40,000 unreachable queries and 40,000 matched reachable controls. Models are identified by their recorded provider IDs; aliases and availability may change.

- `index.html`: graph examples, exact recorded prompts, gold answers, recorded responses, model results and limitations.
- `data/explainer.json`: graph/prompt examples and all 20 aggregate model–complexity cells.
- `data/luna-outcomes.jsonl.gz` and `data/deepinfra-outcomes.jsonl.gz`: all 80,000 observations, including final response text. Exported through a field allowlist; provider IDs, transport envelopes, credentials and logs are excluded.
- `reports/joint-analysis.json` and `.md`: full-precision joint intervals, findings, and provenance hashes. Paths inside these original reports refer to the private source workspace, not files promised in this release.
- `src/graph_reasoning/`: original graph generator, complexity metrics and prompt builders. No model execution code is included.
- `verify.py`: offline checksum, coverage, aggregate-count and interval verification.
- `REFERENCES.md`, `references.bib`: related work and methods citations.
- `CITATION.cff`: authorship metadata for citing this research artifact.

## Main finding and scope

Each model has tested settings above and below 90% successful correct rejection under jointly corrected intervals. This is **not** a controlled model ranking, a universal capacity bound, or a production-safety guarantee. It is a retrospective joint analysis of completed confirmation studies, not a prospectively registered four-model study. Different model neighborhoods and inference settings were tested. All 20 primary cells are retained.

Breadth means children per internal predicate, not maximum layer width. The topology consists of two disconnected spines with distractor leaves. The target exists in both answer classes; changing the entity's starting fact changes reachability. Failure to derive a positive query is scored False under this benchmark's stated reachability convention—not a general claim that lack of evidence implies falsity.

## Reproduce the statistical summary

Use Python 3.11 or newer in a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python verify.py
```

The verifier recomputes the 20 primary counts and Bonferroni-adjusted Clopper–Pearson intervals from exported scored rows. It does not replay provider transport parsing or independently reassess every model response. Original provider envelopes and operational logs are intentionally not included. Model text is provided for further scoring audits; automated scores are the frozen original classifications.

Recreate a world with `make_connectivity_example(depth, breadth, replicate, reachable, negated, seed)` from `src/graph_reasoning/connectivity_dataset.py`, and create its messages with `condition_a_branching` from `prompts.py`. Instance IDs encode these parameters: `connectivity-d4-b2-i30979-u-p-s62471930`; `r/u` means reachable/unreachable, `n/p` means negated/non-negated. Luna seed: 62471930; DeepInfra seed: 62472001. The exact full provider request bodies are not part of this public export; hashes link observations to the archived originals.

## Publish on GitHub

1. Create a repository and upload **this directory's contents**, not the parent research workspace.
2. Review the attribution, model-response redistribution terms, and choose licenses for your code and data before publication. No redistribution license has been assumed or granted by this preparation step.
3. For GitHub Pages, select deployment from your repository's default branch and `/ (root)` in Settings → Pages. The entry point is `index.html`.
4. Add your repository URL to `CITATION.cff` once it exists. Consider a versioned archival DOI for a paper release.

The gzip files are intended for Git-based upload, not manual expansion into thousands of files. The page does not need them to render. No repository has been created or pushed by this preparation step.

## Data dictionary

One JSON object per line after gzip decompression. Key fields: `model`, `instance_id`, `depth`, `breadth`, `reachable`, `negated`, `gold_answer`, parsed `answer`, `classification`, `raw_content` (final model response text), `request_sha256`. Classifications: `correct`, `wrong_final`, `budget_exhausted`, `no_final`, `unknown`. A correct parsed answer with output-budget exhaustion is not a successful completion. Infrastructure unknowns remain unknown; intervals cover both best- and worst-case assignments.

The inferential family covers 20 successful-correct-rejection cells only, with 2,000 primary worlds each. Reachable accuracy is descriptive. Correct-rejection failure is not synonymous with an explicit false positive. See the report for the distinction and the statistical assumptions.

## Attribution and provenance

Research author: Sheraz Mahmood. Research tooling and explainer preparation used AI assistance. This release is a research artifact, not a peer-reviewed paper. The generator in this snapshot is the project's controlled-connectivity generator, not an unmodified PrOntoQA dataset. Cite the related papers as methodological foundations, not as endorsements or proof of novelty. Third-party paper PDFs and upstream benchmark data are not redistributed here.
