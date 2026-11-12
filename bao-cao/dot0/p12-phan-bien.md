# P12 — Phản biện độc lập, Đợt 0 (12/11/2026)

**Trạng thái:** xong bản phản biện Đợt 0 · gửi KTS trưởng · chờ KTS / chủ dự án xem.
Nhánh: `phong/p12-dot0` — https://github.com/TKandCo/daovang/pull/new/phong/p12-dot0 (KHÔNG tự tạo PR).
P12 độc lập, không nhận việc từ phòng khác; báo cáo này chưa chia sẻ cho P1 / P4 / P8.
Nhãn: [CAO] chính thức · [TB] nhiều nguồn khớp · [THẤP] một nguồn / mâu thuẫn · CHƯA XÁC MINH. Không phải tư vấn pháp lý / thuế / đầu tư.

## Tóm tắt 5 dòng
1. **Lỗi lớn nhất: kế hoạch đổi sang Mức A "affiliate / dropship" nhưng mọi báo cáo và cổng Đợt 1 vẫn viết cho mô hình nhập hàng.** Chưa ai tính lãi lỗ của affiliate hay dropship.
2. Cổng Đợt 1 (≥ 1 SKU lãi dương + ≥ 30 đơn) **quá dễ**: qua được mà dự án vẫn lỗ gần hết 1.000 USD.
3. "Phí sàn ~23–24%" chỉ là phí *tối thiểu*. Chính ví dụ của P4 cho thấy shop mới tham gia voucher + affiliate lên **~36%**, chưa tính quảng cáo và hoàn hàng.
4. KTS chấm **quá dễ** ở "Độ tin cậy kỹ thuật" và "Chi phí & thời gian" (chưa có mã, chưa đo chi phí mà vẫn 7–8 điểm), và **bỏ sót mâu thuẫn giữa các phòng**.
5. Phần vững: bảng phí P4 (số học đúng, nguồn rõ, nhiều dòng khớp nguồn thứ hai), nguyên tắc không cào dữ liệu của P1, khuyến nghị "đợt đầu không ngành có điều kiện + gắn nhãn AI tất cả" của P8.

---

## Phần 1 — Kế hoạch tổng (lịch mở phòng, sổ ngân sách Mức A, sổ quyết định, vận hành cloud)

