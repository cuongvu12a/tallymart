---
status: draft
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [backend, reconciliation]
related_code: []
---

# Reconciliation

## Purpose

What this context does: the Reconciliation row of [README: Architecture](../../README.md#architecture). In the core it compares Payment gateways only ([Q-31](../OPEN_QUESTIONS.md#q-31) decision).

## Terms

[GLOSSARY: Money](../GLOSSARY.md#money)

## Rules

<a id="r-rec-01"></a>
### R-REC-01: A reconciliation job runs every night

- A reconciliation job MUST run every night and compare external records with internal data.
- Reason: money that does not match the bank must be found, not lost silently.
- Source: README, The problem ("nightly reconciliation job").
- ✅ The nightly job compares Gateway transactions with internal Payments and finds a mismatch. What happens next: [R-REC-02](#r-rec-02).
- ❌ Mismatches are found only when a seller complains.

<a id="r-rec-02"></a>
### R-REC-02: A mismatch is reported, never corrected automatically

- A mismatch MUST be reported. A person fixes it with correcting Ledger entries ([R-LED-02](ledger.md#r-led-02)), recorded in the Audit trail ([R-ARCH-04](../RULES_AND_CONSTRAINTS.md#r-arch-04)).
- Reason: a mismatch usually means a bug; an automatic fix would hide it.
- Alternative: do not write rules that "fix" known mismatch types → report them.
- Source: [Q-31](../OPEN_QUESTIONS.md#q-31) decision (owner, 2026-11-21).
- ✅ A gateway transaction has no internal Payment → it appears in the mismatch report. ❌ The job creates the missing Payment by itself.

## Conditional behavior

None yet.

## Edge cases

- The gateway file or API is unavailable at job time → the report says the source was missing ([R-REC-02](#r-rec-02)); nothing is assumed to match.
- A mismatch is found → reported ([R-REC-02](#r-rec-02)).

## Open questions

None.

## Related

- COD is not in the core; it is a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) ([Q-35](../OPEN_QUESTIONS.md#q-35)).

- Reconciliation → Ledger (README arrow; in-process call: [R-ARCH-03](../RULES_AND_CONSTRAINTS.md#r-arch-03)); two-way file or API exchange with payment gateways (README diagram): [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow)
