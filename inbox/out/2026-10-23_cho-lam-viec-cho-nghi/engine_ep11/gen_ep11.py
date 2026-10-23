"""Tập 11: Chỗ làm việc sáng đều, chỗ nghỉ được chênh (bài 03 kho AH-Decode-Decor, mục "Chỗ làm việc cần độ sáng gần đều, còn chỗ nghỉ ngơi được phép chênh sáng nhiều hơn").
Reel nhiều ảnh theo bộ khuôn mau_tap7 (xem engine/mau_tap7/README.md). Mỗi cảnh chọn ảnh qua khoá `img` (IMGS); mỗi đoạn cảnh liên tiếp
cùng một ảnh là một "run" (engine_ep11_rNN_<ảnh>.py và engine_video_ep11_rNN_<ảnh>.py). Doodle: nét mới vẽ bằng draw_ep11.py trên ảnh gốc không doodle (anh/goc/), lộ dần theo lời."""
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
PHOTO = "Ảnh dự án: Union Street House, Melbourne · Prior Barraclough · ảnh Ben Hosking"
DGC = "Diagram: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014)"
MBC = "Mặt bằng gác lửng: Prior Barraclough, nguồn ArchDaily (2023) · ghi chú Giả Thuyết Kiến Trúc"
# ảnh làm việc: (file, npz doodle, credit). Ảnh chụp lấy từ anh/goc/ của bài (ảnh gốc không doodle), nét vẽ mới bằng draw_ep11.py
IMGS = dict(
    mo=("source_mo.png", "doodle_ep11_mo.npz", PHOTO),        # ảnh 14 (goc): bàn gác lửng khi vách lam kéo mở
    kin=("source_kin.png", "doodle_ep11_kin.npz", PHOTO),     # ảnh 13 (goc): cùng bàn khi vách lam kéo kín
    togo=("source_togo.png", "doodle_ep11_togo.npz", PHOTO),  # ảnh 15 (goc): ghế Togo sát mặt kính phòng khách
    tong=("source_tong.png", "", PHOTO),                      # ảnh 17 (goc): ảnh tổng bếp, bàn ăn, vách lam gác lửng
    dga=("source_dga.png", "", DGC),                          # ảnh 12: diagram ba vùng sáng, dải hình vẽ (bỏ tiêu đề)
    dgb=("source_dgb.png", "", DGC),                          # ảnh 12: dải thang năm lần + dòng kết
    mb=("source_mb.png", "", MBC),                            # ảnh 03: mặt bằng gác lửng (cắt vùng chú thích)
)
def MO(fx, fy=666):
    """ảnh ngang 3:2 zoom kín khung (z 2.05): mép trên ảnh ~230, mép dưới ~1540, chữ trắng trên ảnh"""
    return ((fx, fy), 2.05, (540, round(230 + 0.984 * fy)))


def STRIP(cx, cy):
    """dải bản vẽ 2:1 (hoặc dẹt hơn) rộng ~1040 px, nằm gọn y ~603–1123 để tiêu đề ở trên, phụ đề ba dòng ở dưới"""
    return ((cx, cy), 1.083, (540, 863))


