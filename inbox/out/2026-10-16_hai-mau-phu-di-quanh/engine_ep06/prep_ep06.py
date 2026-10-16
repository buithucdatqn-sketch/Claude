"""Tập 6: tách lớp doodle gốc của ảnh 10 (hai màu ấm đi quanh) thành nền sạch + lớp nét (npz)."""
import sys, numpy as np, cv2
from PIL import Image
OUT = sys.argv[1]
im = Image.open(OUT + "original/10-doodle-hai-mau-am.jpg").convert("RGB")
w, h = im.size
s = 2400 / max(w, h)
im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)  # 1800x2400
im.save(OUT + "source_orig.png")
a = np.array(im)
K = 1.2  # toạ độ đo trên ảnh xem 1500x2000 -> 1800x2400
BOX = dict(  # (x0,y0,x1,y1) trên ảnh xem
    title=(30, 105, 535, 190), credit=(20, 220, 235, 300),
    lab1=(50, 325, 220, 470), arr1=(120, 470, 375, 670),
    lab2=(35, 805, 210, 1000), arr2a=(205, 845, 290, 1210), arr2b=(85, 1000, 195, 1735))
mn = a.min(2)
white = (mn > 205)
mask_all = np.zeros(white.shape, np.uint8)
layer = {}
for k, (x0, y0, x1, y1) in BOX.items():
    m = np.zeros_like(mask_all)
    X0, Y0, X1, Y1 = [int(round(v * K)) for v in (x0, y0, x1, y1)]
    m[Y0:Y1, X0:X1] = white[Y0:Y1, X0:X1]
    mask_all |= m
    ys, xs = np.nonzero(m)
    pts = np.stack([xs, ys], 1).astype(np.float32)
    if k.startswith("arr"):
        o = np.lexsort((pts[:, 0], pts[:, 1]))  # tail (trên) -> head (dưới)
        pts = pts[o]
    layer[k] = pts
    print(k, len(pts))
big = cv2.dilate(mask_all, np.ones((7, 7), np.uint8))
clean = cv2.inpaint(a, big, 5, cv2.INPAINT_TELEA)
Image.fromarray(clean).save(OUT + "source.png")
np.savez_compressed(OUT + "engine_ep06/doodle_ep06.npz", **layer)
