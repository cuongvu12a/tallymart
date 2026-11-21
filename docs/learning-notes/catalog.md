---
status: active
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [docs, catalog, inventory]
related_code: []
---

# Ghi chú học tập: Catalog

Cách đọc các ghi chú này: [learning-notes/README](README.md).

## Mọi Product đều có Variant; Stock nằm trên Variant

- [ ] Owner đã đọc
- **Loại:** kỹ thuật, đánh đổi
- **Ở đâu:** Catalog và Inventory · rule [R-CAT-01](../domain/catalog.md#r-cat-01) · đã quyết trong [Q-13](../OPEN_QUESTIONS.md#q-13) · khái niệm [L-16](../LEARNING_MODE.md#l-16), [L-20](../LEARNING_MODE.md#l-20)
- **Chuyện gì xảy ra:** Product là thứ Buyer duyệt xem ("Áo thun cotton"). Variant là thứ Buyer thực sự mua ("Áo thun cotton, size M, màu đen"). Price và Stock thuộc về Variant. Một Product không có tùy chọn nào vẫn có một Variant mặc định.
- **Vì sao làm vậy:**
  - Lock Stock ([R-INV-02](../domain/inventory.md#r-inv-02)) cần đúng một dòng để lock cho mỗi đơn vị bán được. Nếu Product đơn giản giữ Stock trên Product còn Product khác giữ trên Variant, sẽ có hai nhánh code lock, và test concurrency phải phủ cả hai.
  - Sau này chuyển Stock từ Product sang Variant nghĩa là migrate Stock và mọi Stock reservation, đụng thẳng vào [R-INV-01](../domain/inventory.md#r-inv-01). Thêm một dòng cho mỗi Product đơn giản thì rẻ; lần migrate đó thì không.
  - Đây là ý tưởng chung "một nhánh code": thêm một giá trị mặc định thay vì một trường hợp đặc biệt.
- **Có thể sai ở đâu:**
  - UI hiện "Stock" của Product là tổng qua các Variant, rồi ai đó viết code reserve dựa trên tổng đó. Reservation luôn nhắm vào một Variant.
  - Variant mặc định bị xóa trong khi còn Order trỏ tới nó. Variant đã bán nên được ngừng dùng (retire), không xóa.
- **Tự kiểm tra:**
  1. Vì sao "Stock trên Product cho Product đơn giản" tạo ra hai chỗ để một bug Oversell ẩn nấp?
  2. Một Stock reservation lock dòng nào, và vì sao phải đúng một dòng?
  3. Seller thêm size cho một Product vốn chỉ có Variant mặc định. Stock hiện có của nó sẽ ra sao?
- **Đọc thêm:** "product variant SKU data model"; "special case pattern" vs "null object".
