---
description: Apache Spark performance diagnosis and optimization playbook (Stages 3 and 4)
---

# Playbook: Spark Performance Diagnosis

Execute Stages 3 and 4 for Apache Spark performance work. Change one variable at a time and save before/after evidence under `evidence/`.

## Steps

1. **Pin environment and reproduce:** Fix `spark-submit` configuration, dependency versions, and representative input data. Record baseline metrics.
2. **Inspect Spark UI stage telemetry:** Capture stage task duration distributions (median, p95, max), input/output rows and bytes, shuffle read/write, disk/memory spill, and executor utilization.
3. **Correlate with physical plans:** Compare the slow stage against `EXPLAIN FORMATTED` and SQL operator metrics in the Spark UI.
4. **Measure key frequency and partition skew:** Profile join keys, null keys, tenants, and dates (`df.groupBy(key).count().orderBy(desc("count"))`) alongside partition size distributions.
5. **Verify AQE behavior:** Check whether `spark.sql.adaptive.enabled=true` and `spark.sql.adaptive.skewJoin.enabled=true` are active and whether skewed shuffle partitions were actually split.
6. **Evaluate candidate fixes (one at a time, in priority order):**
   - Filter invalid rows and pre-aggregate before shuffle (Subtract Before You Add).
   - Fix accidental many-to-many joins (missing join keys or semi/anti join opportunities).
   - Broadcast small tables (`broadcast()` or `spark.sql.autoBroadcastJoinThreshold`).
   - Align partitioning (`repartition` / `coalesce`) with downstream contracts.
   - Isolate hot keys into a separate path and union results.
   - Salt skewed join keys and strip salt after aggregation or join.
   - Tune AQE thresholds only after verifying why defaults did not trigger.
7. **Verify one variable at a time (Stage 4):** Run the packaged job on the same representative dataset, compare outputs and invariants, and capture physical plan diffs plus before/after metrics across repeated runs.
8. **Package evidence:** Save `evidence/<id>-plan-diff.txt`, `evidence/<id>-metrics.json`, `evidence/<id>-dataset.md`, and `evidence/<id>-rollback.md`.

## Outputs

- Optimized Spark job code preserving all output invariants
- Before/after physical plan diff, metrics, and dataset profile under `evidence/`
- Deployment and rollback notes