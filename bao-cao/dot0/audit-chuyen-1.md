# Audit KTS — Chuyến 1 (12/11/2026)

Người kiểm: KTS trưởng ở phiên điều phối (cùng mô hình với Tổng quản và các phòng — không độc lập tuyệt đối; chủ dự án nên kiểm chọn mẫu).

## Nhánh trong chuyến
| Nhánh (commit) | Nội dung | KTS chạy lại | Điểm | Quyết định |
|---|---|---|---|---|
| `phong/p1-dot0` @ `3a704e7` | Sửa theo audit; Radar v1: 9 bảng mẫu, 21 nguồn, 20 nhóm ứng viên Mức A, script kiểm | Kiểm dữ liệu ĐẠT; 11/11 kiểm thử OK (xem lỗi Windows bên dưới) | ≈ 7,8 | DUYỆT |
| `phong/p4-dot0` @ `4f3509b` | Máy tính lợi nhuận mỗi đơn (đọc bảng phí theo ngày hiệu lực, giá / ROAS hòa vốn, cảnh báo) | 33/33 kiểm thử OK; kiểm ngược 3 ví dụ: 12/12 con số KHỚP | ≈ 8,8 | DUYỆT |
| `phong/p8-dot0` @ `e809469` | Sửa theo audit; checklist tuân thủ 36 mục; 32 câu hỏi chuyên gia; 18 quy tắc video AI | Không có mã; đọc báo cáo + kết quả script kiểm nguồn của phòng | ≈ 8,0 | DUYỆT |
| `phong/p9-dot0` @ `8494acd` | Schema chung, lõi (cấu hình, khóa từ biến môi trường, nhật ký che dữ liệu khách), quét khóa + pre-commit | 14 + 8 + 7 = 29 kiểm thử OK; quét toàn repo SẠCH | ≈ 8,7 | DUYỆT |
| `phong/p12-dot0` @ `af009c1` | Phản biện độc lập kế hoạch, báo cáo, audit; tự kiểm 7 dòng bảng phí | Đọc toàn văn; số học khớp | ≈ 9,0 | DUYỆT |
| `ban-thu-ky-2026-11-12` @ `baaac04` | Quyết định 12/11 (affiliate + dropship, 3 giờ/ngày, app HTML, SQLite, Actions, cổng Đợt 1 mới), trần 2 phòng xây | Quét khóa | — | DUYỆT |

Kiểm trên nhánh chuyến (sau khi gộp cả 6, không xung đột): **73 kiểm thử OK** (P1 11 · P4 33 · P9 29), kiểm ngược P4 khớp, kiểm dữ liệu P1 ĐẠT, quét khóa SẠCH.

## Lỗi phát hiện khi kiểm trên máy Windows của chủ dự án
- Kiểm thử P1 **hỏng trên Windows** khi thư mục tạm (ổ C:) khác ổ với repo (ổ D:): `ValueError: path is on mount 'C:', start on mount 'D:'` (đường dẫn tương đối giữa hai ổ). Bản đã audit: 9 lỗi; bản mới nhất: 22 lỗi.
- Khi đặt thư mục tạm cùng ổ D:, cả hai bản đều OK → logic đúng, lỗi nằm ở cách tính đường dẫn. Trên GitHub Actions (Linux) không gặp.
- Việc cho P1 (chuyến 2): sửa `kiem_tra.py` / kiểm thử để chạy được khi khác ổ; thêm một kiểm thử cho trường hợp này.

## Không đưa vào chuyến này (để chuyến 2)
- 7 commit mới của P1 sau lần audit (`0b27be0` → `54ef454`): bảng giá công cụ số liệu (Metric / FastMoss / Kalodata), lộ trình chi ≤ 100 USD, 4 nhóm chọn trước (N18 phụ kiện thú cưng, N01 hộp / khay nhựa, N02 móc treo / tôn lỗ, N05 dụng cụ vệ sinh nhà), vá script + 13 kiểm thử, biên bản "audit KTS vòng 2" làm trong phiên P1. Lý do: KTS phiên điều phối chưa audit đủ + lỗi Windows ở trên. Kiểm thử của bản này OK khi thư mục tạm cùng ổ.
- Ghi chú: báo cáo P1 ghi chủ dự án đã tạo môi trường cloud riêng `daovang` và mở mạng cho một số trang (metric.vn, banhang.shopee.vn…). Ban thư ký sẽ ghi vào sổ quyết định khi chủ dự án xác nhận.

## Việc tiếp theo (từ P12 + quyết định 12/11)
P1 + P4 viết lại theo affiliate / dropship; P9 app HTML + kiểm khớp JS ↔ Python + GitHub Actions khi PR; P8 thêm mục dữ liệu cá nhân khách trước Đợt 2; KTS kiểm mẫu ngẫu nhiên + đối chiếu chéo giữa các phòng.
