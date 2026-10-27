# Nhật ký Reels · Giả Thuyết Kiến Trúc (AH Decode)

Dữ liệu chi tiết từng tập nằm ở `inbox/series.json`. File này ghi ý và câu móc đã dùng để không lặp.

| Tập | Ngày | Bài kho | Ý đã dùng | Câu móc |
|---|---|---|---|---|
| 4 | 2026-10-15 | bai-01 | Chênh sáng mới làm đồ vật hiện ra | (xem script tập 4) |
| 5 | 2026-10-15 | bai-01 | Nền lùi lại, màu nhấn dồn vào một khối | "Giữa căn hộ này là một khối sơn xanh. Vì sao nó giữ được vai chính?" |
| 6 | 2026-10-16 | bai-01 (ảnh 12, cảnh 8 ảnh 11) | Cùng một màu, khác bề mặt (phần của ý "Một màu chủ đạo, hai màu phụ") | "Cùng một màu sơn, sao chỗ phẳng chỗ sọc nhìn lại khác nhau?" |
| 7 | 2026-10-18 | bai-02 (ảnh 06, 07, 11, 02, 08, 09, 13) | Cứng ở xa, mềm trong tầm tay (bài học 2: thô cạnh mịn) | "Nhà bê tông mộc lên ảnh thì đẹp, sao ở thật lại hay bị chê lạnh?" |
| 6b | 2026-10-16 | bai-01 (ảnh 13, 10, 11, 09, 03, 08) | Một màu chủ đạo, hai màu phụ đi vòng quanh | "Thêm màu thứ hai, thứ ba vào nhà, có bị rối mắt không?" |
| 8 | 2026-10-19 | bai-01 (diagram 01 + ảnh ArchDaily) | Màu đậm trên mảng lớn: diện tích và ánh sáng | "Sơn nguyên một khối tủ to màu xanh, ở lâu có thấy ngộp không?" |
| 9 | 2026-10-21 | bai-03 (ảnh 11, 10, diagram 01, 09, mặt bằng 02) | Bề mặt đón ánh sáng đầu tiên quyết định phòng sáng tới đâu (lần chạy này tự đặt "Tập 7", đánh số lại) | "Cùng một ô cửa, sao phòng sơn trắng sáng hẳn, còn phòng ốp gỗ lại tối?" |

| 10 | 2026-10-22 | bai-02 (ảnh 10, 03, 12, dùng lại ảnh 11; thêm ảnh ArchDaily 39, 26, 24, 29, 6, 35) | Độ thô của vân hợp khoảng cách nhìn và thời gian ở: chỗ đi qua vân to, chỗ ngồi lâu vân mịn (bài học 3 của bài 02; bản 2 chạy lại theo góp ý) | "Cùng một bức tường bê tông, sao đứng xa thấy êm, mà ngồi sát lại thấy nặng nề?" |
| 11 | 2026-10-23 | bai-03 (ảnh gốc 08, 06, 07; diagram 05; mặt cắt 04) | Lớp lọc ngay trong nhà: lam gỗ, rèm mỏng giữa kính và người (mục 2 đoạn cuối + lời khuyên cuối bài) | "Vì sao ánh sáng từ trên cao qua vách lam lại dịu hơn ánh sáng từ kính ngang tầm mắt?" (hai bản đầu "có cách nào ở giữa không?" và "ba giờ chiều, dãy nhà phố…" bị chủ Trang chê, không dùng) |

| 12 | 2026-10-26 | bai-04 (ảnh gốc 04, 05, 10; diagram 01; mặt bằng 03) | Đối xứng dành cho chỗ cần yên, như đầu giường (bài học 1 của bài 04; đã dựng video 71,25 giây) | "Phòng khách kê lệch hẳn, vậy vì sao đầu giường trong căn hộ này lại được kê đối xứng?" (bản đầu cùng ngày "Phòng khách kê lệch hẳn một bên, sao nhìn vẫn thấy cân?" bị bỏ vì làm sai instruction) |
Ý bị cấm (chủ Trang từ chối): "chất cảm chỉ hiện khi ánh sáng xiên" của bài 02 (ảnh 04, 05), các bản làm lại ngày 19/10 và 21/10 đều huỷ; "chỗ làm việc sáng gần đều, chỗ nghỉ được chênh sáng" của bài 03 (ảnh 12–16), từ chối 23/10.
Mã bài tiếp theo: tập 12. Tập 11 dùng bài 03, nên tập 12 lấy bài khác bài 03 (mục 0.5b). Bài 01 và bài 02 coi như đã hết ý mới; bài 03 chỉ còn ý "ánh sáng từ trên cao" (vị trí ô cửa, chủ Trang đã chuyển hướng khỏi ý này ngày 21/10). Cần chủ Trang thêm bài mới vào AH-Decode-Decor/ trước lần chạy sau.

