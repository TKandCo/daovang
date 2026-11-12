# P4 — Tài chính, thuế, lợi nhuận từng SKU — Đợt 0 (12/11/2026)

Nhãn tin cậy: **[CAO]** = trang chính thức của sàn / cổng Chính phủ, đọc trực tiếp; **[TB]** = nhiều nguồn thứ cấp khớp; **[THẤP]** = mâu thuẫn hoặc chỉ qua kết quả tìm kiếm, chưa đọc toàn văn.
Tệp bảng phí: `...\scratchpad\hst\bao-cao\dot0\bang-phi-v1.csv` (79 dòng, UTF-8 có BOM, nội dung không dấu để tránh lỗi mã hóa).
Mọi số trong tệp này đều **đọc ngày 12/11/2026**; phí sàn đổi 2–3 lần/năm nên cần kiểm lại trước khi niêm yết giá.

## 1. Tóm tắt 10 dòng
1. Shopee (shop thường, không Mall), hiệu lực 23/05/2026 [CAO]: phí cố định theo ngành **13,5–16,5% thời trang, 17% sắc đẹp, 15,5–17% sức khỏe, 11–16% tiêu dùng, 13–16% nhà cửa còn lại, điện tử 2–15%** (đã gồm GTGT 8%), tăng 1–3 điểm so với trước.
2. Shopee **phí xử lý giao dịch 6%** từ 01/05/2026 (đổi tên từ "phí thanh toán" 24/04/2026), mọi phương thức kể cả COD; **phí hạ tầng 3.000đ/đơn**; Voucher Xtra **5,5%** (tối đa 50.000đ/sp, trước 4%) từ 23/05/2026; PiShip 2.700đ/đơn (trước 1.620).
3. Tổng phí sàn điển hình của shop thời trang Shopee ≈ **21% giá bán + 3.000đ/đơn** (trước hoa hồng affiliate, quảng cáo, ship).
4. TikTok Shop (shop thường) [CAO]: hoa hồng mặc định **14%** từ 03/07/2026 (khoảng 9–16% tùy ngành; blog nói 12,5% là số cũ), **phí giao dịch 6%** từ 09/05/2026 (trước 5%), **phí xử lý đơn 3.000đ** từ 27/10/2025 (không hoàn khi đã giao), VXP 5%. Tổng ≈ 20–21% + 3.000đ.
5. Thuế: sàn **khấu trừ thay từ 01/07/2025** (NĐ 117/2025) — hàng hóa **GTGT 1% + TNCN 0,5% = 1,5% doanh thu** mỗi đơn, bất kể tổng doanh thu năm [CAO].
6. Ngưỡng miễn thuế GTGT + TNCN năm 2026 = **1 tỷ đồng/năm** theo **NĐ 141/2026/NĐ-CP** (ký 29/04/2026, hiệu lực 01/01/2026, sửa NĐ 68/2026) [CAO về ngưỡng; xem mục 2]. Các số 100/200/500 triệu là bản cũ hoặc văn bản bị sửa.
7. Doanh thu ≤ 1 tỷ: không nộp thuế nhưng **vẫn bị sàn khấu trừ rồi phải làm thủ tục hoàn thuế cuối năm**, nộp thông báo doanh thu mẫu 01/TKN-CNKD trước 31/01 năm sau. Vốn bị "treo" 1,5% doanh thu cả năm.
8. Doanh thu > 1 tỷ: khai theo quý, **bắt buộc hóa đơn điện tử có mã**; TNCN chọn theo tỷ lệ doanh thu (0,5% bán hàng, trên phần vượt ngưỡng) hoặc theo lợi nhuận (15% cho tới 3 tỷ, 17% đến 50 tỷ, 20% trên); > 3 tỷ bắt buộc theo lợi nhuận.
9. Tiền về: Shopee ghi nhận doanh thu ngày thứ 4 sau giao thành công (tối đa 15 ngày nếu nghi gian lận), rút tay bất kỳ lúc nào (về TK ≤ 24 giờ, đôi khi 3–4 ngày làm việc); TikTok shop mới **8 ngày**, shop đã qua giai đoạn điều chỉnh **3 ngày**.
10. Hoàn/hủy là khoản lỗ lớn nhất ở hàng giá thấp: hàng "Trả hàng & Hoàn tiền" sàn không tính phí nhưng shop chịu ship trả tối đa 40.000đ/đơn (lỗi shop / đổi ý). Tỷ lệ hoàn điển hình: **CHƯA XÁC MINH** (không có số liệu nguồn tin cậy) — phải đo bằng dữ liệu shop.

