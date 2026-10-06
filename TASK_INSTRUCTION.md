# INSTRUCTION — Scheduled task "AH Decode · Reel hằng ngày"

Kho mã và dữ liệu: GitHub `buithucdatqn-sketch/claude` (nhánh `main`). Cách lấy: dùng add_repo (quyền push) rồi `git clone --depth 1 https://github.com/buithucdatqn-sketch/claude /home/claude/claude` (timeout lệnh ≥ 10 phút; chỉ MỘT lệnh git tại một thời điểm), sau đó gọi register_repo_root. Gọi thư mục clone là REPO. Cấu trúc: `REPO/engine/` (bộ engine), `REPO/inbox/` (INBOX), `REPO/TASK_INSTRUCTION.md` (bản sao của chính tài liệu này). Cuối mỗi lần chạy: chép `engine_epNN.py` và `engine_video_epNN.py` vào `OUT/engine_epNN/`, `git add inbox`, commit, và `git pull --rebase origin main && git push origin main` (một lần; nếu bị 429 thì đợi 10 giây thử lại một lần).

Mỗi lần chạy là một phiên mới, không nhớ gì từ các cuộc trò chuyện trước. Mọi thông tin cần thiết nằm trong tài liệu này và thư mục INBOX.
Chạy một lượt, không hỏi lại. Nếu thiếu đầu vào thì dừng và báo rõ thiếu gì (mục 9).

## 1. Nhiệm vụ
Mỗi ngày, TỰ chọn MỘT nguyên lý thiết kế decor nội thất, rồi TỰ lấy MỘT ảnh dự án thật trên một trong các tạp chí thiết kế (Yatzer, Yellowtrace, Dwell, Wallpaper*) phù hợp để minh hoạ nguyên lý đó, và tạo gói sản xuất cho một reel dọc 9:16, dài 45–60 giây, series "AH Decode". Reel giải thích MỘT nguyên lý trang trí nội thất bằng các nét doodle trắng nét đứt vẽ lên chính ảnh gốc.
Mỗi reel là một bài học TRỌN VẸN và CÓ CHIỀU SÂU (mục 4a): nguồn gốc lý thuyết, cơ chế vì sao mắt thấy vậy, đọc nguyên lý trên ảnh, lỗi hay gặp, cách áp dụng cụ thể, cách chọn mua/chọn đồ và thiết kế, rồi công thức tổng kết. Người xem phải học được điều cụ thể mà họ chưa biết, không phải những câu chung chung. Không hẹn "tập sau"; cảnh cuối chỉ mời theo dõi Fanpage Giả Thuyết Kiến Trúc và các bài viết về kiến trúc dành riêng cho thành viên (link ở phần bình luận).

**Tên gọi (dùng đúng, không lẫn):** Fanpage tên là **Giả Thuyết Kiến Trúc**. **AH Decode** là một series MỚI của Fanpage này, chuyên phân tích các nguyên tắc thiết kế và cách chọn đồ decor. AH Decode KHÔNG phải tên Fanpage: không viết "Fanpage AH Decode". Header trên khung vẫn là `AH DECODE · <CHỦ ĐỀ>`.
Chạy trọn một lượt, không chờ duyệt lý thuyết hay ảnh giữa chừng.
Gói gồm: (1) kịch bản lời đọc theo cảnh và file chữ thuần để dán vào ElevenLabs, (2) các khung hình 1080×1920, (3) bảng phân cảnh, (4) video reel dựng sẵn (bản không tiếng, hoặc có tiếng nếu đã có audio), (5) danh mục nguồn đã đối chiếu, (6) caption đăng bài.
Người dùng nói tiếng Việt, mọi chữ trên khung và lời đọc đều bằng tiếng Việt.

## 2. Đầu vào (INBOX = REPO/inbox)
Chế độ mặc định là TỰ ĐỘNG: không cần người dùng gửi ảnh. Chỉ cần:
- `INBOX/series.json`: danh sách các tập đã làm (số tập, nguyên lý, URL bài nguồn và URL ảnh đã dùng, ngày). Nếu chưa có thì tạo mới. Dùng để không lặp lại nguyên lý hoặc ảnh/dự án đã dùng (không dùng lại cùng một dự án trong 60 ngày gần nhất).
- `INBOX/override/` (tuỳ chọn, có thì ưu tiên): `<tên>.jpg|png` ảnh do người dùng gửi + `<tên>.txt` (dòng 1 = credit đúng dạng `tên dự án · studio · nhiếp ảnh gia`, các dòng sau = nguyên lý muốn nói). Có thư mục này thì bỏ qua mục 2b, làm đúng như ảnh người dùng gửi.
- `INBOX/audio/<slug>.mp3|wav|m4a` (tuỳ chọn): giọng đọc ElevenLabs của chính tập này (người dùng làm từ file `elevenlabs.txt` của lần chạy trước). Có file này thì làm bước 9 (ghép tiếng) trong mục 4.
- Xử lý xong: cập nhật `series.json`; ảnh override chuyển sang `INBOX/done/`.

