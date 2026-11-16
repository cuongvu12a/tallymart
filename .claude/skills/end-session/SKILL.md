---
name: end-session
description: Use at the end of every working session, before the final report. Trigger phrases - "/end-session", "end of session", "wrap up", "let's stop here", "finish for today", "update STATUS".
---

# End a session

Checks that docs match what changed, then overwrites [STATUS.md](../../../STATUS.md). The rules for this are in [CLAUDE.md: End of session](../../../CLAUDE.md#7-end-of-session) and the [sync table](../../../CLAUDE.md#5-keeping-docs-in-sync-must-checked-before-you-report-a-task-as-done). Do not copy the table here; read it.

## Stop and ask when

- Tests or lint fail → STOP before writing "done" anywhere. Put the work under "In progress" or "Blocked" with the failure (R-TEST-01).
- A change needs a doc update, but you are not sure what the doc should say → STOP. Ask; do not guess.
- The diff touches a file you must not edit (`.env*`, merged migrations, `packages/api-client/`) → STOP and report it (R-REPO-01 to R-REPO-03).

## Steps

1. List what changed in this session:
   ```
   git status --short
   git diff --stat
   ```
   Add commits made in this session, if any: `git log --oneline` since the session started.
2. Run tests and lint: `TODO (TM-repo-setup)`. Until the commands exist, write "tests and lint: not available yet" in the report.
3. Walk the sync table row by row. For each row, write one of: "updated <file>", "not needed: <reason>", or "unsure: <reason>". Pure refactors, formatting, and internal renames need no doc change.
4. Make the doc updates found in step 3. Set `last_verified` only on docs you actually compared with the code.
5. If `scripts/check-docs.sh` exists, run it and fix what it reports. If it does not exist, say so in the report.
6. If an architectural decision was made, propose an ADR with the `propose-adr` skill.
7. If you made a mistake that an AI could repeat, propose one line for CLAUDE.md "Recurring AI mistakes". Add it only after the owner agrees.
8. Overwrite `STATUS.md`. Never append. Keep these sections: Done / In progress / Blocked / Next, plus `Last updated: <today>`. Remove items that are no longer true. Keep it at 50 lines or fewer:
   ```
   wc -l STATUS.md
   ```
9. Final report: what was done, the test and lint result, the result of step 3 row by row, ADRs proposed, and anything unsure.

## Edge cases

- Nothing changed in the session → still update "Last updated" and "Next" in STATUS.md if the plan changed; otherwise say "no changes" and stop.
- Work is half done → describe it under "In progress" with the exact next step, so the next session can continue without asking.

Done when: every sync-table row has a result, the needed docs are updated, `check-docs.sh` has run (or is reported missing), STATUS.md is overwritten and has 50 lines or fewer, and the final report lists the test and lint result.
