---
status: draft
owner: Cuong Vu
last_verified: 2026-11-21
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
| Branch name | `<type>/tm-xx-<slug>`, for example `feat/tm-12-reserve-stock`. Docs work with no issue: `docs/<slug>` | [Q-08](OPEN_QUESTIONS.md#q-08) decision |
| Commit and PR title | Conventional Commits: `<type>(<context>): <summary> (TM-xx)`. Types: `feat`, `fix`, `docs`, `test`, `refactor`, `chore` | [Q-08](OPEN_QUESTIONS.md#q-08) decision |
| PR flow | One short-lived branch per work item → PR to `main` → CI passes → squash merge, one commit per work item | [Q-08](OPEN_QUESTIONS.md#q-08) decision |
| Who merges | AI sessions push the branch and open the PR. Only the owner merges, on GitHub. AI MUST NOT merge or push to `main` | [Q-08](OPEN_QUESTIONS.md#q-08) decision |
| Before CI exists | Work still goes through a PR; checks are run by hand until TM-repo-setup adds CI | [Q-08](OPEN_QUESTIONS.md#q-08) decision |

- ✅ `feat(inventory): reserve stock with TTL (TM-12)` · ❌ `update code`

## File names in `docs/`

| Doc type | File name | Example |
|---|---|---|
| Domain doc | `docs/domain/<context>.md`, lower case | `docs/domain/inventory.md` |
| Spec | `docs/specs/TM-xx-<short-name>.md` | `docs/specs/TM-12-reserve-stock.md` |
| ADR | `docs/decisions/NNNN-<short-name>.md` | `docs/decisions/0001-modular-monolith.md` |
| Runbook | `docs/runbooks/<task>.md` | `docs/runbooks/replay-dlq.md` |

## Code layout

Source: [Q-01](OPEN_QUESTIONS.md#q-01) decision (owner, 2026-11-21). Boundary rule: [R-ARCH-02](RULES_AND_CONSTRAINTS.md#r-arch-02).

```
apps/api/src/modules/<context>/
  domain/          plain TypeScript: entities, rules, no NestJS, no DB
  application/     use cases; opens DB transactions; calls domain and ports
  infrastructure/  repositories, Port implementations (sandbox, fake)
  api/             controllers, DTOs
  index.ts         the context's public interface; the only file other contexts import
```

- Create a layer folder only when it has code. Do not add empty layers.
- Each context's tables live in a Postgres schema named after the context, for example `inventory`.

## Data

- Primary keys are UUIDs. Prefer UUIDv7 (ordered by time, better for B-tree indexes) when the chosen PostgreSQL version has a built-in generator (PostgreSQL 18 `uuidv7()`, unverified); otherwise UUIDv4. The PostgreSQL version is chosen at TM-repo-setup. Source: owner decision, 2026-11-21.
- Reason: IDs shown in the API cannot be guessed, and an extracted context keeps its IDs without clashes ([R-ARCH-01](RULES_AND_CONSTRAINTS.md#r-arch-01)).

## Money

Source: [Q-12](OPEN_QUESTIONS.md#q-12) decision (owner, 2026-11-21).

- A money amount MUST be an integer in the smallest unit of its currency, stored as a `bigint` column next to a `currency` column with an ISO 4217 code.
- The core uses VND only. The `currency` column exists so another currency needs no migration (a [learning extension](PROJECT_OVERVIEW.md#learning-extensions)).
- In TypeScript, a money amount is a `bigint` or a small Money type, never a JS `number`, because float rounding would break [R-LED-01](domain/ledger.md#r-led-01). In JSON, it is a string.
- Rounding of percentage fees: [Q-19](OPEN_QUESTIONS.md#q-19).
- ✅ `{"amount": "150000", "currency": "VND"}` · ❌ `{"price": 150000.0}`

## API

- Errors: Problem Details with a stable `code` ([R-API-02](RULES_AND_CONSTRAINTS.md#r-api-02)).
- Write APIs: `Idempotency-Key` ([R-API-01](RULES_AND_CONSTRAINTS.md#r-api-01)).

## Tooling

Source: [Q-10](OPEN_QUESTIONS.md#q-10) decision (owner, 2026-11-21). These tools are approved as dependencies ([R-REPO-04](RULES_AND_CONSTRAINTS.md#r-repo-04)); anything else, including ESLint plugins, still needs approval.

| Job | Tool |
|---|---|
| Lint | ESLint, with `eslint-plugin-boundaries` for module boundaries ([Q-01](OPEN_QUESTIONS.md#q-01)) |
| Format | Prettier |
| Type check | TypeScript compiler, no emit |
| Unit and integration tests | Jest; Testcontainers for a real Postgres and broker |
| Mock HTTP for providers | WireMock |
| End-to-end web tests | Playwright |
| Load tests | k6 |
| Network faults | Toxiproxy |

Which test levels a task needs: [R-TEST-03](RULES_AND_CONSTRAINTS.md#r-test-03). Commands: TODO (TM-repo-setup).

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
