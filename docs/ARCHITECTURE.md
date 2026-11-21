---
status: draft
owner: Cuong Vu
last_verified: 2026-11-21
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
| Ordering | Inventory | unlabeled | In-process call ([R-ARCH-03](RULES_AND_CONSTRAINTS.md#r-arch-03)) |
| Ordering | Payment | unlabeled | In-process call |
| Payment | Ledger | unlabeled | In-process call; MAY share Payment's DB transaction ([R-ARCH-03](RULES_AND_CONSTRAINTS.md#r-arch-03)) |
| Reconciliation | Ledger | unlabeled | In-process call |
| Ordering | Shipping | event `OrderPaid` | Shipping reacts to a paid order |
| Ordering | Notification | event `OrderPaid` | Notification reacts to a paid order |
| Shipping | Invoicing | event `Delivered` | Invoicing reacts to a delivery |
| Shipping | Ledger | event `Delivered` | Ledger reacts to a delivery |

Unlabeled arrows are in-process calls through the callee's public interface; labeled arrows are events ([R-ARCH-03](RULES_AND_CONSTRAINTS.md#r-arch-03), [Q-02](OPEN_QUESTIONS.md#q-02) decision).

Identity and Catalog have no arrows in the README diagram.

Edges that other docs need but the README does not draw:

| From | To | Kind | Why | Source |
|---|---|---|---|---|
| Shipping | Ordering | event `Delivered` | The Order changes only on clean Shipping events; Carrier statuses stay in Shipping | [Q-24](OPEN_QUESTIONS.md#q-24) |
| Ordering | Shipping | in-process call | A Shipment is created after the Seller confirms ([R-ORD-05](domain/ordering.md#r-ord-05)) | [Q-38](OPEN_QUESTIONS.md#q-38) |
| Ordering | Payment | in-process call | Refund on a Seller cancel or a late payment ([R-PAY-04](domain/payment.md#r-pay-04)) | [Q-23](OPEN_QUESTIONS.md#q-23) |
| Ledger | Invoicing | when the Marketplace fee is taken | The e-invoice to the Seller for the fee ([R-INVC-02](domain/invoicing.md#r-invc-02)); call or event: decided in the Invoicing spec | [Q-30](OPEN_QUESTIONS.md#q-30) |

- No Shipping quote at checkout: no Ordering → Shipping edge before payment ([R-ORD-06](domain/ordering.md#r-ord-06)).
- Notifications in the core: [R-NTF-03](domain/notification.md#r-ntf-03).
- Failed delivery is owned by Shipping ([R-SHP-03](domain/shipping.md#r-shp-03)); Returns and Disputes are a [learning extension](PROJECT_OVERVIEW.md#learning-extensions).
- Admin actions stay in the owning context, with one Audit trail ([R-ARCH-04](RULES_AND_CONSTRAINTS.md#r-arch-04)).

### External systems

Providers are listed only in [README: External integrations](../README.md#external-integrations). This doc adds only what the README diagram shows about direction:

- Two-way arrows: Payment, Shipping, and Reconciliation (file or API, with payment gateways).
- One-way, outgoing: Notification, Invoicing.
- Not in the diagram: the Identity providers and the Public data APIs from the README integrations table. The README names no context for Public data.

Every external system sits behind a port with a sandbox implementation and a fake implementation: [R-INT-01](RULES_AND_CONSTRAINTS.md#r-int-01).

- Reconciliation compares Payment gateways only in the core ([Q-31](OPEN_QUESTIONS.md#q-31)).
- A Withdrawal leaves through an outgoing bank transfer port, with only a Fake implementation in the core ([R-LED-06](domain/ledger.md#r-led-06)).

## Cross-cutting mechanisms

| Mechanism | Rule | Open details |
|---|---|---|
| `Idempotency-Key` on every write API, stored in Postgres in the same DB transaction | [R-API-01](RULES_AND_CONSTRAINTS.md#r-api-01) | none |
| Problem Details errors with a stable `code` | [R-API-02](RULES_AND_CONSTRAINTS.md#r-api-02) | none |
| Transactional Outbox, from the first cross-context event | [R-EVT-01](RULES_AND_CONSTRAINTS.md#r-evt-01) | none |
| Checkout saga with compensation, orchestrated by Ordering; the Order row is the saga state | [R-ORD-02](domain/ordering.md#r-ord-02) | steps: Ordering spec |
| Inbox for consumers that touch money, Stock or e-invoices | [R-EVT-02](RULES_AND_CONSTRAINTS.md#r-evt-02) | retry counts: after measurement |
| Audit trail for Admin actions | [R-ARCH-04](RULES_AND_CONSTRAINTS.md#r-arch-04) | none |
| Stuck-state alerts (metrics and alerts, no work queue), with the observability capability group | [Q-44](OPEN_QUESTIONS.md#q-44) | none |
| Ports with sandbox and fake implementations | [R-INT-01](RULES_AND_CONSTRAINTS.md#r-int-01) | none |

## Module boundaries

One NestJS module per context, each owning its tables in its own Postgres schema; other contexts use only its public interface, and a lint rule checks this ([R-ARCH-02](RULES_AND_CONSTRAINTS.md#r-arch-02)). Folder layout: [CONVENTIONS: Code layout](CONVENTIONS.md#code-layout).

## Repo layout

The layout is in [README: Tech stack](../README.md#tech-stack). Rules that apply to its paths: `apps/web` → [R-WEB-01](RULES_AND_CONSTRAINTS.md#r-web-01); `packages/api-client` → [R-REPO-03](RULES_AND_CONSTRAINTS.md#r-repo-03). None of these paths exist yet.

## Stack

The full stack, per capability group: [README: Tech stack](../README.md#tech-stack). Choosing or changing any part of it needs an ADR ([decisions/](decisions/README.md)).
