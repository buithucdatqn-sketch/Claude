"""Tập 14: Sơn trắng làm phòng hẹp rộng thêm bao nhiêu (sổ tay AH+ "Công thức chọn màu nội thất", kho AH-Decode-Decor/so-tay-cong-thuc-chon-mau-noi-that/,
chương 1 "Kiểm soát ánh sáng trong không gian hẹp", mục 1.2 "Mặt bao quanh càng sáng, phòng càng rộng", 1.3 "Ba bước áp dụng", 1.4 Pawson House).
Reel nhiều ảnh theo bộ khuôn mau_tap7 (xem engine/mau_tap7/README.md), mã gốc từ gen_ep13.py. Mỗi cảnh chọn ảnh qua khoá `img` (IMGS); mỗi đoạn cảnh
liên tiếp cùng một ảnh là một "run" (engine_ep14_rNN_<ảnh>.py và engine_video_ep14_rNN_<ảnh>.py). Ảnh lấy từ chính file PDF của chương (pdfimages),
không phóng to. Doodle: nét trắng mới vẽ bằng draw_ep14.py (ảnh trong sổ tay không có doodle)."""
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
PAW = "Ảnh dự án: Pawson House, London (1997–1999) · John Pawson · ảnh Todd Eberle"
HANH = "Ảnh: Ryunosuke Kikuno / Unsplash, qua sổ tay AH+ Công thức chọn màu nội thất"
KHE = "Ảnh: Danielle-Claude Bélanger / Unsplash, qua sổ tay AH+ Công thức chọn màu nội thất"
DGC = "Hình 1.2: AH+, theo von Castell, Hecht và Oberfeld (2018)"
LRVC = "Hình M.1: AH+, số liệu Dulux Australia, dải TCVN 7114-1"
# ảnh làm việc: (file, npz doodle, credit). Tất cả lấy từ PDF chương 1 và phần mở đầu của sổ tay (pdfimages, kích thước gốc)
IMGS = dict(
    hanh=("source_hanh.png", "doodle_ep14_hanh.npz", HANH),      # trang tên chương 1: hành lang, dải cắt (100, 470, 1300, 1900) của ảnh 1325x1988
    khe=("source_khe.png", "doodle_ep14_khe.npz", KHE),          # mục 1.3: góc phòng tường trắng, dải cắt (0, 0, 1164, 1100) của ảnh 1164x1745
    dg=("source_dg.png", "", DGC),                               # Hình 1.2 "Tường sáng nới phòng" (648x606)
    lrv=("source_lrv.png", "", LRVC),                            # Hình M.1 "LRV: phần ánh sáng bề mặt trả lại" (648x621)
    banan=("source_banan.png", "doodle_ep14_banan.npz", PAW),    # Pawson House: bàn ăn, vách kính ra vườn (1200x948)
    thang=("source_thang.png", "doodle_ep14_thang.npz", PAW),    # Pawson House: cầu thang một vế, dải cắt (0, 0, 632, 560) của ảnh 632x800
    bep=("source_bep.png", "doodle_ep14_bep.npz", PAW),          # Pawson House: bếp tầng sát vườn, tường trắng, sàn đá (1200x948)
)


def STRIP(cx, cy, z=1.0, ay=880):
    """thẻ ảnh/bản vẽ nằm gọn giữa hai khối chữ (y ~610–1240): tiêu đề ở trên, phụ đề ở dưới, chữ nâu trên nền trắng"""
    return ((cx, cy), z, (540, ay))


