"""Tập 6: Cùng màu, khác bề mặt (bài 01 kho AH-Decode-Decor, ảnh 12 có doodle sẵn).
Sinh engine_ep06.py + engine_video_ep06.py từ hai engine gốc, và script.md/elevenlabs.txt từ cùng dữ liệu cảnh.
Ảnh dọc (1800x2400): thu nhỏ thẻ ảnh (CARD_W2 1440) và hạ tâm thẻ (C2 y 1880) để tiêu đề và lời đọc nằm ngoài ảnh ở cảnh rộng.
Doodle: không vẽ nét mới; lộ dần chính các nét doodle gốc của bài (doodle_ep06.npz: elip, mũi tên, nhãn chữ) theo mục 2c."""
import json
import re

E = "/home/user/Claude/engine/"
OUT = "/home/user/Claude/inbox/out/2026-10-18_cung-mau-khac-be-mat/"
WPS = 3.2      # tốc độ đọc dự kiến (từ/giây)
TRANS = 0.7

WIDE = "WIDE"
SC = [
    dict(part="A", head="Cùng màu sơn, sao sẫm hơn?", cam=WIDE, dark=False, dd=[],
         vo="Cùng một màu sơn xanh, sao mặt tủ này sẫm hơn mặt kia?"),
    dict(part="B", head="Căn phòng cần sáng, vừa, tối", cam=((450, 900), 2.2, (540, 900)), dark=False, dd=[],
         vo="Theo sách của hai tác giả Kilmer, căn phòng cần đủ mảng sáng, mảng vừa và mảng tối. Nghe như phải dùng nhiều màu.",
         tts="Theo sách của hai tác giả Kin-mơ, căn phòng cần đủ mảng sáng, mảng vừa và mảng tối. Nghe như phải dùng nhiều màu."),
    dict(part="C", head="Bề mặt cũng góp phần", cam=((1250, 1300), 2.2, (540, 900)), dark=False, dd=[],
         vo="Không hẳn đâu nha. Tụi mình hay nghĩ cùng màu sơn là cùng độ sáng. Mà bề mặt cũng góp phần không nhỏ."),
    dict(part="D", head="Nan dọc đổ bóng nên sẫm hơn", cam=((900, 1500), 1.5, (540, 900)), free=True, dark=True, dd=["arr1", "lab1", "arr2", "lab2"],
         vo="Mặt có nan dọc tự đổ bóng, nên trông sẫm hơn. Mặt sơn phẳng trơn thì trông sáng hơn. Cùng một màu sơn đó."),
    dict(part="E", head="Một màu xanh, đủ sáng vừa tối", cam=((900, 1500), 2.2, (540, 900)), dark=False, dd=[],
         vo="Ở căn hộ Green Box tại Berlin, của văn phòng Ester Bruzkus Architekten, tủ nan dọc đứng cạnh mặt sơn phẳng. Chỉ một màu xanh mà đủ sáng, vừa, tối.",
         tts="Ở căn hộ Gơ-rin Bốc tại Béc-lin, của văn phòng Ét-xtơ Bơ-rúc-cút Ác-ki-téc-ken, tủ nan dọc đứng cạnh mặt sơn phẳng. Chỉ một màu xanh mà đủ sáng, vừa, tối."),
    dict(part="H", head="Đổi bề mặt, đừng vội đổi màu", cam=WIDE, dark=False, dd=[],
         vo="Muốn thêm sáng tối, hãy đổi bề mặt, đừng vội đổi màu. Bài đầy đủ dành cho thành viên nằm ở phần bình luận nha."),
    dict(part="I", head="end", cam="END", dark=False, vo="", dd=[]),
]

