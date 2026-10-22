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
    hl=("source_hl.png", "doodle_ep10_hl.npz", PHOTO),     # ảnh 11 hành lang lối vào (nét gốc: arr1/lab1 vân ván khuôn to, arr2/lab2 phòng trong mịn hơn)
    ph=("source_ph.png", "doodle_ep10_ph.npz", PHOTO),     # ảnh 12 phòng ngủ cô con gái (nét gốc: lab_top, arr_ke/lab_ke, arr_san/lab_san)
    dgt=("source_dgt.png", "", "Diagram: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014)"),   # ảnh 10, hàng trên: hai khoảng cách đứng xa, đứng sát
    dgc=("source_dgc.png", "", "Diagram: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014)"),   # ảnh 10, dòng kết "vân thô để chỗ nhìn xa, vân mịn để chỗ ở gần"
    dgb=("source_dgb.png", "", "Diagram: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014)"),   # ảnh 10, hàng dưới: hai vòng vân và câu kết
    mb=("source_mb.png", "", "Mặt bằng: Studio Saransh, nguồn ArchDaily (2025) · ghi chú Giả Thuyết Kiến Trúc"),  # ảnh 03, mặt bằng tầng một, cắt hai phòng ngủ tầng một và chú thích
)
SC = [
    dict(move="push", part="A", blk=1, img="hl", head="Cùng một bức tường: xa thì êm, sát thì nặng?", cam=WIDE, dark=False, dd=[],
         vo="Cùng một bức tường bê tông, sao đứng xa thấy êm, mà đứng sát lại thấy nặng nề?"),
    dict(move="pan_l", part="B", blk=2, img="dgt", head="Kilmer & Kilmer (2014): đá khối to, phòng nhỏ, khó chịu", cam=((1020, 465), 1.1, (540, 925)), free=True, dark=False, dd=[],
         vo="Sách nội thất của hai tác giả Kilmer lưu ý, đá khối to, tức là vân rất to, xây trong phòng nhỏ thì người ở thấy khó chịu.",
         tts="Sách nội thất của hai tác giả Kin-mơ lưu ý, đá khối to, tức là vân rất to, xây trong phòng nhỏ thì người ở thấy khó chịu."),
    dict(move="push", part="C", blk=2, img="dgt", head="Vân to hay nhỏ: hợp với phòng và khoảng cách nhìn", cam=((1300, 465), 1.3, (540, 900)), free=True, dark=False, dd=[],
         vo="Nghĩa là vân to hay nhỏ phải hợp với độ rộng của phòng, và với khoảng cách mình đứng nhìn."),
    dict(move="pull", part="C", blk=2, img="dgb", head="Đứng xa: chỉ còn sọc mảnh, êm", cam=((560, 390), 1.4, (540, 925)), free=True, dark=False, dd=[],
         vo="Đứng xa, vết cốp pha trên tường chỉ còn là những sọc mảnh, nhìn êm."),
    dict(move="push", part="C", blk=2, img="hl", head="Đứng sát: thấy gờ, lỗ bọt khí", cam=((830, 1050), 3.0, (540, 900)), dark=True, dd=[],
         vo="Còn đứng sát, từng gờ bê tông, từng lỗ bọt khí hiện rõ, nên bức tường thấy nặng."),
    dict(move="pan_r", part="D", blk=3, img="hl", head="MS House: vân to ở hành lang lối vào", cam=((900, 900), 2.2, (540, 900)), dark=True, dd=[],
         vo="Ở MS House, một nhà bê tông bên Ấn Độ, tụi mình để ý vân to nhất nằm ở hành lang lối vào, chỗ đi qua, nhìn từ xa.",
         tts="Ở Em-ét Hao-xơ, một nhà bê tông bên Ấn Độ, tụi mình để ý vân to nhất nằm ở hành lang lối vào, chỗ đi qua, nhìn từ xa."),
    dict(move="pull", part="D", blk=3, img="hl", head="Phòng trong: chỗ dừng lại thì mịn hơn", cam=((460, 1150), 2.4, (540, 900)), dark=True, dd=[],
         vo="Bước qua cửa vào phòng trong, chỗ người ta dừng lại lâu hơn, đã có gỗ, có thảm, mịn hơn."),
    dict(move="push", part="D", blk=3, img="mb", head="Mặt bằng tầng một: phòng ngủ trên lầu", cam=((653, 360), 1.0, (540, 925)), free=True, dark=False, dd=[],
         vo="Lên tới phòng ngủ trên lầu, vân còn nhỏ hơn nữa."),
    dict(move="pan_u", part="D", blk=3, img="ph", head="Phòng ngủ: sàn ô đá nhỏ lặp lại", cam=((600, 1700), 2.3, (540, 900)), dark=True, dd=[],
         vo="Sàn chỉ còn những ô đá nhỏ lặp lại, mắt có chi tiết để nhìn mà không thấy nặng."),
    dict(move="pan_l", part="F", blk=4, img="hl", head="Gợi ý cho nhà phố: vân rõ ở lối vào", cam=((800, 1500), 2.2, (540, 900)), dark=True, dd=[],
         vo="Tụi mình nghĩ nhà phố cũng làm được, bê tông vân rõ để ở lối vào, giếng trời,"),
    dict(move="push", part="F", blk=4, img="ph", head="Phòng ngủ trên lầu: trát vôi mịn", cam=((420, 900), 2.3, (540, 900)), dark=True, dd=[],
         vo="còn phòng ngủ trên lầu thì trát vôi mịn."),
    dict(move="pan_r", part="H", blk=5, img="dgc", head="Đi qua, nhìn xa: vân thô · Ngồi lâu, ở gần: vân mịn", cam=((1020, 184), 1.15, (540, 925)), free=True, dark=False, dd=[],
         vo="Tóm lại, chỗ đi qua, nhìn từ xa thì vân thô, chỗ ngồi lâu, ở gần thì vân mịn."),
    dict(move="push", part="I", blk=5, img="ph", head="end", cam="END", dark=False, vo="", dd=[],
         say="Bài phân tích về vân to, vân nhỏ của bề mặt từ sách của Kilmer, mọi người xem phần bình luận nha.",
         tts="Bài phân tích về vân to, vân nhỏ của bề mặt từ sách của Kin-mơ, mọi người xem phần bình luận nha."),
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


T_AUDIO = []   # giai đoạn B: điền mốc cảnh theo ghi âm


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
           # khung cuối: chữ khớp lời mời (mẫu tập 7)
           ('(1196, "Bài viết phân tích đầy đủ", 58, 240),\n    (1260, "xem ở dòng đầu tiên", 58, 240),\n    (1348, "trong phần bình luận", 66, 255),',
            '(1196, "Bài phân tích về vân to, vân nhỏ", 54, 240),\n    (1258, "của bề mặt, từ sách của Kilmer", 50, 240),\n    (1348, "xem ở phần bình luận", 66, 255),')]
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
COVER = [dict(img="ph", head="Vân thô ở xa, vân mịn ở gần", vo="Tường bê tông nhám: xa thì đẹp, sát sao lại nặng?", dark=False),
         dict(img="ph", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep10.py", False,
      wrap_data([scene_line(COVER[0], 0, 3, "WIDE", []), scene_line(COVER[1], 3, 4, "END_SAFE", [])],
                DOODLE.replace("@NPZ@", "none.npz")), "ph", "cover")

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
