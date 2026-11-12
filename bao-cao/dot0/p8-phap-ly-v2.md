# P8 — Pháp lý & tuân thủ — Đợt 0, bản 2 (12/11/2026)

**Trạng thái:** 🟡 xong việc giao; độ tin cậy bị giới hạn vì phiên cloud **không mở được trang gốc** (mạng phiên chặn help.shopee.vn / .sg, portal.mof.gov.vn, misaeshop.vn, bigseller.com — lỗi DNS). Chỉ dựa vào kết quả tìm kiếm.
Nhánh `phong/p8-dot0` → tạo PR: https://github.com/TKandCo/daovang/pull/new/phong/p8-dot0 (P8 không tự tạo / gộp PR).
Nghiên cứu tổng hợp, **không phải tư vấn pháp lý chính thức**.

## 1. Đã làm (việc → bằng chứng)
| Việc | Bằng chứng |
|---|---|
| Sửa theo audit: hạ "Shopee Video trừ 12 điểm + gỡ video" xuống **[THẤP]** (trang là Shopee Singapore) ở cả tóm tắt dòng 7 và mục (b)4 | `bao-cao/dot0/p8-phap-ly.md`, commit fa0abf7 |
| Bổ sung QĐ 3389/QĐ-BTC (06/10/2025): không phải mọi HKD bắt buộc tài khoản riêng; nhóm doanh thu thấp có thể không bắt buộc — nguồn mâu thuẫn → [THẤP] cho ngưỡng | như trên, dòng mới bảng mục (b)1; nguồn N5 |
| Bổ sung mẫu 01/BK-STK (TT 18/2026/TT-BTC, 05/03/2026); TT 50/2026 (13/05/2026) thay 4 mẫu khác, không thấy thay 01/BK-STK (một nguồn mâu thuẫn); hạn 20/04 → 31/07/2026 đã qua, HKD mới nộp lúc nào: CHƯA XÁC MINH | như trên; nguồn N6, N7 |
| Ghi rõ toàn bộ báo cáo là nghiên cứu, không phải tư vấn | dòng 2 `p8-phap-ly.md` |
| Checklist tuân thủ 5 giai đoạn, 36 mục, dạng danh sách (đọc trên điện thoại), có mục **affiliate / dropship Mức A** | `phap-ly/checklist-tuan-thu.md`, 26 mã nguồn N1–N26 |
| Câu hỏi gom sẵn: thuế (9), đăng ký kinh doanh cấp xã (5), luật sư (8), Shopee (5), TikTok Shop (5) | `phap-ly/cau-hoi-chuyen-gia.md` |
| Quy tắc video AI cho P2: 18 quy tắc nhóm A–G (nhãn, người thật, sự thật, bản quyền, affiliate/dropship, hồ sơ mỗi video) | `phap-ly/quy-tac-video-ai.md` |

