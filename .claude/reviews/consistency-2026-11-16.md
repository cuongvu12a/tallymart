# Docs consistency review: 2026-11-16

Scope: `docs/` (except `docs/overview/`), `CLAUDE.md`, `STATUS.md`, `README.md`, `.claude/skills/*/SKILL.md`.
Method: three independent reviewers (rules and domain; cross-file facts and terms; epics and questions). They found 158 raw items. After dedupe and verification against the README, 64 findings remain.

Authority used: `README.md`, project-brief rules in `RULES_AND_CONSTRAINTS.md`, and filled-in Decisions. **All 42 Q-IDs are still `_pending_`**, so only README and the brief count.

How a "Fix" is chosen: a Fix is proposed only when (a) the README settles the conflict, or (b) a doc states a pending question's answer as fact. In case (b), the Fix replaces the claim with `Not decided: Q-xx`. That brings back the undecided state and picks no side. Reject (b)-type Fixes if you want them handled differently.

## Summary

| Severity | Count |
|---|---|
| Blocker | 20 |
| Major | 19 |
| Minor | 25 |
| **Total** | **64** |

| Proposal | Count | Q-IDs |
|---|---|---|
| Fix | 54 | — |
| Ask: new Q-ID | 8 | Q-43 to Q-50 (drafts in the appendix) |
| Ask: extend an existing Q | 4 | Q-04, Q-06, Q-27, Q-31 |
| Merge | 1 | Q-33 → Q-20 |
| Owner input (no Q-ID needed) | 2 | C-47, C-49 |

(A finding can carry both a Fix and an Ask.)

The five known findings from the system tour map to C-12 (R-API-01), C-25 (Reconciliation sources), C-01 (EP-06 ↔ EP-10), C-05 (EP-21) and C-03 (EP-11/EP-12). Correction to known finding 4: Q-32 and Q-41 are **not** duplicates of each other. EP-21 cites the wrong question, and no question asks what EP-21 needs (→ Q-44).

## Findings

