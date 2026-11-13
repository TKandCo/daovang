# Audit KTS (Sonnet) — P9 sửa lần 2 + gộp thử chuyến 2 — 13/11/2026

## 1. P9 `origin/phong/p9-dot1` @ 961775f
- Nhánh đúng; không còn commit TẠM (0 commit tiêu đề "tạm"); đã gộp `p4-dot1 @ e13a831` bằng merge commit 538f705.
- `git diff origin/phong/p9-dot1 origin/phong/p4-dot1 -- apps/finance/` = TRỐNG (không chép tay mã P4).
- `bao-cao/trang-thai/p9.md`: có trạng thái XONG, mã việc, nhánh, thời điểm, kiểm đã/chưa, cần ai quyết, link báo cáo. Nhược nhỏ: "Commit cuối" không ghi mã băm (chỉ nói "commit có tiêu đề [XONG]").
- Windows thật (repo D:, temp C:, autocrlf=true), worktree `D:\GITHUB PROJECTS\_hop_dot1\kts-p9b`, riêng nhánh P9: **HỎNG 1/10 = "unittest P1 radar"** (9 lỗi `ValueError: path is on mount 'C:', start on mount 'D:'` tại apps/radar/kiem_tra.py dòng 108, `os.path.relpath`). 9/10 bộ còn lại ĐẠT (P4 tài chính, schema, core, tools+app 40s, kiểm ngược P4, dữ liệu P1, app khớp nguồn, kiểm khớp JS↔Python 100%, quét khóa).
  - Gốc lỗi là mã P1 trên `main` (không phải mã P9); `phong/p1-dot1` đã có bản vá (dùng ntpath/relpath an toàn). P9 tự báo "ĐẠT 10/10" khi chạy riêng nhánh — không đúng trên Windows thật; P9 chưa kiểm Windows thật (đã tự ghi).
- Bốc ngẫu nhiên hạt giống 20261113, 3 ví dụ: don-06, don-01, don-05 (`apps/finance/vi-du-kiem-khop.json`, chạy lõi JS trong app/daovang.html qua node). Tính tay: ln = (1-hoàn)·cm − hoàn·chi_phí_mỗi_đơn_hoàn.
  - don-06: cm 72000; hoàn 33000 (ship 30000 + phí xử lý 3000); ln = 0,9·72000 − 0,1·33000 = 61500. JS 61500 ✓
  - don-01: cm 50250; hoàn 61000 (40000 + 30%·60000 + 3000); ln = 45225 − 6100 = 39125. JS 39125 ✓
  - don-05: cm 47500; hoàn 62000 (40000 + 50%·40000 + 2000); ln = 42750 − 6200 = 36550. JS 36550 ✓
  - cm, chi_phi_moi_don_hoan, biên ròng khớp mong đợi của P4.

Chấm (bảng chấm điểm): Đúng yêu cầu 8,5 · Bằng chứng 8,5 · Tin cậy kỹ thuật 7,5 (kiểm Windows thật chưa làm, báo 10/10 chưa đúng trên Windows riêng nhánh) · Chi phí/thời gian 8 · Rủi ro/tuân thủ 8 (không vi phạm quy tắc; lỗi thuộc P1) → **≈ 8,2/10 — DUYỆT**, điều kiện: P9 không gom riêng, chỉ gom cùng/sau P1.

## 2. Gộp thử chuyến 2 (worktree `D:\GITHUB PROJECTS\_hop_dot1\kts-c2`, từ origin/main 6e40388)
Thứ tự: ban-thu-ky-dot1 → p9-dot1 → p1-dot1 → p4-dot1 → p8-dot1. Không dùng autocrlf=false (không cần). **Không xung đột bước nào**; p4-dot1 "Already up to date" (P9 đã chứa).
Kiểm thử bản gộp (Windows thật): **TẤT CẢ ĐẠT 10/10**: P4 tài chính OK · P1 radar OK (4,9s) · schema OK · core OK · tools+app OK · kiểm ngược P4 ĐẠT · dữ liệu P1 ĐẠT (13 CSV) · app khớp nguồn ĐẠT · kiểm khớp JS↔Python 100% · quét khóa SẠCH. Cây sạch sau chạy.
Số ca unittest từng bộ không in ra bởi runner (chỉ OK/HỎNG) — chưa đếm.

## 3. Quyết định
- P9: DUYỆT (≈ 8,2).
- Chuyến 2 SẴN SÀNG gom. Thứ tự khuyên dùng: thư ký → P1 → P9 (đã gồm P4; P4 tự lọt) → P8. Bắt buộc P1 đi cùng chuyến với P9 (nếu tách, kiểm thử hỏng trên Windows ổ khác nhau). Nên đổi dòng trạng thái P9 "Commit cuối" ghi mã băm khi gom.

## 4. Chưa kiểm
- Không dò p4/p8/p1 sâu ngoài kiểm thử tự động; không soát nội dung pháp lý P8; điện thoại thật, GitHub Actions thật, CI trên Linux; số ca unittest; tính tay chỉ 3/18 ví dụ (ví dụ affiliate / dropship không nằm trong mẫu ngẫu nhiên này).
- Worktree tạm kts-p9b, kts-c2 còn giữ (chỉ đọc, chưa xóa).
