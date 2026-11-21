---
status: draft
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [backend, ordering]
related_code: []
---

# Ordering

## Purpose

Orders and the order state machine. Ordering orchestrates the checkout saga. Responsibility: [README: Architecture](../../README.md#architecture).

## Terms

[GLOSSARY: Orders and payment](../GLOSSARY.md#orders-and-payment)

## Rules

<a id="r-ord-01"></a>
### R-ORD-01: The order state machine blocks invalid transitions

- An order's state MUST change only through the order state machine. An invalid transition MUST be rejected.
- Do not set the state field directly, because an out-of-order or repeated update could move an order backward → ask the state machine to apply the transition.
- Source: README, The problem ("A 'delivered' order goes back to 'in transit'" → "State machine blocks invalid transitions").
- ✅ A delivered Order does not go back to "in transit" (README, The problem). Carrier statuses do not move the Order directly: Shipping keeps its own Shipment state machine and publishes clean events such as `Delivered`; the Order changes only on those events ([R-SHP-01](shipping.md#r-shp-01)).
- ❌ A late update moves a delivered Order back to "in transit".

- The Order, the Payment and the Shipment each have their own state machine. The Order keeps business states only (from [Q-24](../OPEN_QUESTIONS.md#q-24) option B: awaiting payment, paid, delivered, completed, cancelled; plus the Seller confirmation of [R-ORD-05](#r-ord-05)). Exact state names and transitions are fixed in the Ordering spec, which MUST also tell the Order state "delivered" apart from the Shipping event `Delivered` in the GLOSSARY. Source: Q-24 decision (owner, 2026-11-21).

<a id="r-ord-02"></a>
### R-ORD-02: Ordering orchestrates the checkout saga, with compensation

- The checkout saga MUST be orchestrated by Ordering. Every step that can fail after an earlier step succeeded MUST have a compensation.
- Reason: a failure in the middle of checkout must not leave stock reserved or money taken for an order that will not complete.
- Source: README, Architecture (Ordering row) and The problem ("saga with compensation").
- ✅ Payment fails → every earlier step is compensated; nothing stays reserved or taken. The Order row and its state machine are the saga state; a job resumes Orders stuck in a step, and every step is idempotent ([Q-25](../OPEN_QUESTIONS.md#q-25) decision). The list of steps and Compensations is written in the Ordering spec.
- ❌ Payment fails → the stock stays reserved until someone notices.


<a id="r-ord-03"></a>
### R-ORD-03: A repeated "Place order" creates one order

- Applies [R-API-01](../RULES_AND_CONSTRAINTS.md#r-api-01) to placing an Order: a repeat with the same `Idempotency-Key` MUST NOT create another Order or another Payment. One checkout creates one Order ([R-ORD-04](#r-ord-04)).
- Reason (proposed by AI, owner to confirm): "Place order" is the write a Buyer is most likely to repeat (double click, retry on a slow network), and a repeat would create a second Order and a second Payment.
- Alternative (proposed by AI, owner to confirm): do not find repeats by comparing Order contents → use the `Idempotency-Key`.
- Source: README, The problem.
- ✅ Double click → no extra Order and no extra Payment. ❌ Double click → a second Order and a second Payment.

<a id="r-ord-04"></a>
### R-ORD-04: An Order belongs to exactly one Seller

- An Order MUST belong to exactly one Seller. One checkout MUST cover the Products of one Seller only, and creates one Order with one Payment and one Shipment.
- Reason: with one Seller per Order, the Marketplace fee, paying the Seller, Refunds and the Shipment all stay per Order, so both invariants are easier to prove.
- Alternative: do not mix Sellers in one Order → the Buyer checks out once per Seller. Several Sellers in one checkout is a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions).
- Source: [Q-05](../OPEN_QUESTIONS.md#q-05) decision (owner, 2026-11-21).
- ✅ A Cart with Products from Seller X and Seller Y → checkout is refused until the Cart holds one Seller's Products.
- ❌ One Order holds lines from Seller X and Seller Y.

<a id="r-ord-05"></a>
### R-ORD-05: The Seller confirms a paid Order before a Shipment is created

- After payment, the Order MUST wait for the Seller to confirm before a Shipment is created. The confirmation has a deadline (value: Ordering spec). A Seller cancel, or a missed deadline, MUST run Compensation: release the Stock and refund the Buyer in full ([R-PAY-04](payment.md#r-pay-04)).
- Reason: in real marketplaces a Seller can find the Products missing after payment; handling that is a strong test of Compensation.
- Alternative: do not create the Shipment straight from `OrderPaid` → wait for the Seller.
- Source: [Q-38](../OPEN_QUESTIONS.md#q-38) decision (owner, 2026-11-21).
- ✅ The Seller cancels a paid Order → Stock released, full Refund, Order cancelled. ❌ The Seller cancels and the Buyer's money stays taken.

<a id="r-ord-06"></a>
### R-ORD-06: The Shipping fee is a flat amount stored on the Order

- The Shipping fee MUST be a flat amount from a setting, copied onto the Order when it is placed. There is no Carrier quote at checkout.
- Reason: a quote at checkout would need Shipping before Ordering in the Build order; a flat fee keeps checkout simple. Carrier quotes are a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions).
- Source: [Q-43](../OPEN_QUESTIONS.md#q-43) decision (owner, 2026-11-21).
- ✅ The Buyer sees the full Price plus the flat Shipping fee before paying. ❌ Ordering calls a Carrier during checkout.

## Conditional behavior

None yet.

## Edge cases

- The payment result never arrives → the order MUST NOT stay "awaiting payment" forever ([R-PAY-02](payment.md#r-pay-02)). Timeout: [Q-22](../OPEN_QUESTIONS.md#q-22).
- The payment succeeds after the Stock reservation expired → reserve again, or refund automatically if there is no Stock ([R-INV-05](inventory.md#r-inv-05)).
- A Cart with Products from several Sellers → checkout is refused ([R-ORD-04](#r-ord-04)).

## Open questions

None. Returns and Disputes are a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) ([Q-37](../OPEN_QUESTIONS.md#q-37)); failed delivery is in Shipping ([R-SHP-03](shipping.md#r-shp-03)).

## Related

- Calls Inventory and Payment in-process ([R-ARCH-03](../RULES_AND_CONSTRAINTS.md#r-arch-03)).
- Publishes `OrderPaid` to Shipping and Notification: [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
