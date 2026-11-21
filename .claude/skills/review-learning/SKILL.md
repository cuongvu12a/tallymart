---
name: review-learning
description: Use when the owner asks for a review, a hint, a comparison or a contrast of code they wrote for a learning point. Trigger phrases - "/review-learning", "review my code for TM-xx", "hint", "I'm stuck", "show fix", "compare", "give up", "contrast Factory", "contrast optimistic lock".
---

# Review learning

Reviews code the owner wrote for a learning point, without writing it for them. Rules: [CLAUDE.md: Learning mode](../../../CLAUDE.md#4a-learning-mode). Concept map and the mistakes table: [docs/LEARNING_MODE.md](../../../docs/LEARNING_MODE.md).

Call: `/review-learning <TM-xx | file> [hint | show fix | compare | give up | contrast <concept>]`. With no mode, run **Check**, then **Review**.

## Hard limits (every mode)

- MUST NOT edit the owner's files: no fix, no stub removal, no test change. Code goes in chat only, and only in the modes that allow it (show fix, compare, contrast).
- The only file this skill writes is the "Owner's recurring mistakes" table in [LEARNING_MODE.md](../../../docs/LEARNING_MODE.md#owners-recurring-mistakes). Contrast MAY also write under `scratch/` (see Contrast, step 2).
- Report test and lint results as they really are (R-TEST-01). Never say "should pass".

## Stop and ask when

- The target is a TM-xx with no spec, or a spec with no "Learning points (owner-written)" section → STOP. Ask which concepts the owner practiced.
- A file is given but no concept from the [concept map](../../../docs/LEARNING_MODE.md#concept-map) matches it → STOP. Ask which `L-NN` it practices.
- `compare` or `contrast` is asked while tests fail, and the owner did not type "give up" (compare only) → STOP. Say which tests fail and offer `hint`.

## A. Check (always first)

1. Run tests and lint: `TODO (TM-repo-setup)`. Until the commands exist, say "tests and lint: not available yet" and review by reading only.
2. Report the real result: pass and fail counts, and the name of each failing test.
3. List every remaining owner stub: `grep -rn "TODO(owner)" apps packages` (skip folders that do not exist). Show `file:line` and its `LEARN:` concept.

## B. Review (default)

For each learning point in the spec:

1. Grade it: **Met**, **Almost** or **Not yet**, with one sentence of evidence (`file:line`).
2. Check the common traps of that concept. Examples:

   | Concept | Trap |
   |---|---|
   | Factory ([L-02](../../../docs/LEARNING_MODE.md#l-02)) | The factory registers its own implementations inside itself, so adding one means editing it |
   | Builder ([L-03](../../../docs/LEARNING_MODE.md#l-03)) | The built object can still be changed; `build()` does not check the invariant |
   | Singleton, DI ([L-01](../../../docs/LEARNING_MODE.md#l-01), [L-07](../../../docs/LEARNING_MODE.md#l-07)) | Per-request state kept in a singleton; a captive dependency |
   | Transactions, locking ([L-15](../../../docs/LEARNING_MODE.md#l-15), [L-16](../../../docs/LEARNING_MODE.md#l-16)) | Check-then-act race; an external call inside a DB transaction; locks taken in different orders |
   | Keyset pagination ([L-14](../../../docs/LEARNING_MODE.md#l-14)) | No tie-breaker column, so rows are skipped or repeated |
   | Index ([L-17](../../../docs/LEARNING_MODE.md#l-17)) | Column order breaks the leftmost prefix; a claim with no `EXPLAIN` to back it |
   | Cache ([L-21](../../../docs/LEARNING_MODE.md#l-21), [L-22](../../../docs/LEARNING_MODE.md#l-22)) | The cache is not invalidated on write; no TTL; a stampede on a hot key |
   | Rate limiter ([L-23](../../../docs/LEARNING_MODE.md#l-23)) | Read then write in Redis as two steps; the counter lives in process memory |
   | Consumer, outbox ([L-25](../../../docs/LEARNING_MODE.md#l-25), [L-26](../../../docs/LEARNING_MODE.md#l-26)) | The consumer is not idempotent; retries never end; publish happens after commit |
   | Retry ([L-28](../../../docs/LEARNING_MODE.md#l-28)) | Retry of a call that is not idempotent; no jitter |

3. Check clean code: names (against [GLOSSARY](../../../docs/GLOSSARY.md), R-DOC-01), coupling, single responsibility, duplication, and the rules the spec lists.
4. Write each issue as `file:line` + one guiding question. Example: "`stock.repository.ts:42`: what happens if two requests read `stock = 1` at the same time?"
5. MUST NOT give fixed code in this mode.

## C. Hint (`hint`)

Use when a test fails or the owner is stuck. Each call goes up **one** level only. Count the hints already given for the same failing test in this conversation. If you cannot tell, start at level 1.

| Level | Give |
|---|---|
| 1 | The name of the concept, and why the test fails |
| 2 | The exact place that is wrong (`file:line`) |
| 3 | Pseudocode for the fix |
| 4 | Only after the owner types `show fix`: the fixed code, in chat. Do not edit the file; the owner types it in. Then add the mistake to the recurring mistakes table |

## D. Compare (`compare`)

Runs only when tests pass, or when the owner types `give up`.

1. Write your own solution in chat. Do not write it into the owner's files.
2. Show a table: difference → which way is better → why → trade-off. Where the owner's way is better, say so plainly.
3. The owner decides whether to change anything.

## E. Contrast (`contrast <concept>`)

Runs only when the owner's code passes its tests. Goal: the owner sees what the concept is best for.

1. Ask first: "Without <concept>, where do you think the code would get messy or break?" Wait for the answer, in English.
2. Write a version WITHOUT the concept, the way a beginner would (`if/switch`, `new` everywhere, check-then-act, a DB call on every request…). Put it in chat or under `scratch/learning/<concept>/`, never in `apps/` or `packages/`. No `.gitignore` exists yet: before the first use of `scratch/`, ask the owner to ignore it.
3. Pick 2–3 change or load scenarios that fit TallyMart: add a new implementation, write a unit test, 50 concurrent requests, 3 million rows, one instance dies…
4. Show a table: scenario → version without the concept (which files change, how many places, what goes wrong) → owner's version. For measurable concepts (locks, indexes, cache, rate limit), run it or write a test that proves it, and give the measured number: oversold units, p95 latency, query count. Never estimate (R-TEST-02). If the commands do not exist yet, say the number is not measured.
5. The other side: 1–2 cases where the concept is too much or harmful (an extra layer, harder debugging, more memory), and what to use then.
6. Compare the owner's guess from step 1 with the result. For each benefit the owner did not guess, add a row to the mistakes table with Concept = "<concept>: benefit not seen".
7. Suggest one sentence the owner can copy into the "Solution Architect view" part of their study note: "Use X in module Y because Z; without it, W."

## F. Teach-back (end of every mode)

1. Ask 1–2 questions that make the owner explain the idea again in their own words. The owner answers in English.
2. Check the answer: name each wrong or missing idea.
3. Add each mistake to the recurring mistakes table: today's date, `L-NN <concept>`, the mistake, the correct idea. If the same row exists, add today's date to it instead.

## Edge cases

- The owner asks you to "just fix it" → refuse and offer `hint` at the next level (CLAUDE.md 4a).
- A test looks wrong to the owner → discuss it in chat. Do not change it. The owner decides; a test change goes through the spec.
- No owner stubs remain and tests pass → Review, then suggest `compare` or `contrast`.

Done when: the real test and lint results are reported, the remaining owner stubs are listed, the mode's output is given without editing the owner's files, the teach-back questions are asked and checked, and mistakes are added to the table.
