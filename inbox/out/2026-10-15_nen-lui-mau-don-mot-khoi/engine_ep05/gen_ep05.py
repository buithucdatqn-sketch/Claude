"""Tập 5: Nền lùi, màu dồn vào một khối (bài 01 kho AH-Decode-Decor, ảnh 04 có doodle sẵn).
Sinh engine_ep05.py + engine_video_ep05.py từ hai engine gốc, và script.md/elevenlabs.txt từ cùng dữ liệu cảnh.
Ảnh dọc (1800x2400): thu nhỏ thẻ ảnh (CARD_W2 1440) và hạ tâm thẻ (C2 y 1880) để tiêu đề và lời đọc nằm ngoài ảnh ở cảnh rộng.
Doodle: không vẽ nét mới; lộ dần chính các nét doodle gốc của bài (doodle_ep05.npz: elip, mũi tên, nhãn chữ) theo mục 2c."""
import json
import re

E = "/home/user/claude/engine/"
OUT = "/home/user/claude/inbox/out/2026-10-15_nen-lui-mau-don-mot-khoi/"
WPS = 3.2      # tốc độ đọc dự kiến (từ/giây)
TRANS = 0.7

WIDE = "WIDE"
SC = [
    dict(part="A", head="Vì sao khối xanh giữ vai chính?", cam=WIDE, dark=False, dd=[],
         vo="Khối xanh giữa nhà giữ vai chính. Vì sao?"),
    dict(part="B", head="Cách thứ nhất: nền lùi", cam=((900, 1000), 2.2, (540, 900)), dark=False, dd=[],
         vo="Kilmer và Kilmer: tường, sàn trung tính, màu đậm dồn vào đồ đạc.",
         tts="Kin-mơ và Kin-mơ: tường, sàn trung tính, màu đậm dồn vào đồ đạc."),
    dict(part="B", head="Mắt đọc màu theo xung quanh", cam=((700, 700), 2.2, (540, 900)), dark=False, dd=[],
         vo="Albers, 1963: mắt đọc màu theo xung quanh.",
         tts="An-bơ, năm một chín sáu ba: mắt đọc màu theo xung quanh."),
    dict(part="D", head="Màu trung tính lùi về nền", cam=((800, 1550), 1.7, (540, 880)), free=True, dark=True, dd=["arr1", "lab1"],
         vo="Bê tông, sàn gỗ, rèm: trung tính."),
    dict(part="D", head="Một khối duy nhất có màu mạnh", cam=((1150, 1900), 2.1, (700, 800)), free=True, dark=True, dd=["arr2", "lab2"],
         vo="Khối xanh là màu mạnh duy nhất trong khung."),
    dict(part="C", head="Trong khối: nền và nhấn đảo vai", cam=((450, 1400), 2.2, (540, 900)), dark=False, dd=[],
         vo="Đứng trong khối xanh, như ở bếp: xanh thành nền, đồ nhỏ sáng màu là điểm nhấn."),
    dict(part="E", head="Thử hình dung: tường cũng sơn màu", cam=((300, 450), 2.4, (540, 900)), dark=False, dd=[],
         vo="Tường cũng sơn màu thì khối xanh hẳn mất vị trí trung tâm."),
    dict(part="F", head="Thử ngay trong nhà", cam=((1100, 1400), 2.2, (540, 900)), dark=False, dd=[],
         vo="Tụi mình chọn màu chủ đạo cho khối lớn nhất, thường tủ hoặc sàn gỗ. Rồi đứng ở cửa, bàn ăn: nó là đồ hay nền?"),
    dict(part="G", head="Chọn màu cho mảng lớn", cam=((1100, 1750), 2.4, (540, 900)), dark=False, dd=[],
         vo="Màu phủ mảng lớn trông đậm hơn mẫu nhỏ: nên chọn nhạt hơn một bậc."),
    dict(part="H", head="Công thức", cam=WIDE, dark=False, dd=[],
         vo="Theo tụi mình: đừng chỉ hỏi màu gì, hãy hỏi màu ấy định sơn ở đâu."),
    dict(part="I", head="end", cam="END", dark=False, vo="", dd=[],
         tts="Ây-ết Đi-cốt, series về nguyên tắc thiết kế và chọn đồ đê-co. Theo dõi Giả Thuyết Kiến Trúc, bài viết cho thành viên ở link bình luận.",
         say="AH Decode, series về nguyên tắc thiết kế và chọn đồ decor. Theo dõi Giả Thuyết Kiến Trúc, bài viết cho thành viên ở link bình luận."),
]