## 2b. Chọn nguyên lý và lấy ảnh từ tạp chí thiết kế (chế độ tự động)
**Nguồn ảnh (chỉ các trang sau, không trang nào khác):** Yatzer (www.yatzer.com), Yellowtrace (www.yellowtrace.com.au), Dwell (www.dwell.com), Wallpaper* (www.wallpaper.com). Đã thử: bốn trang này truy cập được bằng `curl -A "Mozilla/5.0"`. The Local Project chặn truy cập tự động (403 Cloudflare) và Est Living chặn bằng captcha: KHÔNG dùng và KHÔNG cố vượt. Đầu mỗi lần chạy kiểm tra từng trang bằng `curl -sS -m 20 -L -A "Mozilla/5.0" -o /dev/null -w "%{http_code}" <URL>`; trang nào không trả 200 thì bỏ qua lần đó. Nếu không trang nào truy cập được thì dừng và báo (mục 9).
Cách lấy ảnh theo trang (cấu trúc có thể đổi, hãy xem HTML thật):
- Yatzer: trang bài chứa `https://media.yatzer.com/...jpg`; bản không hậu tố kích thước là bản gốc lớn nhất, `-1400x…` là dự phòng. Credit nhiếp ảnh: câu "Photography by …" trong bài.
- Yellowtrace: bài viết WordPress; ảnh ở `assets.yellowtrace.com.au/wp-content/uploads/...`; bỏ hậu tố kích thước `-1040x700` để lấy bản gốc (nếu 404 thì dùng bản có hậu tố lớn nhất). Credit nằm trong bài ("Photography by/Photo by …").
- Dwell: ảnh ở `images2.dwell.com/photos/.../original.jpg`. Credit nhiếp ảnh và kiến trúc sư nằm trong bài hoặc chú thích ảnh.
- Wallpaper*: lấy ảnh từ thẻ `og:image`/`img` trong bài (ưu tiên URL lớn nhất); credit nằm ở chú thích ảnh hoặc cuối bài ("Photography: …").
Mỗi lần chọn trang có ảnh phù hợp nguyên lý nhất; luân phiên giữa các trang để đa dạng, không dùng một trang quá hai ngày liên tiếp.

**Chọn nguyên lý (task tự tìm và chọn lọc, không đợi người dùng)**
1. Tự tìm nguyên lý trong chính các nguồn học thuật ở mục 3 (giáo trình, chuyên khảo, nghiên cứu có phản biện), không lấy từ các tạp chí ảnh. Dùng WebSearch/WebFetch để đọc chương, đoạn trích, abstract, rồi chọn MỘT nguyên lý mà: (a) được nêu rõ trong ít nhất 2 nguồn học thuật độc lập; (b) có thể minh hoạ bằng nét vẽ trên một ảnh nội thất (đường, trục, hình, khối, màu, nhịp); (c) đủ chất liệu cho cả bảy phần ở mục 4a trong 45–60 giây; (d) chưa dùng trong `series.json`; (e) đọc được NỘI DUNG giải thích (abstract đầy đủ, đoạn trích sách, toàn văn mở), không chỉ thấy tên nguyên lý trong mục lục. Chỉ thấy mục lục thì chưa đủ để nói cơ chế: chọn nguyên lý khác có nguồn đọc được.
   Nên ưu tiên phạm vi hẹp và cụ thể (ví dụ "gần nhau: khoảng cách quyết định nhóm" thay vì "các nguyên lý Gestalt") để có chỗ đi sâu.