| # | Điểm yếu | Bằng chứng / phản ví dụ | Mức | Cách kiểm rẻ nhất |
|---|---|---|---|---|
| 1.1 | **Mức A đổi mô hình nhưng các phòng chưa theo kịp.** Sổ ngân sách ghi "không tồn kho: affiliate / dropship + hàng mẫu". Nhưng: P1 vẫn đề xuất "thử lô ≤ 300 USD/SKU, 3 SKU ≤ 900 USD, nhập thêm lô gấp 2" (`p1-radar.md` mục 5). Công thức P4 chỉ có `COGS` của hàng tự nhập, không có biến nào cho affiliate hay dropship. Sổ quyết định không ghi việc yêu cầu P1 / P4 làm lại theo Mức A. | `so-ngan-sach.md`; `p1-radar.md` §5 bước 1, 6; `p4-tai-chinh.md` §5 | **CAO** | Tổng quản giao P1 + P4 một việc nửa ngày: viết lại quy trình thử hàng và công thức lãi theo đúng Mức A. Ban thư ký ghi vào sổ quyết định. |
| 1.2 | **"Affiliate" và "dropship" là hai nghề khác nhau, chưa được chọn.** Affiliate = quảng bá hàng shop khác lấy hoa hồng. Không cần shop, không có "SKU lãi ròng". Shopee Affiliate thu phí 0,98% và khấu trừ TNCN 10% với khoản ≥ 250.000 đ [CAO theo P1, bài Shopee 09/07/2026]; Mẹ & Bé không có hoa hồng. Dropship = shop của mình bán, nhà cung cấp gửi hàng, nên vẫn chịu đủ phí sàn 23–36%. Cổng Đợt 1 "≥ 1 SKU lãi ròng dương" **không đo được** với affiliate. P8 ghi "affiliate có cần HKD không: CHƯA XÁC MINH". | `p1-radar.md` §2, §4; `p8-phap-ly.md` §2 | **CAO** | Chủ dự án chọn 1 trong 2 hướng chính cho Đợt 1 (hoặc tỷ lệ chia). P4 thêm 1 dòng công thức cho affiliate: hoa hồng × (1 − 0,98%) × (1 − 10%) − chi phí video. |
| 1.3 | **Dropship có rủi ro vận hành chưa ai nêu.** (a) Nhà cung cấp hết hàng → shop phải hủy đơn → bị tính điểm phạt / tỷ lệ đơn không thành công. (b) Giao chậm vì hạn chuẩn bị hàng. (c) Hàng không hóa đơn → chính P8 xếp "hàng không rõ nguồn gốc" là rủi ro #1. (d) Shop phải trả tiền nhà cung cấp trước, còn tiền sàn về sau giao hàng + 3–8 ngày. Báo cáo nào cũng chưa có số điểm phạt / hạn giao hàng của Shopee. | `p8-phap-ly.md` §6 #1; `p4-tai-chinh.md` §4 (chu kỳ tiền về) | **CAO** | P8 / P4 đọc trang "Sao Quả Tạ" / hạn chuẩn bị hàng trên Kênh Người Bán (30 phút). Trước khi chọn nhà dropship, đặt 1 đơn thử để đo số ngày giao thật. |
| 1.4 | **Thời gian của chủ dự án chưa có số, dù là điểm nghẽn đã được ghi nhận.** Sổ quyết định nói "thời gian một người là điểm nghẽn". Checklist vẫn "chờ chủ dự án: số giờ mỗi ngày". Riêng Đợt 0 chủ dự án đã có **≥ 15 việc tự làm**: đăng ký HKD, ngân hàng, hỏi thuế, hỏi Metric, đọc điều kiện API, chụp trang chính sách AI, tải PDF phí, luật sư… (gộp từ 3 biên bản audit và mục 8 P1). Đợt 1 thêm việc quay / duyệt video, trả lời khách, đóng gói hàng mẫu. | `checklist.md` mục "Chờ chủ dự án"; `audit-p1/p4/p8.md` "Việc phải sửa" | **CAO** | Chủ dự án ghi giờ thật trong 7 ngày (bảng tay). Ban thư ký cộng giờ ước tính cho mỗi việc trong checklist. Nếu tổng > số giờ rảnh thì cắt bớt phòng. |
| 1.5 | **Chi phí ẩn chưa vào Mức A.** (a) Gói Claude: sổ ghi "token giả định nằm trong gói hiện có" mà không ghi giá gói. Chạy 5–6 phiên cloud song song có thể cần gói cao hơn → CHƯA XÁC MINH, có thể lớn hơn cả dòng "token 50 USD". (b) Máy chủ chạy liên tục cho Đợt 2: "chưa ước tính" (`van-hanh-cloud.md`). (c) Phí ship trả hàng ≤ 40.000 đ/đơn + đóng gói + ship hàng mẫu. (d) Kế toán chỉ 50 USD (≈ 1 buổi), trong khi P4 có 10 câu và P8 khuyên "kế toán hằng quý". (e) 1,5% thuế bị sàn giữ cả năm (P4 §1.7). | `so-ngan-sach.md`; `van-hanh-cloud.md` §Giới hạn; `p8-phap-ly.md` (e).4 | **TB** | Chủ dự án ghi giá gói Claude đang trả vào sổ. Ban thư ký thêm dòng "chi phí cố định / tháng" và nhân với 6 tháng. |
| 1.6 | **Không có giả định doanh thu nào.** Không tài liệu nào có số đơn / ngày, giá trung bình hay tỷ lệ chuyển đổi dự kiến (dù ghi GIẢ ĐỊNH). Nên không ai biết 150 USD quảng cáo mua được bao nhiêu đơn. Ví dụ P4: ROAS hòa vốn 3,8–10,8 (GIẢ ĐỊNH). Với quảng cáo thử 150 USD ≈ 3,9 triệu đ và ROAS hòa vốn ~4, phải đạt ≥ 15,6 triệu đ doanh thu từ quảng cáo chỉ để hòa. Shop mới chưa có đánh giá thường đạt ROAS thấp hơn mức này: CHƯA XÁC MINH, phải đo. | `p4-tai-chinh.md` §5 | **TB** | P4 lập 1 bảng 3 kịch bản (xấu / vừa / tốt) cho 8 tuần, ghi rõ GIẢ ĐỊNH, chỉ ra điểm hòa vốn theo số đơn. |
| 1.7 | **Thứ tự chi tiền rủi ro: P2 Xưởng UGC 250 USD (25% vốn) mở cùng lúc với việc tìm sản phẩm.** Nếu đến tuần 8 chưa có SKU thắng thì phần lớn 250 USD đã trả cho gói tháng mà không còn dùng. Lịch Đợt 1 mở 3 phòng xây (P2, P6, P1 đầy đủ) trong khi P4 vẫn đang làm `apps/finance/` → có thể vượt trần "tối đa 3 phòng xây". | `lich-mo-phong.md`; `audit-p4.md` "phòng P4 cloud đang làm" | **TB** | Chỉ trả gói video theo tháng, sau khi có ≥ 1 sản phẩm qua điểm P1. Đếm lại số phòng "đang xây" khi mở Đợt 1. |

