"""Tập 17 bản 2 (chương 3 sổ tay AH+, mục 3.2, 3.4, Hình 3.1): trần tối hơn tường. Mã gốc từ gen_ep16.py.
Reel nhiều ảnh theo bộ khuôn mau_tap7. Ảnh chụp phóng tràn màn hình; sơ đồ (IMGS có cờ sketch) dựng bằng chế độ SKETCH của engine:
nét hiện dần theo thứ tự vẽ trên nền trắng, lớp nét tách bằng sketch_ep17.py. Doodle ảnh chụp: nét trắng mới vẽ bằng draw_ep17.py."""
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
# ảnh làm việc: (file, npz doodle, credit[, sketch]). Tất cả lấy từ PDF chương 3 của sổ tay (pdfimages, kích thước gốc)
IMGS = dict(
    cao=("source_cao.png", "doodle_ep17_cao.npz", "Ảnh: phòng khách trần cao · Ivan Santos / Unsplash, qua sổ tay AH+"),   # trang ảnh tràn chương 3 (1334x2000)
    dailly=("source_dailly.png", "doodle_ep17_dailly.npz", "Ảnh dự án: nhà Dailly, Brussels · Mamout · ảnh Séverin Malaud / Dezeen, qua sổ tay AH+"),   # mục 3.1 (946x1182)
    klinker=("source_klinker.png", "doodle_ep17_klinker.npz", "Ảnh dự án: Klinker Apartment · Colombo and Serboli · ảnh Roberto Ruiz / Divisare"),   # mục 3.4 (529x793)
    d31=("source_d31.png", "sketch_ep17_d31.npz", "Hình 3.1: AH+, sổ tay Công thức chọn màu nội thất", True),   # cắt bỏ tiêu đề lớn (756x535), vẽ dần trên nền trắng
    ebook=("source_ebook.png", "", "Ảnh: sổ tay AH+ Công thức chọn màu nội thất · Giả Thuyết Kiến Trúc"),
)


def STRIP(cx, cy, z=1.0, ay=900):
    """thẻ ảnh/bản vẽ nằm gọn giữa hai khối chữ (y ~610–1240)"""
    return ((cx, cy), z, (540, ay))


# Ảnh chụp: phóng to, tràn màn hình (chủ Trang yêu cầu 2026-10-30: ảnh doodle quá nhỏ). cao: phủ kín khung (free=False, cover tự neo);
# dailly, klinker: cũng phủ kín khung (ảnh nhỏ nên phóng 1,7 và 2,5 lần, engine làm nét nhẹ khi phóng).
CAO = ((667, 950), 2.2, (540, 925))
DAI = ((380, 420), 2.1, (540, 925))
KLI = ((264.5, 380), 2.1, (540, 925))
D31 = STRIP(378, 267, 0.88, 900)     # sơ đồ vẽ dần, gần kín bề ngang khung


