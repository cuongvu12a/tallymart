---
status: draft
owner: Cuong Vu
last_verified: 2026-11-16
applies_to: [backend, web, repo, docs]
related_code: []
---

# Rules and constraints

Cross-cutting hard rules. Rules for one context live in that context's doc. Area codes and where each area's rules live: [docs/README: Area codes](README.md#area-codes).

Precedence on conflict: RULES > TM-xx spec > CONVENTIONS > habits.

## Architecture

<a id="r-arch-01"></a>
### R-ARCH-01: Modular monolith; extracting a service needs an ADR

- The backend MUST be one deployable modular monolith, split by bounded context.
- A context MUST NOT be extracted into a separate service without a measurable reason recorded in an ADR.
- Reason: extraction adds network failures and distributed transactions, which put both core invariants at risk.
- Source: README, Architecture.
- ✅ "ADR 0012: extract Catalog search because p95 is X ms under Y RPS (measured by `<script>`)."
- ❌ Creating `apps/payment-service` because "it is cleaner".

> OPEN QUESTION Q-01: Folder layout, boundary enforcement and table ownership inside `apps/api`. DO NOT assume. → [details](OPEN_QUESTIONS.md#q-01)

## HTTP API

<a id="r-api-01"></a>
### R-API-01: Every write API takes an `Idempotency-Key`

- Every API that changes state MUST accept an `Idempotency-Key` header. A repeated request with the same key MUST have the effect of exactly one request.
- Reason: a user who clicks "Place order" twice on a flaky network must not get two Orders or two Payments.
- Source: README, The problem.
- ✅ Two `POST` requests with the same key → one Order. What the second response returns: Not decided ([Q-04](OPEN_QUESTIONS.md#q-04)).
- ❌ Two `POST` requests with the same key → two Orders.

| Condition | Behavior |
|---|---|
| Same key, same body, first request finished | Not decided: [Q-04](OPEN_QUESTIONS.md#q-04) |
| Same key, different body | Not decided: [Q-04](OPEN_QUESTIONS.md#q-04) |
| Same key, first request still running | Not decided: [Q-04](OPEN_QUESTIONS.md#q-04) |
| Key missing | Not decided: [Q-04](OPEN_QUESTIONS.md#q-04) |

> OPEN QUESTION Q-04: Storage, TTL, replay behavior and status codes for `Idempotency-Key`. DO NOT assume. → [details](OPEN_QUESTIONS.md#q-04)
> OPEN QUESTION Q-03: What is the API error format and the list of status codes? DO NOT assume. → [details](OPEN_QUESTIONS.md#q-03)

## Events

<a id="r-evt-01"></a>
### R-EVT-01: A DB change and its event MUST NOT diverge

- When a DB write must produce an event, the event MUST be recorded through a Transactional Outbox in the same DB transaction.
- When the Outbox is built (with the first cross-context event, or later): Not decided ([Q-26](OPEN_QUESTIONS.md#q-26)). The README names the Outbox as the solution, not when to build it.
- Once the Outbox exists, do not publish to the broker directly after the commit, because the publish can fail after the commit → write to the outbox, and let a relay publish it.
- Reason: "order paid but nobody ships it".
- Source: README, The problem.
- ✅ Order status update and outbox row in one transaction; a relay publishes `OrderPaid`.
- ❌ `commit()` then `broker.publish()`; the process crashes between them.

> OPEN QUESTION Q-26: Build the Outbox with the first cross-context event, or publish directly first and add it later? DO NOT assume. → [details](OPEN_QUESTIONS.md#q-26)
> OPEN QUESTION Q-27: Retries, DLQ handling and consumer deduplication. DO NOT assume. → [details](OPEN_QUESTIONS.md#q-27)

## External integrations

<a id="r-int-01"></a>
### R-INT-01: Every external service sits behind a port with two implementations

- Every external service MUST be called only through a port. Each port MUST have a sandbox implementation and a fake implementation.
- Do not call a provider SDK or URL from business code, because tests could then not run without the network → call the port.
- Source: README, External integrations.
- ✅ `Payment` calls a payment-gateway port; the test wires the fake implementation.
- ❌ The `Payment` module imports a VNPay client directly.

<a id="r-int-02"></a>
### R-INT-02: Tests and CI use only fake implementations

- Tests and CI MUST NOT call a real sandbox, because sandboxes are slow, rate-limited and sometimes down, which makes tests flaky → use the fake implementation.
- Source: project brief ("never call real sandboxes in tests / CI"); README, External integrations ("Tests and CI use only the fake implementation").

| Where the code runs | Implementation | Example |
|---|---|---|
| Unit test | Fake | Payment port → fake returns "paid" |
| Integration test | Fake | Same, with a real Postgres via Testcontainers |
| CI | Fake | No sandbox keys in CI |
| Local run with sandbox keys in `.env` | Sandbox | Calls VNPay sandbox |
| Local run with empty sandbox keys | Fake | README: "leave empty to use the fakes" |

- ✅ A test simulates "IPN sent 10 times" with the fake implementation.
- ❌ A CI job that needs `VNPAY_*` secrets to pass.

## Tests and measurements

<a id="r-test-01"></a>
### R-TEST-01: A task is done only when tests + lint pass

- A task MUST NOT be reported as done unless its Definition of Done in the table below is met. For a task that changes code, config or tests, that means tests and lint pass.
- If the commands do not exist yet, the report MUST say that tests and lint could not run.
- Reason: "done" must be checkable, not a feeling.
- Source: project brief.
- ✅ "Done. Tests: pass. Lint: pass." ❌ "Done, should work."

| Task type | Done when |
|---|---|
| Changes code, config or tests | Tests and lint pass |
| Changes only docs (no code, config or tests) | Every link resolves; `scripts/check-docs.sh` passes (if it exists); the consistency checks in [`/audit-docs`](../.claude/skills/audit-docs/SKILL.md) pass |

- Source of the docs-only row: owner decision, 2026-11-16.

<a id="r-test-02"></a>
### R-TEST-02: Every published number is measured by a script in the repo

- Every number in the README Metrics table MUST come from a script in the repo. A number not measured yet MUST stay blank.
- Do not write an estimated number, because the project's claim is proof by measurement → leave it blank until a script measures it.
- Source: README, Metrics.
- ✅ "oversold: 0, measured by `<script path>`". ❌ "oversold: 0 (expected)".
- The values already in the README "After" column ("oversold: 0", "recorded once") are **targets** until a script measures them. A target MUST NOT be reported as a result. Source: owner decision, 2026-11-16.

## Web app

<a id="r-web-01"></a>
### R-WEB-01: No business logic in the web app

- `apps/web` MUST NOT contain business rules (stock checks, prices, fees, state transitions).
- Reason: rules in two places drift apart, and the API is where the invariants are protected → call the API through `packages/api-client`.
- Source: project brief.
- ✅ The web app shows the error the API returns when stock runs out.
- ❌ The web app computes the marketplace fee.

## Repo hygiene

<a id="r-repo-01"></a>
### R-REPO-01: Never edit a merged migration

- A migration that is merged MUST NOT be edited, because databases that already ran it will not run it again → add a new migration.
- Source: project brief.
- ✅ New migration that adds a column. ❌ Editing the old migration to add the column.

<a id="r-repo-02"></a>
### R-REPO-02: Never edit `.env*` files

- AI sessions MUST NOT edit any `.env*` file, because these files hold secrets and local settings → tell the owner which variable is needed and why.
- Source: project brief.
- ✅ "Add `X` to your `.env`: it is needed for Y." ❌ Writing a key into `.env`.

<a id="r-repo-03"></a>
### R-REPO-03: Never edit `packages/api-client/`

- `packages/api-client/` MUST NOT be edited by hand, because it is generated from OpenAPI and changes would be lost → change the API and regenerate (command: TODO (TM-repo-setup)).
- Source: project brief; README, Tech stack.
- ✅ Change the NestJS controller, regenerate the client. ❌ Fix a type in the generated client.

<a id="r-repo-04"></a>
### R-REPO-04: Never add a dependency without asking

- A new dependency MUST NOT be added without the owner's approval, because every dependency adds risk and upkeep for one developer → ask first, with the reason and any alternatives.
- Source: project brief.
- ✅ "May I add X for Y? Alternative: Z." ❌ Running `pnpm add` without asking.

## Docs, terms and language

<a id="r-doc-01"></a>
### R-DOC-01: Use GLOSSARY terms exactly

- Code, APIs, events, tables, docs and commits MUST use the terms in [GLOSSARY](GLOSSARY.md), never a forbidden synonym, because two names for one thing cause wrong code.
- Source: project brief.
- ✅ `Order`. ❌ `Purchase`, `Transaction` for an order.

<a id="r-doc-02"></a>
### R-DOC-02: Cite rules by ID

- When a change applies or touches a rule, the code comment, commit, PR or report MUST cite the rule ID.
- Reason (proposed by AI, owner to confirm): an ID lets a reviewer find the rule a change protects, and lets an audit find every place that depends on a rule when the rule changes.
- Alternative (proposed by AI, owner to confirm): do not only describe the effect ("prevents overselling") → name the rule ID next to it.
- Source: project brief.
- ✅ "Rejects the stock reservation when stock is short (R-INV-01)." ❌ "Prevents overselling."

<a id="r-doc-03"></a>
### R-DOC-03: All repo files are in plain English

- Every file in the repo (code, comments, commits, docs, skills) MUST be in plain English: short sentences, common words, no idioms.
- Vietnamese MAY appear only in the GLOSSARY "Vietnamese (spoken)" column and in the generated `docs/overview/system-tour.html` (its VI translation) → use the English term everywhere else. Source of the exception: owner decision, 2026-11-16.
- Reason (proposed by AI, owner to confirm): AI sessions and future readers read every file; short plain-English sentences leave less room for a wrong reading.
- Alternative (proposed by AI, owner to confirm): instead of an idiom or a Vietnamese word, write the plain English sentence and use the GLOSSARY term.
- Source: project brief.
- ✅ `// Release the stock reservation when it expires.` ❌ A comment in Vietnamese.

## Edge cases

- A rule here and a rule in a domain doc conflict → STOP and ask the owner. Do not pick one.
- A rule's source is changed (README edited, brief changed) → update the rule and its `Source` line in the same change.
