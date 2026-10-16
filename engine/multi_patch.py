"""Vá hai engine gốc (engine_storyboard_v7.py, engine_video.py) để một reel dùng NHIỀU ảnh.
Mỗi cảnh có trường img (id ảnh); ảnh nằm trong <thư_mục_ảnh>/source_<id>.png. Hình học thẻ ảnh (dọc/ngang) tính lại theo từng ảnh
bằng use_image(). Chuyển giữa hai ảnh khác nhau trong video là chuyển mờ 0,7 giây; cùng ảnh thì camera nội suy như cũ.
Chế độ mực (ink=True trong cảnh): cảnh dùng sơ đồ/mặt bằng/trục đo nền trắng: toàn khung coi như nền giấy nên nét và chữ vẽ bằng mực nâu đậm (không phủ tối trên/dưới), nét mới vẽ bằng Brush (ellipse/arrow) từ dd.
Mỗi cảnh có thể có credit riêng (trường credit), mặc định là CREDIT.
Dùng: patch(source_text, video=bool, ids=["10", "13"], data_block=str) -> text engine mới (gen_epNN.py gọi hàm này)."""


def _rep(s, a, b):
    assert a in s, a[:80]
    return s.replace(a, b)


GEOM = '''IMG_IDS = %(ids)r
IMG = {i: Image.open(os.path.join(SRC_DIR, "source_%%s.png" %% i)).convert("RGB") for i in IMG_IDS}

# ---------------- board geometry (2x master, 1x = reel canvas); tính lại cho từng ảnh bằng use_image ----------------
B2W, B2H = W * 2, H * 2
ANGLE = 1.2  # degrees, counter-clockwise (card is hung very slightly crooked)
CUR = None


def use_image(i):
    """chọn ảnh hiện hành: đặt lại src, kích thước và hình học thẻ (ảnh dọc: thẻ hẹp 1440, hạ tâm; ảnh ngang: thẻ 1920)"""
    global CUR, src, SW, SH, CARD_W2, BORDER2, PH_W2, PH_H2, CARD_H2, C2, S2, ROT, CARD_TOP1, CARD_BOT1
    CUR = i
    src = IMG[i]
    SW, SH = src.size
    BORDER2 = 0
    CARD_W2, C2 = (1440, (B2W / 2, 1880.0)) if SH > SW else (1920, (B2W / 2, 1810.0))
    PH_W2 = CARD_W2 - 2 * BORDER2
    PH_H2 = int(round(PH_W2 * SH / SW))
    CARD_H2 = PH_H2 + 2 * BORDER2
    S2 = PH_W2 / SW
    ROT = cv2.getRotationMatrix2D(C2, ANGLE, 1.0)
    CARD_TOP1, CARD_BOT1 = (C2[1] - CARD_H2 / 2) / 2, (C2[1] + CARD_H2 / 2) / 2


use_image(IMG_IDS[0])
CREDIT_CUR = [CREDIT]  # credit của cảnh đang dựng (cảnh có thể đặt credit riêng)


'''