# Một câu hỏi trung tâm: phòng trần cao trông trống và lạnh, sơn trần màu gì để phòng ấm lại?
# Mạch: móc (tình huống của sổ tay mục mở chương 3) → thói quen chọn màu ấm vì "màu nóng tiến, màu lạnh lùi" → hiện tượng đó chỉ đo được
# trên mảng màu nhỏ (3.2) → thí nghiệm trên mô hình phòng: trần, tường sáng thì cao hơn, sàn không ảnh hưởng (Oberfeld 2010) → tách độ sáng,
# sắc độ, độ rực của trần: độ sáng quyết định (von Castell 2018a) → vì vậy làm trần tối hơn tường (kỹ thuật 1, Klinker) → báo chủ nhà vài cm,
# cái thấy rõ là ấm cúng → hành lang sâu: tường cuối tối hơn (Hình 3.1, vẽ dần) → chốt trả lời câu móc → lời mời.
SC = [
    dict(move="push", part="A", blk=1, img="cao", head="Trần cao, phòng trống và lạnh", cam=CAO, dark=True, dd=[],
         vo="Trần cao làm sofa trông nhỏ lại, phòng ngồi lâu thấy trống và lạnh. Sơn trần màu gì để phòng ấm lại?",
         tts="Trần cao làm sô-pha trông nhỏ lại, phòng ngồi lâu thấy trống và lạnh. Sơn trần màu gì để phòng ấm lại?"),
    dict(move="pan_d", part="B", blk=2, img="dailly", head="Thói quen sơn trần màu ấm", cam=DAI, dark=True, dd=["gach", "lab_gach"],
         vo="Nhiều người sẽ sơn trần màu ấm, vì quen câu màu nóng tiến lại gần, màu lạnh lùi ra xa, nên nghĩ trần màu ấm sẽ thấp xuống."),
    dict(move="hold", part="C", blk=2, img="dailly", head="Đo trên mảng màu nhỏ, không đo trên căn phòng", cam=DAI, dark=True, dd=["hoi", "lab_hoi"],
         vo="Màu tiến, màu lùi có thật, nhưng chỉ được đo trên những mảng màu nhỏ trong phòng thí nghiệm, chứ không đo trên một căn phòng."),
    dict(move="pull", part="C", blk=3, img="cao", head="Oberfeld, Hecht và Gamer (2010)", cam=CAO, dark=True, dd=["tran", "lab_tran", "tuong", "lab_tuong"],
         vo="Khi thử trên mô hình phòng, nhóm Oberfeld thấy trần và tường càng sáng thì phòng trông càng cao.",
         tts="Khi thử trên mô hình phòng, nhóm Ô-bơ-phen thấy trần và tường càng sáng thì phòng trông càng cao."),
    dict(move="push", part="C", blk=3, img="cao", head="von Castell, Hecht và Oberfeld (2018)", cam=CAO, dark=True, dd=["dosang", "lab_dosang"],
         vo="Năm 2018, nhóm von Castell tách riêng độ sáng tối, màu gì và độ tươi của màu trần, và thấy độ sáng tối quyết định gần hết,",
         tts="Năm hai nghìn không trăm mười tám, nhóm phôn Cát-xten tách riêng độ sáng tối, màu gì và độ tươi của màu trần, và thấy độ sáng tối quyết định gần hết,"),
    dict(move="hold", part="C", blk=3, img="cao", head="Trần đỏ hay xanh lam cao gần như nhau", cam=CAO, dark=True, dd=[],
         vo="còn trần đỏ và trần xanh lam trông cao gần như nhau."),
    dict(move="hold", part="C", blk=4, img="d31", head="Hai hành lang giống hệt nhau", cam=D31, free=True, dark=False, dd=["trai", "lab_trai"], keep=[],
         vo="Sổ tay vẽ hai hành lang giống hệt nhau để thấy điều này, tường cuối sáng thì trông xa hơn,"),
    dict(move="hold", part="C", blk=4, img="d31", head="Tối hơn thì trông gần hơn", cam=D31, free=True, dark=False, dd=["phai", "lab_phai"], keep=["trai", "lab_trai"],
         vo="còn tường cuối tối hơn thì trông gần hơn, và trần cũng thế."),
    dict(move="push", part="F", blk=5, img="klinker", head="Trần tối hơn tường", cam=KLI, dark=True, dd=["tranx", "lab_tranx"],
         vo="Vì vậy, muốn trần cao thấp xuống thì sơn trần tối hơn tường,"),
    dict(move="hold", part="F", blk=5, img="klinker", head="Màu gì thì theo bảng màu của nhà", cam=KLI, dark=True, dd=[],
         vo="còn màu gì thì chọn theo bảng màu chung của nhà, như xám than hay gỗ tối màu."),
    dict(move="pan_u", part="D", blk=5, img="klinker", head="Klinker Apartment, Barcelona (2019)", cam=KLI, dark=True, dd=["kem", "lab_kem"],
         vo="Phòng ngủ này ở Barcelona có trần xanh xám đậm, tối hẳn so với tường kem.",
         tts="Phòng ngủ này ở Bác-xê-lô-na có trần xanh xám đậm, tối hẳn so với tường kem."),
    dict(move="hold", part="F", blk=5, img="klinker", head="Báo trước với chủ nhà", cam=KLI, dark=True, dd=[],
         vo="Sổ tay dặn nên báo trước với chủ nhà rằng trần chỉ thấp đi vài xăng-ti-mét,"),
    dict(move="hold", part="F", blk=5, img="klinker", head="Cái thấy rõ là ấm cúng, êm hơn", cam=KLI, dark=True, dd=[],
         vo="còn điều họ thường thấy rõ hơn là phòng ấm cúng và êm hơn."),
    dict(move="pull", part="H", blk=6, img="cao", head="Đổi độ sáng tối, không chỉ đổi màu nóng lạnh", cam=CAO, dark=True, dd=[],
         vo="Vậy muốn phòng trần cao ấm lại, điều cần đổi là độ sáng tối của trần so với tường, còn nóng hay lạnh thì tùy bảng màu của nhà."),
    dict(move="hold", part="I", blk=6, img="ebook", head="end", cam="END", dark=False, vo="", dd=[],
         say="Ba cách chỉnh cao thấp, nông sâu của căn phòng bằng màu có trong sổ tay Công thức chọn màu kiến trúc nội thất, mọi người xem ở phần bình luận nha."),
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
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · MÀU CHO PHÒNG TRẦN CAO"'),
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
            '(1252, "Sổ tay Công thức chọn màu nội thất", 54, 240),\n    (1314, "cách chỉnh cao thấp, nông sâu", 48, 240),\n    (1398, "xem ở phần bình luận", 66, 255),')]
    if len(IMGS[img]) > 3 and IMGS[img][3]:
        rep.append(("SKETCH = False  #", "SKETCH = True  #"))
    if img in ("cao", "dailly", "klinker"):   # ảnh chụp phủ kín khung: bỏ băng keo
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
    open(OUT + "engine_ep17/" + dst, "w").write(s)


