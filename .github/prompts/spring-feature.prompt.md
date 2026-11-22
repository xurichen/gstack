---
description: Java Spring feature implementation playbook (Stages 3 and 4)
---

# Playbook: Spring Feature Implementation

Execute Stages 3 and 4 for Java Spring Boot features. Change one variable at a time and save before/after evidence under `evidence/`.

## Steps

1. **Write a failing unit test from the spec (Red):** Target the narrowest seam (pure domain logic, validator, mapper, or service method) using JUnit 5 and AssertJ.
2. **Implement the minimal passing slice (Green):** Make the smallest change needed to pass the test.
3. **Add edge and contract cases:** Cover Bean Validation, authorization, error mapping, idempotency, and concurrency (optimistic/pessimistic locking or unique constraints).
4. **Test framework seams with slice tests:**
   - Web layer: `@WebMvcTest` + `MockMvc` for request binding, JSON serialization, status codes, and exception mapping.
   - Data layer: `@DataJpaTest` + `TestEntityManager` for query methods, mappings, and rollback behavior.
   - Do not use `@SpringBootTest` where a narrower slice test suffices.
5. **Verify against a real database with Testcontainers (Stage 4):**
   - Run the real target database family and version (for example PostgreSQL 16 or MySQL 8.4).
   - Execute Flyway or Liquibase migrations cleanly.
   - Inspect generated SQL, constraints, indexes, foreign keys, transaction boundaries, and query counts (Hibernate Statistics or `p6spy` / `datasource-proxy`).
6. **Run the real packaged artifact:** Build the boot JAR (`./mvnw package` or `./gradlew bootJar`), run it with production-like configuration and Actuator/Micrometer enabled, and execute smoke and contract tests.
7. **Package evidence:** Save `evidence/<id>-test-results.xml`, `evidence/<id>-db-evidence.md`, `evidence/<id>-queries.txt`, `evidence/<id>-perf.json`, and `evidence/<id>-rollback.md`.

## Outputs

- Implemented feature code and layered tests (unit, slice, Testcontainers integration, contract)
- Database, query-count, test, and performance evidence under `evidence/`
- Compatibility, canary, and rollback plan