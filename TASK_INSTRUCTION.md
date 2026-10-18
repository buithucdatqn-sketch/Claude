# INSTRUCTION — Scheduled task "AH Decode · Reel hằng ngày"

Kho mã và dữ liệu: GitHub `buithucdatqn-sketch/claude` (nhánh `main`). Cách lấy: dùng add_repo (quyền push) rồi `git clone --depth 1 https://github.com/buithucdatqn-sketch/claude /home/claude/claude` (timeout lệnh ≥ 10 phút; chỉ MỘT lệnh git tại một thời điểm), sau đó gọi register_repo_root. Gọi thư mục clone là REPO. Cấu trúc: `REPO/engine/` (bộ engine), `REPO/inbox/` (INBOX), `REPO/TASK_INSTRUCTION.md` (bản sao của chính tài liệu này). Thông tin nội dung của mỗi tập lấy từ KHO BÀI (mục 2a), một kho GitHub khác. Cuối mỗi lần chạy: chép `engine_epNN.py` và `engine_video_epNN.py` vào `OUT/engine_epNN/`, `git add inbox`, commit, và `git pull --rebase origin main && git push origin main` (một lần; nếu bị 429 thì đợi 10 giây thử lại một lần).

Mỗi lần chạy là một phiên mới, không nhớ gì từ các cuộc trò chuyện trước. Mọi thông tin cần thiết nằm trong tài liệu này, thư mục INBOX và KHO BÀI.
Chạy một lượt, không hỏi lại. Nếu thiếu đầu vào thì dừng và báo rõ thiếu gì (mục 9).

## 1. Nhiệm vụ
Mỗi ngày, lấy MỘT Ý CHƯA DÙNG của một bài trong KHO BÀI (mục 2a; một bài có thể cho nhiều tập, mỗi tập một ý khác nhau) và dùng NỘI DUNG CỦA BÀI làm toàn bộ thông tin của reel (nguyên tắc, nguồn gốc, cơ chế, cách áp dụng, cách chọn đồ, nguồn tham khảo). Task KHÔNG tự nghiên cứu và KHÔNG tự viết thêm thông tin ngoài bài (mục 3). Ảnh lấy trước hết trong thư mục `anh/` của chính bài đó, và được lấy thêm ẢNH (không lấy thông tin) của CHÍNH công trình mà bài phân tích từ trang nguồn ảnh của công trình (mục 2b, ví dụ Yatzer). Mỗi reel phải có nhiều ảnh của công trình, có ít nhất một ảnh diagram (sketch) của bài, và mặt bằng nếu bài có (mục 2d). Thông tin nội dung vẫn chỉ lấy từ bài (mục 3). Từ đó tạo gói sản xuất cho một reel dọc 9:16, dài 55–75 giây, series "AH Decode". Reel giải thích MỘT nguyên tắc nội thất/decor bằng các nét doodle trắng nét đứt vẽ lên chính ảnh gốc.
Mỗi reel là một bài học TRỌN VẸN và CÓ CHIỀU SÂU (mục 4a) về nội thất và decor, chắt lọc từ bài trong kho: nguồn gốc nguyên tắc, cơ chế vì sao mắt thấy vậy, đọc nguyên lý trên ảnh, lỗi hay gặp, cách áp dụng cụ thể, cách chọn mua/chọn đồ và thiết kế, rồi công thức tổng kết. Người xem phải học được điều cụ thể mà họ chưa biết, không phải những câu chung chung. Không hẹn "tập sau"; cảnh cuối chỉ nhắc series AH Decode và nói bài viết phân tích đầy đủ xem ở dòng đầu tiên trong phần bình luận (KHÔNG có cụm "theo dõi Fanpage" và tên Fanpage, vì khung cuối quá nhiều chữ). Lời đọc phải là một mạch kể dễ hiểu (mục 4a), không phải chuỗi thông tin rời.

**Tên gọi (dùng đúng, không lẫn):** Fanpage tên là **Giả Thuyết Kiến Trúc**. **AH Decode** là một series MỚI của Fanpage này, chuyên phân tích các nguyên tắc thiết kế và cách chọn đồ decor. AH Decode KHÔNG phải tên Fanpage: không viết "Fanpage AH Decode". Header trên khung vẫn là `AH DECODE · <CHỦ ĐỀ>`.
Chạy trọn một lượt, không chờ duyệt lý thuyết hay ảnh giữa chừng.

## 1a. TRỌNG TÂM SERIES: NỘI THẤT VÀ DECOR, KHÔNG PHẢI KIẾN TRÚC (bắt buộc)
AH Decode dạy người xem cách làm đẹp và chọn đồ cho không gian bên trong: những thứ họ tự quyết được trong nhà mình mà không cần xây, đập hay sửa kết cấu. Các bài trong KHO BÀI đã được biên soạn cho series này; mục 1a dùng để chọn chi tiết khoanh trên ảnh, để chọn MỘT ý chính khi bài dài, và để nhận ra bài lệch trọng tâm (khi đó bỏ qua bài đó theo mục 2a).
- ĐÚNG trọng tâm: phối màu (bánh xe màu, tương cận, bổ túc, tam giác màu, sắc độ, độ bão hoà, màu nền và màu nhấn, nhiệt độ màu, màu ảnh hưởng nhau và theo ánh sáng); chọn kiểu dáng đồ nội thất (dáng cong hay góc cạnh, chân cao hay sát sàn, trọng lượng thị giác, tỷ lệ món đồ so với phòng và so với nhau, công thái học, kích thước chuẩn của bàn ghế); chọn vật liệu và bề mặt (gỗ, đá, vải, kim loại, độ bóng mờ, vân, tương phản chất cảm); bố cục và sắp xếp đồ (nhóm trò chuyện, lối đi, điểm nhấn, cân bằng, nhịp lặp, khoảng thở); hoạ tiết và vải (pha hoạ tiết theo tỷ lệ, rèm, thảm, gối); đèn và ánh sáng decor (đèn nhiều lớp, nhiệt độ màu bóng đèn, đèn làm điểm nhấn); styling (treo tranh, bày đồ trên kệ, nhóm vật trang trí, cây); các nhà thiết kế nội thất, nhà trang trí, nhà thiết kế đồ nội thất và tạo dáng công nghiệp (ví dụ Charles và Ray Eames, Hans Wegner, Florence Knoll, Dieter Rams, Dorothy Draper, Elsie de Wolfe, Andrée Putman) cùng triết lý, cách làm của họ; các nguyên lý thị giác (Gestalt, tương phản, thứ bậc…) KHI áp vào đồ đạc, màu, vật liệu, bố cục đồ.
- SAI trọng tâm, KHÔNG làm: lý thuyết kiến trúc và không gian công trình (prospect–refuge, trục và trình tự không gian, ngưỡng và chuyển tiếp, hình khối, mặt bằng, kết cấu, độ cao trần, vách kính, cửa sổ, quan hệ nhà với cảnh quan); phân tích tác phẩm hay lý thuyết của kiến trúc sư (Wright, Le Corbusier, Kahn, Zumthor…) với tư cách kiến trúc sư. Kiến trúc sư chỉ được nhắc khi bàn đến món đồ nội thất họ thiết kế (ví dụ ghế Barcelona của Mies van der Rohe và Lilly Reich) và chỉ ở tư cách người thiết kế đồ.
- Phép thử với bài và ý chính được chọn: người xem có áp dụng được điều này bằng cách mua, đổi, sơn, dời hoặc bày lại đồ trong một căn phòng có sẵn không? Nếu chỉ áp dụng được khi xây hoặc sửa công trình thì loại.
- Trên ảnh, nét doodle khoanh và chỉ vào ĐỒ VẬT, MÀU, VẬT LIỆU, HOẠ TIẾT, ĐÈN, cách bày đồ; không lấy trần, cột, vách, cửa sổ, kết cấu làm đối tượng phân tích chính.
Gói gồm: (1) kịch bản lời đọc theo cảnh và file chữ thuần để dán vào ElevenLabs, (2) các khung hình 1080×1920, (3) bảng phân cảnh, (4) video reel: KHÔNG dựng trong lần làm tập mới; chỉ dựng sau khi người dùng gửi file ghi âm (mục 5c), (5) bảng đối chiếu từng nhận định với bài trong kho, (6) caption đăng bài.
Người dùng nói tiếng Việt, mọi chữ trên khung và lời đọc đều bằng tiếng Việt.

