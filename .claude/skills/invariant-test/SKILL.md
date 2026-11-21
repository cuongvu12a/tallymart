---
name: invariant-test
description: Use when a change touches stock, stock reservations, payments, IPN handling, or ledger entries, and needs tests that prove the core invariants. Trigger phrases - "/invariant-test", "prove no oversell", "test the ledger balances", "concurrency test", "test duplicate IPN".
---

# Invariant tests

Writes tests that prove the two core invariants and the IPN rule still hold. Shapes A and B come from the [README Metrics table](../../../README.md#metrics). Shape C comes from [R-LED-01](../../../docs/domain/ledger.md#r-led-01).

| Test shape | Rule | Pass condition |
|---|---|---|
| A. 50 concurrent requests on stock 10 | [R-INV-01](../../../docs/domain/inventory.md#r-inv-01) | oversold = 0: no more than 10 succeed. Whether exactly 10 must succeed: Not decided ([Q-46](../../../docs/OPEN_QUESTIONS.md#q-46)) |
| B. The same IPN sent 10 times | [R-PAY-01](../../../docs/domain/payment.md#r-pay-01) | One payment recorded, one set of ledger entries |
| C. Ledger sum after any money flow | [R-LED-01](../../../docs/domain/ledger.md#r-led-01) | Sum of all ledger entries = 0 |

## Stop and ask when

- The code under test does not exist yet → STOP. Report which module is missing.
- A test needs a value that an open question still holds (for example the TTL value, which waits for Q-22) → STOP. Name the `Q-NN`; do not pick a value.
- Making a test pass seems to need a real sandbox → STOP. Tests MUST use the fake implementation ([R-INT-02](../../../docs/RULES_AND_CONSTRAINTS.md#r-int-02)). Extend the fake instead, or ask.
- A new test dependency is needed (for example a concurrency helper) → STOP and ask (R-REPO-04).

## Steps

1. Name the rule IDs the change touches. Pick the shapes (A, B, C) that cover them. Shape C applies to every change that writes ledger entries.
2. Use a real PostgreSQL through Testcontainers, because locks and transactions are what is being tested. An in-memory store would hide the race. Wire every external port to its fake implementation.
3. Put the rule ID in each test name, so `/audit-docs` can find it: for example `R-INV-01: 50 concurrent reserves on stock 10 never oversell`.
4. Shape A: set stock to 10. Start 50 requests at the same moment (start them all, then await them all together; do not await one by one). Each request uses a different user and a different `Idempotency-Key`. Assert the counts and the final stock read from the DB.
5. Shape B: make the fake payment gateway send the same IPN 10 times, both one after another and at the same moment. Assert one payment, one order state change, and one set of ledger entries.
6. Shape C: after the flow under test, read every ledger entry from the DB and assert the sum is exactly 0. Compare as integers, never as floats.
7. Add one failure variant per shape where it applies: the fake gateway times out, or returns an error, or the reservation expires during the flow. Assert the invariant still holds.
8. Run each test several times in a row to catch flaky races: `TODO (TM-repo-setup)`.
9. If a number in the README Metrics table is now measured, report it with the script path ([R-TEST-02](../../../docs/RULES_AND_CONSTRAINTS.md#r-test-02): values in the README "After" column are targets until measured). Do not edit the README without asking the owner.

## Edge cases

- A test passes only with a sleep or a fixed delay → it is not proving the race. Rewrite it so all requests start together.
- Shape A ends with fewer than 10 successes → report it. Whether that is a failure: Not decided ([Q-46](../../../docs/OPEN_QUESTIONS.md#q-46)).

Done when: every touched rule ID has a test named after it, shapes A, B and C pass with fakes only, the failure variants pass, and repeated runs give the same result.
