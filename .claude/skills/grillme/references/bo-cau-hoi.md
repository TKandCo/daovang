# Bộ câu hỏi grillme

Đây là kho để **chọn**, không phải danh sách để hỏi hết. Chỉ hỏi những chiều chưa rõ và quan trọng, tức là trả lời khác đi thì cách làm khác đi. Hỏi bằng lời đời thường, kèm ví dụ của chính dự án đó.

Mục lục:
1. Các chiều bắt buộc (mọi loại yêu cầu)
2. Tạo mới
3. Sửa
4. Bổ sung
5. Thay thế
6. Thiết kế / kiến trúc
7. Kỹ thuật làm rõ câu trả lời mờ
8. Dấu hiệu cần đào sâu thêm

---

## 1. Các chiều bắt buộc

### 1.1 Mục tiêu và lý do thật
- Việc này giải quyết chuyện gì cho ông? Hiện giờ chuyện đó đang diễn ra thế nào?
- Vì sao làm lúc này? Có sự kiện, hạn chót, hay ai đó đang chờ không?
- Nếu không làm thì điều gì xảy ra?

### 1.2 Ai dùng, ai chịu ảnh hưởng
- Ai trực tiếp dùng? (ông, gia đình, bạn bè, khách lạ, trẻ em, người lớn tuổi)
- Họ dùng ở đâu, lúc nào, bằng thiết bị gì? Có lúc tay bận, mắt bận, ồn ào không?
- Ai không dùng nhưng chịu ảnh hưởng? (người được chia sẻ, người có dữ liệu nằm trong hệ thống)

### 1.3 "Xong" trông như thế nào
- Ông nhìn thấy gì thì biết là xong và đúng ý?
- Có con số nào đo được không? (thời gian, tỷ lệ đúng, chi phí, số lần)
- Bản đầu tiên tối thiểu cần làm được gì? Phần nào để sau được?

### 1.4 Phạm vi và điều KHÔNG muốn
- Việc này **không** bao gồm gì?
- Có điều gì ông chắc chắn không muốn xảy ra, dù mọi thứ khác đúng?
- Có cách làm nào ông đã thử hoặc đã thấy và không thích không? Vì sao?

### 1.5 Ràng buộc
- Tiền: trần chi phí ban đầu và hằng tháng?
- Thời gian: cần trước ngày nào? Có mốc giữa chừng không?
- Công cụ, nền tảng: bắt buộc dùng hay tránh cái gì? (ví dụ: chạy trên máy nhà, không phụ thuộc AI, không thu phí)
- Ai duyệt cuối? Có việc nào phải hỏi trước khi làm không?

### 1.6 Ưu tiên khi xung đột
- Khi buộc phải chọn, cái nào thắng: rẻ / nhanh / chất lượng / an toàn / đơn giản?
- Nếu chỉ được giữ một điều trong danh sách mong muốn, đó là điều gì?

### 1.7 Dữ liệu và an toàn (bắt buộc với hạng A: tiền thật, sức khỏe, trẻ em, dữ liệu người khác)
- Hệ thống sẽ giữ dữ liệu gì về ai? Giữ bao lâu? Ai được xem?
- Có dữ liệu của trẻ em hoặc người ngoài gia đình không? Họ đã đồng ý chưa?
- Nếu thông tin sai (sai liều, sai tiền, sai số liệu) thì ai bị hại, hại tới đâu?
- Có thao tác nào khó đảo ngược không? (xóa dữ liệu, gửi tin cho người khác, đặt lệnh, chi tiền)
- Khi mất mạng, mất AI hay mất nhà cung cấp, hệ thống còn làm được gì?

### 1.8 Ảnh hưởng tới phần đã có
- Việc này đụng tới phần nào đang chạy? Có ai đang dùng phần đó không?
- Cần giữ tương thích với gì? (dữ liệu cũ, thói quen của người dùng, đường link đã chia sẻ)

---

## 2. Tạo mới
- Ông hình dung một ngày người dùng dùng nó: từ lúc mở ra tới lúc xong việc, kể từng bước.
- Thứ gần nhất với ý này mà ông từng thấy ở đâu? Giống ở điểm nào, khác ở điểm nào?
- Đây là để dùng trong nhà, để chia sẻ miễn phí, hay hướng tới bán? (câu trả lời đổi mức chặt chẽ cần có)
- Bản thử nhỏ nhất cho ông biết "ý này đáng làm tiếp" là gì?
- Nếu thành công, 6 tháng sau nó lớn tới đâu? (để biết có cần nền móng chắc ngay từ đầu không)

