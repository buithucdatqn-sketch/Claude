# Ảnh · tập 13

Kho: `buithucdatqn-sketch/A---material`, nhánh `AH-Interior-notes`, commit `bd74e5309164916cffb99e784b36711b2b82f7f2`, thư mục `AH-Decode-Decor/bai-04-3-bai-hoc-can-bang-thi-giac-noi-that/anh/`. Bản gốc chép trong `original/kho/`.
Một ảnh ngoài kho (mục 0.6d: được lấy thêm ảnh của chính công trình): ArchDaily, trang https://www.archdaily.com/1010507/palmeira-apartament-studio-gameiro (trang bài ghi ở `nguon_anh_cong_trinh`), ảnh số 21 (`palmeira-apartment-studio-gameiro_21.jpg`, bản large_jpg 2000 px, nhiếp ảnh gia ghi trên trang: Francisco Nogueira). Chỉ lấy ảnh và credit, không lấy chữ hay thông tin. Bản gốc trong `original/archdaily/21.jpg`, danh sách URL của cả bộ ảnh trên trang trong `original/archdaily/urls.txt` (chỉ ảnh 21 được dùng và giữ lại; các ảnh khác tải để xem thử đã xoá). Trang Yatzer (nguồn ảnh thứ nhất theo YAML) bị proxy chặn 403, nên không lấy.

## Bảng ảnh của bài 04 và việc dùng ở tập 13
| Ảnh | Loại | Dùng ở tập 13 | Đã dùng ở tập 12? |
|---|---|---|---|
| 01-diagram-ba-kieu-can-bang.png | diagram | không | có (cảnh 2–5) |
| 02-diagram-suc-nang-thi-giac.png | diagram | cảnh 2 (`source_dg.png`, phần hình đòn bẩy, bỏ tiêu đề lớn), cảnh 3–4 (`source_dgb.png`, phần nhãn "xa trục, nên nặng thêm" và dòng ba yếu tố, bỏ tiêu đề lớn) | không |
| 03-mat-bang-palmeira.png | mặt bằng | cảnh 5 (`source_mb.png`, cắt vùng phòng khách, lỗ cửa giữa, phòng ăn) | có (vùng phòng ngủ chính, cảnh 6) |
| 06-doodle-lo-suoi-va-tranh.jpg + goc/06 | ảnh doodle (mực ĐEN) + ảnh gốc sạch, phòng khách | ẢNH CHÍNH. Dùng ảnh gốc `goc/06`: cảnh 6–7 (`source_khachb.png`, dải y 560–1760 của ảnh xem), cảnh 8 (`source_nhomb.png`, dải dưới bên phải), cảnh 9 (`source_tub.png`, dải giữa có tủ cổ) | không |
| 10-doodle-anh-tong.jpg + goc/10 | ảnh doodle + ảnh gốc sạch, phòng khách nhìn từ đầu kia | cảnh 10–12 (`source_trucb.png`, dải y 300–1560: đáy hoa trần, lỗ cửa giữa, hai hốc kệ giống nhau) | có (dải dưới: sofa, ghế đen, lò sưởi, cảnh 10–11) |
| ArchDaily 21 | ảnh chụp ngoài kho, phòng khách nhìn từ cửa vào | cảnh 1 (mở, sạch), 13–14 (doodle mới nối lò sưởi và tranh), 15 (khung cuối) | không |
| 04, 05, 08, 09 | ảnh doodle/gốc phòng ngủ, phòng tắm, bài học 3 | không | 04, 05: có |
| 07-diagram-hai-cho-dung.png | diagram (bài học 3) | không | không |

Đạt mục 2d: một diagram (02), mặt bằng (03) đặt ngay trước cảnh ảnh chụp phòng khách, ảnh nhiều góc của phòng khách. Không ảnh nào quá khoảng nửa số cảnh: ảnh 06 (cảnh 6–9, bốn dải) = 4/15; ArchDaily 21 = 4/15 (kể cả khung cuối); ảnh 10 = 3/15; sơ đồ 02 = 3/15.

## Hạn chế (trung thực)
- **Mục 2d yêu cầu ảnh của ít nhất BA không gian khác nhau của công trình; tập này chỉ có phòng khách (từ ba góc: ảnh 06, ảnh 10 nhìn từ đầu kia, ArchDaily 21) và chỗ thông sang phòng ăn nhìn qua lỗ cửa giữa (ảnh 10).** Lý do: bài học 2 chỉ nói về phòng khách, và chủ Trang chọn ý cụ thể này. Thêm ảnh phòng ngủ, phòng tắm, bếp hay sân chỉ để đủ số sẽ làm reel gánh thêm chủ đề (mục 0.6b, 0.6h) và trùng tập 12. Xin chủ Trang xác nhận có chấp nhận ngoại lệ này.
- Doodle gốc của bài 04 vẽ mực ĐEN (và nhãn đen sát mép), không hợp quy cách nét trắng nét đứt và dải nhãn y 610–1240 (mục 6, 0.6d). Vì vậy không lộ nét gốc mà dùng ảnh gốc sạch `goc/06`, `goc/10` và vẽ nét trắng mới bằng `engine_ep13/draw_ep13.py`, giữ đúng chỗ khoanh và lời nhãn của bài (lò sưởi cùng màu tường, tranh sẫm nhỏ treo cao xa trục, trục giữa, tủ cổ gần trục, hoa trần, hai hốc kệ).
- Các ảnh phòng khách đều sáng, nét trắng trên tường kem kém nổi; engine có viền tối nhẹ quanh nét (halo) nên vẫn đọc được. Chữ nhãn khá nhỏ trên thẻ ảnh (thẻ cao khoảng 440–520 px để chừa chỗ phụ đề ba dòng).
- Ảnh ArchDaily 21 có lò sưởi bên trái, tranh bên phải (cùng hướng nhìn với ảnh 06). Ảnh 10 nhìn từ đầu kia nên lò sưởi nằm bên phải, sofa và tranh bên trái; lời đọc không nói "bên trái/bên phải" để khỏi sai hướng khi đổi ảnh.
- Ảnh 06 gốc (2500 px) và ArchDaily 21 (2000 px) đủ nét; dải cắt nhỏ (`source_nhomb.png` 1207×882, `source_tub.png` 1304×770) hơi mềm khi phóng trên thẻ 960 px nhưng vẫn rõ.

## Credit
- Ảnh chụp: Palmeira Apartment, Lisbon · Studio Gameiro · ảnh Francisco Nogueira (YAML `cong_trinh`; ArchDaily ghi cùng nhiếp ảnh gia).
- Sơ đồ 02: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014) (chú thích trên chính sơ đồ: "Arnheim, 1954; Kilmer & Kilmer, 2014").
- Mặt bằng: Studio Gameiro, nguồn ArchDaily (2023), ghi chú Giả Thuyết Kiến Trúc (chú thích trên bản vẽ của bài).