## 2. Tham số thuế đã xác minh

| Tham số | Giá trị | Nguồn / ngày | Tin cậy |
|---|---|---|---|
| Sàn khấu trừ, kê khai, nộp thay thuế cho hộ / cá nhân kinh doanh | Từ 01/07/2025; sàn có chức năng thanh toán; công ty TNHH/CP không thuộc đối tượng khấu trừ | Shopee Uni bài 24233; TikTok Seller University "Withholding Taxes…" (NĐ 117/2025/NĐ-CP, Luật 56/2024/QH15) | CAO |
| Thuế suất khấu trừ, hàng hóa, cá nhân cư trú | GTGT 1% + TNCN 0,5%, tính trên (giá hàng − giảm giá của shop − phần đồng tài trợ của shop), không gồm phí ship. Dịch vụ: 5% + 2%. Cá nhân không cư trú: 1% + 1% | Shopee Uni 24233, 24204 | CAO |
| Hoàn hàng | Sàn trừ thuế tương ứng vào kỳ sau | Shopee Uni 24233 | CAO |
| Ngưỡng không chịu thuế GTGT + không nộp TNCN, 2026 | **1 tỷ đồng/năm**, hiệu lực 01/01/2026 | NĐ 141/2026/NĐ-CP (ký 29/04/2026, Phó Thủ tướng) — toàn văn đăng cổng xaydungchinhsach.chinhphu.vn; MISA, einvoice.vn, thuvienphapluat đều khớp | CAO (ngưỡng) / TB (ngày ký, hiệu lực hồi tố) |
| Căn cứ trước đó | Luật Thuế TNCN 109/2025/QH15 Điều 7: ngưỡng 500 triệu "Chính phủ trình UBTVQH điều chỉnh"; NĐ 68/2026/NĐ-CP (ban hành 05/03/2026) dùng 500 triệu, bị NĐ 141 sửa lên 1 tỷ | xaydungchinhsach.chinhphu.vn (bài Điều 7); MISA | CAO / TB |
| Thông báo doanh thu (hộ ≤ 1 tỷ) | Mẫu 01/TKN-CNKD (TT 18/2026/TT-BTC), 1 lần/năm, chậm nhất 31/01 năm sau; hộ mới: nửa đầu năm hạn 31/07 | einvoice.vn, easyinvoice.vn | TB |
| Hóa đơn điện tử | > 1 tỷ: bắt buộc HĐĐT có mã của cơ quan thuế (hoặc máy tính tiền nối thuế), đăng ký trong 30 ngày sau kỳ vượt; ≤ 1 tỷ: tự nguyện | NĐ 141/2026 (nội dung điều 8 khoản 5 NĐ 68 sửa đổi) — cổng Chính phủ | CAO |
| Cách tính khi > 1 tỷ — GTGT | Doanh thu × tỷ lệ theo ngành (phân phối, cung cấp hàng hóa **1%**; sản xuất / vận tải 2%; dịch vụ 5%) | Shopee (1%); einvoice.vn; **chưa đối chiếu điều khoản gốc về việc tính trên toàn bộ hay phần vượt ngưỡng** | TB |
| Cách tính khi > 1 tỷ — TNCN | Doanh thu 1–3 tỷ chọn: (a) (DT − ngưỡng) × tỷ lệ ngành (**0,5% phân phối hàng hóa**), hoặc (b) (DT − chi phí) × **15%**; 3–50 tỷ: (DT − chi phí) × **17%**; > 50 tỷ: × **20%**; > 3 tỷ bắt buộc theo lợi nhuận; phương pháp chọn giữ ổn định 2 năm | Luật TNCN 109/2025 Điều 7 (chinhphu.vn, các mức 15/17/20 và 0,5%) + luatvietnam.vn (phương pháp giữ 2 năm); nhiều blog ghi 17% cho nhóm 1–3 tỷ → mâu thuẫn, ưu tiên bản Chính phủ | CAO (mức Luật) / TB (áp vào ngưỡng 1 tỷ) |
| Khai thuế | > 1 tỷ: theo quý (khai tháng khi > 50 tỷ); quyết toán TNCN theo năm trước 31/03 năm sau | luatvietnam.vn (NĐ 68) | TB |
| Sổ kế toán | TT 152/2025/TT-BTC hiệu lực 01/01/2026: S1a-HKD (nhóm không chịu thuế), S2a-HKD (nộp theo tỷ lệ % doanh thu), S2b–S2e-HKD (TNCN theo lợi nhuận, 4 sổ), S3a-HKD (thuế khác); lưu ≥ 5 năm. **Mốc phân nhóm trong thông tư là 500 triệu — chưa thấy văn bản cập nhật lên 1 tỷ** | sapo.vn, thuvienphapluat (qua tìm kiếm) | TB |
| Thuế trên phí sàn | Shopee: GTGT **8%** đến 23h59 31/12/2026 (NQ 204/2025/QH15); từ 01/01/2027 chưa có thông báo. TikTok: nêu GTGT 10% + TNDN nhà thầu 5% trên dịch vụ nhà cung cấp nước ngoài; phí đã gồm thuế | Shopee Uni 25329; TikTok SU "Basic Tax Information…" (cập nhật 30/09/2026) | CAO |
| Chuyển lên công ty | Không có mốc doanh thu / lao động bắt buộc chung (mốc 10 lao động cũ của NĐ 78/2015 đã hết hiệu lực); chỉ bắt buộc khi ngành có điều kiện đòi pháp nhân. Thủ tục: NĐ 168/2025 Điều 27; phải hoàn tất nghĩa vụ thuế hoặc cam kết kế thừa | sapo.vn, ketoanthuanthien.vn (qua tìm kiếm, chưa đọc toàn văn) | THẤP–TB |

