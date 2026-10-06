"""Tập 3: Dáng cong và góc nhọn của đồ nội thất (contour bias).
Sinh engine_ep03.py + engine_video_ep03.py từ hai engine gốc, và script/elevenlabs từ cùng dữ liệu cảnh."""
import json
import re
import sys

E = "/home/claude/claude/engine/"
OUT = "/home/claude/claude/inbox/out/2026-10-06_dang-cong-goc-nhon/"
WPS = 3.2      # tốc độ đọc dự kiến (từ/giây)
TRANS = 0.7

# camera: (focus trên ảnh xem 2000px, zoom, anchor)
WIDE = "WIDE"
SC = [
    dict(part="A", head="Ghế nào cũng bo tròn", cam=WIDE, dark=False,
         vo="Rèm thẳng, khung vuông, mà ghế nào cũng bo tròn. Vì sao?"),
    dict(part="B", head="Đường của cái đẹp", cam=WIDE, dark=True,
         vo="Năm 1753, William Hogarth gọi đường lượn là đường của cái đẹp.",
         tts="Năm mười bảy năm mươi ba, William Hogarth gọi đường lượn là đường của cái đẹp."),
    dict(part="C", head="Thí nghiệm năm 2006", cam=WIDE, dark=True,
         vo="Năm 2006, Bar và Neta cho xem từng cặp đồ, khác chủ yếu ở góc sắc hay cong.",
         tts="Năm hai nghìn lẻ sáu, Bar và Neta cho xem từng cặp đồ, khác chủ yếu ở góc sắc hay cong."),
    dict(part="C", head="Vấn đề là góc sắc", cam=((1560, 990), 1.7, (540, 900)), dark=True,
         vo="Dưới một phần mười giây, bản cong được thích hơn. Có thể vì góc sắc gợi mối nguy, đường thẳng thì không."),
    dict(part="D", head="Ghế: chỗ chạm không có góc", cam=((900, 1010), 1.9, (540, 900)), dark=True,
         vo="Ghế bành: lưng ôm tròn, chân váy bo, chỗ chạm không có góc."),
    dict(part="D", head="Bàn: góc tù", cam=((1560, 990), 1.8, (540, 900)), dark=True,
         vo="Bàn tám cạnh: vẫn có góc, nhưng là góc tù."),
    dict(part="E", head="Nên tránh", cam=((1560, 990), 1.8, (540, 900)), dark=True,
         vo="Nên tránh bàn góc sắc sát đầu gối."),
    dict(part="F", head="Áp dụng", cam=((1250, 960), 1.4, (540, 900)), dark=True,
         vo="Thử đổi bàn trà sang mặt tròn hoặc góc bo."),
    dict(part="G", head="Chọn mua", cam=((1150, 1000), 1.5, (540, 900)), dark=True,
         vo="So hai bản cùng một món, nên chọn bản bo cong."),
    dict(part="H", head="Công thức", cam=WIDE, dark=False,
         vo="Giữ đường thẳng, chỉ bo những góc sắc."),
    dict(part="I", head="end", cam="END", dark=False, vo="",
         tts="AH Decode, series về nguyên tắc thiết kế và chọn đồ decor. Theo dõi Giả Thuyết Kiến Trúc, bài viết cho thành viên ở link bình luận."),
]

