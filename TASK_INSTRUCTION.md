# INSTRUCTION — Scheduled task "AH Decode · Reel hằng ngày"

Kho mã và dữ liệu: GitHub `buithucdatqn-sketch/claude` (nhánh `main`). Cách lấy: dùng add_repo (quyền push) rồi `git clone --depth 1 https://github.com/buithucdatqn-sketch/claude /home/claude/claude` (timeout lệnh ≥ 10 phút; chỉ MỘT lệnh git tại một thời điểm), sau đó gọi register_repo_root. Gọi thư mục clone là REPO. Cấu trúc: `REPO/engine/` (bộ engine), `REPO/inbox/` (INBOX), `REPO/TASK_INSTRUCTION.md` (bản sao của chính tài liệu này). Thông tin nội dung của mỗi tập lấy từ KHO BÀI (mục 2a), một kho GitHub khác. Cuối mỗi lần chạy: chép `engine_epNN.py` và `engine_video_epNN.py` vào `OUT/engine_epNN/`, `git add inbox`, commit, và `git pull --rebase origin main && git push origin main` (một lần; nếu bị 429 thì đợi 10 giây thử lại một lần).

Mỗi lần chạy là một phiên mới, không nhớ gì từ các cuộc trò chuyện trước. Mọi thông tin cần thiết nằm trong tài liệu này, thư mục INBOX và KHO BÀI.
Chạy một lượt, không hỏi lại. Nếu thiếu đầu vào thì dừng và báo rõ thiếu gì (mục 9).

## 1. Nhiệm vụ
Mỗi ngày, lấy MỘT bài chưa dùng trong KHO BÀI (mục 2a) và dùng NỘI DUNG CỦA BÀI làm toàn bộ thông tin của reel (nguyên tắc, nguồn gốc, cơ chế, cách áp dụng, cách chọn đồ, nguồn tham khảo). Task KHÔNG tự nghiên cứu và KHÔNG tự viết thêm thông tin ngoài bài (mục 3). Sau đó TỰ lấy MỘT ảnh dự án thật trên một trong các tạp chí thiết kế (Yatzer, Yellowtrace, Dwell, Wallpaper*) phù hợp để minh hoạ nguyên lý đó, và tạo gói sản xuất cho một reel dọc 9:16, dài 45–60 giây, series "AH Decode". Reel giải thích MỘT nguyên tắc nội thất/decor bằng các nét doodle trắng nét đứt vẽ lên chính ảnh gốc.
Mỗi reel là một bài học TRỌN VẸN và CÓ CHIỀU SÂU (mục 4a) về nội thất và decor, chắt lọc từ bài trong kho: nguồn gốc nguyên tắc, cơ chế vì sao mắt thấy vậy, đọc nguyên lý trên ảnh, lỗi hay gặp, cách áp dụng cụ thể, cách chọn mua/chọn đồ và thiết kế, rồi công thức tổng kết. Người xem phải học được điều cụ thể mà họ chưa biết, không phải những câu chung chung. Không hẹn "tập sau"; cảnh cuối chỉ mời theo dõi Fanpage Giả Thuyết Kiến Trúc và các bài viết về kiến trúc dành riêng cho thành viên (link ở phần bình luận).

**Tên gọi (dùng đúng, không lẫn):** Fanpage tên là **Giả Thuyết Kiến Trúc**. **AH Decode** là một series MỚI của Fanpage này, chuyên phân tích các nguyên tắc thiết kế và cách chọn đồ decor. AH Decode KHÔNG phải tên Fanpage: không viết "Fanpage AH Decode". Header trên khung vẫn là `AH DECODE · <CHỦ ĐỀ>`.
Chạy trọn một lượt, không chờ duyệt lý thuyết hay ảnh giữa chừng.

## 1a. TRỌNG TÂM SERIES: NỘI THẤT VÀ DECOR, KHÔNG PHẢI KIẾN TRÚC (bắt buộc)
AH Decode dạy người xem cách làm đẹp và chọn đồ cho không gian bên trong: những thứ họ tự quyết được trong nhà mình mà không cần xây, đập hay sửa kết cấu. Các bài trong KHO BÀI đã được biên soạn cho series này; mục 1a dùng để chọn chi tiết khoanh trên ảnh, để chọn MỘT ý chính khi bài dài, và để nhận ra bài lệch trọng tâm (khi đó bỏ qua bài đó theo mục 2a).
- ĐÚNG trọng tâm: phối màu (bánh xe màu, tương cận, bổ túc, tam giác màu, sắc độ, độ bão hoà, màu nền và màu nhấn, nhiệt độ màu, màu ảnh hưởng nhau và theo ánh sáng); chọn kiểu dáng đồ nội thất (dáng cong hay góc cạnh, chân cao hay sát sàn, trọng lượng thị giác, tỷ lệ món đồ so với phòng và so với nhau, công thái học, kích thước chuẩn của bàn ghế); chọn vật liệu và bề mặt (gỗ, đá, vải, kim loại, độ bóng mờ, vân, tương phản chất cảm); bố cục và sắp xếp đồ (nhóm trò chuyện, lối đi, điểm nhấn, cân bằng, nhịp lặp, khoảng thở); hoạ tiết và vải (pha hoạ tiết theo tỷ lệ, rèm, thảm, gối); đèn và ánh sáng decor (đèn nhiều lớp, nhiệt độ màu bóng đèn, đèn làm điểm nhấn); styling (treo tranh, bày đồ trên kệ, nhóm vật trang trí, cây); các nhà thiết kế nội thất, nhà trang trí, nhà thiết kế đồ nội thất và tạo dáng công nghiệp (ví dụ Charles và Ray Eames, Hans Wegner, Florence Knoll, Dieter Rams, Dorothy Draper, Elsie de Wolfe, Andrée Putman) cùng triết lý, cách làm của họ; các nguyên lý thị giác (Gestalt, tương phản, thứ bậc…) KHI áp vào đồ đạc, màu, vật liệu, bố cục đồ.
- SAI trọng tâm, KHÔNG làm: lý thuyết kiến trúc và không gian công trình (prospect–refuge, trục và trình tự không gian, ngưỡng và chuyển tiếp, hình khối, mặt bằng, kết cấu, độ cao trần, vách kính, cửa sổ, quan hệ nhà với cảnh quan); phân tích tác phẩm hay lý thuyết của kiến trúc sư (Wright, Le Corbusier, Kahn, Zumthor…) với tư cách kiến trúc sư. Kiến trúc sư chỉ được nhắc khi bàn đến món đồ nội thất họ thiết kế (ví dụ ghế Barcelona của Mies van der Rohe và Lilly Reich) và chỉ ở tư cách người thiết kế đồ.
- Phép thử với bài và ý chính được chọn: người xem có áp dụng được điều này bằng cách mua, đổi, sơn, dời hoặc bày lại đồ trong một căn phòng có sẵn không? Nếu chỉ áp dụng được khi xây hoặc sửa công trình thì loại.
- Trên ảnh, nét doodle khoanh và chỉ vào ĐỒ VẬT, MÀU, VẬT LIỆU, HOẠ TIẾT, ĐÈN, cách bày đồ; không lấy trần, cột, vách, cửa sổ, kết cấu làm đối tượng phân tích chính.
Gói gồm: (1) kịch bản lời đọc theo cảnh và file chữ thuần để dán vào ElevenLabs, (2) các khung hình 1080×1920, (3) bảng phân cảnh, (4) video reel dựng sẵn (bản không tiếng, hoặc có tiếng nếu đã có audio), (5) bảng đối chiếu từng nhận định với bài trong kho, (6) caption đăng bài.
Người dùng nói tiếng Việt, mọi chữ trên khung và lời đọc đều bằng tiếng Việt.

