---
description: Universal playbook for creating or building any new intelligent-work artifact (code, document, spec, model, plan, design, or CLI tool)
---

# Playbook: Create or Build (Universal)

Execute Stages 3 and 4 for creating a new artifact in any domain. Change one variable at a time and preserve before/after evidence under `evidence/`.

## Steps

1. **Define the narrowest failing check first (Red):** Turn the Stage 1 acceptance criteria into an executable test, invariant script, schema validator, or explicit pass/fail rubric before drafting or coding.
2. **Build the minimal working slice (Green):** Produce the smallest complete vertical slice that passes the initial check. Keep scope strictly within the ticket.
3. **Cover boundaries and failure modes:** Add edge cases, invalid inputs, error handling, counterexamples, permissions, or audience constraints required by the spec.
4. **Refine while holding invariants constant:** Remove redundant logic, filler text, unused fields, or unnecessary abstractions (Subtract Before You Add) while re-running the checks after each change.
5. **Verify against the real artifact (Stage 4):**
   - Code or CLI: build the real artifact and run it with real inputs, real configs, and real exit-code/stdout checks.
   - Data or quantitative model: run calculations on the real dataset and verify totals, bounds, and reconciliation checks.
   - Document, plan, or design: inspect the final rendered artifact against every spec criterion and verify every cited fact against its primary source.
6. **Package evidence:** Save test results, verification logs, primary-source checks, and rollback or revision recovery notes under `evidence/<id>-*`.

## Outputs

- Final created artifact (code, document, model, script, or deliverable)
- Verification evidence files under `evidence/`
- Rollback or recovery notes
