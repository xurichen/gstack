---
description: Universal playbook for evidence-grounded research, option comparison, synthesis, and decision analysis
---

# Playbook: Research and Decision Analysis (Universal)

Execute Stages 3 and 4 for research reports, architecture evaluations, vendor or tool comparisons, market or policy analyses, and strategic recommendations.

## Steps

1. **Lock decision criteria and scope:** Confirm the exact decision question, evaluation dimensions, hard constraints, and disqualifying criteria from the Stage 1 spec.
2. **Collect primary evidence:** Retrieve authoritative primary sources (official docs, filings, benchmarks, real datasets, direct measurements) for every option symmetrically. Label every claim `[Fact]` (with source) or `[Recommended Practice]` / inference.
3. **Eliminate gaps and verify conflicts:** Where sources conflict or omit key numbers, inspect the primary source directly. Never extrapolate missing numbers or fabricate citations; mark genuinely unavailable data as unverified.
4. **Compute explicit comparisons:** Build a symmetric comparison matrix across shared dimensions, showing concrete trade-offs, quantitative drivers (Explain the Number), and sensitivity to key assumptions.
5. **Stress-test the recommendation:** Actively look for the strongest counterargument, failure mode, and condition under which the runner-up option wins.
6. **Verify against primary sources (Stage 4):** Audit every figure, date, quote, and link in the final artifact against the retrieved primary source record. Confirm zero broken or mismatched citations.
7. **Package evidence:** Save the source verification log (`evidence/<id>-sources.md`), calculation sheets or scripts, and final deliverable.

## Outputs

- Grounded research synthesis or decision memo with inline primary-source citations
- Symmetric comparison table and explicit assumptions
- Source verification log under `evidence/`
