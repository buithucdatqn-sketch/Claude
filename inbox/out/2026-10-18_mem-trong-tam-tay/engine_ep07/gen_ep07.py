"""Tập 7: Cứng ở xa, mềm trong tầm tay (bài 02 kho AH-Decode-Decor, bài học 2 "Đặt bề mặt thô cạnh bề mặt mịn").
Ảnh chính 08 (phòng khách, dọc 1600x2400, doodle sẵn); ảnh phụ 09 (phòng ngủ, ngang 2400x1602, doodle sẵn) cho các cảnh phòng ngủ (mục 5d).
Sinh engine_ep07.py + engine_video_ep07.py (ảnh chính), engine_ep07_ngu.py + engine_video_ep07_ngu.py (ảnh phụ),
scenes.json, splice.json và elevenlabs.txt từ cùng một dữ liệu cảnh.
Doodle: không vẽ nét mới; lộ dần chính các nét doodle gốc của bài (doodle_ep07*.npz, tách bằng make_layers.py) theo mục 2c."""
import json
import os
import re

E = "/home/user/Claude/engine/"
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
WPS = 3.2      # tốc độ đọc dự kiến (từ/giây) cho bản nháp; giai đoạn B căn lại theo ghi âm
TRANS = 0.7

WIDE = "WIDE"
SC = [
    dict(part="A", blk=1, head="Bê tông mộc: đẹp trên ảnh, lạnh khi ở?", cam=WIDE, dark=False, dd=[],
         vo="Nhà bê tông mộc lên ảnh thì đẹp, sao ở thật lại hay bị chê lạnh?"),
    dict(part="B", blk=2, head="Kilmer & Kilmer (2014): mặt trơn lạnh, vải dày ấm", cam=((800, 330), 3.4, (540, 900)), dark=False, dd=[],
         vo="Hai tác giả Kilmer viết, phòng nhiều mặt trơn thường lạnh, còn thảm, vải dày mang lại hơi ấm.",
         tts="Hai tác giả Kin-mơ viết, phòng nhiều mặt trơn thường lạnh, còn thảm, vải dày mang lại hơi ấm."),
    dict(part="C", blk=3, head="Không thiếu vân, chỉ thiếu đồ mềm", cam=((560, 1000), 4.6, (540, 900)), dark=False, dd=[],
         vo="Mà bê tông mộc đâu có thiếu vân, nó thường thiếu đồ mềm đặt ngay bên cạnh."),
    dict(part="C", blk=4, head="Tường, sàn cứng dội tiếng, nên nghe vang", cam=((330, 1420), 4.2, (540, 900)), dark=False, dd=[],
         vo="Tường, sàn cứng còn dội tiếng bước chân, nên nhà bê tông vừa trông lạnh, vừa nghe vang."),
    dict(part="D", blk=5, head="MS House: trần, tường, sàn đều cứng", cam=((1310, 800), 3.0, (745, 720)), free=True, dark=True,
         dd=["arr_vo", "lab_vo"],
         vo="Như phòng khách nhà MS House ở Ấn Độ, trần và tường bê tông, sàn đá, đều cứng.",
         tts="Như phòng khách nhà Em-ét Hao-xơ ở Ấn Độ, trần và tường bê tông, sàn đá, đều cứng."),
    dict(part="D", blk=5, head="Trong tầm tay: mềm và ấm", cam=((272, 1690), 3.0, (322, 1080)), free=True, dark=True,
         dd=["arr_sofa", "lab_sofa"],
         vo="Còn đồ trong tầm tay thì mềm, ấm. Bộ sofa vải xù nổi hẳn trên nền bê tông.",
         tts="Còn đồ trong tầm tay thì mềm, ấm. Bộ sô-pha vải xù nổi hẳn trên nền bê tông."),
    dict(part="D", blk=5, head="Gỗ ở chỗ lưng tựa, bê tông lùi lên cao", cam=WIDE, dark=False, dd=[], img="ngu",
         cam_ngu=((980, 700), 3.1, (540, 880)), dd_ngu=["arr_dau", "lab_dau"],
         vo="Phòng ngủ cũng vậy, gỗ ốp đúng chỗ lưng tựa đầu giường, còn bê tông lùi lên cao."),
    dict(part="F", blk=6, head="Thử ở nhà mình", cam=((620, 2000), 3.0, (540, 900)), dark=False, dd=[],
         vo="Nhà toàn bê tông thì thử đổi đầu giường, lưng ghế sang gỗ, thêm thảm sợi đay, rèm vải lanh cho đỡ vang."),
    dict(part="H", blk=6, head="Cứng ở xa, mềm trong tầm tay", cam=WIDE, dark=False, dd=[],
         vo="Vậy cứ giữ bê tông, chỉ cần để mặt cứng ở xa, đồ mềm trong tầm tay."),
    dict(part="I", blk=6, head="end", cam="END", dark=False, vo="", dd=[],
         say="Bài phân tích đầy đủ nằm trong gói thành viên, mọi người vào phần bình luận xem nha."),
]

