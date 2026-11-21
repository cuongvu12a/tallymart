---
status: draft
owner: Cuong Vu
last_verified: 2026-11-21
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
- The check and the change MUST be protected by locking at the DB level ([R-INV-02](#r-inv-02)), because two requests can pass an unprotected check at the same time. Mechanism: [R-INV-02](#r-inv-02).
- Source: README, tagline and The problem.
- ✅ 50 concurrent requests against a starting Stock of 10 → units sold or reserved never exceed 10; oversold = 0 (README Metrics). In the test, with one unit per request, no per-user cap and no rate limit, exactly 10 MUST succeed; this is a test condition, not part of the rule ([Q-46](../OPEN_QUESTIONS.md#q-46)).
- ❌ 50 concurrent requests → 11 succeed.

<a id="r-inv-02"></a>
### R-INV-02: The database is where overselling is stopped

- The protection against overselling MUST be enforced at the DB level (locking).
- Do not rely on a cache or a rate limiter alone, because they can fail or be skipped → the DB decides.
- Mechanism: one conditional `UPDATE` that changes the available Stock only when enough is left; zero rows changed means not enough Stock. A `CHECK (available >= 0)` constraint is the second guard. Source: [Q-15](../OPEN_QUESTIONS.md#q-15) decision (owner, 2026-11-21).
- A Redis counter MAY sit in front only as a filter, after a measurement shows the need; the DB still decides.
- Source: README, The problem ("Locking at the DB level").
- ✅ The DB rejects the change that would oversell.
- ❌ Only a Redis counter decides, and the DB is updated later.

<a id="r-inv-03"></a>
### R-INV-03: Stock reservations expire

- Every stock reservation MUST have a TTL. When the TTL passes without the reservation being used, its stock MUST become sellable again.
- Reason: a buyer who never pays must not block stock forever.
- Source: README, The problem ("stock reservations with a TTL").
- ✅ A reservation expires; the stock is available to the next buyer.
- ❌ An unpaid reservation keeps the stock blocked with no end time.

<a id="r-inv-05"></a>
### R-INV-05: A Stock reservation is made when the Order is placed, and ends in exactly one way

- A Stock reservation MUST be made when the Order is placed, before payment. It MUST end in exactly one of two ways: the payment succeeds → the reservation becomes a final deduction; or it expires or the payment fails → its Stock is released.
- The TTL MUST be at least the payment window, so a Buyer who pays in time always gets the Stock. Value: **20 minutes**, for a 15-minute payment window ([R-PAY-02](payment.md#r-pay-02), [Q-22](../OPEN_QUESTIONS.md#q-22)).
- A scheduled job releases expired reservations with a conditional update, so a release and a payment for the same reservation cannot both win.
- Reason: reserving at checkout is the smallest window that still guarantees Stock to a Buyer who pays in time; reserving at "add to Cart" lets carts block Stock.
- Alternative: do not reserve when a Product is added to the Cart, and do not wait until payment → reserve at checkout.
- Source: [Q-14](../OPEN_QUESTIONS.md#q-14) decision (owner, 2026-11-21).
- ✅ A reservation expires at the same moment its IPN arrives → exactly one of "released" or "deducted" happens.
- ❌ The expiry job releases the Stock and the IPN handler deducts it as well.

<a id="r-inv-04"></a>
### R-INV-04: Per-user rate limiting in flash sales

- Flash sale requests MUST be rate limited per user.
- R-INV-01 MUST still hold if the rate limiter fails or is turned off, because the limiter protects capacity and fairness, not the invariant.
- Source: README, The problem.
- Mechanism: a token bucket in Redis, per user per Flash sale. Values are set after a k6 load test. If Redis is down, requests are still served (fail-open). Source: [Q-16](../OPEN_QUESTIONS.md#q-16) decision (owner, 2026-11-21).
- ✅ A user above the per-user limit is throttled (429).
- ❌ The rate limiter is the only thing that stops overselling.

<a id="r-inv-06"></a>
### R-INV-06: A Flash sale has its own Stock pool

- A Flash sale MUST have a time window, a special Price, its own Stock pool set aside from normal Stock, and a per-user quantity cap.
- Reason: a separate pool keeps a sale from blocking normal Orders, and makes the concurrency test match the README example (Stock 10, 50 Buyers).
- Alternative: do not run a Flash sale on normal Stock → set aside a pool.
- Source: [Q-17](../OPEN_QUESTIONS.md#q-17) decision (owner, 2026-11-21).
- ✅ A sale of 10 units ends; normal Stock of the Variant was never touched. ❌ Flash sale Buyers take all normal Stock.

## Conditional behavior

None yet.

## Edge cases

- Two Buyers try to reserve the last unit at the same moment → at most one succeeds (R-INV-01).
- The payment succeeds after the reservation expired → try to reserve again; if there is no Stock, the Payment is refunded automatically ([R-INV-05](#r-inv-05); Refund flow: [Q-23](../OPEN_QUESTIONS.md#q-23)).
- The same reserve request arrives twice → one effect. Over HTTP: the `Idempotency-Key` ([R-API-01](../RULES_AND_CONSTRAINTS.md#r-api-01)). From Ordering it is an in-process call ([R-ARCH-03](../RULES_AND_CONSTRAINTS.md#r-arch-03)); how a repeated call has one effect is part of the Checkout saga ([Q-25](../OPEN_QUESTIONS.md#q-25)).

## Open questions

None. Multi-channel stock sync is a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) ([Q-40](../OPEN_QUESTIONS.md#q-40)).

## Related

- Stock belongs to a Variant: [R-CAT-01](catalog.md#r-cat-01).

- Ordering uses Inventory: [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
