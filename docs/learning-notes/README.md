---
status: active
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [docs]
related_code: []
---

# Ghi chú học tập

Đây là các ghi chú AI viết để owner học. Mỗi ghi chú giải thích một quy tắc nghiệp vụ hoặc một kỹ thuật mà một Module dùng: vì sao làm như vậy, và có thể sai ở đâu. Nguồn: chỉ thị của owner, 2026-11-21.

- Ghi chú chỉ để giải thích. Chúng không phải nguồn sự thật ([docs/README: Sources of truth](../README.md#sources-of-truth)). Mỗi ghi chú MUST link tới rule, ADR hoặc câu hỏi mà nó giải thích, và MUST NOT tự đặt ra rule riêng.
- Ghi chú MUST NOT để lộ code mà owner phải tự viết. Với một khái niệm nằm dưới "Owner writes" trong [bản đồ khái niệm](../LEARNING_MODE.md#concept-map), ghi chú chỉ giải thích vấn đề, các phương án và các bẫy, không bao giờ đưa code lời giải.
- Ghi chú MUST NOT chép thứ tự, ngày tháng hay số ngày từ ghi chú học riêng của owner nằm ngoài repo này. Tên khái niệm và link `L-NN` thì được.
- Ghi chú viết bằng tiếng Việt (quyết định của owner, 2026-11-21, là một ngoại lệ trong [R-DOC-03](../RULES_AND_CONSTRAINTS.md#r-doc-03)). Các thuật ngữ GLOSSARY giữ nguyên tiếng Anh ([R-DOC-01](../RULES_AND_CONSTRAINTS.md#r-doc-01)).

<a id="when-ai-writes-a-note"></a>
## Khi nào AI viết ghi chú

Viết ghi chú khi một task xây, sửa hoặc quyết định một trong các thứ sau:

| Loại | Ví dụ |
|---|---|
| Nghiệp vụ | Một quy tắc về tiền, Stock hay trạng thái Order; vì sao marketplace giữ tiền tới khi giao hàng; vì sao một Order chỉ có một Seller |
| Kỹ thuật | Một cơ chế chống concurrency, một DB constraint làm lưới an toàn, idempotency, một bước saga và Compensation của nó, Outbox, một retry policy |
| Đánh đổi | Một phương án bị loại, kèm lý do, khi lý do đó dạy được điều gì |

Không viết ghi chú cho CRUD đơn thuần, cấu hình hay đặt tên.

<a id="where-notes-go"></a>
## Ghi chú đặt ở đâu

- Mỗi Context một file: `docs/learning-notes/<context>.md` (ví dụ `inventory.md`).
- Chủ đề cắt ngang nhiều Context: `docs/learning-notes/<topic>.md` (ví dụ `money.md`, `idempotency.md`).
- Thêm ghi chú mới lên đầu file, và thêm file vào mục lục bên dưới.
- Báo mọi ghi chú đã viết trong báo cáo cuối của task, để owner biết cần đọc gì.

<a id="note-format"></a>
## Định dạng ghi chú

```markdown
## <Tiêu đề ngắn>

- [ ] Owner đã đọc
- **Loại:** nghiệp vụ | kỹ thuật | đánh đổi
- **Ở đâu:** <module, file hoặc spec> · rule [R-XX-NN](...) · khái niệm [L-NN](...)
- **Chuyện gì xảy ra:** 2 đến 4 câu.
- **Vì sao làm vậy:** vấn đề nó ngăn chặn; phương án thay thế và vì sao không chọn.
- **Có thể sai ở đâu:** lỗi hoặc edge case mà nó xử lý, hoặc vẫn chưa xử lý.
- **Tự kiểm tra:** 1 đến 3 câu hỏi để trả lời mà không nhìn lại (kiểu phỏng vấn).
- **Đọc thêm:** link trong repo; tên phổ biến của pattern hoặc bài báo để tra cứu.
```

Chỉ owner mới tick "Owner đã đọc".

<a id="index"></a>
## Mục lục

| File | Chủ đề |
|---|---|
| [money.md](money.md) | Tiền là số nguyên theo đơn vị nhỏ nhất |
| [ledger.md](ledger.md) | Tiền Seller chờ 7 ngày, rút tiền; phí sàn 5% và làm tròn; Ledger account là dữ liệu; double-entry; Ledger trước Payment |
| [ordering.md](ordering.md) | Ba state machine riêng; Seller xác nhận và Compensation; một Order thuộc về một Seller |
| [catalog.md](catalog.md) | Variant mặc định; Stock nằm trên Variant |
| [architecture.md](architecture.md) | Ranh giới modular monolith; call và event; một DB transaction dùng chung duy nhất |
| [api.md](api.md) | `Idempotency-Key`; lỗi dạng Problem Details |
| [inventory.md](inventory.md) | Flash sale và rate limit fail-open; lost update và ba phương án lock; vòng đời Stock reservation |
| [data.md](data.md) | Primary key UUID, v7 so với v4 |
| [events.md](events.md) | Outbox ở phía gửi, inbox ở phía nhận |
| [identity.md](identity.md) | Access token ngắn, refresh token xoay vòng |
