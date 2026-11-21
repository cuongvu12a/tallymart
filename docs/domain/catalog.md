---
status: draft
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [backend, catalog]
related_code: []
---

# Catalog

## Purpose

Products, variants and prices, and search. Responsibility: [README: Architecture](../../README.md#architecture).

## Terms

[GLOSSARY: Catalog and stock](../GLOSSARY.md#catalog-and-stock)

## Rules

<a id="r-cat-01"></a>
### R-CAT-01: Every Product has at least one Variant; Price and Stock belong to the Variant

- Every Product MUST have at least one Variant. Price and Stock MUST belong to a Variant, never to the Product. A Product with no options has one default Variant.
- Reason: one sellable unit with one Stock row keeps the locking design the same for every Product ([R-INV-02](inventory.md#r-inv-02)), and moving Stock from Product to Variant later would mean migrating Stock and Stock reservations.
- Alternative: do not put a Price or Stock column on the Product → create a default Variant.
- Source: [Q-13](../OPEN_QUESTIONS.md#q-13) decision (owner, 2026-11-21).
- ✅ A T-shirt sold in one size has one default Variant that holds its Price and Stock.
- ❌ `products.stock` exists, and a second code path handles Products with Variants.

## Conditional behavior

None yet.

## Edge cases

None recorded yet.

## Open questions

None.

## Related

- Catalog owns Product reviews and Seller ratings, built at Build-order step 10 ([Q-50](../OPEN_QUESTIONS.md#q-50)).
- Bulk import of Products, Prices and Stock is in, with the full Catalog at step 9 ([Q-40](../OPEN_QUESTIONS.md#q-40)).

- Money format of a Price: [CONVENTIONS: Money](../CONVENTIONS.md#money).
- Catalog tables with seed data come at Build-order step 0; the Seller-facing Catalog API, which needs Identity for ownership, comes at step 9: [Build order](../PROJECT_OVERVIEW.md#build-order).

- Search with Elasticsearch is in a later capability group: [README: Tech stack](../../README.md#tech-stack).
