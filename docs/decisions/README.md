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

## ADRs proposed from closed questions

Structural decisions the owner made in [OPEN_QUESTIONS](../OPEN_QUESTIONS.md). Each one still needs an ADR; the owner writes or approves it.

| Decision | Question | Rule |
|---|---|---|
| Money as an integer in the smallest unit plus a currency code; VND only in the core | [Q-12](../OPEN_QUESTIONS.md#q-12) | [CONVENTIONS: Money](../CONVENTIONS.md#money) |
| Every Product has at least one Variant; Price and Stock per Variant | [Q-13](../OPEN_QUESTIONS.md#q-13) | [R-CAT-01](../domain/catalog.md#r-cat-01) |
| Ledger accounts as data, keyed by account type, Account holder and currency | [Q-18](../OPEN_QUESTIONS.md#q-18), [Q-35](../OPEN_QUESTIONS.md#q-35) | [R-LED-04](../domain/ledger.md#r-led-04) |
| One NestJS module per context with layers; one Postgres schema per context; `eslint-plugin-boundaries` | [Q-01](../OPEN_QUESTIONS.md#q-01) | [R-ARCH-02](../RULES_AND_CONSTRAINTS.md#r-arch-02) |
| In-process calls for unlabeled arrows; Payment → Ledger shares one DB transaction | [Q-02](../OPEN_QUESTIONS.md#q-02) | [R-ARCH-03](../RULES_AND_CONSTRAINTS.md#r-arch-03) |
| RFC 9457 Problem Details with a stable `code` | [Q-03](../OPEN_QUESTIONS.md#q-03) | [R-API-02](../RULES_AND_CONSTRAINTS.md#r-api-02) |
| Stock locking: conditional `UPDATE` plus `CHECK` | [Q-15](../OPEN_QUESTIONS.md#q-15) | [R-INV-02](../domain/inventory.md#r-inv-02) |
| UUID primary keys, v7 preferred | owner decision, 2026-11-21 | [CONVENTIONS: Data](../CONVENTIONS.md#data) |
| Inbox table for consumers that touch money, Stock or e-invoices | [Q-27](../OPEN_QUESTIONS.md#q-27) | [R-EVT-02](../RULES_AND_CONSTRAINTS.md#r-evt-02) |
| Separate state machines for Order, Payment and Shipment; the Order row is the saga state | [Q-24](../OPEN_QUESTIONS.md#q-24), [Q-25](../OPEN_QUESTIONS.md#q-25) | [R-ORD-01](../domain/ordering.md#r-ord-01), [R-ORD-02](../domain/ordering.md#r-ord-02) |
| JWT access token with a rotating refresh token in the DB | [Q-06](../OPEN_QUESTIONS.md#q-06) | [R-IDN-03](../domain/identity.md#r-idn-03) |
