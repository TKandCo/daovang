# Biên bản audit KTS vòng 2 — P1 Radar v1 (chép nguyên văn)

> P1 chép lại biên bản KTS trả về trong phiên cloud ngày 12/11/2026, không sửa nội dung. KTS ở phiên điều phối có thể chép sang tệp audit chính thức của KTS.
> Các việc P1 đã sửa theo biên bản này: xem `p1-radar-v2.md` mục 10. Một số nhận định trong biên bản (S25/S26 trùng URL; "2 triệu đơn áo dài" không tìm thấy; thú cưng 1.912,5) P1 đã kiểm lại và trả lời tại đó.

---

# Audit KTS vòng 2 — P1 Radar v1, nhánh `phong/p1-dot0` (12/11/2026)

Người kiểm: KTS trưởng (cùng mô hình với Tổng quản và P1, không độc lập tuyệt đối). Kiểm trực tiếp, không sửa tệp repo. Thử nghiệm hỏng dữ liệu làm trong thư mục tạm của phiên.

## 1. Phạm vi và an toàn
| Mục | Kết quả |
|---|---|
| `git diff origin/main --stat` | 17 tệp: `apps/radar/**` (14 tệp), `bao-cao/dot0/p1-cong-cu-so-lieu.md`, `p1-radar-v2.md`, `p1-radar.md`. KHÔNG sửa tệp phòng khác. ĐÚNG phạm vi. |
| Quét bí mật trong diff | Không có khóa, token, mật khẩu thật. Chỉ có số điện thoại và email công khai của Metric trên trang chính thức (`p1-cong-cu-so-lieu.md` dòng 48) và các dòng chữ hướng dẫn. |
| Tiền | Chưa chi đồng nào. Báo cáo ghi rõ mọi khoản vượt trần chờ chủ dự án duyệt. |
| PR | Chưa kiểm được qua `gh pr list` (GraphQL bị chặn, HTTP 403). `p1-radar-v2.md` chỉ ghi "link tạo PR" và "chủ dự án tạo PR". Chưa thấy dấu hiệu PR tự tạo. |
| Cào sàn / tạo tài khoản | Không thấy. `p1-cong-cu-so-lieu.md` mục 2 ghi dừng khi FastMoss chặn bằng bước kiểm tra chống bot, không vượt. ĐÚNG quy tắc 4. |

## 2. Sửa theo audit vòng 1: ĐÃ SỬA ĐÚNG
- Hoa hồng TikTok theo ngành (14,6→16,1%; 14,5→17,8%) đã hạ xuống [THẤP] và ghi "KHÔNG dùng để chấm điểm" (`p1-radar.md` mục 5).
- Mục Shopee miễn phí cố định đã cập nhật theo đính chính cuối `audit-p4.md` (phí cố định 30 ngày, tối đa 200 đơn, sản phẩm đầu tiên đăng từ 01/11/2026, không miễn 6% giao dịch và 3.000đ hạ tầng). Khớp dòng 42 `bang-phi-v1.csv`. P1 ghi rõ "[CAO theo P4], P1 chưa tự mở trang", trung thực.
- P1 tự phát hiện và sửa thêm ngày phí 6% (01/05 người bán thường, 08/05 Mall). Tốt.
- Còn sót tại `p1-radar.md` dòng 5: câu "trang giá của Kalodata/FastMoss/Metric không công khai giá" đã lỗi thời so với `p1-cong-cu-so-lieu.md`.

## 3. Chạy lại
- `python3 apps/radar/kiem_tra.py` → `ĐẠT — 11 tệp CSV đúng cột, không ô nguồn trống`.
- `python3 -m unittest apps/radar/test_kiem_tra.py` → 11 test, OK.

