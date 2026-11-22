# Universal Engineering and Knowledge Work Methodology: Gardener Loop + Five-Stage Pipeline

**Default entry point:** `gardener-mode` custom agent (`.github/agents/gardener-mode.agent.md`). It wraps the five-stage inner loop (with a fast-track option for small tasks) inside the evolutionary gardener loop and works for all kinds of intelligent work: software engineering, data and ML, systems architecture, research and synthesis, technical or editorial writing, product and strategy, quantitative analysis, operations, and CLI automation.

**Domain preset:** `spark-spring-mode` (`.github/agents/spark-spring-mode.agent.md`) pre-selects the Apache Spark and Java Spring domain packs on top of the same core methodology. Standalone role agents (`planner`, `executor`, `reviewer`) remain available for direct use.

This file is always active across the entire repository. Label documented platform or source mechanisms as **Fact**, and label conventions introduced by this methodology as **Recommended Practice**. Never blend the two.

## Constitution vs. Evolvable Genome

- **Fixed apparatus (Constitution):** These invariants stay constant so evaluation results remain comparable across seasons: `skills/` remains byte-identical to upstream; one stage has one router; verification gates require real-artifact evidence; one review pass closes a task; scoring is deterministic via `scripts/score-eval.py`; no verdict is emitted on incomplete human data; repository prose is in English.
- **Evolvable genome:** Playbooks (`.github/prompts/`), scoped instructions (`.github/instructions/`), domain checklists, and upstream skills pulled from `skills/` are hypotheses subject to selection pressure.

## The Inner Loop: Five Stages (Full-Track) and Fast-Track

Every unit of intelligent work uses either the **Full-Track** (multi-slice features, architecture, research reports, risky changes, high ambiguity) or the **Fast-Track** (small bug fixes, focused edits, short analyses, routine CLI or document updates).

| Stage | Goal | Full-Track Router | Fast-Track Equivalent |
|---|---|---|---|
| 1. Clarify and Specify | Turn observable outcomes into testable acceptance criteria | `planner` | Single-turn brief (goal, constraints, verification check) |
| 2. Slice into Tickets | Split work into independently verifiable vertical slices | `planner` | Single slice (skip splitting) |
| 3. Execute by Playbook | Run one playbook per slice, changing one variable at a time | `executor` | Execute with one playbook and record evidence |
| 4. Verify Against Real Artifact | Prove behavior against the real artifact, data, or source | `executor` | Run the real-artifact verification check |
| 5. Single Review | One review pass for conformance, evidence, compatibility, rollback | `reviewer` | Concise single review pass |

## Core Working Rules

- **Selection over authority:** No rule, playbook, instruction, or skill in this repository is authoritative because of its origin. Every component survives only if recorded evaluation results in `evals/results/` support it.
- **Every variant is a hypothesis:** Playbook wording, instructions, checklists, and pulled skills are tested against local eval suites.
- **One stage, one router:** Only one router (agent or prompt) drives the active stage. Instruction files provide constraints only and never issue stage transitions.
- **Spec before execution:** Acceptance criteria must translate into a failing test, a measurable check, or an inspectable rubric before implementation or drafting begins.
- **Vertical slices:** Each ticket goes from one clear input or entry point to one verifiable output or effect. Never mix a performance optimization or refactor with a semantic or scope change.
- **One variable at a time:** Change one thing per iteration and capture before/after evidence.
- **Real-artifact verification:** Mocks, notebooks, summaries, or intuition prove local plausibility only. Stage 4 requires running or inspecting the real artifact (compiled binary, packaged job, real database via Testcontainers, live CLI command, primary source verification, or rendered deliverable).
- **Single review pass:** After Stage 4 passes, run one review checking spec conformance, evidence completeness, compatibility, and rollback or revision recovery. Findings return work to a named earlier stage. Never open a parallel second review.
- **Runtime vs. gardening separation:** During Stages 1 to 5, never pause mid-task to run evals or rewrite playbooks. If a rule or playbook underperforms, append a one-line observation to `evals/observations/` and continue shipping. Run the gardener loop (`Plant -> Measure -> Select -> Prune`) in a dedicated gardening session.
- **Ticket evidence vs. eval data:** Store per-ticket verification artifacts under `evidence/` so live work is never blocked by benchmark curation. Promote high-signal real cases into `evals/data/<suite>/` after Stage 5 during gardening.

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

## Facts vs. Recommended Practice

- **Fact:** A mechanism, API, default behavior, statistic, or quote verifiable in official documentation or a cited primary source.
- **Recommended Practice:** A workflow rule, threshold, template, or engineering convention introduced by this methodology.

All instruction files, specs, and review outputs must label statements clearly as `[Fact]` or `[Recommended Practice]`.

## Repository Map

- `.github/instructions/shared.instructions.md` (universal rules for all intelligent work)
- `.github/instructions/spark.instructions.md` (Apache Spark domain pack)
- `.github/instructions/spring.instructions.md` (Java Spring domain pack)
- `.github/prompts/work-*.prompt.md` (universal playbooks: create, diagnose, research, refine)
- `.github/prompts/spark-*.prompt.md` and `spring-*.prompt.md` (Spark and Spring playbooks)
- `.github/prompts/run-eval.prompt.md` (eval execution prompt; scoring is run via `scripts/score-eval.py`)
- `.github/agents/gardener-mode.agent.md` (universal default mode)
- `.github/agents/spark-spring-mode.agent.md` (Spark and Spring domain preset)
- `.github/agents/planner.agent.md`, `executor.agent.md`, `reviewer.agent.md` (standalone role agents)
- `evals/` (suites for `general`, `spark`, `spring`, human data, observations, and deterministic results)
- `scripts/score-eval.py` (deterministic eval scorer) and `scripts/verify-repo.py` (mechanical repo verifier)
- `SPEC.md`, `ADAPTATION.md`, `docs/methodology.md` (architecture specification and archival methodology)