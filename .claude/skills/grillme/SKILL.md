---
name: grillme
description: >-
  Công cụ để chủ dự án (nói tiếng Việt, không phải lập trình viên) và tổng quản dự án HIỂU NHAU TRỌN VẸN, bằng lập luận chặt chẽ, có nhãn, có phản biện, không mơ hồ hay phóng đại. Hai chế độ. (1) PHỎNG VẤN: hỏi kỹ chủ dự án trước khi tạo mới, sửa, bổ sung, thay thế, thiết kế hoặc kiến trúc một ý tưởng, tính năng hay dự án. (2) BÁM SÁT: dẫn chủ dự án đi qua một dự án đã hoặc đang xây cho tới khi họ thật sự nắm được: các phần nối nhau ra sao, tiền và dữ liệu đi đâu, các ngưỡng và quy ước nghĩa là gì, AI đã quyết thay họ những gì. Sản phẩm luôn là một tệp PDF. Dùng khi chủ dự án gõ "grillme", "grill me", "phỏng vấn tôi", "hỏi tôi cho rõ", "tôi không hiểu", "giải thích cho tôi", "rối quá", "tôi muốn nắm/bám sát dự án", hoặc yêu cầu tổng quản làm grillme. Chỉ khởi động khi chủ dự án gọi. Tổng quản được nhắc đúng một câu khi thấy chủ dự án sắp duyệt một việc mức Cao mà có vẻ chưa rõ. Không dùng cho tra cứu nhanh hay sửa lỗi nhỏ đã rõ.
---

# grillme — để chủ dự án và tổng quản hiểu nhau trọn vẹn

Thiết kế theo Bản hiểu chung chủ dự án xác nhận ngày 15/11/2026 (`D:\CLAUDE PROJECTS\docs\yeu-cau\2026-11-15-grillme-hoan-thien.md`).

## Vì sao có skill này

Chủ dự án nói: grillme là "phương tiện để tôi bám sát được dự án cùng với các tổng quản". Họ cũng nói thẳng điều tối kỵ: "sự thiếu chặt chẽ, suy tưởng, mơ hồ, khuếch đại, dẫn dắt mà không khách quan, không có biện chứng rõ ràng … thì dù hỏi vài trăm câu, cũng chỉ dẫn tới 1 tập hồ sơ sáo rỗng, không có khả năng thực hiện được."

Vì vậy giá trị của grillme nằm ở **chất lượng lập luận**, không nằm ở số câu hỏi. Mỗi câu hỏi phải đổi được một quyết định. Mỗi khẳng định phải biết nó đến từ đâu. Mỗi phương án phải chịu được phản biện.

## Hai chế độ

| Chế độ | Khi nào | Sản phẩm (PDF) |
|---|---|---|
| **PHỎNG VẤN** | Trước khi làm: ý tưởng mới, sửa, bổ sung, thay thế, thiết kế | Bản hiểu chung + sơ đồ kế hoạch |
| **BÁM SÁT** | Dự án đã hoặc đang xây; chủ dự án thấy rối; sắp duyệt việc lớn | Sổ tay chủ dự án + sơ đồ dự án |

"Tôi muốn làm, thêm, đổi…" thì chọn PHỎNG VẤN. "Tôi không hiểu, rối quá, giải thích cho tôi…" thì chọn BÁM SÁT. Hai chế độ chuyển qua lại được. **BÁM SÁT:** đọc `references/che-do-bam-sat.md`. Phần chung dưới đây áp cho cả hai chế độ.

---

## PHẦN CHUNG (bắt buộc ở cả hai chế độ)