### Lỗ hổng của script (tôi tự thử, sửa bản sao trong thư mục tạm)
Tôi sửa `nhom-ung-vien.csv` bản sao rồi chạy `kiem_tat_ca`. Kết quả: script vẫn báo ĐẠT (không lỗi) ở cả 7 trường hợp:
| Trường hợp hỏng | Script |
|---|---|
| `source_id` chỉ là `;` (thực chất trống) | Không bắt |
| `source_id` chỉ là `S21` (tự đánh giá của P1, không có dữ liệu thật) | Không bắt |
| `mo_hinh` = `mua_dut` (ngoài danh sách nhap/affiliate/dropship/ca_hai) | Không bắt |
| N04 (pháp lý chưa xác minh) bị sửa `legal=15`, tổng sửa cho khớp | Không bắt |
| `captured_at` = `2026-13-45` (đúng dạng nhưng không phải ngày thật) | Không bắt |
| `fee_ref` để trống ở nhóm | Không bắt |
| `demand=20` ở cấp nhóm (quy tắc README: tối đa 10) | Không bắt |

Lỗ hổng khác đọc từ mã:
- Cột `do_tin_cay` của nhóm không bị ép khớp mức thấp nhất trong các nguồn trỏ tới.
- Cột `type` và `export_method` của `source` không được kiểm danh sách. `source.csv` đang dùng `metric_cong_khai`, `san_tu_cong_bo`, `metric_ereport`, `blog_ban_hang` mà README không liệt kê.
- Các bảng mẫu `mau/*.csv` chỉ có tiêu đề nên phần kiểm từng dòng (điểm, lô thử ≤ 300 USD, `owner_approved`) chưa chạy trên dữ liệu thật. Các test cho phần này tự ghi dòng giả để thử.
- Phát hiện thừa: `S25` và `S26` trỏ cùng một URL (blog FastMoss). `S19`, `S20`, `S21` trỏ `github.com/TKandCo/daovang/...`; `S21` trỏ nhánh `phong/p1-dot0`, sẽ gãy sau khi gộp hoặc xóa nhánh.
- `S18` và `S20`–`S26` không bảng nào tham chiếu. Chấp nhận được, nhưng `p1-radar-v2.md` mục 3 vẫn nói "21 dòng" trong khi `source.csv` có 26 dòng.
- Kết luận: "ĐẠT" chỉ chứng minh đúng định dạng, không chứng minh đúng nội dung. Báo cáo P1 đã tự thừa nhận điều này ở mục 4.

## 4. Dữ liệu thô: điểm sơ bộ và danh sách tránh của P8
Kiểm lại 12 nhóm theo quy tắc README mục "Điểm sơ bộ cấp NHÓM":
| Nhóm | Điểm nhu cầu kiểm lại | Kết quả |
|---|---|---|
| N01 | ngành ≥2 nguồn +6; số riêng 04/2024–03/2025 (cũ) +2 = 8 | KHỚP (tổng 26) |
| N02 | +6, số riêng kỳ không rõ +2 = 8 | KHỚP |
| N04 | +6, blog không ngày +2 = 8; pháp lý 6 vì tiếp xúc thực phẩm | KHỚP |
| N05, N06, N07, N13 | +6, không số riêng = 6 | KHỚP |
| N08, N09, N15, N16 | 1 nguồn +4, không số riêng = 4 | KHỚP |
| N14 | +6; số riêng 2 triệu đơn áo dài 01/2026 ≤12 tháng +4 = 10 | KHỚP với quy tắc. Số riêng KHÔNG xác minh được (xem mục 5). |
| N18 | +6; phụ kiện 481,1 tỷ Q3/2026 +4 = 10 | KHỚP (tổng 28) |
| N20 | 0; pháp lý 10; video 6 = 16 | KHỚP |

- Tổng điểm và `diem_toi_da_da_cham` đúng cho cả 20 dòng (script cũng kiểm).
- N10 điểm 6: S04 +4 và S17 (một thương hiệu) +2. Chấp nhận được nhưng đã nới hơn quy tắc ("số riêng của nhóm" nhưng S17 chỉ là một thương hiệu).
- Vi phạm danh sách tránh của P8: KHÔNG nhóm nào là mỹ phẩm, TPCN, đồ chơi trẻ em hay điện tử có pin/sạc. P1 còn tự loại thức ăn thú cưng, chất tẩy rửa, cát khử mùi, hộp đựng thực phẩm, Mẹ & Bé. Tốt.
- Vùng xám đã được P1 tự gắn cờ: N04 (dụng cụ bếp), N17 (ốp lưng in hình, nhãn hiệu tên dòng máy), N16 (giá đỡ laptop/điện thoại, `fee_ref` là ngành "Điện tử" nên cần tra lại), N15 (văn phòng phẩm, không gắn như đồ chơi).
- Mọi nhóm đều có nguồn + ngày + độ tin cậy; phần chưa đo ghi "CHƯA ĐO" đúng.
- Điểm yếu: nhóm xếp hạng chủ yếu dựa số cấp NGÀNH. Chênh điểm 2 đến 6 điểm trên thang 45, không đủ để phân biệt nhóm. P1 tự nói đúng điều này.

