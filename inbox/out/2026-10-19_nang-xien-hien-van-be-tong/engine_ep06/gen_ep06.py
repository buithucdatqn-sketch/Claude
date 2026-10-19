"""Tập 6: Nắng xiên hiện vân bê tông (bài 02 kho AH-Decode-Decor, ảnh 04 có doodle sẵn).
Sinh engine_ep06.py + engine_video_ep06.py từ hai engine gốc, và script.md/elevenlabs.txt từ cùng dữ liệu cảnh.
Ảnh dọc (1600x2400): thu nhỏ thẻ ảnh (CARD_W2 1280) và hạ tâm thẻ (C2 y 1880) để tiêu đề và lời đọc nằm ngoài ảnh ở cảnh rộng.
Doodle: không vẽ nét mới; lộ dần chính các nét doodle gốc của bài (doodle_ep06.npz: elip, mũi tên, nhãn chữ) theo mục 2c."""
import json
import re

E = "/home/user/Claude/engine/"
OUT = "/home/user/Claude/inbox/out/2026-10-19_nang-xien-hien-van-be-tong/"
WPS = 3.2      # tốc độ đọc dự kiến (từ/giây)
TRANS = 0.7

WIDE = "WIDE"
SC = [
    dict(part="A", head="Bê tông: ảnh ấm, đời lạnh?", cam=WIDE, dark=False, dd=[],
         vo="Cùng một bức tường bê tông, sao trên ảnh thì ấm mà ngoài đời lại lạnh?"),
    dict(part="B", head="Chất cảm cần ánh xiên (Kilmer & Kilmer, 2014)", cam=((800, 800), 2.2, (540, 900)), dark=False, dd=[],
         vo="Sách Designing Interiors của hai tác giả Kilmer nói chất cảm chỉ hiện rõ khi ánh sáng chiếu xiên.",
         tts="Sách Đi-dai-ninh In-tia-ri-ơ của hai tác giả Kin-mơ nói chất cảm chỉ hiện rõ khi ánh sáng chiếu xiên."),
    dict(part="C", head="Đèn rải đều: tường thành mảng xám", cam=((540, 1250), 2.2, (540, 900)), dark=False, dd=[],
         vo="Tụi mình hay gặp ở nhà phố. Giữ bê tông trần công phu, rồi chiếu bằng lưới đèn âm trần rải đều. Vân chìm mất, chỉ còn mảng xám."),
    dict(part="D", head="Nắng đi xiên, gờ nào cũng đổ bóng", cam=((1250, 700), 2.1, (540, 900)), dark=True, dd=["burst", "dash1", "dash2"],
         vo="Mặt bê tông có vô số gờ nhỏ. Nắng đi xiên thì mỗi gờ đổ một vệt bóng, và mắt nhận ra bề mặt nhám. Ánh sáng chiếu thẳng thì bóng mất, tường phẳng lì."),
    dict(part="E", head="Ban công phòng ngủ chính, Ahmedabad", cam=((640, 1150), 1.8, (540, 900)), free=True, dark=True, dd=["arr1", "lab1", "arr2", "lab2"],
         vo="Ban công phòng ngủ chính trong nhà của Studio Saransh ở Ahmedabad. Chỗ có nắng hiện rõ vệt ván khuôn. Chỗ trong bóng chỉ còn mảng xám phẳng.",
         tts="Ban công phòng ngủ chính trong nhà của Xtu-đi-ô Xa-ran ở A-mê-đa-bát. Chỗ có nắng hiện rõ vệt ván khuôn. Chỗ trong bóng chỉ còn mảng xám phẳng."),
    dict(part="H", head="Cho ánh sáng đi sát mặt tường", cam=WIDE, dark=False, dd=[],
         vo="Vậy muốn tường bê tông bớt lạnh, hãy cho ánh sáng đi sát mặt tường. Gói thành viên có bài phân tích đầy đủ, kèm ba việc làm lại cho nhà phố bê tông trần, ở phần bình luận nha."),
    dict(part="I", head="end", cam="END", dark=False, vo="", dd=[]),
]

