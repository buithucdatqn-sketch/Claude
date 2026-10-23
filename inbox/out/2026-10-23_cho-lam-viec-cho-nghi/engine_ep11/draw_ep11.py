"""Tập 11: vẽ nét doodle mới lên ảnh gốc không doodle của bài 03 (anh/goc/), theo bộ khuôn engine/mau_tap7/draw_doodle.py.
Chép vào OUT/engine_epNN/draw_epNN.py, sửa khối "nét của từng ảnh" và tên file npz (doodle_epNN_<ảnh>.npz).
Vẽ nét doodle mới (nét trắng, nét đứt, nét tay) lên ảnh sạch, lưu thành lớp npz cùng dạng với lớp tách từ doodle gốc
(make_layers): mỗi khoá là mảng điểm (x, y) theo ĐÚNG thứ tự vẽ, để engine lộ dần nét từ đuôi tới đầu mũi tên.
Khoá bắt đầu bằng "lab" là nhãn chữ viết tay (hiện khi nét đạt 55-75%), còn lại là nét.
Toạ độ theo ảnh làm việc (source_<ảnh>.png). Chạy: python3 -I draw_ep10.py <OUT> ; ảnh xem thử ghi ra <OUT>/doodle_preview/."""
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


# ---- nét của từng ảnh (toạ độ ảnh làm việc) ----
DASH = lambda w: (5.5 * w, 3.5 * w)
L = {}
# mo: ảnh 14 gốc, bàn gác lửng khi vách lam kéo mở (2000x1333, khung thẻ z~0.95)
w = 10
L["mo"] = dict(
    # cảnh 2: mảng kính vườn là chỗ sáng nhất trong tầm nhìn
    g_ring=loop((1085, 835), 245, 190, w, DASH(w), 3.0, 1, tilt=-4),
    lab_g=label("chỗ sáng nhất/trong tầm nhìn", (620, 400), 96),
    g_arr=arrow([(1270, 470), (1220, 560), (1160, 642)], w, DASH(w), 2.0, 2),
    # cảnh 3: mặt bàn ngay cạnh mảng sáng ấy trông tối đi
    lab_d=label("mặt bàn/trông tối đi", (140, 560), 96),
    d_arr=arrow([(300, 790), (320, 880), (320, 975)], w, DASH(w), 2.0, 4),
    # cảnh 8: vách lam trượt dọc mép gác, người ngồi tự chọn kéo kín hay mở
    s_out=poly([(1325, 430), (1985, 420), (1985, 1010), (1330, 1015)], w, DASH(w), 2.5, 13),
    lab_s=label("vách lam/trượt", (930, 430), 92),
    s_arr1=arrow([(1660, 720), (1760, 722), (1880, 725)], w, DASH(w), 1.0, 14),
    s_arr2=arrow([(1650, 720), (1550, 718), (1430, 715)], w, DASH(w), 1.0, 15),
    # cảnh 9: phép thử nheo mắt
    n_ring=loop((1085, 800), 280, 175, w, DASH(w), 3.0, 5, tilt=6),
    lab_n=label("nheo mắt lại:/chỉ còn thấy ô cửa?", (490, 400), 84),
    n_arr=arrow([(1300, 470), (1265, 545), (1225, 615)], w, DASH(w), 2.0, 6),
)
# kin: ảnh 13 gốc, cùng bàn khi vách lam kéo kín (1600x2400, zoom kín)
w = 6
L["kin"] = dict(
    # cảnh 7: vách lam kéo kín, trước mặt chỉ còn tường gỗ
    v_out=poly([(1405, 820), (1585, 790), (1585, 1330), (1408, 1320)], w, DASH(w), 2.0, 7),
    lab_v=label("vách lam kéo kín,/sáng lọt qua khe", (560, 780), 76),
    v_arr=arrow([(1180, 960), (1290, 1010), (1385, 1060)], w, DASH(w), 1.5, 8),
    lab_w=label("trước mặt/chỉ còn tường gỗ", (430, 1160), 76),
    # cảnh 11: rèm hay vách lam kéo được giữa bàn và mảng kính
    lab_b=label("rèm hay vách lam/kéo được", (330, 1080), 76),
    b_arr=arrow([(980, 1180), (1180, 1230), (1390, 1250)], w, DASH(w), 1.5, 10),
)
# togo: ảnh 15 gốc, ghế Togo sát mặt kính phòng khách (1600x2400, zoom kín)
w = 6
L["togo"] = dict(
    lab_k=label("kính sáng hơn hẳn/tường gỗ", (290, 900), 76),
    k_arr=arrow([(820, 1030), (900, 1000), (980, 965)], w, DASH(w), 1.5, 11),
    lab_t=label("ghế Togo,/chỗ ngồi nghỉ", (290, 1170), 76),
    t_arr=arrow([(470, 1330), (520, 1420), (560, 1530)], w, DASH(w), 1.5, 12),
)

os.makedirs(OUT + "doodle_preview", exist_ok=True)
for img, layers in L.items():
    np.savez(os.path.join(HERE, f"doodle_ep11_{img}.npz"), **{k: np.array(v, np.float32) for k, v in layers.items()})
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
