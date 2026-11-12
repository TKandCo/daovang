# Radar sản phẩm v1 (thủ công) — Phòng P1

Bộ bảng CSV để **ghi tay** sản phẩm ứng viên, nhà cung cấp, giá, tín hiệu xu hướng và chấm điểm 100.
Mở bằng Excel / Google Sheets / LibreOffice (lưu lại dạng **CSV UTF-8**). Không cần lập trình.

**Không cào sàn, không tạo tài khoản, không vượt CAPTCHA.** Chỉ ghi số từ: shop của bạn, báo cáo công khai,
công cụ trả phí bạn đã mua (tính năng xuất file chính thức), chương trình affiliate, Google Trends xem tay.
Không ghi mật khẩu, khóa API, số tài khoản, thông tin khách hàng vào bất kỳ bảng nào.

## Thư mục
| Thư mục | Nội dung |
|---|---|
| `mau/` | 9 bảng mẫu (chỉ có dòng tiêu đề) — chép ra rồi điền |
| `du-lieu/source.csv` | Danh sách nguồn (mỗi nguồn một mã `S..`) — mọi bảng khác trỏ về đây |
| `du-lieu/nhom-ung-vien.csv` | 20 nhóm sản phẩm ứng viên Mức A, điểm sơ bộ (xem `bao-cao/dot0/p1-radar-v2.md`) |
| `kiem_tra.py` | Script kiểm: đúng cột, không ô nguồn trống, điểm hợp lệ, phí trỏ đúng bảng phí |
| `test_kiem_tra.py` | Kiểm thử cho script trên |

## Quy tắc chung khi điền
1. **Mỗi dòng phải có `source_id` + `captured_at`** (ngày bạn ghi, dạng `2026-11-12`). Nhiều nguồn: cách nhau bằng `;` (vd `S03;S10`).
2. Nguồn mới → thêm một dòng vào `du-lieu/source.csv` trước: mã, tên, loại, **link**, ngày đăng, độ tin cậy.
3. Độ tin cậy chỉ dùng: `CAO` (chính thức) · `TB` (nhiều nguồn khớp) · `THAP` (một nguồn / mâu thuẫn) · `CHUA_XAC_MINH`.
4. Chưa có số → ghi `CHƯA ĐO` (ở cột điểm) hoặc để trống ô số liệu — **không đoán**. Số tự giả định ghi chữ "GIẢ ĐỊNH" ở cột ghi chú.
5. Phí sàn: KHÔNG tự gõ. Ghi `fee_ref` = `sàn|loại phí|ngành` đúng như một dòng trong `bao-cao/dot0/bang-phi-v1.csv`
   (vd `Shopee|phi_co_dinh|Van phong pham`). Script sẽ báo nếu gõ sai.
6. Lưu tệp dạng CSV UTF-8, giữ nguyên dòng tiêu đề.

## Từng bảng (cột chính)
| Bảng | Dùng để | Cột cần chú ý |
|---|---|---|
| `source` | Danh sách nguồn | `type` (chỉ dùng): paid_tool / google_trends / platform_public / affiliate / manual / bao_chi_dan_metric / metric_cong_khai / metric_ereport / san_tu_cong_bo / blog_ban_hang / noi_bo; `export_method`: chep_tay / xem_tay / xuat_file / api / doc_tep / nhap_tay; `url`: link, hoặc đường dẫn tệp trong repo (vd `bao-cao/dot0/p8-phap-ly.md`) cho nguồn nội bộ; `license_note`: có được phép dùng không |
| `product` | Một sản phẩm "khái niệm" (không phải link shop) | `regulated_flag` (CO/KHONG — ngành có điều kiện), `ip_risk_flag` (CO/KHONG — nghi nhái), `model`: nhap / affiliate / dropship / ca_hai (script chặn giá trị khác) |
| `supplier` | Nhà cung cấp | `type`: cho_si / nha_phan_phoi / forwarder_1688 / dropship; `docs_available`: có hóa đơn CO/KHONG; `public_contact_note`: chỉ kênh công khai của doanh nghiệp, không ghi tài khoản/mật khẩu |
| `supplier_quote` | Báo giá | `unit_cost_vnd`, `ship_cost_per_unit_vnd`, `quoted_at`, `valid_until` |
| `listing_price` | Giá bán đối thủ (xem tay) | `shop_ref`: tên shop công khai; `sold_est_30d`: số ước tính từ công cụ — ghi rõ nguồn |
| `trend_signal` | Tín hiệu xu hướng (dạng dọc) | `metric`: sales_30d / growth_3m / search_index / nganh_growth_yoy…; `period_start`, `period_end` |
| `score` | Chấm điểm một sản phẩm | 7 cột điểm + `total` + `fee_ref` + `decision` (nhap_thu / theo_doi / affiliate_truoc / bo) |
| `trial_batch` | Lô thử | `cost_total_usd` **≤ 300**; `owner_approved` phải là `CO` (chủ dự án đã duyệt) — script chặn nếu sai |
| `affiliate_item` | Sản phẩm bán affiliate | `commission_rate_pct` ghi đúng như trang affiliate hiển thị, kèm nguồn + ngày |

