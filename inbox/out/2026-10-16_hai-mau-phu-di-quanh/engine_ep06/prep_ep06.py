"""Tập 6 (nhiều ảnh): với mỗi ảnh doodle trong kho, tạo nền đã xoá doodle (source_NN.png), bản gốc thu nhỏ (source_orig_NN.png)
và lớp nét (doodle_NN.npz: mũi tên theo thứ tự từ đuôi tới đầu, nhãn chữ). Hộp đo trên ảnh xem thu nhỏ (cạnh dài view px)."""
import sys, numpy as np, cv2
from PIL import Image
OUT = sys.argv[1]
# id: (file, độ lớn ảnh xem [w,h], hộp {tên: (x0,y0,x1,y1)}, mũi tên {tên: điểm đuôi}, hộp bỏ đi (tiêu đề, credit))
CFG = {
 "10": ("10-doodle-hai-mau-am.jpg", (1500, 2000),
        dict(lab1=(50, 325, 220, 470), arr1=(120, 470, 375, 670), lab2=(35, 805, 210, 1000),
             arr2a=(205, 845, 290, 1210), arr2b=(85, 1000, 195, 1735)),
        dict(arr1=(130, 485), arr2a=(220, 855), arr2b=(120, 1010)),
        dict(title=(30, 105, 535, 190), credit=(20, 220, 235, 300)), 205, False),
 "13": ("13-doodle-anh-tong.jpg", (750, 1000),
        dict(lab=(588, 722, 735, 780), arr=(515, 688, 592, 752)),
        dict(arr=(585, 735)),
        dict(title=(530, 20, 748, 145), credit=(578, 898, 708, 948)), 225, False),
 "11": ("11-doodle-dap-mau-bep.jpg", (2000, 1500),
        dict(lab_wall=(1610, 35, 1945, 95), lab_same=(1510, 155, 1955, 220), lab_stone=(970, 185, 1365, 240),
             arr_stone=(585, 195, 965, 790), lab_cab=(1050, 1400, 1265, 1455), arr_cab=(590, 1190, 1045, 1430)),
        dict(arr_stone=(955, 205), arr_cab=(1040, 1420)),
        dict(title=(865, 35, 1450, 120), credit=(290, 1420, 955, 1465)), 225, True),
}
for iid, (fn, view, boxes, tails, junk, thr, thin) in CFG.items():
    im = Image.open(OUT + "original/" + fn).convert("RGB")
    w, h = im.size
    s = 2400 / max(w, h)
    im = im.resize((round(w * s), round(h * s)), Image.LANCZOS)
    im.save(OUT + f"source_orig_{iid}.png")
    a = np.array(im)
    K = a.shape[1] / view[0]
    white = (a.min(2) > thr)
    if thin:  # bỏ khối trắng dày (nắp lọ, muối...) chỉ giữ nét mỏng
        k = np.ones((13, 13), np.uint8)
        thick = cv2.morphologyEx(white.astype(np.uint8), cv2.MORPH_OPEN, k)
        white = white & (cv2.dilate(thick, np.ones((5, 5), np.uint8)) == 0)
    mask_all = np.zeros(white.shape, np.uint8)
    layer = {}
    for k_, (x0, y0, x1, y1) in {**boxes, **junk}.items():
        X0, Y0, X1, Y1 = [int(round(v * K)) for v in (x0, y0, x1, y1)]
        m = np.zeros_like(mask_all)
        m[Y0:Y1, X0:X1] = white[Y0:Y1, X0:X1]
        mask_all |= m
        if k_ in junk:
            continue
        ys, xs = np.nonzero(m)
        pts = np.stack([xs, ys], 1).astype(np.float32)
        if k_.startswith("arr"):
            t = np.array(tails[k_], np.float32) * K
            pts = pts[np.argsort(np.hypot(pts[:, 0] - t[0], pts[:, 1] - t[1]))]
        layer[k_] = pts
        print(iid, k_, len(pts))
    big = cv2.dilate(mask_all, np.ones((7, 7), np.uint8))
    Image.fromarray(cv2.inpaint(a, big, 5, cv2.INPAINT_TELEA)).save(OUT + f"source_{iid}.png")
    np.savez_compressed(OUT + f"engine_ep06/doodle_{iid}.npz", **layer)
    dbg = a.copy(); dbg[mask_all > 0] = (255, 0, 0)
    Image.fromarray(dbg).resize((a.shape[1] // 3, a.shape[0] // 3)).save(f"/tmp/claude-0/dbg_{iid}.png")
