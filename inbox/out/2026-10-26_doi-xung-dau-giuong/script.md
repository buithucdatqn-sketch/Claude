# AH Decode · Đối xứng dành cho đầu giường · tập 12 · giai đoạn A, chờ ghi âm

Bài: bai-04 (kho AH-Decode-Decor, nhánh AH-Interior-notes, commit bd74e53), bài học 1 "Dùng cân bằng đối xứng cho những chỗ cần sự yên ổn, như đầu giường", cùng phần mở "Mắt người cân đồ đạc… bập bênh" làm nguồn gốc. Bài 04 mới duyệt 2026-10-26; tập 11 dùng bài 03 nên đổi bài đúng mục 0.5b. Làm theo bộ khuôn `engine/mau_tap7/` (mã gốc gen_ep11.py), bộ nguyên tắc hành văn mục 0.6f, quy tắc viết lời trước, cắt cảnh sau (mục 0.6h).

Lần chạy này là bản làm lại trong cùng ngày: bản đầu (một ảnh, sáu cảnh, ý lò sưởi và tranh sẫm của bài học 2, slug `lech-ma-van-can`) làm theo prompt lịch chạy cũ thay vì TASK_INSTRUCTION, chủ Trang chê "hoàn toàn không đúng yêu cầu trong instruction"; bản đó đã bỏ hẳn (không commit vào nhánh này), ý bài học 2 coi như CHƯA dùng.

## Câu hỏi trung tâm
Phòng khách kê lệch hẳn, vậy vì sao đầu giường trong căn hộ này lại được kê đối xứng?
Trả lời theo bài: mắt giữ thăng bằng như cơ thể, thấy món nặng món nhẹ (Kilmer & Kilmer 2014); đối xứng là cách mắt nhận ra nhanh nhất; hai bên giống hệt nhau thì mắt không phải so, dừng ở trục giữa và thấy yên (diễn giải của bài). Palmeira chỉ kê đối xứng ở đầu giường và trong vách tắm, còn phòng khách kê lệch (nhận xét của bài); Kilmer nhắc đối xứng quá nhiều làm phòng tĩnh, buồn tẻ. Vì vậy giữ đối xứng ở đầu giường, chỗ cần yên, các phòng khác không cần.

