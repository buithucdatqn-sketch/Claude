"""Tập 7: Ánh sáng từ trên cao (bài 03 kho AH-Decode-Decor). Ba ảnh của bài: ảnh chụp 07 (nền = ảnh gốc anh/goc/07,
nét = doodle gốc tách bằng hiệu hai ảnh), sơ đồ 05 (cửa ngang tầm mắt / cửa sát trần), mặt cắt dọc 04.
Sinh engine_ep07.py + engine_video_ep07.py từ engine v8 (nhiều ảnh nguồn), và script.md/elevenlabs.txt từ cùng dữ liệu cảnh."""
import json
import re

E = "/home/user/Claude/engine/"
OUT = "/home/user/Claude/inbox/out/2026-10-21_anh-sang-tu-tren-cao/"
WPS = 3.2      # tốc độ đọc dự kiến (từ/giây)
TRANS = 0.7

CREDITS = dict(
    main="Ảnh dự án: Union Street House, Northcote, Melbourne · Prior Barraclough · ảnh Ben Hosking",
    sodo="Sơ đồ: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014)",
    catdoc="Mặt cắt dọc: bản vẽ Prior Barraclough, nguồn ArchDaily (2023)",
)
WIDE = ("C", 1.0, (540, 940))
COVER = ("cover", 540, 900)
SC = [
    dict(part="A", img="main", head="Mở kính lớn, vẫn bật đèn ban ngày?", cam=WIDE, dark=False, dd=[],
         vo="Nhà phố mở kính thật lớn, mà ba giờ chiều vẫn phải bật đèn. Lạ không?"),
    dict(part="B", img="main", head="Kilmer & Kilmer (2014), Designing Interiors", cam=((600, 700), 2.1, COVER), dark=False, dd=[],
         vo="Hai tác giả Kilmer nói, vị trí ô cửa quyết định ánh sáng vào sâu tới đâu.",
         tts="Hai tác giả Kin-mơ nói, vị trí ô cửa quyết định ánh sáng vào sâu tới đâu."),
    dict(part="C", img="sodo", head="Kính ngang tầm mắt: nắng gắt, trời chói", cam=((540, 1300), 1.35, ("top", 520)), dark=False, dd=[],
         vo="Kính ngang tầm mắt đưa nắng gắt vào sát cửa, lại đặt mảng trời chói ngay trước mắt. Thế là kéo rèm."),
    dict(part="C", img="sodo", head="Cửa sát trần: ánh sáng chạm trần trước", cam=((1620, 1300), 1.35, ("top", 520)), dark=False, dd=[],
         vo="Cửa sát trần thì ánh sáng chạm trần và tường trước, tới mắt đã dịu."),
    dict(part="E", img="catdoc", head="Mặt cắt: ô kính cao ở đầu hồi", cam=((900, 875), 1.2, ("top", 520)), dark=False, dd=[],
         vo="Nhà Union Street của Prior Barraclough ở Melbourne kín hai bên hông. Họ kéo mái cao dần, mở ô kính sát mái ở đầu hồi.",
         tts="Nhà Diu-ni-ơn Xtrít của Prai-ơ Ba-ra-clo ở Meo-bơn kín hai bên hông. Họ kéo mái cao dần, mở ô kính sát mái ở đầu hồi."),
    dict(part="E", img="main", head="Ô kính cao sát mái, dưới là vách lam", cam=((620, 850), 2.1, COVER), dark=True, dd=["arr_kinh", "lab_kinh", "arr_lam", "lab_lam"],
         vo="Nhìn từ bàn ăn, ngay dưới ô kính là vách lam gỗ của gác lửng."),
    dict(part="E", img="lam", head="Qua lam, ánh sáng in vệt lên tường gỗ", cam=((800, 900), 1.5, ("top", 540)), dark=True, dd=["arr_lam6", "lab_lam6", "arr_vet", "lab_vet"],
         vo="Từ cầu thang, ánh sáng qua lam in thành vệt trên tường gỗ, không rơi thẳng xuống người."),
    dict(part="E", img="main", head="Trần gỗ sáng dần về phía ô kính", cam=((800, 600), 1.5, ("top", 540)), dark=True, dd=["arr_tran", "lab_tran"],
         vo="Quay lại bàn ăn, trần gỗ sáng dần về phía ô kính,"),
    dict(part="E", img="main", head="Mặt bàn không có vệt nắng nào", cam=((800, 1300), 1.6, ("top", -184)), dark=True, dd=["arr_ban"],
         vo="còn mặt bàn không có vệt nắng nào."),
    dict(part="H", img="main", head="Chốt lại", cam=WIDE, dark=False, dd=[],
         vo="Nhà sáng không nhờ nhiều kính, mà nhờ ánh sáng chạm vào đâu trước khi tới mắt. Bài phân tích đầy đủ cho thành viên ở phần bình luận nha."),
    dict(part="I", img="main", head="end", cam=("C", 0.8, (540, 600)), dark=False, vo="", dd=[],
         tts="Ây-ết Đi-cốt, series về nguyên tắc thiết kế và chọn đồ đê-co. Theo dõi Giả Thuyết Kiến Trúc. Bài viết phân tích đầy đủ xem ở dòng đầu tiên trong phần bình luận.",
         say="AH Decode, series về nguyên tắc thiết kế và chọn đồ decor. Theo dõi Giả Thuyết Kiến Trúc. Bài viết phân tích đầy đủ xem ở dòng đầu tiên trong phần bình luận."),
]

