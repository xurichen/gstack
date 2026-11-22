# Specification: Universal Evolutionary Engineering & Knowledge-Work Methodology (`spark-spring-skills`)

A Copilot-native methodology repository for **all kinds of intelligent work** (software engineering, data and ML, systems architecture, research and synthesis, technical or editorial writing, product and strategy, quantitative analysis, operations, and CLI tooling), with first-class domain packs for Apache Spark and Java Spring. Built on an evolutionary model: order emerges from local selection and contingency, not from authority.

Status: v1.0 (all previous OPEN review items resolved and enforced mechanically by `scripts/score-eval.py` and `scripts/verify-repo.py`).

## 1. Purpose

The repository turns a coding and knowledge-work assistant (GitHub Copilot in VS Code) into a disciplined agent using native configuration files: always-on instructions, scoped domain instructions, reusable playbooks, custom role agents, and a deterministic local evaluation harness. Its product is measurable behavior across any intellectual task, not a code library.

## 2. Design Principles

1. **Selection over authority.** No rule, playbook, instruction, or skill in this repository is authoritative because of its origin. Upstream skills (`skills/`) and ported playbooks are seed stock. A component survives only if recorded evidence in `evals/results/` supports it.
2. **Local contingency.** Fitness is local to one codebase or workspace, one task distribution, one set of stack versions, one LLM model version (`model_id`), and one date. Results recorded before a major stack or model version change are stale and must be re-run before citation. Results from another codebase are priors, not evidence.
3. **Gardening, not architecture.** Variants are planted, measured, selected, and pruned in a continuous loop. The human is the gardener.
4. **Evaluation is the selection pressure.** Every working rule is a testable hypothesis.
5. **No global comparisons or rankings.** No cross-project scores, no global variant rankings, and no preference votes. Every variant is measured against fixed local tasks and its local champion.
6. **Facts vs. recommended practice.** Documented mechanisms and primary-source facts (`[Fact]`) are never blended with methodology conventions (`[Recommended Practice]`).

## 3. Constitution vs. Evolvable Genome

To prevent tension between stage discipline and evolution, the repository explicitly separates:

- **Fixed apparatus (Constitution / Invariants):** The experimental harness that remains constant so eval records stay comparable across seasons (Section 7).
- **Evolvable genome:** Playbooks (`.github/prompts/`), scoped instructions (`.github/instructions/`), domain checklists, and upstream skills pulled from `skills/`. All are subject to selection pressure.

## 4. Repository Structure

- `skills/`: Upstream Matt Pocock skill pack, kept byte-identical to upstream (seed stock).
- `.github/copilot-instructions.md`: Always-on rules, pipeline, constitution vs. genome, and canonical selection rules.
- `.github/instructions/`:
  - `shared.instructions.md` (`applyTo: "**"`): Universal Red-Green-Refine loop, five grounding principles, universal spec checklist, evidence naming, and observation logging.
  - `spark.instructions.md` and `spring.instructions.md`: Domain packs for Apache Spark and Java Spring (extensible by adding `<domain>.instructions.md`).
- `.github/prompts/`:
  - Universal playbooks: `work-create.prompt.md`, `work-diagnose.prompt.md`, `work-research.prompt.md`, `work-refine.prompt.md`.
  - Domain playbooks: `spark-performance.prompt.md`, `spark-correctness.prompt.md`, `spring-feature.prompt.md`, `spring-diagnose.prompt.md`.
  - Eval generation prompt: `run-eval.prompt.md` (generation only; scoring is external).
- `.github/agents/`:
  - `gardener-mode.agent.md`: Default universal entry point for all intelligent work.
  - `spark-spring-mode.agent.md`: Pre-configured Spark and Spring domain preset.
  - `planner.agent.md` (read-only), `executor.agent.md`, `reviewer.agent.md` (read-only).
- `evals/`: Suites (`general/`, `spark/`, `spring/`), human-input data (`data/`), runtime friction inbox (`observations/`), and immutable deterministic results (`results/`).
- `scripts/score-eval.py`: Deterministic lexicographic scorer (Python stdlib).
- `scripts/verify-repo.py`: Mechanical acceptance verifier (Python stdlib).

## 5. Inner Loop (Full-Track & Fast-Track) and Gardener Outer Loop

- **Full-Track (5 stages):** Clarify & Specify (`planner`) -> Slice into Tickets (`planner`) -> Execute by Playbook (`executor`) -> Verify Against Real Artifact (`executor`) -> Single Review (`reviewer`).
- **Fast-Track (3 compressed steps):** Single-turn Brief -> Execute + Real-Artifact Verify -> Concise Single Review. Prevents ceremony from starving real-world usage and mutation signals.
- **Runtime vs. Gardening separation:** During live tasks, agents never pause to run evals; they log playbook friction to `evals/observations/` and continue shipping. Gardening (`Plant -> Measure -> Select -> Prune`) runs in dedicated offline sessions.

## 6. Evaluation System (Resolved Design)

1. **Three starter suites (6 tasks each):** `evals/general/tasks.md` (universal intelligent work), `evals/spark/tasks.md` (local-scale reproducible Spark fixtures), and `evals/spring/tasks.md` (JUnit + Testcontainers). Each task defines all five fields (`Input`, `Operation`, `Scoring`, `Baseline`, `Human-Input Data`) plus `Tier` (`human` or `synthetic`).
2. **No blended total score:** Replaced by a **lexicographic 3-part gate** enforced by `scripts/score-eval.py`:
   - Tier 1 (`human`) binary checks: 100% pass, zero regressions required for promotion.
   - Tier 2 (`synthetic`) binary checks: zero regressions (usable alone for fast early pruning, never for promotion).
   - Tier 1 primary metric deltas above the 5% timing noise floor + cost guardrail (median token cost at most 2.0x champion unless correctness improved).
3. **Suite-size-aware selection:**
   - Starter suites (fewer than 20 tasks): paired champion-vs-challenger runs on identical fixtures; prune on any binary regression or failure to improve the target task across 3 paired trials.
   - Mature suites (20 or more tasks): two consecutive full-suite losses to champion -> prune or rewrite.
4. **Decoupled human-input data:** Ticket verification artifacts stay in `evidence/`; reusable real cases are promoted to `evals/data/<suite>/` with four required English header keys (`source`, `date`, `task_id`, `expected_output_note`). Missing or template files deterministically produce `verdict: "data_incomplete"`.
5. **Deterministic external scoring:** Agents run generation in a clean worktree via `.github/prompts/run-eval.prompt.md`; `python3 scripts/score-eval.py` computes verdicts, stamps `date`, `git_sha`, `model_id`, `stack_versions`, and `prompt_hash`, and writes immutable JSON to `evals/results/`.

## 7. Invariants (Constitution)

1. `skills/` remains byte-identical to upstream.
2. One stage has exactly one router.
3. Stage 4 verification gates accept only real-artifact evidence.
4. Exactly one review pass closes a task.
5. Every verdict in `evals/results/` is produced deterministically by `scripts/score-eval.py` and includes `date`, `git_sha`, `model_id`, `stack_versions`, `variant_id`, `prompt_hash`, and per-task results.
6. No keep, promote, prune, or rewrite verdict is issued when required human-input data is incomplete.
7. Repository prose and metadata keys in added layers are in English.

## 8. Mechanical Acceptance Verification

Run `python3 scripts/verify-repo.py && python3 scripts/score-eval.py --self-test && node scripts/check-frontmatter.mjs` to mechanically verify every invariant and acceptance check.