## 2. Đầu vào (INBOX = REPO/inbox)
Chế độ mặc định là TỰ ĐỘNG: không cần người dùng gửi ảnh. Chỉ cần:
- KHO BÀI (mục 2a): nguồn thông tin duy nhất cho nội dung reel.
- `INBOX/series.json`: danh sách các tập đã làm (số tập, bài trong kho đã dùng `bai_kho` = đường dẫn file + commit SHA của nhánh lúc đọc, ý đã dùng `y_bai` = tiêu đề mục trong bài + tóm tắt một dòng, nguyên lý, đường dẫn ảnh đã dùng trong kho, ngày, `trang_thai`). Nếu chưa có thì tạo mới. Dùng để không lặp lại Ý đã làm (một bài được dùng nhiều lần, mỗi lần một ý khác) và không lặp lại ảnh.
- `INBOX/override/`: KHÔNG còn dùng (không nhận ảnh hay nguồn ngoài kho). Nếu thư mục có file thì bỏ qua và nhắc trong báo cáo.
- `INBOX/audio/<slug>.mp3|wav|m4a` (tuỳ chọn): giọng đọc ElevenLabs của một tập đang ở trạng thái `cho_ghi_am` (người dùng làm từ `elevenlabs.txt` của tập đó). ĐẦU MỖI LẦN CHẠY phải kiểm tra thư mục này trước: có file khớp `slug` của tập `cho_ghi_am` thì làm giai đoạn 2 (mục 5c: dựng video theo nhịp giọng đọc rồi ghép tiếng) cho tập đó, đổi `trang_thai` thành `da_dung_video`. Làm xong giai đoạn 2 thì vẫn làm tiếp một tập mới (giai đoạn 1) như thường.
- Xử lý xong: cập nhật `series.json`.

