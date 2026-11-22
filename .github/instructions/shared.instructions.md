---
applyTo: "**"
---

# Shared Instructions for All Intelligent Work

This file applies across the entire repository for every kind of intelligent work: software engineering, data and analytics, research and synthesis, technical or editorial writing, product design, strategy, operations, and CLI tooling. Statements are labeled `[Fact]` or `[Recommended Practice]`.

## Universal Execution Loop (Stage 3 Core)

`[Recommended Practice]` Follow the Red-Green-Refine loop adapted to the domain of the task:

1. **Red (failing check first):** Write or define the narrowest failing verification check before editing or drafting.
   - Code or CLI: failing unit test, schema check, or command assertion.
   - Data or quantitative analysis: invariant check (row counts, totals, reconciliation constraints, bounds).
   - Research, writing, or strategy: explicit rubric (questions to answer, required primary sources, audience constraints, falsifiable claims).
2. **Green (minimal change):** Make the smallest change or draft that satisfies the check, changing one variable at a time.
3. **Refine (preserve invariants):** Improve clarity, structure, or efficiency while keeping every acceptance check green.
4. **Edge and adversarial coverage:** Add boundary cases, malformed inputs, counterarguments, failure modes, and security or compatibility checks.
5. **Real-artifact verification (Stage 4):** Validate the actual output artifact against real inputs, real environments, or primary sources.

## Five Grounding Principles (Universal)

`[Recommended Practice]` Every piece of work must satisfy five operational principles:

| Principle | Universal Rule | Non-Code Example (Research / Writing / Analysis) | Code / Systems Example |
|---|---|---|---|
| **Prove it works** | Verify the real output artifact against real inputs or sources | Verify every cited figure against the primary source; execute calculations on the real dataset | Build the real artifact and run it against representative data or a real database |
| **Explain the number** | Every quantitative claim must trace to its mechanism or formula | Break down a cost or forecast into explicit drivers and assumptions | Attribute latency or runtime deltas to query count, shuffle, spill, lock contention, or pool saturation |
| **Test behavior, not implementation** | Assert observable contracts and outcomes, not internal steps | Verify the document answers every decision question accurately without contradicting constraints | Assert HTTP status, DB state, output schema, or CLI exit code instead of internal mock calls |
| **Subtract before you add** | Remove waste, noise, unused fields, or redundant layers first | Cut filler sections, redundant claims, and ungrounded scope before adding new analysis | Prune unused columns, redundant queries, or unnecessary abstractions before adding caches or hardware |
| **Fix root causes** | Address the underlying mechanism rather than masking symptoms | Resolve an inconsistent assumption or missing definition rather than hedging prose | Fix skew keys, missing indexes, or transaction boundaries rather than raising timeouts or memory |

## Fact vs. Recommended Practice Labeling

`[Recommended Practice]` Explicitly distinguish:

- **`[Fact]`**: Verifiable in official platform documentation, measured tool output, or a cited primary source.
- **`[Recommended Practice]`**: A workflow convention, heuristic, threshold, or template introduced by this methodology.

Never present a recommended practice as a platform requirement, and never present an unverified claim as a fact.

## Universal Specification Checklist (Stage 1)

`[Recommended Practice]` Before starting execution on any non-trivial task, confirm:

- [ ] **Deliverable contract:** Exact output artifact, format, audience, and boundaries of what is in or out of scope.
- [ ] **Observable acceptance criteria:** Concrete checks that distinguish pass from fail.
- [ ] **Invariants:** Constraints that must not break (schemas, totals, factual accuracy, backward compatibility, tone, or policy constraints).
- [ ] **Sources and ground truth:** Authoritative data, files, APIs, or primary references to use.
- [ ] **Failure modes and edge cases:** Known pitfalls, bad inputs, counterexamples, or adversarial cases.
- [ ] **Budget and constraints:** Time, cost, latency, length, or resource ceilings.
- [ ] **Verification method:** How the real artifact will be tested in Stage 4.
- [ ] **Rollback or recovery plan:** How to revert or recover if the change causes harm after release or publication.

## Evidence Naming Convention

`[Recommended Practice]` Store per-ticket verification evidence under `evidence/` using:

`evidence/<ticket-id>-<stage>-<metric>.<ext>`

Examples:

- `evidence/TASK-101-spec.md` (Stage 1 specification)
- `evidence/TASK-101-plan-diff.txt` (Stage 4 execution or query plan diff)
- `evidence/TASK-101-metrics.json` (Stage 4 before/after metrics)
- `evidence/TASK-101-sources.md` (Stage 4 primary-source verification log)
- `evidence/TASK-101-test-results.xml` (Stage 4 automated test results)
- `evidence/TASK-101-rollback.md` (Stage 5 rollback or recovery notes)

## Runtime Observation Logging

`[Recommended Practice]` If a playbook, instruction, or pulled skill causes friction or misses a failure mode during live work, do not stop to run evals mid-task. Append a brief entry to `evals/observations/` noting the file, symptom, and task context so the gardener loop can plant and evaluate a challenger in a dedicated session.