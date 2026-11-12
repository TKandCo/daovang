# Tài chính P4 — máy tính mỗi đơn, affiliate, dropship, sổ lãi lỗ (Đào Vàng)

Tính lợi nhuận ròng một đơn bán trên **Shopee** hoặc **TikTok Shop**, đọc phí từ `bao-cao/dot0/bang-phi-v1.csv`.
Chỉ cần Python 3.10+ (không cài thêm gì). Không đọc / không gửi dữ liệu ra ngoài.

> Số bạn nhập (giá vốn, giá bán, tỷ lệ hoàn, quảng cáo…) là GIẢ ĐỊNH. **Không phải khuyến nghị đầu tư / không đảm bảo lợi nhuận.**

## Chạy kiểm thử (một lệnh, đứng ở thư mục gốc repo)

```bash
python3 -m unittest discover -s apps/finance -t apps/finance -v
```

Kết quả đúng: dòng cuối là `OK`.

## Kiểm ngược 3 ví dụ trong báo cáo P4

```bash
cd apps/finance && python3 -m taichinh.kiem_nguoc
```

## Tính một đơn

Đứng trong thư mục `apps/finance`:

```bash
python3 -m taichinh --san shopee --nganh "Sac dep" --gia-ban 250000 --voucher-shop 25000 --gia-von 95000 --dong-goi 3500 --ty-le-hoan 5 --quang-cao 10
```

Xem tên ngành có trong bảng phí (gõ không dấu, gõ một phần tên cũng được nếu không trùng):

```bash
python3 -m taichinh --san shopee --liet-ke-nganh
```

### Các tham số chính
| Tham số | Ý nghĩa | Mặc định |
|---|---|---|
| `--san` | `shopee` hoặc `tiktok` | bắt buộc |
| `--nganh` | ngành trong bảng phí (TikTok bỏ trống = mức mặc định 14%) | bắt buộc với Shopee |
| `--gia-ban`, `--gia-von` | giá niêm yết, giá vốn (đ) | bắt buộc |
| `--ngay-ban` | YYYY-MM-DD; chọn mức phí đúng ngày hiệu lực | hôm nay |
| `--voucher-shop` | giảm giá / mã do shop chịu (đ) | 0 |
| `--dong-goi`, `--ship-shop-chiu` | đóng gói; ship shop chịu thêm (đ) | 0 |
| `--voucher-san` | có tham gia Voucher Xtra (Shopee 5,5%) / VXP (TikTok 5%), trần 50.000đ/sp | không |
| `--aff-shop-tra` | % hoa hồng shop trả cho affiliate / creator | 0 |
| `--quang-cao` | % doanh thu chi quảng cáo | 0 |
| `--ty-le-hoan`, `--ship-tra-hang`, `--hong-hang-hoan` | % đơn trả hàng; ship trả shop chịu (đ); % hàng hoàn hỏng | 0; trần bảng phí (Shopee 40.000đ); 30% |
| `--thue-gtgt`, `--thue-tncn` | % thuế sàn khấu trừ | 1 và 0,5 (bảng phí) |
| `--muc thap\|giua\|cao` | chọn mức khi bảng phí ghi khoảng (vd. 13.5-16.5) | `cao` (thận trọng) |
| `--phi-nganh` | ghi đè % phí ngành nếu đã tra PDF ngành cấp 3 | — |
| `--shop-moi` | Shopee: miễn phí cố định shop mới (30 ngày / 200 đơn) | không |
| `--bo-phi-ha-tang` | Shopee: bỏ 3.000đ phí hạ tầng (kịch bản "chỉ Mall thu", chưa xác minh) | không |
| `--aff-nhan`, `--thue-aff` | % hoa hồng bạn NHẬN nếu làm affiliate → so sánh với nhập trực tiếp | — |
| `--json` | in JSON (cho công cụ khác đọc) | — |

### Đầu ra
Lợi nhuận ròng / đơn, biên ròng (trên doanh thu đơn), giá bán hòa vốn (có / không quảng cáo), ROAS hòa vốn,
so sánh nhập trực tiếp vs affiliate, danh sách **CẢNH BÁO** (mức khoảng, nguồn chưa chắc, phí hạ tầng chỉ Mall?,
GTGT phí sàn sau 31/12/2026…) và dòng "không đảm bảo lợi nhuận". Mỗi khoản phí ghi nguồn, độ tin cậy, ngày hiệu lực.

## Công thức (theo `bao-cao/dot0/p4-tai-chinh.md` mục 5)
- `Rev = giá bán − voucher shop`
- `CM = Rev − giá vốn − đóng gói − ship shop chịu − phí ngành·Rev − phí giao dịch·Rev − phí mỗi đơn − min(voucher sàn·Rev, 50.000) − affiliate·Rev − thuế khấu trừ·Rev`
- `LN trước QC = (1 − r)·CM − r·(đóng gói + ship shop chịu + ship trả hàng + d·giá vốn [+ 3.000đ với TikTok])`
- `LN = LN trước QC − quảng cáo%·Rev` · `Biên ròng = LN / Rev` · `ROAS hòa vốn = Rev / LN trước QC`
- Giá hòa vốn: giá niêm yết làm `LN = 0` (giữ nguyên voucher shop và các tỷ lệ), tìm bằng chia đôi.
- Affiliate: `hoa hồng kỳ vọng = (1 − r)·tỷ lệ nhận·Rev·(1 − thuế aff)`, trừ cùng chi phí quảng cáo; vốn hàng = 0.

