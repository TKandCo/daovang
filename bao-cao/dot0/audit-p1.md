# Audit KTS — P1 Radar, Đợt 0 (12/11/2026)

Người kiểm: KTS trưởng (cùng mô hình với Tổng quản — không độc lập tuyệt đối; chủ dự án nên kiểm chọn mẫu).

## Đã kiểm trực tiếp (đối chiếu độc lập bằng tìm kiếm riêng, 3 khẳng định)
| Khẳng định trong báo cáo P1 | Kết quả đối chiếu | Ghi chú |
|---|---|---|
| Luật TMĐT 2025 (122/2025/QH15) hiệu lực 01/07/2026 | KHỚP — nhiều nguồn (thuvienphapluat, luatvietnam, VnEconomy) | Số điều không thống nhất (41 hay 42); chưa đối chiếu văn bản gốc |
| TikTok Shop tăng phí từ 09/05/2026 | KHỚP về ngày (VCCI 04/05/2026); phí giao dịch 5% → 6% có nguồn | |
| TikTok hoa hồng "thời trang 14,6→16,1%; mẹ & bé 14,5→17,8%" | KHÔNG XÁC NHẬN được con số cụ thể. 17,8% có xuất hiện nhưng gắn với nhóm Mall, không tách ngành mẹ & bé | Hạ độ tin cậy xuống [THẤP]; không đưa vào bảng phí cho tới khi lấy từ Seller Center |
| Shopee "miễn phí cố định 30 ngày đầu" cho shop mới | CHỈ 1 NGUỒN (VCCI 16/05/2026); khác với ưu đãi khác tìm được (giảm 50% phí cố định 01/06–31/08/2026, đã hết hạn) | [THẤP]; kiểm tra Kênh Người Bán |

## Nhận xét
- Điểm mạnh: ghi rõ nhãn độ tin cậy, thừa nhận không đọc được trang chính thức của Shopee Open Platform / TikTok Partner Center, không đề xuất cào dữ liệu; khung chấm điểm và kiến trúc dữ liệu dùng được.
- Điểm yếu: một số con số phí chưa có nguồn chính thức; nhiều mục API / chatbot dừng ở [THẤP] / CHƯA XÁC MINH (đúng thực tế nhưng chưa đủ để quyết định xây trợ lý chốt đơn).
- Chưa kiểm: giá Metric / Kalodata / FastMoss; điều kiện API Shopee VN cho hộ kinh doanh; điều kiện đăng ký TikTok Partner Center ở Việt Nam. Ba việc này chủ dự án phải tự hỏi sàn / nhà cung cấp.

## Điểm (bang-cham-diem.md)
| Tiêu chí | Điểm |
|---|---|
| Đúng yêu cầu (25%) | 8 |
| Bằng chứng & nguồn (25%) | 6,5 |
| Độ tin cậy kỹ thuật (20%) | 7 (chỉ thiết kế, chưa có mã) |
| Chi phí & thời gian (15%) | 8 |
| Rủi ro & tuân thủ (15%) | 8 |
| **Tổng** | **≈ 7,4 — cần sửa nhỏ** |

## Việc phải sửa
1. P1: hạ các con số hoa hồng TikTok / miễn phí cố định Shopee xuống [THẤP] trong báo cáo; chờ P4 có bảng phí chính thức rồi mới dùng trong chấm điểm biên lợi nhuận.
2. Chủ dự án (tự làm): hỏi giá Metric; xem điều kiện đăng ký API của hai sàn; chụp bảng phí cố định từ Kênh Người Bán.
