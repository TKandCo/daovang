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