DOODLE = r'''
_L = np.load(os.path.join(HERE, "doodle_ep07.npz"))
LAYER = {k: _L[k] for k in _L.files}   # toạ độ trên ảnh làm việc 1600x2400 của ảnh mà cảnh dùng (khoá *6/vet: ảnh "lam")
RAD = dict(arr_tran=0.8, arr_lam=0.8, arr_kinh=0.8, arr_ban=0.8, arr_lam6=0.8, arr_vet=0.8)   # bán kính nét gốc (px ảnh làm việc)


def _stamp(wb, pts, r_src):
    """lộ lại nét doodle gốc theo đúng thứ tự vẽ (mỗi điểm là một chấm bút)"""
    rr = max(1, int(round(r_src * wb.v.s * SS)))
    for p in pts:
        x, y = wb.v.pt((float(p[0]), float(p[1])))
        if hasattr(wb, "circ"):
            wb.circ.append((int(x * SS), int(y * SS), rr))
        else:
            cv2.circle(wb.m, (int(x * SS), int(y * SS)), rr, 255, -1, cv2.LINE_AA)


def _label(text, cam, pts):
    """nhãn chữ viết tay gốc của bài, đưa vào lớp nhãn (hiện khi nét đạt 55-75%)"""
    r = max(0.55, 0.62 * cam.s)
    for p in pts:
        x, y = cam.pt((float(p[0]), float(p[1])))
        text.d.ellipse((x - r, y - r, x + r, y + r), fill=255)


def doodle(i, wb, text, cam):
    for k in SCENES[i].get("dd", []):
        if k.startswith("lab"):
            _label(text, cam, LAYER[k])
        else:
            _stamp(wb, LAYER[k], RAD[k])
'''


def words(s):
    return len(s.split())


