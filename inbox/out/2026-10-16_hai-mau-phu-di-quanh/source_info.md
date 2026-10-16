# Ảnh nguồn · Tập 6 (làm lại lần 2: nhiều ảnh + ảnh định vị)
Cả sáu ảnh nằm trong `AH-Decode-Decor/bai-01-3-bai-hoc-phoi-mau-noi-that-can-ho/anh/`, nhánh AH-Interior-notes, commit 65b5427c55046c43f02d8e7ec0829e03ae0fdd03. Bản gốc ở `original/`.
| Ảnh | Loại | Cảnh | Vai trò |
|---|---|---|---|
| `09-truc-do-the-green-box.jpg` (1652×1167) | trục đo màu | 2, 12 | Cả căn hộ: khối xanh giữa nhà, vàng ở sofa và mảng ốp đồng, hồng tím ở thảm. Cảnh 12 khoanh hai chỗ có vàng bằng nét mực |
| `08-diagram-xanh-o-giua-am-di-quanh.png` (2160×2020) | sơ đồ khái niệm | 3 | Chú giải chủ đạo / phụ 1 / phụ 2 để giảng lý thuyết |
| `03-mat-bang-the-green-box.png` (3640×2200→2400×1451) | mặt bằng | 5, 8 | Định vị: khoanh bếp (cảnh 5) và phòng khách quanh thảm tròn (cảnh 8) bằng nét mực. Đã xoá tiêu đề và dòng nguồn in sẵn (engine in credit riêng) |
| `13-doodle-anh-tong.jpg` | ảnh chụp + doodle gốc | 1, 4, 6, 13 | Bếp: xanh phủ tủ và tường; ghế quầy bếp hồng tím quay lại |
| `11-doodle-dap-mau-bep.jpg` | ảnh chụp + doodle gốc | 7 | Màu chủ đạo lặp lại: tường sơn, mặt đá vân, tủ ô liu |
| `10-doodle-hai-mau-am.jpg` | ảnh chụp + doodle gốc | 9, 10, 11 | Phòng khách: đồng vàng, đá hồng, thảm hồng tím |
- Credit: ảnh chụp "Ảnh dự án: The Green Box, Berlin · Ester Bruzkus Architekten · ảnh Robert Rieger"; mặt bằng và trục đo "… (qua ArchDaily)" theo `nguon_anh_cong_trinh` trong YAML; sơ đồ 08 không in thêm vì ảnh đã in sẵn nguồn (Kilmer & Kilmer 2014, tr. 166–167; Beadle 2023).
- Thứ tự cảnh gom theo khu vực: bếp (5→6→7) rồi phòng khách (8→9→10→11), để người xem không nhảy qua lại.
- Bản làm việc: cạnh dài tối đa 2400 px, không phóng to. `source_<id>.png`; ảnh chụp có doodle thì nền đã xoá doodle (inpaint TELEA, đã xem lại) và lớp nét `engine_ep06/doodle_<id>.npz`. Dựng bằng `engine_ep06/prep_ep06.py`.
- Chuyển ảnh: chuyển mờ 0,7 giây; sang/ra khỏi cảnh mực thì nền chuyển từ ảnh sang giấy trắng theo cùng nhịp (engine/multi_patch.py).
- Hạn chế: trục đo 09 chỉ 1652 px nên khi zoom hơi mềm; trục đo không dán nhãn nên tên khu vực do lời đọc nói; vị trí ảnh chụp 10 (lò sưởi) chỉ nói chung là "phòng khách quanh thảm tròn" vì bài không nêu chính xác; cảnh 5, 8 để lộ mép mặt bằng; chưa chạy lệnh qa an toàn riêng.
