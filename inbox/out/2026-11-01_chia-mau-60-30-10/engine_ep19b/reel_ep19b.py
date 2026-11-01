# -*- coding: utf-8 -*-
"""Tập 19 bản 2 · Chia màu 60-30-10 (sổ tay AH+ chương 2 mục 2.4). Dữ liệu cảnh cho engine/sketch_anim/sketch_reel.py.
Nét vẽ bay vào là chính các tầng màu của quy tắc: nền (trần, sàn, tường), khối tủ xanh (30%), đồ rời rực màu (10%).
Chạy (từ thư mục tập):  python3 -I engine_ep19b/reel_ep19b.py frames .   |   ... video .
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
CREDIT = 'Ảnh dự án: First House · HANGHAR · ảnh Luis Díaz Díaz'
H22 = 'Hình 2.2 · sổ tay AH+, mục 2.4 · kinh nghiệm hành nghề'
LOI = open(P('ban_nhap', 'loi_v3.txt'), encoding='utf8').read().strip().split('\n')


def R(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]


def ell(cx, cy, rx, ry, n=28):
    return [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]


UP, OFFY = 2.5, 85


def DC(cx_o=324, k=1.45, yc_o=375, fy=1010):
    s = k / UP
    return (cx_o * UP, (yc_o - OFFY) * UP - (fy - 960) / s, 1920 / s)


GROUPS = [
    dict(name='plan', box=(25, 88, 622, 402)),
    dict(name='g_top', box=(315, 95, 612, 150)), dict(name='g_bep', box=(370, 195, 542, 262)),
    dict(name='r_sq', box=(228, 128, 277, 172)), dict(name='r_chairs', box=(385, 262, 538, 382)),
    dict(name='lg60', box=(25, 415, 245, 487)), dict(name='lg30', box=(318, 420, 545, 492)),
    dict(name='lg10', box=(25, 488, 258, 558)), dict(name='lrv', box=(30, 562, 525, 662), by='y'),
]
K60 = ['plan', 'lg60']
K30 = K60 + ['g_top', 'g_bep', 'lg30']
K10 = K30 + ['r_sq', 'r_chairs', 'lg10']

# ảnh _15 (2000x2667): nền và khối tủ xanh
NEN15 = [[(0, 470), (560, 540), (920, 560)], [(1640, 625), (2000, 700)], [(0, 2090), (640, 1625)], [(1640, 1560), (2000, 1520)]]
ISLAND = [R(925, 535, 1635, 2440)]
COUNTER = [[(0, 1345), (625, 1322), (632, 1625), (0, 2090)]]
# ảnh _12 (2000x1500): đồ rời
BUCKET = [[(55, 1180), (285, 1175), (275, 1465), (65, 1468), (55, 1180)], [(110, 1268), (175, 1302), (255, 1282)]]
BOOKS = [R(332, 1300, 548, 1390), [(345, 1265), (520, 1235), (545, 1300)]]
RUG = [[(1095, 1195), (1625, 1195), (1990, 1492), (1110, 1498), (1095, 1195)]]
TEAPOT = [ell(1270, 1302, 80, 52)]
SPONGE = [ell(1395, 1365, 26, 20)]
# ảnh _13 (2000x1333): hai ghế vàng
CHAIR1 = [[(1095, 812), (1130, 775), (1200, 760), (1265, 768), (1300, 822)], [(1095, 812), (1180, 900), (1305, 940), (1300, 822)],
          [(1100, 815), (1262, 1155)], [(1295, 825), (1112, 1095)], [(1305, 965), (1378, 1112)]]
CHAIR2 = [[(1750, 878), (1915, 935)], [(1594, 1011), (1745, 1025), (1900, 1085)], [(1752, 880), (1606, 1190)],
          [(1912, 938), (1930, 1294)], [(1910, 945), (1717, 1289)], [(1640, 1050), (1880, 1240)]]

EP = dict(
    HEAD='AH DECODE · CHIA MÀU 60-30-10',
    VIDEO='reel_chia-mau-60-30-10_silent.mp4',
    IMGS=dict(
        f15=dict(path=P('original', 'archdaily-first-house', 'HANGHAR_FirstHouse_15.jpg'), credit=CREDIT),
        f12=dict(path=P('source_f12.png'), empty=P('empty_f12.png'), credit=CREDIT),
        f13=dict(path=P('original', 'archdaily-first-house', 'HANGHAR_FirstHouse_13.jpg'), credit=CREDIT),
        h22=dict(kind='diagram', path=P('original', 'so-tay', 'hinh-2-2-60-30-10.png'), crop=(0, OFFY, 648, 665), up=UP, groups=GROUPS),
    ),
    SCENES=[
        dict(img='f15', fit=True, cam=(1000, 1333, 3556), cam1=(1000, 1333, 3420), box='top', sub=LOI[0], src=CREDIT),
        dict(img='h22', cam=DC(), cam1=DC(k=1.47), box='diagram', sub=LOI[1], src=H22, draw=[('plan', 0.3, 3.2)]),
        dict(img='h22', cam=DC(k=1.47), cam1=DC(k=1.47), box='diagram', sub=LOI[2], src=H22, keep=['plan'],
             draw=[('lg60', 0.5, 2.2)]),
        dict(img='h22', cam=DC(k=1.47), cam1=DC(k=1.47), box='diagram', sub=LOI[3], src=H22, keep=K60,
             draw=[('g_top', 0.4, 1.5), ('g_bep', 1.3, 2.3), ('lg30', 2.1, 3.3)]),
        dict(img='h22', cam=DC(k=1.47), cam1=DC(k=1.47), box='diagram', sub=LOI[4], src=H22, keep=K30,
             draw=[('r_sq', 0.4, 1.0), ('r_chairs', 0.9, 2.5), ('lg10', 2.3, 3.5)]),
        dict(img='f15', fit=True, cam=(1000, 1333, 3420), cam1=(1000, 1333, 3300), box='top', sub=LOI[5], src=CREDIT,
             objs=[dict(t=0.5, d=(0, -900), rot=10, strokes=NEN15, color='ink'),
                   dict(t=1.6, d=(1000, 300), rot=-18, strokes=ISLAND), dict(t=2.3, d=(-1000, 400), rot=20, strokes=COUNTER)]),
        dict(img='f12', fit=True, empty=True, real=(4.3, 5.1), cam=(1000, 750, 3556), cam1=(1000, 750, 3450), box='top', sub=LOI[6], src=CREDIT,
             objs=[dict(t=0.6, d=(-900, 300), rot=-24, strokes=BUCKET, color='ink'),
                   dict(t=1.2, d=(-700, 600), rot=18, strokes=BOOKS, color='ink'),
                   dict(t=2.9, d=(900, 500), rot=20, strokes=RUG, color='ink'),
                   dict(t=3.4, d=(600, -700), rot=-16, strokes=TEAPOT, color='ink'),
                   dict(t=3.7, d=(700, 400), rot=30, strokes=SPONGE, color='ink')],
             fade_objs=(4.6, 5.3)),
        dict(img='h22', cam=DC(k=1.47), cam1=DC(k=1.47), box='diagram', sub=LOI[7], src=H22 + ' · mốc 30 theo Dulux Trade',
             keep=K10, draw=[('lrv', 0.6, 2.8)]),
        dict(img='f13', fit=True, cam=(1000, 666, 3556), cam1=(1000, 666, 3450), box='top', sub=LOI[8], src=CREDIT,
             objs=[dict(t=0.8, d=(-900, 300), rot=-22, strokes=CHAIR1, color='ink'),
                   dict(t=1.5, d=(900, 300), rot=24, strokes=CHAIR2, color='ink')]),
        dict(img='f15', fit=True, cam=(1150, 1400, 2900), cam1=(1150, 1400, 2800), box='top', sub=LOI[9], src=CREDIT,
             objs=[dict(t=0.4, d=(0, 900), rot=12, strokes=ISLAND)]),
        dict(img='endv', endvideo=True, sub=LOI[10]),
    ],
    TAIL=1.0,
    END_VIDEO=dict(video=P('original', 'chu-trang', 'AH_mockup_tablet.mp4'),
                   lines=[(380, 'Cách chia màu 60-30-10 và mốc độ sáng', 50, 255),
                          (440, 'trong sổ tay chọn màu AH+ của tụi mình', 40, 240),
                          (512, 'mọi người xem ở phần bình luận nha', 58, 255)],
                   credit=(1440, 'Video: sổ tay AH+ Công thức chọn màu nội thất · Giả Thuyết Kiến Trúc', 28, 215)),
)

T_AUDIO = None   # giai đoạn B: mốc bắt đầu từng trang theo ghi âm (thêm mốc kết thúc)
if T_AUDIO:
    for i, sc in enumerate(EP['SCENES']):
        sc['dur'] = T_AUDIO[i + 1] - T_AUDIO[i]

if __name__ == '__main__':
    sketch_reel.run(EP, sys.argv[1] if len(sys.argv) > 1 else 'frames', sys.argv[2] if len(sys.argv) > 2 else OUT)