## 3. Sửa
- Ông thấy hiện tượng gì? Ở đâu, lúc nào, trên thiết bị nào? Có ảnh chụp hoặc câu báo lỗi không?
- Lẽ ra phải đúng thế nào?
- Lỗi xảy ra mỗi lần, hay thỉnh thoảng? Bắt đầu từ khi nào? Lúc đó có gì vừa thay đổi?
- Ai đang bị ảnh hưởng? Gấp tới mức nào: chặn ngay, trong tuần, hay gom vào đợt sau?
- Có cách tạm nào đang dùng không?

## 4. Bổ sung
- Tính năng này giúp ông làm được việc gì mà hiện giờ chưa làm được? (hỏi ra bài toán, không chỉ tính năng)
- Có cách nào đơn giản hơn để đạt cùng mục đích không? Ông có chấp nhận cách đó không?
- Nó nằm ở đâu trong cái đang có? Có thay đổi thói quen của người đang dùng không?
- Nếu nó làm phần cũ chậm hơn, phức tạp hơn hay đắt hơn, ông chấp nhận tới đâu?

## 5. Thay thế
- Điều gì ở cái cũ làm ông muốn đổi? Kể một lần cụ thể.
- Cái cũ có điểm nào tốt cần giữ lại?
- Chuyển dữ liệu, cài đặt, đường link cũ ra sao? Có được phép mất gì không?
- Nếu cái mới không như kỳ vọng thì quay lại cái cũ bằng cách nào? Giữ cái cũ bao lâu?
- Chạy song song một thời gian, hay chuyển hẳn một lần?

## 6. Thiết kế / kiến trúc
- Quy mô: bao nhiêu người dùng, bao nhiêu dữ liệu, bây giờ và 1 năm nữa? (ước lượng là đủ)
- Hệ thống chạy ở đâu? Ai bảo trì khi không có Claude?
- Phần nào ông muốn thay được dễ dàng về sau? (nhà cung cấp AI, nơi lưu, giao diện)
- Quyết định nào khó đảo ngược nhất? Cần cân nhắc kỹ từ bây giờ.
- Chi phí vận hành hằng tháng chấp nhận được là bao nhiêu? Vượt thì làm gì?
- Có hệ thống nào khác cần nối vào không? (dự án khác của ông, dịch vụ ngoài)

---

## 7. Kỹ thuật làm rõ câu trả lời mờ

| Khi chủ dự án nói… | Thử hỏi… |
|---|---|
| "Làm cho tốt / chuyên nghiệp" | "Tốt nghĩa là gì với ông? Có ví dụ nào ông thấy là tốt không?" |
| "Đơn giản thôi" | "Đơn giản cho người dùng, hay đơn giản để làm? Hai cái đó đôi khi ngược nhau." |
| "Như cái X" | "Giống X ở điểm nào? Có điểm nào của X ông không muốn?" |
| "Tùy ông" | Đưa đề xuất cụ thể kèm lý do, hỏi "Tôi làm thế này nhé?" Ghi là giả định đã được đồng ý. |
| "Càng nhiều càng tốt" | "Nếu chỉ được 3 cái trước, ông chọn 3 cái nào?" |
| "Nhanh" | "Nhanh là trong vài giây khi dùng, hay xong việc trong vài ngày?" |
| "An toàn" | "An toàn khỏi điều gì: mất dữ liệu, lộ thông tin, hay thông tin sai gây hại?" |
| Hai mong muốn chọi nhau | "Hai điều này kéo về hai phía: [A] và [B]. Khi buộc phải chọn, cái nào thắng?" |

**Tiền-khám-nghiệm:** "Giả sử 3 tháng sau ông nói 'việc này hỏng rồi'. Lý do có khả năng nhất là gì?" Câu trả lời thường lộ ra rủi ro thật và tiêu chí "xong" mà chủ dự án chưa nói.

**Hỏi "vì sao" tới gốc:** dừng khi chạm tới mục tiêu cuộc sống hoặc công việc cụ thể (tiết kiệm thời gian cho ai, tránh rủi ro gì, kiếm được gì). Thường 2–3 tầng là đủ.

---

## 8. Dấu hiệu cần đào sâu thêm
- Chủ dự án dùng từ cảm tính ("hay", "xịn", "mượt") mà chưa có ví dụ.
- Câu trả lời có "chắc", "có lẽ", "tạm thời".
- Có người thứ ba (gia đình, khách, bạn bè) nhưng chưa rõ họ cần gì.
- Có chữ "tự động" đi cùng tiền, sức khỏe, gửi tin, hay xóa.
- Ước lượng chi phí hoặc thời gian của chủ dự án khác xa ước lượng của mình.
- Yêu cầu có vẻ đi ngược một chỉ đạo cũ trong tài liệu dự án.
