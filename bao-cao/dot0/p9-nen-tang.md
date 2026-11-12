# P9 Nền tảng kỹ thuật và bảo mật — báo cáo Đợt 0

**Trạng thái:** 🟢 Đợt 0 xong phần mã khung · đã đẩy nhánh `phong/p9-dot0` · **chờ chủ dự án** duyệt đề xuất công nghệ (mục 7) và tạo PR.
Tạo PR (chủ dự án bấm): https://github.com/TKandCo/daovang/pull/new/phong/p9-dot0 — P9 KHÔNG tự tạo / gộp PR.

## 1. Đã làm (việc → bằng chứng)
| Việc | Tệp | Bằng chứng |
|---|---|---|
| Schema tối thiểu: SKU, Đơn hàng (+ dòng đơn), Khách, Nhà cung cấp, Video, Dòng bảng phí — mỗi bản ghi có `nguon` + `ngay_nguon` (bảng phí: `nguon` + `hieu_luc_tu`, ngày tra lấy từ "(tra dd/mm/yyyy)") | `packages/schema/daovang_schema/__init__.py`, `packages/schema/README.md` | 14 kiểm thử ĐẠT; đọc được 79/79 dòng `bao-cao/dot0/bang-phi-v1.csv`, cả 79 dòng qua `kiem_tra()` |
| Khách tối thiểu dữ liệu cá nhân: chỉ mã ẩn danh, tỉnh/thành, số đơn, đồng ý nhận tin; từ chối `ho_ten, sdt, email, dia_chi, cccd, so_tai_khoan` | như trên | kiểm thử `test_khach_cam_du_lieu_ca_nhan` |
| Video: báo lỗi nếu nội dung AI rời trạng thái nháp mà chưa gắn nhãn, hoặc có người thật mà chưa có văn bản đồng ý (Quy tắc 6) | như trên | `test_video_nhan_ai_va_dong_y` |
| Lõi: cấu hình JSON không bí mật + ghi đè bằng biến môi trường `DAOVANG_*`; từ chối tệp cấu hình có tên khóa giống bí mật; `lay_khoa()` chỉ đọc biến môi trường, không in giá trị | `packages/core/daovang_core/cau_hinh.py` | 3 kiểm thử ĐẠT |
| Nhật ký che dữ liệu khách: SĐT VN (nhiều dạng viết) → `[SDT]`, email, dãy 9–19 số (CCCD / số tài khoản), token, Bearer; trường nhạy cảm trong dict / `extra=` → `[CHE]` | `packages/core/daovang_core/nhat_ky.py` | 5 kiểm thử ĐẠT, gồm 1 kiểm thử "không che nhầm" mã đơn / SKU / giá / ngày |
| Quét khóa (chỉ thư viện chuẩn): 12 loại mẫu + tên tệp cấm (khớp `.gitignore`); chế độ `--staged` / `--tat-ca` / đường dẫn; `--cai-dat` cài pre-commit (không ghi đè hook khác); không in nguyên khóa | `tools/quet-khoa.py`, `tools/README.md` (hướng dẫn tiếng Việt) | 7 kiểm thử ĐẠT: bắt đủ 12 khóa giả, không báo nhầm tệp sạch, pre-commit **chặn thật** một commit có khóa giả trong repo tạm, quét toàn repo hiện tại = SẠCH |
| Không sửa `.gitignore`, không đụng `apps/`, `ban-thu-ky/`, `quy-trinh/` | `git diff --name-only origin/main` | chỉ `packages/`, `tools/`, báo cáo này |

Chạy lại (KTS):
```bash
python3 -m unittest discover -s packages/schema/tests
```
```bash
python3 -m unittest discover -s packages/core/tests
```
```bash
python3 -m unittest discover -s tools/tests
```
```bash
python3 tools/quet-khoa.py --tat-ca
```
Kết quả ngày 12/11/2026 trên Python 3.13: 14 + 8 + 7 = **29 kiểm thử ĐẠT**, quét = SẠCH.

## 2. Số liệu
Không có số liệu phí / thuế / thị trường mới. Mọi số trong bảng phí là của P4 (`bang-phi-v1.csv`), P9 chỉ đọc.

## 3. Phát hiện khi đọc bảng phí v1 (gửi P4 / KTS)
- 1/79 dòng (`phi_SPayLater_dich_vu_tra_gop`) có nguồn "(qua tim kiem)", **không có ngày tra** → `ngay_nguon` rỗng. Dòng này đã là [THẤP].
- Cột `muc` và `hieu_luc_tu` là chữ tự do ("Nguoi ban 40 / Shopee 60", "2026-09-01 hoac 2027-01-01") → máy chỉ đọc số được ở dạng "a" / "a-b" (`khoang_muc()`), các dòng khác trả None, công cụ phải xử lý tay.
- Đề xuất bảng phí v2 (P4 quyết): tách cột `ngay_tra` riêng; `muc_min`, `muc_max` dạng số bên cạnh `muc` nguyên văn. Schema sẽ thêm trường có mặc định, không phá v1.

