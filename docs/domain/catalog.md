---
status: draft
owner: Cuong Vu
last_verified: 2026-11-16
applies_to: [backend, catalog]
related_code: []
---

# Catalog

## Purpose

Products, variants and prices, and search. Responsibility: [README: Architecture](../../README.md#architecture).

## Terms

[GLOSSARY: Catalog and stock](../GLOSSARY.md#catalog-and-stock)

## Rules

No rules yet. The README gives this context responsibilities but no rules.

## Conditional behavior

None yet.

## Edge cases

None recorded yet.

## Open questions

> OPEN QUESTION Q-13: What is a variant, and do price and stock belong to the product or the variant? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-13)

> OPEN QUESTION Q-12: Currency, and how money amounts (prices) are stored. DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-12)

> OPEN QUESTION Q-09: Does Catalog depend on Identity (sellers own products)? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-09)

> OPEN QUESTION Q-40: Bulk product import: in scope? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-40)

## Related

- Search with Elasticsearch is in a later capability group: [README: Tech stack](../../README.md#tech-stack).
