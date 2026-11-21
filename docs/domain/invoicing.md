---
status: draft
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [backend, invoicing]
related_code: []
---

# Invoicing

## Purpose

Issuing, adjusting and replacing e-invoices. Responsibility: [README: Architecture](../../README.md#architecture). Provider: [README: External integrations](../../README.md#external-integrations).

## Terms

[GLOSSARY: Shipping, notification, invoicing](../GLOSSARY.md#shipping-notification-invoicing)

## Rules

<a id="r-invc-01"></a>
### R-INVC-01: The e-invoice provider sits behind a port

- Applies [R-INT-01](../RULES_AND_CONSTRAINTS.md#r-int-01) to the e-invoice provider: SePay eInvoice MUST be reached through a port with a sandbox and a fake implementation.
- Reason (proposed by AI, owner to confirm): a real e-invoice is a tax document, so tests must never issue one by accident.
- Alternative (proposed by AI, owner to confirm): do not call the SePay eInvoice SDK from Invoicing code → call the port.
- Source: README, External integrations.
- ✅ Tests issue an e-invoice through the fake. ❌ Tests call the SePay eInvoice sandbox.

<a id="r-invc-02"></a>
### R-INVC-02: The marketplace invoices the Seller for the Marketplace fee

- In the core, the marketplace MUST issue an e-invoice to the Seller for the Marketplace fee of each Order, when the fee is taken ([R-LED-05](ledger.md#r-led-05)). Buyer invoices for Products are not in the core.
- Reason: it invoices only money the marketplace earns, which the Ledger already records. Vietnamese e-invoice law is not checked (unverified; get qualified advice).
- Source: [Q-30](../OPEN_QUESTIONS.md#q-30) decision (owner, 2026-11-21).
- ✅ Fee taken for an Order → one e-invoice to its Seller. ❌ An e-invoice to the Buyer for the Products.

## Conditional behavior

None yet.

## Edge cases

- `Delivered` arrives twice → one e-invoice, through the inbox ([R-EVT-02](../RULES_AND_CONSTRAINTS.md#r-evt-02)).

## Open questions

None. Seller tax withholding is a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) ([Q-39](../OPEN_QUESTIONS.md#q-39)).

## Related

- Consumes `Delivered` from Shipping: [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