## 2. Đầu vào (INBOX = REPO/inbox)
Chế độ mặc định là TỰ ĐỘNG: không cần người dùng gửi ảnh. Chỉ cần:
- KHO BÀI (mục 2a): nguồn thông tin duy nhất cho nội dung reel.
- `INBOX/series.json`: danh sách các tập đã làm (số tập, bài trong kho đã dùng `bai_kho` = đường dẫn file + commit SHA của nhánh lúc đọc, nguyên lý, URL bài tạp chí và URL ảnh đã dùng, ngày). Nếu chưa có thì tạo mới. Dùng để không lặp lại bài trong kho, và không lặp lại ảnh/dự án (không dùng lại cùng một dự án trong 60 ngày gần nhất).
- `INBOX/override/` (tuỳ chọn, có thì ưu tiên): `<tên>.jpg|png` ảnh do người dùng gửi + `<tên>.txt` (dòng 1 = credit đúng dạng `tên dự án · studio · nhiếp ảnh gia`, các dòng sau = đường dẫn bài trong KHO BÀI muốn dùng, nếu có). Có thư mục này thì bỏ qua phần tìm ảnh ở mục 2b, dùng ảnh người dùng gửi; nội dung vẫn lấy từ KHO BÀI (bài được chỉ định, hoặc bài chưa dùng tiếp theo theo mục 2a).
- `INBOX/audio/<slug>.mp3|wav|m4a` (tuỳ chọn): giọng đọc ElevenLabs của chính tập này (người dùng làm từ file `elevenlabs.txt` của lần chạy trước). Có file này thì làm bước 9 (ghép tiếng) trong mục 4.
- Xử lý xong: cập nhật `series.json`; ảnh override chuyển sang `INBOX/done/`.