Lần chạy 2026-10-25: DỪNG, không làm tập 12. Kho `AH-Decode-Decor/` (nhánh AH-Interior-notes, commit ffc360a) vẫn chỉ có bài 01, 02, 03; bài 01 và 02 hết ý mới, bài 03 trùng bài tập 11 (mục 0.5b) và chỉ còn ý đã chuyển hướng. Bài "cân bằng thị giác" mới chỉ là bản nháp trong `draft/` (README kho: không lấy từ draft/). Cần chủ Trang đưa bài mới vào `AH-Decode-Decor/bai-04-.../`. Mã bài tiếp theo vẫn là tập 12.

Lần chạy 2026-10-26: kho có bài 04 (cân bằng thị giác, Palmeira Apartment). Tập 12 dùng bài học 1 của bài 04. Bài 04 còn bài học 2 (kê lệch mà vẫn cân: lò sưởi lớn sáng màu và tranh sẫm, ảnh 06, diagram 02) và bài học 3 (kiểm tra cân bằng từ chỗ đứng và ngồi, ảnh 07, 08, 09). Mã bài tiếp theo: tập 13, phải lấy bài khác bài 04 (mục 0.5b); nếu bài 01–03 không còn ý mới thì báo chủ Trang trước khi làm bài 04 hai ngày liền.

Lần chạy 2026-10-27: DỪNG, không làm tập 13. Kho `AH-Decode-Decor/` (nhánh AH-Interior-notes, commit bd74e53) không có bài mới sau bài 04. Đã gộp mọi nhánh (mới nhất `claude/happy-mccarthy-k39xaa`, tập 12): mọi bài học của bài 01, 02, 03 đều đã dùng hoặc bị cấm (mục 0.3, 0.6e), không còn ý mức bài học để xen kẽ. Hai bài học còn lại nằm cả ở bài 04, bài của tập 12 ngày hôm trước, nên làm tập 13 từ bài 04 là vi phạm mục 0.5b (không cùng một bài hai tập liên tiếp) và ghi chú 2026-10-26 ("báo chủ Trang trước khi làm bài 04 hai ngày liền"). Chờ chủ Trang chọn: (1) thêm bài mới vào kho; hoặc (2) cho phép làm bài 04 bài học 2 (lò sưởi sáng màu cân với bức tranh sẫm, ảnh 06; bản đầu ngày 26/10 đã bỏ vì sai quy trình, ý chưa dùng) hoặc bài học 3 (kiểm tra cân bằng từ chỗ đứng và ngồi, ảnh 07, 08, 09). Mã bài tiếp theo vẫn là tập 13.

Lần chạy 2026-10-27 (tiếp, sau khi chủ Trang cho phép): tập 13 làm bài 04 bài học 2 (ngoại lệ có chủ ý so với mục 0.5b, bài 04 hai ngày liền). Giai đoạn A xong, chờ ghi âm. Chủ Trang đọc bản 4 và yêu cầu làm lại vì lời chỉ nói món to, món nhỏ và kể tên đồ, chưa phân tích màu đậm hay màu chìm vào nền và khoảng cách tới trục. Bản 6 cân từng món theo ba yếu tố, và đã thêm mục 6i vào TASK_INSTRUCTION. Giai đoạn B cùng ngày: ghép giọng chủ Trang gửi (82,29 giây), câu móc thu thành "…trông vẫn cân đối?", phụ đề sửa theo; video 83,9 giây.

Cập nhật bảng (thêm dòng):
| 13 | 2026-10-27 | bai-04 (ảnh gốc 06 ba dải; sơ đồ 01 khung bất đối xứng, sơ đồ 02; mặt bằng 03; ArchDaily 21) | Lò sưởi to mà màu chìm vào tường kem cân với cụm món nhỏ màu đậm (tranh đen xám, ghế gỗ đen) bên kia trục; hai món cùng xa trục nên lò sưởi hơn về độ to, tranh hơn về màu; sofa to mà chìm; tủ gỗ đậm gần trục; kê lệch quanh trục có sẵn, món to nhất có món cân lại (bài học 2 của bài 04, có sofa và tủ gỗ theo yêu cầu chủ Trang) | "Một bên phòng khách là chiếc lò sưởi rất to, bên kia treo một bức tranh nhỏ hơn, vậy vì sao căn phòng không nghiêng?" (hai bản đầu và bản trình bày "chỉ có một bức tranh… vẫn ngang nhau" bỏ vì nói quá bài) |
Mã bài tiếp theo: tập 14. Bài 04 còn bài học 3 (kiểm tra cân bằng từ chỗ đứng và ngồi, ảnh 07, 08, 09). Kho vẫn chưa có bài mới; tập 14 lấy bài khác bài 04 thì phải có bài mới (mục 0.5b), hoặc chủ Trang cho phép làm bài học 3 của bài 04 lần nữa.
