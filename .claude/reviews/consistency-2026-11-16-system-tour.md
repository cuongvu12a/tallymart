# Consistency review: SYSTEM_TOUR.md, 2026-11-16

Scope: `docs/overview/SYSTEM_TOUR.md` against its `derived_from` sources. The owner asked for this check and approved, ahead of time, every fix that the sources settle. No code exists yet, so this review ran only the consistency checks (`/audit-docs` step 4b). The checks ran as three separate reviewers: A (rules and decisions), B (facts and terms), C (epics and questions).

Note: step 4b of `/audit-docs` leaves derived files in `docs/overview/` out of its scope. This review covered the tour only because the owner asked for it. See O-06.

## Fixed (the sources settle these)

| ID | Sev | Tour (before) | Source | Fix applied |
|---|---|---|---|---|
| C-01 | Blocker | "in the order the task brief asked for" (4.1) | none; the same list is the "proposal only" step list in Q-25 | Now says the diagrams follow the step list that Q-25 proposes, which is a proposal, not a decision |
| C-02 | Major | "Use the Stock reservation (Stock deduction)" | "Stock deduction" is not a GLOSSARY term; R-INV-03 says "used" | "Use the Stock reservation (R-INV-03) · how ❓Q-14 · step ❓Q-25" |
| C-03 | Major | "you get an E-invoice after delivery" (Buyer); B10 drawn as Core | Q-30: who receives an e-invoice is pending | Now says who receives it is not decided; B10 is now an undecided step with ❓Q-30 |
| C-04 | Major | "`Delivered` triggers ... the Seller's money" (4.3) | ledger.md R-LED-03: what counts as successful delivery is not decided (Q-20) | Now says Invoicing and Ledger react to `Delivered`, and links Q-20 |
| C-05 | Major | Solid S1 → eKYC → list Products | Q-11: when eKYC is required is pending | eKYC is now a branch labelled "when ❓Q-11" |
| C-06 | Major | Solid path from Admin sign-in to the nightly job | reconciliation.md R-REC-01: the job runs every night | The Admin sign-in no longer leads to the job |
| C-07 | Major | Cancellation drawn and listed as Core | The README does not mention Cancellation; it comes from EP-14 | Cancellation is now Proposed (EP-14) in the Buyer table, the journey and the state diagram. Refund stays Core |
| C-08 | Major | "Not allowed: commit, then publish" | R-EVT-01 applies this "once the Outbox exists"; when to build the Outbox is Q-26 | Added "Once the Outbox exists" and ❓Q-26 |
| C-09 | Major | `PAY->>ORD: Payment result` | No source draws a Payment → Ordering edge | Replaced the arrow with a note: there is no such arrow in the README; how Ordering learns the result ❓Q-02 ❓Q-25 |
| C-10 | Major | Solid "Sold out" reply | An honest "sold out" comes only from EP-04 | Now a dotted arrow labelled EP-04 |
| C-11 | Major | "If a Product shows as available, you can really buy it" | This is the EP-04 detail; the tour marks it Proposed | Replaced with "Stock is never oversold" (R-INV-01) |
| C-12 | Major | `LED --> Seller` arrow (big picture) | The README names no context that pays the Seller | Now `TallyMart --> Seller` |
| C-13 | Minor | "pays through a Payment gateway: VNPay, QR bank transfer or card" | GLOSSARY: gateways are VNPay, SePay, Stripe; card and QR are payment methods | Reworded: the Buyer pays by these methods *through* a gateway |
| C-14 | Minor | Marketplace fee note placed at payment time | Q-19: taken at payment or at delivery is pending | Note now says "at payment or at delivery ❓Q-19" |
| C-15 | Minor | "Same IPN again (up to 10 times)" | The README uses 10 only as an example | Now "(README example: 10 times)" |
| C-16 | Minor | Missing markers | ordering.md (timeout: Q-22); GLOSSARY Cancellation (Q-38, Q-25); Q-25 step order | Added ❓Q-22 to the timeout branch, ❓Q-38 to Cancel, and a ❓Q-25 note to 4.1b |
| C-17 | Minor | Failure table rule cell and "Shown in" cell | R-ORD-02 is the saga rule; 4.1a does not draw the rate limit | Added R-ORD-02; the "Shown in" cell now says the rate limit is not drawn |
| C-18 | Minor | "## 5. Order life cycle" | GLOSSARY forbids "order lifecycle (as a name)" | Heading is now "5. Order state machine" (the anchor `#s5` did not change) |
| C-19 | Minor | "accounts ❓Q-18" | GLOSSARY forbids "account (alone)" | Now "Ledger accounts" |
| C-20 | Minor | 14 GLOSSARY terms used before they were explained; 10 never explained | Task rule: explain each term at its first use | Explanations moved to first use (section 1, the section 2 context table, the 4.1 intro, table cells). Added the missing ones: Price, Return window, Available money, Shipping quote, Shipping label, Seller tax withholding, Product review, Seller rating, Notification, Payment method, COD, Oversell |
| C-21 | Minor | Admin table row "COD money from Carriers reconciled" | EP-22 Benefits names only BUY | Row removed from the Admin table |
| C-22 | Minor | Buyer notification row was all Proposed | The README draws `OrderPaid → Notification` | Split: the `OrderPaid` notification is Core (recipient ❓Q-29); the other steps are Proposed (EP-11) |
| C-23 | Minor | "Stock per Product or Variant" (Core) | Where Stock lives is Q-13 | Now "Stock, never oversold" |
| C-24 | Minor | Ledger corrections row cited EP-08 alone | The README says "append-only"; R-LED-02 | Row now cites R-LED-02 |
| C-25 | Minor | EP-18 rows missing Q-20; "Decisions that affect" lists missing Q-IDs; Q-21 described as "payment methods" | EPICS EP-18; Q-21 is "Payment method → provider mapping" | Added Q-20 to both EP-18 rows. Added Q-25, Q-29, Q-30, Q-38, Q-39 (Buyer), Q-18, Q-36, Q-37 (Seller) and Q-11 (Admin). Q-21 now reads "which provider serves each Payment method" |
| C-26 | Minor | "Run a flash sale" (Seller) | Whether a Seller sets aside Stock and a Price is Q-17 | Now "Flash sale · the Seller's part ❓Q-17" |

