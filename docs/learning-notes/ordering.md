---
status: active
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [docs, ordering]
related_code: []
---

# Ghi chú học tập: Ordering

Cách đọc các ghi chú này: [learning-notes/README](README.md).

## Ba state machine riêng: Order, Payment, Shipment

- [ ] Owner đã đọc
- **Loại:** kỹ thuật, đánh đổi
- **Ở đâu:** Ordering, Payment, Shipping · rule [R-ORD-01](../domain/ordering.md#r-ord-01), [R-SHP-01](../domain/shipping.md#r-shp-01) · đã quyết trong [Q-24](../OPEN_QUESTIONS.md#q-24)
- **Chuyện gì xảy ra:** Order chỉ giữ trạng thái nghiệp vụ (chờ thanh toán, đã trả, Seller đã xác nhận, đã giao, hoàn tất, đã huỷ). Payment có state machine riêng (pending, thành công, thất bại, đã refund). Shipment có state machine riêng nhận status thô từ Carrier. Order chỉ đổi trạng thái khi nhận event "sạch" từ Payment hay Shipping, ví dụ `Delivered`.
- **Vì sao làm vậy:**
  - Status từ Carrier rất "bẩn": tới trùng, tới sai thứ tự, có mã lạ. Nếu đổ thẳng vào Order, Order có thể nhảy lùi từ "đã giao" về "đang giao", và tiền Seller ([R-LED-03](../domain/ledger.md#r-led-03)) dựa vào một trạng thái không đáng tin.
  - Mỗi context sở hữu state của mình, đúng với ranh giới ở [architecture.md](architecture.md).
  - Bị loại: một state machine lớn gộp cả trạng thái giao hàng. Ít bảng hơn, nhưng mọi status nhiễu của Carrier đều chạm vào Order.
- **Có thể sai ở đâu:**
  - Trùng tên: trạng thái Order "delivered" và event `Delivered` của Shipping. Ordering spec phải đặt tên tách bạch trong GLOSSARY.
  - Một event tới khi Order đang ở trạng thái không cho phép (ví dụ `Delivered` cho Order đã huỷ). State machine phải từ chối và ghi lại, không được im lặng bỏ qua.
- **Tự kiểm tra:**
  1. Carrier gửi "đang giao" sau "đã giao". Lớp nào chặn, và Order có biết chuyện đó không?
  2. Vì sao tách state machine lại giúp test dễ hơn?
- **Đọc thêm:** "state machine pattern"; "XState statecharts" (chỉ để hiểu khái niệm).

## Seller xác nhận đơn, và Compensation khi Seller huỷ

- [ ] Owner đã đọc
- **Loại:** nghiệp vụ, kỹ thuật
- **Ở đâu:** Ordering · rule [R-ORD-02](../domain/ordering.md#r-ord-02), [R-ORD-05](../domain/ordering.md#r-ord-05), [R-PAY-04](../domain/payment.md#r-pay-04) · đã quyết trong [Q-25](../OPEN_QUESTIONS.md#q-25), [Q-38](../OPEN_QUESTIONS.md#q-38) · khái niệm [L-27](../LEARNING_MODE.md#l-27)
- **Chuyện gì xảy ra:** Sau khi Buyer trả tiền, Order chờ Seller xác nhận còn hàng trước khi tạo Shipment, có hạn chót. Nếu Seller huỷ hoặc quá hạn, saga chạy Compensation: nhả Stock và refund toàn phần cho Buyer. Bản thân dòng Order là state của saga; một job quét các Order bị kẹt ở một bước và chạy tiếp.
- **Vì sao làm vậy:**
  - Thực tế Seller có thể phát hiện hết hàng sau khi Buyer đã trả. Đây là bài Compensation rõ nhất: tiền đã vào, Stock đã giữ, giờ phải đảo cả hai mà Ledger vẫn cân.
  - Dùng dòng Order làm state thì chỉ có một nguồn sự thật. Mỗi bước phải idempotent, vì job có thể chạy lại một bước sau khi process crash.
  - Bị loại: bảng saga riêng (process manager). Mạnh hơn khi có nhiều saga khác nhau, nhưng thừa khi chỉ có checkout.
- **Có thể sai ở đâu:**
  - Refund thành công nhưng nhả Stock thất bại, rồi process crash. Job phải nhìn trạng thái Order và chạy tiếp đúng bước còn thiếu, không chạy lại refund.
  - Seller xác nhận đúng lúc job hết hạn huỷ Order: cùng kiểu race như Stock reservation hết hạn ([inventory.md](inventory.md)). Chỉ một bên được thắng.
- **Tự kiểm tra:**
  1. Liệt kê các bước của checkout và Compensation của từng bước.
  2. Process crash ngay sau khi refund xong. Lần chạy lại tiếp theo làm gì, và làm sao không refund hai lần?
  3. Vì sao Compensation không phải là "rollback"?
- **Đọc thêm:** "saga pattern orchestration" (microservices.io); "compensating transaction pattern" (Microsoft Azure Architecture Center).

## Một Order thuộc về đúng một Seller

- [ ] Owner đã đọc
- **Loại:** nghiệp vụ, đánh đổi
- **Ở đâu:** Ordering · rule [R-ORD-04](../domain/ordering.md#r-ord-04) · đã quyết trong [Q-05](../OPEN_QUESTIONS.md#q-05)
- **Chuyện gì xảy ra:** Một lần checkout chỉ gồm Product của một Seller. Nó tạo một Order với một Payment và một Shipment. Một Cart có Product của hai Seller không thể checkout nguyên như vậy.
- **Vì sao làm vậy:**
  - Trong marketplace, mỗi Seller giao hàng riêng, được trả tiền riêng, và tự trả Marketplace fee của mình. Nếu một Order trộn nhiều Seller, tất cả những thứ đó trở thành "theo từng dòng": state machine của Order, Refund, fee và việc trả tiền cho Seller. Đó là phương án phức tạp nhất mà lại dạy được ít điều mới.
  - Với một Seller mỗi Order, cả hai invariant đều dễ chứng minh hơn: Stock và tiền của một Order thuộc về một Seller.
  - Marketplace thật cho Buyer trả một lần cho nhiều Seller. Họ thường tách checkout thành mỗi Seller một Order dưới một bản ghi cha (chưa kiểm chứng với các marketplace Việt Nam cụ thể). Đó là phương án B, được giữ làm một [learning extension](../PROJECT_OVERVIEW.md#learning-extensions).
- **Có thể sai ở đâu (lần nâng cấp đã lên kế hoạch):** Trong phần lõi, một Payment trỏ tới một Order. Chuyển sang B nghĩa là thêm một bản ghi cha và trỏ Payment sang đó. Owner chấp nhận chi phí này: lần nâng cấp đó chính là nơi học partial failure (Seller 2 hết Stock sau khi Seller 1 đã reserve), Compensation và Refund một phần.
- **Tự kiểm tra:**
  1. Vì sao state machine "theo từng dòng" xuất hiện ngay khi một Order chứa hai Seller?
  2. Ở phương án B, Buyer trả một lần cho hai Order và một Seller hủy. Chuyện gì xảy ra với Payment, Ledger và Order còn lại?
  3. Khi chuyển từ A sang B, bảng nào đổi và bảng nào giữ nguyên?
- **Đọc thêm:** "order splitting marketplace"; "saga pattern partial failure".