SC = [
    dict(move="push", part="A", blk=1, img="mo", head="Bàn cạnh kính vườn, sao trông tối?", cam=MO(1000), free=True, dark=True, dd=[],
         vo="Bàn làm việc kê ngay cạnh mảng kính vườn, sao mặt bàn lại trông tối?"),
    dict(move="pan_r", part="C", blk=2, img="mo", head="Mắt chỉnh theo chỗ sáng nhất", cam=MO(1085), free=True, dark=True, dd=["g_ring", "g_arr", "lab_g"],
         vo="Vì theo cách tụi mình hiểu, mắt tự chỉnh theo chỗ sáng nhất trong tầm nhìn."),
    dict(move="pan_l", part="C", blk=2, img="mo", head="Kính sáng quá, mặt bàn trông tối", cam=MO(640), free=True, dark=True, dd=["d_arr", "lab_d"],
         vo="Nên mảng kính sáng quá thì mọi thứ còn lại, kể cả trang sách trên bàn, đều trông tối đi."),
    dict(move="push", part="B", blk=2, img="dgb", head="Kilmer & Kilmer (2014): không chênh quá năm lần", cam=STRIP(1060, 310), free=True, dark=False, dd=[],
         vo="Sách nội thất của hai tác giả Kilmer khuyên, lúc làm việc, tường và sàn không nên sáng hơn hay tối hơn trang sách quá năm lần.",
         tts="Sách nội thất của hai tác giả Kin-mơ khuyên, lúc làm việc, tường và sàn không nên sáng hơn hay tối hơn trang sách quá năm lần."),
    dict(move="pan_u", part="D", blk=3, img="mb", head="Union Street House: bàn trên gác lửng", cam=STRIP(950, 475), free=True, dark=False, dd=[],
         vo="Thử nhìn nhà Union Street ở Melbourne. Bàn làm việc trên gác lửng, sát mép thông tầng, nhìn qua là thấy mảng kính vườn.",
         tts="Thử nhìn nhà Diu-ni-ơn Xtrít ở Meo-bơn. Bàn làm việc trên gác lửng, sát mép thông tầng, nhìn qua là thấy mảng kính vườn."),
    dict(move="pull", part="D", blk=3, img="kin", head="Vách lam kéo kín: chỉ còn tường gỗ", cam=((1010, 1100), 2.3, (540, 925)), dark=True, dd=["v_out", "v_arr", "lab_v", "lab_w"],
         vo="Nên dọc mép gác có một vách lam gỗ trượt. Kéo kín lại, trong tầm mắt không còn mảng kính nào, trước mặt chỉ còn tường gỗ."),
    dict(move="hold", part="D", blk=3, img="mo", head="Kín hay mở: người ngồi tự chọn", cam=MO(1450), free=True, dark=True, dd=["s_out", "s_arr1", "s_arr2", "lab_s"],
         vo="Nhà thiết kế không cố làm chỗ làm việc lúc nào cũng sáng đều, mà để người ngồi tự chọn kéo kín hay mở."),
    dict(move="push", part="D", blk=3, img="togo", head="Phòng khách: chỗ nghỉ được chênh", cam=((800, 1250), 2.2, (540, 925)), dark=True, dd=["k_arr", "lab_k", "t_arr", "lab_t"],
         vo="Còn ghế Togo dưới phòng khách đặt sát kính, tường gỗ quanh ghế tối hơn nhiều. Nhưng đó là chỗ nghỉ, nên chênh vẫn được.",
         tts="Còn ghế Tô-gô dưới phòng khách đặt sát kính, tường gỗ quanh ghế tối hơn nhiều. Nhưng đó là chỗ nghỉ, nên chênh vẫn được."),
    dict(move="pan_l", part="F", blk=4, img="mo", head="Thử ở nhà: nheo mắt nhìn", cam=MO(1000), free=True, dark=True, dd=["n_ring", "n_arr", "lab_n"],
         vo="Vậy ở nhà, ngồi đúng chỗ làm việc giữa chiều rồi nheo mắt. Nếu chỉ còn thấy rõ ô cửa, chênh sáng đang quá lớn."),
    dict(move="pan_d", part="F", blk=4, img="kin", head="Xoay bàn, thêm rèm hay vách lam", cam=((900, 1300), 2.2, (540, 925)), dark=True, dd=["b_arr", "lab_b"],
         vo="Khi đó, xoay bàn vuông góc với cửa sổ, hoặc thêm tấm rèm hay vách lam kéo được giữa bàn và mảng kính."),
    dict(move="pull", part="H", blk=5, img="tong", head="Làm việc: sáng đều. Nghỉ: được chênh", cam=MO(1000), free=True, dark=True, dd=[],
         vo="Tóm lại, lúc làm việc đừng để mảng kính sáng nằm trong tầm mắt. Còn chỗ nghỉ thì cứ để chênh."),
    dict(move="push", part="I", blk=5, img="tong", head="end", cam="END", dark=False, vo="", dd=[],
         say="Còn bài phân tích đầy đủ về ánh sáng tự nhiên trong nhà, mọi người xem phần bình luận nha.",
         tts="Còn bài phân tích đầy đủ về ánh sáng tự nhiên trong nhà, mọi người xem phần bình luận nha."),
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


# Giai đoạn B: điền mốc cảnh theo ghi âm (mỗi cảnh bắt đầu khoảng 0,35–0,4 giây trước câu của nó). Giai đoạn A để trống.
T_AUDIO = []


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
    của run mở bằng hoà tan từ run trước (ghep_ep11.py), chữ cảnh trước mờ đi như cũ."""
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
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · CHÊNH SÁNG THEO VIỆC"'),
           ("CARD_W2, BORDER2 = 1920, 0", f"CARD_W2, BORDER2 = {cw}, 0  # theo tỷ lệ ảnh của run"),
           ("C2 = (B2W / 2, 1810.0)", f"C2 = (B2W / 2, {cy})"),
           ("borderMode=cv2.BORDER_REFLECT)", "borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255, 0))"),
           # cảnh nối không chữ (trước khung cuối): không vẽ header, không phủ tối dải chữ
           ("    t.put((60, SAFE_Y0 + 4), HEAD, 34, 220)\n", "    if sc[\"head\"]:\n        t.put((60, SAFE_Y0 + 4), HEAD, 34, 220)\n"),
           ("    return top < TOP_END, bot > cr_y - 20, warn", "    return top < TOP_END and bool(sc[\"head\"]), bot > cr_y - 20 and bool(sc[\"vo\"]), warn"),
           # khung cuối: chữ khớp lời mời (mẫu tập 7)
           ('(1196, "Bài viết phân tích đầy đủ", 58, 240),\n    (1260, "xem ở dòng đầu tiên", 58, 240),\n    (1348, "trong phần bình luận", 66, 255),',
            '(1196, "Bài phân tích đầy đủ", 58, 240),\n    (1260, "về ánh sáng tự nhiên trong nhà", 52, 240),\n    (1344, "xem ở phần bình luận", 66, 255),')]
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
    open(OUT + "engine_ep11/" + dst, "w").write(s)


T = times()
for k, s in enumerate(SC):
    s["t"] = f"{T[k]:g}–{T[k + 1]:g}s"
RUNS = []
for n, ks in enumerate(runs(), 1):
    img = SC[ks[0]]["img"]
    tag = f"r{n:02d}_{img}"
    data, d0, dl = build_run(T, ks)
    build("engine_storyboard_v7.py", f"engine_ep11_{tag}.py", False, data, img, tag)
    build("engine_video.py", f"engine_video_ep11_{tag}.py", True, data, img, tag)
    RUNS.append(dict(tag=tag, img=img, src=IMGS[img][0], scenes=[k + 1 for k in ks], t_in_main=T[ks[0]],
                     cut_from=d0, cut_len=dl + (1.0 if ks[-1] == len(SC) - 1 else 0.0),
                     first_frame=2 if ks[0] > 0 else 1))
json.dump(RUNS, open(OUT + "engine_ep11/runs.json", "w"), ensure_ascii=False, indent=1)

# ảnh bìa 1080x1920: cảnh rộng trên ảnh 14 (bàn gác lửng nhìn ra kính vườn), tiêu đề ngắn + câu móc
COVER = [dict(img="mo", head="Bàn cạnh kính vườn, sao trông tối?", vo="Chỗ làm việc nên sáng gần đều, chỗ nghỉ thì được chênh.", dark=False),
         dict(img="mo", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep11.py", False,
      wrap_data([scene_line(COVER[0], 0, 3, "WIDE", []), scene_line(COVER[1], 3, 4, "END_SAFE", [])],
                DOODLE.replace("@NPZ@", "none.npz")), "mo", "cover")

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
FOREIGN = ["Kilmer", "Union", "Street", "House", "Melbourne", "Togo", "Prior", "Barraclough", "AH", "Decode"]
bad = re.findall(r"\d", " ".join(spoken)) + [w for w in FOREIGN if re.search(r"\b" + w + r"\b", " ".join(spoken))]
print("chữ số / tên nước ngoài chưa phiên âm trong bản đọc:", bad)
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep11/scenes.json", "w"), ensure_ascii=False, indent=1)
