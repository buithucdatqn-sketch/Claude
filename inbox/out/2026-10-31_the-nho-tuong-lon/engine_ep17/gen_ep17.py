"""Tập 17 bản 3 (phần kết sổ tay AH+, mục K.2, phụ lục D3, Hình PK.2, PK.3): thẻ màu nhỏ, bức tường lớn. Mã gốc từ gen bản 2.
Ảnh chụp Casa Tahiti (ArchDaily) phủ kín khung, nét doodle trắng vẽ mới bằng draw_ep17.py; sơ đồ dựng bằng chế độ SKETCH của engine
(nét hiện dần theo thứ tự vẽ trên nền trắng, lớp nét tách bằng sketch_ep17.py)."""
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
TAH = "Ảnh dự án: Casa Tahiti · Margine · ảnh Nicolò Panzeri / ArchDaily"
# ảnh làm việc: (file, npz doodle, credit[, sketch]). Ảnh chụp: bộ ảnh Casa Tahiti trên ArchDaily (chủ Trang cho phép lấy ảnh công trình ngoài sách
# và tự vẽ doodle, 2026-10-31). Sơ đồ: Hình PK.2, PK.3 trích từ PDF phần kết của sổ tay, vẽ dần trên nền trắng.
IMGS = dict(
    tuong=("source_tuong.png", "doodle_ep17_tuong.npz", TAH),   # bếp: tủ và tường sơn hồng (2000x2933)
    tam=("source_tam.png", "doodle_ep17_tam.npz", TAH),         # phòng tắm sơn vàng (2000x2867)
    tu=("source_tu.png", "doodle_ep17_tu.npz", TAH),            # tủ hồng sát tường trắng (2000x2933)
    hanh=("source_hanh.png", "doodle_ep17_hanh.npz", TAH),      # lối đi nhìn về phòng tắm vàng (2000x2800)
    pk2=("source_pk2.png", "sketch_ep17_pk2.npz", "Hình PK.2: AH+, sổ tay Công thức chọn màu nội thất", True),   # cắt bỏ tiêu đề (648x453)
    ebook=("source_ebook.png", "", "Ảnh: sổ tay AH+ Công thức chọn màu nội thất · Giả Thuyết Kiến Trúc"),
)


def STRIP(cx, cy, z=1.0, ay=900):
    """thẻ ảnh/bản vẽ nằm gọn giữa hai khối chữ (y ~610–1240)"""
    return ((cx, cy), z, (540, ay))


# Ảnh chụp phủ kín khung (free=False, cover tự neo), zoom vào đúng chi tiết đang nói; ảnh 2000 px nên phóng gần 1:1.
TUONG = ((1000, 1300), 2.6, (540, 925))
TAM = ((1300, 1100), 2.6, (540, 925))
TU = ((750, 1300), 2.8, (540, 925))
HANH = ((700, 1300), 2.5, (540, 925))
PK2 = STRIP(324, 226, 0.9, 910)


