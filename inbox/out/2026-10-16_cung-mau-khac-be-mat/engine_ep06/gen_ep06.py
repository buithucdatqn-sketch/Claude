"""Tập 6: Nền lùi, màu dồn vào một khối (bài 01 kho AH-Decode-Decor, ảnh 04 có doodle sẵn).
Sinh engine_ep06.py + engine_video_ep06.py từ hai engine gốc, và script.md/elevenlabs.txt từ cùng dữ liệu cảnh.
Ảnh dọc (1800x2400): thu nhỏ thẻ ảnh (CARD_W2 1440) và hạ tâm thẻ (C2 y 1880) để tiêu đề và lời đọc nằm ngoài ảnh ở cảnh rộng.
Doodle: không vẽ nét mới; lộ dần chính các nét doodle gốc của bài (doodle_ep06.npz: elip, mũi tên, nhãn chữ) theo mục 2c."""
import json
import re

E = "/home/user/Claude/engine/"
OUT = "/home/user/Claude/inbox/out/2026-10-16_cung-mau-khac-be-mat/"
WPS = 3.2      # tốc độ đọc dự kiến (từ/giây)
TRANS = 0.7

WIDE = "WIDE"
SC = [
    dict(part="A", blk=1, head="Cùng màu, sao khác nhau?", cam=WIDE, dark=False, dd=[],
         vo="Cùng một màu sơn, sao chỗ phẳng chỗ sọc nhìn lại khác nhau?"),
    dict(part="B", blk=2, head="Phòng cần đủ sáng, vừa, tối", cam=((1000, 700), 2.2, (540, 900)), dark=False, dd=[],
         vo="Sách của hai tác giả Kilmer nói căn phòng nào cũng cần đủ mảng sáng, mảng vừa và mảng tối.",
         tts="Sách của hai tác giả Kin-mơ nói căn phòng nào cũng cần đủ mảng sáng, mảng vừa và mảng tối."),
    dict(part="C", blk=3, head="Chỉ một màu thì lấy đâu ra sáng tối?", cam=((420, 1500), 2.2, (540, 900)), dark=False, dd=[],
         vo="Nhưng nếu chỉ sơn một màu, lấy đâu ra chỗ sáng, chỗ tối?"),
    dict(part="C", blk=4, head="Rãnh đổ bóng, nên trông sẫm hơn", cam=((430, 1900), 2.2, (540, 900)), dark=False, dd=[],
         vo="Câu trả lời nằm ở bề mặt. Mặt có rãnh tự đổ bóng, nên trông sẫm hơn mặt trơn, dù cùng một màu sơn."),
    dict(part="D", blk=5, head="Cánh tủ nan dọc: sẫm hơn", cam=((900, 2050), 2.1, (540, 1650)), free=True, dark=True, dd=["arr2", "lab2"],
         vo="Trong ảnh này, cánh tủ nan dọc trông sẫm hơn."),
    dict(part="D", blk=5, head="Tường sơn phẳng: sáng hơn", cam=((1420, 620), 2.1, (800, 520)), free=True, dark=True, dd=["arr1", "lab1"],
         vo="Tường sơn phẳng ngay bên cạnh thì sáng hơn."),
    dict(part="E", blk=5, head="The Green Box, Berlin", cam=((1400, 1250), 2.1, (540, 900)), dark=False, dd=[],
         vo="Căn hộ này là The Green Box ở Berlin, do Ester Bruzkus Architekten thiết kế.",
         tts="Căn hộ này là Đờ Grin Bốc ở Béc-lin, do Ét-xtơ Bờ-rút-cút Ạc-hi-tếch-ten thiết kế."),
    dict(part="D", blk=5, head="Một họ xanh, mỗi chỗ một độ sáng", cam=((600, 1250), 2.1, (540, 900)), dark=False, dd=[],
         vo="Ở khu bếp cũng vậy, tường sơn, đá vân và tủ ô liu, mỗi chỗ một độ sáng.",
         tts="Ở khu bếp cũng vậy, tường sơn, đá vân và tủ ô-liu, mỗi chỗ một độ sáng."),
    dict(part="H", blk=6, head="Một màu, đủ sáng vừa tối", cam=WIDE, dark=False, dd=[],
         vo="Một màu thôi, nhưng đổi bề mặt là có đủ sáng, vừa, tối."),
    dict(part="I", blk=6, head="end", cam="END", dark=False, vo="", dd=[],
         tts="Bài phân tích đầy đủ dành cho thành viên, mọi người ghé phần bình luận nha.",
         say="Bài phân tích đầy đủ dành cho thành viên, mọi người ghé phần bình luận nha."),
]

DOODLE = r'''
_L = np.load(os.path.join(HERE, "doodle_ep06.npz"))
LAYER = {k: _L[k] for k in _L.files}   # toạ độ trên ảnh làm việc 1800x2400 (source.png)
RAD = dict(arr1=0.9, arr2=0.9)         # bán kính nét gốc (px ảnh làm việc)


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
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · CÙNG MÀU, KHÁC BỀ MẶT"'),
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
        s = s.replace('"reel1_silent.mp4"', '"reel_cung-mau-khac-be-mat_silent.mp4"')
    else:
        s = s.replace('"frames_v7"', '"frames"').replace('"storyboard_reel1_v7.png"', '"storyboard.png"')
        s = s.replace("AH Decode · Cân bằng thị giác — bảng phân cảnh v7", "AH Decode · Cùng màu, khác bề mặt")
        s = s.replace("Ảnh dán bằng băng giấy ở giữa mép trên · không viền · nền trắng trơn · chữ nâu đậm trên nền, trắng trên ảnh",
                      "Ảnh dán bằng băng giấy · nền trắng · chữ nâu trên nền, trắng trên ảnh")
        s = s.replace("Camera zoom vào ảnh khi nói đến chi tiết · ~28 giây · nét vẽ chạy animation theo nhịp lời đọc",
                      "Camera zoom vào chi tiết · nét doodle gốc của bài lộ dần theo lời đọc")
        s = s.replace("Ảnh tối ~14% ở cảnh có nét vẽ; cảnh 1, 6, 7 giữ ảnh nguyên bản.",
                      "Ảnh tối ~14% ở cảnh có nét vẽ (cảnh 5, 6); các cảnh khác giữ ảnh nguyên bản.")
    open(OUT + "engine_ep06/" + dst, "w").write(s)


data, total = build_data()
build("engine_storyboard_v7.py", "engine_ep06.py", False, data)
build("engine_video.py", "engine_video_ep06.py", True, data)

# ---- bảng cảnh + elevenlabs.txt (khối dán sẵn, thẻ ngắt 1,2 giây giữa 6 cảnh kịch bản) ----
shown = [x.get("say", x["vo"]) for x in SC]
spoken = [x.get("tts", x["vo"]) for x in SC]
nw = sum(words(x) for x in shown)
blocks = {}
for x, sp in zip(SC, spoken):
    blocks.setdefault(x["blk"], []).append(sp)
BR = ' <break time="1.2s" /> '
el = BR.join(" ".join(v) for k, v in sorted(blocks.items()))
open(OUT + "elevenlabs.txt", "w").write(el + "\n")
print("total engine", round(total, 1), "words", nw)
for k, x in enumerate(SC):
    print(k + 1, x["blk"], x["t"], words(shown[k]), x["head"])
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep06/scenes.json", "w"), ensure_ascii=False, indent=1)
