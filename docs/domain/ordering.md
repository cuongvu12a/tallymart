---
status: draft
owner: Cuong Vu
last_verified: 2026-11-16
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
- ✅ A delivered Order does not go back to "in transit" (README, The problem). Whether carrier statuses move the Order state at all, and which state machine rejects them: Not decided ([Q-24](../OPEN_QUESTIONS.md#q-24), [Q-28](../OPEN_QUESTIONS.md#q-28)).
- ❌ A late update moves a delivered Order back to "in transit".

> OPEN QUESTION Q-24: What are the order states and the allowed transitions? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-24)

<a id="r-ord-02"></a>
### R-ORD-02: Ordering orchestrates the checkout saga, with compensation

- The checkout saga MUST be orchestrated by Ordering. Every step that can fail after an earlier step succeeded MUST have a compensation.
- Reason: a failure in the middle of checkout must not leave stock reserved or money taken for an order that will not complete.
- Source: README, Architecture (Ordering row) and The problem ("saga with compensation").
- ✅ Payment fails → every earlier step is compensated; nothing stays reserved or taken. The steps and each compensation: Not decided ([Q-25](../OPEN_QUESTIONS.md#q-25)).
- ❌ Payment fails → the stock stays reserved until someone notices.

> OPEN QUESTION Q-25: What are the saga steps and the compensation for each? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-25)

<a id="r-ord-03"></a>
### R-ORD-03: A repeated "Place order" creates one order

- Applies [R-API-01](../RULES_AND_CONSTRAINTS.md#r-api-01) to placing an Order: a repeat with the same `Idempotency-Key` MUST NOT create another Order or another Payment. How many Orders one checkout creates: Not decided ([Q-05](../OPEN_QUESTIONS.md#q-05)).
- Reason (proposed by AI, owner to confirm): "Place order" is the write a Buyer is most likely to repeat (double click, retry on a slow network), and a repeat would create a second Order and a second Payment.
- Alternative (proposed by AI, owner to confirm): do not find repeats by comparing Order contents → use the `Idempotency-Key`.
- Source: README, The problem.
- ✅ Double click → no extra Order and no extra Payment. ❌ Double click → a second Order and a second Payment.

## Conditional behavior

None yet.

## Edge cases

- The payment result never arrives → the order MUST NOT stay "awaiting payment" forever ([R-PAY-02](payment.md#r-pay-02)). Timeout: [Q-22](../OPEN_QUESTIONS.md#q-22).
- The payment succeeds after the stock reservation expired → not decided: [Q-14](../OPEN_QUESTIONS.md#q-14).
- An order with products from several sellers → not decided: [Q-05](../OPEN_QUESTIONS.md#q-05).

## Open questions

> OPEN QUESTION Q-05: Can one order hold products from several sellers? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-05)

> OPEN QUESTION Q-02: Does Ordering call Inventory and Payment in-process, or through events? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-02)

> OPEN QUESTION Q-43: Does checkout need a Shipping quote before payment, and how does Ordering get it? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-43)

> OPEN QUESTION Q-37: After-sales exceptions (failed delivery, Return): in scope, and which context owns them? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-37)

> OPEN QUESTION Q-38: Is there a Seller handling step (and a Seller cancel) between payment and Shipment? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-38)

## Related

- Publishes `OrderPaid` to Shipping and Notification: [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