DOODLE = r'''
_L = np.load(os.path.join(HERE, "doodle_ep06.npz"))
LAYER = {k: _L[k] for k in _L.files}   # toạ độ trên ảnh làm việc 1600x2400 (source.png)
RAD = dict(arr1=0.8, arr2=0.8, dash1=0.8, dash2=0.8, burst=0.8)         # bán kính nét gốc (px ảnh làm việc)


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


def cover(fx, fy, z, anc, m=40):
    """dời điểm neo để ảnh phủ kín khung 1080x1920 khi zoom (ảnh dọc 1600x2400, 0.4 px khung / px ảnh ở z=1)"""
    sc = z * 0.4
    assert sc * 2400 >= 1920 + 2 * m, z
    ax = min(max(anc[0], 1080 + m - sc * (1600 - fx)), sc * fx - m)
    ay = min(max(anc[1], 1920 + m - sc * (2400 - fy)), sc * fy - m)
    return (round(ax), round(ay))


def words(s):
    return len(s.split())


def build_data():
    t = 0.0
    scenes = []
    for k, s in enumerate(SC):
        spoken = s.get("tts", s["vo"])
        dur = max(3.5, TRANS + words(spoken) / WPS)
        if s["head"] == "end":
            dur = 3.5
        a, b = round(t, 1), round(t + dur, 1)
        t = b
        s["t"] = f"{a:g}–{b:g}s"
        s["dur"] = b - a
        if s["cam"] == WIDE:
            cam = "WIDE"
        elif s["cam"] == "END":
            cam = "(CENTER, 0.8, (540, 600))"
        else:
            (fx, fy), z, anc = s["cam"]
            if not s.get("free"):
                anc = cover(fx, fy, z, anc)
            cam = f"(({fx}, {fy}), {z}, {anc})"
        scenes.append(f'    dict(t="{s["t"]}", head={json.dumps(s["head"], ensure_ascii=False)}, '
                      f'vo={json.dumps(s["vo"], ensure_ascii=False)},\n         cam={cam}, dark={s["dark"]}, dd={s["dd"]}),')
    data = ('# ---------------- scenes ----------------\nCENTER = (SW / 2, SH / 2)\nOBJ = {}\n\n'
            'WIDE = (CENTER, 1.0, (540, 940))\nSCENES = [\n' + "\n".join(scenes) + '\n]\n'
            'END = len(SCENES) - 1\nBOARDS = {}\n' + DOODLE + '\n\n')
    return data, t


def build(src, dst, video, data):
    s = open(E + src).read()
    rep = [('CREDIT = "Ảnh dự án: [tên dự án] · [studio] · [nhiếp ảnh gia]"',
            'CREDIT = "Ảnh dự án: MS House, Ahmedabad · Studio Saransh · ảnh Ishita Sitwala, The Fishy Project"'),
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · NẮNG XIÊN HIỆN VÂN BÊ TÔNG"'),
           ("CARD_W2, BORDER2 = 1920, 0", "CARD_W2, BORDER2 = 1280, 0  # ảnh dọc 3:4: thẻ hẹp hơn để chữ nằm ngoài ảnh"),
           ("C2 = (B2W / 2, 1810.0)", "C2 = (B2W / 2, 1880.0)")]
    rep.append(("borderMode=cv2.BORDER_REFLECT)", "borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255, 0))"))
    for a_, b_ in rep:
        assert a_ in s, a_
        s = s.replace(a_, b_)
    a = s.index("# ---------------- scenes")
    b = s.index('def render_scene') if not video else s.index('BOARDS["plain"] = make_board(1.0)')
    s = s[:a] + data + s[b:]
    if video:
        s = s.replace('"reel1_silent.mp4"', '"reel_nang-xien-hien-van-be-tong_silent.mp4"')
    else:
        s = s.replace('"frames_v7"', '"frames"').replace('"storyboard_reel1_v7.png"', '"storyboard.png"')
        s = s.replace("AH Decode · Cân bằng thị giác — bảng phân cảnh v7", "AH Decode · Nắng xiên hiện vân bê tông")
        s = s.replace("Ảnh dán bằng băng giấy ở giữa mép trên · không viền · nền trắng trơn · chữ nâu đậm trên nền, trắng trên ảnh",
                      "Ảnh dán bằng băng giấy · nền trắng · chữ nâu trên nền, trắng trên ảnh")
        s = s.replace("Camera zoom vào ảnh khi nói đến chi tiết · ~28 giây · nét vẽ chạy animation theo nhịp lời đọc",
                      "Camera zoom vào chi tiết · nét doodle gốc của bài lộ dần theo lời đọc")
        s = s.replace("Ảnh tối ~14% ở cảnh có nét vẽ; cảnh 1, 6, 7 giữ ảnh nguyên bản.",
                      "Ảnh tối ~14% ở cảnh có nét vẽ (cảnh 4, 5); các cảnh khác giữ ảnh nguyên bản.")
    open(OUT + "engine_ep06/" + dst, "w").write(s)


data, total = build_data()
build("engine_storyboard_v7.py", "engine_ep06.py", False, data)
build("engine_video.py", "engine_video_ep06.py", True, data)

# ---- script.md + elevenlabs.txt ----
NAMES = dict(A="Câu móc", B="Lý thuyết", C="Vấn đề", D="Cơ chế", E="Ví dụ công trình", H="Kết", I="Khung cuối")
voiced = [s for s in SC if s["head"] != "end"]
nw = sum(words(s["vo"]) for s in voiced)
rows = []
for k, s in enumerate(SC):
    head = "(khung cuối cố định, không lời)" if s["head"] == "end" else s["head"]
    cam = "rộng" if s["cam"] == WIDE else ("khung cuối" if s["cam"] == "END" else f"zoom {s['cam'][1]}× vào {s['cam'][0]}")
    dd = ", ".join(s["dd"]) or "không nét"
    rows.append(f'| {k + 1} | {s["t"]} | {NAMES[s["part"]]} | {head} | {s["vo"] or "—"} | {cam}; {dd} |')
subs = "\n".join(f'| {k + 1} | {s["vo"]} | {s.get("tts", s["vo"])} |' for k, s in enumerate(voiced))
md = (f"# Giả thuyết kiến trúc · AH Decode · Nắng xiên hiện vân bê tông · BẢN NHÁP chờ duyệt\n\n"
      f"Bài trong kho: `AH-Decode-Decor/bai-02-3-bai-hoc-chat-cam-vat-lieu-noi-that/bai-02.md` (nhánh AH-Interior-notes, commit 8fd09bd), ý chính: mục \"Chất cảm chỉ hiện rõ khi ánh sáng chiếu xiên qua bề mặt\".\n"
      f"Ảnh: `anh/04-doodle-nang-xien-ban-cong.jpg` · MS House, Ahmedabad · Studio Saransh · ảnh Ishita Sitwala, The Fishy Project\n"
      f"Thời lượng dự kiến: {total:.1f} giây + 1 giây giữ khung cuối · {nw} từ lời đọc · {len(SC)} cảnh (6 cảnh có lời + khung cuối).\n"
      f"Nét: dùng doodle gốc của bài (tia nắng nét đứt, mũi tên, hai nhãn \"phần có nắng lộ từng vệt ván khuôn\" và \"phần trong bóng chỉ còn mảng xám phẳng\"), lộ dần; không vẽ nét mới.\n\n"
      "| # | Thời lượng | Phần | Tiêu đề trên khung | Lời đọc | Hình |\n|---|---|---|---|---|---|\n" + "\n".join(rows) +
      "\n\n## Đối chiếu phụ đề (loi) và bản đọc (tts)\n\n| Cảnh | Phụ đề | Bản đọc |\n|---|---|---|\n" + subs + "\n\n"
      "## Tên riêng đã phiên âm\n\n| Chính tả gốc | Phiên âm |\n|---|---|\n"
      "| Kilmer | Kin-mơ |\n| Designing Interiors | Đi-dai-ninh In-tia-ri-ơ |\n"
      "| Studio Saransh | Xtu-đi-ô Xa-ran |\n| Ahmedabad | A-mê-đa-bát |\n")
open(OUT + "script.md", "w").write(md)

el = '\n<break time="1.2s" />\n'.join(s.get("tts", s["vo"]) for s in voiced)
el += "\n\n---\n--- Gợi ý cài đặt: giọng nam hoặc nữ trầm ấm, tốc độ 1.0, mô hình Multilingual v2, ngôn ngữ Vietnamese ---\n"
open(OUT + "elevenlabs.txt", "w").write(el)
print("total", round(total, 1), "words", nw)
for s in SC:
    print(s["t"], words(s["vo"]), s["head"])
