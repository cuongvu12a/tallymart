---
status: draft
owner: Cuong Vu
last_verified: 2026-11-19
applies_to: [backend, docs, repo]
related_code: []
---

# Learning mode

TallyMart is also the owner's backend learning project. This file is the **concept map**. For each concept, it says where the concept shows up in TallyMart, which code the owner writes, and what AI may do around it.

The rules AI follows are in [CLAUDE.md: Learning mode](../CLAUDE.md#4a-learning-mode). Reviews, hints and comparisons run through [`/review-learning`](../.claude/skills/review-learning/SKILL.md).

## How to use this file

- **This file is not a plan.** What to build next comes from the [Build order](PROJECT_OVERVIEW.md#build-order), [EPICS](product/EPICS.md) and the `docs/specs/TM-xx-*.md` specs. A concept is practiced when the spec that builds its module is worked on, never earlier.
- **This file decides nothing.** "Where it appears" names a place in TallyMart. It does not choose an answer to an open question. Where a choice is open, the row links to the `Q-NN`. For example, the owner may practice three locking strategies, but which one ships is [Q-15](OPEN_QUESTIONS.md#q-15).
- The concept list comes from the owner's study notes, which live outside this repo. Only concept names are copied here. Their order and dates are not. Source of this file: owner instruction, 2026-11-19.
- `OWNER TO CONFIRM` marks a mapping that AI proposed and the owner has not checked. Until the owner confirms it, AI MUST treat that row's "Owner writes" cell as owner-written (the safer side).

### Who edits this file

- Only the owner edits the concept map and the definitions.
- Exception: `/review-learning` MAY add rows to [Owner's recurring mistakes](#owners-recurring-mistakes). It MUST NOT change any other part of the file.

## Definitions

| Term | Meaning |
|---|---|
| Concept | One piece of knowledge the owner practices, with a stable ID `L-NN`. An ID is never reused. A removed concept keeps its row, marked `(removed YYYY-MM-DD: reason)` |
| Learning point | A concept that a spec practices, listed in the spec's "Learning points (owner-written)" section ([template](specs/_template.md)), with the functions or files the owner writes |
| Owner stub | A function body that AI leaves for the owner: a `// LEARN:` comment and a `throw new Error("TODO(owner): …")` line. Format: [CLAUDE.md: Learning mode](../CLAUDE.md#4a-learning-mode). An owner stub is not a Fake implementation (that is a port implementation for tests, [R-INT-01](RULES_AND_CONSTRAINTS.md#r-int-01)) |

## What AI may do for every concept

These apply to every row below. Each row's last column adds only what is specific to it.

- Repo setup, tool configuration, Docker Compose services for dependencies (PostgreSQL, Redis, RabbitMQ).
- DTOs, validation decorators, controllers and CRUD code that are not part of the concept being practiced.
- Interfaces and types, including Port interfaces and their Fake implementations ([R-INT-01](RULES_AND_CONSTRAINTS.md#r-int-01)).
- Scripts that generate test data, scripts that send load or take measurements ([R-TEST-02](RULES_AND_CONSTRAINTS.md#r-test-02)).
- Failing tests written before the owner's code, including edge cases and error cases.
- Docs.

AI MUST NOT add a dependency for any of this without asking ([R-REPO-04](RULES_AND_CONSTRAINTS.md#r-repo-04)).

## Concept map

### Design patterns and code structure

| ID | Concept | Where it appears in TallyMart | Owner writes | AI may also do |
|---|---|---|---|---|
| <a id="l-01"></a>L-01 | Singleton; singleton scope of a DI container; "one instance per process" | Shared clients that live once per process: the Redis client, the DB pool. The per-process limit matters again in [L-23](#l-23). OWNER TO CONFIRM which module first | The provider that creates the shared client, and its scope choice | Health check that uses the client |
| <a id="l-02"></a>L-02 | Factory (registry form), Simple Factory vs Factory Method | Payment: pick the Payment gateway Port implementation for a Payment method ([R-PAY-03](domain/payment.md#r-pay-03); mapping: [Q-21](OPEN_QUESTIONS.md#q-21)). Also Notification channels ([R-NTF-02](domain/notification.md#r-ntf-02)) | The registry factory: lookup by key, error on an unknown key. Registration happens in the composition root, not inside the factory | Fake implementations for each key |
| <a id="l-03"></a>L-03 | Builder with validation; immutable result | Ledger: build the set of Ledger entries for one money movement; `build()` rejects a set whose sum is not 0 ([R-LED-01](domain/ledger.md#r-led-01)). Which Ledger accounts exist: [Q-18](OPEN_QUESTIONS.md#q-18). OWNER TO CONFIRM | The builder, its `build()` checks, and how the result is made immutable | Test data for balanced and unbalanced sets |
| <a id="l-04"></a>L-04 | Strategy; replacing `if/switch` by type | OWNER TO CONFIRM. Candidates: choosing a Shipping quote policy ([Q-43](OPEN_QUESTIONS.md#q-43)); computing the Marketplace fee ([Q-19](OPEN_QUESTIONS.md#q-19)). Both are open | The strategy interface's implementations and the code that selects one | The interface type |
| <a id="l-05"></a>L-05 | Adapter; wrapping a third-party SDK behind our Port | Every Port: Payment gateways ([R-PAY-03](domain/payment.md#r-pay-03)), Carriers ([R-SHP-02](domain/shipping.md#r-shp-02)), Notification channels, E-invoice ([R-INVC-01](domain/invoicing.md#r-invc-01)) | The sandbox adapter that maps the provider's request and response shapes (IPN fields, Carrier status codes) to our Port types | Port interface, Fake implementation, recorded HTTP fixtures for mock-HTTP tests |
| <a id="l-06"></a>L-06 | Decorator; middleware as a pipeline | Adding cache, logging or retry around a Port or a repository without changing it. Natural first use: the cache around Product detail ([L-21](#l-21)) | The decorator class and where it is wired | Timing logs used for measurement |
| <a id="l-07"></a>L-07 | Dependency injection: constructor injection, lifetimes, composition root, captive dependency | The NestJS module of the first module that has a Port: bind the Port to its sandbox or Fake implementation by environment ([R-INT-01](RULES_AND_CONSTRAINTS.md#r-int-01), [R-INT-02](RULES_AND_CONSTRAINTS.md#r-int-02)). OWNER TO CONFIRM whether later modules count | That binding, and constructor injection in the class that uses the Port | Wiring in later modules, if the owner confirms |
| <a id="l-08"></a>L-08 | Repository; Unit of Work; transaction boundary in the service layer | Every module. The clearest case: placing an Order writes several tables in one DB transaction. Steps: [Q-25](OPEN_QUESTIONS.md#q-25) | The service method that opens the DB transaction, and the repository methods it calls inside it | Plain CRUD repository methods that are not a learning point |
| <a id="l-09"></a>L-09 | Observer; in-process events; publish before or after commit | Reacting to `OrderPaid` inside the process, if contexts call each other in-process ([Q-02](OPEN_QUESTIONS.md#q-02)). Leads to [L-26](#l-26) | The handler registration and the "after commit" decision | Tests that publish an event |
| <a id="l-10"></a>L-10 | Layered architecture, DTO vs entity, modular monolith, ports and adapters | All of `apps/api` ([R-ARCH-01](RULES_AND_CONSTRAINTS.md#r-arch-01)). Layout: [Q-01](OPEN_QUESTIONS.md#q-01) | What each module exposes to other modules (its public API), once Q-01 is decided | DTO ↔ entity mapping code |

### HTTP API and security

| ID | Concept | Where it appears in TallyMart | Owner writes | AI may also do |
|---|---|---|---|---|
| <a id="l-11"></a>L-11 | REST design: methods, status codes, `Location`, error format | All write endpoints. Error format: [Q-03](OPEN_QUESTIONS.md#q-03) | The controller of the first write endpoint the owner builds, its status codes and `Location` header. OWNER TO CONFIRM which endpoint (build order: [Q-09](OPEN_QUESTIONS.md#q-09)) | Other CRUD controllers, OpenAPI annotations |
| <a id="l-12"></a>L-12 | `Idempotency-Key`; safe and idempotent methods; "a timeout is not a failure" | Every write API ([R-API-01](RULES_AND_CONSTRAINTS.md#r-api-01)); "Place order" ([R-ORD-03](domain/ordering.md#r-ord-03)). Behavior and storage: [Q-04](OPEN_QUESTIONS.md#q-04) | The key check: first request, repeat with the same body, repeat with a different body, two requests at the same moment | The failing tests for those four cases |
| <a id="l-13"></a>L-13 | Authentication vs authorization; JWT checks; RBAC; password hashing | Identity ([R-IDN-01](domain/identity.md#r-idn-01), [R-IDN-02](domain/identity.md#r-idn-02)). Roles and token lifetime: [Q-06](OPEN_QUESTIONS.md#q-06) | JWT verification (signature, `exp`, `iss`, `aud`), the role guard, the password hash and verify calls | Registration DTOs, test users |
| <a id="l-14"></a>L-14 | Cursor (keyset) pagination vs OFFSET | The Seller's order list with a few million rows ([README: Metrics](../README.md#metrics)) | The keyset query with a tie-breaker column, and cursor encode and decode | Seed script for millions of Orders; p95 script |

### Database

| ID | Concept | Where it appears in TallyMart | Owner writes | AI may also do |
|---|---|---|---|---|
| <a id="l-15"></a>L-15 | Transactions, ACID, isolation levels, lost update, write skew | Inventory: reserving stock ([R-INV-01](domain/inventory.md#r-inv-01)); Ledger writes ([R-LED-01](domain/ledger.md#r-led-01)) | The DB transaction that reserves stock, and its isolation level | Concurrency test written first (`/invariant-test` shape A) |
| <a id="l-16"></a>L-16 | Stopping an Oversell: `SELECT … FOR UPDATE`, atomic conditional `UPDATE`, optimistic lock with `version`, `CHECK` as a safety net, deadlock and lock order | Inventory ([R-INV-02](domain/inventory.md#r-inv-02)). Which strategy ships: [Q-15](OPEN_QUESTIONS.md#q-15). Stock reservation lifecycle: [Q-14](OPEN_QUESTIONS.md#q-14) | The locking SQL and the retry on conflict. OWNER TO CONFIRM whether to build all three strategies as a lab before Q-15 is decided | Script that counts oversold units under 50 concurrent requests |
| <a id="l-17"></a>L-17 | B-Tree index, composite index and column order, partial, expression and covering index, index on foreign keys, write cost | The Seller's order list ([README: Metrics](../README.md#metrics)). Product search is a second candidate. OWNER TO CONFIRM | The index migration and the reason for each column order | Seed data, the measurement script |
| <a id="l-18"></a>L-18 | Reading `EXPLAIN (ANALYZE, BUFFERS)`; measuring p50 and p95; the order "measure, locate, analyze, fix, measure again" | Same place as [L-17](#l-17) | The before and after plans with a short note, and the changed query | The script that runs `EXPLAIN` and records p95 |
| <a id="l-19"></a>L-19 | N+1 query; JOIN vs batch `IN (...)` | Loading the Products of many Orders in the Seller's order list or the Buyer's Order history | The query that loads related rows in one batch | A test that counts queries, written first |
| <a id="l-20"></a>L-20 | Normalization, snapshot data, PK/FK/UNIQUE/CHECK constraints, UUID vs auto-increment | Order tables: whether the Order keeps a copy (snapshot) of the Price the Buyer paid. OWNER TO CONFIRM. Money storage: [Q-12](OPEN_QUESTIONS.md#q-12). Variant: [Q-13](OPEN_QUESTIONS.md#q-13) | The schema migration of the Order tables and its constraints | Migrations for tables that are not a learning point |

### Cache and rate limiting

| ID | Concept | Where it appears in TallyMart | Owner writes | AI may also do |
|---|---|---|---|---|
| <a id="l-21"></a>L-21 | Cache-aside, TTL, invalidation, eviction policy, "a cache is not always a win" | Catalog: Product detail with cache ([README: Metrics](../README.md#metrics)). The DB, not a cache, decides Stock ([R-INV-02](domain/inventory.md#r-inv-02)) | The read path (get, miss, load, set with TTL) and the invalidation when a Product changes | p95 script with and without cache |
| <a id="l-22"></a>L-22 | Cache stampede, penetration, avalanche, hot key; simple `SET NX PX` lock | Same place. A Flash sale Product is the hot key | The protection: TTL jitter, one loader per key, caching "not found" | Load script that triggers a stampede |
| <a id="l-23"></a>L-23 | Token bucket; atomic Redis script; race between instances; fail-open vs fail-closed | Per-user rate limit in a Flash sale ([R-INV-04](domain/inventory.md#r-inv-04)). Values and algorithm: [Q-16](OPEN_QUESTIONS.md#q-16). R-INV-01 MUST hold if the limiter fails | The limiter script and the guard that calls it. The fail-open or fail-closed choice is part of Q-16 | Load script with several API instances |

### Messaging and multi-step flows

| ID | Concept | Where it appears in TallyMart | Owner writes | AI may also do |
|---|---|---|---|---|
| <a id="l-24"></a>L-24 | Message queue basics: exchange, queue, binding, ack, prefetch | `OrderPaid` → Shipping and Notification ([ARCHITECTURE: Data flow](ARCHITECTURE.md#data-flow)) | Exchange, queue and binding declarations, and the ack handling in the first consumer | RabbitMQ in Docker Compose |
| <a id="l-25"></a>L-25 | At-least-once delivery, idempotent consumer, bounded retry with backoff, DLQ, poison message | Consumers in Shipping, Notification, Invoicing, Ledger. Carrier updates by event key ([R-SHP-01](domain/shipping.md#r-shp-01)). IPN handling ([R-PAY-01](domain/payment.md#r-pay-01)) is the same idea for a Webhook. Details: [Q-27](OPEN_QUESTIONS.md#q-27) | The duplicate check, the retry limit and the routing to the DLQ | Tests that deliver the same message twice; a poison message fixture |
| <a id="l-26"></a>L-26 | Dual write; Transactional Outbox; relay | `OrderPaid` ([R-EVT-01](RULES_AND_CONSTRAINTS.md#r-evt-01)). When: [Q-26](OPEN_QUESTIONS.md#q-26) | The outbox write in the same DB transaction, and the relay | A test that stops the process between commit and publish |
| <a id="l-27"></a>L-27 | Saga orchestration vs choreography; Compensation; timeout; "unknown result" of an external call | Checkout saga ([R-ORD-02](domain/ordering.md#r-ord-02)); Re-query on a missing IPN ([R-PAY-02](domain/payment.md#r-pay-02)). Steps: [Q-25](OPEN_QUESTIONS.md#q-25); schedule: [Q-22](OPEN_QUESTIONS.md#q-22) | The orchestrator steps, each Compensation, and the handling of an unknown result | Fake implementation modes: timeout, error, duplicate IPN |
| <a id="l-28"></a>L-28 | Timeout, retry with exponential backoff and jitter, retry storm, circuit breaker | Calls to Payment gateways and Carriers. Circuit breaker is not named in the README. OWNER TO CONFIRM | The retry and timeout wrapper, often as a Decorator ([L-06](#l-06)) | Fault injection setup for tests |
| <a id="l-29"></a>L-29 | Notification system: duplicate prevention, retries, delivery status | Notification ([R-NTF-01](domain/notification.md#r-ntf-01)). Duplicate handling: [Q-27](OPEN_QUESTIONS.md#q-27). Which events: [Q-29](OPEN_QUESTIONS.md#q-29) | The duplicate check and the delivery status update | Message templates |

### Scale and operations

| ID | Concept | Where it appears in TallyMart | Owner writes | AI may also do |
|---|---|---|---|---|
| <a id="l-30"></a>L-30 | Stateless API, scaling out, L7 load balancer, health check, graceful shutdown (`SIGTERM`) | `apps/api` behind Nginx ([README: Tech stack](../README.md#tech-stack)) | The Nginx upstream and health check config, the `SIGTERM` handler | Compose file with several API instances; load script |
| <a id="l-31"></a>L-31 | Connection pool size and pool mode | `apps/api` → PostgreSQL under load | The pool size choice with its measurement | The load script |
| <a id="l-32"></a>L-32 | Docker image layers, build cache, multi-stage build | `apps/api` image | The `Dockerfile` for `apps/api`. OWNER TO CONFIRM whether Compose files also count | Compose services for dependencies |
| <a id="l-33"></a>L-33 | CI pipeline (lint → test → build); integration tests with a real DB; mock-HTTP tests for providers | GitHub Actions ([README: Tech stack](../README.md#tech-stack)). Tooling: [Q-10](OPEN_QUESTIONS.md#q-10) | The pipeline order and its cache steps | Test container setup |
| <a id="l-34"></a>L-34 | Unit test doubles (mock, spy) | Any unit test. Ports use Fake implementations, not mocks ([R-INT-02](RULES_AND_CONSTRAINTS.md#r-int-02)). OWNER TO CONFIRM | Only when a spec lists L-34; otherwise AI writes tests | All other tests |
| <a id="l-35"></a>L-35 | Logs, metrics, traces; correlation ID; p95; SLO | Observability capability group ([README: Tech stack](../README.md#tech-stack)). OWNER TO CONFIRM | Correlation ID propagation, the first p95 metric | Dashboards and collector config |
| <a id="l-36"></a>L-36 | CQRS read model | Search capability group in the README (Elasticsearch, CQRS). OWNER TO CONFIRM | The write → read model update | Index mapping config |
| <a id="l-37"></a>L-37 | Read replicas, replication lag, read-your-writes, partitioning | Load capability group in the README (read replicas, partitioning). OWNER TO CONFIRM | Which reads go to a replica, and the partition key | Replica setup |
| <a id="l-38"></a>L-38 | Kubernetes: Deployment, Service, probes, rolling update, HPA | README capability group with Kubernetes (kind/k3d) + Helm. OWNER TO CONFIRM | Liveness and readiness probes and the rolling update settings | Cluster setup, Helm boilerplate |
| <a id="l-39"></a>L-39 | Backward-compatible deploys; expand–contract migrations | Any migration that changes an existing column ([R-REPO-01](RULES_AND_CONSTRAINTS.md#r-repo-01)) | The expand and contract migration pair | Data backfill script |

## Checked in every review (no single module)

`/review-learning` checks these in every review. They have no owner-written code of their own.

- SOLID, coupling and cohesion, Law of Demeter, composition over inheritance, Tell Don't Ask.
- Naming against [GLOSSARY](GLOSSARY.md) ([R-DOC-01](RULES_AND_CONSTRAINTS.md#r-doc-01)), duplication, single responsibility.
- YAGNI: a pattern used where a plain function would do.

## Concepts with no natural module yet

These concepts are in the owner's study list, but no TallyMart module needs them now. They are practiced outside this repo, unless the owner adds a module.

| Concept | Why no module |
|---|---|
| Big-O, data structures, HashMap internals | Used everywhere, owned by no module |
| TCP, UDP, DNS, TLS, "what happens when you type a URL" | Infrastructure knowledge; no TallyMart code |
| MVCC and WAL internals | Explains [L-15](#l-15) and [L-16](#l-16); no code of its own |
| CAP, consistency models, quorum | Only one database; see [L-37](#l-37) for read-your-writes |
| Sharding, consistent hashing | One database; no shard key needed |
| Unique ID generators (Snowflake, UUIDv7) | The primary key choice is not decided. OWNER TO CONFIRM if it needs a question |
| URL shortener, news feed, chat | README extension tracks or epics marked "Won't (this time)" ([EP-31](product/EPICS.md#ep-31)) |
| Behavioral interviews, presenting the project | Not code |

## Owner's recurring mistakes

Added by the owner or by `/review-learning`. If the same mistake comes back, add the new date to the existing row instead of a new row.

| Date | Concept | Mistake | Correct idea |
|---|---|---|---|