## Bảng cảnh (13 cảnh, 277 từ phụ đề; thời lượng tính nháp 3,2 từ/giây trong engine, giai đoạn B căn lại theo ghi âm; ước giọng thật khoảng 64–68 giây)
| # | Phần | Ảnh | Tiêu đề trên khung | Phụ đề (loi) | Bản đọc (tts) |
|---|---|---|---|---|---|
| 1 | A | ảnh 04 phòng ngủ chính (gốc) | Một căn hộ, hai cách kê đồ | Phòng khách kê lệch hẳn, vậy vì sao đầu giường trong căn hộ này lại được kê đối xứng? | giữ nguyên |
| 2 | B | ảnh 01 sơ đồ ba kiểu cân bằng | Theo Kilmer & Kilmer (2014), mắt cũng giữ thăng bằng | Trong một cuốn sách năm 2014 về thiết kế nội thất, hai tác giả Kilmer cho rằng mắt người cũng giữ thăng bằng như cơ thể. | Trong một cuốn sách năm hai nghìn không trăm mười bốn về thiết kế nội thất, hai tác giả Kin-mơ cho rằng mắt người cũng giữ thăng bằng như cơ thể. |
| 3 | B | ảnh 01 sơ đồ ba kiểu cân bằng | Theo Kilmer & Kilmer (2014), mắt cũng giữ thăng bằng | Nhìn vào một căn phòng, mắt thấy món đồ này nặng, món kia nhẹ. | giữ nguyên |
| 4 | C | ảnh 01 sơ đồ, khung đối xứng | Hai nửa giống nhau qua một trục | Hai tác giả cũng cho rằng đối xứng là cách giữ thăng bằng mà mắt nhận ra nhanh nhất. | giữ nguyên |
| 5 | C | ảnh 01 sơ đồ, khung đối xứng | Mắt dừng lại ở trục giữa | Theo tụi mình, hai bên đã giống hệt nhau thì mắt không phải so bên nào nặng hơn, nên dừng ở trục giữa và thấy yên. | giữ nguyên |
| 6 | D | ảnh 03 mặt bằng | Phòng ngủ và phòng tắm chính nằm sát nhau | Phòng ngủ chính của căn hộ Palmeira tại Lisbon, do Studio Gameiro cải tạo, được kê đúng theo trục giữa ấy. | Phòng ngủ chính của căn hộ Pan-mây-ra tại Lít-bon, do Xtu-đi-ô Ga-mây-rô cải tạo, được kê đúng theo trục giữa ấy. |
| 7 | D | ảnh 04, dải đèn thả và đầu giường (doodle mới) | Tấm đầu giường gỗ chạm tay dài hơn giường | Giường nằm giữa một tấm đầu giường bằng gỗ chạm tay, hai bên là hai đèn thả giống nhau, cách đều trục. | giữ nguyên |
| 8 | D | ảnh 05 phòng tắm, hai vòi sen (doodle mới) | Hai vòi sen trong hai ô kính bằng nhau | Phòng tắm ngay bên cạnh cũng đối xứng, nhưng chỉ ở hai vòi sen trong vách kính, | giữ nguyên |
| 9 | D | ảnh 05, dải dưới: chậu rửa, bồn (doodle mới) | Ngoài vách kính, đồ đặt theo chỗ dùng | còn chậu rửa và bồn vệ sinh bên ngoài thì đặt lệch, chỗ nào tiện dùng thì đặt ở đó. | giữ nguyên |
| 10 | H | ảnh 10 phòng khách, dải dưới (doodle mới) | Sofa và lò sưởi đặt lệch hai bên trục | Tụi mình thấy cái khéo của căn hộ là chỉ kê đối xứng ở chỗ nằm nghỉ và chỗ đứng tắm, còn phòng khách thì kê lệch. | giữ nguyên |
| 11 | E | ảnh 10 phòng khách, dải dưới (doodle mới) | Theo Kilmer & Kilmer (2014), đối xứng cũng có giới hạn | Chính Kilmer cũng nhắc rằng dùng đối xứng quá nhiều sẽ làm căn phòng tĩnh và buồn tẻ. | Chính Kin-mơ cũng nhắc rằng dùng đối xứng quá nhiều sẽ làm căn phòng tĩnh và buồn tẻ. |
| 12 | F | ảnh 04, dải đèn thả và đầu giường (doodle mới) | Đối xứng ở đầu giường, kê lệch ở phòng khác | Vì vậy, phòng ngủ nên giữ đối xứng ở đầu giường, chỗ người ta cần yên khi nằm nghỉ, còn các phòng khác thì không cần. | giữ nguyên |
| 13 | I | ảnh 04 phòng ngủ chính (gốc) | (khung cuối) | Bài phân tích đầy đủ về cân bằng thị giác khi bày biện nội thất, mọi người xem ở phần bình luận nhé. | giữ nguyên |

## Lời đọc dán vào ElevenLabs
```
Phòng khách kê lệch hẳn, vậy vì sao đầu giường trong căn hộ này lại được kê đối xứng?
<break time="1.2s" />
Trong một cuốn sách năm hai nghìn không trăm mười bốn về thiết kế nội thất, hai tác giả Kin-mơ cho rằng mắt người cũng giữ thăng bằng như cơ thể. Nhìn vào một căn phòng, mắt thấy món đồ này nặng, món kia nhẹ. Hai tác giả cũng cho rằng đối xứng là cách giữ thăng bằng mà mắt nhận ra nhanh nhất. Theo tụi mình, hai bên đã giống hệt nhau thì mắt không phải so bên nào nặng hơn, nên dừng ở trục giữa và thấy yên.
<break time="1.2s" />
Phòng ngủ chính của căn hộ Pan-mây-ra tại Lít-bon, do Xtu-đi-ô Ga-mây-rô cải tạo, được kê đúng theo trục giữa ấy. Giường nằm giữa một tấm đầu giường bằng gỗ chạm tay, hai bên là hai đèn thả giống nhau, cách đều trục. Phòng tắm ngay bên cạnh cũng đối xứng, nhưng chỉ ở hai vòi sen trong vách kính, còn chậu rửa và bồn vệ sinh bên ngoài thì đặt lệch, chỗ nào tiện dùng thì đặt ở đó.
<break time="1.2s" />
Tụi mình thấy cái khéo của căn hộ là chỉ kê đối xứng ở chỗ nằm nghỉ và chỗ đứng tắm, còn phòng khách thì kê lệch. Chính Kin-mơ cũng nhắc rằng dùng đối xứng quá nhiều sẽ làm căn phòng tĩnh và buồn tẻ. Vì vậy, phòng ngủ nên giữ đối xứng ở đầu giường, chỗ người ta cần yên khi nằm nghỉ, còn các phòng khác thì không cần. Bài phân tích đầy đủ về cân bằng thị giác khi bày biện nội thất, mọi người xem ở phần bình luận nhé.
```

