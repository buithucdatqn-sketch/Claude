"""Tập 7: Bề mặt hắt sáng (bài 03 kho AH-Decode-Decor, bài học 2). Hai ảnh chụp 11 và 10 (nền = ảnh gốc anh/goc/,
nét = doodle gốc tách bằng hiệu hai ảnh), sơ đồ 01, sơ đồ 09, mặt bằng tầng trệt 02.
Sinh engine_ep07.py + engine_video_ep07.py từ engine v8 (nhiều ảnh nguồn), và script.md/elevenlabs.txt từ cùng dữ liệu cảnh."""
import json
import re

E = "/home/user/Claude/engine/"
OUT = "/home/user/Claude/inbox/out/2026-10-21_be-mat-hat-sang/"
WPS = 3.2      # tốc độ đọc dự kiến (từ/giây)
TRANS = 0.7

CREDITS = dict(
    main="Ảnh dự án: Union Street House, Northcote, Melbourne · Prior Barraclough · ảnh Ben Hosking",
    sodo="Sơ đồ: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014)",
    mb="Mặt bằng tầng trệt: bản vẽ Prior Barraclough, nguồn ArchDaily (2023)",
)
WIDE = ("C", 1.0, (540, 940))
COVER = ("cover", 540, 900)
SC = [
    dict(part="A", img="main", head="Sao phòng gỗ tối hơn?", cam=WIDE, dark=False, dd=[],
         vo="Cùng một ô cửa, sao phòng sơn trắng sáng hẳn, còn phòng ốp gỗ lại tối?"),
    dict(part="B", img="sodo1", head="Kilmer & Kilmer (2014): ánh sáng hắt lại", cam=("C", 1.25, ("top", 520)), dark=False, dd=[],
         vo="Theo hai tác giả Kilmer, mắt chỉ thấy ánh sáng do bề mặt hắt lại. Tường trắng mờ hắt nhiều, gỗ sẫm nuốt bớt.",
         tts="Theo hai tác giả Kin-mơ, mắt chỉ thấy ánh sáng do bề mặt hắt lại. Tường trắng mờ hắt nhiều, gỗ sẫm nuốt bớt."),
    dict(part="C", img="sodo9", head="Trần sáng nhất, sàn tối nhất", cam=("C", 1.25, ("top", 520)), dark=False, dd=[],
         vo="Nên trần cần sáng nhất, rồi tới tường, mặt bàn, sàn. Mặt mờ cho ánh sáng tỏa đều."),
    dict(part="C", img="sodo9", head="Gạch bóng kính: vệt nắng chói", cam=("C", 1.25, ("top", 520)), dark=False, dd=[],
         vo="Nhà phố hay lát gạch bóng kính cho dễ lau, rồi trên sàn hiện vệt nắng chói."),
    dict(part="E", img="mb", head="Union Street House: ốp gỗ gần hết", cam=("C", 1.15, ("top", 520)), dark=False, dd=[],
         vo="Nhà Union Street của Prior Barraclough ở Melbourne lại ốp gỗ gần hết, tường, trần lẫn đồ.",
         tts="Nhà Diu-ni-ơn Xtrít của Prai-ơ Ba-ra-clo ở Meo-bơn lại ốp gỗ gần hết, tường, trần lẫn đồ."),
    dict(part="E", img="mb", head="Gỗ hắt ít, bù bằng kính hai đầu", cam=("C", 1.15, ("top", 520)), dark=False, dd=[],
         vo="Gỗ hắt ít sáng hơn tường trắng, nên họ bù bằng kính ở hai đầu nhà."),
    dict(part="E", img="main", head="Gỗ mờ: không có điểm chói", cam=((850, 1000), 1.7, ("top", 400)), dark=True, dd=["arr_lam", "lab_lam", "lab_cauthang"],
         vo="Ánh sáng qua vách lam chuyển đều trên tường và mặt dưới cầu thang. Không có điểm chói nào."),
    dict(part="E", img="inox", head="Bếp đổi hẳn: hốc inox bóng", cam=((800, 900), 1.7, ("top", 540)), dark=True, dd=["arr_inox", "lab_inox", "arr_go", "lab_go"],
         vo="Bếp, chỗ cần sáng nhất, thì đổi hẳn. Hốc bếp bọc inox bóng, phản chiếu cả ánh sáng lẫn đồ vật."),
    dict(part="E", img="inox", head="Giấu trong hốc hẹp", cam=((760, 750), 2.1, COVER), dark=False, dd=[],
         vo="Mặt bóng giấu trong hốc hẹp, nên chỗ nấu sáng lên mà không chói ra phòng."),
    dict(part="H", img="main", head="Chốt lại", cam=WIDE, dark=False, dd=[],
         vo="Phòng sáng tới đâu, do bề mặt đầu tiên ánh sáng chạm vào. Bài phân tích đầy đủ cho thành viên ở phần bình luận nha."),
    dict(part="I", img="main", head="end", cam=("C", 0.8, (540, 600)), dark=False, vo="", dd=[],
         tts="Ây-ết Đi-cốt, series về nguyên tắc thiết kế và chọn đồ đê-co. Theo dõi Giả Thuyết Kiến Trúc. Bài viết phân tích đầy đủ xem ở dòng đầu tiên trong phần bình luận.",
         say="AH Decode, series về nguyên tắc thiết kế và chọn đồ decor. Theo dõi Giả Thuyết Kiến Trúc. Bài viết phân tích đầy đủ xem ở dòng đầu tiên trong phần bình luận."),
]

