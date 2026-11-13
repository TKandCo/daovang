# Ngoại lệ đề xuất — Đào Vàng (KTS, 13/11/2026)

Tất cả chỉ là ĐỀ XUẤT, trạng thái: **chờ chủ dự án duyệt**. Ghi vào `docs/quan-tri/NGOAI_LE.md` (chưa tồn tại) chỉ khi chủ dự án duyệt.

| # | Quy tắc | Nội dung đề xuất | Lý do | Điều kiện / hạn xem lại |
|---|---|---|---|---|
| 1 | QT-02 | CHỈ nếu GitHub gói hiện tại không cho bảo vệ nhánh ở repo riêng tư: tạm dùng quy tắc giấy 11–12 + KTS quét hậu kiểm mỗi chuyến (`git log --first-parent origin/main` không có commit nào không phải merge PR) | Công cụ chặn không có; vẫn muốn có đường kiểm | Chủ dự án kiểm gói trước (chưa kiểm). Hạn 13/12/2026, hoặc nâng gói / đổi chỗ để có bảo vệ thật |
| 2 | QT-03 | Chấp nhận KTS (Sonnet) + P12 (Fable) là "phiên khác viết" dù cùng hãng AI; lớp độc lập thật là kiểm thử tự động + chủ dự án kiểm chọn mẫu | Hiện không có người / hãng khác; đã ghi trong CLAUDE.md mục "Đa dạng mô hình" | Xem lại sau 2 chuyến (đã hẹn 13/11) |
| 3 | BM-01 | Dùng `tools/quet-khoa.py` (tự viết, chỉ thư viện chuẩn) thay gitleaks tạm thời, thêm quét lịch sử hằng tuần bằng chính nó | Chạy được trên Windows không cần cài; gitleaks chưa có trên máy | Hạn: trước khi có khóa hoặc dữ liệu thật đầu tiên — khi đó phải thêm gitleaks |
| 4 | FE-01 | App một tệp giữ `script-src 'unsafe-inline'`; ghi rõ giới hạn trong README app (hoặc chuyển sang CSP theo hash) | App cố ý là MỘT tệp tự chạy offline | Xem lại khi app có dữ liệu khách hoặc đăng nhập |
| 5 | QT-06 | Một chuyến tàu = một bản phát hành (số phiên bản + CHANGELOG theo chuyến, không theo từng nhánh phòng) | Phòng không được tăng phiên bản (quy tắc 12); PR chỉ do chuyến | Xem lại cuối Đợt 1 |
| 6 | SL-02 / SL-03 / SL-05 | Chưa bắt buộc sao lưu tự động + khôi phục thử hằng tháng cho tới khi có dữ liệu thật; lúc đó là bắt buộc từ ngày đầu | Chưa có dữ liệu ngoài mã (mã đã ở git + GitHub) | Hết hạn tự động khi có SQLite / đơn hàng thật đầu tiên |
| 7 | KT-02 | Chưa đo độ phủ phần tiền; thay bằng kiểm khớp JS↔Python (5.012 ví dụ) + kiểm ngược | Chưa có công cụ đo độ phủ | Hạn 13/12/2026 |
| 8 | PT-03 (mục 17 của tiêu chuẩn) | KHÔNG cần ngoại lệ: `kiem-thu.yml` của `p9-dot1` đã ghim action theo SHA (đúng hạng A). Chỉ cần xác minh SHA khớp tag | — | — |

Ghi chú: các quy tắc KAD (không áp dụng) không cần ngoại lệ vì chưa có thành phần liên quan; chúng chuyển thành bắt buộc khi thành phần xuất hiện.
