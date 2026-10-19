"""Tập 8 (bản 2, một mạch): Khối màu đậm có ngộp không, diện tích và ánh sáng (bài 01 kho AH-Decode-Decor, The Green Box).
Khai thác phần bài 01 chưa tập nào dùng (tập 4, 5, 6, 6b đã làm: chênh sáng, nền lùi, cùng màu khác bề mặt,
hai màu phụ): câu hỏi của bác hàng xóm, lỗi mỗi phòng một màu (diagram 01), cách 2 nền đậm (diagram 02),
Albers "mảng lớn lấn át mảng nhỏ", phòng nhỏ dễ ngộp, mảng lớn trông đậm hơn mẫu thử, ánh sáng hai mặt kính
so với một mặt thoáng hướng tây, chọn nhạt hơn mẫu thử một bậc. Xen kẽ bài: tập 7 là bài 02 nên tập 8 lấy bài 01.
Ảnh chụp lấy mới từ ArchDaily (bộ ảnh Robert Rieger của chính công trình), không trùng ảnh tập 4, 5, 6, 6b; không có mặt bằng vì mặt bằng duy nhất đã dùng ở tập 6b.
Dựng trên gen_ep07.py của tập 7 (run theo ảnh, hoà tan khi đổi ảnh)."""
import json
import os
import re

E = "/home/user/Claude/engine/"
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
WPS = 3.2      # tốc độ đọc dự kiến (từ/giây) cho bản nháp; giai đoạn B căn lại theo ghi âm
TRANS = 0.7

