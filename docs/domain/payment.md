---
status: draft
owner: Cuong Vu
last_verified: 2026-11-16
applies_to: [backend, payment]
related_code: []
---

# Payment

## Purpose

Payment gateway integration, IPNs and webhooks, refunds. Responsibility: [README: Architecture](../../README.md#architecture). Providers: [README: External integrations](../../README.md#external-integrations).

## Terms

[GLOSSARY: Orders and payment](../GLOSSARY.md#orders-and-payment)

## Rules

<a id="r-pay-01"></a>
### R-PAY-01: IPN handling is idempotent

- An IPN that arrives several times MUST be recorded once.
- Do not record a payment each time an IPN arrives, because gateways resend IPNs → recognize a repeat and do not apply it a second time. What to reply to the gateway for a repeat: Not decided ([Q-04](../OPEN_QUESTIONS.md#q-04)).
- Source: README, The problem and Metrics ("IPN sent 10 times → recorded once").
- ✅ The same IPN arrives 10 times → one payment, one set of ledger entries.
- ❌ 10 IPNs → 10 Payments are recorded.

<a id="r-pay-02"></a>
### R-PAY-02: Re-query the payment status when the IPN does not arrive

- When an IPN is late or never arrives, the system MUST actively query the gateway for the payment status (for VNPay: `querydr`).
- Reason: an order must not stay "awaiting payment" forever because one webhook was lost.
- Source: README, The problem.
- ✅ No IPN after a while → the system queries the gateway and updates the payment.
- ❌ The system waits only for the IPN.

> OPEN QUESTION Q-22: When and how often to re-query, and when to give up? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-22)

<a id="r-pay-03"></a>
### R-PAY-03: Payment gateways sit behind a port

- Applies [R-INT-01](../RULES_AND_CONSTRAINTS.md#r-int-01) to payment gateways: every gateway MUST be reached through a port with a sandbox and a fake implementation.
- Reason (proposed by AI, owner to confirm): Payment tests must simulate duplicate, late and missing IPNs, which a sandbox cannot do on demand.
- Alternative (proposed by AI, owner to confirm): do not call a gateway SDK from Payment code → call the port.
- Source: README, External integrations.
- ✅ Tests simulate a duplicate IPN with the fake. ❌ Tests need the VNPay sandbox.

## Conditional behavior

None yet.

## Edge cases

- An IPN and the re-query result arrive at the same time → not decided: [Q-22](../OPEN_QUESTIONS.md#q-22).
- An IPN for an unknown or already closed order → not decided: [Q-25](../OPEN_QUESTIONS.md#q-25).

## Open questions

> OPEN QUESTION Q-21: Which payment method uses which provider (VNPay, SePay, Stripe)? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-21)

> OPEN QUESTION Q-23: Refund flow and its ledger entries. DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-23)

> OPEN QUESTION Q-34: Who decides a Refund for a Return, and how fast? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-34)

> OPEN QUESTION Q-35: Is cash on delivery (COD) in scope? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-35)

## Related

- Ordering → Payment and Payment → Ledger (README arrows; in-process call or event: [Q-02](../OPEN_QUESTIONS.md#q-02)): [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
