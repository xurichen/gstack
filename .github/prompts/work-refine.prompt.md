---
description: Universal playbook for refactoring, editing, compressing, or optimizing an existing artifact while preserving invariants
---

# Playbook: Refine and Optimize (Universal)

Execute Stages 3 and 4 for improving an existing artifact (refactoring code, optimizing performance or cost, editing or tightening prose, simplifying an architecture or workflow) without breaking its external contract.

## Steps

1. **Freeze baseline invariants:** Capture current outputs, contracts, schemas, test results, factual claims, and baseline performance or size metrics before making any change.
2. **Identify the bottleneck or waste:** Measure where latency, cost, complexity, or reader confusion actually comes from (Explain the Number).
3. **Subtract before you add:** Remove dead code, unused columns, redundant queries, filler prose, or unnecessary indirection first.
4. **Apply one change at a time:** Make a single structural or optimization change per iteration, keeping behavior and invariants locked.
5. **Re-verify invariants and compare before/after:** Confirm zero semantic or factual regressions and record concrete before/after deltas on the target metric.
6. **Verify against the real artifact (Stage 4):** Run the packaged artifact, full test suite, or complete document audit against representative inputs. Confirm no downstream consumer or contract is broken.
7. **Package evidence:** Save before/after diffs (`evidence/<id>-diff.txt`), metrics comparison (`evidence/<id>-metrics.json`), invariant verification logs, and rollback steps.

## Outputs

- Refined or optimized artifact with zero invariant regressions
- Before/after metric and invariant comparison under `evidence/`
- Rollback notes
