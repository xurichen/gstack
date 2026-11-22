---
applyTo: "**/*spark*/**,**/spark*/**,**/etl/**,**/pipelines/**,**/*.scala"
---

# Apache Spark Domain Pack Instructions

This file extends `shared.instructions.md` for Apache Spark jobs and data pipelines. Customize `applyTo` above if your Spark modules live under different paths. Statements are labeled `[Fact]` or `[Recommended Practice]`.

## Spark Specification Checklist (Stage 1)

`[Recommended Practice]` Before editing a Spark job, specify:

- [ ] Input and output schemas (explicit `StructType`, nullability, precision).
- [ ] Invariants: row count expectations, uniqueness keys, null rules, deduplication rules, boundary timestamps, decimal precision.
- [ ] Join semantics and many-to-many explosion risks.
- [ ] Skew-key candidates: null keys, sentinel values, single hot join key, top tenants, hot dates.
- [ ] Late-data and watermarking behavior (for streaming or event-time pipelines).
- [ ] Partitioning and output file contracts (file count range, target file size, partition columns, format).
- [ ] Performance budget: runtime, task duration distribution, shuffle read/write, disk spill, output file count.
- [ ] Representative dataset profile and malformed-data test cases.

## Spark Guardrails (Stage 3)

### Skew and Shuffle Guardrails

- `[Fact]` Adaptive Query Execution (`spark.sql.adaptive.enabled=true`) is enabled by default in Spark 3.2+ and can split skewed shuffle partitions when `spark.sql.adaptive.skewJoin.enabled=true`.
- `[Recommended Practice]` Measure key frequency distributions before choosing a fix. Test candidate fixes one variable at a time: filter invalid/null keys early, pre-aggregate before join, fix many-to-many join keys, broadcast small tables, repartition on business keys, isolate hot keys, salt skewed keys, or rely on AQE.
- `[Recommended Practice]` Save physical plan diffs and before/after metrics on the same representative dataset for every candidate change.

### Plan and Partition Guardrails

- `[Fact]` Physical plans are inspected via `EXPLAIN` (`df.explain("formatted")` / `"extended"`) or the Spark UI SQL tab; `spark.sql.adaptive.coalescePartitions.enabled` controls adaptive post-shuffle partition coalescing.
- `[Recommended Practice]` Capture before/after physical plan diffs for every non-trivial query or join change.
- `[Recommended Practice]` Align output partitioning and file counts with downstream consumers (Athena, Trino, Iceberg, Delta, Parquet readers) as part of the spec contract.

### Caching and UDF Guardrails

- `[Fact]` `persist()` and `cache()` hold executor memory or disk until `unpersist()` is called or the application ends; black-box UDFs prevent Catalyst expression pushdown and whole-stage codegen optimizations.
- `[Recommended Practice]` Apply "subtract before you add": prune unused columns, push filters down, and pre-aggregate before considering caching. Use UDFs only when built-in SQL expressions cannot express the logic, and attach before/after CPU and duration evidence.

## Spark Verification Gate (Stage 4)

`[Recommended Practice]` A Spark change passes Stage 4 only when all items are verified:

- [ ] Packaged job (fat JAR or production wheel/script) executed in the target runtime, not approximated in a notebook.
- [ ] Representative data volume, key distribution, file layout, schema, and malformed records covered.
- [ ] Business outputs and invariants (schema, values, row counts, duplicates, nulls, boundaries) compared row-for-row or by deterministic checksum.
- [ ] Optimized and physical plan diff saved and inspected.
- [ ] Duration, task distribution (median vs. p99/max), shuffle read/write, spill, input/output partitions, executor GC, and task retries compared before and after.
- [ ] Repeated enough times to rule out single-run cluster noise.
- [ ] Confirmed that speedups preserved semantics, file usability, and downstream contracts.

## Spark PR Evidence Checklist

`[Recommended Practice]` Every Spark PR includes under `evidence/`:

1. Spec and data contract changes (`evidence/<id>-spec.md`).
2. Minimal test fixture and expected output/schema (`evidence/<id>-fixture.json`, `evidence/<id>-expected.json`).
3. Physical plan diff (`evidence/<id>-plan-diff.txt`).
4. Representative dataset description: rows, partitions, key skew, bad-record ratio (`evidence/<id>-dataset.md`).
5. Before/after metrics: duration, shuffle, spill, skew, partitions, output files (`evidence/<id>-metrics.json`).
6. Deployment and rollback plan (`evidence/<id>-rollback.md`).