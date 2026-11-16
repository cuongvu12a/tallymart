---
status: draft
owner: Cuong Vu
last_verified: 2026-11-16
applies_to: [backend, web]
related_code: []
---

# Architecture

## Style

A modular monolith, split by bounded context. Extracting a context into a separate service needs a measurable reason and an ADR: [R-ARCH-01](RULES_AND_CONSTRAINTS.md#r-arch-01).

## Contexts

The 10 contexts and their responsibilities are listed in [README: Architecture](../README.md#architecture). That table is the only list. Each context has a domain doc in [domain/](domain/):

[identity](domain/identity.md) · [catalog](domain/catalog.md) · [ordering](domain/ordering.md) · [inventory](domain/inventory.md) · [payment](domain/payment.md) · [ledger](domain/ledger.md) · [reconciliation](domain/reconciliation.md) · [shipping](domain/shipping.md) · [notification](domain/notification.md) · [invoicing](domain/invoicing.md)

## Data flow

Every dependency between contexts that the README diagram shows. "Event" means the README labels the arrow with an event name. "Unlabeled" means the README draws an arrow with no label.

| From | To | README label | Meaning in the README |
|---|---|---|---|
| Ordering | Inventory | unlabeled | Ordering uses Inventory |
| Ordering | Payment | unlabeled | Ordering uses Payment |
| Payment | Ledger | unlabeled | Payment uses Ledger. Call or event: [Q-02](OPEN_QUESTIONS.md#q-02) |
| Reconciliation | Ledger | unlabeled | Reconciliation uses Ledger. Call or event: [Q-02](OPEN_QUESTIONS.md#q-02) |
| Ordering | Shipping | event `OrderPaid` | Shipping reacts to a paid order |
| Ordering | Notification | event `OrderPaid` | Notification reacts to a paid order |
| Shipping | Invoicing | event `Delivered` | Invoicing reacts to a delivery |
| Shipping | Ledger | event `Delivered` | Ledger reacts to a delivery |

> OPEN QUESTION Q-02: For each unlabeled arrow, is it an in-process call or an event? DO NOT assume. → [details](OPEN_QUESTIONS.md#q-02)

Identity and Catalog have no arrows in the README diagram.

Edges that other docs need but the README does not draw:

> OPEN QUESTION Q-43: Does Ordering get a Shipping quote from Shipping at checkout (no Ordering → Shipping arrow before `OrderPaid`)? DO NOT assume. → [details](OPEN_QUESTIONS.md#q-43)

> OPEN QUESTION Q-24: Do carrier statuses change the Order state (no Shipping → Ordering arrow)? DO NOT assume. → [details](OPEN_QUESTIONS.md#q-24)

> OPEN QUESTION Q-29: Which events notify whom (the README draws only `OrderPaid` → Notification)? DO NOT assume. → [details](OPEN_QUESTIONS.md#q-29)

> OPEN QUESTION Q-30: Does Invoicing adjust e-invoices after a Refund (no Payment → Invoicing arrow)? DO NOT assume. → [details](OPEN_QUESTIONS.md#q-30)

> OPEN QUESTION Q-37: After-sales exceptions: in scope, and which context owns them? DO NOT assume. → [details](OPEN_QUESTIONS.md#q-37)

> OPEN QUESTION Q-41: Admin back-office and audit trail: scope and home? DO NOT assume. → [details](OPEN_QUESTIONS.md#q-41)

### External systems

Providers are listed only in [README: External integrations](../README.md#external-integrations). This doc adds only what the README diagram shows about direction:

- Two-way arrows: Payment, Shipping, and Reconciliation (file or API, with payment gateways).
- One-way, outgoing: Notification, Invoicing.
- Not in the diagram: the Identity providers and the Public data APIs from the README integrations table. The README names no context for Public data.

Every external system sits behind a port with a sandbox implementation and a fake implementation: [R-INT-01](RULES_AND_CONSTRAINTS.md#r-int-01).

> OPEN QUESTION Q-31: Which sources does Reconciliation compare? The README table names gateways, banks and carriers; the README diagram shows gateways only. DO NOT assume. → [details](OPEN_QUESTIONS.md#q-31)

> OPEN QUESTION Q-47: How does a Withdrawal move money to the Seller's bank (no outgoing bank transfer in the README)? DO NOT assume. → [details](OPEN_QUESTIONS.md#q-47)

## Cross-cutting mechanisms

| Mechanism | Rule | Open details |
|---|---|---|
| `Idempotency-Key` on every write API | [R-API-01](RULES_AND_CONSTRAINTS.md#r-api-01) | [Q-04](OPEN_QUESTIONS.md#q-04) |
| Transactional Outbox | [R-EVT-01](RULES_AND_CONSTRAINTS.md#r-evt-01) | [Q-26](OPEN_QUESTIONS.md#q-26), [Q-27](OPEN_QUESTIONS.md#q-27) |
| Checkout saga with compensation, orchestrated by Ordering | [R-ORD-02](domain/ordering.md#r-ord-02) | [Q-25](OPEN_QUESTIONS.md#q-25) |
| Ports with sandbox and fake implementations | [R-INT-01](RULES_AND_CONSTRAINTS.md#r-int-01) | none |

## Module boundaries

> OPEN QUESTION Q-01: What is the folder layout inside `apps/api`, how are module boundaries enforced, and who owns which tables? DO NOT assume. → [details](OPEN_QUESTIONS.md#q-01)

## Repo layout

The layout is in [README: Tech stack](../README.md#tech-stack). Rules that apply to its paths: `apps/web` → [R-WEB-01](RULES_AND_CONSTRAINTS.md#r-web-01); `packages/api-client` → [R-REPO-03](RULES_AND_CONSTRAINTS.md#r-repo-03). None of these paths exist yet.

## Stack

The full stack, per capability group: [README: Tech stack](../README.md#tech-stack). Choosing or changing any part of it needs an ADR ([decisions/](decisions/README.md)).