### 1. Khung lập luận 4 phần
Chủ dự án chọn cả 4 phần. Mọi **phương án** và mọi **kết luận** đưa cho chủ dự án phải có:
1. **Nhãn** cho từng khẳng định. Khẳng định là câu nêu sự kiện hoặc đánh giá về dự án hay về phương án.
   - **[Lời ông]:** chủ dự án nói hoặc chọn. Trích nguyên văn khi có thể.
   - **[Sự thật]:** có nguồn kiểm được. Ghi nguồn: tệp và dòng, commit, link, ngày tra.
   - **[Suy luận]:** rút ra từ các ý trên. Nói rõ rút ra từ ý nào.
   - **[Phỏng đoán]:** chưa có căn cứ, kể cả mọi ước tính về thời gian và chi phí.

   Không trộn nhãn trong một câu. **Phạm vi:** mọi gạch đầu dòng hay câu văn nêu sự kiện, con số hoặc đánh giá đều phải có nhãn; tiêu đề và dòng thông tin đầu tệp thì không cần. Trong bảng có cột "Nguồn" thì nguồn ở cột đó thay cho nhãn [Sự thật] của dòng; dòng không có nguồn phải ghi nhãn khác. Kiến thức nhớ mà chưa tra lại (ví dụ một bài báo khoa học) gắn [Phỏng đoán], hoặc tra rồi gắn [Sự thật]. **Trước khi gửi phản biện, tự rà lại mọi câu có con số**: chạy thử cho thấy đây là chỗ hay sót nhãn nhất. Ý nào do tổng quản đề xuất mà chủ dự án chưa duyệt thì gắn **[Đề xuất]**, và không được nằm trong mục "quyết định đã chốt".
2. **Phản biện mạnh nhất:** lý lẽ tốt nhất CHỐNG lại phương án này, và các phương án khác bị loại vì sao. Phản biện phải đủ sức làm phương án lung lay; một phản biện yếu dựng lên cho dễ bác bỏ là gian.
3. **Khi nào phương án sai:** điều kiện nào xảy ra thì nó hỏng, và dấu hiệu nào giúp phát hiện sớm.
4. **Con số thay tính từ.** "Tốt hơn, nhanh, an toàn, mạnh, tối ưu, đáng kể…" phải đi kèm con số. Chưa có số thì ghi "chưa đo". Không dùng từ khuếch đại ("cực kỳ", "hoàn hảo", "đột phá").

### 2. Mức hậu quả quyết định độ nặng của quy trình
Đầu buổi, ghi mức của việc để chủ dự án sửa nếu thấy sai:
- **Cao:** đụng tiền thật, dữ liệu người khác, pháp lý, sức khỏe, kết luận lời/lỗ hay đi tiếp/dừng, hoặc khó đảo ngược. **Mọi câu về gu trình bày, bố cục cũng chạy đủ quy trình.**
- **Vừa:** đổi cách làm hoặc chi phí, đảo ngược được. Chạy đủ quy trình.
- **Thấp:** chỉ tài liệu, tên gọi, chỉnh nhỏ đã rõ. Chỉ cần khung 4 phần; không cần phản biện, không cần PDF.

