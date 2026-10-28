"""Tập 15: Căn hộ mở bỏ vách ngăn, ranh giới nằm lại trên sàn (sổ tay AH+ "Công thức chọn màu nội thất", kho AH-Decode-Decor/so-tay-cong-thuc-chon-mau-noi-that/,
chương 2 "Phân vùng chức năng bằng màu sắc trong không gian mở", mục 2.1 và 2.3 nhà Rietveld Schröder).
Reel nhiều ảnh theo bộ khuôn mau_tap7 (xem engine/mau_tap7/README.md), mã gốc từ gen_ep14.py. Ảnh lấy từ chính file PDF của chương (pdfimages),
không phóng to. Doodle: nét trắng mới vẽ bằng draw_ep15.py (ảnh trong sổ tay không có doodle)."""
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
RIET = "Ảnh: Nhà Rietveld Schröder (1924) · Stijn Poelstra / Centraal Museum, qua Dezeen"
# ảnh làm việc: (file, npz doodle, credit). Tất cả lấy từ PDF chương 2 của sổ tay (pdfimages, kích thước gốc)
IMGS = dict(
    bep=("source_bep.png", "doodle_ep15_bep.npz", RIET),         # mục 2.1: bếp và bàn ăn chung một không gian (1182x788)
    thang=("source_thang.png", "", RIET),                        # mục 2.3: hộp kính khung trắng bao quanh cầu thang (946x1419)
    tang=("source_tang.png", "doodle_ep15_tang.npz", RIET),      # mục 2.3: tầng trên khi các vách trượt mở (1182x788)
    phong=("source_phong.png", "doodle_ep15_phong.npz", RIET),   # mục 2.3: phòng sàn đỏ, ghế Đỏ-Lam (1182x788)
    ebook=("source_ebook.png", "", "Ảnh: sổ tay AH+ Công thức chọn màu nội thất · Giả Thuyết Kiến Trúc"),  # ảnh chủ Trang gửi 2026-10-28 cho khung cuối (800x1000)
)


def STRIP(cx, cy, z=1.0, ay=880):
    """thẻ ảnh/bản vẽ nằm gọn giữa hai khối chữ (y ~610–1240): tiêu đề ở trên, phụ đề ở dưới, chữ nâu trên nền trắng"""
    return ((cx, cy), z, (540, ay))