**Ghi chú quyết định ngưỡng:** Shopee Uni (bài 24204) vẫn ghi "100 triệu năm 2025, 200 triệu từ 2026" — đã cũ. Luật TNCN: 500 triệu. NĐ 141/2026: **1 tỷ**. Văn bản mới nhất theo ngày ký (29/04/2026) là NĐ 141 → dùng **1 tỷ**, nhưng nên có kế toán / chi cục thuế xác nhận bằng văn bản vì chưa đọc được bản PDF gốc.

## 3. Phí nền tảng (tóm tắt; chi tiết 79 dòng trong CSV)

**Shopee, shop thường (không Mall) — hiệu lực 23/05/2026 [CAO] (Shopee Uni bài 27540, đã gồm GTGT 8%)**

| Ngành | Phí cố định | Trước 23/05 |
|---|---|---|
| Thời trang | 13,5–16,5% | 12,5–13,5% |
| Sắc đẹp | 17% | 14% |
| Sức khỏe | 15,5–17% | 12,5–14% |
| Tiêu dùng còn lại (gồm Mẹ & Bé không liệt kê) — *giả định* | 11–16% | 10–13% |
| Mẹ & Bé: da bé, tắm gội bé | 10,5% | 11,5% |
| Thực phẩm & đồ uống (nhóm liệt kê) | 10% | 10–11% |
| Nhà cửa & đời sống còn lại | 13–16% | 10–13% |
| Dụng cụ chăm sóc nhà | 10–10,5% | 11–11,5% |
| Điện tử | 2% (điện thoại, laptop) … 8,5–15% (còn lại) | 2% … 7,5–11% |

