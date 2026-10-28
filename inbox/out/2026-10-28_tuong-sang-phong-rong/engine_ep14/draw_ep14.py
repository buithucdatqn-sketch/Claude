"""Tập 14 (từ bộ khuôn draw_doodle.py): vẽ nét doodle mới (bản gốc: tập 10, inbox/out/2026-10-22_van-tho-xa-van-min-gan/engine_ep10/draw_ep14.py).
Chép vào OUT/engine_epNN/draw_epNN.py, sửa khối "nét của từng ảnh" và tên file npz (doodle_epNN_<ảnh>.npz).
Vẽ nét doodle mới (nét trắng, nét đứt, nét tay) lên ảnh sạch, lưu thành lớp npz cùng dạng với lớp tách từ doodle gốc
(make_layers): mỗi khoá là mảng điểm (x, y) theo ĐÚNG thứ tự vẽ, để engine lộ dần nét từ đuôi tới đầu mũi tên.
Khoá bắt đầu bằng "lab" là nhãn chữ viết tay (hiện khi nét đạt 55-75%), còn lại là nét.
Toạ độ theo ảnh làm việc (source_<ảnh>.png). Chạy: python3 -I draw_ep14.py <OUT> ; ảnh xem thử ghi ra <OUT>/doodle_preview/."""
import math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "./") + "/"
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = next(f for f in (os.path.join(HERE, "PatrickHand-Regular.ttf"), os.path.join(HERE, "..", "PatrickHand-Regular.ttf"),
                        os.path.join(HERE, "..", "..", "..", "..", "engine", "PatrickHand-Regular.ttf")) if os.path.isfile(f))


def _resample(pts, step=1.0):
    pts = np.asarray(pts, float)
    seg = np.r_[0, np.cumsum(np.hypot(*np.diff(pts, axis=0).T))]
    t = np.arange(0, seg[-1], step)
    return np.c_[np.interp(t, seg, pts[:, 0]), np.interp(t, seg, pts[:, 1])], t