**Cổng Đợt 0 có thực tế không?** Phần lớn có. HKD mất 3 ngày làm việc [TB, P8], shop mở trong 2 tuần là khả thi. Nhưng:
- "Máy tính phí khớp ≥ 3 đơn **mẫu**": đơn mẫu tự làm thì so máy tính với chính bảng tính của mình, nên vòng tròn. Phải là ≥ 3 đơn thật (hoặc bản đối soát thật trên Kênh Người Bán), nhưng muốn có đơn thật thì phải đăng sản phẩm, mà đăng sản phẩm thì kích hoạt đồng hồ 30 ngày miễn phí cố định.
- "20 sản phẩm ứng viên đã chấm điểm": báo cáo P1 hiện có **0** sản phẩm được chấm, chỉ có khung chấm.

**Cổng Đợt 1 có thực tế không?** Có, nhưng **quá dễ** (xem kịch bản thất bại F1). "≥ 1 SKU lãi ròng dương" chưa định nghĩa có trừ chi phí công cụ / video / hàng mẫu hay không. Chỉ 30 đơn với tỷ lệ hoàn ~5–10% (GIẢ ĐỊNH) thì sai số quá lớn để kết luận một SKU "lãi". Đề xuất: "lãi ròng **cộng dồn của cả dự án** trong 4 tuần cuối Đợt 1 ≥ 0 sau mọi phí, kể cả công cụ; ≥ 30 đơn của **một** SKU". Điều kiện dừng ("không tăng vốn") là điểm tốt, nên giữ.

---

## Phần 2 — Báo cáo P1 / P4 / P8 và ba biên bản audit

