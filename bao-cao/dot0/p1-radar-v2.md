# P1 — Radar v2 (sửa theo audit + Radar v1 thủ công + 20 nhóm ứng viên)
Ngày: 12/11/2026 · Người lập: Trưởng phòng P1 (phiên cloud) · Nhánh: `phong/p1-dot0`

**Trạng thái:** 🟡 đã sửa xong 8 việc audit KTS vòng 2 (mục 10); nhánh sẵn sàng cho KTS chấm lại · đang chờ: chủ dự án tạo PR + đối chiếu số trên Seller Center / Metric · rủi ro: mọi số thị trường chỉ đọc qua trích đoạn tìm kiếm (mạng phiên cloud chặn trang gốc).

Cập nhật 12/11/2026: chủ dự án đồng ý chọn 4 nhóm N18, N01, N02, N05; giá công cụ + kết luận họp KTS ở `p1-cong-cu-so-lieu.md`; nguồn S22–S26 đã thêm. Tổng quản sẽ gộp chuyến tạo PR.

Link tạo PR: https://github.com/TKandCo/daovang/pull/new/phong/p1-dot0

---

## 1. Đã làm
| Việc | Bằng chứng |
|---|---|
| Sửa theo audit: hoa hồng TikTok theo ngành (14,6→16,1%; 14,5→17,8%) hạ xuống **[THẤP]**, ghi rõ không dùng để chấm điểm; dùng bảng phí P4 | `bao-cao/dot0/p1-radar.md` mục 5 "Bối cảnh phí" |
| Đính chính miễn phí cố định Shopee: người bán có sản phẩm đầu tiên đăng từ 01/11/2026 được miễn **phí cố định** 30 ngày, tối đa 200 đơn; không miễn 6% giao dịch + 3.000đ hạ tầng [CAO theo P4, bài https://banhang.shopee.vn/edu/article/2139] | cùng mục; khớp dòng `uu_dai_nguoi_ban_moi` trong `bang-phi-v1.csv` |
| Sửa thêm một chỗ sai tự phát hiện: bản cũ ghi Shopee 6% "từ 08/05/2026, trước đó 4,9%"; bảng phí P4 (nguồn chính thức bài 2150) ghi 01/05/2026 cho người bán thường, 08/05 cho Mall | cùng mục |
| Radar v1: 9 bảng mẫu theo kiến trúc mục 6 (product, supplier, supplier_quote, listing_price, trend_signal, source, score, trial_batch, affiliate_item), mỗi bảng có `source_id` + `captured_at` | `apps/radar/mau/*.csv` |
| Hướng dẫn tiếng Việt: cách điền, thang 100, công thức biên, cách trỏ phí sang `bang-phi-v1.csv` qua `fee_ref` | `apps/radar/README.md` |
| 27 nguồn có link (hoặc đường dẫn tệp trong repo cho nguồn nội bộ), ngày, độ tin cậy | `apps/radar/du-lieu/source.csv` |
| 20 nhóm ứng viên Mức A, điểm sơ bộ | `apps/radar/du-lieu/nhom-ung-vien.csv` (mục 2 dưới) |
| Script kiểm + 11 kiểm thử | `apps/radar/kiem_tra.py`, `apps/radar/test_kiem_tra.py` → **ĐẠT / OK** (mục 4) |

Không cào sàn, không tạo tài khoản, không chi tiền. Không bảng nào chứa dữ liệu khách / tài khoản / khóa.

## 2. 20 nhóm ứng viên (sắp theo điểm sơ bộ)
Cách chọn: giá vốn thường thấp, hợp affiliate / dropship, **loại** mỹ phẩm, TPCN / thực phẩm (cả thức ăn thú cưng), đồ chơi trẻ em, điện tử có pin / sạc, chất tẩy rửa
(theo `p8-phap-ly.md` mục 3 và tóm tắt dòng 10), và Mẹ & Bé (Shopee Affiliate không tính hoa hồng ngành này — S18 [CAO]).
"Giá vốn thấp" là nhận định chung; **giá vốn từng nhóm CHƯA ĐO** (chưa có báo giá nào).

Điểm sơ bộ = Nhu cầu (≤ 10 ở cấp nhóm) + Pháp lý (≤ 15) + Video (≤ 10) → **tối đa 45**. Cạnh tranh, Biên sau phí, Hoàn trả, Mùa vụ (55 điểm) = **CHƯA ĐO**.
Cách chấm từng phần: `apps/radar/README.md` mục "Điểm sơ bộ cấp NHÓM".

| # | Nhóm | Tín hiệu (nguồn) | Tin cậy | Điểm /45 |
|---|---|---|---|---|
| N14 | Trang phục Tết (áo dài cách tân) — ưu tiên affiliate | thời trang lớn (S02, S05); ~2 triệu đơn áo dài TikTok 01/2026 (S01, S27) | THẤP | 28 |
| N18 | Phụ kiện thú cưng (không thức ăn / thuốc) | thú cưng Q3/2026 ~1.921,5 tỷ (báo khác ghi tròn 1.912), +38,2% (S06, S08, S09); phụ kiện 481,1 tỷ (S07) | TB | 28 |
| N01 | Hộp / khay / thùng nhựa sắp xếp (không đựng thực phẩm) | NC-ĐS Q1 +32,17% (S03); TikTok NC-ĐS +94% năm 2025 (S10); eReport cũ (S11) | THẤP | 26 |
| N02 | Móc treo, kệ dán, tấm tôn lỗ | NC-ĐS; eReport > 1 tỷ, +12,55% so quý trước (S12) | THẤP | 26 |
| N03 | Giá treo chậu cây, phụ kiện ban công | NC-ĐS; eReport chỉ tiêu đề (S13) | CHƯA XÁC MINH | 24 |
| N05 | Dụng cụ vệ sinh nhà (không hóa chất) | chỉ cấp ngành NC-ĐS | THẤP | 24 |
| N04 | Dụng cụ bếp không điện | NC-ĐS; blog không ngày (S15); pháp lý tiếp xúc thực phẩm CHƯA XÁC MINH | THẤP | 22 |
| N06 | Đồ phòng tắm không điện | cấp ngành NC-ĐS | THẤP | 22 |
| N07 | Vải trang trí nhà | cấp ngành NC-ĐS | THẤP | 22 |
| N10 | Túi vải / túi ví không thương hiệu | phụ kiện thời trang +56,95% H1 (S04); một thương hiệu +~200% (S17) | THẤP | 22 |
| N11 | Balo phổ thông | eReport số 12/2024–11/2025 (S14); S04 | THẤP | 22 |
| N13 | Đồ mặc nhà, áo thun cơ bản | thời trang lớn (S02, S05) | THẤP | 22 |
| N19 | Đồ vệ sinh thú cưng không hóa chất | ngành thú cưng (S06, S08) | TB | 22 |
| N08 | Phụ kiện tóc, thắt lưng | phụ kiện thời trang +56,95% (S04, 1 nguồn) | THẤP | 20 |
| N09 | Trang sức thời trang | S04 | THẤP | 20 |
| N12 | Tất / vớ | thời trang lớn (S02, S05) | THẤP | 20 |
| N15 | Văn phòng phẩm | VPP +41,44% H1, sản lượng −10,02% (S04, 1 nguồn) | THẤP | 20 |
| N16 | Phụ kiện bàn làm việc không điện | S04 | THẤP | 20 |
| N20 | Dụng cụ tập tại nhà | KHÔNG tìm được số 2026 | CHƯA XÁC MINH | 16 |
| N17 | Phụ kiện điện thoại không pin / sạc | chỉ định tính (S16); rủi ro sở hữu trí tuệ | THẤP | 14 |

Đọc bảng: điểm chênh nhau ít và phần lớn dựa số cấp NGÀNH → mới đủ để chọn **nhóm nào đi tìm sản phẩm trước** (gợi ý N18, N01, N02, N05; N14 chỉ affiliate vì mùa Tết),
chưa đủ để quyết nhập. Không phải khuyến nghị đầu tư / không đảm bảo lợi nhuận.

Bối cảnh chung (không chấm điểm): Q3/2026 4 sàn ~150.400 tỷ, +45,16% (S08); nhiều nhóm "doanh số tăng, sản lượng giảm" (S04, S06) → giá bán bình quân tăng, nhóm giá rẻ có thể bị ép;
số shop thú cưng giảm 9% (S08). Mức độ tin cậy như cột trên.

## 3. Số liệu dùng (nguồn + ngày + độ tin cậy)
Toàn bộ ở `apps/radar/du-lieu/source.csv` (27 dòng, ngày tra 12/11/2026). Lưu ý quan trọng:
- **Cập nhật sau khi mở mạng (môi trường `daovang`, chủ dự án duyệt 12/11/2026):** đọc được trang gốc S03 (Metric Q1/2026 — khớp, nâng [CAO]) và trang giá Metric S22–S23. Các số còn lại vẫn chỉ qua trích đoạn tìm kiếm: brandsvietnam.com và kalodata chặn truy cập tự động; eReport Metric và bài Shopee 2139 không hiện số khi không đăng nhập / không chạy JavaScript.
- **Trước khi mở mạng:** tất cả con số thị trường đọc qua trích đoạn của công cụ tìm kiếm, KHÔNG mở được trang gốc: mạng phiên cloud chặn metric.vn, brandsvietnam.com, vietnam.vn,
  banhang.shopee.vn (thử 12/11/2026: lỗi DNS / proxy 403). Vì vậy số có nhiều báo cùng dẫn → [TB]; một báo → [THẤP].
- Gốc của hầu hết số là **Metric** (số ước tính từ dữ liệu công khai của sàn, theo chính Metric) — "nhiều báo khớp" thực chất là nhiều báo chép cùng một nguồn.
- Các eReport Metric (S11–S14) tiêu đề ghi "cập nhật 10/2026" nhưng kỳ số liệu có khi chỉ đến 03/2025 hoặc 11/2025.
- Hai số thú cưng bị báo ghi lệch: 1.921,5 tỷ và 1.912,5 tỷ — dùng 1.921,5 theo đa số trích đoạn, [TB].

## 4. Đã kiểm gì / chưa kiểm gì
**Đã kiểm (chạy được, lặp lại được):**
```bash
python3 apps/radar/kiem_tra.py
```
→ `ĐẠT — 11 tệp CSV đúng cột, không ô nguồn trống`
```bash
python3 -m unittest apps/radar/test_kiem_tra.py
```
→ `Ran 11 tests … OK`. Kiểm thử cố tình làm hỏng dữ liệu và xác nhận script bắt được: sai cột, ô `source_id` trống, ngày trống, mã nguồn không tồn tại,
điểm vượt tối đa, tổng sai, `fee_ref` không có trong bảng phí, lô thử > 300 USD và chưa có chủ dự án duyệt.
- Mọi `fee_ref` của 20 nhóm trỏ đúng dòng có thật trong `bang-phi-v1.csv` (script kiểm).
- Đính chính miễn phí cố định đối chiếu với `p4-tai-chinh.md` dòng 56 và `bang-phi-v1.csv` dòng 42 — khớp.
- Quét khóa trên phần thay đổi trước khi đẩy (mục 9).

**Chưa kiểm:**
- Chỉ mở được trang gốc S03, S22, S23 (sau khi mở mạng); các số khác ở mục 2 chưa đối chiếu với trang gốc. KTS / chủ dự án nên mở 3–4 link (gợi ý S04, S06, S12) để kiểm mẫu.
- Chưa có giá vốn, giá bán đối thủ, mức cạnh tranh, tỷ lệ hoàn, mùa vụ của nhóm nào → 55/100 điểm CHƯA ĐO.
- Chưa kiểm ngược (backtest) thang điểm vì chưa có lô thử / số bán thật nào — thang 100 vẫn là giả định khởi điểm.
- Pháp lý từng nhóm chỉ dựa báo cáo P8; chưa hỏi P8 riêng về: dụng cụ tiếp xúc thực phẩm (N04, cả N01 nếu bán hộp đựng đồ ăn), ốp lưng in hình (N17).
- Ngành cấp 3 của VPP / phụ kiện bàn / thể thao trên hai sàn chưa tra (đã ghi trong cột ghi chú) → `fee_ref` của N15, N16, N20 là tạm.
- Script chỉ kiểm định dạng / tính nhất quán, KHÔNG kiểm nội dung số có đúng với nguồn hay không.

## 5. Khó khăn cần quyết định
| Việc | Ai quyết |
|---|---|
| Chọn 3–5 nhóm để bắt đầu tìm sản phẩm + báo giá (gợi ý N18, N01, N02, N05) | Chủ dự án |
| Có mua công cụ số liệu (Metric / Kalodata) để đo cạnh tranh và doanh số cấp sản phẩm không — giá vẫn CHƯA XÁC MINH | Chủ dự án (tiền thật) |
| ~~Mở mạng phiên cloud~~ — ĐÃ XONG 12/11/2026 (môi trường `daovang`) | Chủ dự án |
| N14 áo dài Tết: chỉ affiliate hay bỏ (rủi ro mùa vụ) | Chủ dự án |

## 6. Kế hoạch tiếp theo + tiền dự kiến chi
- Với 3–5 nhóm được chọn: ghi tay 5–10 sản phẩm mỗi nhóm vào `product` / `listing_price` (xem trên sàn, không cào), xin 2–3 báo giá dropship → chấm đủ 100 điểm.
- Tiền dự kiến chi: **0 đ** cho tới khi chủ dự án duyệt công cụ / hàng mẫu.

## 7. Đề xuất
- Gộp `nhom-ung-vien` vào `packages/schema` sau khi P9 có lược đồ chung (bảng `product`, `supplier`, `score` ở đây đã đặt tên cột theo mục 6 báo cáo cũ). Lợi ích: ráp với P4. Công sức nhỏ. Rủi ro: đổi tên cột → script kiểm sẽ báo ngay.

## 8. Tự chấm (KTS chấm lại độc lập)
| Tiêu chí | Tự chấm |
|---|---|
| Đúng yêu cầu (25%) | 8,5 |
| Bằng chứng & nguồn (25%) | 6,5 (đã đối chiếu lại các số KTS hỏi; phần lớn vẫn chỉ qua trích đoạn) |
| Độ tin cậy kỹ thuật (20%) | 7,5 (script + 21 kiểm thử đạt; vẫn chỉ kiểm định dạng, không kiểm nội dung) |
| Chi phí & thời gian (15%) | 9 (0 đ) |
| Rủi ro & tuân thủ (15%) | 8,5 |
| **Tổng** | **≈ 7,9** (vòng 1 tự chấm 7,9; KTS chấm vòng 2 ≈ 7,6 — xem `p1-bien-ban-audit-kts-v2.md`) |

## 9. Quét khóa trước khi đẩy
`git diff` của nhánh so với `origin/main` được quét các mẫu khóa / mật khẩu / token (`api_key`, `secret`, `password`, `token`, `sk-`, `AKIA`, `-----BEGIN`): chỉ trúng 3 dòng chữ hướng dẫn (README: "Không ghi mật khẩu, khóa API…", mô tả cột `supplier`, và chính mục này) — không có khóa / mật khẩu thật.

## 10. Đối chiếu audit KTS vòng 2 (12/11/2026) — đã sửa
Biên bản KTS chép nguyên văn: `bao-cao/dot0/p1-bien-ban-audit-kts-v2.md` (KTS chấm ≈ 7,6, cần sửa nhỏ).

| # | KTS yêu cầu | P1 đã làm |
|---|---|---|
| 1 | Số thú cưng 1.921,5 hay 1.912,5; số shop −9% | Tra lại: 1.921,5 tỷ +38,2% được nhiều báo ghi, một số báo ghi tròn 1.912 tỷ "hơn 38%" → ghi cả hai (S06, N18). Số shop thú cưng −9% còn 20.700 chỉ có 1 nguồn → ghi [THẤP] (S08, ghi chú N18). Số −10,68% KTS thấy là số gian hàng TOÀN thị trường, khác chỉ số |
| 2 | "~2 triệu đơn áo dài" không tìm thấy | Tra lại: nhiều báo cùng ghi (MotTheGioi, Giao Thương – Công Thương, CafeBiz) → thêm S27, **giữ** +4 điểm N14 |
| 3 | S25 FastMoss hạ [THẤP], URL | Đã hạ [THẤP]; S25 = blog FastMoss so sánh EchoTik, S26 = blog FastMoss về giá Kalodata (hai URL khác nhau) |
| 4 | S03 URL; S19–S21 trỏ nhánh tạm | S03 đã đọc trang gốc metric.vn, khớp → nâng [CAO], giữ URL. S19–S21 đổi sang đường dẫn tệp trong repo (script kiểm tệp có thật) |
| 5 | Vá 7 lỗ hổng script + kiểm danh sách type / export_method, độ tin cậy nhóm | Đã vá cả 7 lỗ hổng + 3 kiểm thêm; 21 kiểm thử (thêm 10) → OK. Áp quy tắc "độ tin cậy nhóm ≤ nguồn yếu nhất": 7 nhóm hạ từ [TB] xuống [THẤP] (N01, N05, N06, N07, N12, N13, N14), N03 hạ xuống CHƯA XÁC MINH; hiện 16 nhóm [THẤP], 2 CHƯA XÁC MINH (N03, N20), chỉ N18 và N19 còn [TB] |
| 6 | Báo cáo: "21 dòng", mâu thuẫn về mạng | Sửa thành 27; mục 3 tách rõ trước / sau khi mở mạng và nguồn nào đọc được trang gốc |
| 7 | `p1-radar.md` dòng 5 lỗi thời | Đã sửa, trỏ sang `p1-cong-cu-so-lieu.md` |
| 8 | Giá FastMoss [THẤP]; "KTS chưa tự mở trang giá Metric" | Đã ghi trong `p1-cong-cu-so-lieu.md` |

Vẫn chưa làm được: KTS độc lập mở trang giá Metric (chủ dự án nên tự mở 1 lần); điều khoản dùng dữ liệu của các công cụ.
Sau khi sửa: `python3 apps/radar/kiem_tra.py` → ĐẠT; `python3 -m unittest apps/radar/test_kiem_tra.py` → 21 kiểm thử OK.