DOODLE = r'''
_L = np.load(os.path.join(HERE, "doodle_ep07.npz"))
LAYER = {k: _L[k] for k in _L.files}   # toạ độ trên ảnh làm việc (source.png)
RAD = 0.9                              # bán kính chấm bút khi lộ lại nét gốc (px ảnh làm việc)


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
            _stamp(wb, LAYER[k], RAD)
'''


def dur(s):
    return max(3.5, TRANS + words(s.get("say", s["vo"])) / WPS)


def times():
    T = [0.0]
    for s in SC:
        T.append(round(T[-1] + dur(s), 2))
    return T


def cover(fx, fy, z, anc, sw, sh, m=40):
    """dời điểm neo để ảnh phủ kín khung 1080x1920 khi zoom (0.4 px khung / px ảnh ở z=1)"""
    sc = z * 0.4
    assert sc * sh >= 1920 + 2 * m and sc * sw >= 1080 + 2 * m, z
    ax = min(max(anc[0], 1080 + m - sc * (sw - fx)), sc * fx - m)
    ay = min(max(anc[1], 1920 + m - sc * (sh - fy)), sc * fy - m)
    return (round(ax), round(ay))


def words(s):
    return len(s.split())


def cam_str(s, cam, sw=1600, sh=2400):
    if cam == WIDE:
        return "WIDE"
    if cam == "END":
        return "END_SAFE"
    (fx, fy), z, anc = cam
    if not s.get("free"):
        anc = cover(fx, fy, z, anc, sw, sh)
    return f"(({fx}, {fy}), {z}, {anc})"


def scene_line(s, a, b, cam, dd):
    return (f'    dict(t="{a:g}–{b:g}s", head={json.dumps(s["head"], ensure_ascii=False)}, '
            f'vo={json.dumps(s["vo"], ensure_ascii=False)},\n         cam={cam}, dark={s["dark"]}, dd={dd}),')


def wrap_data(lines, doodle):
    return ('# ---------------- scenes ----------------\nCENTER = (SW / 2, SH / 2)\nOBJ = {}\n\n'
            'WIDE = WIDE_SAFE\nSCENES = [\n' + "\n".join(lines) + '\n]\n'
            'END = len(SCENES) - 1\nBOARDS = {}\n' + doodle + '\n\n')


def build_data(T):
    lines = []
    for k, s in enumerate(SC):
        a, b = T[k], T[k + 1]
        s["t"] = f"{a:g}–{b:g}s"
        lines.append(scene_line(s, a, b, cam_str(s, s["cam"]), s["dd"]))
    return wrap_data(lines, DOODLE)


def build_data_ngu(T):
    """engine phụ cho các cảnh dùng ảnh phòng ngủ (liền nhau): cảnh trước (ảnh phụ toàn cảnh) + các cảnh ảnh phụ + khung cuối giả.
    Video ghép: chỉ lấy đoạn của các cảnh ảnh phụ, đặt vào đúng mốc của chúng trong video chính."""
    ks = [i for i, s in enumerate(SC) if s.get("img") == "ngu"]
    k0, k1 = ks[0], ks[-1]
    prev, nxt = SC[k0 - 1], SC[-1]
    d0 = T[k0] - T[k0 - 1]
    lines = [scene_line(prev, 0, d0, "WIDE", [])]
    t = d0
    for k in ks:
        s = SC[k]
        d = T[k + 1] - T[k]
        cam = s["cam_ngu"]
        lines.append(scene_line(s, t, t + d, cam if cam == "WIDE" else cam_str(dict(s, free=True), cam, 2400, 1602), s["dd_ngu"]))
        t += d
    lines.append(scene_line(nxt, t, t + 0.5, "END_SAFE", []))
    return wrap_data(lines, DOODLE.replace("doodle_ep07.npz", "doodle_ep07_ngu.npz")), k0, k1, d0, t - d0


