"""Tập 7: Cứng ở xa, mềm trong tầm tay (bài 02 kho AH-Decode-Decor, bài học 2 "Đặt bề mặt thô cạnh bề mặt mịn").
Reel nhiều ảnh (bản 3, theo yêu cầu chủ Trang: thêm mặt bằng, diagram và các không gian khác của MS House).
Mỗi cảnh chọn ảnh qua khoá `img` (IMGS). Mỗi đoạn cảnh liên tiếp cùng một ảnh là một "run": script sinh
engine_ep07_rNN_<ảnh>.py (khung hình) và engine_video_ep07_rNN_<ảnh>.py (video) cho run đó, gồm cảnh trước
(ảnh của run, toàn cảnh, cùng chữ cảnh trước) + các cảnh của run + khung cuối giả (nếu run không chứa khung cuối).
Ghép: cắt đúng đoạn của từng run (runs.json) rồi nối theo thứ tự (mục 5d mở rộng).
Doodle: không vẽ nét mới; lộ dần chính các nét doodle gốc của bài (doodle_ep07*.npz, tách bằng make_layers.py) theo mục 2c."""
import json
import os
import re

def _repo_engine(d):
    """tìm thư mục engine/ của repo (chứa engine_video.py) từ vị trí file này đi lên"""
    while d != "/":
        if os.path.isfile(os.path.join(d, "engine", "engine_video.py")):
            return os.path.join(d, "engine") + "/"
        d = os.path.dirname(d)
    raise SystemExit("không tìm thấy engine/engine_video.py")