2. Danh mục tham khảo để bắt đầu (không giới hạn, có thể mở rộng khi tìm thêm nguồn xác minh được): cân bằng (đối xứng, bất đối xứng, hướng tâm), trục, nhịp điệu và lặp lại, tiến cấp, điểm nhấn và thứ bậc thị giác, tỷ lệ và scale, khoảng thở (negative space), thống nhất và hài hoà, tương phản và đa dạng, các nguyên lý Gestalt (gần nhau, tương đồng, liên tục, khép kín, nền–hình), sắc độ/độ sáng/độ bão hoà, bảng màu tương cận và bổ túc, tỷ lệ phân bổ màu (60-30-10 chỉ là quy tắc kinh nghiệm), nhiệt độ màu, chất liệu và vân, pha hoạ tiết, ánh sáng nhiều lớp, lớp trước–giữa–sau, ngưỡng và chuyển tiếp, prospect–refuge, đường dẫn mắt.
3. Xoay vòng: ưu tiên nhóm chưa dùng nhiều; hết danh mục thì quay lại với góc nhìn khác. Ghi nguyên lý và các nguồn đã dùng vào `series.json`.
4. Chỉ giữ nguyên lý nếu qua được mục 3 (≥ 3 nguồn đã xác minh ở mức tương xứng, trong đó phần cơ chế đọc được nội dung). Nếu không thì chọn nguyên lý khác.

**Tìm ảnh minh hoạ trên các trang nguồn**
5. Lấy danh sách bài từ trang chủ, chuyên mục nội thất/kiến trúc hoặc sitemap của trang nguồn (chuyên mục nào 404 thì dùng sitemap). Chọn các bài về nhà ở/nội thất công trình đã hoàn thành, ưu tiên bài mới. Mở bài, lấy các URL ảnh theo hướng dẫn từng trang ở trên.
6. Tải về xem thử (Read ảnh) ít nhất 6–10 ảnh ứng viên, chọn ảnh minh hoạ RÕ NHẤT cho nguyên lý. Tiêu chí bắt buộc:
   - Ảnh nội thất ĐÃ HOÀN THIỆN, ảnh thật, không phải render, bản vẽ, sơ đồ hay ảnh quảng cáo có chữ/logo chèn lên.
   - Khung ngang (tỷ lệ rộng/cao từ 1,3 đến 1,9). KHÔNG dùng ảnh dọc hoặc vuông (engine khung hình tính cho ảnh ngang).
   - Cạnh dài ≥ 1800 px (bản gốc), nét, không mờ, không có người nhận diện được rõ mặt.
   - Nguyên lý hiện ra rõ bằng mắt thường: bạn phải chỉ ra được cụ thể vật nào, đường nào sẽ vẽ doodle. Nếu phải gượng ép thì bỏ ảnh.
   - Không dùng lại ảnh đã có trong `series.json`; không dùng ảnh của dự án đã dùng trong 60 ngày.
7. Tải ảnh: `curl -sS -m 60 -o <file> <URL>`; kiểm tra bằng PIL rằng ảnh mở được. Tạo bản làm việc: thu nhỏ cạnh dài còn 2400 px (LANCZOS, giữ tỷ lệ) lưu thành `source.png`; mọi toạ độ doodle đặt theo bản làm việc này. Giữ ảnh gốc trong `OUT/original/` để tham chiếu.
8. Lấy credit từ chính trang bài (đọc kỹ chữ trên trang, không đoán): tên dự án (tiêu đề bài), studio/kiến trúc sư (thường nằm trong tiêu đề hoặc đoạn credit cuối bài), nhiếp ảnh gia (các câu kiểu "Photography by …", "Photo: …"; với Yatzer, tên nhiếp ảnh gia thường có trong tên file ảnh). Ghép: `<tên dự án> · <studio> · ảnh <nhiếp ảnh gia> · <tên tạp chí nguồn>`. Nếu thiếu một mục thì bỏ mục đó, không bịa. Dòng credit trên khung hiển thị dưới dạng `Ảnh dự án: ...`; nếu dài quá 960 px thì giảm cỡ chữ dòng credit (tối thiểu 26) hoặc xuống hai dòng, không cắt.
9. Lưu `OUT/source_info.md`: URL bài nguồn, URL ảnh đã tải, thời điểm tải, credit đầy đủ, ghi chú ảnh vì sao chọn.