## Phiên âm cho ElevenLabs
| Chính tả gốc | Phiên âm |
|---|---|
| Kilmer | Kin-mơ |
| Palmeira | Pan-mây-ra |
| Lisbon | Lít-bon |
| Studio Gameiro | Xtu-đi-ô Ga-mây-rô |
| 2014 | hai nghìn không trăm mười bốn |

## Ba điều người xem học được
1. Mắt giữ thăng bằng như cơ thể, thấy món nặng món nhẹ; đối xứng là cách giữ thăng bằng mắt nhận ra nhanh nhất, vì hai bên giống nhau nên mắt không phải so mà dừng ở trục giữa và thấy yên.
2. Ở Palmeira, đối xứng chỉ có ở đầu giường (tấm gỗ chạm tay dài hơn giường, hai đèn thả cách đều trục) và trong vách tắm (hai vòi sen); ngoài vách, chậu rửa và bồn đặt theo chỗ tiện dùng.
3. Kilmer nhắc dùng đối xứng quá nhiều làm phòng tĩnh và buồn tẻ, nên chỉ giữ đối xứng ở đầu giường, các phòng khác không cần.
Không trùng các tập trước (bài 04 chưa dùng). Để dành cho tập làm bài học 3: ý "kê đối xứng chặt chẽ chỉ có tác dụng khi người ta đứng trên trục" (không dùng ở đây); tập đó không lặp nhận xét "hai đèn thả cách đều trục".

## Hình
- Một diagram (01, hàng ba kiểu rồi khung đối xứng), mặt bằng (03), ba không gian (phòng ngủ chính, phòng tắm chính, phòng khách). Ảnh 04 ở 4/13 cảnh.
- Doodle gốc của bài 04 vẽ mực đen, nhãn sát mép ảnh, nên dùng ảnh gốc sạch `anh/goc/` và vẽ nét trắng nét đứt mới bằng `draw_ep12.py`, theo đúng chỗ khoanh và nhãn của bài. Mọi cảnh ảnh chụp ở phần C, D, F (cảnh 7–10, 12) có nét; cảnh móc, cảnh 11 (phần E) và khung cuối để ảnh sạch.
- Camera: push, pan_u, hold, pull xen kẽ; hai cảnh liền nhau không cùng kiểu; đổi ảnh bằng hoà tan; không zoom từ toàn cảnh vào chi tiết. Engine khung (10 run): không còn dòng LỖI hay CẢNH BÁO vùng an toàn chữ.

## Lượt chấm độc lập
- Lượt 1 (bản 2, 290 từ): câu M KHÔNG ĐẠT. Câu móc nói phòng tắm kê lệch (sai bài, mâu thuẫn câu sau); "yên", "trục giữa" không được dùng tiếp; câu diễn giải của bài nghe như lời Kilmer; "Vì vậy" ở câu chốt sai quan hệ; câu chốt chưa trả lời vế "phòng khác thì không"; "chỉ dành đối xứng cho" là lối dịch. Đã viết lại cả bốn khối. Không theo một đề xuất của người chấm (dùng ý "đối xứng chỉ có tác dụng khi đứng trên trục"), vì đó là bài học 3; vế "phòng khác thì không" trả lời bằng cảnh báo của Kilmer trong chính bài học 1. Người chấm đồng ý ở lượt 2.
- Lượt 2 (bản 3): câu M ĐẠT, sâu và dễ hiểu đạt, không dấu hai chấm. Bốn việc bắt buộc, đã sửa hết: câu chốt đưa chữ "yên" trở lại, bỏ lối bị động "đối xứng nên giữ cho"; câu 4 đổi "Theo hai tác giả" thành "Hai tác giả cũng cho rằng" để không hai câu liền nhau cùng mở bằng "Theo"; câu 10 đổi thành "Tụi mình thấy…"; câu phòng tắm đổi thành "cũng đối xứng, nhưng chỉ ở hai vòi sen trong vách kính". Theo hai gợi ý: tiêu đề cảnh 6 có thông tin, cảnh 11 (cảnh báo của Kilmer) đặt trên ảnh phòng khách.
- Sửa thêm sau lượt 2: câu 2 rút cho vừa ba dòng phụ đề.
- Lượt 3: câu M, câu 6 và chín điểm 0.6f đạt. Một việc bắt buộc, đã sửa: câu 2 "cuốn sách về thiết kế nội thất năm 2014" dễ nghe thành "nội thất của năm 2014", viết lại thành "Trong một cuốn sách năm 2014 về thiết kế nội thất, hai tác giả Kilmer cho rằng mắt người cũng giữ thăng bằng như cơ thể." Người chấm xác nhận sửa xong câu này thì không cần thêm lượt. Phụ đề cảnh 5, 10, 12 (26–27 từ) vẫn vừa ba dòng trên khung đã dựng.

