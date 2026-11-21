---
status: draft
owner: Cuong Vu
last_verified: YYYY-MM-DD
applies_to: [backend, <context>]
related_code: []
---

# TM-xx: <short title>

Copy this file to `docs/specs/TM-xx-<short-name>.md`. Delete these instruction lines.
A spec describes one work item. Rules it creates or changes MUST be moved into the matching domain doc or RULES file when the work is done, because each fact lives in one place.

GitHub issue: TM-xx

## Goal

What the user or system can do after this work, in one or two sentences.

## Rules involved

| Rule ID | New, changed or used | Note |
|---|---|---|
| R-<AREA>-NN | used | |

## Behavior

| Condition | Behavior | Example |
|---|---|---|
| | | |

## Edge cases

- Concurrency: <what happens when two requests race>
- External failure: <what happens when the provider is slow, down, or sends duplicates>
- Repeat: <what happens when the same request arrives twice> (R-API-01)

## Acceptance criteria

Each item MUST be checkable by a test or a measurement.

- [ ] <test or measurement that proves it>

## Learning points (owner-written)

The concepts this spec practices, from the [concept map](../LEARNING_MODE.md#concept-map). The owner writes the functions and files listed here. AI writes only owner stubs and failing tests for them ([CLAUDE.md: Learning mode](../../CLAUDE.md#4a-learning-mode)). Write "None" if the spec practices no concept.

| Concept | Functions or files the owner writes | Stub and failing tests ready |
|---|---|---|
| [L-NN](../LEARNING_MODE.md#l-nn) <concept name> | `<path>`: `<function>` | [ ] |

## Out of scope

-

## Questions this work needs

Link each question the work touches, with its Decision. Do not copy a question here: it lives only in [OPEN_QUESTIONS](../OPEN_QUESTIONS.md). A question with `Decision: _pending_` stops the spec ([`/start-spec`](../../.claude/skills/start-spec/SKILL.md)).

| Question | Decision |
|---|---|
| [Q-NN](../OPEN_QUESTIONS.md#q-nn) | <one line> |

## Docs to update when done

Check the sync table in [CLAUDE.md](../../CLAUDE.md#5-keeping-docs-in-sync-must-checked-before-you-report-a-task-as-done) and list the docs here.

-