| # | Điểm yếu | Bằng chứng | Mức | Cách kiểm rẻ nhất |
|---|---|---|---|---|
| 2.1 | **"Phí sàn ~23–24%" bị dùng như sự thật, nhưng chỉ là phí tối thiểu và chỉ có 1 nguồn báo chí.** P1 dùng con số này ở 3 chỗ (§1.8, §4, §5), nguồn VnBusiness 18/05/2026, và chính tiêu đề bài đó ghi "**25%** doanh thu". Theo bộ quy tắc của dự án, một nguồn = [THẤP], không phải [TB]. Tính lại từ ví dụ P4 (phí sàn + thuế 1,5%): A thời trang **24,5%**, C nhà cửa **25,3%**, B làm đẹp có Voucher Xtra + affiliate 5% **36,3%**. Shop mới thường phải vào voucher để có lượt xem → mức thật gần 30–36% hơn 24%. Khung chấm biên lãi của P1 dùng "phí sàn ~24%" nên **chấm biên cao hơn thực tế**. | `p1-radar.md` §1, §5 tiêu chí 3; `p4-tai-chinh.md` §5 (tính lại: B = (38.250+13.500+3.000+12.375+11.250+3.375)/225.000 = 36,3%); [VnBusiness](https://vnbusiness.vn/hai-ong-lon-shopee-va-tiktok-shop-cung-day-phi-san-cham-nguong-ky-luc-25-doanh-thu.html) | **CAO** | P1 thay "~24%" bằng phép tính của máy tính P4 theo từng ngành, có và không có voucher. |
| 2.2 | **Nhãn "Tổng phí sàn + affiliate / Rev" trong ví dụ P4 không gồm thuế 1,5%**, nên ghi 23,0% thay vì 24,5% (A). Số CM đúng, chỉ nhãn gây hiểu nhầm. Dễ là nguồn của con số "23–24%" đang lan sang kế hoạch. | `p4-tai-chinh.md` §5 bảng | THẤP | Sửa nhãn thành "…chưa gồm thuế khấu trừ". |
| 2.3 | **Mâu thuẫn giữa các phòng mà KTS không bắt.** (a) Ngày phí xử lý giao dịch 6% Shopee: P1 ghi "từ 08/05/2026", P4 ghi 01/05 cho shop thường (08/05 là Mall). (b) Hoàn thuế đã khấu trừ: P8 ghi "doanh thu dưới **200 triệu** có thể xin hoàn", P4 ghi hộ **≤ 1 tỷ** phải làm thủ tục hoàn. (c) P1 gán "thời trang 14,6 → 16,1%" cho **TikTok**; tìm kiếm của P12 cho thấy VnBusiness dùng con số 14,6 → 16,1% cho **Shopee** [THẤP]. Đây có thể là lỗi gán sàn, không phải "không tìm thấy số" như KTS ghi. | `p1-radar.md` §5; `p8-phap-ly.md` §1 dòng "Sàn khấu trừ"; `p4-tai-chinh.md` §1.7; `audit-p1.md` | **TB** | KTS thêm bước "đối chiếu chéo giữa các phòng" vào mẫu audit (grep cùng một khái niệm ở mọi báo cáo). |
| 2.4 | **BHXH bắt buộc của chủ hộ: P8 để [THẤP], P4 không nhắc, sổ ngân sách không có.** Kiểm của P12: chủ HKD nộp thuế theo kê khai bắt buộc đóng từ 01/07/2025, tối thiểu ~690.000 đ/tháng (29,5% × 2,34 triệu) [TB, nhiều nguồn: Sở/ BHXH địa phương]. Từ 01/07/2026, BHXH **dừng thu** với chủ hộ doanh thu < 1 tỷ/năm (CV 5628/BHXH-QLT TP.HCM và các bài khớp) [TB, chưa đọc văn bản gốc]. Hệ quả: hiện có lẽ **không tốn**, nhưng phải hỏi để khỏi bị truy thu, và sẽ thành chi phí ~8 triệu đ/năm khi vượt 1 tỷ. | [Hà Tĩnh](https://hatinh.gov.vn/vi/bai-viet/tu-172025-chu-ho-kinh-doanh-phai-dong-bhxh-bat-buoc-moi-thang-it-nhat-585000-dong), [Báo Văn hóa](https://baovanhoa.vn/doi-song/chu-ho-kinh-doanh-duoi-1-ti-dong-duoc-dung-dong-bhxh-bat-buoc-tu-nam-2026-247888.html), [lsvn](https://lsvn.vn/chu-ho-kinh-doanh-doanh-thu-tu-1-ti-dong-nam-tro-xuong-co-the-tham-gia-bhxh-tu-nguyen-a176780.html), [VietnamFinance](https://vietnamfinance.vn/ho-kinh-doanh-duoi-1-ty-dong-nam-khong-bat-buoc-phai-dong-bao-hiem-xa-hoi-d147961.html) | TB | Thêm 1 câu vào danh sách hỏi chi cục thuế / BHXH xã. |
| 2.5 | **P8 thiếu phần dữ liệu cá nhân khách hàng**, dù phạm vi P8 có mục này (định nghĩa agent). Trợ lý chốt đơn (P3) và sổ đơn hàng sẽ xử lý tên, SĐT, địa chỉ. P8 chỉ nhắc NĐ 330/2026 về phạt dữ liệu trong hệ thống AI. Không có checklist cho dữ liệu người mua. KTS vẫn chấm "Rủi ro & tuân thủ" **9/10**. | `p8-phap-ly.md` §4 (chỉ 1 dòng NĐ 330); `.claude/agents/p8-phap-ly.md` | TB | P8 thêm 1 mục ngắn trước Đợt 2 (trước khi mở P3). Chưa gấp cho Đợt 1. |
| 2.6 | **KTS chấm quá dễ hai tiêu chí theo đúng định nghĩa của bảng chấm.** "Độ tin cậy kỹ thuật" = "chạy lại được, có kiểm thử". Cả 3 phòng chưa có mã, KTS tự ghi "chỉ thiết kế, chưa có mã" nhưng vẫn cho 7–7,5. "Chi phí & thời gian" = "chi phí mỗi đơn vị đầu ra **có đo**". Không phòng nào đo chi phí / thời gian của mình, vẫn được 8. Nếu chấm đúng chữ (ví dụ 5 và 6), P4 còn ≈ 7,5 và P8 ≈ 7,4, tức **"cần sửa nhỏ" thay vì "đạt"**. | `bang-cham-diem.md`; ba tệp `audit-*.md` | **TB** | KTS hoặc ghi "không áp dụng, chia lại trọng số" cho báo cáo nghiên cứu, hoặc chấm theo chữ. Phải thống nhất trước Đợt 1. |
| 2.7 | **Mẫu kiểm của KTS nhỏ và không ngẫu nhiên.** Mỗi phòng kiểm 3 khẳng định, chọn tay. Bảng phí 79 dòng thì 3 dòng ≈ 4%, dưới mức "≥ 20%/tuần" của `CLAUDE.md`. Ngược lại có chỗ chấm **quá chặt**: KTS hạ "miễn phí cố định 30 ngày" của P1 xuống [THẤP], sau đó tự đính chính trong audit P4. Biên bản P1 đã chốt điểm thì không sửa lại. | `CLAUDE.md` mục Audit; `audit-p4.md` "Đính chính audit P1" | TB | KTS chọn dòng bằng số ngẫu nhiên (ví dụ dòng 7, 19, 33, 48, 61…), ghi danh sách dòng đã chọn vào biên bản. |

### Kiểm ngược bảng phí `bang-phi-v1.csv` (P12 tự kiểm, 12/11/2026)
**Hạn chế:** mạng của phiên P12 **chặn** `banhang.shopee.vn` và `seller-vn.tiktok.com` (lỗi DNS / 403). P12 **không đọc được nguồn chính thức** mà P4 ghi, nên chỉ đối chiếu bằng tìm kiếm độc lập (nguồn thứ hai). Đây là kiểm [TB], chưa phải [CAO].

| Dòng CSV | P4 ghi | Kết quả P12 | Nguồn đối chiếu |
|---|---|---|---|
| Shopee phí xử lý giao dịch | 6%, từ 01/05/2026 (Mall 08/05), mọi phương thức, trước 4,91% | **KHỚP** về 6% và 4,91% → 6%. Ngày shop thường / Mall: nguồn tách 01/05 vs 08/05, nguồn khác nói cả hai 01/05 → [TB] | [Sapo](https://www.sapo.vn/blog/phi-dich-vu-shopee-la-gi-tinh-phi-dich-vu-shopee), [BigSeller](https://www.bigseller.com/blog/articleDetails/thue-gtgt-shopee.4536.htm) |
| Shopee phí cố định thời trang | 13,5–16,5% từ 23/05/2026 (trước 12,5–13,5) | **KHỚP** với Sapo. VnBusiness ghi "14,6 → 16,1%" (cách gộp khác) | [Sapo 23/05](https://www.sapo.vn/blog/shopee-tang-phi-hang-loat-tu-23-05), [VnBusiness](https://vnbusiness.vn/hai-ong-lon-shopee-va-tiktok-shop-cung-day-phi-san-cham-nguong-ky-luc-25-doanh-thu.html) |
| Shopee Voucher Xtra | 5,5%, tối đa 50.000 đ/sp, từ 23/05/2026 (trước 4%) | **KHỚP** 4% → 5,5% (BigSeller) và trần 50.000 đ (Sapo) | [BigSeller](https://www.bigseller.com/blog/articleDetails/phi-shopee-2026-thay-doi-nhu-the-nao.4575.htm), Sapo như trên |
| Shopee ship trả hàng người bán chịu | ≤ 40.000 đ (20.000 Hỏa tốc), từ 01/04/2025 | **KHỚP** (GHN, BigSeller). Bổ sung: có chương trình hoàn phí ship / PiShip giảm thêm phần này → P4 có thể đang **tính lỗ hoàn hàng cao hơn thực tế** nếu tham gia PiShip | [GHN](https://ghn.vn/blogs/tip-ban-hang/tra-hang-shopee-ai-chiu-phi), [Sapo 10/2025](https://www.sapo.vn/blog/cap-nhat-tu-shopee-tiktok-shop-thang-10-2025) |
| TikTok phí giao dịch | 6% đơn tạo sau 00:00 09/05/2026 (trước 5%) | **KHỚP** (Viettel Store, BigSeller, BSS) | [BigSeller](https://www.bigseller.com/blog/articleDetails/phi-tiktok-shop-moi-nhat-2026.4733.htm), [Viettel Store](https://viettelstore.vn/tin-tuc/ban-hang-tren-tiktok-co-mat-phi-khong-chi-tiet-cac-loai-phi-2026) |
| TikTok phí xử lý đơn | 3.000 đ/đơn giao thành công từ 27/10/2025, không hoàn | **KHỚP** | [Sapo](https://www.sapo.vn/blog/tiktok-thu-phi-xu-ly-don-hang), Viettel Store |
| Shopee ưu đãi người bán mới | Miễn phí cố định 30 ngày, ≤ 200 đơn, sp đầu tiên từ 01/11/2026 [CAO] | **KHÔNG TÌM THẤY nguồn thứ hai.** Kết quả gần nhất là chương trình 200 đơn của **Shopee Malaysia**. Ghi chú: bảng ngân sách Mức A dựa vào ưu đãi này | tìm kiếm 12/11/2026; P12 không mở được bài 2139 |

Kết luận kiểm ngược: **6/7 dòng khớp** nguồn thứ hai. 1 dòng (ưu đãi người bán mới) **chưa kiểm được**. Lưu ý thêm: Ủy ban Cạnh tranh Quốc gia đã yêu cầu Shopee hoãn phí mới, nhưng các bài báo cho thấy việc hoãn là của chương trình **"Duy trì hiển thị"**, không phải bảng phí 23/05 ([Bộ Công Thương](https://moit.gov.vn/tin-tuc/uy-ban-canh-tranh-quoc-gia-yeu-cau-shopee-khong-ap-dung-cac-loai-phi-moi-doi-voi-nguoi-ban-hang.html), [VnEconomy](https://vneconomy.vn/shopee-hoan-ap-phi-moi-sau-yeu-cau-cua-uy-ban-canh-tranh-quoc-gia.htm)). CSV đã ghi đúng điều này. P4 nên thêm 1 câu vào báo cáo để người đọc không nhầm.
Số học ví dụ P4: P12 tính lại cả 3 ví dụ (CM, LN theo `r`, ROAS hòa vốn), **đều khớp**.

---

## Ba kịch bản thất bại

| # | Nếu… | Dự án mất gì | Dấu hiệu sớm |
|---|---|---|---|
| F1 | **Qua cổng Đợt 1 bằng một SKU "lãi" nhỏ** trong khi tổng dự án lỗ (công cụ video 250 + quảng cáo 150 + mẫu 200 USD đã tiêu) | Mở Đợt 2 (thêm P3, P5, P7, TikTok, máy chủ chưa ước tính) trên nền chưa có lãi thật → hết dự phòng 100 USD, quyết định dừng bị trễ 2 tháng | Lãi của "SKU thắng" < chi phí công cụ hằng tháng; < 30 đơn của chính SKU đó; ROAS thật < ROAS hòa vốn của máy tính P4 |
| F2 | **Dropship: nhà cung cấp hết hàng / giao chậm** trong tuần có quảng cáo | Hủy đơn → điểm phạt shop, giảm hiển thị; tiền quảng cáo đã trả; đánh giá xấu khó gỡ đối với shop mới | Tỷ lệ hủy / giao trễ > vài % trong 2 tuần đầu; nhà cung cấp không báo tồn kho theo ngày; không có hóa đơn khi hỏi |
| F3 | **Chủ dự án quá tải**: giờ rảnh thật ít hơn số việc (≥ 15 việc tự làm ở Đợt 0 + video + chăm khách ở Đợt 1) | Trễ tuần 8 mà không có đủ dữ liệu thật; ưu đãi 30 ngày miễn phí cố định trôi qua khi chưa bán được; báo cáo các phòng đọng chờ duyệt | Checklist "chờ chủ dự án" dài thêm mỗi tuần; PR chờ gộp > 3 ngày; chưa có con số "giờ / ngày" sau tuần 1 |

---

## Phần vững (nói rõ)
- **Bảng phí P4**: mỗi dòng có ngày hiệu lực, nguồn, nhãn tin cậy. Các mâu thuẫn được liệt kê thay vì giấu. 6/7 dòng P12 kiểm đều khớp nguồn thứ hai. Công thức có tính hoàn hàng + ROAS hòa vốn, ví dụ đúng số học. Ghi nhận rủi ro GTGT 01/01/2027 là tốt.
- **P1**: không đề xuất cào dữ liệu; thừa nhận trang chính thức không đọc được; "chưa dùng API sàn ở Đợt 0–1" là hợp lý.
- **P8**: tách luật với chính sách sàn; khuyến nghị đợt đầu (không ngành có điều kiện, chỉ diễn viên AI hư cấu, gắn nhãn tất cả) an toàn và rẻ; tự hạ nhãn ở chỗ chưa đọc văn bản gốc.
- **Kế hoạch**: điều kiện dừng "không tăng vốn"; vốn hàng tách vốn công cụ; phòng nghiên cứu không có khóa; tối đa 3 phòng xây. Các nguyên tắc này đúng hướng.
- **KTS**: ghi trung thực "cùng mô hình, không độc lập tuyệt đối", và tự đính chính audit P1.

## Đã kiểm / chưa kiểm
**Đã kiểm:** đọc toàn văn 4 tài liệu kế hoạch, 3 báo cáo, CSV 79 dòng, 3 biên bản audit, bảng chấm điểm, checklist. Tính lại 3 ví dụ P4 và tổng điểm có trọng số của 3 audit (khớp: 7,4 / 8,3 / 8,1). Đối chiếu 7 dòng CSV bằng tìm kiếm độc lập. Tra BHXH chủ hộ và việc Shopee hoãn phí.
**Chưa kiểm:** không mở được trang chính thức Shopee / TikTok (mạng chặn), nên không có dòng nào nâng lên [CAO]. Chưa kiểm hoa hồng TikTok theo ngành (PDF 2.041 dòng), thuế NĐ 141/2026 bản gốc, giá công cụ (Metric / Kalodata), giá gói Claude, quy định điểm phạt / hạn giao hàng của Shopee, điều khoản Shopee Affiliate 01/12/2025.

**Việc đề xuất cho chủ dự án (rẻ nhất trước):**
1. Mở Kênh Người Bán, chụp trang "ưu đãi người bán mới" (bài 2139) và trang điểm phạt. Khoảng 15 phút, xác nhận dòng CSV duy nhất chưa kiểm được.
2. Chọn hướng Đợt 1: affiliate hay dropship.
3. Ghi số giờ rảnh / ngày.

*Không phải tư vấn pháp lý / thuế / đầu tư; không đảm bảo lợi nhuận. Mọi số kịch bản là GIẢ ĐỊNH.*
