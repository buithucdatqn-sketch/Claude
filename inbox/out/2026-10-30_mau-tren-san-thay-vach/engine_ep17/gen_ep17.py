"""Tập 17 (chương 2 sổ tay AH+, mục 2.1–2.3, Hình 2.3): màu trên sàn thay cho vách. Mã gốc từ gen_ep16.py (tập 16, chương 4).
Reel nhiều ảnh theo bộ khuôn mau_tap7 (xem engine/mau_tap7/README.md). Mỗi cảnh chọn ảnh qua khoá `img` (IMGS); mỗi đoạn cảnh
liên tiếp cùng một ảnh là một "run" (engine_ep17_rNN_<ảnh>.py và engine_video_ep17_rNN_<ảnh>.py). Ảnh lấy từ chính file PDF của chương (pdfimages),
không phóng to. Doodle: nét trắng mới vẽ bằng draw_ep17.py (ảnh trong sổ tay không có doodle)."""
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
RS = "Ảnh: nhà Rietveld Schröder · Stijn Poelstra / Centraal Museum, qua sổ tay AH+"
# ảnh làm việc: (file, npz doodle, credit). Tất cả lấy từ PDF chương 2 của sổ tay (pdfimages, kích thước gốc, không phóng to)
IMGS = dict(
    tren=("source_tren.png", "doodle_ep17_tren.npz", RS),   # mục 2.3: tầng trên khi vách trượt mở, sàn đỏ đen trắng xám (1182x788)
    d21=("source_d21.png", "", "Hình 2.1: AH+, sổ tay Công thức chọn màu nội thất"),   # 540x380
    do=("source_do.png", "doodle_ep17_do.npz", RS),         # mục 2.3: phòng sàn đỏ, ghế đỏ lam, khối lam cạnh giường, tường xám (1182x788)
    d23=("source_d23.png", "", "Hình 2.3 (phần nên làm): AH+, sổ tay Công thức chọn màu nội thất"),   # cắt từ 540x1130
    bep=("source_bep.png", "", RS),                          # mục 2.1: bếp và bàn ăn, ghế đỏ, thanh lam trên kệ (1182x788)
    ebook=("source_ebook.png", "", "Ảnh: sổ tay AH+ Công thức chọn màu nội thất · Giả Thuyết Kiến Trúc"),
)


def STRIP(cx, cy, z=1.0, ay=900):
    """thẻ ảnh/bản vẽ nằm gọn giữa hai khối chữ (y ~610–1240): tiêu đề ở trên, phụ đề ở dưới, chữ nâu trên nền trắng"""
    return ((cx, cy), z, (540, ay))