DOODLE = r'''
_L = np.load(os.path.join(HERE, "doodle_ep05.npz"))
LAYER = {k: _L[k] for k in _L.files}   # toạ độ trên ảnh làm việc 1800x2400 (source.png)
RAD = dict(arr1=0.8, arr2=0.8)         # bán kính nét gốc (px ảnh làm việc)


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
    """dời điểm neo để ảnh phủ kín khung 1080x1920 khi zoom (ảnh dọc 1800x2400, 0.4 px khung / px ảnh ở z=1)"""
    sc = z * 0.4
    assert sc * 2400 >= 1920 + 2 * m, z
    ax = min(max(anc[0], 1080 + m - sc * (1800 - fx)), sc * fx - m)
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
            dur = max(dur, 7.0)
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
            'CREDIT = "Ảnh dự án: The Green Box, Berlin · Ester Bruzkus Architekten · ảnh Robert Rieger"'),
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · NỀN LÙI, MÀU DỒN MỘT KHỐI"'),
           ("CARD_W2, BORDER2 = 1920, 0", "CARD_W2, BORDER2 = 1440, 0  # ảnh dọc 3:4: thẻ hẹp hơn để chữ nằm ngoài ảnh"),
           ("C2 = (B2W / 2, 1810.0)", "C2 = (B2W / 2, 1880.0)")]
    rep.append(("borderMode=cv2.BORDER_REFLECT)", "borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255, 0))"))
    for a_, b_ in rep:
        assert a_ in s, a_
        s = s.replace(a_, b_)
    a = s.index("# ---------------- scenes")
    b = s.index('def render_scene') if not video else s.index('BOARDS["plain"] = make_board(1.0)')
    s = s[:a] + data + s[b:]
    if video:
        s = s.replace('"reel1_silent.mp4"', '"reel_nen-lui-mau-don-mot-khoi_silent.mp4"')
    else:
        s = s.replace('"frames_v7"', '"frames"').replace('"storyboard_reel1_v7.png"', '"storyboard.png"')
        s = s.replace("AH Decode · Cân bằng thị giác — bảng phân cảnh v7", "AH Decode · Nền lùi, màu dồn một khối")
        s = s.replace("Ảnh dán bằng băng giấy ở giữa mép trên · không viền · nền trắng trơn · chữ nâu đậm trên nền, trắng trên ảnh",
                      "Ảnh dán bằng băng giấy · nền trắng · chữ nâu trên nền, trắng trên ảnh")
        s = s.replace("Camera zoom vào ảnh khi nói đến chi tiết · ~28 giây · nét vẽ chạy animation theo nhịp lời đọc",
                      "Camera zoom vào chi tiết · nét doodle gốc của bài lộ dần theo lời đọc")
        s = s.replace("Ảnh tối ~14% ở cảnh có nét vẽ; cảnh 1, 6, 7 giữ ảnh nguyên bản.",
                      "Ảnh tối ~14% ở cảnh có nét vẽ (cảnh 4, 5); các cảnh khác giữ ảnh nguyên bản.")
    open(OUT + "engine_ep05/" + dst, "w").write(s)


data, total = build_data()
build("engine_storyboard_v7.py", "engine_ep05.py", False, data)
build("engine_video.py", "engine_video_ep05.py", True, data)

# ---- script.md + elevenlabs.txt ----
NAMES = dict(A="Mở", B="Nguồn gốc", C="Cơ chế", D="Đọc trên ảnh", E="Phản ví dụ", F="Áp dụng",
             G="Chọn đồ", H="Công thức", I="Cảnh cuối")
shown = [s.get("say", s["vo"]) for s in SC]
spoken_all = [s.get("tts", s["vo"]) for s in SC]
nw = sum(words(x) for x in shown)
rows = []
for k, s in enumerate(SC):
    head = "(khung cuối cố định)" if s["head"] == "end" else s["head"]
    cam = "rộng" if s["cam"] == WIDE else ("khung cuối" if s["cam"] == "END" else f"zoom {s['cam'][1]}× vào {s['cam'][0]}")
    dd = ", ".join(s["dd"]) or "không nét"
    rows.append(f'| {k + 1} | {s["t"]} | {s["part"]} · {NAMES[s["part"]]} | {head} | {shown[k]} | {cam}; {dd} |')
md = (f"# AH Decode · Nền lùi, màu dồn một khối · BẢN NHÁP chờ duyệt\n\n"
      f"Bài trong kho: `AH-Decode-Decor/bai-01-3-bai-hoc-phoi-mau-noi-that-can-ho/bai-01.md` (commit 65b5427), ý chính: mục \"Nền lùi lại, màu nhấn dồn vào một khối\".\n"
      f"Ảnh: `anh/04-doodle-nen-lui.jpg` · The Green Box, Berlin · Ester Bruzkus Architekten · ảnh Robert Rieger\n"
      f"Thời lượng dự kiến: {total:.1f} giây + 1 giây giữ khung cuối · {nw} từ lời đọc (chữ viết) · {len(SC)} cảnh.\n"
      f"Nét: chỉ dùng doodle gốc của bài (hai mũi tên và hai nhãn \"trần bê tông, sàn gỗ sáng lùi về nền\", \"sơn mài xanh, màu duy nhất trong khung\"), lộ dần; không vẽ nét mới.\n\n"
      "| # | Thời lượng | Phần | Tiêu đề trên khung | Lời đọc | Hình |\n|---|---|---|---|---|---|\n" + "\n".join(rows) +
      "\n\n## Lời đọc liền mạch\n\n" + " ".join(shown) + "\n\n"
      "## Phiên âm cho ElevenLabs\n\n| Chính tả gốc | Phiên âm |\n|---|---|\n"
      "| Kilmer | Kin-mơ |\n| Albers | An-bơ |\n| 1963 | năm một chín sáu ba |\n"
      "| AH Decode | Ây-ết Đi-cốt |\n| decor | đê-co |\n")
open(OUT + "script.md", "w").write(md)


def lines(txt):
    parts = re.split(r'(?<=[.?!])\s+', txt.strip())
    return "\n".join(p for p in parts if p)


el = "\n\n".join(lines(x) for x in spoken_all)
el += "\n\n---\n--- Gợi ý cài đặt: giọng nữ hoặc nam trầm ấm, tốc độ 1.0, mô hình đa ngôn ngữ, ngôn ngữ Vietnamese ---\n"
open(OUT + "elevenlabs.txt", "w").write(el)
print("total", round(total, 1), "words", nw)
for s in SC:
    print(s["t"], words(s.get("say", s["vo"])), s["head"])
