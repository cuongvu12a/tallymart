---
name: close-question
description: Use when the owner has filled in a Decision in docs/OPEN_QUESTIONS.md and the answer must move into the docs. Trigger phrases - "/close-question", "close Q-07", "I answered Q-xx", "apply my decision", "move the decision into the docs".
---

# Close an open question

Moves an owner's decision from [OPEN_QUESTIONS.md](../../../docs/OPEN_QUESTIONS.md) into the docs it affects.
The process is defined in [docs/README: Closing an open question](../../../docs/README.md#closing-an-open-question). Follow it; this skill gives the checkable steps.

## Stop and ask when

- The `Decision` is still `_pending_`, or empty → STOP. Only the owner decides.
- The `Decision` is ambiguous: it names no option, mixes options without saying how, or leaves a value open (for example "short TTL") → STOP. Quote the unclear part and ask.
- The decision conflicts with an existing rule or an accepted ADR → STOP. Name both sources.
- The decision changes a rule that code already implements → STOP. Say which code must change; do not change code in this skill.

## Steps

1. Read the full entry for `Q-NN` in `docs/OPEN_QUESTIONS.md`: Context, Options, Recommendation, Decision.
2. Restate the decision in one sentence, using MUST / MUST NOT. Check it against the stop conditions above.
3. Find every reference to the question:
   ```
   grep -rn "Q-NN" docs CLAUDE.md STATUS.md .claude
   ```
   List each file and line.
4. For each affected doc, write the answer where it belongs:
   - A rule → add it with the next free rule ID for its area, with reason, alternative, source (`Q-NN decision`), and ✅ / ❌ examples ([Rule IDs](../../../docs/README.md#rule-ids)).
   - A term → update [GLOSSARY](../../../docs/GLOSSARY.md).
   - A structure or data flow → update [ARCHITECTURE](../../../docs/ARCHITECTURE.md).
   Each fact goes in ONE file. Other files link to it.
5. Replace every one-line `> OPEN QUESTION Q-NN` with the answer, or with a link to where the answer now lives. Re-run the grep from step 3: only `OPEN_QUESTIONS.md` may still mention `Q-NN` as open.
6. If the decision is architectural (a technology, library, or major structure), propose an ADR with the `propose-adr` skill. Do not mark it accepted.
7. In `OPEN_QUESTIONS.md`: set the status to `answered` in BOTH the summary table and the `**Status:**` line of the section, and add under `Decision` a line `Answer now lives in: <links>`. Do not delete the entry.
8. Set `last_verified` to today only on docs you changed AND checked against the README, the brief, or code. No code yet → check against the README and the brief.
9. Report: the decision, the files changed, new rule IDs, the ADR proposed (if any), and anything you were unsure about.

## Edge cases

- The decision makes another open question obsolete → report it; do not close the other question without the owner.
- The decision raises a new question → add it with the next free `Q-NN` ([Adding a question](../../../docs/README.md#adding-a-question)).

Done when: the decision is in the affected docs as rules or facts, no doc outside `OPEN_QUESTIONS.md` shows `Q-NN` as open, the question's status is `answered` with links, and an ADR is proposed if the decision is architectural.
