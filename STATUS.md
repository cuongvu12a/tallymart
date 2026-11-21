# STATUS

Overwrite this file at the end of every session. Never append. Keep it at 50 lines or fewer.

Last updated: 2026-11-21

## Done

- Documentation foundation (commit bee4e91): `CLAUDE.md`, `AGENTS.md` (symlink), `docs/`, six skills in `.claude/skills/`, `scripts/check-docs.sh`.
- Product discovery: [docs/product/EPICS.md](docs/product/EPICS.md) (EP-01 to EP-31) and questions Q-33 to Q-42.
- Docs consistency review: [.claude/reviews/consistency-2026-11-16.md](.claude/reviews/consistency-2026-11-16.md). Approved fixes applied; new questions Q-43 to Q-48; Q-33 merged into Q-20; `/audit-docs` now has "Consistency checks" (step 4b). Docs-only Definition of Done (R-TEST-01): links resolve, `check-docs.sh` passes, consistency checks pass.

## In progress

- Nothing. Changes from the consistency review are not committed yet.

## Blocked

- The first module (Inventory, per the decided [Build order](docs/PROJECT_OVERVIEW.md#build-order)) is not blocked by any question.
- The EP-06 ↔ EP-10 loop waits for Q-43.

## Next

1. Owner reviews the open items in the review report ("Left for the owner").
2. Owner confirms the 9 drafted rule reasons marked "(proposed by AI, owner to confirm)".
3. All open questions closed on 2026-11-21 except Q-51 (ownership checks, needed at Build-order step 9). Learning notes (Vietnamese) in docs/learning-notes/.
4. Write the ADRs listed as "to be written" in [docs/decisions/README.md](docs/decisions/README.md).
5. TM-repo-setup: create the pnpm monorepo and real commands, then update CLAUDE.md "Commands".

## Owner to-do (left from round 1, 2026-11-21)

- [docs/LEARNING_MODE.md](docs/LEARNING_MODE.md): round 1 to 3 updates applied. Still OWNER TO CONFIRM: L-11 first endpoint, L-20 Order snapshot, and the other marked rows.
- Q-06 is still ★, but Identity is now Build-order step 9: keep or drop the ★.
- Approve or write the 3 ADRs under "ADRs proposed from closed questions" in [docs/decisions/README.md](docs/decisions/README.md).
- Deferred by the owner: regenerate the system tour (`/update-tour`); it still shows round 1 questions as open.
