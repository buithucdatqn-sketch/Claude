# -*- coding: utf-8 -*-
"""Tập 19 · Đèn làm lệch màu gỗ (sổ tay AH+, phần kết K.1). Dữ liệu cảnh cho engine/sketch_anim/sketch_reel.py.
Chạy (từ thư mục tập):  python3 -I engine_ep19/reel_ep19.py frames .   |   python3 -I engine_ep19/reel_ep19.py video .
Giai đoạn B: đặt T_AUDIO (mốc bắt đầu từng trang theo ghi âm) rồi chạy lại.
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = HERE
while not os.path.exists(os.path.join(REPO, 'engine', 'sketch_anim', 'sketch_reel.py')):
    REPO = os.path.dirname(REPO)
sys.path.insert(0, os.path.join(REPO, 'engine', 'sketch_anim'))
import sketch_reel  # noqa: E402

OUT = os.path.dirname(HERE)
P = lambda *a: os.path.join(OUT, *a)
CREDIT = 'Ảnh dự án: Stage in Hayama · Takanori Ineyama Architects · ảnh Koichi Torimura'
PK1 = 'Hình PK.1 · sổ tay AH+ Công thức chọn màu nội thất, mục K.1'


def R(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]


def ell(cx, cy, rx, ry, n=30, a0=-2.0, turns=1.08):
    return [(cx + rx * math.cos(a), cy + ry * math.sin(a)) for a in [a0 + 2 * math.pi * turns * k / n for k in range(n + 1)]]


# sơ đồ PK.1: cắt bỏ tiêu đề (y < 58), phóng 2,5 lần
UP, OFFY = 2.5, 68


def DC(cx_o, k=1.6, yc_o=300, fy=1040):
    """camera cho sơ đồ: tâm x theo toạ độ gốc, k = px khung / px gốc, đặt y gốc yc_o tại y khung fy."""
    s = k / UP
    h = 1920 / s
    cy = (yc_o - OFFY) * UP - (fy - 960) / s
    return (cx_o * UP, cy, h)


def DP(pts):
    return [(x * UP, (y - OFFY) * UP) for x, y in pts]


GROUPS = [
    dict(name='L_lamp', box=(95, 60, 225, 168), by='y'),
    dict(name='L_rays', box=(55, 160, 265, 318)),
    dict(name='L_table', box=(15, 298, 290, 368)),
    dict(name='L_lab', box=(15, 368, 300, 545), by='y'),
    dict(name='div', box=(316, 90, 334, 475)),
    dict(name='R_lamp', box=(425, 60, 545, 168), by='y'),
    dict(name='R_rays', box=(375, 160, 600, 318)),
    dict(name='R_table', box=(340, 290, 645, 372)),
    dict(name='R_lab', box=(340, 372, 645, 545), by='y'),
]
LEFT = ['L_lamp', 'L_rays', 'L_table', 'L_lab']
RIGHT = ['div', 'R_lamp', 'R_rays', 'R_table', 'R_lab']

# đồ đạc ảnh _10 (toạ độ ảnh 2000x1600)
SOFA = [[(940, 1165), (1000, 1146), (1172, 1150), (1180, 1205)],
        [(916, 1252), (926, 1482), (1268, 1490), (1284, 1252), (1180, 1214), (950, 1214), (916, 1252)],
        R(1022, 1176, 1166, 1230),
        [(1000, 1292), (1080, 1262), (1200, 1270), (1268, 1302), (1250, 1420), (1150, 1468), (1050, 1452), (1002, 1382), (1000, 1292)]]
STUMP = [[(1300, 1322), (1420, 1296), (1546, 1322), (1540, 1352), (1302, 1352), (1300, 1322)], R(1332, 1292, 1420, 1316),
         [(1332, 1352), (1314, 1478), (1272, 1510)], [(1520, 1352), (1542, 1470), (1600, 1502)],
         [(1342, 1480), (1420, 1520), (1502, 1490)]]
CABINET = [R(1077, 945, 1345, 1245), [(1077, 1050), (1240, 1050)], [(1077, 1142), (1240, 1142)], [(1240, 945), (1240, 1245)]]
WALLPATCH = [R(1470, 930, 1640, 1130)]
REDCHAIR = [[(305, 1176), (360, 1150), (430, 1160), (446, 1230), (400, 1262), (320, 1252), (305, 1176)],
            [(330, 1252), (318, 1345)], [(426, 1246), (440, 1336)], [(376, 1262), (372, 1330)]]
GLOW = [ell(792, 845, 85, 72)]
# ảnh _21 đã căn theo _10
PENDANT21 = [[(1070, 482), (1285, 482), (1300, 596), (1285, 712), (1070, 712), (1055, 596), (1070, 482)], [(1178, 0), (1178, 480)]]
ARC21 = [[(596, 934), (616, 896), (680, 893), (702, 934), (596, 934)]]
# ảnh _20
PENDANT20 = [[(1100, 370), (1280, 370), (1298, 455), (1282, 540), (1098, 540), (1082, 455), (1100, 370)], [(1190, 0), (1190, 368)]]
SCONCE20 = [R(1398, 608, 1448, 648)]
WOOD20 = [[(1305, 600), (1690, 525), (1690, 1000), (1305, 1000), (1305, 600)]]

EP = dict(
    HEAD='AH DECODE · ĐÈN LÀM LỆCH MÀU GỖ',
    VIDEO='reel_den-lech-mau-go_silent.mp4',
    IMGS=dict(
        h10=dict(path=P('source_h10.png'), empty=P('empty_h10.png'), credit=CREDIT),
        h21=dict(path=P('source_h21.png'), credit=CREDIT),
        h20=dict(path=P('original', 'archdaily-stage-in-hayama', 'stage-in-hayama-takanori-ineyama-architects_20.jpg'), credit=CREDIT),
        pk1=dict(kind='diagram', path=P('original', 'so-tay', 'hinh-PK1-cung-cap-mau-hai-ngon-den.png'),
                 crop=(0, OFFY, 648, 540), up=UP, groups=GROUPS),
    ),
    SCENES=[
        dict(img='h10', empty=True, real=(3.9, 4.8), cam=(1050, 1130, 1060), cam1=(1050, 1120, 1000), box='top',
             sub='Ban ngày màu sơn rất hợp với tủ gỗ, sao tối bật đèn lên lại thấy lệch tông?', src=CREDIT,
             objs=[dict(t=0.45, d=(-1100, 500), rot=-26, strokes=SOFA), dict(t=1.25, d=(1000, 700), rot=30, strokes=STUMP)],
             fade_objs=(4.1, 4.9)),
        dict(img='h10', cam=(1360, 1060, 1150), cam1=(1350, 1060, 1110), box='top',
             sub='Mẫu sơn và mẫu gỗ khớp nhau dưới ánh sáng này vẫn có thể lệch nhau dưới ngọn đèn khác.', src=CREDIT,
             objs=[dict(t=1.4, d=(-900, -700), rot=-18, strokes=CABINET), dict(t=2.0, d=(900, -500), rot=22, strokes=WALLPATCH)]),
        dict(img='h10', img2='h21', fade=(0.6, 2.4), cam=(600, 1060, 1150), cam1=(615, 1055, 1100), box='left',
             sub='Trong cặp ảnh này, dưới đèn ấm lúc chạng vạng, mảng gỗ gần đèn ngả cam, còn ghế đỏ sẫm lại.', src=CREDIT,
             objs=[dict(t=2.5, d=(700, -600), rot=20, strokes=GLOW, color='orange'),
                   dict(t=3.2, d=(-900, 600), rot=-24, strokes=REDCHAIR)]),
        dict(img='pk1', cam=DC(190), cam1=DC(200), box='diagram',
             sub='Ngọn đèn hiện màu tốt hay kém được ghi trên nhãn đèn bằng chỉ số hoàn màu Ra.', src=PK1,
             draw=[('L_lamp', 0.4, 1.2), ('L_rays', 1.1, 2.1), ('L_table', 1.9, 3.1), ('L_lab', 2.9, 4.0)]),
        dict(img='pk1', cam=DC(200), cam1=DC(215), box='diagram', keep=LEFT,
             sub='Chỉ số Ra chỉ tính tám mẫu màu không quá rực, còn màu đỏ đậm có chỉ số riêng là R9.',
             src='Theo CIE 13.3-1995, dẫn trong sổ tay AH+ mục K.1',
             rays=[dict(t=1.4, dur=1.0, pts=DP([(160, 537), (220, 539), (282, 536)]), head=False)]),
        dict(img='pk1', cam=DC(330), cam1=DC(334), box='diagram', keep=LEFT,
             sub='Vì vậy, đèn có Ra khá cao vẫn có thể hiện sai màu đỏ đậm, màu nâu gỗ và màu da người.', src=PK1,
             draw=[('div', 0.5, 1.0), ('R_lamp', 0.9, 1.6), ('R_rays', 1.5, 2.4), ('R_table', 2.3, 3.6), ('R_lab', 3.4, 4.5)]),
        dict(img='h20', cam=(1360, 700, 1200), cam1=(1390, 690, 1140), box='bottom',
             sub='Phòng nhiều đồ gỗ thì nên chọn đèn có Ra từ chín mươi trở lên và R9 trên năm mươi.',
             src=CREDIT + '. Ngưỡng Ra, R9 theo quy chuẩn năng lượng California 2019 (sổ tay AH+ K.1)',
             objs=[dict(t=0.9, d=(0, -900), rot=14, strokes=PENDANT20), dict(t=1.6, d=(900, -300), rot=-20, strokes=SCONCE20),
                   dict(t=2.3, d=(900, 500), rot=16, strokes=WOOD20)]),
        dict(img='pk1', cam=DC(324), cam1=DC(324, k=1.63), box='diagram', keep=LEFT + RIGHT,
             sub='Mẫu sơn cũng nên đặt cạnh mẫu gỗ dưới đúng đèn ấy, thấy lệch thì đổi một bên trước khi mua.', src=PK1,
             rays=[dict(t=1.2, dur=1.4, pts=DP([(560, 452), (450, 462), (330, 462), (215, 452)]))]),
        dict(img='h21', cam=(1000, 900, 1600), cam1=(1000, 880, 1500), box='bottom',
             sub='Vậy chọn màu cho căn nhà cũng là chọn luôn ngọn đèn sẽ thắp mỗi tối.', src=CREDIT,
             objs=[dict(t=0.9, d=(0, -900), rot=12, strokes=PENDANT21), dict(t=1.5, d=(-900, -200), rot=-20, strokes=ARC21)]),
        dict(img='h20', cam=(1000, 666, 1332), cam1=(1000, 666, 1300), box='top', end=True, move='drift',
             sub='Cách soi mẫu dưới đèn có trong sổ tay Kinh nghiệm chọn màu kiến trúc nội thất, mọi người xem ở phần bình luận nha.',
             src='AH Decode · series phân tích nguyên tắc thiết kế và cách chọn đồ decor. ' + CREDIT),
    ],
    TAIL=1.0,
)

T_AUDIO = None   # giai đoạn B: danh sách mốc bắt đầu từng trang (giây) theo ghi âm, thêm mốc kết thúc
if T_AUDIO:
    for i, sc in enumerate(EP['SCENES']):
        sc['dur'] = T_AUDIO[i + 1] - T_AUDIO[i]

if __name__ == '__main__':
    sketch_reel.run(EP, sys.argv[1] if len(sys.argv) > 1 else 'frames', sys.argv[2] if len(sys.argv) > 2 else OUT)