def patch(s, video, ids, data_block):
    s = _rep(s, 'SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "source.png")',
             'SRC_DIR = sys.argv[1] if len(sys.argv) > 1 else HERE  # thư mục chứa source_<id>.png')
    s = _rep(s, 't.d.textlength(CREDIT, font=F(s))', 't.d.textlength(CREDIT_CUR[0], font=F(s))')
    s = _rep(s, 't.put(xy, CREDIT, s, fill, anchor)', 't.put(xy, CREDIT_CUR[0], s, fill, anchor)')
    a, b = s.index('src = Image.open(SRC)'), s.index('def src_to_b2')
    s = s[:a] + GEOM % dict(ids=ids) + s[b:]
    a = s.index('# ---------------- scenes')
    b = s.index('BOARDS["plain"] = make_board(1.0)') if video else s.index('def render_scene')
    s = s[:a] + data_block + s[b:]
    boards = ('for _i in IMG_IDS:\n    use_image(_i)\n    BOARDS[(_i, "plain")] = make_board(1.0)\n'
              '    BOARDS[(_i, "dark")] = make_board(0.86)\n    BOARDS[(_i, "clean")] = BOARDS[(_i, "plain")]\n')
    if video:
        s = _rep(s, 'BOARDS["plain"] = make_board(1.0)\nBOARDS["dark"] = make_board(0.86)\nBOARDS["clean"] = BOARDS["plain"]\n', boards)
        s = _rep(s, '    sc = SCENES[i]\n    cam = Cam(*sc["cam"])\n    key = "dark" if', '    sc = SCENES[i]\n    use_image(sc["img"])\n    CREDIT_CUR[0] = sc.get("credit", CREDIT)\n    cam = Cam(*sc["cam"])\n    key = "dark" if')
        s = _rep(s, '        st, sb = not title_on_fabric, not vo_on_fabric', '        st, sb = not title_on_fabric and not sc.get("ink"), not vo_on_fabric and not sc.get("ink")')
        s = _rep(s, '    base, fabm = rr[..., :3] * fac, 1.0 - np.clip(rr[..., 3] / 255.0, 0, 1)\n',
                 '    base, fabm = rr[..., :3] * fac, 1.0 - np.clip(rr[..., 3] / 255.0, 0, 1)\n'
                 '    pi = (1.0 if i and L[i - 1]["sc"].get("ink") else 0.0) * (1 - p) + (1.0 if ly["sc"].get("ink") else 0.0) * p\n'
                 '    fabm = fabm * (1 - pi) + pi  # cảnh mực: cả khung là nền giấy, nét và chữ màu mực\n')
        s = _rep(s, 'return dict(sc=sc, cam=sc["cam"], key=key,', 'return dict(sc=sc, img=sc["img"], cam=sc["cam"], key=key,')
        s = _rep(s, '        cam = Cam(*ly["cam"])\n        rr = render_cam(ly["key"], cam)\n',
                 '        use_image(ly["img"])\n        cam = Cam(*ly["cam"])\n        rr = render_cam((ly["img"], ly["key"]), cam)\n')
        old = ('        cam = lerp_cam(prev["cam"], ly["cam"], p)\n        r1 = render_cam(ly["key"], cam)\n'
               '        if prev["key"] != ly["key"] and p < 1:\n            r0 = render_cam(prev["key"], cam)\n'
               '            rr = r0 * (1 - p) + r1 * p\n        else:\n            rr = r1\n')
        new = ('        if prev["img"] != ly["img"]:  # ảnh khác: chuyển mờ giữa cảnh cuối của ảnh cũ và cảnh đầu của ảnh mới\n'
               '            use_image(ly["img"])\n            r1 = render_cam((ly["img"], ly["key"]), Cam(*ly["cam"]))\n'
               '            if p < 1:\n                use_image(prev["img"])\n'
               '                r0 = render_cam((prev["img"], prev["key"]), Cam(*prev["cam"]))\n'
               '                rr = r0 * (1 - p) + r1 * p\n            else:\n                rr = r1\n'
               '        else:\n            use_image(ly["img"])\n            cam = lerp_cam(prev["cam"], ly["cam"], p)\n'
               '            r1 = render_cam((ly["img"], ly["key"]), cam)\n'
               '            if prev["key"] != ly["key"] and p < 1:\n                r0 = render_cam((ly["img"], prev["key"]), cam)\n'
               '                rr = r0 * (1 - p) + r1 * p\n            else:\n                rr = r1\n')
        s = _rep(s, old, new)
    else:
        s = _rep(s, 'BOARDS["plain"] = make_board(1.0)\nBOARDS["dark"] = make_board(0.86)\nBOARDS["clean"] = make_board(1.0)\n', boards)
        s = _rep(s, '    sc = SCENES[i]\n    cam = Cam(*sc["cam"])\n', '    sc = SCENES[i]\n    use_image(sc["img"])\n    CREDIT_CUR[0] = sc.get("credit", CREDIT)\n    cam = Cam(*sc["cam"])\n')
        s = _rep(s, '    base, fabm = rr[..., :3], 1.0 - np.clip(rr[..., 3] / 255.0, 0, 1)\n', '    base, fabm = rr[..., :3], 1.0 - np.clip(rr[..., 3] / 255.0, 0, 1)\n    if sc.get("ink"):\n        fabm = np.ones_like(fabm)  # cảnh mực: cả khung là nền giấy\n')
        s = _rep(s, 'base = scrim(base, top=not title_on_fabric, bottom=not vo_on_fabric)', 'base = scrim(base, top=not title_on_fabric and not sc.get("ink"), bottom=not vo_on_fabric and not sc.get("ink"))')
        s = _rep(s, 'rr = cam.render(*BOARDS[key])', 'rr = cam.render(*BOARDS[(sc["img"], key)])')
    return s