def build(src, dst, video, data, portrait=True, vname="reel_mem-trong-tam-tay_silent.mp4"):
    s = open(E + src).read()
    rep = [('CREDIT = "Ảnh dự án: [tên dự án] · [studio] · [nhiếp ảnh gia]"',
            'CREDIT = "Ảnh dự án: MS House, Ahmedabad · Studio Saransh · ảnh Ishita Sitwala, The Fishy Project"'),
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · CỨNG Ở XA, MỀM TRONG TẦM TAY"'),
           ]
    if portrait:  # ảnh dọc 2:3 (1600x2400): thẻ hẹp 1280 để giữ 0,4 px khung / px ảnh và chữ nằm ngoài ảnh ở cảnh rộng
        rep += [("CARD_W2, BORDER2 = 1920, 0", "CARD_W2, BORDER2 = 1280, 0  # ảnh dọc 2:3: thẻ hẹp hơn để chữ nằm ngoài ảnh"),
                ("C2 = (B2W / 2, 1810.0)", "C2 = (B2W / 2, 1880.0)")]
    rep.append(("borderMode=cv2.BORDER_REFLECT)", "borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255, 0))"))
    for a_, b_ in rep:
        assert a_ in s, a_
        s = s.replace(a_, b_)
    a = s.index("# ---------------- scenes")
    b = s.index('def render_scene') if not video else s.index('BOARDS["plain"] = make_board(1.0)')
    s = s[:a] + data + s[b:]
    if video:
        s = s.replace('"reel1_silent.mp4"', f'"{vname}"')
    else:
        tag = "" if portrait else "_ngu"
        s = s.replace('"frames_v7"', f'"frames{tag}"').replace('"storyboard_reel1_v7.png"', f'"storyboard{tag}.png"')
        s = s.replace("AH Decode · Cân bằng thị giác — bảng phân cảnh v7", "AH Decode · Cứng ở xa, mềm trong tầm tay")
        s = s.replace("Ảnh dán bằng băng giấy ở giữa mép trên · không viền · nền trắng trơn · chữ nâu đậm trên nền, trắng trên ảnh",
                      "Ảnh dán bằng băng giấy · nền trắng · chữ nâu trên nền, trắng trên ảnh")
        s = s.replace("Camera zoom vào ảnh khi nói đến chi tiết · ~28 giây · nét vẽ chạy animation theo nhịp lời đọc",
                      "Camera zoom vào chi tiết · nét doodle gốc của bài lộ dần theo lời đọc")
        s = s.replace("Ảnh tối ~14% ở cảnh có nét vẽ; cảnh 1, 6, 7 giữ ảnh nguyên bản.",
                      "Ảnh tối ~14% ở cảnh có nét vẽ; cảnh phòng ngủ dùng ảnh 09 (ghép từ engine phụ).")
    open(OUT + "engine_ep07/" + dst, "w").write(s)


T = times()
data = build_data(T)
build("engine_storyboard_v7.py", "engine_ep07.py", False, data)
build("engine_video.py", "engine_video_ep07.py", True, data)
data_n, K0, K1, D0, DL = build_data_ngu(T)
build("engine_storyboard_v7.py", "engine_ep07_ngu.py", False, data_n, portrait=False)
build("engine_video.py", "engine_video_ep07_ngu.py", True, data_n, portrait=False, vname="reel_ngu_silent.mp4")
json.dump(dict(scenes=[K0, K1], t_in_main=T[K0], cut_from=D0, cut_len=DL), open(OUT + "engine_ep07/splice.json", "w"))

# ---- elevenlabs.txt: sáu khối kịch bản nối bằng thẻ ngắt 1,2 giây (theo prompt của routine) ----
shown = [x.get("say", x["vo"]) for x in SC]
spoken = [x.get("tts", x.get("say", x["vo"])) for x in SC]
blocks = {}
for x, sp in zip(SC, spoken):
    blocks.setdefault(x["blk"], []).append(sp)
BR = '\n<break time="1.2s" />\n'
el = BR.join(" ".join(v) for k, v in sorted(blocks.items()))
open(OUT + "elevenlabs.txt", "w").write(el + "\n")
nw = sum(words(x) for x in shown)
print("tổng engine", T[-1], "giây; từ lời đọc", nw, "; ước tính giọng đọc ~", round(nw / 3.4 + 5 * 1.0, 1), "giây")
for k, x in enumerate(SC):
    print(k + 1, x["blk"], x["part"], x["t"], words(shown[k]), x["head"])
FOREIGN = ["Kilmer", "MS", "House", "Studio", "Saransh", "Ahmedabad", "teak", "sofa", "AH", "Decode"]
bad = re.findall(r"\d", " ".join(spoken)) + [w for w in FOREIGN if re.search(r"\b" + w + r"\b", " ".join(spoken))]
print("chữ số / tên nước ngoài chưa phiên âm trong bản đọc:", bad)
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep07/scenes.json", "w"), ensure_ascii=False, indent=1)