T = times()
for k, s in enumerate(SC):
    s["t"] = f"{T[k]:g}–{T[k + 1]:g}s"
RUNS = []
for n, ks in enumerate(runs(), 1):
    img = SC[ks[0]]["img"]
    tag = f"r{n:02d}_{img}"
    data, d0, dl = build_run(T, ks)
    build("engine_storyboard_v7.py", f"engine_ep17_{tag}.py", False, data, img, tag)
    build("engine_video.py", f"engine_video_ep17_{tag}.py", True, data, img, tag)
    RUNS.append(dict(tag=tag, img=img, src=IMGS[img][0], scenes=[k + 1 for k in ks], t_in_main=T[ks[0]],
                     cut_from=d0, cut_len=dl + (1.0 if ks[-1] == len(SC) - 1 else 0.0),
                     first_frame=2 if ks[0] > 0 else 1))
json.dump(RUNS, open(OUT + "engine_ep17/runs.json", "w"), ensure_ascii=False, indent=1)

# ảnh bìa 1080x1920: cảnh rộng trên ảnh phòng ngủ Klinker (trần xanh xám đậm), tiêu đề ngắn
COVER = [dict(img="klinker", head="Trần tối hơn tường", vo="Muốn phòng trần cao ấm lại, đổi độ sáng của trần chứ không chỉ đổi sang màu ấm, theo sổ tay AH+.", dark=False),
         dict(img="klinker", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep17.py", False,
      wrap_data([scene_line(COVER[0], 0, 3, "WIDE", []), scene_line(COVER[1], 3, 4, "END_SAFE", [])],
                DOODLE.replace("@NPZ@", "none.npz")), "klinker", "cover")

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
FOREIGN = ["sofa", "Oberfeld", "Castell", "Klinker", "Barcelona", "Rietveld", "Schröder", "Utrecht", "Edgar", "Rubin", "Wagemans", "Gestalt", "Checklist", "checklist", "Stijl", "Foster", "Barragán", "Gilardi", "Casa", "Luis", "Mexico", "Munsell", "Oberfeld", "Hecht", "Itten", "Johannes", "Castell", "von", "Pawson", "John", "London", "AH", "Decode", "Bauhaus", "LRV", "cm"]
bad = re.findall(r"\d", " ".join(spoken)) + [w for w in FOREIGN if re.search(r"\b" + w + r"\b", " ".join(spoken))]
print("chữ số / tên nước ngoài chưa phiên âm trong bản đọc:", bad)
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep17/scenes.json", "w"), ensure_ascii=False, indent=1)
