"""Tập 18 (bài 05 bài học 2, Kilmer & Kilmer 2014): tủ trắng kín tường, bếp trông như lùi ra sau. Mã gốc từ gen_ep17.py.
Ảnh chụp Lane Cove House (anh/goc/ của bài, ảnh Rory Gardiner) phủ kín khung, nét doodle trắng vẽ mới bằng draw_ep18.py;
sơ đồ "độ sáng" (anh/01 của bài, cắt một hàng) và mặt bằng vị trí chụp (anh/vi-tri-chup/07, thêm nét cam bằng mb_ep18.py)
dựng bằng chế độ SKETCH (nét hiện dần trên nền trắng, lớp nét tách bằng sketch_ep18.py)."""
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
LCH = "Ảnh dự án: Lane Cove House · Lachlan Seegers Architect · ảnh Rory Gardiner"
IMGS = dict(
    bep=("source_bep.png", "doodle_ep18_bep.npz", LCH),      # bếp: dãy tủ trắng, đảo đá (2000x2500, anh/goc/07)
    an=("source_an.png", "doodle_ep18_an.npz", LCH),         # phòng ăn nhìn thẳng dãy tủ (2500x2000, anh/goc/05)
    hanh=("source_hanh.png", "doodle_ep18_hanh.npz", LCH),   # hành lang (1996x2500, anh/goc/06)
    sang=("source_sang.png", "sketch_ep18_sang.npz", "Hình: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014)", True),   # hàng "độ sáng" của anh/01 (1080x307)
    mb=("source_mb.png", "sketch_ep18_mb.npz", "Mặt bằng: Lachlan Seegers Architect (qua ArchDaily), ghi chú Giả Thuyết Kiến Trúc", True),   # 920x900
)


def STRIP(cx, cy, z=1.0, ay=900):
    """thẻ sơ đồ nằm gọn giữa hai khối chữ (y ~610–1240)"""
    return ((cx, cy), z, (540, ay))


# Ảnh chụp phủ kín khung (free=False, cover tự neo). Ảnh dọc 2000x2500 ở zoom 2,2 chỉ lia dọc được trong khoảng hẹp
# (điểm nhìn y ~1140–1275), nên nhãn doodle đặt ở y ảnh ~830–1570 để rơi vào dải y 610–1240 của khung.
BEP_A = ((1050, 1230), 2.15, (540, 925))     # cảnh rộng: dãy tủ, đảo đá, bàn ăn
BEP_K = ((1150, 1200), 2.2, (540, 925))      # khối tủ trên cao
BEP_L = ((1000, 1250), 2.2, (540, 925))      # tủ lùi ra sau, đảo đá phía trước
AN = ((1150, 960), 2.65, (540, 925))         # dãy tủ nhìn thẳng từ bàn ăn
HANH = ((998, 1300), 2.3, (540, 925))        # hai tường dọc hành lang
SANG = STRIP(540, 153, 1.0, 905)
MB = STRIP(460, 450, 0.75, 905)