### 3. Ba kiểu rối và cách xử lý
| Kiểu | Dấu hiệu | Cách xử lý |
|---|---|---|
| **A. Gu trình bày, bố cục** | "gần đúng mà thiếu cái gì đó", khó tả bằng lời | Trước khi phác, đọc lại mọi yêu cầu cũ của chủ dự án về phần này (CHANGELOG, sổ quyết định), để không vẽ ngược ý cũ. Dựng **bản 0 "sửa tối thiểu"** làm đối chứng, cộng **2–3 bản phác thật**. **Mỗi bản thử một giả thuyết** về "cái còn thiếu", và chỉ đổi một trục (bố cục, mật độ thông tin, hoặc thứ tự đọc), để biết chủ dự án thích thay đổi nào. Trình bày theo thứ tự trục, không xếp hạng, không gắn [Đề xuất]. Mỗi bản ghi điểm yếu của nó; rủi ro chung của mọi bản thì ghi riêng. Cắt ảnh gọn. Kèm **ví dụ sản phẩm thật** bên ngoài: trang đã mở đọc được thì gắn [Sự thật] kèm link; chỉ thấy qua kết quả tìm kiếm thì gắn [Phỏng đoán]. Hỏi chủ dự án có ví dụ nào tự ưng không. Gu đã chốt (bản được chọn và lý do chủ dự án nêu) **ghi vào sổ** để lần sau không phải chỉ lại |
| **B. Quy ước, ngưỡng không hiểu** | "t > 2,85 thì đạt hay sao đó" | Con số chủ dự án nhắc có thể không được in ở đâu mà do mã tự tính ra (ví dụ mốc t tự nâng theo số cách thử), nên tìm cả trong công thức, không chỉ tìm chữ. Với mỗi ngưỡng: nghĩa là gì, bằng lời đời thường; vì sao chọn đúng số đó, ghi 1 trong 3 loại: **có nguồn** / **AI đặt** (có bằng chứng như commit hay ghi chú) / **không rõ ai đặt**; **1 ví dụ đạt + 1 ví dụ không đạt** bằng số thật của dự án (không có số thật thì ghi "chưa có số thật" và nói cách lấy); đổi ngưỡng thì kết quả đổi ra sao. **Hai nơi ghi cùng một ngưỡng mà khác nhau** (mã một số, tài liệu một số) thì nêu ngay, mức Cao. Ngưỡng không có căn cứ thì hỏi chủ dự án giữ hay đổi |
| **C. Thiếu chuyên môn** | lĩnh vực chủ dự án không quen | Tổng quản **đóng vai chuyên gia**: liệt kê những câu người trong nghề sẽ hỏi, những bẫy hay gặp, kèm nguồn, rồi hỏi chủ dự án từng điểm. Điểm không có nguồn thì gắn [Phỏng đoán]. Ở chỗ dính trách nhiệm pháp lý hoặc sức khỏe, thêm dòng **[Đề xuất] nên có người thật xác nhận**; chủ dự án quyết có thuê hay không |

### 4. Phản biện độc lập (mức Cao và Vừa)
Trước khi bất kỳ PDF nào tới tay chủ dự án:
1. Gọi một subagent (Agent tool) chạy **mô hình khác** với mô hình đang viết. Ví dụ: bên viết là Opus thì dùng `model: "sonnet"`; bên viết là Sonnet thì dùng `"opus"`. Phiên phản biện chỉ đọc bản viết và mã, tài liệu của dự án; **không đọc cuộc phỏng vấn**, để không bị kéo theo cách nghĩ của bên viết.
2. Giao cho phiên phản biện đúng bộ tiêu chí sau và yêu cầu trả lời bằng tiếng Việt, mỗi điểm có trích dẫn và mức Cao/Vừa/Thấp:
   - lấy mẫu 20 khẳng định: câu nào thiếu nhãn hoặc sai nhãn;
   - chỗ nào bên viết chèn ý của mình làm như lời chủ dự án;
   - tính từ hoặc so sánh nào thiếu con số;
   - phương án nào thiếu phần 2 hoặc phần 3 của khung lập luận;
   - mâu thuẫn nội bộ;
   - **viết lại "phản biện mạnh nhất"** cho phương án chính nếu bản gốc đưa phản biện yếu;
   - điều chủ dự án đã nói mà bản viết bỏ sót.

   Phiên phản biện phải nêu **ít nhất 3 điểm yếu có trích dẫn**. Trả về "không có gì" thì coi là phản biện chưa đạt và chạy lại.
3. Bên viết sửa theo phản biện. Biên bản phản biện và những gì đã sửa đưa vào PDF, mục "Phản biện".

### 5. Kiểm hiểu (chủ dự án chọn cả hai cách)
- **Câu tình huống:** 2–3 câu dạng "nếu X xảy ra thì phần nào bị ảnh hưởng, ông sẽ quyết gì?". Đây không phải câu đố mẹo.
- **Ông kể lại 3 điều** bằng lời của mình: việc này làm gì; tiền và dữ liệu đi đâu; ông phải duyệt gì. Tổng quản so với thực tế và chỉ ra chỗ lệch.

Lệch chỗ nào thì giải thích lại theo cách khác (ví dụ khác, sơ đồ khác), không nhắc lại y câu cũ. Ghi kết quả vào PDF.

