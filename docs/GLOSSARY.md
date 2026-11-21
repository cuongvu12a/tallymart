---
status: draft
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [backend, web, docs]
related_code: []
---

# Glossary

One term per concept. Use the term exactly in code, APIs, events, tables, docs and commits ([R-DOC-01](RULES_AND_CONSTRAINTS.md#r-doc-01)).

- **DO NOT use** lists forbidden synonyms. If you see one, replace it with the term.
- **Vietnamese (spoken)** maps the words people say to the term. Apart from the generated system tour HTML, it is the only place in the repo where Vietnamese appears ([R-DOC-03](RULES_AND_CONSTRAINTS.md#r-doc-03)). The column is a draft: the owner MUST confirm it.
- A definition that the README does not give is marked with an open question.

## People and access

| Term | Definition | DO NOT use | Vietnamese (spoken) | Context |
|---|---|---|---|---|
| `User` | Any account in the system: a buyer, a seller or an admin | account (for the person), member (alone) | người dùng, tài khoản | Identity |
| `Buyer` | A user who places orders | customer, client, shopper | người mua, khách, khách hàng | Identity |
| `Seller` | A user who lists products and receives money after successful delivery | vendor, merchant, shop (the README phrase "multi-vendor marketplace" is the only exception) | người bán, nhà bán, shop | Identity |
| `Admin` | A user who runs the marketplace. One of a user's roles ([R-IDN-03](domain/identity.md#r-idn-03)); Admin actions: [R-ARCH-04](RULES_AND_CONSTRAINTS.md#r-arch-04) | operator, staff | admin, quản trị viên | Identity |
| `Role` | A named set of permissions used for RBAC | group, permission level | vai trò, quyền | Identity |

## Catalog and stock

| Term | Definition | DO NOT use | Vietnamese (spoken) | Context |
|---|---|---|---|---|
| `Product` | An item a seller lists for sale | item (for a listing), listing, goods (as a name for a Product) | sản phẩm, hàng | Catalog |
| `Variant` | One sellable version of a Product. Every Product has at least one; a Product with no options has one default Variant. Price and Stock belong to the Variant ([R-CAT-01](domain/catalog.md#r-cat-01)) | option (for a Variant), SKU (as a name for the concept) | biến thể, phân loại | Catalog |
| `Price` | The amount a buyer pays for one unit of a Variant. Money format: [CONVENTIONS: Money](CONVENTIONS.md#money) | cost (for a Price) | giá, giá bán | Catalog |
| `Stock` | The quantity of a Variant that can be sold ([R-CAT-01](domain/catalog.md#r-cat-01)) | inventory (Inventory is the context name), quantity on hand | tồn kho, hàng tồn, tồn | Inventory |
| `Stock reservation` | Stock held for a limited time (TTL) so nobody else can buy it. Lifecycle: [R-INV-05](domain/inventory.md#r-inv-05) | hold, lock (lock means a DB lock), allocation | giữ hàng, giữ chỗ | Inventory |
| `Oversell` | Selling more units than the stock allows. MUST never happen ([R-INV-01](domain/inventory.md#r-inv-01)) | overbook | bán lố, bán vượt tồn | Inventory |
| `Flash sale` | A sale where many buyers compete for little stock. With a time window, a special Price, its own Stock pool and a per-user cap ([R-INV-06](domain/inventory.md#r-inv-06)) | deal, promotion (for this concept) | flash sale, săn sale | Inventory |

## Orders and payment

| Term | Definition | DO NOT use | Vietnamese (spoken) | Context |
|---|---|---|---|---|
| `Order` | A buyer's request to buy products, tracked by the order state machine | purchase, transaction (for an Order) | đơn, đơn hàng | Ordering |
| `Order state machine` | The allowed order states and transitions. The Order keeps business states only; Payment and Shipment have their own ([R-ORD-01](domain/ordering.md#r-ord-01)) | order workflow, order lifecycle (as a name) | trạng thái đơn | Ordering |
| `Checkout saga` | The multi-step checkout process that Ordering orchestrates, with compensation | checkout flow, checkout transaction | luồng checkout | Ordering |
| `Compensation` | A step that undoes the effect of an earlier saga step | rollback (rollback means a DB rollback) | bù trừ, hoàn tác | Ordering |
| `Payment` | Money a buyer pays for an order through a payment gateway | charge, transaction (for a Payment) | thanh toán | Payment |
| `Payment gateway` | An external provider that takes the buyer's money (VNPay, SePay, Stripe) | PSP, processor | cổng thanh toán | Payment |
| `Gateway transaction` | A record of money movement kept by a payment gateway or a bank | transaction (alone), bank record | giao dịch | Payment, Reconciliation |
| `IPN` | A webhook from a payment gateway that reports a payment result | callback (for an IPN) | IPN, callback | Payment |
| `Webhook` | An HTTP call from an external system that reports an event | push notification (that is a Notification channel) | webhook | Payment, Shipping |
| `Refund` | Money returned to a buyer for a payment | chargeback (that is a card dispute), return (that is goods) | hoàn tiền | Payment |
| `Cart` | Products a Buyer has chosen before checkout. One checkout covers the Products of one Seller only ([R-ORD-04](domain/ordering.md#r-ord-04)) | basket, bag | giỏ hàng | Ordering |
| `Payment method` | The way a Buyer pays (for example card or bank QR). In the core, VNPay only ([R-PAY-03](domain/payment.md#r-pay-03)) | payment type, payment option | phương thức thanh toán | Payment |
| `Re-query` | Asking a Payment gateway for a payment's status when the IPN is late or missing (VNPay: `querydr`). Schedule: [R-PAY-02](domain/payment.md#r-pay-02) | poll (as a name), recheck | tra cứu lại giao dịch | Payment |
| `Cancellation` | Ending an Order before it ships, with Compensation. A Seller may cancel a paid Order before confirming it ([R-ORD-05](domain/ordering.md#r-ord-05)) | void, abort (for an Order) | hủy đơn | Ordering |

## Money

| Term | Definition | DO NOT use | Vietnamese (spoken) | Context |
|---|---|---|---|---|
| `Ledger` | The append-only, double-entry record of all money the marketplace holds | journal, books | sổ cái | Ledger |
| `Ledger entry` | One line in the ledger. All entries sum to 0 ([R-LED-01](domain/ledger.md#r-led-01)) | transaction (for a Ledger entry), record, posting | bút toán | Ledger |
| `Ledger account` | A named group of Ledger entries (for example one Seller wallet), identified by account type, Account holder and currency ([R-LED-04](domain/ledger.md#r-led-04)) | account (alone), bucket | tài khoản sổ cái | Ledger |
| `Account holder` | The party a Ledger account belongs to: a Seller, the marketplace or a Payment gateway; a Carrier later, for COD ([R-LED-04](domain/ledger.md#r-led-04)) | owner (for an account), account owner | chủ tài khoản | Ledger |
| `Shipping fee` | The flat amount a Buyer pays for shipping, copied onto the Order when it is placed ([R-ORD-06](domain/ordering.md#r-ord-06)) | delivery fee, freight | phí ship, phí vận chuyển | Ordering |
| `Inbox` | A table where a consumer records the event IDs it has processed, in the same DB transaction as its change ([R-EVT-02](RULES_AND_CONSTRAINTS.md#r-evt-02)) | dedup table, processed log | inbox | all |
| `Seller wallet` | Money the marketplace holds for one seller, kept as ledger entries | balance (as a name), account (alone; use Ledger account) | ví người bán, ví shop | Ledger |
| `Marketplace fee` | The amount the marketplace deducts from a seller's money. Rule: [R-LED-05](domain/ledger.md#r-led-05) | commission, platform fee | phí sàn | Ledger |
| `Withdrawal` | A seller taking money out of the seller wallet. Rules: [R-LED-06](domain/ledger.md#r-led-06) | cash out, payout, paid out | rút tiền | Ledger |
| `Successful delivery` | The point after which a Seller may be paid ([R-LED-03](domain/ledger.md#r-led-03)). N days (a setting, 7) after `Delivered` ([R-LED-03](domain/ledger.md#r-led-03)) | completed delivery, done (as a name) | giao thành công | Ledger, Shipping |
| `Return window` | A period after successful delivery in which a Buyer may start a Return. N days, a setting, 7 by default ([R-LED-03](domain/ledger.md#r-led-03)); Returns themselves are a learning extension | grace period, cooling-off period | thời hạn đổi trả | Ledger |
| `Available money` | Money in a Seller wallet the Seller may withdraw now. Becomes available at successful delivery ([R-LED-03](domain/ledger.md#r-led-03)) | free balance, withdrawable balance (as a name) | tiền khả dụng | Ledger |
| `Money release` | Making a Seller's money available. It happens at successful delivery ([R-LED-03](domain/ledger.md#r-led-03)). "Release" alone is used for ending a Stock reservation | release (alone, for money), unlock, settle (for this concept) | giải ngân cho shop | Ledger |
| `Reconciliation` | Comparing external records with internal data to find mismatches. In the core, Payment gateways only ([Q-31](OPEN_QUESTIONS.md#q-31)) | matching, audit (for this concept) | đối soát | Reconciliation |
| `Mismatch` | A difference that Reconciliation finds between an external record and internal data. Reported, never corrected automatically ([R-REC-02](domain/reconciliation.md#r-rec-02)) | discrepancy, diff (as a name) | lệch đối soát | Reconciliation |

## Shipping, notification, invoicing

| Term | Definition | DO NOT use | Vietnamese (spoken) | Context |
|---|---|---|---|---|
| `Carrier` | An external shipping company (GHN, GHTK) | shipper (that means the delivery person), courier | đơn vị vận chuyển, hãng vận chuyển | Shipping |
| `Shipment` | A delivery of goods by a carrier. One Order has one Shipment ([R-ORD-04](domain/ordering.md#r-ord-04)) | delivery (as a name), parcel | vận đơn, đơn vận chuyển | Shipping |
| `Shipping quote` | A carrier's price for a shipment | estimate, rate (as a name) | báo giá ship, phí ship | Shipping |
| `Notification` | A message sent to a user by email, SMS or push | alert, message (as a name for a Notification) | thông báo | Notification |
| `E-invoice` | An electronic invoice issued, adjusted or replaced through SePay eInvoice | bill, receipt | hóa đơn điện tử | Invoicing |

## Product discovery terms (draft)

Terms raised by product discovery in [product/EPICS.md](product/EPICS.md). Status: **draft**. The owner MUST confirm each term. A term whose epic is rejected is removed. The context is open until the linked question is answered.

| Term | Definition | DO NOT use | Vietnamese (spoken) | Context |
|---|---|---|---|---|
| `eKYC` | Electronic identity check of a Seller (the README names FPT.AI OCR). Required before a Seller's first Withdrawal ([R-IDN-04](domain/identity.md#r-idn-04)) | KYC check, verification (alone) | eKYC, xác minh danh tính | Identity |
| `Seller team member` | A user who acts for a Seller with limited permissions (for example, packing only). Not in the core: Q-06 decided roles Buyer, Seller and Admin only | staff, sub-account, employee | nhân viên shop, tài khoản phụ | Identity |
| `Shipping label` | The printed document a Seller sticks on the goods so the Carrier can collect them | waybill, airway bill | phiếu gửi hàng, tem vận đơn | Shipping |
| `Return to sender` | Goods coming back to the Seller after a failed delivery attempt by the Carrier | RTS, return (that is a Buyer-initiated Return) | hoàn hàng, chuyển hoàn | Shipping ([R-SHP-03](domain/shipping.md#r-shp-03)) |
| `Return` | A Buyer sending goods back after successful delivery, usually leading to a Refund | refund (that is money), exchange | trả hàng | later: [learning extension](PROJECT_OVERVIEW.md#learning-extensions) |
| `Dispute` | A case where a Buyer and a Seller disagree about an Order and an Admin decides | complaint, ticket, chargeback (that is a card dispute) | khiếu nại, tranh chấp | later: [learning extension](PROJECT_OVERVIEW.md#learning-extensions) |
| `Wallet hold` | Money in a Seller wallet that cannot be withdrawn yet, for example while a Dispute is open | hold (alone; that word is forbidden for Stock reservation), freeze, reserve (for money) | tạm giữ tiền | later: [learning extension](PROJECT_OVERVIEW.md#learning-extensions) |
| `COD` | Cash on delivery: the Carrier collects the money from the Buyer and sends it to the marketplace later | cash payment, pay later | COD, thu hộ, ship COD | later: [learning extension](PROJECT_OVERVIEW.md#learning-extensions) |
| `Seller statement` | A per-Order list of every ledger entry that changed a Seller wallet (payment, Marketplace fee, Refund, shipping) | payout report, settlement report, balance sheet | sao kê, đối soát của shop | Ledger ([Q-42](OPEN_QUESTIONS.md#q-42)) |
| `Audit trail` | An append-only record of who did what, when, with the value before and after, especially for Admin actions | log (alone), history | lịch sử thao tác, nhật ký | all ([R-ARCH-04](RULES_AND_CONSTRAINTS.md#r-arch-04)) |
| `Seller tax withholding` | Tax the marketplace deducts from a Seller's money and declares for the Seller (law unverified) | tax deduction, tax fee | khấu trừ thuế, sàn nộp thuế thay | later: [learning extension](PROJECT_OVERVIEW.md#learning-extensions) |
| `Product review` | A rating and comment on a Product by a Buyer whose Order was delivered | feedback, comment (as a name) | đánh giá sản phẩm | Catalog |
| `Seller rating` | A score for a Seller built from Product reviews and Order outcomes | shop rating, reputation (as a name) | đánh giá shop, điểm shop | Catalog |
| `Voucher` | A code or offer that lowers what the Buyer pays, funded by the marketplace or a Seller | coupon, discount code, promotion (for this concept) | voucher, mã giảm giá | later: [learning extension](PROJECT_OVERVIEW.md#learning-extensions) |

## Technical terms

| Term | Definition | DO NOT use | Vietnamese (spoken) | Context |
|---|---|---|---|---|
| `Context` | A bounded context: one business area with its own model and rules | domain (for a context; the `docs/domain/` folder name is allowed), service (until extracted) | context, miền | all |
| `Module` | The code that implements one context inside `apps/api` | package (for this concept), service | module | all |
| `Invariant` | A condition that MUST be true at all times | constraint (for the two core invariants) | bất biến | all |
| `Idempotency key` | A client value sent in the `Idempotency-Key` header so a repeated write has one effect | request ID, dedup token | idempotency key | all |
| `Event` | A fact that already happened, published for other contexts (`OrderPaid`, `Delivered`) | message (for an Event; a broker message carries an Event), command | sự kiện, event | all |
| `Transactional Outbox` | A table written in the same DB transaction as the change; a relay then publishes its events | event log | outbox | all |
| `DLQ` | Dead-letter queue: where a message goes after its retries run out | error queue, failed queue | DLQ | all |
| `Port` | An interface in front of an external system | adapter (the adapter implements the port), gateway (for the interface) | port | all |
| `Fake implementation` | A port implementation that simulates the external system with no network call | mock, stub (for this concept) | fake | all |
| `Sandbox` | A provider's test environment (VNPay sandbox, GHN staging, Stripe test mode) | staging (for our own env), test server | sandbox | all |
| `Phase` | A capability group in the README roadmap. Not a timeline. The README's own "Phase 0" status line is the only exception | milestone, release (for a Phase) | giai đoạn | all |
