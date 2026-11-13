# P1 — Công cụ số liệu: tự làm hay mua? (họp KTS + bảng giá)
Ngày: 12/11/2026 · Người lập: Trưởng phòng P1 · Nhánh: `phong/p1-dot0`

**Trạng thái:** 🟢 đã họp KTS và tra giá · chờ chủ dự án: duyệt lộ trình mục 4 (chưa chi đồng nào).

Quyết định của chủ dự án (12/11/2026, trong phiên):
1. Đồng ý chọn 3–5 nhóm để tìm sản phẩm trước. P1 chốt **4 nhóm: N18 phụ kiện thú cưng, N01 hộp/khay nhựa sắp xếp, N02 móc treo/tôn lỗ, N05 dụng cụ vệ sinh nhà**.
   KTS lưu ý: N05 mới có tín hiệu cấp ngành; N02 thị trường hẹp, nguồn [THẤP].
2. Báo giá công cụ, nhưng họp KTS trước để biết có tự làm được không.
3. Mở mạng phiên cloud: đã tạo môi trường riêng `daovang` (chủ dự án duyệt), mở metric.vn, hotro.metric.vn, banhang.shopee.vn, brandsvietnam, vietnam.vn, kalodata, fastmoss.

---

## 1. Kết luận họp KTS (tóm tắt, KTS chỉ đọc, không sửa tệp)
- **Tự làm được khoảng 70% Radar, gần 0 đồng, hợp pháp.** Đây là các việc xem tay rồi ghi vào bảng CSV đã có: giá đối thủ, đếm số shop, tỷ lệ đánh giá 1–2 sao, Google Trends (tải CSV), báo cáo công khai cấp ngành.
- **Không tự làm được nếu không cào:** doanh số ước tính 30 ngày và đà tăng 3 tháng của từng sản phẩm đối thủ. Thiếu phần này thì tiêu chí Nhu cầu chỉ đạt tối đa 10/20 điểm, nên khó đạt ngưỡng 70.
- **Giá trị với Mức A:** vừa phải. Mức A không có tồn kho nên chọn sai chỉ mất vài chục USD tiền mẫu. Đáng mua **một đợt ngắn**, không đáng thuê dài hạn.
- **Công sức tự làm (ƯỚC TÍNH, chưa đo):** lượt đầu khoảng 9–10 giờ cho 4 nhóm × 8 sản phẩm; sau đó 2–3 giờ/tuần. Phần xem trang sàn do **chủ dự án** làm, vì agent không được giả lập người dùng trên sàn. Agent soạn bảng và chấm điểm.
- **Điều kiện trước khi chi:**
  - có ≥ 15 sản phẩm đã qua lọc tay;
  - chi ≤ 100 USD (dòng "P1 Radar & dữ liệu" trong `ban-thu-ky/so-ngan-sach.md`);
  - điều khoản cho dùng nội bộ và xuất file;
  - công cụ có dữ liệu Shopee;
  - thanh toán bằng thẻ trả trước có hạn mức.
- **Rủi ro:**
  - Số của công cụ là ước tính. Cần đối chiếu 5–10 sản phẩm với số "đã bán" xem tay trên sàn.
  - Điều khoản dùng dữ liệu chưa đọc. Nếu sau này đóng gói Radar bán cho seller khác, có thể không được chép số liệu của công cụ vào.
  - Không chia sẻ tài khoản với người ngoài.
  - Không dùng API nào không rõ giấy phép dữ liệu (ví dụ EchoTik).

## 2. Bảng giá (tra 12/11/2026)
### Metric.vn — đa sàn (Shopee, TikTok Shop, Lazada, Tiki). Giá chính thức [CAO] — S22
**KTS chưa tự mở được trang này** (công cụ tìm kiếm không trả trang giá) → chủ dự án nên tự mở https://metric.vn/analytics/pricing để xác nhận. Trang giá chỉ hiện chữ khi mở bằng trình duyệt, nên tôi mở trang giá công khai của Metric một lần bằng trình duyệt tự động. Không đăng nhập, không tạo tài khoản.

| Gói "Ecom Analytics" | Thời hạn | Lượt phân tích | Advanced (lịch sử số liệu 1 năm) | Premium (lịch sử 2 năm) |
|---|---|---|---|---|
| Starter | **4 tháng** | 200 | **8 triệu đ** | 12 triệu đ |
| Metric 500 | 12 tháng | 500 | 18 triệu đ (tải chi tiết 20.000 dòng) | 27 triệu đ |
| Metric 1000 | 12 tháng | 1.000 | 32 triệu đ (50.000 dòng) | 48 triệu đ |
| Dùng thử | **7 ngày, miễn phí** | — | — | — |

