---
status: draft
owner: Cuong Vu
last_verified: 2026-11-16
applies_to: [backend, inventory]
related_code: []
---

# Inventory

## Purpose

What this context does: the Inventory row of [README: Architecture](../../README.md#architecture).

## Terms

[GLOSSARY: Catalog and stock](../GLOSSARY.md#catalog-and-stock)

## Rules

<a id="r-inv-01"></a>
### R-INV-01: Stock is never oversold (core invariant)

- The number of units sold or reserved MUST NEVER exceed the stock, under any level of concurrency.
- The check and the change MUST be protected by locking at the DB level ([R-INV-02](#r-inv-02)), because two requests can pass an unprotected check at the same time. Which locking mechanism: Not decided ([Q-15](../OPEN_QUESTIONS.md#q-15)).
- Source: README, tagline and The problem.
- ✅ 50 concurrent requests against a starting Stock of 10 → units sold or reserved never exceed 10; oversold = 0 (README Metrics). Whether exactly 10 must succeed: Not decided ([Q-46](../OPEN_QUESTIONS.md#q-46)).
- ❌ 50 concurrent requests → 11 succeed.

<a id="r-inv-02"></a>
### R-INV-02: The database is where overselling is stopped

- The protection against overselling MUST be enforced at the DB level (locking).
- Do not rely on a cache or a rate limiter alone, because they can fail or be skipped → the DB decides.
- Source: README, The problem ("Locking at the DB level").
- ✅ The DB rejects the change that would oversell.
- ❌ Only a Redis counter decides, and the DB is updated later.

> OPEN QUESTION Q-15: Which DB-level locking strategy? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-15)

<a id="r-inv-03"></a>
### R-INV-03: Stock reservations expire

- Every stock reservation MUST have a TTL. When the TTL passes without the reservation being used, its stock MUST become sellable again.
- Reason: a buyer who never pays must not block stock forever.
- Source: README, The problem ("stock reservations with a TTL").
- ✅ A reservation expires; the stock is available to the next buyer.
- ❌ An unpaid reservation keeps the stock blocked with no end time.

> OPEN QUESTION Q-14: When is a reservation made, what is the TTL, and what happens on expiry and on late payment? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-14)

<a id="r-inv-04"></a>
### R-INV-04: Per-user rate limiting in flash sales

- Flash sale requests MUST be rate limited per user.
- R-INV-01 MUST still hold if the rate limiter fails or is turned off, because the limiter protects capacity and fairness, not the invariant.
- Source: README, The problem.
- ✅ A user above the per-user limit is throttled. Limit values: Not decided ([Q-16](../OPEN_QUESTIONS.md#q-16)).
- ❌ The rate limiter is the only thing that stops overselling.

> OPEN QUESTION Q-16: Rate limit values and algorithm. DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-16)

## Conditional behavior

None yet.

## Edge cases

- Two Buyers try to reserve the last unit at the same moment → at most one succeeds (R-INV-01).
- A reservation expires while its payment is still being processed → not decided: [Q-14](../OPEN_QUESTIONS.md#q-14).
- The same reserve request arrives twice → one effect. How (HTTP `Idempotency-Key` per [R-API-01](../RULES_AND_CONSTRAINTS.md#r-api-01), or an in-process call): Not decided ([Q-02](../OPEN_QUESTIONS.md#q-02), [Q-14](../OPEN_QUESTIONS.md#q-14)).

## Open questions

> OPEN QUESTION Q-17: What exactly is a flash sale (time window, price, stock pool, per-user cap)? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-17)

> OPEN QUESTION Q-13: Does stock belong to the product or the variant? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-13)

> OPEN QUESTION Q-46: In the flash-sale test, is selling fewer units than the stock a failure? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-46)

> OPEN QUESTION Q-40: Multi-channel stock sync: in scope? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-40)

## Related

- Ordering uses Inventory: [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
