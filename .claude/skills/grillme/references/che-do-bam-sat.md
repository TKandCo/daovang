# Chế độ BÁM SÁT — để chủ dự án thật sự nắm dự án

> Phần chung trong SKILL.md áp đầy đủ ở đây: khung lập luận 4 phần, mức hậu quả, ba kiểu rối A/B/C, phản biện độc lập bằng mô hình khác, kiểm hiểu, sản phẩm PDF. Tệp này chỉ nói những gì riêng của BÁM SÁT.

## Vì sao có chế độ này

Tổng quản xây nhanh và tốt, nhưng mỗi lượt làm đều có hàng chục quyết định nhỏ: chọn công cụ, chọn nơi lưu, đặt ngưỡng, chọn cách tính, bỏ qua một trường hợp. Chủ dự án duyệt PR hay bấm "ok" mà không nắm những quyết định đó thì thực chất là **AI tự quyết thay**. Dự án càng lớn, chủ dự án càng thấy rối, và dần thành người đứng ngoài chính dự án của mình.

Mục tiêu của BÁM SÁT là đến cuối, chủ dự án **tự kể lại được** bằng lời của mình:
1. Dự án làm gì, cho ai, đang ở đâu.
2. Các khối chính và cách chúng nối nhau.
3. Tiền, dữ liệu, quyền đi qua đâu.
4. Những quyết định quan trọng đã có, và **cái nào mình chưa thật sự duyệt**.
5. Điểm yếu, rủi ro, và việc mình phải làm hoặc phải quyết.

Không đặt mục tiêu "chủ dự án hiểu mã". Mục tiêu là **đủ hiểu để quyết đúng và kiểm được tổng quản**.

## Bước 0: Chuẩn bị (chủ dự án chưa thấy gì)

Đọc kỹ dự án: CLAUDE.md, README, `docs/` (gồm `docs/quan-tri/`), sổ quyết định, checklist, báo cáo, lịch sử git và PR gần đây, cấu trúc thư mục, các tệp cấu hình chính. **Đọc cả các nhánh chưa gộp** (`git log --all`, `git show <nhánh>:<tệp>`), và tách rõ hai phần: **đã vào bản chính** và **đang chờ chủ dự án duyệt**. Chủ dự án thường rối chính vì không biết cái mình thấy là bản nào. Bản trên máy có thể cũ: ghi ngày của lần lấy về gần nhất. Muốn lấy bản mới (`git fetch`) thì làm theo quy tắc của dự án, hoặc hỏi trước. Rồi tự dựng **bản đồ 3 tầng**:
- **Tầng 1:** dự án trong 1 câu.
- **Tầng 2:** 4–7 khối chính. Mỗi khối 1 dòng "làm gì", kèm mũi tên nối giữa các khối.
- **Tầng 3:** với mỗi khối: chạy ở đâu, giữ dữ liệu gì, tốn tiền gì, ai sửa, rủi ro chính.

Lập riêng **danh sách ngưỡng và quy ước** (kiểu rối B): mọi con số quyết định đạt/không đạt, cảnh báo, chấm điểm. Mỗi ngưỡng ghi: đặt ở đâu (tệp, dòng), có căn cứ không, đổi ngưỡng thì kết quả đổi ra sao. Đây là thứ chủ dự án hay vấp nhất (ví dụ "t > 2,85 thì đạt hay sao đó").

Đồng thời lập **danh sách quyết định ngầm**: những lựa chọn có hậu quả mà không thấy dấu vết chủ dự án duyệt trong sổ quyết định, PR, hay lời trong phiên. Ví dụ: chọn nhà cung cấp, lưu dữ liệu khách ở đâu, công thức tính phí, ngưỡng cảnh báo, việc tự động gửi tin hay tự động chi tiền, quyền ai xem gì.
- **Vẫn tính là ngầm** khi chủ dự án chỉ duyệt *hướng* ("làm sổ lãi lỗ"), còn *con số, ngưỡng, giả định, công thức* có hậu quả là do AI đặt.
- **Thêm loại "lệch nhau":** tài liệu nói một đằng, mã hay việc làm một nẻo. Ví dụ: README ghi "chưa có mã" trong khi đã có app; quy trình ghi phải qua bước X nhưng bước X bị bỏ.
- **Xếp mức hậu quả cho từng dòng:**
  - **Cao:** đổi quyết định đi tiếp hay dừng, đổi kết luận lời/lỗ, đụng tiền thật, dữ liệu người khác, pháp lý.
  - **Vừa:** đổi cách làm hoặc chi phí, đảo ngược được.
  - **Thấp:** chỉ là tài liệu hoặc tên gọi.

  Ghi kèm bằng chứng (tệp, commit) cho mỗi dòng; không chắc thì ghi "chưa kiểm".

