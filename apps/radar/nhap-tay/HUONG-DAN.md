# Ghi tay khi xem sàn — 4 nhóm đã chọn

Mở tệp `4-nhom.csv` bằng Google Sheets (điện thoại) hoặc Excel.
Mỗi sản phẩm bạn xem = **1 dòng**. Chỉ ghi những gì sàn hiện công khai. Không chắc thì **để trống**, đừng đoán.

## 4 nhóm
| Mã | Nhóm | Tìm trên sàn bằng từ |
|---|---|---|
| N18 | Phụ kiện thú cưng | vòng cổ chó mèo, dây dắt, bát ăn, lược chải |
| N01 | Hộp / khay nhựa sắp xếp | khay xếp chồng, hộp chia ngăn |
| N02 | Móc treo / tôn lỗ | bảng tôn lỗ, móc dán tường |
| N05 | Dụng cụ vệ sinh nhà | cây lau nhà, chổi, khăn microfiber |

Không ghi: thức ăn / thuốc thú cưng, hóa chất tẩy rửa, hộp quảng cáo "đựng thực phẩm".

## Các cột (★ = bắt buộc)
| Cột | Ghi gì | Ví dụ |
|---|---|---|
| ★ `nhom_id` | Mã nhóm ở bảng trên | `N18` |
| ★ `san` | `shopee` hoặc `tiktok` | `shopee` |
| ★ `ngay_xem` | Ngày bạn xem | `2026-11-12` |
| ★ `ten_san_pham` | Tên ngắn | `Vòng cổ mèo có chuông` |
| ★ `link` | Bấm **Chia sẻ → Sao chép liên kết**, dán vào | `https://shopee.vn/...` |
| ★ `gia_ban_vnd` | Giá đang bán | `35.000` |
| `da_ban` | Số "Đã bán" sàn hiện | `1,2k` |
| `so_sao` | Số sao | `4,8` |
| `hoa_hong_pct` | % hoa hồng nếu thấy trong **Shopee Affiliate** / TikTok Affiliate | `10` |
| `gia_nhap_vnd` | Giá nhà cung cấp dropship báo (gồm ship tới khách) | `18.000` |
| `ghi_chu` | Gì cũng được | `nhiều shop bán cùng ảnh` |

Mỗi nhóm cố gắng **5–10 dòng**, ở cả hai sàn nếu được.

## Không được
- Không ghi tên / SĐT / địa chỉ khách, không ghi mật khẩu, số tài khoản.
- Không dùng phần mềm tự chép dữ liệu sàn. Chỉ xem và gõ tay.

## Ghi xong
Lưu dạng **CSV UTF-8**, gửi lại tệp (hoặc nhắn P1). P1 chạy:
```bash
python3 apps/radar/kiem_tra.py
```
```bash
python3 apps/radar/cham_diem.py
```
Máy sẽ tính cho từng dòng: **affiliate** (tiền hoa hồng thực nhận sau phí 0,98% + thuế 10%)
và **dropship** (lãi sau phí sàn theo ngành, có / không voucher). Đây là ước tính, không đảm bảo lợi nhuận.
