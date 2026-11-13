# Giao việc Đợt 1 — đợt A (Tổng quản, 13/11/2026)

Căn cứ: chuyến 1 đã gộp (PR #2); quyết định 12/11 trong `ban-thu-ky/nhat-ky-quyet-dinh.md` (affiliate + dropship đo riêng, 3 giờ/ngày,
app HTML kiểu Holygrail, SQLite, GitHub Actions khi PR, cổng Đợt 1 = lãi ròng cộng dồn dự án ≥ 0); phản biện `bao-cao/dot0/p12-phan-bien.md`;
audit `bao-cao/dot0/audit-chuyen-1.md`.

Trần: tối đa **2 phòng XÂY công cụ** cùng lúc → đợt A: **P4** (công thức) + **P9** (app HTML). P1, P8 làm sửa lỗi / nghiên cứu (không xây công cụ mới).
P2 Xưởng UGC chưa mở (chờ ≥ 1 nhóm qua điểm P1). P12 phản biện ở cuối đợt A, trước chuyến 2.
Tất cả: tuân CLAUDE.md quy tắc 11–12 (nhánh `phong/<pN>-dot1`, kiểm thử XONG, đẩy nhánh, KHÔNG tạo PR); báo cáo theo `quy-trinh/mau-bao-cao-tuan.md`
có "đã kiểm gì / chưa kiểm gì"; chi tiền = 0 (mọi khoản chi chờ chủ dự án). Kiểm thử phải chạy được trên **Windows khi repo và thư mục tạm khác ổ đĩa**.

| Mã | Phòng | Việc | Đầu ra | Tiêu chí chấm |
|---|---|---|---|---|
| P4-D1A | P4 Tài chính (XÂY) | (1) Công thức **affiliate**: hoa hồng thực nhận = hoa hồng × (1 − 0,98%) × (1 − 10% khi ≥ 250.000 đ/lần) − chi phí nội dung; (2) **dropship**: thêm phí nhà cung cấp, tiền ứng trước, chu kỳ tiền về (Shopee ngày 4, TikTok 3–8 ngày), chi phí hủy đơn; (3) **sổ lãi lỗ cộng dồn dự án** (đo cổng Đợt 1: mọi phí kể cả công cụ, quảng cáo, hàng mẫu); (4) bảng 3 kịch bản xấu / vừa / tốt 8 tuần (GIẢ ĐỊNH) chỉ ra điểm hòa vốn theo số đơn (P12 mục 1.6); (5) sửa nhãn "tổng phí… chưa gồm thuế khấu trừ" (P12 2.2); (6) tệp ví dụ kiểm khớp `apps/finance/vi-du-kiem-khop.json` (đầu vào + đầu ra mong đợi) cho P9 | `apps/finance/`, `bao-cao/dot1/p4.md` | kiểm thử ĐẠT; kiểm ngược công thức bằng tính tay ≥ 5 ví dụ; mọi số GIẢ ĐỊNH ghi rõ |
| P9-D1A | P9 Nền tảng (XÂY) | (1) **App HTML một tệp** kiểu Holygrail `app/daovang.html`: chạy offline, mở trên điện thoại (khổ 412 px), không máy chủ, không gọi mạng; bản đầu = **máy tính lợi nhuận mỗi đơn** đọc bảng phí đóng gói sẵn trong tệp (sinh từ `bao-cao/dot0/bang-phi-v1.csv` bằng script); lưu nhập liệu ở trình duyệt (localStorage), KHÔNG chứa dữ liệu khách; (2) **kiểm khớp JS ↔ Python**: chạy cùng bộ ví dụ qua bản JS (node) và bản Python P4, lệch > 1 đ là HỎNG; (3) **GitHub Actions** `.github/workflows/kiem-thu.yml` chỉ chạy khi PR: mọi `unittest`, kiểm khớp, quét khóa; chỉ action chính thức, ghim phiên bản, quyền tối thiểu; (4) nút tải bản sao lưu nhập liệu | `app/`, `tools/`, `.github/workflows/`, `bao-cao/dot1/p9.md` | kiểm khớp 100% ví dụ hiện có của P4; kiểm thử ĐẠT; ảnh chụp app khổ 412 px; ước tính phút Actions / lần |
| P1-D1A | P1 Radar (sửa + nghiên cứu) | (1) Gộp 7 commit mới từ `phong/p1-dot0` (từ `0b27be0` đến `54ef454`) vào nhánh mới; (2) **sửa lỗi Windows** `ValueError: path is on mount 'C:', start on mount 'D:'` + kiểm thử cho trường hợp khác ổ; (3) chấm điểm theo **affiliate / dropship riêng** (P12 1.1–1.2); thay "phí sàn ~24%" bằng mức theo ngành, có / không voucher, lấy từ máy P4 (P12 2.1); (4) bảng nhập tay cho 4 nhóm đã chọn (N18, N01, N02, N05) để chủ dự án điền khi xem sàn | `apps/radar/`, `bao-cao/dot1/p1.md` | kiểm thử ĐẠT kể cả khác ổ; không cào sàn |
| P8-D1A | P8 Pháp lý (nghiên cứu) | (1) Mục **dữ liệu cá nhân khách** (tên, SĐT, địa chỉ trong đơn) — trước khi mở P3 (P12 2.5); (2) **dropship**: hạn chuẩn bị hàng, điểm phạt / "Sao Quả Tạ" khi hủy đơn, trách nhiệm người bán với hàng của nhà cung cấp (P12 1.3); (3) affiliate cá nhân có cần hộ kinh doanh / mã số thuế không; (4) BHXH chủ hộ (P12 2.4) — câu hỏi cho chi cục thuế / BHXH | `phap-ly/`, `bao-cao/dot1/p8.md` | mọi khẳng định có nguồn + độ tin cậy hoặc CHƯA XÁC MINH |

Sau đợt A: P12 phản biện → KTS audit → Tổng quản gom **chuyến 2** → chủ dự án tạo PR + gộp.
