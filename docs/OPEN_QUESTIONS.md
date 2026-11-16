---
status: draft
owner: Cuong Vu
last_verified: 2026-11-16
applies_to: [backend, web, repo, docs]
related_code: []
---

# Open questions

The only place where undecided questions, their options and their analysis live. Other docs hold one line that links here.

- **★** = MUST be answered before the first module is built. The ★ questions come first, then the rest in [build order](PROJECT_OVERVIEW.md#build-order).
- A **Recommendation** is advice, not a decision. MUST NOT be written into another doc as a fact, and MUST NOT be built on until the owner fills in **Decision**.
- `(unverified)` marks a technical claim that has not been checked against an official source.
- IDs are stable and never reused. How to add or close a question: [docs/README: Open questions](README.md#open-questions).
- "Solo cost" = how hard the option is for one developer to build and maintain.
- `product` = raised by product discovery ([product/EPICS.md](product/EPICS.md)). These questions decide scope, not implementation.

## Summary

| ID | ★ | Question | Affected docs | Status |
|---|---|---|---|---|
| [Q-01](#q-01) | ★ | Folder layout, boundaries and table ownership in `apps/api` | RULES, ARCHITECTURE, CONVENTIONS | open |
| [Q-02](#q-02) | ★ | How contexts call each other | ARCHITECTURE, inventory, ledger, ordering, payment, reconciliation | open |
| [Q-03](#q-03) | ★ | API error format and status codes | RULES, CONVENTIONS, identity | open |
| [Q-04](#q-04) | ★ | `Idempotency-Key` behavior and storage | RULES, ARCHITECTURE, PROJECT_OVERVIEW, decisions/README, payment | open |
| [Q-05](#q-05) | ★ | Can one order hold products from several sellers? | GLOSSARY, product/EPICS, ordering, shipping | open |
| [Q-06](#q-06) | ★ | Roles, token lifetime, admin powers | PROJECT_OVERVIEW, GLOSSARY, product/EPICS, identity | open |
| [Q-07](#q-07) | ★ | Non-goals | PROJECT_OVERVIEW, CLAUDE.md | open |
| [Q-08](#q-08) | ★ | Branch names, commit format, PR flow | CONVENTIONS | open |
| [Q-09](#q-09) | ★ | Approve the build order; which module is first | PROJECT_OVERVIEW, CLAUDE.md, product/EPICS, catalog, start-spec skill | open |
| [Q-10](#q-10) | ★ | Lint, format and test tooling; test levels for "done" | CONVENTIONS, CLAUDE.md | open |
| [Q-11](#q-11) | | Seller eKYC: required before what? | GLOSSARY, product/EPICS, identity | open |
| [Q-12](#q-12) | | Currency and money storage | CONVENTIONS, GLOSSARY, product/EPICS, catalog, ledger | open |
| [Q-13](#q-13) | | What is a variant; where do price and stock live? | PROJECT_OVERVIEW, GLOSSARY, product/EPICS, catalog, inventory | open |
| [Q-14](#q-14) | | Stock reservation lifecycle and TTL | GLOSSARY, product/EPICS, inventory, ordering, invariant-test skill | open |
| [Q-15](#q-15) | | DB-level locking strategy for stock | product/EPICS, inventory | open |
| [Q-16](#q-16) | | Per-user rate limit values and algorithm | product/EPICS, inventory | open |
| [Q-17](#q-17) | | What exactly is a flash sale? | GLOSSARY, product/EPICS, inventory | open |
| [Q-18](#q-18) | | Ledger accounts | GLOSSARY, product/EPICS, ledger, invariant-test skill | open |
| [Q-19](#q-19) | | Marketplace fee rate and timing | GLOSSARY, product/EPICS, ledger | open |
| [Q-20](#q-20) | | Successful delivery, return window, withdrawal rules | GLOSSARY, product/EPICS, ledger | open |
| [Q-21](#q-21) | | Payment method → provider mapping | GLOSSARY, product/EPICS, payment | open |
| [Q-22](#q-22) | | Re-query schedule and payment timeout | GLOSSARY, product/EPICS, ordering, payment | open |
| [Q-23](#q-23) | | Refund flow and ledger entries | product/EPICS, ledger, payment | open |
| [Q-24](#q-24) | | Order states and transitions | ARCHITECTURE, GLOSSARY, product/EPICS, ordering, shipping | open |
| [Q-25](#q-25) | | Checkout saga steps and compensation | ARCHITECTURE, GLOSSARY, product/EPICS, ordering, payment | open |
| [Q-26](#q-26) | | Outbox with the first event, or later? | RULES, ARCHITECTURE, PROJECT_OVERVIEW, decisions/README | open |
| [Q-27](#q-27) | | Retries, DLQ, consumer deduplication | RULES, ARCHITECTURE, invoicing, ledger, notification | open |
| [Q-28](#q-28) | | Shipment event key and state machine | product/EPICS, ordering, shipping | open |
| [Q-29](#q-29) | | Which events notify whom, on which channel | ARCHITECTURE, product/EPICS, notification | open |
| [Q-30](#q-30) | | Who issues e-invoices, for what, and when | ARCHITECTURE, product/EPICS, invoicing | open |
| [Q-31](#q-31) | | Reconciliation sources and mismatch handling | ARCHITECTURE, GLOSSARY, product/EPICS, reconciliation | open |
| [Q-32](#q-32) | | Performance targets per capability | PROJECT_OVERVIEW | open |
| [Q-33](#q-33) | | `product` When does Seller money become available for Withdrawal? | — | merged into [Q-20](#q-20) |
| [Q-34](#q-34) | | `product` Who decides a Refund for a Return, and how fast? | product/EPICS, payment | open |
| [Q-35](#q-35) | | `product` Is cash on delivery (COD) in scope? | GLOSSARY, product/EPICS, ledger, payment, reconciliation | open |
| [Q-36](#q-36) | | `product` Engagement and revenue features: in, later, or out? | GLOSSARY, product/EPICS | open |
| [Q-37](#q-37) | | `product` After-sales exceptions: in scope, and which context owns them? | ARCHITECTURE, GLOSSARY, product/EPICS, ordering, shipping | open |
| [Q-38](#q-38) | | `product` Is there a Seller handling step between payment and Shipment? | GLOSSARY, product/EPICS, ordering, shipping | open |
| [Q-39](#q-39) | | `product` Vietnam compliance scope: Seller tax withholding, personal data | GLOSSARY, product/EPICS, identity, invoicing, ledger | open |
| [Q-40](#q-40) | | `product` Bulk product import and multi-channel stock sync: in scope? | product/EPICS, catalog, inventory | open |
| [Q-41](#q-41) | | `product` Admin back-office, audit trail and fraud tools: scope and home | ARCHITECTURE, GLOSSARY, product/EPICS, identity | open |
| [Q-42](#q-42) | | `product` Reporting: Seller statement, Seller reports, finance reports | GLOSSARY, product/EPICS, ledger | open |
| [Q-43](#q-43) | | Does checkout need a Shipping quote before payment? | ARCHITECTURE, PROJECT_OVERVIEW, product/EPICS, ordering, shipping | open |
| [Q-44](#q-44) | | `product` Stuck-state detection: in scope, and where does it live? | product/EPICS | open |
| [Q-45](#q-45) | | How do epics and enabling work become the plan? | PROJECT_OVERVIEW, docs/README, product/EPICS | open |
| [Q-46](#q-46) | | In the flash-sale test, is underselling a failure? | inventory, invariant-test skill | open |
| [Q-47](#q-47) | | `product` How does a Withdrawal move money to the Seller's bank? | ARCHITECTURE, product/EPICS, ledger | open |
| [Q-48](#q-48) | | Which file owns the doc process? | docs/README | open |

---

## ★ Before the first module

<a id="q-01"></a>
### Q-01: Folder layout, boundaries and table ownership in `apps/api` ★

**Status:** open

**Context.** The README says "modular monolith, split by bounded context" and plans to extract some contexts later ([R-ARCH-01](RULES_AND_CONSTRAINTS.md#r-arch-01)). Without clear boundaries, contexts read each other's tables. Then extraction becomes impossible, and the invariants can be broken from code outside Inventory or Ledger. This decides every file path, and every `related_code` entry.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. One NestJS module per context, with layers inside | `apps/api/src/modules/<context>/` with `domain/`, `application/`, `infrastructure/`, `api/`. Each context exports a small public interface. Each context owns its tables (one Postgres schema per context). A lint rule blocks imports into another context's internals | Clear boundaries; easy to extract later; rules sit in pure domain code that is easy to test | More folders and files per feature | Medium | Low: only Inventory code can change stock; only Ledger code can write entries |
| B. One flat NestJS module per context | `modules/<context>/` with controller, service, repository files. Shared tables allowed | Least code; standard NestJS style | Boundaries hold only by discipline; business rules mix with framework code | Low | Medium: any module can update stock or ledger tables directly |
| C. One pnpm package per context | `packages/<context>` with its own `package.json`; `apps/api` wires them | Strongest boundaries (enforced by package dependencies) | Build and tooling overhead; slower changes across contexts | High | Low |

**Recommendation.** A. Both invariants depend on one owner per piece of data, so "only Inventory writes stock, only Ledger writes entries" must be enforced by a tool, not by memory. A also keeps rules in plain TypeScript, so unit tests run with no DB or NestJS. Keep the layers thin; do not add a layer that has nothing in it. A boundary lint rule needs a dependency, so it needs approval ([R-REPO-04](RULES_AND_CONSTRAINTS.md#r-repo-04)); for example `eslint-plugin-boundaries` or `dependency-cruiser` (unverified fit). **Would change it:** if you want the least structure while the domain model is still unclear, choose B, and plan a move to A before Payment and Ledger.

**Decision:** _pending_

<a id="q-02"></a>
### Q-02: How contexts call each other ★

**Status:** open

**Context.** The README diagram labels some arrows as events (`OrderPaid`, `Delivered`). The other four arrows have no label: Ordering → Inventory, Ordering → Payment, Payment → Ledger, Reconciliation → Ledger ([ARCHITECTURE: Data flow](ARCHITECTURE.md#data-flow)). This choice decides whether "reserve stock" and "write ledger entries" happen inside the same DB transaction as the caller's change. That matters for both invariants.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Unlabeled = in-process call; labeled = event | Ordering calls Inventory's public interface and gets an answer at once. Reactions after the fact go through events | Simple; fast; easy to debug; matches the diagram labels (unverified reading of the diagram) | Callers are coupled to the callee's interface | Low | Low, if each call has a clear transaction boundary |
| B. Everything is an event | All cross-context work is asynchronous | Loose coupling; ready for extraction | Hard to answer "is there stock?" before the user leaves the page; many more failure paths | High | Medium: more places where state can diverge |
| C. A per-arrow decision | Decide each arrow alone | Most precise | Needs analysis now, with no code | Medium | Depends |

A related choice for A: can one DB transaction cover two contexts (for example the Payment and Ledger writes)? Sharing a transaction is simpler and keeps R-LED-01 atomic. It also couples the two contexts' tables, and it breaks once a context is extracted.

**Recommendation.** A. Allow a shared transaction only for Payment → Ledger, and record it in an ADR, because recording a payment without its ledger entries breaks R-LED-01. **Would change it:** an early plan to extract Payment or Ledger. Then choose events with an outbox ([Q-26](#q-26)).

**Decision:** _pending_

<a id="q-03"></a>
### Q-03: API error format and status codes ★

**Status:** open

**Context.** Every endpoint, the generated client and the web app depend on one error format. Stock conflicts, idempotency conflicts and invalid state transitions each need an error code the client can read. The README says nothing about this.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. RFC 9457 Problem Details | `application/problem+json` with `type`, `title`, `status`, `detail`, plus a stable `code` field | A standard; OpenAPI tools understand it (unverified for the chosen generator) | A little more setup | Low | None |
| B. Own envelope | `{ "error": { "code", "message", "details" } }` | Simple; full control | Not a standard; you design every field | Low | None |
| C. NestJS default | Built-in exception format | Nothing to build | No stable error codes; hard to type in the client | Very low | None directly; clients may retry wrongly |

Status codes to fix whichever option is chosen: validation 400, not signed in 401, no permission 403, not found 404, state or stock conflict 409, idempotency conflicts (see [Q-04](#q-04)), rate limited 429.

**Recommendation.** A, with a stable machine-readable `code` (for example `STOCK_NOT_ENOUGH`, `INVALID_TRANSITION`). Clients must tell "retry is safe" apart from "do not retry", and stable codes make that testable. **Would change it:** if the client generator cannot type Problem Details well, choose B with the same fields.

**Decision:** _pending_

<a id="q-04"></a>
### Q-04: `Idempotency-Key` behavior and storage ★

**Status:** open

**Context.** [R-API-01](RULES_AND_CONSTRAINTS.md#r-api-01) is in the README, but not how it works. If the key check and the business write are not atomic, two parallel requests with the same key can both run, which means two orders and two stock reservations (risk to R-INV-01). The first write API needs this.

**Options (storage)**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Postgres table in the same transaction | Unique `(user, key)` row, with a request hash and the stored response, inserted in the same transaction as the business write | Atomic with the change; survives a Redis loss | A DB row per write; needs a cleanup job | Medium | Lowest |
| B. Redis `SET NX` + TTL | Lock and cached response in Redis | Fast; TTL is built in | Not atomic with the DB; a Redis restart loses keys, and repeats run again | Low | Medium |
| C. Only natural uniqueness per endpoint | Unique constraints (for example one order per cart) | No generic mechanism | Not every write has a natural key; R-API-01 says every write API | Low | Medium |

**Behavior to fix whichever storage is chosen**

| Condition | Proposed behavior (unverified against the IETF draft "The Idempotency-Key HTTP Header Field") |
|---|---|
| Key missing on a write API | 400 |
| Same key, same body, finished | Return the stored response; no new effect |
| Same key, different body | 422 |
| Same key, first request still running | 409; the client retries later |
| Key older than the TTL | Treated as new. TTL to decide: 24 hours is common (unverified) |
| Key scope | Per user + per endpoint |

**IPNs and carrier webhooks.** They are write endpoints, but the provider does not send our header. The README asks for an `Idempotency-Key` on every write API and for carrier updates to be deduplicated "by event key" (README, The problem). Which key a carrier update uses is [Q-28](#q-28).

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| W1. Exempt them from the header | IPNs deduplicate by the gateway's transaction ID, carrier updates by the event key; R-API-01 names this exception | No extra mechanism | R-API-01 gets an exception; two dedup paths | Low | Low if each path is tested |
| W2. Derive a key inside the endpoint | The endpoint builds an Idempotency key from the provider's ID and uses the same storage as option A above | R-API-01 holds with no exception; one mechanism | The key is not sent by a client, so the header name is a stretch | Low | Lowest |

Also decide: what the endpoint replies to a repeat. Gateways usually resend until they get a success reply (unverified), so a repeat may need the same reply as the first call ([R-PAY-01](domain/payment.md#r-pay-01)).

Recommendation for IPNs and webhooks: W2, replying to a repeat with the stored first reply. **Would change it:** a provider whose IDs are not unique per event.

**Recommendation.** A. Correctness matters more than speed here, and only the same DB transaction guarantees "one key, one effect" even after a crash. Redis MAY be added later as a fast first check, never as the only one. **Would change it:** none expected. If measurements show the table is a bottleneck, keep A and add the Redis check.

**Decision:** _pending_

<a id="q-05"></a>
### Q-05: Can one order hold products from several sellers? ★

**Status:** open

**Context.** The README says "multi-vendor" and "pays the seller after successful delivery". Shipping, the marketplace fee, paying the seller, and refunds all depend on how orders map to sellers. This shapes the first ERD, and changing it later means migrating money data (R-LED-01, R-LED-02).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Cart limited to one seller | A buyer can check out products of one seller at a time | Simplest; one order = one seller = one shipment = one payment | Poor experience for buyers | Low | Lowest |
| B. Checkout splits into one order per seller; one payment covers them | Checkout with N sellers creates N orders and one payment | Common marketplace pattern (unverified for VN marketplaces); paying the seller and shipping stay per order | Partial failures (one seller's stock runs out); refunds of part of a payment | High | Medium: more paths where money and stock must stay matched |
| C. One order with lines from many sellers | Split per seller only at shipping and when paying the seller | One order for the buyer | State machine, fee and paying the seller become per line; complex | Very high | High |

**Recommendation.** Model "each order belongs to exactly one seller" from day one. Build A first, and add B later as a parent record over orders. B then needs no change to the order, shipment or ledger model. Both invariants are easier to prove when each order has one seller. **Would change it:** if multi-seller checkout is a goal for the first demo, build B directly.

**Decision:** _pending_

<a id="q-06"></a>
### Q-06: Roles, token lifetime, admin powers ★

**Status:** open

**Context.** The README names buyers, sellers and admins, JWT, RBAC, and a later move to Keycloak. Identity is likely the first module ([Q-09](#q-09)). Rules for every other context depend on who may do what ([R-IDN-01](domain/identity.md#r-idn-01)).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. One user, many roles; short access token + rotating refresh token | A user can be buyer and seller. Access JWT about 15 minutes; refresh token stored in the DB and rotated on each use | Normal practice; refresh can be revoked; maps to Keycloak later (unverified mapping effort) | Refresh token table and rotation logic | Medium | None |
| B. Separate account types; long-lived JWT | Buyer and seller are different accounts; token valid for days | Very simple | Cannot revoke a token; a seller who also buys needs two accounts | Low | Indirect: a stolen token can request withdrawals |
| C. Server sessions (cookies) | Session in Redis or the DB | Easy to revoke | Does not match the README (JWT) | Medium | None |

Admin powers to list: approve sellers, approve withdrawals, see reconciliation reports, issue refunds. These are candidates only. The wider back-office scope (queues, audit trail, fraud tools) is [Q-41](#q-41).

**Ownership checks.** RBAC answers "may a Seller edit Products?", not "may this Seller edit this Product?". Also decide whether business code may check ownership (a Seller acts only on their own Products, Orders and Seller wallet), and where that check lives: in each module, or in one shared guard. The README says only "RBAC authorization".

**Recommendation.** A. Revocable tokens matter once Withdrawals exist, and one account with many roles is what the RBAC in the README implies. **Would change it:** if Keycloak is moved earlier, use its tokens and skip the refresh-token table.

**Decision:** _pending_

<a id="q-07"></a>
### Q-07: Non-goals ★

**Status:** open

**Context.** The README lists no non-goals. Without them, AI sessions add features nobody asked for. A non-goal list also protects the main goal: correctness, not feature count.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Short explicit list | The owner picks from candidates such as: native mobile apps; a production launch; seller storefront design; recommendation features. Asked in their own questions, not here: currency ([Q-12](#q-12)), cash on delivery ([Q-35](#q-35)), Vouchers, ads and sponsored placement ([Q-36](#q-36)). Not a candidate: real money in tests and CI (the README uses sandboxes and staging only). Still a candidate: a production launch | Clear scope; AI sessions can say no | Must be kept up to date | Low | Lowers risk: fewer money paths |
| B. No list; decide case by case | Scope grows by request | Flexible | Scope creep | Low | Higher |

**Recommendation.** A. Each candidate is a guess and needs the owner's choice. Money-path candidates are decided in [Q-35](#q-35) and [Q-36](#q-36). **Would change it:** nothing; only the list contents are open.

**Decision:** _pending_

<a id="q-08"></a>
### Q-08: Branch names, commit format, PR flow ★

**Status:** open

**Context.** Default branch is `main` (decided). Commits must link to `TM-xx` issues, so history explains why code changed. With one developer and AI sessions, a PR is also the place where CI checks R-TEST-01 before a merge.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Short-lived branches + PR + squash merge | Branch `tm-12-reserve-stock`; PR to `main`; CI must pass; squash merge with title `feat(inventory): reserve stock with TTL (TM-12)` | CI gates every change; one commit per work item; easy to revert | A few more steps per change | Low | Lower: tests run before merge |
| B. Commit straight to `main` | Small commits with `TM-12: ...` | Fastest | No gate before code lands; harder to revert one feature | Very low | Higher |
| C. Git flow (develop, release branches) | Long-lived branches | Release control | Too heavy for one developer | High | None |

**Recommendation.** A, with Conventional Commits types (`feat`, `fix`, `docs`, `test`, `refactor`, `chore`) and the `TM-xx` ID in every PR title. Concurrency tests only protect the invariants if they run before code reaches `main`. **Would change it:** if CI does not exist yet, B is acceptable until TM-repo-setup adds CI.

**Decision:** _pending_

<a id="q-09"></a>
### Q-09: Approve the build order; which module is first ★

**Status:** open

**Context.** The owner asked for work to follow module dependencies, not the README dates. The proposed graph is in [PROJECT_OVERVIEW: Build order](PROJECT_OVERVIEW.md#build-order). The ordering choices the README does NOT back are listed once, in the "Needs (not backed up)" column of that table. A Shipping quote at checkout would add one more ([Q-43](#q-43)).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Strict dependency order | Identity → Catalog → Inventory → Ledger → Payment → Ordering → events → Shipping, Notification → Invoicing; Reconciliation after Ledger | Each module is built on real neighbors; no throwaway code | The first end-to-end checkout comes late | Low | Lowest: Ledger exists before any money moves |
| B. Walking skeleton | Build a thin Ordering early, against fake Inventory and Payment ports; replace the fakes one by one | End-to-end flow early; shows integration problems early | Fakes of internal modules are extra code; money paths exist before the Ledger | Medium | Medium: payments without a ledger for a while |
| C. Follow the README roadmap order | Ordering before Inventory and Payment; Ledger later | Matches the README | Ignores the diagram; money moves before the ledger exists | Medium | High for R-LED-01 |

Cross-cutting pieces: build ports with fakes with the first external system (Payment, or Identity if Google OAuth comes first). Build `Idempotency-Key` with the first write API that a buyer can repeat.

**Recommendation.** A. Building the Ledger before Payment means no money is ever recorded outside the double-entry ledger, which protects R-LED-01 from the first payment. Identity first is a convenience choice, because every other context needs users. Catalog can start right after it. **Would change it:** if an early demo of checkout matters more, use B, but keep Payment behind its fake until the Ledger exists.

**Decision:** _pending_

<a id="q-10"></a>
### Q-10: Lint, format and test tooling; test levels for "done" ★

**Status:** open

**Context.** [R-TEST-01](RULES_AND_CONSTRAINTS.md#r-test-01) says a task is done only when tests and lint pass. The README names Jest, Testcontainers, WireMock, Playwright, k6 and Toxiproxy, but no lint or format tool. Every tool is a dependency, so the owner must approve it ([R-REPO-04](RULES_AND_CONSTRAINTS.md#r-repo-04)).

**Options (lint and format)**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. ESLint + Prettier | Common pair; the NestJS starter project uses them (unverified for the current NestJS version) | Large rule ecosystem, including boundary rules ([Q-01](#q-01)) | Two tools, slower | Low | None |
| B. Biome | One tool for lint and format | Fast; one config | Fewer plugins; boundary rules may need another tool (unverified) | Low | None |

**Test levels a task needs to be done (proposal)**

| Change | Required tests |
|---|---|
| A rule with an ID | A unit test that names the rule ID |
| DB or messaging code | An integration test with Testcontainers |
| Anything that touches stock or ledger | A concurrency test that proves R-INV-01 or R-LED-01 |
| An external integration | A test with the fake implementation, including duplicates and timeouts |

**Recommendation.** A plus the test levels above, plus a type check. A fits best with the boundary lint rule recommended in Q-01. Tests named after rule IDs make `/audit-docs` able to find where each rule is enforced. **Would change it:** if Q-01 chooses `dependency-cruiser` for boundaries, B becomes equally good.

**Decision:** _pending_

---

## Identity

<a id="q-11"></a>
### Q-11: Seller eKYC: required before what?

**Status:** open

**Context.** The README lists FPT.AI OCR for seller eKYC, but not when it is required. Money leaves the marketplace only through a Withdrawal, so eKYC is mostly a money-safety control.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Before listing products | A seller cannot sell until verified | Strongest control | Blocks Catalog work on an external integration | Medium | None |
| B. Before the first withdrawal | Selling is open; withdrawal needs eKYC | Catalog is not blocked; protects the money exit | Unverified sellers can sell | Medium | None |
| C. Not in the core | Added later | Least work | No control on money leaving | Low | None to the invariants; risk of fraud |

**Recommendation.** B. It protects the only path where money leaves, and it does not block early modules. Legal requirements in Vietnam for marketplace sellers are not checked (unverified). **Would change it:** a legal requirement to verify sellers before they sell.

**Decision:** _pending_

## Catalog

<a id="q-12"></a>
### Q-12: Currency and money storage

**Status:** open

**Context.** Prices, payments, fees and ledger entries all store money. A rounding error breaks R-LED-01 because entries would no longer sum to exactly 0. The README names VN providers and Stripe, but no currency.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Integer in the smallest unit + currency code; VND only | `bigint` column plus `currency` column; in TypeScript a `bigint` or a small Money type; in JSON a string | Exact; no rounding; VND has no minor unit in ISO 4217 (unverified) | Must convert at the API edge | Low | Lowest |
| B. `numeric(19,4)` decimal | Decimal column; a decimal library in TypeScript | Supports fractions | Needs a library (dependency); easy to mix with JS `number` | Medium | Low if used everywhere |
| C. JS `number` (float) | Plain numbers | No work | Float rounding errors | Very low | High: sums may not be exactly 0 |

**Recommendation.** A. Integers make "sum of entries = 0" exact, and a currency column costs nothing now and avoids a migration if Stripe needs another currency later. Fees in percent must define one rounding rule ([Q-19](#q-19)). **Would change it:** a real need for more than one currency in the core.

**Decision:** _pending_

<a id="q-13"></a>
### Q-13: What is a variant; where do price and stock live?

**Status:** open

**Context.** The README says "Products, variants, prices" for Catalog and "Stock" for Inventory. Where stock lives decides the row that R-INV-01 locks.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Every product has at least one variant; price and stock are per variant | A product without options has one default variant | One code path; stock row = variant | An extra row for simple products | Low | Low |
| B. Price per product, stock per variant | Variants differ only in stock | Simpler prices | Cannot price sizes differently | Low | Low |
| C. No variants in the core | Product = sellable unit | Simplest | A migration when variants come | Very low | Low now, migration risk later |

**Recommendation.** A. One sellable unit with one stock row keeps the locking design in Q-15 simple and the same for every product. **Would change it:** a decision to keep the core very small (C).

**Decision:** _pending_

## Inventory

<a id="q-14"></a>
### Q-14: Stock reservation lifecycle and TTL

**Status:** open

**Context.** [R-INV-03](domain/inventory.md#r-inv-03) says reservations have a TTL. The README does not say when they start, how long they last, or what happens when payment arrives after expiry. This is where R-INV-01 meets external failures.

**Options (when the reservation is made)**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. When adding to cart | Stock is reserved while the Product is in the Cart | Buyer is sure to get it | Carts block stock; easy to abuse in a flash sale | Medium | Low, but poor stock use |
| B. When the order is placed, before payment | Reserve at checkout; becomes a final deduction when paid; released on expiry or failure | Common pattern; stock is reserved only while paying | Needs an expiry job | Medium | Low |
| C. Only when paid | No reservation; deduct on payment | Simplest | A buyer pays and then finds no stock → refund | Low | Low for stock, but forces refunds |

**Details to fix**

| Item | Proposal |
|---|---|
| TTL | At least as long as the payment window, so a buyer who pays in time always has the stock. The VNPay payment URL expiry time (about 15 minutes) is unverified |
| Expiry | A scheduled job releases expired reservations with a conditional update, so a release and a payment cannot both win |
| Payment after expiry | Try to reserve again. If there is no stock, refund automatically ([Q-23](#q-23)) |

**Recommendation.** B with the details above. Reserving at checkout is the smallest window that still guarantees stock to a buyer who pays in time. The late-payment rule closes the main hole between R-INV-01 and external delays. **Would change it:** if flash sales are the main case, keep B but give each flash sale its own short TTL ([Q-17](#q-17)).

**Decision:** _pending_

<a id="q-15"></a>
### Q-15: DB-level locking strategy for stock

**Status:** open

**Context.** [R-INV-02](domain/inventory.md#r-inv-02) says the DB stops overselling. The README metric is 50 concurrent requests on stock 10 → oversold 0.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. `SELECT ... FOR UPDATE` then update | Lock the stock row, check, write, commit | Easy to read; the check can be complex | Holds a row lock during app logic; slow under a flash sale | Low | Low |
| B. Single conditional update | `UPDATE ... SET available = available - n WHERE id = ? AND available >= n`; zero rows changed = not enough stock | Atomic; shortest lock time | The check must fit in SQL | Low | Lowest |
| C. Optimistic version column | Read version, update `WHERE version = ?`, retry on conflict | No lock held | Many retries on a hot row | Medium | Low, but can starve under load |
| D. Redis atomic counter in front of the DB | Lua script decrements in Redis; DB updated after | Very fast | Two sources of truth; Redis loss can oversell | High | High unless the DB still checks |

In every option, add a DB `CHECK (available >= 0)` constraint as a second guard.

**Recommendation.** B plus the CHECK constraint. It is the simplest option that is correct by construction, and it is easy to prove with the README concurrency test. Add D only as a filter in front of B, and only when a measurement shows the hot row is a bottleneck. **Would change it:** a measured lock-contention problem that B cannot handle.

**Decision:** _pending_

<a id="q-16"></a>
### Q-16: Per-user rate limit values and algorithm

**Status:** open

**Context.** [R-INV-04](domain/inventory.md#r-inv-04) requires per-user rate limiting in flash sales. It protects capacity and fairness, not the invariant.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Fixed window in Redis | Count per user per minute | Simple | Bursts at window edges | Low | None |
| B. Token bucket or sliding window in Redis | Smooth limit with a burst size | Fair; standard | A little more logic | Low | None |
| C. In memory per instance | Counter in the process | No Redis | Wrong with more than one API instance | Very low | None |

**Recommendation.** B in Redis. Set the numbers (for example requests per user per flash sale per minute) after a k6 load test, not before. If Redis is down, the system SHOULD still serve requests, because the DB still protects R-INV-01. **Would change it:** nothing in the algorithm; the values wait for measurement.

**Decision:** _pending_

<a id="q-17"></a>
### Q-17: What exactly is a flash sale?

**Status:** open

**Context.** The README names flash sales as the main overselling risk but does not define them.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Time window + special price + own stock pool + per-user quantity cap | Stock for the sale is set aside from normal stock | Normal sales unaffected; the hot row is isolated; clear rules | More model and admin work | Medium | Low |
| B. Time window + special price on normal stock | Only the price changes | Simple | Normal buyers compete with the sale on one row | Low | Low (same lock), worse performance |

**Recommendation.** A. A separate stock pool makes the concurrency test match the README example exactly (stock 10, 50 buyers), and keeps a sale from blocking normal orders. **Would change it:** if flash sales are only a load-test scenario and not a product feature, use B.

**Decision:** _pending_

## Ledger

<a id="q-18"></a>
### Q-18: Ledger accounts

**Status:** open

**Context.** The README lists seller wallets, marketplace fees and withdrawals, and says the marketplace holds the money until delivery. A double-entry ledger needs a fixed list of account types to post against (R-LED-01, R-LED-03).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Small fixed set | Gateway clearing (money the gateway owes us); per-seller pending (paid, not yet delivered); per-seller available (seller wallet); marketplace fee revenue; refunds payable; bank | Covers every README money flow; pending vs available shows R-LED-03 | Needs a short design | Medium | Lowest |
| B. One account per seller | One seller wallet amount, nothing else | Very simple | Cannot express "held until delivery"; fees have no account | Low | High: entries cannot balance correctly |
| C. Full chart of accounts | General accounting standard | Complete | Far more than needed | High | Low |

Also decide: every money movement is one group of entries that sums to 0 itself, checked in the DB or in one write function (unverified best mechanism: a deferred constraint trigger vs a single insert function).

**Recommendation.** A. It is the smallest set that makes R-LED-01 and R-LED-03 checkable: "available" money can only come from "pending" after successful delivery ([Q-20](#q-20)). **Would change it:** cash on delivery ([Q-35](#q-35)) or Vouchers ([Q-36](#q-36)) being in scope, which need more accounts.

**Decision:** _pending_

<a id="q-19"></a>
### Q-19: Marketplace fee rate and timing

**Status:** open

**Context.** The README says the marketplace "deducts its fee" but gives no rate or timing.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. One percentage for all orders, stored on each order when it is created | Fee rate copied onto the order | Simple; a rate change never rewrites old orders | No category pricing | Low | Low |
| B. Percentage per category | Rate depends on the product category | Realistic | Needs category rules; mixed orders | Medium | Low |
| C. Per-seller rate | Negotiated rates | Flexible | Admin work | Medium | Low |

Timing: take the fee when money moves from pending to available (on delivery), or at payment. Rounding: one rule (for example round down for the fee), written once.

**Recommendation.** A, taken at delivery, with one rounding rule. Storing the rate on the order makes past fees reproducible during reconciliation. Taking it at delivery means a refunded order before delivery needs no fee reversal. The rate value is the owner's choice. **Would change it:** a product need for category pricing.

**Decision:** _pending_

<a id="q-20"></a>
### Q-20: Successful delivery, return window, withdrawal rules

**Status:** open

**Context.** [R-LED-03](domain/ledger.md#r-led-03) pays the seller after successful delivery. The README does not define "successful", returns, or how sellers withdraw.

Merged from Q-33 (2026-11-16): product discovery found a direct conflict. Sellers say cash flow is their biggest pain and that keeping money unavailable for long makes small Sellers leave. Buyers, the Admin team and the business strategist say the money must stay unavailable until the return window ends, because a Refund after a Withdrawal leaves the Seller wallet negative and the marketplace pays. Epics: [EP-09](product/EPICS.md#ep-09), [EP-18](product/EPICS.md#ep-18).

**Options (when seller money becomes available)**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. On the carrier's `Delivered` event | Money moves to available at once | Simple | A return after delivery needs money back from the seller | Low | Medium |
| B. `Delivered` + a return window of N days | A job moves money after N days with no return | Handles returns safely | Needs a scheduled job | Medium | Low |
| C. Buyer confirms, or auto-confirm after N days | A Buyer action makes the money available | Buyer has control | More UI and states | Medium | Low |
| D. Partial release at successful delivery (from Q-33) | Most of the money is available at successful delivery; a fixed share stays unavailable until the return window ends | Faster cash flow; still covers most Refunds | Refunds above the share can leave the Seller wallet negative | Medium | Medium: a negative Seller wallet needs its own ledger accounts |
| E. Faster release as a paid option (from Q-33) | B by default; a Seller can pay for earlier release (ties to [Q-36](#q-36)) | Revenue; Seller chooses | The marketplace carries credit risk | High | Medium |

Withdrawal rules to set: minimum amount, admin approval or automatic, how often, eKYC ([Q-11](#q-11)).

**Recommendation.** B with N as a setting, and withdrawals approved by an admin in the core. Show the release date per Order to Sellers so the wait is predictable (from Q-33). Money that cannot be taken back must not become available early. **Would change it:** returns being out of scope ([Q-37](#q-37)), which makes A enough; evidence that Sellers will not join with B (then D).

**Decision:** _pending_

## Payment

<a id="q-21"></a>
### Q-21: Payment method → provider mapping

**Status:** open

**Context.** The README says buyers pay "via VNPay / QR bank transfer / card", and lists VNPay, SePay and Stripe as providers. It does not map methods to providers.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. VNPay → VNPay; QR bank transfer → SePay; card → Stripe | Three adapters behind one payment port | Matches the README lists (unverified that this is the intent) | Three integrations | High | Low with R-PAY-01 per provider |
| B. VNPay only in the core; others later | One adapter first | Fastest path to a real payment | Port design tested against one provider only | Low | Low |

**Recommendation.** B first, with the port shaped so A can follow. Design the port from what all three share (create payment, receive IPN, query status, refund), and prove it with the fake before adding a second provider. **Would change it:** a demo that needs card payments early.

**Decision:** _pending_

<a id="q-22"></a>
### Q-22: Re-query schedule and payment timeout

**Status:** open

**Context.** [R-PAY-02](domain/payment.md#r-pay-02) says to re-query when the IPN does not arrive. The README does not say when, how often, or when to give up. This decides how long stock stays reserved ([Q-14](#q-14)).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Scheduled job | Every few minutes, query payments still pending after X minutes, with backoff, until the payment window ends | Works even if the buyer closes the browser | A job to run and test | Medium | Low |
| B. Only when the buyer returns to the return URL | Query when the browser comes back | Simple | A buyer who closes the tab leaves the order stuck | Low | Medium |
| C. Both A and B | Return URL triggers a fast check; the job is the safety net | Fast for the buyer; safe | Two code paths (both idempotent per R-PAY-01) | Medium | Lowest |

After the window ends with no result: mark the payment failed, release the reservation, and close the order. VNPay may limit how often `querydr` can be called (unverified).

**Recommendation.** C. The job alone already meets R-PAY-02; the return-URL check only makes it faster. **Would change it:** if gateway rate limits are tight, use A only.

**Decision:** _pending_

<a id="q-23"></a>
### Q-23: Refund flow and ledger entries

**Status:** open

**Context.** The README lists refunds under Payment. A refund moves money back, so it needs ledger entries (R-LED-01, R-LED-02). Late payment after reservation expiry ([Q-14](#q-14)) may also need an automatic refund.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Full refunds only, before the seller is paid | Admin or system refunds the whole payment while money is still pending | Simple; no money taken back from sellers | No partial refunds; no refunds after the seller is paid | Low | Low |
| B. Full and partial refunds, before and after the seller is paid | Any amount, any time | Complete | Seller wallets can go negative; complex | High | Medium |

Every refund: a new set of reversing ledger entries, never an edit. The gateway refund call can fail, so the refund needs its own state (requested → sent → confirmed) and re-query.

**Recommendation.** A first. It covers the system-triggered case (late payment) and the most common admin case, with no negative wallets. **Would change it:** returns being in scope ([Q-37](#q-37)).

**Decision:** _pending_

## Ordering

<a id="q-24"></a>
### Q-24: Order states and transitions

**Status:** open

**Context.** [R-ORD-01](domain/ordering.md#r-ord-01) requires a state machine. The README mentions only "awaiting payment", "in transit" and "delivered", and says a "delivered" order must not go back to "in transit". The README draws no Shipping → Ordering arrow, so whether carrier statuses change the Order state at all is part of this question. Name clash: `Delivered` is also the Shipping event name; if the Order keeps a state with the same name, the GLOSSARY must tell them apart.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. One order state machine that includes shipping states | e.g. AwaitingPayment → Paid → InTransit → Delivered → Completed; plus Cancelled, Expired, Refunded | One place to look | Carrier details leak into Ordering | Low | Low |
| B. Separate machines: order, payment, shipment | Order keeps business states (AwaitingPayment, Paid, Delivered, Completed, Cancelled); Payment and Shipping keep their own; the order changes on their events | Each context owns its states; carrier noise stays in Shipping | More states to keep in sync | Medium | Low |

The state names above are examples, not decisions.

**Recommendation.** B. Carrier statuses are noisy and arrive out of order ([R-SHP-01](domain/shipping.md#r-shp-01)). Keeping them in Shipping means Ordering sees only clean events such as `Delivered`, which R-LED-03 depends on. **Would change it:** a wish for the smallest model in the first version (A).

**Decision:** _pending_

<a id="q-25"></a>
### Q-25: Checkout saga steps and compensation

**Status:** open

**Context.** The README says Ordering orchestrates the checkout saga with compensation ([R-ORD-02](domain/ordering.md#r-ord-02)). Steps and compensations are not listed. An IPN for a closed order also needs a rule.

**Options (where saga state lives)**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. The order row is the saga state | Order state + state machine drive the steps; jobs resume stuck orders | No extra table; one source of truth | Order states also mean saga steps | Low | Low |
| B. A separate saga table (process manager) | Saga record with step and retries | Clear; reusable | More code | Medium | Low |
| C. In memory | Steps run in one request | Simplest | A crash loses the saga | Very low | High |

Proposed steps for A or B (proposal only): place order → reserve stock → create payment → wait for IPN or re-query → paid: make the stock deduction final, publish `OrderPaid` → failed or expired: release stock, close order. Paid for a closed order → refund ([Q-23](#q-23)).

**Recommendation.** A. One developer, one source of truth, and every step is idempotent and can resume after a crash. **Would change it:** sagas beyond checkout (returns, withdrawals) that would reuse B.

**Decision:** _pending_

## Events

<a id="q-26"></a>
### Q-26: Outbox with the first event, or later?

**Status:** open

**Question.** Build the Transactional Outbox together with the first cross-context event, or publish directly first and add the Outbox later?

**Context.** [R-EVT-01](RULES_AND_CONSTRAINTS.md#r-evt-01) comes from the README row "DB write succeeds, publishing fails → order paid but nobody ships it". The README names the Outbox as the solution, not when to build it (owner, 2026-11-16). The first cross-context event is likely `OrderPaid`, which leads to Shipping and to the seller's money (R-LED-03).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Outbox with the first event | Outbox table + relay worker that publishes to RabbitMQ | R-EVT-01 holds from day one; every publisher is written once, the right way | A table, a relay, and their tests before the first event | Medium | Lowest |
| B. Publish directly, add the Outbox later | `commit` then `publish` | Fastest first event | Knowingly builds the bug the project exists to prevent; every publisher changes later | Low now, higher later | Medium: lost `OrderPaid` = paid but not shipped |
| C. In-process events first, Outbox when RabbitMQ arrives | NestJS event emitter in the same process | No broker needed | Handlers in the same transaction couple contexts; lost if the process crashes after commit | Low | Medium |

**Recommendation.** A. The relay is small (poll the table, publish, mark sent), and the failure it prevents is one of the six listed in the README. Retrofitting later touches every publisher. **Would change it:** if the first event has no effect on money or stock (for example a notification only), B is acceptable for that event alone.

**Decision:** _pending_

<a id="q-27"></a>
### Q-27: Retries, DLQ, consumer deduplication

**Status:** open

**Context.** An Outbox delivers events at least once (unverified wording; standard for this pattern), so consumers will see repeats. The README mentions "message queue + DLQ" in its roadmap and deduplication only for carrier events. A repeated `Delivered` could pay a Seller twice.

**Options (deduplication)**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Inbox table per consumer | Store processed event IDs in the same transaction as the handler's change | Generic; exact once in effect | A table and a cleanup job | Medium | Lowest |
| B. Natural idempotency per handler | Each handler checks its own state (e.g. "already released to the Seller for this order?") | No extra table | Easy to forget in one handler | Low | Medium |

Also decide which consumers MUST give one effect per repeated event, and which MAY repeat it: Ledger (paying a Seller twice), Invoicing (a second e-invoice), Notification (a second Notification). The domain docs leave all three undecided.

Retries: N attempts with backoff, then the DLQ. DLQ messages are replayed by hand with a runbook ([runbooks/](runbooks/README.md)).

**Recommendation.** A for handlers that touch money or stock, B allowed for notifications. The inbox makes "one event, one effect" testable in the same way for every money handler. **Would change it:** nothing expected; retry counts wait for measurement.

**Decision:** _pending_

## Shipping

<a id="q-28"></a>
### Q-28: Shipment event key and state machine

**Status:** open

**Context.** [R-SHP-01](domain/shipping.md#r-shp-01) deduplicates carrier updates by an event key. The README does not define the key, or the statuses.

**Options (event key)**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Carrier's own event ID | Use the ID in the webhook | Exact | Not every carrier sends one (unverified for GHN and GHTK) | Low | Low |
| B. Carrier + tracking code + carrier status + carrier timestamp | Build the key from fields | Works for any carrier | A carrier that resends with a new timestamp is not caught | Low | Low |
| C. A per carrier, B as fallback | Adapter decides | Best fit per carrier | Two paths | Medium | Low |

Out-of-order updates: a transition table is the authority. A move back is rejected. Some backward-looking moves can be real (for example delivery failed, then returned to sender), so the table needs care (unverified per carrier).

**Recommendation.** C, with a shipment state machine in Shipping (see [Q-24](#q-24) option B). **Would change it:** both carriers sending a reliable event ID (then A only).

**Decision:** _pending_

## Notification

<a id="q-29"></a>
### Q-29: Which events notify whom, on which channel

**Status:** open

**Context.** The README lists email, SMS and push providers and the `OrderPaid` arrow, but no notification list.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Minimal: email only | Buyer: order paid, delivered. Seller: new paid order | Small; one provider | No SMS or push yet | Low | None |
| B. All channels from the start | Email, SMS, push per event | Complete | Three providers to integrate and fake | High | None |

**Recommendation.** A. Notifications do not affect the invariants, so they can stay small while the core is built. **Would change it:** a demo that needs SMS or push.

**Decision:** _pending_

## Invoicing

<a id="q-30"></a>
### Q-30: Who issues e-invoices, for what, and when

**Status:** open

**Context.** The README says Invoicing issues, adjusts and replaces e-invoices through SePay eInvoice, triggered by `Delivered`. It does not say who the seller of record is. This is a legal question under Vietnamese e-invoice rules (unverified; get qualified advice).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Marketplace invoices the seller for the marketplace fee | One e-invoice per fee | Small; the marketplace invoices only its own income | Buyers get no invoice from the system | Low | None |
| B. Marketplace issues the buyer's invoice for the Products on behalf of the seller | Invoice per order to the buyer | Buyer gets an invoice | Legal basis unverified | Medium | None |
| C. Both | A and B | Complete | Most work | High | None |

**Recommendation.** A for the core, pending legal advice. It invoices only money the marketplace earns, which the ledger already records. **Would change it:** advice that the marketplace must issue buyer invoices.

**Decision:** _pending_

## Reconciliation

<a id="q-31"></a>
### Q-31: Reconciliation sources and mismatch handling

**Status:** open

**Context.** [R-REC-01](domain/reconciliation.md#r-rec-01) requires a nightly job (README, The problem). The README contradicts itself on sources: its context table names payment gateways, banks and shipping carriers; its diagram shows only payment gateways (`REC <-- file / API --> VNP`), and its integrations list names no bank provider. It also does not say which data from carriers (shipping fees? cash on delivery, [Q-35](#q-35)?) or what happens on a mismatch.

**Options (sources)**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| S1. Payment gateways only | Matches the README diagram | One port; smallest | Carrier money and bank movements are not checked | Low | Low while no money flows through carriers |
| S2. Gateways + carriers | Adds carrier fee and COD reports | Covers COD and shipping fees | A second source format | Medium | Lower if COD is in scope |
| S3. Gateways + carriers + bank statements | Adds a bank data source | Matches the README table | No bank provider in the README; needs a new integration | High | Lowest |

Recommendation for sources: S1 for the core; S2 when COD ([Q-35](#q-35)) or shipping fees enter the ledger; S3 only once a bank data source is named. **Would change it:** a decision to keep the README table literally (S3).

**Options (on mismatch)**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Report only; a person fixes it with correcting entries | Mismatch report; admin action adds entries | Nothing changes money without a person; finds bugs | Manual work | Low | Lowest |
| B. Auto-correct known cases | Rules fix some mismatches | Less manual work | Can hide a bug; an automatic money change | Medium | Medium |

Schedule: nightly (README). Exact time: a fixed time at night, Vietnam time (Asia/Ho_Chi_Minh). Source unavailable: retry, then report "not reconciled" (never "matched").

**Recommendation.** A. A mismatch usually means a bug, and an automatic fix would hide it. Corrections as new entries keep R-LED-02. **Would change it:** a large number of known, harmless mismatch types after months of data.

**Decision:** _pending_

## Measurement

<a id="q-32"></a>
### Q-32: Performance targets per capability

**Status:** open

**Context.** The README states one target (p99 < 200ms at 2,000 RPS, in the load and observability capability group) and a Metrics table with "Before / After" columns. [R-TEST-02](RULES_AND_CONSTRAINTS.md#r-test-02) requires every number to be measured.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Measure first, then set targets | Build a baseline script per capability, then pick targets | Targets based on data | No target at the start | Low | None |
| B. Use the README target for everything from the start | p99 < 200ms at 2,000 RPS everywhere | One clear number | Too early; may push for caching before correctness | Low | Medium: speed work can weaken correctness |

Correctness targets are already fixed by the README: oversold = 0, IPN recorded once.

**Recommendation.** A for speed; the correctness targets apply from the first test. **Would change it:** nothing expected.

**Decision:** _pending_

## Product

These questions come from product discovery on 2026-11-15. Each one decides the scope of epics in [product/EPICS.md](product/EPICS.md). Claims about Vietnamese law and competitors are not checked (unverified).

<a id="q-33"></a>
### Q-33: When does Seller money become available for Withdrawal?

**Status:** merged into [Q-20](#q-20) (2026-11-16). Answer Q-20, not this question. The text below is kept as a record. · **Tags:** `product`

**Context.** Product discovery found a direct conflict. Sellers say cash flow is their biggest pain and that keeping money unavailable for long makes small Sellers leave. Buyers, the Admin team and the business strategist say the money must stay unavailable until the return window ends, because a Refund after a Withdrawal leaves the Seller wallet negative and the marketplace pays. [Q-20](#q-20) defines successful delivery and the return window. This question decides the product stance on top of it. Epics: [EP-09](product/EPICS.md#ep-09), [EP-18](product/EPICS.md#ep-18).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Full release after the return window | All of an Order's money becomes available only after the return window in [Q-20](#q-20) ends | Simplest; no negative Seller wallet | Slowest cash flow for Sellers | Low | Lowest |
| B. Partial release at successful delivery | Most of the money is available at successful delivery; a fixed share stays until the return window ends | Faster cash flow; still covers most Refunds | Refunds above the unavailable share can leave the Seller wallet negative | Medium | Medium: a negative Seller wallet needs its own ledger accounts |
| C. Faster release as a paid option | Option A by default; a Seller can pay for earlier release (ties to [Q-36](#q-36)) | Revenue; Seller chooses | The marketplace carries credit risk for paying Sellers | High | Medium |

**Recommendation.** A for the core. It keeps the Ledger simple while [R-LED-01](domain/ledger.md#r-led-01) is being proven, and every perspective except Sellers backs it. Show the release date per Order to Sellers so the wait is predictable. **Would change it:** evidence that Sellers will not join with option A.

**Decision:** merged into [Q-20](#q-20); not answered here.

<a id="q-34"></a>
### Q-34: Who decides a Refund for a Return, and how fast?

**Status:** open · **Tags:** `product`

**Context.** Buyers want a Refund in a few taps, back to the original payment method, on a clear deadline. Sellers say automatic Refunds without the Products coming back are where they lose money, and want time to respond with evidence. The Admin team wants automatic Refunds only below a threshold. [Q-23](#q-23) covers the Refund flow and ledger entries; this question decides who makes the decision. Epics: [EP-17](product/EPICS.md#ep-17), [EP-18](product/EPICS.md#ep-18).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Seller response window, then Admin | The Seller has a fixed time to accept or contest; a contested case goes to an Admin | Fair to both sides | Slower for Buyers; needs Admin work | Medium | None |
| B. Refund after the Products come back | The Refund starts when the Carrier reports the Products returned to the Seller | Protects Sellers | Slow for Buyers; depends on Carrier events | Medium | None |
| C. Automatic below a threshold | Small amounts are refunded at once; larger ones use A | Fast for most Buyers | A fraud channel if the threshold is wrong | Medium | None |

**Recommendation.** A. It needs no fraud scoring and fits a small team. **Would change it:** the Admin team cannot handle the volume of contested cases.

**Decision:** _pending_

<a id="q-35"></a>
### Q-35: Is cash on delivery (COD) in scope?

**Status:** open · **Tags:** `product`

**Context.** The Buyer perspective rates COD a must: many Buyers will not pay first to an unknown Seller (unverified). The README lists only VNPay, QR bank transfer and card, and says the marketplace holds the money. With COD the Carrier holds the money first and sends it to the marketplace later. That adds new ledger accounts, a new Reconciliation source (Carrier money) and a new failure case (Buyer refuses the Products). [Q-07](#q-07) links here for COD. Epic: [EP-22](product/EPICS.md#ep-22).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Out of scope | Online payment only; record COD as a non-goal in [Q-07](#q-07) | Fewer money paths | Unrealistic for the Vietnamese market (unverified) | None | Lowest |
| B. Later, but designed for now | Not built in the core, but the ledger accounts ([Q-18](#q-18)) leave room for money held by a Carrier | Keeps the option open cheaply | Some design work with no feature yet | Low | Low |
| C. In the core | Build COD with Carrier Reconciliation | Realistic | Large extra scope before the core is proven | High | Medium: money owed by a Carrier must balance |

**Recommendation.** B. Adding a new money holder after the ledger accounts are fixed is costly; reserving room for it now is cheap. **Would change it:** the owner wants the project to model the Vietnamese market closely (then C), or wants the smallest scope (then A).

**Decision:** _pending_

<a id="q-36"></a>
### Q-36: Engagement and revenue features: in, later, or out?

**Status:** open · **Tags:** `product`

**Context.** Buyers expect vouchers and reviews; Sellers want Seller-funded vouchers; the business strategist lists subscription tiers and sponsored placement as revenue. The business analyst and the strategist push back on vouchers before the Ledger is proven, because every voucher splits money across more ledger entries. The strategist also pushes back on chat and livestream selling early. [Q-07](#q-07) links here for these candidates. Epics: [EP-25](product/EPICS.md#ep-25), [EP-29](product/EPICS.md#ep-29), [EP-30](product/EPICS.md#ep-30), [EP-31](product/EPICS.md#ep-31).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. All out | Record them as non-goals in [Q-07](#q-07) | Smallest scope; focus on the stated goal | Less realistic product | None | Lowest |
| B. Reviews and ratings in; money features later | Product reviews and Seller ratings (no money) are in; vouchers, subscriptions and ads wait until the Ledger is proven | Trust value without new money paths | Two decision points | Low | Low |
| C. All in | Build all of them | Realistic marketplace | Large scope; many new money paths | High | High |

**Recommendation.** B. Reviews and ratings do not touch money; vouchers and paid tiers do. **Would change it:** a goal to demonstrate Voucher accounting, which is a strong ledger showcase.

**Decision:** _pending_

<a id="q-37"></a>
### Q-37: After-sales exceptions: in scope, and which context owns them?

**Status:** open · **Tags:** `product`

**Context.** Every perspective raised failed delivery, Return after delivery and Disputes between Buyer and Seller. The README covers Refunds (Payment) and Compensation in the Checkout saga, but no context owns a case that spans Shipping, Payment, Ledger and Inventory after the Order is paid. Epics: [EP-16](product/EPICS.md#ep-16), [EP-17](product/EPICS.md#ep-17), [EP-18](product/EPICS.md#ep-18).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Inside Ordering | The Order state machine gains return and dispute states; Ordering orchestrates | No new context | Ordering grows large; mixes checkout with long-running cases | Medium | Low |
| B. A new context for after-sales | A new context owns Returns and Disputes, and calls Payment, Ledger, Inventory and Shipping | Clear owner; keeps Ordering small | An 11th context; changes the README context list | Medium | Low |
| C. Failed delivery only | Only return to sender is in scope; Returns and Disputes are non-goals | Smallest scope | Buyers cannot get a Refund after delivery | Low | Low |

**Recommendation.** Decide scope first (C or not), then the home. If Returns are in, B, because a Return can last weeks after the Order has finished checkout. **Would change it:** the owner prefers to keep the README's 10 contexts unchanged (then A).

**Decision:** _pending_

<a id="q-38"></a>
### Q-38: Is there a Seller handling step between payment and Shipment?

**Status:** open · **Tags:** `product`

**Context.** The README goes from `OrderPaid` straight to Shipping. In practice a Seller confirms, packs and hands Products to the Carrier, or cancels when Products are missing. Sellers need bulk handling and shipping labels. The business analyst notes that no context owns this step, so Orders can get stuck after payment. Epic: [EP-15](product/EPICS.md#ep-15).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Automatic Shipment | `OrderPaid` creates the Shipment at once; the Seller only prints the label | Matches the README; simplest | No way for a Seller to cancel before handover | Low | None |
| B. Seller confirms first | The Order waits for the Seller to confirm before a Shipment is created, with a deadline | Realistic; Seller can cancel cleanly | Needs a timeout and Compensation | Medium | Low: a cancel must release Stock and start a Refund |

**Recommendation.** B. A Seller cancel after payment happens in real marketplaces, and it is a strong test of Compensation. **Would change it:** a wish to match the README flow exactly.

**Decision:** _pending_

<a id="q-39"></a>
### Q-39: Vietnam compliance scope: Seller tax withholding, personal data

**Status:** open · **Tags:** `product`

**Context.** The business strategist and the business analyst report that Vietnamese rules may require marketplaces to withhold and declare tax for household Sellers, and that personal data rules apply to Buyer data shown to Sellers (unverified, both). Tax withholding changes the ledger accounts ([Q-18](#q-18)) and e-invoices ([Q-30](#q-30)). Data retention for accounting records may conflict with deletion requests (unverified). Epics: [EP-23](product/EPICS.md#ep-23), [EP-24](product/EPICS.md#ep-24).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Both in, after checking the law | The owner checks the current rules; both are built as required | Realistic | Needs legal research first | High | Medium: withholding adds ledger accounts |
| B. Personal data in; tax withholding designed for, built later | Masking and consent are built; ledger accounts leave room for withheld tax | Cheap now; no rework later | Tax feature missing | Medium | Low |
| C. Both out | Record as non-goals ([Q-07](#q-07)) | Smallest scope | Less realistic | None | None |

**Recommendation.** B. Data masking is cheap if designed early; withholding mainly needs room in the ledger accounts. **Would change it:** a checked legal source that makes withholding central to how Seller money is split.

**Decision:** _pending_

<a id="q-40"></a>
### Q-40: Bulk product import and multi-channel stock sync: in scope?

**Status:** open · **Tags:** `product`

**Context.** Sellers who sell on several marketplaces want bulk import of Products and an API to keep Stock in sync. Stock sync lets an external system change Stock, which adds a new write path next to Stock reservations. [R-INV-01](domain/inventory.md#r-inv-01) protects only TallyMart's own Stock. Epics: [EP-27](product/EPICS.md#ep-27), [EP-28](product/EPICS.md#ep-28).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Both out | Sellers enter Products and Stock in the web app | Smallest scope | Unrealistic for multi-channel Sellers | None | None |
| B. Bulk import only | File import of Products, Prices and Stock | Big Seller value; one write path | No live sync | Medium | Low |
| C. Both | Bulk import plus a Stock sync API | Realistic | External writes race with Stock reservations | High | Medium |

**Recommendation.** B. Bulk import is high value with low risk. A sync API should wait until the locking strategy ([Q-15](#q-15)) is proven under load. **Would change it:** a wish to test Stock correctness against an external writer.

**Decision:** _pending_

<a id="q-41"></a>
### Q-41: Admin back-office, audit trail and fraud tools: scope and home

**Status:** open · **Tags:** `product`

**Context.** The Admin team and the business analyst both rate a back-office a must: one timeline per Order, queues for stuck Orders and Reconciliation mismatches, manual corrections made only as new ledger entries, a second Admin approving large amounts, and an audit trail of every Admin action. Fraud signals and Seller penalties were rated lower. Admin powers are part of [Q-06](#q-06). Stuck-state detection (EP-21) overlaps the queues: [Q-44](#q-44). The audit trail is cross-cutting and has no owner in the README. Epics: [EP-19](product/EPICS.md#ep-19), [EP-26](product/EPICS.md#ep-26).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Each context exposes its own Admin actions; audit trail is cross-cutting | No new context; each module records its Admin actions in a shared audit format | Fits the modular monolith | Audit format must be agreed early | Medium | Low |
| B. A new back-office context | One context owns Admin workflows and the audit trail | One place to look | Tempts direct writes into other contexts' tables | Medium | Medium: could bypass Ledger rules |
| C. Minimal | Only manual ledger adjustments and an audit trail; no queues or fraud tools | Smallest scope | Mismatches found by Reconciliation have no workflow | Low | Low |

**Recommendation.** A, with fraud tools later. Keeping Admin actions inside the owning context keeps "only Ledger writes ledger entries" true. **Would change it:** nothing expected.

**Decision:** _pending_

<a id="q-42"></a>
### Q-42: Reporting: Seller statement, Seller reports, finance reports

**Status:** open · **Tags:** `product`

**Context.** Sellers, the business analyst and the business strategist all rate a Seller statement (every ledger entry per Order: payment, Marketplace fee, Refund, shipping) a must; the strategist calls it the main differentiator. Sellers also want sales reports; finance wants a daily close report. The Ledger holds the data, but the README gives no context the job of reporting. Epic: [EP-20](product/EPICS.md#ep-20).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Seller statement only, served by Ledger | Ledger exposes a read view per Seller wallet | Small; high trust value | No sales or finance reports | Low | None |
| B. Statement plus a read model for reports | Reports are built from events into a separate read model | Fits the CQRS plans in the README | More moving parts | Medium | None (read only) |
| C. Out | No reports in scope | Smallest | Sellers cannot check their money | None | None |

**Recommendation.** A first. It proves the ledger to Sellers with the least work; B can follow when the read model is built for other reasons. **Would change it:** nothing expected.

**Decision:** _pending_

## Raised by the consistency review (2026-11-16)

These questions come from the docs consistency review (`.claude/reviews/consistency-2026-11-16.md`). Each one was found as a conflict that the README does not settle.

<a id="q-43"></a>
### Q-43: Does checkout need a Shipping quote before payment?

**Status:** open

**Context.** EP-06 (Checkout) needs "a Shipping quote from EP-10", and EP-10 (Shipping) needs EP-06's `OrderPaid`, so the epics form a loop. The README gives Shipping "multi-carrier quotes" but draws no Ordering → Shipping arrow before `OrderPaid`. The Build order puts Ordering (step 6) before Shipping (step 8). Epics: [EP-06](product/EPICS.md#ep-06), [EP-10](product/EPICS.md#ep-10).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Quote at checkout from Shipping | Ordering asks Shipping for a Shipping quote (new edge). Split EP-10 into quotes (built before EP-06) and Shipments (after EP-06) | Buyer sees the full Price; breaks the loop | A new edge the README does not draw; Shipping work starts earlier | Medium | None directly; the quote is part of the Payment amount (R-LED-01) |
| B. No quote at checkout | Flat or free shipping; quotes only when the Shipment is created | No new edge; keeps the README diagram | Buyer does not see the real shipping price | Low | None |
| C. Ordering computes the fee itself | A fee table inside Ordering | No call to Shipping | Duplicates Shipping's job; drifts from carrier prices | Low | None |

**Recommendation.** A. The README gives quotes to Shipping, and splitting EP-10 removes the loop without moving the rest of the Build order. **Would change it:** if the first demo can live with a flat fee, B, and add A later.

**Decision:** _pending_

<a id="q-44"></a>
### Q-44: Stuck-state detection: in scope, and where does it live?

**Status:** open · **Tags:** `product`

**Context.** EP-21 detects Orders paid with no Shipment, Shipments with no update, missing IPNs, a growing DLQ and failed e-invoices. It was labelled "README (observability)", but the README's observability group lists OpenTelemetry, SLOs and load tests, not stuck-state detection. It cited [Q-32](#q-32) (performance targets), which does not ask this. Its queues overlap EP-19's "queues for stuck Orders" ([Q-41](#q-41)). Epic: [EP-21](product/EPICS.md#ep-21).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Alerts only, inside the observability group | Metrics and alerts on stuck states; no work queue | Small; fits the README's observability tools | Someone must act on alerts by hand | Low | None; it detects breaks |
| B. Part of the back-office (EP-19) | Stuck items appear in Admin queues | One place for Admin work | Waits for the Q-41 decision | Medium | None |
| C. Later | Not in the first plan | Least work | Silent failures cost money | None | None |

**Recommendation.** A for alerts; queues follow [Q-41](#q-41). **Would change it:** if the back-office is in the core, B.

**Decision:** _pending_

<a id="q-45"></a>
### Q-45: How do epics and enabling work become the plan?

**Status:** open

**Context.** [product/EPICS.md](product/EPICS.md) says only epics whose Decision is `accepted` or `changed` go into the plan. No epic covers Build-order step 0 (repo setup, ports with fakes, `Idempotency-Key`) or step 7 (Events + Outbox), so that work could never enter the plan ([PROJECT_OVERVIEW: Build order](PROJECT_OVERVIEW.md#build-order)). The allowed epic Decision values are defined nowhere in [docs/README](README.md). Closing a question never updates an epic's Scope. `docs/product/` has no row in the CLAUDE.md routing table.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Epics are the plan input | Add an enabling epic for steps 0 and 7; define epic Decision values (`_pending_`, `accepted`, `changed`, `rejected`) in docs/README; `/close-question` updates the Scope of linked epics; add `docs/product/` to CLAUDE.md routing | One list to plan from | One more epic to keep | Low | Lower: the Outbox and `Idempotency-Key` get planned explicitly |
| B. The Build order is the plan | Sprints follow Build-order steps; epics map onto steps | Follows module dependencies directly | Two planning inputs to keep in sync | Low | None |

**Recommendation.** A. **Would change it:** if the sprint plan is meant to follow modules, not features, B.

**Decision:** _pending_

<a id="q-46"></a>
### Q-46: In the flash-sale test, is underselling a failure?

**Status:** open

**Context.** The README Metrics row is "Flash sale: 50 concurrent requests, stock of 10 → oversold: 0". The domain doc and the `/invariant-test` skill said "exactly 10 succeed", which also forbids selling fewer than 10 (underselling). The README does not require that. "Exactly 10" also assumes one unit per request, no per-user cap ([Q-17](#q-17)) and no rate limit ([Q-16](#q-16)).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. Only oversold = 0 | The test fails only if more than 10 succeed | Matches the README | A bug that rejects valid requests passes the test | Low | None |
| B. Also exactly N succeed, under stated test conditions | The test fixes 1 unit per request, no cap, no rate limit, and checks exactly 10 succeed | Catches over-locking bugs | A test condition, not a domain rule; must be stated in the test | Low | None |

**Recommendation.** B as a test condition only; R-INV-01 stays "never more than the stock". **Would change it:** nothing expected.

**Decision:** _pending_

<a id="q-47"></a>
### Q-47: How does a Withdrawal move money to the Seller's bank?

**Status:** open · **Tags:** `product`

**Context.** EP-09 moves available money "to a verified bank account" and handles "reversal of a failed bank transfer". The README lists Withdrawals under Ledger but names no outgoing bank transfer provider, port or context ([README: External integrations](../README.md#external-integrations)). Epic: [EP-09](product/EPICS.md#ep-09).

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. An outgoing-transfer port with a fake only | A port for outgoing bank transfers; only the fake exists in scope | Follows R-INT-01; testable | No real sandbox transfer | Low | Lowest |
| B. Pick a provider | For example a gateway's outgoing-transfer API (unverified that any README provider offers one) | Real sandbox flow | New integration; needs an ADR and approval ([R-REPO-04](RULES_AND_CONSTRAINTS.md#r-repo-04)) | High | Low |
| C. Manual transfer by an Admin | An Admin transfers by hand and records it; ledger entries follow | No integration | Manual work; slower | Low | Low if every step is a ledger entry |

**Recommendation.** A or C until a provider is chosen. **Would change it:** a provider with an outgoing-transfer sandbox.

**Decision:** _pending_

<a id="q-48"></a>
### Q-48: Which file owns the doc process?

**Status:** open

**Context.** [docs/README](README.md), [CLAUDE.md](../CLAUDE.md) and the skills in `.claude/skills/` describe parts of the same process differently. `last_verified` while no code exists: `/end-session` forbids the update, but CLAUDE.md and docs/README require it. Recurring AI mistakes: CLAUDE.md says "add", `/end-session` says "propose, then add after the owner agrees". ADR status: docs/README has `deprecated` and `decision_status`; `/propose-adr` and decisions/README use `superseded` and `draft`/`active`. `/start-spec` uses an undefined `R-<AREA>-NEW` placeholder, and the spec template invites pending questions that `/start-spec` forbids.

**Options**

| Option | How it works | Pros | Cons | Solo cost | Risk to invariants |
|---|---|---|---|---|---|
| A. docs/README owns the process | CLAUDE.md and the skills link to docs/README and never restate a rule; each conflict above is fixed in docs/README first | One source; fewer drifts | Skills must link out | Low | None |
| B. Each skill owns its own step | docs/README describes only formats | Skills stay self-contained | The same rule in many places drifts again | Low | None |

**Recommendation.** A. **Would change it:** nothing expected.

**Decision:** _pending_
