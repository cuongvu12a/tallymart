---
status: draft
owner: Cuong Vu
last_verified: 2026-11-16
applies_to: [backend, reconciliation]
related_code: []
---

# Reconciliation

## Purpose

What this context does: the Reconciliation row of [README: Architecture](../../README.md#architecture). Which external sources it compares: Not decided ([Q-31](../OPEN_QUESTIONS.md#q-31)); the README table and diagram differ.

## Terms

[GLOSSARY: Money](../GLOSSARY.md#money)

## Rules

<a id="r-rec-01"></a>
### R-REC-01: A reconciliation job runs every night

- A reconciliation job MUST run every night and compare external records with internal data.
- Reason: money that does not match the bank must be found, not lost silently.
- Source: README, The problem ("nightly reconciliation job").
- ✅ The nightly job compares Gateway transactions with internal Payments and finds a mismatch. What happens to the mismatch: Not decided ([Q-31](../OPEN_QUESTIONS.md#q-31)).
- ❌ Mismatches are found only when a seller complains.

## Conditional behavior

None yet.

## Edge cases

- The gateway file or API is unavailable at job time → not decided: [Q-31](../OPEN_QUESTIONS.md#q-31).
- A mismatch is found → not decided: [Q-31](../OPEN_QUESTIONS.md#q-31). Any correction is a new ledger entry ([R-LED-02](ledger.md#r-led-02)).

## Open questions

> OPEN QUESTION Q-31: Which sources (the README table and diagram differ), and what happens on a mismatch? The schedule is nightly (README). DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-31)

> OPEN QUESTION Q-35: Is cash on delivery (COD) in scope? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-35)

## Related

- Reconciliation → Ledger (README arrow; in-process call or event: [Q-02](../OPEN_QUESTIONS.md#q-02)); two-way file or API exchange with payment gateways (README diagram): [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
