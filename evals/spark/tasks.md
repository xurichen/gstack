# Apache Spark Evaluation Suite (Starter Suite)

This starter suite covers core Apache Spark engineering tasks using reproducible local-scale fixtures (`local[*]` or small dev cluster, 2 to 10 million rows) so challengers can be evaluated repeatedly without multi-hour production cluster queues. Production-scale ratios are preserved in the fixture distributions and optional production-scale notes.

## Task 1: Data Skew Fix

- **Task ID:** `spark-skew-01`
- **Tier:** `human`

**Input**
- Local-scale representative dataset: 5M-row events table where top 3 `tenant_id` values hold 78% of rows, joined on `tenant_id` + `event_date` (mirrors production skew profile).
- Malformed data: null `tenant_id` (0.3%), single hot `event_date` (12%).

**Operation**
- Use `.github/prompts/spark-performance.prompt.md`.
- Profile skew keys, test candidate fixes one variable at a time (null filtering, pre-aggregation, hot-key isolation, salting, broadcast, AQE), and save physical plan diff and before/after metrics.

**Scoring**
- Binary: Output row count, schema, and invariants (uniqueness, nulls, boundaries) match reference output exactly -> `true`, else `false`.
- Primary metric: `duration_delta_pct` (float, lower is better). Secondary metrics: `shuffle_bytes_delta_pct`, `spill_bytes_delta_pct`, `plan_diff_lines`.
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Anonymized production `tenant_id` frequency distribution and human-verified expected post-join row and distinct counts at `evals/data/spark/spark-skew-01-skew-distribution.json`.

## Task 2: Shuffle Spill Reduction

- **Task ID:** `spark-shuffle-02`
- **Tier:** `human`

**Input**
- Local-scale representative dataset: 3M-row orders table joined with 1M-row customers table under constrained local executor memory (`2g`) and default `spark.sql.shuffle.partitions=200`.
- Budget: disk spill below 50MB on local-scale fixture (scaled equivalent of production budget).

**Operation**
- Use `.github/prompts/spark-performance.prompt.md`.
- Tune partitioning, AQE coalescing, and join strategy one variable at a time; capture physical plan diff and spill metrics.

**Scoring**
- Binary: Disk spill below 50MB, output invariants identical to reference -> `true`, else `false`.
- Primary metric: `spill_bytes_delta_pct` (float, lower is better). Secondary metrics: `shuffle_bytes_delta_pct`, `duration_delta_pct`, `plan_diff_lines`.
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Real job partition-size distribution and human-confirmed spill/duration thresholds at `evals/data/spark/spark-shuffle-02-partition-stats.json`.

## Task 3: Small Files and Partition Sizing

- **Task ID:** `spark-partition-03`
- **Tier:** `synthetic`

**Input**
- Parquet writer producing 1,200 tiny files (average 400KB) due to over-partitioned shuffle output.
- Downstream contract: 16 to 32 output files, target file size 16MB to 32MB on local-scale fixture (mirrors production 128MB to 256MB contract).

**Operation**
- Use `.github/prompts/spark-performance.prompt.md`.
- Configure adaptive coalescing, target partition sizing, or explicit repartitioning to satisfy the output file contract without introducing skew.

**Scoring**
- Binary: Output file count within `[16, 32]`, max file size within contract, data checksum identical -> `true`, else `false`.
- Primary metric: `output_file_count` (integer, target inside contract range). Secondary metrics: `avg_file_size_mb`, `max_file_size_mb`, `plan_diff_lines`.
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Real storage file-size listing and human-confirmed downstream consumer contract at `evals/data/spark/spark-partition-03-file-contract.json`.

## Task 4: Correctness Bug with Watermark and Late Data

- **Task ID:** `spark-correctness-04`
- **Tier:** `human`

**Input**
- Deterministic local Parquet or JSON fixture generated from `evals/data/spark/spark-correctness-04-edge-cases.json` containing nulls, duplicate keys, timezone boundary timestamps, and late-arriving records.
- Defect: current job drops valid late-arriving records at watermark boundaries.

**Operation**
- Use `.github/prompts/spark-correctness.prompt.md`.
- Build an explicit `StructType` fixture test, fix watermark and late-data semantics, add boundary regressions, and verify packaged execution.

**Scoring**
- Binary: Output matches expected dataset row-for-row on schema, values, counts, duplicates, nulls, and boundaries -> `true`, else `false`.
- Primary metric: `regression_cases_passed` (integer, higher is better). Secondary metrics: `plan_diff_lines`, `duration_delta_pct`.
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Human-annotated edge cases (late events, nulls, duplicates, timezone edges) and row-verified expected output at `evals/data/spark/spark-correctness-04-edge-cases.json`.

## Task 5: Caching Decision

- **Task ID:** `spark-cache-05`
- **Tier:** `synthetic`

**Input**
- Three-stage DAG where intermediate `stage2` (unused wide columns still attached) is reused by `stage3` and `stage4`, currently calling `persist(StorageLevel.MEMORY_AND_DISK)` with no `unpersist()`.

**Operation**
- Use `.github/prompts/spark-performance.prompt.md`.
- Apply Subtract Before You Add (prune unused columns, push filters down, pre-aggregate) before evaluating no-cache vs. memory vs. serialized cache and explicit `unpersist()`.

**Scoring**
- Binary: Total shuffle read/write does not increase, GC time does not increase, explicit `unpersist()` added if cached, output identical -> `true`, else `false`.
- Primary metric: `gc_time_delta_pct` (float, lower is better). Secondary metrics: `shuffle_read_delta_pct`, `shuffle_write_delta_pct`, `duration_delta_pct`.
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Optional real DAG stage size and GC telemetry at `evals/data/spark/spark-cache-05-dag-metrics.json`.

## Task 6: UDF Replacement

- **Task ID:** `spark-udf-06`
- **Tier:** `synthetic`

**Input**
- Job containing 3 UDFs (string normalization, timestamp parsing, JSON field extraction) blocking Catalyst optimization (`BatchEvalPython` or black-box Scala UDF) on a 2M-row local-scale dataset.

**Operation**
- Use `.github/prompts/spark-performance.prompt.md`.
- Replace each UDF with built-in Spark SQL functions (`regexp_replace`, `to_timestamp`, `get_json_object` / `from_json`) where semantics match exactly, and attach before/after CPU and duration evidence.

**Scoring**
- Binary: All replaceable UDFs removed from physical plan, output identical on all edge cases (nulls, malformed JSON, invalid dates) -> `true`, else `false`.
- Primary metric: `duration_delta_pct` (float, lower is better). Secondary metrics: `cpu_time_delta_pct`, `plan_diff_lines`.
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Real UDF input/output edge-case pairs verified by humans at `evals/data/spark/spark-udf-06-io-pairs.json`.