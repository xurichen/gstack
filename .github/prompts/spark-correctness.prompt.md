---
description: Apache Spark correctness bug diagnosis and fix playbook (Stages 3 and 4)
---

# Playbook: Spark Correctness Bug Fix

Execute Stages 3 and 4 for Apache Spark correctness bugs. Change one variable at a time and save before/after evidence under `evidence/`.

## Steps

1. **Reproduce with a minimal fixture:** Build the smallest DataFrame fixture that reproduces the defect using an explicit `StructType` schema (never rely on schema inference). Record input fixture and expected output.
2. **Assert explicit invariants:** Assert exact schema, column values, row counts, deduplication rules, null handling, decimal precision, and boundary timestamps.
3. **Locate the root cause:** Inspect transformation logic, join types, implicit type casts, null semantics, window frame boundaries, or watermark and late-data handling.
4. **Apply the minimal fix:** Change one variable and confirm the minimal fixture passes.
5. **Add regression coverage:** Add tests for empty inputs, single rows, all-null keys, malformed records, duplicate primary keys, timezone boundaries, and late-arriving events.
6. **Verify at the integration layer:** Test with the real storage format (Parquet, ORC, Delta, Iceberg, Avro, JSON), real connectors, and real write modes (`overwrite`, `append`, `merge`).
7. **Run packaged job on representative data (Stage 4):** Build the fat JAR or production package, run it against representative data (including bad records and skew), and compare outputs, plans, and metrics.
8. **Package evidence:** Save `evidence/<id>-fixture.json`, `evidence/<id>-expected.json`, `evidence/<id>-plan-diff.txt`, `evidence/<id>-metrics.json`, and `evidence/<id>-rollback.md`.

## Outputs

- Fixed Spark job code and regression tests
- Fixtures, expected outputs, plan diff, and representative-run evidence under `evidence/`
- Deployment and rollback notes