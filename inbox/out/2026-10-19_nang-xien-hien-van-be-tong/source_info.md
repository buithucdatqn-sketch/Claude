# Ảnh nguồn · Tập 6

- Ảnh trong kho: `AH-Decode-Decor/bai-02-3-bai-hoc-chat-cam-vat-lieu-noi-that/anh/04-doodle-nang-xien-ban-cong.jpg` (1667×2500, ảnh dọc 2:3). Nhánh `AH-Interior-notes`, commit `8fd09bdd396e0e27f055d6cba0816b568e47ea0e`. Bản gốc ở `original/`.
- Credit (theo YAML `cong_trinh`): MS House, Ahmedabad · Studio Saransh · ảnh Ishita Sitwala, The Fishy Project.
- Lý do chọn: ảnh loại (a), có doodle sẵn của bài, khớp đúng ý "chất cảm chỉ hiện rõ khi ánh sáng chiếu xiên" và câu hỏi mở "ảnh ấm, ngoài đời lạnh". Ảnh 04 chưa dùng ở tập nào (tập 4, 5 dùng ảnh của bài 01).
- Bản làm việc: `source.png` 1600×2400 (LANCZOS), đã xoá doodle bằng cv2.inpaint TELEA (mặt nạ nét trắng ≥250, lọc nét mảnh, chỉ trong các hộp của từng nét). `source_orig.png` còn doodle.
- Lớp nét: `engine_ep06/doodle_ep06.npz` gồm tia nắng nét đứt (dash1, dash2, burst), hai mũi tên (arr1, arr2) và hai nhãn gốc (lab1, lab2). Tiêu đề gốc "chất cảm cần ánh xiên", dòng phụ "nắng chéo qua tán cây, vân mới hiện" và dòng credit vẽ tay đã xoá khỏi nền, không dùng (engine in credit riêng).
- Hạn chế: mặt nạ nét trắng trên vùng nắng sáng/lá cây không tách hoàn toàn, nên đầu mũi tên nằm trên mảng nắng và các nét đứt cắt qua nắng có thể đứt đoạn hoặc thiếu vài đoạn khi lộ dần; chưa dựng video (chờ giọng đọc), cần xem kỹ lớp nền ở vùng tường nắng khi dựng.
