# STATUS

Overwrite this file at the end of every session. Never append. Keep it at 50 lines or fewer.

Last updated: 2026-11-21

## Done

- Documentation foundation, product discovery ([docs/product/EPICS.md](docs/product/EPICS.md)) and the 2026-11-16 consistency review.
- 2026-11-21: every open question closed except Q-51. Decisions moved into rules, domain docs, GLOSSARY, ARCHITECTURE and CONVENTIONS; every epic has a Decision.
- Build order decided: Inventory first, Ledger before Payment; the Build order is the plan ([PROJECT_OVERVIEW: Build order](docs/PROJECT_OVERVIEW.md#build-order)).
- Non-goals and [learning extensions](docs/PROJECT_OVERVIEW.md#learning-extensions) recorded.
- AI may keep [LEARNING_MODE](docs/LEARNING_MODE.md) in sync. [docs/learning-notes/](docs/learning-notes/README.md) started (Vietnamese study notes, 11 files).
- Branch `docs/close-open-questions` pushed (commits 4d258e5, b9facb3 and this STATUS update). PR to be opened and merged by the owner: https://github.com/cuongvu12a/tallymart/pull/new/docs/close-open-questions

## In progress

- Nothing.

## Blocked

- Nothing blocks TM-repo-setup or Inventory.
- AI cannot open PRs: `gh` CLI is not installed (`brew install gh`, `gh auth login`).

## Next

1. Owner opens and merges the PR above on GitHub.
2. TM-repo-setup (Build-order step 0): pnpm monorepo, NestJS `apps/api`, ESLint + Prettier + `eslint-plugin-boundaries`, Jest + Testcontainers, Docker Compose for PostgreSQL (pick the version; UUIDv7 needs 18, unverified). Ask the owner before pinning versions. Then fill CLAUDE.md "Commands" and a runbook.
3. Step 0 continued: `Idempotency-Key` table, Catalog tables with seed data, Identity stub behind a "current user" interface.
4. Step 1: Inventory spec with `/start-spec`; owner stubs for L-15, L-16 (three-strategy lab), L-12, L-20 (Inventory tables).

## Owner to-do

- Approve or write the 11 ADRs proposed in [docs/decisions/README.md](docs/decisions/README.md).
- LEARNING_MODE rows still `OWNER TO CONFIRM`: L-02 (one provider key), L-04 (no candidate left), L-11 (first endpoint), L-20 (Order price snapshot), and older marked rows.
- Confirm the 9 rule reasons marked "(proposed by AI, owner to confirm)" and the open items in [.claude/reviews/consistency-2026-11-16.md](.claude/reviews/consistency-2026-11-16.md).
- Read the learning notes and tick "Owner đã đọc".
- Deferred: `/update-tour`; SYSTEM_TOUR still shows the closed questions as open.
- Q-51 (where ownership checks live) before Build-order step 9.