Các khoản khác (đã gồm GTGT): **phí xử lý giao dịch 6%** (từ 01/05/2026) trên (giá SP + ship khách trả − KM shop − KM ngân hàng); **phí hạ tầng 3.000đ/đơn**; **Voucher Xtra 5,5%, tối đa 50.000đ/sp** (nếu tham gia; không dùng chung với đồng tài trợ mã); **đồng tài trợ mã: shop 40% / Shopee 60%** (từ 23/05/2026); PiShip 2.700đ/đơn; phí rút tiền 10.800đ (miễn lần 1 mỗi tháng). Freeship Xtra dành cho người bán: **CHƯA XÁC MINH** (blog ghi 7,85%, bài phí dịch vụ chính thức không liệt kê). Hoa hồng affiliate: shop tự đặt, trừ vào doanh thu đơn.
**Người bán mới (đang áp dụng với bạn):** miễn phí cố định 30 ngày, tối đa 200 đơn thành công, nếu sản phẩm đầu tiên đăng từ 01/11/2026 [CAO, bài 2139]. Chỉ miễn *phí cố định* — vẫn phải trả 6% xử lý giao dịch + 3.000đ hạ tầng. Ưu đãi giảm 3 điểm % / 50% (01/06–31/08/2026) đã hết hạn.

**TikTok Shop, shop thường — [CAO]**
- Hoa hồng nền tảng theo ngành cấp 3, cột Marketplace hiệu lực **03/07/2026** (PDF chính thức, tôi gộp 2.041 dòng): mặc định 14%; thời trang nữ 14–15%, nam 13–15%, giày 14–15%, phụ kiện 13–15,5%; sắc đẹp 9,5–16% (trung vị 15,5%); sức khỏe 14–15,5%; mẹ & bé 9–15%; nhà cửa 8,5–15%; điện tử 2–14%; thực phẩm 8,5–13,5%.
- Phí giao dịch **6%** (đơn tạo sau 00:00 ngày 09/05/2026; trước đó 5%) × (khách trả + trợ giá sàn − hoàn tiền khách). Từ 21/10/2026 có giảm 0–1,5 điểm % theo "ads take rate" 30 ngày (chỉ khi chạy quảng cáo).
- Phí xử lý đơn **3.000đ** mỗi đơn giao thành công (từ 27/10/2025), không hoàn nếu sau đó khách hoàn.
- VXP **5%** (tối đa 50.000đ/sp), VXP+ cộng 1,5–4 điểm %. Hoa hồng nhà sáng tạo: shop tự đặt (Shop Ads 1–80%).
- Ưu đãi shop mới 50% hoa hồng (tối đa 3 điểm) áp dụng đến 30/09/2026 cho shop mở 01/01–26/06/2026: **đã hết hạn**, ưu đãi mới sau 10/2026 CHƯA XÁC MINH.

## 4. Đối soát, tiền về, hoàn / trả
- **Shopee [CAO]:** doanh thu vào Số dư TK Shopee ngay khi khách bấm "Đã nhận hàng", hoặc **ngày thứ 4** sau giao thành công nếu không có yêu cầu trả hàng, hoặc sau khi xử lý xong trả hàng; đơn nghi gian lận tới 15 ngày. Sau khi hoàn thành khách vẫn có thể xin hoàn, Shopee cấn trừ số dư. Rút: tự động 2 lần/tháng hoặc ngày 15, hoặc rút tay (trước 17h trong ngày); về ngân hàng trong 24 giờ, đặc biệt 3–4 ngày làm việc.
- **TikTok [CAO]:** đơn giao xong → chờ 8 ngày (shop mới), 3 ngày (shop đã qua giai đoạn điều chỉnh shop mới), 1 ngày (Mall đủ điều kiện), 15 ngày (bị đánh giá rủi ro), tối đa 30 ngày; rút được sau đối soát ~24 giờ.
- **Ai chịu phí khi hoàn (Shopee, bài 10626) [CAO]:** (a) "Hoàn tiền ngay – chưa nhận được hàng": shop không bị tính phí cố định / dịch vụ / xử lý giao dịch; (b) "Hoàn tiền ngay" lý do khác: shop vẫn chịu **phí xử lý giao dịch**, phí cố định + dịch vụ chỉ tính trên phần bán thành công; (c) "Trả hàng & Hoàn tiền": **không** tính phí dịch vụ / cố định / xử lý giao dịch; phí ship trả hàng shop chịu tối đa **40.000đ/đơn** (20.000đ Hỏa tốc) với lý do đổi ý hoặc lỗi shop, từ 01/04/2025, trừ hoàn một phần, lỗi DVVC, hoàn tiền ngay. Thuế khấu trừ được sàn hoàn trừ theo đơn trả.
- **TikTok:** phí xử lý đơn 3.000đ không hoàn nếu đã giao; phí giao dịch tính theo số tiền sau hoàn. Chính sách hoàn phí hoa hồng, ship trả: CHƯA XÁC MINH.
- **Tỷ lệ hoàn / hủy điển hình:** CHƯA XÁC MINH. Tìm kiếm không cho số có nguồn tin cậy (chỉ nhận định định tính: thời trang hoàn cao do mua theo cảm tính). Đề xuất cắm tham số `r` rồi đo thực tế sau 100–200 đơn đầu.

