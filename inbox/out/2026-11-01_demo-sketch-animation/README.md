# Demo phong cách hình: animation sketch graphic (chờ chủ Trang duyệt)

Ngày: 2026-11-01. Đây chỉ là bản thử phong cách phần hình, không phải tập reel chính thức. Nhật ký và series.json chưa cập nhật.

- File: `demo_sketch_silent.mp4` (20 giây, 1080×1920, 30 khung/giây, H.264, track âm thanh im lặng), `demo_keyframes.jpg` (các khung chính).
- Ảnh: `AH-Decode-Decor/bai-03-3-bai-hoc-anh-sang-tu-nhien-noi-that/anh/goc/07-goc-cua-cao-ban-an.jpg` (ảnh chụp gốc, chưa có doodle). Ảnh dự án: Union Street House · Prior Barraclough · ảnh Ben Hosking.
- Ý dùng thử: "ánh sáng từ trên cao" của bài 03 (ý chưa dùng). Phụ đề chỉ là lời mẫu, chưa phải kịch bản.
- Engine: `engine/sketch_anim/sketch_demo.py` (chạy `python3 -I sketch_demo.py <ảnh> <thư_mục_ra>`).

## Nhịp hình của demo
| Thời điểm | Hình |
|---|---|
| 0–6,4 giây | Trên giấy trắng, nét ký họa rút từ ảnh tự vẽ ra: nét dài, nét khung lớn trước, chi tiết sau. Nét rung nhẹ khoảng 7,5 lần mỗi giây, giống hoạt hình vẽ tay. |
| 5,6–8,6 giây | Lớp nét chì đổ bóng quét chéo vào, theo chỗ sáng tối của ảnh. |
| 8,4–10,6 giây | Ảnh thật hiện dần dưới lớp nét. Nét ký họa vẫn còn, mờ đi một nửa. |
| 10,6–14,4 giây | Camera zoom vào ô kính. Nét trắng vẽ tay khoanh vách lam, mũi tên chỉ ô kính, nhãn chữ hiện dần. |
| 14,4–20 giây | Camera lùi ra. Ba mũi tên cam (nét nhấn duy nhất) chạy theo đường đi ánh sáng: qua vách lam, lên trần, rồi xuống bàn ăn. Vòng tròn nhỏ chạy dọc mũi tên. |

## Cần chủ Trang chọn
1. Video mẫu chủ Trang nhắc tới không tới được phiên này, nên demo dựa trên cách hiểu thông dụng của kiểu animation sketch. Nếu video mẫu khác (ví dụ chỉ dùng nét, không hiện ảnh thật; hoặc có nhân vật, có màu nước), xin đẩy video vào `inbox/override/` hoặc mô tả lại.
2. Có giữ bước hiện ảnh thật ở cuối không, hay để nguyên bản ký họa suốt reel.
3. Độ dày lớp nét chì đổ bóng: giữ như demo, hay bớt nữa.
4. Lưu ý quy cách cũ (mục 9: không tô mảng, không gradient): bước ảnh thật hiện dần là hoà ảnh, không phải tô màu, nhưng xin chủ Trang xác nhận.

## Bản 2 (theo video mẫu chủ Trang gửi lại): nét viền bay vào lắp ráp

- File: `demo_lap_rap_silent.mp4` (13,6 giây), `demo_lap_rap_keyframes.jpg`.
- Engine: `engine/sketch_anim/empty_room.py` (tạo ảnh phòng trống từ ảnh gốc: tường ván gỗ chép theo cột, sàn bê tông ghép mảnh vá) và `engine/sketch_anim/sketch_assemble.py`.
- Ảnh phủ kín khung 1080×1920 như video mẫu. Phụ đề nằm trên mẩu giấy trắng dán băng keo, đổi chỗ theo cảnh để không che chi tiết đang nói (trên, dưới, góc trái). Mọi chữ nằm trong y 336–1490.

| Thời điểm | Hình |
|---|---|
| 0–0,5 giây | Phòng trống (đã xoá đảo bếp, bàn, bốn ghế, thảm, ghế đôn inox, kệ trên gác). |
| 0,5–4,8 giây | Lần lượt thảm, đảo bếp, bàn, bốn ghế, ghế đôn, kệ bay vào từ mép khung. Nét viền dày màu kem, xoay, nảy rồi đáp đúng chỗ. Nét rung nhẹ 10 lần mỗi giây. |
| 5,3–6,4 giây | Hoà sang ảnh thật, nét viền mờ đi. |
| 6,6–9,6 giây | Camera zoom vào ô kính. Khung vách lam rồi ô kính bay vào theo cùng kiểu. |
| 10,4–13,6 giây | Camera lùi ra. Ba mũi tên cam vẽ đường đi ánh sáng xuống bàn ăn. |

Hạn chế: phòng trống tạo bằng cách xoá đồ trên ảnh, nên nhìn kỹ vẫn thấy sàn hơi phẳng, ở mép gác còn vết mờ nhỏ chỗ chậu cây. Bản 1 (`demo_sketch_silent.mp4`) giữ lại để so sánh.

### Sửa theo góp ý 2026-11-01 (bản 2 được đánh giá "tạm ổn")
- Credit tên công trình chuyển vào trong hộp chữ phụ đề, không còn thẻ riêng đè lên ảnh.
- Bỏ băng keo trên các hộp chữ.
- Ghi nhớ: demo chỉ thử một ảnh điển hình; reel thật vẫn theo instruction (nhiều ảnh, có bản vẽ). Đã ghi thành mục 00b trong `TASK_INSTRUCTION.md`.
