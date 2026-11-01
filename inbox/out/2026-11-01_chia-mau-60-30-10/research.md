# Research · Tập 19 bản 2 · Chia màu 60-30-10 (sổ tay AH+, chương 2 mục 2.4)

Bản 1 của tập 19 ("Đèn làm lệch màu gỗ", K.1, `inbox/out/2026-11-01_den-lech-mau-go/`) bị chủ Trang bỏ ngày 2026-11-01: "các animation sketch không phù hợp vì nó trình diễn các đối tượng phụ như ghế sofa… chứ không liên quan gì đến nội dung chính… Hãy làm lại hoặc chọn ví dụ khác, bài học khác dễ trình bày hơn, dễ hiểu hơn với số đông."
Chọn ý mới sao cho chính các món được nét vẽ lắp vào LÀ nội dung bài học: quy tắc 60-30-10 chia diện tích màu thành nền (trần, sàn, tường), khối phân vùng (một mảng màu phủ trọn một khu, như hệ tủ bếp) và điểm nhấn (ghế, đèn, vật dụng rời). Nét bay vào lần lượt là đúng ba tầng đó.

Bài kho: `AH-Decode-Decor/so-tay-cong-thuc-chon-mau-noi-that/03-chuong-2-khong-gian-mo.pdf`, mục 2.4 (tr. 25) và checklist 2.6 (tr. 29); nhánh AH-Interior-notes, commit `0deebf6381c57999600a4a4381cce35db97f3074`. Bản chữ: `original/so-tay/c2.txt`.
Khác các tập trước: tập 17 bản 1 (chương 2 mục 2.1–2.3 hình và nền, chủ Trang bỏ, chưa đăng) không nói 60-30-10; tập 5 (bài 01 "nền lùi, màu nhấn dồn vào một khối", Green Box) gần phần "khối 30%" nhưng không có tỷ lệ ba tầng, không có màu rực cho đồ rời, không có mốc chênh LRV 30 điểm. Ảnh mới hoàn toàn (First House, chưa tập nào dùng). Tập trước (18) dùng bài 05, nên sổ tay không trùng bài liền kề (mục 0.5b).

## A. Mở
- 2.4: "Khi đã chọn được các màu cho một căn hộ mở, câu hỏi tiếp theo là mỗi màu nên chiếm bao nhiêu diện tích."
## B. Nguồn gốc, mức chắc chắn
- 2.4: "Quy tắc 60-30-10 là một quy ước hành nghề phổ biến… Chúng mình không tìm thấy nguồn gốc của quy tắc trong tài liệu khoa học hay sách kinh điển, nên xem đây là điểm khởi đầu chứ không phải định luật." / "Mức bằng chứng: quy tắc 60-30-10 và mốc chênh lệch LRV 30 điểm là kinh nghiệm hành nghề."
## C. Cơ chế, nội dung quy tắc
- "60% là phần nền, gồm trần, sàn và các mảng tường bao. Phần này nên dùng màu sáng nằm trong dải LRV của TCVN 7114-1… để nối các khu vực thành một thể thống nhất."
- "30% là khối phân vùng, tức một mảng màu phủ trọn một khu vực, chẳng hạn toàn bộ hệ tủ bếp, hoặc mảng tường và trần của khu ăn."
- "10% là điểm nhấn, gồm ghế, đèn và các vật dụng rời. Phần này có thể dùng màu rực nhất." Checklist 2.6: "Màu rực chỉ dùng cho phần điểm nhấn 10%."
- "Tuy vậy, tỷ lệ diện tích thôi là chưa đủ, vì hai vùng chỉ tách nhau rõ khi chênh lệch độ sáng giữa chúng đủ lớn. Đối với các bề mặt cần phân biệt, hướng dẫn của Dulux Trade cho rằng chênh lệch LRV từ 30 điểm trở lên giúp nhận diện các bộ phận chính⁸. Vì vậy, hai màu khác sắc độ nhưng gần nhau về LRV sẽ phân vùng kém hơn so với dự kiến."
- Hình 2.2: mặt bằng khách, bếp, ăn theo 60-30-10; "LRV nền ≈ 81, khối ≈ 29, chênh ≈ 52 điểm (mốc ≥ 30)"; "Ô màu và số LRV chỉ là minh họa, tính từ mã HEX."
- Câu kéo: "Chia diện tích theo 60-30-10, rồi kiểm tra chênh lệch LRV giữa nền và khối phân vùng." Checklist: "Nền sáng và lặng, khối phân vùng rõ biên, điểm nhấn ít và rực."
## D. Đọc trên ảnh (ảnh ngoài sách, mục 0.6k; chủ Trang cho phép trong phiên)
- First House, Murcia · HANGHAR · ảnh Luis Díaz Díaz (ArchDaily). Nhìn trên ảnh: trần, sàn, tường trắng/sáng; cả khối tủ bếp và đảo bếp sơn xanh lá đậm (ảnh 15, 02); phòng bên có chiếc xô vàng, tấm thảm xanh dương đậm, chồng sách, ấm trắng (ảnh 12); phòng khác có ghế xếp gỗ vàng, ghế dây vàng (ảnh 13).
- Đo trên ảnh (RGB trung bình, xem `source_info.md`): tường trắng và khối xanh chênh độ sáng lớn. Không nói LRV của sơn thật (sách và trang ảnh không có).
## E. Lỗi hay gặp
- "hai màu khác sắc độ nhưng gần nhau về LRV sẽ phân vùng kém hơn"; Hình 2.3: "Tránh để mảng màu dừng lưng chừng".
## F, G. Áp dụng
- Câu kéo và checklist 2.6 như trên.
## H. Chốt
- Checklist: "Nền sáng và lặng, khối phân vùng rõ biên, điểm nhấn ít và rực."
## I. Cảnh cuối
- Mẫu tập 17 bản 3, 18.
