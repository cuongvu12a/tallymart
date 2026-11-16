# CLAUDE.md

Entry point for every AI session in TallyMart. `AGENTS.md` is a symlink to this file.
Keep this file under 150 lines. Every line must stop a mistake.

## 1. What this project is

TallyMart is a multi-vendor e-commerce marketplace: a NestJS backend and a Next.js web app.
Goal: be correct under concurrent load and when external systems fail, proven by tests and measured numbers. Details: [README.md](README.md).
Status: no code exists yet. Current state: [STATUS.md](STATUS.md).

Two core invariants. Every change MUST protect them:
- **Stock is never oversold:** [R-INV-01](docs/domain/inventory.md#r-inv-01)
- **The ledger always balances (sum of entries = 0):** [R-LED-01](docs/domain/ledger.md#r-led-01)

Non-goals are not decided yet: [Q-07](docs/OPEN_QUESTIONS.md#q-07). DO NOT assume.
In the README, a "Phase" is a capability group, not a timeline ([GLOSSARY](docs/GLOSSARY.md#technical-terms)). Ignore the README dates and sprint numbers.
What to build next: [Build order](docs/PROJECT_OVERVIEW.md#build-order), a proposal until [Q-09](docs/OPEN_QUESTIONS.md#q-09) is decided.
Sources of truth: [docs/README: Sources of truth](docs/README.md#sources-of-truth). Anything else is an OPEN QUESTION.

## 2. When you… → read first

| When you… | Read first |
|---|---|
| Start any session | [STATUS.md](STATUS.md) |
| Change business behavior in a context | `docs/domain/<context>.md` (in [docs/domain/](docs/domain/)) and [GLOSSARY](docs/GLOSSARY.md) |
| Name anything (class, table, API field, event) | [GLOSSARY](docs/GLOSSARY.md) |
| Write or change any code | [RULES_AND_CONSTRAINTS](docs/RULES_AND_CONSTRAINTS.md), [CONVENTIONS](docs/CONVENTIONS.md) |
| Add a module, a service or a data flow | [ARCHITECTURE](docs/ARCHITECTURE.md) |
| Work on a TM-xx issue | `docs/specs/TM-xx-<name>.md` if it exists ([template](docs/specs/_template.md)) |
| Decide what to build next | [PROJECT_OVERVIEW: Build order](docs/PROJECT_OVERVIEW.md#build-order) (a proposal until Q-09 is decided) |
| Meet a question nobody has decided | [OPEN_QUESTIONS](docs/OPEN_QUESTIONS.md) |
| Choose a technology, library or major structure | [decisions/README](docs/decisions/README.md) |
| Write or edit any doc | [docs/README](docs/README.md) |
| Run, operate or recover the system | [runbooks/](docs/runbooks/README.md) |

## 3. Commands

```
TODO (TM-repo-setup): install, build, test, lint, typecheck, run, regenerate the API client.
```

- The commands under "Getting started" in the README are planned. They do not run yet. MUST NOT run or invent commands.
- **A task is done only when tests + lint pass** ([R-TEST-01](docs/RULES_AND_CONSTRAINTS.md#r-test-01)). If they cannot run yet, say so in your report. A docs-only task has its own Definition of Done in R-TEST-01.

> OPEN QUESTION Q-10: Lint, format and test tooling; which test levels count for "done"? DO NOT assume. → [details](docs/OPEN_QUESTIONS.md#q-10)

## 4. Hard rules

Each rule is one line here. The reason, the alternative and examples are behind the link.

- MUST NOT edit a merged migration. Add a new migration instead. [R-REPO-01](docs/RULES_AND_CONSTRAINTS.md#r-repo-01)
- MUST NOT edit `.env*` files. Ask the owner. [R-REPO-02](docs/RULES_AND_CONSTRAINTS.md#r-repo-02)
- MUST NOT edit `packages/api-client/`. It is generated from OpenAPI. [R-REPO-03](docs/RULES_AND_CONSTRAINTS.md#r-repo-03)
- MUST NOT add a dependency without asking first. [R-REPO-04](docs/RULES_AND_CONSTRAINTS.md#r-repo-04)
- MUST NOT call real sandboxes in tests or CI. Use the fake implementation. [R-INT-02](docs/RULES_AND_CONSTRAINTS.md#r-int-02)
- MUST NOT put business logic in the web app. [R-WEB-01](docs/RULES_AND_CONSTRAINTS.md#r-web-01)
- MUST use GLOSSARY terms exactly, never a forbidden synonym. [R-DOC-01](docs/RULES_AND_CONSTRAINTS.md#r-doc-01)
- MUST cite a rule by its ID when you apply it, or when your change touches it. [R-DOC-02](docs/RULES_AND_CONSTRAINTS.md#r-doc-02)
- MUST write every repo file in plain English. [R-DOC-03](docs/RULES_AND_CONSTRAINTS.md#r-doc-03)
- Every write API takes an `Idempotency-Key`. [R-API-01](docs/RULES_AND_CONSTRAINTS.md#r-api-01)

## 5. Keeping docs in sync (MUST, checked before you report a task as done)

| If you changed… | You MUST update… |
|---|---|
| Business behavior (a rule, a condition, a state transition) | `docs/domain/<context>.md`: the rule + `last_verified` |
| Created a new module folder | add its path to `related_code` of the matching `docs/domain/<context>.md` |
| Added / removed / renamed a module, service or data flow | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| Introduced a new domain term | [docs/GLOSSARY.md](docs/GLOSSARY.md) |
| Chose or changed a technology, library or a major structure | propose a new ADR in [docs/decisions/](docs/decisions/README.md) |
| Build / test / run commands, environment variables | CLAUDE.md "Commands" + [docs/runbooks/](docs/runbooks/README.md) |
| Changed a source listed in `SYSTEM_TOUR.md` `derived_from` | run [`/update-tour`](.claude/skills/update-tour/SKILL.md): it regenerates [docs/overview/SYSTEM_TOUR.md](docs/overview/SYSTEM_TOUR.md), then `system-tour.html` |
| Progress, unfinished work, blockers | [STATUS.md](STATUS.md) (end of session) |

- A pure refactor, formatting, or renaming internal variables needs no doc change.
- If you are not sure whether a doc must change, say so in the final report. Never skip it silently.
- Run `bash scripts/check-docs.sh` before you report done. It reports docs whose `related_code` paths changed while the doc did not.
- HOW to write and maintain docs: [docs/README.md](docs/README.md). Do not repeat it here.

## 6. When unsure

- Docs are missing or two docs conflict → STOP. Name both sources and ask.
- You meet an OPEN QUESTION → do not assume an answer. Ask, or work only on what is not blocked.
- A recommendation in `OPEN_QUESTIONS.md` is advice, not a decision. MUST NOT build on it until its `Decision` is filled in.
- Precedence on conflict: [RULES_AND_CONSTRAINTS](docs/RULES_AND_CONSTRAINTS.md) (top of file).

## 7. End of session

Run the [`/end-session`](.claude/skills/end-session/SKILL.md) skill. It covers these steps:

1. Overwrite [STATUS.md](STATUS.md) with these sections: done / in progress / blocked / next. Never append. Keep it at 50 lines or fewer.
2. If you made an architectural decision, propose an ADR ([process](docs/README.md#adr-process)).
3. Report which docs you updated, and which docs you were unsure about.

## 8. Recurring AI mistakes

Add one line per mistake when it happens: what went wrong → what to do instead.

<!-- none yet -->
