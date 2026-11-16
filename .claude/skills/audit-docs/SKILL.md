---
name: audit-docs
description: Use when the user says "audit docs", "/audit-docs", "check docs against code", "check docs for consistency", or before closing a sprint. Finds drift between docs/ and the code, and contradictions between docs, that per-change checks miss; reports them, and edits docs only after the user approves.
---

# Audit docs

Find places where `docs/` no longer matches the code. Report first. Edit only after approval.

How docs are written (frontmatter, rule IDs, open questions): [docs/README.md](../../../docs/README.md).

## Edge case: no code yet

If the repo has no application code (no `apps/` folder, or every `related_code` in `docs/` is `[]`):
1. Say: "No code exists yet. Only the cross-checks and the consistency checks were run."
2. Run only step 4 and step 4b. Then report (step 5) and stop.

## Step 1: Select docs

1. List every `.md` file in `docs/`. Skip templates: files whose name starts with `_`, and `docs/decisions/0000-template.md`.
2. Read each file's frontmatter. Keep files with `status: active` or `status: draft`.
3. Select a file if EITHER:
   - `last_verified` is more than 21 days before today, OR
   - code under any `related_code` path changed since `last_verified`:
     ```
     git log --since=<last_verified> --oneline -- <path>
     ```
     Any output = changed.
4. List the selected files and why each was selected.

## Step 2: Map rules to code

For each rule ID (`R-<AREA>-NN`) in a selected doc:
- Search the paths in that doc's `related_code` for the code that enforces the rule. Search for the rule ID first (tests and comments cite it, per R-DOC-02), then for the behavior.
- Note the file and line.

## Step 3: Classify

| Mark | Meaning |
|---|---|
| ✅ | The code matches the rule |
| ⚠️ | The code exists but behaves differently from the rule |
| ❓ | No code found for the rule |
| 🕳 | Code behavior under `related_code` that no rule describes (list it separately) |

Read the code before you choose a mark. Do not mark ✅ from the file name alone.

## Step 4: Cross-checks (run on ALL docs in `docs/`, plus `CLAUDE.md` and `STATUS.md`)

1. **Broken links:** every relative link points to an existing file. For `#anchor` links, the anchor exists (an `<a id="...">` tag or a heading slug).
2. **Synonyms:** for each term in [GLOSSARY](../../../docs/GLOSSARY.md), search docs and code for its "DO NOT use" words. Report each hit with file and line. Ignore the GLOSSARY itself.
3. **Language:** Vietnamese text appears only in the GLOSSARY "Vietnamese (spoken)" column.
4. **Open questions answered by code:** for each question in [OPEN_QUESTIONS](../../../docs/OPEN_QUESTIONS.md) with status `open`, check whether the code already shows a choice. If it does, report it. Do NOT close the question; the owner decides.
5. **`related_code` paths:** every path exists.
6. If `scripts/check-docs.sh` exists, run it and include its output.

## Step 4b: Consistency checks (run even when no code exists)

**Scope:** every file in `docs/` except derived files in `docs/overview/`, plus `CLAUDE.md`, `STATUS.md`, `README.md` and `.claude/skills/*/SKILL.md`.

**Authority:** the sources of truth in [docs/README](../../../docs/README.md#sources-of-truth). Between any other docs there is no winner: report the conflict, never pick a side.

Run the three groups independently (for example as three reviewers that do not see each other's output), then merge.

**A. Rules and domain**
1. For each rule, the ✅ / ❌ examples, the condition table and the edge cases agree. An example MUST NOT answer a case that the rule's own table or edge cases mark "Not decided".
2. No rule, example, epic, GLOSSARY entry or domain text states an answer to a question whose `Decision` is `_pending_`, or a value (number, timeout, limit, role, state, owner context) that the authoritative sources do not give. A recommendation is not a decision.
3. Rule IDs are unique. Every cited `R-…` ID and every `#r-…` / `#q-…` anchor exists. Area codes match the [area-code table](../../../docs/README.md#area-codes). Every rule has a reason, a source and ✅ / ❌ examples; a prohibition also has an alternative.
4. Two rule IDs do not state the same rule. A context rule that applies a cross-cutting rule says "Applies R-xxx".

**B. Cross-file facts and terms**
5. A fact stated in two files says the same thing in both: providers, contexts, events, edges between contexts, roles, phases, states.
6. The README diagram, [ARCHITECTURE: Data flow](../../../docs/ARCHITECTURE.md#data-flow) and the [Build order](../../../docs/PROJECT_OVERVIEW.md#build-order) agree. A solid Build-order edge MUST be backed by the README, in the README's direction.
7. GLOSSARY: grep every "DO NOT use" word and judge each hit against its qualifier. A domain term used in two or more files is defined. A ban with no qualifier does not block a word the docs need (for example "transaction" in "DB transaction"). Role names are the same everywhere.
8. One fact, one place: report README content copied into a doc instead of linked, and any paragraph or table repeated in two files.

**C. Epics and questions**
9. Epic graph: no loops, including dependencies stated only in text (for example "must use EP-14"). Every cited epic ID exists. A summary row lists the same dependencies as its section. An epic scoped `README` does not depend on, or describe the behavior of, an epic scoped `new scope proposal`. Every `README` scope label is backed by README text.
10. Open questions: no question is asked under two IDs; each ID asks one question; every OPEN QUESTION line links to an existing Q-ID; the "Affected docs" column matches the docs that hold the line; summary title and status match the section; no open question is already answered by the README or a decided question; a merged question says "merged into Q-xx".
11. Process: CLAUDE.md, STATUS.md and the skills describe the same process as [docs/README](../../../docs/README.md). Every file, section, script or rule ID that a skill cites exists and says what the skill claims.

**Finding format:** `file:line` (each side) · a short quote of each side (15 words or fewer) · what conflicts · category (contradiction / unbacked claim / duplicate / broken reference / terminology / loop).

**Merge:** dedupe, give each finding an ID `C-NN`, and a severity:
- **Blocker:** breaks the build order or the plan, or an unbacked claim that looks like a decision.
- **Major:** two files say different things about behavior.
- **Minor:** wording, links, formatting.

For each finding propose ONE of: **Fix** (the exact edit, only when the authoritative sources settle it), **Ask** (a new or extended Q-ID with options, a recommendation and `Decision: _pending_`), or **Merge** (duplicate Q-IDs: [docs/README: Merging duplicate questions](../../../docs/README.md#merging-duplicate-questions)).

Write the report to `.claude/reviews/consistency-YYYY-MM-DD.md`, then apply nothing until the owner approves (step 6). Example: [consistency-2026-11-16.md](../../reviews/consistency-2026-11-16.md).

## Step 5: Report

One table per selected doc:

| Rule | Mark | Code location | Note |
|---|---|---|---|

Then:
- 🕳 code with no rule
- Cross-check findings (step 4), grouped by check
- Consistency findings (step 4b): summary counts by severity, then the Blocker and Major rows
- **Proposed edits:** a numbered list. Each item: file, what to change, why, and which finding it fixes.

## Step 6: Apply only after approval

- MUST NOT edit any doc before the user approves the proposed edits. The user MAY approve only some items.
- After approval, apply exactly the approved edits.
- Set `last_verified` to today ONLY for docs you actually compared with the code in steps 2 and 3, or, for consistency fixes, docs you changed and re-checked against the authoritative sources. Do not change it for docs you only link-checked, because the date would then claim a check that never happened.
- If a fix changes a rule, follow [docs/README.md](../../../docs/README.md) (rule IDs are never reused).
- Report which files changed.
