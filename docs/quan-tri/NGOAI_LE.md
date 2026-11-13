# Sổ ngoại lệ — Đào Vàng (tiêu chuẩn v1.0, hạng A)

Chỉ ghi ngoại lệ ĐÃ được chủ dự án duyệt trực tiếp trong phiên Tổng quản Đào Vàng (mục 17 tiêu chuẩn).

| Mã quy tắc | Ngoại lệ | Lý do | Biện pháp thay thế | Ngày duyệt | Hạn xem lại |
|---|---|---|---|---|---|
| QT-02 | Nhánh `main` của repo riêng tư daovang KHÔNG khóa được bằng cài đặt GitHub (gói Free chỉ cho repo công khai — CP xác nhận theo tài liệu GitHub; gói thật của tài khoản chưa kiểm) | Không nâng gói GitHub Team ở Mức vốn A | (1) Quy tắc 11–13: không ai đẩy thẳng main, phòng không tạo PR, Tổng quản gom chuyến, chủ dự án tạo PR + gộp; (2) KTS hậu kiểm mỗi chuyến: `git log --first-parent origin/main` chỉ được có commit merge PR — có commit lạ thì ghi sự cố; (3) Trạm Kiểm Định báo mọi commit vào main không qua PR; (4) GitHub Actions `kiem-thu.yml` chạy ở mỗi PR | 13/11/2026 (chủ dự án) | 13/02/2027 hoặc khi có doanh thu / nâng gói |

Đề xuất đang chờ duyệt: `docs/quan-tri/NGOAI_LE_DE_XUAT.md`.
