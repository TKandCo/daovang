# tools — công cụ dùng chung

## `quet-khoa.py` — quét khóa bí mật trước khi commit / push

Chỉ cần Python 3 (có sẵn trên macOS / Linux; Windows cài từ python.org). Không cần cài thêm gì.

### Cài một lần để tự quét mỗi lần commit (pre-commit)
Mở cửa sổ dòng lệnh (Terminal), vào thư mục dự án rồi chạy:
```bash
python3 tools/quet-khoa.py --cai-dat
```
Thấy dòng "Đã cài pre-commit" là xong. Từ giờ, mỗi lần commit, máy tự quét các tệp sắp commit; thấy khóa thì
**chặn commit** và chỉ ra tệp + dòng. Nếu máy đã có pre-commit của công cụ khác, lệnh sẽ dừng, không ghi đè
(chỉ thêm `--ghi-de` khi chắc chắn). Lưu ý: mỗi bản sao repo (mỗi máy, mỗi phiên cloud) phải cài lại một lần.

### Chạy tay
```bash
python3 tools/quet-khoa.py
```
(quét các tệp đã `git add`; nên chạy ngay trước `git push`, cùng với `git diff --cached`)
```bash
python3 tools/quet-khoa.py --tat-ca
```
(quét toàn bộ repo)

### Đọc kết quả
- `SẠCH` → được commit.
- `CÓ n NGHI VẤN` → mỗi dòng: `tệp:dòng [loại] 4 ký tự đầu…` (không in nguyên khóa).
  - Khóa thật: gỡ khỏi tệp, `git restore --staged <tệp>`, **thu hồi / đổi khóa** ở nhà cung cấp (coi như đã lộ).
  - Chắc chắn vô hại (ví dụ dữ liệu mẫu): thêm chú thích `quet-khoa: bo-qua` ở cuối dòng đó.

### Bắt được gì
Khóa riêng (PEM), AWS, GitHub, Anthropic, OpenAI, Google, Slack, Stripe live, Telegram bot, JWT, chuỗi kết nối
có mật khẩu, gán dạng `api_key = "…"` / `mat_khau: "…"` (≥ 12 ký tự). Chặn cả **tên tệp** cấm commit: `.env`,
`*.pem`, `*.key`, `secrets/`, `data/`, `du-lieu-that/`, `exports/`, `*.sqlite`, `*.db` (khớp `.gitignore`).

### Giới hạn
Không bắt được mật khẩu ngắn, khóa không có dạng đặc trưng, khóa bị chia nhiều dòng, hay dữ liệu khách trong CSV
(họ tên, SĐT) — cái đó chặn bằng `.gitignore` (thư mục `data/`, `du-lieu-that/`). Pre-commit có thể bị bỏ qua bằng
`git commit --no-verify` → đề xuất bật thêm *secret scanning* của GitHub (miễn phí cho repo riêng tư? CHƯA XÁC MINH).

Kiểm thử: `python3 -m unittest discover -s tools/tests`

## `chay-kiem-thu.py` — chạy TOÀN BỘ kiểm thử bằng một lệnh
```bash
python3 tools/chay-kiem-thu.py
```
(Windows: `py tools\chay-kiem-thu.py`.) Gồm mọi bộ `unittest`, kiểm ngược P4, kiểm dữ liệu P1, app khớp nguồn,
kiểm khớp JS ↔ Python, quét khóa. Dòng cuối `TẤT CẢ ĐẠT` mới được báo sẵn sàng. Chưa cài Node.js thì thêm `--nhanh`
(bỏ kiểm khớp — khi đó CHƯA đủ điều kiện báo sẵn sàng). GitHub Actions (`.github/workflows/kiem-thu.yml`) chạy
đúng lệnh này, chỉ khi có PR vào `main`. Phòng nào thêm thư mục kiểm thử mới → thêm vào `BO_UNITTEST` trong tệp
này (nếu quên, bước "kiểm thử mồ côi" sẽ HỎNG).

## `dong-goi-app.py` — đóng gói `app/daovang.html`
`python3 tools/dong-goi-app.py` ghép `app/src/*` + bảng phí (`bao-cao/dot0/bang-phi-v1.csv`, đọc bằng chính mã
Python của P4) thành một tệp. `--kiem` chỉ kiểm tệp đang có còn khớp nguồn không.

## `kiem-khop.py` — kiểm khớp app (JS) ↔ máy tính Python của P4
`python3 tools/kiem-khop.py` (cần Node.js ≥ 18). Chạy cùng bộ ví dụ (3 ví dụ kiểm ngược P4 × mức giữa / cao ×
có / không hoàn, 400 ví dụ tự sinh, và `apps/finance/vi-du-kiem-khop.json` nếu P4 đã có) qua cả hai bản.
Tiền lệch > 1 đ = HỎNG; chữ cảnh báo / tên khoản / nguồn phải giống hệt; ví dụ nhập sai phải báo cùng lỗi.
`--so-ngau-nhien 5000` để kiểm kỹ hơn, `--chi-tiet` để in mọi chỗ lệch.
