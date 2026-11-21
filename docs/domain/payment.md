---
status: draft
owner: Cuong Vu
last_verified: 2026-11-21
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
- Do not record a payment each time an IPN arrives, because gateways resend IPNs → recognize a repeat and do not apply it a second time. The endpoint derives an Idempotency key from the gateway's transaction ID and replies to a repeat with the stored first reply ([R-API-01](../RULES_AND_CONSTRAINTS.md#r-api-01)).
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

- Schedule: the payment window is **15 minutes**. When the Buyer comes back to the return URL, the status is checked at once. A job re-queries pending payments every 5 minutes until the window ends, then once more; a payment still pending is then closed as failed. Source: [Q-22](../OPEN_QUESTIONS.md#q-22) decision (owner, 2026-11-21).

<a id="r-pay-03"></a>
### R-PAY-03: Payment gateways sit behind a port

- Applies [R-INT-01](../RULES_AND_CONSTRAINTS.md#r-int-01) to payment gateways: every gateway MUST be reached through a port with a sandbox and a fake implementation.
- Reason (proposed by AI, owner to confirm): Payment tests must simulate duplicate, late and missing IPNs, which a sandbox cannot do on demand.
- Alternative (proposed by AI, owner to confirm): do not call a gateway SDK from Payment code → call the port.
- Source: README, External integrations.
- In the core, only VNPay has an adapter. The port is shaped from what VNPay, SePay and Stripe share: create payment, receive IPN, query status, refund. SePay and Stripe are a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) ([Q-21](../OPEN_QUESTIONS.md#q-21)).
- ✅ Tests simulate a duplicate IPN with the fake. ❌ Tests need the VNPay sandbox.

<a id="r-pay-04"></a>
### R-PAY-04: Only full Refunds, and only before the Seller's money is available

- In the core, a Refund MUST be for the whole Payment, and MUST happen before the Seller's money for that Order is available ([R-LED-06](ledger.md#r-led-06)). It is triggered by the system (late payment with no Stock, [R-INV-05](inventory.md#r-inv-05); a Seller cancel, [R-ORD-05](ordering.md#r-ord-05)) or by an Admin.
- Reason: a Refund after the Seller could withdraw can leave a Seller wallet negative.
- Source: [Q-23](../OPEN_QUESTIONS.md#q-23) decision (owner, 2026-11-21). Partial Refunds are a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions).
- ✅ The Seller cancels after payment → full Refund; the Seller's pending money is reversed. ❌ A partial Refund after the Seller withdrew the money.

## Conditional behavior

None yet.

## Edge cases

- An IPN and the re-query result arrive at the same time → both use the same Idempotency key from the gateway's transaction ID, so the payment is recorded once ([R-PAY-01](#r-pay-01)).
- A successful IPN for an Order that is already closed → the Payment is refunded automatically ([R-PAY-04](#r-pay-04)); the late-payment rule for an expired Stock reservation is [R-INV-05](inventory.md#r-inv-05).

## Open questions

None. Refunds for Returns wait for Returns, a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) ([Q-34](../OPEN_QUESTIONS.md#q-34)).

## Related

- COD is not in the core; it is a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) ([Q-35](../OPEN_QUESTIONS.md#q-35)).

- Ordering → Payment and Payment → Ledger (README arrows; in-process calls; Payment → Ledger MAY share one DB transaction: [R-ARCH-03](../RULES_AND_CONSTRAINTS.md#r-arch-03)): [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
