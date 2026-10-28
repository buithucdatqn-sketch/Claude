"""Tập 15: Căn phòng cân trong ảnh mà lệch khi bước vào (bài 04 kho AH-Decode-Decor, bài học 3 "Kiểm tra cân bằng từ những chỗ người sẽ đứng và ngồi,
không chỉ từ một tấm ảnh"). Reel nhiều ảnh theo bộ khuôn mau_tap7 (xem engine/mau_tap7/README.md), mã gốc từ gen_ep13.py. Mỗi cảnh chọn ảnh qua khoá
`img` (IMGS); mỗi đoạn cảnh liên tiếp cùng một ảnh là một "run". Doodle: nét trắng mới vẽ bằng draw_ep15.py trên ảnh gốc không doodle (anh/goc/),
theo đúng chỗ chỉ và lời nhãn doodle của bài ở ảnh 08, 09 (doodle gốc của bài 04 vẽ mực đen, mục 0.2b)."""
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
# ảnh làm việc: (file, npz doodle, credit). Ảnh chụp lấy từ anh/goc/ của bài (ảnh gốc không doodle); xem source_info.md
IMGS = dict(
    ngu=("source_ngu.png", "doodle_ep15_ngu.npz", PHOTO),      # ảnh 04 gốc (2400x2400): đầu giường nhìn từ chân giường, đúng trục
    ngub=("source_ngub.png", "doodle_ep15_ngub.npz", PHOTO),   # ảnh 04 gốc, dải y 670-2020: hai đèn thả, trục giường
    d7t=("source_d7t.png", "", DGC),                           # ảnh 07 diagram, phần mặt bằng hai chỗ đứng A, B
    d7b=("source_d7b.png", "", DGC),                           # ảnh 07 diagram, hai khung "A đứng trên trục thấy", "B đứng ở góc phòng thấy" và chú thích
    v08=("source_v08.png", "", MBC),                           # vi-tri-chup/08: phòng ngủ chính, vị trí máy ảnh ở góc phòng (che nhãn số ảnh)
    lech=("source_lech.png", "doodle_ep15_lech.npz", PHOTO),   # ảnh 08 gốc, dải y 1150-2300: một đèn, khung tranh, đầu giường bị cắt
    loso=("source_loso.png", "doodle_ep15_loso.npz", PHOTO),   # ảnh 09 gốc, dải y 900-2200: chụp lò sưởi, hai hốc kệ còn một
    tong=("source_tong.png", "doodle_ep15_tong.npz", PHOTO),   # ảnh 10 gốc, dải y 840-2300: phòng khách nhìn về phòng ăn, sofa, cửa
)


def STRIP(cx, cy, z=1.0, ay=880):
    """thẻ ảnh/bản vẽ nằm gọn giữa hai khối chữ (y ~610–1240): tiêu đề ở trên, phụ đề ở dưới, chữ nâu trên nền trắng"""
    return ((cx, cy), z, (540, ay))


