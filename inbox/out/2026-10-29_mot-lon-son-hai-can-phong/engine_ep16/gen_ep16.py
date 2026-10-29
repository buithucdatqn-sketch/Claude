"""Tập 16 (chương 4 sổ tay AH+, mục 4.1–4.7): cùng một lon sơn, hai căn phòng. Mã gốc từ tập 14: Sơn trắng làm phòng hẹp rộng thêm bao nhiêu (sổ tay AH+ "Công thức chọn màu nội thất", kho AH-Decode-Decor/so-tay-cong-thuc-chon-mau-noi-that/,
chương 1 "Kiểm soát ánh sáng trong không gian hẹp", mục 1.2 "Mặt bao quanh càng sáng, phòng càng rộng", 1.3 "Ba bước áp dụng", 1.4 Pawson House).
Reel nhiều ảnh theo bộ khuôn mau_tap7 (xem engine/mau_tap7/README.md), mã gốc từ gen_ep13.py. Mỗi cảnh chọn ảnh qua khoá `img` (IMGS); mỗi đoạn cảnh
liên tiếp cùng một ảnh là một "run" (engine_ep16_rNN_<ảnh>.py và engine_video_ep16_rNN_<ảnh>.py). Ảnh lấy từ chính file PDF của chương (pdfimages),
không phóng to. Doodle: nét trắng mới vẽ bằng draw_ep16.py (ảnh trong sổ tay không có doodle)."""
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
HF = "Ảnh: Home Farm, Oxfordshire · John Pawson · ảnh John Pawson, qua sổ tay AH+"
GIL = "Ảnh dự án: Casa Gilardi, Mexico City · Luis Barragán · ảnh Eduardo Luque / ArchDaily, qua sổ tay AH+"
# ảnh làm việc: (file, npz doodle, credit). Tất cả lấy từ PDF chương 4 của sổ tay (pdfimages, kích thước gốc, không phóng to)
IMGS = dict(
    hf=("source_hf.png", "doodle_ep16_hf.npz", HF),        # mục 4.2: nắng tây in hai mảng cam qua cửa sổ lên tường trát xám, kệ nến (900x900)
    hf2=("source_hf2.png", "doodle_ep16_hf2.npz", HF),     # mục 4.2: ảnh thứ hai, vệt nắng cam dọc tường xám cạnh khung tranh (900x900)
    d41=("source_d41.png", "", "Hình 4.1: AH+, sổ tay Công thức chọn màu nội thất"),            # 864x864
    hanh=("source_hanh.png", "doodle_ep16_hanh.npz", GIL),  # trang tên chương 4: hành lang vàng, cuối là tường xanh lam (1200x1800)
    khe=("source_khe.png", "doodle_ep16_khe.npz", GIL),     # mục 4.7: khe mở đứng gắn kính sơn vàng (600x900)
    d48=("source_d48.png", "", "Hình 4.8: AH+, ô màu minh hoạ theo ký hiệu Munsell"),          # 648x708
    d412=("source_d412.png", "", "Hình 4.12: AH+, sổ tay Công thức chọn màu nội thất"),        # 648x654
    ebook=("source_ebook.png", "", "Ảnh: sổ tay AH+ Công thức chọn màu nội thất · Giả Thuyết Kiến Trúc"),
)


def STRIP(cx, cy, z=1.0, ay=880):
    """thẻ ảnh/bản vẽ nằm gọn giữa hai khối chữ (y ~610–1240): tiêu đề ở trên, phụ đề ở dưới, chữ nâu trên nền trắng"""
    return ((cx, cy), z, (540, ay))


