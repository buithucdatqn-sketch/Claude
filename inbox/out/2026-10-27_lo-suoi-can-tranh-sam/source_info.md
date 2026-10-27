# Ảnh · tập 13

Kho: `buithucdatqn-sketch/A---material`, nhánh `AH-Interior-notes`, commit `bd74e5309164916cffb99e784b36711b2b82f7f2`, thư mục `AH-Decode-Decor/bai-04-3-bai-hoc-can-bang-thi-giac-noi-that/anh/`. Bản gốc chép trong `original/kho/`.
Một ảnh ngoài kho (mục 0.6d: được lấy thêm ảnh của chính công trình): ArchDaily, trang https://www.archdaily.com/1010507/palmeira-apartament-studio-gameiro (trang bài ghi ở `nguon_anh_cong_trinh`), ảnh số 21 (`palmeira-apartment-studio-gameiro_21.jpg`, bản large_jpg 2000 px, nhiếp ảnh gia ghi trên trang: Francisco Nogueira). Chỉ lấy ảnh và credit, không lấy chữ hay thông tin. Bản gốc trong `original/archdaily/21.jpg`, danh sách URL của cả bộ ảnh trên trang trong `original/archdaily/urls.txt` (chỉ ảnh 21 được dùng và giữ lại; các ảnh khác tải để xem thử đã xoá). Trang Yatzer (nguồn ảnh thứ nhất theo YAML) bị proxy chặn 403, nên không lấy.

## Bảng ảnh của bài 04 và việc dùng ở tập 13
| Ảnh | Loại | Dùng ở tập 13 | Đã dùng ở tập 12? |
|---|---|---|---|
| 01-diagram-ba-kieu-can-bang.png | diagram | cảnh 2 và cảnh 14–16 (`source_bat.png`, khung "bất đối xứng": khối lớn bên này, nhóm nhỏ sẫm bên kia, điểm tựa bập bênh) | có (cảnh 2–5, khung khác) |
| 02-diagram-suc-nang-thi-giac.png | diagram | cảnh 3 (`source_dgb.png`, "vật lớn, màu nhạt, cùng màu nền" / "vật nhỏ, màu sẫm, tương phản mạnh với nền", dòng các yếu tố), cảnh 4 (`source_dg.png`, hình đòn bẩy), bỏ tiêu đề lớn | không |
| 03-mat-bang-palmeira.png | mặt bằng | cảnh 5 (`source_mb.png`, cắt vùng phòng khách, lỗ cửa giữa, phòng ăn) | có (vùng phòng ngủ chính, cảnh 6) |
| 06-doodle-lo-suoi-va-tranh.jpg + goc/06 | ảnh doodle (mực ĐEN) + ảnh gốc sạch, phòng khách | ẢNH CHÍNH. Dùng ảnh gốc `goc/06`: cảnh 6–9 và 11 (`source_khachb.png`, dải y 560–1760: trục, lò sưởi, tranh, ghế đen, mũi tên khoảng cách), cảnh 10 (`source_nhomb.png`: ghế gỗ đen, sofa), cảnh 12–13 (`source_tub.png`: tủ cổ gần trục) | không |
| 10-doodle-anh-tong.jpg + goc/10 | ảnh doodle + ảnh gốc sạch, phòng khách nhìn từ đầu kia | bản 5 không dùng (bản 4 dùng dải hoa trần, hai hốc kệ; `source_trucb.png` còn trong thư mục) | có (dải dưới) |
| ArchDaily 21 | ảnh chụp ngoài kho, phòng khách nhìn từ cửa vào | cảnh 1 (mở, sạch), 17 (khung cuối) | không |
| 04, 05, 08, 09 | ảnh doodle/gốc phòng ngủ, phòng tắm, bài học 3 | không | 04, 05: có |
| 07-diagram-hai-cho-dung.png | diagram (bài học 3) | không | không |

Đạt mục 2d (trừ ba không gian, xem hạn chế): hai diagram (01, 02), mặt bằng (03) đặt ngay trước cảnh ảnh chụp phòng khách. Ảnh 06 chiếm 8/17 cảnh (cảnh 6–13, bốn dải cắt khác nhau), gần nửa số cảnh, vì bản 5 cân từng món trên chính ảnh này theo yêu cầu chủ Trang; sơ đồ 01 = 4/17; ArchDaily 21 = 2/17; sơ đồ 02 = 2/17; mặt bằng = 1/17.

## Hạn chế (trung thực)
- **Mục 2d yêu cầu ảnh của ít nhất BA không gian khác nhau của công trình; tập này chỉ có phòng khách (từ ba góc: ảnh 06, ảnh 10 nhìn từ đầu kia, ArchDaily 21) và chỗ thông sang phòng ăn nhìn qua lỗ cửa giữa (ảnh 10).** Lý do: bài học 2 chỉ nói về phòng khách, và chủ Trang chọn ý cụ thể này. Thêm ảnh phòng ngủ, phòng tắm, bếp hay sân chỉ để đủ số sẽ làm reel gánh thêm chủ đề (mục 0.6b, 0.6h) và trùng tập 12. Xin chủ Trang xác nhận có chấp nhận ngoại lệ này.
- Doodle gốc của bài 04 vẽ mực ĐEN (và nhãn đen sát mép), không hợp quy cách nét trắng nét đứt và dải nhãn y 610–1240 (mục 6, 0.6d). Vì vậy không lộ nét gốc mà dùng ảnh gốc sạch `goc/06`, `goc/10` và vẽ nét trắng mới bằng `engine_ep13/draw_ep13.py`, giữ đúng chỗ khoanh và lời nhãn của bài (lò sưởi cùng màu tường, tranh sẫm nhỏ treo cao xa trục, trục giữa, tủ cổ gần trục, hoa trần, hai hốc kệ).
- Các ảnh phòng khách đều sáng, nét trắng trên tường kem kém nổi; engine có viền tối nhẹ quanh nét (halo) nên vẫn đọc được. Chữ nhãn khá nhỏ trên thẻ ảnh (thẻ cao khoảng 440–520 px để chừa chỗ phụ đề ba dòng). Băng keo ở giữa mép trên thẻ có thể che một phần đỉnh ảnh (đã dời vòng "hoa trần" xuống dưới băng keo ở cảnh 11).
- Ảnh ArchDaily 21 có lò sưởi bên trái, tranh bên phải (cùng hướng nhìn với ảnh 06). Ảnh 10 nhìn từ đầu kia nên lò sưởi nằm bên phải, sofa và tranh bên trái; lời đọc không nói "bên trái/bên phải" để khỏi sai hướng khi đổi ảnh.
- Ảnh 06 gốc (2500 px) và ArchDaily 21 (2000 px) đủ nét; dải cắt nhỏ (`source_nhomb.png` 1207×882, `source_tub.png` 1304×770) hơi mềm khi phóng trên thẻ 960 px nhưng vẫn rõ.

## Credit
- Ảnh chụp: Palmeira Apartment, Lisbon · Studio Gameiro · ảnh Francisco Nogueira (YAML `cong_trinh`; ArchDaily ghi cùng nhiếp ảnh gia).
- Sơ đồ 02: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014) (chú thích trên chính sơ đồ: "Arnheim, 1954; Kilmer & Kilmer, 2014").
- Mặt bằng: Studio Gameiro, nguồn ArchDaily (2023), ghi chú Giả Thuyết Kiến Trúc (chú thích trên bản vẽ của bài).
- Mặt bằng 03 giữ nguyên nhãn và các số vị trí chụp 03, 05, 06 của bài (không xoá khỏi bản vẽ gốc).
