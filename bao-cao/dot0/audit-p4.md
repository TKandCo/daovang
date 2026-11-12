# Audit KTS — P4 Tài chính, Đợt 0 (12/11/2026)

Người kiểm: KTS trưởng (cùng mô hình với Tổng quản — không độc lập tuyệt đối; chủ dự án nên kiểm chọn mẫu). Không phải tư vấn thuế.

## Đã kiểm trực tiếp (đối chiếu bằng tìm kiếm riêng, 3 khẳng định)
| Khẳng định trong báo cáo P4 | Kết quả đối chiếu | Ghi chú |
|---|---|---|
| TikTok Shop hoa hồng mặc định 14% cho nhà bán thường từ 03/07/2026 | KHỚP (BSS Commerce, BigSeller dẫn Seller Center) | Mức thực tế khác theo ngành; Mall 16% từ 03/08/2026; VnExpress nói một số ngành tăng / giảm 0,5–3% |
| Shopee Voucher Xtra 5,5% (tối đa 50.000 đ/sản phẩm) từ 23/05/2026 | KHỚP (Sapo, Tuổi Trẻ) | BigSeller bản 01/05/2026 còn ghi 4% — bản cũ hơn |
| Shopee phí hạ tầng 3.000 đ/đơn | KHỚP về mức (Sapo, Báo Pháp Luật) | Một nguồn (ai-hay) nói chỉ áp dụng Shopee Mall — mâu thuẫn, kiểm trên Kênh Người Bán |

## Nhận xét
- Điểm mạnh: phần lớn số phí lấy từ trang / PDF chính thức của sàn; bảng phí 79 dòng có ngày hiệu lực + nguồn; công thức lợi nhuận ròng và ROAS hòa vốn có ví dụ GIẢ ĐỊNH; liệt kê 10 mâu thuẫn nguồn và 10 câu hỏi cho kế toán.
- Điểm yếu: chưa đọc được bản gốc NĐ 141/2026, 68/2026, TT 18/2026, 152/2025 (thuế chỉ ở mức [TB]); phí cố định Shopee mới có cấp ngành 1–2; tỷ lệ hoàn trả CHƯA XÁC MINH; bảng CSV viết không dấu.
- Rủi ro cần nhớ: GTGT 8% trên phí sàn chỉ đến hết 12/2026 → bảng phí phải có phiên bản 2027.

## Điểm (bang-cham-diem.md)
| Tiêu chí | Điểm |
|---|---|
| Đúng yêu cầu (25%) | 9 |
| Bằng chứng & nguồn (25%) | 8 |
| Độ tin cậy kỹ thuật (20%) | 7,5 (bảng dùng được, chưa có công cụ — phòng P4 cloud đang làm) |
| Chi phí & thời gian (15%) | 8 |
| Rủi ro & tuân thủ (15%) | 9 |
| **Tổng** | **≈ 8,3 — đạt** |

## Việc phải sửa / làm tiếp
1. P4 (cloud): công cụ `apps/finance/` đọc được `bang-phi-v1.csv`; ghi chú mâu thuẫn "phí hạ tầng chỉ Mall?".
2. Chủ dự án: tải PDF phí cố định cấp 3 ngành định bán từ Kênh Người Bán; mang 10 câu hỏi (mục cuối `p4-tai-chinh.md`) đi hỏi kế toán / chi cục thuế.

## Đính chính audit P1
Audit P1 hạ "Shopee miễn phí cố định 30 ngày cho shop mới" xuống [THẤP]. P4 tìm thấy trên trang chính thức: shop có sản phẩm đầu tiên đăng từ 01/11/2026 được miễn phí cố định 30 ngày, tối đa 200 đơn [CAO theo P4]. KTS chấm P1 hơi chặt ở điểm này; điểm P1 giữ nguyên ≈ 7,4 vì các điểm yếu khác vẫn đúng.