All checks passed after the fixes:
- 602 links resolve.
- All 38 Q-IDs and 31 epic IDs exist.
- All 13 diagrams render (Mermaid 11.4.1, headless Chrome).
- Section 7 was regenerated from the file.

## Left for the owner

| ID | Sev | Finding | Options |
|---|---|---|---|
| O-01 | Major | 4.1a and 4.1b draw the steps in the order of the Q-25 "proposal only" list, marked ❓Q-25. A recommendation must not be built on, but here it is shown, labelled as a proposal, so the steps can be read. | Keep as is, or show the steps without any order (for example a table) until Q-25 is decided |
| O-02 | Major | Ordering runs the saga, so it must learn the payment result, but no source draws a Payment → Ordering edge. ARCHITECTURE "Edges that other docs need" does not list it. | Extend Q-02 to cover this return path, or add a new Q-ID and a line in ARCHITECTURE |
| O-03 | Minor | The context table in section 2 restates the README table, which ARCHITECTURE calls "the only list". It now also carries the plain explanations of terms. | Keep it as an allowed summary in a derived view, or replace it with a link |
| O-04 | Minor | "Seller account" and "Admin account" (feature rows) name the user account. GLOSSARY forbids "account (for the person)". This is a borderline case. | Keep, or rename to "Seller sign-up" / "Admin sign-in" |
| O-05 | Minor | Section 5 was named "Order life cycle" in the owner's brief. It was renamed because of the GLOSSARY ban. | Confirm |
| O-06 | Minor | `/audit-docs` step 4b leaves `docs/overview/` out of its scope, so a derived view is never checked against its sources unless someone asks. | Add a "derived views" check to `/audit-docs`, or rely on `/update-tour` |
