# Archival Methodology: Universal Evolutionary Workflow for Intelligent Work

## 1. Overview

This methodology combines an evolutionary outer loop (**Gardener Loop**: `Plant -> Measure -> Select -> Prune`) with a disciplined inner loop (**Full-Track 5 Stages** or **Fast-Track 3 Steps**) that applies to every kind of intelligent work: software engineering, data pipelines, machine learning, research and synthesis, technical or editorial writing, quantitative modeling, strategy, operations, and CLI tooling.

Documented platform mechanisms and primary-source evidence are labeled `[Fact]`. Process conventions, checklists, and thresholds introduced by this methodology are labeled `[Recommended Practice]`.

## 2. The Inner Loop

### Full-Track (5 Stages)

1. **Stage 1: Clarify and Specify (`planner`, read-only).** Convert ambiguous goals into testable acceptance criteria, invariants, primary sources, budgets, and rollback conditions.
2. **Stage 2: Slice into Tickets (`planner`, read-only).** Split work into vertical slices (one input/entry point to one verifiable output/effect). Never mix semantic or scope changes with optimization or refactoring.
3. **Stage 3: Execute by Playbook (`executor`).** Select one playbook from `.github/prompts/`, run the Red-Green-Refine loop, change one variable at a time, and record before/after evidence under `evidence/`.
4. **Stage 4: Verify Against Real Artifact (`executor`).** Validate against real artifacts, datasets, databases (Testcontainers), packaged jobs, live CLI commands, or primary sources. Refuse completion when evidence is missing.
5. **Stage 5: Single Review (`reviewer`, read-only).** Perform one review checking spec conformance, evidence completeness, compatibility/invariants, rollback readiness, and the five grounding principles. Findings return work to a named earlier stage.

### Fast-Track (3 Compressed Steps)

For small fixes, focused edits, or routine tasks:

1. **Single-Turn Brief (`planner`):** State goal, acceptance check, invariants, and verification method.
2. **Execute and Verify (`executor`):** Run one playbook, change one variable at a time, and verify against the real artifact.
3. **Concise Single Review (`reviewer`):** Confirm acceptance criteria, invariants, and rollback in one pass.

## 3. Five Grounding Principles

1. **Prove it works:** Verify the real output artifact on real inputs or primary sources rather than mocks, notebooks, or intuition.
2. **Explain the number:** Trace every quantitative claim or performance delta to its underlying driver or mechanism.
3. **Test behavior, not implementation:** Assert observable contracts, schemas, outputs, and decision criteria rather than internal steps.
4. **Subtract before you add:** Remove unused columns, redundant queries, dead code, or filler prose before adding caches, hardware, or abstractions.
5. **Fix root causes:** Resolve the underlying mechanism rather than masking symptoms.

## 4. Domain Packs

Universal instructions live in `.github/instructions/shared.instructions.md` (`applyTo: "**"`) and universal playbooks live in `.github/prompts/work-*.prompt.md`.

Domain packs layer specialized checklists, guardrails, and verification gates on top:

- **Apache Spark:** `.github/instructions/spark.instructions.md`, `spark-performance.prompt.md`, `spark-correctness.prompt.md`, and `evals/spark/tasks.md`.
- **Java Spring:** `.github/instructions/spring.instructions.md`, `spring-feature.prompt.md`, `spring-diagnose.prompt.md`, and `evals/spring/tasks.md`.
- **Additional domains:** Add `.github/instructions/<domain>.instructions.md`, optional playbooks, and `evals/<domain>/tasks.md`.

## 5. Evolutionary Selection and Deterministic Scoring

Live tasks never pause for mid-task gardening; friction notes go to `evals/observations/`. During dedicated gardening sessions:

1. Plant a challenger variant with an explicit hypothesis.
2. Generate candidate outputs in a clean worktree via `.github/prompts/run-eval.prompt.md`.
3. Score deterministically via `python3 scripts/score-eval.py`, which validates human-input data headers, enforces lexicographic promotion without blended total scores, records `git_sha`, `model_id`, `stack_versions`, and `prompt_hash`, and writes an immutable JSON record to `evals/results/`.
4. Promote, keep, prune, or rewrite strictly according to the canonical Selection, Pruning, and Contingency Rules in `evals/README.md`.

## 6. Boundaries and Self-Testing

This methodology is not an authoritative standard from Apache, Spring, or GitHub. Validate its local value via paired A/B tests on representative local tasks measuring defect rate, rework, token consumption, and wall-clock time under identical acceptance criteria.