### 6. Sản phẩm: PDF
- Viết bản Markdown theo mẫu trong `assets/`, rồi chuyển sang PDF bằng `python <thư mục skill>/scripts/md_to_pdf.py <vao.md> <ra.pdf>` (script dùng Edge có sẵn, không cần cài gì thêm).
- Tên tệp có số phiên bản: `…-v1.pdf`, `…-v2.pdf`. **Trang 1 ghi số phiên bản, ngày, và "Thay đổi so với bản trước".**
- Gửi chủ dự án ngay trong khung chat (SendUserFile, nếu có). Lưu cả Markdown lẫn PDF trong `docs/` của dự án; việc lưu đi theo quy trình commit của dự án.
- Có thay đổi thì xuất bản PDF mới. Không sửa đè bản cũ đã gửi.
- **Ngưỡng nặng** (chủ dự án duyệt): một buổi không quá **45 phút**; **PDF chính** không quá **6 trang**, phần "Đọc trong 1 phút" gói trong 1 trang. Biên bản phản biện, chi tiết kỹ thuật và từ điển được đưa sang **PDF phụ lục** (cùng số phiên bản, tên `…-phu-luc.pdf`). Vượt ngưỡng thì tách buổi.
- **Không lưu được vào repo** (chạy thử chỉ đọc, hoặc dự án chưa có `docs/`): lưu ở thư mục tạm, ghi rõ chỗ lưu trên trang 1, và đề xuất chỗ lưu chính thức.

### 7. Nguyên tắc hỏi
1. **Tự tìm trước, hỏi sau.** Đọc CLAUDE.md, README, `docs/` (gồm `docs/quan-tri/`), sổ quyết định, CHANGELOG, các nhánh chưa gộp, lịch sử git. Kiểm `git rev-parse --is-shallow-repository`: nếu repo là bản sao rút gọn (không đủ lịch sử) thì ghi rõ hạn chế này. Không hỏi điều tự tra được.
2. **Một câu hỏi = một quyết định.** Mỗi lượt 1–4 câu, câu quan trọng nhất đứng trước.
3. **Lựa chọn và đề xuất.** Câu về *cách làm* thì dùng AskUserQuestion: 2–4 phương án, mỗi phương án kèm hệ quả bằng con số nếu có; được gắn "(Đề xuất)" khi có căn cứ. Câu về *mục tiêu, mong muốn, gu, ai dùng* thì **không** gắn "(Đề xuất)". Câu cần chủ dự án kể thì hỏi mở.
4. **Câu chốt hướng hỏi sớm**: câu mà trả lời khác đi thì nền móng khác hẳn (dùng trong nhà hay để bán; một hay nhiều người dùng; có trẻ em không).
5. **"Tôi chưa biết" là câu trả lời hợp lệ.** Đề xuất một mặc định an toàn, ghi thành câu hỏi mở.
6. **Không dẫn dắt.** Ý của chủ dự án có rủi ro thì nêu rủi ro một lần, bằng số, rồi để chủ dự án quyết.
7. **Bắt mâu thuẫn ngay** và hỏi khi buộc phải chọn thì cái nào thắng.
8. **Số lượt không giới hạn** (chủ dự án chọn). Chủ dự án nói "đủ rồi" thì dừng ngay. Kỷ luật: mỗi câu phải đổi được một quyết định. Câu tổng quản cân nhắc rồi **bỏ** thì ghi vào mục "Câu đã bỏ" kèm lý do, để chủ dự án xem lại. **Không bỏ câu về gu trình bày.** Câu chưa hỏi vì đã đủ 4 câu trong lượt thì ghi vào mục "Câu để lượt sau".
9. **Không làm trong lúc grillme.** Không viết mã sản phẩm, không sửa dự án, không mua, không tạo tài khoản. Chỉ được làm bản phác, PDF và ghi tài liệu.
10. **Tôn trọng chỉ đạo cũ** của chủ dự án; chỉ hỏi lại khi yêu cầu mới đi ngược chỉ đạo cũ.
11. **Không bao giờ hỏi mật khẩu, khóa API, số thẻ.** Chỉ hỏi có hay không, và cất ở đâu.

---

## CHẾ ĐỘ PHỎNG VẤN