## Chấm điểm 100 (từ mục 5 `bao-cao/dot0/p1-radar.md`)
| Tiêu chí | Tối đa | Cách chấm |
|---|---|---|
| Nhu cầu (`demand`) | 20 | ≥ 2 nguồn khớp về doanh số 30 ngày / đà tăng 3 tháng / Google Trends: 15–20; chỉ 1 nguồn: tối đa 10 |
| Cạnh tranh (`competition`) | 15 | Ít shop, top 3 không chiếm > 60%, giá chưa bị đạp, có chỗ khác biệt → cao |
| Biên sau phí (`margin`) | 25 | Biên ròng ≥ 20% = 25; 12–20% = 15; 8–12% = 8; < 8% = 0 **và loại**. Phí lấy từ `bang-phi-v1.csv` qua `fee_ref` |
| Pháp lý (`legal`) | 15 | Thuộc ngành có điều kiện mà chưa có giấy tờ → 0 **và loại** (xem `p8-phap-ly.md`) |
| Hoàn trả (`returns`) | 10 | Dễ vỡ, sai cỡ, hỏng → thấp |
| Mùa vụ (`season`) | 5 | Quanh năm 5; còn ≥ 6 tuần trước đỉnh 3; qua đỉnh 0 |
| Video (`video`) | 10 | Dễ trình diễn ≤ 30 giây, có trước/sau → cao |

Ngưỡng: **≥ 70** đề xuất nhập thử (chủ dự án duyệt) · **55–69** theo dõi / thử affiliate trước · **< 55** bỏ.
Loại ngay không tính điểm: biên ròng < 8%, thiếu giấy tờ ngành điều kiện, nghi hàng nhái.

### Tính biên (cột `margin_note` ghi cách tính)
Biên ròng = (giá bán − giá vốn − ship nhập − phí cố định − phí giao dịch − phí đơn − quảng cáo − dự phòng hoàn − thuế) / giá bán.
- Phí cố định / hoa hồng / phí giao dịch / phí đơn: lấy đúng dòng trong `bang-phi-v1.csv` (P4). Shopee người bán mới được **miễn phí cố định 30 ngày,
  tối đa 200 đơn** nếu sản phẩm đầu tiên đăng từ 01/11/2026 (bảng phí dòng `uu_dai_nguoi_ban_moi`, [CAO theo P4]) — chỉ dùng cho kịch bản 30 ngày đầu,
  KHÔNG dùng để chấm điểm dài hạn.
- Hoa hồng TikTok theo từng ngành: chủ dự án đối chiếu Seller Center trước khi chốt (audit KTS 12/11/2026).
- Quảng cáo, hoàn trả, thuế: chưa có số thật → ghi "GIẢ ĐỊNH" + mức dùng.

### Điểm sơ bộ cấp NHÓM (bảng `nhom-ung-vien.csv`)
Nhóm chưa có sản phẩm / báo giá cụ thể nên chỉ chấm được 3 tiêu chí (tối đa 45); 4 tiêu chí còn lại ghi `CHƯA ĐO` (55 điểm).
- Nhu cầu cấp nhóm, tối đa 10 (vì số chỉ ở cấp ngành, gốc dữ liệu chủ yếu là Metric):
  ngành mạnh (top doanh số hoặc tăng ≥ 30%) có ≥ 2 nguồn **+6** / 1 nguồn **+4** / chỉ nhận định định tính **+2** / không có **0**;
  cộng số riêng của nhóm: ≤ 12 tháng **+4** / cũ hơn hoặc chỉ tiêu đề **+2** / không có **0**.
- Pháp lý cấp nhóm: ngoài nhóm có điều kiện theo P8 **10** (chưa 15 vì chưa kiểm hóa đơn / nhãn / nhái từng sản phẩm); còn vướng quy định CHƯA XÁC MINH **6**.
- Video: đánh giá chủ quan của P1 (nguồn `S21`, độ tin cậy THẤP).
- Độ tin cậy của nhóm = mức **thấp nhất** trong các nguồn dữ liệu của nhóm (không tính nguồn nội bộ `noi_bo`); nhóm chỉ có nguồn nội bộ thì `CHUA_XAC_MINH` và điểm nhu cầu phải là 0.
- Script chặn: `demand` cấp nhóm > 10, `legal` khác 6 / 10, `fee_ref` trống, `mo_hinh` lạ, ngày không có thật, `do_tin_cay` cao hơn nguồn.
Điểm sơ bộ chỉ để XẾP THỨ TỰ nhóm nào đáng tìm sản phẩm trước — không phải điểm quyết định nhập.

## Kiểm trước khi gửi
```bash
python3 apps/radar/kiem_tra.py
```
```bash
python3 -m unittest apps/radar/test_kiem_tra.py
```
Phải in `ĐẠT` và `OK`. Nếu báo lỗi: sửa đúng dòng được nêu.

Không phải khuyến nghị đầu tư / không đảm bảo lợi nhuận. Mọi ngưỡng trên là giả định khởi điểm, chỉnh sau lô thử đầu.