## 5. Đối chiếu nguồn độc lập (WebSearch ngày 12/11/2026)
Tôi kiểm 7 khẳng định. Số mẫu theo yêu cầu (≥ 5) đạt.
| # | Khẳng định | Nguồn trong repo | Kết quả |
|---|---|---|---|
| 1 | Metric Starter 4 tháng Advanced 8 triệu; 500 lượt 18 triệu; dùng thử 7 ngày | S22 | KHÔNG KIỂM ĐƯỢC. Tìm kiếm không ra trang giá của Metric. Số này chỉ có từ lần đọc của P1 bằng trình duyệt; tôi chưa tự mở được. Nên chủ dự án hoặc KTS mở `metric.vn/analytics/pricing` để xác nhận. Phép tính 8 triệu / 26.000 ≈ 308 USD đúng số học. |
| 2 | FastMoss Basic 49, Pro 89, Ultimate 139 USD/tháng; tháng đầu 29 USD | S25 [TB] | KHỚP MỘT PHẦN. Delzonic (ghi kiểm tháng 9/2026) và Pulse Signal khớp 49/89/139. SaaSWorthy ghi 59/299, TrustRadius ghi 59/109. Còn mâu thuẫn. "Tháng đầu 29 USD" không xác nhận được. Nên hạ [TB] → [THẤP]. S25 ghi nguồn "blog FastMoss + nolyn.ai" nhưng URL trong `source.csv` là blog Kalodata, lệch. |
| 3 | Nhà cửa–Đời sống Q1/2026 doanh số 18,2 nghìn tỷ, +32,17%, hạng 2 sản lượng, hạng 3 doanh số | S03 | KHỚP (BrandsVietnam tóm tắt báo cáo Metric). Tuy nhiên S03 ghi URL `metric.vn/insights/...`; nguồn tôi tìm ra là BrandsVietnam. Nên đổi URL cho đúng chỗ đã đọc. |
| 4 | Thú cưng Q3/2026 1.921,5 tỷ, +38,2% | S06, S08, S09 | KHÔNG KHỚP. Nguồn VietBao ghi 1.912,5 tỷ, "hơn 38%". P1 chọn 1.921,5 "theo đa số trích đoạn" nhưng tôi không tái hiện được số đó. Cần kiểm lại hoặc ghi cả hai số. |
| 5 | Phụ kiện thú cưng 481,1 tỷ; thức ăn 795 tỷ | S07 | KHỚP. |
| 6 | Số shop thú cưng giảm 9% | S08 | KHÔNG KHỚP. Nguồn tôi thấy ghi giảm 2,47% so với Q2 và giảm 10,68% so với cùng kỳ. Số "9%" không xác nhận được. Nhóm N18 dùng số này trong ghi chú cạnh tranh. |
| 7 | Phụ kiện thời trang +56,95% (sản lượng −3,15%); văn phòng phẩm +41,44% (−10,02%) | S04 [THẤP] | KHÔNG XÁC NHẬN. Tìm ra: hai nhóm doanh thu tăng, sản lượng giảm (đúng chiều), nhưng không thấy các con số. Giữ [THẤP], đúng nhãn. |
| 8 | CafeBiz: TikTok 34.600 tỷ vượt Shopee 33.100 tỷ (15/12/2025–25/01/2026) | S01 [TB] | KHỚP về hai số (nhiều báo khác dẫn). |
| 9 | "~2 triệu đơn áo dài tháng 1/2026" | S01, dùng cho N14 | KHÔNG KHỚP / không tìm được. Một bài khác ghi "3,4 triệu sản phẩm linh vật ngựa", áo dài "hàng trăm tỷ", không có số 2 triệu đơn. Số này đang làm N14 đứng đầu bảng (+4 điểm). Bỏ +4 thì N14 còn 24, ngang N03/N05. |
| 10 | S05: làm đẹp 49.507 tỷ, thời trang nữ 40.351 tỷ (H1/2026) | S05 | KHỚP. |