- **Không có gói theo tháng.** Gói rẻ nhất là 8 triệu đ cho 4 tháng ≈ **308 USD** (theo tỷ giá tham chiếu 26.000 đ/USD của sổ ngân sách). Mức này **vượt trần 100 USD gấp 3 lần**.
- Lượt phân tích không dùng hết thì mất khi hết hạn gói.
- Gói Starter không ghi có "tải dữ liệu chi tiết". Trang hỗ trợ (S24, ghi cập nhật khoảng 2 năm trước) cũng nói tải dữ liệu chỉ có từ gói Advanced. Tức là gói rẻ nhất **có thể không xuất được CSV** → CHƯA XÁC MINH, phải hỏi Metric.
- Dùng thử: trang giá ghi 7 ngày; trang hỗ trợ cũ ghi 10 lượt, 3 ngày → [THẤP], hỏi lại Metric.
- Kho eReport: trang ghi "Free 7 ngày xem mọi báo cáo" (đọc 12/11/2026, [CAO] về việc có ưu đãi; điều kiện chưa đọc).
- Metric Omni Analytics (TikTok video, quảng cáo Facebook — **không phải dữ liệu sàn Shopee**): dùng thử 100 credits trong 5 ngày; Advanced 12 triệu đ/năm; Premium 24 triệu đ/năm (S23, [CAO]).
- Liên hệ: 033 806 2221 · info@metric.vn (trên trang chính thức).

### FastMoss — chủ yếu TikTok Shop. Giá [THẤP] — S25 (hạ từ [TB] sau audit KTS vòng 2: có nguồn ghi 59/109 hoặc 59/299 USD)
- Basic 49 USD/tháng (**tháng đầu 29 USD**); Pro 89 USD; Ultimate 139 USD. Thêm người dùng phải trả thêm tiền.
- Nguồn: blog của chính FastMoss và một trang so sánh (tra 10/2026) khớp nhau; nhưng TrustRadius / SaaSWorthy ghi khác → mâu thuẫn. "Tháng đầu 29 USD" KTS không xác nhận được.
- Trang giá chính thức chặn bằng bước kiểm tra chống bot. **Tôi dừng, không vượt** (quy tắc 4).
- Có bao phủ Shopee Việt Nam không: CHƯA XÁC MINH.

### Kalodata — chủ yếu TikTok Shop. Giá [THẤP] — S26
- Các nguồn ghi khác nhau: 45,99–129,99 USD/tháng (App Store); 59,9 / 119,9 USD (blog FastMoss, đối thủ cạnh tranh nên có thể thiên lệch).
- Dữ liệu Shopee VN có thể chỉ có ở gói Professional (nguồn cũ).
- Dùng thử 7 ngày: [THẤP].
- Trang chính thức không tải được (quá thời gian chờ).

## 3. Kiểm lại số liệu cũ khi đã có mạng
- Các trang eReport Metric (S11–S14) giờ chỉ hiện danh sách báo cáo và nút đăng nhập, không hiện số. **Chưa đối chiếu được** → giữ [THẤP].
- banhang.shopee.vn (bài 2139) tải được nhưng nội dung hiện bằng JavaScript, không ra chữ. Đính chính "miễn phí cố định 30 ngày" vẫn dựa vào P4 [CAO theo P4].
- brandsvietnam.com, kalodata.com: trang chặn truy cập tự động → vẫn chưa đọc được.

## 4. Đề xuất lộ trình tối ưu chi phí (chờ chủ dự án duyệt)
| Bước | Việc | Tiền |
|---|---|---|
| 1 | Tự làm lượt 1 cho 4 nhóm đã chọn: chủ dự án xem tay trang sàn và ghi vào `apps/radar/mau/` (P1 soạn sẵn bảng, có hướng dẫn); Google Trends | 0 đ |
| 2 | Khi có ≥ 15 sản phẩm: **chủ dự án tự đăng ký dùng thử Metric 7 ngày** + eReport 7 ngày miễn phí. Gom hết sản phẩm cần tra vào tuần dùng thử | 0 đ |
| 3 | Nếu cần thêm số TikTok Shop: FastMoss Basic **tháng đầu 29 USD [THẤP]**, hoặc 49 USD. Thẻ trả trước, tắt tự gia hạn, hủy sau 1 tháng | 29–59 USD [THẤP] (nằm trong trần 100 USD) |
| 4 | Chỉ khi shop đã có doanh thu: cân nhắc Metric Starter 8 triệu đ/4 tháng | ≈ 308 USD — **vượt trần, cần chủ dự án duyệt riêng** |

Trước bước 2–3, chủ dự án tự hỏi nhà cung cấp:
- gói rẻ nhất có xuất được CSV không;
- dùng thử có cần thẻ thanh toán không;
- điều khoản có cho dùng nội bộ không.

P1 có thể soạn nháp câu hỏi. Chủ dự án là người gửi.

**Khuyến nghị P1, khớp với KTS:** tự làm trước, dùng thử miễn phí, chưa mua gì. Bỏ qua gói Metric trả phí ở Mức A.
Không phải khuyến nghị đầu tư / không đảm bảo lợi nhuận.

## 5. Đã kiểm gì / chưa kiểm gì
- **Đã kiểm:**
  - Giá Metric đọc trực tiếp trên trang chính thức ngày 12/11/2026, đã bấm từng tab gói Starter / 500 / 1000.
  - Đã thêm 5 nguồn mới S22–S26 vào `apps/radar/du-lieu/source.csv`; `python3 apps/radar/kiem_tra.py` → ĐẠT.
- **Chưa kiểm:**
  - Điều khoản sử dụng của Metric, FastMoss, Kalodata (trang điều khoản Metric chuyển về trang chủ).
  - Giá Kalodata và FastMoss trên trang chính thức (bị chặn).
  - Gói Starter có xuất CSV không; thời gian dùng thử thật (7 hay 3 ngày).
  - Công sức 9–10 giờ là ước tính của KTS, chưa đo.