# Lời đọc: viết liền thành năm khối trước (mục 0.6h), rồi mới cắt cảnh. Khối nối bằng từ khóa
# (vách ngăn → nền màu → vách trượt → mặt sàn → ranh giới → sàn hoặc trần). Thẻ ngắt 1,2 giây giữa các khối (prompt lịch chạy).
# Giai đoạn B: lời sửa theo ghi âm của chủ Trang, cắt cảnh tại quãng nghỉ.
SC = [
    dict(move="push", part="A", blk=1, img="bep", head="Căn hộ mở, bỏ vách ngăn", cam=STRIP(591, 394, 0.9, 897), free=True, dark=False, dd=[],
         vo="Bỏ vách ngăn cho căn hộ thoáng, vậy bếp với phòng khách còn tách nhau bằng gì?"),
    dict(move="pan_r", part="C", blk=2, img="bep", head="Bỏ vách, cả sàn là một nền màu", cam=STRIP(591, 394, 0.9, 897), free=True, dark=True, dd=["san", "lab_san"],
         vo="Bỏ vách xong, phòng khách, bếp và bàn ăn nằm chung một nền màu,"),
    dict(move="hold", part="C", blk=2, img="bep", head="Khu vực chỉ nhận ra nhờ đồ đạc", cam=STRIP(591, 394, 0.9, 897), free=True, dark=True, dd=["ghe", "lab_ghe", "quay", "lab_quay", "ban", "lab_ban"],
         vo="nên người ở chỉ nhận ra từng khu nhờ đồ đạc, và cả căn dễ loang thành một khoảng."),
    dict(move="pull", part="B", blk=3, img="thang", head="Theo sổ tay, nhà Rietveld Schröder (1924)", cam=STRIP(473, 709, 0.5, 878), free=True, dark=False, dd=[],
         vo="Muốn biết khi vách mất thì lấy gì chia chỗ, sổ tay dẫn tới nhà Rietveld Schröder ở Utrecht, do Gerrit Rietveld thiết kế năm 1924,",
         tts="Muốn biết khi vách mất thì lấy gì chia chỗ, sổ tay dẫn tới nhà Rít-ve-lơ Xờ-rô-đơ ở Ú-trếch, do Hê-rít Rít-ve-lơ thiết kế năm một nghìn chín trăm hai mươi bốn,"),
    dict(move="hold", part="B", blk=3, img="thang", head="Theo sổ tay, nhà Rietveld Schröder (1924)", cam=STRIP(473, 709, 0.5, 878), free=True, dark=False, dd=[],
         vo="một ví dụ kinh điển về mặt bằng mở dùng màu để chia chỗ."),
    dict(move="pan_l", part="C", blk=3, img="tang", head="Ban ngày tầng trên để mở", cam=STRIP(591, 394, 0.9, 897), free=True, dark=True, dd=["chung", "lab_chung"],
         vo="Tầng trên ban ngày để mở, tối mới kéo vách chia phòng. Ảnh này chụp lúc vách đã thu lại,"),
    dict(move="push", part="D", blk=3, img="tang", head="Vách thu lại, sàn vẫn chia mảng", cam=STRIP(591, 394, 0.9, 897), free=True, dark=True, dd=["do", "lab_do", "den", "lab_den", "a_trang", "lab_trang"],
         vo="mà sàn vẫn chia thành các mảng đỏ, đen, trắng có viền rõ,"),
    dict(move="hold", part="D", blk=3, img="tang", head="Trần cũng có thanh màu", cam=STRIP(591, 394, 0.9, 897), free=True, dark=True, dd=["t_do", "t_den", "t_vang", "lab_tran"],
         vo="còn trên trần có vài thanh đỏ, lam, vàng."),
    dict(move="pan_d", part="C", blk=4, img="phong", head="Vách thu lại, ranh giới ở lại trên sàn", cam=STRIP(591, 394, 0.9, 897), free=True, dark=True, dd=["mang", "lab_ranh"],
         vo="Sổ tay hiểu rằng vách thì thu lại được, còn ranh giới giữa các khu vẫn ở lại trên sàn."),
    dict(move="hold", part="C", blk=4, img="phong", head="Màu là cách báo hiệu rẻ nhất", cam=STRIP(591, 394, 0.9, 897), free=True, dark=True, dd=[],
         vo="Theo kinh nghiệm của sổ tay, màu là cách báo hiệu từng khu với chi phí thấp nhất và dễ đổi nhất."),
    dict(move="push", part="F", blk=4, img="phong", head="Đặt màu xuống sàn hoặc lên trần", cam=STRIP(591, 394, 0.9, 897), free=True, dark=True, dd=["tran_l", "a_tran", "lab_lt", "lab_xs"],
         vo="Vì vậy, nếu bỏ vách, mọi người có thể thử đặt màu xuống sàn hoặc lên trần, chứ đừng chỉ trông vào vách."),
    dict(move="push", part="I", blk=5, img="ebook", head="end", cam="END", dark=False, vo="", dd=[],
         say="Chương không gian mở trong sổ tay Công thức chọn màu nội thất, kèm bảng kiểm tra phân vùng, dành cho thành viên, mọi người xem ở phần bình luận."),
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
    của run mở bằng hoà tan từ run trước (ghep_ep15.py), chữ cảnh trước mờ đi như cũ."""
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
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · CĂN HỘ MỞ"'),
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
            '(1252, "Sổ tay Công thức chọn màu nội thất", 54, 240),\n    (1314, "chương không gian mở, danh mục phân vùng", 44, 240),\n    (1398, "xem ở phần bình luận", 66, 255),')]
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
    open(OUT + "engine_ep15/" + dst, "w").write(s)


T = times()
for k, s in enumerate(SC):
    s["t"] = f"{T[k]:g}–{T[k + 1]:g}s"
RUNS = []
for n, ks in enumerate(runs(), 1):
    img = SC[ks[0]]["img"]
    tag = f"r{n:02d}_{img}"
    data, d0, dl = build_run(T, ks)
    build("engine_storyboard_v7.py", f"engine_ep15_{tag}.py", False, data, img, tag)
    build("engine_video.py", f"engine_video_ep15_{tag}.py", True, data, img, tag)
    RUNS.append(dict(tag=tag, img=img, src=IMGS[img][0], scenes=[k + 1 for k in ks], t_in_main=T[ks[0]],
                     cut_from=d0, cut_len=dl + (1.0 if ks[-1] == len(SC) - 1 else 0.0),
                     first_frame=2 if ks[0] > 0 else 1))
json.dump(RUNS, open(OUT + "engine_ep15/runs.json", "w"), ensure_ascii=False, indent=1)

# ảnh bìa 1080x1920: cảnh rộng trên ảnh phòng khách (lò sưởi và tranh), tiêu đề ngắn
COVER = [dict(img="tang", head="Bỏ vách, ranh giới ở đâu?", vo="Phân vùng căn hộ mở bằng màu, theo sổ tay AH+ Công thức chọn màu nội thất.", dark=False),
         dict(img="tang", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep15.py", False,
      wrap_data([scene_line(COVER[0], 0, 3, "WIDE", []), scene_line(COVER[1], 3, 4, "END_SAFE", [])],
                DOODLE.replace("@NPZ@", "none.npz")), "tang", "cover")

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
FOREIGN = ["Rietveld", "Schröder", "Gerrit", "Utrecht", "AH", "Decode", "De", "Stijl", "UNESCO"]
bad = re.findall(r"\d", " ".join(spoken)) + [w for w in FOREIGN if re.search(r"\b" + w + r"\b", " ".join(spoken))]
print("chữ số / tên nước ngoài chưa phiên âm trong bản đọc:", bad)
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep15/scenes.json", "w"), ensure_ascii=False, indent=1)
