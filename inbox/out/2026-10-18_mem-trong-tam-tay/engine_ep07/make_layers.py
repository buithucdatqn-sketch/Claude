"""Tách lớp doodle gốc (mục 2c) cho tập 7.
Ảnh chính 08 (phòng khách, 1600x2400): source_orig.png -> source.png (nền đã xoá nét) + engine_ep07/doodle_ep07.npz
Ảnh phụ 09 (phòng ngủ, 2400x1602): source_ngu_orig.png -> source_ngu.png + engine_ep07/doodle_ep07_ngu.npz
Toạ độ BOX đo trên ảnh xem thu nhỏ (08: 1000x1500, 09: 1500x1001), nhân K sang ảnh làm việc."""
import sys, collections
import numpy as np, cv2
from PIL import Image
OUT = sys.argv[1] if len(sys.argv) > 1 else "./"


def order_from(m, start):
    """sắp điểm của nét theo khoảng cách loang từ đuôi nét, để lộ dần từ đuôi tới đầu mũi tên"""
    ys, xs = np.nonzero(m)
    pts = set(zip(xs.tolist(), ys.tolist()))
    s = min(pts, key=lambda p: (p[0] - start[0]) ** 2 + (p[1] - start[1]) ** 2)
    dist = {s: 0}
    q = collections.deque([s])
    while q:
        x, y = q.popleft()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                n = (x + dx, y + dy)
                if n in pts and n not in dist:
                    dist[n] = dist[(x, y)] + 1
                    q.append(n)
    rest = [p for p in pts if p not in dist]
    return np.array(sorted(dist, key=dist.get) + rest, np.float32)


def flood(white, seed):
    """giữ thành phần liên thông chứa điểm gần seed nhất (mũi tên vẽ trên nền có đốm trắng)"""
    n, lab = cv2.connectedComponents(white, connectivity=8)
    ys, xs = np.nonzero(white)
    k = np.argmin((xs - seed[0]) ** 2 + (ys - seed[1]) ** 2)
    return (lab == lab[ys[k], xs[k]]).astype(np.uint8)


def fill_cols(bg, a, m):
    """lấp theo cột (nền có vân dọc như thớ gỗ): nội suy giữa điểm sạch trên và dưới"""
    H = m.shape[0]
    for x in np.nonzero(m.any(0))[0]:
        col = m[:, x] > 0
        good = np.nonzero(~col)[0]
        for c in range(3):
            bg[col, x, c] = np.interp(np.nonzero(col)[0], good, a[good, x, c]).astype(np.uint8)


def fill_grain(bg, a, m, avoid, r=20, tol=24, seed=7):
    """lấp giữ vân hạt (vải xù, bê tông): mỗi điểm trong nét lấy màu một điểm sạch ngẫu nhiên gần đó.
    Điểm lấy mẫu phải nằm ngoài vùng avoid (nét + quầng sáng) và gần màu ước lượng trơn (TELEA) tại chỗ đó,
    để không bê màu đồ vật bên cạnh (cột giường, khung tranh) vào nền."""
    rng = np.random.default_rng(seed)
    smooth = cv2.inpaint(a, (m | avoid) * 255, 9, cv2.INPAINT_TELEA).astype(np.int16)
    ys, xs = np.nonzero(m)
    sy, sx = ys.copy(), xs.copy()
    todo = np.ones(len(ys), bool)
    for it in range(200):
        if not todo.any():
            break
        n = todo.sum()
        rr = r if it < 120 else 2 * r
        ty = np.clip(ys[todo] + rng.integers(-rr, rr + 1, n), 0, a.shape[0] - 1)
        tx = np.clip(xs[todo] + rng.integers(-rr, rr + 1, n), 0, a.shape[1] - 1)
        ok = avoid[ty, tx] == 0
        diff = np.abs(a[ty, tx].astype(np.int16) - smooth[ys[todo], xs[todo]]).max(1)
        ok &= diff < (tol if it < 150 else 3 * tol)
        idx = np.nonzero(todo)[0][ok]
        sy[idx], sx[idx] = ty[ok], tx[ok]
        todo[idx] = False
    bg[ys, xs] = np.where(todo[:, None], smooth[ys, xs], a[sy, sx]).astype(np.uint8)


def fill_rows(bg, a, m):
    """lấp theo hàng (ván gỗ nằm ngang): nội suy giữa điểm sạch bên trái và bên phải"""
    Wd = m.shape[1]
    for y in np.nonzero(m.any(1))[0]:
        row = m[y] > 0
        good = np.nonzero(~row)[0]
        for c in range(3):
            bg[y, row, c] = np.interp(np.nonzero(row)[0], good, a[y, good, c]).astype(np.uint8)


