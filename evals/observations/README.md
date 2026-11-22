# Runtime Observations Inbox

Use this directory to log playbook, instruction, or skill friction encountered during live work (Stages 1 to 5) without pausing the active ticket to run evals.

## How to Log an Observation

Append one concise entry to `evals/observations/log.md` (created on first entry):

```markdown
- **YYYY-MM-DD** | `<playbook-or-instruction-file>` | `<domain/task-type>` | Symptom: <what went wrong or caused wasted turns> | Candidate hypothesis: <what challenger change to test in the next gardening session>
```

During offline gardening sessions, review `log.md`, turn recurring symptoms into challenger hypotheses, evaluate them via `scripts/score-eval.py`, and archive resolved notes.