Tổng: kiểm 10 khẳng định, 4 KHỚP, 1 khớp một phần (FastMoss), 3 KHÔNG KHỚP/không tìm thấy (số thú cưng, số shop −9%, 2 triệu đơn áo dài), 1 KHÔNG XÁC NHẬN (S04), 1 KHÔNG KIỂM ĐƯỢC (giá Metric). Số mẫu kiểm đạt ≥ 20% (10 trên khoảng 40 khẳng định số).

## 6. Không bịa số? Chưa phát hiện bịa, nhưng có số chưa tái hiện được
- P1 nhiều lần ghi rõ "đọc qua trích đoạn tìm kiếm, chưa mở trang gốc"; giá FastMoss/Kalodata ghi mâu thuẫn trung thực. Điểm cộng.
- Hai số (1.921,5 tỷ và "2 triệu đơn áo dài") là các con số cụ thể mà tôi không tái hiện được. Đây là vấn đề "nguồn" chứ chưa kết luận là bịa; cần P1 cung cấp đúng đoạn trích.
- Báo cáo có mâu thuẫn nội bộ: `p1-radar-v2.md` mục 3 và mục 5 vẫn nói "mạng phiên cloud chặn metric.vn", trong khi `p1-cong-cu-so-lieu.md` nói đã mở mạng và đọc trang giá Metric. Cần thống nhất để người đọc biết số nào đọc trang gốc, số nào chỉ qua tìm kiếm.
- `p1-cong-cu-so-lieu.md` ghi họp KTS: "Công sức 9–10 giờ là ước tính của KTS". Đây là ước tính, không phải số đo; đã ghi "ƯỚC TÍNH" nên chấp nhận được. Nội dung họp KTS tôi không xác minh được vì không có biên bản gốc (KTS trong phiên đó là agent khác).

## 7. Điều tôi KHÔNG kiểm được và vì sao
- Trang giá Metric (S22, S23, S24): WebSearch không trả trang giá.
- Điều khoản dùng, xuất CSV của Starter, thời gian dùng thử thật: chưa ai đọc được; P1 đã ghi "chưa kiểm".
- Trang giá chính thức FastMoss, Kalodata: bị chặn, không vượt.
- Số trong eReport Metric (S11–S14): chỉ thấy tiêu đề, cần đăng nhập.
- PR: GraphQL bị chặn nên không liệt kê được.
- Chưa mở tệp thực tế của P4/P8 ngoài các dòng đã trích; chỉ đối chiếu `bang-phi-v1.csv` dòng 5, 6, 12, 42–44, 57 và `p8-phap-ly.md` dòng 17, 86.

## 8. Điểm (bang-cham-diem.md)
| Tiêu chí | Trọng số | Điểm | Ghi chú |
|---|---|---|---|
| Đúng yêu cầu | 25% | 8,5 | Đủ 4 hạng mục + tệp bổ sung; 9 bảng mẫu, README tiếng Việt, 20 nhóm, script ĐẠT; sửa theo audit đúng. Trừ vì báo cáo còn câu lỗi thời, số liệu "21 nguồn". |
| Bằng chứng & nguồn | 25% | 6,0 | Có link, ngày, độ tin cậy cho mọi số. Nhưng 3 số không tái hiện được, S04 không xác nhận, S25 gắn [TB] dù mâu thuẫn, giá Metric chưa kiểm độc lập. Số thị trường đa phần là bản chép lại từ báo, không phải trang gốc. |
| Độ tin cậy kỹ thuật | 20% | 7,0 | Script + 11 test chạy lại được; nhưng lỗ hổng mục 3 (nội dung, ngày thật, `;`, ngoài danh sách, cap cấp nhóm). Không có lỗi ẩn nghiêm trọng. |
| Chi phí & thời gian | 15% | 9,0 | 0 đ, kế hoạch lộ trình mua công cụ có trần, thẻ trả trước, hủy tự gia hạn. |
| Rủi ro & tuân thủ | 15% | 8,5 | Tránh đúng danh sách P8, không cào, không bí mật, cờ rủi ro IP/thực phẩm. Trừ nhẹ vì S21 trỏ nhánh tạm và mâu thuẫn mô tả "mạng chặn". |
| **Tổng** | | **≈ 7,6 — cần sửa nhỏ** | Tăng từ 7,4 nhờ có công cụ chạy được và sửa đúng. Chưa lên 8 vì bằng chứng. |

