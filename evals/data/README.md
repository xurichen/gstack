# Human-Input Eval Data Directory

Human-supplied evaluation data lives here, organized by suite:

```text
evals/data/
  README.md
  general/
    _template.json
    _template.md
    <task-id>-<slug>.json|.md
  spark/
    _template.json
    _template.md
    <task-id>-<slug>.json|.md
  spring/
    _template.json
    _template.md
    <task-id>-<slug>.json|.md
```

## File Naming

`<task-id>-<slug>.<ext>`

- `task-id`: Matches the task ID in `evals/<suite>/tasks.md` (for example `general-spec-01`, `spark-skew-01`, `spring-nplus1-01`).
- `slug`: Short kebab-case descriptor (for example `real-incident-log`, `skew-sample`, `order-query-log`).
- `ext`: `json` or `md`.

## Required Header Block (English Keys)

Every human-input data file must open with four required metadata fields so `scripts/score-eval.py` can validate completeness mechanically:

| Key | Description | Example |
|---|---|---|
| `source` | Person or team who supplied and verified the case | `Platform Engineering @alex` |
| `date` | ISO date when supplied or verified (`YYYY-MM-DD`) | `2026-11-22` |
| `task_id` | Matching eval task ID | `general-diagnose-02` |
| `expected_output_note` | Human-verified expected outcome or acceptance criteria | `Identifies stale cache key + missing retry jitter; zero fabricated log lines` |

### JSON Format

```json
{
  "_header": {
    "source": "Platform Engineering @alex",
    "date": "2026-11-22",
    "task_id": "general-diagnose-02",
    "expected_output_note": "Identifies stale cache key and missing retry jitter"
  },
  "data": {}
}
```

### Markdown Format (YAML Frontmatter)

```markdown
---
source: "Platform Engineering @alex"
date: "2026-11-22"
task_id: "general-diagnose-02"
expected_output_note: "Identifies stale cache key and missing retry jitter"
---

Real case details here.
```

## Template Rule

Every suite folder contains `_template.json` and `_template.md` marked with `"source": "TEMPLATE_NOT_REAL_DATA"`. `scripts/score-eval.py` automatically rejects any file containing `TEMPLATE_NOT_REAL_DATA` and records the run as `verdict: "data_incomplete"`.

## Usage Rules

1. **Never fabricate real data:** Templates and synthetic examples must never masquerade as human-input data.
2. **Multiple files per task allowed:** Differentiate by `slug` when a task needs both an input sample and an expected output record.
3. **CLI parity:** For CLI tasks, store real command invocations and real captured terminal stdout/stderr/exit codes in this same structure.
4. **Decoupled from live tickets:** During live work, keep ticket-specific samples in `evidence/`; promote reusable cases into `evals/data/<suite>/` during gardening sessions.