# Ảnh nguồn · Tập 7 (bản 3, nhiều ảnh)

Kho: `buithucdatqn-sketch/A---material`, nhánh `AH-Interior-notes`, commit `8fd09bdd396e0e27f055d6cba0816b568e47ea0e`, thư mục `AH-Decode-Decor/bai-02-3-bai-hoc-chat-cam-vat-lieu-noi-that/anh/`. Bản gốc của mọi ảnh ở `original/`.

| Ảnh trong bài | Loại | Bản làm việc | Cảnh | Ghi chú |
|---|---|---|---|---|
| 06-doodle-bong-va-nham-sanh-an.jpg | doodle (xoá sạch) | source_an.png 2400×2398 | 1, 4 | nhãn gốc nói về ánh sáng, không khớp lời nên xoá hết |
| 07-diagram-can-can-tho-min.png | diagram của bài | source_dg.png 2160×930 (cắt hàng ba khung, bỏ tiêu đề lớn và dòng nguồn) | 2 | bắt buộc theo mục 2d |
| 11-doodle-van-tho-hanh-lang.jpg | doodle (xoá sạch) | source_hl.png 1600×2400 | 3 | nhãn gốc nói về tỷ xích vân (ý chưa dùng) nên xoá hết |
| 02-mat-bang-tang-tret-ms-house.png | mặt bằng | source_mb.png 1360×700 (cắt vùng phòng khách, sảnh ăn) | 5 | chú thích gốc "phòng khách", "sảnh ăn hai tầng" |
| 08-doodle-tho-min-phong-khach.jpg | doodle (lộ dần) | source.png 1600×2400 | 6, 7, 9 | lộ "trần, tường bê tông ván ép mặt mịn và cứng", "sofa vải xù dày" |
| 09-doodle-go-o-gan-phong-ngu.jpg | doodle (lộ dần) | source_ngu.png 2400×1602 | 8 | lộ "ốp gỗ đầu giường" |
| 13-doodle-anh-tong.jpg | doodle (lộ dần) | source_tong.png 1600×2400 | 10, 11, 12 | lộ "bê tông vân ván khuôn to thô, trên cao, ở xa", "bàn gỗ, lưng ghế mây mịn, ngay trong tầm tay" |

Credit trên khung (mỗi run một dòng credit riêng):
- Ảnh công trình: MS House, Ahmedabad · Studio Saransh · ảnh Ishita Sitwala, The Fishy Project (YAML `cong_trinh`).
- Diagram: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014).
- Mặt bằng: Studio Saransh, nguồn ArchDaily (2025) · ghi chú Giả Thuyết Kiến Trúc (theo dòng ghi trên chính ảnh mặt bằng của bài).

Ảnh ngoài bài (Yatzer): theo yêu cầu chủ Trang, instruction đã cho phép lấy thêm ảnh MS House từ https://www.yatzer.com/ms-house-ahmedabad-india-studio-saransh (YAML `nguon_anh_cong_trinh`). Lần chạy này KHÔNG lấy được: mạng của môi trường chặn yatzer.com (curl: proxy trả 403 CONNECT; WebFetch: không phân giải được tên miền). Bảy ảnh trong bài đã đủ mặt bằng, diagram và năm không gian.

Tách lớp: `engine_ep07/make_layers.py`. Chữ trên bê tông: lấy hạt bê tông quanh nét hoặc inpaint TELEA; mũi tên trên sofa vải xù: lấy hạt vải quanh nét; mũi tên qua cột, tủ gỗ vân dọc: lấp theo cột; qua ván đầu giường nằm ngang: lấp theo hàng.
Hạn chế: ảnh 13 còn vệt mờ dưới hai mũi tên ở bàn ăn (nét gốc hiện lại đè lên ở cảnh 11); ảnh 11 còn vệt rất nhẹ trên bậc thềm (ngoài khung camera); công tắc đầu giường ảnh 09 hơi nhoè ở mép trên.