# Một câu hỏi trung tâm: nhà hẹp sợ tủ bếp kịch trần làm bếp trông chật; vì sao dãy tủ trắng kín tường ở Lane Cove lại trông như lùi ra sau?
# Mạch: móc → nguồn Kilmer 2014 (tường trắng trông rộng hơn; sáng lùi, tối tiến; sơ đồ vẽ dần) → cơ chế của bài (đường tối cho mắt mốc đo
# khoảng cách, kéo tường lại gần; chỉ sơn trắng chưa đủ) → Lane Cove (mặt bằng: dãy tủ trọn bức tường) → cánh phẳng, khe mảnh, không tay nắm
# → không còn đường tối, thành bức tường trắng → màu sáng lùi, mảng tủ lùi ra sau → chốt (sáng và trơn = ít đường tối) → hành lang nhà ống → lời mời.
SC = [
    dict(move="push", part="A", blk=1, img="bep", head="Tủ kịch trần mà bếp không chật?", cam=BEP_A, dark=True, dd=[],
         vo="Nhiều nhà hẹp ngại đóng tủ bếp cao kịch trần, vì sợ bếp trông chật hơn."),
    dict(move="hold", part="A", blk=1, img="bep", head="Tủ kịch trần mà bếp không chật?", cam=BEP_A, dark=True, dd=[],
         vo="Vậy mà dãy tủ trắng kín cả bức tường ở căn bếp này lại trông như lùi ra sau, vì sao?"),
    dict(move="hold", part="B", blk=2, img="sang", head="Theo Kilmer & Kilmer (2014)", cam=SANG, free=True, dark=False, dd=["tieu", "mat", "sang"], keep=[],
         vo="Trong sách năm 2014, hai tác giả Rosemary và Otie Kilmer viết rằng phòng có tường trắng, hay sơn màu lạnh thật nhạt,",
         tts="Trong sách năm hai nghìn không trăm mười bốn, hai tác giả Rô-dơ-me-ri và Ô-ti Kin-mơ viết rằng phòng có tường trắng, hay sơn màu lạnh thật nhạt,"),
    dict(move="hold", part="B", blk=2, img="sang", head="Theo Kilmer & Kilmer (2014)", cam=SANG, free=True, dark=False, dd=[], keep=["tieu", "mat", "sang"],
         vo="thường trông rộng hơn phòng sơn màu ấm và tối."),
    dict(move="hold", part="B", blk=2, img="sang", head="Màu sáng lùi ra, màu tối tiến lại", cam=SANG, free=True, dark=False, dd=["toi"], keep=["tieu", "mat", "sang"],
         vo="Theo hai tác giả, màu sáng có vẻ lùi ra xa, còn màu tối có vẻ tiến lại gần."),
    dict(move="hold", part="C", blk=3, img="sang", head="Đường tối kéo bức tường lại gần", cam=SANG, free=True, dark=False, dd=[], keep=["tieu", "mat", "sang", "toi"],
         vo="Bài phân tích của tụi mình cho rằng cạnh tủ, tay nắm, khung cửa hay đường ron trên mặt tường đều là những đường tối,"),
    dict(move="hold", part="C", blk=3, img="sang", head="Đường tối kéo bức tường lại gần", cam=SANG, free=True, dark=False, dd=[], keep=["tieu", "mat", "sang", "toi"],
         vo="cho mắt một mốc để đo khoảng cách, nên mỗi đường như vậy lại kéo bức tường lại gần."),
    dict(move="hold", part="C", blk=3, img="sang", head="Chỉ sơn tường trắng thì chưa đủ", cam=SANG, free=True, dark=False, dd=[], keep=["tieu", "mat", "sang", "toi"],
         vo="Vì thế, chỉ sơn tường trắng thì chưa đủ."),
    dict(move="hold", part="D", blk=4, img="mb", head="Lane Cove House, Sydney", cam=MB, free=True, dark=False, dd=["mb"], keep=[],
         vo="Căn bếp ở đầu video, trong nhà Lane Cove ở Sydney, làm đúng điều này.",
         tts="Căn bếp ở đầu video, trong nhà Lên Cô-vơ ở Xít-ni, làm đúng điều này."),
    dict(move="hold", part="D", blk=4, img="mb", head="Dãy tủ chạy trọn một bức tường", cam=MB, free=True, dark=False, dd=["tu"], keep=["mb"],
         vo="Trên mặt bằng, dãy tủ chạy trọn bức tường phía sau đảo bếp."),
    dict(move="pan_r", part="D", blk=5, img="an", head="Cánh phẳng, khe mảnh, không tay nắm", cam=AN, dark=True, dd=["cao", "lab_cao", "khe", "lab_khe"],
         vo="Dãy tủ cao từ sàn lên sát trần, cánh tủ phẳng và trắng, không có tay nắm lộ ra, còn khe giữa các cánh rất mảnh."),
    dict(move="push", part="D", blk=6, img="bep", head="Mặt tủ gần như không còn đường tối", cam=BEP_K, dark=True, dd=["khoi", "lab_khoi"],
         vo="Mặt tủ gần như không còn đường tối nào, nên cả dãy tủ trông như một bức tường trắng chứ không còn như một món đồ."),
    dict(move="pan_d", part="D", blk=7, img="bep", head="Màu sáng lùi, mảng tủ lùi ra sau", cam=BEP_L, dark=True, dd=["lui", "lab_lui"],
         vo="Mà màu sáng thì lùi ra xa, nên trong ảnh này cả mảng tủ lùi hẳn ra sau,"),
    dict(move="hold", part="D", blk=7, img="bep", head="Màu sáng lùi, mảng tủ lùi ra sau", cam=BEP_L, dark=True, dd=["dao", "lab_dao"],
         vo="nhường chỗ cho đảo đá và bàn ăn đứng phía trước."),
    dict(move="pull", part="H", blk=8, img="bep", head="Mặt tủ sáng và trơn, ít đường tối", cam=BEP_A, dark=True, dd=[],
         vo="Tủ kịch trần vì vậy không làm bếp trông chật hơn, miễn là mặt tủ được giữ thật sáng và trơn, nghĩa là ít đường tối."),
    dict(move="pan_u", part="F", blk=9, img="hanh", head="Hành lang nhà ống cũng giữ tường sáng, trơn", cam=HANH, dark=True, dd=["tuong", "lab_tuong"],
         vo="Với hành lang dài và hẹp của nhà ống, tụi mình cũng khuyên giữ hai tường dọc thật sáng và trơn như vậy."),
    dict(move="hold", part="I", blk=10, img="bep", head="end", cam="END", dark=False, vo="", dd=[],
         say="Bài phân tích về màu tiến, màu lùi từ sách của hai tác giả Kilmer, mọi người xem ở phần bình luận nha.",
         tts="Bài phân tích về màu tiến, màu lùi từ sách của hai tác giả Kin-mơ, mọi người xem ở phần bình luận nha."),
]

