# Adaptation Guide: Universal Gardener Methodology + Domain Packs

## Provenance

- **Upstream seed stock:** `skills/` is retained byte-identical from [mattpocock/skills](https://github.com/mattpocock/skills) (MIT License). It acts as seed stock; individual skills may be adapted into `.github/` variants and evaluated locally without modifying `skills/` in place.
- **Playbooks and principles:** The Spark and Spring playbooks and five grounding principles were adapted from pstack concepts into VS Code Copilot native files under `.github/`, then generalized to support all kinds of intelligent work.

## What Was Added

All additions live outside `skills/`:

- `.github/copilot-instructions.md`: Always-on rules, constitution vs. genome boundary, Full-Track/Fast-Track pipeline, and canonical selection rules.
- `.github/instructions/shared.instructions.md`: Universal Red-Green-Refine loop, five grounding principles, spec checklist, evidence naming, and observation logging (`applyTo: "**"`).
- `.github/instructions/spark.instructions.md` and `spring.instructions.md`: Scoped domain packs for Apache Spark and Java Spring.
- `.github/prompts/`:
  - Universal playbooks: `work-create.prompt.md`, `work-diagnose.prompt.md`, `work-research.prompt.md`, `work-refine.prompt.md`.
  - Domain playbooks: `spark-performance.prompt.md`, `spark-correctness.prompt.md`, `spring-feature.prompt.md`, `spring-diagnose.prompt.md`.
  - Eval generation prompt: `run-eval.prompt.md`.
- `.github/agents/`:
  - `gardener-mode.agent.md` (universal default entry point for any intelligent work).
  - `spark-spring-mode.agent.md` (Spark and Spring domain preset).
  - `planner.agent.md` (read-only), `executor.agent.md`, `reviewer.agent.md` (read-only).
- `evals/`: Three 6-task starter suites (`general/`, `spark/`, `spring/`), human-input data templates (`data/`), runtime friction inbox (`observations/`), and deterministic result schema (`results/`).
- `scripts/score-eval.py`: Deterministic lexicographic eval scorer with built-in `--self-test`.
- `scripts/verify-repo.py`: Mechanical verifier for all repository invariants and acceptance checks.
- `SPEC.md` and `docs/methodology.md`: Finalized specification and archival methodology reference.

## Using This Repository in VS Code Copilot

No plugin installation is required. Open the repository in VS Code and Copilot automatically loads `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, `.github/prompts/*.prompt.md`, and `.github/agents/*.agent.md`.

1. Pick `@gardener-mode` for any general intelligent work (software, data, research, writing, analysis, strategy, CLI) or `@spark-spring-mode` for Spark and Spring tasks.
2. Invoke playbooks directly with `/work-create`, `/work-diagnose`, `/work-research`, `/work-refine`, `/spark-performance`, `/spark-correctness`, `/spring-feature`, `/spring-diagnose`, or `/run-eval`.
3. Note on agent tool names: `.github/agents/*.agent.md` uses standard read/search/edit/runCommands tool identifiers. Adjust the `tools:` frontmatter list if your local VS Code Copilot version uses custom MCP or workspace tool IDs.

## Adding a New Domain Pack

To extend this repository for another domain (for example Python ML, Kubernetes Ops, Legal/Policy Review, Financial Modeling, or Technical Writing):

1. Add `.github/instructions/<domain>.instructions.md` with an appropriate `applyTo` glob, domain spec checklist, guardrails, and Stage 4 verification gate.
2. Add optional domain playbooks under `.github/prompts/<domain>-*.prompt.md`.
3. Add a 6-task starter suite under `evals/<domain>/tasks.md` and templates under `evals/data/<domain>/`.
4. Score variants with `python3 scripts/score-eval.py --suite <domain> ...`.

## Verification Commands

```bash
python3 scripts/verify-repo.py
python3 scripts/score-eval.py --self-test
node scripts/check-frontmatter.mjs
```