def fill_shift(bg, a, m, dy, x_min=0):
    """lấp bằng vân lấy từ chỗ lệch dy px (vải xù, giữ được hạt vải thay vì làm nhoè)"""
    ys, xs = np.nonzero(m)
    keep = xs >= x_min           # phần nằm ngoài vải (mép kính, sàn) để inpaint lo
    ys, xs = ys[keep], xs[keep]
    sy = np.clip(ys + dy, 0, a.shape[0] - 1)
    bad = m[sy, xs] > 0          # chỗ lấy mẫu còn dính nét: lấy phía ngược lại
    sy[bad] = np.clip(ys[bad] - dy, 0, a.shape[0] - 1)
    bg[ys, xs] = a[sy, xs]


def run(src, dst, npz, K, BOX, ARROWS, extra_thr={}, cols={}, shift={}, fsr={}, clip={}, rows={}, grain=(), noflood=()):
    a = np.array(Image.open(OUT + src).convert("RGB"))
    mn = a.min(2)
    parts, mask = {}, np.zeros(mn.shape, np.uint8)
    for k, (x0, y0, x1, y1) in BOX.items():
        X0, Y0, X1, Y1 = [int(round(v * K)) for v in (x0, y0, x1, y1)]
        m = np.zeros_like(mask)
        thr = extra_thr.get(k, 150)
        m[Y0:Y1, X0:X1] = mn[Y0:Y1, X0:X1] > thr
        if k in ARROWS and k not in noflood:  # mũi tên đi qua nền sáng/đốm: chỉ giữ phần nối với đuôi
            m = flood(m, (ARROWS[k][0] * K, ARROWS[k][1] * K))
        if k not in ARROWS:  # nhãn chữ: bỏ đốm sáng lẻ của nền (vài px), giữ dấu tiếng Việt
            n, lab, st, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
            for j in range(1, n):
                if st[j, 4] < 6:
                    m[lab == j] = 0
        if k in clip:  # bỏ phần mặt nạ dính vào đồ trắng thật (công tắc đèn)
            m[:, :clip[k]] = 0
        parts[k] = m
        mask |= m
    big = cv2.dilate(mask, np.ones((9, 9), np.uint8))
    for k in ARROWS:  # mũi tên lấy ngưỡng cao (chỉ lõi nét) nên quầng mờ rộng hơn: nới mặt nạ thêm
        if k not in cols and k not in shift and k not in fsr and k not in rows:
            big |= cv2.dilate(parts[k], np.ones((19, 19), np.uint8))
    special = np.zeros_like(mask)
    for k in list(cols) + list(shift) + list(fsr):
        d = cv2.dilate(parts[k], np.ones((13, 13), np.uint8))
        if k in cols:
            x0_, x1_ = cols[k]
            d[:, :x0_] = 0
            d[:, x1_:] = 0
        if k in shift:
            d[:, :shift[k][1]] = 0
        if k in fsr:
            d[:, :fsr[k]] = 0
        special |= d
    bg = cv2.inpaint(a, (big & (1 - special)) * 255, 6, cv2.INPAINT_TELEA)
    for k, (x0_, x1_) in cols.items():
        d = cv2.dilate(parts[k], np.ones((13, 13), np.uint8))
        d[:, :x0_] = 0
        d[:, x1_:] = 0
        fill_cols(bg, a, d)
    for k, dy in shift.items():
        fill_shift(bg, a, cv2.dilate(parts[k], np.ones((13, 13), np.uint8)), *dy)
    for k, x_min in fsr.items():
        d = cv2.dilate(parts[k], np.ones((13, 13), np.uint8))
        d[:, :x_min] = 0
        fill_grain(bg, a, d, cv2.dilate(mask, np.ones((15, 15), np.uint8)))
    for k, (y0_, y1_) in rows.items():
        d = cv2.dilate(parts[k], np.ones((13, 13), np.uint8))
        d[:y0_] = 0
        d[y1_:] = 0
        fill_rows(bg, a, d)
        special |= d
    for k in grain:  # vân bê tông dạng hạt: lấy mẫu ngẫu nhiên quanh nét, không để mảng nhoè
        d = cv2.dilate(parts[k], np.ones((19, 19) if k in ARROWS else (11, 11), np.uint8))
        for k2, (y0_, y1_) in rows.items():
            if k2 == k:
                d[y0_:y1_] = 0
        if k in cols:
            d[:, cols[k][0]:cols[k][1]] = 0
        fill_grain(bg, a, d, cv2.dilate(mask, np.ones((15, 15), np.uint8)))
        special |= d
    big |= special
    Image.fromarray(bg).save(OUT + dst)
    layers = {}
    for k, m in parts.items():
        if k in ARROWS:
            layers[k] = order_from(m, (ARROWS[k][0] * K, ARROWS[k][1] * K))
        else:
            ys, xs = np.nonzero(m)
            layers[k] = np.stack([xs, ys], 1).astype(np.float32)
    np.savez(OUT + "engine_ep07/" + npz, **layers)
    for k, v in layers.items():
        print(npz, k, v.shape, v.min(0).astype(int), v.max(0).astype(int))


