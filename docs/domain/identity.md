---
status: draft
owner: Cuong Vu
last_verified: 2026-11-16
applies_to: [backend, identity]
related_code: []
---

# Identity

## Purpose

Users (buyers, sellers, admins), authentication and authorization. Responsibility: [README: Architecture](../../README.md#architecture).

## Terms

[GLOSSARY: People and access](../GLOSSARY.md#people-and-access)

## Rules

<a id="r-idn-01"></a>
### R-IDN-01: Authorization uses RBAC

- Access to a protected action MUST be decided by the user's roles (RBAC).
- Do not grant access by a hard-coded user ID or email address, because it cannot be audited or changed safely → grant access by role.
- Whether business code may also check ownership (a Seller acts only on their own Products or Seller wallet), and where: Not decided ([Q-06](../OPEN_QUESTIONS.md#q-06)).
- Source: README, Architecture (Identity row).
- ✅ A user whose roles do not allow an action is rejected. Which roles exist and what each may do: Not decided ([Q-06](../OPEN_QUESTIONS.md#q-06)).
- ❌ `if (user.email === "...")` to allow an action.

<a id="r-idn-02"></a>
### R-IDN-02: Authentication can move to Keycloak without changing business code

- Business code MUST NOT depend on how a token is issued. Today authentication uses JWT. The README plans a later move to Keycloak.
- Keycloak and Google OAuth are external systems, so they sit behind a port: [R-INT-01](../RULES_AND_CONSTRAINTS.md#r-int-01).
- Reason (proposed by AI, owner to confirm): the README plans a move from JWT to Keycloak; if business code depends on how tokens are issued, that move changes every module.
- Alternative (proposed by AI, owner to confirm): do not read or issue tokens in business code → read the current user from one auth abstraction.
- Source: README, Architecture and External integrations.
- ✅ Controllers read the current user from one auth abstraction.
- ❌ Business code parses a JWT by hand.

## Conditional behavior

None yet.

## Edge cases

- A request with no valid token reaches a protected action → reject it. Status code: [Q-03](../OPEN_QUESTIONS.md#q-03).

## Open questions

> OPEN QUESTION Q-06: Which roles exist, can one user hold several roles, are ownership checks allowed, token lifetime, and admin powers? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-06)

> OPEN QUESTION Q-11: Must a seller pass eKYC (FPT.AI OCR) before listing products or before a withdrawal? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-11)

> OPEN QUESTION Q-39: Personal data protection and retention: in scope? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-39)

> OPEN QUESTION Q-41: Admin back-office and audit trail: scope and home? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-41)

## Related

- [ARCHITECTURE](../ARCHITECTURE.md)
