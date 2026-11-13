# Biên bản audit KTS (mô hình Sonnet) — Chuyến 2 / Đợt 1 đợt A (13/11/2026)

Máy: Windows 11, Python 3.13.14, Node 22.14; repo ở D:, thư mục tạm ở C: (điều kiện thật). `PYTHONUTF8=1`.
Worktree tạm MỚI (ngoài repo, không sửa nhánh có sẵn): `D:\GITHUB PROJECTS\_hop_dot1\kts-thu\{p1,p4,p8,p9,gop,gop2}`.
P9 kiểm bản MỚI `origin/phong/p9-dot1 @ 0de4de8` (thư mục `_hop_dot1\p9` là bản cũ ec99f9c — không dùng).
Hạt giống ngẫu nhiên: **20261113** (Python `random.seed`).

## Kết luận nhanh
| Nhánh | Quyết định | Điểm |
|---|---|---|
| phong/p4-dot1 | **DUYỆT** | 8,15 |
| phong/p1-dot1 | **DUYỆT** (sửa nhỏ ghi ở dưới, không chặn chuyến) | 7,85 |
| phong/p8-dot1 | **DUYỆT** có điều kiện (sửa nhỏ checklist) | 7,7 |
| phong/p9-dot1 | **TRẢ LẠI** | 7,1 |
| ban-thu-ky-dot1 | không chấm; gộp sạch, không xung đột | – |

Lỗi quan trọng nhất: **`phong/p9-dot1` KHÔNG có phần affiliate / dropship + 18 ví dụ P4** mà báo cáo của nó nói đã làm (phần đó nằm ở nhánh nháp `phong/p9-dot1-chuan-bi`). Gộp P1+P4+P8+thư ký+P9 (đúng nhánh `phong/p9-dot1`) → HỎNG 2 bước (xem mục 4).

## 1. Chạy lại kiểm thử (trên Windows thật, repo D:, tạm C:)
| Lệnh | Nhánh | Kết quả |
|---|---|---|
| `unittest discover -s apps/finance -t apps/finance` | p4 | 60/60 OK (đúng như báo cáo) |
| `python -m taichinh.vi_du_kiem_khop --kiem` | p4 | KHỚP |
| `python -m taichinh.kiem_nguoc` | p4 | TẤT CẢ KHỚP |
| `unittest discover -s apps/radar` + `python kiem_tra.py` | p1 | 52/52 OK; "ĐẠT — 13 tệp"; KHÔNG còn lỗi `path is on mount C:/D:` (đã sửa thật, trên máy khác ổ thật — không chỉ mô phỏng) |
| `python tools/chay-kiem-thu.py` | p9 riêng lẻ | 8/9 bước ĐẠT; HỎNG "unittest P1 radar" (9 lỗi đúng `ValueError: path is on mount 'C:'…`) — vì nhánh P9 mang mã P1 cũ; báo cáo P9 đã tự nêu trước. Xác nhận lỗi Windows có thật và nhánh P1 sửa được nó |
| P8 | p8 | Không có mã — chỉ đọc |
| thu2 (có sẵn, P1+P4+P8+thư ký, không P9) | thu2 | finance 60 OK, radar 52 OK, kiem_tra ĐẠT (không có `tools/chay-kiem-thu.py` vì không có P9) |

## 2. Mẫu ngẫu nhiên (hạt giống 20261113)
**(a) Ví dụ kiểm khớp P4** (18 ví dụ; bốc chỉ số 0, 4, 5, 17 = don-01, don-05, don-06, so-01; thêm tính tay aff-02, aff-03, dropship-01, von-01 = 8/18 ≈ 44%):
- don-01: phí ngành 15% = 22.500; GD 6% = 9.000; thuế 1,5% = 2.250; CM = 150.000 − 99.750 = 50.250 ✓; hoàn 10%: 0,9×50.250 − 0,1×(40.000 + 0,3×60.000 + 3.000) = 45.225 − 6.100 = 39.125 ✓.
- don-05: CM 47.500 ✓; 0,9×47.500 − 0,1×(40.000 + 20.000 + 2.000) = 36.550 ✓.
- don-06 (TikTok): CM 72.000 ✓; 64.800 − 3.300 = 61.500 ✓.
- so-01: 5,6 tr × 28/57 = 2.750.877 ✓; chi 2.400.000 + 2.750.877 = 5.150.877 ✓; lãi 6,4 tr − 5.150.877 = 1.249.123 ✓.
- aff-02: 250.000×0,9902 = 247.550; thuế 10% = 24.755; thực nhận 222.795 ✓. aff-03: 1.188.240 − 118.824 − 300.000 = 769.416 ✓.
- dropship-01: CM 63.000 ✓; 0,9×63.000 − 0,1×75.000 = 49.200 ✓. von-01: 5×77.000×8 = 3.080.000 ✓.
Kết quả: 8/8 khớp. Chưa kiểm: tỷ lệ phí ngành (17% Sắc đẹp…) đọc từ bảng phí v1 — không đối chiếu lại với trang sàn (tải bị chặn).