DOODLE = r'''
def doodle(i, wb, text, cam):
    def lab(p, s_, size=60):
        x, y = cam.pt(D([p])[0])
        text.put((x, y), s_, size)

    def P(p):
        return D([p])[0]

    def note(xy, s_, target, size=56, bow=-30):
        text.put(xy, s_, size)
        w_ = text.d.textlength(s_, font=F(size))
        tx, ty = cam.pt(P(target))
        wb.ink_arrow((xy[0] + w_ / 2, xy[1] + size + 14), (tx, ty - 10), bow=bow)

    if i == 0:  # mở: ghế tròn và khung thẳng
        wb.contour(OBJ["chair2"], offset=12, eps=3, w=7)
        wb.contour(OBJ["chair3"], offset=12, eps=3, w=7)
        wb.contour(OBJ["frame2"], offset=10, eps=2, w=6)
    elif i == 1:  # Hogarth: đường lượn trên lưng ghế và băng ghế
        wb.line(P((585, 760)), P((735, 860)), 7, bow=-40)
        wb.line(P((180, 690)), P((960, 650)), 7, bow=30)
        note((60, 420), "đường lượn", (560, 655), 58, bow=20)
    elif i == 2:  # cặp: cong và góc
        wb.contour(OBJ["chair3"], offset=12, eps=3, w=7)
        wb.contour(OBJ["t4"], offset=10, eps=2, w=7)
        note((60, 420), "cong", (930, 900), 58, bow=20)
        note((640, 420), "có góc", (1740, 985), 58, bow=-20)
    elif i == 3:  # cơ chế: góc
        wb.contour(OBJ["t4"], offset=10, eps=2, w=8)
        wb.arrow(P((1690, 1180)), P((1595, 1030)), 7, bow=-20)
        lab((1550, 1150), "góc", 64)
    elif i == 4:  # ghế
        wb.contour(OBJ["chair2"], offset=10, eps=3, w=8)
        wb.line(P((855, 872)), P((1040, 1040)), 7, bow=-30)
        lab((560, 720), "lưng ôm tròn", 54)
        lab((960, 1150), "chân váy bo", 50)
    elif i == 5:  # bàn tám cạnh
        wb.contour(OBJ["t3"], offset=10, eps=2, w=8)
        wb.contour(OBJ["t4"], offset=10, eps=2, w=8)
        wb.arrow(P((1850, 1150)), P((1945, 1030)), 7, bow=-20)
        lab((1600, 1150), "góc tù", 64)
    elif i == 6:  # lỗi: góc vuông giả định
        wb.line(P((1530, 990)), P((1530, 1060)), 7)
        wb.line(P((1530, 1060)), P((1700, 1060)), 7)
        wb.arrow(P((1300, 1140)), P((1515, 1065)), 7, bow=-20)
        lab((1180, 1150), "góc sắc ở đây?", 54)
    elif i == 7:  # áp dụng: bàn trà giữa nhóm ghế
        wb.contour(OBJ["t3"], offset=10, eps=2, w=8)
        wb.arrow(P((1300, 780)), P((1420, 895)), 7, bow=20)
        lab((1060, 680), "mặt tròn, góc bo?", 54)
    elif i == 8:  # chọn mua: món hay chạm
        wb.contour(OBJ["chair4"], offset=12, eps=3, w=8)
        wb.contour(OBJ["t3"], offset=10, eps=2, w=8)
        lab((1180, 1150), "ghế", 58)
        lab((1380, 770), "bàn trà", 58)
    elif i == 9:  # công thức
        wb.contour(OBJ["chair2"], offset=12, eps=3, w=7)
        wb.contour(OBJ["chair3"], offset=12, eps=3, w=7)
        wb.dashed(P((1520, 120)), P((1520, 700)), 6)
        note((60, 420), "góc: bo", (830, 900), 56, bow=20)
        note((620, 420), "đường: thẳng", (1520, 300), 56, bow=-20)
'''

OBJ = r'''
OBJ = dict(
    chair2=D([(685, 812), (740, 800), (775, 840), (880, 1000), (920, 1080), (925, 1250), (745, 1250), (740, 1080), (700, 950), (682, 870)]),
    chair3=D([(852, 880), (900, 870), (942, 905), (1000, 980), (1080, 1100), (1100, 1250), (935, 1250), (930, 1090), (880, 960), (848, 912)]),
    chair4=D([(1080, 1000), (1160, 985), (1250, 1040), (1310, 1150), (1330, 1250), (1100, 1250), (1080, 1100)]),
    frame2=D([(1655, 172), (1840, 172), (1865, 555), (1680, 552)]),
    t2=D([(1110, 838), (1340, 838), (1390, 860), (1335, 890), (1110, 892), (1080, 862)]),
    t3=D([(1300, 905), (1580, 905), (1630, 935), (1580, 965), (1300, 965), (1258, 935)]),
    t4=D([(1550, 985), (1910, 985), (1965, 1022), (1925, 1058), (1560, 1058), (1520, 1022)]),
)
'''


def words(s):
    return len(s.split())


def build_data():
    t = 0.0
    scenes = []
    for k, s in enumerate(SC):
        spoken = s.get("tts", s["vo"])
        dur = max(3.5, TRANS + words(spoken) / WPS)
        if s["head"] == "end":
            dur = max(dur, 6.0)
        a, b = round(t, 1), round(t + dur, 1)
        t = b
        s["t"] = f"{a:g}–{b:g}s"
        s["dur"] = b - a
        if s["cam"] == WIDE:
            cam = "WIDE"
        elif s["cam"] == "END":
            cam = "(CENTER, 1.0, (540, 640))"
        else:
            (fx, fy), z, anc = s["cam"]
            cam = f"((({fx} * 1.2), ({fy} * 1.2)), {z}, {anc})"
        scenes.append(f'    dict(t="{s["t"]}", head={json.dumps(s["head"], ensure_ascii=False)}, '
                      f'vo={json.dumps(s["vo"], ensure_ascii=False)},\n         cam={cam}, dark={s["dark"]}),')
    data = ('# ---------------- scenes ----------------\nCENTER = (SW / 2, SH / 2)\n\n\n'
            'def D(pts):\n    """toạ độ đo trên ảnh xem 2000px -> ảnh làm việc 2400px"""\n'
            '    return [(x * 1.2, y * 1.2) for x, y in pts]\n\n' + OBJ +
            '\nWIDE = (CENTER, 1.0, (540, 905))\nSCENES = [\n' + "\n".join(scenes) + '\n]\n'
            'END = len(SCENES) - 1\nBOARDS = {}\n' + DOODLE + '\n\n')
    return data, t


