# Ảnh nguồn · Tập 4

- Ảnh trong kho: `AH-Decode-Decor/bai-01-3-bai-hoc-phoi-mau-noi-that-can-ho/anh/07-doodle-tuong-phan-thu-vien.jpg` (1875×2500, ảnh dọc 3:4). Nhánh `AH-Interior-notes`, commit `65b5427c55046c43f02d8e7ec0829e03ae0fdd03`. Bản gốc chép ở `original/`.
- Credit (theo YAML `cong_trinh` của bài): The Green Box, Berlin · Ester Bruzkus Architekten · ảnh Robert Rieger. Bài không ghi doodle ảnh 07 là do chủ Trang dựng, nên credit không thêm "Giả Thuyết Kiến Trúc".
- Lý do chọn: ảnh loại (a), có doodle sẵn của bài và khớp đúng ý chính (mục "Chênh sáng mới làm đồ vật hiện ra": kệ xanh đậm, gáy sách sáng). Có thêm mảng ốp sọc cạnh cánh tủ sơn phẳng để minh hoạ "cùng màu, khác bề mặt".
- Bản làm việc: thu nhỏ còn 1800×2400 (LANCZOS). `source_orig.png` là bản thu nhỏ còn nguyên doodle. `source.png` là lớp nền đã xoá doodle.
- Cách xoá: dò lại đường elip gốc dọc theo pháp tuyến rồi làm mượt, chỉnh tay đoạn đầu bên phải. Sau đó inpaint (OpenCV TELEA) theo một dải mảnh 7–13 px. Riêng mũi tên và nhãn chữ thì lấy mặt nạ pixel trắng trên nền xanh. Nẹp đứng dưới nhãn được chép lại từ các hàng ngay phía trên.
- Lớp nét: `engine_ep04/doodle_ep04.npz` gồm ba phần. (1) Đường elip gốc, theo thứ tự vẽ. (2) Pixel mũi tên, lộ từ đuôi tới đầu. (3) Pixel nhãn "gáy sách sáng hiện ra trước", hiện dần như nhãn chữ.
- Hạn chế:
  - Chỗ elip cắt ngang gáy sách còn vài vệt inpaint nhẹ, rõ nhất quanh sách "Genius of Flexibility", "Toscana" và chân hàng sách dưới. Thấy được khi zoom cảnh 6, còn ở cảnh 5 và 10 thì elip vẽ đè lên.
  - Nhãn gốc "tương phản sắc đô" thiếu dấu nặng (đúng ra là "sắc độ"), nên KHÔNG cho hiện và đã xoá khỏi nền.
  - Dòng credit vẽ tay trong ảnh đã xoá, vì engine in credit dưới ảnh.
