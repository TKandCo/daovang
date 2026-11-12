# P1 — Nghiên cứu xu hướng sản phẩm & nguồn hàng (Đợt 0)
Ngày: 12/11/2026 · Người lập: Trưởng phòng P1 · Phạm vi: nguồn dữ liệu HỢP PHÁP cho "Radar sản phẩm"

Nhãn độ tin cậy: [CAO] nguồn chính thức · [TB] nhiều nguồn khớp · [THẤP] một nguồn / mâu thuẫn · CHƯA XÁC MINH = không tìm được.
Giới hạn nghiên cứu: các trang tài liệu chính thức của Shopee Open Platform (open.shopee.com) và TikTok Shop Partner Center (JavaScript) KHÔNG đọc được bằng công cụ; trang giá của Kalodata/FastMoss/Metric không công khai giá. Vì vậy nhiều mục chỉ đạt [TB]/[THẤP] và phải xác minh tay (xem mục 8).

---

## 1. Tóm tắt 10 dòng
1. Không có nguồn nào cho "radar tự động miễn phí hoàn toàn". Lộ trình hợp pháp, rẻ nhất: dùng công cụ trả phí/dùng thử (Kalodata, FastMoss, Metric) để XEM, tự ghi tay top sản phẩm vào bảng của mình; không cào sàn.
2. Metric.vn (công ty Việt) bao phủ Shopee/TikTok Shop/Lazada/Tiki/Sendo, có "Tải dữ liệu chuyên sâu" ra Excel/CSV nhưng giới hạn theo số dòng và theo gói; giá KHÔNG công khai (gọi 033 806 2221 / info@metric.vn).
3. Kalodata/FastMoss: mạnh về TikTok Shop, có VN; giá công bố bởi blog mâu thuẫn (~29–99 USD/tháng) → CHƯA XÁC MINH, phải xem trang đăng nhập / App Store VN.
4. Google Trends API chính thức vẫn ở bản alpha, xin quyền mới được dùng (chưa thấy phát hành rộng); trước mắt dùng giao diện web Google Trends xem tay.
5. Shopee Affiliate (VN) cho người bán/KOC xem sản phẩm có hoa hồng; tham gia cần ≥ 2 sản phẩm hợp lệ, duyệt ~5 ngày; hoa hồng nguồn nói 11% hoặc tới 20% (mâu thuẫn). Dùng làm tín hiệu "sàn đẩy gì", KHÔNG phải dữ liệu để cào.
6. API Shopee VN: một bài tổng hợp (~2 năm tuổi) nói VN KHÔNG hỗ trợ nhà phát triển cá nhân bên thứ ba và tài khoản kết nối phải là Shop Yêu Thích/Mall [THẤP] — nếu đúng, hộ kinh doanh nhỏ chưa tự gọi API được; phải qua phần mềm bên thứ ba (BigSeller, Ginee, Sapo...) đã được Shopee cấp quyền.
7. API TikTok Shop: có loại "Seller in-house developer" cho app tùy chỉnh chỉ đọc dữ liệu shop mình, duyệt khoảng 5 ngày làm việc [TB-CAO theo trích dẫn trang chính thức]; có API Customer Service (gửi/nhận tin nhắn). CHƯA XÁC MINH Việt Nam có được đăng ký loại này không.
8. Phí sàn đã tăng mạnh 05/2026: tổng chi phí sàn ~23–24% doanh thu, lãi ròng nhiều shop chỉ 5–10% → khung chấm điểm phải trừ phí thật, ưu tiên sản phẩm biên gộp ≥ 35–40%.
9. Luật TMĐT 2025 hiệu lực 01/07/2026: người bán phải định danh; hộ kinh doanh kê khai (không còn thuế khoán từ 01/01/2026) → cần hóa đơn đầu vào; hàng tiểu ngạch không hóa đơn là rủi ro pháp lý/thuế.
10. Đề xuất: Radar v1 = bảng tính/SQLite nhập tay + xuất CSV từ công cụ trả phí, chấm điểm 100, thử lô ≤ 300 USD/SKU; chưa làm API cho tới khi xác minh điều kiện đăng ký.

---

## 2. Bảng so sánh nguồn dữ liệu xu hướng / bán chạy

