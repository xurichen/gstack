---
description: Java Spring performance and persistence diagnosis playbook (Stages 3 and 4)
---

# Playbook: Spring Diagnosis and Fix

Execute Stages 3 and 4 for diagnosing Java Spring Boot bugs, latency spikes, N+1 queries, connection-pool saturation, or transaction defects. Change one variable at a time and save before/after evidence under `evidence/`.

## Steps

1. **Reproduce in a controlled test:** Capture the exact request, response, generated SQL, query count, and transaction outcome (commit vs. rollback) using Testcontainers and deterministic seed data.
2. **Check for N+1 queries:** Enable SQL logging or Hibernate Statistics / `datasource-proxy` and count exact SQL statements per endpoint call.
3. **Check `@Transactional` self-invocation:** Inspect whether an intra-class method call bypasses the Spring proxy and silently drops `REQUIRES_NEW`, `readOnly`, or rollback rules.
4. **Check `open-in-view` and serialization-time lazy loading:** Verify `spring.jpa.open-in-view=false`. Identify any lazy associations triggered during JSON serialization or view rendering.
5. **Choose the narrowest fetch strategy per use case:**
   - Fixed small associations: `JOIN FETCH` or `@EntityGraph`.
   - Optional or large collections: DTO projections, dedicated queries, or `@BatchSize`.
   - Read-only views: DTO projections to avoid entity lifecycle overhead.
6. **Add a regression query-count assertion:** Lock the maximum allowed SQL count in an integration test so CI catches regressions automatically.
7. **Compare Actuator and Micrometer metrics (Stage 4):** Measure before and after under identical load for p50/p95/p99 latency, HikariCP pool usage, error rate, and query counts.
8. **Package evidence:** Save `evidence/<id>-repro.md`, `evidence/<id>-queries.txt`, `evidence/<id>-perf.json`, and `evidence/<id>-rollback.md`.

## Outputs

- Minimal root-cause fix and query-count or rollback regression test
- Reproduction log, SQL diff, and Actuator/Micrometer before/after metrics under `evidence/`
- Deployment and rollback notes