L_ = STRIP(591, 394, 0.9, 900)      # ảnh ngang 1182x788
D21 = STRIP(270, 190, 0.86, 905)      # Hình 2.1, 540x380
D23 = STRIP(270, 235, 0.69, 905)     # Hình 2.3 cắt phần "Nên" (bỏ tiêu đề lớn), 540x470
# Một câu hỏi trung tâm: nhà bỏ hết vách cho thoáng, sao nhìn lại loang, không rõ đâu là bếp, đâu là chỗ ngồi?
# Mạch: móc → lý do (2.1: cả nhà chung một nền màu) → hình và nền (Rubin 1915) → điều kiện thành hình (Wagemans 2012) → hệ quả: cả nhà chỉ còn nền
# (rào một lần: suy luận từ nguyên lý) → Rietveld Schröder: vách thu lại, ranh giới nằm trên sàn; màu mạnh ở mảng nhỏ, mặt lớn làm nền
# → nhà mình: cho khu cần tách thành hình, khối màu chạy hết mép tủ, màu trên sàn hay trần → chốt → lời mời. Khối đọc nối bằng thẻ ngắt 1,2 giây.
SC = [
    dict(move="push", part="A", blk=1, img="tren", head="Nhà mở bỏ vách, vì sao dễ lẫn lộn", cam=L_, free=True, dark=False, dd=[],
         vo="Nhà bỏ hết vách cho thoáng, sao nhìn lại lẫn lộn, không rõ đâu là bếp, đâu là chỗ ngồi?"),
    dict(move="pan_r", part="A", blk=2, img="d21", head="Cả nhà nằm trên một nền màu", cam=D21, free=True, dark=False, dd=[],
         vo="Lý do thường là cả nhà nằm trên một nền màu, nên mỗi khu chỉ còn được nhận ra nhờ đồ đạc."),
    dict(move="hold", part="B", blk=2, img="d21", head="Hình và nền theo tâm lý học Gestalt", cam=D21, free=True, dark=False, dd=[],
         vo="Theo tâm lý học Gestalt, mắt luôn tách một vùng nổi lên làm hình, còn phần còn lại lùi ra sau làm nền.",
         tts="Theo tâm lý học Ghe-xtan, mắt luôn tách một vùng nổi lên làm hình, còn phần còn lại lùi ra sau làm nền."),
    dict(move="push", part="C", blk=3, img="d21", head="Theo Wagemans và cộng sự (2012)", cam=D21, free=True, dark=False, dd=[],
         vo="Một tổng quan năm 2012 cho thấy vùng nào nhỏ hơn, có biên rõ và tương phản với xung quanh thì dễ thành hình,",
         tts="Một tổng quan năm hai nghìn không trăm mười hai cho thấy vùng nào nhỏ hơn, có biên rõ và tương phản với xung quanh thì dễ thành hình,"),
    dict(move="hold", part="C", blk=3, img="d21", head="Màu đồng nhất được đọc là nền", cam=D21, free=True, dark=False, dd=[],
         vo="còn một mảng màu đồng nhất thường được đọc là nền."),
    dict(move="pull", part="C", blk=3, img="d21", head="Suy luận từ nguyên lý, chưa có thí nghiệm", cam=D21, free=True, dark=False, dd=[],
         vo="Sổ tay nói rõ, dùng điều này để chia khu trong nhà là suy luận từ nguyên lý, chưa có thí nghiệm nào chứng minh."),
    dict(move="pan_l", part="D", blk=4, img="tren", head="Nhà Rietveld Schröder, Utrecht (1924)", cam=L_, free=True, dark=False, dd=["vach", "lab_vach"],
         vo="Ở tầng trên nhà Rietveld Schröder tại Utrecht, xây năm 1924, ban ngày các vách trượt được thu lại,",
         tts="Ở tầng trên nhà Rít-ven Srơ-đơ tại U-tréc, xây năm một nghìn chín trăm hai mươi tư, ban ngày các vách trượt được thu lại,"),
    dict(move="hold", part="D", blk=4, img="tren", head="Ranh giới nằm lại trên sàn", cam=L_, free=True, dark=False, dd=["sando", "lab_sando", "sanden", "lab_sanden"],
         vo="nhưng sàn vẫn chia thành những mảng đỏ, đen, trắng và xám có biên rõ, nên ranh giới các khu vẫn nằm lại trên sàn."),
    dict(move="push", part="D", blk=4, img="do", head="Màu mạnh chỉ ở mảng nhỏ", cam=L_, free=True, dark=False, dd=["san", "lab_san", "lam", "lab_lam", "ghe", "lab_ghe"],
         vo="Màu mạnh chỉ nằm ở mảng nhỏ, như mảng sàn đỏ, khối lam cạnh giường và chiếc ghế đỏ lam,"),
    dict(move="hold", part="D", blk=4, img="do", head="Tường lớn giữ màu xám", cam=L_, free=True, dark=False, dd=["xam", "lab_xam"],
         vo="còn bức tường lớn giữ màu xám."),
    dict(move="pan_d", part="F", blk=5, img="d23", head="Cho khu cần tách thành hình", cam=D23, free=True, dark=False, dd=[],
         vo="Ở nhà mình, muốn tách khu bếp hay hốc tường sau sofa thì cho khu ấy nhỏ hơn, biên rõ hơn và tương phản hơn nền,"),
    dict(move="pull", part="F", blk=5, img="tren", head="Màu xuống sàn, lên trần, thay cho vách", cam=L_, free=True, dark=False, dd=["tran", "lab_tran"],
         vo="và có thể đặt màu xuống sàn hay lên trần thay cho vách."),
    dict(move="push", part="H", blk=6, img="bep", head="Có hình thì hết lẫn lộn", cam=L_, free=True, dark=False, dd=[],
         vo="Vậy nhà mở lẫn lộn không phải vì thiếu vách, mà vì cả nhà chỉ có nền, chưa có khu nào thành hình."),
    dict(move="hold", part="I", blk=6, img="ebook", head="end", cam="END", dark=False, vo="", dd=[],
         say="Các bước phân vùng nhà mở bằng màu có trong sổ tay Công thức chọn màu kiến trúc nội thất, mọi người xem ở phần bình luận nha."),
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
    của run mở bằng hoà tan từ run trước (ghep_ep17.py), chữ cảnh trước mờ đi như cũ."""
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
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · PHÂN VÙNG NHÀ MỞ BẰNG MÀU"'),
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
            '(1252, "Sổ tay Công thức chọn màu nội thất", 54, 240),\n    (1314, "các bước phân vùng nhà mở bằng màu", 48, 240),\n    (1398, "xem ở phần bình luận", 66, 255),')]
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

# ảnh bìa 1080x1920: cảnh rộng trên ảnh tầng trên nhà Rietveld Schröder (vách mở, sàn nhiều mảng màu), tiêu đề ngắn
COVER = [dict(img="tren", head="Màu trên sàn thay cho vách", vo="Vì sao nhà mở dễ loang, và cách để ranh giới nằm lại trên sàn, theo sổ tay AH+.", dark=False),
         dict(img="tren", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep17.py", False,
      wrap_data([scene_line(COVER[0], 0, 3, "WIDE", []), scene_line(COVER[1], 3, 4, "END_SAFE", [])],
                DOODLE.replace("@NPZ@", "none.npz")), "tren", "cover")

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
FOREIGN = ["Rietveld", "Schröder", "Utrecht", "Edgar", "Rubin", "Wagemans", "Gestalt", "Checklist", "checklist", "Stijl", "Foster", "Barragán", "Gilardi", "Casa", "Luis", "Mexico", "Munsell", "Oberfeld", "Hecht", "Itten", "Johannes", "Castell", "von", "Pawson", "John", "London", "AH", "Decode", "Bauhaus", "LRV", "cm"]
bad = re.findall(r"\d", " ".join(spoken)) + [w for w in FOREIGN if re.search(r"\b" + w + r"\b", " ".join(spoken))]
print("chữ số / tên nước ngoài chưa phiên âm trong bản đọc:", bad)
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep17/scenes.json", "w"), ensure_ascii=False, indent=1)
