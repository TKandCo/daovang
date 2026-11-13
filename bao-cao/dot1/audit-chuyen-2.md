# Chuyến 2 — tóm tắt (Tổng quản, 13/11/2026)

KTS trưởng (mô hình Sonnet, khác mô hình phòng viết) audit 2 vòng: `audit-kts-chuyen2-vong1.md` (P1, P4, P8 duyệt; P9 trả lại) và
`audit-kts-chuyen2-vong2-p9.md` (P9 bản sửa `961775f` duyệt). Tổng quản gom theo thứ tự KTS khuyên: thư ký → P1 → P9 (đã chứa P4) → P4 → P8.

| Nhánh (commit) | Nội dung | Điểm KTS | Quyết định |
|---|---|---|---|
| `ban-thu-ky-dot1` @ `4b8d740` | Giao việc Đợt 1; quy tắc 13 (báo XONG); đa dạng mô hình (KTS Sonnet, P12 Fable); tiêu chuẩn chung v1.0 hạng A + tự chấm + đề xuất ngoại lệ | — | Duyệt |
| `phong/p1-dot1` @ `d2a129c` | Sửa lỗi Windows khác ổ; chấm affiliate / dropship; bảng nhập tay 4 nhóm | 7,85 | Duyệt |
| `phong/p4-dot1` @ `e13a831` | Công thức affiliate + dropship, sổ lãi lỗ cộng dồn, 3 kịch bản 8 tuần, 18 ví dụ kiểm khớp | 8,15 | Duyệt |
| `phong/p8-dot1` @ `841ba91` | Dữ liệu cá nhân khách, dropship / điểm phạt, affiliate, BHXH | 7,7 (sửa nhỏ) | Duyệt |
| `phong/p9-dot1` @ `961775f` | App HTML (máy tính lợi nhuận + affiliate + dropship), kiểm khớp JS ↔ Python, GitHub Actions khi PR, `.gitattributes` | 8,2 | Duyệt |

Kiểm trên nhánh chuyến (Windows thật, repo ổ D:, temp ổ C:): gộp không xung đột; `python tools/chay-kiem-thu.py` → **TẤT CẢ ĐẠT 10/10**;
157 kiểm thử OK (P1 38 · P4 60 · schema 14 · core 8 · tools + app 37); kiểm khớp JS ↔ Python 100%; quét khóa sạch.

Chưa kiểm / việc sau: GitHub Actions chạy thật (lần đầu ở PR này); app trên điện thoại thật; 3 chỗ lệch thuế giữa phòng (ngưỡng 250.000đ,
10% TNCN hay 5% + 5% từ 01/10/2026, hoàn thuế 200 triệu hay 1 tỷ) → P8 xác minh, P4 sửa; nguồn P8 N38 / N29 và P1 S06 cần sửa;
QT-02 chờ chủ dự án chọn (ngoại lệ hay nâng gói GitHub Team).
