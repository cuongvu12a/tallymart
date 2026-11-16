---
status: draft
owner: Cuong Vu
last_verified: 2026-11-15
applies_to: [backend, repo]
related_code: []
---

# Runbooks

This folder is empty on purpose. No code exists yet, so there is nothing to run or operate.

## What goes here

One file per task, named `<task>.md` ([naming](../CONVENTIONS.md#file-names-in-docs)). A runbook tells a person how to do one operational task, step by step, with real commands.

| Kind of runbook | When it gets written |
|---|---|
| Set up and run the system locally | When the repo setup work item (TM-repo-setup) is done |
| Environment variables: name, purpose, where the value comes from | When the first variable is added |
| Recover from a failure (for example, messages in the DLQ, a failed reconciliation run) | When the feature that can fail is built |

## Rules for a runbook

- Every command MUST be real and tested. If it does not exist yet, write `TODO (TM-xx)`. MUST NOT invent commands.
- Every runbook MUST say how to check that the task worked.
- Secrets MUST NOT appear in a runbook. Name the variable and where to get it instead.
