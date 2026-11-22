# Java Spring Evaluation Suite (Starter Suite)

This starter suite covers core Java Spring Boot engineering tasks using JUnit 5, slice tests, and Testcontainers against real database engines.

## Task 1: N+1 Query Fix

- **Task ID:** `spring-nplus1-01`
- **Tier:** `human`

**Input**
- Entities: `Order` (`OneToMany` `OrderItem`) and `Customer` (`ManyToOne` `Order`).
- Current behavior: `OrderRepository.findAll()` returning 100 orders triggers `1 + 100 + 100*N` SQL queries with `spring.jpa.open-in-view=true`.
- SLO: p99 latency below 300ms, SQL query count at most 10.

**Operation**
- Use `.github/prompts/spring-diagnose.prompt.md` then `.github/prompts/spring-feature.prompt.md`.
- Set `spring.jpa.open-in-view=false`, evaluate `JOIN FETCH`, `@EntityGraph`, DTO projection, or `@BatchSize`, and add a query-count regression assertion.

**Scoring**
- Binary: Query count at most 10, p99 below 300ms, all functional and Testcontainers tests pass -> `true`, else `false`.
- Primary metric: `query_count_delta` (integer, lower is better). Secondary metrics: `latency_p99_delta_pct`.
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Real anonymized SQL query log for 100-order list rendering and human-confirmed query-count/p99 thresholds at `evals/data/spring/spring-nplus1-01-query-log.json`.

## Task 2: `@Transactional` Self-Invocation Bug

- **Task ID:** `spring-tx-02`
- **Tier:** `human`

**Input**
- Service class `OrderService` where `process()` calls `this.validate()` annotated with `@Transactional(propagation = Propagation.REQUIRES_NEW)`.
- Current defect: proxy is bypassed on self-invocation, so `REQUIRES_NEW` does not isolate rollback boundaries.

**Operation**
- Use `.github/prompts/spring-diagnose.prompt.md`.
- Extract the independent transaction boundary to a collaborator bean (or justified alternative) and add a Testcontainers rollback verification test.

**Scoring**
- Binary: `validate` commits or rolls back in an independent transaction verified against a real database, integration tests pass -> `true`, else `false`.
- Primary metric: `rollback_assertions_passed` (integer, higher is better). Secondary metrics: `query_count_delta`.
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Real rollback incident trace and human-confirmed expected database state before/after exception at `evals/data/spring/spring-tx-02-rollback-case.json`.

## Task 3: Slice Test Selection

- **Task ID:** `spring-slice-03`
- **Tier:** `synthetic`

**Input**
- Endpoint `POST /api/orders` (`OrderController` -> `OrderService` -> `OrderRepository` -> `PaymentClient`) currently tested exclusively with full `@SpringBootTest` taking 45 seconds.
- Target: unit + slice tests finish in under 5 seconds while keeping one Testcontainers integration smoke test.

**Operation**
- Use `.github/prompts/spring-feature.prompt.md`.
- Replace bloated context tests with narrow seams (`@WebMvcTest`, Mockito unit tests, `@DataJpaTest`, `@RestClientTest`/WireMock) plus one Testcontainers smoke test.

**Scoring**
- Binary: Unit and slice suite passes in under 5 seconds with no drop in behavioral coverage, Testcontainers smoke test passes -> `true`, else `false`.
- Primary metric: `test_time_total_sec` (float, lower is better). Secondary metrics: `test_count_unit`, `test_count_slice`, `test_count_integration`.
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Optional baseline timing log from CI at `evals/data/spring/spring-slice-03-timing-baseline.json`.

## Task 4: Open-in-View Removal

- **Task ID:** `spring-osiv-04`
- **Tier:** `human`

**Input**
- Application with 12 controllers mixing JSON APIs and Thymeleaf views running `spring.jpa.open-in-view=true`, causing long-held DB connections and HikariCP pool saturation. Three templates rely on lazy associations.

**Operation**
- Use `.github/prompts/spring-diagnose.prompt.md`.
- Identify every serialization/template lazy-loading trigger, replace with explicit fetch queries or DTO projections, and enable `spring.jpa.open-in-view=false` globally.

**Scoring**
- Binary: `spring.jpa.open-in-view=false` active globally, zero `LazyInitializationException` failures, peak HikariCP usage reduced, all tests pass -> `true`, else `false`.
- Primary metric: `hikari_pool_usage_delta_pct` (float, lower is better). Secondary metrics: `latency_p99_delta_pct`, `query_count_delta`.
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Real list of lazy-loading stack traces across controllers and human-prioritized fix order at `evals/data/spring/spring-osiv-04-lazy-triggers.json`.

## Task 5: Testcontainers Migration Verification

- **Task ID:** `spring-migration-05`
- **Tier:** `synthetic`

**Input**
- Flyway migrations `V1__init.sql` through `V12__add_index.sql` currently tested only on H2 in-memory DB, targeting PostgreSQL 15 and 16 in production.

**Operation**
- Use `.github/prompts/spring-feature.prompt.md`.
- Configure Testcontainers verification across target database versions, validate full migration + rollback script feasibility + generated SQL compatibility.

**Scoring**
- Binary: All target database container versions migrate cleanly with zero dialect errors and verified rollback notes -> `true`, else `false`.
- Primary metric: `migration_time_sec_per_version` (float, lower is better).
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Real migration logs and human-verified dialect compatibility notes at `evals/data/spring/spring-migration-05-migration-logs.json`.

## Task 6: Contract-Preserving API Change

- **Task ID:** `spring-contract-06`
- **Tier:** `synthetic`

**Input**
- Existing `GET /api/customers/{id}` returns `CustomerResponse` embedding `orders: List<OrderSummary>`.
- Requirement: introduce slim `GET /api/customers/{id}` (without orders) + `GET /api/customers/{id}/orders` while keeping existing clients working unchanged for 6 months.

**Operation**
- Use `.github/prompts/spring-feature.prompt.md`.
- Preserve backward-compatible contract (versioned or additive/deprecated path), add contract tests (Spring Cloud Contract or Pact), and document migration and rollback thresholds.

**Scoring**
- Binary: Legacy client contract tests pass unchanged, new endpoint passes all tests, rollback path verified -> `true`, else `false`.
- Primary metric: `latency_p99_delta_pct` (float, lower is better). Secondary metrics: `query_count_delta`.
- Cost telemetry: `tokens`, `time_sec`.

**Baseline:** to be measured

**Human-Input Data:** Real legacy client request/response payloads and human-verified compatibility contract at `evals/data/spring/spring-contract-06-legacy-contract.json`.