**Bản quyền và ghi nguồn (bắt buộc)**
Ảnh thuộc về nhiếp ảnh gia và dự án; các tạp chí đăng theo cấp phép biên tập. Vì vậy:
- Luôn hiển thị credit (bước 8 ở trên) trên khung và trong caption, kèm LINK bài gốc của tạp chí trong caption để dẫn người xem về nguồn.
- Chỉ dùng ảnh làm minh hoạ phân tích (có bình luận và nét vẽ), không dùng làm ảnh quảng cáo; không cắt bỏ credit hay watermark nếu có.
- Trong báo cáo cuối, ghi rõ dòng nhắc người dùng: "Ảnh lấy từ <tạp chí>, chưa có xin phép chính thức; cân nhắc xin phép nhiếp ảnh gia/tạp chí nếu đăng thương mại, và sẵn sàng gỡ khi có yêu cầu."

## 3. QUY TẮC NGUỒN (bắt buộc, không ngoại lệ)
Mọi nhận định phân tích (nguyên lý, cơ chế tri giác, quy tắc phối màu…) phải đối chiếu được với sách giáo trình, chuyên khảo hoặc nghiên cứu có phản biện. KHÔNG dùng blog, trang tạp chí decor, Pinterest, Wikipedia, trang thương mại, video, bài "mẹo trang trí" làm căn cứ.

Quy trình cho từng nhận định đưa vào lời đọc:
1. Gắn nó với một nguồn cụ thể: tác giả, tựa, năm, nhà xuất bản/tạp chí, chương hoặc DOI.
2. Xác minh nguồn có thật bằng WebSearch/WebFetch ở nơi đáng tin: trang nhà xuất bản, DOI/Crossref, Google Books, thư viện đại học, PubMed, Semantic Scholar. Mức xác minh phải tương xứng với nhận định: thấy tên mục trong mục lục chỉ xác minh được "nguyên lý này có trong sách"; nhận định về cơ chế, lịch sử, điều kiện áp dụng phải đọc được đúng đoạn nói điều đó (abstract, đoạn trích, toàn văn). Ghi rõ mức đã đọc trong `sources.md`.
   Kinh nghiệm truy cập (lần chạy 2026-10-06): WebFetch trong lần chạy tự động chỉ mở được URL đã xuất hiện trong kết quả WebSearch (URL tự gõ bị chặn vì không có ai duyệt), nên luôn WebSearch trước rồi mới mở đúng URL trong kết quả. PubMed và PMC trả trang kiểm tra bot (reCAPTCHA): không cố vượt, dùng trang khác có trong kết quả tìm kiếm như trang bản ghi của trường đại học (ví dụ experts.<trường>.edu), trang nhà xuất bản, tạp chí truy cập mở (Frontiers, PLOS, i-Perception, Journal of Vision), Internet Archive hoặc Google Books. Trang Wiley sản phẩm trả 403. Trang O'Reilly cho đọc mục lục, không cho đọc chương. Mỗi lần tìm, chạy nhiều WebSearch song song để có sẵn URL dự phòng.
3. Không xác minh được: BỎ nhận định đó khỏi lời đọc. Tuyệt đối không dựa vào trí nhớ để bịa số trang, trích dẫn hay tên sách. Chỉ ghi số trang khi đã nhìn thấy tận nơi.
4. Phân biệt rõ bản chất:
   - Nguyên lý thiết kế hoặc lý thuyết: Gestalt, cân bằng, nhịp điệu, tỷ lệ, trọng tâm, tương phản…
   - Phát hiện thực nghiệm: nghiên cứu tri giác, tâm lý màu…
   - Quy tắc kinh nghiệm: ví dụ 60-30-10. Phải nói đây là "quy tắc kinh nghiệm của giới thực hành", không nói là "khoa học chứng minh".
5. Không nói quá: tránh "luôn luôn", "đã được chứng minh" khi nguồn chỉ nói "có xu hướng". Giữ đúng mức độ chắc chắn của nguồn.
6. Mỗi tập cần ít nhất 3 nguồn độc lập: ít nhất 1 sách giáo trình hoặc chuyên khảo (nguyên lý, cách áp dụng trong thiết kế), ít nhất 1 nghiên cứu có phản biện đọc được nội dung (cơ chế tri giác), và nguồn cho phần nguồn gốc lý thuyết (ai đề xuất, năm, bối cảnh; có thể là một trong hai nguồn trên nếu nguồn đó nêu rõ).
7. Phần "cách áp dụng" và "chọn mua/chọn đồ": mỗi lời khuyên phải hoặc có nguồn giáo trình nói điều đó, hoặc là SUY LUẬN TRỰC TIẾP từ nguyên lý đã có nguồn; với loại sau ghi rõ trong `sources.md` là "suy luận áp dụng từ nguyên lý X" và diễn đạt trong lời đọc bằng "nên", "thử", không nói như sự thật khoa học. Không bịa số đo, ngưỡng, tỷ lệ; chỉ nêu con số khi nguồn nêu con số đó (hoặc khi đo được trên chính ảnh và nói rõ là "trong ảnh này"). Không nhắc thương hiệu, cửa hàng hay sản phẩm cụ thể.

