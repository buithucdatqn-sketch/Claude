# Bộ khuôn reel nhiều ảnh (bản mẫu chất lượng: tập 7 "Cứng ở xa, mềm trong tầm tay")

Chép nguyên thư mục này vào `OUT/engine_epNN/`, đổi `ep07` thành `epNN` trong tên file và trong mã, rồi sửa dữ liệu của tập. Bản gốc đã chạy: `inbox/out/2026-10-18_mem-trong-tam-tay/engine_ep07/`. Tập 8 (`inbox/out/2026-10-19_mau-dam-mang-lon/engine_ep08/`) dùng cùng khuôn.

| File | Việc | Sửa gì mỗi tập |
|---|---|---|
| `make_layers.py` | Tách lớp doodle gốc của từng ảnh: nền sạch `source_<ảnh>.png` + nét `doodle_epNN_<ảnh>.npz` | Mỗi ảnh một lời gọi `run(...)`: `BOX` (khung từng nhãn, mũi tên, đo trên ảnh xem thu nhỏ), `ARROWS` (đuôi mũi tên), ngưỡng, cách lấp nền (`grain` cho bê tông, vải xù; `cols` cho vân gỗ dọc; `rows` cho ván ngang; mặc định inpaint TELEA). Xem lại nền bằng Read đến khi sạch. |
| `draw_doodle.py` | Vẽ nét doodle MỚI (nét trắng, nét đứt, rung tay, góc vẽ lố, mũi tên, vòng bao, khung bao, nhãn Patrick Hand) lên ảnh sạch hoặc ảnh lấy thêm từ trang nguồn, lưu `doodle_epNN_<ảnh>.npz` cùng dạng lớp của `make_layers.py` (điểm theo thứ tự vẽ, khoá `lab…` là nhãn) và ảnh xem thử `doodle_preview/` | Chép thành `draw_epNN.py`, sửa khối nét của từng ảnh. Đặt nhãn sao cho sau camera rơi vào dải y 610–1240; vùng cần chỉ nằm sát đáy ảnh thì dùng khung thẻ (`free=True`, zoom < 1) hoặc cắt ảnh. |
| `gen_epNN.py` | Một nguồn dữ liệu cảnh duy nhất: sinh engine khung + engine video cho từng run, `runs.json`, `scenes.json`, `elevenlabs.txt`, engine ảnh bìa | `IMGS` (ảnh, npz, credit riêng), `SC` (mỗi cảnh: `img`, `head`, `vo`, `tts`, `cam`, `dd`, `move`), `T_AUDIO` (mốc cảnh theo ghi âm, giai đoạn B), `HEAD`, chữ khung cuối, `COVER`. |
| `sheet_epNN.py` | Chạy engine khung của mọi run, gom `frames/`, dựng `storyboard.png` | Tên hiển thị của ảnh (`NAME`). |
| `render_epNN.sh` | Dựng video các run song song (3 tiến trình) | Không. |
| `ghep_epNN.py` | Cắt từng run và nối bằng hoà tan 0,45 giây, ghép giọng đã xử lý | Chạy `python3 -I ghep_epNN.py OUT audio/bai-NNN_xu-ly.wav OUT/reel_<slug>_final.mp4`. |

Thứ tự chạy: `make_layers.py` (ảnh có doodle gốc) → `draw_epNN.py` (nét mới) → `gen_epNN.py` → `sheet_epNN.py` (xem storyboard, sửa camera) → (giai đoạn B) đặt `T_AUDIO`, sửa lời theo ghi âm → `gen_epNN.py` → `sheet_epNN.py` → `render_epNN.sh` → `ghep_epNN.py`.
Đường dẫn engine tự tìm từ vị trí file (thư mục chứa engine/engine_video.py), chạy được ở mọi chỗ clone repo.

**Câu dài hơn ba dòng phụ đề (thêm 2026-10-24, TASK_INSTRUCTION mục 4 bước 4 và mục 0.6h):** viết lời liền trước, cắt cảnh sau; KHÔNG cắt câu cho vừa khung. Tách phụ đề thành hai trang trong cùng một cảnh bằng hai mục `SC` liền nhau: cùng `img`, cùng `cam`, cùng `head`, mục sau `move="hold"`, `dd=[]`; `vo` mỗi mục là một nửa câu (nửa đầu kết bằng dấu phẩy), `tts` hai mục ghép lại đúng câu. `gen_epNN.py` gom hai mục vào cùng một run nên camera không đổi, chỉ phụ đề sang trang. Mẫu: `inbox/out/2026-10-23_lop-loc-trong-nha/engine_ep11/gen_ep11.py` (cảnh 2–3, 5–6, 10–11). Giai đoạn B: mốc trang sau lấy theo chỗ ngắt hơi trong câu (silencedetect hoặc mốc chữ của sherpa-onnx).

**Sơ đồ vẽ dần, ảnh phóng tràn màn hình (thêm 2026-10-30, TASK_INSTRUCTION mục 0.6j):** `sketch_layers.py` tách nét mực của một sơ đồ thành các nhóm theo thứ tự vẽ (npz); run nào dùng ảnh có cờ sketch thì `gen_epNN.py` bật `SKETCH = True` trong engine (nền trắng, không thẻ, không băng keo; nét hiện dần, giữ màu mực; khoá `keep` của cảnh là nhóm đã vẽ ở cảnh trước). Run ảnh chụp bật `TAPE = False` và dùng camera `free=False` zoom khoảng 2,1–2,2 để ảnh phủ kín khung. Mẫu: `inbox/out/2026-10-30_tran-toi-hon-tuong/engine_ep17/` (`gen_ep17.py`, `sketch_ep17.py`, `draw_ep17.py`).