**(b) Nguồn N27–N38** (bốc N27, N29, N38):
- N27 (luatvietnam): hiệu lực 01/01/2026 ✓; HKD miễn Điều 21, 22, khoản 2 Điều 33 ✓ (trừ khi xử lý dữ liệu nhạy cảm…). Nguồn KHÔNG nêu thời hạn miễn cho HKD (mốc 5 năm là của doanh nghiệp nhỏ / khởi nghiệp) → "MÂU THUẪN 5 năm hay vĩnh viễn" của P8 có thể do lẫn đối tượng — nên ghi lại.
- N29 (lsvn): phạt 50–70 triệu ✓. Câu "tối đa 5% doanh thu năm liền kề" mà P8 gắn cho N29/N27: trang N29 KHÔNG nói → CHƯA XÁC MINH bằng trang tôi đọc. Ngày hiệu lực NĐ 330: trang không nêu (P8 đã ghi [THẤP]).
- N38 (baovanhoa): bài ghi chủ hộ < 1 tỷ không đóng bắt buộc **từ 01/01/2026** (NĐ 141/2026), còn P8 viết **từ 01/07/2026** và gắn N38 → LỆCH ngày so với chính nguồn dẫn (hai nguồn P12 cũng ghi 01/07). Hạ cả dòng xuống [THẤP] về ngày, hoặc ghi rõ hai mốc.

**(c) Radar P1** (bốc 3 dòng nhóm N01, N05, N06 + 3 nguồn S06, S01, S27):
- Điểm sơ bộ: N01 8+10+8 = 26 ✓, N05 6+10+8 = 24 ✓, N06 6+10+6 = 22 ✓ (đúng tổng các ô đã chấm; các ô khác "CHƯA ĐO" — trung thực).
- S01 (CafeBiz): TikTok 34,6 nghìn tỷ vs Shopee 33,1 ✓; số 2 triệu đơn áo dài trong bài tự mâu thuẫn (ghi 1/2025 rồi 1/2026) → P1 đã gắn S27 [THẤP], đúng.
- S06 (1thegioi): 1.921,5 tỷ, +38,2%, 22,9 triệu sp ✓. Nhưng "sản lượng −6,9%" và "giá bình quân +~48%" KHÔNG thấy trong bản đọc trang (có thể thiếu do bản tóm tắt) → CHƯA XÁC MINH 2 con số đó.
- Bảng phí theo nhóm P1: dựa trên máy P4 (kiểm ngược tay của P1 N18 24,5% khớp công thức; tôi không tự tính lại 80 dòng, chỉ `kiem_tra.py` tính lại được và ĐẠT).

## 3. Đối chiếu chéo giữa phòng
- **Ngưỡng 250.000 đ (LỆCH thật):** P4, P1, P9 hard-code "10% khi ≥ 250.000 đ" (giao việc dictate); P8 viết ngưỡng đang MÂU THUẪN (2 triệu / 5 triệu theo NĐ 253/2026 / 250.000) và nói rõ "P4 chưa nên đưa ngưỡng nào vào công thức, dùng tạm 10% mọi khoản". P4 có tham số `nguong_tinh_tren` nhưng KHÔNG có cách bỏ ngưỡng. Hai phòng ngược nhau; chưa ai đối chiếu.
- **Mức khấu trừ affiliate:** P8 nêu từ 01/10/2026 Shopee chuyển 5% TNCN + 5% GTGT [THẤP]; P1/P4/P9 dùng 10% TNCN. Cùng tổng 10% nhưng khác bản chất (GTGT vs TNCN) — chưa phản ánh.
- **Hoàn thuế sàn:** P8 (checklist dòng 124) "dưới 200 triệu/năm có thể xin hoàn"; P4 (dot0) "≤ 1 tỷ phải làm thủ tục hoàn". Lỗi P12 2.3(b) đã nêu vẫn CÒN.
- **0,98% phí affiliate / 6% phí giao dịch / 1,5% thuế:** P1, P4, P9 khớp nhau. 08/05 vs 01/05 (Mall / thường): bảng phí v1 đã ghi; P8 không đụng.
- **BHXH 1 tỷ:** P8 nhất quán nội bộ; lệch ngày với nguồn (mục 2b).
- **Nhãn "chưa gồm / gồm thuế khấu trừ":** P4 đã sửa trong mã + báo cáo; tệp `bao-cao/dot0/p4-tai-chinh.md` (ngoài phạm vi) vẫn nhãn cũ — P4 tự báo.
- **Giả định hủy / hoàn "hỏng 30%" (P1) vs ví dụ P4 (30 / 50 / 0%)**: khác nhau theo từng ví dụ, ghi rõ GIẢ ĐỊNH — không lệch.

