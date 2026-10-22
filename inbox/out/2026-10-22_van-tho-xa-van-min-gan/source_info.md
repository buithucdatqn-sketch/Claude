# source_info.md · Tập 10 (bản 3)
Kho: github.com/buithucdatqn-sketch/A---material, nhánh AH-Interior-notes, commit 6d869f9a07f7186a0d5a3543bdb027671437b4b4, bài 02.
Ảnh ngoài bài: bộ ảnh MS House trên ArchDaily (https://www.archdaily.com/1032005/ms-house-studio-saransh), chủ Trang cho phép ngày 2026-10-22. Chỉ lấy ảnh và credit, không lấy chữ. URL từng ảnh: `original/archdaily/urls.txt`; ảnh gốc: `original/archdaily/`.
Credit ảnh công trình (bài và ArchDaily ghi giống nhau): MS House, Ahmedabad · Studio Saransh · ảnh Ishita Sitwala, The Fishy Project.

| Ảnh | Nguồn, loại | Cảnh | Đã dùng ở tập trước? | Xử lý, doodle |
|---|---|---|---|---|
| ArchDaily 39 | mặt ngoài nhìn từ vườn | 1 (câu móc, khung thẻ rộng) | chưa | không nét |
| anh/10-diagram-ty-xich-khoang-cach.png | diagram của bài | 2, 3 (hàng trên), 12 (dòng kết) | chưa | cắt dải `source_dgt.png`, `source_dgc.png` |
| ArchDaily 26 | mặt ngoài nhìn xa, tường vân cốp pha | 4, 13 (khung cuối) | chưa | nét mới: khung đứt bao mảng tường + nhãn "sọc mảnh, nhìn êm" |
| ArchDaily 24 | tường bê tông nhìn sát | 5 | chưa | nét mới: nhãn "gờ, lỗ bọt khí", mũi tên, vòng bao hàng lỗ bọt khí |
| anh/11-doodle-van-tho-hanh-lang.jpg | ảnh của bài, hành lang lối vào | 6 | CÓ, tập 7 (chủ Trang cho dùng lại) | nền sạch (đã xoá nét gốc ở tập 7) + nét mới: khung bao mảng tường cạnh cửa, nhãn "vân cốp pha to, chỗ đi qua", mũi tên |
| ArchDaily 29 | phòng khách | 7 (khung thẻ) | chưa | nét mới: khung bao mảng tường sau, nhãn "bê tông ván ép, mặt mịn" |
| anh/03-mat-bang-tang-mot-ms-house.png | mặt bằng của bài | 8 | chưa | cắt vùng hai phòng ngủ tầng một, chú thích gốc |
| ArchDaily 6 | phòng ngủ con gái | 9 (khung thẻ, cắt nửa dưới `source_a6c.png`) | chưa | nét mới: nhãn "ô đá nhỏ lặp lại" trên mảng gỗ, mũi tên, vòng bao sàn ô đá |
| ArchDaily 35 | cổng lối vào | 10 (khung thẻ, cắt nửa dưới `source_a35c.png`) | chưa | nét mới: khung bao dải tường cổng, nhãn "vân rõ ở lối vào", mũi tên ngắn |
| anh/12-doodle-van-nho-phong-ngu.jpg | ảnh của bài, phòng ngủ (kệ, tường vôi) | 11 | chưa | nền sạch (make_layers_ep10.py) + nét mới: nhãn "tường trát vôi mịn", mũi tên |

Nét doodle vẽ bằng `engine_ep10/draw_ep10.py` (nét trắng, nét đứt, rung tay, góc vẽ lố), lưu `doodle_ep10_<ảnh>.npz` theo đúng thứ tự vẽ để engine lộ dần; ảnh xem thử ở `doodle_preview/`. Mỗi ảnh chỉ dùng ở một hoặc hai cảnh; ba không gian trở lên (mặt ngoài, hành lang, phòng khách, phòng ngủ, lối vào).

## Hạn chế
- Nhãn gốc vẽ sẵn trên ảnh 11 và 12 của bài nằm sát mép ảnh nên không dùng; thay bằng nét vẽ mới đặt giữa dải an toàn (y 610–1240).
- Ảnh phòng khách, phòng ngủ, lối vào có vùng cần chỉ nằm sát đáy ảnh, nên dựng bằng khung thẻ (ảnh giữa khung, chữ nâu ở ngoài) để nhãn nằm trong dải an toàn; nhãn trên thẻ nhỏ hơn cảnh zoom kín (khoảng 40–55 px).
