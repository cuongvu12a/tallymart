---
status: active
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [docs, backend]
related_code: []
---

# Ghi chú học tập: kiến trúc

Cách đọc các ghi chú này: [learning-notes/README](README.md). Public interface của Module là phần owner tự viết ([L-10](../LEARNING_MODE.md#l-10)), nên các ghi chú này giải thích ý tưởng và các bẫy, không đưa code.

## Modular monolith với ranh giới được kiểm bằng công cụ

- [ ] Owner đã đọc
- **Loại:** kỹ thuật, đánh đổi
- **Ở đâu:** toàn bộ `apps/api` · rule [R-ARCH-01](../RULES_AND_CONSTRAINTS.md#r-arch-01), [R-ARCH-02](../RULES_AND_CONSTRAINTS.md#r-arch-02) · bố cục [CONVENTIONS: Code layout](../CONVENTIONS.md#code-layout) · đã quyết trong [Q-01](../OPEN_QUESTIONS.md#q-01) · khái niệm [L-10](../LEARNING_MODE.md#l-10)
- **Chuyện gì xảy ra:** Một app deploy duy nhất, chia thành mỗi Context một NestJS module. Mỗi Context sở hữu các bảng của nó trong Postgres schema riêng và expose một public interface (`index.ts`). Một lint rule làm build fail khi code import phần bên trong của Context khác.
- **Vì sao làm vậy:**
  - Monolith tránh được lỗi mạng và distributed transaction, hai thứ sẽ đe dọa cả hai invariant ([R-ARCH-01](../RULES_AND_CONSTRAINTS.md#r-arch-01)).
  - Nhưng monolith không có ranh giới sẽ thành "big ball of mud": code nào cũng update được bảng nào. Khi đó "chỉ Inventory được đổi Stock" là mong muốn, không phải sự thật.
  - Schema riêng và public interface giữ lại khả năng tách một Context ra sau này: dữ liệu và điểm vào của nó đã tách sẵn.
  - Các layer (`domain`, `application`, `infrastructure`, `api`) giữ quy tắc nghiệp vụ trong TypeScript thuần, nên các test quan trọng nhất chạy không cần DB và không cần NestJS.
  - Bị loại: NestJS module phẳng dùng chung bảng (ranh giới chỉ dựa vào kỷ luật), và mỗi Context một pnpm package (quá nhiều tooling cho một developer).
- **Có thể sai ở đâu:**
  - Public interface phình thành bản sao của phần bên trong ("expose hết"). Hãy expose use case ("reserve Stock"), không expose bảng hay entity.
  - Tạo sẵn layer rỗng "để sau dùng". Chỉ thêm layer khi nó có code.
  - Một báo cáo cần dữ liệu từ ba Context, và ai đó join xuyên schema. Hãy dùng interface của từng Context, hoặc xây read model sau ([L-36](../LEARNING_MODE.md#l-36)).
- **Tự kiểm tra:**
  1. Chính xác thì cái gì ngăn Ordering chạy `UPDATE` trên bảng của Inventory, và vì sao ở đây công cụ tốt hơn code review?
  2. Những phần nào của một Context sẽ chuyển đi nguyên vẹn nếu nó được tách thành một service?
  3. Khi nào modular monolith là lựa chọn tốt hơn microservices? Nêu hai lý do.
- **Đọc thêm:** "modular monolith" (Kamil Grzybek, Simon Brown); "hexagonal architecture / ports and adapters"; "bounded context" (Domain-Driven Design).

## Call để lấy câu trả lời, event để báo sự thật; chỉ một transaction dùng chung

- [ ] Owner đã đọc
- **Loại:** kỹ thuật, đánh đổi
- **Ở đâu:** [ARCHITECTURE: Data flow](../ARCHITECTURE.md#data-flow) · rule [R-ARCH-03](../RULES_AND_CONSTRAINTS.md#r-arch-03) · đã quyết trong [Q-02](../OPEN_QUESTIONS.md#q-02) · khái niệm [L-09](../LEARNING_MODE.md#l-09), [L-27](../LEARNING_MODE.md#l-27)
- **Chuyện gì xảy ra:** Khi một Context cần câu trả lời ngay ("còn Stock không?"), nó gọi Context kia in-process. Khi một việc đã xảy ra (`OrderPaid`, `Delivered`), nó publish một Event và các Context khác phản ứng. Một DB transaction không bao giờ trải qua hai Context, trừ Payment → Ledger.
- **Vì sao làm vậy:**
  - Buyer đang chờ ở trang checkout; một Event không thể trả lời "còn Stock không?" trước khi trang timeout. Một call thì được.
  - Event hợp với những sự thật mà nhiều Context sẽ phản ứng sau, và giúp bên publish không cần biết ai đang nghe.
  - Một transaction xuyên nhiều Context sẽ che giấu coupling và sẽ vỡ vào ngày một Context bị tách ra. Vì vậy các bước có thể fail xuyên Context dùng Compensation thay thế ([R-ORD-02](../domain/ordering.md#r-ord-02)).
  - Payment → Ledger là ngoại lệ duy nhất: một payment đã ghi mà thiếu Ledger entry sẽ vi phạm [R-LED-01](../domain/ledger.md#r-led-01), và Compensation không sửa được khoản tiền chưa từng được ghi.
- **Có thể sai ở đâu:**
  - Ordering gọi Inventory, call thành công, rồi Payment fail. Không có Compensation thì Stock vẫn bị reserve tới khi hết TTL.
  - Một Event được publish trước khi DB transaction commit; sau đó transaction rollback, nhưng listener đã hành động rồi. Đây là lý do có Outbox ([R-EVT-01](../RULES_AND_CONSTRAINTS.md#r-evt-01), [L-26](../LEARNING_MODE.md#l-26)).
- **Tự kiểm tra:**
  1. Vì sao "reserve Stock" là call chứ không phải Event?
  2. Transaction dùng chung Payment → Ledger sẽ tốn gì nếu một ngày Payment bị tách ra?
  3. Liệt kê từng bước xuyên Context trong checkout và Compensation của nó.
- **Đọc thêm:** "orchestration vs choreography"; "saga pattern" (Chris Richardson, microservices.io); "dual write problem".
