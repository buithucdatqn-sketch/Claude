"""Tập 12: Đối xứng dành cho chỗ cần yên, như đầu giường (bài 04 kho AH-Decode-Decor, bài học 1 "Dùng cân bằng đối xứng cho những chỗ cần sự yên ổn, như đầu giường").
Reel nhiều ảnh theo bộ khuôn mau_tap7 (xem engine/mau_tap7/README.md), mã gốc từ gen_ep12.py. Mỗi cảnh chọn ảnh qua khoá `img` (IMGS); mỗi đoạn cảnh
liên tiếp cùng một ảnh là một "run" (engine_ep12_rNN_<ảnh>.py và engine_video_ep12_rNN_<ảnh>.py). Doodle: nét trắng mới vẽ bằng draw_ep12.py trên ảnh
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
    ngu=("source_ngu.png", "doodle_ep12_ngu.npz", PHOTO),        # ảnh 04 (goc): đầu giường phòng ngủ chính
    ngub=("source_ngub.png", "doodle_ep12_ngub.npz", PHOTO),     # ảnh 04 (goc), dải giữa: đèn thả và tấm đầu giường
    dg=("source_dg.png", "", DGC),                               # ảnh 01: hàng ba kiểu cân bằng (bỏ tiêu đề lớn)
    dgl=("source_dgl.png", "", DGC),                             # ảnh 01: khung "đối xứng"
    mb=("source_mb.png", "", MBC),                               # ảnh 03: vùng phòng ngủ chính, phòng tắm chính
    tam=("source_tam.png", "doodle_ep12_tam.npz", PHOTO),        # ảnh 05 (goc): hai vòi sen trong vách kính
    tamb=("source_tamb.png", "doodle_ep12_tamb.npz", PHOTO),     # ảnh 05 (goc), dải dưới: chậu rửa, vách kính, bồn vệ sinh
    khachb=("source_khachb.png", "doodle_ep12_khachb.npz", PHOTO),  # ảnh 10 (goc), dải dưới: sofa, ghế đen, lò sưởi
)


def STRIP(cx, cy, z=1.0, ay=880):
    """thẻ ảnh/bản vẽ nằm gọn giữa hai khối chữ (y ~610–1240): tiêu đề ở trên, phụ đề ở dưới, chữ nâu trên nền trắng"""
    return ((cx, cy), z, (540, ay))


# Lời đọc bản 3 (sau lượt chấm 1): viết liền thành bốn khối trước (mục 4 bước 4a), rồi mới cắt cảnh. Khối nối bằng từ khóa
# (thăng bằng → đối xứng → trục giữa → kê lệch → đối xứng quá nhiều). Thẻ ngắt 1,2 giây giữa các khối (prompt lịch chạy, như tập 11).
SC = [
    dict(move="push", part="A", blk=1, img="ngu", head="Một căn hộ, hai cách kê đồ", cam=STRIP(1200, 1200, 0.6, 890), free=True, dark=False, dd=[],
         vo="Phòng khách kê lệch hẳn, vậy vì sao đầu giường trong căn hộ này lại được kê đối xứng?"),
    dict(move="pan_u", part="B", blk=2, img="dg", head="Theo Kilmer & Kilmer (2014), mắt cũng giữ thăng bằng", cam=STRIP(1045, 615, 0.9, 856), free=True, dark=False, dd=[],
         vo="Trong một cuốn sách năm 2014 về thiết kế nội thất, hai tác giả Kilmer cho rằng mắt người cũng giữ thăng bằng như cơ thể.",
         tts="Trong một cuốn sách năm hai nghìn không trăm mười bốn về thiết kế nội thất, hai tác giả Kin-mơ cho rằng mắt người cũng giữ thăng bằng như cơ thể."),
    dict(move="hold", part="B", blk=2, img="dg", head="Theo Kilmer & Kilmer (2014), mắt cũng giữ thăng bằng", cam=STRIP(1045, 615, 0.9, 856), free=True, dark=False, dd=[],
         vo="Nhìn vào một căn phòng, mắt thấy món đồ này nặng, món kia nhẹ."),
    dict(move="push", part="C", blk=2, img="dgl", head="Hai nửa giống nhau qua một trục", cam=STRIP(365, 615, 0.6, 890), free=True, dark=False, dd=[],
         vo="Hai tác giả cũng cho rằng đối xứng là cách giữ thăng bằng mà mắt nhận ra nhanh nhất."),
    dict(move="pull", part="C", blk=2, img="dgl", head="Mắt dừng lại ở trục giữa", cam=STRIP(365, 615, 0.6, 890), free=True, dark=False, dd=[],
         vo="Theo tụi mình, hai bên đã giống hệt nhau thì mắt không phải so bên nào nặng hơn, nên dừng ở trục giữa và thấy yên."),
    dict(move="pan_u", part="D", blk=3, img="mb", head="Phòng ngủ và phòng tắm chính nằm sát nhau", cam=STRIP(1280, 555, 1.1), free=True, dark=False, dd=[],
         vo="Phòng ngủ chính của căn hộ Palmeira tại Lisbon, do Studio Gameiro cải tạo, được kê đúng theo trục giữa ấy.",
         tts="Phòng ngủ chính của căn hộ Pan-mây-ra tại Lít-bon, do Xtu-đi-ô Ga-mây-rô cải tạo, được kê đúng theo trục giữa ấy."),
    dict(move="push", part="D", blk=3, img="ngub", head="Tấm đầu giường gỗ chạm tay dài hơn giường", cam=STRIP(1200, 584, 1.0), free=True, dark=False, dd=["ax", "hb", "lab_lp", "lp_l", "lp_r"],
         vo="Giường nằm giữa một tấm đầu giường bằng gỗ chạm tay, hai bên là hai đèn thả giống nhau, cách đều trục."),
    dict(move="pull", part="D", blk=3, img="tam", head="Hai vòi sen trong hai ô kính bằng nhau", cam=((1255, 700), 3.0, (540, 800)), dark=True, dd=["r_l", "r_r", "lab_vs"],
         vo="Phòng tắm ngay bên cạnh cũng đối xứng, nhưng chỉ ở hai vòi sen trong vách kính,"),
    dict(move="pan_u", part="D", blk=3, img="tamb", head="Ngoài vách kính, đồ đặt theo chỗ dùng", cam=STRIP(1200, 530, 1.0), free=True, dark=False, dd=["cr", "bo", "lab_lech", "a_cr", "a_bo"],
         vo="còn chậu rửa và bồn vệ sinh bên ngoài thì đặt lệch, chỗ nào tiện dùng thì đặt ở đó."),
    dict(move="push", part="H", blk=4, img="khachb", head="Sofa và lò sưởi đặt lệch hai bên trục", cam=STRIP(1200, 579, 1.0), free=True, dark=False, dd=["sofa", "ls", "lab_kl"],
         vo="Tụi mình thấy cái khéo của căn hộ là chỉ kê đối xứng ở chỗ nằm nghỉ và chỗ đứng tắm, còn phòng khách thì kê lệch."),
    dict(move="hold", part="E", blk=4, img="khachb", head="Theo Kilmer & Kilmer (2014), đối xứng cũng có giới hạn", cam=STRIP(1200, 579, 1.0), free=True, dark=False, dd=[],
         vo="Chính Kilmer cũng nhắc rằng dùng đối xứng quá nhiều sẽ làm căn phòng tĩnh và buồn tẻ.",
         tts="Chính Kin-mơ cũng nhắc rằng dùng đối xứng quá nhiều sẽ làm căn phòng tĩnh và buồn tẻ."),
    dict(move="pull", part="F", blk=4, img="ngub", head="Đối xứng ở đầu giường, kê lệch ở phòng khác", cam=STRIP(1200, 584, 1.0), free=True, dark=False, dd=["ax", "lab_ax"],
         vo="Vì vậy, phòng ngủ nên giữ đối xứng ở đầu giường, chỗ người ta cần yên khi nằm nghỉ, còn các phòng khác thì không cần."),
    dict(move="push", part="I", blk=4, img="ngu", head="end", cam="END", dark=False, vo="", dd=[],
         say="Bài phân tích đầy đủ về cân bằng thị giác khi bày biện nội thất, mọi người xem ở phần bình luận nhé."),
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
# Giai đoạn B (2026-10-24): ghi âm lop-loc-trong-nha.mp3, 56,92 giây (ElevenLabs, giọng Tony Hoang). Lời nhận dạng bằng
# sherpa-onnx zipformer-vi-2025-04-20; ranh giới đoạn nói theo silencedetect -35 dB / 0,25 giây (xem script.md).
# Mỗi cảnh bắt đầu khoảng 0,37 giây trước câu của nó; cảnh cuối kéo đến hết giọng + 0,6 giây.
# Giai đoạn B (2026-10-26): ghi âm doi-xung-dau-giuong.mp3, 69,64 giây (ElevenLabs, giọng Tony Hoang). Ranh giới đoạn nói theo
# silencedetect -35 dB / 0,25 giây; câu ghép vào đoạn theo độ dài (đếm đỉnh âm tiết, xem script.md) vì không chạy được nhận dạng lời.
# Mỗi cảnh bắt đầu khoảng 0,37 giây trước câu của nó; cảnh cuối kéo đến hết giọng + 0,6 giây.
T_AUDIO = [0, 6.04, 16.02, 19.70, 23.83, 28.87, 34.99, 40.41, 44.12, 48.15, 54.67, 59.29, 65.07, 70.24]


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
    của run mở bằng hoà tan từ run trước (ghep_ep12.py), chữ cảnh trước mờ đi như cũ."""
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
            '(1180, "Bài phân tích đầy đủ về cân bằng thị giác", 50, 240),\n    (1236, "khi bày biện nội thất", 50, 240),\n    (1330, "xem ở phần bình luận", 66, 255),')]
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
    open(OUT + "engine_ep12/" + dst, "w").write(s)


