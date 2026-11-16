---
status: draft
owner: Cuong Vu
last_verified: 2026-11-16
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

## Conditional behavior

None yet.

## Edge cases

- `Delivered` arrives twice → not decided whether a second e-invoice is prevented, and how: [Q-27](../OPEN_QUESTIONS.md#q-27).

## Open questions

> OPEN QUESTION Q-30: Who issues an e-invoice, for what amount, and when is it adjusted or replaced? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-30)

> OPEN QUESTION Q-39: Seller tax withholding: in scope? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-39)

## Related

- Consumes `Delivered` from Shipping: [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
