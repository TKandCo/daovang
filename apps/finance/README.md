# Máy tính lợi nhuận mỗi đơn (P4 — Đào Vàng)

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

## Cấu trúc
- `taichinh/bang_phi.py` — đọc CSV, tách mức dạng khoảng / trần, chọn dòng theo ngày; mức "Truoc dd/mm/yyyy: x" trong ghi chú được dựng thành phiên bản cũ.
- `taichinh/tinh_loi_nhuan.py` — công thức, cảnh báo.
- `taichinh/__main__.py` — dòng lệnh. `taichinh/kiem_nguoc.py` — tái tạo 3 ví dụ báo cáo.
- `tests/` — kiểm thử.

Chưa dùng `packages/schema` (P9 chưa xây); tên trường sẽ đổi theo schema chung khi có.