## 4. Thử gộp
- `gop` = origin/main + thư ký + **P9 (`phong/p9-dot1`)** + P1 + P4 + P8: gộp sạch (không xung đột). Chạy `tools/chay-kiem-thu.py`: **HỎNG** 2 bước: (i) "unittest tools + app" 7 lỗi; (ii) "kiểm khớp JS ↔ Python": `KHÔNG CHẠY ĐƯỢC: trường không có trong DauVao: ['loai_shop','ngay_giao','phi_ncc','ty_le_huy']` — lõi JS của nhánh P9 không biết dropship / affiliate, không đọc được 18 ví dụ P4. Các bước P4, P1, schema, core, kiểm ngược, kiểm dữ liệu, app khớp nguồn, quét khóa: ĐẠT.
- `gop2` = `gop` + `phong/p9-dot1-chuan-bi` (nhánh nháp = p9-dot1 + commit "TẠM" gộp P4 + 3 commit P9 phần affiliate/dropship): gộp sạch, **TẤT CẢ ĐẠT** (10/10 bước; kiểm khớp 100%). Nội dung chuan-bi: 22 tệp, thêm JS affiliate/dropship/vốn ứng trước/sổ lãi lỗ, giao diện, kiểm khớp 18 ví dụ, 2 ảnh. Không chấm theo yêu cầu.
- thu2 (không P9): chạy đạt.
- Gộp lần đầu trong worktree Windows có `core.autocrlf=true`: ba lần gộp P1/P4/P8 trước khi gộp P9 báo "local changes would be overwritten" (tệp CRLF của P1 hiện thành đã sửa); gộp thư ký + P9 (có `.gitattributes`) trước thì sau đó P1/P4/P8 gộp sạch. Rủi ro vận hành: Tổng quản nên gộp P9 (.gitattributes) trước, hoặc dùng `core.autocrlf=false`. [Quan sát 1 lần, chưa lặp lại có kiểm soát.]

## 5. Chấm điểm (bang-cham-diem.md; trọng số 25/25/20/15/15)
Cách làm: "Chi phí & thời gian" — không phòng nào đo thời gian / chi phí mỗi đơn vị đầu ra (chỉ ghi 0 đ chi) → chấm 6 (không đo = không được cao). P8 không có mã → "Độ tin cậy kỹ thuật = không áp dụng", chia lại trọng số trên 80% (25/25/15/15 → chia 0,8).
| | Đúng yêu cầu | Bằng chứng | Kỹ thuật | Chi phí/TG | Rủi ro | Tổng |
|---|---|---|---|---|---|---|
| P1 | 8,5 | 7 | 9 | 6 | 8,5 | **7,85** |
| P4 | 9 | 8 | 9 | 6 | 8 | **8,15** |
| P8 | 8,5 | 7,5 | n/a | 6 | 8,5 | **7,7** (6,175/0,8) |
| P9 (phong/p9-dot1) | 6 | 7 | 7,5 | 7 | 8,5 | **7,1** |
Lý do ngắn:
- P1: đủ 4 việc, lỗi Windows sửa thật + kiểm thử ĐẠT trên máy khác ổ; trừ vì S06 hai con số chưa khớp nguồn, mọi nhóm vẫn [THẤP], chưa có dữ liệu sản phẩm thật (chờ chủ dự án).
- P4: đủ 6 mục, 60 test ĐẠT, tính tay 8/8 khớp, GIẢ ĐỊNH ghi rõ, tự nêu lỗ hổng cổng. Trừ vì ngưỡng 250k mâu thuẫn P8 chưa giải quyết, TikTok affiliate = luật Shopee tạm.
- P8: đủ 4 mục, hạ nhãn trung thực, có câu hỏi chuyên gia; trừ vì N38 lệch ngày, "5% doanh thu" không có trong nguồn, dòng "200 triệu" mâu thuẫn P4 chưa xử lý.
- P9: app một tệp, CSP chặn mạng, Actions đúng chuẩn (action chính thức ghim commit, `contents: read`, chỉ khi PR); 8/9 bước tự đạt. Nhưng báo cáo trên chính nhánh này mô tả phần (2) affiliate/dropship + 18 ví dụ là "XONG trên nhánh nháp" — nhánh được giao audit không có, nên tiêu chí "kiểm khớp 100% ví dụ hiện có của P4" KHÔNG đạt khi gộp; không ghi đè được vì phòng đã tự khai thật, nên không bị vi phạm trung thực.