## 5. Công thức

**Ký hiệu (mỗi đơn, 1 SKU):** `P` = giá niêm yết; `Ds` = giảm giá của shop (mã shop, flash sale tự chịu); `Rev = P − Ds` (cũng là doanh thu tính thuế, trừ phần đồng tài trợ); `COGS` giá vốn gồm nhập + bao bì tiêu hao; `f` = phí cố định ngành; `t` = phí xử lý giao dịch (6%); `H` = phí hạ tầng (3.000đ); `v` = Voucher Xtra / VXP (0 nếu không tham gia; 5,5% Shopee, 5% TikTok; tối đa 50.000đ); `a` = hoa hồng affiliate (shop tự đặt); `k` = thuế khấu trừ (1,5%); `Sx` = phí ship shop chịu thêm (freeship shop tài trợ, vượt khối lượng); `B` = đóng gói, in phiếu; `A` = chi phí quảng cáo / đơn.

**Lợi nhuận đóng góp trước quảng cáo (đơn giao thành công):**
`CM = Rev − COGS − B − Sx − f·Rev − t·Rev − H − min(v·Rev, 50.000) − a·Rev − k·Rev`
(Shopee: cơ sở của `t` là Rev + ship khách trả; pass-through ship coi như triệt tiêu. Cơ sở tính của Voucher Xtra: CHƯA XÁC MINH.)

**Lợi nhuận ròng kỳ vọng mỗi đơn có hoàn tỷ lệ `r` (loại "Trả hàng & Hoàn tiền"):**
`LN = (1 − r)·CM − r·(B + Sx + Sret + d·COGS) − A`
với `Sret` = ship trả hàng shop chịu (≤ 40.000đ), `d` = tỷ lệ hàng hoàn không bán lại được.
Lưu ý: nếu doanh thu năm ≤ 1 tỷ thì `k·Rev` là **tạm ứng được hoàn lại** cuối năm → lợi nhuận kinh tế cao hơn `k·Rev`, nhưng dòng tiền vẫn thiếu cho tới khi hoàn xong; nếu > 1 tỷ thì `k` là thuế thật cộng thêm phần chênh theo phương pháp đã chọn.

**ROAS hòa vốn (theo doanh thu đơn do quảng cáo mang lại):**
`ROAS_hv = Rev / LN_trước_QC`, với `LN_trước_QC = (1−r)·CM − r·(B + Sx + Sret + d·COGS)`.
Quảng cáo lỗ khi ROAS thực < `ROAS_hv`. (Định nghĩa "doanh thu" trong ROAS của Shopee / TikTok có thể khác — giá trị đơn gồm ship? — CHƯA XÁC MINH.)

**3 ví dụ — GIẢ ĐỊNH, không phải số liệu thật:** giả định giá vốn, giá bán, tỷ lệ hoàn; phí lấy từ bảng Shopee 23/05/2026; mức phí cố định chọn giữa khoảng ngành.