E = _repo_engine(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
WPS = 3.2      # tốc độ đọc dự kiến (từ/giây) cho bản nháp; giai đoạn B căn lại theo ghi âm
TRANS = 0.7

WIDE = "WIDE"
PHOTO = "Ảnh dự án: MS House, Ahmedabad · Studio Saransh · ảnh Ishita Sitwala, The Fishy Project"
# ảnh làm việc: (file, npz doodle gốc, credit)
IMGS = dict(
    khach=("source.png", "doodle_ep07.npz", PHOTO),            # ảnh 08 phòng khách (doodle)
    ngu=("source_ngu.png", "doodle_ep07_ngu.npz", PHOTO),       # ảnh 09 phòng ngủ chính (doodle)
    tong=("source_tong.png", "doodle_ep07_tong.npz", PHOTO),    # ảnh 13 sảnh ăn nhìn từ bàn ăn (doodle)
    an=("source_an.png", "doodle_ep07_an.npz", PHOTO),          # ảnh 06 sảnh ăn hai tầng (đã xoá nét)
    hl=("source_hl.png", "doodle_ep07_hl.npz", PHOTO),          # ảnh 11 hành lang lối vào (đã xoá nét)
    dg=("source_dg.png", "", "Diagram: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014)"),  # ảnh 07, cắt hàng ba khung
    mb=("source_mb.png", "", "Mặt bằng: Studio Saransh, nguồn ArchDaily (2025) · ghi chú Giả Thuyết Kiến Trúc"),  # ảnh 02, cắt vùng phòng khách và sảnh ăn (chú thích gốc đủ to)
)
SC = [
    dict(move="push", part="A", blk=1, img="an", head="Bê tông mộc: đẹp trên ảnh, lạnh khi ở?", cam=WIDE, dark=False, dd=[],
         vo="Nhà bê tông mộc lên ảnh thì đẹp, sao ở thật lại hay bị chê lạnh?"),
    dict(move="pan_l", part="B", blk=2, img="dg", head="Kilmer & Kilmer (2014): mặt trơn lạnh, vải dày ấm", cam=((1080, 465), 1.12, (540, 925)), free=True, dark=False, dd=[],
         vo="Hai tác giả Kilmer viết, phòng nhiều mặt trơn thường lạnh, còn thảm và vải dày thì ấm.",
         tts="Hai tác giả Kin-mơ viết, phòng nhiều mặt trơn thường lạnh, còn thảm và vải dày thì ấm."),
    dict(move="pull", part="C", blk=3, img="hl", head="Bê tông lạnh vì thiếu đồ mềm bên cạnh", cam=((720, 860), 3.0, (540, 900)), dark=False, dd=[],
         vo="Mà bê tông hoặc các vật liệu cứng thường gây lạnh lẽo, vì nó thường thiếu đồ mềm bên cạnh."),
    dict(move="pan_r", part="C", blk=4, img="an", head="Tường, sàn cứng dội tiếng, nên nghe vang", cam=((1150, 1500), 2.4, (540, 900)), dark=False, dd=[],
         vo="Tường, sàn cứng còn dội tiếng bước chân, nên nhà vừa trông lạnh, vừa nghe vang."),
    dict(move="push", part="D", blk=5, img="mb", head="MS House: mặt bằng tầng trệt", cam=((790, 350), 1.27, (540, 925)), free=True, dark=False, dd=[],
         vo="Thử nhìn nhà MS House ở Ấn Độ, hai tầng, xây quanh chín cây sầu đâu.",
         tts="Thử nhìn nhà Em-ét Hao-xơ ở Ấn Độ, hai tầng, xây quanh chín cây sầu đâu."),
    dict(move="pan_u", part="D", blk=5, img="khach", head="Phòng khách: trần, tường, sàn đều cứng", cam=((1310, 800), 3.0, (745, 720)), free=True, dark=True,
         dd=["arr_vo", "lab_vo"],
         vo="Ở phòng khách, trần, tường bê tông và sàn đá đều là mặt cứng."),
    dict(move="push", part="D", blk=5, img="khach", head="Trong tầm tay: mềm và ấm", cam=((272, 1690), 3.0, (322, 1080)), free=True, dark=True,
         dd=["arr_sofa", "lab_sofa"],
         vo="Còn đồ trong tầm tay thì mềm và ấm, như bộ sofa vải xù này.",
         tts="Còn đồ trong tầm tay thì mềm và ấm, như bộ sô-pha vải xù này."),
    dict(move="pull", part="D", blk=5, img="ngu", head="Phòng ngủ: gỗ ở chỗ lưng tựa", cam=((980, 700), 3.1, (540, 880)), free=True, dark=True,
         dd=["arr_dau", "lab_dau"],
         vo="Ở phòng ngủ, gỗ ốp đúng chỗ lưng tựa đầu giường, còn bê tông lùi lên cao."),
    dict(move="pan_l", part="F", blk=6, img="khach", head="Thử ở nhà mình", cam=((620, 2000), 3.0, (540, 900)), dark=False, dd=[],
         vo="Thử đổi đầu giường, lưng ghế sang gỗ, thêm thảm đay và rèm vải lanh cho đỡ vang."),
    dict(move="push", part="H", blk=6, img="tong", head="Bê tông thô: trên cao, ở xa", cam=((650, 900), 3.25, (540, 925)), free=True, dark=True,
         dd=["arr_xa", "lab_xa"],
         vo="Vậy cứ giữ bê tông, chỉ cần để mặt cứng ở xa,"),
    dict(move="pull", part="H", blk=6, img="tong", head="Gỗ, mây: ngay trong tầm tay", cam=((275, 1680), 2.4, (300, 925)), free=True, dark=True,
         dd=["arr_tam1", "arr_tam2", "lab_tam"],
         vo="còn đồ mềm thì để trong tầm tay, thì sẽ giảm cảm giác lạnh lẽo."),
    dict(move="push", part="I", blk=6, img="tong", head="end", cam="END", dark=False, vo="", dd=[],
         say="Bài phân tích về chất cảm vật liệu, nguyên tắc cứng và mềm từ sách của Kilmer, mọi người xem phần bình luận nha.",
         tts="Bài phân tích về chất cảm vật liệu, nguyên tắc cứng và mềm từ sách của Kin-mơ, mọi người xem phần bình luận nha."),
]

DOODLE = r'''
_P = os.path.join(HERE, "@NPZ@")
LAYER = dict(np.load(_P)) if os.path.isfile(_P) else {}   # toạ độ trên ảnh làm việc của run
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


# Giai đoạn B: mốc cảnh căn theo ghi âm Tap_7.mp3 (51,0 giây; nhận dạng lời bằng sherpa-onnx zipformer-vi, xem script.md):
# mỗi cảnh bắt đầu khoảng 0,35–0,4 giây trước câu của nó; cảnh cuối kéo đến hết giọng + 0,6 giây.
T_AUDIO = [0, 3.6, 8.85, 13.75, 18.45, 22.95, 26.62, 30.4, 34.8, 39.2, 42.05, 45.35, 51.6]


def times():
    if T_AUDIO:
        return list(T_AUDIO)
    T = [0.0]
    for s in SC:
        T.append(round(T[-1] + dur(s), 2))
    return T


def size(img):
    from PIL import Image
    return Image.open(OUT + IMGS[img][0]).size


def geom(img):
    """thẻ ảnh: ảnh dọc/vuông cao 1920 (2x) như tập 5, 6; ảnh ngang rộng 1920 như engine gốc"""
    sw, sh = size(img)
    if sh >= sw:
        return round(1920 * sw / sh), 1880.0
    return 1920, 1810.0


def cover(fx, fy, z, anc, img, m=40):
    """dời điểm neo để ảnh phủ kín khung 1080x1920 khi zoom"""
    sw, sh = size(img)
    k = geom(img)[0] / (2 * sw)          # px khung / px ảnh ở z=1
    sc = z * k
    assert sc * sh >= 1920 + 2 * m and sc * sw >= 1080 + 2 * m, (img, z)
    ax = min(max(anc[0], 1080 + m - sc * (sw - fx)), sc * fx - m)
    ay = min(max(anc[1], 1920 + m - sc * (sh - fy)), sc * fy - m)
    return (round(ax), round(ay))


def words(s):
    return len(s.split())


def cam_str(s, cam):
    if cam == WIDE:
        return "WIDE"
    if cam == "END":
        return "END_SAFE"
    (fx, fy), z, anc = cam
    if not s.get("free"):
        anc = cover(fx, fy, z, anc, s["img"])
    return f"(({fx}, {fy}), {z}, {anc})"


def scene_line(s, a, b, cam, dd, move=None):
    mv = move or s.get("move", "hold")
    return (f'    dict(t="{a:g}–{b:g}s", head={json.dumps(s["head"], ensure_ascii=False)}, '
            f'vo={json.dumps(s["vo"], ensure_ascii=False)},\n         cam={cam}, dark={s["dark"]}, dd={dd}, move="{mv}"),')


def wrap_data(lines, doodle):
    return ('# ---------------- scenes ----------------\nCENTER = (SW / 2, SH / 2)\nOBJ = {}\n\n'
            'WIDE = WIDE_SAFE\nSCENES = [\n' + "\n".join(lines) + '\n]\n'
            'END = len(SCENES) - 1\nBOARDS = {}\n' + doodle + '\n\n')


def runs():
    R = []
    for k, s in enumerate(SC):
        if R and SC[R[-1][-1]]["img"] == s["img"]:
            R[-1].append(k)
        else:
            R.append([k])
    return R


def build_run(T, ks):
    """dữ liệu cảnh cho một run: cảnh trước + các cảnh của run + khung cuối giả.
    Cảnh trước dùng ĐÚNG camera của cảnh đầu run, đứng yên (không zoom từ ảnh toàn cảnh vào nữa): đoạn cắt
    của run mở bằng hoà tan từ run trước (ghep_ep07.py), chữ cảnh trước mờ đi như cũ."""
    img = SC[ks[0]]["img"]
    lines, t, d0 = [], 0.0, 0.0
    if ks[0] > 0:
        prev = SC[ks[0] - 1]
        d0 = T[ks[0]] - T[ks[0] - 1]
        first = SC[ks[0]]
        lines.append(scene_line(prev, 0, d0, cam_str(first, first["cam"]), [], move="hold"))
        t = d0
    for k in ks:
        s = SC[k]
        d = T[k + 1] - T[k]
        lines.append(scene_line(s, t, t + d, cam_str(s, s["cam"]), s["dd"]))
        t += d
    if ks[-1] != len(SC) - 1:
        end = SC[-1]
        lines.append(scene_line(end, t, t + 0.5, "END_SAFE", [], move="hold"))
    return wrap_data(lines, DOODLE.replace("@NPZ@", IMGS[img][1] or "none.npz")), d0, t - d0


def build(src, dst, video, data, img, tag):
    s = open(E + src).read()
    cw, cy = geom(img)
    rep = [('CREDIT = "Ảnh dự án: [tên dự án] · [studio] · [nhiếp ảnh gia]"', f'CREDIT = "{IMGS[img][2]}"'),
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · CỨNG Ở XA, MỀM TRONG TẦM TAY"'),
           ("CARD_W2, BORDER2 = 1920, 0", f"CARD_W2, BORDER2 = {cw}, 0  # theo tỷ lệ ảnh của run"),
           ("C2 = (B2W / 2, 1810.0)", f"C2 = (B2W / 2, {cy})"),
           ("borderMode=cv2.BORDER_REFLECT)", "borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255, 0))"),
           # khung cuối: chữ khớp lời mời chủ Trang đã chỉnh trong ghi âm Tap_7.mp3
           ('(1196, "Bài viết phân tích đầy đủ", 58, 240),\n    (1260, "xem ở dòng đầu tiên", 58, 240),\n    (1348, "trong phần bình luận", 66, 255),',
            '(1196, "Bài phân tích về chất cảm vật liệu,", 54, 240),\n    (1258, "nguyên tắc cứng và mềm từ sách của Kilmer", 46, 240),\n    (1348, "xem ở phần bình luận", 66, 255),')]
    for a_, b_ in rep:
        assert a_ in s, a_
        s = s.replace(a_, b_)
    a = s.index("# ---------------- scenes")
    b = s.index('def render_scene') if not video else s.index('BOARDS["plain"] = make_board(1.0)')
    s = s[:a] + data + s[b:]
    if video:
        s = s.replace('"reel1_silent.mp4"', f'"{tag}_silent.mp4"')
    else:
        s = s.replace('"frames_v7"', f'"frames_{tag}"').replace('"storyboard_reel1_v7.png"', f'"storyboard_{tag}.png"')
    open(OUT + "engine_ep07/" + dst, "w").write(s)


T = times()
for k, s in enumerate(SC):
    s["t"] = f"{T[k]:g}–{T[k + 1]:g}s"
RUNS = []
for n, ks in enumerate(runs(), 1):
    img = SC[ks[0]]["img"]
    tag = f"r{n:02d}_{img}"
    data, d0, dl = build_run(T, ks)
    build("engine_storyboard_v7.py", f"engine_ep07_{tag}.py", False, data, img, tag)
    build("engine_video.py", f"engine_video_ep07_{tag}.py", True, data, img, tag)
    RUNS.append(dict(tag=tag, img=img, src=IMGS[img][0], scenes=[k + 1 for k in ks], t_in_main=T[ks[0]],
                     cut_from=d0, cut_len=dl + (1.0 if ks[-1] == len(SC) - 1 else 0.0),
                     first_frame=2 if ks[0] > 0 else 1))
json.dump(RUNS, open(OUT + "engine_ep07/runs.json", "w"), ensure_ascii=False, indent=1)

# ảnh bìa 1080x1920: một cảnh rộng trên ảnh 13 (bàn ăn, bê tông trên cao), tiêu đề ngắn của reel + câu móc
COVER = [dict(img="tong", head="Cứng ở xa, mềm trong tầm tay", vo="Vì sao nhà bê tông mộc hay bị chê lạnh?", dark=False),
         dict(img="tong", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep07.py", False,
      wrap_data([scene_line(COVER[0], 0, 3, "WIDE", []), scene_line(COVER[1], 3, 4, "END_SAFE", [])],
                DOODLE.replace("@NPZ@", "none.npz")), "tong", "cover")

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
print("runs", [(r["tag"], r["scenes"]) for r in RUNS])
print("tổng engine", T[-1], "giây; từ lời đọc", nw, "; ước tính giọng đọc ~", round(nw / 3.4 + 5 * 1.0, 1), "giây")
for k, x in enumerate(SC):
    print(k + 1, x["blk"], x["part"], x["t"], words(shown[k]), x["head"])
FOREIGN = ["Kilmer", "MS", "House", "Studio", "Saransh", "Ahmedabad", "teak", "sofa", "AH", "Decode"]
bad = re.findall(r"\d", " ".join(spoken)) + [w for w in FOREIGN if re.search(r"\b" + w + r"\b", " ".join(spoken))]
print("chữ số / tên nước ngoài chưa phiên âm trong bản đọc:", bad)
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep07/scenes.json", "w"), ensure_ascii=False, indent=1)
