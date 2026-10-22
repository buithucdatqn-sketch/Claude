"""Tách lớp doodle gốc (mục 2c) cho tập 10: ảnh 12 (phòng ngủ cô con gái, 1600x2400, đo trên ảnh xem 1334x2000, K=1.2)."""
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


def fill_poly(bg, a, m, box, seed=3):
    """lấp chữ trên tường trát phẳng: khớp mặt đa thức bậc hai từ vùng sạch quanh chữ, thêm hạt nhiễu cùng độ lệch"""
    x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1].astype(np.float64)
    mm = m[y0:y1, x0:x1] > 0
    yy, xx = np.mgrid[y0:y1, x0:x1]
    X = np.stack([np.ones(xx.size), xx.ravel(), yy.ravel(), xx.ravel() ** 2, xx.ravel() * yy.ravel(), yy.ravel() ** 2], 1) / 1.0
    X[:, 1:3] /= 1000.0
    X[:, 3:] /= 1e6
    good = ~mm.ravel()
    rng = np.random.default_rng(seed)
    for c in range(3):
        v = sub[:, :, c].ravel()
        w, *_ = np.linalg.lstsq(X[good], v[good], rcond=None)
        fit = (X @ w).reshape(sub.shape[:2])
        sd = (v[good] - (X[good] @ w)).std()
        out = fit + rng.normal(0, sd * 0.8, fit.shape)
        d = bg[y0:y1, x0:x1, c]
        d[mm] = np.clip(out[mm], 0, 255).astype(np.uint8)


def run(src, dst, npz, K, BOX, ARROWS, extra_thr={}, cols={}, shift={}, fsr={}, clip={}, rows={}, grain=(), noflood=(), thin=(), poly={}, wide=()):
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
        if k not in cols and k not in shift and k not in fsr and k not in rows and k not in thin:
            big |= cv2.dilate(parts[k], np.ones((19, 19), np.uint8))
    for k in wide:
        big |= cv2.dilate(parts[k], np.ones((25, 25), np.uint8))
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
    for k, box in poly.items():
        d = cv2.dilate(parts[k], np.ones((21, 21), np.uint8))
        fill_poly(bg, a, d, box)
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
    np.savez(OUT + "engine_ep10/" + npz, **layers)
    for k, v in layers.items():
        print(npz, k, v.shape, v.min(0).astype(int), v.max(0).astype(int))


# ảnh 12: phòng ngủ cô con gái (kệ gỗ teak, tường vôi, sàn terrazzo ô nhỏ)
run("source_ph_orig.png", "source_ph.png", "doodle_ep10_ph.npz", 1.2,
    BOX=dict(title=(28, 28, 600, 104), lab_top=(20, 172, 325, 342),
             lab_ke=(20, 608, 428, 715), arr_ke=(215, 725, 352, 1205),
             lab_san=(88, 1328, 498, 1448), arr_san=(498, 1368, 812, 1768),
             credit=(32, 1630, 748, 1684)),
    ARROWS=dict(arr_ke=(226, 735), arr_san=(506, 1376)),
    extra_thr=dict(title=215, lab_top=215, lab_ke=215, lab_san=185, arr_ke=215, arr_san=215, credit=200),
    grain=("title", "lab_top", "lab_ke", "arr_ke", "credit"),
    thin=("arr_san",), wide=("lab_san",))
