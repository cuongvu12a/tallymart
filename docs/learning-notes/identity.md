---
status: active
owner: Cuong Vu
last_verified: 2026-11-21
applies_to: [docs, identity]
related_code: []
---

# Ghi chú học tập: Identity

Cách đọc các ghi chú này: [learning-notes/README](README.md). Phần kiểm tra JWT và role guard là phần owner tự viết ([L-13](../LEARNING_MODE.md#l-13)), nên ghi chú này giải thích vấn đề và các bẫy, không đưa code.

## Access token ngắn, refresh token xoay vòng

- [ ] Owner đã đọc
- **Loại:** kỹ thuật
- **Ở đâu:** Identity, Build-order bước 9 · rule [R-IDN-03](../domain/identity.md#r-idn-03) · đã quyết trong [Q-06](../OPEN_QUESTIONS.md#q-06) · khái niệm [L-13](../LEARNING_MODE.md#l-13)
- **Chuyện gì xảy ra:** Một user có thể có nhiều role (Buyer, Seller, Admin). Access token là JWT sống khoảng 15 phút. Refresh token lưu trong DB; mỗi lần dùng để lấy access token mới thì refresh token cũ bị vô hiệu và một refresh token mới được cấp.
- **Vì sao làm vậy:**
  - JWT không thu hồi được trước khi hết hạn, vì server không lưu nó. Để thời hạn ngắn thì một token bị lộ chỉ dùng được ít phút.
  - Refresh token nằm trong DB nên thu hồi được (đăng xuất, khoá tài khoản). Xoay vòng nghĩa là nếu kẻ trộm dùng một refresh token đã được dùng rồi, server phát hiện ra việc dùng lại và có thể khoá cả chuỗi token.
  - Quan trọng khi có Withdrawal: một token bị lộ không được phép rút tiền mãi mãi.
  - Bị loại: JWT sống nhiều ngày (không thu hồi được), và session trên server (đơn giản nhưng không luyện được JWT).
- **Có thể sai ở đâu:**
  - Chỉ kiểm tra chữ ký JWT mà quên `exp`, `iss`, `aud`.
  - Hai tab trình duyệt cùng refresh một lúc bằng cùng refresh token: tab thứ hai bị coi là "dùng lại". Cần một khoảng ân hạn nhỏ hoặc xử lý cẩn thận.
  - Đặt role trong JWT rồi đổi role của user: token cũ vẫn mang role cũ tới khi hết hạn. Đó là một lý do để access token ngắn.
- **Tự kiểm tra:**
  1. Vì sao không thu hồi được JWT, và thời hạn 15 phút giúp gì?
  2. Kẻ trộm lấy được refresh token và dùng trước user thật. Chuyện gì xảy ra khi user thật refresh?
  3. Authentication và authorization khác nhau thế nào? RBAC thuộc cái nào?
- **Đọc thêm:** "refresh token rotation reuse detection" (Auth0); RFC 7519 (JWT); "OAuth 2.0 Security Best Current Practice".
