"""Tập 13: Lò sưởi lớn màu sáng cân với bức tranh sẫm nhỏ (bài 04 kho AH-Decode-Decor, bài học 2 "Đặt một món lớn đối trọng với một nhóm món nhỏ hay một mảng sẫm màu để căn phòng lệch mà vẫn cân").
Reel nhiều ảnh theo bộ khuôn mau_tap7 (xem engine/mau_tap7/README.md), mã gốc từ gen_ep12.py. Mỗi cảnh chọn ảnh qua khoá `img` (IMGS); mỗi đoạn cảnh
liên tiếp cùng một ảnh là một "run" (engine_ep13_rNN_<ảnh>.py và engine_video_ep13_rNN_<ảnh>.py). Doodle: nét trắng mới vẽ bằng draw_ep13.py trên ảnh
gốc không doodle (anh/goc/), theo đúng nhãn doodle của bài (doodle gốc của bài 04 vẽ mực đen, không hợp quy cách nét trắng mục 6)."""
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
PHOTO = "Ảnh dự án: Palmeira Apartment, Lisbon · Studio Gameiro · ảnh Francisco Nogueira"
DGC = "Sơ đồ: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014)"
MBC = "Mặt bằng: Studio Gameiro, nguồn ArchDaily (2023) · ghi chú Giả Thuyết Kiến Trúc"
# ảnh làm việc: (file, npz doodle, credit). Ảnh chụp lấy từ anh/goc/ của bài (ảnh gốc không doodle), thu về 2400 px; dải cắt *b là một phần của ảnh vuông
IMGS = dict(
    rong=("source_rong.png", "doodle_ep13_rong.npz", PHOTO),        # ảnh ArchDaily 21 (ngang): phòng khách nhìn từ cửa, lò sưởi trái, tranh phải
    bat=("source_bat.png", "", DGC),                                # ảnh 01: khung "bất đối xứng" (khối lớn bên này, nhóm nhỏ sẫm bên kia, điểm tựa bập bênh)
    dg=("source_dg.png", "", DGC),                                  # ảnh 02: đòn bẩy, phần hình và phụ đề (bỏ tiêu đề lớn)
    dgb=("source_dgb.png", "", DGC),                                # ảnh 02: phần nhãn "xa trục" và dòng tổng kết ba yếu tố
    mb=("source_mb.png", "", MBC),                                  # ảnh 03: vùng phòng khách, lỗ cửa giữa, phòng ăn
    khachb=("source_khachb.png", "doodle_ep13_khachb.npz", PHOTO),  # ảnh 06 (goc), dải y 560-1760 của ảnh xem: lò sưởi, tủ cổ, tranh, sofa
    nhomb=("source_nhomb.png", "doodle_ep13_nhomb.npz", PHOTO),    # ảnh 06 (goc), dải dưới bên phải: sofa, ghế gỗ đen, bình hoa khô, mép dưới bức tranh
    tub=("source_tub.png", "doodle_ep13_tub.npz", PHOTO),          # ảnh 06 (goc), dải giữa: tủ cổ gỗ đậm gần trục giữa
    trucb=("source_trucb.png", "doodle_ep13_trucb.npz", PHOTO),     # ảnh 10 (goc), dải y 300-1560: hoa trần (đáy), lỗ cửa giữa, hai hốc kệ
)


def STRIP(cx, cy, z=1.0, ay=880):
    """thẻ ảnh/bản vẽ nằm gọn giữa hai khối chữ (y ~610–1240): tiêu đề ở trên, phụ đề ở dưới, chữ nâu trên nền trắng"""
    return ((cx, cy), z, (540, ay))


