---
description: Generate candidate outputs for an eval suite in a clean worktree; deterministic scoring is performed externally by scripts/score-eval.py
---

# Playbook: Run Eval Generation (Scoring Is External)

Run candidate task execution for one named variant in a clean git worktree. This prompt performs **generation and artifact capture only**. Never self-grade `binary_pass`, never read champion scores to tune answers, and never write directly to `evals/results/`.

## Inputs

- `suite`: `general`, `spark`, or `spring` (or a custom suite name under `evals/`)
- `variant_id`: unique variant identifier (for example `work-diagnose-v2-hypothesis-first`)
- `variant_file`: path to the prompt, instruction, or skill file under test
- `run_dir`: output directory for raw task outputs and machine-readable logs (for example `evals/runs/<suite>-<variant_id>-<timestamp>/`)

## Steps

1. **Verify clean isolation:** Confirm you are running in a clean git worktree with only the single `variant_id` change active. Do not inspect `evals/results/` for champion scores.
2. **Read suite tasks:** Open `evals/<suite>/tasks.md` and read all tasks (all 5 fields: `Input`, `Operation`, `Scoring`, `Baseline`, `Human-Input Data`).
3. **Check human-input data presence:** Inspect `evals/data/<suite>/` for the files referenced by each task. Do not fabricate missing data; if any required human-input file is missing or still marked `TEMPLATE_NOT_REAL_DATA`, continue capturing raw outputs if requested and let `scripts/score-eval.py` emit `verdict: "data_incomplete"`.
4. **Execute tasks one by one:** For each task:
   - Run the referenced playbook against the task's `Input` fixture.
   - Save raw artifacts, test outputs (JUnit XML, JSON metrics, stdout/stderr logs), and wall-clock/token telemetry to `<run_dir>/<task_id>.json`.
   - Record raw measured values only; set unmeasured fields to `null`. Never estimate metrics.
5. **Hand off to the deterministic scorer:** Print the exact terminal command for the human gardener to run:

```bash
python3 scripts/score-eval.py \
  --suite <suite> \
  --variant-id <variant_id> \
  --variant-file <variant_file> \
  --model-id <copilot-model-id> \
  --run-dir <run_dir> \
  [--champion-file evals/results/<champion-record>.json]
```

## Constraints

- Test exactly one `variant_id` per run.
- Do not modify `skills/`, `evals/results/`, or unrelated playbooks during the run.
- Never self-grade pass/fail or emit a keep/promote/prune/rewrite verdict in chat.
