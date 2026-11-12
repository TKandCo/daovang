# packages/core — lõi dùng chung tối thiểu (Đợt 0)

Chỉ thư viện chuẩn Python 3.10+. Ba việc:

1. **Cấu hình** — `doc_cau_hinh("cau-hinh.json", mac_dinh={...})`: đọc tệp JSON *không bí mật*, ghi đè bằng biến
   môi trường `DAOVANG_<TÊN_IN_HOA>` (ví dụ `DAOVANG_SO_NGAY=30`). Tệp có tên khóa giống bí mật (`key`, `token`,
   `secret`, `password`, `mat_khau`, `khoa`) → báo lỗi, không đọc.
2. **Khóa bí mật** — `lay_khoa("TEN_BIEN")`: chỉ đọc từ biến môi trường / cài đặt môi trường cloud. Thiếu → lỗi
   `ThieuKhoa` hướng dẫn bằng tiếng Việt, không in giá trị.
3. **Nhật ký che dữ liệu khách** — `log = tao_nhat_ky("p3")`: tự che số điện thoại VN → `[SDT]`, email → `[EMAIL]`,
   dãy 9–19 chữ số (CCCD, số tài khoản) → `[SO-DAI]`, token phổ biến → `[KHOA]`; trường tên `sdt, email, dia_chi,
   ho_ten, cccd, so_tai_khoan, token…` (trong dict hoặc `extra=`) → `[CHE]`. Hàm `che(chuoi)` dùng riêng được.

```python
import sys; sys.path.insert(0, "packages/core")
from daovang_core import tao_nhat_ky, lay_khoa
log = tao_nhat_ky("thu")
log.info("khach goi 0912345678")   # -> khach goi [SDT]
```

Giới hạn đã biết: KHÔNG nhận ra họ tên hay địa chỉ viết tự do trong câu (chỉ che khi nằm trong trường có tên
nhạy cảm) → quy ước: không bao giờ đưa tên / địa chỉ khách vào chuỗi nhật ký. Dấu thời gian Unix 10 chữ số cũng bị che.

Kiểm thử: `python3 -m unittest discover -s packages/core/tests`
