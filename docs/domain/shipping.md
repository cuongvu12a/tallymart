---
status: draft
owner: Cuong Vu
last_verified: 2026-11-21
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
- Do not apply every webhook as it arrives, because carriers send duplicates and updates out of order → deduplicate by event key, and let a state machine reject invalid transitions (README, The problem). Shipping keeps its own Shipment state machine ([Q-24](../OPEN_QUESTIONS.md#q-24)).
- Source: README, The problem.
- ✅ "Delivered" arrives twice → one `Delivered` event.
- ❌ "Delivered" arrives twice → the seller is paid twice.

- Event key: the Carrier's own event ID when the Carrier sends one; otherwise Carrier + tracking code + Carrier status + Carrier timestamp. The Carrier adapter builds the key. Source: [Q-28](../OPEN_QUESTIONS.md#q-28) decision (owner, 2026-11-21).

<a id="r-shp-02"></a>
### R-SHP-02: Carriers sit behind a port

- Applies [R-INT-01](../RULES_AND_CONSTRAINTS.md#r-int-01) to carriers: every carrier MUST be reached through a port with a sandbox and a fake implementation.
- Reason (proposed by AI, owner to confirm): Shipping tests must send duplicate and out-of-order statuses, which carrier staging cannot do on demand.
- Alternative (proposed by AI, owner to confirm): do not call a carrier SDK from Shipping code → call the port.
- Source: README, External integrations.
- ✅ Tests send out-of-order statuses through the fake. ❌ Tests call GHN staging.

<a id="r-shp-03"></a>
### R-SHP-03: Failed delivery and return to sender are handled in Shipping

- A failed delivery and the Return to sender that follows MUST be states of the Shipment state machine, owned by Shipping. The Compensation for the Order (Stock and Refund) is fixed in the Shipping spec.
- Returns after successful delivery and Disputes are a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions).
- Source: [Q-37](../OPEN_QUESTIONS.md#q-37) decision (owner, 2026-11-21).
- ✅ The Carrier reports a failed delivery, then the goods come back → the Shipment ends in "returned to sender". ❌ A failed delivery leaves the Order "in transit" forever.

## Conditional behavior

None yet.

## Edge cases

- "In transit" arrives after "delivered" → a delivered Order does not go back (README, The problem). The Shipment state machine rejects it ([R-SHP-01](#r-shp-01)).
- A status from a Carrier that is not in the allowed list → the Shipment state machine rejects it ([R-SHP-01](#r-shp-01)).

## Open questions

None. No Shipping quote at checkout ([R-ORD-06](ordering.md#r-ord-06)); a Shipment is created after the Seller confirms ([R-ORD-05](ordering.md#r-ord-05)).

## Related

- One Order has one Shipment: [R-ORD-04](ordering.md#r-ord-04).

- Consumes `OrderPaid`; publishes `Delivered` to Invoicing and Ledger: [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