| | A. Thời trang, Shopee | B. Làm đẹp, Shopee, có VXtra + affiliate | C. Nhà cửa nhỏ, Shopee, freeship shop trợ |
|---|---|---|---|
| P / Ds / Rev | 150.000 / 0 / 150.000 | 250.000 / 25.000 / 225.000 | 90.000 / 0 / 90.000 |
| COGS · B · Sx (đ) | 60.000 · 3.000 · 0 | 95.000 · 3.500 · 0 | 40.000 · 2.500 · 10.000 |
| f | 15% = 22.500 | 17% = 38.250 | 14,5% = 13.050 |
| t 6% | 9.000 | 13.500 | 5.400 |
| H | 3.000 | 3.000 | 3.000 |
| v | 0 | 5,5% = 12.375 | 0 |
| a | 0 | 5% = 11.250 | 0 |
| k 1,5% | 2.250 | 3.375 | 1.350 |
| Tổng phí sàn + affiliate / Rev | 23,0% | 34,8% | 23,8% |
| **CM (đ, % Rev)** | **50.250 (33,5%)** | **44.750 (19,9%)** | **14.700 (16,3%)** |
| ROAS hòa vốn, r = 0 | **2,99** | **5,03** | **6,12** |
| r = 10% / 5% / 8%, Sret = 40.000, d = 30% | LN trước QC 39.125 → ROAS_hv **3,83** (r = 10%) | 38.912 → **5,78** (r = 5%) | 8.364 → **10,76** (r = 8%) |

Bài học từ ví dụ: SKU giá thấp (C) bị hoàn 8% đã làm ROAS hòa vốn gần gấp đôi vì ship trả 40.000đ lớn so với biên 14.700đ → nên đặt giá sàn / loại SKU có CM < ~60.000đ nếu không kiểm soát được hoàn. Khi đổi sang TikTok, ví dụ A cho kết quả gần như bằng nhau (hoa hồng thời trang nữ trung vị 15% + 6% + 3.000đ), nhưng cơ sở tính phí giao dịch của TikTok gồm cả trợ giá sàn và ship khách trả.

**Rủi ro 01/01/2027:** nếu GTGT trên phí sàn quay về 10% và sàn giữ nguyên phần phí chưa thuế, phí đã gồm thuế tăng khoảng ×(1,10/1,08) ≈ +1,85% tương đối (ví dụ 6% → ~6,11%, 15% → ~15,28%). GIẢ ĐỊNH — Shopee chưa thông báo.

## 6. Mâu thuẫn nguồn
1. **Phí cố định Shopee:** blog ghi dải 1,21–8,1%, "mặc định 12,5%", hoặc 1,5–18% (đúng khoảng thực nhưng không nói theo ngành). Bảng chính thức 27540 + PDF giải quyết → dùng bảng chính thức. Blog thường lẫn mức trước / sau 23/05/2026.
2. **Ngày phí xử lý giao dịch Shopee:** blog "24/04" (ngày đổi tên) / "01/05" / "08/05" (Mall). Chính thức: đổi tên 24/04/2026; **01/05 shop thường, 08/05 Mall**. Mức "4,91% trước đó" chỉ có ở blog [TB].
3. **Voucher Xtra:** BigSeller / blog 4%; chính thức **5,5% từ 23/05/2026**. **PiShip:** 1.620 → 2.700. **TikTok VXP:** blog 4% (có nơi 3% → 4%); trang chính thức **5%**.
4. **Hoa hồng TikTok:** blog 12,5% (thường) / 14,5–15% (Mall) "từ 02/03/2026"; trang chính thức mặc định **14%** (từ 03/07/2026), Mall 15,5% rồi 16% (03/08/2026), bảng Mall mới 20/10/2026.
5. **GTGT trên phí sàn:** Shopee 8% đến 31/12/2026; TikTok nêu GTGT 10% + TNDN 5% (cơ chế nhà cung cấp nước ngoài, phí đã gồm thuế) — hai sàn khác nhau về cách thể hiện; hộ kinh doanh có phải "tự nộp thay" cho TikTok hay không CHƯA XÁC MINH.
6. **Ngưỡng thuế:** 100 / 200 triệu (Shopee Uni, bản 2025), 500 triệu (Luật TNCN 109/2025; NĐ 68/2026), **1 tỷ (NĐ 141/2026)**. Ngày hiệu lực NĐ 68: nguồn ghi 05/03/2026, một nguồn ghi nhầm 05/03/2025. Luật TNCN 109/2025 có hiệu lực 01/07/2026 theo báo chí trong khi NĐ 141 áp dụng từ 01/01/2026 → cần kế toán xác nhận cách áp dụng nửa đầu năm 2026.
7. **TNCN 15% hay 17% cho nhóm 1–3 tỷ:** một số blog 17%; Luật (cổng Chính phủ) 15% cho nhóm "trên 500 triệu đến 3 tỷ" (nay ngưỡng đã nâng lên 1 tỷ, chưa thấy điều khoản gốc nói rõ bậc 15% bắt đầu từ 1 tỷ).
8. **Mốc phân nhóm sổ kế toán TT 152/2025:** 500 triệu (bài đã đọc) vs ngưỡng 1 tỷ mới. Cũng bất đồng cách đánh số S2a / S2b.
9. **Số hiệu nghị định:** vài bài trích 252/2026, 254/2026 cho cùng nội dung — không tìm thấy bản gốc → bỏ.
10. **Freeship Xtra người bán:** blog 7,85%; không có trong danh sách phí dịch vụ chính thức hiện hành; một trang cũ nói đã ngừng từ 01/04/2025.