# Lời đọc bản 1: viết liền thành năm khối trước (mục 4 bước 4a), rồi mới cắt cảnh. Khối nối bằng từ khóa
# (ngang nhau → thăng bằng → nặng → trục → trục có sẵn). Thẻ ngắt 1,2 giây giữa các khối (prompt lịch chạy, như tập 11, 12).
SC = [
    dict(move="push", part="A", blk=1, img="rong", head="Hai bên khác hẳn mà căn phòng không nghiêng", cam=STRIP(1000, 667, 0.81, 863), free=True, dark=False, dd=[],
         vo="Một bên phòng khách là chiếc lò sưởi rất to, bên kia treo một bức tranh nhỏ hơn, vậy vì sao căn phòng không nghiêng?"),
    dict(move="push", part="B", blk=2, img="bat", head="Theo Kilmer & Kilmer (2014), mắt cân đồ như cân bập bênh", cam=STRIP(348, 504, 0.52, 863), free=True, dark=False, dd=[],
         vo="Theo hai tác giả Kilmer, hai bên căn phòng không cần giống nhau, miễn là mắt thấy được thăng bằng.",
         tts="Theo hai tác giả Kin-mơ, hai bên căn phòng không cần giống nhau, miễn là mắt thấy được thăng bằng."),
    dict(move="pan_l", part="C", blk=2, img="dgb", head="Theo Arnheim (1954), điều làm món đồ nặng thêm", cam=STRIP(1080, 530, 1.1, 863), free=True, dark=False, dd=[],
         vo="Năm 1954, nhà tâm lý học Rudolf Arnheim cho rằng món đồ càng to, màu càng nổi trên nền thì trong mắt người càng nặng,",
         tts="Năm một nghìn chín trăm năm mươi bốn, nhà tâm lý học Ru-đôn Ác-nhai-mơ cho rằng món đồ càng to, màu càng nổi trên nền thì trong mắt người càng nặng,"),
    dict(move="push", part="C", blk=2, img="dg", head="Theo Arnheim (1954), điều làm món đồ nặng thêm", cam=STRIP(1080, 660, 0.88, 863), free=True, dark=False, dd=[],
         vo="và càng xa trục giữa phòng, tức đường chia đôi căn phòng, thì càng nặng,"),
    dict(move="hold", part="C", blk=2, img="dg", head="Theo Arnheim (1954), điều làm món đồ nặng thêm", cam=STRIP(1080, 660, 0.88, 863), free=True, dark=False, dd=[],
         vo="như người ngồi càng xa điểm tựa bập bênh thì càng đè mạnh."),
    dict(move="pan_u", part="D", blk=3, img="mb", head="Phòng khách ở Palmeira, Lisbon", cam=STRIP(976, 665, 0.9, 900), free=True, dark=False, dd=[],
         vo="Ở phòng khách của căn hộ Palmeira,",
         tts="Ở phòng khách của căn hộ Pan-mây-ra,"),
    dict(move="push", part="D", blk=3, img="khachb", head="Món to mà cùng màu tường thì không nặng lắm", cam=STRIP(1200, 745, 0.87, 863), free=True, dark=False, dd=["ls", "lab_ls"],
         vo="lò sưởi tuy to hơn bức tranh, nhưng cùng màu với tường nên không nặng lắm."),
    dict(move="pan_r", part="D", blk=3, img="khachb", head="Món nhỏ mà đậm, xa trục thì nặng thêm", cam=STRIP(1200, 745, 0.87, 863), free=True, dark=False, dd=["tr", "ax", "lab_tr", "lab_ax"],
         vo="Bức tranh nhỏ hơn mà màu đậm nhất phòng, lại treo xa trục,"),
    dict(move="pan_d", part="D", blk=3, img="nhomb", head="Nhiều món gần nhau thành một mảng", cam=STRIP(603, 522, 0.63, 863), free=True, dark=False, dd=["tr_n", "lab_tr", "grp"],
         vo="và cùng với sofa, ghế gỗ đen, bình hoa khô, nhìn trong ảnh giống như một mảng liền, nên hai bên gần như ngang nhau.",
         tts="và cùng với sô-pha, ghế gỗ đen, bình hoa khô, nhìn trong ảnh giống như một mảng liền, nên hai bên gần như ngang nhau."),
    dict(move="pull", part="E", blk=4, img="trucb", head="Mắt cần điểm tựa, đó là trục giữa phòng", cam=STRIP(1200, 782, 0.8, 863), free=True, dark=False, dd=["ax", "lab_ax"],
         vo="Theo cách tụi mình hiểu, mắt người cần một điểm tựa, chính là trục giữa phòng, và kê lệch thì nên lệch quanh trục ấy."),
    dict(move="hold", part="E", blk=4, img="trucb", head="Hoa trần và hai hốc kệ giữ trục", cam=STRIP(1200, 782, 0.8, 863), free=True, dark=False, dd=["ht", "lab_ht", "hk_l", "hk_r", "lab_hk"],
         vo="Phòng khách này có sẵn trục nhờ hoa trần ở giữa và hai hốc kệ giống nhau."),
    dict(move="push", part="E", blk=4, img="tub", head="Một chỗ dừng cho mắt cạnh trục", cam=STRIP(652, 385, 0.74, 863), free=True, dark=False, dd=["tu", "ax", "lab_tu", "lab_ax"],
         vo="Chiếc tủ cổ gỗ đậm đứng gần trục còn cho mắt một chỗ dừng."),
    dict(move="pan_u", part="F", blk=5, img="bat", head="Ở nhà mình, bắt đầu từ trục có sẵn", cam=STRIP(348, 504, 0.52, 863), free=True, dark=False, dd=[],
         vo="Vì vậy, muốn kê lệch mà vẫn cân, nên tìm trước một cái trục có sẵn, như ô cửa ban công hay bàn thờ."),
    dict(move="hold", part="F", blk=5, img="bat", head="Đặt gì để cân lại món to nhất", cam=STRIP(348, 504, 0.52, 863), free=True, dark=False, dd=[],
         vo="Quanh trục ấy, món to nhất, thường là sofa, cần một món cân lại ở phía bên kia, như bức tranh màu đậm.",
         tts="Quanh trục ấy, món to nhất, thường là sô-pha, cần một món cân lại ở phía bên kia, như bức tranh màu đậm."),
    dict(move="pan_l", part="H", blk=5, img="rong", head="Hai bên nặng ngang nhau trong mắt", cam=STRIP(1000, 667, 0.81, 863), free=True, dark=False, dd=["ls", "tr", "a_ls", "a_tr", "lab_dt"],
         vo="Món ấy không cần to bằng, vì căn phòng không nghiêng khi hai bên nặng ngang nhau trong mắt người."),
    dict(move="push", part="I", blk=5, img="rong", head="end", cam="END", dark=False, vo="", dd=[],
         say="Bài phân tích về cân bằng thị giác, từ sách của hai tác giả Kilmer, mọi người xem ở phần bình luận.",
         tts="Bài phân tích về cân bằng thị giác, từ sách của hai tác giả Kin-mơ, mọi người xem ở phần bình luận."),
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
    của run mở bằng hoà tan từ run trước (ghep_ep13.py), chữ cảnh trước mờ đi như cũ."""
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
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"'),
           ("CARD_W2, BORDER2 = 1920, 0", f"CARD_W2, BORDER2 = {cw}, 0  # theo tỷ lệ ảnh của run"),
           ("C2 = (B2W / 2, 1810.0)", f"C2 = (B2W / 2, {cy})"),
           ("borderMode=cv2.BORDER_REFLECT)", "borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255, 0))"),
           # cảnh nối không chữ (trước khung cuối): không vẽ header, không phủ tối dải chữ
           ("    t.put((60, SAFE_Y0 + 4), HEAD, 34, 220)\n", "    if sc[\"head\"]:\n        t.put((60, SAFE_Y0 + 4), HEAD, 34, 220)\n"),
           ("    return top < TOP_END, bot > cr_y - 20, warn", "    return top < TOP_END and bool(sc[\"head\"]), bot > cr_y - 20 and bool(sc[\"vo\"]), warn"),
           # khung cuối: chữ khớp lời mời (mẫu tập 7)
           ('(1196, "Bài viết phân tích đầy đủ", 58, 240),\n    (1260, "xem ở dòng đầu tiên", 58, 240),\n    (1348, "trong phần bình luận", 66, 255),',
            '(1180, "Bài phân tích về cân bằng thị giác", 56, 240),\n    (1244, "từ sách của Kilmer & Kilmer (2014)", 50, 240),\n    (1330, "xem ở phần bình luận", 66, 255),')]
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
    open(OUT + "engine_ep13/" + dst, "w").write(s)


T = times()
for k, s in enumerate(SC):
    s["t"] = f"{T[k]:g}–{T[k + 1]:g}s"
RUNS = []
for n, ks in enumerate(runs(), 1):
    img = SC[ks[0]]["img"]
    tag = f"r{n:02d}_{img}"
    data, d0, dl = build_run(T, ks)
    build("engine_storyboard_v7.py", f"engine_ep13_{tag}.py", False, data, img, tag)
    build("engine_video.py", f"engine_video_ep13_{tag}.py", True, data, img, tag)
    RUNS.append(dict(tag=tag, img=img, src=IMGS[img][0], scenes=[k + 1 for k in ks], t_in_main=T[ks[0]],
                     cut_from=d0, cut_len=dl + (1.0 if ks[-1] == len(SC) - 1 else 0.0),
                     first_frame=2 if ks[0] > 0 else 1))
json.dump(RUNS, open(OUT + "engine_ep13/runs.json", "w"), ensure_ascii=False, indent=1)

# ảnh bìa 1080x1920: cảnh rộng trên ảnh phòng khách (lò sưởi và tranh), tiêu đề ngắn
COVER = [dict(img="rong", head="Lò sưởi to, tranh nhỏ, sao vẫn cân?", vo="Cân bằng thị giác khi bày biện nội thất, theo Kilmer & Kilmer (2014).", dark=False),
         dict(img="rong", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep13.py", False,
      wrap_data([scene_line(COVER[0], 0, 3, "WIDE", []), scene_line(COVER[1], 3, 4, "END_SAFE", [])],
                DOODLE.replace("@NPZ@", "none.npz")), "rong", "cover")

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
FOREIGN = ["Kilmer", "Palmeira", "Lisbon", "Studio", "Gameiro", "AH", "Decode", "Arnheim", "Rudolf", "sofa"]
bad = re.findall(r"\d", " ".join(spoken)) + [w for w in FOREIGN if re.search(r"\b" + w + r"\b", " ".join(spoken))]
print("chữ số / tên nước ngoài chưa phiên âm trong bản đọc:", bad)
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep13/scenes.json", "w"), ensure_ascii=False, indent=1)
