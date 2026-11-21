---
name: start-spec
description: Use when starting work on a TM-xx GitHub issue that changes behavior and has no spec yet. Trigger phrases - "/start-spec", "start TM-12", "write a spec for TM-xx", "spec this issue", "let's begin TM-xx".
---

# Start a spec

Creates `docs/specs/TM-xx-<short-name>.md` from the [spec template](../../../docs/specs/_template.md) before any code is written.
How to write docs: [docs/README.md](../../../docs/README.md). Do not copy the template here; copy the file.

## Stop and ask when

- There is no `TM-xx` ID → STOP. Ask for the issue ID.
- The work needs an open question that has no `Decision` in [OPEN_QUESTIONS](../../../docs/OPEN_QUESTIONS.md) → STOP. List each blocking `Q-NN` with one line on why it blocks. Do not pick an answer, not even the recommended option.
- The work needs a module that the [Build order](../../../docs/PROJECT_OVERVIEW.md#build-order) puts later, and that does not exist yet → STOP. Name the missing module.
- The issue text conflicts with a rule → STOP. Name the rule ID and the issue text.

## Steps

1. Read the issue goal from the owner. Write it as one or two sentences in plain English.
2. Copy `docs/specs/_template.md` to `docs/specs/TM-xx-<short-name>.md`. Remove the instruction lines. Set `status: draft` and today's `last_verified`. Keep `related_code: []` unless the code paths already exist.
3. Find the context(s) involved. Read each `docs/domain/<context>.md` and [RULES_AND_CONSTRAINTS](../../../docs/RULES_AND_CONSTRAINTS.md).
4. Fill "Rules involved": every rule ID the work uses, changes, or adds. A new rule gets `R-<AREA>-NEW` until the domain doc gives it a real ID ([docs/README: Rule IDs](../../../docs/README.md#rule-ids)).
5. Find blocking questions:
   ```
   grep -nE "Q-[0-9]{2}" docs/domain/<context>.md docs/RULES_AND_CONSTRAINTS.md docs/ARCHITECTURE.md docs/CONVENTIONS.md docs/PROJECT_OVERVIEW.md docs/product/EPICS.md
   ```
   This finds OPEN QUESTION lines and plain `Q-NN` links. For each question the work touches, check its `Decision`. Any `_pending_` → apply the stop condition.
6. Fill "Behavior" as a table: condition → behavior → example. Use [GLOSSARY](../../../docs/GLOSSARY.md) terms only.
7. Fill "Edge cases" with at least: concurrency, external failure (slow, down, duplicate), and repeated request (R-API-01).
8. Write "Acceptance criteria": each item is a test or a measurement. If the work touches stock or money, add an item that uses the `invariant-test` skill.
9. Propose "Learning points (owner-written)" from the [concept map](../../../docs/LEARNING_MODE.md#concept-map): the `L-NN` concepts this work practices and the functions or files the owner writes. The owner confirms or edits the list. Write "None" if there are none.
10. Fill "Docs to update when done" from the [CLAUDE.md sync table](../../../CLAUDE.md#5-keeping-docs-in-sync-must-checked-before-you-report-a-task-as-done).
11. Show the spec to the owner and wait for approval before writing code.

## Edge cases

- The work is a pure refactor with no behavior change → no spec is needed. Say so and stop.
- The issue is too big for one spec (more than one context changes behavior) → propose a split into several TM-xx issues.

Done when: the spec file exists with every section filled, it names every rule ID it touches, it lists no `_pending_` question that the work needs, every acceptance criterion is a test or a measurement, and the owner has approved it.
