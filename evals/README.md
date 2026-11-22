# Evaluation Design: Selection Pressure

## Principle

Every working rule, playbook wording, instruction constraint, or upstream skill pulled from `skills/` is a hypothesis. The evaluation layer tests hypotheses under local conditions. Fitness is always local: measured on representative tasks for this codebase, under recorded stack versions and LLM model version, on a specific date.

## Suite Structure

Starter suites live under `evals/`:

- `evals/general/tasks.md`: 6 universal tasks for all kinds of intelligent work (specification, root-cause diagnosis, evidence-grounded research, invariant-preserving refinement, quantitative data analysis, CLI contract verification).
- `evals/spark/tasks.md`: 6 Apache Spark tasks (local-scale reproducible fixtures with optional production-scale notes).
- `evals/spring/tasks.md`: 6 Java Spring tasks (JUnit, slice tests, and Testcontainers).

Every task defines **five fields**:

1. **Input:** Fixture, dataset, source set, or environment state (schema, distribution, code or document state, configuration).
2. **Operation:** What the agent must do, referencing a specific playbook or instruction file.
3. **Scoring:** Hard binary checks first (tests pass, invariants hold, zero fabricated citations, contract met), followed by primary task metrics and cost telemetry (`tokens`, `time_sec`).
4. **Baseline:** Current champion result, or `to be measured` until a real run is recorded.
5. **Human-Input Data:** Required real-world human-supplied cases under `evals/data/<suite>/` and tier classification (`human` or `synthetic`).

## Execution and Deterministic Scoring

Generation and scoring are strictly separated to eliminate agent self-scoring bias:

1. **Generate:** Run `.github/prompts/run-eval.prompt.md` in a clean git worktree for one `variant_id`. Capture raw artifacts and machine-readable test/metric outputs under `evals/runs/<run-name>/`. The agent never grades pass/fail and never writes to `evals/results/`.
2. **Score deterministically:** Run `python3 scripts/score-eval.py` in the terminal. The script validates `evals/data/<suite>/`, enforces the human-data gate, applies the lexicographic rule against the champion record, stamps `date`, `git_sha`, `model_id`, `stack_versions`, and `prompt_hash`, and writes an immutable JSON record to `evals/results/`.

See `evals/results/README.md` for the exact JSON schema and an explicitly marked example record.

<!-- BEGIN CANONICAL SELECTION AND CONTINGENCY RULES -->
### Selection, Pruning, and Contingency Rules

- **Challenger entry:** Every new variant enters as a challenger. It never replaces the champion directly.
- **Starter suites (fewer than 20 tasks):** Use paired champion-vs-challenger runs on identical fixtures and seeds. Prune or rewrite immediately if the challenger introduces any binary regression against the champion on any task, or fails to improve its target task across 3 paired trials.
- **Mature suites (20 or more tasks):** A challenger that loses to the champion in two consecutive full-suite runs is pruned or rewritten.
- **Lexicographic promotion (no blended total score):** A challenger replaces the champion only when it passes 100% of required human-input (Tier 1) binary checks with zero regressions, introduces zero synthetic (Tier 2) binary regressions, improves primary metrics on Tier 1 tasks above the 5% timing noise floor, and stays within the cost guardrail (median token cost at most 2.0x champion unless correctness improved). Synthetic-only runs may prune weak challengers early, never promote a champion.
- **Human-data gate:** Any eval run missing required `evals/data/<suite>/` files (or containing template placeholders) is recorded as `data_incomplete` and produces no keep, promote, prune, or rewrite verdict.
- **Upgrade regression:** A champion that regresses on a re-run after a major stack or model version change loses champion status, and the suite re-opens to challengers.
- **Local contingency:** Every result is local to one codebase, one task distribution, one set of stack versions, one LLM model version, and one date. Results recorded before a major stack or model version change are stale and must be re-run before citation. Results from another codebase are priors, not evidence.
<!-- END CANONICAL SELECTION AND CONTINGENCY RULES -->

## Human-Input Data vs. Synthetic Fixtures

Eval cases are tagged as two non-compensable tiers:

- **Tier 1 (`human`):** Real cases, real distributions, real CLI invocations, and human-verified expected outputs stored under `evals/data/<suite>/`. Required to promote a challenger to champion.
- **Tier 2 (`synthetic`):** Controlled synthetic fixtures and edge cases. Useful for fast pre-screening and early pruning of broken challengers; never sufficient on their own to promote a champion.

**Decoupling from live ticket work:** Per-ticket verification data lives under `evidence/` so live tickets are never blocked waiting to curate benchmark suites. After Stage 5 approval, gardeners promote high-signal real cases from `evidence/` into `evals/data/<suite>/` with complete headers.

## What This Eval System Is Not

It is not a global benchmark or competition. There are no cross-project scores, no global variant rankings, and no preference votes. Every record measures one variant against a fixed local rubric and its local champion.