## 2a. KHO BÀI: nguồn thông tin của reel (bắt buộc)
- Vị trí: GitHub `buithucdatqn-sketch/A---material`, nhánh `AH-Interior-notes`, thư mục `AH-Decode-Decor/` (https://github.com/buithucdatqn-sketch/A---material/tree/AH-Interior-notes/AH-Decode-Decor/).
- Cách lấy: dùng add_repo cho `buithucdatqn-sketch/A---material` (chỉ cần quyền đọc), rồi `git clone --depth 1 -b AH-Interior-notes https://github.com/buithucdatqn-sketch/A---material /home/claude/material` (timeout ≥ 10 phút; chỉ MỘT lệnh git tại một thời điểm). Nếu thư mục đã có thì `git -C /home/claude/material pull origin AH-Interior-notes`. Nếu clone không được nhưng công cụ GitHub MCP đọc được kho thì đọc bằng `get_file_contents` (ref `refs/heads/AH-Interior-notes`). Gọi thư mục bài là KHO = `/home/claude/material/AH-Decode-Decor/`. KHÔNG sửa, commit hay push gì vào kho bài.
- Đọc cấu trúc thư mục trước: nếu có README, mục lục, file hướng dẫn hay quy ước đặt tên (ví dụ số thứ tự, trạng thái "đã duyệt"/"nháp") thì làm theo. Mỗi bài thường là một file (`.md`, `.txt`, hoặc tài liệu khác) hoặc một thư mục con; file không phải bài (README, mẫu, ảnh, ghi chú chung) thì không tính là bài.
- Ý trong bài: mỗi ý là một bài học/mục nội dung riêng của bài (thường là một mục tiêu đề `##` hoặc một "bài học" bài tự đánh số), đủ để kể thành một mạch có cơ chế và cách áp dụng (mục 4a). Phần mở bài, lý thuyết chung hay kết bài không tính là ý riêng, nhưng được dùng làm nguồn gốc/cơ chế cho bất kỳ ý nào. Lần đầu đọc một bài, liệt kê các ý của bài vào `research.md`.
- Chọn ý: theo thứ tự bài (mục lục nếu có, không thì số thứ tự hoặc tên file tăng dần), lấy bài đầu tiên còn ý CHƯA có trong `series.json` (so theo `bai_kho.duong_dan` + `y_bai`), rồi lấy ý chưa dùng đầu tiên của bài đó theo thứ tự trong bài. Một ý chỉ được làm MỘT lần; bài thì được dùng lại cho đến khi hết ý. Bỏ qua bài ghi rõ là nháp/chưa xong. Nếu ý (hoặc cả bài) lệch trọng tâm mục 1a (lý thuyết kiến trúc) thì bỏ qua, ghi vào `series.json` với `trang_thai: "bo_qua_lech_trong_tam"` kèm lý do, rồi lấy ý kế tiếp.
- Đọc TOÀN BỘ bài (Read hết, không bỏ đoạn nào), kể cả phần nguồn tham khảo, ghi chú ảnh, gợi ý dự án nếu có. Reel chỉ làm MỘT ý đã chọn; các ý khác của bài chỉ được nhắc ngắn trong caption khi cần làm rõ, không hẹn "tập sau". Chỉ đánh dấu ý đó là đã dùng (`y_bai`), không đánh dấu cả bài.
- Nếu bài có ảnh minh hoạ công trình trong `anh/` thì dùng theo mục 2b. Link trỏ ra ngoài kho chỉ được mở để lấy thêm ẢNH của chính công trình đó theo mục 2b; không lấy chữ hay thông tin từ đó.

## 2b. Ảnh: thư mục `anh/` của bài, cộng ảnh của chính công trình từ trang nguồn ảnh (bắt buộc)
Nguồn ảnh, theo thứ tự:
- Thứ nhất: ảnh trong `anh/` của bài đang làm (đường dẫn như trong YAML `anh_theo_thu_tu`): ảnh doodle, diagram, mặt bằng, ảnh công trình.
- Thứ hai (được phép, nên dùng khi `anh/` thiếu không gian): ảnh của CHÍNH công trình mà bài phân tích (YAML `cong_trinh`), lấy từ trang nguồn ảnh mà bài ghi trong YAML `nguon_anh_cong_trinh` (ví dụ bài 02: Yatzer cho ảnh, ArchDaily cho mặt bằng). Chỉ lấy ảnh, KHÔNG lấy chữ, số liệu hay nhận định từ trang đó (mục 3). Chỉ ảnh của đúng công trình ấy, đúng bộ ảnh đã đăng cùng bài trên trang; không lấy ảnh công trình khác, không lấy ảnh từ trang không do bài ghi. Credit theo trang: `<công trình> · <studio> · ảnh <nhiếp ảnh gia>`; lưu ảnh gốc vào `OUT/original/` và ghi URL trang, URL ảnh vào `source_info.md`. Ảnh ngoài bài là ảnh sạch (không doodle): dùng như loại (b).
- Nếu mạng của môi trường chặn trang nguồn (curl, WebFetch bị từ chối), ghi rõ trong báo cáo và làm với ảnh trong `anh/`; không lấy ảnh từ trang khác để thay.
- Không dùng ảnh người dùng gửi ngoài kho, không tìm ảnh bằng công cụ tìm kiếm.
1. Xem (Read) toàn bộ ảnh trong `anh/` của bài. Phân loại: ảnh công trình/nội thất thật; sơ đồ (diagram); mặt bằng, trục đo; ảnh đã có nét doodle; ảnh bìa dựng sẵn.
2. Chọn MỘT ảnh CHÍNH minh hoạ rõ nhất ý chính của bài, rồi chọn thêm các ảnh khác theo mục 2d (bắt buộc: diagram, mặt bằng nếu có, ít nhất ba không gian): cảnh nào lời đọc nói về một chỗ khác thì dùng ảnh chỗ đó (ví dụ cảnh nói về khu bếp thì dùng ảnh bếp), cùng quy tắc ưu tiên (a)–(c) và cùng quy cách mục 6; ghi rõ cảnh nào dùng ảnh nào trong `source_info.md` và `series.json` (`anh_kho` liệt kê đủ). Cách dựng: xem mục 5d. KHÔNG cần ưu tiên khung ngang: ảnh ngang, dọc hay vuông đều dùng được (engine phải chỉnh bố cục khung, vùng đặt ảnh và camera cho đúng tỷ lệ ảnh được chọn, vẫn giữ nguyên quy cách mục 6). Thứ tự ưu tiên:
   (a) Ảnh trong bài ĐÃ CÓ nét doodle (tên có `doodle`, hoặc ảnh có nét trắng nét đứt/nhãn chữ vẽ sẵn): ưu tiên dùng, vì đó là phân tích có sẵn của bài. Không vẽ nét mới đè lên; thay vào đó làm cho chính doodle đó CHUYỂN ĐỘNG theo nguyên tắc dựng video ở mục 5b (xem mục 2c).
   (b) Ảnh nội thất thật, sạch, không có doodle: dùng engine như thường lệ (đặt toạ độ và vẽ nét mới theo mục 5).
   (c) Diagram (sketch) và mặt bằng của bài DÙNG ĐƯỢC làm ảnh nền cho cảnh nguồn gốc, cơ chế, giới thiệu công trình (mục 2d). Cắt vùng có chú thích (bỏ tiêu đề lớn, lề trắng) để chữ trên diagram đủ to, đặt thẻ ảnh trong dải y 610–1240 (chữ của khung là chữ nâu trên nền trắng, không viết đè lên diagram). Không dùng ảnh bìa dựng sẵn làm nền.
   Ý chính của reel nên chọn sao cho khớp với ảnh doodle có sẵn của bài.
3. Chọn ảnh khớp với ý đang làm. Ảnh CHÍNH (ảnh có nét doodle được lộ dần cho ý của tập) không trùng ảnh chính hay ảnh có nét lộ dần của tập trước (so theo `series.json`). Ảnh phụ (diagram, mặt bằng, ảnh không gian dùng nền sạch) được dùng lại ở tập khác vì bài thường ít ảnh, nhưng ưu tiên ảnh chưa dùng; nêu rõ trong báo cáo ảnh nào dùng lại.
4. Tạo bản làm việc: thu nhỏ cạnh dài còn tối đa 2400 px (LANCZOS, giữ tỷ lệ; không phóng to) lưu thành `source.png`; mọi toạ độ doodle đặt theo bản này. Chép ảnh gốc vào `OUT/original/`. Ảnh nhỏ hơn 1200 px cạnh dài: vẫn làm, ghi hạn chế.
5. Credit: lấy từ YAML và chú thích trong bài (`cong_trinh`, `nguon_anh_cong_trinh`, tên tác giả ảnh nếu bài ghi). Định dạng: `<công trình> · <studio> · ảnh <nhiếp ảnh gia>`; thiếu mục nào bỏ mục đó, không bịa. Dòng trên khung: `Ảnh dự án: ...` (dài quá 960 px thì giảm cỡ chữ, tối thiểu 26, hoặc xuống hai dòng, không cắt). Ảnh do chủ bài dựng (bìa, doodle, diagram) ghi thêm "Giả Thuyết Kiến Trúc" nếu bài ghi như vậy.
6. Lưu `OUT/source_info.md`: đường dẫn ảnh trong kho (hoặc URL trang và URL ảnh nếu lấy ngoài bài), commit SHA, credit, lý do chọn ảnh, cảnh nào dùng ảnh nào, hạn chế.

## 2d. Reel nhiều ảnh: mặt bằng, diagram và các không gian khác (bắt buộc)
Người xem cần hình dung được cả công trình, nên các cảnh KHÔNG được xoay quanh một ảnh:
- Ít nhất MỘT ảnh diagram (sketch) của bài, thường ở cảnh nguồn gốc hoặc cơ chế (ví dụ tập 7: diagram 07 "Thô và mịn, cán cân ấm lạnh" ở cảnh Kilmer).
- Mặt bằng công trình nếu bài có (trong `anh/` hoặc từ trang nguồn ảnh), ở cảnh giới thiệu công trình, cắt vùng có chú thích phòng đang nói tới.
- Ảnh của ít nhất BA không gian khác nhau của công trình (ví dụ lối vào, sảnh, phòng khách, phòng ngủ, bếp). Mỗi cảnh nói về chỗ nào thì dùng ảnh chỗ đó.
- Một ảnh không chiếm quá khoảng một nửa số cảnh. Cảnh mở và cảnh chốt nên dùng ảnh rộng, gợi cảm nhất của công trình.
- Ảnh doodle của bài mà nhãn gốc không khớp lời cảnh đó: xoá sạch nét (mục 2c) và dùng như ảnh sạch; chỉ lộ những nhãn khớp lời.
Cách dựng: mục 5d.


## 2c. Làm doodle có sẵn trong ảnh chuyển động (khi chọn ảnh loại (a))
- Dựng hai lớp từ ảnh gốc: (1) lớp nền = ảnh đã xoá nét doodle (inpaint bằng OpenCV `cv2.inpaint` trên mặt nạ nét trắng/nhãn chữ; xem lại bằng Read, sửa mặt nạ đến khi sạch, không để vệt), (2) lớp nét = chính các nét doodle gốc tách theo mặt nạ (giữ nguyên hình dáng, màu trắng, nét đứt, nhãn chữ như bài vẽ). Nếu không xoá sạch được thì dùng kỹ thuật lộ dần (reveal) trực tiếp trên ảnh gốc: phủ ảnh nền chưa có nét rồi lộ nét theo mặt nạ.
- Tách mặt nạ thành các nét/cụm nét riêng (connected components, sắp theo thứ tự đọc tự nhiên hoặc theo thứ tự lời đọc), mỗi cụm là một "nét" để vẽ dần. Nhãn chữ là cụm riêng, hiện sau khi nét liên quan vẽ đạt khoảng 55–75%.
- Chuyển động đúng như mục 5b, không đổi nhịp: camera zoom/di chuyển giữa các cảnh theo `cam`, nét được vẽ dần (nét chạy theo đường, đầu nét lộ ra trước) sau khi camera dừng, xong ở khoảng 62% thời lượng cảnh; chữ và nét cảnh cũ mờ đi 0,25 giây đầu chuyển cảnh; nét thuộc cảnh sau không được hiện trước. Mỗi cảnh chỉ hiện cụm nét liên quan đến lời đọc của cảnh đó, các cụm đã vẽ ở cảnh trước mờ đi khi sang cảnh mới.
- Trong `SCENES`, thay `doodle()` bằng danh sách cụm nét của lớp nét gốc (cụm nào thuộc cảnh nào). Các phần còn lại (băng keo, nền trắng, chữ Patrick Hand, credit, khung cuối) giữ nguyên mục 6.
- Kiểm tra (mục 7): lớp nền không còn vệt nét cũ, lộ nét khớp lời đọc, nét không bị cắt hay lệch so với ảnh gốc.

## 3. QUY TẮC THÔNG TIN: CHỈ LẤY TỪ BÀI TRONG KHO (bắt buộc, không ngoại lệ)
Bài trong KHO BÀI là nguồn thông tin duy nhất cho lời đọc, chữ trên khung và caption. Task không tự nghiên cứu (không WebSearch, không mở trang web để lấy thông tin, kể cả link nguồn mà bài dẫn) và không tự viết thêm kiến thức. Riêng ảnh của chính công trình được lấy thêm từ trang nguồn ảnh theo mục 2b.
1. Mọi nhận định (nguyên lý, nguồn gốc, tên người, năm, cơ chế, số liệu, lời khuyên áp dụng và chọn đồ) phải có trong bài, đúng ý và đúng mức chắc chắn của bài. Ghi vị trí trong bài (tên file + tiêu đề mục hoặc đoạn, kèm trích ngắn) vào `sources.md`.
2. Được phép: rút gọn, diễn đạt lại cho dễ nghe, đổi thứ tự cho tự nhiên, chọn ý, thêm câu nối và từ nối ("vì", "nên", "nghĩa là", "thử nhìn lại ảnh") để các ý thành một mạch, giải thích điều bài nói bằng lời đời thường (những việc này KHÔNG phải thêm kiến thức),  và mô tả điều nhìn thấy trực tiếp trên ảnh (gọi tên món đồ, màu, vật liệu trong ảnh, nói rõ là "trong ảnh này"). Không được: thêm tên, năm, số đo, tỷ lệ, nghiên cứu, ví dụ hay lời khuyên mà bài không có; dựa vào trí nhớ để bổ sung.
3. Giữ nguyên cách bài phân loại và mức chắc chắn: bài gọi là "quy tắc kinh nghiệm" thì nói là quy tắc kinh nghiệm; bài nói "có xu hướng" thì không nói "luôn luôn" hay "đã được chứng minh". Lời khuyên dùng "nên", "thử" như bài.
4. Nguồn tham khảo: nếu bài có danh mục nguồn thì chép đúng như bài ghi vào `sources.md` và chọn 2–3 nguồn chính cho caption; không tự xác minh lại, không thêm nguồn ngoài bài. Bài không có danh mục nguồn thì caption không ghi mục nguồn (không bịa), `sources.md` ghi rõ "bài không kèm nguồn".
5. Nghi bài có lỗi (năm, tên, số liệu mâu thuẫn trong chính bài): không tự sửa theo trí nhớ; bỏ nhận định đó khỏi reel và ghi rõ trong báo cáo để người dùng kiểm tra bài gốc.
6. Không nhắc thương hiệu, cửa hàng hay sản phẩm cụ thể trừ khi bài có và đó là tên đồ nội thất kinh điển (ví dụ ghế của một nhà thiết kế); không có trong bài thì không nhắc.
7. Thông tin không có ngoại lệ: không truy cập web để lấy thông tin dự án. Ngoại lệ duy nhất là ẢNH (và credit của ảnh) của chính công trình từ trang nguồn ảnh mà bài ghi (mục 2b).

## 4. Quy trình
1. Lấy KHO BÀI, chọn bài và đọc toàn bộ bài (mục 2a).
2. Kiểm tra bài và ý chính với phép thử mục 1a (áp dụng được bằng cách mua, đổi, sơn, dời, bày lại đồ). Bài lệch trọng tâm thì bỏ qua theo mục 2a.
3. Trước khi viết lời, soạn `OUT/research.md`: ghi chú bài theo các phần ở mục 4a (A–I), mỗi ý kèm vị trí trong bài (tiêu đề mục/đoạn) và trích ngắn đúng câu chữ của bài. Phần nào bài không có thì ghi "bài không có". Kịch bản chỉ được dùng ý có trong `research.md`. Sau đó tìm ảnh (chế độ tự động, mục 2b) hoặc xem ảnh override, chọn chi tiết trên ảnh khớp với ý của bài.
4. Viết kịch bản 8–13 cảnh, tổng 55–75 giây, khoảng 150–210 từ lời đọc, theo mục 4a (ưu tiên nghe là hiểu: câu hoàn chỉnh, có từ nối, thành một mạch kể). Tiếng Việt chuẩn, tự nhiên như người đang kể chuyện. Lời đọc dùng để dán vào ElevenLabs nên không có ký hiệu lạ, không chú thích trong ngoặc. Mỗi cảnh tối đa khoảng 26 từ (kiểm tra lời đọc không bị cắt hay tràn trên khung).
5. Nhờ một agent khác chưa thấy quá trình làm đọc BÀI GỐC trong kho (đưa đường dẫn file), `research.md`, `script.md`, `sources.md` và chấm theo mục 4b (chiều sâu và trung thành với bài). Sửa theo góp ý TRƯỚC khi dựng hình.
6. Đặt toạ độ doodle bằng cách tự xem ảnh (đọc ảnh bằng Read): trục, đường, hình bao đồ vật bằng đa giác thô theo toạ độ ảnh làm việc.
7. Chạy engine khung hình (mục 5). Xem LẠI từng khung (mục 7). Sửa toạ độ rồi chạy lại cho đến khi đạt.
8. Soạn `elevenlabs.txt` (mục 8b) từ lời đọc đã chốt.
9. KHÔNG dựng video ở giai đoạn này. Vẫn sinh sẵn `engine_video_epNN.py` (mục 5b) để giai đoạn 2 dùng.
10. Hoàn thiện `sources.md` (bản đầu viết cùng kịch bản ở bước 4, để agent ở bước 5 đối chiếu được), viết `caption.txt`, rồi báo cáo (mục 8).
11. Commit, push, gửi file và báo người dùng (mục 8), ghi `trang_thai: "cho_ghi_am"` trong `series.json`, rồi DỪNG. Video chỉ dựng ở lần chạy sau khi đã có file ghi âm trong INBOX/audio (mục 5c).

## 4a. Cấu trúc kịch bản: ưu tiên NGHE LÀ HIỂU (55–75 giây)
**Thứ tự ưu tiên khi các yêu cầu mâu thuẫn: (1) người nghe hiểu được ngay, không cần đọc bài; (2) trung thành với bài (mục 3); (3) đủ các phần dưới đây; (4) ngắn gọn.** Không được cắt chữ đến mức câu thành mảnh rời để cho vừa số từ hay đủ phần; thà bỏ một phần còn hơn viết câu cụt.
Kịch bản là MỘT MẠCH KỂ liền, như một người đang giải thích cho bạn bè nghe: có câu hỏi, có lý do, có ví dụ trong ảnh, có việc làm. Mỗi cảnh là một hoặc hai câu HOÀN CHỈNH (có chủ ngữ, vị ngữ, đọc to lên nghe là một ý trọn), và câu sau nối được với câu trước bằng từ nối hoặc câu chuyển ("vì", "nên", "nghĩa là", "thử nhìn lại ảnh", "ngược lại", "vậy…").
Các phần gợi ý (đảo thứ tự nếu kể tự nhiên hơn; phần có dấu * bắt buộc, các phần còn lại dùng khi bài có nội dung, không ép):
- A*. Mở (1 cảnh, 4–6s): một quan sát CỤ THỂ trên ảnh dẫn vào câu hỏi mà reel sẽ trả lời (ví dụ "Hai mươi khung ảnh trên một bức tường, sao nhìn không rối?"). Không mở bằng câu chung như "Bạn có biết…".
- B. Nguồn gốc nguyên tắc (1 cảnh, 4–6s): ai đề xuất hay làm nổi tiếng nó, năm nào, theo đúng bài (nhà lý thuyết màu, nhà thiết kế nội thất/trang trí, nhà thiết kế đồ nội thất, nhà nghiên cứu tri giác). Nói thành câu có nghĩa ("Josef Albers, trong cuốn sách năm 1963, nhận ra rằng…"), không chỉ ném tên và năm. Không lấy kiến trúc sư hay lý thuyết kiến trúc làm nguồn gốc.
- C*. Cơ chế, vì sao mắt thấy vậy (2–3 cảnh, 10–16s): giải thích bằng ngôn ngữ đời thường điều bài nói (mắt/não làm gì, khi nào thì xảy ra), có chữ "vì" hay "nên" nối nguyên nhân với kết quả. Được diễn giải lại bằng lời dễ hiểu và thêm câu nối, miễn không thêm sự kiện, nguyên nhân hay số liệu mà bài không có. Nếu bài chỉ nêu kết quả mà không nêu lý do thì nói đúng như vậy ("bài không giải thích vì sao, nhưng quan sát cho thấy…"), không bịa lý do.
- D*. Đọc trên ảnh (2–3 cảnh, 10–16s): mỗi cảnh một chi tiết, zoom vào đúng MÓN ĐỒ, MẢNG MÀU, VẬT LIỆU hay NHÓM ĐỒ, gọi tên nó và nói nguyên lý đang hoạt động ra sao ở đó, bằng câu hoàn chỉnh ("Trong ảnh này, kệ sơn xanh đậm, còn gáy sách phần lớn sáng màu, nên mắt thấy sách trước rồi mới thấy kệ").
- E. Lỗi hay gặp hoặc phản ví dụ (1 cảnh, 4–7s): nếu làm sai thì trông thế nào; nói rõ đây là lỗi bài nêu hay chỉ là giả định của tác giả.
- F*. Cách áp dụng cụ thể (1–2 cảnh, 5–9s): một hai việc làm được ngay trong nhà mình, đủ cụ thể để làm theo, lấy từ bài.
- G. Chọn mua, chọn đồ (1 cảnh, 4–7s): nguyên tắc này đổi cách chọn đồ thế nào; cụ thể, lấy từ bài.
- H*. Chốt (1 cảnh, 4–6s): một hai câu tóm lại dễ nhớ, có thông tin, nối được với mở bài (trả lời lại câu hỏi ở cảnh A).
- I*. Cảnh cuối (1 cảnh, 8–10s, tính trong tổng thời lượng): nhắc AH Decode là series về nguyên tắc thiết kế và chọn đồ decor, và CÂU CUỐI CÙNG luôn là: bài viết phân tích đầy đủ xem ở dòng đầu tiên trong phần bình luận. KHÔNG mời "theo dõi Fanpage", KHÔNG đọc tên Fanpage (bỏ cho bớt chữ), KHÔNG nhắc tập sau, không đọc nguồn hay credit. Lời đọc mẫu (khoảng 22 từ): "AH Decode, series về nguyên tắc thiết kế và chọn đồ decor. Bài viết phân tích đầy đủ xem ở dòng đầu tiên trong phần bình luận."
Quy tắc:
- Nội dung lấy từ bài (mục 3). Bài không có nội dung cho một phần thì bỏ phần đó, ghi rõ trong `script.md` và báo cáo; KHÔNG tự nghiên cứu hay tự viết để lấp chỗ trống. Phần D luôn làm được vì là quan sát trên ảnh.
- Mỗi cảnh mang một ý trọn vẹn. Không dồn nhiều thông tin rời vào một câu; nếu một cảnh cần nhiều chi tiết thì tách thành hai câu hoặc hai cảnh.
- Cấm câu cụt và câu liệt kê rời kiểu "Bê tông, sàn gỗ, rèm: trung tính." hay "Khối xanh: màu mạnh duy nhất." Viết thành câu đủ ý: "Trong ảnh này, bê tông, sàn gỗ và rèm đều là màu trung tính, nên chúng lùi về làm nền."
- Cấm các cụm chung chung không kèm giải thích: "tạo cảm giác hài hoà", "trông đẹp hơn", "thu hút ánh nhìn", "tạo điểm nhấn", "cân bằng thị giác" khi chưa nói vì sao và bằng cách nào. Không lặp lại cùng một ý bằng chữ khác để kéo dài thời lượng.
- Độ dài: khoảng 150–210 từ lời đọc (cảnh cuối tính vào), 8–13 cảnh, mỗi cảnh tối đa khoảng 26 từ (nếu lời đọc hiển thị quá 3 dòng trên khung thì kiểm tra không bị cắt hay tràn). Cách làm đã dùng: viết dữ liệu cảnh một lần trong script sinh engine, tự tính thời lượng mỗi cảnh = 0,7 giây + số từ / 3,2 (tối thiểu 3,5 giây), in tổng số từ và tổng thời lượng. Vượt ngưỡng thì bớt một phần không bắt buộc (B, E, G) hoặc bớt một ý phụ, KHÔNG nén câu thành mảnh rời.
- Lời khuyên (phần E, F, G) lấy từ bài, dùng "nên", "thử", "nên tránh"; giữ đúng ai là người khuyên và mức chắc chắn của bài ("theo tụi mình", "có xu hướng", "dễ").

## 4b. Tự chấm trước khi dựng hình
Agent đọc lại (bước 5) CÓ bài gốc và kịch bản, trả lời có/không cho từng câu, kèm lý do. Câu 1 đặt ĐẦU TIÊN vì quan trọng nhất:
1. Đọc to kịch bản thành một lượt liền. Người CHƯA đọc bài có hiểu reel nói gì, vì sao, và nên làm gì không? Liệt kê từng câu cụt, câu liệt kê rời, câu thiếu chủ ngữ/vị ngữ, chỗ chuyển ý đột ngột, từ viết tắt hay cách nói chỉ người đã đọc bài mới hiểu. Có câu nào như vậy thì phải viết lại, kể cả khi phải bỏ một phần không bắt buộc.
2. Có đủ các phần bắt buộc (A, C, D, F, H, I) và các phần tuỳ chọn có mặt thì có ý cụ thể không? Phần cơ chế có nói được vì sao (có chữ nối nguyên nhân, không chỉ nhắc lại định nghĩa) và đúng điều bài viết không?
3. Người xem có học được ít nhất ba điều cụ thể họ có thể chưa biết? Liệt kê ba điều đó.
4. Có câu chung chung, lặp ý hoặc nói quá bài không? Liệt kê.
5. Lời khuyên áp dụng và chọn đồ có làm theo được ngay không, và có đúng như bài không?
6. Mọi nhận định đều có trong bài gốc và có dòng tương ứng (vị trí trong bài) trong `sources.md`? Có tên, năm, số liệu, lời khuyên, nguyên nhân nào ngoài bài không? (Câu nối và diễn giải bằng lời đời thường điều bài nói thì KHÔNG tính là ngoài bài.) Liệt kê.
0. Có đúng trọng tâm mục 1a (nội thất, decor, màu, đồ đạc, vật liệu, bố cục đồ; không phải lý thuyết kiến trúc)? Có câu, cảnh hay nguồn nào lệch sang kiến trúc không?
Có câu trả lời "không" thì sửa kịch bản (không tìm thêm nguồn ngoài bài), rồi hỏi lại agent chấm lượt nữa trước khi dựng hình. Khi sửa theo góp ý, KHÔNG chữa bằng cách thêm từ rào đón rời ("hẳn", "như ở bếp", "trong khung") vào câu cụt; viết lại cả câu cho trọn nghĩa. Nếu hai tiêu chí mâu thuẫn, áp dụng thứ tự ưu tiên ở đầu mục 4a.

## 5. Engine dựng khung (thư mục ENGINE = REPO/engine)
Gồm: `engine_video.py` (mục 5b), `engine_storyboard_v7.py` (chạy bằng `python3 -I`; script tự thêm thư mục của nó vào sys.path), `silhouette.py`, `PatrickHand-Regular.ttf`, `reel1_source_example.png` (ảnh mẫu tập #1). Cần: Python 3, Pillow, numpy, opencv-python (pip cần `--break-system-packages`), ffmpeg.
Chạy: `python3 -I engine_storyboard_v7.py <ảnh> <thư_mục_ra>`
Engine v7 đang hard-code ảnh và toạ độ của tập #1. Mỗi tập, sao chép thành `engine_epNN.py` rồi sửa CHỈ các phần sau:
- `SCENES` (tiêu đề `head`, lời `vo`, thời lượng `t`, camera `cam=(điểm_focus_trên_ảnh, zoom, vị_trí_trên_khung)`, `dark`). Cảnh cuối luôn có `head="end"`, `vo=""`.
- `OBJ`: đa giác thô quanh đồ vật (toạ độ ảnh làm việc). Hàm `doodle()`: trục, đường nối, hình bao, nhãn.
- `CREDIT`, `HEAD` (đầu trang luôn là `AH DECODE · <TÊN CHỦ ĐỀ VIẾT HOA>`), tên file ra.
Không đổi: kích thước 1080×1920, nền trắng, băng keo giấy ở giữa mép trên, ảnh không viền, chữ viết tay Patrick Hand, bố cục chữ theo vùng an toàn (mục 6a, đã cài trong engine: hàm `text_layout`, `qa_text`, cam `WIDE_SAFE`, `END_SAFE`), khung cuối `END_LINES` (đã cố định: "AH Decode · series phân tích nguyên tắc thiết kế và cách chọn đồ decor / Bài viết phân tích đầy đủ / xem ở dòng đầu tiên / trong phần bình luận"; KHÔNG có dòng "Theo dõi Fanpage" và tên Fanpage).
Cách làm nhanh đã dùng ở tập 2 (xem `inbox/out/2026-10-06_gestalt-gan-nhau/engine_ep02/`): viết một script nhỏ đọc hai engine gốc, thay khối từ dòng `# ---------------- scenes` đến trước `def render_scene` (engine khung) hoặc trước `BOARDS["plain"] = make_board(1.0)` (engine video) bằng khối dữ liệu của tập, thay `CREDIT`, `HEAD`, tên file ra, rồi ghi thành `engine_epNN.py` và `engine_video_epNN.py`. Một nguồn dữ liệu cho cả hai engine nên chúng luôn đồng bộ. Hàm `D(pts)` trong khối dữ liệu đó đổi toạ độ đo trên ảnh xem thu nhỏ sang ảnh làm việc 2400 px.
Cảnh không có vật để khoanh (nguồn gốc, cơ chế) vẫn phải có hình: dùng cảnh rộng hoặc zoom vào vùng liên quan, nét doodle tối giản (một đường, một mũi tên) hoặc không nét; không chèn đồ hoạ khác.

## 5b. Engine dựng video (`engine_video.py`, nằm cùng thư mục ENGINE)
Là bản mở rộng của engine khung hình: cùng `SCENES`, `OBJ`, `doodle()`, `CREDIT`, `HEAD`. Mỗi tập sao chép thành `engine_video_epNN.py` và sửa CÙNG các phần như mục 5, nên giữ hai engine đồng bộ (sửa dữ liệu cảnh một lần, dán sang cả hai).
Chạy: `python3 -I engine_video_epNN.py <ảnh> <thư_mục_ra>` → `<thư_mục_ra>/video/reel1_silent.mp4` (đổi tên thành `reel_<slug>_silent.mp4`).
Mất khoảng 6–7 phút cho mỗi 30 giây video (30 fps, 1080×1920, H.264 CRF 17), tức khoảng 10–15 phút cho reel 55–75 giây: chạy nền (`nohup … > log 2>&1 &`), làm việc khác trong lúc chờ, rồi kiểm tra log. Engine ghi thêm vài ảnh `probe_*.png` vào thư mục `video/`: xoá sau khi chuyển file mp4 ra.
Hành vi đã duyệt, không tự ý đổi:
- Thời lượng mỗi cảnh lấy từ trường `t` của `SCENES` (ví dụ "3–8s"); video dài đến hết cảnh cuối + 1 giây.
- Chuyển cảnh 0,7 giây: camera nội suy zoom và vị trí; chữ và nét của cảnh cũ mờ đi trong 0,25 giây đầu; tiêu đề và lời đọc của cảnh mới hiện ra ở cuối quãng chuyển.
- Nét doodle được vẽ dần (theo thứ tự các nét trong `doodle()`), bắt đầu sau khi camera dừng, xong ở khoảng 62% thời lượng cảnh; nhãn chữ trong `doodle()` hiện khi nét vẽ đạt khoảng 55–75%.
- Khung cuối giữ thêm 1 giây. Video có sẵn track âm thanh im lặng để ghép tiếng sau.
Nếu một cảnh quá ngắn để vẽ hết nét (cảnh nhiều nét mà dưới 3 giây), kéo dài cảnh đó trong `SCENES` hoặc bớt nét, không tăng tốc vẽ.

## 5d. Reel dùng nhiều ảnh
Cách hiện hành (tập 7, `inbox/out/2026-10-18_mem-trong-tam-tay/engine_ep07/`): mỗi cảnh khai báo `img` (khoá trong `IMGS`: file ảnh làm việc, npz doodle gốc, credit riêng của ảnh). `gen_epNN.py` gom các cảnh liên tiếp cùng ảnh thành "run" và sinh cho mỗi run `engine_epNN_rKK_<ảnh>.py` + `engine_video_epNN_rKK_<ảnh>.py` (cảnh trước dựng toàn cảnh trên ảnh của run, các cảnh của run, khung cuối giả nếu run không chứa khung cuối); hình học thẻ tự tính theo tỷ lệ ảnh (dọc, vuông: thẻ cao 1920 ở bảng 2x, C2 y 1880; ngang: rộng 1920, C2 y 1810). `runs.json` ghi mốc cắt của mỗi run; `sheet_epNN.py` chạy engine khung của từng run, gom khung vào `frames/` và dựng `storyboard.png`. Giai đoạn 2: dựng video từng run, cắt đúng đoạn `cut_from`, `cut_len` của mỗi run và nối theo thứ tự (`ffmpeg` trim + concat), rồi ghép tiếng.
Cách cũ (tập 6) cho một ảnh phụ, còn dùng được:
- Trong dữ liệu cảnh, đánh dấu cảnh đó (`img`, `cam_bep`, `dd_bep`); script sinh thêm `engine_epNN_<anh>.py` và `engine_video_epNN_<anh>.py` từ engine gốc, với ba cảnh: cảnh trước (ảnh phụ toàn cảnh, cùng tiêu đề và lời của cảnh trước trong video chính), cảnh dùng ảnh phụ, một khung cuối giả. Ảnh ngang dùng hình học thẻ mặc định của engine gốc, ảnh dọc dùng bản thẻ hẹp như tập 5, 6.
- Ảnh phụ cũng tách lớp doodle gốc như mục 2c (`source_<anh>.png`, `doodle_epNN_<anh>.npz`). Ở video chính, cảnh đó để camera rộng, không nét (để quãng chuyển sang cảnh sau mượt).
- Ghép: lấy đúng đoạn của cảnh ảnh phụ trong video phụ (bắt đầu từ đầu cảnh, gồm cả 0,7 giây chuyển cảnh từ ảnh phụ toàn cảnh vào), thay vào đúng mốc thời gian của cảnh đó trong video chính (`ffmpeg` trim + concat), rồi mới ghép tiếng.
- Bảng phân cảnh dùng khung của cảnh đó từ engine phụ.

## 5c. Giai đoạn 2: dựng video theo giọng đọc (chỉ khi có file ghi âm)
Không có bản video không tiếng làm trước. Trình tự: đo audio, căn `t` từng cảnh theo nhịp đọc, dựng video bằng engine video (mục 5b) từ `engine_video_epNN.py` của tập, rồi ghép tiếng. Kiểm tra video theo mục 7 trước khi giao. Đầu ra: `reel_<slug>_final.mp4` (xoá bản không tiếng trung gian nếu có). Commit, push, gửi video cho người dùng.
1. Đo thời lượng audio: `ffprobe -v error -show_entries format=duration -of csv=p=0 <audio>`. KHÔNG tự cắt hay kéo giãn giọng.
2. Tìm ranh giới từng câu/cảnh: `ffmpeg -i <audio> -af silencedetect=noise=-35dB:d=0.25 -f null -`, ghép các quãng nghỉ với các đoạn (cảnh) theo thứ tự trong `elevenlabs.txt`. Đặt lại `t` của từng cảnh trong dữ liệu cảnh (gen_epNN.py) sao cho mỗi cảnh bắt đầu khoảng 0,3–0,5 giây trước câu của nó (để chuyển cảnh 0,7 giây trùng quãng nghỉ) và cảnh cuối kéo đến hết giọng đọc. Sinh lại `engine_epNN.py` và `engine_video_epNN.py` từ cùng dữ liệu; cập nhật `script.md` (cột thời lượng).
3. Dựng video bằng engine video (mục 5b) với `t` mới (chạy nền), rồi ghép: `ffmpeg -y -i <video_dung> -i <audio> -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -af "loudnorm=I=-16:TP=-1.5:LRA=11,apad" -t <thời lượng video> reel_<slug>_final.mp4`.
4. Chuẩn âm lượng nhẹ đã nằm trong lệnh ghép (loudnorm I=-16).
5. Kiểm tra bằng cách trích vài khung và đối chiếu thời điểm nhãn chữ với câu đang đọc (dùng silencedetect); báo cáo nếu lệch quá 1 giây.

## 6. Quy cách hình ảnh (đã duyệt, không tự ý đổi)
- Khung 1080×1920. Nền trắng trơn. Ảnh dự án là ảnh GỐC, không sketch hoá, không làm mờ; dán bằng một miếng băng keo giấy ở giữa mép trên, không viền, hơi nghiêng ~1°, có bóng nhẹ.
- Cảnh rộng: ảnh nằm giữa khung (cam `WIDE_SAFE`, thẻ ảnh gọn trong y ~610–1210); chữ nằm NGOÀI ảnh (nâu đậm), mũi tên trắng/nâu chỉ vào nét doodle. Cảnh nói chi tiết: camera zoom vào ảnh; khi hết chỗ nền thì chữ trắng viết lên ảnh, có phủ tối nhẹ đúng dải chữ để dễ đọc. Mọi chữ theo vùng an toàn mục 6a.
- Mọi nét doodle trên ảnh: màu TRẮNG, NÉT ĐỨT, nét tay tự nhiên. Đồ vật được bao bằng đường đứt ôm theo hình dáng tổng quát (không khoanh tròn), sau khi zoom vào đúng đồ vật/cụm.
- Tất cả chữ viết tay. Header nhỏ ở đầu vùng an toàn (y 344), tiêu đề cảnh bên dưới (y 392, tối đa 2 dòng), KHÔNG đánh số "Bước n". Dòng credit nhỏ ngay dưới ảnh. Không gạch chân lượn sóng.
- Khung cuối (cam `END_SAFE`): ảnh rộng + credit dưới ảnh, rồi "AH Decode · series phân tích nguyên tắc thiết kế và cách chọn đồ decor / Bài viết phân tích đầy đủ / xem ở dòng đầu tiên / trong phần bình luận" (đã cố định trong engine). KHÔNG có cụm "Theo dõi Fanpage" và tên Fanpage (quá nhiều chữ). Không có dòng nguồn, không nhắc tập sau.

## 6a. Vùng an toàn chữ: Reels VÀ bảng tin Facebook (bắt buộc)
Lý do: khi reel 9:16 hiện trên bảng tin (newsfeed) Facebook, nó bị cắt thành khung 4:5 ở giữa, chỉ còn thấy y 285–1635 (ffmpeg `crop=1080:1350:0:285`); trong trình xem Reels, đáy khung bị chú thích và nút che, nửa dưới mép phải bị cột nút (thích, bình luận, chia sẻ) che. Tập 6 đã bị mất header và tiêu đề trên bảng tin vì chữ đặt ở y 96–330. Từ nay:
- MỌI chữ (header, tiêu đề, credit, phụ đề, nhãn doodle, chữ khung cuối) nằm trong y 340–1490 và x 60–1020; ở nửa dưới (y > 1000) chữ không vượt x 960 (tránh cột nút Reels). Khối chữ rộng tối đa 880 px.
- Bố cục cố định (engine `text_layout`): header y 344; tiêu đề y 392, cỡ 80, tối đa 2 dòng (hết ở ~590); phụ đề cỡ 56, tối đa 3 dòng, dòng cuối kết thúc ở ~1482; credit cỡ 30 ngay trên phụ đề. Ảnh, nét vẽ và nền có thể tràn ngoài vùng an toàn; chỉ chữ phải ở trong.
- Chọn camera sao cho mép ảnh KHÔNG cắt ngang khối chữ: mép trên ảnh ≤ 310 (tiêu đề nằm trên ảnh, chữ trắng) hoặc ≥ 600 (tiêu đề nằm trên nền trắng, chữ nâu); mép dưới ảnh ≤ y credit − 20 (khoảng 1270 với phụ đề 2 dòng) hoặc ≥ 1520. Engine in `CẢNH BÁO cảnh n: mép … cắt ngang khối …` kèm số gợi ý khi vi phạm.
- Nhãn và mũi tên doodle cần đọc được phải nằm giữa hai khối chữ (khoảng y 610–1240), không chồng lên tiêu đề hay phụ đề. Nếu một ảnh có nhiều nhãn trải quá cao, chỉ lộ các nhãn khớp lời đọc vừa trong dải đó (ví dụ cảnh bếp tập 6 chỉ lộ nhãn "đá vân xanh sau bồn rửa").
- Cảnh rộng dùng `WIDE = WIDE_SAFE`, khung cuối dùng cam `END_SAFE` (khai báo sẵn trong engine; trong khối dữ liệu cảnh của tập, KHÔNG tự đặt lại WIDE bằng toạ độ cũ).
- Kiểm tra tự động: mỗi lần chạy engine khung và engine video, hàm `qa_text` in `LỖI: chữ ra ngoài vùng an toàn Reels/bảng tin (cảnh n …)`. Có dòng LỖI hoặc CẢNH BÁO nào thì sửa camera (hoặc rút gọn tiêu đề/phụ đề) rồi chạy lại cho đến khi sạch, trước khi giao.
- Xem thử bằng mắt: trích vài khung video và cắt `ffmpeg -vf "crop=1080:1350:0:285"` để xem đúng như trên bảng tin; header, tiêu đề, phụ đề phải còn đủ.

## 7. Kiểm tra bắt buộc trước khi giao (đọc từng khung bằng Read)
- Đạt mục 2d: có ít nhất một diagram (sketch) của bài, có mặt bằng nếu bài có, có ảnh của ít nhất ba không gian khác nhau, không ảnh nào chiếm quá khoảng nửa số cảnh; chú thích trên diagram, mặt bằng đọc được ở khung 1080×1920.
- Chạy engine không còn dòng `LỖI: chữ ra ngoài vùng an toàn Reels/bảng tin` hay `CẢNH BÁO … cắt ngang khối …` (mục 6a); đã xem thử khung cắt 4:5 của bảng tin.
- Hình bao ôm đúng đồ vật được nhắc trong lời đọc; nét không tràn ra ngoài ảnh; không có "cục" đậm do nét chồng nhau.
- Chữ đọc rõ, có đủ dấu tiếng Việt, không bị cắt, không đè lên nét vẽ khó đọc, không nằm vắt ngang mép ảnh.
- Lời đọc khớp với hình trong cùng cảnh, là một mạch kể hiểu được khi nghe, không có câu cụt; tổng thời lượng 55–75 giây (tốc độ đọc khoảng 2,5–3 từ/giây), 150–210 từ.
- Đủ các phần bắt buộc (A, C, D, F, H, I) theo mục 4a; kịch bản nghe là hiểu, không có câu cụt; đã qua tự chấm mục 4b (câu 1 đầu tiên).
- Từng nhận định trong lời đọc đều có trong bài gốc và có dòng tương ứng trong `sources.md` (mục 3.1); không có nhận định ngoài bài.
- Video: trích ít nhất 12 khung (đầu, giữa quá trình vẽ, cuối từng cảnh chính, khung cuối) để kiểm tra: nét vẽ đã đủ khi cảnh kết thúc, không có nét của cảnh cũ lẫn sang cảnh mới, chữ không bị cắt, chuyển cảnh không giật. Kiểm tra `ffprobe`: 1080×1920, h264, có track âm thanh, thời lượng đúng dự kiến.
- Không có logo, thương hiệu hay tên người xuất hiện sai trong khung.
Kịch bản và nguồn đã được agent độc lập chấm ở bước 5 mục 4; nếu sau đó kịch bản còn đổi, nhờ đọc lại lần nữa.

## 8. Đầu ra (OUT = INBOX/out/<YYYY-MM-DD>_<slug>/)
- `research.md`: ghi chú bài theo các phần mục 4a, kèm vị trí và trích ngắn trong bài (bước 3 mục 4). Đầu file ghi bài đã dùng: đường dẫn trong kho, link GitHub, commit SHA.
- `script.md`: bảng cảnh (thời lượng, phần nội dung A–I, tiêu đề, lời đọc, hình) + phần lời đọc liền mạch + kết quả tự chấm mục 4b.
- `elevenlabs.txt`: văn bản thuần để người dùng dán thẳng vào ElevenLabs (mục 8b).
- `source_info.md`, `original/`.
- `frames/scene_*.png` + `storyboard.png` + `frames.zip`.
- Giai đoạn 1 (tập mới): KHÔNG có video. Giai đoạn 2 (đã có ghi âm): `reel_<slug>_final.mp4`.
- `sources.md`: mỗi nhận định → vị trí trong bài (file + mục/đoạn + trích ngắn) → mức chắc chắn theo bài (nguyên lý / thực nghiệm / quy tắc kinh nghiệm) → nguồn mà bài dẫn cho ý đó (nếu có, chép đúng như bài). Cuối file: danh mục nguồn tham khảo của bài.
- `caption.txt`: caption đăng bài có chiều sâu, bổ sung cho reel (không chép lại lời đọc): vài đoạn ngắn về nguồn gốc, cơ chế, cách áp dụng và gợi ý chọn đồ, lấy từ bài theo cùng quy tắc mục 3 như lời đọc; rồi dòng giới thiệu và mời "AH Decode là series mới của Giả Thuyết Kiến Trúc, phân tích các nguyên tắc thiết kế và cách chọn đồ decor. Theo dõi Fanpage Giả Thuyết Kiến Trúc. Bài viết phân tích đầy đủ xem ở dòng đầu tiên trong phần bình luận."; rồi 2–3 nguồn chính lấy từ danh mục nguồn của bài (nếu bài có), credit ảnh đầy đủ theo bài (chỉ ghi link nếu chính bài có ghi); hashtag vừa phải. Không tự điền link (người dùng tự dán vào dòng đầu tiên của phần bình luận).
- Gửi cho người dùng (SendUserFile) ở giai đoạn 1: `elevenlabs.txt` đầu tiên, rồi ảnh bảng phân cảnh, `script.md`, `sources.md`, `caption.txt`; kèm tóm tắt tối đa 6 dòng: bài đã dùng trong kho, nguyên lý, ba điều người xem học được, điểm cần duyệt (kể cả phần bài thiếu hoặc nghi lỗi), credit đã có hay còn thiếu, và nhắc "gửi file ghi âm vào INBOX/audio/<slug>.mp3 để dựng video". Đồng thời dán nguyên văn nội dung `elevenlabs.txt` (phần dán) vào cả câu trả lời và thông báo PushNotification, để người dùng copy ngay. Giai đoạn 2: gửi `reel_<slug>_final.mp4` và báo thời lượng.
Đây là BẢN NHÁP chờ người dùng duyệt. Không đăng, không gửi đi đâu khác.

## 8b. Quy cách `elevenlabs.txt`
Mục tiêu: người dùng mở file, chọn tất cả, dán vào ElevenLabs, không phải sửa gì.
- Chỉ có lời đọc, theo đúng thứ tự cảnh. Không đánh số cảnh, không tiêu đề, không chú thích, không ngoặc chỉ dẫn, không emoji, không hashtag, không tên file.
- Mỗi cảnh một đoạn; giữa các đoạn cách một dòng trống. Trong đoạn, mỗi câu một dòng.
- Đọc được thành tiếng một cách tự nhiên: viết số, ký hiệu và từ viết tắt thành chữ (ví dụ "60-30-10" thành "sáu mươi, ba mươi, mười"; "≠" thành "không bằng"; "%" thành "phần trăm").
- PHIÊN ÂM SẴN mọi tên và từ tiếng Anh (hoặc tiếng nước ngoài khác) ngay trong lời đọc, để người dùng dán thẳng vào ElevenLabs, KHÔNG phải sửa gì: tên người, tên tác phẩm, tên series, thuật ngữ tiếng Anh. Viết theo âm tiếng Việt, các âm tiết nối bằng gạch nối, không để kèm chính tả gốc trong ngoặc. Ví dụ: "AH Decode" → "Ây-ết Đi-cốt"; "decor" → "đê-co"; "Hogarth" → "Hô-gát"; "Dieter Rams" → "Đi-tơ Ram"; "Charles và Ray Eames" → "Sác-lơ và Rây Im-xơ"; "Hans Wegner" → "Han Ve-gơ-nơ"; "Josef Albers" → "Giô-dép An-bơ"; "Bauhaus" → "Bao-hao". Chọn cách đọc theo ngôn ngữ gốc của tên (tên Đức đọc kiểu Đức…). Giữ CÙNG một cách phiên âm cho cùng một tên trong cả file.
- Chỉ `elevenlabs.txt` dùng phiên âm. Chữ trên khung hình, `script.md` và `caption.txt` giữ chính tả gốc. Trong `script.md` thêm bảng nhỏ "Phiên âm cho ElevenLabs" (chính tả gốc → phiên âm) để người dùng tra.
- Dấu câu để điều khiển nhịp: dấu phẩy và chấm đủ rõ; chỗ cần ngắt dài hơn thì dùng dấu "..." hoặc dòng trống, không chèn thẻ kỹ thuật. Câu hoàn chỉnh, tối đa khoảng 25 từ.
- Độ dài khớp thời lượng cảnh trong `SCENES`: khoảng 2,5–3 từ mỗi giây, trừ khoảng 0,7 giây chuyển cảnh ở đầu mỗi cảnh. Cuối file ghi thêm một dòng riêng NGOÀI phần dán: `--- Gợi ý cài đặt: giọng nữ hoặc nam trầm ấm, tốc độ 1.0, mô hình đa ngôn ngữ, ngôn ngữ Vietnamese ---` để người dùng tham khảo (dòng này phân tách bằng một dòng trống và dấu `---`, người dùng chỉ dán phần phía trên). Không ghi chú tên riêng hay cách đọc ở dòng này vì lời đọc đã phiên âm sẵn.
- Cảnh cuối chỉ đọc câu giới thiệu series AH Decode và câu cuối cùng (không mời theo dõi Fanpage, không đọc tên Fanpage): bài viết phân tích đầy đủ xem ở dòng đầu tiên trong phần bình luận (mẫu ở mục 4a, phần I). Không gợi ý tập sau, không đọc nguồn hay credit. Cảnh cuối trong `elevenlabs.txt` viết dạng phiên âm, ví dụ: "Ây-ết Đi-cốt, series về nguyên tắc thiết kế và chọn đồ đê-co. Bài viết phân tích đầy đủ xem ở dòng đầu tiên trong phần bình luận." ("series" là từ quen dùng trong tiếng Việt, giữ nguyên.)

## 9. Khi gặp sự cố
- Bài không có ảnh nào dùng được làm nền: vẫn làm bản tốt nhất với ảnh có sẵn của bài, nêu rõ hạn chế; KHÔNG tìm ảnh ngoài kho.
- Ảnh quá nhỏ (<1200 px cạnh dài), quá tối, hoặc không minh hoạ được ý chính của bài: vẫn làm bản tốt nhất có thể, ghi rõ hạn chế (ví dụ zoom bị mềm) và đề nghị ảnh khác.
- Không truy cập được KHO BÀI (add_repo/clone/GitHub MCP đều lỗi, hoặc không thấy thư mục `AH-Decode-Decor/` trên nhánh `AH-Interior-notes`): dừng, báo lỗi cụ thể. KHÔNG tự nghiên cứu để thay thế.
- Hết ý chưa dùng trong mọi bài của kho: dừng và báo người dùng thêm bài; không tự viết bài mới, không làm lại ý đã dùng. (Vẫn làm giai đoạn 2 nếu có file ghi âm đang chờ.)
- Bài thiếu nội dung cho một vài phần (B, E, G là tuỳ chọn; thiếu C, F hoặc H thì báo cáo): làm với phần bài có (mục 4a), ghi rõ phần thiếu trong báo cáo. Bài quá mỏng để làm reel 55–75 giây có chiều sâu: vẫn làm bản tốt nhất, ghi rõ hạn chế; không tự bổ sung kiến thức ngoài bài.
- Dựng video quá thời gian hoặc ffmpeg lỗi: vẫn giao khung hình, script và `elevenlabs.txt`, nói rõ video chưa dựng được và vì sao.
- Công cụ lỗi (mạng, thư viện): thử lại một lần, rồi báo lỗi cụ thể thay vì bỏ qua bước.

## 10. Việc KHÔNG làm
- Không tự nghiên cứu, không lấy thông tin nội dung từ web hay từ trí nhớ; chỉ dùng bài trong KHO BÀI (mục 3). Không sửa hay push gì vào kho bài.
- Không đổi quy cách hình ảnh ở mục 6. Không sketch hoá ảnh dự án. Không bỏ credit.
- Không dùng ảnh/đồ hoạ nào ngoài thư mục `anh/` của bài và ảnh của chính công trình từ trang nguồn ảnh bài ghi (mục 2b). Không lấy thông tin nội dung từ trang web nào.
- Không đổi nhịp chuyển cảnh/vẽ nét đã duyệt (mục 5b), không thêm nhạc nền, hiệu ứng hay phụ đề chạy chữ khi chưa được yêu cầu.
- Không bịa tên studio, nhiếp ảnh gia hay dự án khi thiếu credit; chỉ ghi những gì có trên trang bài nguồn.
- Không hẹn hay gợi ý "tập sau" ở bất kỳ đâu (khung, lời đọc, caption).
- Không làm tập về lý thuyết kiến trúc hay không gian công trình (mục 1a): không prospect–refuge, không phân tích nhà của kiến trúc sư, không lấy trần, cột, vách kính, view làm nội dung chính.
- Không dừng giữa chừng để chờ duyệt lý thuyết hay ảnh.