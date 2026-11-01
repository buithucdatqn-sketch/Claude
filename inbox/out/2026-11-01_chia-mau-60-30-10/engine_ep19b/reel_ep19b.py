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
CREDIT = 'Ảnh dự án: Curva Apartment, Brasília · Isabela Bandeira + Gabriela Lauria · ảnh Júlia Tótoli'
H22 = 'Hình 2.2 · sổ tay AH+, mục 2.4 · kinh nghiệm hành nghề'
LOI = open(P('ban_nhap', 'loi_v4.txt'), encoding='utf8').read().strip().split('\n')


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

# Curva Apartment (ArchDaily): _7 bếp (2000x1333), _12 góc ăn (1365x2048), _2 phòng khách (2000x1333), _9 quầy bếp (1365x2048)
WALL7 = [R(1530, 255, 2000, 950)]
NAVY7 = [R(690, 262, 1500, 1095), [(0, 1135), (690, 850), (780, 850), (780, 1333)], [(1405, 1333), (1420, 1080), (1600, 990), (2000, 960)]]
TABLE = [ell(711, 1244, 360, 55), [(560, 1300), (600, 1700), (840, 1700), (860, 1300)]]
CH_FL = [ell(333, 1327, 95, 113), [(320, 1410), (600, 1420), (600, 1500), (330, 1500), (320, 1410)],
         [(240, 1500), (225, 1840)], [(393, 1520), (395, 1840)], [(600, 1500), (640, 1740)]]
CH_FR = [ell(1083, 1327, 85, 113), [(810, 1420), (1080, 1410), (1090, 1500), (820, 1510), (810, 1420)],
         [(800, 1510), (785, 1745)], [(1060, 1510), (1048, 1840)], [(1150, 1430), (1190, 1800)]]
CH_BL = [ell(422, 1200, 62, 70), [(360, 1380), (355, 1560)]]
CH_BR = [ell(940, 1195, 62, 68), [(990, 1380), (1000, 1500)]]
PRINTS = [R(60, 781, 233, 1029), R(255, 795, 400, 1020), R(425, 810, 552, 1018)]
ARM = [[(1105, 800), (1130, 760), (1210, 755), (1245, 800), (1230, 860), (1120, 870), (1105, 800)], [(1085, 880), (1070, 935)], [(1200, 880), (1210, 935)]]
STOOLS = [ell(1610, 1075, 100, 38), [(1530, 1090), (1500, 1320)], [(1690, 1090), (1714, 1320)],
          ell(1790, 1165, 90, 42), [(1720, 1180), (1702, 1330)]]
NAVY9 = [R(775, 700, 1365, 1450), [(0, 1300), (1050, 1300), (1100, 1380), (1060, 1640), (760, 1650), (760, 1500), (0, 1480)]]

EP = dict(
    HEAD='AH DECODE · CHIA MÀU 60-30-10',
    VIDEO='reel_chia-mau-60-30-10_silent.mp4',
    IMGS=dict(
        c10=dict(path=P('original', 'archdaily-curva', 'apartamento-curva-isabela-bandeira-plus-gabriela-lauria_10.jpg'), credit=CREDIT),
        c7=dict(path=P('original', 'archdaily-curva', 'apartamento-curva-isabela-bandeira-plus-gabriela-lauria_7.jpg'), credit=CREDIT),
        c12=dict(path=P('source_c12.png'), empty=P('empty_c12.png'), credit=CREDIT),
        c2=dict(path=P('original', 'archdaily-curva', 'apartamento-curva-isabela-bandeira-plus-gabriela-lauria_2.jpg'), credit=CREDIT),
        c9=dict(path=P('original', 'archdaily-curva', 'apartamento-curva-isabela-bandeira-plus-gabriela-lauria_9.jpg'), credit=CREDIT),
        h22=dict(kind='diagram', path=P('original', 'so-tay', 'hinh-2-2-60-30-10.png'), crop=(0, OFFY, 648, 665), up=UP, groups=GROUPS),
    ),
    SCENES=[
        dict(img='c10', fit=True, cam=(1000, 666, 3556), cam1=(1000, 666, 3420), box='top', sub=LOI[0], src=CREDIT),
        dict(img='h22', cam=DC(), cam1=DC(k=1.47), box='diagram', sub=LOI[1], src=H22, draw=[('plan', 0.3, 3.2)]),
        dict(img='h22', cam=DC(k=1.47), cam1=DC(k=1.47), box='diagram', sub=LOI[2], src=H22, keep=['plan'],
             draw=[('lg60', 0.5, 2.2)]),
        dict(img='h22', cam=DC(k=1.47), cam1=DC(k=1.47), box='diagram', sub=LOI[3], src=H22, keep=K60,
             draw=[('g_top', 0.4, 1.5), ('g_bep', 1.3, 2.3), ('lg30', 2.1, 3.3)]),
        dict(img='h22', cam=DC(k=1.47), cam1=DC(k=1.47), box='diagram', sub=LOI[4], src=H22, keep=K30,
             draw=[('r_sq', 0.4, 1.0), ('r_chairs', 0.9, 2.5), ('lg10', 2.3, 3.5)]),
        dict(img='c7', fit=True, cam=(1000, 666, 3556), cam1=(1000, 666, 3420), box='top', sub=LOI[5], src=CREDIT,
             objs=[dict(t=0.5, d=(900, -500), rot=12, strokes=WALL7, color='ink'), dict(t=1.5, d=(-900, 400), rot=-16, strokes=NAVY7)]),
        dict(img='c12', fit=True, empty=True, real=(4.4, 5.2), cam=(683, 1024, 2427), cam1=(683, 1024, 2380), box='top', sub=LOI[6], src=CREDIT,
             objs=[dict(t=0.5, d=(0, 900), rot=10, strokes=TABLE, color='ink'),
                   dict(t=1.1, d=(-900, 500), rot=-22, strokes=CH_FL, color='ink'), dict(t=1.5, d=(900, 500), rot=24, strokes=CH_FR, color='ink'),
                   dict(t=1.9, d=(-800, -400), rot=-18, strokes=CH_BL, color='ink'), dict(t=2.3, d=(800, -400), rot=18, strokes=CH_BR, color='ink'),
                   dict(t=2.8, d=(-700, -600), rot=-14, strokes=PRINTS, color='ink')],
             fade_objs=(4.7, 5.4)),
        dict(img='h22', cam=DC(k=1.47), cam1=DC(k=1.47), box='diagram', sub=LOI[7], src=H22 + ' · mốc 30 theo Dulux Trade',
             keep=K10, draw=[('lrv', 0.6, 2.8)]),
        dict(img='c2', fit=True, cam=(1000, 666, 3556), cam1=(1000, 666, 3420), box='top', sub=LOI[8], src=CREDIT,
             objs=[dict(t=0.8, d=(0, -900), rot=16, strokes=ARM, th=9), dict(t=1.5, d=(900, 400), rot=-20, strokes=STOOLS, th=9)]),
        dict(img='c9', fit=True, cam=(683, 1024, 2427), cam1=(700, 1060, 2300), box='top', sub=LOI[9], src=CREDIT,
             objs=[dict(t=0.5, d=(900, 400), rot=14, strokes=NAVY9)]),
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