| ID | Sev | Files | Conflict | Proposal |
|---|---|---|---|---|
| C-01 | Blocker | EPICS.md:114 vs :31, :142; PROJECT_OVERVIEW.md:120,122; README.md:50-57 | **Loop.** EP-06 needs a "Shipping quote from EP-10"; EP-10 needs EP-06 (`OrderPaid`). The summary row for EP-06 hides the EP-10 edge. The Build order puts Shipping (step 8) after Ordering (step 6). README and ARCHITECTURE have no Ordering→Shipping edge for a quote. | **Ask Q-43** (checkout Shipping quote). Fix after: add the EP-10 edge to the EP-06 summary row. |
| C-02 | Blocker | EPICS.md:169 vs :177-178; OPEN_QUESTIONS.md:877 | **Hidden loop.** EP-14 (scope README) says "a Seller … cancels a paid Order". EP-15 says "a Seller cancel must use EP-14" but does not list EP-14. A Seller cancel is Q-38 new scope, and the README never mentions cancellation by a Seller. | **Fix:** EP-14 → "A Buyer or a timeout cancels…; Seller cancel: Not decided: Q-38". EP-15 Depends on: add EP-14. |
| C-03 | Blocker | EPICS.md:148-149, :155-156 vs :39-41; README.md:55; ARCHITECTURE.md:32 | README-scoped EP-11 (notify on "failed delivery", "Refund done") and EP-12 ("after a Refund or partial Return") rely on EP-16/EP-17 (new scope, Q-37). EP-11's notifications also need Shipping/Payment/Ledger→Notification edges. Neither the README nor ARCHITECTURE has those edges (Q-29). | **Fix:** split each epic's text into a README part and an "only if Q-37 adds EP-16/EP-17" part. EP-11 links Q-29 for the extra events. |
| C-04 | Blocker | EPICS.md:162 vs :204; domain/reconciliation.md:27 vs :33; OPEN_QUESTIONS.md:736 | README-scoped EP-13 ("each mismatch gets an owner and is closed with a reason") and reconciliation.md's ✅ example ("reported the next morning") answer mismatch handling. Q-31 leaves that open, and EP-19 (new scope) owns that workflow. | **Fix:** both → "Mismatch handling: Not decided: Q-31". |
| C-05 | Blocker | EPICS.md:218-220, :72; OPEN_QUESTIONS.md:748, :927; README.md:119 | EP-21 says "Scope: README (observability)", but the README never mentions stuck-state detection. EP-21 cites Q-32 (performance targets), while the context map files it under Q-41, whose epic list leaves EP-21 out. It overlaps EP-19 "queues for stuck Orders". Depends on omits EP-07 and EP-12, and no epic owns the DLQ. | **Ask Q-44** (stuck-state detection: scope and home). **Fix:** relabel EP-21 "new scope proposal (Q-44)", remove Q-32, add EP-07 and EP-12 to its dependencies. |
| C-06 | Blocker | PROJECT_OVERVIEW.md:70-79,114,121 vs EPICS.md:13; docs/README.md:141-151; close-question SKILL.md; CLAUDE.md:23-35 | Only `accepted`/`changed` epics enter the plan, but no epic covers Build-order step 0 (repo, ports with fakes, `Idempotency-Key`) or step 7 (Events + Outbox). Epic Decision values are defined nowhere. Closing a question never updates an epic's Scope. `docs/product/` has no row in the CLAUDE.md routing table. | **Ask Q-45** (how epics and enabling work become the plan). |
| C-07 | Blocker | PROJECT_OVERVIEW.md:94,119 vs :118; OPEN_QUESTIONS.md:252; EPICS.md:32 | Ledger before Payment is called "README backs it" (solid `LED --> PAY`, step 5) and "open" (step 4; Q-09 "NOT backed"). EP-07 → EP-08 takes the "backed" side. | **Fix:** make `LED -.-> PAY` dashed, move Ledger in step 5 to the "not backed → Q-09" column, and add "(order: Q-09)" to EP-07's dependency. |
| C-08 | Blocker | PROJECT_OVERVIEW.md:105,122 vs README.md:57 | Solid `LED --> SHP`, with the note "Shipping sends `Delivered` to Ledger, so Ledger must exist". In the README, Ledger *consumes* `Delivered`, so Shipping does not need Ledger. The README reverses this edge. | **Fix:** remove `LED --> SHP` and the step 8 sentence. Add `SHP --> LED` only as a note for step 4/10. |
| C-09 | Blocker | EPICS.md:28-29,31,37 vs PROJECT_OVERVIEW.md:88-90,116-117,124; OPEN_QUESTIONS.md:248-251 | EPICS states as firm the dependencies that the Build order marks "not backed → Q-09": EP-03→EP-01, EP-04→EP-03, EP-06→EP-03, EP-13→EP-07. | **Fix:** annotate each with "(order: Q-09)". |
| C-10 | Blocker | domain/ledger.md:44; EPICS.md:142-143; OPEN_QUESTIONS.md:466 vs :502-508, :782-786; README.md | "The seller's money becomes available after the `Delivered` event" (R-LED-03 ✅, EP-10 "`Delivered` releases money"). The README says only "after successful delivery". Whether a return window applies is Q-20/Q-33, and Q-33 recommends the opposite. | **Fix:** all three → "after successful delivery (README); what counts and when: Not decided: Q-20". |
| C-11 | Blocker | domain/inventory.md:24,27,65; invariant-test SKILL.md:12,38 vs README.md:134 | "Exactly 10 succeed, 40 are rejected" / "fewer than 10 → failure" adds a no-undersell rule. The README requires only "oversold: 0". The example also assumes 1 unit per request, no per-user cap (Q-17) and no rate limit (Q-16). | **Ask Q-46** (is underselling a failure?). |
| C-12 | Blocker | RULES_AND_CONSTRAINTS.md:37 vs :42 | R-API-01 ✅ "The second response returns the first result" answers the row "Same key, same body, first request finished → Not decided: Q-04". | **Fix:** delete the second sentence of the ✅ example. |
| C-13 | Blocker | domain/inventory.md:25; RULES_AND_CONSTRAINTS.md:167 vs OPEN_QUESTIONS.md:399-408; README.md:22 | R-INV-01 forbids "read the stock, check it in application code, then write". That rules out Q-15 options A (`SELECT … FOR UPDATE`) and C. R-DOC-02's ✅ example ("conditional update") is Q-15's recommendation. The README says only "Locking at the DB level". | **Fix:** R-INV-01 → "Stock MUST be protected by locking at the DB level (README). Mechanism: Not decided: Q-15." R-DOC-02 ✅ → "Rejects the reservation when stock is short (R-INV-01)." |
| C-14 | Blocker | domain/inventory.md:58 vs OPEN_QUESTIONS.md:425 | ✅ "One user sending 100 requests per second is throttled" fixes a limit, while Q-16 says to set values after a load test. | **Fix:** → "✅ A user above the per-user limit is throttled. Values: Not decided: Q-16." |
| C-15 | Blocker | domain/ordering.md:38 vs OPEN_QUESTIONS.md:373, :610 | ✅ "Payment fails → reservation released and order closed" builds in Q-14 (reservation timing) and the proposed Q-25 saga (close, not retry). | **Fix:** → "Payment fails → compensation runs (README). Steps: Not decided: Q-25." |
| C-16 | Blocker | domain/identity.md:27; GLOSSARY.md:82; EPICS.md:78,80 vs OPEN_QUESTIONS.md:188-198; README.md:68 | "Only users with the `Seller` role may create a product", the GLOSSARY term "Seller team member", and README-scoped EP-01's "Seller team members", "Admin roles split by job" all fix the role set. Q-06 is open. The README says only "Buyers, sellers, admins … RBAC". | **Fix:** identity.md ✅ → neutral example, mark "Seller team member" as "proposed: Q-06", and move EP-01's team members and Admin split to "Not decided: Q-06". |
| C-17 | Blocker | domain/identity.md:25 vs README.md:68; OPEN_QUESTIONS.md:249 | "Do not check user IDs … to grant access" is unbacked. It also blocks ownership checks (a Seller edits only their own Products or Wallet) that RBAC alone cannot express. | **Ask → extend Q-06** with "ownership checks: allowed, and where?". **Fix:** replace the line with "Not decided: Q-06". |
| C-18 | Blocker | EPICS.md:106-108, :113-115, :127-129, :134, :155 vs OPEN_QUESTIONS.md:440, :481, :508, :715-719, :786 | README-scoped epics state pending recommendations as scope. EP-05 "set aside Stock" (Q-17). EP-06 cart and "full Price incl. Shipping quote" (Q-05, Q-43). EP-08 "fee fixed when the Order is placed" (Q-19). EP-09 "release date per Order, Admin approval above a limit" (Q-33; Q-20 recommends approval for all). EP-12 "Buyers can ask for one" (Q-30 recommends no Buyer invoices). | **Fix:** move each to a "Depends on decision: Q-xx" note in the epic, and keep only README-backed text as scope. |
| C-19 | Blocker | GLOSSARY.md:84,87,89 vs OPEN_QUESTIONS.md:856-862, :950-956 | The GLOSSARY assigns contexts: Return to sender → Shipping, Wallet hold → Ledger, Seller statement → Ledger. Q-37/Q-42 still list ownership as options. | **Fix:** Context column → "Not decided: Q-37" / "Not decided: Q-42". |
| C-20 | Blocker | OPEN_QUESTIONS.md:632-635; PROJECT_OVERVIEW.md:121 vs README.md:25; RULES_AND_CONSTRAINTS.md:55 | Q-26 option B "Publish directly, add the Outbox later" and Build-order step 7 "Outbox at the same time or later?" conflict with README:25 (Transactional Outbox is the README's answer) and R-EVT-01. | **Fix:** mark Q-26 option B "ruled out by README:25 / R-EVT-01". Narrow Q-26 to what is left open (if anything). Step 7 → "Outbox comes with the first event (R-EVT-01)". |
| C-21 | Major | OPEN_QUESTIONS.md:492-508 vs :772-786; EPICS.md (Q-33 links) | **Duplicate.** Q-20 ("when seller money becomes available") and Q-33 ask the same question. Q-20 B equals Q-33 A. | **Merge:** keep Q-20 (older and broader). Mark Q-33 "merged into Q-20" and move its Seller/Buyer context into Q-20. Re-point EPICS links. |
| C-22 | Major | OPEN_QUESTIONS.md:215 vs :322, :810, :829; :466, :730, :508, :569 vs :848 | Q-07's non-goal candidates repeat Q-12 (currency), Q-35 (COD) and Q-36 (vouchers, ads). Q-18 and Q-31 point to Q-07 for COD/coupons. Q-20 and Q-23 point to Q-07/Q-20 for returns, but Q-37 owns returns. | **Fix:** in Q-07, link those candidates to Q-12, Q-35 and Q-36 instead of asking them again. Re-point Q-18 and Q-31 to Q-35/Q-36, and Q-20 and Q-23 to Q-37. |
| C-23 | Major | OPEN_QUESTIONS.md:215 vs README.md:6, :97 | Q-07 candidate "real money or a production launch (sandboxes only)" is already answered: the README says sandbox/staging only. | **Fix:** remove the candidate and cite README:6. |
| C-24 | Major | OPEN_QUESTIONS.md:158 vs RULES_AND_CONSTRAINTS.md:34; README.md:23, :27; OPEN_QUESTIONS.md:671-674 | Q-04's context states as fact that IPNs and carrier webhooks do not take `Idempotency-Key` and "deduplicate by the provider's own ID (R-SHP-01)". The README says "every write API" and "deduplication by event key". Q-28 still lists composite keys. | **Ask → extend Q-04** with an option row for the IPN/webhook exemption. **Fix:** replace "provider's own ID (R-SHP-01)" with "event key (README:27); which key: Q-28". |
| C-25 | Major | README.md:74 + domain/reconciliation.md:13 + GLOSSARY.md:63 + EPICS.md:162 vs README.md:63; ARCHITECTURE.md:48; PROJECT_OVERVIEW.md:124; domain/reconciliation.md:32,41 | **README contradicts itself.** Its context table says gateways + banks + carriers; its diagram shows only gateways. ARCHITECTURE, step 10 and reconciliation.md's own edge cases follow the diagram. Banks have no provider in README:99-106. ARCHITECTURE reads the two-way `REC <-- file / API --> VNP` arrow as "incoming". | **Ask → extend Q-31:** add "README table vs diagram" to Context, plus options (gateways only / + carriers / + banks, with a bank data source). |
| C-26 | Major | EPICS.md:134 vs README.md:95-106 | A Withdrawal pays out to "a verified bank account" and handles a "failed bank transfer". No README integration, port or context makes an outgoing bank transfer. | **Ask Q-47** (how a Withdrawal moves money out). |
| C-27 | Major | ARCHITECTURE.md:40-48, :67-73 vs README.md:59-63, :87, :99-106; domain/identity.md:34 | ARCHITECTURE's external-systems table and repo layout are copied from the README and have drifted. Rows missing: Identity (Keycloak, Google OAuth, FPT.AI OCR) and Public data (provinces API, VietQR). The Reconciliation direction is wrong. | **Fix:** replace the copy with a link to README "Integrations", plus only a Direction column for what the README draws (two-way for REC). |
| C-28 | Major | ARCHITECTURE.md:29-30; domain/payment.md:61; domain/ledger.md:64 vs ARCHITECTURE.md:36; OPEN_QUESTIONS.md:95 | The "Meaning in the README" column says "Payment writes to Ledger" and "reads or writes Ledger". The README draws only an arrow, and call vs event is Q-02. Related lines also leave out the Shipping→Ledger (`Delivered`) edge. | **Fix:** "Meaning" → "README draws an arrow. Call or event: Q-02". Add the missing edges to the Related lines. |
| C-29 | Major | domain/ordering.md:26-28; domain/shipping.md:25,41 vs README.md:27; OPEN_QUESTIONS.md:587-589, :676-678 | "A late 'in transit' for a delivered order is rejected (R-ORD-01)". README:27 backs "a state machine blocks invalid transitions" but does not say which one. Pinning it on the order state machine assumes Q-24 option A. Q-28 says some backward moves can be real. There is no Shipping→Ordering edge. | **Fix:** cite README:27 for the outcome. Whose state machine, and which moves: "Not decided: Q-24, Q-28". |
| C-30 | Major | domain/payment.md:25 vs RULES_AND_CONSTRAINTS.md:42 | R-PAY-01 fixes the reply to a duplicate IPN ("return success"). R-API-01 leaves replay responses to Q-04. | **Fix:** keep "recorded once" (README:135). Reply → "Not decided: Q-04". |
| C-31 | Major | domain/payment.md:28 vs domain/ledger.md:42 | ❌ "10 IPNs → the seller wallet is credited 10 times" implies one IPN credits the wallet. That conflicts with R-LED-03 (pay only after delivery). | **Fix:** ❌ → "10 IPNs → 10 Payments recorded". |
| C-32 | Major | domain/payment.md:50 vs :24 | The edge case "IPN and re-query arrive at the same time → one payment (R-PAY-01)" cites a rule that does not cover this race. | **Fix:** → "Not decided: Q-22". |
| C-33 | Major | domain/ledger.md:51 vs domain/invoicing.md:30; domain/notification.md:39 | A duplicate `Delivered` event is "paid once" in ledger.md but "not decided" in invoicing.md and notification.md. All three depend on Q-27. | **Ask → extend Q-27:** "Must every consumer give one effect per duplicate event?" Align all three to "Mechanism: Q-27". |
| C-34 | Major | RULES_AND_CONSTRAINTS.md:73 vs README.md:51, :59, :70 | R-INT-01 ✅ "`Ordering` calls a payment port" skips the Payment context. In the README, Ordering → Payment → gateway. | **Fix:** → "✅ `Payment` calls a payment-gateway port." |
| C-35 | Major | RULES_AND_CONSTRAINTS.md:107-110 vs README.md:134-135; OPEN_QUESTIONS.md:761 | R-TEST-02 ❌ "oversold: 0 (expected)", yet the README's own "After" column holds "oversold: 0" and "recorded once" with nothing measured. Both sides are authoritative. | **Ask Q-48** (is the Metrics "After" column a target or a measured result?). |
| C-36 | Major | RULES_AND_CONSTRAINTS.md:98-99 vs STATUS.md:7-9; end-session SKILL.md:12 | R-TEST-01 does not say whether a docs-only task can be "done" when tests and lint cannot run. STATUS lists docs work as "Done". | **Ask Q-49** (R-TEST-01 for docs-only tasks). |
| C-37 | Major | CLAUDE.md:15 vs docs/README.md:15-22 | CLAUDE.md: "Sources of truth: README plus the project brief". docs/README adds filled-in Decisions and accepted ADRs. | **Fix:** add filled-in Decisions to CLAUDE.md (your task brief confirms them). Accepted ADRs: confirm, then Fix. |
| C-38 | Major | CLAUDE.md:18,31; start-spec SKILL.md:15 vs PROJECT_OVERVIEW.md:60 | CLAUDE.md and start-spec treat the Build order as "what to build next". PROJECT_OVERVIEW calls it "a proposal … not a decision" (Q-09). | **Fix:** CLAUDE.md and start-spec → "Build order (a proposal until Q-09 is decided)". |
| C-39 | Major | docs/README.md:56,62,158-164; CLAUDE.md:65,95 vs end-session SKILL.md:26,29; propose-adr SKILL.md:21,27,32; decisions/README.md:11; start-spec SKILL.md:23,40; specs/_template.md:48-50 | The process docs disagree. `last_verified` when no code exists (end-session forbids it; CLAUDE.md requires it). Recurring mistakes: CLAUDE.md says add, end-session says propose. ADR statuses: `deprecated` vs `superseded`; `draft`/`active`. start-spec's `R-<AREA>-NEW` is undefined. The spec template invites pending questions that start-spec forbids. | **Ask Q-50** (which file owns the doc process). Then align the others to it. |
| C-40 | Minor | close-question SKILL.md:34 vs docs/README.md:149 | The skill sets only the summary-table status. The section's `**Status:** open` stays stale. | **Fix:** the skill sets both. |
| C-41 | Minor | OPEN_QUESTIONS.md:198 vs :927; EPICS.md:205-206 | Q-06 (Admin powers) and Q-41 (back-office) overlap. Q-41 links Q-06, but Q-06 does not link back. | **Fix:** add "Back-office scope: Q-41" to Q-06. |
| C-42 | Minor | OPEN_QUESTIONS.md:795, :927 vs EPICS.md:46,199, :72,315 | Q-34 lists EP-18, but EP-18 cites Q-37 and Q-33. Q-41's epics leave out EP-21. | **Fix:** align the lists (after C-05 and C-21). |
| C-43 | Minor | EPICS.md:67-69 vs :38,40,48,54,55; EPICS.md:323 vs :315-316 | The context map leaves out EP-14, 16, 22, 29 and 30 (Ledger) and EP-22 (Shipping). Line 323 says "EP-25 to EP-31 … do not reorder", but lines 315-316 say EP-26, 29 and 30 do. | **Fix:** complete the map and reword line 323. |
| C-44 | Minor | EPICS.md:149,156,254 | Missing dependencies: EP-11 (EP-09, EP-14), EP-12 (EP-14), EP-26 (EP-09, EP-14, EP-17). | **Fix:** add them. |
| C-45 | Minor | OPEN_QUESTIONS.md:33,55,56-65 vs CLAUDE.md; PROJECT_OVERVIEW.md; domain/*.md; ARCHITECTURE.md | Affected docs listed for Q-10, Q-32 and Q-33 to Q-42 have no one-line OPEN QUESTION, which docs/README.md:139 requires. | **Fix:** add the lines, or trim the Affected-docs column where a doc is not really affected. |
| C-46 | Minor | OPEN_QUESTIONS.md:25 vs :91 | The Q-02 title differs between the summary table and its section. | **Fix:** use the section title. |
| C-47 | Minor | docs/README.md:92 vs RULES R-DOC-02, R-DOC-03; R-LED-03, R-ORD-03, R-IDN-02, R-PAY-03, R-SHP-02, R-NTF-02, R-INVC-01 | These 9 rules have no Reason, which the rule format requires. | **Owner input:** supply the reasons (the brief rules need your words), or let the rule format make Reason optional. |
| C-48 | Minor | domain/_template.md:33-37 vs all 10 domain docs | The template's "Conditional behavior" section is missing everywhere. | **Fix:** add the section with "None yet." |
| C-49 | Minor | docs/README.md:18 vs RULES_AND_CONSTRAINTS.md:80 | R-INT-02 cites "project brief", but docs/README's list of brief-backed rules leaves it out. | **Owner fact:** does the brief back R-INT-02? Fix whichever side is wrong. |
| C-50 | Minor | domain/ordering.md:43-48; payment.md:42-46; shipping.md:33-37; notification.md:31-35; invoicing.md:21-26 vs RULES R-API-01, R-INT-01 | R-ORD-03 repeats R-API-01. R-PAY-03, R-SHP-02, R-NTF-02 and R-INVC-01 repeat R-INT-01. | **Fix:** keep the IDs (never reused). Each body becomes "Applies R-xxx to <context>" plus the context-specific part. |
| C-51 | Minor | domain/inventory.md:67 vs OPEN_QUESTIONS.md:101, :373 | "Same reserve request twice → one effect (R-API-01)". Whether "reserve" is an HTTP API at all depends on Q-02 and Q-14. | **Fix:** keep "one effect"; mechanism → "Not decided: Q-02, Q-14". |
| C-52 | Minor | domain/inventory.md:24 vs :27 | "Sold or reserved MUST NEVER exceed the stock" vs "10 succeed, stock is 0". The meaning depends on whether a reservation reduces stock (Q-14, Q-15). | **Fix:** → "never exceed the starting stock of 10". |
| C-53 | Minor | invariant-test SKILL.md:8,14,33 vs README.md:130-135; RULES R-TEST-02 | Shape C (ledger sum) says it comes from the README Metrics table; it comes from R-LED-01. "Do not edit the README (R-TEST-02)" cites a rule that does not say this. | **Fix:** cite R-LED-01. Remove the wrong R-TEST-02 citation. |
| C-54 | Minor | start-spec SKILL.md:26 vs CONVENTIONS.md:36-61; PROJECT_OVERVIEW.md; EPICS.md | The skill's grep for blocking questions misses CONVENTIONS, PROJECT_OVERVIEW and EPICS links. | **Fix:** grep `Q-[0-9]+` across `docs/` (except overview). |
| C-55 | Minor | docs/README.md:67 vs :179; CLAUDE.md:75 | "`scripts/check-docs.sh` … reads this field" is in the present tense, but the script does not exist. | **Fix:** → "will read (not created yet)". |
| C-56 | Minor | STATUS.md:9-10, :27 vs `.claude/skills/*`; git log; docs/overview | STATUS is stale: it lists 1 skill (there are 6), says "No commits yet" (there is one), and omits product discovery. Its "proposed README Roadmap edit" exists only in out-of-scope `docs/overview/`. | **Fix:** rewrite at /end-session. Link the Roadmap item to its source. |
| C-57 | Minor | OPEN_QUESTIONS.md:54 vs README.md:26 | Q-31 asks for a "schedule". The README already says "nightly reconciliation job". | **Fix:** Q-31 cites README:26 for the schedule and drops it from the question. |
| C-58 | Minor | RULES:35,74; ordering.md:46,48; inventory.md:27; OPEN_QUESTIONS.md:83,215,218,466,504,651,776,927; EPICS.md:299,331,333; audit-docs SKILL.md:15 | Forbidden synonyms in use: "charge", "service" (for a module), "item", "coupon", bare "hold", "paid out", "history", "Phase 0" as a timeline. README uses "charged", "item" and "Phase 0" itself; the README is not edited. | **Fix:** replace them with GLOSSARY terms (R-DOC-01). |
| C-59 | Minor | GLOSSARY.md:21,31,32,33,43,47,60,72,100,104 | Bans so broad they block needed words. "goods" (the GLOSSARY breaks it 5 times). "transaction" (DB transaction, Transactional Outbox, README). "account" (Ledger account). "option" (decision options). "cost". "message" (DLQ row, README). "member" (Seller team member). "domain" (the `docs/domain/` folder). | **Fix:** add qualifiers, e.g. "goods (as a name for Product)", "transaction (for an Order or Payment)", "account (for a User or Seller wallet)". Allow the `docs/domain/` folder name. |
| C-60 | Minor | GLOSSARY.md (missing) vs OPEN_QUESTIONS, EPICS, domain docs | Terms used but not defined: cart, successful delivery, return window, pending/available money, release, payment method, mismatch, re-query, cancellation, Ledger account. | **Fix:** add them. Where the meaning is pending, write "Definition: Not decided: Q-xx" (e.g. successful delivery → Q-20, Ledger account → Q-18). |
| C-61 | Minor | OPEN_QUESTIONS.md:586-587 vs GLOSSARY.md:104 | `Delivered` is both an Order state (Q-24 options) and a Shipping event. | **Fix:** add the name clash to Q-24's context. |
| C-62 | Minor | EPICS.md:16 vs OPEN_QUESTIONS.md:833,871,889,927,946 | "BA = business analyst" vs "the system analyst" for the same perspective. | **Fix:** use one name. |
| C-63 | Minor | CLAUDE.md:26,65,66 vs CONVENTIONS.md:42 | `docs/domain/<area>.md` vs `<context>`. "Area" is the area code. | **Fix:** CLAUDE.md → `<context>`. |
| C-64 | Minor | CLAUDE.md:9,18,83,91; PROJECT_OVERVIEW.md:15,48-51; GLOSSARY.md:110; STATUS.md:3; end-session SKILL.md:30; RULES:13; domain/{inventory,ledger,shipping,reconciliation}.md:13; OPEN_QUESTIONS.md:246-263 vs PROJECT_OVERVIEW.md:110-124; EPICS.md:297-335 vs OPEN_QUESTIONS Q-33..Q-36 | Content is copied instead of linked. Examples: the goal sentence (×3), "Phase is not a timeline" (×3), the STATUS rule (×3), precedence (×2), domain Purpose lines restating the README (reconciliation's has already drifted, see C-25), Build-order analysis (×2), perspective-conflict analysis (×2). | **Fix:** keep one home for each fact and link to it elsewhere. CLAUDE.md one-liners stay but get a link. |

## Dropped after verification

- EP-04 "Stock reservations with a TTL" called unbacked: README:22 backs it (only the TTL *value* is Q-14).
- R-EVT-01 vs Q-26 "which wins": README:25 settles it in favour of the Outbox (kept as a Fix, C-20).
- `docs/README.md:129` `../OPEN_QUESTIONS.md` link: correct from a doc in a subfolder, which is the example's context.
- `#q-nn` in templates: placeholders by design.
- EPICS `SPRINT_PLAN.md` vs "ignore sprints": CLAUDE.md ignores the README's sprint *numbers*. You do plan sprints, so there is no conflict.

## Appendix: draft new questions (written in full at Step 3)

| Q-ID | Question | Options | Recommendation |
|---|---|---|---|
| Q-43 | Does checkout need a Shipping quote before payment, and how does Ordering get it? | A. Yes: Ordering asks Shipping for a quote (new edge). Split EP-10 into quotes (before EP-06) and shipments (after). B. No quote at checkout (flat or free shipping). C. Ordering computes the fee itself. | A: the README gives Shipping "multi-carrier quotes", and splitting EP-10 breaks the loop. |
| Q-44 | Is stuck-state detection (paid with no Shipment, missing IPN, DLQ growth) in scope, and where does it live? | A. Part of the README observability group (metrics and alerts only). B. Part of the back-office (EP-19, Q-41). C. Later. | A for alerts; queues go to Q-41. |
| Q-45 | How do epics and enabling work become the plan? | A. Add an enabling epic for Build-order steps 0 and 7. Define epic Decision values in docs/README. close-question updates epic Scope. Route `docs/product/` in CLAUDE.md. B. The Build order is the plan, and epics map onto its steps. | A. |
| Q-46 | In the flash-sale test, is selling fewer units than the stock (underselling) a failure? | A. Only oversold = 0 is required (README). B. Also exactly N succeed, under stated test conditions (1 unit per request, no cap, no rate limit). | B as a test condition, not a domain rule. |
| Q-47 | How does a Withdrawal move money to the Seller's bank? | A. A payout port with a fake only (no real provider in scope). B. Pick a provider (e.g. through a gateway's payout API, unverified). C. Manual transfer by an Admin, recorded in the Ledger. | A or C until a provider is chosen. |
| Q-48 | README Metrics "After" column: a target or a measured result? | A. A target: R-TEST-02 then covers only a measured column (add one). B. Measured only: blank the README cells until a script fills them. | A. |
| Q-49 | Does R-TEST-01 apply to docs-only tasks? | A. Docs-only tasks are done when docs checks pass. B. Nothing is "done" until tests can run; docs go under "in progress". | A. |
| Q-50 | Which file owns the doc process when CLAUDE.md, docs/README and the skills disagree? | A. docs/README owns it; CLAUDE.md and the skills link to it and never restate it. B. Each skill owns its own step. | A. |

---

## Step 3: what was applied (2026-11-16)

Owner approval: all 64 items, with these changes. C-20 is not a Fix: Q-26 already asks the owner's question. It was reworded to the owner's text, and R-EVT-01 now says "when to build it: Q-26". C-35 and C-36: no new question; owner decisions were written into R-TEST-02 (README "After" values are targets) and R-TEST-01 (docs-only Definition of Done). C-37: accepted, non-superseded ADRs count. C-49: R-INT-02 cites the brief and the README.

**New and changed question IDs.** Q-48 and Q-49 from the draft appendix were not created, so the numbers moved:
- Q-43 (checkout Shipping quote)
- Q-44 (stuck-state detection)
- Q-45 (epics and enabling work → plan)
- Q-46 (underselling in the flash-sale test)
- Q-47 (Withdrawal bank transfer)
- Q-48 (who owns the doc process; was "Q-50" in the draft)
- Extended: Q-04 (IPN/webhook key and reply), Q-06 (ownership checks), Q-27 (which consumers need one effect), Q-31 (README table vs diagram; source options; schedule removed).
- Merged: Q-33 into Q-20.
- Reworded: Q-26.

**Corrections made during the re-check** (the three reviewers re-ran their checks on the changed files):
- C-07 was wrong. Making only Payment → Ledger dashed was inconsistent, because Ordering → Inventory and Reconciliation → Ledger are the same kind of README arrow and stay solid. Reverted to solid; the README backs it.
- C-55 was wrong. `scripts/check-docs.sh` exists (commit bee4e91). docs/README and CLAUDE.md now describe it and require running it. It passes (exit 0).
- C-08 follow-up: EP-10 no longer depends on EP-08. Ledger consumes `Delivered`.
- Slips fixed:
  - forbidden words in new text ("payout", "held", "goods");
  - the term `Release` renamed to `Money release`;
  - R-IDN-01's prohibition got back its reason and alternative;
  - inventory example no longer assumes stock belongs to a Product (Q-13);
  - Cart pointer corrected;
  - R-ORD-03 no longer fixes one Order per checkout (Q-05);
  - Q-07 no longer claims the README rules out a production launch;
  - R-TEST-01 rule text now points to its own table;
  - R-EVT-01's direct-publish ban now applies "once the Outbox exists".
- The OPEN_QUESTIONS "Affected docs" column was regenerated from the docs that cite each Q-ID.

**C-47 drafts (owner to confirm).** Each rule now has a Reason and an Alternative marked "(proposed by AI, owner to confirm)":

| Rule | Drafted reason |
|---|---|
| R-DOC-02 | An ID lets a reviewer find the rule a change protects, and an audit find every dependent place when the rule changes |
| R-DOC-03 | AI sessions and future readers read every file; plain English leaves less room for a wrong reading |
| R-LED-03 | Until the Buyer has the Products, money may go back to the Buyer; money a Seller withdrew cannot be recovered |
| R-ORD-03 | "Place order" is the write most likely to be repeated; a repeat would create a second Order and Payment |
| R-IDN-02 | The README plans JWT → Keycloak; business code that knows token details would change in every module |
| R-PAY-03 | Payment tests must simulate duplicate, late and missing IPNs, which a sandbox cannot do on demand |
| R-SHP-02 | Shipping tests must send duplicate and out-of-order statuses, which carrier staging cannot do on demand |
| R-NTF-02 | Tests must check what was sent without sending real email, SMS or push to anyone |
| R-INVC-01 | A real e-invoice is a tax document; tests must never issue one by accident |

Every alternative follows the pattern "do not call the provider / do not do X → call the port / do Y".

**Not applied, or partly applied:**
- C-39: Ask only (Q-48). The process conflicts are listed in Q-48 and were not aligned.
- C-64: applied to the goal sentence, the Phase note, precedence, the domain Purpose lines (inventory, ledger, shipping, reconciliation), the Q-09 list, and the sources-of-truth list. Not applied:
  - EPICS "Conflicts between perspectives". Kept as the record of who said what; it now says the analysis lives in the questions.
  - The STATUS rule copy in `/end-session`. That depends on Q-48.
- Mark `docs/overview/SYSTEM_TOUR.md` stale: not done. `docs/overview/` no longer exists in the working tree (it was untracked; nothing in this session deleted it).

## Left for the owner (found by the re-check, not settled by the sources)

| ID | Sev | Files | Conflict | Proposal |
|---|---|---|---|---|
| N-01 | Major | RULES R-TEST-01, R-TEST-02; docs/README "Merging duplicate questions"; OPEN_QUESTIONS Q-26 | These now cite "owner decision, 2026-11-16" or "owner instruction". The docs/README sources-of-truth table does not list that kind of source. | Ask: add a row "a dated owner decision written in the rule's Source line", or record such decisions as answered Q-IDs. |
| N-02 | Major | CLAUDE.md:73; audit-docs step 4b scope | CLAUDE.md has a new row (not from this session) that says to regenerate `docs/overview/SYSTEM_TOUR.md` from `derived_from`. The folder does not exist, and `derived_from` is not in the docs/README frontmatter table. | Owner: restore the folder or remove the row; if it stays, define `derived_from`. |
| N-03 | Major | EPICS EP-14 (Scope: README) | "A Buyer or a timeout cancels a paid Order". The README never mentions cancelling a paid Order (only compensation and a payment timeout). | Ask: extend Q-38 (who may cancel), or relabel EP-14's Buyer cancel as new scope. |
| N-04 | Major | EPICS EP-02, EP-05 (Scope: README) | EP-05 "protection against bots" and "countdown", and EP-02 "an Admin reviews the result", are not in the README. Same pattern as C-18. | Fix in the C-18 style: "Depends on decision" notes (Q-06, Q-17). |
| N-05 | Minor | domain/payment.md edge case; Q-22 | "IPN and re-query arrive at the same time → Q-22". Q-22 is about the schedule and timeout only. Its option C treats the race as covered by R-PAY-01. | Ask: add this case to Q-22 or to Q-04 (IPN repeats). |
| N-06 | Minor | `.claude/reviews/` | This report is linked from `/audit-docs` and OPEN_QUESTIONS, but it is untracked. | Commit it with the docs changes. |