def build_data():
    t = 0.0
    scenes = []
    for s in SC:
        spoken = s.get("tts", s["vo"])
        dur = max(3.5, TRANS + words(spoken) / WPS)
        if s["head"] == "end":
            dur = max(dur, 7.0)
        a, b = round(t, 1), round(t + dur, 1)
        t = b
        s["t"] = f"{a:g}–{b:g}s"
        s["dur"] = b - a
        scenes.append(f'    dict(t="{s["t"]}", img="{s["img"]}", head={json.dumps(s["head"], ensure_ascii=False)}, '
                      f'vo={json.dumps(s["vo"], ensure_ascii=False)},\n         cam={s["cam"]!r}, dark={s["dark"]}, dd={s["dd"]}),')
    photos = (f'PHOTOS["main"].credit = {CREDITS["main"]!r}\n'
              f'PHOTOS["lam"] = Photo(os.path.join(HERE, "..", "source_lam.png"), credit={CREDITS["main"]!r})\n'
              f'PHOTOS["sodo"] = Photo(os.path.join(HERE, "..", "source_sodo.png"), 1200, 1810.0, credit={CREDITS["sodo"]!r})\n'
              f'PHOTOS["catdoc"] = Photo(os.path.join(HERE, "..", "source_catdoc.png"), 1920, 1810.0, credit={CREDITS["catdoc"]!r})\n')
    data = ('# ---------------- scenes ----------------\nCENTER = (SW / 2, SH / 2)\nOBJ = {}\n' + photos +
            '\nSCENES = [\n' + "\n".join(scenes) + '\n]\nEND = len(SCENES) - 1\nBOARDS = {}\n' + DOODLE + '\n\n')
    return data, t


def build(src, dst, video, data):
    s = open(E + src).read()
    rep = [('CREDIT = "Ảnh dự án: [tên dự án] · [studio] · [nhiếp ảnh gia]"', f'CREDIT = {CREDITS["main"]!r}'),
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · ÁNH SÁNG TỪ TRÊN CAO"'),
           ("CARD_W2, BORDER2 = 1920, 0", "CARD_W2, BORDER2 = 1320, 0  # ảnh chính dọc 2:3: thẻ hẹp hơn để chữ nằm ngoài ảnh"),
           ("C2 = (B2W / 2, 1810.0)", "C2 = (B2W / 2, 1880.0)"),
           ("borderMode=cv2.BORDER_REFLECT)", "borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255, 0))")]
    for a_, b_ in rep:
        assert a_ in s, a_
        s = s.replace(a_, b_)
    a = s.index("# ---------------- scenes")
    b = s.index("# ---------------- render ----------------")
    s = s[:a] + data + s[b:]
    if video:
        s = s.replace('"reel1_silent.mp4"', '"reel_anh-sang-tu-tren-cao_silent.mp4"')
    else:
        s = s.replace('"frames_v7"', '"frames"').replace('"storyboard_reel1_v7.png"', '"storyboard.png"')
        s = s.replace("AH Decode · Cân bằng thị giác — bảng phân cảnh v7", "AH Decode · Ánh sáng từ trên cao")
        s = s.replace("Ảnh dán bằng băng giấy ở giữa mép trên · không viền · nền trắng trơn · chữ nâu đậm trên nền, trắng trên ảnh",
                      "Hai ảnh chụp 07, 06 + sơ đồ 05 + mặt cắt 04 · nền trắng · chữ nâu trên nền, trắng trên ảnh")
        s = s.replace("Camera zoom vào ảnh khi nói đến chi tiết · ~28 giây · nét vẽ chạy animation theo nhịp lời đọc",
                      "Camera zoom vào chi tiết · nét doodle gốc của bài lộ dần theo lời đọc · đổi ảnh = mờ chéo 0,7 giây")
        s = s.replace("Ảnh tối ~14% ở cảnh có nét vẽ; cảnh 1, 6, 7 giữ ảnh nguyên bản.",
                      "Ảnh tối ~14% ở cảnh có nét vẽ (cảnh 6–9); các cảnh khác giữ ảnh nguyên bản.")
    open(OUT + "engine_ep07/" + dst, "w").write(s)


data, total = build_data()
build("engine_storyboard_v8.py", "engine_ep07.py", False, data)
build("engine_video_v8.py", "engine_video_ep07.py", True, data)

# ---- script.md + elevenlabs.txt ----
NAMES = dict(A="Mở", B="Nguồn gốc", C="Cơ chế", D="Đọc trên ảnh", E="Ví dụ công trình", F="Áp dụng",
             G="Chọn đồ", H="Chốt", I="Cảnh cuối")
