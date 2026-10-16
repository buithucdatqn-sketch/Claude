"""Tách lớp doodle gốc của ảnh 11 (bếp): source_bep.png (nền đã xoá nét), doodle_ep06_bep.npz.
Mũi tên đi qua lọ, kệ đá nên tách bằng loang (BFS) theo điểm trắng nối với đuôi mũi tên, rồi inpaint TELEA;
chữ nằm trên tường sơn và tủ trơn nên lấp theo cột như ảnh 12."""
import sys, collections
import numpy as np, cv2
from PIL import Image
OUT = sys.argv[1]
a = np.array(Image.open(OUT + "source_bep_orig.png").convert("RGB"))
mn, mx = a.min(2).astype(int), a.max(2).astype(int)
K = 1.2  # ảnh xem 2000x1500 -> ảnh làm việc 2400x1800
TEXT = dict(title=(860, 40, 1450, 115), tuong=(1605, 35, 1945, 92), cungho=(1505, 155, 1955, 215),
            lab1=(970, 185, 1365, 240), lab2=(1050, 1400, 1262, 1455), credit=(290, 1425, 950, 1462))
ARR = dict(arr1=((955, 205), (560, 180, 965, 790)), arr2=((1035, 1418), (590, 1190, 1045, 1425)))

def box(b):
    return [int(round(v * K)) for v in b]

parts = {}
for k, b in TEXT.items():
    X0, Y0, X1, Y1 = box(b)
    m = np.zeros(mn.shape, np.uint8)
    m[Y0:Y1, X0:X1] = (mn[Y0:Y1, X0:X1] > 150)
    parts[k] = m

def trace(tail, b):
    X0, Y0, X1, Y1 = box(b)
    ok = np.zeros(mn.shape, bool)
    ok[Y0:Y1, X0:X1] = (mn[Y0:Y1, X0:X1] > 200) & ((mx - mn)[Y0:Y1, X0:X1] < 40)
    tx, ty = tail[0] * K, tail[1] * K
    ys, xs = np.nonzero(ok)
    j = np.argmin((xs - tx) ** 2 + (ys - ty) ** 2)
    s = (int(xs[j]), int(ys[j]))
    dist = {s: 0}; q = collections.deque([s])
    while q:
        x, y = q.popleft()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                n = (x + dx, y + dy)
                if X0 <= n[0] < X1 and Y0 <= n[1] < Y1 and ok[n[1], n[0]] and n not in dist:
                    dist[n] = dist[(x, y)] + 1; q.append(n)
    pts = sorted(dist, key=dist.get)
    m = np.zeros(mn.shape, np.uint8)
    for x, y in pts:
        m[y, x] = 1
    return m, np.array(pts, np.float32)

layers = {}
for k, (tail, b) in ARR.items():
    parts[k], layers[k] = trace(tail, b)

bg = a.copy()
# chữ: lấp theo cột
tm = np.zeros(mn.shape, np.uint8)
for k in TEXT:
    tm |= parts[k]
tm = cv2.dilate(tm, np.ones((9, 9), np.uint8))
H = tm.shape[0]
for x in np.nonzero(tm.any(0))[0]:
    col = tm[:, x] > 0
    good = np.nonzero(~col)[0]
    for c in range(3):
        v = np.interp(np.arange(H), good, a[good, x, c])
        bg[col, x, c] = v[col].astype(np.uint8)
# mũi tên: inpaint
am = cv2.dilate(parts["arr1"] | parts["arr2"], np.ones((7, 7), np.uint8))
bg = cv2.inpaint(bg, am, 4, cv2.INPAINT_TELEA)
Image.fromarray(bg).save(OUT + "source_bep.png")
for k in ("lab1", "lab2"):
    ys, xs = np.nonzero(parts[k]); layers[k] = np.stack([xs, ys], 1).astype(np.float32)
np.savez(OUT + "engine_ep06/doodle_ep06_bep.npz", **layers)
for k, v in layers.items():
    print(k, v.shape, v.min(0), v.max(0))