## 7. Điều cần hỏi kế toán / chi cục thuế
1. Hộ kinh doanh bán hàng hóa trên sàn, doanh thu dự kiến 2026 ≤ 1 tỷ: có phải làm hồ sơ hoàn thuế GTGT + TNCN bị sàn khấu trừ (1,5%) không? Mẫu, thời điểm (sau 31/12/2026? trước 31/03/2027?), nộp ở đâu; có được xin **miễn khấu trừ ngay** bằng văn bản để khỏi bị treo vốn không?
2. Xác nhận bằng văn bản: ngưỡng 1 tỷ là doanh thu **cộng tất cả kênh** (Shopee + TikTok + bán ngoài) hay từng sàn? Tính theo doanh thu trước hay sau giảm giá / hoàn hàng?
3. Khi vượt 1 tỷ: GTGT 1% tính trên **toàn bộ** doanh thu hay chỉ phần vượt? TNCN tỷ lệ 0,5% tính trên phần vượt 1 tỷ (theo tài liệu đã đọc); bậc 15% theo lợi nhuận áp dụng từ 1 tỷ đến 3 tỷ đúng không?
4. Nên chọn ngay từ đầu phương pháp **lợi nhuận** (sổ S2b–S2e, cần hóa đơn đầu vào) hay **tỷ lệ doanh thu**? Phương pháp phải giữ 2 năm; nếu mua hàng không có hóa đơn (nhập chợ, nhà bán nhỏ) thì chi phí bị loại.
5. TikTok: hộ kinh doanh đã có MST có thuộc "tổ chức có mã số thuế đã xác minh" phải **tự kê khai nộp GTGT 10% + TNDN 5% thay TikTok** không? Có nên tránh cung cấp MST hộ kinh doanh để TikTok thu trọn gói không?
6. Hóa đơn điện tử: bán hàng qua sàn cho người tiêu dùng, hộ ≤ 1 tỷ có phải xuất hóa đơn cho khách không? Khi > 1 tỷ, dùng hóa đơn từ máy tính tiền hay HĐĐT có mã; sàn xuất hộ hay shop tự xuất?
7. Sổ sách bắt buộc năm 2026 cho hộ ≤ 1 tỷ (S1a?) và mốc phân nhóm sổ có đã chuyển từ 500 triệu lên 1 tỷ không; cách lưu hồ sơ Shopee/TikTok (báo cáo thu nhập, chứng từ khấu trừ).
8. Mua hàng nhập khẩu / hàng sỉ không hóa đơn: cách ghi sổ giá vốn hợp lệ.
9. Khi nào nên chuyển công ty: so sánh tổng gánh nặng (GTGT được khấu trừ đầu vào, TNDN, sàn không còn khấu trừ thuế thay, chi phí kế toán) với hộ kinh doanh ở các mức doanh thu 1 / 3 / 10 tỷ; có điều kiện kinh doanh nào (mỹ phẩm, thực phẩm chức năng, điện tử) buộc phải là doanh nghiệp không.
10. GTGT trên phí sàn sau 31/12/2026: sàn có tăng phí hiệu quả không (liên quan định giá năm sau).

