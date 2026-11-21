---
status: active
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [docs, backend]
related_code: []
---

# Ghi chú học tập: HTTP API

Cách đọc các ghi chú này: [learning-notes/README](README.md). Phần kiểm tra `Idempotency-Key` là phần owner tự viết ([L-12](../LEARNING_MODE.md#l-12)), nên ghi chú dưới đây giải thích các trường hợp và các bẫy, không đưa code.

## `Idempotency-Key`: một key, một tác dụng, kể cả sau crash

- [ ] Owner đã đọc
- **Loại:** kỹ thuật
- **Ở đâu:** mọi write API, đầu tiên là Stock reservation của Inventory · rule [R-API-01](../RULES_AND_CONSTRAINTS.md#r-api-01) · đã quyết trong [Q-04](../OPEN_QUESTIONS.md#q-04) · khái niệm [L-12](../LEARNING_MODE.md#l-12)
- **Chuyện gì xảy ra:** Client gửi một key ngẫu nhiên kèm mỗi lệnh ghi. Server lưu key, hash của request body và response vào một bảng Postgres, trong cùng DB transaction với lệnh ghi nghiệp vụ. Request lặp lại với cùng key nhận response đã lưu và không thay đổi gì. Key hết hạn sau 24 giờ.
- **Vì sao làm vậy:**
  - "Timeout không phải là thất bại." Khi request bị timeout, client không thể biết server đã làm xong việc hay chưa. Retry an toàn duy nhất là retry mà server nhận ra được.
  - Dòng key và lệnh ghi nghiệp vụ phải commit cùng nhau. Nếu lưu key trước rồi process crash trước khi ghi, lần retry bị bỏ qua sai; nếu lệnh ghi commit trước rồi mất key, lần retry làm việc hai lần.
  - Chỉ dùng Redis thì bị loại: nó không nằm trong DB transaction, và Redis restart là mất key.
  - Provider (IPN, webhook của Carrier) không gửi header này, nên endpoint tự dựng key từ ID của provider và dùng cùng bảng. Một cơ chế, một bộ test.
- **Các trường hợp cần xử lý:**

  | Trường hợp | Phản hồi |
  |---|---|
  | Request đầu tiên | Làm việc, lưu response |
  | Cùng key, cùng body, đã xong | Response đã lưu |
  | Cùng key, body khác | 422: client dùng lại key do nhầm |
  | Cùng key, request đầu vẫn đang chạy | 409: retry sau |
  | Không có key | 400 |

- **Có thể sai ở đâu:**
  - Hai request cùng key tới cùng một lúc. Cả hai đều thấy "chưa có dòng nào". Unique constraint trên key phải làm một trong hai fail; code phải biến lỗi đó thành trường hợp 409, không phải 500.
  - Key chỉ được scope theo chuỗi key. Hai user tình cờ chọn cùng một key sẽ đụng nhau. Scope phải theo user và endpoint.
  - Response được lưu trước khi transaction commit, rồi transaction rollback. Khi đó request lặp lại trả về thành công cho một việc chưa từng xảy ra.
- **Tự kiểm tra:**
  1. Vì sao dòng key và lệnh ghi nghiệp vụ phải nằm trong một DB transaction? Mô tả kiểu crash làm hỏng mỗi thứ tự còn lại.
  2. Hai request giống hệt nhau tới cách nhau 1 ms. Đi qua từng bước xem mỗi request thấy gì.
  3. Vì sao body khác mà cùng key là lỗi, chứ không phải một request mới?
- **Đọc thêm:** IETF draft "The Idempotency-Key HTTP Header Field"; bài của Stripe "Designing robust and predictable APIs with idempotency"; bài của Brandur Leach "Implementing Stripe-like idempotency keys in Postgres".

## Lỗi dạng Problem Details với `code` ổn định

- [ ] Owner đã đọc
- **Loại:** kỹ thuật
- **Ở đâu:** mọi endpoint · rule [R-API-02](../RULES_AND_CONSTRAINTS.md#r-api-02) · đã quyết trong [Q-03](../OPEN_QUESTIONS.md#q-03) · khái niệm [L-11](../LEARNING_MODE.md#l-11)
- **Chuyện gì xảy ra:** Mọi lỗi đều là `application/problem+json` với `type`, `title`, `status`, `detail` và một `code` ổn định như `STOCK_NOT_ENOUGH`.
- **Vì sao làm vậy:** Status code nói nhóm vấn đề; `code` nói chính xác là lỗi nào, ở dạng chương trình có thể rẽ nhánh và test có thể assert. Client cần nó để quyết định "retry" (409 đang xử lý, 429) hay "không retry" (409 không đủ Stock, 422). Một định dạng chuẩn cũng giúp client được generate có kiểu cho mọi lỗi.
- **Có thể sai ở đâu:** Hai lỗi khác nhau dùng chung một `code`, hoặc một `code` bị đổi tên làm client cũ vỡ. Hãy coi các giá trị `code` là một phần của hợp đồng API.
- **Tự kiểm tra:**
  1. "Không đủ Stock" và "request vẫn đang xử lý" đều là 409. Client phân biệt chúng thế nào, và nên làm gì với mỗi cái?
  2. Vì sao 422 tốt hơn 400 cho trường hợp dùng lại `Idempotency-Key` với body khác?
- **Đọc thêm:** RFC 9457 "Problem Details for HTTP APIs".