T = times()
for k, s in enumerate(SC):
    s["t"] = f"{T[k]:g}–{T[k + 1]:g}s"
RUNS = []
for n, ks in enumerate(runs(), 1):
    img = SC[ks[0]]["img"]
    tag = f"r{n:02d}_{img}"
    data, d0, dl = build_run(T, ks)
    build("engine_storyboard_v7.py", f"engine_ep12_{tag}.py", False, data, img, tag)
    build("engine_video.py", f"engine_video_ep12_{tag}.py", True, data, img, tag)
    RUNS.append(dict(tag=tag, img=img, src=IMGS[img][0], scenes=[k + 1 for k in ks], t_in_main=T[ks[0]],
                     cut_from=d0, cut_len=dl + (1.0 if ks[-1] == len(SC) - 1 else 0.0),
                     first_frame=2 if ks[0] > 0 else 1))
json.dump(RUNS, open(OUT + "engine_ep12/runs.json", "w"), ensure_ascii=False, indent=1)

# ảnh bìa 1080x1920: cảnh rộng trên ảnh 04 (đầu giường), tiêu đề ngắn
COVER = [dict(img="ngu", head="Vì sao riêng đầu giường lại kê đối xứng?", vo="Cân bằng thị giác khi bày biện nội thất, theo Kilmer & Kilmer (2014).", dark=False),
         dict(img="ngu", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep12.py", False,
      wrap_data([scene_line(COVER[0], 0, 3, "WIDE", []), scene_line(COVER[1], 3, 4, "END_SAFE", [])],
                DOODLE.replace("@NPZ@", "none.npz")), "ngu", "cover")

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
FOREIGN = ["Kilmer", "Palmeira", "Lisbon", "Studio", "Gameiro", "AH", "Decode"]
bad = re.findall(r"\d", " ".join(spoken)) + [w for w in FOREIGN if re.search(r"\b" + w + r"\b", " ".join(spoken))]
print("chữ số / tên nước ngoài chưa phiên âm trong bản đọc:", bad)
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep12/scenes.json", "w"), ensure_ascii=False, indent=1)
