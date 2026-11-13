# App Đào Vàng — một tệp HTML (`app/daovang.html`)

Mở trên điện thoại / máy tính, **không cần mạng, không cần máy chủ, không cài gì**. Bản đầu: **máy tính lợi nhuận mỗi đơn**
(Shopee / TikTok Shop) — cùng đầu vào, cùng kết quả với `python -m taichinh` của P4 (`apps/finance/`).

> Số bạn nhập là GIẢ ĐỊNH. **Không phải khuyến nghị đầu tư / không đảm bảo lợi nhuận.**

## Dùng
1. Chép tệp `app/daovang.html` vào điện thoại (Zalo gửi cho chính mình, Google Drive, cáp USB…).
2. Mở bằng trình duyệt (Chrome / Safari). Nhập giá bán, giá vốn… → kết quả hiện ngay, thanh dưới đáy luôn hiện lợi nhuận / đơn.
3. **Sổ SKU**: đặt tên rồi bấm *Lưu* để giữ phép tính của từng sản phẩm; bấm *Mở* để gọi lại.
4. **Sao lưu**: dữ liệu chỉ nằm trong trình duyệt của máy đó. Bấm *Tải bản sao lưu* định kỳ (tệp `.json`);
   đổi máy / lỡ xóa → *Nhập bản sao lưu*.

Không nhập tên, số điện thoại, địa chỉ khách vào app. App chặn mọi kết nối mạng (Content-Security-Policy).

## Sửa app (dành cho phòng P9)
- Mã nguồn: `app/src/khung.html` (bố cục), `app/src/taichinh.js` (lõi tính — chép 1:1 từ Python P4),
  `app/src/giao-dien.js` (ô nhập, lưu, sao lưu). **Không sửa `app/daovang.html` bằng tay.**
- Đóng gói lại sau mỗi lần sửa nguồn hoặc bảng phí: `python3 tools/dong-goi-app.py`
- Kiểm khớp với Python P4 (cần Node.js): `python3 tools/kiem-khop.py`
- Toàn bộ kiểm thử repo: `python3 tools/chay-kiem-thu.py`

Khi P4 đổi công thức trong `apps/finance/taichinh/tinh_loi_nhuan.py`, kiểm khớp sẽ HỎNG cho tới khi P9 sửa
`app/src/taichinh.js` theo — đó là chủ ý (app không được lặng lẽ tính khác Python).
