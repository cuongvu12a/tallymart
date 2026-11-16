---
name: propose-adr
description: Use when a technology, library, or major structure is chosen or changed, when a closed open question is architectural, or when the owner asks to record a decision. Trigger phrases - "/propose-adr", "write an ADR", "record this decision", "propose an ADR for X", "we chose X over Y".
---

# Propose an ADR

Creates a proposed ADR in [docs/decisions/](../../../docs/decisions/README.md). The process and the extra frontmatter fields are in [docs/README: ADR process](../../../docs/README.md#adr-process). Template: [0000-template.md](../../../docs/decisions/0000-template.md).

## Stop and ask when

- Nobody has made the decision yet → STOP. An ADR records a decision; it does not make one. If it is still a question, add or update it in [OPEN_QUESTIONS](../../../docs/OPEN_QUESTIONS.md) instead.
- The change would edit an ADR with `decision_status: accepted` → STOP. Write a new ADR that supersedes it.
- The decision adds a dependency the owner has not approved → STOP and ask first (R-REPO-04).
- The decision conflicts with an accepted ADR, but the owner did not say it replaces it → STOP. Name both.

## Steps

1. Find the next number: the highest `NNNN` in `docs/decisions/` plus 1, with four digits. `0000` is the template.
2. Copy the template to `docs/decisions/NNNN-<short-name>.md`. Remove the instruction lines.
3. Set frontmatter: `status: draft`, `decision_status: proposed`, today's `last_verified`, `supersedes: []` or the replaced numbers, `related_code: []` unless the paths exist.
4. Context: the problem, the rule IDs and core invariants affected, and the `Q-NN` it answers. If it comes from an open question, link to it; do not copy its analysis.
5. Options: the options that were really considered, with pros and cons. For an answered question, link to its Options table and add only what is new.
6. Decision: the chosen option in one or two sentences, using MUST / MUST NOT. It MUST match the owner's words.
7. Consequences: what gets easier, what gets harder, and which docs and rules change.
8. Verification: a test, lint rule, or script that checks the code follows the decision. If none exists yet, write `TODO (TM-xx)` or `TODO (TM-repo-setup)`.
9. Add a row to the index in `docs/decisions/README.md`. If it comes from the "ADRs to be written" table, remove that row. If it supersedes an ADR, mark the old one as superseded in the index only.
10. Report the ADR path and ask the owner to accept or reject it.

## Edge cases

- The owner accepts → only the owner, or you on the owner's word, sets `decision_status: accepted` and `status: active`. After that, the file is never edited.
- The owner rejects → set `decision_status: rejected`. Keep the file; the number is not reused.

Done when: the ADR file exists with the next number, `decision_status: proposed`, all sections filled or marked `TODO`, it is listed in the decisions index, and the owner has been asked to accept or reject it.
