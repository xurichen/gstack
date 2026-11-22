# General Intelligent Work Evaluation Suite (Starter Suite)

This starter suite covers universal knowledge, analytical, engineering, and operational tasks beyond Spark and Spring. Every task has five fields (`Input`, `Operation`, `Scoring`, `Baseline`, `Human-Input Data`) and runs locally without cloud cluster dependencies.

## Task 1: Ambiguous Request to Testable Specification

- **Task ID:** `general-spec-01`
- **Tier:** `human`

**Input**
- A messy, underspecified stakeholder request (3 to 5 paragraphs containing conflicting constraints, hidden edge cases, and unstated success criteria) stored in `evals/data/general/general-spec-01-stakeholder-brief.md`.

**Operation**
- Use `gardener-mode` (Stage 1) or `planner.agent.md` with `.github/instructions/shared.instructions.md`.
- Produce a testable specification with explicit `[Fact]` vs. `[Recommended Practice]` labels, observable acceptance criteria, invariants, open-question list, and verification method.

**Scoring**
- Binary: All required spec checklist sections present, zero fabricated stakeholder facts, all planted conflicts surfaced, every acceptance criterion falsifiable -> `true`, else `false`.
- Primary metric: `conflict_recall_pct` (float, higher is better).
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Real anonymized stakeholder brief with a human-verified list of planted ambiguities, conflicts, and mandatory invariants at `evals/data/general/general-spec-01-stakeholder-brief.md`.

## Task 2: Root-Cause Diagnosis of a Multi-Factor Failure

- **Task ID:** `general-diagnose-02`
- **Tier:** `human`

**Input**
- A real or anonymized incident bundle (timeline, error logs, config diff, and metric snapshot) where one obvious symptom masks a deeper root cause, stored in `evals/data/general/general-diagnose-02-incident-bundle.json`.

**Operation**
- Use `.github/prompts/work-diagnose.prompt.md`.
- Form a falsifiable hypothesis, isolate the true root cause, cite exact log lines or timestamps, and propose a minimal fix plus regression check.

**Scoring**
- Binary: True root cause identified (not surface symptom), zero fabricated log lines or timestamps, falsifiable check included -> `true`, else `false`.
- Primary metric: `root_cause_precision` (float 0.0 to 1.0, higher is better).
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Real incident bundle with human-verified root cause and accepted regression check at `evals/data/general/general-diagnose-02-incident-bundle.json`.

## Task 3: Evidence-Grounded Trade-Off and Decision Memo

- **Task ID:** `general-research-03`
- **Tier:** `human`

**Input**
- A local folder of 4 to 6 primary source excerpts (pricing tables, technical specs, policy docs, or benchmark CSVs) and a concrete decision question with hard constraints, stored in `evals/data/general/general-research-03-source-pack.md`.

**Operation**
- Use `.github/prompts/work-research.prompt.md`.
- Produce a symmetric comparison matrix, quantitative driver breakdown, recommendation, strongest counterargument, and source verification log.

**Scoring**
- Binary: Zero fabricated figures or citations, every hard constraint respected, all options compared symmetrically across shared criteria -> `true`, else `false`.
- Primary metric: `citation_accuracy_pct` (float, higher is better).
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Curated primary-source packet and human-verified ground-truth fact table at `evals/data/general/general-research-03-source-pack.md`.

## Task 4: Invariant-Preserving Document or Spec Compression

- **Task ID:** `general-refine-04`
- **Tier:** `synthetic`

**Input**
- A bloated 1,500-word technical design memo containing 12 mandatory factual invariants (numbers, SLAs, dates, API constraints) buried in filler prose and redundant sections.

**Operation**
- Use `.github/prompts/work-refine.prompt.md`.
- Compress the memo by at least 45% (Subtract Before You Add) while preserving 100% of the 12 mandatory invariants verbatim in meaning and value.

**Scoring**
- Binary: Word count reduced by at least 45% AND all 12 factual invariants preserved with zero distortion -> `true`, else `false`.
- Primary metric: `word_reduction_pct` (float, higher is better).
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Optional human-annotated real memo at `evals/data/general/general-refine-04-memo-invariants.json` (synthetic fixture sufficient for Tier 2 early pruning).

## Task 5: Quantitative Dataset Audit and Anomaly Analysis

- **Task ID:** `general-data-05`
- **Tier:** `synthetic`

**Input**
- A local CSV dataset (5,000 rows) containing planted anomalies: duplicate IDs, negative amounts, timezone boundary skew, and a silent category-mapping drift.

**Operation**
- Use `.github/prompts/work-diagnose.prompt.md` or `work-create.prompt.md`.
- Write and run a deterministic verification script on the real CSV, reconcile totals, isolate every anomaly class, and explain the quantitative impact.

**Scoring**
- Binary: Script executes cleanly on the real CSV, all 4 planted anomaly classes detected with exact row counts, reconciled totals match ground truth -> `true`, else `false`.
- Primary metric: `anomaly_f1` (float 0.0 to 1.0, higher is better).
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Optional anonymized production CSV sample and human-verified reconciliation totals at `evals/data/general/general-data-05-dataset-audit.json`.

## Task 6: CLI Tool Contract Verification

- **Task ID:** `general-cli-06`
- **Tier:** `synthetic`

**Input**
- A small CLI script (Python or Node) with a documented flag/stdin/stdout/exit-code contract and 2 subtle regressions (non-zero exit code swallowed on invalid input; malformed JSON output on empty stdin).

**Operation**
- Use `.github/prompts/work-diagnose.prompt.md` and `work-create.prompt.md`.
- Reproduce failures with real terminal invocations, fix both regressions one variable at a time, and prove the contract with automated CLI tests.

**Scoring**
- Binary: All real CLI contract assertions (stdout, stderr, exit codes) pass on valid, empty, and malformed inputs -> `true`, else `false`.
- Primary metric: `contract_checks_passed` (integer, higher is better).
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Real command invocations and human-verified terminal stdout/stderr/exit-code transcripts at `evals/data/general/general-cli-06-cli-transcript.md`.
