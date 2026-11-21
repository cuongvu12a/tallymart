---
status: draft
owner: Cuong Vu
last_verified: 2026-11-21
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

<a id="r-arch-02"></a>
### R-ARCH-02: A context owns its tables; other contexts use only its public interface

- Each context MUST own its tables, in its own Postgres schema. Code in another context MUST NOT read or write those tables, and MUST NOT import the context's internals; it calls the context's public interface.
- A lint rule (`eslint-plugin-boundaries`) MUST block imports into another context's internals, so the boundary is checked by a tool, not by memory.
- Reason: both invariants depend on one owner per piece of data. Only Inventory code may change Stock ([R-INV-01](domain/inventory.md#r-inv-01)); only Ledger code may write Ledger entries ([R-LED-01](domain/ledger.md#r-led-01)).
- Alternative: do not query another context's table for convenience → add a method to that context's public interface.
- Source: [Q-01](OPEN_QUESTIONS.md#q-01) decision (owner, 2026-11-21). Layout: [CONVENTIONS: Code layout](CONVENTIONS.md#code-layout).
- ✅ Ordering calls Inventory's public `reserve` method. ❌ Ordering runs `UPDATE inventory.stock ...`.

<a id="r-arch-03"></a>
### R-ARCH-03: Unlabeled arrows are in-process calls; only Payment → Ledger shares a DB transaction

- An unlabeled arrow in [ARCHITECTURE: Data flow](ARCHITECTURE.md#data-flow) MUST be an in-process call through the callee's public interface. A labeled arrow MUST be an event.
- A DB transaction MUST NOT span two contexts, except Payment → Ledger: recording a payment and writing its Ledger entries MAY share one DB transaction. An ADR records this exception.
- Reason: a caller needs some answers at once ("is there Stock?"), so those are calls. A payment without its Ledger entries would break [R-LED-01](domain/ledger.md#r-led-01), so that one pair is written atomically. Every other cross-context step that can fail is handled by Compensation ([R-ORD-02](domain/ordering.md#r-ord-02)).
- Alternative: do not wrap Ordering and Inventory in one shared DB transaction → call Inventory, and compensate if a later step fails.
- Source: [Q-02](OPEN_QUESTIONS.md#q-02) decision (owner, 2026-11-21).
- ✅ Payment records an IPN and its Ledger entries in one DB transaction. ❌ Ordering, Inventory and Payment all write in one DB transaction.

<a id="r-arch-04"></a>
### R-ARCH-04: Admin actions live in the owning context and are recorded in one Audit trail

- An Admin action MUST be implemented in the context that owns the data it changes, and MUST be recorded in the Audit trail in one shared format: who, what, when, the value before and after.
- Reason: keeping Admin actions in the owning context keeps rules like "only Ledger writes Ledger entries" true; one format lets every action be reviewed the same way.
- Alternative: do not build a separate back-office that writes other contexts' tables → call the owning context's public interface.
- Source: [Q-41](OPEN_QUESTIONS.md#q-41) decision (owner, 2026-11-21). Fraud tools are a [learning extension](PROJECT_OVERVIEW.md#learning-extensions).
- ✅ An Admin correction is a new pair of Ledger entries written by Ledger, with an Audit trail row. ❌ An Admin tool updates a Seller wallet row directly.

## HTTP API

<a id="r-api-01"></a>
### R-API-01: Every write API takes an `Idempotency-Key`

- Every API that changes state MUST accept an `Idempotency-Key` header. A repeated request with the same key MUST have the effect of exactly one request.
- Reason: a user who clicks "Place order" twice on a flaky network must not get two Orders or two Payments.
- Source: README, The problem.
- ✅ Two `POST` requests with the same key → one Order; the second response is the stored first response.
- ❌ Two `POST` requests with the same key → two Orders.

| Condition | Behavior |
|---|---|
| Same key, same body, first request finished | Return the stored response; no new effect |
| Same key, different body | 422 |
| Same key, first request still running | 409; the client retries later |
| Key missing on a write API | 400 |
| Key older than 24 hours | Treated as a new key |

- Storage: a Postgres table with a unique `(user, endpoint, key)` row, the request hash and the stored response, inserted in the same DB transaction as the business write. A cleanup job removes rows older than the TTL. Redis MAY be added later as a fast first check, never as the only one.
- IPNs and carrier webhooks do not send the header. The endpoint derives the key from the provider's ID and uses the same table; a repeat gets the stored first reply ([R-PAY-01](domain/payment.md#r-pay-01)).
- Source of the behavior: [Q-04](OPEN_QUESTIONS.md#q-04) decision (owner, 2026-11-21).

<a id="r-api-02"></a>
### R-API-02: Errors use Problem Details with a stable `code`

- Every error response MUST be RFC 9457 Problem Details (`application/problem+json`: `type`, `title`, `status`, `detail`) plus a stable, machine-readable `code` field.
- Status codes: 400 validation, 401 not signed in, 403 no permission, 404 not found, 409 a Stock or state conflict or an `Idempotency-Key` still in progress, 422 an `Idempotency-Key` reused with a different body, 429 rate limited.
- Reason: the client must tell "retry is safe" apart from "do not retry", and a stable `code` makes that testable. One format also lets the generated client type every error.
- Alternative: do not return the framework's default error body or a free-text message → return Problem Details with a `code`.
- Source: [Q-03](OPEN_QUESTIONS.md#q-03) decision (owner, 2026-11-21).
- ✅ `409 {"type": "...", "title": "Not enough Stock", "status": 409, "code": "STOCK_NOT_ENOUGH"}` · ❌ `500 {"message": "error"}`

## Events

<a id="r-evt-01"></a>
### R-EVT-01: A DB change and its event MUST NOT diverge

- When a DB write must produce an event, the event MUST be recorded through a Transactional Outbox in the same DB transaction.
- The Outbox is built with the first cross-context event ([Q-26](OPEN_QUESTIONS.md#q-26) decision, owner, 2026-11-21).
- Do not publish to the broker directly after the commit, because the publish can fail after the commit → write to the outbox, and let a relay publish it.
- Reason: "order paid but nobody ships it".
- Source: README, The problem.
- ✅ Order status update and outbox row in one transaction; a relay publishes `OrderPaid`.
- ❌ `commit()` then `broker.publish()`; the process crashes between them.

<a id="r-evt-02"></a>
### R-EVT-02: A consumer that touches money, Stock or e-invoices uses an inbox

- Events are delivered at least once, so a consumer can see the same event twice. A handler that changes money, Stock or e-invoices MUST record the event ID in an inbox table in the same DB transaction as its change, and skip an event ID it has already processed.
- A notification handler MAY rely on its own state instead (natural idempotency).
- After its retries run out, a message goes to the DLQ. Retry counts are set after measurement.
- Reason: a repeated `Delivered` must not pay a Seller twice; an inbox makes "one event, one effect" testable the same way for every money handler.
- Alternative: do not rely on each money handler inventing its own duplicate check → use the inbox.
- Source: [Q-27](OPEN_QUESTIONS.md#q-27) decision (owner, 2026-11-21).
- ✅ `Delivered` arrives twice → one Money release. ❌ `Delivered` arrives twice → two Money releases.

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

<a id="r-test-03"></a>
### R-TEST-03: Each kind of change needs its test level

- A change to code MUST come with the tests its kind needs, from the table below. A test that proves a rule MUST name the rule ID in its test name.
- Reason: the invariants are only proven by the right kind of test; a unit test with mocks cannot show an Oversell under concurrent requests. Rule IDs in test names let [`/audit-docs`](../.claude/skills/audit-docs/SKILL.md) find where each rule is enforced.
- Alternative: do not count a unit test with a mocked DB as proof for stock or Ledger code → write the concurrency test against a real DB.
- Source: [Q-10](OPEN_QUESTIONS.md#q-10) decision (owner, 2026-11-21).

| Change | Required tests |
|---|---|
| A rule with an ID | A unit test whose name contains the rule ID |
| DB or messaging code | An integration test with Testcontainers |
| Anything that touches Stock or the Ledger | A concurrency test that proves [R-INV-01](domain/inventory.md#r-inv-01) or [R-LED-01](domain/ledger.md#r-led-01) |
| An external integration | A test with the Fake implementation, including duplicates and timeouts |

- ✅ `it("R-INV-01: 50 concurrent reservations on Stock 10 never oversell")` · ❌ `it("works")`

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
- Vietnamese MAY appear only in the GLOSSARY "Vietnamese (spoken)" column, in the generated `docs/overview/system-tour.html` (its VI translation), and in [docs/learning-notes/](learning-notes/README.md) (study notes for the owner; GLOSSARY terms stay in English) → use the English term everywhere else. Source of the exceptions: owner decisions, 2026-11-16 and 2026-11-21.
- Reason (proposed by AI, owner to confirm): AI sessions and future readers read every file; short plain-English sentences leave less room for a wrong reading.
- Alternative (proposed by AI, owner to confirm): instead of an idiom or a Vietnamese word, write the plain English sentence and use the GLOSSARY term.
- Source: project brief.
- ✅ `// Release the stock reservation when it expires.` ❌ A comment in Vietnamese.

## Edge cases

- A rule here and a rule in a domain doc conflict → STOP and ask the owner. Do not pick one.
- A rule's source is changed (README edited, brief changed) → update the rule and its `Source` line in the same change.
