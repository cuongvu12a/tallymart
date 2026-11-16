---
status: draft
owner: Cuong Vu
last_verified: 2026-11-15
applies_to: [backend, web, repo, docs]
related_code: []
---

# Conventions

Naming, layout and patterns. Hard rules are in [RULES_AND_CONSTRAINTS](RULES_AND_CONSTRAINTS.md). If a convention conflicts with a rule, the rule wins.

## Language

All repo files are in plain English: [R-DOC-03](RULES_AND_CONSTRAINTS.md#r-doc-03). Names in code use [GLOSSARY](GLOSSARY.md) terms: [R-DOC-01](RULES_AND_CONSTRAINTS.md#r-doc-01).

| Where | ✅ | ❌ |
|---|---|---|
| Class or type name | `StockReservation` | `Hold`, `Lock` |
| Event name | `OrderPaid` | `PurchaseCompleted` |
| Doc text | "The order is paid." | "The purchase went through." |

## Work items

- Work items are GitHub issues with IDs `TM-xx`. Do not use other ID formats (for example `FEAT-xxx`), because one ID format lets docs, commits and issues link to each other → use `TM-xx`.
- Specs: `docs/specs/TM-xx-<short-name>.md`, from the [spec template](specs/_template.md).
- `TM-repo-setup` is the placeholder for the repo setup work item. Replace it with the real `TM-xx` ID when the issue exists.

## Git

| Item | Convention | Source |
|---|---|---|
| Default branch | `main` | project brief |
| Branch names, commit message format, PR flow | Not decided | [Q-08](OPEN_QUESTIONS.md#q-08) |

> OPEN QUESTION Q-08: Branch names, commit message format and PR flow. DO NOT assume. → [details](OPEN_QUESTIONS.md#q-08)

## File names in `docs/`

| Doc type | File name | Example |
|---|---|---|
| Domain doc | `docs/domain/<context>.md`, lower case | `docs/domain/inventory.md` |
| Spec | `docs/specs/TM-xx-<short-name>.md` | `docs/specs/TM-12-reserve-stock.md` |
| ADR | `docs/decisions/NNNN-<short-name>.md` | `docs/decisions/0001-modular-monolith.md` |
| Runbook | `docs/runbooks/<task>.md` | `docs/runbooks/replay-dlq.md` |

## Code layout

> OPEN QUESTION Q-01: Folder layout and boundaries inside `apps/api`. DO NOT assume. → [details](OPEN_QUESTIONS.md#q-01)

## Money

> OPEN QUESTION Q-12: Currency, and how money amounts are stored and passed in code and the API. DO NOT assume. → [details](OPEN_QUESTIONS.md#q-12)

## API

> OPEN QUESTION Q-03: API error format and status codes. DO NOT assume. → [details](OPEN_QUESTIONS.md#q-03)

## Tooling

> OPEN QUESTION Q-10: Lint, format and test tooling, and which test levels a task needs to be done. DO NOT assume. → [details](OPEN_QUESTIONS.md#q-10)

## Preferred and forbidden patterns

Patterns the README or brief already decide. Each links to its rule.

| Do not | Because | Do instead | Rule |
|---|---|---|---|
| Call a provider SDK from business code | Tests would need the network | Call the port | [R-INT-01](RULES_AND_CONSTRAINTS.md#r-int-01) |
| Call a sandbox in tests or CI | Flaky, slow, rate-limited | Use the fake implementation | [R-INT-02](RULES_AND_CONSTRAINTS.md#r-int-02) |
| Publish to the broker after commit | The publish can fail after the commit | Write to the Transactional Outbox in the same transaction | [R-EVT-01](RULES_AND_CONSTRAINTS.md#r-evt-01) |
| Update or delete a ledger entry | It breaks the history and can hide errors | Add a new correcting entry | [R-LED-02](domain/ledger.md#r-led-02) |
| Change order state outside the state machine | Invalid transitions slip in | Go through the order state machine | [R-ORD-01](domain/ordering.md#r-ord-01) |
| Put business rules in `apps/web` | Rules drift between two places | Call the API through `packages/api-client` | [R-WEB-01](RULES_AND_CONSTRAINTS.md#r-web-01) |
