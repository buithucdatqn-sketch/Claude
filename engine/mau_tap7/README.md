# Bộ khuôn reel nhiều ảnh (bản mẫu chất lượng: tập 7 "Cứng ở xa, mềm trong tầm tay")

Chép nguyên thư mục này vào `OUT/engine_epNN/`, đổi `ep07` thành `epNN` trong tên file và trong mã, rồi sửa dữ liệu của tập. Bản gốc đã chạy: `inbox/out/2026-10-18_mem-trong-tam-tay/engine_ep07/`. Tập 8 (`inbox/out/2026-10-19_mau-dam-mang-lon/engine_ep08/`) dùng cùng khuôn.

| File | Việc | Sửa gì mỗi tập |
|---|---|---|
| `make_layers.py` | Tách lớp doodle gốc của từng ảnh: nền sạch `source_<ảnh>.png` + nét `doodle_epNN_<ảnh>.npz` | Mỗi ảnh một lời gọi `run(...)`: `BOX` (khung từng nhãn, mũi tên, đo trên ảnh xem thu nhỏ), `ARROWS` (đuôi mũi tên), ngưỡng, cách lấp nền (`grain` cho bê tông, vải xù; `cols` cho vân gỗ dọc; `rows` cho ván ngang; mặc định inpaint TELEA). Xem lại nền bằng Read đến khi sạch. |
| `gen_epNN.py` | Một nguồn dữ liệu cảnh duy nhất: sinh engine khung + engine video cho từng run, `runs.json`, `scenes.json`, `elevenlabs.txt`, engine ảnh bìa | `IMGS` (ảnh, npz, credit riêng), `SC` (mỗi cảnh: `img`, `head`, `vo`, `tts`, `cam`, `dd`, `move`), `T_AUDIO` (mốc cảnh theo ghi âm, giai đoạn B), `HEAD`, chữ khung cuối, `COVER`. |
| `sheet_epNN.py` | Chạy engine khung của mọi run, gom `frames/`, dựng `storyboard.png` | Tên hiển thị của ảnh (`NAME`). |
| `render_epNN.sh` | Dựng video các run song song (3 tiến trình) | Không. |
| `ghep_epNN.py` | Cắt từng run và nối bằng hoà tan 0,45 giây, ghép giọng đã xử lý | Tên file giọng và tên file ra. |

Thứ tự chạy: `make_layers.py` → `gen_epNN.py` → `sheet_epNN.py` (xem storyboard, sửa camera) → (giai đoạn B) đặt `T_AUDIO`, sửa lời theo ghi âm → `gen_epNN.py` → `sheet_epNN.py` → `render_epNN.sh` → `ghep_epNN.py`.
