---
status: active
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [docs]
related_code: []
---

# Ghi chú học tập: tiền

Cách đọc các ghi chú này: [learning-notes/README](README.md).

## Tiền là số nguyên theo đơn vị nhỏ nhất, không bao giờ là float

- [ ] Owner đã đọc
- **Loại:** kỹ thuật
- **Ở đâu:** mọi bảng và mọi field API chứa tiền · [CONVENTIONS: Money](../CONVENTIONS.md#money) · đã quyết trong [Q-12](../OPEN_QUESTIONS.md#q-12) · khái niệm [L-20](../LEARNING_MODE.md#l-20)
- **Chuyện gì xảy ra:** Một số tiền được lưu là số nguyên theo đơn vị nhỏ nhất của loại tiền, trong cột `bigint`, đi kèm cột `currency` chứa mã ISO 4217 như `VND`. Trong TypeScript nó là `bigint` hoặc một kiểu Money nhỏ. Trong JSON nó đi dưới dạng string, ví dụ `{"amount": "150000", "currency": "VND"}`.
- **Vì sao làm vậy:**
  - Float (JS `number`, SQL `float`) không biểu diễn chính xác được hầu hết các phân số thập phân. `0.1 + 0.2` ra `0.30000000000000004`. Nếu các Ledger entry mang sai số kiểu này, tổng của chúng không đúng bằng 0, và [R-LED-01](../domain/ledger.md#r-led-01) bị vi phạm vì một lý do chẳng liên quan gì tới nghiệp vụ.
  - Số nguyên thì không có làm tròn. Khi đó việc làm tròn chỉ xảy ra ở chỗ nghiệp vụ quyết định, ví dụ khi tính Marketplace fee theo phần trăm ([Q-19](../OPEN_QUESTIONS.md#q-19)).
  - Phần lớn client đọc số trong JSON thành JS `number`. JS `number` chỉ chính xác tới 2^53 − 1 (khoảng 9 × 10^15). Dùng string thì tránh được giới hạn này và mọi mất mát âm thầm.
  - Cột `currency` bây giờ chỉ tốn một cột. Không có nó, sau này thêm loại tiền thứ hai sẽ phải migrate mọi dòng chứa tiền.
  - Bị loại: số thập phân `numeric(19,4)`. Nó cũng chính xác, nhưng cần một thư viện decimal trong TypeScript (một dependency mới) và dễ bị trộn nhầm với `number` thường.
- **Có thể sai ở đâu:**
  - Ai đó parse string JSON bằng `Number(...)` rồi tính toán trên đó. Hệ thống kiểu nên làm việc này khó xảy ra (kiểu Money, hoặc `bigint`).
  - Cộng hai số tiền khác loại tiền. Code cộng tiền phải kiểm tra cùng một currency.
  - Một fee phần trăm bị làm tròn ở hai chỗ theo hai cách. Chỉ một quy tắc làm tròn, trong một hàm ([Q-19](../OPEN_QUESTIONS.md#q-19)).
- **Tự kiểm tra:**
  1. Vì sao float phá vỡ "tổng Ledger entry = 0" ngay cả khi mọi bước nghiệp vụ đều đúng?
  2. Vì sao gửi tiền dạng string trong JSON thay vì dạng number?
  3. Một fee là 2.5% của 99,999 VND. Làm tròn ở đâu, làm tròn thế nào, và phần dư đi đâu?
- **Đọc thêm:** "floating point arithmetic decimal" (IEEE 754); pattern "Money" của Martin Fowler; ISO 4217 minor units.