## 2a. KHO BÀI: nguồn thông tin của reel (bắt buộc)
- Vị trí: GitHub `buithucdatqn-sketch/A---material`, nhánh `AH-Interior-notes`, thư mục `AH-Decode-Decor/` (https://github.com/buithucdatqn-sketch/A---material/tree/AH-Interior-notes/AH-Decode-Decor/).
- Cách lấy: dùng add_repo cho `buithucdatqn-sketch/A---material` (chỉ cần quyền đọc), rồi `git clone --depth 1 -b AH-Interior-notes https://github.com/buithucdatqn-sketch/A---material /home/claude/material` (timeout ≥ 10 phút; chỉ MỘT lệnh git tại một thời điểm). Nếu thư mục đã có thì `git -C /home/claude/material pull origin AH-Interior-notes`. Nếu clone không được nhưng công cụ GitHub MCP đọc được kho thì đọc bằng `get_file_contents` (ref `refs/heads/AH-Interior-notes`). Gọi thư mục bài là KHO = `/home/claude/material/AH-Decode-Decor/`. KHÔNG sửa, commit hay push gì vào kho bài.
- Đọc cấu trúc thư mục trước: nếu có README, mục lục, file hướng dẫn hay quy ước đặt tên (ví dụ số thứ tự, trạng thái "đã duyệt"/"nháp") thì làm theo. Mỗi bài thường là một file (`.md`, `.txt`, hoặc tài liệu khác) hoặc một thư mục con; file không phải bài (README, mẫu, ảnh, ghi chú chung) thì không tính là bài.
- Chọn bài: bài CHƯA có trong `series.json` (so theo đường dẫn), theo thứ tự trong mục lục nếu có, không thì theo số thứ tự hoặc tên file tăng dần. Bỏ qua bài ghi rõ là nháp/chưa xong. Nếu bài lệch trọng tâm mục 1a (lý thuyết kiến trúc) thì bỏ qua, ghi vào `series.json` với `trang_thai: "bo_qua_lech_trong_tam"` kèm lý do, rồi lấy bài kế tiếp.
- Đọc TOÀN BỘ bài (Read hết, không bỏ đoạn nào), kể cả phần nguồn tham khảo, ghi chú ảnh, gợi ý dự án nếu có. Bài dài hơn một reel: chọn MỘT ý chính đủ cho bảy phần B–H (mục 4a), phần còn lại có thể đưa vào caption; KHÔNG chia thành nhiều tập, không hẹn "tập sau". Đánh dấu cả bài là đã dùng.
- Nếu bài có kèm ảnh, link ảnh hoặc gợi ý dự án minh hoạ thuộc bốn trang nguồn ở mục 2b: ưu tiên dùng (vẫn kiểm tiêu chí ảnh và lấy credit theo mục 2b). Ảnh bài gợi ý nằm ngoài bốn trang nguồn thì không dùng, tự tìm ảnh theo mục 2b.

## 2b. Lấy ảnh từ tạp chí thiết kế (chế độ tự động)
**Nguồn ảnh (chỉ các trang sau, không trang nào khác):** Yatzer (www.yatzer.com), Yellowtrace (www.yellowtrace.com.au), Dwell (www.dwell.com), Wallpaper* (www.wallpaper.com). Đã thử: bốn trang này truy cập được bằng `curl -A "Mozilla/5.0"`. The Local Project chặn truy cập tự động (403 Cloudflare) và Est Living chặn bằng captcha: KHÔNG dùng và KHÔNG cố vượt. Đầu mỗi lần chạy kiểm tra từng trang bằng `curl -sS -m 20 -L -A "Mozilla/5.0" -o /dev/null -w "%{http_code}" <URL>`; trang nào không trả 200 thì bỏ qua lần đó. Nếu không trang nào truy cập được thì dừng và báo (mục 9).
Cách lấy ảnh theo trang (cấu trúc có thể đổi, hãy xem HTML thật):
- Yatzer: trang bài chứa `https://media.yatzer.com/...jpg`; bản không hậu tố kích thước là bản gốc lớn nhất, `-1400x…` là dự phòng. Credit nhiếp ảnh: câu "Photography by …" trong bài.
- Yellowtrace: bài viết WordPress; ảnh ở `assets.yellowtrace.com.au/wp-content/uploads/...`; bỏ hậu tố kích thước `-1040x700` để lấy bản gốc (nếu 404 thì dùng bản có hậu tố lớn nhất). Credit nằm trong bài ("Photography by/Photo by …").
- Dwell: ảnh ở `images2.dwell.com/photos/.../original.jpg`. Credit nhiếp ảnh và kiến trúc sư nằm trong bài hoặc chú thích ảnh.
- Wallpaper*: lấy ảnh từ thẻ `og:image`/`img` trong bài (ưu tiên URL lớn nhất); credit nằm ở chú thích ảnh hoặc cuối bài ("Photography: …").
Mỗi lần chọn trang có ảnh phù hợp nguyên lý nhất; luân phiên giữa các trang để đa dạng, không dùng một trang quá hai ngày liên tiếp.

**Tìm ảnh minh hoạ trên các trang nguồn** (nội dung đã chốt từ bài trong kho trước, ảnh sau)
5. Lấy danh sách bài từ chuyên mục NỘI THẤT (interiors, interior design, design) hoặc sitemap của trang nguồn (chuyên mục nào 404 thì dùng sitemap). Ưu tiên bài về dự án do nhà thiết kế nội thất/studio nội thất thực hiện, nhà ở, căn hộ, khách sạn, nhà hàng có phần nội thất và đồ đạc nổi bật; tránh bài mà điểm chính là kiến trúc, hình khối hay cảnh quan. Ưu tiên bài mới. Mở bài, lấy các URL ảnh theo hướng dẫn từng trang ở trên.
6. Tải về xem thử (Read ảnh) ít nhất 6–10 ảnh ứng viên, chọn ảnh minh hoạ RÕ NHẤT cho ý chính của bài. Tiêu chí bắt buộc:
   - Ảnh nội thất ĐÃ HOÀN THIỆN, ảnh thật, không phải render, bản vẽ, sơ đồ hay ảnh quảng cáo có chữ/logo chèn lên.
   - Khung ngang (tỷ lệ rộng/cao từ 1,3 đến 1,9). KHÔNG dùng ảnh dọc hoặc vuông (engine khung hình tính cho ảnh ngang).
   - Cạnh dài ≥ 1800 px (bản gốc), nét, không mờ, không có người nhận diện được rõ mặt.
   - Nguyên lý hiện ra rõ bằng mắt thường trên ĐỒ ĐẠC, MÀU, VẬT LIỆU hoặc CÁCH BÀY ĐỒ: bạn phải chỉ ra được cụ thể món đồ nào, mảng màu nào sẽ vẽ doodle. Ảnh mà thứ nổi bật nhất là kiến trúc (trần, cột, vách kính, view) thì bỏ. Nếu phải gượng ép thì bỏ ảnh.
   - Không dùng lại ảnh đã có trong `series.json`; không dùng ảnh của dự án đã dùng trong 60 ngày.
7. Tải ảnh: `curl -sS -m 60 -o <file> <URL>`; kiểm tra bằng PIL rằng ảnh mở được. Tạo bản làm việc: thu nhỏ cạnh dài còn 2400 px (LANCZOS, giữ tỷ lệ) lưu thành `source.png`; mọi toạ độ doodle đặt theo bản làm việc này. Giữ ảnh gốc trong `OUT/original/` để tham chiếu.
8. Lấy credit từ chính trang bài (đọc kỹ chữ trên trang, không đoán): tên dự án (tiêu đề bài), studio/nhà thiết kế nội thất (ưu tiên ghi người làm nội thất; nếu bài chỉ ghi kiến trúc sư thì ghi kiến trúc sư; thường nằm trong tiêu đề hoặc đoạn credit cuối bài), nhiếp ảnh gia (các câu kiểu "Photography by …", "Photo: …"; với Yatzer, tên nhiếp ảnh gia thường có trong tên file ảnh). Ghép: `<tên dự án> · <studio> · ảnh <nhiếp ảnh gia> · <tên tạp chí nguồn>`. Nếu thiếu một mục thì bỏ mục đó, không bịa. Dòng credit trên khung hiển thị dưới dạng `Ảnh dự án: ...`; nếu dài quá 960 px thì giảm cỡ chữ dòng credit (tối thiểu 26) hoặc xuống hai dòng, không cắt.
9. Lưu `OUT/source_info.md`: URL bài nguồn, URL ảnh đã tải, thời điểm tải, credit đầy đủ, ghi chú ảnh vì sao chọn.

**Bản quyền và ghi nguồn (bắt buộc)**
Ảnh thuộc về nhiếp ảnh gia và dự án; các tạp chí đăng theo cấp phép biên tập. Vì vậy:
- Luôn hiển thị credit (bước 8 ở trên) trên khung và trong caption, kèm LINK bài gốc của tạp chí trong caption để dẫn người xem về nguồn.
- Chỉ dùng ảnh làm minh hoạ phân tích (có bình luận và nét vẽ), không dùng làm ảnh quảng cáo; không cắt bỏ credit hay watermark nếu có.
- Trong báo cáo cuối, ghi rõ dòng nhắc người dùng: "Ảnh lấy từ <tạp chí>, chưa có xin phép chính thức; cân nhắc xin phép nhiếp ảnh gia/tạp chí nếu đăng thương mại, và sẵn sàng gỡ khi có yêu cầu."

## 3. QUY TẮC THÔNG TIN: CHỈ LẤY TỪ BÀI TRONG KHO (bắt buộc, không ngoại lệ)
Bài trong KHO BÀI là nguồn thông tin duy nhất cho lời đọc, chữ trên khung và caption. Task không tự nghiên cứu (không WebSearch/WebFetch để tìm hay xác minh nội dung) và không tự viết thêm kiến thức.
1. Mọi nhận định (nguyên lý, nguồn gốc, tên người, năm, cơ chế, số liệu, lời khuyên áp dụng và chọn đồ) phải có trong bài, đúng ý và đúng mức chắc chắn của bài. Ghi vị trí trong bài (tên file + tiêu đề mục hoặc đoạn, kèm trích ngắn) vào `sources.md`.
2. Được phép: rút gọn, diễn đạt lại cho dễ nghe, đổi thứ tự cho tự nhiên, chọn ý; và mô tả điều nhìn thấy trực tiếp trên ảnh (gọi tên món đồ, màu, vật liệu trong ảnh, nói rõ là "trong ảnh này"). Không được: thêm tên, năm, số đo, tỷ lệ, nghiên cứu, ví dụ hay lời khuyên mà bài không có; dựa vào trí nhớ để bổ sung.
3. Giữ nguyên cách bài phân loại và mức chắc chắn: bài gọi là "quy tắc kinh nghiệm" thì nói là quy tắc kinh nghiệm; bài nói "có xu hướng" thì không nói "luôn luôn" hay "đã được chứng minh". Lời khuyên dùng "nên", "thử" như bài.
4. Nguồn tham khảo: nếu bài có danh mục nguồn thì chép đúng như bài ghi vào `sources.md` và chọn 2–3 nguồn chính cho caption; không tự xác minh lại, không thêm nguồn ngoài bài. Bài không có danh mục nguồn thì caption không ghi mục nguồn (không bịa), `sources.md` ghi rõ "bài không kèm nguồn".
5. Nghi bài có lỗi (năm, tên, số liệu mâu thuẫn trong chính bài): không tự sửa theo trí nhớ; bỏ nhận định đó khỏi reel và ghi rõ trong báo cáo để người dùng kiểm tra bài gốc.
6. Không nhắc thương hiệu, cửa hàng hay sản phẩm cụ thể trừ khi bài có và đó là tên đồ nội thất kinh điển (ví dụ ghế của một nhà thiết kế); không có trong bài thì không nhắc.
7. Ngoại lệ duy nhất cho phép tra cứu trên web: tìm ảnh và credit ảnh ở bốn trang nguồn (mục 2b). Thông tin trên trang tạp chí chỉ dùng cho credit và mô tả dự án trong `source_info.md`, không dùng làm nội dung bài học.

## 4. Quy trình
1. Lấy KHO BÀI, chọn bài và đọc toàn bộ bài (mục 2a). Chế độ override: dùng bài được chỉ định trong file `.txt` nếu có.
2. Kiểm tra bài và ý chính với phép thử mục 1a (áp dụng được bằng cách mua, đổi, sơn, dời, bày lại đồ). Bài lệch trọng tâm thì bỏ qua theo mục 2a.
3. Trước khi viết lời, soạn `OUT/research.md`: ghi chú bài theo đúng bảy phần ở mục 4a, mỗi ý kèm vị trí trong bài (tiêu đề mục/đoạn) và trích ngắn đúng câu chữ của bài. Phần nào bài không có thì ghi "bài không có". Kịch bản chỉ được dùng ý có trong `research.md`. Sau đó tìm ảnh (chế độ tự động, mục 2b) hoặc xem ảnh override, chọn chi tiết trên ảnh khớp với ý của bài.
4. Viết kịch bản 10–13 cảnh, tổng 45–60 giây, khoảng 110–160 từ lời đọc, theo mục 4a. Câu ngắn, dễ đọc, tự nhiên, tiếng Việt chuẩn. Lời đọc dùng để dán vào ElevenLabs nên không có ký hiệu lạ, không chú thích trong ngoặc. Mỗi cảnh tối đa khoảng 22 từ (hiển thị tối đa 3 dòng trên khung).
5. Nhờ một agent khác chưa thấy quá trình làm đọc BÀI GỐC trong kho (đưa đường dẫn file), `research.md`, `script.md`, `sources.md` và chấm theo mục 4b (chiều sâu và trung thành với bài). Sửa theo góp ý TRƯỚC khi dựng hình.
6. Đặt toạ độ doodle bằng cách tự xem ảnh (đọc ảnh bằng Read): trục, đường, hình bao đồ vật bằng đa giác thô theo toạ độ ảnh làm việc.
7. Chạy engine khung hình (mục 5). Xem LẠI từng khung (mục 7). Sửa toạ độ rồi chạy lại cho đến khi đạt.
8. Soạn `elevenlabs.txt` (mục 8b) từ lời đọc đã chốt.
9. Dựng video bằng engine video (mục 5b). Xem lại các khung trích từ video (mục 7).
10. Hoàn thiện `sources.md` (bản đầu viết cùng kịch bản ở bước 4, để agent ở bước 5 đối chiếu được), viết `caption.txt`, rồi báo cáo (mục 8).
11. Chỉ khi có file audio trong INBOX/audio: ghép tiếng vào video (mục 5c) và kiểm tra thời lượng.

## 4a. Cấu trúc kịch bản có chiều sâu (45–60 giây)
Thứ tự gợi ý; được đảo thứ tự nếu kể tự nhiên hơn, nhưng phải đủ bảy phần nội dung (B–H). Thời lượng ghi là gợi ý.
- A. Mở (1 cảnh, 3–4s): một quan sát CỤ THỂ trên ảnh dẫn vào câu hỏi (ví dụ "Hai mươi khung ảnh trên một bức tường, sao không rối?"). Không mở bằng câu chung như "Bạn có biết…".
- B. Nguồn gốc nguyên tắc (1 cảnh, 4–5s): ai đề xuất hay làm nổi tiếng nó, năm nào, trong bối cảnh nào, theo đúng bài: nhà lý thuyết màu (Itten, Albers), nhà thiết kế nội thất hoặc nhà trang trí, nhà thiết kế đồ nội thất và tạo dáng công nghiệp, nhà nghiên cứu tri giác. Không lấy kiến trúc sư hay lý thuyết kiến trúc làm nguồn gốc. Chỉ nêu tên, năm khi bài có.
- C. Cơ chế, vì sao mắt thấy vậy (1–2 cảnh, 6–9s): giải thích bằng ngôn ngữ đời thường điều bài nói (mắt/não làm gì, khi nào thì xảy ra, yếu tố nào mạnh hơn yếu tố nào nếu bài có nói). Đây là phần tạo chiều sâu chính, không được thay bằng câu định nghĩa.
- D. Đọc trên ảnh (2–3 cảnh, 10–14s): mỗi cảnh một chi tiết, zoom vào đúng MÓN ĐỒ, MẢNG MÀU, VẬT LIỆU hay NHÓM ĐỒ, gọi tên nó và chỉ ra nguyên lý đang hoạt động thế nào ở đó (màu gì lặp ở đâu, dáng ghế ra sao, chất liệu nào đặt cạnh chất liệu nào, khoảng cách giữa các món…).
- E. Lỗi hay gặp hoặc phản ví dụ (1 cảnh, 4–6s): nếu làm sai thì trông thế nào. Không dựng ảnh khác; dùng chính ảnh với nét gợi ý (ví dụ mũi tên "nếu dời khung này ra xa…") hoặc chỉ vào chỗ trong ảnh mà nguyên lý bị phá có chủ ý.
- F. Cách áp dụng cụ thể (1 cảnh, 4–6s): một hai việc người xem làm được ngay trong nhà mình, đủ cụ thể để làm theo, lấy từ bài (mục 3).
- G. Chọn mua, chọn đồ (1 cảnh, 4–6s): nguyên tắc này đổi cách chọn đồ thế nào: chọn dáng, màu, kích thước, chất liệu, hoạ tiết, chọn theo bộ hay phối lẻ, chọn bao nhiêu món; lấy từ bài (mục 3). Đây là phần người xem cần nhất, phải cụ thể.
- H. Công thức (1 cảnh, 3–4s): một câu tóm tắt dễ nhớ, có thông tin (không phải khẩu hiệu rỗng).
- I. Cảnh cuối (1 cảnh, 7–9s, tính trong tổng 45–60 giây): nhắc AH Decode là series về nguyên tắc thiết kế và chọn đồ decor, mời theo dõi Fanpage Giả Thuyết Kiến Trúc và nhắc bài viết về kiến trúc dành riêng cho thành viên ở link bình luận. KHÔNG nhắc tập sau, không đọc nguồn hay credit. Lời đọc mẫu (giữ ngắn, khoảng 25 từ): "AH Decode, series về nguyên tắc thiết kế và chọn đồ decor. Theo dõi Giả Thuyết Kiến Trúc, bài viết cho thành viên ở link bình luận."
Quy tắc chiều sâu:
- Nội dung B–H lấy từ bài (mục 3). Bài không có nội dung cho một phần thì gộp hoặc bỏ phần đó, ghi rõ trong `script.md` và báo cáo; KHÔNG tự nghiên cứu hay tự viết để lấp chỗ trống. Riêng phần D (đọc trên ảnh) luôn làm được vì là quan sát trên ảnh.
- Mỗi cảnh phải chứa ít nhất một thông tin cụ thể (tên người/khái niệm, cơ chế, điều kiện, vật cụ thể trong ảnh, việc làm cụ thể). Câu nào bỏ đi mà người xem không mất thông tin gì thì bỏ.
- Cấm các cụm chung chung không kèm giải thích: "tạo cảm giác hài hoà", "trông đẹp hơn", "thu hút ánh nhìn", "tạo điểm nhấn", "cân bằng thị giác" khi chưa nói vì sao và bằng cách nào.
- Không lặp lại cùng một ý bằng chữ khác để kéo dài thời lượng.
- Ngân sách chữ chặt: 110–160 từ cho CẢ 13 cảnh, nên mỗi câu phải gọn. Cách làm đã dùng ở tập 2: viết dữ liệu cảnh một lần trong script sinh engine, tự tính thời lượng mỗi cảnh = 0,7 giây + số từ / 3,2 (tối thiểu 3,5 giây), rồi in tổng số từ và tổng thời lượng để cắt cho vừa trước khi dựng.
- Lời khuyên (phần E, F, G) lấy từ bài, dùng "nên", "thử", "nên tránh"; không viết "Vì vậy…" như thể suy luận là kết luận của nghiên cứu.

## 4b. Tự chấm trước khi dựng hình
Agent đọc lại (bước 5) trả lời có/không cho từng câu, kèm lý do:
0. Tập có đúng trọng tâm mục 1a không (nội thất, decor, màu, đồ đạc, vật liệu, bố cục đồ; không phải lý thuyết kiến trúc)? Có câu, cảnh hay nguồn nào lệch sang kiến trúc không? Có thì phải sửa, kể cả đổi nguyên tắc.
1. Có đủ bảy phần B–H, mỗi phần có ít nhất một ý cụ thể?
2. Phần cơ chế có nói được vì sao (không chỉ nhắc lại định nghĩa)? Có đúng điều bài viết không?
3. Người xem có học được ít nhất ba điều cụ thể họ có thể chưa biết? Liệt kê ba điều đó.
4. Có câu chung chung, lặp ý hoặc nói quá bài nào không? Liệt kê.
5. Lời khuyên áp dụng và chọn đồ có làm theo được ngay không, và có đúng như bài không?
6. Mọi nhận định đều có trong bài gốc và có dòng tương ứng (vị trí trong bài) trong `sources.md`? Có tên, năm, số liệu, lời khuyên nào ngoài bài không? Liệt kê.
Có câu trả lời "không" thì sửa kịch bản cho đúng bài (không tìm thêm nguồn ngoài bài), rồi mới dựng hình.

## 5. Engine dựng khung (thư mục ENGINE = REPO/engine)
Gồm: `engine_video.py` (mục 5b), `engine_storyboard_v7.py` (chạy bằng `python3 -I`; script tự thêm thư mục của nó vào sys.path), `silhouette.py`, `PatrickHand-Regular.ttf`, `reel1_source_example.png` (ảnh mẫu tập #1). Cần: Python 3, Pillow, numpy, opencv-python (pip cần `--break-system-packages`), ffmpeg.
Chạy: `python3 -I engine_storyboard_v7.py <ảnh> <thư_mục_ra>`
Engine v7 đang hard-code ảnh và toạ độ của tập #1. Mỗi tập, sao chép thành `engine_epNN.py` rồi sửa CHỈ các phần sau:
- `SCENES` (tiêu đề `head`, lời `vo`, thời lượng `t`, camera `cam=(điểm_focus_trên_ảnh, zoom, vị_trí_trên_khung)`, `dark`). Cảnh cuối luôn có `head="end"`, `vo=""`.
- `OBJ`: đa giác thô quanh đồ vật (toạ độ ảnh làm việc). Hàm `doodle()`: trục, đường nối, hình bao, nhãn.
- `CREDIT`, `HEAD` (đầu trang luôn là `AH DECODE · <TÊN CHỦ ĐỀ VIẾT HOA>`), tên file ra.
Không đổi: kích thước 1080×1920, nền trắng, băng keo giấy ở giữa mép trên, ảnh không viền, chữ viết tay Patrick Hand, bố cục chữ, khung cuối `END_LINES` (đã cố định: "AH Decode · series phân tích nguyên tắc thiết kế và cách chọn đồ decor / Theo dõi Fanpage / Giả Thuyết Kiến Trúc / Bài viết về kiến trúc dành riêng cho thành viên / Link ở phần bình luận").
Cách làm nhanh đã dùng ở tập 2 (xem `inbox/out/2026-10-06_gestalt-gan-nhau/engine_ep02/`): viết một script nhỏ đọc hai engine gốc, thay khối từ dòng `# ---------------- scenes` đến trước `def render_scene` (engine khung) hoặc trước `BOARDS["plain"] = make_board(1.0)` (engine video) bằng khối dữ liệu của tập, thay `CREDIT`, `HEAD`, tên file ra, rồi ghi thành `engine_epNN.py` và `engine_video_epNN.py`. Một nguồn dữ liệu cho cả hai engine nên chúng luôn đồng bộ. Hàm `D(pts)` trong khối dữ liệu đó đổi toạ độ đo trên ảnh xem thu nhỏ sang ảnh làm việc 2400 px.
Cảnh không có vật để khoanh (nguồn gốc, cơ chế) vẫn phải có hình: dùng cảnh rộng hoặc zoom vào vùng liên quan, nét doodle tối giản (một đường, một mũi tên) hoặc không nét; không chèn đồ hoạ khác.

## 5b. Engine dựng video (`engine_video.py`, nằm cùng thư mục ENGINE)
Là bản mở rộng của engine khung hình: cùng `SCENES`, `OBJ`, `doodle()`, `CREDIT`, `HEAD`. Mỗi tập sao chép thành `engine_video_epNN.py` và sửa CÙNG các phần như mục 5, nên giữ hai engine đồng bộ (sửa dữ liệu cảnh một lần, dán sang cả hai).
Chạy: `python3 -I engine_video_epNN.py <ảnh> <thư_mục_ra>` → `<thư_mục_ra>/video/reel1_silent.mp4` (đổi tên thành `reel_<slug>_silent.mp4`).
Mất khoảng 6–7 phút cho mỗi 30 giây video (30 fps, 1080×1920, H.264 CRF 17), tức khoảng 10–15 phút cho reel 45–60 giây: chạy nền (`nohup … > log 2>&1 &`), làm việc khác trong lúc chờ, rồi kiểm tra log. Engine ghi thêm vài ảnh `probe_*.png` vào thư mục `video/`: xoá sau khi chuyển file mp4 ra.
Hành vi đã duyệt, không tự ý đổi:
- Thời lượng mỗi cảnh lấy từ trường `t` của `SCENES` (ví dụ "3–8s"); video dài đến hết cảnh cuối + 1 giây.
- Chuyển cảnh 0,7 giây: camera nội suy zoom và vị trí; chữ và nét của cảnh cũ mờ đi trong 0,25 giây đầu; tiêu đề và lời đọc của cảnh mới hiện ra ở cuối quãng chuyển.
- Nét doodle được vẽ dần (theo thứ tự các nét trong `doodle()`), bắt đầu sau khi camera dừng, xong ở khoảng 62% thời lượng cảnh; nhãn chữ trong `doodle()` hiện khi nét vẽ đạt khoảng 55–75%.
- Khung cuối giữ thêm 1 giây. Video có sẵn track âm thanh im lặng để ghép tiếng sau.
Nếu một cảnh quá ngắn để vẽ hết nét (cảnh nhiều nét mà dưới 3 giây), kéo dài cảnh đó trong `SCENES` hoặc bớt nét, không tăng tốc vẽ.

## 5c. Ghép giọng ElevenLabs (chỉ khi có audio)
1. Đo thời lượng audio: `ffprobe -v error -show_entries format=duration -of csv=p=0 <audio>`.
2. So với thời lượng video:
   - Chênh trong ±1,5 giây: ghép luôn.
   - Audio dài hơn video hơn 1,5 giây, hoặc ngắn hơn hơn 3 giây: KHÔNG tự cắt hay kéo giãn giọng. Điều chỉnh `t` các cảnh (kéo dài/rút ngắn cảnh có lời nhiều/ít) theo nhịp đọc rồi dựng lại video; nếu không biết ranh giới từng câu, dùng `ffmpeg -af silencedetect=noise=-35dB:d=0.25` để tìm các quãng nghỉ, ghép từng câu với từng cảnh theo thứ tự trong `elevenlabs.txt`.
3. Ghép: `ffmpeg -y -i video_silent.mp4 -i audio -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest out.mp4`. Nếu audio ngắn hơn video, thêm `-af apad` rồi `-t <thời lượng video>` thay cho `-shortest`.
4. Chuẩn âm lượng nhẹ: `-af loudnorm=I=-16:TP=-1.5:LRA=11`.
5. Kiểm tra bằng cách trích vài khung và đối chiếu thời điểm nhãn chữ với câu đang đọc (dùng silencedetect); báo cáo nếu lệch quá 1 giây.

## 6. Quy cách hình ảnh (đã duyệt, không tự ý đổi)
- Khung 1080×1920. Nền trắng trơn. Ảnh dự án là ảnh GỐC, không sketch hoá, không làm mờ; dán bằng một miếng băng keo giấy ở giữa mép trên, không viền, hơi nghiêng ~1°, có bóng nhẹ.
- Cảnh rộng: ảnh nằm giữa khung; chữ nằm NGOÀI ảnh (nâu đậm), mũi tên trắng/nâu chỉ vào nét doodle. Cảnh nói chi tiết: camera zoom vào ảnh; khi hết chỗ nền thì chữ trắng viết lên ảnh, có phủ tối nhẹ để dễ đọc.
- Mọi nét doodle trên ảnh: màu TRẮNG, NÉT ĐỨT, nét tay tự nhiên. Đồ vật được bao bằng đường đứt ôm theo hình dáng tổng quát (không khoanh tròn), sau khi zoom vào đúng đồ vật/cụm.
- Tất cả chữ viết tay. Header nhỏ ở trên cùng, tiêu đề cảnh bên dưới, KHÔNG đánh số "Bước n". Dòng credit nhỏ ngay dưới ảnh. Không gạch chân lượn sóng.
- Khung cuối: ảnh rộng + credit dưới ảnh, rồi "AH Decode · series phân tích nguyên tắc thiết kế và cách chọn đồ decor / Theo dõi Fanpage / Giả Thuyết Kiến Trúc / Bài viết về kiến trúc dành riêng cho thành viên / Link ở phần bình luận" (đã cố định trong engine). Không có dòng nguồn, không nhắc tập sau.

## 7. Kiểm tra bắt buộc trước khi giao (đọc từng khung bằng Read)
- Hình bao ôm đúng đồ vật được nhắc trong lời đọc; nét không tràn ra ngoài ảnh; không có "cục" đậm do nét chồng nhau.
- Chữ đọc rõ, có đủ dấu tiếng Việt, không bị cắt, không đè lên nét vẽ khó đọc, không nằm vắt ngang mép ảnh.
- Lời đọc khớp với hình trong cùng cảnh, tổng thời lượng 45–60 giây (tốc độ đọc khoảng 2,5–3 từ/giây), 110–160 từ.
- Đủ bảy phần nội dung B–H của mục 4a; đã qua tự chấm mục 4b.
- Từng nhận định trong lời đọc đều có trong bài gốc và có dòng tương ứng trong `sources.md` (mục 3.1); không có nhận định ngoài bài.
- Video: trích ít nhất 12 khung (đầu, giữa quá trình vẽ, cuối từng cảnh chính, khung cuối) để kiểm tra: nét vẽ đã đủ khi cảnh kết thúc, không có nét của cảnh cũ lẫn sang cảnh mới, chữ không bị cắt, chuyển cảnh không giật. Kiểm tra `ffprobe`: 1080×1920, h264, có track âm thanh, thời lượng đúng dự kiến.
- Không có logo, thương hiệu hay tên người xuất hiện sai trong khung.
Kịch bản và nguồn đã được agent độc lập chấm ở bước 5 mục 4; nếu sau đó kịch bản còn đổi, nhờ đọc lại lần nữa.

## 8. Đầu ra (OUT = INBOX/out/<YYYY-MM-DD>_<slug>/)
- `research.md`: ghi chú bài theo bảy phần mục 4a, kèm vị trí và trích ngắn trong bài (bước 3 mục 4). Đầu file ghi bài đã dùng: đường dẫn trong kho, link GitHub, commit SHA.
- `script.md`: bảng cảnh (thời lượng, phần nội dung A–I, tiêu đề, lời đọc, hình) + phần lời đọc liền mạch + kết quả tự chấm mục 4b.
- `elevenlabs.txt`: văn bản thuần để người dùng dán thẳng vào ElevenLabs (mục 8b).
- `source_info.md`, `original/`.
- `frames/scene_*.png` + `storyboard.png` + `frames.zip`.
- `reel_<slug>_silent.mp4` (và `reel_<slug>_final.mp4` nếu đã có audio).
- `sources.md`: mỗi nhận định → vị trí trong bài (file + mục/đoạn + trích ngắn) → mức chắc chắn theo bài (nguyên lý / thực nghiệm / quy tắc kinh nghiệm) → nguồn mà bài dẫn cho ý đó (nếu có, chép đúng như bài). Cuối file: danh mục nguồn tham khảo của bài.
- `caption.txt`: caption đăng bài có chiều sâu, bổ sung cho reel (không chép lại lời đọc): vài đoạn ngắn về nguồn gốc, cơ chế, cách áp dụng và gợi ý chọn đồ, lấy từ bài theo cùng quy tắc mục 3 như lời đọc; rồi dòng giới thiệu và mời "AH Decode là series mới của Giả Thuyết Kiến Trúc, phân tích các nguyên tắc thiết kế và cách chọn đồ decor. Theo dõi Fanpage Giả Thuyết Kiến Trúc. Các bài viết về kiến trúc dành riêng cho thành viên: link ở phần bình luận."; rồi 2–3 nguồn chính lấy từ danh mục nguồn của bài (nếu bài có), credit ảnh đầy đủ và link bài gốc của tạp chí; hashtag vừa phải. Không tự điền link thành viên (người dùng tự dán vào bình luận).
- Gửi cho người dùng (SendUserFile): `elevenlabs.txt` đầu tiên, rồi video, ảnh bảng phân cảnh, `script.md`, `sources.md`, `caption.txt`; kèm tóm tắt tối đa 6 dòng: bài đã dùng trong kho, nguyên lý, ba điều người xem học được, điểm cần duyệt (kể cả phần bài thiếu hoặc nghi lỗi), credit đã có hay còn thiếu, và nhắc "gửi lại file giọng đọc vào INBOX/audio để ghép tiếng".
Đây là BẢN NHÁP chờ người dùng duyệt. Không đăng, không gửi đi đâu khác.

## 8b. Quy cách `elevenlabs.txt`
Mục tiêu: người dùng mở file, chọn tất cả, dán vào ElevenLabs, không phải sửa gì.
- Chỉ có lời đọc, theo đúng thứ tự cảnh. Không đánh số cảnh, không tiêu đề, không chú thích, không ngoặc chỉ dẫn, không emoji, không hashtag, không tên file.
- Mỗi cảnh một đoạn; giữa các đoạn cách một dòng trống. Trong đoạn, mỗi câu một dòng.
- Đọc được thành tiếng một cách tự nhiên: viết số, ký hiệu và từ viết tắt thành chữ (ví dụ "60-30-10" thành "sáu mươi, ba mươi, mười"; "≠" thành "không bằng"; "%" thành "phần trăm").
- PHIÊN ÂM SẴN mọi tên và từ tiếng Anh (hoặc tiếng nước ngoài khác) ngay trong lời đọc, để người dùng dán thẳng vào ElevenLabs, KHÔNG phải sửa gì: tên người, tên tác phẩm, tên series, thuật ngữ tiếng Anh. Viết theo âm tiếng Việt, các âm tiết nối bằng gạch nối, không để kèm chính tả gốc trong ngoặc. Ví dụ: "AH Decode" → "Ây-ết Đi-cốt"; "decor" → "đê-co"; "Hogarth" → "Hô-gát"; "Dieter Rams" → "Đi-tơ Ram"; "Charles và Ray Eames" → "Sác-lơ và Rây Im-xơ"; "Hans Wegner" → "Han Ve-gơ-nơ"; "Josef Albers" → "Giô-dép An-bơ"; "Bauhaus" → "Bao-hao". Chọn cách đọc theo ngôn ngữ gốc của tên (tên Đức đọc kiểu Đức…). Giữ CÙNG một cách phiên âm cho cùng một tên trong cả file.
- Chỉ `elevenlabs.txt` dùng phiên âm. Chữ trên khung hình, `script.md` và `caption.txt` giữ chính tả gốc. Trong `script.md` thêm bảng nhỏ "Phiên âm cho ElevenLabs" (chính tả gốc → phiên âm) để người dùng tra.
- Dấu câu để điều khiển nhịp: dấu phẩy và chấm đủ rõ; chỗ cần ngắt dài hơn thì dùng dấu "..." hoặc dòng trống, không chèn thẻ kỹ thuật. Câu ngắn, tối đa khoảng 18 từ.
- Độ dài khớp thời lượng cảnh trong `SCENES`: khoảng 2,5–3 từ mỗi giây, trừ khoảng 0,7 giây chuyển cảnh ở đầu mỗi cảnh. Cuối file ghi thêm một dòng riêng NGOÀI phần dán: `--- Gợi ý cài đặt: giọng nữ hoặc nam trầm ấm, tốc độ 1.0, mô hình đa ngôn ngữ, ngôn ngữ Vietnamese ---` để người dùng tham khảo (dòng này phân tách bằng một dòng trống và dấu `---`, người dùng chỉ dán phần phía trên). Không ghi chú tên riêng hay cách đọc ở dòng này vì lời đọc đã phiên âm sẵn.
- Cảnh cuối chỉ đọc câu giới thiệu series AH Decode, lời mời theo dõi Fanpage Giả Thuyết Kiến Trúc và nhắc bài viết về kiến trúc dành riêng cho thành viên, link ở phần bình luận (mẫu ở mục 4a, phần I). Không gợi ý tập sau, không đọc nguồn hay credit. Cảnh cuối trong `elevenlabs.txt` viết dạng phiên âm, ví dụ: "Ây-ết Đi-cốt, series về nguyên tắc thiết kế và chọn đồ đê-co. Theo dõi Giả Thuyết Kiến Trúc, bài viết cho thành viên ở link bình luận." ("series" và "link" là từ quen dùng trong tiếng Việt, giữ nguyên.)

## 9. Khi gặp sự cố
- Không truy cập được trang nguồn nào hoặc không tìm được ảnh đạt tiêu chí sau khi xem ít nhất 10 ứng viên: dừng, báo rõ lý do và các ảnh/bài đã thử; KHÔNG chuyển sang nguồn ảnh khác, KHÔNG lấy ảnh từ Google/Pinterest.
- Ảnh quá nhỏ (<1200 px cạnh dài), quá tối, hoặc không minh hoạ được ý chính của bài: vẫn làm bản tốt nhất có thể, ghi rõ hạn chế (ví dụ zoom bị mềm) và đề nghị ảnh khác.
- Không truy cập được KHO BÀI (add_repo/clone/GitHub MCP đều lỗi, hoặc không thấy thư mục `AH-Decode-Decor/` trên nhánh `AH-Interior-notes`): dừng, báo lỗi cụ thể. KHÔNG tự nghiên cứu để thay thế.
- Hết bài chưa dùng trong kho: dừng và báo người dùng thêm bài; không tự viết bài mới, không dùng lại bài cũ.
- Bài thiếu nội dung cho một vài phần B–H: làm với phần bài có (mục 4a), ghi rõ phần thiếu trong báo cáo. Bài quá mỏng để làm reel 45–60 giây có chiều sâu: vẫn làm bản tốt nhất, ghi rõ hạn chế; không tự bổ sung kiến thức ngoài bài.
- Dựng video quá thời gian hoặc ffmpeg lỗi: vẫn giao khung hình, script và `elevenlabs.txt`, nói rõ video chưa dựng được và vì sao.
- Công cụ lỗi (mạng, thư viện): thử lại một lần, rồi báo lỗi cụ thể thay vì bỏ qua bước.

## 10. Việc KHÔNG làm
- Không tự nghiên cứu, không lấy thông tin nội dung từ web hay từ trí nhớ; chỉ dùng bài trong KHO BÀI (mục 3). Không sửa hay push gì vào kho bài.
- Không đổi quy cách hình ảnh ở mục 6. Không sketch hoá ảnh dự án. Không bỏ credit.
- Không dùng ảnh/đồ hoạ ngoài ảnh đã chọn từ bốn trang nguồn ở mục 2b (hoặc ảnh người dùng gửi ở chế độ override). Không dùng Est Living, The Local Project hay bất kỳ nguồn ảnh nào khác.
- Không đổi nhịp chuyển cảnh/vẽ nét đã duyệt (mục 5b), không thêm nhạc nền, hiệu ứng hay phụ đề chạy chữ khi chưa được yêu cầu.
- Không bịa tên studio, nhiếp ảnh gia hay dự án khi thiếu credit; chỉ ghi những gì có trên trang bài nguồn.
- Không hẹn hay gợi ý "tập sau" ở bất kỳ đâu (khung, lời đọc, caption).
- Không làm tập về lý thuyết kiến trúc hay không gian công trình (mục 1a): không prospect–refuge, không phân tích nhà của kiến trúc sư, không lấy trần, cột, vách kính, view làm nội dung chính.
- Không dừng giữa chừng để chờ duyệt lý thuyết hay ảnh.