# Research · Tập 19 · Đèn làm lệch màu gỗ (sổ tay AH+, phần kết K.1)

Bài kho: `AH-Decode-Decor/so-tay-cong-thuc-chon-mau-noi-that/07-phan-ket-kiem-chung-tai-cong-truong.pdf` (trang sách 71–73, mục K.1 "Phép thử 1 - Soi mẫu dưới đúng loại đèn sẽ lắp"), kèm một câu của `06-chuong-5-ai-va-bang-mau.pdf` mục 5.3 (đồng sắc dị phổ, K.1 dẫn lại "Như đã nói ở mục 5.3"). Nhánh `AH-Interior-notes`, commit `0deebf6381c57999600a4a4381cce35db97f3074`. Link: https://github.com/buithucdatqn-sketch/A---material/tree/AH-Interior-notes/AH-Decode-Decor/so-tay-cong-thuc-chon-mau-noi-that
Bản chữ trích bằng pdftotext: `original/so-tay/07-phan-ket.txt`, `original/so-tay/06-chuong-5.txt`.

Chọn ý (mục 0.1, 0.5b, 0.6k, 0.6m): tập 18 dùng bài 05, nên tập 19 lấy sổ tay AH+. Nhật ký ghi phần sổ tay chưa làm ý chính: chương 5, K.1, K.3, phụ lục B4. K.3 (độ bóng) bỏ vì nửa quan trọng của nó là "ánh sáng xiên làm lộ khuyết tật", sát ý cấm mục 0.3. K.1 có tình huống phổ biến (màu duyệt ban ngày, sống buổi tối dưới đèn nhà mình), có số đo tra được (Ra, R9) và một hiểu lầm để bác (đèn có Ra khá cao vẫn hoàn màu kém với đỏ đậm, gỗ, da). Khác tập 16 (hướng nắng đổi màu sơn) và tập 17 bản 3 (thẻ nhỏ, tường lớn, K.2).

## A. Mở / tình huống
- K.1: "Chủ nhà thường duyệt thẻ màu dưới đèn văn phòng vào ban ngày, nhưng lại sống với bức tường đó chủ yếu vào buổi tối, dưới đèn LED của chính căn nhà, và hai tình huống chiếu sáng ấy có thể cho ra hai màu khác nhau."
- Câu kéo: "Màu đã duyệt dưới một ngọn đèn chưa chắc còn đúng dưới ngọn đèn khác."
## B. Nguồn gốc
- Ra, CRI theo CIE 13.3-1995 (cước chú ¹); California Energy Commission 2019 (²); TCVN 7114-1:2008 (⁵).
## C. Cơ chế
- 5.3 / K.1: "hai mẫu có phổ phản xạ khác nhau có thể trông giống hệt nhau dưới nguồn sáng này nhưng lại khác nhau dưới nguồn sáng khác, hiện tượng gọi là đồng sắc dị phổ⁶. Vì vậy, một mẫu sơn khớp với mẫu gỗ dưới đèn văn phòng chưa chắc còn khớp dưới đèn LED ấm của phòng khách."
- K.1: "Chỉ số hoàn màu chung Ra, thường gọi là CRI, được tính từ tám mẫu màu thử có độ rực vừa phải, trải đều quanh vòng sắc độ. Ngoài ra, CIE quy định thêm sáu mẫu bổ sung, mở đầu bằng một mẫu đỏ đậm¹. Chỉ số riêng của mẫu đỏ đậm này là R9, và R9 không nằm trong Ra. Vì vậy, một nguồn sáng có Ra khá cao vẫn có thể hoàn màu kém với màu đỏ đậm, nâu gỗ hay màu da."
- Hình PK.1: cùng cặp mẫu sơn và gỗ; dưới đèn sẽ lắp (Ra ≥ 90, R9 > 50) khớp, dưới đèn tạm Ra thấp lệch.
## D. Đọc trên ảnh (ảnh ngoài sách, mục 0.6k; cặp ảnh này chính sổ tay dùng ở K.1)
- Sổ tay K.1, chú thích ảnh: "Cùng một phòng và cùng vị trí máy ảnh, dưới ánh sáng ban ngày (trên) và đèn ấm lúc chạng vạng (dưới). Stage in Hayama, Kanagawa, Nhật Bản (Takanori Ineyama Architects, 2022). Ảnh: Koichi Torimura / ArchDaily."
- Đo trên ảnh ArchDaily _10 (ngày) và _21 (chạng vạng), RGB trung bình: mảng gỗ tường sau gần đèn tường (x 650–850, y 720–860) R−B 32 → 52 (ngả cam hơn), sáng 40 → 62; ghế đỏ (x 300–420, y 1180–1280) R−B 47 → 25, sáng 51 → 30 (sẫm lại, bớt đỏ); tường trắng bên phải không ngả vàng mà tối xám (238 → 62), nên KHÔNG nói "tường ngả vàng"; sàn ngả xanh xám (R−B 2 → −18), không đưa vào lời.
- Không nói gì về chỉ số hoàn màu của đèn trong nhà Hayama (sách không có).
## E. Lỗi hay gặp
- K.1 thao tác 2: "Không duyệt màu dưới đèn văn phòng hay đèn tạm của công trường."
## F. Áp dụng
- K.1: "Lấy thông số của đúng mẫu đèn sẽ lắp từ hồ sơ chiếu sáng hoặc nhãn sản phẩm, gồm Ra, R9 (nếu hãng công bố) và nhiệt độ màu." / "mang thẻ màu, mẫu sơn và mẫu vật liệu đến công trình, rồi chiếu bằng đúng mẫu đèn đó" / "Đặt mẫu sơn cạnh vật liệu sẽ đi cùng như gỗ, đá hay vải, rồi so sánh dưới cả ánh sáng ban ngày lẫn ánh đèn. Nếu cặp mẫu khớp dưới nguồn sáng này mà lệch dưới nguồn sáng kia, hãy đổi một trong hai trước khi đặt hàng."
## G. Chọn đồ (đèn)
- K.1: "TCVN 7114-1:2008 … ghi rõ rằng bóng đèn có Ra nhỏ hơn 80 không nên dùng cho nơi làm việc thường xuyên hoặc nơi có người ở lâu⁵. Như vậy, Ra 80 chỉ là mức sàn. Với mảng màu chủ đạo, gỗ, đá và tường trưng bày, mức tham chiếu Ra ≥ 90 và R9 > 50 của California là ngưỡng đặt hàng hợp lý hơn."
## H. Chốt
- Câu kéo K.1: "Duyệt màu dưới đúng ngọn đèn sẽ thắp mỗi tối, không phải dưới đèn phòng họp."
## I. Cảnh cuối
- Mẫu tập 17 bản 3 (sổ tay AH+): "… có trong sổ tay Kinh nghiệm chọn màu kiến trúc nội thất, mọi người xem ở phần bình luận nhá."