def build(src, dst, video, data):
    s = open(E + src).read()
    s = s.replace('CREDIT = "Ảnh dự án: [tên dự án] · [studio] · [nhiếp ảnh gia]"',
                  'CREDIT = "Ảnh dự án: The Twenty Two New York · Child Studio · ảnh Alixe Lay · Yellowtrace"')
    s = s.replace('HEAD = "AH DECODE · CÂN BẰNG THỊ GIÁC"', 'HEAD = "AH DECODE · DÁNG CONG & GÓC SẮC"')
    a = s.index("# ---------------- scenes")
    b = s.index('def render_scene') if not video else s.index('BOARDS["plain"] = make_board(1.0)')
    s = s[:a] + data + s[b:]
    if video:
        s = s.replace('"reel1_silent.mp4"', '"reel_dang-cong-goc-nhon_silent.mp4"')
    else:
        s = s.replace('"frames_v7"', '"frames"').replace('"storyboard_reel1_v7.png"', '"storyboard.png"')
        s = s.replace("AH Decode · Cân bằng thị giác — bảng phân cảnh v7", "AH Decode · Dáng cong & góc sắc")
        s = s.replace('font=F(60), fill=(255, 255, 255))', 'font=F(50), fill=(255, 255, 255))')
        s = s.replace("Ảnh dán bằng băng giấy ở giữa mép trên · không viền · nền trắng trơn · chữ nâu đậm trên nền, trắng trên ảnh",
                      "Ảnh dán bằng băng giấy · nền trắng · chữ nâu trên nền, trắng trên ảnh")
        s = s.replace("Camera zoom vào ảnh khi nói đến chi tiết · ~28 giây · nét vẽ chạy animation theo nhịp lời đọc",
                      "Camera zoom vào chi tiết · nét vẽ chạy dần theo lời đọc")
        s = s.replace("Ảnh tối ~14% ở cảnh có nét vẽ; cảnh 1, 6, 7 giữ ảnh nguyên bản.",
                      "Ảnh tối ~14% ở cảnh có nét vẽ; cảnh mở, công thức và cảnh cuối giữ ảnh nguyên bản.")
    open(E + dst, "w").write(s)


data, total = build_data()
build("engine_storyboard_v7.py", "engine_ep03.py", False, data)
build("engine_video.py", "engine_video_ep03.py", True, data)

# ---- script.md + elevenlabs.txt ----
NAMES = dict(A="Mở", B="Nguồn gốc", C="Cơ chế / bằng chứng", D="Đọc trên ảnh", E="Lỗi hay gặp", F="Áp dụng",
             G="Chọn đồ", H="Công thức", I="Cảnh cuối")
spoken_all = [s.get("tts", s["vo"]) for s in SC]
nw = sum(words(x) for x in spoken_all)
rows = []
for k, s in enumerate(SC):
    head = "(khung cuối cố định)" if s["head"] == "end" else s["head"]
    rows.append(f'| {k + 1} | {s["t"]} | {s["part"]} · {NAMES[s["part"]]} | {head} | {s.get("tts", s["vo"])} |')
md = (f"# AH Decode · Dáng cong & góc sắc (contour bias) — BẢN NHÁP chờ duyệt\n\n"
      f"Ảnh: The Twenty Two New York · Child Studio · ảnh Alixe Lay · Yellowtrace\n"
      f"Thời lượng dự kiến: {total:.1f} giây + 1 giây giữ khung cuối · {nw} từ lời đọc (tính theo cách đọc) · {len(SC)} cảnh.\n\n"
      "| # | Thời lượng | Phần | Tiêu đề trên khung | Lời đọc |\n|---|---|---|---|---|\n" + "\n".join(rows) +
      "\n\n## Lời đọc liền mạch\n\n" + " ".join(spoken_all) + "\n")
open(OUT + "script.md", "w").write(md)


def lines(txt):
    parts = re.split(r'(?<=[.?!])\s+', txt.strip())
    return "\n".join(p for p in parts if p)


el = "\n\n".join(lines(x) for x in spoken_all)
el += ("\n\n--- Gợi ý cài đặt: giọng nữ hoặc nam trầm ấm, tốc độ 1.0, mô hình đa ngôn ngữ, ngôn ngữ Vietnamese. "
       "Chỉ dán phần phía trên dòng này. Tên riêng: Hogarth (đọc gần như 'Hô-ga'), Bar và Neta (đọc 'Ba' và 'Nê-ta'); "
       "nếu ElevenLabs đọc sai tên AH Decode, thay bằng cách viết theo âm bạn muốn ---\n")
open(OUT + "elevenlabs.txt", "w").write(el)
print("total", round(total, 1), "words", nw)
for s in SC:
    print(s["t"], words(s.get("tts", s["vo"])), s["head"])
