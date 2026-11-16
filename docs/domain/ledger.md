---
status: draft
owner: Cuong Vu
last_verified: 2026-11-16
applies_to: [backend, ledger]
related_code: []
---

# Ledger

## Purpose

What this context does: the Ledger row of [README: Architecture](../../README.md#architecture).

## Terms

[GLOSSARY: Money](../GLOSSARY.md#money)

## Rules

<a id="r-led-01"></a>
### R-LED-01: The ledger always balances (core invariant)

- The sum of all ledger entries MUST always be 0.
- Do not write a single-sided entry, because money would appear or disappear with no record of where it came from → every money movement is written as entries that balance.
- Source: README, tagline and The problem.
- ✅ A movement of 100 is written as +100 on one Ledger account and -100 on another.
- ❌ Only +100 is written to a seller wallet.

<a id="r-led-02"></a>
### R-LED-02: The ledger is append-only

- A ledger entry MUST NOT be updated or deleted.
- Reason: changing history hides mistakes and breaks reconciliation → fix a mistake by adding new correcting entries.
- Source: README, Architecture ("Append-only double-entry ledger").
- ✅ A wrong fee is fixed with a new pair of entries that reverses it.
- ❌ `UPDATE ledger_entries SET amount = ...`.

<a id="r-led-03"></a>
### R-LED-03: The seller is paid only after successful delivery

- The marketplace holds the buyer's money, deducts its marketplace fee, and MUST pay the seller only after successful delivery.
- Reason (proposed by AI, owner to confirm): until the Buyer has the Products, the money may have to go back to the Buyer, and money a Seller has already withdrawn cannot be recovered.
- Alternative (proposed by AI, owner to confirm): do not make the Seller's money available when the Payment succeeds → keep it unavailable to the Seller until successful delivery.
- Source: README, The problem; diagram (`Shipping -- Delivered --> Ledger`).
- ✅ The Seller's money becomes available only after successful delivery. What counts as successful delivery, and whether a return window applies: Not decided ([Q-20](../OPEN_QUESTIONS.md#q-20)).
- ❌ The seller can withdraw money for an order that has only been paid.

> OPEN QUESTION Q-20: What counts as successful delivery, is there a return window, and what are the withdrawal rules? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-20)

## Conditional behavior

None yet.

## Edge cases

- The same `Delivered` event arrives twice → not decided whether every consumer must give one effect, and how: [Q-27](../OPEN_QUESTIONS.md#q-27).
- A refund after the seller was paid → not decided: [Q-23](../OPEN_QUESTIONS.md#q-23).

## Open questions

> OPEN QUESTION Q-18: Which ledger accounts exist? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-18)

> OPEN QUESTION Q-19: Marketplace fee rate, and when it is taken. DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-19)

> OPEN QUESTION Q-12: Currency, and how money amounts are stored. DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-12)

> OPEN QUESTION Q-35: Is cash on delivery (COD) in scope? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-35)

> OPEN QUESTION Q-39: Seller tax withholding: in scope? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-39)

> OPEN QUESTION Q-42: Seller statement and finance reports: in scope? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-42)

> OPEN QUESTION Q-47: How does a Withdrawal move money to the Seller's bank? DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-47)

## Related

- Payment → Ledger and Reconciliation → Ledger (README arrows; in-process call or event: [Q-02](../OPEN_QUESTIONS.md#q-02)); Shipping → Ledger (`Delivered`): [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