### Bước 0: Chuẩn bị và mở đầu
- Tự tìm trước (mục 7, nguyên tắc 1). Xếp **loại** yêu cầu (bảng dưới) và **mức hậu quả** (mục 2).
- Tin mở đầu: nhắc lại điều đã hiểu trong 3–5 dòng có nhãn; liệt kê giả định; nói mức của việc; nói chủ dự án có thể dừng bất cứ lúc nào bằng câu "đủ rồi".

| Loại | Dấu hiệu | Trọng tâm hỏi |
|---|---|---|
| Tạo mới | "làm một…", "xây…" | Vì sao, cho ai, "xong" là gì, bản đầu (MVP) |
| Sửa | "lỗi", "sai", "chưa đúng" | Hiện tượng cụ thể, đúng là thế nào, ảnh hưởng ai, gấp tới đâu |
| Bổ sung | "thêm…" | Bài toán đằng sau tính năng, có đụng phần cũ không |
| Thay thế | "đổi sang…" | Vì sao đổi, giữ lại gì, đường lui, cách chuyển dữ liệu |
| Thiết kế / kiến trúc | "thiết kế", "hệ thống" | Ràng buộc, quy mô, ưu tiên khi xung đột, cái gì khó đảo ngược |

### Bước 1: Lập bản đồ những gì cần biết
Đọc `references/bo-cau-hoi.md`, mục 1 và mục của đúng loại yêu cầu. Đánh dấu từng chiều: đã rõ (kèm nguồn) / suy ra được (giả định cần xác nhận) / chưa biết. Chỉ hỏi chiều chưa biết mà trả lời khác đi thì cách làm khác đi.

### Bước 2: Các lượt hỏi
Thứ tự: **mục tiêu và lý do → tiêu chí "xong" → phạm vi và điều không muốn → ràng buộc → rủi ro và dữ liệu → chi tiết.** Ngoại lệ là câu chốt hướng, được hỏi sớm.

Sau mỗi lượt, tóm 1–2 dòng điều vừa chốt (gắn [Lời ông]), để chủ dự án sửa ngay nếu hiểu sai. Câu trả lời còn mờ thì dùng các kỹ thuật ở `references/bo-cau-hoi.md`, mục 7.

### Bước 3: Khi nào dừng
Đủ cả ba điều:
- mọi chiều bắt buộc đã rõ, hoặc đã thành câu hỏi mở có mặc định;
- không còn mâu thuẫn;
- tiêu chí "xong" kiểm được, tức đo được hoặc nhìn thấy được.

Hoặc chủ dự án nói "đủ rồi".

### Bước 4: Bản hiểu chung + sơ đồ kế hoạch → phản biện → PDF → xác nhận
1. Viết theo `assets/mau-ban-hieu-chung.md`, gồm **sơ đồ kế hoạch**: việc gì, phòng nào làm, tuần nào, mốc xong. Mọi ước tính thời gian gắn [Phỏng đoán].
2. Phản biện độc lập (mục 4), rồi sửa.
3. Xuất PDF (mục 6), gửi chủ dự án.
4. Kiểm hiểu (mục 5).
5. Hỏi xác nhận. Chủ dự án sửa thì ra bản PDF mới. Khi chủ dự án xác nhận, ghi nguyên văn câu xác nhận và ngày vào tệp.
6. Chỉ sau bước này mới bắt đầu làm. Bản hiểu chung là **căn cứ kiểm thu**.

## Liên hệ Bộ tiêu chuẩn chung (nếu dự án đang theo)
- Dự án hạng A: bắt buộc hỏi `references/bo-cau-hoi.md` mục 1.7 (dữ liệu và an toàn).
- Có dùng AI thì hỏi máy làm gì khi mất AI (quy tắc AI-04).
- Câu hỏi mở nào đụng quy tắc BẮT BUỘC thì ghi mã quy tắc.
- Tiêu chuẩn đặt ở `D:\CLAUDE PROJECTS\tieu-chuan\` (bản chép trong dự án: `docs/quan-tri/TIEU_CHUAN_CODE.md`).
