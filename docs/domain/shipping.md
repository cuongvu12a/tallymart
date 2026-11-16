---
status: draft
owner: Cuong Vu
last_verified: 2026-11-16
applies_to: [backend, shipping]
related_code: []
---

# Shipping

## Purpose

What this context does: the Shipping row of [README: Architecture](../../README.md#architecture). Providers: [README: External integrations](../../README.md#external-integrations).

## Terms

[GLOSSARY: Shipping, notification, invoicing](../GLOSSARY.md#shipping-notification-invoicing)

## Rules

<a id="r-shp-01"></a>
### R-SHP-01: Carrier status updates are deduplicated by event key

- A carrier status update that arrives more than once MUST have one effect. Repeats are found by an event key.
- Do not apply every webhook as it arrives, because carriers send duplicates and updates out of order → deduplicate by event key, and let a state machine reject invalid transitions (README, The problem). Which state machine: Not decided ([Q-24](../OPEN_QUESTIONS.md#q-24), [Q-28](../OPEN_QUESTIONS.md#q-28)).
- Source: README, The problem.
- ✅ "Delivered" arrives twice → one `Delivered` event.
- ❌ "Delivered" arrives twice → the seller is paid twice.

> OPEN QUESTION Q-28: What is the event key, and does a shipment have its own state machine? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-28)

<a id="r-shp-02"></a>
### R-SHP-02: Carriers sit behind a port

- Applies [R-INT-01](../RULES_AND_CONSTRAINTS.md#r-int-01) to carriers: every carrier MUST be reached through a port with a sandbox and a fake implementation.
- Reason (proposed by AI, owner to confirm): Shipping tests must send duplicate and out-of-order statuses, which carrier staging cannot do on demand.
- Alternative (proposed by AI, owner to confirm): do not call a carrier SDK from Shipping code → call the port.
- Source: README, External integrations.
- ✅ Tests send out-of-order statuses through the fake. ❌ Tests call GHN staging.

## Conditional behavior

None yet.

## Edge cases

- "In transit" arrives after "delivered" → a delivered Order does not go back (README, The problem). Which state machine rejects it, and whether some backward moves are real: Not decided ([Q-24](../OPEN_QUESTIONS.md#q-24), [Q-28](../OPEN_QUESTIONS.md#q-28)).
- A status from a carrier that is not in the allowed list → not decided: [Q-28](../OPEN_QUESTIONS.md#q-28).

## Open questions

> OPEN QUESTION Q-05: How do shipments relate to orders (one order, one shipment)? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-05)

> OPEN QUESTION Q-43: Does checkout need a Shipping quote before payment? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-43)

> OPEN QUESTION Q-37: Failed delivery and return to sender: in scope, and which context owns them? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-37)

> OPEN QUESTION Q-38: Is there a Seller handling step between payment and Shipment? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-38)

## Related

- Consumes `OrderPaid`; publishes `Delivered` to Invoicing and Ledger: [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