# ảnh 08: phòng khách
run("source_orig.png", "source.png", "doodle_ep07.npz", 1.6,
    BOX=dict(credit=(425, 12, 962, 44), title=(28, 192, 702, 262), sub=(585, 308, 978, 352),
             lab_vo=(665, 452, 978, 530), arr_vo=(812, 505, 852, 550),
             lab_teak=(14, 605, 200, 648), arr_teak=(198, 612, 252, 682),
             lab_sofa=(34, 998, 122, 1108), arr_sofa=(110, 1028, 308, 1088)),
    ARROWS=dict(arr_teak=(203, 618), arr_sofa=(117, 1043), arr_vo=(818, 540)),
    extra_thr=dict(arr_sofa=238, arr_teak=200, arr_vo=200),
    cols=dict(arr_teak=(0, 1600)), fsr=dict(arr_sofa=238))  # x mép trái của vải sofa; phần đuôi trên kính để inpaint

# ảnh 09: phòng ngủ (ảnh phụ cho cảnh phòng ngủ)
run("source_ngu_orig.png", "source_ngu.png", "doodle_ep07_ngu.npz", 1.6,
    BOX=dict(title=(18, 38, 534, 104), sub=(638, 68, 958, 146), credit=(505, 956, 1006, 982),
             lab_dau=(580, 358, 710, 432), arr_dau=(530, 380, 576, 507),
             lab_tu=(758, 728, 884, 806), arr_tu=(889, 604, 1093, 766)),
    ARROWS=dict(arr_dau=(566, 387), arr_tu=(896, 759)),
    extra_thr=dict(arr_dau=200, arr_tu=200, credit=170),
    cols=dict(arr_tu=(int(996 * 1.6), 2400), arr_dau=(878, 908)),  # tủ gỗ vân dọc và cột giường: lấp theo cột
    clip=dict(arr_dau=846), noflood=("arr_dau",),
    rows=dict(arr_dau=(int(452 * 1.6), 1602)),  # ván gỗ đầu giường nằm ngang: lấp theo hàng
    grain=("title", "sub", "lab_dau", "arr_dau"))  # chữ và mũi tên trên tường bê tông

# ảnh 13: ảnh tổng (sảnh ăn hai tầng nhìn từ bàn ăn) — cảnh mở và cảnh chốt
run("source_tong_orig.png", "source_tong.png", "doodle_ep07_tong.npz", 1.6,
    BOX=dict(title=(52, 28, 378, 274), credit=(452, 972, 698, 1042),
             lab_xa=(303, 413, 532, 522), arr_xa=(398, 522, 482, 712),
             lab_tam=(13, 848, 302, 917), arr_tam1=(33, 917, 137, 1262), arr_tam2=(163, 919, 337, 1152)),
    ARROWS=dict(arr_xa=(410, 535), arr_tam1=(50, 925), arr_tam2=(172, 932)),
    extra_thr=dict(title=200, arr_xa=205, arr_tam1=215, arr_tam2=215, credit=190),
    grain=("title", "lab_xa", "arr_xa"))

# ảnh 06: sảnh ăn hai tầng — chỉ dùng nền sạch (nhãn gốc nói về ánh sáng, không hợp lời đọc)
run("source_an_orig.png", "source_an.png", "doodle_ep07_an.npz", 2.4,
    BOX=dict(lab1=(18, 33, 212, 92), arr1=(102, 93, 158, 248), title=(683, 33, 982, 77), sub=(746, 103, 937, 132),
             lab2=(238, 870, 392, 932), arr2=(266, 850, 320, 872), plus1=(186, 826, 217, 854), plus2=(763, 864, 797, 895),
             credit=(603, 955, 962, 978)),
    ARROWS=dict(arr1=(110, 100), arr2=(316, 862)),
    extra_thr=dict(arr1=200, arr2=200, plus1=200, plus2=200, lab2=200, credit=190),
    grain=("lab1", "arr1", "title", "sub", "lab2", "arr2", "plus1", "plus2", "credit"))

# ảnh 11: hành lang lối vào — chỉ dùng nền sạch
run("source_hl_orig.png", "source_hl.png", "doodle_ep07_hl.npz", 1.6,
    BOX=dict(credit=(556, 18, 828, 64), title=(43, 123, 562, 182), sub=(153, 228, 542, 272),
             lab1=(143, 343, 507, 417), arr1=(483, 368, 527, 667), lab2=(233, 1338, 517, 1412), arr2=(283, 958, 382, 1322)),
    ARROWS=dict(arr1=(510, 378), arr2=(375, 1312)),
    extra_thr=dict(arr1=200, arr2=243, lab2=200),
    grain=("credit", "title", "sub", "lab1", "arr1", "lab2", "arr2"))
