---
status: active
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [docs, ledger]
related_code: []
---

# Ghi chú học tập: Ledger

Cách đọc các ghi chú này: [learning-notes/README](README.md). Ledger builder là phần owner tự viết ([L-03](../LEARNING_MODE.md#l-03)), nên các ghi chú này giải thích vấn đề và các bẫy, không đưa code.

## Tiền của Seller chờ 7 ngày sau `Delivered`, rút tiền phải được duyệt

- [ ] Owner đã đọc
- **Loại:** nghiệp vụ, đánh đổi
- **Ở đâu:** Ledger · rule [R-LED-03](../domain/ledger.md#r-led-03), [R-LED-06](../domain/ledger.md#r-led-06) · đã quyết trong [Q-20](../OPEN_QUESTIONS.md#q-20), [Q-47](../OPEN_QUESTIONS.md#q-47)
- **Chuyện gì xảy ra:** Khi Buyer trả tiền, tiền của Seller nằm ở tài khoản "Seller pending". Sau event `Delivered` thêm N = 7 ngày (một setting) mới chuyển sang "Seller available". Seller chỉ rút được tiền available, phải có eKYC, và mỗi Withdrawal phải được Admin duyệt. Tiền đi ra qua một port chuyển khoản, trong core chỉ có Fake implementation.
- **Vì sao làm vậy:**
  - Tiền đã rời sàn thì không lấy lại được. Nếu Seller rút ngay lúc `Delivered` rồi Buyer khiếu nại, ví Seller có thể bị âm và sàn phải chịu.
  - 7 ngày là "return window": chỗ chừa sẵn cho Return (một learning extension). Hiện chưa có Return, nhưng Admin vẫn refund toàn phần được trong khoảng này ([R-PAY-04](../domain/payment.md#r-pay-04)).
  - Đây đúng là xung đột thật giữa các vai: Seller muốn tiền nhanh (dòng tiền), Buyer và Admin muốn giữ lâu (an toàn). Hiện ngày tiền về cho từng Order là cách làm dịu xung đột mà không phá an toàn.
  - Bị loại: trả ngay lúc `Delivered` (không có chỗ cho Return), và trả một phần sớm (thêm luồng tiền khi Ledger còn chưa chứng minh xong).
- **Có thể sai ở đâu:**
  - Job chuyển "pending → available" chạy hai lần cho cùng Order. Cần một khoá nguồn duy nhất cho nhóm bút toán ([R-LED-07](../domain/ledger.md#r-led-07)).
  - N đổi từ 7 sang 3: Order cũ dùng N nào? Nên tính ngày tiền về lúc `Delivered` và lưu lại, giống rate phí lưu trên Order.
- **Tự kiểm tra:**
  1. Vẽ đường đi của 100,000 VND từ lúc Buyer trả tiền tới lúc Seller rút, qua từng Ledger account.
  2. Vì sao "available" chỉ được sinh ra từ "pending", không bao giờ trực tiếp từ Payment?
  3. Vì sao rút tiền cần cả eKYC lẫn Admin duyệt, trong khi bán hàng thì không?
- **Đọc thêm:** "marketplace escrow payout delay"; "settlement period marketplace".

## Phí sàn 5%, lưu trên Order, làm tròn xuống

- [ ] Owner đã đọc
- **Loại:** nghiệp vụ, kỹ thuật
- **Ở đâu:** Ledger · rule [R-LED-05](../domain/ledger.md#r-led-05) · đã quyết trong [Q-19](../OPEN_QUESTIONS.md#q-19) · liên quan [money.md](money.md)
- **Chuyện gì xảy ra:** Lúc đặt Order, rate phí hiện tại (5%) được chép lên Order. Lúc giao thành công, phí được tính từ rate đã lưu và làm tròn xuống tới đồng VND. Ví dụ Order 99,999 VND: 5% là 4,999.95, phí thu là 4,999 VND.
- **Vì sao làm vậy:**
  - Rate lưu trên Order thì đổi rate sau này không làm thay đổi Order cũ, và Reconciliation tính lại được đúng phí của mọi Order trong quá khứ. Đây là ý "snapshot" (khái niệm [L-20](../LEARNING_MODE.md#l-20)).
  - Thu phí lúc giao thành công thì một Order bị refund trước đó không cần bút toán đảo phí.
  - Chỉ một quy tắc làm tròn, ở một chỗ. Làm tròn xuống là lợi cho Seller, nên không ai phàn nàn bị thu dư.
- **Có thể sai ở đâu:**
  - Tính phí bằng float rồi mới làm tròn: sai số trôi vào Ledger ([money.md](money.md)). Tính bằng số nguyên: `amount * 5 / 100` với phép chia nguyên đã là làm tròn xuống, nhưng phải chú ý thứ tự nhân trước chia sau.
  - Hai chỗ trong code cùng tính phí: một chỗ hiển thị cho Seller, một chỗ ghi Ledger, rồi lệch nhau 1 đồng.
- **Tự kiểm tra:**
  1. Vì sao phải lưu rate trên Order thay vì lưu sẵn số tiền phí?
  2. Với số nguyên, `amount / 100 * 5` và `amount * 5 / 100` khác nhau thế nào?
  3. Admin đổi rate từ 5% sang 6% giữa chừng. Order nào bị ảnh hưởng?
- **Đọc thêm:** "banker's rounding vs round half up"; "snapshot pattern order price".

## Ledger account là dữ liệu, không phải code

- [ ] Owner đã đọc
- **Loại:** kỹ thuật, đánh đổi
- **Ở đâu:** Ledger · rule [R-LED-04](../domain/ledger.md#r-led-04) · đã quyết trong [Q-18](../OPEN_QUESTIONS.md#q-18) và [Q-35](../OPEN_QUESTIONS.md#q-35)
- **Chuyện gì xảy ra:** Một Ledger account là một dòng, xác định bởi ba thứ: loại account (ví dụ "Seller available"), Account holder (holder type + holder ID, ví dụ Seller 42) và currency. Mỗi Ledger entry trỏ tới đúng một account. Một kiểu người giữ tiền mới, như Carrier thu tiền COD, được thêm vào dưới dạng dữ liệu mới.
- **Vì sao làm vậy:**
  - Ledger entry là append-only ([R-LED-02](../domain/ledger.md#r-led-02)). Một entry ghi hôm nay không bao giờ được sửa. Vì vậy thứ mà entry trỏ tới hôm nay vẫn phải còn hợp lý khi xuất hiện các loại account mới.
  - Phương án tồi là mỗi account một cột hoặc một nhánh code, ví dụ cột `seller_wallet_balance`. Khi đó COD, Voucher hay khấu trừ thuế đều cần đổi schema, và entry cũ không thể chuyển sang cấu trúc mới mà không sửa lịch sử.
  - Đây là ý tưởng "chừa chỗ trong thiết kế bây giờ, xây sau": COD chưa được xây ([learning extensions](../PROJECT_OVERVIEW.md#learning-extensions)), nhưng mô hình chứa được nó mà không cần migrate dữ liệu tiền.
- **Có thể sai ở đâu:**
  - "Số dư" được lưu thành một con số trên account và cập nhật tại chỗ. Khi đó số dư và các entry có thể lệch nhau. Entry mới là sự thật; số dư là tổng các entry (hoặc một cache của tổng đó, có thể tính lại).
  - Một account được tạo tùy hứng, với loại account bị gõ sai. Loại account nên lấy từ một danh sách cố định trong DB, không phải text tự do.
- **Tự kiểm tra:**
  1. Vì sao "append-only" khiến mô hình account khó đổi về sau hơn một bảng thường?
  2. Tiền của Seller nằm ở đâu trong khoảng giữa `OrderPaid` và lúc giao hàng thành công, và entry nào chuyển nó sang "available"?
  3. Năm sau thêm COD. Liệt kê các dòng và code mới cần có, và chỉ ra rằng không Ledger entry hiện có nào bị đổi.
- **Đọc thêm:** "double-entry bookkeeping"; "Accounting Patterns" của Martin Fowler (Account, Entry); các bài viết về ledger của Modern Treasury.

## Double-entry: mọi lần dịch chuyển tiền có tổng bằng 0

- [ ] Owner đã đọc
- **Loại:** nghiệp vụ, kỹ thuật
- **Ở đâu:** Ledger · rule [R-LED-01](../domain/ledger.md#r-led-01), [R-LED-02](../domain/ledger.md#r-led-02) · còn mở: cách ép buộc, [Q-49](../OPEN_QUESTIONS.md#q-49) · khái niệm [L-03](../LEARNING_MODE.md#l-03)
- **Chuyện gì xảy ra:** Tiền không bao giờ tự sinh ra hay tự biến mất. Mỗi lần dịch chuyển là một nhóm Ledger entry, cộng ở một account và trừ ở account khác, và mỗi nhóm có tổng bằng 0. Nếu mọi nhóm có tổng bằng 0 thì toàn bộ Ledger có tổng bằng 0.
- **Vì sao làm vậy:** Với bản ghi một phía ("Seller wallet +100"), một bug có thể tạo ra tiền từ hư không mà không ai để ý. Với hai phía, thiếu một phía sẽ lộ ra thành tổng khác 0, và một test hoặc một lần kiểm tra hằng đêm bắt được. Sửa sai nghĩa là thêm một nhóm đảo ngược, nhờ vậy lịch sử những gì đã xảy ra vẫn nhìn thấy được cho Reconciliation.
- **Có thể sai ở đâu:**
  - Process crash giữa hai lệnh insert, chỉ một nửa nhóm được ghi. Cả nhóm phải nằm trong một DB transaction.
  - Nhóm được kiểm tra trong code, nhưng một đoạn code khác insert entry trực tiếp. Đó là lý do [Q-49](../OPEN_QUESTIONS.md#q-49) hỏi DB có nên kiểm tra thêm không.
  - Cùng một sự kiện tiền được ghi hai lần (IPN hoặc event `Delivered` bị lặp). Mỗi nhóm cần một source key unique để lần lặp không có tác dụng ([Q-27](../OPEN_QUESTIONS.md#q-27)).
- **Tự kiểm tra:**
  1. Buyer trả 100,000 VND bằng thẻ. Viết các entry (account và dấu) cho lần thanh toán, rồi cho lần giao hàng thành công với Marketplace fee 5%.
  2. Vì sao "tổng toàn bộ Ledger = 0" không đủ để chứng minh một lần dịch chuyển cụ thể là đúng?
  3. Sửa một fee bị sai thế nào mà không sửa entry nào?
- **Đọc thêm:** "double-entry accounting for engineers"; "idempotent ledger posting".

## Xây Ledger trước Payment

- [ ] Owner đã đọc
- **Loại:** đánh đổi
- **Ở đâu:** [Build order](../PROJECT_OVERVIEW.md#build-order) · đã quyết trong [Q-09](../OPEN_QUESTIONS.md#q-09)
- **Chuyện gì xảy ra:** Ledger là bước 2 trong Build order; Payment là bước 3. Ngay từ Payment đầu tiên, mọi khoản tiền đều được ghi vào Ledger double-entry.
- **Vì sao làm vậy:** Nếu Payment làm trước, sẽ có một giai đoạn tiền dịch chuyển mà không có Ledger. Code viết trong giai đoạn đó thường ghi tiền vào bảng riêng của nó, rồi sau này phải gò Ledger quanh nó. Xây Ledger trước thì invariant đúng ngay từ ngày đầu.
- **Có thể sai ở đâu:** Ledger được thiết kế khi chưa có caller thật nên thiếu thứ Payment cần. Cách giảm rủi ro: viết các test Ledger đầu tiên chính là các lần dịch chuyển tiền mà Payment sẽ làm (nhận thanh toán, Refund, giao hàng).
- **Tự kiểm tra:** Vì sao "thêm ledger sau" tốn kém hơn "thêm payment sau"?
