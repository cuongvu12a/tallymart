---
status: draft
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [backend, notification]
related_code: []
---

# Notification

## Purpose

Email, SMS and push notifications, and tracking whether each one was delivered. Responsibility: [README: Architecture](../../README.md#architecture). Providers: [README: External integrations](../../README.md#external-integrations).

## Terms

[GLOSSARY: Shipping, notification, invoicing](../GLOSSARY.md#shipping-notification-invoicing)

## Rules

<a id="r-ntf-01"></a>
### R-NTF-01: The delivery status of every notification is tracked

- The system MUST record whether each notification was delivered.
- Reason: without it, nobody can tell whether a user was told about their order.
- Source: README, Architecture (Notification row).
- ✅ An email that bounced is recorded as not delivered.
- ❌ The system sends and forgets.

<a id="r-ntf-02"></a>
### R-NTF-02: Notification channels sit behind a port

- Applies [R-INT-01](../RULES_AND_CONSTRAINTS.md#r-int-01) to notification channels: email, SMS and push providers MUST be reached through a port with a sandbox and a fake implementation.
- Reason (proposed by AI, owner to confirm): tests must check what was sent without sending real email, SMS or push to anyone.
- Alternative (proposed by AI, owner to confirm): do not call a provider SDK from Notification code → call the port.
- Source: README, External integrations.
- ✅ Tests check the fake received one email. ❌ Tests send real email through Mailtrap.

<a id="r-ntf-03"></a>
### R-NTF-03: In the core, notifications are emails for three events

- In the core, Notification MUST send only email: to the Buyer when an Order is paid and when it is delivered; to the Seller when a new paid Order arrives. SMS and push are a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions).
- Source: [Q-29](../OPEN_QUESTIONS.md#q-29) decision (owner, 2026-11-21).
- ✅ `OrderPaid` → one email to the Buyer, one to the Seller. ❌ An SMS provider is called in the core.

## Conditional behavior

None yet.

## Edge cases

- `OrderPaid` arrives twice → the handler checks its own sent records and sends once; an inbox is not required for notifications ([R-EVT-02](../RULES_AND_CONSTRAINTS.md#r-evt-02)).

## Open questions

None.

## Related

- Consumes `OrderPaid`: [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
