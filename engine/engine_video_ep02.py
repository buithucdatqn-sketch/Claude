"""Reel storyboard generator v5 (one oak pin per print, beige margins, all-white text).
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
CREDIT = "Ảnh dự án: Anderson Residence · Aaron G. Green · ảnh Sterling Reed · Dwell"
HEAD = "AH DECODE · TẦM NHÌN & NƠI TRÚ ẨN"
# Khung cuối cố định cho mọi tập: giới thiệu series AH Decode, mời theo dõi Fanpage Giả Thuyết Kiến Trúc, KHÔNG nhắc tập sau. (y, chữ, cỡ, độ đậm)
END_LINES = [
    (1060, "AH Decode · series phân tích nguyên tắc thiết kế", 40, 215),
    (1108, "và cách chọn đồ decor", 40, 215),
    (1200, "Theo dõi Fanpage", 58, 235),
    (1268, "Giả Thuyết Kiến Trúc", 104, 255),
    (1440, "Bài viết về kiến trúc dành riêng", 54, 240),
    (1502, "cho thành viên", 54, 240),
    (1590, "Link ở phần bình luận", 64, 255),
]
INK = (46, 38, 32)
PAPER = (229, 215, 191)  # beige print margin


def F(size):
    return ImageFont.truetype(FONT, size)


def put_credit(t, xy, size, fill, anchor="la"):
    """credit một dòng; dài quá 960 px thì giảm cỡ chữ (tối thiểu 26)"""
    s = size
    while s > 26 and t.d.textlength(CREDIT, font=F(s)) > 960:
        s -= 1
    t.put(xy, CREDIT, s, fill, anchor)


src = Image.open(SRC).convert("RGB")
SW, SH = src.size

# ---------------- board geometry (2x master, 1x = reel canvas) ----------------
B2W, B2H = W * 2, H * 2
CARD_W2, BORDER2 = 1920, 0
PH_W2 = CARD_W2 - 2 * BORDER2
PH_H2 = int(round(PH_W2 * SH / SW))
CARD_H2 = PH_H2 + 2 * BORDER2
C2 = (B2W / 2, 1810.0)
ANGLE = 1.2  # degrees, counter-clockwise (card is hung very slightly crooked)
S2 = PH_W2 / SW
ROT = cv2.getRotationMatrix2D(C2, ANGLE, 1.0)
CARD_TOP1, CARD_BOT1 = (C2[1] - CARD_H2 / 2) / 2, (C2[1] + CARD_H2 / 2) / 2


def src_to_b2(p):
    ux = C2[0] + p[0] * S2 - PH_W2 / 2
    uy = C2[1] + p[1] * S2 - PH_H2 / 2
    return (ROT[0, 0] * ux + ROT[0, 1] * uy + ROT[0, 2], ROT[1, 0] * ux + ROT[1, 1] * uy + ROT[1, 2])


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


def make_board(dark, swatches=False):
    global _LINEN
    if _LINEN is None:
        _LINEN = linen()
    fab = np.full((B2H, B2W, 3), 255.0, np.float32)  # plain white background
    # paper card (unrotated), then rotate rgb + alpha together
    x0, y0 = int(C2[0] - CARD_W2 / 2), int(C2[1] - CARD_H2 / 2)
    rgb = np.empty((B2H, B2W, 3), np.float32)
    rgb[:] = PAPER
    rng = np.random.default_rng(5)
    paper = np.empty((CARD_H2, CARD_W2, 3), np.float32)
    paper[:] = PAPER
    paper *= (1 + 0.012 * cv2.GaussianBlur(rng.normal(size=(CARD_H2, CARD_W2)).astype(np.float32), (0, 0), 1.2))[..., None]
    ph = np.array(src.resize((PH_W2, PH_H2), Image.LANCZOS)).astype(np.float32) * dark
    paper[BORDER2:BORDER2 + PH_H2, BORDER2:BORDER2 + PH_W2] = ph
    # hairline shadow where the print edge meets the white margin
    edge = np.zeros((CARD_H2, CARD_W2), np.float32)
    rgb[y0:y0 + CARD_H2, x0:x0 + CARD_W2] = paper
    al = np.zeros((B2H, B2W), np.float32)
    al[y0:y0 + CARD_H2, x0:x0 + CARD_W2] = 1
    rgb = cv2.warpAffine(rgb, ROT, (B2W, B2H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    al = cv2.warpAffine(al, ROT, (B2W, B2H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    # soft shadows on the linen
    s1 = cv2.GaussianBlur(np.roll(np.roll(al, 26, 0), 14, 1), (0, 0), 30) * 0.42
    s2 = cv2.GaussianBlur(np.roll(np.roll(al, 8, 0), 4, 1), (0, 0), 7) * 0.30
    fab *= ((1 - s1) * (1 - s2))[..., None]
    out = fab * (1 - al[..., None]) + rgb * al[..., None]
    if swatches:
        for sw in SWATCHES:
            add_swatch(out, sw)
    cx, cy = C2[0], y0 + 6  # tape centred on the top edge
    px = ROT[0, 0] * cx + ROT[0, 1] * cy + ROT[0, 2]
    py = ROT[1, 0] * cx + ROT[1, 1] * cy + ROT[1, 2]
    draw_tape(out, (px, py), ANGLE - 3.0)
    b2 = np.concatenate([np.clip(out, 0, 255), (al * 255)[..., None]], 2).astype(np.uint8)
    b1 = cv2.resize(b2, (W, H), interpolation=cv2.INTER_AREA)
    return b1, b2


# ---------------- camera ----------------
class Cam:
    def __init__(self, focus_src, z, anchor):
        self.z, self.A = z, anchor
        fb = src_to_b2(focus_src)
        self.F = (fb[0] / 2, fb[1] / 2)
        self.s = z * S2 / 2  # canvas px per source px

    def pt(self, p):
        bx, by = src_to_b2(p)
        return (self.A[0] + self.z * (bx / 2 - self.F[0]), self.A[1] + self.z * (by / 2 - self.F[1]))

    def board_y(self, y1):
        return self.A[1] + self.z * (y1 - self.F[1])

    @property
    def card_top(self):
        return self.board_y(CARD_TOP1)

    @property
    def card_bottom(self):
        return self.board_y(CARD_BOT1)

    def render(self, b1, b2):
        z = self.z
        if z <= 1.25:
            M = np.float32([[z, 0, self.A[0] - z * self.F[0]], [0, z, self.A[1] - z * self.F[1]]])
            return cv2.warpAffine(b1, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT).astype(np.float32)
        s = z / 2
        M = np.float32([[s, 0, self.A[0] - s * 2 * self.F[0]], [0, s, self.A[1] - s * 2 * self.F[1]]])
        out = cv2.warpAffine(b2, M, (W, H), flags=cv2.INTER_LANCZOS4, borderMode=cv2.BORDER_REFLECT).astype(np.float32)
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
        mask = np.zeros((SH + 2 * pad, SW + 2 * pad), np.uint8)
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


def D(pts):
    """toạ độ đo trên ảnh xem 2000px -> ảnh làm việc 2400px"""
    return [(x * 1.2, y * 1.2) for x, y in pts]


OBJ = dict(
    window=D([(108, 340), (300, 322), (395, 318), (412, 880), (300, 900), (108, 905)]),
    sofa=D([(632, 785), (1325, 785), (1332, 900), (1325, 985), (632, 990), (628, 900)]),
    sofa_r=D([(1372, 905), (1505, 825), (1840, 980), (1836, 1150), (1700, 1232), (1380, 1060)]),
    ottomans=D([(305, 1000), (460, 930), (690, 925), (688, 1060), (600, 1195), (335, 1190)]),
    tables=D([(792, 935), (1030, 930), (1230, 950), (1310, 1080), (1310, 1195), (820, 1180)]),
    ghost=D([(450, 360), (630, 360), (630, 950), (450, 950)]),
)

WIDE = (CENTER, 1.0, (540, 905))
SCENES = [
    dict(t="0–3.5s", head="Bạn sẽ ngồi đâu?", vo="Vào phòng này, bạn sẽ ngồi đâu?",
         cam=WIDE, dark=False),
    dict(t="3.5–9.5s", head="Tầm nhìn và nơi trú ẩn", vo="Thập niên bảy mươi, Jay Appleton đặt tên cho hai điều: tầm nhìn, và nơi trú ẩn.",
         cam=WIDE, dark=True),
    dict(t="9.5–16.1s", head="Vì sao thấy yên tâm?", vo="Giả thuyết: chỗ vừa được che vừa nhìn xa giúp tổ tiên sống sót, nên ta thấy yên tâm.",
         cam=WIDE, dark=True),
    dict(t="16.1–19.9s", head="Nơi trú: lưng tựa vách", vo="Sofa tựa vách gỗ đặc, trần thấp dần: nơi trú.",
         cam=(((975 * 1.2), (640 * 1.2)), 1.9, (540, 900)), dark=True),
    dict(t="19.9–23.4s", head="Tầm nhìn: ra tận biển", vo="Bên trái, vách kính nhìn ra biển: tầm nhìn.",
         cam=(((560 * 1.2), (640 * 1.2)), 1.8, (540, 900)), dark=True),
    dict(t="23.4–30.3s", head="Công cụ của Wright", vo="Nghiên cứu nhà Frank Lloyd Wright ghi nhận ông hay dùng độ cao trần và khoảng cách tới tường đặc.",
         cam=WIDE, dark=True),
    dict(t="30.3–37.2s", head="Nhưng bằng chứng nói gì?", vo="Nhưng tổng hợp ba mươi tư nghiên cứu: trong nhà, tầm nhìn có bằng chứng mạnh hơn hẳn nơi trú.",
         cam=WIDE, dark=True),
    dict(t="37.2–41.3s", head="Đừng quây kín", vo="Nên tránh quây góc ngồi bằng vách cao hay tủ đứng.",
         cam=(((560 * 1.2), (640 * 1.2)), 1.8, (540, 900)), dark=True),
    dict(t="41.3–45.8s", head="Áp dụng", vo="Thử đặt ghế chính tựa tường đặc, mặt hướng ra cửa sổ.",
         cam=WIDE, dark=True),
    dict(t="45.8–51.2s", head="Chọn đồ: cao sát tường, thấp ở giữa", vo="Đồ cao nên sát tường, đồ giữa phòng nên thấp hơn tầm mắt khi ngồi.",
         cam=(((820 * 1.2), (930 * 1.2)), 1.9, (540, 860)), dark=True),
    dict(t="51.2–54.7s", head="Công thức", vo="Lưng có chỗ dựa, mắt có đường xa.",
         cam=WIDE, dark=False),
    dict(t="54.7–63.8s", head="end", vo="",
         cam=(CENTER, 1.0, (540, 640)), dark=False),
]
END = len(SCENES) - 1
BOARDS = {}

def doodle(i, wb, text, cam):
    def lab(p, s_, size=60):
        x, y = cam.pt(D([p])[0])
        text.put((x, y), s_, size)

    def P(p):
        return D([p])[0]

    def note(xy, s_, target, size=56, bow=-30):
        """nhãn trên nền trắng phía trên ảnh + mũi tên mực chỉ vào điểm trên ảnh"""
        text.put(xy, s_, size)
        w_ = text.d.textlength(s_, font=F(size))
        tx, ty = cam.pt(P(target))
        wb.ink_arrow((xy[0] + w_ / 2, xy[1] + size + 14), (tx, ty - 10), bow=bow)

    sofa = OBJ["sofa"]
    if i == 1:  # nguồn gốc: hai cụm khái niệm
        wb.contour(OBJ["window"], offset=14, eps=3, w=7)
        wb.contour(sofa, offset=14, eps=3, w=7)
        note((60, 420), "tầm nhìn", (250, 330), 58, bow=20)
        note((520, 420), "nơi trú", (980, 775), 58, bow=-20)
    elif i == 2:  # cơ chế: nhìn ra xa từ chỗ được che
        wb.contour(sofa, offset=14, eps=3, w=7)
        wb.arrow(P((900, 860)), P((300, 640)), 7, bow=-30)
    elif i == 3:  # nơi trú
        wb.contour(sofa, offset=16, eps=3, w=8)
        wb.line(P((660, 205)), P((1270, 362)), 8)
        wb.dashed(P((645, 230)), P((645, 860)), 7)
        wb.dashed(P((1288, 410)), P((1288, 860)), 7)
        lab((690, 312), "trần dốc xuống", 54)
        lab((760, 560), "vách gỗ đặc", 54)
    elif i == 4:  # tầm nhìn
        wb.contour(OBJ["window"], offset=14, eps=3, w=8)
        wb.arrow(P((900, 870)), P((330, 660)), 8, bow=-36)
        lab((120, 420), "ra biển", 58)
    elif i == 5:  # Wright: trần + tường
        wb.line(P((660, 205)), P((1270, 362)), 7)
        wb.line(P((60, 250)), P((600, 170)), 7)
        wb.dashed(P((645, 230)), P((645, 860)), 6)
        lab((1000, 150), "độ cao trần", 50)
        lab((680, 720), "tường đặc", 50)
    elif i == 6:  # bằng chứng
        wb.contour(OBJ["window"], offset=14, eps=3, w=7)
        wb.contour(sofa, offset=14, eps=3, w=7)
        note((40, 400), "tầm nhìn: mạnh", (250, 330), 56, bow=20)
        note((560, 400), "nơi trú: yếu hơn", (980, 775), 56, bow=-20)
    elif i == 7:  # lỗi: tủ cao chắn
        wb.contour(OBJ["ghost"], offset=4, eps=2, w=8)
        wb.line(P((470, 390)), P((610, 900)), 6)
        wb.line(P((610, 390)), P((470, 900)), 6)
        wb.arrow(P((900, 870)), P((660, 760)), 7, bow=-16)
        lab((410, 250), "tủ cao ở đây?", 54)
    elif i == 8:  # áp dụng
        wb.contour(sofa, offset=14, eps=3, w=7)
        wb.contour(OBJ["sofa_r"], offset=14, eps=3, w=7)
        wb.arrow(P((960, 860)), P((330, 660)), 7, bow=-30)
        wb.arrow(P((1500, 900)), P((420, 600)), 7, bow=-50)
    elif i == 9:  # chọn đồ
        wb.contour(OBJ["ottomans"], offset=12, eps=3, w=8)
        wb.contour(OBJ["tables"], offset=12, eps=3, w=8)
        wb.dashed(P((300, 650)), P((1340, 650)), 6)
        lab((330, 540), "tầm mắt lúc ngồi", 50)
        lab((420, 1215), "thấp", 54)
    elif i == 10:  # công thức
        wb.contour(sofa, offset=14, eps=3, w=7)
        wb.arrow(P((900, 860)), P((300, 640)), 7, bow=-30)


BOARDS["plain"] = make_board(1.0)
BOARDS["dark"] = make_board(0.86)
BOARDS["clean"] = BOARDS["plain"]

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
    cam = Cam(*sc["cam"])
    key = "dark" if sc["dark"] else "plain"
    if i == END:
        key = "clean"
    wb = Brush(cam)
    td, tm = Text(), Text()
    top, bot = cam.card_top, cam.card_bottom
    st, sb = False, False
    if i == END:
        put_credit(tm, (W // 2, bot + 30), 34, 225, "ma")
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
            put_credit(tm, (60, bot + 26), 34, 230)
            tm.block(60, vo_below, sc["vo"], 60, 78)
        else:
            put_credit(tm, (60, 1388), 32, 235)
            tm.block(60, 1450, sc["vo"], 60, 78)
    a, b = times(sc["t"])
    f = scrim(np.ones((H, 1, 3), np.float32), top=st, bottom=sb)
    full = np.zeros((H * SS, W * SS), np.uint8)
    for x, y, r in wb.circ:
        cv2.circle(full, (x, y), r, 255, -1, cv2.LINE_AA)
    fullm = cv2.resize(full, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32) / 255
    tmm = np.array(tm.img, np.float32) / 255
    tdm = np.array(td.img, np.float32) / 255
    return dict(sc=sc, cam=sc["cam"], key=key, wb=wb, tm=tmm, td=tdm, f=f, t0=a, t1=b,
                final=np.maximum(fullm, np.maximum(tmm, tdm)), n=len(wb.circ))


L = [layout(i) for i in range(len(SCENES))]
print("layouts done", [l["n"] for l in L])
TOTAL = L[-1]["t1"] + 1.0  # hold last frame 1s extra


def render_cam(key, cam):
    return cam.render(*BOARDS[key])


def lerp_cam(c0, c1, p):
    (f0, z0, a0), (f1, z1, a1) = c0, c1
    z = math.exp(math.log(z0) * (1 - p) + math.log(z1) * p)
    f = (f0[0] + (f1[0] - f0[0]) * p, f0[1] + (f1[1] - f0[1]) * p)
    a = (a0[0] + (a1[0] - a0[0]) * p, a0[1] + (a1[1] - a0[1]) * p)
    return Cam(f, z, a)


proc = subprocess.Popen(
    ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
     "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", f"{TOTAL:.2f}",
     "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
     "-c:a", "aac", "-b:a", "128k", os.path.join(OUT, "video", "reel_tam-nhin-noi-tru_silent.mp4")], stdin=subprocess.PIPE)

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
        cam = Cam(*ly["cam"])
        rr = render_cam(ly["key"], cam)
        fac = ly["f"]
        a_old = 0.0
        a_main = sm((u - 0.15) / 0.5)
        t_start = 0.0
    else:
        prev = L[i - 1]
        p = sm(u / TRANS)
        cam = lerp_cam(prev["cam"], ly["cam"], p)
        r1 = render_cam(ly["key"], cam)
        if prev["key"] != ly["key"] and p < 1:
            r0 = render_cam(prev["key"], cam)
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
