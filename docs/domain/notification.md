---
status: draft
owner: Cuong Vu
last_verified: 2026-11-16
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

## Conditional behavior

None yet.

## Edge cases

- `OrderPaid` arrives twice → not decided whether two notifications are acceptable: [Q-27](../OPEN_QUESTIONS.md#q-27).

## Open questions

> OPEN QUESTION Q-29: Which events notify whom, on which channel? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-29)

## Related

- Consumes `OrderPaid`: [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