## 8. Khó khăn / điều cần chủ dự án quyết định
1. **Chưa lấy được bản PDF gốc NĐ 141/2026, NĐ 68/2026, TT 18/2026, TT 152/2025** (Thư viện Pháp luật chặn công cụ tải); các tỷ lệ chi tiết (GTGT 1% khi > 1 tỷ, bậc TNCN theo ngưỡng mới) dựa trên Luật TNCN (cổng Chính phủ) + Shopee + blog khớp [TB]. Cần chủ dự án / kế toán tải bản gốc từ chinhphu.vn hoặc Công báo để chốt trước khi đưa vào máy tính lợi nhuận.
2. **Chọn ngành và mức phí cố định:** bảng chính thức theo ngành cấp 3 nằm trong PDF "Shopee non-Mall_Phi Co Dinh tu 23.05.2026"; tôi chỉ có bảng tóm tắt theo ngành cấp 1–2 → máy tính cần PDF đầy đủ (chủ dự án / P1 xác định SKU & ngành cấp 3, rồi tra). TikTok đã gộp từ PDF chính thức (2.041 dòng, có thể trích đầy đủ nếu cần).
3. **Ngưỡng cảnh báo biên:** đề xuất P4 đặt luật "SKU có CM < 15% Rev hoặc < 15.000đ không chạy quảng cáo / không freeship" — cần chủ dự án duyệt.
4. **Mức dự phòng thuế:** vẫn trừ `k = 1,5%` trong lợi nhuận (thận trọng) và ghi riêng "khoản chờ hoàn" để không đánh giá thấp lợi nhuận khi ≤ 1 tỷ — chủ dự án cần chọn cách hiển thị.
5. **Giấy phép / điều kiện hộ kinh doanh với từng ngành hàng** (mỹ phẩm, thực phẩm, điện tử) — ngoài phạm vi P4, chuyển P-pháp lý nếu có.
6. Tỷ lệ hoàn, giá vốn, chi phí đóng gói, ads: toàn bộ là **giả định** cho tới khi có dữ liệu thật — đề nghị Đợt 1 bán thử có sổ theo dõi từng đơn.

*Không phải tư vấn thuế / đầu tư. Mọi con số cần kế toán xác nhận trước khi dùng cho kê khai.*

## Nguồn chính (đã đọc trực tiếp 12/11/2026)
- Shopee: https://banhang.shopee.vn/edu/article/27540 (phí 23/05/2026) · /2150 (phí xử lý giao dịch) · /2139 (phí cố định + ưu đãi shop mới) · /25329 (GTGT trên phí; HẠ TẦNG, PiShip, rút tiền) · /18182 (Voucher Xtra) · /3110 (phí dịch vụ) · /234 (thanh toán) · /10626 (trả hàng / hoàn tiền) · /24233 và /24204 (khấu trừ thuế)
- TikTok Shop VN: seller-vn.tiktok.com/university/essay?knowledge_id= 3396736626312961 (hoa hồng) · 753295858337537 (phí giao dịch) · 2968734088120080 (phí xử lý đơn) · 5776954021037841 (VXP+) · 6091769578850065 (đối soát) · 6837804173133569 và 2632156783101712 (thuế) · 3747225037670161 (affiliate)
- Pháp lý: https://xaydungchinhsach.chinhphu.vn/toan-van-nghi-dinh-so-141-2026-nd-cp-nang-nguong-doanh-thu-khong-phai-chiu-thue-len-1-ty-dong-119260504154326455.htm · https://xaydungchinhsach.chinhphu.vn/quy-dinh-thue-thu-nhap-ca-nhan-doi-voi-thu-nhap-tu-kinh-doanh-119260327063731539.htm · MISA (misaeshop.vn/40801), einvoice.vn/tin-tuc/hkd-doanh-thu-1ty-nam, luatvietnam.vn (NĐ 68), sapo.vn (TT 152/2025)