# Một câu hỏi trung tâm: cùng một lon sơn, vì sao phòng hướng Tây ngả cam còn phòng khuất nắng lại xám?
# Mạch: móc → tình huống của sổ tay (mục 4.1) → Foster (2011): tường không có màu cố định → mắt bù màu không trọn → vì sao nắng thấp ngả cam,
# vì sao ánh trời làm xám → Casa Gilardi: màu cùng phía ánh sáng làm ánh sáng đậm thêm (cách đọc của sổ tay) → ở nhà thì chọn ngược phía → thử mẫu → chốt.
# Khối đọc nối bằng thẻ ngắt 1,2 giây (prompt lịch chạy).
SC = [
    dict(move="push", part="A", blk=1, img="hf", head="Một lon sơn, hai căn phòng", cam=STRIP(450, 450, 0.6, 900), free=True, dark=False, dd=[],
         vo="Cùng một lon sơn, sao phòng này ngả cam, phòng kia lại xám xịt?"),
    dict(move="pan_r", part="A", blk=2, img="d41", head="Phòng Tây cuối chiều: ngả cam", cam=STRIP(432, 432, 0.6, 900), free=True, dark=False, dd=[],
         vo="Màu be ở phòng khách hướng Tây, chiều xuống là ngả cam,"),
    dict(move="hold", part="A", blk=2, img="d41", head="Phòng Bắc trời quang: xám đi", cam=STRIP(432, 432, 0.6, 900), free=True, dark=False, dd=[],
         vo="còn ở phòng ngủ hướng Bắc lại xám, thiếu sức sống."),
    dict(move="pull", part="B", blk=3, img="hf2", head="D. H. Foster (2011): tường không có một màu cố định", cam=STRIP(450, 450, 0.6, 900), free=True, dark=True, dd=["v_nang", "lab_nang"],
         vo="Theo nhà nghiên cứu Foster, bức tường không có một màu cố định,",
         tts="Theo nhà nghiên cứu Phốt-xtơ, bức tường không có một màu cố định,"),
    dict(move="hold", part="B", blk=3, img="hf2", head="Màu mình thấy: lớp sơn và ánh sáng", cam=STRIP(450, 450, 0.6, 900), free=True, dark=True, dd=["v_xam", "lab_xam"],
         vo="vì màu mình thấy tùy vào cả lớp sơn lẫn ánh sáng chiếu vào lúc đó."),
    dict(move="push", part="C", blk=4, img="hf", head="Nắng cam gặp màu ấm", cam=STRIP(450, 450, 0.6, 900), free=True, dark=True, dd=["m1", "m2", "lab_m"],
         vo="Nắng chiều vốn ngả cam, lại gặp màu be cũng ấm, nên phòng hướng Tây càng cam hơn."),
    dict(move="pan_l", part="C", blk=4, img="d41", head="Phòng Bắc: phần lớn chỉ có ánh sáng trời", cam=STRIP(432, 432, 0.6, 900), free=True, dark=False, dd=[],
         vo="Phòng hướng Bắc thì phần lớn thời gian khuất nắng, chỉ nhận ánh sáng trời."),
    dict(move="hold", part="C", blk=4, img="d41", head="Ánh sáng trời ngả xanh: màu be xám đi", cam=STRIP(432, 432, 0.6, 900), free=True, dark=False, dd=[],
         vo="Ngày trời quang, ánh sáng ấy ngả xanh, làm màu be xám đi."),
    dict(move="push", part="D", blk=5, img="hanh", head="Nhà Gilardi, Thành phố Mexico · Luis Barragán (1975–1977)", cam=STRIP(600, 900, 0.6, 900), free=True, dark=False, dd=[],
         vo="Kiến trúc sư Luis Barragán thì dùng màu để đổi chính ánh sáng.",
         tts="Kiến trúc sư Lu-ít Ba-ra-gan thì dùng màu để đổi chính ánh sáng."),
    dict(move="hold", part="D", blk=5, img="hanh", head="Nhà Gilardi, Thành phố Mexico · Luis Barragán (1975–1977)", cam=STRIP(600, 900, 0.6, 900), free=True, dark=False, dd=["tran", "lab_tran", "tuong", "lab_tuong"],
         vo="Ở nhà Gilardi tại Thành phố Mexico, hành lang ra hồ bơi sơn vàng cả tường lẫn trần,",
         tts="Ở nhà Hi-lác-đi tại Thành phố Mê-hi-cô, hành lang ra hồ bơi sơn vàng cả tường lẫn trần,"),
    dict(move="pan_d", part="D", blk=5, img="khe", head="Ô kính trên tường cũng sơn vàng", cam=STRIP(300, 450, 0.6, 900), free=True, dark=False, dd=["khe", "lab_khe"],
         vo="và cả những ô kính trên tường cũng sơn vàng."),
    dict(move="pull", part="D", blk=5, img="hanh", head="Nhìn từ sảnh: hành lang chìm trong ánh vàng", cam=STRIP(600, 900, 0.6, 900), free=True, dark=False, dd=[],
         vo="Nhìn từ sảnh, cả hành lang chìm trong ánh vàng."),
    dict(move="push", part="F", blk=6, img="d48", head="Phòng Tây: màu mát pha xám", cam=STRIP(324, 354, 0.6, 900), free=True, dark=False, dd=[],
         vo="Ở nhà mình thì chọn màu ngược tông với ánh sáng. Phòng hướng Tây chọn màu mát pha xám,"),
    dict(move="hold", part="F", blk=6, img="d48", head="Phòng khuất nắng: màu đất ấm, đủ rực", cam=STRIP(324, 354, 0.6, 900), free=True, dark=False, dd=[],
         vo="còn phòng khuất nắng chọn màu đất ấm, đủ rực để không bị xám đi."),
    dict(move="pull", part="H", blk=7, img="hf", head="Lon sơn không đổi, ánh sáng mới đổi", cam=STRIP(450, 450, 0.6, 900), free=True, dark=False, dd=[],
         vo="Vậy lon sơn không đổi, ánh sáng mới đổi."),
    dict(move="pan_r", part="F", blk=7, img="d412", head="Thử mảng lớn trên tường thật, đúng giờ", cam=STRIP(324, 327, 0.6, 900), free=True, dark=False, dd=[],
         vo="Nên trước khi sơn, mọi người thử một mảng lớn trên tường thật, vào đúng giờ hay dùng phòng."),
    dict(move="push", part="I", blk=7, img="ebook", head="end", cam="END", dark=False, vo="", dd=[],
         say="Bảng màu theo bốn nhóm hướng cửa ở Việt Nam có trong sổ tay cho thành viên, mọi người xem ở phần bình luận nha."),
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
    của run mở bằng hoà tan từ run trước (ghep_ep16.py), chữ cảnh trước mờ đi như cũ."""
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
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · MÀU THEO HƯỚNG NẮNG"'),
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
            '(1252, "Sổ tay Công thức chọn màu nội thất", 54, 240),\n    (1314, "bảng màu theo bốn nhóm hướng cửa", 48, 240),\n    (1398, "xem ở phần bình luận", 66, 255),')]
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
    open(OUT + "engine_ep16/" + dst, "w").write(s)


T = times()
for k, s in enumerate(SC):
    s["t"] = f"{T[k]:g}–{T[k + 1]:g}s"
RUNS = []
for n, ks in enumerate(runs(), 1):
    img = SC[ks[0]]["img"]
    tag = f"r{n:02d}_{img}"
    data, d0, dl = build_run(T, ks)
    build("engine_storyboard_v7.py", f"engine_ep16_{tag}.py", False, data, img, tag)
    build("engine_video.py", f"engine_video_ep16_{tag}.py", True, data, img, tag)
    RUNS.append(dict(tag=tag, img=img, src=IMGS[img][0], scenes=[k + 1 for k in ks], t_in_main=T[ks[0]],
                     cut_from=d0, cut_len=dl + (1.0 if ks[-1] == len(SC) - 1 else 0.0),
                     first_frame=2 if ks[0] > 0 else 1))
json.dump(RUNS, open(OUT + "engine_ep16/runs.json", "w"), ensure_ascii=False, indent=1)

# ảnh bìa 1080x1920: cảnh rộng trên ảnh phòng khách (lò sưởi và tranh), tiêu đề ngắn
COVER = [dict(img="hf", head="Một lon sơn, hai căn phòng", vo="Vì sao phòng hướng Tây ngả cam, phòng khuất nắng lại xám, theo sổ tay AH+.", dark=False),
         dict(img="hf", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep16.py", False,
      wrap_data([scene_line(COVER[0], 0, 3, "WIDE", []), scene_line(COVER[1], 3, 4, "END_SAFE", [])],
                DOODLE.replace("@NPZ@", "none.npz")), "hf", "cover")

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
FOREIGN = ["Foster", "Barragán", "Gilardi", "Casa", "Luis", "Mexico", "Munsell", "Oberfeld", "Hecht", "Itten", "Johannes", "Castell", "von", "Pawson", "John", "London", "AH", "Decode", "Bauhaus", "LRV", "cm"]
bad = re.findall(r"\d", " ".join(spoken)) + [w for w in FOREIGN if re.search(r"\b" + w + r"\b", " ".join(spoken))]
print("chữ số / tên nước ngoài chưa phiên âm trong bản đọc:", bad)
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep16/scenes.json", "w"), ensure_ascii=False, indent=1)
