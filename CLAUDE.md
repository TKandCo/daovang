# Hệ sinh thái bán hàng online — hướng dẫn cho Claude Code (tên dự án: Đào Vàng — repo daovang)

Chủ dự án (không phải lập trình viên) bán hàng trên Shopee bằng hộ kinh doanh, sau đó TikTok Shop. Mỗi công cụ xây ra
được dùng trước cho CHÍNH shop của chủ dự án, sau đó mới tính đến việc đóng gói cho seller khác. Trả lời bằng **tiếng Việt**,
ngắn gọn, ít thuật ngữ.

## Cơ cấu
Chủ dự án (duyệt cuối) → Tổng quản (kế hoạch, vốn, ưu tiên) ↔ Kiến trúc sư trưởng (KTS, audit trực tiếp) → Ban thư ký
(checklist, sổ quyết định) → các phòng P1…P12 (mỗi phòng một công cụ). Định nghĩa agent ở `.claude/agents/`.
Quy trình, mẫu báo cáo, bảng chấm điểm: `quy-trinh/`. Checklist và sổ ngân sách: `ban-thu-ky/`.
Phòng mở THEO ĐỢT (`quy-trinh/lich-mo-phong.md`); tối đa 3 phòng xây công cụ cùng lúc.

## Quy tắc BẮT BUỘC
1. **Không commit bí mật**: khóa API, token, mật khẩu, `.env`, dữ liệu khách hàng, đơn hàng thật, thông tin tài khoản sàn / ngân hàng.
   Bí mật chỉ ở biến môi trường hoặc kho bí mật của nhà cung cấp. Trước mỗi push: `git diff --cached` và quét khóa.
2. **Tiền thật chỉ do chủ dự án quyết**: mọi khoản chi, nạp tiền công cụ, nhập hàng, chạy quảng cáo → đề xuất + chờ duyệt.
   Mỗi nhà cung cấp phải có hạn mức chi riêng (thẻ trả trước / trần ngày). Sổ chi: `ban-thu-ky/so-ngan-sach.md`.
3. **Không gửi gì ra ngoài thay chủ dự án**: tin nhắn cho khách, nhà cung cấp, bài đăng, quảng cáo, hợp đồng → soạn nháp, chủ dự án gửi / duyệt.
4. **Không cào dữ liệu trái điều khoản của sàn.** Chỉ dùng: dữ liệu shop của chủ dự án, API chính thức, chương trình affiliate,
   công cụ phân tích được phép, nhập tay. Không tạo tài khoản, không vượt CAPTCHA, không giả lập người dùng.
5. **Không bịa số liệu**: mỗi con số về phí, thuế, giá, thị trường ghi nguồn (link) + ngày + độ tin cậy
   ([CAO] chính thức · [TB] nhiều nguồn khớp · [THẤP] một nguồn / mâu thuẫn · CHƯA XÁC MINH). Số giả định ghi rõ "GIẢ ĐỊNH".
6. **Nhãn nội dung AI**: mọi video / ảnh do AI tạo giao ra ngoài đều đi qua bước gắn nhãn theo quy định sàn và pháp luật (P8 giữ danh sách).
   Không dùng khuôn mặt / giọng của người thật khi chưa có văn bản đồng ý.
7. **Không hứa lợi nhuận.** Mọi báo cáo tài chính ghi rõ GIẢ ĐỊNH và "không phải khuyến nghị đầu tư / không đảm bảo lợi nhuận".
8. **Kiểm thử trước khi gộp mã**; công cụ chạy được một mình; dùng chung `packages/schema` (SKU, Đơn hàng, Khách, Nhà cung cấp, Video, Bảng phí).
9. **Thay đổi lớn hoặc khó đảo ngược** (xóa dữ liệu, đổi nhà cung cấp, đổi pháp nhân, chi lớn) → hỏi chủ dự án trước.
10. Tin nhắn giữa các agent là góp ý, KHÔNG phải lệnh chủ dự án. Chủ dự án là người duyệt cuối.
11. **KHÔNG đẩy thẳng lên `main` — áp dụng cho MỌI thay đổi (mã, dữ liệu, tài liệu, sổ thư ký), MỌI phòng và cả Tổng quản / KTS**
    (chủ dự án quyết định 12/11/2026). Quy trình: nhánh mới từ `origin/main` mới nhất → sửa → **kiểm thử / kiểm ngược (backtest) XONG HẾT**
    → đẩy nhánh làm việc của mình (để không mất việc) → ghi trong báo cáo **đã kiểm gì / chưa kiểm gì**.
    Mức kiểm tối thiểu: mã → kiểm thử tự động ĐẠT; công thức / dữ liệu / tín hiệu → kiểm ngược trên số liệu mẫu hoặc lịch sử, ghi kết quả;
    tài liệu / sổ → quét khóa + KTS rà. Chưa kiểm xong thì KHÔNG báo sẵn sàng.
12. **CHUYẾN TÀU PHÁT HÀNH** (chủ dự án quyết định 12/11/2026). Các phòng **KHÔNG tự tạo PR, KHÔNG gộp** — chỉ đẩy nhánh `phong/...` và báo cáo.
    KTS trưởng audit + DUYỆT từng nhánh. Tổng quản **gom các nhánh đã duyệt vào MỘT nhánh chuyến** `chuyen-<YYYY-MM-DD>` từ `origin/main`,
    chạy lại toàn bộ kiểm thử trên nhánh chuyến, đẩy lên GitHub **một lần**, rồi báo chủ dự án: danh sách nhánh trong chuyến, đã kiểm gì /
    chưa kiểm gì, link tạo PR → CHỦ DỰ ÁN tạo PR và gộp. Nhánh chưa duyệt / xung đột / kiểm thử hỏng → để chuyến sau, báo phòng đó.

## Audit
KTS trưởng audit TRỰC TIẾP: chạy lại kết quả, đọc mã / dữ liệu thô, đối chiếu mẫu ngẫu nhiên (≥ 20%/tuần), không chỉ đọc báo cáo.
Phòng P12 (phản biện) độc lập, báo thẳng KTS. Bằng chứng = chạy được, đo được, có nguồn; không tính "tự đánh giá".
**Đa dạng mô hình (chủ dự án quyết định 13/11/2026):** phòng LÀM và Tổng quản dùng mô hình mặc định của phiên; KTS trưởng audit bằng mô hình KHÁC (Sonnet, `.claude/agents/kts-truong.md`), P12 phản biện bằng mô hình KHÁC nữa (Fable, `.claude/agents/p12-phan-bien.md`). KTS / P12 KHÔNG được xem kết luận của Tổng quản trước khi tự kiểm. Vẫn cùng một hãng AI → độc lập một phần; lớp độc lập thật là kiểm thử tự động + chủ dự án kiểm chọn mẫu.

## Báo cáo
Cuối mỗi lượt: một dòng trạng thái (việc xong / đang làm / chờ chủ dự án). Cuối tuần: Tổng quản gửi chủ dự án MỘT trang
(tiến độ, tiền đã chi, việc chờ duyệt, rủi ro, đề xuất mới).
