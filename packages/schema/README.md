# packages/schema — cấu trúc dữ liệu chung (bản 0.1.0, Đợt 0)

Mã: `daovang_schema/__init__.py` (chỉ thư viện chuẩn Python 3.10+). Mọi công cụ (P1 radar, P3 chốt đơn,
P4 tài chính, P5 kho…) dùng chung các kiểu dưới đây để ráp lại được.

## Quy ước chung
- **Tiền**: số nguyên VND (`..._vnd`). Không dùng số thực cho tiền.
- **Ngày**: `YYYY-MM-DD`.
- **Nguồn + ngày** (Quy tắc 5): mọi bản ghi có `nguon` (link / "nhap tay" / "xuat file Shopee") và `ngay_nguon`.
- **Độ tin cậy**: `CAO` · `TB` · `THAP` · `CHUA XAC MINH` (không dấu; `chuan_hoa_do_tin_cay("Thấp")` → `THAP`).
- `kiem_tra()` trả danh sách lỗi (rỗng = hợp lệ). `thanh_dict()` / `tu_dict()` để lưu JSON; trường lạ bị từ chối.

## Các kiểu
| Kiểu | Trường bắt buộc | Ghi chú |
|---|---|---|
| `SKU` | ma_sku, ten, gia_ban_vnd, gia_von_vnd, nguon, ngay_nguon | `nganh` khớp cột `nganh` bảng phí |
| `DonHang` + `DongDon` | ma_don, san, ngay_dat, trang_thai, dong, nguon, ngay_nguon | `tong_hang_vnd()` = Σ(SL×đơn giá − giảm giá người bán); `ma_khach` là mã ẩn danh |
| `Khach` | ma_khach, nguon, ngay_nguon | **Tối thiểu dữ liệu cá nhân**: chỉ mã ẩn danh, tỉnh/thành, số đơn, đồng ý nhận tin. `tu_dict` từ chối `ho_ten, sdt, email, dia_chi, cccd, so_tai_khoan…` |
| `NhaCungCap` | ma_ncc, ten, kenh, nguon, ngay_nguon | `hinh_thuc`: nhap_truc_tiep / affiliate / dropship / chua_ro |
| `Video` | ma_video, tieu_de, nguon, ngay_nguon | Báo lỗi nếu video AI rời trạng thái nháp mà chưa gắn nhãn, hoặc có người thật mà chưa có văn bản đồng ý (Quy tắc 6) |
| `DongBangPhi` | 9 cột đúng thứ tự của `bao-cao/dot0/bang-phi-v1.csv` | Giữ chuỗi nguyên văn; `khoang_muc()` đổi "13.5-16.5" → (13.5, 16.5), chữ → None; `ngay_nguon` lấy từ "(tra dd/mm/yyyy)" trong cột nguồn |

Đọc bảng phí: `doc_bang_phi("bao-cao/dot0/bang-phi-v1.csv")` — chịu được BOM, báo lỗi nếu cột lệch hoặc dòng thừa cột.

## Dùng thử
```bash
python3 -c "import sys; sys.path.insert(0,'packages/schema'); from daovang_schema import doc_bang_phi; print(len(doc_bang_phi('bao-cao/dot0/bang-phi-v1.csv')))"
```

## Kiểm thử
```bash
python3 -m unittest discover -s packages/schema/tests
```

## Mở rộng
Thêm trường **có giá trị mặc định** ở cuối kiểu → không phá công cụ cũ. Đổi / xóa trường → tăng `PHIEN_BAN`, qua PR riêng.
Theo `quy-trinh/van-hanh-cloud.md`, `packages/schema` do Tổng quản / KTS duyệt.
