# Ảnh nguồn · Tập 6 (làm lại với nhiều ảnh)
Cả ba ảnh nằm trong `AH-Decode-Decor/bai-01-3-bai-hoc-phoi-mau-noi-that-can-ho/anh/`, nhánh AH-Interior-notes, commit 65b5427c55046c43f02d8e7ec0829e03ae0fdd03. Bản gốc ở `original/`. Credit chung: The Green Box, Berlin · Ester Bruzkus Architekten · ảnh Robert Rieger.
| Ảnh | Dùng ở cảnh | Vai trò trong lời giảng | Doodle gốc được làm chuyển động |
|---|---|---|---|
| `13-doodle-anh-tong.jpg` (1875×2500, dọc) | 1, 2, 3, 4, 9, khung cuối | Thấy cả căn bếp: xanh phủ tường, tủ, trần là màu chủ đạo; ghế quầy bếp hồng là màu phụ quay lại | mũi tên và nhãn "ghế hồng màu phụ quay lại" |
| `10-doodle-hai-mau-am.jpg` (1875×2500, dọc) | 5, 6, 7 | Hai màu phụ: đồng vàng; đá hồng và thảm hồng tím; và hai màu ấy đặt cạnh nhau | ba mũi tên, hai nhãn |
| `11-doodle-dap-mau-bep.jpg` (2500×1875, ngang) | 8 | Màu chủ đạo tự lặp lại trên tường sơn, mặt đá vân, tủ ô liu | hai mũi tên, bốn nhãn |
- Lý do đổi: bản đầu chỉ dùng ảnh 10 (không có màu chủ đạo) nên người xem không hiểu "chủ đạo" là gì. Giờ mỗi khái niệm có ảnh thấy được khái niệm đó. Cả ba ảnh chưa dùng ở tập 4, 5.
- Bản làm việc: cạnh dài 2400 px; `source_<id>.png` là nền đã xoá doodle (mặt nạ pixel trắng trong từng hộp, ảnh 11 loại thêm khối trắng dày của nắp lọ, inpaint TELEA); `source_orig_<id>.png` còn doodle. Lớp nét: `engine_ep06/doodle_<id>.npz`. Tiêu đề gốc, nhãn tiêu đề và dòng credit vẽ tay trên ảnh đã xoá, không dùng. Dựng bằng `engine_ep06/prep_ep06.py`.
- Chuyển ảnh: chuyển mờ 0,7 giây (engine/multi_patch.py); cùng ảnh thì camera zoom như cũ.
- Hạn chế: cảnh 5 và 8 để lộ mép ảnh (nền trắng quanh thẻ) vì nhãn gốc nằm sát mép; chưa chạy lệnh qa an toàn riêng, chữ do engine dựng theo bố cục đã duyệt.
