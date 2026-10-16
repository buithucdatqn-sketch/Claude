# Ảnh nguồn · Tập 6

- Ảnh trong kho: `AH-Decode-Decor/bai-01-3-bai-hoc-phoi-mau-noi-that-can-ho/anh/12-doodle-cung-mau-khac-be-mat.jpg` (1875×2500, dọc 3:4). Nhánh `AH-Interior-notes`, commit `65b5427c55046c43f02d8e7ec0829e03ae0fdd03`. Bản gốc ở `original/`.
- Credit (YAML `cong_trinh`): The Green Box, Berlin · Ester Bruzkus Architekten · ảnh Robert Rieger. Bài không ghi ai dựng doodle nên không thêm "Giả Thuyết Kiến Trúc".
- Lý do chọn: ảnh loại (a), có doodle sẵn (hai mũi tên, nhãn "mặt sơn phẳng sáng hơn", "mặt nan dọc trông sẫm hơn") khớp đúng ý "cùng màu, khác bề mặt". Chưa dùng ở tập nào (tập 4 dùng ảnh 07, tập 5 dùng ảnh 04).
- Bản làm việc 1800×2400 (LANCZOS). `source_orig.png` còn doodle; `source.png` là nền đã xoá tiêu đề, dòng phụ, credit vẽ tay, nhãn và mũi tên. Vì nan tủ và khe ván tường là cấu trúc dọc, vùng xoá được lấp bằng nội suy theo cột (OpenCV inpaint để lại vệt zigzag trên nan tủ). Kiểm tra bằng mắt: nền sạch.
- Lớp nét: `engine_ep06/doodle_ep06.npz` (arr1, arr2 là mũi tên, lộ từ đuôi tới đầu; lab1, lab2 là nhãn chữ gốc; `sub` là dòng "nan đổ bóng nên trông tối hơn", tách sẵn nhưng chưa dùng). Tách bằng `engine_ep06/make_layers.py`.
- Hạn chế: ảnh chỉ có một khối tủ nan, tường sơn và mặt đá; bếp trong lời đọc được minh hoạ bằng cảnh zoom vào đá, tường, tủ trong cùng ảnh. Mũi tên 1 trỏ vào tường sát mép đá nên đầu mũi tên nằm gần mép đá.

## Ảnh phụ (giai đoạn B, theo yêu cầu chủ Trang: cảnh 8 đổi sang ảnh khu bếp)
- `AH-Decode-Decor/bai-01-3-bai-hoc-phoi-mau-noi-that-can-ho/anh/11-doodle-dap-mau-bep.jpg` (2500×1875, ngang 4:3), cùng commit. Bản gốc ở `original/`. Dùng cho cảnh 8 ("Ở khu bếp cũng vậy...").
- Bản làm việc 2400×1800: `source_bep_orig.png` (còn nét), `source_bep.png` (đã xoá tiêu đề "một màu, ba chất liệu", nhãn "tường sơn xanh đậm", "cùng họ xanh, khác độ sáng", credit vẽ tay, hai mũi tên và hai nhãn). Mũi tên đi qua lọ và kệ đá nên tách bằng loang theo điểm trắng nối với đuôi mũi tên rồi inpaint TELEA; chữ trên tường và tủ lấp theo cột. `engine_ep06/make_layers_bep.py`.
- Lớp nét: `engine_ep06/doodle_ep06_bep.npz` (hai mũi tên và hai nhãn gốc "đá vân xanh sau bồn rửa", "tủ xanh ô liu").
- Dựng: engine phụ `engine_video_ep06_bep.py`, cắt đoạn cảnh 8 (33–38 giây) ghép vào video chính.