DOODLE = r'''
_L = np.load(os.path.join(HERE, "doodle_ep07.npz"))
LAYER = {k: _L[k] for k in _L.files}   # toạ độ trên ảnh làm việc 1600x2400 của ảnh mà cảnh dùng (arr/lab_inox, arr/lab_go: ảnh "inox"; còn lại: ảnh "main")
RAD = dict(arr_lam=0.8, arr_san=0.8, arr_inox=0.8, arr_go=0.8)   # bán kính nét gốc (px ảnh làm việc)


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


# Mốc cảnh theo giọng đọc bai-03 (inbox/audio/be-mat-hat-sang.mp3, 54,75 giây): mỗi cảnh bắt đầu 0,4 giây trước câu của nó
# (ranh giới câu lấy từ silencedetect -35 dB / 0,12 s, ghép cụm câu theo số tiếng); cảnh cuối kéo quá giọng đọc 0,75 giây.
TIMES = [0.0, 4.49, 11.2, 16.94, 21.37, 27.34, 31.28, 36.14, 42.14, 46.08, 51.8, 55.5]


def build_data():
    t = 0.0
    scenes = []
    for k, s in enumerate(SC):
        a, b = TIMES[k], TIMES[k + 1]
        t = b
        s["t"] = f"{a:g}–{b:g}s"
        s["dur"] = b - a
        scenes.append(f'    dict(t="{s["t"]}", img="{s["img"]}", head={json.dumps(s["head"], ensure_ascii=False)}, '
                      f'vo={json.dumps(s["vo"], ensure_ascii=False)},\n         cam={s["cam"]!r}, dark={s["dark"]}, dd={s["dd"]}),')
    photos = (f'PHOTOS["main"].credit = {CREDITS["main"]!r}\n'
              f'PHOTOS["inox"] = Photo(os.path.join(HERE, "..", "source_inox.png"), credit={CREDITS["main"]!r})\n'
              f'PHOTOS["sodo1"] = Photo(os.path.join(HERE, "..", "source_sodo1.png"), 1200, 1810.0, credit={CREDITS["sodo"]!r})\n'
              f'PHOTOS["sodo9"] = Photo(os.path.join(HERE, "..", "source_sodo9.png"), 1200, 1810.0, credit={CREDITS["sodo"]!r})\n'
              f'PHOTOS["mb"] = Photo(os.path.join(HERE, "..", "source_mb.png"), 1400, 1810.0, credit={CREDITS["mb"]!r})\n')
    data = ('# ---------------- scenes ----------------\nCENTER = (SW / 2, SH / 2)\nOBJ = {}\n' + photos +
            '\nSCENES = [\n' + "\n".join(scenes) + '\n]\nEND = len(SCENES) - 1\nBOARDS = {}\n' + DOODLE + '\n\n')
    return data, t


def build(src, dst, video, data):
    s = open(E + src).read()
    rep = [('CREDIT = "Ảnh dự án: [tên dự án] · [studio] · [nhiếp ảnh gia]"', f'CREDIT = {CREDITS["main"]!r}'),
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · BỀ MẶT HẮT SÁNG"'),
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
        s = s.replace('"reel1_silent.mp4"', '"reel_be-mat-hat-sang_silent.mp4"')
    else:
        s = s.replace('"frames_v7"', '"frames"').replace('"storyboard_reel1_v7.png"', '"storyboard.png"')
        s = s.replace("AH Decode · Cân bằng thị giác — bảng phân cảnh v7", "AH Decode · Bề mặt hắt sáng")
        s = s.replace("Ảnh dán bằng băng giấy ở giữa mép trên · không viền · nền trắng trơn · chữ nâu đậm trên nền, trắng trên ảnh",
                      "Hai ảnh chụp 11, 10 + sơ đồ 01, 09 + mặt bằng 02 · nền trắng · chữ nâu trên nền, trắng trên ảnh")
        s = s.replace("Camera zoom vào ảnh khi nói đến chi tiết · ~28 giây · nét vẽ chạy animation theo nhịp lời đọc",
                      "Camera zoom vào chi tiết · nét doodle gốc của bài lộ dần theo lời đọc · đổi ảnh = mờ chéo 0,7 giây")
        s = s.replace("Ảnh tối ~14% ở cảnh có nét vẽ; cảnh 1, 6, 7 giữ ảnh nguyên bản.",
                      "Ảnh tối ~14% ở cảnh có nét vẽ (cảnh 7, 8); các cảnh khác giữ ảnh nguyên bản.")
    open(OUT + "engine_ep07/" + dst, "w").write(s)


data, total = build_data()
build("engine_storyboard_v8.py", "engine_ep07.py", False, data)
build("engine_video_v8.py", "engine_video_ep07.py", True, data)

# ---- script.md + elevenlabs.txt ----
NAMES = dict(A="Mở", B="Nguồn gốc", C="Cơ chế", D="Đọc trên ảnh", E="Ví dụ công trình", F="Áp dụng",
             G="Chọn đồ", H="Chốt", I="Cảnh cuối")
IMGN = dict(main="ảnh chụp 11 (gỗ mờ, cầu thang)", inox="ảnh chụp 10 (hốc bếp inox)", sodo1="sơ đồ 01 (bề mặt hắt sáng)", sodo9="sơ đồ 09 (thang phản xạ)", mb="mặt bằng tầng trệt 02")
shown = [s.get("say", s["vo"]) for s in SC]
spoken_all = [s.get("tts", s["vo"]) for s in SC]
nw = sum(words(x) for x in shown)
rows = []
for k, s in enumerate(SC):
    head = "(khung cuối cố định)" if s["head"] == "end" else s["head"]
    cam = "rộng" if s["cam"] == WIDE else ("khung cuối" if s["part"] == "I" else f"zoom {s['cam'][1]}× vào {s['cam'][0]}")
    dd = ", ".join(s["dd"]) or "không nét"
    rows.append(f'| {k + 1} | {s["t"]} | {s["part"]} · {NAMES[s["part"]]} | {IMGN[s["img"]]} | {head} | {shown[k]} | {cam}; {dd} |')
md = (f"# AH Decode · Bề mặt hắt sáng · BẢN NHÁP chờ duyệt\n\n"
      f"Bài trong kho: `AH-Decode-Decor/bai-03-3-bai-hoc-anh-sang-tu-nhien-noi-that/bai-03.md` (commit dad48a5), ý chính: mục \"Bề mặt đón ánh sáng đầu tiên quyết định căn phòng sáng tới đâu\".\n"
      f"Ảnh chụp: `anh/11-doodle-go-mo-gam-cau-thang.jpg`, `anh/10-doodle-go-mo-inox-bong.jpg` (nền: ảnh gốc cùng số trong `anh/goc/`); bản vẽ: `anh/01-diagram-be-mat-hat-sang.png`, `anh/09-diagram-thang-phan-xa.png`, `anh/02-mat-bang-tang-tret-union-street.png` · Union Street House, Northcote, Melbourne · Prior Barraclough · ảnh Ben Hosking\n"
      f"Thời lượng dự kiến: {total:.1f} giây + 1 giây giữ khung cuối · {nw} từ lời đọc (chữ viết) · {len(SC)} cảnh.\n"
      f"Nét: chỉ dùng doodle gốc của ảnh 11 (mũi tên và nhãn \"vách lam gác lửng, chỗ ánh sáng vào\", \"mặt dưới cầu thang, sáng chuyển đều\") và ảnh 10 (hai mũi tên, nhãn \"hốc inox phản chiếu đồ vật và ánh sáng\", \"tường gỗ mờ, không có điểm chói\"), lộ dần; không vẽ nét mới. Sơ đồ và mặt bằng giữ nguyên nhãn có sẵn.\n\n"
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
