---
status: draft
owner: Cuong Vu
last_verified: 2026-11-21
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
- Successful delivery: N days after the `Delivered` event with no open case, **N = 7** as a setting (the return window). The Seller sees the release date per Order. Source: [Q-20](../OPEN_QUESTIONS.md#q-20) decision (owner, 2026-11-21).
- ✅ The Seller's money becomes available 7 days after `Delivered`.
- ❌ The seller can withdraw money for an order that has only been paid.

<a id="r-led-04"></a>
### R-LED-04: Ledger accounts are data, keyed by account type, Account holder and currency

- A Ledger account MUST be identified by its account type, its Account holder (holder type + holder ID) and its currency. A new account type or holder type MUST be added as new data, never by changing existing Ledger entries.
- Initial account types: gateway clearing (money a Payment gateway owes the marketplace), Seller pending (paid, not yet delivered), Seller available (the Seller wallet), Marketplace fee revenue, refunds payable, bank. Initial holder types: Seller, marketplace, Payment gateway. A Carrier holder type is reserved for COD, a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions).
- Reason: Ledger entries are append-only ([R-LED-02](#r-led-02)), so entries cannot be re-keyed later. COD, Vouchers and tax withholding each add accounts; with accounts as data, that is new rows, not a migration of money data.
- Alternative: do not hard-code one column or one code path per account → post every entry against a Ledger account row.
- Source: [Q-18](../OPEN_QUESTIONS.md#q-18) and [Q-35](../OPEN_QUESTIONS.md#q-35) decisions (owner, 2026-11-21).
- ✅ COD is added later: a Carrier holder type and its accounts are inserted; no existing entry changes.
- ❌ A `seller_wallet_balance` column, or an account enum that only code knows, so a new account needs a migration of old entries.

<a id="r-led-05"></a>
### R-LED-05: The Marketplace fee is 5%, fixed on the Order, taken at successful delivery

- The Marketplace fee rate MUST be copied onto the Order when it is placed. The fee MUST be taken at successful delivery, rounded down to a whole VND. The rate for new Orders is **5%** (a setting).
- Reason: a rate stored on the Order makes past fees reproducible in Reconciliation and stops a rate change from touching existing Orders; taking it at delivery means a Refund before delivery needs no fee reversal. Rounding down is one rule, in one place, in the Seller's favor.
- Alternative: do not read the current rate when the fee is taken → use the rate stored on the Order.
- Source: [Q-19](../OPEN_QUESTIONS.md#q-19) decision (owner, 2026-11-21).
- ✅ An Order of 99,999 VND → fee 4,999 VND (4,999.95 rounded down). ❌ The rate changes to 6% and old Orders are charged 6%.

<a id="r-led-06"></a>
### R-LED-06: A Withdrawal needs available money, eKYC and Admin approval

- A Withdrawal MUST take only available money, MUST need the Seller's eKYC ([R-IDN-04](identity.md#r-idn-04)), and MUST be approved by an Admin.
- The money goes out through an outgoing bank transfer port; in the core only its Fake implementation exists.
- Reason: money that has left the marketplace cannot be taken back; the approval and the port with a fake let the flow be tested without a real bank.
- Source: [Q-20](../OPEN_QUESTIONS.md#q-20), [Q-47](../OPEN_QUESTIONS.md#q-47) decisions (owner, 2026-11-21).
- ✅ A Seller asks for a Withdrawal → an Admin approves → the fake transfer succeeds → Ledger entries move the money out. ❌ A Withdrawal of money still pending delivery.

<a id="r-led-07"></a>
### R-LED-07: Each group of Ledger entries is checked in code and in the DB

- Every group of Ledger entries for one money movement MUST be written through one write function that checks the sum is 0 and inserts the group in one DB transaction. A DB check at commit MUST also reject a group whose sum is not 0.
- Reason: the code path is where the rule lives; the DB check catches any write that bypasses it ([R-LED-01](#r-led-01)).
- Source: [Q-49](../OPEN_QUESTIONS.md#q-49) decision (owner, 2026-11-21).
- ✅ A bug builds an unbalanced group → the DB rejects the commit. ❌ A raw insert of one entry succeeds.

## Conditional behavior

None yet.

## Edge cases

- The same `Delivered` event arrives twice → one effect, through the inbox ([R-EVT-02](../RULES_AND_CONSTRAINTS.md#r-evt-02)).
- A Refund after the Seller's money is available → not in the core: only full Refunds before that point ([R-PAY-04](payment.md#r-pay-04)); partial and late Refunds are a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions).

## Open questions

None.

## Related

- Seller statement: the Ledger serves a read view per Seller wallet; other reports are out of the core ([Q-42](../OPEN_QUESTIONS.md#q-42)).
- Seller tax withholding: room in the Ledger accounts ([R-LED-04](#r-led-04)); built later as a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) ([Q-39](../OPEN_QUESTIONS.md#q-39)).

- Money amounts: [CONVENTIONS: Money](../CONVENTIONS.md#money). COD is a learning extension, not in the core: [PROJECT_OVERVIEW: Learning extensions](../PROJECT_OVERVIEW.md#learning-extensions).

- Payment → Ledger and Reconciliation → Ledger (README arrows; in-process calls; Payment → Ledger MAY share one DB transaction: [R-ARCH-03](../RULES_AND_CONSTRAINTS.md#r-arch-03)); Shipping → Ledger (`Delivered`): [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