# Một câu hỏi trung tâm: màu chọn trên thẻ thì vừa mắt, sơn lên cả bức tường lại đậm và rực hẳn, vì sao?
# Mạch: móc → lý do 1, kích thước (thẻ vài cm giữa tường trắng, PK.2 trái vẽ dần) → CIE 208:2014: mảng lớn sáng hơn, rực hơn (phòng tắm vàng)
# → lý do 2, ánh sáng dội (tủ hồng sát tường trắng; Bloj 1999) → tường trắng sát tủ ửng hồng hơn, thẻ nhỏ không cho thấy → vì vậy mảng thử
# 1 m², hai lớp, qua góc (PK.2 phải vẽ dần) → xem ba mốc giờ (PK.3 vẽ dần) → chốt → lời mời.
SC = [
    dict(move="push", part="A", blk=1, img="tuong", head="Thẻ màu vừa mắt, tường lại rực", cam=TUONG, dark=True, dd=[],
         vo="Màu chọn trên thẻ thì vừa mắt, sơn lên cả bức tường lại sáng và rực hơn hẳn, vì sao?"),
    dict(move="hold", part="B", blk=2, img="pk2", head="Lý do thứ nhất là kích thước", cam=PK2, free=True, dark=False, dd=["trai"], keep=[],
         vo="Sổ tay AH+ nêu hai lý do. Lý do đầu tiên là kích thước, vì tấm thẻ chỉ vài xăng-ti-mét đặt giữa tường trắng,",
         tts="Sổ tay Ây-hát cộng nêu hai lý do. Lý do đầu tiên là kích thước, vì tấm thẻ chỉ vài xăng-ti-mét đặt giữa tường trắng,"),
    dict(move="hold", part="B", blk=2, img="pk2", head="Lý do thứ nhất là kích thước", cam=PK2, free=True, dark=False, dd=[], keep=["trai"],
         vo="còn bức tường sơn thật thì chiếm phần lớn tầm nhìn."),
    dict(move="pan_u", part="C", blk=3, img="tam", head="CIE 208:2014", cam=TAM, dark=True, dd=["vang", "lab_vang"],
         vo="Một báo cáo kỹ thuật năm 2014 tổng hợp các thí nghiệm và cho thấy mảng màu lớn thường trông sáng hơn, rực hơn mảng nhỏ,",
         tts="Một báo cáo kỹ thuật năm hai nghìn không trăm mười bốn tổng hợp các thí nghiệm và cho thấy mảng màu lớn thường trông sáng hơn, rực hơn mảng nhỏ,"),
    dict(move="hold", part="C", blk=3, img="tam", head="Mảng lớn sáng hơn, rực hơn", cam=TAM, dark=True, dd=[],
         vo="có khi còn đổi cả sắc màu, dù nghiên cứu về hiện tượng này còn ít."),
    dict(move="push", part="C", blk=4, img="tu", head="Lý do thứ hai là ánh sáng dội", cam=TU, dark=True, dd=["doi", "lab_doi"],
         vo="Lý do thứ hai là ánh sáng dội từ mặt màu sang mặt bên cạnh."),
    dict(move="hold", part="C", blk=4, img="tu", head="Bloj, Kersten và Hurlbert (1999)", cam=TU, dark=True, dd=[],
         vo="Năm 1999, một nhóm nghiên cứu cho người xem một tấm bìa gập, nửa đỏ tía, nửa trắng,",
         tts="Năm một nghìn chín trăm chín mươi chín, một nhóm nghiên cứu cho người xem một tấm bìa gập, nửa đỏ tía, nửa trắng,"),
    dict(move="hold", part="C", blk=4, img="tu", head="Bloj, Kersten và Hurlbert (1999)", cam=TU, dark=True, dd=[],
         vo="và ánh sáng dội từ nửa đỏ tía phủ một quầng hồng lên nửa trắng."),
    dict(move="pan_r", part="D", blk=4, img="tu", head="Tường trắng sát tủ hồng ửng màu", cam=TU, dark=True, dd=["gan", "lab_gan", "xa", "lab_xa"],
         vo="Ở căn bếp này, phần tường trắng sát tủ hồng cũng ửng màu hơn phần ở xa."),
    dict(move="pull", part="C", blk=4, img="hanh", head="Tường, trần, sàn dội màu lên nhau", cam=HANH, dark=True, dd=["mat", "lab_mat"],
         vo="Trong phòng, tường, trần và sàn đều dội ánh sáng lên nhau, nên màu của một bức tường còn tùy các mặt xung quanh,"),
    dict(move="hold", part="C", blk=4, img="hanh", head="Điều tấm thẻ không cho thấy", cam=HANH, dark=True, dd=[],
         vo="điều mà tấm thẻ đặt giữa tường trắng không cho thấy."),
    dict(move="hold", part="F", blk=5, img="pk2", head="Mảng thử một mét vuông, hai lớp", cam=PK2, free=True, dark=False, dd=["phai", "kt"], keep=["trai"],
         vo="Vì vậy, nên sơn một mảng thử khoảng một mét vuông, hai lớp, ngay trên bức tường sẽ sơn,"),
    dict(move="hold", part="F", blk=5, img="pk2", head="Cho mảng thử chạy qua góc tường", cam=PK2, free=True, dark=False, dd=[], keep=["trai", "phai", "kt"],
         vo="và cho chạy qua góc tường để thấy cả phía sáng, phía tối lẫn màu dội sang tường bên cạnh."),
    dict(move="pull", part="H", blk=6, img="tuong", head="Một ô nhỏ chưa phải cả bức tường", cam=TUONG, dark=True, dd=[],
         vo="Tấm thẻ chỉ cho biết màu của một ô nhỏ trên nền trắng, chưa cho biết màu của cả bức tường trong căn phòng thật."),
    dict(move="hold", part="I", blk=6, img="ebook", head="end", cam="END", dark=False, vo="", dd=[],
         say="Ba phép thử màu ngay tại công trình có trong sổ tay Công thức chọn màu kiến trúc nội thất, mọi người xem ở phần bình luận nha."),
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
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · THẺ MÀU VÀ BỨC TƯỜNG"'),
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
            '(1252, "Sổ tay Công thức chọn màu nội thất", 54, 240),\n    (1314, "ba phép thử màu tại công trình", 48, 240),\n    (1398, "xem ở phần bình luận", 66, 255),')]
    if len(IMGS[img]) > 3 and IMGS[img][3]:
        rep.append(("SKETCH = False  #", "SKETCH = True  #"))
    if img in ("tuong", "tam", "tu", "hanh"):   # ảnh chụp phủ kín khung: bỏ băng keo
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

# ảnh bìa 1080x1920: cảnh rộng trên ảnh bếp hồng Casa Tahiti, tiêu đề ngắn
COVER = [dict(img="tuong", head="Thẻ màu nhỏ, bức tường lớn", vo="Vì sao màu chọn trên thẻ sơn lên tường lại đậm và rực hơn, theo sổ tay AH+.", dark=False),
         dict(img="tuong", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep17.py", False,
      wrap_data([scene_line(COVER[0], 0, 3, "WIDE", []), scene_line(COVER[1], 3, 4, "END_SAFE", [])],
                DOODLE.replace("@NPZ@", "none.npz")), "tuong", "cover")

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
FOREIGN = ["Bloj", "CIE", "AH+", "Tahiti", "sofa", "Oberfeld", "Castell", "Klinker", "Barcelona", "Rietveld", "Schröder", "Utrecht", "Edgar", "Rubin", "Wagemans", "Gestalt", "Checklist", "checklist", "Stijl", "Foster", "Barragán", "Gilardi", "Casa", "Luis", "Mexico", "Munsell", "Oberfeld", "Hecht", "Itten", "Johannes", "Castell", "von", "Pawson", "John", "London", "AH", "Decode", "Bauhaus", "LRV", "cm"]
bad = re.findall(r"\d", " ".join(spoken)) + [w for w in FOREIGN if re.search(r"\b" + w + r"\b", " ".join(spoken))]
print("chữ số / tên nước ngoài chưa phiên âm trong bản đọc:", bad)
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep17/scenes.json", "w"), ensure_ascii=False, indent=1)