## Đợt 1: affiliate · dropship · sổ lãi lỗ · kịch bản (đứng trong `apps/finance`)

### Affiliate — `taichinh/affiliate.py`
`thực nhận = hoa hồng × (1 − 0,98%) × (1 − 10% nếu khoản ≥ 250.000 đ) − chi phí nội dung`
(nguồn [CAO]: https://shopee.vn/blog/?p=190331, qua `bao-cao/dot0/p1-radar.md`).
- `thuc_nhan(hoa_hong_goc, chi_phi_noi_dung, san="shopee", nguong_tinh_tren="truoc_phi")` — một khoản thanh toán.
- `thuc_nhan_tu_don(gia_tri_don, ty_le_hoa_hong, so_don, ty_le_huy_hoan, chi_phi_noi_dung)` — gộp đơn một kỳ.
- Ngưỡng so với hoa hồng gốc (mặc định, thận trọng) hay sau phí: CHƯA XÁC MINH → tham số. Thuế 10% trừ trên TOÀN khoản.
- TikTok Affiliate: phí / thuế CHƯA XÁC MINH → dùng tạm luật Shopee + cảnh báo.

### Dropship — `taichinh/dropship.py`
- `tinh_dropship(DauVao(..., gia_von=giá NCC), phi_ncc, ty_le_huy, chi_phi_moi_don_huy, ngay_giao, loai_shop)`
  - phí NCC tính như đóng gói (mất cả khi hoàn); `LN mỗi đơn đặt = (1 − h)·LN − h·chi phí hủy` (mặc định chi phí hủy = phí NCC, GIẢ ĐỊNH).
  - `chi_ra_moi_don_dat` (trả NCC + quảng cáo lúc đặt), `tien_ve_moi_don_dat` (sàn trả sau phí, thuế, ship trả hàng).
- Chu kỳ tiền về [CAO, `bao-cao/dot0/p4-tai-chinh.md` §4]: Shopee ngày thứ 4 sau giao (+1 ngày rút); TikTok 8 ngày shop mới /
  3 ngày shop thường / 1 Mall / 15 rủi ro (+1 ngày rút).
- `von_ung_truoc(don_moi_ngay, chi_ra, tien_ve, ngay_tre)` — mô phỏng số dư theo ngày; ổn định: vốn cần = đơn/ngày × chi ra × ngày trễ.

### Sổ lãi lỗ cộng dồn — `taichinh/so_lai_lo.py` (đo cổng Đợt 1)
```bash
python3 -m taichinh.so_lai_lo --so du-lieu-mau/so-lai-lo-mau.csv --ngay-cuoi 2027-01-10
```
Cột: `ngay,thu_chi,loai,mo_hinh,kenh,so_tien_vnd,phan_bo_tu,phan_bo_den,mo_ta,nguon`. `mo_hinh` = affiliate / dropship / chung.
Gói công cụ trả trước → điền `phan_bo_tu/den` để rải đều theo ngày. In: lãi 4 tuần cuối (cổng), lãi từ đầu dự án, theo mô hình.
**Dữ liệu thật để NGOÀI repo** (vd. `du-lieu-that/` — đã có trong `.gitignore`); công cụ cảnh báo nếu sổ nằm trong repo ngoài `du-lieu-mau/`.

### Bảng 3 kịch bản 8 tuần — `taichinh/kich_ban.py`
```bash
python3 -m taichinh.kich_ban
```
Mọi số là GIẢ ĐỊNH (ghi ở đầu tệp); in lãi từng tuần, lãi 4 tuần cuối → cổng, điểm hòa vốn theo số đơn.

### Tệp kiểm khớp cho P9 — `vi-du-kiem-khop.json`
```bash
python3 -m taichinh.vi_du_kiem_khop          # sinh lại tệp
python3 -m taichinh.vi_du_kiem_khop --kiem   # so tệp với mã hiện tại
```
18 ví dụ (`loai`: don · dropship · affiliate · affiliate_tu_don · von_ung_truoc · so_lai_lo). Ví dụ `don` / `dropship` có
`phi_ap_dung` (mức phí đã tra) để bản JS kiểm CÔNG THỨC không cần đọc CSV. Tên khóa `dau_vao` = tên trường `DauVao`.
Dung sai trong khóa `dung_sai`. Tỷ lệ đầu ra (`bien_rong`, `ty_le_phi_*`) là phân số.

### Nhãn phí (P12 2.2)
Đầu ra có `ty_le_phi_san_aff_chua_thue` (phí sàn + affiliate, **chưa gồm thuế khấu trừ**) và `ty_le_phi_gom_thue_khau_tru`.

## Cấu trúc
- `taichinh/bang_phi.py` — đọc CSV, tách mức dạng khoảng / trần, chọn dòng theo ngày; mức "Truoc dd/mm/yyyy: x" trong ghi chú được dựng thành phiên bản cũ.
- `taichinh/tinh_loi_nhuan.py` — công thức, cảnh báo.
- `taichinh/__main__.py` — dòng lệnh. `taichinh/kiem_nguoc.py` — tái tạo 3 ví dụ báo cáo.
- `taichinh/affiliate.py`, `dropship.py`, `so_lai_lo.py`, `kich_ban.py`, `vi_du_kiem_khop.py` — Đợt 1.
- `du-lieu-mau/` — CSV mẫu (GIẢ ĐỊNH). `tests/` — kiểm thử (`test_taichinh.py` Đợt 0, `test_dot1.py` Đợt 1).

Chưa dùng `packages/schema` (P9 chưa xây); tên trường sẽ đổi theo schema chung khi có.
