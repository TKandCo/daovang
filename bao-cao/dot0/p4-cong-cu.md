# P4 — Công cụ máy tính lợi nhuận mỗi đơn — Đợt 0 (12/11/2026)

**Trạng thái:** 🟢 xong phần việc giao · nhánh `phong/p4-dot0` đã đẩy · **chờ chủ dự án tạo PR** sau audit KTS:
https://github.com/TKandCo/daovang/pull/new/phong/p4-dot0

## 1. Trạng thái
🟢 Đúng tiến độ. 33/33 kiểm thử ĐẠT; 3 ví dụ của `p4-tai-chinh.md` tái tạo KHỚP 12/12 con số. Chi tiền: 0 đ.

## 2. Đã làm (việc → bằng chứng)
| Việc | Bằng chứng |
|---|---|
| Máy tính lợi nhuận mỗi đơn, Python thư viện chuẩn, đọc `bang-phi-v1.csv` | `apps/finance/taichinh/` (`bang_phi.py`, `tinh_loi_nhuan.py`, `__main__.py`); hướng dẫn `apps/finance/README.md` |
| Đầu vào: giá bán, giá vốn, ngành, sàn, ngày bán, vận chuyển, voucher shop / voucher sàn, quảng cáo (% doanh thu), tỷ lệ hoàn, affiliate shop trả, thuế GTGT / TNCN (tham số, mặc định 1% + 0,5% từ bảng phí) | `python3 -m taichinh --help` |
| Đầu ra: lợi nhuận ròng, biên ròng, giá hòa vốn (có / không quảng cáo), ROAS hòa vốn, so sánh nhập trực tiếp vs affiliate, dòng "không đảm bảo lợi nhuận", nguồn + độ tin cậy + hiệu lực từng khoản phí; `--json` | chạy mẫu trong README |
| Mức dạng khoảng ("13.5-16.5"): chọn `--muc thap/giua/cao`, **mặc định cao**; luôn in cảnh báo kèm khoảng | `test_mac_dinh_cao`, `test_khoang_thap_giua_cao` |
| Chọn mức theo ngày hiệu lực: dòng có ngày bắt đầu muộn nhất ≤ ngày bán; dòng "từ … đến …" hết hạn thì bỏ; mức cũ trong ghi chú ("Truoc 23/05/2026: 14.0", "truoc do 5%") dựng thành phiên bản cũ; không có mức cho ngày đó → báo THIẾU DỮ LIỆU (không đoán) | `TestNgayHieuLuc` (6 kiểm thử) |
| Cảnh báo mâu thuẫn **"phí hạ tầng 3.000đ chỉ Shopee Mall?"** — in ở MỌI kết quả Shopee; vẫn tính 3.000đ (thận trọng); `--bo-phi-ha-tang` để xem kịch bản kia | `test_canh_bao_ha_tang_mall` |
| Cảnh báo khác: GTGT 8% phí sàn hết 31/12/2026 (ngày bán sau đó); thuế 1,5% có thể được hoàn nếu ≤ 1 tỷ; Voucher Xtra chưa rõ cơ sở tính; ngày bắt đầu phí hạ tầng chưa xác minh; TikTok chưa có phí ship trả hàng | `tinh_loi_nhuan.py` |
| KIỂM NGƯỢC 3 ví dụ | `cd apps/finance && python3 -m taichinh.kiem_nguoc` → "TẤT CẢ KHỚP"; `TestKiemNguoc` |
| Kiểm thử unittest (công thức tính tay, giá hòa vốn cho LN = 0, trần voucher, hoàn hàng, ngày hiệu lực, mức khoảng, thiếu dữ liệu, CLI) | `python3 -m unittest discover -s apps/finance -t apps/finance -v` → `Ran 33 tests … OK` |

## 3. Số liệu — kết quả kiểm ngược (ví dụ GIẢ ĐỊNH của báo cáo P4, ngày bán 12/11/2026)
Báo cáo P4 chọn phí cố định **giữa khoảng** (thời trang 15%, nhà cửa 14,5%) → kiểm ngược chạy `--muc giua`.

| Ví dụ | CM công cụ / báo cáo | ROAS hv r = 0 | LN trước QC có hoàn | ROAS hv có hoàn |
|---|---|---|---|---|
| A. Thời trang Shopee | 50.250 / 50.250 | 2,985 → **2,99** / 2,99 | 39.125 / 39.125 | 3,834 → **3,83** / 3,83 |
| B. Làm đẹp, VXtra + aff | 44.750 / 44.750 | 5,028 → 5,03 / 5,03 | 38.912,5 / 38.912 | 5,782 → 5,78 / 5,78 |
| C. Nhà cửa nhỏ, freeship | 14.700 / 14.700 | 6,122 → 6,12 / 6,12 | 8.364 / 8.364 | 10,760 → **10,76** / 10,76 |

**Lệch:** không có. Chỉ B lệch 0,5đ do báo cáo cắt số lẻ (38.912,5 → 38.912).
**Khác biệt khi dùng mặc định `cao` (thận trọng):** A thời trang 16,5% → CM 48.000đ, ROAS hv có hoàn **4,04** (thay vì 3,83); C nhà cửa 16% → CM 13.350đ, ROAS hv có hoàn **12,64** (thay vì 10,76). B không đổi (sắc đẹp 17% là một số). → Báo cáo P4 nên ghi rõ ví dụ dùng mức giữa; khi định giá thật nên tra PDF ngành cấp 3 rồi nhập `--phi-nganh`.

