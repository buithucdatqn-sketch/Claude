"""Tách lớp doodle gốc của ảnh 12 (mục 2c): source_orig.png (còn nét), source.png (nền đã xoá nét), doodle_ep06.npz"""
import sys, collections
import numpy as np, cv2
from PIL import Image
OUT = sys.argv[1]
im = Image.open(OUT + "original/12-doodle-cung-mau-khac-be-mat.jpg").convert("RGB")
im = im.resize((1800, 2400), Image.LANCZOS)
im.save(OUT + "source_orig.png")
a = np.array(im)
K = 1.2  # toạ độ xem thu nhỏ 1500x2000 -> 1800x2400
BOX = dict(  # (x0,y0,x1,y1) theo ảnh xem 1500x2000
    title=(930, 25, 1500, 110), sub=(930, 135, 1470, 215),
    lab1=(1200, 440, 1460, 560), arr1=(915, 470, 1205, 670),
    arr2=(435, 1585, 862, 1870), lab2=(862, 1800, 1110, 1920),
    credit=(1200, 1860, 1470, 1965))
mn = a.min(2)
mask = np.zeros(mn.shape, np.uint8)
parts = {}
for k, (x0, y0, x1, y1) in BOX.items():
    m = np.zeros_like(mask)
    X0, Y0, X1, Y1 = [int(round(v * K)) for v in (x0, y0, x1, y1)]
    thr = 195 if k == 'arr2' else 140   # arr2 nằm trên nan tủ sáng; chữ nằm trên nền xanh tối
    m[Y0:Y1, X0:X1] = (mn[Y0:Y1, X0:X1] > thr)
    parts[k] = m
    mask |= m
big = cv2.dilate(mask, np.ones((9, 9), np.uint8))
# nền có cấu trúc dọc (nan tủ, khe ván tường): lấp theo cột, nội suy giữa điểm sạch trên và dưới
bg = a.copy()
H = big.shape[0]
for x in np.nonzero(big.any(0))[0]:
    col = big[:, x] > 0
    good = np.nonzero(~col)[0]
    for c in range(3):
        bg[:, x, c] = np.interp(np.arange(H), good, a[good, x, c]).astype(np.uint8)
Image.fromarray(bg).save(OUT + "source.png")

def order_from(m, start):
    ys, xs = np.nonzero(m)
    pts = set(zip(xs.tolist(), ys.tolist()))
    s = min(pts, key=lambda p: (p[0]-start[0])**2 + (p[1]-start[1])**2)
    dist = {s: 0}; q = collections.deque([s])
    while q:
        x, y = q.popleft()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                n = (x+dx, y+dy)
                if n in pts and n not in dist:
                    dist[n] = dist[(x, y)] + 1; q.append(n)
    rest = [p for p in pts if p not in dist]
    return np.array(sorted(dist, key=dist.get) + rest, np.float32)

layers = {}
layers["arr1"] = order_from(parts["arr1"], (1195*K, 490*K))     # đuôi mũi tên 1
layers["arr2"] = order_from(parts["arr2"], (855*K, 1848*K))     # đuôi mũi tên 2
for k in ("lab1", "lab2", "sub"):
    ys, xs = np.nonzero(parts[k]); layers[k] = np.stack([xs, ys], 1).astype(np.float32)
np.savez(OUT + "engine_ep06/doodle_ep06.npz", **layers)
for k, v in layers.items(): print(k, v.shape, v.min(0), v.max(0))