Phiếu tự chấm của P1 (≈ 7,9) cao hơn 0,3 điểm, chủ yếu ở độ tin cậy kỹ thuật và rủi ro.

## 9. Việc phải sửa (P1, chỉ trong `apps/radar/` và `bao-cao/dot0/p1-*.md`)
1. `apps/radar/du-lieu/source.csv` S06, S08, S09: ghi cả hai số thú cưng (1.912,5 và 1.921,5) hoặc dẫn đoạn trích đúng; kiểm lại "số shop −9%" (nguồn tôi thấy −2,47% qoq, −10,68% yoy). Cập nhật cột `tin_hieu_nhu_cau` và `ghi_chu` N18, N19 nếu đổi.
2. `source.csv` S01 và `nhom-ung-vien.csv` N14: tìm lại đoạn trích "~2 triệu đơn áo dài". Nếu không có, bỏ khỏi `tin_hieu_nhu_cau`, trừ 4 điểm (N14: demand 6, tổng 24, `diem_toi_da_da_cham` 45), sửa mục 2 và gợi ý trong `p1-radar-v2.md` (N14 không còn đứng đầu).
3. `source.csv` S25: hạ `reliability` TB → THAP (nguồn mâu thuẫn); sửa URL cho khớp nguồn đã đọc (Delzonic / blog FastMoss riêng). S26 trỏ URL khác S25 (hiện trùng).
4. `source.csv` S03: sửa URL sang nguồn thực đã đọc (BrandsVietnam) hoặc ghi rõ chưa mở metric.vn. S19–S21: dùng đường dẫn tương đối `bao-cao/dot0/...` thay URL nhánh tạm.
5. `apps/radar/kiem_tra.py` + `test_kiem_tra.py`: thêm kiểm (a) `source_id` sau khi tách `;` phải có ít nhất 1 mã và không chỉ `S21`; (b) ngày phải là ngày hợp lệ (`datetime.strptime`); (c) `fee_ref` không được trống ở `nhom-ung-vien` và `score`; (d) `mo_hinh` thuộc danh sách; (e) `demand` cấp nhóm ≤ 10, `legal` thuộc {6, 10}; (f) `type`, `export_method` của `source` thuộc danh sách (cập nhật README); (g) `do_tin_cay` của nhóm không cao hơn mức thấp nhất trong các nguồn dữ liệu. Thêm test cho từng trường hợp.
6. `bao-cao/dot0/p1-radar-v2.md`: sửa "21 dòng" → 26; thống nhất mục 3 và mục 5 về việc mạng đã mở hay chưa (nói rõ nguồn nào đọc trang gốc); thêm mục "đối chiếu KTS vòng 2" với các số lệch trên; sửa phiếu tự chấm.
7. `bao-cao/dot0/p1-radar.md` dòng 5: bỏ câu "trang giá ... không công khai giá" hoặc trỏ sang `p1-cong-cu-so-lieu.md`.
8. `bao-cao/dot0/p1-cong-cu-so-lieu.md`: ghi rõ giá FastMoss là [THẤP] sau khi đối chiếu; ghi "KTS chưa tự mở được trang giá Metric" cho tới khi có người xác nhận.

## 10. Việc cho chủ dự án / Tổng quản
- Chủ dự án: tự mở `metric.vn/analytics/pricing` đối chiếu giá 8 / 12 / 18 / 27 triệu; hỏi Metric Starter có xuất CSV không; chưa chi gì, đúng lộ trình P1. Tạo PR sau khi P1 sửa mục 9.
- Tổng quản: khi gộp vào `main`, kiểm `git diff --cached` quét khóa (CLAUDE.md quy tắc 1). Không phải khuyến nghị đầu tư / không đảm bảo lợi nhuận.

Trạng thái: audit xong, P1 cần sửa nhỏ (điểm ≈ 7,6) trước khi gộp.