Có sẵn `docs/quan-tri/SO_TAY_CHU_DU_AN.md` từ lần trước thì đọc nó trước, rồi chỉ cập nhật phần đã thay đổi kể từ ngày ghi trong sổ.

## Bước 1: Tin nhắn đầu tiên: toàn cảnh, rồi hỏi muốn nắm tới đâu
Tin nhắn đầu gồm:
1. **Toàn cảnh 3 dòng** (tầng 1, kèm "đang ở đâu").
2. **Sơ đồ khối tầng 2.** Chủ dự án cần thấy bản đồ trước rồi mới chọn được chỗ muốn đi.
3. **Việc đang chờ chủ dự án duyệt** (nếu có), mỗi việc 1 dòng. Đây thường là lý do thật khiến họ thấy rối.
4. Các câu hỏi bên dưới.

Số tiền nào là ước tính hoặc giả định thì gắn nhãn **GIẢ ĐỊNH** ngay cạnh con số; chỉ số tiền đã thật sự chi hoặc thu mới không cần nhãn. Lẫn hai loại này là cách nhanh nhất làm chủ dự án hiểu sai.

Câu hỏi (1 lượt, 2–3 câu):
- Phần nào đang thấy rối nhất? Hỏi mở, hoặc cho chọn nhiều (multiSelect). AskUserQuestion chỉ cho tối đa 4 phương án, nên khi có hơn 4 khối thì gộp các khối gần nhau thành 3–4 nhóm theo câu hỏi chủ dự án hay đặt (ví dụ "tiền và lãi lỗ", "công cụ", "luật và dữ liệu khách", "cách đội làm việc"); ô "Khác" để chủ dự án tự gõ.
- Hiểu để làm gì? Ví dụ: để duyệt một việc sắp tới; để tự kể cho người khác; để biết dự án có an toàn không; để quyết đi tiếp hay dừng. (Đây là câu về mong muốn, không gắn "(Đề xuất)".)
- Buổi này ông có khoảng bao lâu? (giữ mỗi buổi ngắn: ~15–30 phút, vài khối; phần còn lại để buổi sau)

## Bước 2: Đi từng lớp, từng khối

1. **Bắt đầu bằng tầng 1 và sơ đồ tầng 2.** Vẽ sơ đồ khối đơn giản bằng chữ hoặc mũi tên ngay trong khung chat; nếu có công cụ vẽ thì dùng. Đừng mở đầu bằng chi tiết.
2. **Mỗi lần giải thích một khối**, theo khung:
   - **Nó làm gì**, bằng ví dụ đời thường. Ví dụ: "Phòng P4 giống người kế toán: nhận giá nhập, phí sàn, rồi tính ra lãi từng đơn."
   - **Nó lấy gì vào, đưa gì ra, nối với khối nào.**
   - **Tiền và dữ liệu:** có tốn tiền không, giữ dữ liệu của ai.
   - **Ai quyết cái gì ở đây:** điều chủ dự án đã duyệt, và **điều AI đã chọn thay**.
   - **Chỗ yếu:** một hai điều có thể hỏng, nói thẳng.
