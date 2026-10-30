"""Tập 17 (chép từ engine/mau_tap7/sketch_layers.py). Tách nét của một sơ đồ (sketch) để engine vẽ dần trên nền trắng (chế độ SKETCH của engine_video.py, engine_storyboard_v7.py).
Chủ Trang yêu cầu 2026-10-30: cảnh dùng sơ đồ phải là các nét vẽ từ từ xuất hiện theo thứ tự vẽ trên nền trắng,
không phải dán hình lên nền trắng.

Cách làm: mực = điểm ảnh đủ tối hoặc đủ rực so với giấy trắng. Mực được nối thành từng cụm (nét, chữ, mảng gạch) bằng
phép giãn nhẹ, mỗi cụm thuộc một nhóm theo khung GROUPS (toạ độ ảnh làm việc). Trong mỗi nhóm: các nét dài (khung, đường
phối cảnh) vẽ trước, rồi các cụm nhỏ theo thứ tự đọc (trên xuống, trái sang). Trong mỗi cụm, điểm sắp theo khoảng cách
đi dọc nét (BFS từ đầu nét), nên nét "chạy" như ngòi bút. Lưu npz: mỗi nhóm một khoá, mảng điểm (x, y) theo thứ tự vẽ.

Dùng: chép thành OUT/engine_epNN/sketch_epNN.py, sửa JOBS, chạy python3 -I sketch_epNN.py <OUT>.
Trong gen_epNN.py: ảnh sơ đồ khai báo sketch=True trong IMGS; cảnh dùng dd=[nhóm vẽ trong cảnh], keep=[nhóm đã vẽ ở cảnh trước]."""
import os, sys
from collections import deque
import numpy as np
import cv2
from PIL import Image

OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "./") + "/"
HERE = os.path.dirname(os.path.abspath(__file__))


def ink_mask(a, dark=200, sat=60):
    """mực: kênh nhỏ nhất < dark (nét đen, xám) hoặc chênh kênh > sat (nét màu)"""
    a = a.astype(np.int16)
    return (a.min(2) < dark) | ((a.max(2) - a.min(2)) > sat)


def order_component(ys, xs):
    """sắp điểm của một cụm theo đường đi BFS từ điểm trên-trái nhất (nét chạy liền như ngòi bút)"""
    pts = set(zip(xs.tolist(), ys.tolist()))
    start = min(pts, key=lambda p: (p[0] + p[1], p[1]))
    seen, out, q = {start}, [], deque([start])
    while pts:
        while q:
            x, y = q.popleft()
            out.append((x, y))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    n = (x + dx, y + dy)
                    if n in pts and n not in seen:
                        seen.add(n)
                        q.append(n)
        pts -= seen
        if pts:   # phần rời của cụm (nét đứt): đi tiếp từ điểm gần nhất
            lx, ly = out[-1]
            nxt = min(pts, key=lambda p: abs(p[0] - lx) + abs(p[1] - ly))
            seen.add(nxt)
            q.append(nxt)
    return out


def run(src, npz, groups, join=3, dark=200, sat=60, long_frac=0.35):
    a = np.array(Image.open(src).convert("RGB"))
    H, W = a.shape[:2]
    m = ink_mask(a, dark, sat).astype(np.uint8)
    lab_n, lab = cv2.connectedComponents(cv2.dilate(m, np.ones((join, join), np.uint8)), connectivity=8)
    comps = []
    for k in range(1, lab_n):
        ys, xs = np.nonzero((lab == k) & (m > 0))
        if len(ys) < 4:
            continue
        cx, cy = xs.mean(), ys.mean()
        g = next((name for name, (x0, y0, x1, y1) in groups if x0 <= cx < x1 and y0 <= cy < y1), None)
        if g is None:
            continue
        diag = np.hypot(xs.max() - xs.min(), ys.max() - ys.min())
        comps.append((g, 0 if diag > long_frac * min(W, H) else 1, int(cy // 40), cx, ys, xs))
    layers = {}
    for name, _ in groups:
        cs = sorted([c for c in comps if c[0] == name], key=lambda c: (c[1], c[2], c[3]))
        pts = []
        for c in cs:
            pts += order_component(c[4], c[5])
        layers[name] = np.array(pts, np.float32).reshape(-1, 2)
    np.savez(npz, **layers)
    prev = np.full_like(a, 255)
    allm = np.zeros((H, W), bool)
    for v in layers.values():
        v = v.astype(int)
        allm[v[:, 1], v[:, 0]] = True
    prev[allm] = a[allm]
    Image.fromarray(prev).save(os.path.splitext(npz)[0] + "_preview.png")
    print(os.path.basename(npz), {k: len(v) for k, v in layers.items()}, "mực bỏ sót:", int((m > 0).sum() - allm.sum()))


# ---- mỗi tập sửa khối này: (ảnh làm việc, npz ra, [(nhóm, (x0, y0, x1, y1)), ...] theo thứ tự vẽ) ----
JOBS = [("source_d31.png", "sketch_ep17_d31.npz", [
    ("trai", (0, 14, 378, 450)), ("lab_trai", (0, 450, 378, 535)),        # hành lang trái: tường cuối sáng
    ("phai", (378, 14, 756, 450)), ("lab_phai", (378, 450, 756, 535)),   # hành lang phải: tường cuối tối hơn, vòng cam
    # dòng "chênh khoảng 6,8 cm [TN]" cắt khỏi ảnh (chạm dòng credit; phụ đề đã nói con số, nhãn [TN] không dùng theo mục 0.6f)
])]
for src_, npz_, groups_ in JOBS:
    run(OUT + src_, os.path.join(HERE, npz_), groups_)
