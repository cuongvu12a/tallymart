---
status: active
owner: Cuong Vu
last_verified: 2026-11-15
applies_to: [docs]
related_code: []
---

# Architecture decision records

ADRs record why a technology, library or major structure was chosen. They are append-only: an accepted ADR is never edited.
How to write one: [docs/README: ADR process](../README.md#adr-process). Template: [0000-template.md](0000-template.md).

## Index

| Number | Title | Decision status | Supersedes |
|---|---|---|---|
| none yet | | | |

## ADRs to be written

The README already makes these decisions. Each one still needs an ADR that records the context and the options. The owner writes or approves them.

| Decision in the README | README section | Related rule or question |
|---|---|---|
| Modular monolith, split by bounded context; extraction needs an ADR | Architecture | [R-ARCH-01](../RULES_AND_CONSTRAINTS.md#r-arch-01) |
| `Idempotency-Key` on every write API | The problem | [R-API-01](../RULES_AND_CONSTRAINTS.md#r-api-01), [Q-04](../OPEN_QUESTIONS.md#q-04) |
| Transactional Outbox | The problem | [R-EVT-01](../RULES_AND_CONSTRAINTS.md#r-evt-01), [Q-26](../OPEN_QUESTIONS.md#q-26) |
| Double-entry, append-only ledger | The problem, Architecture | [R-LED-01](../domain/ledger.md#r-led-01), [R-LED-02](../domain/ledger.md#r-led-02) |
| Checkout saga with compensation, orchestrated by Ordering | The problem, Architecture | [R-ORD-02](../domain/ordering.md#r-ord-02) |
| Every external service behind a port with sandbox and fake implementations | External integrations | [R-INT-01](../RULES_AND_CONSTRAINTS.md#r-int-01) |
| pnpm monorepo with a client generated from OpenAPI | Tech stack | [R-REPO-03](../RULES_AND_CONSTRAINTS.md#r-repo-03) |
| Core stack: NestJS, Next.js, PostgreSQL, Redis, RabbitMQ, Docker Compose | Tech stack | none |
