---
status: draft
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [docs]
related_code: []
---

# Epics

## How to use this file

This file lists the big features (epics) TallyMart could have, found by product discovery from five perspectives on 2026-11-15. It is a catalog of scope, not the plan: the [Build order](../PROJECT_OVERVIEW.md#build-order) is the plan, and epics are mapped onto its steps ([Q-45](../OPEN_QUESTIONS.md#q-45) decision). Epics marked `new scope proposal` are outside the README until their linked question in [OPEN_QUESTIONS.md](../OPEN_QUESTIONS.md#product) is answered. Priorities are recommendations, not decisions. Topics the owner left for later learning: [PROJECT_OVERVIEW: Learning extensions](../PROJECT_OVERVIEW.md#learning-extensions). This file holds no business rules: rules, flows and acceptance criteria are written later, one epic at a time, in `docs/domain/` and `docs/specs/`.

- Epic IDs are stable. MUST NOT renumber or reuse them. A rejected epic keeps its ID and is marked `rejected`.
- Perspectives: **BA** = business analyst (system view), **STR** = business strategist, **BUY** = Buyer, **SEL** = Seller, **ADM** = Admin team (support, operations, finance).
- Invariants: **INV** = [R-INV-01](../domain/inventory.md#r-inv-01) (stock is never oversold), **LED** = [R-LED-01](../domain/ledger.md#r-led-01) (the ledger always balances).
- Claims about law and competitors are not checked (unverified). New terms are in the [GLOSSARY draft section](../GLOSSARY.md#product-discovery-terms-draft).

## Summary

Sorted by priority, then ID.

| ID | Epic | Priority | Contexts | Depends on | Scope | Decision |
|---|---|---|---|---|---|---|
| [EP-01](#ep-01) | Accounts and roles | Must | Identity | none | README | accepted (core) |
| [EP-02](#ep-02) | Seller onboarding and eKYC | Must | Identity | EP-01 | README | accepted (core); eKYC through a Fake only ([R-IDN-04](../domain/identity.md#r-idn-04)) |
| [EP-03](#ep-03) | Product catalog | Must | Catalog | EP-01 (order: [Q-09](../OPEN_QUESTIONS.md#q-09)) | README | accepted (core) |
| [EP-04](#ep-04) | Stock and stock reservations | Must | Inventory | EP-03 (order: [Q-09](../OPEN_QUESTIONS.md#q-09)) | README | accepted (core) |
| [EP-05](#ep-05) | Flash sale | Must | Inventory | EP-04 | README | accepted (core) ([R-INV-06](../domain/inventory.md#r-inv-06)) |
| [EP-06](#ep-06) | Checkout and order placement | Must | Ordering | EP-03 (order: [Q-09](../OPEN_QUESTIONS.md#q-09)), EP-04, EP-07; EP-10 for a Shipping quote ([Q-43](../OPEN_QUESTIONS.md#q-43)) | README | accepted (core); flat Shipping fee, no quote ([R-ORD-06](../domain/ordering.md#r-ord-06)) |
| [EP-07](#ep-07) | Online payment | Must | Payment | EP-08 (order: [Q-09](../OPEN_QUESTIONS.md#q-09)) | README | accepted (core); VNPay only ([R-PAY-03](../domain/payment.md#r-pay-03)) |
| [EP-08](#ep-08) | Ledger, Seller wallet and Marketplace fee | Must | Ledger | none | README | accepted (core) |
| [EP-09](#ep-09) | Withdrawal | Must | Ledger | EP-02, EP-08 | README | accepted (core) ([R-LED-06](../domain/ledger.md#r-led-06)) |
| [EP-10](#ep-10) | Shipping and tracking | Must | Shipping | EP-06 | README | accepted (core); Carrier quotes are a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) |
| [EP-12](#ep-12) | E-invoices | Must | Invoicing | EP-10, EP-14 | README | accepted (core); fee e-invoice to the Seller only ([R-INVC-02](../domain/invoicing.md#r-invc-02)) |
| [EP-13](#ep-13) | Reconciliation | Must | Reconciliation | EP-07 (order: [Q-09](../OPEN_QUESTIONS.md#q-09)), EP-08 | README | accepted (core); Payment gateways only ([R-REC-02](../domain/reconciliation.md#r-rec-02)) |
| [EP-14](#ep-14) | Cancellation and Refund before shipment | Must | Ordering, Payment, Inventory, Ledger | EP-06, EP-07 | README | accepted (core) ([R-PAY-04](../domain/payment.md#r-pay-04)) |
| [EP-15](#ep-15) | Seller order handling | Must | Ordering, Shipping | EP-06, EP-10, EP-14 | new scope proposal ([Q-38](../OPEN_QUESTIONS.md#q-38)) | accepted (core) ([R-ORD-05](../domain/ordering.md#r-ord-05)) |
| [EP-16](#ep-16) | Failed delivery and return to sender | Must | Shipping, Inventory, Ledger | EP-10, EP-14 | new scope proposal ([Q-37](../OPEN_QUESTIONS.md#q-37)) | accepted (core) ([R-SHP-03](../domain/shipping.md#r-shp-03)) |
| [EP-17](#ep-17) | Return and Refund after delivery | Must | none yet ([Q-37](../OPEN_QUESTIONS.md#q-37)) | EP-07, EP-08, EP-10 | new scope proposal ([Q-37](../OPEN_QUESTIONS.md#q-37), [Q-34](../OPEN_QUESTIONS.md#q-34)) | later: [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) |
| [EP-19](#ep-19) | Admin back-office and audit trail | Must | all (cross-cutting) | EP-01, EP-08 | new scope proposal ([Q-41](../OPEN_QUESTIONS.md#q-41)) | accepted (core): Admin actions per context and one Audit trail ([R-ARCH-04](../RULES_AND_CONSTRAINTS.md#r-arch-04)) |
| [EP-20](#ep-20) | Seller statement and reports | Must | Ledger | EP-08 | new scope proposal ([Q-42](../OPEN_QUESTIONS.md#q-42)) | accepted (core): Seller statement only ([Q-42](../OPEN_QUESTIONS.md#q-42)) |
| [EP-24](#ep-24) | Personal data protection and retention | Must | Identity, all | EP-01 | new scope proposal ([Q-39](../OPEN_QUESTIONS.md#q-39)) | accepted (core): masking of Buyer data ([R-IDN-05](../domain/identity.md#r-idn-05)) |
| [EP-11](#ep-11) | Notifications for Buyers and Sellers | Should | Notification | EP-06, EP-09, EP-10, EP-14 | README | accepted (core); email only ([R-NTF-03](../domain/notification.md#r-ntf-03)) |
| [EP-18](#ep-18) | Disputes and Wallet hold | Should | none yet, Ledger | EP-08, EP-17 | new scope proposal ([Q-37](../OPEN_QUESTIONS.md#q-37), [Q-20](../OPEN_QUESTIONS.md#q-20), [Q-34](../OPEN_QUESTIONS.md#q-34)) | later: [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) |
| [EP-21](#ep-21) | Stuck-state detection and monitoring | Should | all (cross-cutting) | EP-06, EP-07, EP-10, EP-12 | new scope proposal ([Q-44](../OPEN_QUESTIONS.md#q-44)) | accepted (core): alerts only ([Q-44](../OPEN_QUESTIONS.md#q-44)) |
| [EP-22](#ep-22) | Cash on delivery (COD) | Should | Payment, Ledger, Reconciliation, Shipping | EP-08, EP-10, EP-13 | new scope proposal ([Q-35](../OPEN_QUESTIONS.md#q-35)) | later: [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) |
| [EP-23](#ep-23) | Seller tax withholding | Should | Ledger, Invoicing | EP-08, EP-12 | new scope proposal ([Q-39](../OPEN_QUESTIONS.md#q-39)) | later: [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) |
| [EP-25](#ep-25) | Trust signals: reviews and ratings | Should | none yet | EP-02, EP-10 | new scope proposal ([Q-36](../OPEN_QUESTIONS.md#q-36)) | accepted (core), step 10, in Catalog |
| [EP-27](#ep-27) | Bulk product import | Should | Catalog, Inventory | EP-03, EP-04 | new scope proposal ([Q-40](../OPEN_QUESTIONS.md#q-40)) | accepted (core), step 9 ([Q-40](../OPEN_QUESTIONS.md#q-40)) |
| [EP-26](#ep-26) | Fraud signals and Seller penalties | Could | Identity, all | EP-09, EP-14, EP-17, EP-19 | new scope proposal ([Q-41](../OPEN_QUESTIONS.md#q-41)) | later: [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) |
| [EP-28](#ep-28) | Multi-channel stock sync | Could | Inventory | EP-04 | new scope proposal ([Q-40](../OPEN_QUESTIONS.md#q-40)) | later: [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) |
| [EP-29](#ep-29) | Vouchers | Could | Ordering, Ledger | EP-06, EP-08 | new scope proposal ([Q-36](../OPEN_QUESTIONS.md#q-36)) | later: [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) |
| [EP-30](#ep-30) | Seller subscriptions and sponsored placement | Could | Ledger, Catalog | EP-08 | new scope proposal ([Q-36](../OPEN_QUESTIONS.md#q-36)) | later: [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) |
| [EP-31](#ep-31) | Buyer–Seller chat and livestream selling | Won't (this time) | none yet | EP-01 | README extension track (chat); new scope proposal (livestream, [Q-36](../OPEN_QUESTIONS.md#q-36)) | later: [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) |

## Epic map by context

| Context | Epics |
|---|---|
| Identity | EP-01, EP-02, EP-24, EP-26 |
| Catalog | EP-03, EP-27, EP-30 |
| Inventory | EP-04, EP-05, EP-27, EP-28 (also EP-14, EP-16 restore Stock) |
| Ordering | EP-06, EP-14, EP-15, EP-29 |
| Payment | EP-07, EP-14, EP-22 |
| Ledger | EP-08, EP-09, EP-20, EP-23 (also EP-14, EP-16, EP-18 Wallet hold, EP-22, EP-29, EP-30) |
| Reconciliation | EP-13 (also EP-22 Carrier money) |
| Shipping | EP-10, EP-16 (also EP-15 Shipping labels, EP-22) |
| Notification | EP-11 |
| Invoicing | EP-12 (also EP-23) |
| No context yet | EP-17, EP-18 ([Q-37](../OPEN_QUESTIONS.md#q-37)); EP-19 (cross-cutting, [Q-41](../OPEN_QUESTIONS.md#q-41)); EP-21 (cross-cutting, [Q-44](../OPEN_QUESTIONS.md#q-44)); EP-25, EP-31 |

## Epics

<a id="ep-01"></a>
### EP-01: Accounts and roles
Users sign up and sign in as a Buyer, Seller or Admin, with RBAC. Depends on decision [Q-06](../OPEN_QUESTIONS.md#q-06): Seller team members with limited permissions, and Admin roles split by job (support cannot move money).
- **Benefits:** all users · **Raised by:** ADM, SEL, BUY · **Contexts:** Identity · **Depends on:** none ([Q-06](../OPEN_QUESTIONS.md#q-06))
- **Priority:** Must: every other epic needs to know who acts. · **Invariant:** none · **Scope:** README
- **Decision:** accepted (core) (2026-11-21)

<a id="ep-02"></a>
### EP-02: Seller onboarding and eKYC
A Seller applies, passes eKYC (FPT.AI OCR), registers a bank account, and an Admin reviews the result.
- **Benefits:** ADM, BUY (verified Sellers) · **Raised by:** ADM, STR, BA, BUY · **Contexts:** Identity · **Depends on:** EP-01 ([Q-11](../OPEN_QUESTIONS.md#q-11))
- **Priority:** Must: Withdrawal is the main fraud exit and needs a verified Seller. · **Invariant:** none · **Scope:** README
- **Decision:** accepted (core); eKYC through a Fake only ([R-IDN-04](../domain/identity.md#r-idn-04)) (2026-11-21)

<a id="ep-03"></a>
### EP-03: Product catalog
Sellers create Products, Variants and Prices; Buyers browse and search them.
- **Benefits:** SEL, BUY · **Raised by:** README; SEL, BUY · **Contexts:** Catalog · **Depends on:** EP-01, order: [Q-09](../OPEN_QUESTIONS.md#q-09) ([Q-12](../OPEN_QUESTIONS.md#q-12), [Q-13](../OPEN_QUESTIONS.md#q-13))
- **Priority:** Must: nothing can be sold without it. · **Invariant:** none directly; it decides where Stock lives · **Scope:** README
- **Decision:** accepted (core) (2026-11-21)

<a id="ep-04"></a>
### EP-04: Stock and stock reservations
Stock per Product or Variant, Stock reservations with a TTL during checkout, and an honest "sold out".
- **Benefits:** BUY (no cancel after ordering), SEL · **Raised by:** BUY, SEL, STR · **Contexts:** Inventory · **Depends on:** EP-03, order: [Q-09](../OPEN_QUESTIONS.md#q-09) ([Q-14](../OPEN_QUESTIONS.md#q-14), [Q-15](../OPEN_QUESTIONS.md#q-15))
- **Priority:** Must: it is a core invariant. · **Invariant:** INV · **Scope:** README
- **Decision:** accepted (core) (2026-11-21)

<a id="ep-05"></a>
### EP-05: Flash sale
Many Buyers compete for little Stock, with a countdown, per-user rate limits, and protection against bots. Depends on decision [Q-17](../OPEN_QUESTIONS.md#q-17): whether Sellers set aside Stock and a Price for the sale.
- **Benefits:** BUY, SEL · **Raised by:** BUY, SEL, STR · **Contexts:** Inventory · **Depends on:** EP-04 ([Q-16](../OPEN_QUESTIONS.md#q-16), [Q-17](../OPEN_QUESTIONS.md#q-17))
- **Priority:** Must: it is the README's headline load test for INV. · **Invariant:** INV · **Scope:** README
- **Decision:** accepted (core) ([R-INV-06](../domain/inventory.md#r-inv-06)) (2026-11-21)

<a id="ep-06"></a>
### EP-06: Checkout and order placement
Placing and paying for an Order through the Checkout saga; a retry on a bad network never creates a second Order. Depends on decisions: one checkout covers one Seller only ([R-ORD-04](../domain/ordering.md#r-ord-04)), and whether the full Price including a Shipping quote is shown before payment ([Q-43](../OPEN_QUESTIONS.md#q-43)).
- **Benefits:** BUY · **Raised by:** BUY, BA · **Contexts:** Ordering · **Depends on:** EP-03 (order: [Q-09](../OPEN_QUESTIONS.md#q-09)), EP-04, EP-07; Shipping quote from EP-10, which makes a loop with EP-10 until [Q-43](../OPEN_QUESTIONS.md#q-43) is decided ([Q-05](../OPEN_QUESTIONS.md#q-05), [Q-24](../OPEN_QUESTIONS.md#q-24), [Q-25](../OPEN_QUESTIONS.md#q-25))
- **Priority:** Must: the core flow. · **Invariant:** INV and LED · **Scope:** README
- **Decision:** accepted (core); flat Shipping fee, no quote ([R-ORD-06](../domain/ordering.md#r-ord-06)) (2026-11-21)

<a id="ep-07"></a>
### EP-07: Online payment
Payment by VNPay, QR bank transfer or card, with idempotent IPN handling and re-query when the IPN is late or missing.
- **Benefits:** BUY, ADM · **Raised by:** BUY, STR · **Contexts:** Payment · **Depends on:** EP-08, order: [Q-09](../OPEN_QUESTIONS.md#q-09) ([Q-21](../OPEN_QUESTIONS.md#q-21), [Q-22](../OPEN_QUESTIONS.md#q-22))
- **Priority:** Must: the marketplace holds the money. · **Invariant:** LED · **Scope:** README
- **Decision:** accepted (core); VNPay only ([R-PAY-03](../domain/payment.md#r-pay-03)) (2026-11-21)

<a id="ep-08"></a>
### EP-08: Ledger, Seller wallet and Marketplace fee
The double-entry ledger records every money movement; each Seller wallet is built from ledger entries; the Marketplace fee is deducted. When the fee is fixed, and how Sellers see it: depends on decision [Q-19](../OPEN_QUESTIONS.md#q-19).
- **Benefits:** SEL, ADM, STR · **Raised by:** STR, SEL, ADM · **Contexts:** Ledger · **Depends on:** none ([Q-18](../OPEN_QUESTIONS.md#q-18), [Q-19](../OPEN_QUESTIONS.md#q-19))
- **Priority:** Must: it is a core invariant and the revenue model. · **Invariant:** LED · **Scope:** README
- **Decision:** accepted (core) (2026-11-21)

<a id="ep-09"></a>
### EP-09: Withdrawal
A Seller moves available money from the Seller wallet to a verified bank account. Includes reversal of a failed bank transfer. Depends on decisions: when money is released and whether an Admin approves a Withdrawal ([Q-20](../OPEN_QUESTIONS.md#q-20)), and how the money leaves the marketplace ([Q-47](../OPEN_QUESTIONS.md#q-47)).
- **Benefits:** SEL, ADM · **Raised by:** SEL, STR, BA, ADM · **Contexts:** Ledger · **Depends on:** EP-02, EP-08 ([Q-20](../OPEN_QUESTIONS.md#q-20), [Q-47](../OPEN_QUESTIONS.md#q-47))
- **Priority:** Must: Seller cash flow is the top retention factor. · **Invariant:** LED · **Scope:** README
- **Decision:** accepted (core) ([R-LED-06](../domain/ledger.md#r-led-06)) (2026-11-21)

<a id="ep-10"></a>
### EP-10: Shipping and tracking
Shipping quotes from GHN and GHTK, Shipment creation and pickup, Carrier webhooks, and live tracking for the Buyer. Addresses use the administrative units after the merger.
- **Benefits:** BUY, SEL · **Raised by:** BUY, SEL, BA · **Contexts:** Shipping · **Depends on:** EP-06 (`OrderPaid`). EP-08 consumes `Delivered` from this epic, so EP-08's Money release waits for EP-10, not the other way round ([Q-20](../OPEN_QUESTIONS.md#q-20)). Quotes may be needed before EP-06: [Q-43](../OPEN_QUESTIONS.md#q-43) ([Q-28](../OPEN_QUESTIONS.md#q-28))
- **Priority:** Must: Products must arrive, and successful delivery drives the money ([R-LED-03](../domain/ledger.md#r-led-03)). · **Invariant:** LED (through `Delivered`) · **Scope:** README
- **Decision:** accepted (core); Carrier quotes are a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) (2026-11-21)

<a id="ep-11"></a>
### EP-11: Notifications for Buyers and Sellers
Notifications at the key steps for Buyers (paid, shipped, delivered, Refund done after a Cancellation) and for Sellers (new Order, Withdrawal done). Only if [Q-37](../OPEN_QUESTIONS.md#q-37) accepts EP-16 and EP-17: failed delivery and Refund after a Return. Which events notify whom, and the event edges the README does not draw: [Q-29](../OPEN_QUESTIONS.md#q-29).
- **Benefits:** BUY, SEL · **Raised by:** BUY, BA · **Contexts:** Notification · **Depends on:** EP-06, EP-09, EP-10, EP-14 ([Q-29](../OPEN_QUESTIONS.md#q-29))
- **Priority:** Should: reduces panic and double payment, but the web app can show the same state. · **Invariant:** none · **Scope:** README
- **Decision:** accepted (core); email only ([R-NTF-03](../domain/notification.md#r-ntf-03)) (2026-11-21)

<a id="ep-12"></a>
### EP-12: E-invoices
Issue e-invoices through SePay eInvoice, and adjust or replace them after a Refund. Only if [Q-37](../OPEN_QUESTIONS.md#q-37) accepts EP-17: also after a partial Return. Whether Buyers can ask for one with a company tax ID: depends on decision [Q-30](../OPEN_QUESTIONS.md#q-30).
- **Benefits:** ADM, SEL, BUY · **Raised by:** STR, SEL, BUY, ADM · **Contexts:** Invoicing · **Depends on:** EP-10, EP-14 ([Q-30](../OPEN_QUESTIONS.md#q-30))
- **Priority:** Must: needed to operate legally (unverified). · **Invariant:** none; amounts must match the ledger · **Scope:** README
- **Decision:** accepted (core); fee e-invoice to the Seller only ([R-INVC-02](../domain/invoicing.md#r-invc-02)) (2026-11-21)

<a id="ep-13"></a>
### EP-13: Reconciliation
Compare external records with the ledger every night (README). Which sources (the README table and diagram differ), and what happens to a Mismatch: depend on decision [Q-31](../OPEN_QUESTIONS.md#q-31).
- **Benefits:** ADM, STR · **Raised by:** STR, ADM, BA · **Contexts:** Reconciliation · **Depends on:** EP-07 (order: [Q-09](../OPEN_QUESTIONS.md#q-09)), EP-08 ([Q-31](../OPEN_QUESTIONS.md#q-31))
- **Priority:** Must: it proves the ledger matches reality. · **Invariant:** LED · **Scope:** README
- **Decision:** accepted (core); Payment gateways only ([R-REC-02](../domain/reconciliation.md#r-rec-02)) (2026-11-21)

<a id="ep-14"></a>
### EP-14: Cancellation and Refund before shipment
A Buyer or a timeout cancels a paid Order before it ships (a Seller cancel depends on decision [Q-38](../OPEN_QUESTIONS.md#q-38), see EP-15); Compensation releases Stock, starts the Refund and reverses ledger entries.
- **Benefits:** BUY, SEL · **Raised by:** BA, BUY · **Contexts:** Ordering, Payment, Inventory, Ledger · **Depends on:** EP-06, EP-07 ([Q-23](../OPEN_QUESTIONS.md#q-23), [Q-25](../OPEN_QUESTIONS.md#q-25))
- **Priority:** Must: a missing step here breaks both invariants. · **Invariant:** INV and LED · **Scope:** README
- **Decision:** accepted (core) ([R-PAY-04](../domain/payment.md#r-pay-04)) (2026-11-21)

<a id="ep-15"></a>
### EP-15: Seller order handling
Sellers confirm, pack and hand Orders to the Carrier, or cancel them, in bulk, and print Shipping labels.
- **Benefits:** SEL · **Raised by:** SEL, BA · **Contexts:** Ordering, Shipping · **Depends on:** EP-06, EP-10, EP-14
- **Priority:** Must: no context owns the step after payment, so Orders can get stuck. · **Invariant:** INV and LED (a Seller cancel must use EP-14) · **Scope:** new scope proposal ([Q-38](../OPEN_QUESTIONS.md#q-38))
- **Decision:** accepted (core) ([R-ORD-05](../domain/ordering.md#r-ord-05)) (2026-11-21)

<a id="ep-16"></a>
### EP-16: Failed delivery and return to sender
When the Carrier cannot deliver, the Seller is told, the Products come back, Stock is restored, the Seller wallet is never credited, and the shipping cost has an owner.
- **Benefits:** SEL, ADM · **Raised by:** SEL, BA · **Contexts:** Shipping, Inventory, Ledger · **Depends on:** EP-10, EP-14
- **Priority:** Must: common in practice; Products and money get lost otherwise. · **Invariant:** INV and LED · **Scope:** new scope proposal ([Q-37](../OPEN_QUESTIONS.md#q-37))
- **Decision:** accepted (core) ([R-SHP-03](../domain/shipping.md#r-shp-03)) (2026-11-21)

<a id="ep-17"></a>
### EP-17: Return and Refund after delivery
A Buyer starts a Return in a few taps with photos, the Products come back, and the Refund reaches the original payment method; money is taken back from the Seller wallet.
- **Benefits:** BUY, SEL · **Raised by:** BUY, SEL, BA, STR, ADM · **Contexts:** none yet · **Depends on:** EP-07, EP-08, EP-10
- **Priority:** Must: raised by all five perspectives. · **Invariant:** LED (taking money back), INV (restocking) · **Scope:** new scope proposal ([Q-37](../OPEN_QUESTIONS.md#q-37), [Q-34](../OPEN_QUESTIONS.md#q-34))
- **Decision:** later: [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) (2026-11-21)

<a id="ep-18"></a>
### EP-18: Disputes and Wallet hold
A Buyer opens a Dispute on an Order, the Seller answers with evidence, an Admin decides, and the decision creates the Refund and ledger entries. The disputed money is a Wallet hold until then.
- **Benefits:** BUY, SEL, ADM · **Raised by:** ADM, BA, STR · **Contexts:** none yet, Ledger · **Depends on:** EP-08, EP-17
- **Priority:** Should: EP-17 covers most cases; a Dispute adds the contested ones. · **Invariant:** LED · **Scope:** new scope proposal ([Q-37](../OPEN_QUESTIONS.md#q-37), [Q-20](../OPEN_QUESTIONS.md#q-20), [Q-34](../OPEN_QUESTIONS.md#q-34))
- **Decision:** later: [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) (2026-11-21)

<a id="ep-19"></a>
### EP-19: Admin back-office and audit trail
One timeline per Order, queues for stuck Orders and mismatches, manual corrections made only as new ledger entries with a second Admin approving large amounts, and an audit trail of every Admin action.
- **Benefits:** ADM · **Raised by:** ADM, BA, STR · **Contexts:** all (cross-cutting) · **Depends on:** EP-01, EP-08 ([Q-06](../OPEN_QUESTIONS.md#q-06))
- **Priority:** Must: without it, manual fixes go around the ledger. · **Invariant:** LED · **Scope:** new scope proposal ([Q-41](../OPEN_QUESTIONS.md#q-41))
- **Decision:** accepted (core): Admin actions per context and one Audit trail ([R-ARCH-04](../RULES_AND_CONSTRAINTS.md#r-arch-04)) (2026-11-21)

<a id="ep-20"></a>
### EP-20: Seller statement and reports
A Seller statement lists every ledger entry per Order, with export. Later: sales reports for Sellers and a daily close report for finance.
- **Benefits:** SEL, ADM · **Raised by:** SEL, STR, BA, ADM · **Contexts:** Ledger · **Depends on:** EP-08
- **Priority:** Must (statement): it makes the balanced ledger visible to Sellers, the strategist's main differentiator. · **Invariant:** none (read only) · **Scope:** new scope proposal ([Q-42](../OPEN_QUESTIONS.md#q-42))
- **Decision:** accepted (core): Seller statement only ([Q-42](../OPEN_QUESTIONS.md#q-42)) (2026-11-21)

<a id="ep-21"></a>
### EP-21: Stuck-state detection and monitoring
Detect and warn the Admin team about Orders paid with no Shipment, Shipments with no update, missing IPNs, a growing DLQ and failed e-invoices.
- **Benefits:** ADM, SEL · **Raised by:** ADM, BA · **Contexts:** all (cross-cutting) · **Depends on:** EP-06, EP-07, EP-10, EP-12 ([Q-44](../OPEN_QUESTIONS.md#q-44))
- **Priority:** Should: silent failures cost money, but the core flows come first. · **Invariant:** none; it detects breaks · **Scope:** new scope proposal ([Q-44](../OPEN_QUESTIONS.md#q-44)). The README does not mention stuck-state detection.
- **Decision:** accepted (core): alerts only ([Q-44](../OPEN_QUESTIONS.md#q-44)) (2026-11-21)

<a id="ep-22"></a>
### EP-22: Cash on delivery (COD)
The Carrier collects the money from the Buyer and sends it to the marketplace later; Carrier money is reconciled.
- **Benefits:** BUY · **Raised by:** BUY, BA, STR · **Contexts:** Payment, Ledger, Reconciliation, Shipping · **Depends on:** EP-08, EP-10, EP-13
- **Priority:** Should: a Buyer must-have (unverified), but it adds a money holder; decide before the ledger accounts are fixed. · **Invariant:** LED · **Scope:** new scope proposal ([Q-35](../OPEN_QUESTIONS.md#q-35))
- **Decision:** later, as a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions); Ledger accounts leave room for Carrier money ([Q-35](../OPEN_QUESTIONS.md#q-35), 2026-11-21)

<a id="ep-23"></a>
### EP-23: Seller tax withholding
The marketplace deducts and declares tax for household Sellers (law unverified).
- **Benefits:** ADM, SEL · **Raised by:** STR, BA · **Contexts:** Ledger, Invoicing · **Depends on:** EP-08, EP-12
- **Priority:** Should: it may be legally required (unverified) and changes the ledger accounts, so decide early even if built later. · **Invariant:** LED · **Scope:** new scope proposal ([Q-39](../OPEN_QUESTIONS.md#q-39))
- **Decision:** later: [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) (2026-11-21)

<a id="ep-24"></a>
### EP-24: Personal data protection and retention
Consent, data minimization, export and deletion, masking Buyer phone numbers and addresses shown to Sellers, and retention periods for accounting records.
- **Benefits:** BUY, ADM · **Raised by:** STR, BA · **Contexts:** Identity, all · **Depends on:** EP-01
- **Priority:** Must: a legal baseline (unverified), and masking is cheap only if designed in from the start. · **Invariant:** none · **Scope:** new scope proposal ([Q-39](../OPEN_QUESTIONS.md#q-39))
- **Decision:** accepted (core): masking of Buyer data ([R-IDN-05](../domain/identity.md#r-idn-05)) (2026-11-21)

<a id="ep-25"></a>
### EP-25: Trust signals: reviews and ratings
Product reviews only from Buyers whose Order was delivered, Seller ratings, and a verified-Seller badge from eKYC.
- **Benefits:** BUY · **Raised by:** BUY, STR · **Contexts:** none yet · **Depends on:** EP-02, EP-10
- **Priority:** Should: high trust value and no money path. · **Invariant:** none · **Scope:** new scope proposal ([Q-36](../OPEN_QUESTIONS.md#q-36))
- **Decision:** accepted: Product reviews and Seller ratings in the core, Build-order step 10 ([Q-36](../OPEN_QUESTIONS.md#q-36), 2026-11-21). The verified-Seller badge depends on eKYC, a learning extension. Owning context: [Q-50](../OPEN_QUESTIONS.md#q-50)

<a id="ep-26"></a>
### EP-26: Fraud signals and Seller penalties
Flag fake Orders, Buyers who often refuse delivery, Sellers buying their own Products and abnormal Refund rates; suspend Sellers or block Withdrawals.
- **Benefits:** ADM · **Raised by:** ADM · **Contexts:** Identity, all · **Depends on:** EP-09, EP-14, EP-17, EP-19
- **Priority:** Could: useful at scale; sandbox data has little real fraud. · **Invariant:** none · **Scope:** new scope proposal ([Q-41](../OPEN_QUESTIONS.md#q-41))
- **Decision:** later: [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) (2026-11-21)

<a id="ep-27"></a>
### EP-27: Bulk product import
Sellers create and update many Products, Variants, Prices and Stock from a file.
- **Benefits:** SEL · **Raised by:** SEL, ADM · **Contexts:** Catalog, Inventory · **Depends on:** EP-03, EP-04
- **Priority:** Should: Sellers with hundreds of Variants leave without it. · **Invariant:** INV (bulk Stock writes) · **Scope:** new scope proposal ([Q-40](../OPEN_QUESTIONS.md#q-40))
- **Decision:** accepted (core), step 9 ([Q-40](../OPEN_QUESTIONS.md#q-40)) (2026-11-21)

<a id="ep-28"></a>
### EP-28: Multi-channel stock sync
An API lets a Seller's other sales channels push Stock and read Stock reservations.
- **Benefits:** SEL · **Raised by:** SEL · **Contexts:** Inventory · **Depends on:** EP-04 ([Q-15](../OPEN_QUESTIONS.md#q-15))
- **Priority:** Could: adds an external write path that races with Stock reservations; prove locking first. · **Invariant:** INV · **Scope:** new scope proposal ([Q-40](../OPEN_QUESTIONS.md#q-40))
- **Decision:** later: [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) (2026-11-21)

<a id="ep-29"></a>
### EP-29: Vouchers
Vouchers funded by the marketplace or by a Seller, and free-shipping offers.
- **Benefits:** BUY, SEL · **Raised by:** BUY, SEL, STR · **Contexts:** Ordering, Ledger · **Depends on:** EP-06, EP-08
- **Priority:** Could: expected by Buyers (unverified), but every Voucher splits money across more ledger entries. · **Invariant:** LED · **Scope:** new scope proposal ([Q-36](../OPEN_QUESTIONS.md#q-36))
- **Decision:** later, as a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) after the Ledger is proven ([Q-36](../OPEN_QUESTIONS.md#q-36), 2026-11-21)

<a id="ep-30"></a>
### EP-30: Seller subscriptions and sponsored placement
A paid Seller tier (lower Marketplace fee or faster release of money) and paid placement in search.
- **Benefits:** STR, SEL · **Raised by:** STR · **Contexts:** Ledger, Catalog · **Depends on:** EP-08
- **Priority:** Could: second revenue line; needs traffic first. · **Invariant:** LED · **Scope:** new scope proposal ([Q-36](../OPEN_QUESTIONS.md#q-36))
- **Decision:** later, as a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) outside the core ([Q-36](../OPEN_QUESTIONS.md#q-36), 2026-11-21)

<a id="ep-31"></a>
### EP-31: Buyer–Seller chat and livestream selling
Buyers ask Sellers questions before buying; Sellers sell live.
- **Benefits:** BUY, SEL · **Raised by:** BUY, SEL · **Contexts:** none yet · **Depends on:** EP-01
- **Priority:** Won't (this time): the strategist pushes back; it pulls effort from the stated goal and is a competitor's strength (unverified). · **Invariant:** none · **Scope:** README extension track (chat); new scope proposal (livestream, [Q-36](../OPEN_QUESTIONS.md#q-36))
- **Decision:** later, as a [learning extension](../PROJECT_OVERVIEW.md#learning-extensions) outside the core ([Q-36](../OPEN_QUESTIONS.md#q-36), 2026-11-21)

## Conflicts between perspectives

Both sides are shown. None is resolved here. This table records who said what; the options and analysis live only in the linked questions.

| Topic | One side | Other side | Question |
|---|---|---|---|
| When Seller money is released | SEL: cash flow is the biggest pain; keep only part of the money unavailable, release fast | BUY, ADM, BA, STR: keep it unavailable until the Return window ends; money already withdrawn cannot be recovered. STR: sell faster release as a paid tier instead | [Q-20](../OPEN_QUESTIONS.md#q-20) |
| Who decides a Refund for a Return | BUY: a few taps, fast, back to the original method | SEL: a response window with evidence; Refund after the Products come back. ADM: automatic only below a threshold | [Q-34](../OPEN_QUESTIONS.md#q-34), [Q-23](../OPEN_QUESTIONS.md#q-23) |
| Cash on delivery | BUY: a must; many Buyers will not pay first (unverified) | README: three online methods and "the marketplace holds the money". BA, STR: it reshapes the ledger; decide early | [Q-35](../OPEN_QUESTIONS.md#q-35) |
| Several Sellers in one Order | BUY: one cart, one payment | ADM: one Seller per Order keeps Disputes, partial Refunds and e-invoices simple. BA: decide before building | [Q-05](../OPEN_QUESTIONS.md#q-05) |
| Vouchers and growth features | BUY, SEL: Vouchers are expected; chat helps conversion | BA: no Vouchers at launch, too many money paths. STR: Vouchers only after the ledger is proven; no chat or livestream early | [Q-36](../OPEN_QUESTIONS.md#q-36) |
| When eKYC is required | STR: before the first Withdrawal. BUY: no extra checks before browsing or checkout | ADM: no selling before eKYC; if allowed, Withdrawals stay blocked until eKYC passes | [Q-11](../OPEN_QUESTIONS.md#q-11) |

**Where perspectives agree** (input for the linked questions, not decisions): short Stock reservation TTL (BUY, SEL; [Q-14](../OPEN_QUESTIONS.md#q-14)); no direct edit of a Seller wallet, only new ledger entries (STR, ADM, BA); Marketplace fee fixed when the Order is placed (SEL, STR; [Q-19](../OPEN_QUESTIONS.md#q-19)); reviews only from delivered Orders (BUY, STR).

## Impact on the build order

This section lists impact only. The [Build order](../PROJECT_OVERVIEW.md#build-order) was decided on 2026-11-21 ([Q-09](../OPEN_QUESTIONS.md#q-09)); the rows below can still change it.

| Impact | Epics | Why | Question |
|---|---|---|---|
| Possible new context for after-sales | EP-16, EP-17, EP-18 | No README context owns a case that spans Shipping, Payment, Ledger and Inventory after payment | [Q-37](../OPEN_QUESTIONS.md#q-37) |
| Possible new context or cross-cutting piece for the audit trail | EP-19, EP-26 | Must exist before the first Admin money action, like the step 0 pieces | [Q-41](../OPEN_QUESTIONS.md#q-41) |
| Ledger accounts must leave room before the Ledger step | EP-18, EP-22, EP-23, EP-29, EP-30 | Wallet hold, Carrier money (COD), withheld tax and Vouchers each add accounts; adding them later is costly | [Q-18](../OPEN_QUESTIONS.md#q-18), [Q-20](../OPEN_QUESTIONS.md#q-20), [Q-35](../OPEN_QUESTIONS.md#q-35), [Q-36](../OPEN_QUESTIONS.md#q-36), [Q-39](../OPEN_QUESTIONS.md#q-39) |
| A new step between Ordering and Shipping | EP-15 | A Seller confirm or cancel step changes the Order state machine and the Checkout saga | [Q-38](../OPEN_QUESTIONS.md#q-38), [Q-24](../OPEN_QUESTIONS.md#q-24) |
| Shipment states must include return to sender | EP-16 | Changes the Shipping state machine | [Q-28](../OPEN_QUESTIONS.md#q-28) |
| Identity must design data masking early | EP-24 | Buyer data shown to Sellers must be masked from the first Order screen | [Q-39](../OPEN_QUESTIONS.md#q-39) |
| eKYC before Withdrawal | EP-02, EP-09 | Withdrawal (Ledger step) needs eKYC (Identity) | [Q-11](../OPEN_QUESTIONS.md#q-11) |
| Reporting read model | EP-20 | Option B needs a read model; option A needs nothing new | [Q-42](../OPEN_QUESTIONS.md#q-42) |

EP-25, EP-27, EP-28 and EP-31 come after the core and do not reorder it. EP-26, EP-29 and EP-30 can change it: see the rows above.

## Appendix: what each perspective cared about most

**BA (system view).** The exception lifecycle: cancellation, failed delivery, Return after the Seller was paid. Each must be a Compensation path that keeps Stock and the ledger correct. It found six needs no context owns: Seller order handling, Returns and Disputes, the Admin back-office and audit trail, reporting, tax withholding and data retention. It pushed back on early Withdrawal, Vouchers at launch, and Seller self-delivery that bypasses the Carrier (no trusted `Delivered` event).

**STR (business strategist).** TallyMart cannot win on traffic (unverified); it can win on money and stock that always add up. Its must-haves: the ledger-backed money flow with a Seller statement, Reconciliation as the proof, and a Vietnam compliance baseline (e-invoice, tax withholding decision, eKYC, personal data). It pushed back on paying before delivery, direct edits of a Seller wallet, and livestream or chat early.

**BUY (Buyer).** Pay the trusted way (COD plus online, no double Payment), honest Stock and the full Price before paying, and an easy Return with a visible Refund. It pushed back on releasing Seller money at "delivered", long Stock reservations that let bots keep Stock reserved, and dropping COD.

**SEL (Seller).** Transparent, fast money (statement per ledger entry, fee known up front, a release date), Stock that stays correct across channels, and Order handling at volume. It pushed back on keeping Seller money unavailable for long, long Stock reservations, Refunds decided without the Seller, and fee changes on existing Orders.

**ADM (Admin team).** Every Admin money action goes through the ledger with a second approval and an audit trail; a Reconciliation workbench with owners and ageing; Disputes tied to a Wallet hold. It pushed back on instant Withdrawal, automatic Refunds without checks, and selling before eKYC. It also prefers one Seller per Order.