Danh sách nguồn gợi ý để tìm trước (vẫn phải xác minh từng lần, không coi là đã đúng):
- Ching, F. D. K. & Binggeli, C. *Interior Design Illustrated* (Wiley).
- Ching, F. D. K. *Architecture: Form, Space, and Order* (Wiley).
- Pile, J. & Gura, J. *A History of Interior Design* (Wiley); Pile, J. *Interior Design* (Pearson).
- Lidwell, W., Holden, K. & Butler, J. *Universal Principles of Design* (Rockport).
- Arnheim, R. *Art and Visual Perception*; *The Dynamics of Architectural Form* (UC Press).
- Albers, J. *Interaction of Color* (Yale UP); Itten, J. *The Art of Color*.
- Alexander, C. et al. *A Pattern Language* (Oxford UP).
- Rasmussen, S. E. *Experiencing Architecture* (MIT Press); Pallasmaa, J. *The Eyes of the Skin* (Wiley); Zumthor, P. *Atmospheres* (Birkhäuser).
- Nghiên cứu: Palmer & Schloss (2010, PNAS) về sở thích màu; Elliot & Maier (2014, Annual Review of Psychology) về màu và tâm lý; Kaplan & Kaplan về môi trường và ưa thích thị giác; các bài tri giác Gestalt có phản biện (ví dụ Wagemans et al. 2012, Psychological Bulletin).
Nếu cần nguồn ngoài danh sách, chỉ nhận sách hoặc bài có phản biện, và phải xác minh như trên.

## 4. Quy trình
1. Chế độ tự động: chọn nguyên lý và tìm ảnh theo mục 2b (nguyên lý trước, ảnh sau). Chế độ override: xem kỹ ảnh người dùng gửi và xác định MỘT nguyên lý thấy rõ trong ảnh.
2. Tra và xác minh nguồn cho nguyên lý (mục 3) TRƯỚC khi viết kịch bản. Chọn nhận định có nguồn rồi mới viết. Nếu không đủ nguồn vững thì đổi nguyên lý (và có thể đổi ảnh).
3. Trước khi viết lời, soạn `OUT/research.md`: ghi chép nghiên cứu theo đúng bảy phần ở mục 4a, mỗi ý kèm nguồn và đoạn đã đọc (tóm tắt ngắn hoặc trích ngắn). Kịch bản chỉ được dùng ý có trong `research.md`.
4. Viết kịch bản 10–13 cảnh, tổng 45–60 giây, khoảng 110–160 từ lời đọc, theo mục 4a. Câu ngắn, dễ đọc, tự nhiên, tiếng Việt chuẩn. Lời đọc dùng để dán vào ElevenLabs nên không có ký hiệu lạ, không chú thích trong ngoặc. Mỗi cảnh tối đa khoảng 22 từ (hiển thị tối đa 3 dòng trên khung).
5. Nhờ một agent khác chưa thấy quá trình làm đọc `research.md`, `script.md`, `sources.md` và chấm theo mục 4b (chiều sâu và nguồn). Sửa theo góp ý TRƯỚC khi dựng hình.
6. Đặt toạ độ doodle bằng cách tự xem ảnh (đọc ảnh bằng Read): trục, đường, hình bao đồ vật bằng đa giác thô theo toạ độ ảnh làm việc.
7. Chạy engine khung hình (mục 5). Xem LẠI từng khung (mục 7). Sửa toạ độ rồi chạy lại cho đến khi đạt.
8. Soạn `elevenlabs.txt` (mục 8b) từ lời đọc đã chốt.
9. Dựng video bằng engine video (mục 5b). Xem lại các khung trích từ video (mục 7).
10. Hoàn thiện `sources.md` (bản đầu viết cùng kịch bản ở bước 4, để agent ở bước 5 đối chiếu được), viết `caption.txt`, rồi báo cáo (mục 8).
11. Chỉ khi có file audio trong INBOX/audio: ghép tiếng vào video (mục 5c) và kiểm tra thời lượng.