DOODLE = r'''
_P = os.path.join(HERE, "@NPZ@")
LAYER = dict(np.load(_P)) if os.path.isfile(_P) else {}   # toạ độ trên ảnh làm việc của run
RAD = 0.9                              # bán kính chấm bút khi lộ lại nét gốc (px ảnh làm việc)
RAD_SK = 0.95                          # sơ đồ vẽ dần: chấm bút phủ đúng điểm mực của sơ đồ


def keep_mask(i, cam):
    """sơ đồ vẽ dần: các nhóm nét đã vẽ ở cảnh trước trong cùng run (khoá keep) hiện đủ ngay từ đầu cảnh"""
    m = np.zeros((H * SS, W * SS), np.uint8)
    rr = max(1, int(round(RAD_SK * cam.s * SS)))
    for k in SCENES[i].get("keep", []):
        for p in LAYER[k]:
            x, y = cam.pt((float(p[0]), float(p[1])))
            cv2.circle(m, (int(x * SS), int(y * SS)), rr, 255, -1, cv2.LINE_AA)
    return cv2.resize(m, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255


def _stamp(wb, pts, r_src):
    """lộ lại nét doodle gốc theo đúng thứ tự vẽ (mỗi điểm là một chấm bút)"""
    if SKETCH:
        r_src = RAD_SK
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
T_AUDIO = []   # giai đoạn B: điền theo ghi âm


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


def scene_line(s, a, b, cam, dd, move=None, keep=None):
    mv = move or s.get("move", "hold")
    keep = s.get("keep", []) if keep is None else keep
    return (f'    dict(t="{a:g}–{b:g}s", head={json.dumps(s["head"], ensure_ascii=False)}, '
            f'vo={json.dumps(s["vo"], ensure_ascii=False)},\n         cam={cam}, dark={s["dark"]}, dd={dd}, keep={keep}, move="{mv}"),')


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
    của run mở bằng hoà tan từ run trước (ghep_ep17.py), chữ cảnh trước mờ đi như cũ."""
    img = SC[ks[0]]["img"]
    lines, t, d0 = [], 0.0, 0.0
    if ks[0] > 0:
        prev = SC[ks[0] - 1]
        d0 = T[ks[0]] - T[ks[0] - 1]
        first = SC[ks[0]]
        if first["cam"] == "END":   # thẻ ảnh khung cuối đè vùng tiêu đề: cảnh nối không chữ (engine bỏ phủ tối khi không có chữ)
            prev = dict(prev, head="", vo="")
        lines.append(scene_line(prev, 0, d0, cam_str(first, first["cam"]), [], move="hold", keep=[]))
        t = d0
    for k in ks:
        s = SC[k]
        d = T[k + 1] - T[k]
        lines.append(scene_line(s, t, t + d, cam_str(s, s["cam"]), s["dd"]))
        t += d
    if ks[-1] != len(SC) - 1:
        end = SC[-1]
        lines.append(scene_line(end, t, t + 0.5, "END_SAFE", [], move="hold", keep=[]))
    return wrap_data(lines, DOODLE.replace("@NPZ@", IMGS[img][1] or "none.npz")), d0, t - d0


def build(src, dst, video, data, img, tag):
    s = open(E + src).read()
    cw, cy = geom(img)
    rep = [('CREDIT = "Ảnh dự án: [tên dự án] · [studio] · [nhiếp ảnh gia]"', f'CREDIT = "{IMGS[img][2]}"'),
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · TỦ TRẮNG KÍN TƯỜNG"'),
           ("CARD_W2, BORDER2 = 1920, 0", f"CARD_W2, BORDER2 = {cw}, 0  # theo tỷ lệ ảnh của run"),
           ("C2 = (B2W / 2, 1810.0)", f"C2 = (B2W / 2, {cy})"),
           ("borderMode=cv2.BORDER_REFLECT)", "borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255, 0))"),
           # khung cuối: thẻ ảnh nằm gọn giữa y ~340–960 (trong khung 4:5 của bảng tin, không bị cắt góc), giữa màn hình theo chiều ngang
           ('(1040, "AH Decode · series phân tích nguyên tắc thiết kế", 40, 215),\n    (1088, "và cách chọn đồ decor", 40, 215),', '(1124, "AH Decode · series phân tích nguyên tắc thiết kế", 40, 215),\n    (1170, "và cách chọn đồ decor", 40, 215),'),
           ("END_Z = min(0.8, 760.0 / (CARD_H2 / 2), 960.0 / (CARD_W2 / 2))", "END_Z = min(0.8, 640.0 / (CARD_H2 / 2), 960.0 / (CARD_W2 / 2))"),
           ("END_SAFE = ((SW / 2, SH / 2), END_Z, (540, 944 - END_Z * CARD_H2 / 4))", "END_SAFE = ((SW / 2, SH / 2), END_Z, (540, 1040 - END_Z * CARD_H2 / 4))"),
           # cảnh nối không chữ (trước khung cuối): không vẽ header, không phủ tối dải chữ
           ("    t.put((60, SAFE_Y0 + 4), HEAD, 34, 220)\n", "    if sc[\"head\"]:\n        t.put((60, SAFE_Y0 + 4), HEAD, 34, 220)\n"),
           ("    return top < TOP_END, bot > cr_y - 20, warn", "    return top < TOP_END and bool(sc[\"head\"]), bot > cr_y - 20 and bool(sc[\"vo\"]), warn"),
           # khung cuối: chữ khớp lời mời (mẫu tập 7)
           ('(1196, "Bài viết phân tích đầy đủ", 58, 240),\n    (1260, "xem ở dòng đầu tiên", 58, 240),\n    (1348, "trong phần bình luận", 66, 255),',
            '(1252, "Bài phân tích về màu tiến, màu lùi", 54, 240),\n    (1314, "từ sách của Kilmer & Kilmer", 48, 240),\n    (1398, "xem ở phần bình luận", 66, 255),')]
    if len(IMGS[img]) > 3 and IMGS[img][3]:
        rep.append(("SKETCH = False  #", "SKETCH = True  #"))
    if img in ("bep", "an", "hanh"):   # ảnh chụp phủ kín khung: bỏ băng keo
        rep.append(("TAPE = True     #", "TAPE = False    #"))
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
    open(OUT + "engine_ep18/" + dst, "w").write(s)


T = times()
for k, s in enumerate(SC):
    s["t"] = f"{T[k]:g}–{T[k + 1]:g}s"
RUNS = []
for n, ks in enumerate(runs(), 1):
    img = SC[ks[0]]["img"]
    tag = f"r{n:02d}_{img}"
    data, d0, dl = build_run(T, ks)
    build("engine_storyboard_v7.py", f"engine_ep18_{tag}.py", False, data, img, tag)
    build("engine_video.py", f"engine_video_ep18_{tag}.py", True, data, img, tag)
    RUNS.append(dict(tag=tag, img=img, src=IMGS[img][0], scenes=[k + 1 for k in ks], t_in_main=T[ks[0]],
                     cut_from=d0, cut_len=dl + (1.0 if ks[-1] == len(SC) - 1 else 0.0),
                     first_frame=2 if ks[0] > 0 else 1))
json.dump(RUNS, open(OUT + "engine_ep18/runs.json", "w"), ensure_ascii=False, indent=1)

# ảnh bìa 1080x1920: cảnh rộng trên ảnh bếp hồng Casa Tahiti, tiêu đề ngắn
COVER = [dict(img="bep", head="Tủ kịch trần mà bếp không chật", vo="Vì sao dãy tủ trắng kín cả bức tường lại trông như lùi ra sau.", dark=False),
         dict(img="bep", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep18.py", False,
      wrap_data([scene_line(COVER[0], 0, 3, "WIDE", []), scene_line(COVER[1], 3, 4, "END_SAFE", [])],
                DOODLE.replace("@NPZ@", "none.npz")), "bep", "cover")

# ---- elevenlabs.txt: các khối kịch bản nối bằng thẻ ngắt 1,2 giây (theo prompt của routine) ----
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
FOREIGN = ["Bloj", "CIE", "AH+", "Tahiti", "sofa", "Oberfeld", "Castell", "Klinker", "Barcelona", "Rietveld", "Lane", "Cove", "Sydney", "Kilmer", "Rosemary", "Otie", "Seegers", "Lachlan", "Schröder", "Utrecht", "Edgar", "Rubin", "Wagemans", "Gestalt", "Checklist", "checklist", "Stijl", "Foster", "Barragán", "Gilardi", "Casa", "Luis", "Mexico", "Munsell", "Oberfeld", "Hecht", "Itten", "Johannes", "Castell", "von", "Pawson", "John", "London", "AH", "Decode", "Bauhaus", "LRV", "cm"]
bad = re.findall(r"\d", " ".join(spoken)) + [w for w in FOREIGN if re.search(r"\b" + w + r"\b", " ".join(spoken))]
print("chữ số / tên nước ngoài chưa phiên âm trong bản đọc:", bad)
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep18/scenes.json", "w"), ensure_ascii=False, indent=1)
