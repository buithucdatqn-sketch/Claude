# Ảnh · tập 14

Kho: `buithucdatqn-sketch/A---material`, nhánh `AH-Interior-notes`, commit `acfe39329e2d291c0828c519dc01a8227b673e04`, thư mục `AH-Decode-Decor/so-tay-cong-thuc-chon-mau-noi-that/`.
Sổ tay không có thư mục `anh/`; mọi ảnh trích thẳng từ file PDF của chương bằng `pdfimages -png` (đúng kích thước nhúng trong PDF, không phóng to, không lấy ảnh ngoài kho). Bản trích gốc nằm trong `original/`. Credit tra ở `11-ghi-chu-hinh-anh-va-bia-sau.pdf` và chú thích dưới ảnh trong sách.

## Bảng ảnh và việc dùng ở tập 14 (bản 7, làm lại theo chủ Trang)
| File làm việc | Ảnh gốc (`original/`) | Trong sổ tay | Loại | Credit trên khung | Cảnh |
|---|---|---|---|---|---|
| `source_hanh.png` (cắt 100, 470, 1300, 1900) | `ch1-trang-ten-chuong-hanh-lang-khung-cua.png` 1325×1988 | Trang tên chương 1, hành lang và khung cửa | ảnh nội thất sạch | Ảnh: Ryunosuke Kikuno / Unsplash, qua sổ tay AH+ | 1 (mở), 9–10 (mảng tường sáng; nét mới), 11 (chốt), ảnh bìa |
| `source_mau.png` | `mo-dau-cover-story-khoi-mau.png` 512×512 | Mở đầu, khối mẫu màu khác nhau cả sắc độ, độ sáng và độ rực, cửa hàng sơn Cover Story, Helsinki (Linda Bergroth, 2021) | ảnh nội thất | Ảnh: Cover Story, Helsinki · Paavo Lehtonen / Dezeen, qua sổ tay AH+ | 2–3 (lưới ô mẫu màu; ô sáng, ô tối hơn; nét mới) |
| `source_khe.png` (cắt 0, 0, 1164, 1100) | `ch1-muc-1-3-khe-cua-tuong-trang.png` 1164×1745 | Mục 1.3, ánh sáng ban ngày trên tường trắng | ảnh nội thất sạch | Ảnh: Danielle-Claude Bélanger / Unsplash, qua sổ tay AH+ | 4 (trần sáng, tường sáng; nét mới) |
| `source_dg.png` | `ch1-hinh-1-2-tuong-sang-noi-phong.png` 648×606 | Hình 1.2 "Tường sáng nới phòng" | sơ đồ | Hình 1.2: AH+, theo von Castell, Hecht và Oberfeld (2018) | 5–6 (thí nghiệm) |
| `source_lrv.png` | `mo-dau-hinh-m1-lrv.png` 648×621 | Hình M.1 chỉ số phản xạ ánh sáng LRV | sơ đồ | Hình M.1: AH+, số liệu Dulux Australia, dải TCVN 7114-1 | 7–8 |
| (toàn màn hình, `engine_ep14/end_ep14.py`) | `chu-trang/AH_mockup_tablet.mp4` 1080×1350, 28 giây (chủ Trang gửi; `ebook-so-tay-ah-plus.webp` tĩnh làm dự phòng; `source_ebook.png` chỉ để engine chạy run khung cuối) | Video sổ tay AH+ lật trang trên iPad | video sản phẩm | Video: sổ tay AH+ Công thức chọn màu nội thất · Giả Thuyết Kiến Trúc | 12 (khung cuối: video nguyên cỡ đặt đúng khung 4:5 của bảng tin y 285–1635, hai dải trên dưới lấp bằng vải nền phản chiếu; iPad x 210–1052, y 660–1315; ba dòng mời phía trên iPad, không đè iPad) |
| (không dùng ở bản 7) | ba ảnh Pawson House (`ch1-pawson-*.png`) | Mục 1.4 | ảnh công trình | | bản 1–5 dùng; bản 7 bỏ theo yêu cầu một ý |

Bản 7 không dùng ảnh công trình nào: ý duy nhất (độ sáng của màu) được minh hoạ bằng hai sơ đồ của sổ tay, ảnh khối mẫu màu và hai ảnh nội thất minh hoạ của sổ tay. Ảnh nhiều cảnh nhất là hành lang (4/12 cảnh). Ảnh trong sổ tay không có doodle, nên mọi nét vẽ mới bằng `engine_ep14/draw_ep14.py`.

## Hạn chế
- Ảnh trong PDF nhỏ: Hình 1.2 chỉ 648 px, ảnh cầu thang 632 px. Đủ cho thẻ ảnh trong dải giữa khung (khoảng 520 px), không zoom sâu được.
- Hai ảnh hành lang và góc tường là ảnh Unsplash sổ tay dùng để minh hoạ chương, không phải ảnh của Pawson House. Khung ghi rõ nguồn, lời không gán chúng cho công trình nào.
- Theo ghi chú hình ảnh, sổ tay lưu hành nội bộ và "nếu phát hành rộng hơn, cần rà lại danh sách này để xin phép hoặc thay ảnh". Bản 7 không còn ảnh Pawson House; ảnh khối mẫu màu (Paavo Lehtonen / Dezeen) vẫn chưa có giấy phép đăng công khai, chủ Trang cần quyết định trước khi đăng. Hai ảnh Unsplash dùng được theo giấy phép Unsplash.
- Ảnh khối mẫu màu chỉ 512 px, thẻ ảnh hơi mềm.