## 4. Đã kiểm gì / CHƯA kiểm gì
**Đã kiểm:** 29 kiểm thử đơn vị nêu trên; pre-commit chặn commit thật trong repo git tạm; quét toàn repo hiện tại sạch; đọc toàn bộ bảng phí v1.

**CHƯA kiểm:**
- Chưa chạy trên Windows / macOS của chủ dự án (chỉ Linux cloud, Python 3.13). Mã viết cho Python ≥ 3.10, chưa thử 3.10.
- Chưa thử với tệp xuất đơn thật từ Shopee / TikTok (không được đưa dữ liệu thật lên cloud) → tên cột Đơn hàng là GIẢ ĐỊNH, cần đối chiếu khi có tệp xuất mẫu (che dữ liệu) trên máy chủ dự án.
- Bộ che nhật ký KHÔNG nhận ra họ tên / địa chỉ viết tự do trong câu; dấu thời gian Unix 10 số bị che nhầm. Quy ước bù: không đưa tên / địa chỉ khách vào nhật ký.
- Bộ quét không bắt mật khẩu ngắn, khóa không có dạng đặc trưng, khóa chia nhiều dòng; pre-commit bỏ qua được bằng `--no-verify`.
- Chưa kiểm GitHub secret scanning / push protection có bật được cho repo riêng tư miễn phí không: CHƯA XÁC MINH.
- Chưa có kiểm thử chạy tự động trên GitHub (CI) — xem đề xuất.

## 5. Khó khăn cần quyết định
- **Quyền ghi `packages/schema`** (KTS / Tổng quản): `quy-trinh/van-hanh-cloud.md` ghi chỉ Tổng quản / KTS được ghi, nhưng bản giao việc giao P9 làm. P9 đã làm theo bản giao việc, trong PR riêng; KTS xác nhận khi audit.
- **Nhánh**: làm trên `phong/p9-dot0` đúng bản giao việc.

## 6. Kế hoạch Đợt sau + tiền dự kiến chi
- Khi P4 / P1 bắt đầu dùng: chuyển `apps/finance`, `apps/radar` sang đọc bảng phí qua `doc_bang_phi()` (phòng đó tự sửa thư mục mình).
- Đối chiếu schema Đơn hàng với tệp xuất mẫu (đã che) trên máy chủ dự án.
- **Tiền dự kiến chi: 0 đ.** Mọi thứ ở trên dùng công cụ miễn phí có sẵn.

## 7. ĐỀ XUẤT công nghệ — CHỜ CHỦ DỰ ÁN DUYỆT
Mục tiêu: đơn giản nhất mà chủ dự án (không phải lập trình viên) tự vận hành được.

| Hạng mục | Đề xuất | Lý do | Chi phí |
|---|---|---|---|
| Ngôn ngữ | **Python 3, chỉ thư viện chuẩn** cho lõi; thêm thư viện ngoài chỉ khi cần và ghi lý do | Không phải cài gì, ít lỗi phiên bản, dễ chạy trên mọi máy | 0 đ |
| Lưu dữ liệu chung (không bí mật) | **CSV / JSON trong repo** (bảng phí, danh mục SKU mẫu) | Mở được bằng Excel / Google Sheets, xem thay đổi trên GitHub | 0 đ |
| Dữ liệu thật (đơn, khách, sổ sách) | **Tệp CSV / SQLite trên máy chủ dự án** trong `du-lieu-that/` (đã chặn bằng `.gitignore`), sao lưu ra ổ ngoài hoặc Drive cá nhân có mật khẩu | Không lên repo / cloud (Quy tắc 1) | 0 đ |
| Giao diện cho chủ dự án | Đợt 0–1: **lệnh dòng lệnh + tệp CSV mở bằng Excel / Google Sheets**. Chưa làm web app | Ít thứ phải bảo trì nhất | 0 đ |
| Khóa bí mật | **Biến môi trường / cài đặt môi trường cloud**, mỗi khóa hạn mức chi riêng ở nhà cung cấp | Quy tắc 1, 2 | 0 đ |
| Chặn lộ khóa | `tools/quet-khoa.py --cai-dat` trên mọi bản sao + bật GitHub secret scanning / push protection nếu có (CHƯA XÁC MINH) | Hai lớp | 0 đ (GIẢ ĐỊNH) |
| Kiểm thử tự động | GitHub Actions chạy 3 lệnh `unittest` + quét khóa mỗi PR | KTS khỏi chạy tay; số phút miễn phí cho repo riêng tư CHƯA XÁC MINH | 0 đ (GIẢ ĐỊNH) |

Lợi ích: không chi tiền, ít thứ phải học. Công sức: thấp. Rủi ro: CSV / SQLite không hợp khi nhiều người cùng ghi
hoặc dữ liệu lớn → xem lại ở Đợt 2 (khi cần máy chủ chạy liên tục).

## 8. Tự chấm (KTS chấm lại độc lập)
Đủ 5 việc giao; có kiểm thử chạy được, có danh sách chưa kiểm. Điểm trừ: chưa thử trên máy chủ dự án, schema Đơn hàng chưa đối chiếu tệp xuất thật.
