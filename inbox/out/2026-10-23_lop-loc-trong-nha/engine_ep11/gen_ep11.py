"""Tập 11: Lớp lọc ngay trong nhà (bài 03 kho AH-Decode-Decor, mục "Ánh sáng đi vào từ trên cao…", đoạn "Lam gỗ ở đây là lớp lọc nằm ngay trong nhà" và lời khuyên cuối bài; chủ Trang duyệt hướng này 2026-10-23).
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
DGC = "Sơ đồ: Giả Thuyết Kiến Trúc, diễn giải từ Kilmer & Kilmer (2014)"
MCC = "Mặt cắt: bản vẽ của Prior Barraclough, nguồn ArchDaily (2023) · ghi chú Giả Thuyết Kiến Trúc"
# ảnh làm việc: (file, npz doodle, credit). Ảnh chụp lấy từ anh/goc/ của bài (ảnh gốc không doodle), nét vẽ mới bằng draw_ep11.py
IMGS = dict(
    vuon=("source_vuon.png", "doodle_ep11_vuon.npz", PHOTO),     # ảnh 08 (goc): mặt kính phía bắc ra vườn
    vuont=("source_vuont.png", "doodle_ep11_vuont.npz", PHOTO),  # ảnh 08 (goc), dải trên: mái hiên, tán cây
    dg5=("source_dg5.png", "", DGC),
    dg5l=("source_dg5l.png", "", DGC),                           # ảnh 05, nửa trái (cửa ngang tầm mắt), cho cảnh mở và cảnh 3                             # ảnh 05: diagram cửa ngang tầm mắt / cửa sát trần (cắt dải hình)
    mc=("source_mc.png", "", MCC),                               # ảnh 04: mặt cắt dọc (cắt vùng gác lửng, mái cao)
    lam=("source_lam.png", "doodle_ep11_lam.npz", PHOTO),        # ảnh 06 (goc): vách lam gác lửng nhìn từ cầu thang
    band=("source_band.png", "doodle_ep11_band.npz", PHOTO),     # ảnh 07 (goc), dải dưới: bàn ăn
    ban=("source_ban.png", "doodle_ep11_ban.npz", PHOTO),                           # ảnh 07 (goc): bàn ăn dưới ô kính cao và vách lam
)
WW = dict(vuont=1600, band=1600)


def LAND(img, fx, fy):
    """dải ảnh ngang 3:2 zoom kín khung (z 2.05): mép trên ~230, mép dưới ~1540, chữ trắng trên ảnh"""
    sc = 2.05 * 960 / WW[img]
    return ((fx, fy), 2.05, (540, round(230 + sc * fy)))


def STRIP(cx, cy, z=1.0):
    """dải bản vẽ ~2:1 nằm gọn y ~605–1121: tiêu đề ở trên, phụ đề ba dòng ở dưới, chữ nâu trên nền trắng"""
    return ((cx, cy), z, (540, 863))


SC = [
    dict(move="push", part="A", blk=1, img="ban", head="Vách lam gỗ và mặt kính ngang tầm mắt", cam=((700, 1100), 2.1, (540, 925)), dark=True, dd=[],
         vo="Vì sao ánh sáng từ trên cao qua vách lam lại dịu hơn ánh sáng từ kính ngang tầm mắt?"),
    dict(move="pan_r", part="B", blk=2, img="vuon", head="Theo Kilmer & Kilmer (2014), mắt thấy ánh sáng hắt lại", cam=((800, 1200), 2.1, (540, 925)), dark=True, dd=[],
         vo="Năm 2014, hai tác giả Kilmer nhắc rằng mắt người chỉ thấy ánh sáng khi nó rơi lên một món đồ hay mặt tường rồi hắt lại.",
         tts="Năm hai nghìn không trăm mười bốn, hai tác giả Kin-mơ nhắc rằng mắt người chỉ thấy ánh sáng khi nó rơi lên một món đồ hay mặt tường rồi hắt lại."),
    dict(move="push", part="C", blk=2, img="dg5l", head="Kính ngang tầm mắt gây vệt nắng gắt", cam=STRIP(545, 492, 0.58), free=True, dark=False, dd=[],
         vo="Theo cách tụi mình hiểu, kính ngang tầm mắt đưa nắng vào thành vệt gắt trên sàn và đặt mảng trời chói trước mắt."),
    dict(move="pan_r", part="C", blk=2, img="dg5", head="Ánh sáng chạm tường trước thì dịu hơn", cam=STRIP(1080, 492), free=True, dark=False, dd=[],
         vo="Còn ánh sáng từ ô kính cao rơi lên tường và trần trước rồi mới hắt xuống, nên khi tới mắt người, nó đã dịu đi nhiều."),
    dict(move="pan_u", part="D", blk=3, img="mc", head="Ô kính cao sát mái ở Union Street House", cam=STRIP(1250, 625, 1.04), free=True, dark=False, dd=[],
         vo="Ở Union Street House tại Melbourne, ánh sáng xuống bàn ăn đi vào từ một ô kính cao sát mái.",
         tts="Ở Diu-ni-ơn Xtrít Hao-xơ tại Meo-bơn, ánh sáng xuống bàn ăn đi vào từ một ô kính cao sát mái."),
    dict(move="pull", part="D", blk=3, img="lam", head="Đường đi của ánh sáng từ ô kính cao", cam=((1000, 1000), 2.2, (540, 925)), dark=True, dd=["lab_x", "x_arr", "lab_r", "r_arr"],
         vo="Ngay dưới ô kính là vách lam gỗ của gác lửng, nên ánh sáng phải xuyên qua vách lam rồi mới xuống bếp và bàn ăn."),
    dict(move="pan_r", part="D", blk=3, img="band", head="Mặt bàn ăn dưới ô kính cao", cam=LAND("band", 1050, 534), free=True, dark=True, dd=["t_ring", "t_arr", "lab_t"],
         vo="Trong ảnh chụp bàn ăn, mặt bàn không có một vệt nắng nào."),
    dict(move="push", part="F", blk=4, img="lam", head="Vách lam gỗ của gác lửng nhìn từ cầu thang", cam=((1250, 1100), 2.2, (540, 925)), dark=True, dd=["l_out", "l_arr", "lab_l"],
         vo="Theo tụi mình, vách lam là lớp lọc ngay trong nhà, nên chủ nhà có thể lắp vào ô cửa sẵn có mà không cần đục tường."),
    dict(move="pan_d", part="F", blk=4, img="ban", head="Nhà phố hướng tây vẫn giữ được mặt kính", cam=((800, 1100), 2.1, (540, 925)), dark=True, dd=["lab_v", "v_arr"],
         vo="Vì vậy, với nhà phố hướng tây, tụi mình nghĩ không nhất thiết phải bỏ mặt kính, mà có thể đặt phía trong một vách lam gỗ."),
    dict(move="hold", part="H", blk=5, img="vuont", head="Câu hỏi mỗi khi vẽ một ô cửa", cam=LAND("vuont", 800, 534), free=True, dark=True, dd=[],
         vo="Bởi thế, từ nay mỗi lần vẽ ô cửa, tụi mình sẽ hỏi ánh sáng chạm vào đâu trước, chứ không chỉ hỏi nên mở bao nhiêu kính."),
    dict(move="push", part="I", blk=5, img="ban", head="end", cam="END", dark=False, vo="", dd=[],
         say="Bài phân tích đầy đủ về ánh sáng tự nhiên trong nhà nằm ở phần bình luận."),
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
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · LỚP LỌC ÁNH SÁNG"'),
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

# ảnh bìa 1080x1920: cảnh rộng trên ảnh 06 (vách lam gác lửng), tiêu đề ngắn + câu chốt
COVER = [dict(img="lam", head="Vì sao ánh sáng qua vách lam lại dịu hơn?", vo="Ánh sáng tự nhiên trong nội thất, theo Kilmer & Kilmer (2014).", dark=False),
         dict(img="lam", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep11.py", False,
      wrap_data([scene_line(COVER[0], 0, 3, "WIDE", []), scene_line(COVER[1], 3, 4, "END_SAFE", [])],
                DOODLE.replace("@NPZ@", "none.npz")), "lam", "cover")

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