3. **Sau mỗi khối, kiểm hiểu bằng 1–2 câu tình huống**, không phải câu đố. **Cuối buổi**, mời chủ dự án **kể lại 3 điều** (SKILL.md mục 5). Ví dụ: "Nếu sàn tăng phí 2%, theo ông chỗ nào trong dự án phải sửa?" hay "Nếu máy nhà hỏng tối nay, dữ liệu nào mất?" Chủ dự án trả lời lệch thì giải thích lại theo cách khác (ví dụ khác, sơ đồ khác), không nhắc lại y câu cũ.
4. **Cho chủ dự án hỏi lại bất cứ lúc nào.** Câu hỏi của họ cho biết chỗ nào còn rối.
5. **Từ ngữ:** thuật ngữ nào bắt buộc phải dùng thì giải thích một lần và ghi vào **từ điển của dự án** trong sổ tay. Lần sau dùng đúng từ đó, không đổi tên gọi.

## Bước 3: Duyệt lại các quyết định ngầm

Đây là phần giá trị nhất của BÁM SÁT. **Mỗi buổi đưa tối đa 5 quyết định ngầm**, mức Cao trước, ưu tiên các quyết định nằm trong khối chủ dự án vừa chọn. Phần còn lại ghi vào sổ tay mục 4 để các buổi sau đi tiếp; đổ 18 dòng một lúc thì chủ dự án sẽ bấm "giữ" hết cho xong. Với mỗi quyết định:
- Nói rõ: đã chọn gì, vì sao, phương án khác là gì, đổi về sau có khó không.
- Hỏi chủ dự án: **giữ, đổi, hay cần hiểu thêm?** Dùng AskUserQuestion; phương án tổng quản đề xuất có thể ghi "(Đề xuất)", vì đây là câu về cách làm, không phải về mong muốn.
- Ghi kết quả vào sổ tay, mục "Quyết định đã được chủ dự án xác nhận". Ghi kèm ngày và lời của chủ dự án.

Chủ dự án muốn đổi thì **đừng đổi ngay**. Ghi thành yêu cầu mới; nếu yêu cầu còn mơ hồ thì chuyển sang chế độ PHỎNG VẤN cho riêng điểm đó.

## Bước 4: Sổ tay chủ dự án

Viết hoặc cập nhật `docs/quan-tri/SO_TAY_CHU_DU_AN.md` theo mẫu `assets/mau-so-tay-chu-du-an.md`, cho **phản biện độc lập** (SKILL.md mục 4), rồi **xuất PDF có số phiên bản** gửi chủ dự án (SKILL.md mục 6). Phần giao diện có câu về gu (kiểu A) thì kèm 2–3 bản phác. Dự án có quy định chỗ khác thì theo quy định của dự án. Sổ tay là **tài liệu**, không phải sửa sản phẩm, nhưng việc ghi vào repo vẫn **đi theo quy trình commit của dự án**: nhánh riêng, chuyến, PR; không đẩy thẳng main. Dự án đã có sổ quyết định thì mục 3 của sổ tay chỉ trỏ tới sổ đó, và chỉ ghi thêm những quyết định được xác nhận trong buổi BÁM SÁT. Gửi PDF và hỏi: "Có chỗ nào ông đọc vẫn thấy rối không?"

Sổ tay là tài liệu sống: cập nhật sau mỗi chuyến phát hành, hoặc khi có quyết định lớn. Đầu sổ ghi ngày cập nhật, để lần BÁM SÁT sau chỉ cần đi qua phần đã thay đổi.

## Khi nào dừng một buổi
- Đã đi hết các khối chủ dự án chọn, và họ trả lời được câu tình huống của từng khối.
- Hoặc hết thời gian chủ dự án dành cho buổi này. Khi đó ghi vào sổ tay "đã đi qua khối nào, còn khối nào", để buổi sau nối tiếp.
- Hoặc chủ dự án nói "đủ rồi".

## Lỗi thường gặp cần tránh
- Đổ hết bản đồ tầng 3 vào một tin nhắn dài. Mỗi lần một khối thôi.
- Giải thích bằng tên tệp, tên hàm. Chỉ đưa tên tệp làm chú thích cho ai muốn tra, không dùng nó để giải thích.
- Kể số tiền giả định như thể là số thật.
- Tô đẹp dự án. Chỗ yếu, chỗ chưa kiểm, chỗ AI tự quyết phải nói thẳng: chủ dự án cần sự thật để quyết.
- Sửa dự án ngay trong buổi BÁM SÁT. Chỉ ghi yêu cầu; làm sau, theo quy trình thường của dự án.