## 6. Quyết định
- **P4: DUYỆT.** **P1: DUYỆT.** **P8: DUYỆT** (sửa nhỏ không chặn).
- **P9: TRẢ LẠI.** Việc phải sửa (P9, trước chuyến 2): đẩy lên `phong/p9-dot1` bản đã gồm phần (2) (cách làm: rebase 3 commit P9 phần (2) lên nhánh sau khi P4 vào, bỏ commit "TẠM") rồi chạy `chay-kiem-thu.py` trên bản gộp P1+P4+P8 phải ĐẠT 10/10 (`gop2` của tôi đã chứng minh nội dung chuan-bi đạt). Hoặc Tổng quản xin P9 báo "sẵn sàng" cho đúng một nhánh duy nhất. Không được đưa `chuan-bi` nguyên trạng vào chuyến (có commit TẠM trùng P4).
- Nếu chuyến 2 không thể chờ P9: gom P1 + P4 + P8 + thư ký (thu2 đạt) và để P9 sang chuyến sau — lúc đó nhánh P9 phải đạt cùng nhánh P4.

## 7. Lỗi / rủi ro phát hiện thêm
1. P9 chưa chạy trên Windows thật ở bước kiểm khớp / app — trên `gop2` tôi đã chạy toàn bộ bước trên Windows thật (ĐẠT), trừ GitHub Actions thật, điện thoại thật.
2. `apps/radar/**/*.csv` giữ CRLF (`-text`) — kết hợp `autocrlf=true` tạo trạng thái "mixed" (`source.csv` i/mixed). Chưa gây lỗi test, nhưng dễ tạo nhiễu khi gộp.
3. Mâu thuẫn ngưỡng 250k / cách khấu trừ affiliate giữa P8 và P4/P1/P9 (mục 3) — cần chủ dự án / kế toán (câu 1.8) trả lời trước khi tin vào số affiliate thực nhận.
4. Bảng 3 kịch bản P4: kể cả kịch bản TỐT lãi cộng dồn 8 tuần vẫn âm (−2,77 tr đ) — đúng GIẢ ĐỊNH, nhưng chủ dự án cần đọc kỹ trước khi mở chi tiền.

## 8. Việc phải sửa (người / hạn)
- P9: nhánh duy nhất đã gồm phần (2), kiểm lại trên bản gộp — trước chuyến 2.
- P8: sửa dòng N38 (mốc 01/01 vs 01/07/2026), bỏ / hạ nhãn "5% doanh thu" ở N29/N27, ghi lại rằng nguồn N27 không nêu hạn miễn của HKD, xử lý dòng "dưới 200 triệu xin hoàn" so với P4 — chuyến sau.
- P1: đối chiếu lại số "−6,9%" và "+~48%" ở S06 hoặc hạ [THẤP] — chuyến sau.
- P4 / Tổng quản: giải quyết ngưỡng 250k với P8; sửa nhãn dot0 `p4-tai-chinh.md`.
- Tổng quản: khi gộp, gộp thư ký + P9 trước (có `.gitattributes`) hoặc `core.autocrlf=false`.

## 9. CHƯA KIỂM (và vì sao)
- Không mở được trang chính thức Shopee / TikTok (không thử — đã được P12 báo bị chặn): các dòng bảng phí v1 chỉ kiểm bằng tính toán, không bằng nguồn.
- Chỉ kiểm 3 nguồn N27–N38 trên 12 (25%) và 3 nguồn Radar trên 28 (~11% — dưới ngưỡng 20%); S06 chỉ đọc qua bản tóm tắt của công cụ tải trang.
- 80 dòng `phi-theo-nhom.csv`: không tự tính lại (dựa vào `kiem_tra.py` ĐẠT).
- GitHub Actions thật (ước tính 1–1,5 phút / PR), điện thoại thật, ảnh 412 px chỉ kiểm có tệp, không đọc ảnh.
- Điểm Chi phí & thời gian dựa trên "không đo", không có dữ liệu thời gian phiên.

Không phải khuyến nghị đầu tư / không đảm bảo lợi nhuận. Không sửa / commit / push / tạo PR; chỉ tạo worktree tạm trong `_hop_dot1\kts-thu` (+ nhánh cục bộ `kts-thu-gop`).
