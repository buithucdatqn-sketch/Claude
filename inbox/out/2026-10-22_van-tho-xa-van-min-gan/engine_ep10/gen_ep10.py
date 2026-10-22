"""Tập 10: Vân thô ở xa, vân mịn ở gần (bài 02 kho AH-Decode-Decor, mục "Độ thô của bề mặt phải hợp với kích thước phòng và khoảng cách nhìn").
Reel nhiều ảnh theo bộ khuôn mau_tap7 (xem engine/mau_tap7/README.md). Mỗi cảnh chọn ảnh qua khoá `img` (IMGS); mỗi đoạn cảnh liên tiếp
cùng một ảnh là một "run" (engine_ep10_rNN_<ảnh>.py và engine_video_ep10_rNN_<ảnh>.py). Doodle: không vẽ nét mới, lộ dần chính nét gốc của bài."""
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
    a39=("source_a39.png", "", PHOTO),                         # ArchDaily 39: mặt ngoài nhìn từ vườn (ảnh ngoài bài)
    a26=("source_a26.png", "doodle_ep10_a26.npz", PHOTO),      # ArchDaily 26: mặt ngoài nhìn xa, tường vân cốp pha
    a24=("source_a24.png", "doodle_ep10_a24.npz", PHOTO),      # ArchDaily 24: tường bê tông nhìn sát (gờ, lỗ bọt khí)
    hl=("source_hl.png", "doodle_ep10_hl.npz", PHOTO),         # ảnh 11 của bài: hành lang lối vào (nền sạch, nét mới)
    a29=("source_a29.png", "doodle_ep10_a29.npz", PHOTO),      # ArchDaily 29: phòng khách, bê tông ván ép
    a6c=("source_a6c.png", "doodle_ep10_a6c.npz", PHOTO),      # ArchDaily 6 (cắt nửa dưới): phòng ngủ con gái, sàn ô đá nhỏ
    ph=("source_ph.png", "doodle_ep10_ph.npz", PHOTO),         # ảnh 12 của bài: phòng ngủ, tường vôi (nền sạch, nét mới)
    dgt=("source_dgt.png", "", "Diagram: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014)"),   # ảnh 10, hàng trên
    dgc=("source_dgc.png", "", "Diagram: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014)"),   # ảnh 10, dòng kết
    mb=("source_mb.png", "", "Mặt bằng: Studio Saransh, nguồn ArchDaily (2025) · ghi chú Giả Thuyết Kiến Trúc"),  # ảnh 03, mặt bằng tầng một
)
SC = [
    dict(move="push", part="A", blk=1, img="a39", head="Cùng một bức tường: xa thì êm, sát thì nặng?", cam=WIDE, dark=False, dd=[],
         vo="Cùng một bức tường, sao đứng xa thấy êm, mà đứng sát lại thấy nặng nề?"),
    dict(move="pan_l", part="B", blk=2, img="dgt", head="Kilmer & Kilmer (2014): đá khối to, phòng nhỏ, khó chịu", cam=((1020, 465), 1.1, (540, 925)), free=True, dark=False, dd=[],
         vo="Sách nội thất của hai tác giả Kilmer lưu ý, đá khối to, tức là vân rất to, xây trong phòng nhỏ thì người ở thấy khó chịu.",
         tts="Sách nội thất của hai tác giả Kin-mơ lưu ý, đá khối to, tức là vân rất to, xây trong phòng nhỏ thì người ở thấy khó chịu."),
    dict(move="push", part="C", blk=2, img="dgt", head="Vân to hay nhỏ: hợp với phòng và khoảng cách nhìn", cam=((1300, 465), 1.3, (540, 900)), free=True, dark=False, dd=[],
         vo="Nghĩa là vân to hay nhỏ phải hợp với độ rộng của phòng, và với khoảng cách mình đứng nhìn."),
    dict(move="pull", part="C", blk=2, img="a26", head="Đứng xa: chỉ còn sọc mảnh, êm", cam=((1100, 950), 2.1, (540, 900)), dark=True, dd=["out", "lab"],
         vo="Đứng xa, vết cốp pha trên tường chỉ còn là những sọc mảnh, nhìn êm."),
    dict(move="push", part="C", blk=2, img="a24", head="Đứng sát: thấy gờ, lỗ bọt khí", cam=((600, 1300), 3.0, (540, 900)), dark=True, dd=["lab", "arr", "ring"],
         vo="Còn đứng sát, từng gờ bê tông, từng lỗ bọt khí hiện rõ, nên bức tường thấy nặng."),
    dict(move="pan_r", part="D", blk=3, img="hl", head="MS House: vân to ở hành lang lối vào", cam=((900, 900), 2.2, (540, 900)), dark=True, dd=["out", "lab", "arr"],
         vo="Ở MS House, một nhà bê tông bên Ấn Độ, tụi mình để ý vân to nhất nằm ở hành lang lối vào, chỗ đi qua, nhìn từ xa.",
         tts="Ở Em-ét Hao-xơ, một nhà bê tông bên Ấn Độ, tụi mình để ý vân to nhất nằm ở hành lang lối vào, chỗ đi qua, nhìn từ xa."),
    dict(move="pull", part="D", blk=3, img="a29", head="Phòng khách: bê tông ván ép, mặt mịn hơn", cam=((1000, 667), 0.88, (540, 915)), free=True, dark=False, dd=["out", "lab"],
         vo="Còn phòng khách là chỗ ngồi lâu, nên bê tông ở đó đổ bằng ván ép, mặt mịn hơn."),
    dict(move="push", part="D", blk=3, img="mb", head="Mặt bằng tầng một: phòng ngủ trên lầu", cam=((653, 360), 1.0, (540, 925)), free=True, dark=False, dd=[],
         vo="Lên tới phòng ngủ trên lầu, vân còn nhỏ hơn nữa."),
    dict(move="pan_u", part="D", blk=3, img="a6c", head="Phòng ngủ: sàn ô đá nhỏ lặp lại", cam=((800, 625), 0.78, (540, 920)), free=True, dark=False, dd=["lab", "arr", "ring"],
         vo="Sàn chỉ còn những ô đá nhỏ lặp lại, mắt có chi tiết để nhìn mà không thấy nặng."),
    dict(move="pan_l", part="E", blk=4, img="ph", head="Chỗ tiếp xúc gần: chọn vật liệu cho khéo", cam=((450, 1150), 2.3, (540, 900)), dark=True, dd=["lab", "arr"],
         vo="Cũng vì vậy, nội thất của những ngôi nhà bê tông trần nếu không khéo cân nhắc vật liệu cho những khu vực tiếp xúc gần,"),
    dict(move="push", part="E", blk=4, img="hl", head="Bê tông trần ở sát người: dễ lạnh", cam=((800, 1150), 2.3, (540, 900)), dark=True, dd=[],
         vo="thì cảm giác ở sẽ rất lạnh."),
    dict(move="pan_r", part="H", blk=5, img="dgc", head="Đi qua, nhìn xa: vân thô · Ngồi lâu, ở gần: vân mịn", cam=((1020, 184), 1.15, (540, 925)), free=True, dark=False, dd=[],
         vo="Tóm lại, chỗ đi qua, nhìn từ xa thì vân thô, chỗ ngồi lâu, ở gần thì vân mịn."),
    dict(move="push", part="I", blk=5, img="a26", head="end", cam="END", dark=False, vo="", dd=[],
         say="Bài phân tích về vân to, vân nhỏ của bề mặt và nguyên tắc phối vật liệu cứng mềm theo luật xa gần từ sách của Kilmer, mọi người xem phần bình luận nhá.",
         tts="Bài phân tích về vân to, vân nhỏ của bề mặt và nguyên tắc phối vật liệu cứng mềm theo luật xa gần từ sách của Kin-mơ, mọi người xem phần bình luận nhá."),
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


# Giai đoạn B: mốc cảnh theo ghi âm van-tho-xa-van-min-gan.mp3 (66,85 giây; nhận dạng lời bằng sherpa-onnx zipformer-vi, xem script.md):
# mỗi cảnh bắt đầu khoảng 0,35–0,4 giây trước câu của nó; cảnh cuối kéo đến hết giọng + 0,6 giây.
T_AUDIO = [0, 4.85, 13.05, 17.95, 22.27, 27.72, 34.95, 39.57, 42.16, 46.55, 51.94, 53.6, 59.22, 67.45]


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
    của run mở bằng hoà tan từ run trước (ghep_ep10.py), chữ cảnh trước mờ đi như cũ."""
    img = SC[ks[0]]["img"]
    lines, t, d0 = [], 0.0, 0.0
    if ks[0] > 0:
        prev = SC[ks[0] - 1]
        d0 = T[ks[0]] - T[ks[0] - 1]
        first = SC[ks[0]]
        if first["cam"] == "END":   # thẻ ảnh khung cuối đè vùng tiêu đề: cảnh nối không chữ (engine bỏ phủ tối khi không có chữ)
            prev = dict(prev, head="", vo="")
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
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · VÂN THÔ Ở XA, VÂN MỊN Ở GẦN"'),
           ("CARD_W2, BORDER2 = 1920, 0", f"CARD_W2, BORDER2 = {cw}, 0  # theo tỷ lệ ảnh của run"),
           ("C2 = (B2W / 2, 1810.0)", f"C2 = (B2W / 2, {cy})"),
           ("borderMode=cv2.BORDER_REFLECT)", "borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255, 0))"),
           # cảnh nối không chữ (trước khung cuối): không vẽ header, không phủ tối dải chữ
           ("    t.put((60, SAFE_Y0 + 4), HEAD, 34, 220)\n", "    if sc[\"head\"]:\n        t.put((60, SAFE_Y0 + 4), HEAD, 34, 220)\n"),
           ("    return top < TOP_END, bot > cr_y - 20, warn", "    return top < TOP_END and bool(sc[\"head\"]), bot > cr_y - 20 and bool(sc[\"vo\"]), warn"),
           # khung cuối: chữ khớp lời mời (mẫu tập 7)
           ('(1196, "Bài viết phân tích đầy đủ", 58, 240),\n    (1260, "xem ở dòng đầu tiên", 58, 240),\n    (1348, "trong phần bình luận", 66, 255),',
            '(1180, "Bài phân tích về vân to, vân nhỏ của bề mặt", 44, 240),\n    (1232, "và nguyên tắc phối vật liệu cứng mềm", 44, 240),\n    (1284, "theo luật xa gần, từ sách của Kilmer", 44, 240),\n    (1364, "xem ở phần bình luận", 62, 255),')]
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
    open(OUT + "engine_ep10/" + dst, "w").write(s)


T = times()
for k, s in enumerate(SC):
    s["t"] = f"{T[k]:g}–{T[k + 1]:g}s"
RUNS = []
for n, ks in enumerate(runs(), 1):
    img = SC[ks[0]]["img"]
    tag = f"r{n:02d}_{img}"
    data, d0, dl = build_run(T, ks)
    build("engine_storyboard_v7.py", f"engine_ep10_{tag}.py", False, data, img, tag)
    build("engine_video.py", f"engine_video_ep10_{tag}.py", True, data, img, tag)
    RUNS.append(dict(tag=tag, img=img, src=IMGS[img][0], scenes=[k + 1 for k in ks], t_in_main=T[ks[0]],
                     cut_from=d0, cut_len=dl + (1.0 if ks[-1] == len(SC) - 1 else 0.0),
                     first_frame=2 if ks[0] > 0 else 1))
json.dump(RUNS, open(OUT + "engine_ep10/runs.json", "w"), ensure_ascii=False, indent=1)

# ảnh bìa 1080x1920: cảnh rộng trên ảnh 12 (kệ gỗ, tường vôi, sàn ô đá nhỏ), tiêu đề ngắn + câu móc
COVER = [dict(img="a26", head="Vân thô ở xa, vân mịn ở gần", vo="Cùng một bức tường, sao đứng xa thấy êm, mà đứng sát lại thấy nặng nề?", dark=False),
         dict(img="a26", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep10.py", False,
      wrap_data([scene_line(COVER[0], 0, 3, "WIDE", []), scene_line(COVER[1], 3, 4, "END_SAFE", [])],
                DOODLE.replace("@NPZ@", "none.npz")), "a26", "cover")

# ---- elevenlabs.txt: năm khối kịch bản nối bằng thẻ ngắt 1,2 giây (theo prompt của routine) ----
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
FOREIGN = ["Kilmer", "MS", "House", "Studio", "Saransh", "Ahmedabad", "terrazzo", "AH", "Decode"]
bad = re.findall(r"\d", " ".join(spoken)) + [w for w in FOREIGN if re.search(r"\b" + w + r"\b", " ".join(spoken))]
print("chữ số / tên nước ngoài chưa phiên âm trong bản đọc:", bad)
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep10/scenes.json", "w"), ensure_ascii=False, indent=1)