DOODLE = r'''
_L = np.load(os.path.join(HERE, "doodle_ep06.npz"))
LAYER = {k: _L[k] for k in _L.files}   # toạ độ trên ảnh làm việc 1800x2400 (source.png)
RAD = dict(arr1=1.6, arr2=1.6)         # bán kính nét gốc (px ảnh làm việc)


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
                      "Ảnh tối ~14% ở cảnh có nét vẽ (cảnh 3, 4); các cảnh khác giữ ảnh nguyên bản.")
    open(OUT + "engine_ep06/" + dst, "w").write(s)


data, total = build_data()
build("engine_storyboard_v7.py", "engine_ep06.py", False, data)
build("engine_video.py", "engine_video_ep06.py", True, data)

# ---- script.md + elevenlabs.txt ----
NAMES = dict(A="Mở", B="Nguồn gốc", C="Cơ chế", D="Đọc trên ảnh", E="Phản ví dụ", F="Áp dụng",
             G="Chọn đồ", H="Chốt", I="Cảnh cuối")
shown = [s.get("say", s["vo"]) for s in SC]
spoken_all = [s.get("tts", s["vo"]) for s in SC]
nw = sum(words(x) for x in shown)
rows = []
for k, s in enumerate(SC):
    head = "(khung cuối cố định)" if s["head"] == "end" else s["head"]
    cam = "rộng" if s["cam"] == WIDE else ("khung cuối" if s["cam"] == "END" else f"zoom {s['cam'][1]}× vào {s['cam'][0]}")
    dd = ", ".join(s["dd"]) or "không nét"
    rows.append(f'| {k + 1} | {s["t"]} | {s["part"]} · {NAMES[s["part"]]} | {head} | {shown[k]} | {cam}; {dd} |')
md = (f"# AH Decode · Cùng màu, khác bề mặt · BẢN NHÁP chờ duyệt\n\n"
      f"Bài trong kho: `AH-Decode-Decor/bai-01-3-bai-hoc-phoi-mau-noi-that-can-ho/bai-01.md` (commit 0965b48), ý chính: đoạn \"Một màu chủ đạo, hai màu phụ đi vòng quanh\" (ý: cùng màu, khác bề mặt).\n"
      f"Ảnh: `anh/12-doodle-cung-mau-khac-be-mat.jpg` · The Green Box, Berlin · Ester Bruzkus Architekten · ảnh Robert Rieger\n"
      f"Thời lượng dự kiến: {total:.1f} giây + 1 giây giữ khung cuối · {nw} từ lời đọc (chữ viết) · {len(SC)} cảnh.\n"
      f"Nét: chỉ dùng doodle gốc của bài (hai mũi tên và hai nhãn \"mặt nan dọc trông sẫm hơn\", \"mặt sơn phẳng sáng hơn\"), lộ dần; không vẽ nét mới.\n\n"
      "| # | Thời lượng | Phần | Tiêu đề trên khung | Lời đọc | Hình |\n|---|---|---|---|---|---|\n" + "\n".join(rows) +
      "\n\n## Lời đọc liền mạch\n\n" + " ".join(shown) + "\n\n"
      "## Phiên âm cho ElevenLabs\n\n| Chính tả gốc | Phiên âm |\n|---|---|\n"
      "| Kilmer | Kin-mơ |\n| Green Box | Gơ-rin Bốc |\n| Berlin | Béc-lin |\n| Ester Bruzkus Architekten | Ét-xtơ Bơ-rúc-cút Ác-ki-téc-ken |\n")
open(OUT + "script.md", "w").write(md)


def lines(txt):
    parts = re.split(r'(?<=[.?!])\s+', txt.strip())
    return "\n".join(p for p in parts if p)


el = "\n\n<break time=\"1.2s\" />\n\n".join(lines(x) for x in spoken_all if x.strip())
el += "\n\n---\n--- Gợi ý cài đặt: giọng nữ hoặc nam trầm ấm, tốc độ 1.0, mô hình đa ngôn ngữ, ngôn ngữ Vietnamese ---\n"
open(OUT + "elevenlabs.txt", "w").write(el)
print("total", round(total, 1), "words", nw)
for s in SC:
    print(s["t"], words(s.get("say", s["vo"])), s["head"])