| Nguồn | Giá | Dữ liệu có gì | Hợp pháp? | Xuất file / API? | Độ tin cậy thông tin |
|---|---|---|---|---|---|
| **Metric.vn** (Shopee, TikTok Shop, Lazada, Tiki, Sendo) | KHÔNG công khai; liên hệ 033 806 2221 / info@metric.vn. CHƯA XÁC MINH | Top bán chạy, doanh số, thị phần thương hiệu, báo cáo ngành (eReport, tổng quan sàn quý) | Có — dịch vụ thương mại của công ty VN (người dùng trả phí xem số liệu) | Có: "Tải dữ liệu chuyên sâu" Excel/CSV, tính theo số dòng tải; áp dụng tài khoản Advanced/Premium. Không thấy API. Nguồn: https://hotro.metric.vn/phan-tich-chuyen-sau/tai-du-lieu-chuyen-sau , https://hotro.metric.vn/huong-dan-dang-ky-goi-dich-vu/luot-su-dung/luot-tai-xuong (đọc 12/11/2026) | [CAO] cho tính năng (trang hỗ trợ chính thức); giá CHƯA XÁC MINH. Số liệu của Metric là ước tính từ dữ liệu công khai — tự kiểm bằng cách đối chiếu sản phẩm trên sàn (hướng dẫn của chính Metric: https://hotro.metric.vn/ho-tro/cau-hoi-thuong-gap/du-lieu) |
| **Kalodata** (TikTok Shop, có VN) | Blog mâu thuẫn: ~29, ~40, 45.99–49.99, từ 99 USD/tháng; thử 7 ngày hay không cũng mâu thuẫn (https://creatify.ai/blog/kalodata-pricing-plans-and-what-you-ll-actually-pay-in-2026 , https://tabcut.com/blog/post/does-kalodata-plans-worth-the-price-best-tools-for-tiktok-shop-analytics-kalodata-pricing-plans). Có thể trả bằng tiền địa phương ở VN [THẤP] | Sản phẩm/shop/video/KOL bán chạy, doanh số ước tính, tăng trưởng | Có (dịch vụ thương mại); không cần cào | Trang kalodata.com có đề cập xuất dữ liệu / kết nối lập trình nhưng không thấy chi tiết (https://www.kalodata.com/pricing) | [THẤP] về giá; chức năng [TB] |
| **FastMoss** (TikTok Shop; VN) | Blog: ~47–91 hoặc từ 49–99 USD/tháng; tính theo số tài khoản phụ; trang chính thức không nêu giá (https://www.fastmoss.com/blog/fastmoss-enhanced-account-flexibility-at-a-lower-cost/ — bài 2024) | Sản phẩm, shop, KOL, video, quảng cáo TikTok | Có | Có xuất file theo gói (không rõ hạn mức) | [THẤP] về giá; chức năng [TB] |
| **EchoTik** | CHƯA XÁC MINH | Dữ liệu TikTok Shop; có "API service" (theo bài tự quảng cáo 23/01/2026: https://www.echotik.live/blog/tiktok-shop-data-api-access-endpoints-metrics-and-analytics-2026/) | Chưa rõ nguồn/giấy phép dữ liệu | Có API (không thấy giá, độ phủ VN) | [THẤP] |
| **Google Trends** (web) | Miễn phí | Mức quan tâm tìm kiếm theo từ khóa, vùng VN, theo thời gian | Có | Web: tải CSV thủ công. API chính thức: alpha, đăng ký xin quyền, chưa thấy mở rộng; dữ liệu 5 năm, nhiều từ khóa/lần (https://developers.google.com/search/apis/trends , blog 24/07/2025: https://developers.google.com/search/blog/2025/07/trends-api) | [CAO] về hiện trạng alpha. Không dùng thư viện cào pytrends (đã archive 04/2025 — [THẤP]) |
| **Trang xếp hạng công khai của sàn** (Shopee/TikTok Shop: "Bán chạy", "Top tìm kiếm", Flash Sale) | Miễn phí | Thứ hạng, số đã bán hiển thị công khai | Xem tay: có. Cào hàng loạt: trái điều khoản (KHÔNG làm) | Không (chỉ chụp/ghi tay) | Số "đã bán" hiển thị trên trang sản phẩm là tín hiệu thô, có thể bị làm đẹp — [TB] |
| **Shopee Affiliate (VN)** — affiliate.shopee.vn | Miễn phí đăng ký; phí 0,98% trên tổng hoa hồng (từ 16/05/2025), khấu trừ TNCN 10% với mỗi khoản thanh toán ≥ 250.000 VND (từ 20/11/2025) | Danh sách sản phẩm có hoa hồng, link tiếp thị, báo cáo đơn của chính mình | Có (chương trình chính thức; tuân điều khoản) | Báo cáo của riêng mình trong bảng quản trị; API không thấy | Điều kiện: chủ shop ≥ 2 sản phẩm hợp lệ, duyệt ≤ 5 ngày, ngành không tính hoa hồng: Mẹ & Bé, sức khỏe nhạy cảm, rượu ≥ 15% — [CAO] (bài Shopee 09/07/2026: https://shopee.vn/blog/?p=190331). Mức hoa hồng: nguồn nói 11% hoặc tới 20% → [THẤP] (https://ghn.vn/blogs/tip-ban-hang/shopee-affiliate-la-gi-cach-dang-ky-va-lam-tiep-thi-hieu-qua). Điều khoản 01/12/2025: https://shopee.vn/affiliate/kol-dieu-khoan-tham-gia-update-01-12-2025/ (trang trả lỗi 503 lúc đọc → CHƯA ĐỌC ĐƯỢC) |
| **TikTok Shop Affiliate (VN)** | Miễn phí cho nhà sáng tạo | Sản phẩm có hoa hồng; shop người bán đặt hoa hồng | Có | Không thấy | Điều kiện nhà sáng tạo (≥ 1.000 người theo dõi, ≥ 18 tuổi, CCCD + mã số thuế) [THẤP] — một nguồn tháng 7/2026 (https://www.brandsvietnam.com/congdong/topic/tiktok-shop-affiliate-mua-cuoi-nam-2026-koc-can-chuan-bi-gi-khi-luat-choi-da-doi — trang trả lỗi 403, chỉ dựa trích dẫn tìm kiếm). Hoa hồng: CHƯA XÁC MINH |
| **Báo cáo công khai của Metric / báo chí** (BrandsVietnam, VnBusiness...) | Miễn phí | Số liệu ngành/quý (VD: Q1/2026 bốn sàn ~148.600 tỷ VND, +47% — Metric, qua https://vnbusiness.vn/hai-ong-lon-shopee-va-tiktok-shop-cung-day-phi-san-cham-nguong-ky-luc-25-doanh-thu.html , 18/05/2026) | Có | Không (chép tay) | [TB] |

Nguyên tắc: Radar v1 chỉ dùng (a) tính năng xuất file chính thức của công cụ trả phí trong điều khoản dịch vụ, (b) xem/ghi tay trên sàn, (c) báo cáo công khai. KHÔNG cào hàng loạt Shopee/TikTok; KHÔNG dùng dữ liệu từ nguồn không rõ giấy phép (vd. EchoTik API) trước khi đọc điều khoản.

---

## 3. API chính thức

### 3.1 Shopee Open Platform (open.shopee.com)
- Đăng ký tài khoản developer tại open.shopee.com → chờ duyệt → tạo app → nhận Partner ID/Key (Test trước, Live sau khi Go-Live). [TB] (https://documentation.qiscus.com/app-center/shopee , https://help.useresponse.com/hemi/knowledge-base/article/marketplaces-shopee-vn-developer-account-info-shopee-vietnam-vn_1 — không đọc được nội dung đầy đủ)
- Bài của FPT Shop (không ghi ngày, "2 năm trước" ≈ 2024): duyệt developer là người bán 3 ngày làm việc, đối tác thứ ba 1–2 tuần; Go-Live phản hồi ≤ 24 giờ; có 4 loại developer; đối tác thứ ba cần giấy phép kinh doanh + website. [THẤP] (https://fptshop.com.vn/tin-tuc/thu-thuat/shopee-api-188440)
- **Điểm quyết định nhưng [THẤP]**: cùng bài nói "Shopee Việt Nam không hỗ trợ nhà phát triển cá nhân thứ ba (Individual 3rd Party)" và "tài khoản kết nối API cần là Shop Yêu Thích hoặc thuộc Shopee Mall". Chưa tìm được nguồn thứ hai xác nhận hay bác bỏ; thông tin có thể đã cũ. Biểu mẫu "Shopee OpenAPI Request" nói người bán có hệ thống ERP + đội lập trình thì dùng Open Platform, còn lại đi qua nhà cung cấp thứ ba (https://docs.google.com/forms/d/e/1FAIpQLSeCSsRHQSoQvZccOSHIl5DZAPIkSnS4ivN0Z6rp6N7JIoofvQ/viewform) [THẤP]. Các nguồn khác nhau về loại app ("ERP System" vs "Seller In House System").
- **Hộ kinh doanh / cá nhân tự dùng cho shop mình**: CHƯA XÁC MINH. Hành động: tự mở open.shopee.com, xem mục đăng ký và loại Seller In-House; hoặc hỏi hỗ trợ.
- Loại dữ liệu: Order, Product, Shop (đã xác nhận bởi nhiều nhà cung cấp tích hợp — [TB]); Chat: có Chat API chính thức dùng bởi Ginee tại VN/ID/MY/SG/PH/TH — gửi text, ảnh, emoji, đơn, sản phẩm; xem tối đa 500 tin lịch sử; không gửi/nhận video; đơn kéo mỗi 4 giờ (https://ginee.com/id/help/ginee-chat-access-to-shopee-api/) [TB]. Quảng cáo (Ads API): CHƯA XÁC MINH.
- Quy định chatbot: KHÔNG tìm thấy văn bản chính thức. Chỉ có tuyên bố của nhà cung cấp phần mềm: cửa sổ nhắn 7 ngày kể từ tin cuối của người mua, tối đa 5 tin liên tiếp trước khi khách trả lời; tin AI tính vào tỉ lệ phản hồi (Zaapi, https://help.zaapi.com/llms-full.txt) [THẤP]; tin tự động mặc định của Seller Center không tính vào CRR, chỉ trả lời thủ công hoặc công cụ bên thứ ba qua API chính thức mới tính (Duoke 04/03/2026, bán phần mềm: https://www.duoke.com/en/blog/article/307-Shopee-vs-Lazada-vs-TikTok-Shop-Customer-Service-Rules-Every-Seller-Must-Know-2026) [THẤP]. Điều khoản chatbot của chính Shopee (https://help.shopee.sg/4/article/157965-Chatbot-Terms-of-Service) là cho chatbot hỗ trợ người mua của Shopee, không phải chatbot của người bán [CAO về nội dung, không áp dụng trực tiếp].

### 3.2 TikTok Shop Partner Center (partner.tiktokshop.com)
- Hai cổng: partner.us.tiktokshop.com (Mỹ) và partner.tiktokshop.com (thị trường khác); vùng đăng ký cố định, không đổi được. [TB] (https://developers.apideck.com/connectors/tiktok/docs/application_owner+oauth_credentials)
- Loại "Seller in-house developer": tài khoản shop đã qua KYB (doanh nghiệp) hoặc KYC (cá nhân); một số shop được duyệt tự động, còn lại gửi giấy tờ pháp nhân; duyệt thường 5 ngày làm việc; app tùy chỉnh chỉ truy cập dữ liệu shop mình thường không cần duyệt app / thử nghiệm beta; lỗi 36010071 nếu không đủ điều kiện. [TB-CAO] — trích từ kết quả tìm kiếm của các trang chính thức https://partner.tiktokshop.com/docv2/page/seller-developer-onboarding-onepager , https://partner.tiktokshop.com/docv2/page/developer-onboarding (nội dung trang không đọc được trực tiếp).
- Mâu thuẫn: một FAQ nói "hiện chỉ seller có account manager mới đăng ký được" → [THẤP], phải kiểm tra trong form.
- Custom app và public app cùng OAuth 2.0 và cùng quyền API (theo hướng dẫn bên thứ ba) [TB].
- Loại dữ liệu: sản phẩm, đơn hàng, vận chuyển, thanh toán, quan hệ nhà sáng tạo/affiliate (có trang "affiliate-integration"); API Customer Service: lấy danh sách hội thoại, đọc tin, gửi tin, tạo hội thoại, kết thúc phiên (Celigo https://docs.celigo.com/hc/en-us/articles/18704697472667); webhook sự kiện tin nhắn mới (Data Virtuality). Tin nhắn văn bản tối đa 2.000 ký tự; tin từ bot của TikTok không đồng bộ sang hộp thư ngoài (Gorgias https://docs.gorgias.com/en-US/tiktok-shop-5715568) [TB].
- Quy định chatbot: tin tự động/chatbot không tính vào tỉ lệ phản hồi 24 giờ; yêu cầu ≥ 90% (Duoke, [THẤP]); không tìm thấy chính sách chính thức → CHƯA XÁC MINH.
- Việt Nam có được đăng ký Partner Center loại này không: CHƯA XÁC MINH (không có văn bản chính thức liệt kê thị trường; một bài của Nova Analytics tháng 04/2026 nói TikTok mở Commerce API rộng hơn — [THẤP], tập trung Mỹ/Amazon).

### 3.3 Hệ quả cho dự án
- Đợt 0–1: KHÔNG phụ thuộc API sàn. Tích hợp chat/đơn qua phần mềm bên thứ ba đã được sàn cấp quyền (BigSeller, Ginee, Sapo...) nếu cần; hoặc dùng Seller Center thủ công.
- Song song: nộp đăng ký developer TikTok (Seller in-house) và hỏi Shopee VN — thử, không mất phí [chờ chủ dự án quyết].

---

## 4. Nguồn nhập hàng cho seller nhỏ ở VN

Bối cảnh pháp lý: Luật Thương mại điện tử 2025 (số 122/2025/QH15), hiệu lực 01/07/2026; người bán không còn ẩn danh, sàn phải xác thực người bán (https://baolaocai.vn/tu-hom-nay-172026-ban-hang-online-khong-the-an-danh-nguoi-ban-can-lam-gi-post902924.html ; https://thuvienphapluat.vn/van-ban/Thuong-mai/Luat-Thuong-mai-dien-tu-2025-so-122-2025-QH15-662035.aspx) [TB]. Từ 01/01/2026 hộ kinh doanh chuyển sang tự kê khai, cần sổ sách; thuế ước tính ngành phân phối GTGT 1% + TNCN 0,5% = 1,5% doanh thu (misaeshop, [THẤP]: https://www.misaeshop.vn/24423/phi-san-shopee/) — cần kế toán xác nhận. Hộ kinh doanh gặp khó với hóa đơn đầu vào (https://vneconomy.vn/ho-kinh-doanh-chat-vat-voi-hoa-don-dau-vao-khi-ap-dung-thue-ke-khai.htm) [TB]. Hàng thuộc ngành có điều kiện (mỹ phẩm, thực phẩm chức năng, đồ chơi trẻ em, điện...) phải theo luật chuyên ngành [TB].

| Kênh | Ưu | Nhược | Vốn tối thiểu (tham khảo) | Rủi ro pháp lý | Thời gian về hàng |
|---|---|---|---|---|---|
| **Chợ sỉ** (Tân Bình, An Đông, Ninh Hiệp, Đồng Xuân) | Thấy hàng thật, thương lượng giảm ~10–20%, nhập ít | Hàng phổ thông, cạnh tranh giá cao; nhiều tiểu thương không có hóa đơn | 1–3 triệu VND thử 50–100 sp (nguồn bán khóa học/phần mềm → [THẤP]); lô thử nghiêm túc 5–20 triệu | Không hóa đơn đầu vào → khó chứng minh nguồn gốc khi kê khai; hàng nhái/vi phạm sở hữu trí tuệ | Cùng ngày – 3 ngày |
| **Nhà phân phối / đại lý chính hãng** | Hàng chính hãng, chứng từ đầy đủ, hỗ trợ đổi trả | Yêu cầu đại lý, đặt tối thiểu, biên thấp, giá cạnh tranh sàn (kết quả tìm không xác nhận điều kiện cụ thể → CHƯA XÁC MINH) | Tùy nhà phân phối | Thấp nhất (có hóa đơn, bảo hành) | 2–7 ngày |
| **1688 / Alibaba / Taobao qua đơn vị order** (forwarder) | Giá gốc thấp, mẫu mã đa dạng | Nhà cung cấp chỉ giao nội địa TQ nên phải qua trung gian; phí order + vận chuyển + tỷ giá; chất lượng không đồng đều; đổi trả khó | Lô thử 5–30 triệu VND (ước tính của P1, chưa có nguồn) | Cao: hộ kinh doanh thường khó ký hợp đồng nhập khẩu/tự làm hải quan; hàng tiểu ngạch thường không hóa đơn; từ 2026 siết nguồn gốc/chứng từ, có thể bị phạt, thu giữ, truy thu thuế (https://ai-hay.vn/ho-kinh-doanh-co-duoc-nhap-hang-truc-tiep-tu-trung-quoc-pN1UmHA9hTa — [THẤP], nên hỏi kế toán/hải quan); hàng cấm/điều kiện; vi phạm nhãn hiệu | 7–20 ngày (CHƯA XÁC MINH; tùy tuyến) |
| **Dropship** (Droppii, Kho Si, PingGo, nhóm Facebook sỉ) | Gần như không vốn tồn kho, thử nhanh nhiều SKU | Biên thấp, ít kiểm soát chất lượng/giao hàng; rủi ro hết hàng, hoàn trả; nhiều shop bán trùng | ~0 vốn hàng | Trung bình: vẫn phải chịu trách nhiệm với khách; kiểm tra nguồn gốc hàng của nhà cung cấp | Phụ thuộc nhà cung cấp, 2–5 ngày |
| **Kho ký gửi / mua đứt lô nhỏ** | Giảm vốn | Tùy hợp đồng; CHƯA XÁC MINH mức phổ biến ở VN | Thấp | Cần hợp đồng ghi rõ chứng từ | — |
| **Dịch vụ fulfillment của sàn** (FBS Shopee, FBT TikTok) | Sàn lưu kho + giao | Không tìm được thông tin phí/điều kiện cho seller nhỏ → CHƯA XÁC MINH | CHƯA XÁC MINH | — | — |

### Nhập trực tiếp vs affiliate
- **Nhập trực tiếp**: mình mua hàng, bán trên shop của mình; chịu vốn tồn kho, hoàn trả, bảo hành, chứng từ; được toàn bộ biên (trừ phí sàn ~23–24% doanh thu — VnBusiness 18/05/2026 [TB]) → hợp với shop Shopee/TikTok Shop đã lập.
- **Affiliate**: quảng bá sản phẩm của shop khác để nhận hoa hồng; không vốn, không tồn kho; thu nhập chịu phí 0,98% và khấu trừ TNCN 10% khi ≥ 250.000 VND/lần (nguồn Shopee 09/07/2026); hộ kinh doanh có thể chịu thêm GTGT/TNCN [THẤP]; phụ thuộc quy tắc sàn đổi (xem https://www.brandsvietnam.com/congdong/topic/shopee-affiliate-voi-koc-tai-viet-nam-vi-sao-khong-the-ap-dung-nguyen-cach-lam-cua-tiktok-shop). Radar nên gắn cờ từng sản phẩm: "nhập" / "affiliate" / "cả hai".
- Không phát tán hứa hẹn lợi nhuận; mọi biên dưới đây là mô hình, không phải dự báo.

---

## 5. Khung chấm điểm sản phẩm (100 điểm)

Bối cảnh phí: Shopee phí xử lý giao dịch 6% từ 08/05/2026 (trước đó 4,9%) + phí cố định theo ngành (CHƯA XÁC MINH từng mức; bảng phí là hình ảnh) ; TikTok Shop hoa hồng từ 09/05/2026 tăng (thời trang 14,6% → 16,1%; mẹ & bé 14,5% → 17,8%); tổng phí sàn ~23–24% doanh thu chưa tính quảng cáo; lãi ròng nhiều shop 5–10% (VnBusiness 18/05/2026). Shop mới Shopee được miễn phí cố định 30 ngày đầu [TB].

| # | Tiêu chí | Điểm | Cách chấm (gợi ý, hiệu chỉnh sau lô thử đầu) |
|---|---|---|---|
| 1 | Nhu cầu | 20 | Doanh số ước tính 30 ngày (Metric/Kalodata) + đà tăng 3 tháng + Google Trends cùng chiều + ≥ 2 nguồn khớp (≥ 2 nguồn đạt thang 15–20; 1 nguồn tối đa 10) |
| 2 | Cạnh tranh | 15 | Số shop bán cùng mặt hàng, tập trung (top 3 shop chiếm > 60% → trừ), giá sàn đã bị đạp; có chỗ khác biệt (bộ combo, bảo hành, kích cỡ) |
| 3 | Biên lợi nhuận sau phí | 25 | Biên gộp sau: giá vốn + vận chuyển nhập + phí sàn (~24% mô hình) + quảng cáo (5–10% mô hình) + hoàn trả + thuế (~1,5% mô hình). Biên ròng ≥ 20% = 25đ; 12–20% = 15đ; 8–12% = 8đ; < 8% = 0đ và loại |
| 4 | Rủi ro pháp lý | 15 | Chứng từ đầy đủ; không thuộc ngành điều kiện (mỹ phẩm, thực phẩm chức năng, thuốc, đồ chơi trẻ em, điện/pin, hàng nhãn hiệu); không vi phạm sở hữu trí tuệ; không hàng nhái. Có yếu tố "ngành điều kiện" mà chưa có giấy tờ → 0đ và loại |
| 5 | Rủi ro hoàn trả | 10 | Ngành tỉ lệ hoàn thấp (kích cỡ, dễ vỡ, hỏng điện tử → trừ); đánh giá 1–2 sao phổ biến ở đối thủ; hàng nặng/cồng kềnh |
| 6 | Mùa vụ | 5 | Quanh năm = 5; mùa vụ rõ nhưng còn ≥ 6 tuần trước đỉnh = 3; đã qua đỉnh = 0 (kiểm tra Tết/lễ hội/11.11) |
| 7 | Khả năng làm video | 10 | Dễ trình diễn trong ≤ 30 giây, có "trước/sau", kích thích mua ngay (rất hợp TikTok Shop); sản phẩm trừu tượng = thấp |

Ngưỡng quyết định (đề xuất): ≥ 70 nhập thử; 55–69 theo dõi/thử affiliate trước; < 55 bỏ. Bắt buộc loại ngay (không tính điểm) nếu: biên ròng < 8%, thiếu giấy tờ ngành điều kiện, nghi hàng nhái.
Cập nhật điểm sau mỗi lô thử bằng số liệu thật (tỉ lệ chuyển đổi, hoàn trả, biên thực) — không giữ trọng số cố định nếu sai lệch lớn.

### Quy trình thử lô nhỏ (≤ 300 USD / SKU)
1. Chọn từ danh sách ≥ 70 điểm; tối đa 3 SKU cùng lúc (tổng ≤ 900 USD trong kịch bản vốn 1.000–4.000 USD, giữ ≥ 40% vốn dự phòng cho quảng cáo + vận hành).
2. Kiểm tra pháp lý & chứng từ nhà cung cấp (hóa đơn, nhãn hiệu, giấy công bố nếu cần) TRƯỚC khi đặt.
3. Đặt mẫu 1–3 cái, kiểm chất lượng thật + chụp ảnh/video của mình (sản phẩm đã đạt ≥ 70 điểm nhưng mẫu hỏng → loại).
4. Nhập lô thử: số lượng sao cho tổng ≤ 300 USD gồm cả vận chuyển; ghi đủ chi phí vào bảng.
5. Đăng bán 14–21 ngày; mức quảng cáo cố định thấp (VD ≤ 10% doanh thu dự kiến); mỗi SKU ≥ 5 video (TikTok) hoặc ≥ 1 chiến dịch AMS nhỏ (Shopee).
6. Quy tắc dừng sớm: sau 14 ngày < 10 đơn hoặc hoàn trả > 8% hoặc biên thực < 8% → dừng, thanh lý. Quy tắc mở rộng: ≥ 30 đơn/14 ngày, biên ròng thực ≥ 15%, hoàn trả < 5% → nhập thêm lô lớn gấp 2.
7. Ghi kết quả vào Radar (bảng Lô thử) để hiệu chỉnh điểm. Các ngưỡng trên là giả định khởi điểm, không phải số đã kiểm chứng.

---

## 6. Kiến trúc dữ liệu đề xuất Radar v1 (chỉ mô tả)

Lưu trữ gợi ý: SQLite (một file), nhập từ CSV xuất của công cụ trả phí + nhập tay; không lưu dữ liệu cá nhân khách hàng. Mỗi dòng dữ liệu có `source_id` + `captured_at` để truy nguồn.

| Bảng | Cột chính | Ghi chú |
|---|---|---|
| `product` | product_id, name, category, keywords, variant/sku_group, brand, regulated_flag, ip_risk_flag, season_tag, created_at | Một sản phẩm "khái niệm" (không phải listing) |
| `supplier` | supplier_id, name, type (chợ sỉ/nhà phân phối/1688-forwarder/dropship), contact, docs_available (hóa đơn Y/N), moq, lead_time_days, rating_note | Không lưu mật khẩu/ khóa |
| `supplier_quote` | quote_id, product_id, supplier_id, unit_cost_vnd, moq, ship_cost_per_unit, currency/fx, quoted_at, valid_until | Nhiều báo giá/sản phẩm |
| `listing_price` | id, product_id, platform (shopee/tiktok), shop_ref, price_vnd, sold_est_30d, rating, captured_at, source_id | Giá bán đối thủ + doanh số ước tính |
| `trend_signal` | id, product_id, source_id, metric (sales_30d / growth_3m / search_index), value, region, period_start, period_end, captured_at | Dạng dọc, dễ thêm nguồn mới |
| `source` | source_id, name, type (paid_tool/google_trends/platform_public/affiliate/manual), url, license_note, export_method, reliability (CAO/TB/THAP), cost_per_month | Ghi rõ hợp pháp & cách lấy |
| `fee_config` | platform, category, fee_name, rate, effective_from, source_url | Phí thay đổi (05/2026) → lưu theo ngày hiệu lực |
| `score` | product_id, scored_at, demand, competition, margin, legal, returns, season, video, total, margin_calc_json, decision | Chia theo 7 tiêu chí ở mục 5 |
| `trial_batch` | batch_id, product_id, supplier_id, qty, cost_total_usd, start_date, orders, returns, net_margin_real, decision | Vòng phản hồi hiệu chỉnh điểm |
| `affiliate_item` | id, product_id, platform, commission_rate, rate_source, valid_from/to | Cờ "nhập" vs "affiliate" |

Luồng: nguồn → (nhập CSV/tay) → `trend_signal`/`listing_price` → tính `score` → danh sách "ứng viên" → `trial_batch` → quay lại hiệu chỉnh `score`.
Để sau này gắn trợ lý chốt đơn: bảng `order_event` / `chat_thread` thêm ở giai đoạn sau khi có kênh API hợp pháp (qua phần mềm bên thứ ba hoặc API chính thức) — chưa thiết kế ở v1.

---

## 7. Đề xuất 3 bước nhỏ tiếp theo
1. **(1–2 ngày) Xác minh có/không**: (a) mở trang đăng ký open.shopee.com và Partner Center TikTok xem điều kiện thật cho hộ kinh doanh VN; (b) gọi/gửi email Metric.vn hỏi giá gói + hạn mức tải dữ liệu; (c) xem giá Kalodata/FastMoss trong tài khoản dùng thử hoặc App Store VN. Không tạo tài khoản thay chủ dự án — chủ dự án tự đăng ký.
2. **(3–5 ngày) Radar bản thủ công**: bảng tính/SQLite theo mục 6; chọn 1 công cụ trả phí (khuyến nghị dùng thử Metric hoặc Kalodata 1 tháng) → ghi 30–50 sản phẩm ứng viên + chấm điểm 100 + tra báo giá chợ sỉ/nhà phân phối.
3. **(2 tuần) Thử 1–2 SKU** ≤ 300 USD/SKU theo quy trình mục 5; thu số thật để hiệu chỉnh trọng số điểm. Song song nộp đăng ký developer TikTok (Seller in-house) nếu điều kiện cho phép.

## 8. Khó khăn cần chủ dự án quyết định
1. **Chọn công cụ trả phí nào / ngân sách bao nhiêu** (Metric cho đa sàn và số liệu VN vs Kalodata/FastMoss chỉ TikTok) — giá chưa xác minh.
2. **Kênh nhập chính**: chấp nhận chợ sỉ không hóa đơn (rủi ro thuế) hay ưu tiên nhà phân phối có hóa đơn (biên thấp hơn)? Có làm 1688 qua trung gian không (rủi ro pháp lý cao với hộ kinh doanh)?
3. **Shopee API cho hộ kinh doanh**: nếu đúng "không hỗ trợ cá nhân / cần Shop Yêu Thích", chấp nhận dùng phần mềm bên thứ ba (trả phí, chia sẻ quyền truy cập shop) hay đợi? Cần chủ dự án tự gọi hỗ trợ Shopee.
4. **Phí sàn cố định từng ngành**: chưa lấy được bảng (hình ảnh); cần chủ dự án chụp bảng phí từ Kênh Người Bán để điền `fee_config`.
5. **Ngành hàng** muốn thử (tránh ngành điều kiện: mỹ phẩm, thực phẩm chức năng, đồ chơi trẻ em) — ảnh hưởng nặng đến thang điểm pháp lý.
6. **Kế toán/thuế**: hộ kinh doanh kê khai từ 2026 — cần nhờ kế toán/ chi cục thuế xác nhận mức thuế và quy tắc hóa đơn đầu vào trước khi nhập số lượng lớn.
7. Chatbot chốt đơn: chưa có văn bản chính thức cho phép/giới hạn bot qua API trên cả hai sàn; cần xác minh với sàn trước khi xây trợ lý tự động trả lời.
