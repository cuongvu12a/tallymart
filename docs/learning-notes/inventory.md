---
status: active
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [docs, inventory]
related_code: []
---

# Ghi chú học tập: Inventory

Cách đọc các ghi chú này: [learning-notes/README](README.md). SQL lock, DB transaction reserve và các bảng Inventory là phần owner tự viết ([L-15](../LEARNING_MODE.md#l-15), [L-16](../LEARNING_MODE.md#l-16), [L-20](../LEARNING_MODE.md#l-20)), nên các ghi chú này giải thích vấn đề, các phương án và các bẫy, không bao giờ đưa code lời giải.

## Flash sale: pool Stock riêng, và rate limit fail-open

- [ ] Owner đã đọc
- **Loại:** nghiệp vụ, kỹ thuật
- **Ở đâu:** Inventory · rule [R-INV-04](../domain/inventory.md#r-inv-04), [R-INV-06](../domain/inventory.md#r-inv-06) · đã quyết trong [Q-16](../OPEN_QUESTIONS.md#q-16), [Q-17](../OPEN_QUESTIONS.md#q-17), [Q-46](../OPEN_QUESTIONS.md#q-46) · khái niệm [L-23](../LEARNING_MODE.md#l-23)
- **Chuyện gì xảy ra:** Một Flash sale có khung giờ, Price riêng, pool Stock riêng tách khỏi Stock thường, và giới hạn số lượng mỗi user. Trước DB có một rate limiter token bucket trong Redis cho từng user. Nếu Redis chết, request vẫn được phục vụ (fail-open), vì DB mới là chỗ chặn oversell.
- **Vì sao làm vậy:**
  - Pool riêng: sale không ăn mất Stock của đơn thường, và test concurrency khớp đúng ví dụ README (Stock 10, 50 Buyer). Trong test, với 1 đơn vị mỗi request, không cap, không rate limit, phải đúng 10 request thành công.
  - Rate limiter bảo vệ capacity và sự công bằng (bot không spam được), không bảo vệ bất biến. Vì vậy nó được phép hỏng mà không gây oversell.
  - Token bucket cho phép một cú burst nhỏ rồi giới hạn đều, mượt hơn fixed window (fixed window cho phép gấp đôi giới hạn ở ranh giới hai cửa sổ).
- **Có thể sai ở đâu:**
  - Nhiều instance API cùng đọc rồi ghi bucket trong Redis: race. Đọc và trừ token phải là một thao tác atomic (một script).
  - Đặt con số giới hạn bằng cảm tính. Quyết định là đo bằng k6 trước rồi mới chốt.
  - Chọn fail-closed "cho chắc": Redis chết là cả sale chết, trong khi DB vẫn đủ sức chặn oversell.
- **Tự kiểm tra:**
  1. Vì sao rate limiter không thể là thứ bảo vệ R-INV-01?
  2. Fixed window 10 request/phút: user gửi được tối đa bao nhiêu request trong 2 giây quanh mốc chuyển phút?
  3. Khi nào fail-closed mới là lựa chọn đúng?
- **Đọc thêm:** "token bucket vs sliding window rate limiting"; "Redis rate limiting Lua script"; "fail open vs fail closed".

## Vì sao "kiểm tra rồi ghi" không được bảo vệ sẽ gây oversell

- [ ] Owner đã đọc
- **Loại:** kỹ thuật
- **Ở đâu:** Inventory · rule [R-INV-01](../domain/inventory.md#r-inv-01), [R-INV-02](../domain/inventory.md#r-inv-02) · đã quyết trong [Q-15](../OPEN_QUESTIONS.md#q-15) · khái niệm [L-15](../LEARNING_MODE.md#l-15), [L-16](../LEARNING_MODE.md#l-16)
- **Chuyện gì xảy ra:** Hai request cùng lúc đọc được "còn 1". Cả hai đều qua bước kiểm tra. Cả hai đều ghi. Bán ra hai đơn vị, trong khi chỉ có một. Đây là lost update, và isolation level mặc định của PostgreSQL (Read Committed) không ngăn được nó.
- **Ba phương án bạn sẽ tự xây trong bài lab, và mỗi cái dạy gì:**

  | Phương án | Ý tưởng | Cần để ý |
  |---|---|---|
  | Pessimistic lock (`SELECT … FOR UPDATE`) | Lock dòng, rồi kiểm tra và ghi | Lock bị giữ trong lúc chạy app code; chậm khi Flash sale; thứ tự lock và deadlock khi có nhiều dòng |
  | Conditional update (bản được ship) | Đưa bước kiểm tra vào trong lệnh ghi, để DB quyết định trong một bước | Quy tắc phải gói được trong một điều kiện SQL; "0 dòng bị đổi" là tín hiệu "không đủ Stock" |
  | Optimistic lock (cột `version`) | Chỉ ghi nếu không ai đổi dòng đó kể từ lúc bạn đọc | Nhiều retry trên một dòng nóng; vòng retry cần giới hạn |

  Ở mọi phương án, constraint `CHECK (available >= 0)` là lớp bảo vệ thứ hai: nếu code sai, DB vẫn từ chối.
- **Vì sao bản conditional update được ship:** nó đúng ngay từ cấu trúc (không có khe hở giữa kiểm tra và ghi) và giữ row lock trong thời gian ngắn nhất. Hãy đo cả ba bằng cùng một test trước khi tin điều đó.
- **Có thể sai ở đâu:**
  - Test chạy các request lần lượt, không thực sự song song, và pass vì lý do sai. Hãy cho chúng bắt đầu cùng lúc, bằng một barrier.
  - Reserve nhiều Variant trong một Order khiến hai request lock các dòng theo thứ tự khác nhau → deadlock. Luôn lock theo một thứ tự cố định (ví dụ theo Variant ID).
  - Lỗi của constraint `CHECK` tới client thành 500. Hãy map nó sang lỗi 409 `STOCK_NOT_ENOUGH` ([R-API-02](../RULES_AND_CONSTRAINTS.md#r-api-02)).
- **Tự kiểm tra:**
  1. Vì sao Read Committed không chặn được lost update ở đây? Serializable có chặn được không, và với giá nào?
  2. Với 50 request song song trên Stock 10, đoán số lần retry của optimistic lock. Rồi đo thật.
  3. Vì sao vẫn giữ constraint `CHECK` nếu code đã đúng?
- **Đọc thêm:** tài liệu PostgreSQL "Transaction Isolation" và "Explicit Locking"; Martin Kleppmann, *Designing Data-Intensive Applications*, chương 7 (lost updates, write skew).

## Một Stock reservation kết thúc theo đúng một cách

- [ ] Owner đã đọc
- **Loại:** nghiệp vụ, kỹ thuật
- **Ở đâu:** Inventory · rule [R-INV-05](../domain/inventory.md#r-inv-05) · đã quyết trong [Q-14](../OPEN_QUESTIONS.md#q-14) · giá trị TTL chờ [Q-22](../OPEN_QUESTIONS.md#q-22)
- **Chuyện gì xảy ra:** Đặt Order sẽ reserve Stock trong một khoảng TTL. Sau đó xảy ra đúng một trong hai việc: payment thành công và reservation thành trừ kho chính thức, hoặc hết TTL (hoặc payment fail) và Stock được trả lại. Một payment tới sau khi đã trả Stock sẽ thử reserve lại; nếu không còn Stock, Buyer được refund tự động.
- **Vì sao làm vậy:**
  - Reserve lúc "thêm vào Cart" thì Cart có thể chiếm giữ Stock (bot rất thích điều này trong Flash sale). Chỉ reserve lúc thanh toán nghĩa là Buyer có thể trả tiền rồi mới biết hết Stock. Reserve lúc checkout là khoảng hở nhỏ nhất mà vẫn đảm bảo Stock cho Buyer trả tiền đúng hạn.
  - TTL phải ít nhất bằng thời hạn thanh toán; nếu không, Buyer trả đúng hạn vẫn có thể mất Stock.
- **Có thể sai ở đâu:** Job hết hạn và IPN handler cùng xử lý một reservation vào cùng một lúc. Nếu cả hai dùng "đọc trạng thái, rồi ghi", cả hai đều có thể thắng: Stock vừa được trả lại vừa bị trừ. Mỗi bên chỉ được đổi reservation "khi nó vẫn còn active", để đúng một bên đổi được một dòng và bên kia thấy 0 dòng.
- **Tự kiểm tra:**
  1. Vẽ các trạng thái của một Stock reservation và mọi chuyển trạng thái. Những chuyển trạng thái nào có thể race?
  2. IPN tới 1 giây sau khi hết hạn và Stock đã bán cho người khác. Buyer thấy gì, và có những Ledger entry nào?
  3. Vì sao TTL gắn với payment timeout chứ không chọn riêng?
- **Đọc thêm:** "reservation pattern"; "TTL-based stock hold e-commerce".
