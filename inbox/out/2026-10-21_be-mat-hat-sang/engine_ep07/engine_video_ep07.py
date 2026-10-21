"""Reel video engine v8 (nhiều ảnh nguồn: PHOTOS, SCENES[i]["img"]; đổi ảnh = mờ chéo) (one oak pin per print, beige margins, all-white text).
The project photo is a print pinned on a linen board; the 'camera' zooms into the
board. Doodles (white, dashed) sit on the photo; text goes outside the photo with
ink arrows pointing at the doodles, or white on the photo when the zoom fills the screen."""
import math
import os
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from silhouette import loose_contour  # noqa: E402

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "source.png")
OUT = sys.argv[2] if len(sys.argv) > 2 else HERE
os.makedirs(os.path.join(OUT, "video"), exist_ok=True)

W, H, SS = 1080, 1920, 2
FONT = os.path.join(HERE, "PatrickHand-Regular.ttf")
if not os.path.exists(FONT):
    FONT = os.path.join(HERE, "fonts", "PatrickHand-Regular.ttf")
CREDIT = 'Ảnh dự án: Union Street House, Northcote, Melbourne · Prior Barraclough · ảnh Ben Hosking'
HEAD = "AH DECODE · BỀ MẶT HẮT SÁNG"
# Khung cuối cố định cho mọi tập: giới thiệu series AH Decode, mời theo dõi Fanpage Giả Thuyết Kiến Trúc, KHÔNG nhắc tập sau. (y, chữ, cỡ, độ đậm)
END_LINES = [
    (1060, "AH Decode · series phân tích nguyên tắc thiết kế", 40, 215),
    (1108, "và cách chọn đồ decor", 40, 215),
    (1200, "Theo dõi Fanpage", 58, 235),
    (1268, "Giả Thuyết Kiến Trúc", 104, 255),
    (1440, "Bài viết phân tích đầy đủ", 54, 240),
    (1502, "xem ở dòng đầu tiên", 54, 240),
    (1590, "trong phần bình luận", 64, 255),
]
INK = (46, 38, 32)
PAPER = (229, 215, 191)  # beige print margin


def F(size):
    return ImageFont.truetype(FONT, size)


def put_credit(t, xy, size, fill, anchor="la", credit=None):
    """credit một dòng (riêng cho từng ảnh); dài quá 960 px thì giảm cỡ chữ (tối thiểu 26)"""
    txt = credit or CREDIT
    s = size
    while s > 26 and t.d.textlength(txt, font=F(s)) > 960:
        s -= 1
    t.put(xy, txt, s, fill, anchor)


# ---------------- board geometry (2x master, 1x = reel canvas) ----------------
B2W, B2H = W * 2, H * 2
CARD_W2, BORDER2 = 1320, 0  # ảnh chính dọc 2:3: thẻ hẹp hơn để chữ nằm ngoài ảnh
C2 = (B2W / 2, 1880.0)
ANGLE = 1.2  # degrees, counter-clockwise (card is hung very slightly crooked)


class Photo:
    """một ảnh nguồn và hình học thẻ ảnh của nó; cảnh chỉ tới ảnh qua SCENES[i]["img"] (mặc định "main")"""

    def __init__(self, path, card_w2=None, c2y=None, border2=None, credit=None, angle=ANGLE):
        self.src = Image.open(path).convert("RGB")
        self.SW, self.SH = self.src.size
        self.CARD_W2 = CARD_W2 if card_w2 is None else card_w2
        self.BORDER2 = BORDER2 if border2 is None else border2
        self.PH_W2 = self.CARD_W2 - 2 * self.BORDER2
        self.PH_H2 = int(round(self.PH_W2 * self.SH / self.SW))
        self.CARD_H2 = self.PH_H2 + 2 * self.BORDER2
        self.C2 = (B2W / 2, C2[1] if c2y is None else c2y)
        self.ANGLE = angle
        self.S2 = self.PH_W2 / self.SW
        self.ROT = cv2.getRotationMatrix2D(self.C2, angle, 1.0)
        self.CARD_TOP1, self.CARD_BOT1 = (self.C2[1] - self.CARD_H2 / 2) / 2, (self.C2[1] + self.CARD_H2 / 2) / 2
        self.CARD_L1, self.CARD_R1 = (self.C2[0] - self.CARD_W2 / 2) / 2, (self.C2[0] + self.CARD_W2 / 2) / 2
        self.center = (self.SW / 2, self.SH / 2)
        self.credit = credit
        self.boards = {}

    def src_to_b2(self, p):
        ux = self.C2[0] + p[0] * self.S2 - self.PH_W2 / 2
        uy = self.C2[1] + p[1] * self.S2 - self.PH_H2 / 2
        R = self.ROT
        return (R[0, 0] * ux + R[0, 1] * uy + R[0, 2], R[1, 0] * ux + R[1, 1] * uy + R[1, 2])

    def board(self, key):
        if key not in self.boards:
            self.boards[key] = make_board(0.86 if key == "dark" else 1.0, self)
        return self.boards[key]


PHOTOS = {"main": Photo(SRC)}
DEFAULT_IMG = "main"
src = PHOTOS["main"].src
SW, SH = src.size
PH_W2, PH_H2, CARD_H2 = PHOTOS["main"].PH_W2, PHOTOS["main"].PH_H2, PHOTOS["main"].CARD_H2
S2, ROT = PHOTOS["main"].S2, PHOTOS["main"].ROT
CARD_TOP1, CARD_BOT1 = PHOTOS["main"].CARD_TOP1, PHOTOS["main"].CARD_BOT1


