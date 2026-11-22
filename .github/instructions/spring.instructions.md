---
applyTo: "**/*spring*/**,**/spring*/**,**/src/main/java/**,**/src/test/java/**,**/pom.xml,**/build.gradle*"
---

# Java Spring Domain Pack Instructions

This file extends `shared.instructions.md` for Java Spring Boot services. Customize `applyTo` above if your Spring modules use different paths or Kotlin sources. Statements are labeled `[Fact]` or `[Recommended Practice]`.

## Spring Specification Checklist (Stage 1)

`[Recommended Practice]` Before implementing or modifying a Spring service, specify:

- [ ] API or event contract (endpoints, payloads, status codes, schema evolution rules).
- [ ] Input validation, authorization rules, and error mapping.
- [ ] Transaction semantics: boundaries, propagation, isolation, rollback rules, and self-invocation risks.
- [ ] Idempotency guarantees and retry behavior.
- [ ] Database effects: Flyway/Liquibase migrations, constraints, indexes, and generated SQL expectations.
- [ ] Service SLOs: latency percentiles (p50/p95/p99), error rate, and query-count budget.
- [ ] Contract test and backward-compatibility requirements.
- [ ] Canary criteria and rollback thresholds.

## Spring Guardrails (Stage 3)

### Transaction Self-Invocation Guardrail

- `[Fact]` Spring's default proxy-based `@Transactional` intercepts external calls through the proxy; calling another `@Transactional` method on `this` inside the same class bypasses the proxy and ignores the inner transaction boundary.
- `[Recommended Practice]` Move separate transaction boundaries into a dedicated collaborator bean, use AspectJ weaving when justified, or define the boundary at the entry facade. Always check for self-invocation during review.

### N+1 and Open-in-View Guardrails

- `[Fact]` `spring.jpa.open-in-view` defaults to `true` in Spring Boot, keeping the persistence context open through view rendering or JSON serialization and allowing lazy-loading queries during response rendering.
- `[Recommended Practice]` Set `spring.jpa.open-in-view=false` by default. Fix N+1 queries case by case using `JOIN FETCH`, `@EntityGraph`, DTO projections, `@BatchSize`, or dedicated queries rather than switching relationships to `FetchType.EAGER`.
- `[Recommended Practice]` Add query-count regression assertions (Hibernate Statistics, `datasource-proxy`, or `p6spy`) in integration tests.

### Slice Testing Seams

- `[Fact]` `@WebMvcTest` loads only the web MVC layer; `@DataJpaTest` loads only the JPA persistence layer; `@SpringBootTest` loads the full application context.
- `[Recommended Practice]` Test pure domain logic with fast unit tests, framework wiring with the narrowest slice test, and persistence or migration behavior against a real database via Testcontainers.

## Spring Verification Gate (Stage 4)

`[Recommended Practice]` A Spring change passes Stage 4 only when all items are verified:

- [ ] Integration tests run against the real target database family, version, migrations, and extensions via Testcontainers (not H2 approximations).
- [ ] Generated SQL and query counts inspected and within budget.
- [ ] Contract tests pass for all active consumers.
- [ ] Actuator/Micrometer health, error rate, latency percentiles, query count/latency, HikariCP pool saturation, JVM metrics, and business metrics compared before and after.
- [ ] Real packaged artifact (boot JAR or container image) exercised with production-like configuration.
- [ ] Risky changes include explicit canary criteria and rollback thresholds.

## Spring PR Evidence Checklist

`[Recommended Practice]` Every Spring PR includes under `evidence/`:

1. API, event, schema, and migration specification (`evidence/<id>-spec.md`).
2. Unit, slice, integration, and contract test results (`evidence/<id>-test-results.xml`).
3. Real database evidence when persistence changes: Testcontainers logs, generated SQL, query counts (`evidence/<id>-db-evidence.md`).
4. Query-count and SQL diff evidence for data-access changes (`evidence/<id>-queries.txt`).
5. Actuator/Micrometer or load-test comparison for latency-sensitive changes (`evidence/<id>-perf.json`).
6. Compatibility, canary, and rollback plan (`evidence/<id>-rollback.md`).