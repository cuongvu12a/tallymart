---
status: active
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [docs, backend]
related_code: []
---

# Ghi chú học tập: dữ liệu

Cách đọc các ghi chú này: [learning-notes/README](README.md).

## Primary key UUID, ưu tiên v7

- [ ] Owner đã đọc
- **Loại:** kỹ thuật, đánh đổi
- **Ở đâu:** mọi bảng · [CONVENTIONS: Data](../CONVENTIONS.md#data) · quyết định của owner, 2026-11-21 · khái niệm [L-17](../LEARNING_MODE.md#l-17), [L-20](../LEARNING_MODE.md#l-20)
- **Chuyện gì xảy ra:** Mọi bảng dùng primary key UUID. Ưu tiên UUIDv7 khi phiên bản PostgreSQL sinh được nó; nếu không thì dùng UUIDv4.
- **Vì sao làm vậy:**
  - ID auto-increment lộ ra trong API cho người ngoài biết có bao nhiêu Order và cho họ đoán ID khác (`/orders/1001`, `/orders/1002`).
  - Mỗi Context tự tạo ID mà không cần hỏi một sequence trung tâm, và một Context được tách ra vẫn giữ ID của mình mà không bị trùng.
  - UUIDv4 hoàn toàn ngẫu nhiên. Dòng mới rơi vào các page ngẫu nhiên của B-tree index, gây split page và làm hại cache trên bảng lớn. UUIDv7 bắt đầu bằng timestamp, nên dòng mới rơi gần cuối index, giống auto-increment.
  - Cái giá: 16 byte thay vì 8, và ID khó đọc hơn trong log.
- **Có thể sai ở đâu:** UUIDv7 làm lộ thời điểm tạo của một dòng. Với Order ở đây thì không sao, nhưng không phải loại ID nào cũng vậy.
- **Tự kiểm tra:**
  1. Vì sao key ngẫu nhiên làm insert vào B-tree chậm hơn key có thứ tự?
  2. Nêu một trường hợp UUIDv7 là lựa chọn tệ hơn UUIDv4.
- **Đọc thêm:** RFC 9562 (các phiên bản UUID, gồm v7); "UUID vs bigserial primary key PostgreSQL performance".
