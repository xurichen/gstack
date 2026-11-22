---
description: Universal playbook for diagnosing and fixing bugs, logic errors, data anomalies, process failures, or broken systems
---

# Playbook: Diagnose and Fix (Universal)

Execute Stages 3 and 4 for investigating and resolving any defect, anomaly, or failure. Change one variable at a time and preserve before/after evidence under `evidence/`.

## Steps

1. **Reproduce deterministically:** Pin inputs, versions, environment, and configuration to create the smallest reliable reproduction of the failure. Record the exact baseline symptom and metrics.
2. **Isolate the mechanism:** Gather direct observational evidence (logs, stack traces, execution plans, query counts, row diffs, timeline events, or logical premises) rather than guessing.
3. **Form a falsifiable root-cause hypothesis:** State what causes the failure and what observable signal would disprove your hypothesis. Rule out surface symptoms (Fix Root Causes).
4. **Write a failing regression check:** Encode the exact reproduction into an automated test, data invariant check, or verifiable audit check that fails before the fix.
5. **Apply one minimal fix:** Change one variable at a time and verify the regression check passes without breaking unrelated invariants.
6. **Add adjacent boundary coverage:** Test neighboring edge cases (nulls, empty inputs, concurrency, timezone/rounding edges, malformed records, or conflicting constraints).
7. **Verify against the real artifact (Stage 4):** Re-run the full real artifact on representative data or real inputs and compare before/after behavior and metrics.
8. **Package evidence:** Save `evidence/<id>-repro.md`, before/after metrics or diffs, regression check results, and rollback notes.

## Outputs

- Minimal root-cause fix and regression check
- Before/after diagnostic and verification evidence under `evidence/`
- Rollback plan
