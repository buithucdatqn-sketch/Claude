# source_info.md · Tập 10
Kho: github.com/buithucdatqn-sketch/A---material, nhánh AH-Interior-notes, commit 6d869f9a07f7186a0d5a3543bdb027671437b4b4, bài 02.
Chỉ dùng ảnh trong `anh/` của bài 02 (không tải ảnh ngoài kho, theo prompt của lịch chạy).

| Ảnh kho | Loại | Dùng ở | Đã dùng ở tập trước? | Xử lý |
|---|---|---|---|---|
| anh/10-diagram-ty-xich-khoang-cach.png (2160x2080) | diagram | cảnh 2, 3 (hàng trên), 4 (hàng dưới), 12 (dòng kết) | chưa | cắt ba dải: `source_dgt.png` (hai căn phòng, đứng xa / đứng sát), `source_dgb.png` (hai vòng vân), `source_dgc.png` (dòng kết "vân thô để chỗ nhìn xa, vân mịn để chỗ ở gần"); bỏ tiêu đề |
| anh/03-mat-bang-tang-mot-ms-house.png (1846x1870) | mặt bằng | cảnh 8 | chưa | cắt vùng hai phòng ngủ tầng một và chú thích `source_mb.png` |
| anh/12-doodle-van-nho-phong-ngu.jpg (1667x2500) | ảnh công trình có doodle | cảnh 9, 11, 13 | chưa | thu nhỏ 1600x2400; xoá nét và chữ doodle bằng make_layers_ep10.py (TELEA, nền trát phẳng nên làm mờ nhẹ ở chỗ chữ) → `source_ph.png`; nét gốc đã tách vào `doodle_ep10_ph.npz` nhưng chưa dùng (xem hạn chế) |
| anh/11-doodle-van-tho-hanh-lang.jpg | ảnh công trình | cảnh 1, 5, 6, 7, 10 | CÓ, tập 7 (cảnh 3) | dùng lại nền đã xoá nét của tập 7 (`source_hl.png`) |

Credit ảnh công trình: MS House, Ahmedabad · Studio Saransh · ảnh Ishita Sitwala, The Fishy Project. Mặt bằng: Studio Saransh, nguồn ArchDaily (2025), ghi chú Giả Thuyết Kiến Trúc. Diagram: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014).

## Hạn chế (cần chủ Trang quyết định)
1. Kho không còn đủ ảnh mới của bài 02: chỉ ảnh 12 là ảnh công trình chưa dùng; ảnh 11 tập 7 đã dùng; ảnh 13, 06, 08, 09 của tập 7; ảnh 04, 05 thuộc ý bị cấm; ảnh 01 là diagram về ánh xiên. Reel chỉ có ảnh của HAI không gian (hành lang, phòng ngủ), thiếu yêu cầu ba không gian (mục 2d) và có một ảnh dùng lại (11), trái mục 0.5c của TASK_INSTRUCTION. Prompt của lịch chạy cấm lấy ảnh ngoài kho (archdaily.com, yatzer.com, v.v.), trong khi TASK_INSTRUCTION mục 2b cho phép lấy thêm ảnh của chính công trình từ trang nguồn. Tôi theo prompt (nghiêm hơn) và không tải ảnh ngoài. Muốn đủ ảnh: thêm ảnh MS House vào `anh/` của bài 02 hoặc xác nhận cho phép tải từ ArchDaily (hiện ArchDaily truy cập được).
2. Nhãn doodle gốc của ảnh 11 và 12 nằm sát mép trên hoặc mép dưới ảnh nên khi zoom kín ảnh không vào được dải chữ an toàn (y 340–1490) mà không lộ mép trắng; reel dùng cả hai ảnh như ảnh sạch, không lộ nét.
