---
status: active
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [docs, backend]
related_code: []
---

# Ghi chú học tập: Event

Cách đọc các ghi chú này: [learning-notes/README](README.md). Outbox relay và phần kiểm tra trùng của consumer là phần owner tự viết ([L-25](../LEARNING_MODE.md#l-25), [L-26](../LEARNING_MODE.md#l-26)), nên ghi chú này giải thích vấn đề và các bẫy, không đưa code.

## Outbox ở phía gửi, inbox ở phía nhận

- [ ] Owner đã đọc
- **Loại:** kỹ thuật
- **Ở đâu:** mọi event giữa các context · rule [R-EVT-01](../RULES_AND_CONSTRAINTS.md#r-evt-01), [R-EVT-02](../RULES_AND_CONSTRAINTS.md#r-evt-02) · đã quyết trong [Q-26](../OPEN_QUESTIONS.md#q-26), [Q-27](../OPEN_QUESTIONS.md#q-27) · khái niệm [L-25](../LEARNING_MODE.md#l-25), [L-26](../LEARNING_MODE.md#l-26)
- **Chuyện gì xảy ra:**
  - Phía gửi: khi Order chuyển sang "đã trả", dòng Order và một dòng trong bảng outbox được ghi trong cùng một DB transaction. Một relay đọc outbox, publish lên broker, rồi đánh dấu đã gửi.
  - Phía nhận: consumer nào đụng tới tiền, Stock hay e-invoice thì ghi event ID vào bảng inbox trong cùng DB transaction với thay đổi của nó, và bỏ qua event ID đã xử lý. Consumer gửi notification thì tự kiểm tra bản ghi đã gửi của nó.
  - Hết số lần retry thì message vào DLQ.
- **Vì sao làm vậy:**
  - "Dual write": ghi DB rồi publish là hai hệ thống khác nhau. Crash ở giữa thì Order đã trả mà không ai giao hàng (một trong các lỗi README nêu). Outbox biến hai lần ghi thành một.
  - Nhưng relay có thể publish xong rồi crash trước khi đánh dấu, nên cùng một event có thể tới hai lần ("at-least-once"). Vì vậy phía nhận phải chịu được trùng: đó là inbox.
  - Outbox + inbox cùng nhau cho hiệu quả "đúng một lần" (effectively once), dù việc gửi chỉ là "ít nhất một lần".
  - Làm Outbox ngay từ event đầu tiên vì sửa lại sau này phải đụng vào mọi chỗ publish.
- **Có thể sai ở đâu:**
  - Ghi inbox trong một transaction riêng, trước hoặc sau thay đổi chính: crash ở giữa là hoặc mất event, hoặc xử lý hai lần.
  - Relay publish theo thứ tự lộn xộn khi chạy nhiều instance. Consumer không được giả định event tới đúng thứ tự.
  - Poison message (message lỗi mãi) làm tắc queue nếu retry không có giới hạn.
- **Tự kiểm tra:**
  1. Crash ngay sau `commit()` và trước `publish()`: không có Outbox thì mất gì? Có Outbox thì sao?
  2. Vì sao có Outbox rồi vẫn cần inbox?
  3. Vì sao notification được phép bỏ inbox mà tiền thì không?
- **Đọc thêm:** "transactional outbox pattern" (microservices.io); "idempotent consumer pattern"; "exactly-once delivery is a lie".