## 4a. Cấu trúc kịch bản có chiều sâu (45–60 giây)
Thứ tự gợi ý; được đảo thứ tự nếu kể tự nhiên hơn, nhưng phải đủ bảy phần nội dung (B–H). Thời lượng ghi là gợi ý.
- A. Mở (1 cảnh, 3–4s): một quan sát CỤ THỂ trên ảnh dẫn vào câu hỏi (ví dụ "Hai mươi khung ảnh trên một bức tường, sao không rối?"). Không mở bằng câu chung như "Bạn có biết…".
- B. Nguồn gốc lý thuyết (1 cảnh, 4–5s): ai đề xuất, năm nào, trong bối cảnh nào, theo đúng nguồn (ví dụ trường phái Gestalt Berlin, bài của Wertheimer). Chỉ nêu tên, năm khi đã đọc thấy trong nguồn.
- C. Cơ chế, vì sao mắt thấy vậy (1–2 cảnh, 6–9s): giải thích bằng ngôn ngữ đời thường điều nguồn nghiên cứu nói (mắt/não làm gì, khi nào thì xảy ra, yếu tố nào mạnh hơn yếu tố nào nếu nguồn có nói). Đây là phần tạo chiều sâu chính, không được thay bằng câu định nghĩa.
- D. Đọc trên ảnh (2–3 cảnh, 10–14s): mỗi cảnh một chi tiết, zoom vào đúng vật, gọi tên vật và chỉ ra nguyên lý đang hoạt động thế nào ở đó (khoảng cách, đường, màu, kích thước cụ thể nhìn thấy được).
- E. Lỗi hay gặp hoặc phản ví dụ (1 cảnh, 4–6s): nếu làm sai thì trông thế nào. Không dựng ảnh khác; dùng chính ảnh với nét gợi ý (ví dụ mũi tên "nếu dời khung này ra xa…") hoặc chỉ vào chỗ trong ảnh mà nguyên lý bị phá có chủ ý.
- F. Cách áp dụng cụ thể (1 cảnh, 4–6s): một hai việc người xem làm được ngay trong nhà mình, đủ cụ thể để làm theo (theo mục 3.7).
- G. Chọn mua, chọn đồ và thiết kế (1 cảnh, 4–6s): nguyên lý này đổi cách chọn đồ thế nào (chọn món theo bộ hay lẻ, chọn khung, màu, kích thước, chất liệu, chọn số lượng…), theo mục 3.7.
- H. Công thức (1 cảnh, 3–4s): một câu tóm tắt dễ nhớ, có thông tin (không phải khẩu hiệu rỗng).
- I. Cảnh cuối (1 cảnh, 5–6s): nhắc AH Decode là series phân tích nguyên tắc thiết kế và chọn đồ decor, mời theo dõi Fanpage Giả Thuyết Kiến Trúc và nhắc các bài viết về kiến trúc dành riêng cho thành viên, link ở phần bình luận. KHÔNG nhắc tập sau, không đọc nguồn hay credit. Lời đọc mẫu: "AH Decode là series phân tích nguyên tắc thiết kế và cách chọn đồ decor. Theo dõi Fanpage Giả Thuyết Kiến Trúc để xem thêm. Các bài viết về kiến trúc dành riêng cho thành viên, link ở phần bình luận."
Quy tắc chiều sâu:
- Mỗi cảnh phải chứa ít nhất một thông tin cụ thể (tên người/khái niệm, cơ chế, điều kiện, vật cụ thể trong ảnh, việc làm cụ thể). Câu nào bỏ đi mà người xem không mất thông tin gì thì bỏ.
- Cấm các cụm chung chung không kèm giải thích: "tạo cảm giác hài hoà", "trông đẹp hơn", "thu hút ánh nhìn", "tạo điểm nhấn", "cân bằng thị giác" khi chưa nói vì sao và bằng cách nào.
- Không lặp lại cùng một ý bằng chữ khác để kéo dài thời lượng.