# Lời đọc: viết liền thành sáu khối trước (mục 0.6h), rồi mới cắt cảnh. Khối nối bằng từ khóa
# (rộng → tương phản → sáng hơn → độ sáng → cùng sáng → giữ ánh sáng → vài xăng-ti-mét). Thẻ ngắt 1,2 giây giữa các khối (prompt lịch chạy).
SC = [
    dict(move="push", part="A", blk=1, img="hanh", head="Phòng hẹp và màu sơn trắng", cam=STRIP(600, 715, 0.545, 865), free=True, dark=False, dd=[],
         vo="Sơn trắng cho phòng hẹp trông rộng hơn, nhưng rộng thêm được bao nhiêu?"),
    dict(move="push", part="C", blk=2, img="dg", head="Thí nghiệm của von Castell và cộng sự (2018)", cam=STRIP(324, 303, 0.56, 863), free=True, dark=False, dd=[],
         vo="Năm 2018, nhóm của von Castell thử sơn sáng hơn hai bức tường bên của một căn phòng ảo cỡ thật.",
         tts="Năm hai nghìn không trăm mười tám, nhóm của phôn Cát-xten thử sơn sáng hơn hai bức tường bên của một căn phòng ảo cỡ thật."),
    dict(move="pan_r", part="C", blk=2, img="dg", head="Rộng thêm chưa tới nửa gang tay", cam=STRIP(324, 303, 0.56, 863), free=True, dark=False, dd=[],
         vo="Người xem thấy phòng rộng thêm gần 8 cm, tức là chưa tới nửa gang tay.",
         tts="Người xem thấy phòng rộng thêm gần tám xăng-ti-mét, tức là chưa tới nửa gang tay."),
    dict(move="pan_d", part="C", blk=3, img="khe", head="Câu trả lời cho câu hỏi đầu", cam=STRIP(582, 550, 0.57, 863), free=True, dark=True, dd=[],
         vo="Sơn sáng có làm phòng trông rộng hơn, nhưng chỉ một chút."),
    dict(move="hold", part="C", blk=3, img="khe", head="Vẫn nên sơn tường và trần thật sáng", cam=STRIP(582, 550, 0.57, 863), free=True, dark=True, dd=["a_tran", "lab_tran", "a_tuong", "lab_tuong"],
         vo="Dù vậy, chính nhóm này vẫn khuyên sơn tường và trần sáng nhất có thể."),
    dict(move="push", part="F", blk=3, img="hanh", head="Áp dụng ở nhà mình", cam=STRIP(600, 715, 0.545, 865), free=True, dark=True, dd=["khuon", "len_l", "len_r", "lab_cung"],
         vo="Ở nhà mình, nên sơn tường, khuôn cửa và len chân tường cùng một màu sáng, để cả phòng cùng sáng."),
    dict(move="push", part="D", blk=4, img="banan", head="Ánh sáng phải vào nhà trước", cam=STRIP(600, 474, 0.68, 863), free=True, dark=True, dd=["a_kinh", "lab_vao"],
         vo="Nhưng sơn chỉ giữ lại được ánh sáng đã vào nhà."),
    dict(move="hold", part="D", blk=4, img="banan", head="Pawson House, London (1997–1999)", cam=STRIP(600, 474, 0.68, 863), free=True, dark=True, dd=[],
         vo="Nhà riêng của kiến trúc sư John Pawson ở London từng có nhiều phòng nhỏ và tối.",
         tts="Nhà riêng của kiến trúc sư Giôn Pô-xơn ở Luân Đôn từng có nhiều phòng nhỏ và tối."),
    dict(move="hold", part="D", blk=4, img="banan", head="Pawson House, London (1997–1999)", cam=STRIP(600, 474, 0.68, 863), free=True, dark=True, dd=["kinh", "lab_kinh"],
         vo="Khi cải tạo, ông mở vách kính ra vườn cho ánh sáng vào,"),
    dict(move="push", part="D", blk=4, img="thang", head="Tường trắng và sàn đá", cam=STRIP(316, 280, 0.57, 863), free=True, dark=True, dd=["tw", "lab_tw"],
         vo="rồi tường sơn trắng"),
    dict(move="pan_r", part="D", blk=4, img="bep", head="Tường trắng và sàn đá", cam=STRIP(600, 474, 0.68, 863), free=True, dark=True, dd=["san", "lab_san"],
         vo="và sàn lát đá giữ ánh sáng ấy lại."),
    dict(move="pull", part="H", blk=5, img="hanh", head="Thứ tự cho phòng hẹp", cam=STRIP(600, 715, 0.545, 865), free=True, dark=False, dd=[],
         vo="Vậy với phòng hẹp, hãy lo đưa ánh sáng vào trước,"),
    dict(move="hold", part="H", blk=5, img="hanh", head="Thứ tự cho phòng hẹp", cam=STRIP(600, 715, 0.545, 865), free=True, dark=False, dd=[],
         vo="như bỏ bớt vách ngăn hay thêm đèn hắt tường ở cuối phòng, rồi mới chọn màu sơn thật sáng."),
    dict(move="push", part="I", blk=5, img="banan", head="end", cam="END", dark=False, vo="", dd=[],
         say="Sổ tay Công thức chọn màu nội thất dành cho thành viên có bảng tra nhanh mười bảy tình huống chọn màu, mọi người xem ở phần bình luận."),
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
    của run mở bằng hoà tan từ run trước (ghep_ep14.py), chữ cảnh trước mờ đi như cũ."""
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
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · MÀU CHO PHÒNG HẸP"'),
           ("CARD_W2, BORDER2 = 1920, 0", f"CARD_W2, BORDER2 = {cw}, 0  # theo tỷ lệ ảnh của run"),
           ("C2 = (B2W / 2, 1810.0)", f"C2 = (B2W / 2, {cy})"),
           ("borderMode=cv2.BORDER_REFLECT)", "borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255, 0))"),
           # cảnh nối không chữ (trước khung cuối): không vẽ header, không phủ tối dải chữ
           ("    t.put((60, SAFE_Y0 + 4), HEAD, 34, 220)\n", "    if sc[\"head\"]:\n        t.put((60, SAFE_Y0 + 4), HEAD, 34, 220)\n"),
           ("    return top < TOP_END, bot > cr_y - 20, warn", "    return top < TOP_END and bool(sc[\"head\"]), bot > cr_y - 20 and bool(sc[\"vo\"]), warn"),
           # khung cuối: chữ khớp lời mời (mẫu tập 7)
           ('(1196, "Bài viết phân tích đầy đủ", 58, 240),\n    (1260, "xem ở dòng đầu tiên", 58, 240),\n    (1348, "trong phần bình luận", 66, 255),',
            '(1180, "Sổ tay Công thức chọn màu nội thất", 54, 240),\n    (1244, "bảng tra nhanh 17 tình huống chọn màu", 48, 240),\n    (1330, "xem ở phần bình luận", 66, 255),')]
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
    open(OUT + "engine_ep14/" + dst, "w").write(s)


T = times()
for k, s in enumerate(SC):
    s["t"] = f"{T[k]:g}–{T[k + 1]:g}s"
RUNS = []
for n, ks in enumerate(runs(), 1):
    img = SC[ks[0]]["img"]
    tag = f"r{n:02d}_{img}"
    data, d0, dl = build_run(T, ks)
    build("engine_storyboard_v7.py", f"engine_ep14_{tag}.py", False, data, img, tag)
    build("engine_video.py", f"engine_video_ep14_{tag}.py", True, data, img, tag)
    RUNS.append(dict(tag=tag, img=img, src=IMGS[img][0], scenes=[k + 1 for k in ks], t_in_main=T[ks[0]],
                     cut_from=d0, cut_len=dl + (1.0 if ks[-1] == len(SC) - 1 else 0.0),
                     first_frame=2 if ks[0] > 0 else 1))
json.dump(RUNS, open(OUT + "engine_ep14/runs.json", "w"), ensure_ascii=False, indent=1)

# ảnh bìa 1080x1920: cảnh rộng trên ảnh phòng khách (lò sưởi và tranh), tiêu đề ngắn
COVER = [dict(img="hanh", head="Sơn trắng nới phòng được bao nhiêu?", vo="Màu cho không gian hẹp, theo sổ tay AH+ Công thức chọn màu nội thất.", dark=False),
         dict(img="hanh", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep14.py", False,
      wrap_data([scene_line(COVER[0], 0, 3, "WIDE", []), scene_line(COVER[1], 3, 4, "END_SAFE", [])],
                DOODLE.replace("@NPZ@", "none.npz")), "hanh", "cover")

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
FOREIGN = ["Oberfeld", "Hecht", "Itten", "Johannes", "Castell", "von", "Pawson", "John", "London", "AH", "Decode", "Bauhaus", "LRV", "cm"]
bad = re.findall(r"\d", " ".join(spoken)) + [w for w in FOREIGN if re.search(r"\b" + w + r"\b", " ".join(spoken))]
print("chữ số / tên nước ngoài chưa phiên âm trong bản đọc:", bad)
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep14/scenes.json", "w"), ensure_ascii=False, indent=1)