# Lời đọc bản 1: viết liền thành năm khối trước (mục 4 bước 4a), rồi mới cắt cảnh. Khối nối bằng từ khóa
# (ngang nhau → thăng bằng → nặng → trục → trục có sẵn). Thẻ ngắt 1,2 giây giữa các khối (prompt lịch chạy, như tập 11, 12).
CEN = dict(ngu=(1200, 1200), ngub=(1200, 675), d7t=(800, 475), d7b=(1030, 520), v08=(395, 555), lech=(893, 575), loso=(893, 650), tong=(1200, 730))
# Lời đọc: viết liền thành năm đoạn trước (loi_lien_ban*.txt, mục 4 bước 4a), rồi mới cắt cảnh. Đoạn nối bằng từ khóa
# (cân trong ảnh → cân bằng thay đổi khi đi lại → đổi theo chỗ đứng → chỗ đứng (chân giường, góc phòng, gần lò sưởi) → chụp từ một chỗ đứng → chụp từ cửa, sofa, bàn ăn).
SC = [
    dict(move="push", part="A", blk=1, img="ngu", head="Cân trong ảnh, lệch khi bước vào", cam=STRIP(*CEN["ngu"], 0.6, 890), free=True, dark=False, dd=[],
         vo="Một căn phòng trông rất cân trong ảnh, vậy vì sao bước vào tận nơi, có khi lại thấy lệch?"),
    dict(move="pan_r", part="B", blk=2, img="d7t", head="Theo Kilmer & Kilmer (2014), cân bằng đổi khi người ta đi lại", cam=STRIP(*CEN["d7t"], 0.98, 890), free=True, dark=False, dd=[],
         vo="Theo hai tác giả Kilmer, cân bằng của một căn phòng thay đổi khi người ta đi lại trong đó.",
         tts="Theo hai tác giả Kin-mơ, cân bằng của một căn phòng thay đổi khi người ta đi lại trong đó."),
    dict(move="push", part="C", blk=2, img="d7b", head="Vật ở gần to ra, vật ở xa nhỏ lại", cam=STRIP(*CEN["d7b"], 1.0, 890), free=True, dark=False, dd=[],
         vo="Người đi tới đâu, vật ở gần to ra, vật ở xa nhỏ lại, nên món nào nặng, món nào nhẹ trong mắt cũng đổi theo chỗ đứng."),
    dict(move="pan_u", part="D", blk=3, img="v08", head="Phòng ngủ chính ở Palmeira, Lisbon", cam=STRIP(*CEN["v08"], 0.6, 890), free=True, dark=False, dd=[],
         vo="Ở phòng ngủ chính của căn hộ Palmeira tại Lisbon, giường được kê đối xứng giữa hai đèn thả giống nhau.",
         tts="Ở phòng ngủ chính của căn hộ Pan-mây-ra tại Lít-bon, giường được kê đối xứng giữa hai đèn thả giống nhau."),
    dict(move="push", part="D", blk=3, img="ngub", head="Đứng ở chân giường, đúng trên trục", cam=STRIP(*CEN["ngub"], 1.0, 890), free=True, dark=True, dd=["truc", "den_t", "den_p", "lab_hai"],
         vo="Đứng ở chân giường, đúng trên trục, mọi người thấy đủ hai đèn."),
    dict(move="pan_l", part="D", blk=3, img="lech", head="Sang góc phòng, chỉ còn một đèn", cam=STRIP(*CEN["lech"], 0.92, 890), free=True, dark=True, dd=["a_den", "lab_den"],
         vo="Bước sang một góc phòng thì chỉ còn thấy một chiếc đèn."),
    dict(move="push", part="D", blk=3, img="lech", head="Khung tranh lệch, đầu giường bị cắt", cam=STRIP(*CEN["lech"], 0.92, 890), free=True, dark=True, dd=["tranh", "a_tranh", "lab_tranh", "dau", "lab_dau"],
         vo="Từ góc ấy, khung tranh nằm lệch sang phải, còn tấm đầu giường dài chỉ còn thấy một đoạn."),
    dict(move="hold", part="C", blk=3, img="lech", head="Đối xứng chỉ hiện rõ ở một chỗ đứng", cam=STRIP(*CEN["lech"], 0.92, 890), free=True, dark=True, dd=[],
         vo="Nghĩa là cách kê đối xứng kỹ nhất trong nhà cũng chỉ hiện rõ khi đứng ở một chỗ."),
    dict(move="pan_r", part="D", blk=3, img="loso", head="Lại gần lò sưởi trong phòng khách", cam=STRIP(*CEN["loso"], 0.8, 890), free=True, dark=True, dd=["chup", "a_chup", "lab_chup"],
         vo="Phòng khách cũng vậy, khi đứng lại gần lò sưởi thì chiếc chụp lò sưởi hình nón thành món to nhất trước mắt."),
    dict(move="hold", part="D", blk=3, img="loso", head="Món cân lại đã ra ngoài tầm nhìn", cam=STRIP(*CEN["loso"], 0.8, 890), free=True, dark=True, dd=["a_ngoai", "lab_ngoai"],
         vo="Còn bộ sofa và bức tranh sẫm ở phía bên kia, hai món cân lại chiếc lò sưởi, đã ra ngoài tầm nhìn từ chỗ đứng ấy.",
         tts="Còn bộ sô-pha và bức tranh sẫm ở phía bên kia, hai món cân lại chiếc lò sưởi, đã ra ngoài tầm nhìn từ chỗ đứng ấy."),
    dict(move="pull", part="H", blk=4, img="ngu", head="Ảnh chỉ chắc cân ở chỗ chụp", cam=STRIP(*CEN["ngu"], 0.6, 890), free=True, dark=True, dd=["khung", "lab_mot"],
         vo="Một tấm ảnh cũng chỉ chụp từ một chỗ đứng, nên căn phòng trông cân trong ảnh mới chỉ chắc là cân ở đúng chỗ ấy."),
    dict(move="push", part="F", blk=4, img="tong", head="Chụp từ cửa, từ sofa, từ bàn ăn", cam=STRIP(*CEN["tong"], 0.96, 890), free=True, dark=True, dd=["sofa", "lab_sofa", "an", "lab_an", "cua", "lab_cua"],
         vo="Muốn kiểm tra ở nhà mình, tụi mình gợi ý chụp căn phòng từ cửa ra vào, từ chỗ ngồi sofa và từ bàn ăn, rồi lật trái phải từng tấm ảnh như soi gương.",
         tts="Muốn kiểm tra ở nhà mình, tụi mình gợi ý chụp căn phòng từ cửa ra vào, từ chỗ ngồi sô-pha và từ bàn ăn, rồi lật trái phải từng tấm ảnh như soi gương."),
    dict(move="pan_l", part="F", blk=4, img="tong", head="Lật ảnh để tìm chỗ thiếu món cân lại", cam=STRIP(*CEN["tong"], 0.96, 890), free=True, dark=True, dd=["lat1", "lat2", "lab_lat"],
         vo="Tấm nào lật xong tự dưng thấy lệch hẳn về một bên thì ở chỗ đứng ấy, căn phòng đang thiếu một món cân lại."),
    dict(move="push", part="I", blk=5, img="tong", head="end", cam="END", dark=False, vo="", dd=[],
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
COVER = [dict(img="ngu", head="Cân trong ảnh, lệch khi bước vào?", vo="Cân bằng thị giác đổi theo chỗ đứng, theo Kilmer & Kilmer (2014).", dark=False),
         dict(img="ngu", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep15.py", False,
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
FOREIGN = ["Kilmer", "Palmeira", "Lisbon", "Studio", "Gameiro", "AH", "Decode", "sofa", "Nogueira"]
bad = re.findall(r"\d", " ".join(spoken)) + [w for w in FOREIGN if re.search(r"\b" + w + r"\b", " ".join(spoken))]
print("chữ số / tên nước ngoài chưa phiên âm trong bản đọc:", bad)
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep15/scenes.json", "w"), ensure_ascii=False, indent=1)