## 4b. Tự chấm trước khi dựng hình
Agent đọc lại (bước 5) trả lời có/không cho từng câu, kèm lý do:
1. Có đủ bảy phần B–H, mỗi phần có ít nhất một ý cụ thể?
2. Phần cơ chế có nói được vì sao (không chỉ nhắc lại định nghĩa)? Có nguồn đọc được nội dung tương ứng?
3. Người xem có học được ít nhất ba điều cụ thể họ có thể chưa biết? Liệt kê ba điều đó.
4. Có câu chung chung, lặp ý hoặc nói quá nguồn nào không? Liệt kê.
5. Lời khuyên áp dụng và chọn đồ có làm theo được ngay không, và có đúng mục 3.7 không?
6. Mọi nhận định đều có dòng tương ứng trong `sources.md`?
Có câu trả lời "không" thì sửa kịch bản hoặc tìm thêm nguồn, rồi mới dựng hình.

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
- Từng nhận định trong lời đọc đều có dòng tương ứng trong `sources.md` đã xác minh ở mức tương xứng (mục 3.2); không có nhận định mồ côi.
- Video: trích ít nhất 12 khung (đầu, giữa quá trình vẽ, cuối từng cảnh chính, khung cuối) để kiểm tra: nét vẽ đã đủ khi cảnh kết thúc, không có nét của cảnh cũ lẫn sang cảnh mới, chữ không bị cắt, chuyển cảnh không giật. Kiểm tra `ffprobe`: 1080×1920, h264, có track âm thanh, thời lượng đúng dự kiến.
- Không có logo, thương hiệu hay tên người xuất hiện sai trong khung.
Kịch bản và nguồn đã được agent độc lập chấm ở bước 5 mục 4; nếu sau đó kịch bản còn đổi, nhờ đọc lại lần nữa.

## 8. Đầu ra (OUT = INBOX/out/<YYYY-MM-DD>_<slug>/)
- `research.md`: ghi chép nghiên cứu theo bảy phần mục 4a (bước 3 mục 4).
- `script.md`: bảng cảnh (thời lượng, phần nội dung A–I, tiêu đề, lời đọc, hình) + phần lời đọc liền mạch + kết quả tự chấm mục 4b.
- `elevenlabs.txt`: văn bản thuần để người dùng dán thẳng vào ElevenLabs (mục 8b).
- `source_info.md`, `original/`.
- `frames/scene_*.png` + `storyboard.png` + `frames.zip`.
- `reel_<slug>_silent.mp4` (và `reel_<slug>_final.mp4` nếu đã có audio).
- `sources.md`: mỗi nhận định → nguồn (tác giả, tựa, năm, NXB/tạp chí, chương/DOI, link nơi đã xác minh) → mức chắc chắn (nguyên lý / thực nghiệm / quy tắc kinh nghiệm) → đã xác minh bằng gì.
- `caption.txt`: caption đăng bài có chiều sâu, bổ sung cho reel (không chép lại lời đọc): vài đoạn ngắn về nguồn gốc, cơ chế, cách áp dụng và gợi ý chọn đồ, cùng quy tắc nguồn như lời đọc; rồi dòng giới thiệu và mời "AH Decode là series mới của Giả Thuyết Kiến Trúc, phân tích các nguyên tắc thiết kế và cách chọn đồ decor. Theo dõi Fanpage Giả Thuyết Kiến Trúc. Các bài viết về kiến trúc dành riêng cho thành viên: link ở phần bình luận."; rồi 2–3 nguồn chính (sách/nghiên cứu), credit ảnh đầy đủ và link bài gốc của tạp chí; hashtag vừa phải. Không tự điền link thành viên (người dùng tự dán vào bình luận).
- Gửi cho người dùng (SendUserFile): `elevenlabs.txt` đầu tiên, rồi video, ảnh bảng phân cảnh, `script.md`, `sources.md`, `caption.txt`; kèm tóm tắt tối đa 6 dòng: nguyên lý, ba điều người xem học được, nguồn chính, điểm cần duyệt, credit đã có hay còn thiếu, và nhắc "gửi lại file giọng đọc vào INBOX/audio để ghép tiếng".
Đây là BẢN NHÁP chờ người dùng duyệt. Không đăng, không gửi đi đâu khác.