IMGN = dict(main="ảnh chụp 07 (bàn ăn, ô kính cao)", lam="ảnh chụp 06 (vách lam, tường cầu thang)", sodo="sơ đồ 05 (cửa thấp / cửa cao)", catdoc="mặt cắt dọc 04")
shown = [s.get("say", s["vo"]) for s in SC]
spoken_all = [s.get("tts", s["vo"]) for s in SC]
nw = sum(words(x) for x in shown)
rows = []
for k, s in enumerate(SC):
    head = "(khung cuối cố định)" if s["head"] == "end" else s["head"]
    cam = "rộng" if s["cam"] == WIDE else ("khung cuối" if s["part"] == "I" else f"zoom {s['cam'][1]}× vào {s['cam'][0]}")
    dd = ", ".join(s["dd"]) or "không nét"
    rows.append(f'| {k + 1} | {s["t"]} | {s["part"]} · {NAMES[s["part"]]} | {IMGN[s["img"]]} | {head} | {shown[k]} | {cam}; {dd} |')
md = (f"# AH Decode · Ánh sáng từ trên cao · BẢN NHÁP chờ duyệt\n\n"
      f"Bài trong kho: `AH-Decode-Decor/bai-03-3-bai-hoc-anh-sang-tu-nhien-noi-that/bai-03.md` (commit dad48a5), ý chính: mục \"Ánh sáng đi vào từ trên cao sẽ vào sâu và dịu hơn ánh sáng từ ô cửa ngang tầm mắt\".\n"
      f"Ảnh chụp: `anh/07-doodle-cua-cao-ban-an.jpg` (nền `anh/goc/07-…`), `anh/06-doodle-vach-lam-cau-thang.jpg` (nền `anh/goc/06-…`); bản vẽ: `anh/05-diagram-cua-thap-cua-cao.png`, `anh/04-mat-cat-doc-union-street.png` · Union Street House, Northcote, Melbourne · Prior Barraclough · ảnh Ben Hosking\n"
      f"Thời lượng dự kiến: {total:.1f} giây + 1 giây giữ khung cuối · {nw} từ lời đọc (chữ viết) · {len(SC)} cảnh.\n"
      f"Nét: chỉ dùng doodle gốc của ảnh 07 (bốn mũi tên, ba nhãn) và ảnh 06 (hai mũi tên, nhãn \"vách lam gỗ của gác lửng, phía sau là ô kính sáng\", \"vệt sáng in lên tường gỗ cầu thang\"), lộ dần; không vẽ nét mới. Sơ đồ và mặt cắt giữ nguyên nhãn có sẵn, không thêm nét.\n\n"
      "| # | Thời lượng | Phần | Ảnh | Tiêu đề trên khung | Lời đọc | Hình |\n|---|---|---|---|---|---|---|\n" + "\n".join(rows) +
      "\n\n## Lời đọc liền mạch\n\n" + " ".join(shown) + "\n\n"
      "## Phiên âm cho ElevenLabs\n\n| Chính tả gốc | Phiên âm |\n|---|---|\n"
      "| Kilmer | Kin-mơ |\n| Union Street | Diu-ni-ơn Xtrít |\n| Prior Barraclough | Prai-ơ Ba-ra-clo |\n| Melbourne | Meo-bơn |\n"
      "| AH Decode | Ây-ết Đi-cốt |\n| decor | đê-co |\n")
open(OUT + "script.md", "w").write(md)
el = '\n<break time="1.2s" />\n'.join(x.strip() for x in spoken_all)
el += "\n\n---\n--- Gợi ý cài đặt: giọng nữ hoặc nam trầm ấm, tốc độ 1.0, mô hình đa ngôn ngữ, ngôn ngữ Vietnamese ---\n"
open(OUT + "elevenlabs.txt", "w").write(el)
print("total", round(total, 1), "words", nw)
for s in SC:
    print(s["t"], words(s.get("say", s["vo"])), s["img"], s["head"])
