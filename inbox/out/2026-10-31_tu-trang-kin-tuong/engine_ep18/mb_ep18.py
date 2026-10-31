"""Tập 18: thêm nét cam khoanh dãy tủ bếp lên mặt bằng vị trí chụp của bài (anh/vi-tri-chup/07, đã xoá nhãn "ảnh 03" lệch số),
vẽ thẳng vào ảnh làm việc source_mb.png (màu cam của nét vị trí chụp) và thêm nhóm "tu" (điểm theo thứ tự vẽ) vào sketch_ep18_mb.npz,
để engine SKETCH vẽ dần nét cam sau mặt bằng. Chạy sau sketch_ep18.py: python3 -I mb_ep18.py <OUT>"""
import os, sys
import numpy as np
from PIL import Image
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "./") + "/"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.argv = [sys.argv[0], OUT]
import importlib.util
spec = importlib.util.spec_from_file_location("dr", os.path.join(HERE, "draw_ep18.py"))
dr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dr)          # chỉ dùng các hàm nét tay (poly, label); draw_ep18 ghi lại npz ảnh chụp, không ảnh hưởng
ORANGE = (205, 82, 45)
w = 4
pts = dr.poly([(168, 110), (572, 106), (574, 170), (168, 172)], w, (5.5 * w, 3.5 * w), 0.8, 11)
pts += dr.label("dãy tủ chạy trọn bức tường", (170, 40), 34)
a = np.array(Image.open(OUT + "source_mb_base.png").convert("RGB"))
P = np.array(pts)
ok = (P[:, 0] >= 0) & (P[:, 0] < a.shape[1]) & (P[:, 1] >= 0) & (P[:, 1] < a.shape[0])
P = P[ok]
a[P[:, 1], P[:, 0]] = ORANGE
Image.fromarray(a).save(OUT + "source_mb.png")
z = dict(np.load(os.path.join(HERE, "sketch_ep18_mb.npz")))
z["tu"] = P.astype(np.float32)
np.savez(os.path.join(HERE, "sketch_ep18_mb.npz"), **z)
print("mb", {k: len(v) for k, v in z.items()})