## 8b. Quy cách `elevenlabs.txt`
Mục tiêu: người dùng mở file, chọn tất cả, dán vào ElevenLabs, không phải sửa gì.
- Chỉ có lời đọc, theo đúng thứ tự cảnh. Không đánh số cảnh, không tiêu đề, không chú thích, không ngoặc chỉ dẫn, không emoji, không hashtag, không tên file.
- Mỗi cảnh một đoạn; giữa các đoạn cách một dòng trống. Trong đoạn, mỗi câu một dòng.
- Đọc được thành tiếng một cách tự nhiên: viết số, ký hiệu và từ viết tắt thành chữ (ví dụ "60-30-10" thành "sáu mươi, ba mươi, mười"; "≠" thành "không bằng"; "%" thành "phần trăm"). Tên riêng nước ngoài giữ nguyên chính tả, nếu khó đọc thì thêm cách đọc phiên âm tiếng Việt.
- Dấu câu để điều khiển nhịp: dấu phẩy và chấm đủ rõ; chỗ cần ngắt dài hơn thì dùng dấu "..." hoặc dòng trống, không chèn thẻ kỹ thuật. Câu ngắn, tối đa khoảng 18 từ.
- Độ dài khớp thời lượng cảnh trong `SCENES`: khoảng 2,5–3 từ mỗi giây, trừ khoảng 0,7 giây chuyển cảnh ở đầu mỗi cảnh. Cuối file ghi thêm một dòng riêng NGOÀI phần dán: `--- Gợi ý cài đặt: giọng nữ hoặc nam trầm ấm, tốc độ 1.0, mô hình đa ngôn ngữ, ngôn ngữ Vietnamese ---` để người dùng tham khảo (dòng này phân tách bằng một dòng trống và dấu `---`, người dùng chỉ dán phần phía trên).
- Cảnh cuối chỉ đọc câu giới thiệu series AH Decode, lời mời theo dõi Fanpage Giả Thuyết Kiến Trúc và nhắc bài viết về kiến trúc dành riêng cho thành viên, link ở phần bình luận (mẫu ở mục 4a, phần I). Không gợi ý tập sau, không đọc nguồn hay credit. Giữ chữ "AH Decode" như tên riêng; dòng gợi ý cài đặt cuối file thêm câu: "nếu ElevenLabs đọc sai tên AH Decode, thay bằng cách viết theo âm bạn muốn".

## 9. Khi gặp sự cố
- Không truy cập được trang nguồn nào hoặc không tìm được ảnh đạt tiêu chí sau khi xem ít nhất 10 ứng viên: dừng, báo rõ lý do và các ảnh/bài đã thử; KHÔNG chuyển sang nguồn ảnh khác, KHÔNG lấy ảnh từ Google/Pinterest.
- Ảnh quá nhỏ (<1200 px cạnh dài), quá tối, hoặc không minh hoạ được nguyên lý nào có nguồn: vẫn làm bản tốt nhất có thể, ghi rõ hạn chế (ví dụ zoom bị mềm) và đề nghị ảnh khác.
- Không đọc được nội dung nguồn cho phần cơ chế (chỉ thấy mục lục/tên): đổi sang nguyên lý khác có nguồn đọc được; thử tối đa 3 nguyên lý. Vẫn không được thì làm bản tốt nhất với nguyên lý có nguồn mạnh nhất, ghi rõ nhận định nào chưa xác minh và để người dùng quyết định. KHÔNG giao kịch bản như thể đã đủ nguồn.
- Dựng video quá thời gian hoặc ffmpeg lỗi: vẫn giao khung hình, script và `elevenlabs.txt`, nói rõ video chưa dựng được và vì sao.
- Công cụ lỗi (mạng, thư viện): thử lại một lần, rồi báo lỗi cụ thể thay vì bỏ qua bước.

## 10. Việc KHÔNG làm
- Không dùng nguồn web thường thức. Không dựa trí nhớ để dẫn sách/nghiên cứu.
- Không đổi quy cách hình ảnh ở mục 6. Không sketch hoá ảnh dự án. Không bỏ credit.
- Không dùng ảnh/đồ hoạ ngoài ảnh đã chọn từ bốn trang nguồn ở mục 2b (hoặc ảnh người dùng gửi ở chế độ override). Không dùng Est Living, The Local Project hay bất kỳ nguồn ảnh nào khác.
- Không đổi nhịp chuyển cảnh/vẽ nét đã duyệt (mục 5b), không thêm nhạc nền, hiệu ứng hay phụ đề chạy chữ khi chưa được yêu cầu.
- Không bịa tên studio, nhiếp ảnh gia hay dự án khi thiếu credit; chỉ ghi những gì có trên trang bài nguồn.
- Không hẹn hay gợi ý "tập sau" ở bất kỳ đâu (khung, lời đọc, caption).
- Không dừng giữa chừng để chờ duyệt lý thuyết hay ảnh.