def src_to_b2(p):
    return PHOTOS[DEFAULT_IMG].src_to_b2(p)


# ---------------- colour ----------------
def rel_lum(c):
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(float(x)) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def dominant(img):
    a = np.array(img.resize((160, 108), Image.LANCZOS)).reshape(-1, 3).astype(np.float32)
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5)
    cv2.setRNGSeed(7)
    _, lab, cen = cv2.kmeans(a, 5, None, crit, 4, cv2.KMEANS_PP_CENTERS)
    counts = np.bincount(lab.flatten(), minlength=5).astype(float)
    for k, c in enumerate(cen):
        if c.mean() < 28 or c.mean() > 232:
            counts[k] = 0
    return cen[int(np.argmax(counts))]


DOM = dominant(src)


def fabric_base():
    return np.array((238, 231, 217), np.float32)  # light beige linen (user's reference)


FAB = fabric_base()



def draw_tape(img, c, ang_deg, w=260, h=104):
    """strip of paper (washi) tape stuck over the top edge of the print"""
    cx, cy = c
    rng = np.random.default_rng(8)
    pad = 40
    tw, th = w + 2 * pad, h + 2 * pad
    m = np.zeros((th, tw), np.float32)
    xs = np.arange(0, w + 1, 12)
    zz = lambda: rng.uniform(-4, 4, len(xs))
    top = pad + zz(); bot = pad + h + zz()
    left = [(pad + rng.uniform(-3, 3), pad + y) for y in np.linspace(0, h, 6)]
    poly = [(pad + x, t) for x, t in zip(xs, top)] + [(pad + w + rng.uniform(-3, 3), pad + y) for y in np.linspace(0, h, 6)] \
        + [(pad + x, b) for x, b in zip(xs[::-1], bot[::-1])] + left[::-1]
    cv2.fillPoly(m, [np.array(poly, np.int32)], 1.0)
    m = cv2.GaussianBlur(m, (0, 0), 1.2)
    yy, xx = np.mgrid[0:th, 0:tw].astype(np.float32)
    fib = cv2.GaussianBlur(rng.normal(size=(th, tw)).astype(np.float32), (0, 0), sigmaX=9, sigmaY=0.8)
    fib /= fib.std()
    col = np.array((236, 224, 196), np.float32)[None, None, :] * (1 + 0.018 * fib)[..., None]
    col *= (1 - 0.06 * np.clip(np.abs(yy - th / 2) / (h / 2), 0, 1))[..., None]
    a = m * 0.80
    Mr = cv2.getRotationMatrix2D((tw / 2, th / 2), ang_deg, 1.0)
    col = cv2.warpAffine(col, Mr, (tw, th), flags=cv2.INTER_CUBIC)
    a = cv2.warpAffine(a, Mr, (tw, th), flags=cv2.INTER_LINEAR)
    sh = np.roll(np.roll(cv2.GaussianBlur(a, (0, 0), 6), 7, 0), 3, 1) * 0.35
    x0, y0 = int(cx - tw / 2), int(cy - th / 2)
    reg = img[y0:y0 + th, x0:x0 + tw]
    reg[:] = reg * (1 - sh[..., None])
    reg[:] = reg * (1 - a[..., None]) + col * a[..., None]