Nguồn phí: toàn bộ lấy từ `bang-phi-v1.csv` (nguồn + độ tin cậy từng dòng, tra 12/11/2026). Mặc định "hàng hoàn hỏng 30%" là **GIẢ ĐỊNH** (lấy theo ví dụ báo cáo).

## 4. CHƯA kiểm / chưa xác minh
- **Phí hạ tầng chỉ Mall?** — chưa kiểm trên Kênh Người Bán (cần tài khoản shop; P4 không có). Công cụ chỉ cảnh báo.
- **Không có lịch sử phí TikTok trước 03/07/2026** trong bảng v1 → ngày bán trước đó báo thiếu dữ liệu (đúng thiết kế).
- Mức cũ suy từ ghi chú **không có ngày bắt đầu** → áp cho mọi ngày trước mốc; chỉ đúng trong khoảng gần mốc. Mức 4,91% (phí giao dịch Shopee trước 01/05/2026) là nguồn blog → hạ xuống [TB].
- Cơ sở tính chưa tách: phí giao dịch tính trên Rev (bỏ ship khách trả vì coi là thu hộ); TikTok gồm cả trợ giá sàn → công cụ chưa có tham số trợ giá sàn. Doanh thu tính thuế chưa trừ phần đồng tài trợ mã của shop (40%).
- Shopee: phí hạ tầng có thu khi "Trả hàng & Hoàn tiền" không — CHƯA XÁC MINH (đang không tính, theo công thức gốc). TikTok: 3.000đ mất khi hoàn (bảng phí ghi rõ) → đã cộng vào chi phí đơn hoàn — **khác công thức gốc**, chỉ ảnh hưởng TikTok.
- TikTok: phí ship trả hàng shop chịu chưa có trong bảng → mặc định 0đ + cảnh báo; nên nhập `--ship-tra-hang`.
- So sánh affiliate: tỷ lệ hoa hồng nhận và thuế khấu trừ trên thu nhập affiliate **không có trong bảng phí** → người dùng tự nhập, mặc định thuế 0% + cảnh báo CHƯA XÁC MINH.
- Chưa xử lý: SPayLater, PiShip, giảm phí giao dịch theo ads take rate TikTok, Mall, nhiều SKU / đơn, trần 50.000đ tính theo từng sản phẩm (công cụ coi 1 đơn = 1 sản phẩm).
- Chưa dùng `packages/schema` (chưa tồn tại). Chưa kiểm trên Windows (chỉ Linux, Python 3.13; mã dùng cú pháp ≥ 3.10).

## 5. Khó khăn cần quyết định
- **Chủ dự án:** tải PDF phí cố định ngành cấp 3 cho SKU định bán → nhập `--phi-nganh` (bỏ cảnh báo khoảng).
- **Chủ dự án:** kiểm phí hạ tầng 3.000đ trên Kênh Người Bán khi có shop; nếu chỉ Mall → P4 sửa bảng phí v2.
- **KTS / Tổng quản:** có giữ mặc định `cao` không (đề xuất giữ — thận trọng) và có chuẩn hóa định nghĩa "biên ròng = LN / doanh thu đơn" không.
- **Chủ dự án:** duyệt luật đề xuất ở `p4-tai-chinh.md` mục 8.3 (SKU có CM < 15% hoặc < 15.000đ không chạy quảng cáo) — công cụ đã in đủ số để áp.

## 6. Kế hoạch tiếp theo + tiền dự kiến chi
Bảng phí v2 (phiên bản 2027 khi sàn thông báo GTGT; thêm lịch sử TikTok, phí ship trả TikTok); hàm nhiều SKU / đơn; nối `packages/schema` khi P9 có. Tiền dự kiến: **0 đ**.

## 7. Đề xuất
Cho P1 gọi `--json` để chấm điểm SKU ứng viên theo lợi nhuận ròng và ROAS hòa vốn · lợi ích: loại sớm SKU lỗ · công sức: nhỏ · rủi ro: số đầu vào giả định bị hiểu nhầm là thật (đã có dòng cảnh báo).

## 8. Tự chấm (KTS chấm lại độc lập)
| Tiêu chí | Điểm |
|---|---|
| Đúng yêu cầu (25%) | 9 |
| Bằng chứng & nguồn (25%) | 8,5 (mọi phí từ bảng có nguồn; giả định ghi rõ) |
| Độ tin cậy kỹ thuật (20%) | 8,5 (33 kiểm thử, kiểm ngược khớp; chưa thử Windows) |
| Chi phí & thời gian (15%) | 9 |
| Rủi ro & tuân thủ (15%) | 9 (không bí mật, không dữ liệu thật, không gửi ra ngoài) |
| **Tổng** | **≈ 8,8** |

*Không phải tư vấn thuế. Số ví dụ là GIẢ ĐỊNH — không phải khuyến nghị đầu tư / không đảm bảo lợi nhuận.*
