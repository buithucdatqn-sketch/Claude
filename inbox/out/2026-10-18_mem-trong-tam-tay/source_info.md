# Ảnh nguồn · Tập 7

- Ảnh chính: `AH-Decode-Decor/bai-02-3-bai-hoc-chat-cam-vat-lieu-noi-that/anh/08-doodle-tho-min-phong-khach.jpg` (1667×2500, dọc 2:3), nhánh `AH-Interior-notes`, commit `8fd09bdd396e0e27f055d6cba0816b568e47ea0e`. Dùng cho cảnh 1–6, 8–10.
- Ảnh phụ: `.../anh/09-doodle-go-o-gan-phong-ngu.jpg` (2500×1669, ngang 3:2), cùng commit. Dùng cho cảnh 7 (phòng ngủ), dựng bằng engine phụ `engine_ep07/engine_video_ep07_ngu.py` rồi ghép (mục 5d).
- Bản gốc ở `original/`. Bản làm việc: `source_orig.png` (1600×2400, còn doodle), `source.png` (nền đã xoá nét); `source_ngu_orig.png` (2400×1602), `source_ngu.png`.
- Credit (YAML `cong_trinh`): MS House, Ahmedabad · Studio Saransh · ảnh Ishita Sitwala, The Fishy Project. Bài không ghi ai dựng doodle nên không thêm "Giả Thuyết Kiến Trúc".
- Lý do chọn: hai ảnh loại (a), doodle gốc khớp đúng ý "cứng ở xa, mềm trong tầm tay" (ảnh 08: "trần, tường bê tông ván ép mặt mịn và cứng", "sofa vải xù dày", "khung gỗ teak"; ảnh 09: "ốp gỗ đầu giường", "dãy tủ gỗ sát lối đi"). Chưa dùng ở tập nào. Ảnh 04 (nắng xiên) không dùng vì ý ánh sáng xiên đã bỏ theo yêu cầu chủ Trang.
- Tách lớp: `engine_ep07/make_layers.py`. Chữ trên trần, tường bê tông: inpaint TELEA (ảnh 08) hoặc lấy hạt bê tông quanh nét (ảnh 09); mũi tên trên sofa vải xù: lấy hạt vải ngẫu nhiên quanh nét (inpaint thường để lại vệt nhoè); mũi tên qua cột gỗ, tủ gỗ vân dọc: lấp theo cột; mũi tên trên ván đầu giường nằm ngang: lấp theo hàng. Đã xem lại bằng mắt: nền sạch.
- Lớp nét: `doodle_ep07.npz` (arr_vo, lab_vo, arr_sofa, lab_sofa; tách sẵn nhưng chưa dùng: lab_teak, arr_teak, title, sub, credit), `doodle_ep07_ngu.npz` (arr_dau, lab_dau; chưa dùng: lab_tu, arr_tu, title, sub, credit). Mũi tên lộ từ đuôi tới đầu.
- Hạn chế: chỗ nhãn "ốp gỗ đầu giường" trên tường bê tông ảnh 09 còn hơi loang khi nhìn sát, nhưng nhãn gốc hiện lại đè đúng chỗ đó trong cảnh 7. Công tắc đèn đầu giường bị đầu mũi tên gốc chạm vào nên mép trên hơi nhoè.