def _smooth(pts, n=6):
    """đường cong qua các điểm điều khiển (Catmull-Rom), để nét không thẳng như đồ hoạ vector"""
    P = np.asarray(pts, float)
    P = np.vstack([P[0], P, P[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for s in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * s + (2 * p0 - 5 * p1 + 4 * p2 - p3) * s * s
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * s ** 3))
    out.append(P[-2])
    return np.array(out)


def stroke(pts, w, dash=None, wobble=0.0, seed=0, smooth=True):
    """nét tay: rung nhẹ vuông góc với đường, nét đứt (dash = (dài, hở)), điểm sắp theo thứ tự vẽ"""
    rng = np.random.default_rng(seed)
    P = _smooth(pts) if smooth and len(pts) > 2 else np.asarray(pts, float)
    S, t = _resample(P)
    if wobble:
        d = np.gradient(S, axis=0)
        nrm = np.c_[-d[:, 1], d[:, 0]] / (np.hypot(d[:, 0], d[:, 1])[:, None] + 1e-9)
        ph = rng.uniform(0, 6.3, 2)
        off = wobble * (np.sin(t / 97 + ph[0]) * 0.7 + np.sin(t / 31 + ph[1]) * 0.3)
        S = S + nrm * off[:, None]
    r = w / 2.0
    R = int(math.ceil(r))
    disk = [(dx, dy) for dx in range(-R, R + 1) for dy in range(-R, R + 1) if dx * dx + dy * dy <= r * r]
    seen, order = set(), []
    on = True
    for (x, y), tt in zip(S, t):
        if dash:
            on = (tt % (dash[0] + dash[1])) < dash[0]
        if not on:
            continue
        for dx, dy in disk:
            p = (int(round(x)) + dx, int(round(y)) + dy)
            if p not in seen:
                seen.add(p)
                order.append(p)
    return order, S


def arrow(pts, w, dash, wobble=0.0, seed=0, head=None):
    """mũi tên: thân nét đứt, đầu là hai nét liền vẽ sau cùng"""
    body, S = stroke(pts, w, dash, wobble, seed)
    head = head or 9 * w
    tip = S[-1]
    back = S[max(0, len(S) - int(head))]
    ang = math.atan2(tip[1] - back[1], tip[0] - back[0])
    out = list(body)
    for a in (ang + math.radians(150), ang - math.radians(150)):
        end = (tip[0] + head * math.cos(a), tip[1] + head * math.sin(a))
        h, _ = stroke([tuple(tip), end], w, None, 0, seed, smooth=False)
        out += h
    return out


def loop(center, rx, ry, w, dash, wobble=0.0, seed=0, overshoot=0.12, tilt=-6):
    """vòng bao tay: hình bầu dục hơi méo, vẽ quá điểm đầu một đoạn (nét vượt)"""
    cx, cy = center
    a = np.linspace(-0.4, 2 * math.pi * (1 + overshoot) - 0.4, 90)
    k = 1 + 0.06 * np.sin(3 * a + seed)
    tr = math.radians(tilt)
    x, y = rx * k * np.cos(a), ry * k * np.sin(a)
    pts = np.c_[cx + x * math.cos(tr) - y * math.sin(tr), cy + x * math.sin(tr) + y * math.cos(tr)]
    return stroke(pts, w, dash, wobble, seed, smooth=False)[0]


def poly(pts, w, dash, wobble=0.0, seed=0):
    """đường bao gấp khúc, mỗi góc vẽ lố ra một chút như nét tay"""
    P = [np.array(p, float) for p in pts] + [np.array(pts[0], float)]
    out, seen = [], set()
    for i in range(len(P) - 1):
        a, b = P[i], P[i + 1]
        v = (b - a) / (np.linalg.norm(b - a) + 1e-9)
        o, _ = stroke([tuple(a - v * 3 * w), tuple(b + v * 3 * w)], w, dash, wobble, seed + i, smooth=False)
        for p in o:
            if p not in seen:
                seen.add(p)
                out.append(p)
    return out


def label(text, xy, size, line=1.12):
    """nhãn chữ viết tay (Patrick Hand), nhiều dòng tách bằng '/'"""
    f = ImageFont.truetype(FONT, size)
    lines = text.split("/")
    W = max(int(f.getlength(s)) for s in lines) + 20
    H = int(size * line * len(lines)) + 20
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    for i, s in enumerate(lines):
        d.text((5, 5 + i * size * line), s.strip(), font=f, fill=255)
    ys, xs = np.nonzero(np.array(im) > 128)
    return [(int(x + xy[0]), int(y + xy[1])) for x, y in zip(xs, ys)]


# ---- nét của từng ảnh (toạ độ ảnh làm việc = ảnh gốc trích từ PDF, không thu nhỏ), tập 14 ----
DASH = lambda w: (5.5 * w, 3.5 * w)
L = {}


def O(pts, x0, y0):
    """toạ độ đo trên ảnh gốc -> dải cắt có góc trên trái (x0, y0)"""
    return [(x - x0, y - y0) for x, y in pts]


# khe: góc phòng tường trắng, dải cắt (0, 0, 1164, 1100), cảnh 2: đường ranh trần-tường và góc tường mờ
w = 12
L["khe"] = dict(
    ranh1=stroke([(30, 262), (360, 275), (690, 292)], w, DASH(w), 2.0, 1)[0],
    ranh2=stroke([(694, 300), (697, 650), (700, 1060)], w, DASH(w), 2.0, 2)[0],
    lab_ranh=label("đường ranh/mờ đi?", (120, 520), 90),
    a_tran=stroke([(320, 178), (500, 184), (680, 188)], w, DASH(w), 1.2, 11)[0],
    lab_tran=label("trần sáng", (330, 45), 90),
    a_tuong=stroke([(140, 728), (330, 732), (520, 736)], w, DASH(w), 1.2, 12)[0],
    lab_tuong=label("tường sáng", (140, 590), 90))
# hanh: hành lang, dải cắt (100, 470, 1300, 1900), cảnh 6: khuôn cửa và len chân tường cùng màu tường
w = 13
HX, HY = 100, 470
L["hanh"] = dict(
    khuon=stroke(O([(405, 1690), (406, 1100), (408, 548), (680, 546), (952, 548), (953, 1100), (955, 1690)], HX, HY), w, DASH(w), 2.5, 3)[0],
    len_l=stroke(O([(215, 1652), (310, 1650), (398, 1652)], HX, HY), w, DASH(w), 1.5, 4)[0],
    len_r=stroke(O([(962, 1640), (1000, 1640), (1035, 1641)], HX, HY), w, None, 1.0, 5)[0],
    lab_cung=label("khuôn cửa,/len chân tường/cùng màu sáng", O([(445, 1215)], HX, HY)[0], 84))
# banan: Pawson House, bàn ăn (1200x948), cảnh 8: vách kính ra vườn, ánh sáng vào nhà
w = 9
L["banan"] = dict(
    kinh=poly([(230, 199), (463, 199), (463, 538), (230, 538)], w, DASH(w), 1.5, 6),
    a_kinh=arrow([(475, 470), (560, 540), (640, 600)], w, DASH(w), 1.0, 7, head=50),
    lab_kinh=label("vách kính ra vườn", (240, 610), 66),
    lab_vao=label("ánh sáng từ vườn", (480, 640), 66))
# thang: Pawson House, cầu thang một vế, dải cắt (0, 0, 632, 560), cảnh 9: ánh sáng từ khe kính trên mái đổ xuống dọc tường
w = 6
L["thang"] = dict(
    a_khe=arrow([(352, 15), (350, 160), (332, 300)], w, DASH(w), 0.8, 8, head=34),
    lab_khe=label("ánh sáng từ/khe kính trên mái", (10, 330), 44),
    tw=poly([(330, 8), (590, 8), (590, 330), (330, 330)], w, DASH(w), 1.0, 13),
    lab_tw=label("tường trắng", (380, 350), 50))
# bep: Pawson House, bếp (1200x948), cảnh 10: tường trắng và sàn đá
w = 9
L["bep"] = dict(
    tuong=poly([(300, 215), (760, 215), (760, 495), (300, 495)], w, DASH(w), 1.5, 9),
    san=loop((330, 870), 320, 55, w, DASH(w), 1.5, 10, tilt=0),
    lab_tuong=label("tường trắng/nhiều lớp", (360, 270), 70),
    lab_san=label("sàn lát đá/sát vách kính", (300, 640), 64))

# mau: khối mẫu màu cửa hàng Cover Story (512x512), cảnh 5–6: ba đặc tính của màu; ô sáng và ô tối hơn
w = 4
L["mau"] = dict(
    grid=poly([(104, 131), (210, 131), (210, 226), (104, 226)], w, DASH(w), 0.8, 30),
    lab_grid=label("màu gì, sáng hay tối,/tươi hay ngả xám", (14, 20), 44),
    o_sang=loop((123, 156), 20, 26, w, DASH(w), 0.6, 31, tilt=0),
    o_toi=loop((157, 156), 20, 26, w, DASH(w), 0.6, 32, tilt=0),
    lab_st=label("sáng  tối hơn", (86, 228), 42))
# hanh (thêm cho bản 6): mảng tường sáng bên trái hành lang, cảnh 8
w = 13
L["hanh"]["tw_h"] = poly(O([(215, 520), (395, 520), (395, 1600), (215, 1600)], HX, HY), w, DASH(w), 2.0, 33)
L["hanh"]["lab_twh"] = label("xem độ sáng/trước", O([(440, 1250)], HX, HY)[0], 84)

os.makedirs(OUT + "doodle_preview", exist_ok=True)
for img, layers in L.items():
    np.savez(os.path.join(HERE, f"doodle_ep14_{img}.npz"), **{k: np.array(v, np.float32) for k, v in layers.items()})
    im = Image.open(OUT + f"source_{img}.png").convert("RGB")
    a = np.array(im)
    for k, v in layers.items():
        v = np.array(v)
        ok = (v[:, 0] >= 0) & (v[:, 0] < a.shape[1]) & (v[:, 1] >= 0) & (v[:, 1] < a.shape[0])
        a[v[ok, 1], v[ok, 0]] = 255
    p = Image.fromarray(a)
    p.thumbnail((900, 900))
    p.save(OUT + f"doodle_preview/{img}.jpg", quality=85)
    print(img, {k: len(v) for k, v in layers.items()})