WIDE = "WIDE"
PHOTO = "Ảnh dự án: The Green Box, Berlin · Ester Bruzkus Architekten · ảnh Robert Rieger (qua ArchDaily)"
DIAG = "Diagram: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014)"
# ảnh làm việc: (file, npz doodle gốc, credit). Ảnh chụp lấy mới từ bộ ảnh ArchDaily của chính công trình (trang nguồn ảnh
# bài 01 ghi), không trùng ảnh nào đã dùng ở tập 4, 5, 6, 6b (mục 0.5c). Ảnh sạch, không có nét gốc nên không lộ nét.
IMGS = dict(
    ad8=("source_ad8.png", "", PHOTO),    # ArchDaily 8: phòng khách, khối thư viện xanh cạnh mặt kính
    ad21=("source_ad21.png", "", PHOTO),  # ArchDaily 21: khoảng hẹp giữa vách kính và mảng xanh
    ad17=("source_ad17.png", "", PHOTO),  # ArchDaily 17: tủ nan xanh cạnh mảng tường xanh nhạt lớn
    ad10=("source_ad10.png", "", PHOTO),  # ArchDaily 10: phòng khách sáng, rèm trắng cao kịch trần
    ad18=("source_ad18.png", "", PHOTO),  # ArchDaily 18: tủ xanh đậm, chỗ khuất sáng
    ad15=("source_ad15.png", "", PHOTO),  # ArchDaily 15: tủ áo sơn màu nhạt, mảng lớn
    dg1b=("source_dg1b.png", "", DIAG),   # diagram 01, khung "nền lùi, một màu làm chủ"
)
SC = [
    dict(move="push", part="A", blk=1, img="ad8", head="Khối tủ xanh to: ở lâu có ngộp?", cam=WIDE, dark=False, dd=[],
         vo="Sơn nguyên một khối tủ to màu xanh, ở lâu có thấy ngộp không?"),
    dict(move="pan_d", part="A", blk=1, img="ad8", head="Căn hộ mẫu: The Green Box, Berlin", cam=((1450, 1000), 2.3, (540, 900)), dark=True, dd=[],
         vo="Đó là câu bác hàng xóm hỏi, khi bạn tụi mình sơn cả dãy tủ một màu xanh rêu, theo mẫu căn hộ trong ảnh."),
    dict(move="pull", part="B", blk=2, img="dg1b", head="Albers (1963): mảng lớn lấn át mảng nhỏ", cam=((545, 281), 1.0, (540, 900)), free=True, dark=False, dd=[],
         vo="Mà Josef Albers từng chỉ ra rằng mảng màu lớn luôn lấn át mảng màu nhỏ, và cả dãy tủ chính là một mảng màu rất lớn.",
         tts="Mà Giô-dép An-bơ từng chỉ ra rằng mảng màu lớn luôn lấn át mảng màu nhỏ, và cả dãy tủ chính là một mảng màu rất lớn."),
    dict(move="push", part="C", blk=3, img="ad17", head="Mảng lớn trông đậm hơn mẫu thử", cam=((1000, 1100), 2.3, (540, 900)), dark=True, dd=[],
         vo="Hơn nữa, một màu khi phủ lên mảng lớn bao giờ cũng trông đậm hơn trên tấm mẫu nhỏ, nên sơn xong thường đậm hơn mình tưởng."),
    dict(move="pan_u", part="C", blk=3, img="ad21", head="Phòng nhỏ: màu đậm dễ ngộp", cam=((1300, 1200), 2.3, (540, 900)), dark=True, dd=[],
         vo="Và phòng càng nhỏ, màu đậm càng dễ gây cảm giác ngột ngạt."),
    dict(move="pull", part="D", blk=4, img="ad10", head="The Green Box: hai mặt kính cao kịch trần", cam=WIDE, dark=False, dd=[],
         vo="Nhưng còn ánh sáng nữa. Căn hộ mẫu ở Berlin có tới hai mặt kính cao kịch trần,",
         tts="Nhưng còn ánh sáng nữa. Căn hộ mẫu ở Béc-lin có tới hai mặt kính cao kịch trần,"),
    dict(move="pan_l", part="D", blk=4, img="ad18", head="Một mặt thoáng: khối xanh thành mảng tối", cam=((1200, 1600), 2.3, (540, 900)), dark=True, dd=[],
         vo="còn nhà bạn tụi mình chỉ có một mặt thoáng nhìn về hướng tây, nên khối xanh đậm rất dễ biến thành một mảng tối."),
    dict(move="push", part="F", blk=5, img="ad15", head="Thử ở nhà mình: nhạt hơn mẫu một bậc", cam=((1250, 800), 2.9, (540, 900)), dark=True, dd=[],
         vo="Vì vậy, màu nào sẽ phủ lên mảng lớn, mọi người cứ chọn nhạt hơn tấm mẫu thử một bậc."),
    dict(move="pull", part="H", blk=6, img="ad8", head="Ngộp hay không: còn tùy diện tích, ánh sáng", cam=((1100, 1500), 2.3, (540, 900)), dark=True, dd=[],
         vo="Vậy khối tủ xanh có ngộp không, theo tụi mình, còn tùy nó to cỡ nào so với phòng và nhà đủ sáng hay không."),
    dict(move="push", part="I", blk=6, img="ad8", head="end", cam="END", dark=False, vo="", dd=[],
         say="Bài phân tích về phân bổ màu từ sách của Kilmer, mọi người xem phần bình luận nha.",
         tts="Bài phân tích về phân bổ màu từ sách của Kin-mơ, mọi người xem phần bình luận nha."),
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


# Giai đoạn A: chưa có ghi âm, thời lượng tính theo số từ (mục 4a). Giai đoạn B điền mốc theo ghi âm vào đây.
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
    của run mở bằng hoà tan từ run trước (ghep_ep07.py), chữ cảnh trước mờ đi như cũ."""
    img = SC[ks[0]]["img"]
    lines, t, d0 = [], 0.0, 0.0
    if ks[0] > 0:
        prev = SC[ks[0] - 1]
        d0 = T[ks[0]] - T[ks[0] - 1]
        first = SC[ks[0]]
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
           ('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · MÀU ĐẬM, MẢNG LỚN"'),
           ("CARD_W2, BORDER2 = 1920, 0", f"CARD_W2, BORDER2 = {cw}, 0  # theo tỷ lệ ảnh của run"),
           ("C2 = (B2W / 2, 1810.0)", f"C2 = (B2W / 2, {cy})"),
           ("borderMode=cv2.BORDER_REFLECT)", "borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255, 0))"),
           # khung cuối: lời mời theo mẫu chủ Trang chỉnh ở tập 7 (mục 0.6)
           ('(1196, "Bài viết phân tích đầy đủ", 58, 240),\n    (1260, "xem ở dòng đầu tiên", 58, 240),\n    (1348, "trong phần bình luận", 66, 255),',
            '(1196, "Bài phân tích về phân bổ màu", 54, 240),\n    (1258, "từ sách của Kilmer", 46, 240),\n    (1348, "xem ở phần bình luận", 66, 255),')]
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
    open(OUT + "engine_ep08/" + dst, "w").write(s)


T = times()
for k, s in enumerate(SC):
    s["t"] = f"{T[k]:g}–{T[k + 1]:g}s"
RUNS = []
for n, ks in enumerate(runs(), 1):
    img = SC[ks[0]]["img"]
    tag = f"r{n:02d}_{img}"
    data, d0, dl = build_run(T, ks)
    build("engine_storyboard_v7.py", f"engine_ep08_{tag}.py", False, data, img, tag)
    build("engine_video.py", f"engine_video_ep08_{tag}.py", True, data, img, tag)
    RUNS.append(dict(tag=tag, img=img, src=IMGS[img][0], scenes=[k + 1 for k in ks], t_in_main=T[ks[0]],
                     cut_from=d0, cut_len=dl + (1.0 if ks[-1] == len(SC) - 1 else 0.0),
                     first_frame=2 if ks[0] > 0 else 1))
json.dump(RUNS, open(OUT + "engine_ep08/runs.json", "w"), ensure_ascii=False, indent=1)

# ảnh bìa 1080x1920: cảnh rộng ảnh ArchDaily 8 (khối thư viện xanh), tiêu đề ngắn của reel + câu móc
COVER = [dict(img="ad8", head="Màu đậm, mảng lớn", vo="Khối tủ xanh to, ở lâu có ngộp không?", dark=False),
         dict(img="ad8", head="end", vo="", dark=False)]
build("engine_storyboard_v7.py", "cover_ep08.py", False,
      wrap_data([scene_line(COVER[0], 0, 3, "WIDE", []), scene_line(COVER[1], 3, 4, "END_SAFE", [])],
                DOODLE.replace("@NPZ@", "none.npz")), "ad8", "cover")

# ---- elevenlabs.txt theo mục 8b (không thẻ kỹ thuật) + elevenlabs_break.txt (sáu khối, thẻ ngắt 1,2 giây, theo prompt lịch chạy) ----
shown = [x.get("say", x["vo"]) for x in SC]
spoken = [x.get("tts", x.get("say", x["vo"])) for x in SC]
para = ["\n".join(p.strip() + ("" if p.strip()[-1] in ".?!," else ".") for p in re.split(r"(?<=[.?!])\s+", sp)) for sp in spoken]
open(OUT + "elevenlabs.txt", "w").write("\n\n".join(para) + "\n\n---\nGợi ý cài đặt: giọng nữ hoặc nam trầm ấm, tốc độ 1.0, mô hình đa ngôn ngữ, ngôn ngữ Vietnamese\n---\n")
blocks = {}
for x, sp in zip(SC, spoken):
    blocks.setdefault(x["blk"], []).append(sp)
BR = '\n<break time="1.2s" />\n'
open(OUT + "elevenlabs_break.txt", "w").write(BR.join(" ".join(v) for k, v in sorted(blocks.items())) + "\n")
nw = sum(words(x) for x in shown)
print("runs", [(r["tag"], r["scenes"]) for r in RUNS])
print("tổng engine", T[-1], "giây; từ lời đọc", nw, "; ước tính giọng đọc ~", round(nw / 3.4 + 5 * 1.0, 1), "giây")
for k, x in enumerate(SC):
    print(k + 1, x["blk"], x["part"], x["t"], words(shown[k]), x["head"])
FOREIGN = ["Kilmer", "Albers", "Josef", "Green", "Box", "Berlin", "Ester", "Bruzkus", "AH", "Decode"]
bad = re.findall(r"\d", " ".join(spoken)) + [w for w in FOREIGN if re.search(r"\b" + w + r"\b", " ".join(spoken))]
print("chữ số / tên nước ngoài chưa phiên âm trong bản đọc:", bad)
json.dump([dict(blk=x["blk"], t=x["t"], head=x["head"], loi=shown[k], tts=spoken[k], part=x["part"]) for k, x in enumerate(SC)],
          open(OUT + "engine_ep08/scenes.json", "w"), ensure_ascii=False, indent=1)
