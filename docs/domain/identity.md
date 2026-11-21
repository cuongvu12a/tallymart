---
status: draft
owner: Cuong Vu
last_verified: 2026-11-21
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
- Where business code checks ownership (a Seller acts only on their own Products or Seller wallet): not decided ([Q-51](../OPEN_QUESTIONS.md#q-51)).
- Source: README, Architecture (Identity row).
- ✅ A user whose roles do not allow an action is rejected. Roles: [R-IDN-03](#r-idn-03).
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

<a id="r-idn-03"></a>
### R-IDN-03: One user, many roles; short access token, rotating refresh token

- A user MAY hold several roles: Buyer, Seller, Admin. The access token is a JWT that lives about 15 minutes. The refresh token is stored in the DB and replaced on each use; a used refresh token MUST NOT work again.
- Reason: revocable tokens matter once Withdrawals exist; one account with many roles is what the README's RBAC implies.
- Alternative: do not issue long-lived JWTs that cannot be revoked → short access token plus a rotating refresh token.
- Source: [Q-06](../OPEN_QUESTIONS.md#q-06) decision (owner, 2026-11-21). Built at Build-order step 9; before that, an Identity stub ([Build order](../PROJECT_OVERVIEW.md#build-order)).
- ✅ A stolen refresh token is used after the real user already rotated it → rejected. ❌ A JWT valid for 30 days with no way to revoke it.

<a id="r-idn-04"></a>
### R-IDN-04: eKYC is required before a Seller's first Withdrawal

- A Seller MUST pass eKYC before their first Withdrawal. Selling does not wait for eKYC.
- In the core, eKYC goes through its port with the Fake implementation only; a real provider is a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions).
- Reason: Withdrawal is the only path where money leaves the marketplace; eKYC there protects it without blocking earlier modules.
- Source: [Q-11](../OPEN_QUESTIONS.md#q-11) decision (owner, 2026-11-21). Vietnamese law on this is not checked (unverified).
- ✅ A Seller without eKYC sells, then asks for a Withdrawal → rejected until eKYC passes. ❌ A Withdrawal for a Seller who never passed eKYC.

<a id="r-idn-05"></a>
### R-IDN-05: Buyer personal data shown to Sellers is masked

- Buyer personal data shown to a Seller MUST be limited to what the Seller needs to handle the Order, and masked otherwise. The exact fields are fixed in the spec that first shows Buyer data to a Seller.
- Reason: personal data rules apply to Buyer data shown to Sellers (unverified); masking is cheap when designed early and costly to add later.
- Source: [Q-39](../OPEN_QUESTIONS.md#q-39) decision (owner, 2026-11-21).
- ✅ The Seller sees a masked phone number until the Shipment needs it. ❌ The Seller's Order list shows every Buyer's full phone number and email.

## Conditional behavior

None yet.

## Edge cases

- A request with no valid token reaches a protected action → reject it. Status code: 401 ([R-API-02](../RULES_AND_CONSTRAINTS.md#r-api-02)).

## Open questions

> OPEN QUESTION Q-51: Where do ownership checks live? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-51)

## Related

- [ARCHITECTURE](../ARCHITECTURE.md)
- Admin actions and the Audit trail: [R-ARCH-04](../RULES_AND_CONSTRAINTS.md#r-arch-04).