## 2. Số liệu mới (nguồn + độ tin cậy)
- QĐ 3389/QĐ-BTC ngày 06/10/2025, hiệu lực 01/01/2026 — [luatvietnam](https://luatvietnam.vn/thue/quyet-dinh-3389-qd-btc-cua-bo-tai-chinh-phe-duyet-de-an-chuyen-doi-mo-hinh-va-phuong-phap-quan-ly-thue-doi-voi-ho-kinh-doanh-khi-xoa-bo-thue-khoan-414047-d1.html) [TB]. Ngưỡng 200 triệu cho nhóm "không bắt buộc tài khoản riêng" — [xcyber](https://xcyber.vn/tu-01-01-2026-hkd-nao-phai-mo-tai-khoan-ngan-hang-rieng/), [dhtaxlaw](https://dhtaxlaw.com.vn/tu-01-3-2026-tai-khoan-ngan-hang-ho-kinh-doanh-phai-dung-ten-dang-ky-dung-khong-hkd-nao-bat-buoc-co-tai-khoan-ngan-hang-rieng) [THẤP] (một nguồn khác nói ngược lại).
- Mẫu 01/BK-STK kèm TT 18/2026/TT-BTC (05/03/2026) — [luatvietnam biểu mẫu](https://luatvietnam.vn/bieu-mau/mau-so-01-bk-stkthong-bao-so-tai-khoan-so-hieu-vi-dien-tu-cua-ho-ca-nhan-kinh-doanh-571-107505-article.html), [Sapo](https://www.sapo.vn/blog/mau-01-bk-stk) [TB]. Hạn 31/07/2026 cho HKD ≤ 1 tỷ — [Lao Động](https://news.laodong.vn/kinh-doanh/thoi-han-ho-kinh-doanh-doanh-thu-duoi-1-ti-dong-phai-thong-bao-tai-khoan-den-co-quan-thue-1703592.ldo) [THẤP].
- TT 50/2026/TT-BTC (13/05/2026) — [luatvietnam EN](https://english.luatvietnam.vn/circular-no-50-2026-tt-btc-dated-may-13-2026-of-the-ministry-of-finance-amending-and-supplementing-a-number-of-articles-of-the-ministry-of-finances-434628-doc1.html) [TB]; phạm vi thay mẫu [THẤP] (nguồn mâu thuẫn).
- Shopee VN có nhãn "Video tạo bởi AI", người bán tự khai — [BigSeller](https://www.bigseller.com/blog/articleDetails/4730/shopee-video-la-gi.htm) [TB, blog]. Mức phạt VN: không tìm thấy → [THẤP].
- TikTok Shop VN: video / live có AI phải gắn nhãn AIGC, cấm mạo danh bằng AI — [GHN](https://ghn.vn/blogs/tip-ban-hang/chinh-sach-tiktok-shop) [THẤP, một nguồn không chính thức].

## 3. Đã kiểm gì
- **Mọi khẳng định có nguồn hoặc nhãn** (chạy script Python trên 3 tệp mới):
  - checklist: 36/36 mục có mã nguồn hoặc nhãn; 3 mục là *việc làm* (chụp trang, P8 duyệt, lưu hồ sơ) → đã ghi "việc làm, không phải khẳng định".
  - quy-tac-video-ai: 18/18 quy tắc có mã nguồn / nhãn; quy tắc 18 ghi rõ là quy tắc nội bộ P8.
  - cau-hoi-chuyen-gia: 32 câu; 29 câu kèm mã nguồn / nhãn; 3 câu là câu hỏi thuần, không chứa khẳng định.
  - Mã N1–N26: không có mã dùng mà chưa định nghĩa, không có mã định nghĩa mà không dùng.
- **Quét khóa / dữ liệu cá nhân** trên `phap-ly/` + `bao-cao/dot0/p8-*.md`: không thấy mẫu khóa API (sk-, AKIA, ghp_, AIza, khóa riêng), không có dãy số ≥ 9 chữ số ngoài link, không có email. Rà `git diff --cached` trước mỗi commit: chỉ có 4 tệp trong phạm vi được phép + báo cáo này.
- Truy vấn tìm kiếm không chứa thông tin cá nhân của chủ dự án.

## 4. Chưa kiểm gì
- **Không đọc được văn bản gốc nào** trong lượt này (QĐ 3389, TT 18, TT 50, trang Shopee VN / SG, trang hỏi đáp Bộ Tài chính) — mạng phiên chặn. Mọi nhãn [TB] là "nhiều trang tư vấn khớp", chưa phải văn bản gốc.
- Bảng phân nhóm HKD trong QĐ 3389 (ngưỡng thật); HKD đăng ký sau 31/07/2026 nộp 01/BK-STK khi nào; kỳ khai thuế quý / năm.
- Chính sách AI bản Việt Nam của Shopee và TikTok Shop (mức phạt, ngày hiệu lực).
- Affiliate: có cần HKD, có phải ghi "có hoa hồng"; dropship: phân chia trách nhiệm người bán / nhà cung cấp / sàn, thời gian chuẩn bị hàng.
- Những mục chưa kiểm từ bản 1 vẫn còn (lệ phí địa phương, mã ngành, nghị định xử phạt AI, NĐ 46/2026, điện tử, quyền giọng nói, dữ liệu cá nhân khách).
- Checklist chưa thử hiển thị trên điện thoại thật (chỉ viết dạng danh sách ngắn, không bảng rộng).

## 5. Khó khăn cần quyết định
- **Chủ dự án:** gọi chi cục thuế + bộ phận đăng ký kinh doanh theo `cau-hoi-chuyen-gia.md` mục 1–2 (miễn phí); chụp trang chính sách AI của Shopee VN / TikTok Shop VN; quyết có xin báo giá 1 buổi luật sư (mục 3) không — mọi khoản chi cần duyệt.
- **KTS / chủ dự án:** nếu muốn P8 đọc được văn bản gốc trên cloud, cần cho phép mạng thêm các trang: help.shopee.vn, banhang.shopee.vn, portal.mof.gov.vn, congbao.chinhphu.vn, vbpl.vn (đây chỉ là đề xuất; P8 không tự đổi cài đặt).

## 6. Kế hoạch tuần tới
- Cập nhật checklist khi có câu trả lời của thuế / đăng ký kinh doanh / sàn. Tiền dự kiến chi: **0**.

## 7. Đề xuất
- P2 đọc `phap-ly/quy-tac-video-ai.md` trước khi làm video đầu tiên; P8 duyệt từng video (mục F). Lợi ích: tránh gỡ video / phạt; công sức nhỏ; rủi ro: chậm đăng.

## 8. Tự chấm (KTS chấm lại độc lập)
Đúng yêu cầu 9 · Bằng chứng & nguồn 7 (không đọc được văn bản gốc) · Độ tin cậy kỹ thuật 7 · Chi phí & thời gian 9 · Rủi ro & tuân thủ 9 → **≈ 8,1**.
