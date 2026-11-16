---
status: active
owner: Cuong Vu
last_verified: 2026-11-16
applies_to: [docs]
related_code: []
---

# How to write and maintain docs

This file says HOW to write docs. WHEN to update them is in the sync table in [CLAUDE.md](../CLAUDE.md#5-keeping-docs-in-sync-must-checked-before-you-report-a-task-as-done). That table lives only there.

> OPEN QUESTION Q-48: Which file owns the doc process when this file, CLAUDE.md and the skills disagree? DO NOT assume. → [details](OPEN_QUESTIONS.md#q-48)

> OPEN QUESTION Q-45: How do epics and enabling work become the plan? DO NOT assume. → [details](OPEN_QUESTIONS.md#q-45)

## Sources of truth

| Source | What it may back up |
|---|---|
| [README.md](../README.md) | Product, problem, contexts, stack, integrations |
| The owner's project brief | Repo rules (R-REPO, R-WEB, R-DOC, R-TEST-01, R-INT-02), language, team, TM-xx IDs |
| A filled-in `Decision` in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) | The answer to that question |
| An ADR in [decisions/](decisions/README.md) with `decision_status: accepted` that the index does not mark as superseded. A proposed or rejected ADR is not a source | That decision |

Anything else MUST be written as an OPEN QUESTION (see [below](#open-questions)).

## Frontmatter

Every file in `docs/` MUST start with this block:

```yaml
---
status: draft | active | deprecated
owner: Cuong Vu
last_verified: YYYY-MM-DD
applies_to: [backend, ordering]
related_code: []
---
```

| Field | Meaning | Allowed values |
|---|---|---|
| `status` | Lifecycle state of the doc | `draft`, `active`, `deprecated` |
| `owner` | The person who approves changes | A person's name |
| `last_verified` | The last date someone compared this doc with the code | `YYYY-MM-DD` |
| `applies_to` | Tags for the area | `backend`, `web`, `docs`, `repo`, or a context name in lower case (`ordering`, `inventory`…) |
| `related_code` | Path prefixes of the code this doc describes | `[]` or existing paths |

ADR files add two fields. See [ADR process](#adr-process).

### `status` lifecycle

`draft → active → deprecated`

| Status | Meaning | Rule |
|---|---|---|
| `draft` | Content is not approved, or has open questions | MAY change freely |
| `active` | Approved by the owner and true for the code | Change it only together with the code, or after the owner approves |
| `deprecated` | Replaced or no longer true | MUST name its replacement on the first line under the title: `Replaced by: [X](X.md)` |

### `last_verified`

- Change it ONLY after you have actually compared the doc with the code.
- MUST NOT change the date without checking. A date that nobody checked makes the field useless, because the audit trusts it.
- While no code exists, `last_verified` is the date the doc was written or checked against the README and the brief.

### `related_code`

- List path prefixes. Prefer folders over single files: ✅ `apps/api/src/<module>/` ❌ ten single files.
- `scripts/check-docs.sh` and the [`/audit-docs`](../.claude/skills/audit-docs/SKILL.md) skill both read this field. It is the only map from code to docs. MUST NOT create a second mapping file, because two maps drift apart.
- MUST stay `[]` until the code exists. MUST NOT add paths that do not exist yet.

## One topic per file

- One topic per file. Stay under about 300 lines. Use headings that say what the section is about.
- Each fact lives in exactly one place. Everywhere else links to it. Do not copy the README; link to it.
- Exception: [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md) MAY be longer. It is read only on demand.

## Writing rules

| Rule | ✅ | ❌ |
|---|---|---|
| Use RFC 2119 words | "MUST reject" | "should ideally reject", "consider" |
| One concept, one word | `Order` | "purchase" in one file, "order" in another |
| Conditional rules go in tables | condition → behavior → example | a paragraph of "if… unless…" |
| Edge cases get their own section | `## Edge cases` | edge cases hidden in prose |
| A prohibition states the reason and the alternative | "Do not use X because Y → use Z" | "Do not use X" |
| Commands are real or marked | `TODO (TM-repo-setup)` | a command that does not exist |
| Plain English | short sentences, common words | idioms. Vietnamese appears only where [R-DOC-03](RULES_AND_CONSTRAINTS.md#r-doc-03) allows it |

## Rule IDs

Format: `R-<AREA>-NN`, for example `R-INV-01`.

- Every rule has an ID, a reason, an alternative (for prohibitions), a source, and a ✅ / ❌ example.
- Put an anchor before each rule heading so links stay stable: `<a id="r-inv-01"></a>`.
- A deleted ID is never reused. Mark the rule `(removed YYYY-MM-DD: reason)` and keep the heading.
- Numbers go up within an area: the next rule after `R-INV-04` is `R-INV-05`.

### Area codes

This is the only table of area codes.

| Code | Area | Rules live in |
|---|---|---|
| `ARCH` | Architecture, module boundaries | [RULES_AND_CONSTRAINTS.md](RULES_AND_CONSTRAINTS.md) |
| `API` | HTTP API | [RULES_AND_CONSTRAINTS.md](RULES_AND_CONSTRAINTS.md) |
| `EVT` | Events and messaging | [RULES_AND_CONSTRAINTS.md](RULES_AND_CONSTRAINTS.md) |
| `INT` | External integrations | [RULES_AND_CONSTRAINTS.md](RULES_AND_CONSTRAINTS.md) |
| `TEST` | Tests, CI, measurements | [RULES_AND_CONSTRAINTS.md](RULES_AND_CONSTRAINTS.md) |
| `WEB` | Web app | [RULES_AND_CONSTRAINTS.md](RULES_AND_CONSTRAINTS.md) |
| `REPO` | Repo hygiene | [RULES_AND_CONSTRAINTS.md](RULES_AND_CONSTRAINTS.md) |
| `DOC` | Docs, terms, language | [RULES_AND_CONSTRAINTS.md](RULES_AND_CONSTRAINTS.md) |
| `IDN` | Identity | [domain/identity.md](domain/identity.md) |
| `CAT` | Catalog | [domain/catalog.md](domain/catalog.md) |
| `ORD` | Ordering | [domain/ordering.md](domain/ordering.md) |
| `INV` | Inventory | [domain/inventory.md](domain/inventory.md) |
| `PAY` | Payment | [domain/payment.md](domain/payment.md) |
| `LED` | Ledger | [domain/ledger.md](domain/ledger.md) |
| `REC` | Reconciliation | [domain/reconciliation.md](domain/reconciliation.md) |
| `SHP` | Shipping | [domain/shipping.md](domain/shipping.md) |
| `NTF` | Notification | [domain/notification.md](domain/notification.md) |
| `INVC` | Invoicing | [domain/invoicing.md](domain/invoicing.md) |

## Open questions

All open questions live in [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md). Every question has a stable ID `Q-NN`. An ID is never reused.

In any other doc, an open question is ONE line that links to it:

```
> OPEN QUESTION Q-07: <short question>. DO NOT assume. → [details](../OPEN_QUESTIONS.md#q-07)
```

Options, analysis and recommendations live ONLY in `OPEN_QUESTIONS.md`. A recommendation is advice. MUST NOT write it into another doc as a fact.

### Adding a question

1. Take the next free number.
2. Add it to the summary table and write the full entry: Context, Options, Recommendation, `Decision: _pending_`.
3. Mark it ★ if it MUST be answered before the first module is built.
4. Add the one-line OPEN QUESTION in each affected doc.

### Closing an open question

| Step | Who | Action |
|---|---|---|
| 1 | Owner | Writes the decision under `Decision` in `OPEN_QUESTIONS.md` |
| 2 | AI or owner | Moves the answer into the affected docs, as rules with IDs where it is a rule |
| 3 | AI or owner | Replaces each one-line OPEN QUESTION with the answer, or with a link to it |
| 4 | AI or owner | Proposes an ADR if the decision is architectural ([ADR process](#adr-process)) |
| 5 | AI or owner | Sets the question's status to `answered` and links to where the answer now lives |

The entry stays in `OPEN_QUESTIONS.md` as a record. It is never deleted.

### Merging duplicate questions

When two Q-IDs ask the same question: keep one (usually the older or broader), move the other's context and options into it, and set the other's status and `Decision` to `merged into Q-xx` in both the summary table and its section. The merged ID is never reused. Re-point every link to the kept ID. Source: owner instruction, 2026-11-16.

## ADR process

ADRs live in [decisions/](decisions/README.md) as `NNNN-<short-name>.md`.

1. Copy [decisions/0000-template.md](decisions/0000-template.md). Take the next number after the highest existing one.
2. Set `decision_status: proposed`. The owner accepts or rejects it.
3. After it is `accepted`, an ADR MUST NOT be edited, because it records what was decided and why at that time.
4. To change a decision, write a new ADR with `supersedes: [NNNN]`. Update the index in [decisions/README.md](decisions/README.md) to show the old one as superseded.

| Extra field | Allowed values |
|---|---|
| `decision_status` | `proposed`, `accepted`, `rejected` |
| `supersedes` | `[]` or a list of ADR numbers |

## Templates

| Doc type | Template | File name |
|---|---|---|
| Domain doc | [domain/_template.md](domain/_template.md) | `docs/domain/<context>.md` |
| Spec | [specs/_template.md](specs/_template.md) | `docs/specs/TM-xx-<short-name>.md` |
| ADR | [decisions/0000-template.md](decisions/0000-template.md) | `docs/decisions/NNNN-<short-name>.md` |

## Tools

| Tool | What it does | When to run it |
|---|---|---|
| `scripts/check-docs.sh` | Reports docs whose `related_code` paths changed while the doc itself did not. Modes: working tree (default), `--staged`, `--hook`, or a commit range | Before you report a task as done |
| [`/audit-docs`](../.claude/skills/audit-docs/SKILL.md) | Finds drift between docs and code (stale rules, broken links, wrong synonyms, answered open questions), and runs consistency checks between docs even when no code exists | When asked, and before you close a sprint |
| [`/end-session`](../.claude/skills/end-session/SKILL.md) | Walks the sync table against the session's changes, then overwrites STATUS.md | At the end of every session |
| [`/start-spec`](../.claude/skills/start-spec/SKILL.md) | Creates a TM-xx spec from the template; stops on open questions the work needs | Before writing code for a TM-xx issue that changes behavior |
| [`/close-question`](../.claude/skills/close-question/SKILL.md) | Moves an owner's decision from OPEN_QUESTIONS.md into the affected docs | After the owner fills in a `Decision` |
| [`/propose-adr`](../.claude/skills/propose-adr/SKILL.md) | Creates a proposed ADR with the next number and adds it to the index | When a technology, library or major structure is chosen or changed |
| [`/invariant-test`](../.claude/skills/invariant-test/SKILL.md) | Writes tests that prove R-INV-01, R-LED-01 and R-PAY-01, using fakes only | When a change touches stock, payments, IPNs or ledger entries |