# ---------------- procedural board ----------------
def smoothstep(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def linen():
    rng = np.random.default_rng(11)
    h, w = B2H, B2W
    a = cv2.GaussianBlur(rng.normal(size=(h, w)).astype(np.float32), (0, 0), sigmaX=6.5, sigmaY=0.7)
    b = cv2.GaussianBlur(rng.normal(size=(h, w)).astype(np.float32), (0, 0), sigmaX=0.7, sigmaY=6.5)
    g = cv2.GaussianBlur(rng.normal(size=(h, w)).astype(np.float32), (0, 0), 0.9)
    low = cv2.resize(cv2.GaussianBlur(rng.normal(size=(h // 8, w // 8)).astype(np.float32), (0, 0), 10), (w, h))
    xs = np.arange(w, dtype=np.float32)[None, :]
    ys = np.arange(h, dtype=np.float32)[:, None]
    weave = np.sin(xs * (2 * np.pi / 5.0)) * np.sin(ys * (2 * np.pi / 5.0))
    tex = 0.55 * a / a.std() + 0.55 * b / b.std() + 0.30 * g / g.std() + 0.45 * low / low.std() + 0.22 * weave
    vig = 1 - 0.10 * (((xs - w / 2) / (w / 2)) ** 2 + ((ys - h / 2) / (h / 2)) ** 2) / 2
    img = FAB[None, None, :] * (1 + 0.032 * tex * 1.0)[..., None] * vig[..., None]
    return np.clip(img, 0, 255).astype(np.float32)


def draw_pin(img, c, r=60):
    """light-oak turned wooden pin head, seen from the front"""
    cx, cy = int(round(c[0])), int(round(c[1]))
    pad = int(r * 2.6)
    n = 2 * pad
    x0, y0 = cx - pad, cy - pad
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    px, py = xx - pad, yy - pad
    sh = (np.hypot(px - 0.28 * r, py - 0.40 * r) < r * 1.02).astype(np.float32)
    sh = cv2.GaussianBlur(sh, (0, 0), r * 0.26) * 0.55
    d = np.hypot(px, py)
    a = np.clip((r - d) / 2.5, 0, 1)
    rng = np.random.default_rng(3)
    g = cv2.GaussianBlur(rng.normal(size=(n, n)).astype(np.float32), (0, 0), sigmaX=r * 0.9, sigmaY=1.3)
    g = g / g.std()
    rings = np.sin((d / r) * 9.0 + 1.5 * g) * 0.5
    lit = np.clip(0.90 + 0.22 * (-(px * 0.5 + py * 0.65) / r), 0.6, 1.15)
    tone = (1 + 0.055 * g + 0.04 * rings) * lit * (1 - 0.16 * np.clip(d / r, 0, 1) ** 3)
    col = np.array((224, 190, 142), np.float32)[None, None, :] * tone[..., None]
    col *= (1 - 0.20 * np.exp(-(((d - r * 0.92) / (r * 0.04)) ** 2)))[..., None]
    hl = np.clip(1 - np.hypot((px + 0.34 * r) / (0.30 * r), (py + 0.38 * r) / (0.18 * r)), 0, 1) * 0.35
    col = col * (1 - hl[..., None]) + 255 * hl[..., None]
    ys0, xs0 = max(0, y0), max(0, x0)
    ys1, xs1 = min(img.shape[0], y0 + n), min(img.shape[1], x0 + n)
    sl = (slice(ys0 - y0, ys1 - y0), slice(xs0 - x0, xs1 - x0))
    reg = img[ys0:ys1, xs0:xs1]
    reg *= (1 - sh[sl])[..., None]
    reg[:] = reg * (1 - a[sl][..., None]) + np.clip(col[sl], 0, 255) * a[sl][..., None]


# material samples cut from the project photo, pinned on the empty linen (decor only)
SWATCHES = [
    dict(box=(480, 950, 720, 1086), size2=(440, 250), center2=(520, 3430), angle=3.0),   # oak herringbone floor
    dict(box=(745, 668, 890, 718), size2=(440, 152), center2=(1610, 3400), angle=-3.5),  # green velvet sofa
]


def add_swatch(out, sw):
    bw = 22
    cw, ch = sw["size2"]
    crop = np.array(src.crop(sw["box"]).resize((cw, ch), Image.LANCZOS)).astype(np.float32)
    card = np.empty((ch + 2 * bw, cw + 2 * bw, 3), np.float32)
    card[:] = PAPER
    card[bw:bw + ch, bw:bw + cw] = crop
    pad = 130
    ph_, pw_ = card.shape[0] + 2 * pad, card.shape[1] + 2 * pad
    patch = np.empty((ph_, pw_, 3), np.float32)
    patch[:] = PAPER
    al = np.zeros((ph_, pw_), np.float32)
    patch[pad:pad + card.shape[0], pad:pad + card.shape[1]] = card
    al[pad:pad + card.shape[0], pad:pad + card.shape[1]] = 1
    M = cv2.getRotationMatrix2D((pw_ / 2, ph_ / 2), sw["angle"], 1.0)
    patch = cv2.warpAffine(patch, M, (pw_, ph_), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    al = cv2.warpAffine(al, M, (pw_, ph_), flags=cv2.INTER_LINEAR)
    X0, Y0 = int(sw["center2"][0] - pw_ / 2), int(sw["center2"][1] - ph_ / 2)
    reg = out[Y0:Y0 + ph_, X0:X0 + pw_]
    s1 = cv2.GaussianBlur(np.roll(np.roll(al, 20, 0), 11, 1), (0, 0), 22) * 0.42
    s2 = cv2.GaussianBlur(np.roll(np.roll(al, 6, 0), 3, 1), (0, 0), 5) * 0.28
    reg *= ((1 - s1) * (1 - s2))[..., None]
    reg[:] = reg * (1 - al[..., None]) + patch * al[..., None]
    tx, ty = pw_ / 2, pad + 58
    rx = M[0, 0] * tx + M[0, 1] * ty + M[0, 2]
    ry = M[1, 0] * tx + M[1, 1] * ty + M[1, 2]
    draw_pin(reg, (rx, ry), 36)


_LINEN = None


def make_board(dark, P=None, swatches=False):
    P = P or PHOTOS[DEFAULT_IMG]
    global _LINEN
    if _LINEN is None:
        _LINEN = linen()
    fab = np.full((B2H, B2W, 3), 255.0, np.float32)  # plain white background
    # paper card (unrotated), then rotate rgb + alpha together
    x0, y0 = int(P.C2[0] - P.CARD_W2 / 2), int(P.C2[1] - P.CARD_H2 / 2)
    rgb = np.empty((B2H, B2W, 3), np.float32)
    rgb[:] = PAPER
    rng = np.random.default_rng(5)
    paper = np.empty((P.CARD_H2, P.CARD_W2, 3), np.float32)
    paper[:] = PAPER
    paper *= (1 + 0.012 * cv2.GaussianBlur(rng.normal(size=(P.CARD_H2, P.CARD_W2)).astype(np.float32), (0, 0), 1.2))[..., None]
    ph = np.array(P.src.resize((P.PH_W2, P.PH_H2), Image.LANCZOS)).astype(np.float32) * dark
    paper[P.BORDER2:P.BORDER2 + P.PH_H2, P.BORDER2:P.BORDER2 + P.PH_W2] = ph
    # hairline shadow where the print edge meets the white margin
    edge = np.zeros((P.CARD_H2, P.CARD_W2), np.float32)
    rgb[y0:y0 + P.CARD_H2, x0:x0 + P.CARD_W2] = paper
    al = np.zeros((B2H, B2W), np.float32)
    al[y0:y0 + P.CARD_H2, x0:x0 + P.CARD_W2] = 1
    rgb = cv2.warpAffine(rgb, P.ROT, (B2W, B2H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    al = cv2.warpAffine(al, P.ROT, (B2W, B2H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    # soft shadows on the linen
    s1 = cv2.GaussianBlur(np.roll(np.roll(al, 26, 0), 14, 1), (0, 0), 30) * 0.42
    s2 = cv2.GaussianBlur(np.roll(np.roll(al, 8, 0), 4, 1), (0, 0), 7) * 0.30
    fab *= ((1 - s1) * (1 - s2))[..., None]
    out = fab * (1 - al[..., None]) + rgb * al[..., None]
    if swatches:
        for sw in SWATCHES:
            add_swatch(out, sw)
    cx, cy = P.C2[0], y0 + 6  # tape centred on the top edge
    px = P.ROT[0, 0] * cx + P.ROT[0, 1] * cy + P.ROT[0, 2]
    py = P.ROT[1, 0] * cx + P.ROT[1, 1] * cy + P.ROT[1, 2]
    draw_tape(out, (px, py), P.ANGLE - 3.0)
    b2 = np.concatenate([np.clip(out, 0, 255), (al * 255)[..., None]], 2).astype(np.uint8)
    b1 = cv2.resize(b2, (W, H), interpolation=cv2.INTER_AREA)
    return b1, b2


# ---------------- camera ----------------
class Cam:
    """focus_src: điểm trên ảnh (hoặc "C" = tâm ảnh); anchor: (x, y) trên khung, ("top", y[, x]) đặt mép trên thẻ ở y,
    ("cover"[, x, y]) dời neo để thẻ phủ kín khung nếu zoom đủ lớn"""

    def __init__(self, focus_src, z, anchor, P=None):
        self.P = P or PHOTOS[DEFAULT_IMG]
        self.focus = self.P.center if focus_src == "C" else tuple(focus_src)
        self.z = z
        fb = self.P.src_to_b2(self.focus)
        self.F = (fb[0] / 2, fb[1] / 2)
        self.s = z * self.P.S2 / 2  # canvas px per source px
        self.A = self._anchor(anchor)

    def _anchor(self, anchor):
        if isinstance(anchor, (tuple, list)) and anchor and isinstance(anchor[0], str):
            kind = anchor[0]
            if kind == "top":
                ax = anchor[2] if len(anchor) > 2 else W / 2
                return (ax, anchor[1] + self.z * (self.F[1] - self.P.CARD_TOP1))
            if kind == "cover":
                ax = anchor[1] if len(anchor) > 1 else W / 2
                ay = anchor[2] if len(anchor) > 2 else 900
                m = 40
                z, F, P = self.z, self.F, self.P
                lo, hi = W + m - z * (P.CARD_R1 - F[0]), -m - z * (P.CARD_L1 - F[0])
                if lo <= hi:
                    ax = min(max(ax, lo), hi)
                lo, hi = H + m - z * (P.CARD_BOT1 - F[1]), -m - z * (P.CARD_TOP1 - F[1])
                if lo <= hi:
                    ay = min(max(ay, lo), hi)
                return (ax, ay)
            raise ValueError(anchor)
        return tuple(anchor)

    def pt(self, p):
        bx, by = self.P.src_to_b2(p)
        return (self.A[0] + self.z * (bx / 2 - self.F[0]), self.A[1] + self.z * (by / 2 - self.F[1]))

    def board_y(self, y1):
        return self.A[1] + self.z * (y1 - self.F[1])

    @property
    def card_top(self):
        return self.board_y(self.P.CARD_TOP1)

    @property
    def card_bottom(self):
        return self.board_y(self.P.CARD_BOT1)

    def render(self, b1, b2):
        z = self.z
        if z <= 1.25:
            M = np.float32([[z, 0, self.A[0] - z * self.F[0]], [0, z, self.A[1] - z * self.F[1]]])
            return cv2.warpAffine(b1, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255, 0)).astype(np.float32)
        s = z / 2
        M = np.float32([[s, 0, self.A[0] - s * 2 * self.F[0]], [0, s, self.A[1] - s * 2 * self.F[1]]])
        out = cv2.warpAffine(b2, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255, 0)).astype(np.float32)
        blur = cv2.GaussianBlur(out, (0, 0), 1.5)
        return np.clip(out * 1.45 - blur * 0.45, 0, 255)  # mild unsharp: zoom upsamples the print


# ---------------- brush (white dashed doodles + ink arrows) ----------------
def noise1d(rng, n, corr):
    r = rng.normal(size=n + 80).astype(np.float32).reshape(1, -1)
    b = cv2.GaussianBlur(r, (0, 0), sigmaX=max(1.0, corr / 2.0)).ravel()
    return (b / (b.std() + 1e-6))[40:40 + n]


def densify(pts, step=2.0):
    out = []
    for (x1, y1), (x2, y2) in zip(pts[:-1], pts[1:]):
        n = max(1, int(math.hypot(x2 - x1, y2 - y1) / step))
        for i in range(n):
            t = i / n
            out.append((x1 + (x2 - x1) * t, y1 + (y2 - y1) * t))
    out.append(pts[-1])
    return np.array(out, np.float32)


def bezier(a, b, bow, n=40):
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    dx, dy = b[0] - a[0], b[1] - a[1]
    L = math.hypot(dx, dy) + 1e-6
    cx, cy = mx - dy / L * bow, my + dx / L * bow
    return [((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * cx + t * t * b[0],
             (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * cy + t * t * b[1]) for t in np.linspace(0, 1, n)]


class Brush:
    def __init__(self, cam):
        self.P = cam.P
        self.m = np.zeros((H * SS, W * SS), np.uint8)
        self.v = cam
        self.n = 0
        self.circ = []

    def mask(self):
        return cv2.resize(self.m, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0

    def stroke(self, pts, w=7.0, taper=(0.07, 0.14), amp=2.0, corr=26, floor=0.28):
        self.n += 1
        rng = np.random.default_rng(self.n * 7919 + 13)
        P = densify(pts, 2.0)
        n = len(P)
        if n < 4:
            return
        P[:, 0] += noise1d(rng, n, corr) * amp
        P[:, 1] += noise1d(rng, n, corr) * amp
        t = np.linspace(0, 1, n)
        ramp = np.minimum(smoothstep(t / max(taper[0], 1e-3)), smoothstep((1 - t) / max(taper[1], 1e-3)))
        wv = w * (floor + (1 - floor) * ramp) * (1 + 0.14 * noise1d(rng, n, 40))
        for (x, y), ww in zip(P, wv):
            self.circ.append((int(x * SS), int(y * SS), max(1, int(ww * SS / 2))))

    def dashed_path(self, P, w=8, dash=(80, 150), gap=(16, 28), closed=False, amp=1.6):
        pts = list(P) + ([P[0]] if closed else [])
        D = densify(pts, 3.0)
        rng = np.random.default_rng(self.n * 17 + 3)
        if closed:
            k = int(rng.integers(0, len(D) - 1))
            D = np.vstack([D[k:-1], D[:k + 1]])
        seg = np.hypot(np.diff(D[:, 0]), np.diff(D[:, 1]))
        sacc = np.concatenate([[0], np.cumsum(seg)])
        total = float(sacc[-1]) - (30.0 if closed else 0.0)
        d = 0.0
        while d < total - 6:
            e = min(d + rng.uniform(*dash), total)
            i0, i1 = int(np.searchsorted(sacc, d)), int(np.searchsorted(sacc, e))
            sub = [tuple(p) for p in D[i0:i1 + 1]]
            if len(sub) >= 2:
                self.stroke(sub, w, taper=(0.12, 0.2), amp=amp, corr=16, floor=0.6)
            d = e + rng.uniform(*gap)

    def line(self, a, b, w=8, bow=None, over=6, dash=(80, 150), gap=(16, 28)):
        A, B = self.v.pt(a), self.v.pt(b)
        L = math.hypot(B[0] - A[0], B[1] - A[1]) + 1e-6
        ux, uy = (B[0] - A[0]) / L, (B[1] - A[1]) / L
        A = (A[0] - ux * over, A[1] - uy * over)
        B = (B[0] + ux * over, B[1] + uy * over)
        rng = np.random.default_rng(self.n + 5)
        bw = bow if bow is not None else rng.normal() * 0.012 * L
        self.n += 1
        self.dashed_path(bezier(A, B, bw), w, dash, gap)

    def dashed(self, a, b, w=7):
        self.line(a, b, w, bow=0, over=0, dash=(26, 42), gap=(16, 26))

    def arrow(self, a, b, w=7, bow=40, head=38):
        """dashed arrow between two photo points"""
        A, B = self.v.pt(a), self.v.pt(b)
        path = bezier(A, B, bow)
        self.n += 1
        self.dashed_path(path, w, dash=(46, 80), gap=(14, 22))
        self._head(path, w, head)

    def _head(self, path, w, head):
        (x1, y1), (x2, y2) = path[-4], path[-1]
        ang = math.atan2(y2 - y1, x2 - x1)
        for da in (2.6, -2.6):
            self.stroke([(x2, y2), (x2 + head * math.cos(ang + da), y2 + head * math.sin(ang + da))],
                        w * 0.9, taper=(0.1, 0.5), amp=0.8, corr=8)

    def ink_arrow(self, A, B, w=6, bow=40, head=34):
        """solid hand-drawn annotation arrow, canvas coordinates"""
        path = bezier(A, B, bow)
        self.stroke(path, w, taper=(0.06, 0.2), amp=1.6, corr=30)
        self._head(path, w, head)

    def ellipse(self, cx, cy, rx, ry, w=8, rot=0.0):
        C = self.v.pt((cx, cy))
        rx, ry = rx * self.v.s, ry * self.v.s
        rng = np.random.default_rng(self.n * 31 + 7)
        t0, ph = rng.uniform(-1.2, 0.2), rng.uniform(0, 6.28)
        pts = []
        for i in range(91):
            u = i / 90
            t = t0 + (2 * math.pi + 0.5) * u
            k = 1 + 0.03 * u + 0.025 * math.sin(2 * t + ph)
            x, y = rx * k * math.cos(t), ry * k * math.sin(t)
            pts.append((C[0] + x * math.cos(rot) - y * math.sin(rot), C[1] + x * math.sin(rot) + y * math.cos(rot)))
        self.n += 1
        self.dashed_path(pts, w)

    def contour(self, poly, offset=14, eps=2.5, w=8, dash=(80, 150), gap=(16, 28)):
        pad = 80
        mask = np.zeros((self.v.P.SH + 2 * pad, self.v.P.SW + 2 * pad), np.uint8)
        cv2.fillPoly(mask, [np.array(poly, np.int32) + pad], 255)
        cont = [(x - pad, y - pad) for x, y in loose_contour(mask, offset=offset, eps=eps)]
        self.n += 1
        P = densify([self.v.pt(p) for p in cont] + [self.v.pt(cont[0])], 4.0)[:-1]
        k = max(3, int(len(P) * 0.012) | 1)  # circular moving average: rounds corners, removes spurs
        ext = np.vstack([P[-k:], P, P[:k]])
        ker = np.ones(k, np.float32) / k
        Sx = np.convolve(ext[:, 0], ker, mode="same")[k:-k]
        Sy = np.convolve(ext[:, 1], ker, mode="same")[k:-k]
        self.dashed_path(list(zip(Sx, Sy)), w, dash, gap, closed=True)

    def wave(self, x1, x2, y, w=6):
        pts = [(x1 + (x2 - x1) * i / 30, y + 4 * math.sin(i * 0.9)) for i in range(31)]
        self.stroke(pts, w, taper=(0.05, 0.25), amp=1.2, corr=18)


# ---------------- text ----------------
class Text:
    def __init__(self):
        self.img = Image.new("L", (W, H), 0)
        self.d = ImageDraw.Draw(self.img)

    def wrap(self, text, size, width):
        words, lines, cur = text.split(), [], ""
        for w_ in words:
            t = (cur + " " + w_).strip()
            if self.d.textlength(t, font=F(size)) <= width:
                cur = t
            else:
                lines.append(cur)
                cur = w_
        if cur:
            lines.append(cur)
        return lines

    def put(self, xy, text, size, fill=255, anchor="la"):
        self.d.text(xy, text, font=F(size), fill=fill, anchor=anchor)

    def block(self, x, y, text, size, lh, width=960, fill=255):
        for i, ln in enumerate(self.wrap(text, size, width)):
            self.put((x, y + i * lh), ln, size, fill)


def scrim(base, top=False, bottom=False):
    ys = np.arange(H, dtype=np.float32)
    f = np.ones(H, np.float32)
    if top:
        f *= 0.42 + 0.58 * smoothstep(ys / 620.0)
    if bottom:
        f *= 0.40 + 0.60 * smoothstep((1980 - ys) / 700.0)
    return base * f[:, None, None]


DARK = np.array((62, 54, 46), np.float32)


def compose(base, white, fabm):
    fabm = (fabm > 0.5).astype(np.float32)
    fabm = cv2.GaussianBlur(fabm, (0, 0), 1.0)
    dark = white * fabm
    white = white * (1 - fabm)
    sh = cv2.GaussianBlur(white, (0, 0), 5)
    sh = np.roll(np.roll(sh, 5, 0), 3, 1)
    halo = np.clip(cv2.GaussianBlur(white, (0, 0), 2.4) * 1.7, 0, 1)
    out = base * (1 - 0.40 * sh)[..., None] * (1 - 0.50 * halo)[..., None]
    out = out * (1 - white[..., None]) + 255.0 * white[..., None]
    out = out * (1 - dark[..., None]) + DARK * dark[..., None]
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


# ---------------- scenes ----------------
CENTER = (SW / 2, SH / 2)
OBJ = {}
PHOTOS["main"].credit = 'Ảnh dự án: Union Street House, Northcote, Melbourne · Prior Barraclough · ảnh Ben Hosking'
PHOTOS["inox"] = Photo(os.path.join(HERE, "..", "source_inox.png"), credit='Ảnh dự án: Union Street House, Northcote, Melbourne · Prior Barraclough · ảnh Ben Hosking')
PHOTOS["sodo1"] = Photo(os.path.join(HERE, "..", "source_sodo1.png"), 1200, 1810.0, credit='Sơ đồ: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014)')
PHOTOS["sodo9"] = Photo(os.path.join(HERE, "..", "source_sodo9.png"), 1200, 1810.0, credit='Sơ đồ: Giả Thuyết Kiến Trúc, theo Kilmer & Kilmer (2014)')
PHOTOS["mb"] = Photo(os.path.join(HERE, "..", "source_mb.png"), 1400, 1810.0, credit='Mặt bằng tầng trệt: bản vẽ Prior Barraclough, nguồn ArchDaily (2023)')

SCENES = [
    dict(t="0–4.49s", img="main", head="Sao phòng gỗ tối hơn?", vo="Cùng một ô cửa, sao phòng sơn trắng sáng hẳn, còn phòng ốp gỗ lại tối?",
         cam=('C', 1.0, (540, 940)), dark=False, dd=[]),
    dict(t="4.49–11.2s", img="sodo1", head="Kilmer & Kilmer (2014): ánh sáng hắt lại", vo="Theo hai tác giả Kilmer, mắt chỉ thấy ánh sáng do bề mặt hắt lại. Tường trắng mờ hắt nhiều, gỗ sẫm nuốt bớt.",
         cam=('C', 1.25, ('top', 520)), dark=False, dd=[]),
    dict(t="11.2–16.94s", img="sodo9", head="Trần sáng nhất, sàn tối nhất", vo="Nên trần cần sáng nhất, rồi tới tường, mặt bàn, sàn. Mặt mờ cho ánh sáng tỏa đều.",
         cam=('C', 1.25, ('top', 520)), dark=False, dd=[]),
    dict(t="16.94–21.37s", img="sodo9", head="Gạch bóng kính: vệt nắng chói", vo="Nhà phố hay lát gạch bóng kính cho dễ lau, rồi trên sàn hiện vệt nắng chói.",
         cam=('C', 1.25, ('top', 520)), dark=False, dd=[]),
    dict(t="21.37–27.34s", img="mb", head="Union Street House: ốp gỗ gần hết", vo="Nhà Union Street của Prior Barraclough ở Melbourne lại ốp gỗ gần hết, tường, trần lẫn đồ.",
         cam=('C', 1.15, ('top', 520)), dark=False, dd=[]),
    dict(t="27.34–31.28s", img="mb", head="Gỗ hắt ít, bù bằng kính hai đầu", vo="Gỗ hắt ít sáng hơn tường trắng, nên họ bù bằng kính ở hai đầu nhà.",
         cam=('C', 1.15, ('top', 520)), dark=False, dd=[]),
    dict(t="31.28–36.14s", img="main", head="Gỗ mờ: không có điểm chói", vo="Ánh sáng qua vách lam chuyển đều trên tường và mặt dưới cầu thang. Không có điểm chói nào.",
         cam=((850, 1000), 1.7, ('top', 400)), dark=True, dd=['arr_lam', 'lab_lam', 'lab_cauthang']),
    dict(t="36.14–42.14s", img="inox", head="Bếp đổi hẳn: hốc inox bóng", vo="Bếp, chỗ cần sáng nhất, thì đổi hẳn. Hốc bếp bọc inox bóng, phản chiếu cả ánh sáng lẫn đồ vật.",
         cam=((800, 900), 1.7, ('top', 540)), dark=True, dd=['arr_inox', 'lab_inox', 'arr_go', 'lab_go']),
    dict(t="42.14–46.08s", img="inox", head="Giấu trong hốc hẹp", vo="Mặt bóng giấu trong hốc hẹp, nên chỗ nấu sáng lên mà không chói ra phòng.",
         cam=((760, 750), 2.1, ('cover', 540, 900)), dark=False, dd=[]),
    dict(t="46.08–51.8s", img="main", head="Chốt lại", vo="Phòng sáng tới đâu, do bề mặt đầu tiên ánh sáng chạm vào. Bài phân tích đầy đủ cho thành viên ở phần bình luận nha.",
         cam=('C', 1.0, (540, 940)), dark=False, dd=[]),
    dict(t="51.8–55.5s", img="main", head="end", vo="",
         cam=('C', 0.8, (540, 600)), dark=False, dd=[]),
]
END = len(SCENES) - 1
BOARDS = {}

_L = np.load(os.path.join(HERE, "doodle_ep07.npz"))
LAYER = {k: _L[k] for k in _L.files}   # toạ độ trên ảnh làm việc 1600x2400 của ảnh mà cảnh dùng (arr/lab_inox, arr/lab_go: ảnh "inox"; còn lại: ảnh "main")
RAD = dict(arr_lam=0.8, arr_san=0.8, arr_inox=0.8, arr_go=0.8)   # bán kính nét gốc (px ảnh làm việc)


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
            _stamp(wb, LAYER[k], RAD[k])


# ---------------- render ----------------

import subprocess, re
FPS = 30
TRANS = 0.7
DARKC = DARK


def sm(x):
    return float(smoothstep(np.float32(x)))


def times(t):
    a, b = re.findall(r"[\d.]+", t.replace("–", "-"))[:2]
    return float(a), float(b)


def layout(i):
    sc = SCENES[i]
    P = PHOTOS[sc.get("img", DEFAULT_IMG)]
    cam = Cam(*sc["cam"], P=P)
    key = "dark" if sc["dark"] else "plain"
    wb = Brush(cam)
    td, tm = Text(), Text()
    top, bot = cam.card_top, cam.card_bottom
    st, sb = False, False
    if i == END:
        put_credit(tm, (W // 2, bot + 30), 34, 225, "ma", credit=P.credit)
        for y_, s_, sz_, f_ in END_LINES:
            tm.put((W // 2, y_), s_, sz_, f_, "ma")
    else:
        doodle(i, wb, td, cam)
        title_on_fabric = top >= 440
        vo_lines = len(tm.wrap(sc["vo"], 60, 960))
        vo_below = bot + 110
        vo_on_fabric = vo_below + vo_lines * 78 <= 1800
        st, sb = not title_on_fabric, not vo_on_fabric
        if title_on_fabric:
            tm.put((60, 196), HEAD, 38, 215)
            tm.block(60, 250, sc["head"], 96, 104)
        else:
            tm.put((60, 96), HEAD, 36, 220)
            tm.block(60, 150, sc["head"], 84, 92)
        if vo_on_fabric:
            put_credit(tm, (60, bot + 26), 34, 230, credit=P.credit)
            tm.block(60, vo_below, sc["vo"], 60, 78)
        else:
            put_credit(tm, (60, 1388), 32, 235, credit=P.credit)
            tm.block(60, 1450, sc["vo"], 60, 78)
    a, b = times(sc["t"])
    f = scrim(np.ones((H, 1, 3), np.float32), top=st, bottom=sb)
    full = np.zeros((H * SS, W * SS), np.uint8)
    for x, y, r in wb.circ:
        cv2.circle(full, (x, y), r, 255, -1, cv2.LINE_AA)
    fullm = cv2.resize(full, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    tmm = np.array(tm.img, np.float32) / 255
    tdm = np.array(td.img, np.float32) / 255
    return dict(sc=sc, cam=sc["cam"], P=P, key=key, wb=wb, tm=tmm, td=tdm, f=f, t0=a, t1=b,
                final=np.maximum(fullm, np.maximum(tmm, tdm)), n=len(wb.circ))


L = [layout(i) for i in range(len(SCENES))]
print("layouts done", [l["n"] for l in L])
TOTAL = L[-1]["t1"] + 1.0  # hold last frame 1s extra


def render_cam(key, cam):
    return cam.render(*cam.P.board(key))


def lerp_cam(c0, c1, p, P):
    """nội suy giữa hai camera trên CÙNG một ảnh (focus, zoom theo log, neo)"""
    C0, C1 = Cam(*c0, P=P), Cam(*c1, P=P)
    z = math.exp(math.log(C0.z) * (1 - p) + math.log(C1.z) * p)
    f = (C0.focus[0] + (C1.focus[0] - C0.focus[0]) * p, C0.focus[1] + (C1.focus[1] - C0.focus[1]) * p)
    a = (C0.A[0] + (C1.A[0] - C0.A[0]) * p, C0.A[1] + (C1.A[1] - C0.A[1]) * p)
    return Cam(f, z, a, P=P)


proc = subprocess.Popen(
    ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
     "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", f"{TOTAL:.2f}",
     "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
     "-c:a", "aac", "-b:a", "128k", os.path.join(OUT, "video", "reel_be-mat-hat-sang_silent.mp4")], stdin=subprocess.PIPE)

nframes = int(TOTAL * FPS)
cur = -1
acc = None
ptr = 0
for fi in range(nframes):
    t = fi / FPS
    i = max(k for k in range(len(L)) if L[k]["t0"] <= t + 1e-6)
    ly = L[i]
    u = t - ly["t0"]
    dur = ly["t1"] - ly["t0"]
    if i != cur:
        cur, acc, ptr = i, np.zeros((H * SS, W * SS), np.uint8), 0
    if i == 0:
        p, trans = 1.0, 0.0
        cam = Cam(*ly["cam"], P=ly["P"])
        rr = render_cam(ly["key"], cam)
        fac = ly["f"]
        a_old = 0.0
        a_main = sm((u - 0.15) / 0.5)
        t_start = 0.0
    else:
        prev = L[i - 1]
        p = sm(u / TRANS)
        if prev["P"] is ly["P"]:
            cam = lerp_cam(prev["cam"], ly["cam"], p, ly["P"])
            r1 = render_cam(ly["key"], cam)
            if prev["key"] != ly["key"] and p < 1:
                r0 = render_cam(prev["key"], cam)
                rr = r0 * (1 - p) + r1 * p
            else:
                rr = r1
        else:
            # đổi ảnh nguồn: mờ chéo 0,7 giây giữa hai thẻ ảnh, mỗi thẻ đứng yên ở camera của cảnh mình
            cam = Cam(*ly["cam"], P=ly["P"])
            r1 = render_cam(ly["key"], cam)
            if p < 1:
                r0 = render_cam(prev["key"], Cam(*prev["cam"], P=prev["P"]))
                rr = r0 * (1 - p) + r1 * p
            else:
                rr = r1
        fac = prev["f"] * (1 - p) + ly["f"] * p
        a_old = 1 - sm(u / 0.25)
        a_main = sm((u - 0.40) / 0.30)
        t_start = TRANS + 0.15
    base, fabm = rr[..., :3] * fac, 1.0 - np.clip(rr[..., 3] / 255.0, 0, 1)
    # progressive strokes
    reveal_end = max(t_start + 0.8, 0.62 * dur)
    r = np.clip((u - t_start) / (reveal_end - t_start), 0, 1)
    r = r * r * (3 - 2 * r) * 0.35 + r * 0.65
    tgt = int(ly["n"] * r)
    if tgt > ptr:
        for x, y, rad in ly["wb"].circ[ptr:tgt]:
            cv2.circle(acc, (x, y), rad, 255, -1, cv2.LINE_AA)
        ptr = tgt
    sm_mask = cv2.resize(acc, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    a_lab = sm((r - 0.55) / 0.2) if ly["n"] else 0.0
    layer = np.maximum(sm_mask, np.maximum(ly["tm"] * a_main, ly["td"] * a_lab))
    if a_old > 0.002:
        layer = np.maximum(layer, L[i - 1]["final"] * a_old)
    # fade out at very end
    img = compose(base, layer, fabm)
    proc.stdin.write(np.asarray(img).tobytes())
    if fi % 90 == 0:
        print("frame", fi, "/", nframes, flush=True)
        if fi in (0, 240, 480, 720):
            img.save(os.path.join(OUT, "video", f"probe_{fi}.png"))
proc.stdin.close()
proc.wait()
print("done")