## Tự kiểm
- Lời, tiêu đề, nhãn: không dấu hai chấm (trừ dòng nguồn ảnh), không tiếng Anh trong bản đọc, gọi "mọi người", xưng "tụi mình", rào "theo tụi mình" một lần mỗi khối diễn giải.
- Nguồn Kilmer & Kilmer (2014) hiện trên tiêu đề cảnh 2, 3, 11 và dòng nguồn sơ đồ cảnh 2–5.

## Cần kiểm tra
- Dòng nguồn mặt bằng ghi "ArchDaily (2023)" theo chú thích trên bản vẽ của bài.
- Chữ chú thích trên mặt bằng hơi nhỏ trên điện thoại (khoảng 26–28 px), vì giữ cả cột chú thích lẫn phòng ngủ, phòng tắm.
- Bình luận ghim giữ câu "dành cho thành viên … Buy Me a Coffee" như tập 11; chủ Trang dán link.

## Giai đoạn B: căn cảnh theo ghi âm doi-xung-dau-giuong.mp3
- File: 69,64 giây, mp3 44,1 kHz mono (ElevenLabs, giọng Tony Hoang, `ElevenLabs_2026-10-26T13_31_43_Tony_Hoang__pvc_sp100_s50_sb75_v4.mp3`).
- Không nhận dạng lại được lời: lệnh cài sherpa-onnx và tải mô hình `sherpa-onnx-zipformer-vi-2025-04-20` từ GitHub bị môi trường chặn (lý do "mã tải từ bên ngoài"), máy không có công cụ nhận dạng giọng nào khác. Vì vậy câu được ghép vào đoạn nói theo độ dài (chế độ ghép cụm câu của prompt): silencedetect −35 dB / 0,25 giây cho 27 đoạn nói; đếm đỉnh năng lượng âm tiết trong từng đoạn (240 đỉnh cho 283 tiếng bản đọc, tỷ lệ 0,85), rồi đặt mỗi ranh giới cảnh ở quãng lặng gần nhất với số tiếng lũy kế của kịch bản. Cả 12 ranh giới rơi đúng một quãng lặng, lệch không quá 3 tiếng, nên lời thu khớp kịch bản về độ dài từng câu; phụ đề giữ nguyên chữ của kịch bản. Nếu chủ Trang có đổi chữ khi thu mà không đổi độ dài câu thì cách này không phát hiện được.
- ElevenLabs rút thẻ ngắt 1,2 giây còn 0,47–0,71 giây. Mỗi cảnh bắt đầu khoảng 0,37 giây trước câu của nó; cảnh cuối kéo đến hết giọng + 0,6 giây (`T_AUDIO` trong gen_ep12.py).

| Cảnh | Bắt đầu cảnh (giây) | Đoạn nói (giây) | Đỉnh âm tiết đếm được / tiếng bản đọc × 0,85 |
|---|---|---|---|
| 1 | 0 | 0,00–5,94 | 15 / 16 |
| 2 | 6,04 | 6,41–15,94 | 30 / 26 |
| 3 | 16,02 | 16,39–19,53 | 11 / 12 |
| 4 | 19,70 | 20,07–23,66 | 15 / 16 |
| 5 | 23,83 | 24,20–28,79 | 19 / 22 |
| 6 | 28,87 | 29,24–34,89 | 19 / 18 |
| 7 | 34,99 | 35,36–40,29 | 20 / 19 |
| 8 | 40,41 | 40,78–44,13 | 14 / 14 |
| 9 | 44,12 | 44,49–48,16 | 14 / 17 |
| 10 | 48,15 | 48,52–54,74 | 28 / 23 |
| 11 | 54,67 | 55,04–59,18 | 15 / 15 |
| 12 | 59,29 | 59,66–65,01 | 22 / 22 |
| 13 | 65,07 | 65,44–69,32 | 18 / 20 |

Âm thanh: lọc dưới 80 Hz, giảm ồn nhẹ (afftdn nf −30), tăng 6,5 dB, chặn đỉnh (alimiter 0,76); đo bằng ebur128 trên file đã xử lý: −14,6 LUFS, đỉnh −1,8 dBFS; 48 kHz; không nhạc.
