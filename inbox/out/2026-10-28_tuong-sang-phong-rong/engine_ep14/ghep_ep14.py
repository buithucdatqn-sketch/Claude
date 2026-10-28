"""Ghép video tập 14: cắt đoạn của từng run (runs.json: cut_from, cut_len) từ vid/<tag>/video/<tag>_silent.mp4 rồi nối
bằng hoà tan XF giây (xfade), giữ nguyên mốc thời gian: mỗi run (trừ run đầu) lấy thêm XF giây phía trước điểm cắt
(cảnh nối của run đó đứng yên trên đúng camera cảnh đầu run, cùng chữ cảnh trước), nên chữ không nhảy khi hoà tan.
Khung cuối (run ảnh "ebook") không lấy từ engine mà từ end_ep14.mp4: video sổ tay AH+ chủ Trang gửi, toàn màn hình,
dựng bằng end_ep14.py đúng thời lượng của đoạn. Sau đó ghép giọng đã xử lý audio/tuong-sang-phong-rong_xu-ly.wav (AAC 48 kHz)."""
import json, os, subprocess, sys
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "./") + "/"
HERE = os.path.dirname(os.path.abspath(__file__))
FPS, XF = 30, 0.45
RUNS = json.load(open(os.path.join(HERE, "runs.json")))
ins, parts, total = [], [], 0.0
lens = []
for i, r in enumerate(RUNS):
    pre = 0.0 if i == 0 else XF
    f0 = round((r["cut_from"] - pre) * FPS)
    n = round((r["cut_len"] + pre) * FPS)
    lens.append(n / FPS)
    if r["img"] == "ebook":
        src = [OUT + "original/chu-trang/" + f for f in sorted(os.listdir(OUT + "original/chu-trang")) if f.endswith((".mp4", ".gif"))][0]
        subprocess.run(["/usr/bin/python3", "-I", os.path.join(HERE, "end_ep14.py"), src, OUT, f"{n / FPS + 0.2:.2f}"], check=True)
        f0 = 0
        ins += ["-i", OUT + "end_ep14.mp4"]
    else:
        ins += ["-i", OUT + f"vid/{r['tag']}/video/{r['tag']}_silent.mp4"]
    parts.append(f"[{i}:v]trim=start_frame={f0}:end_frame={f0 + n},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p[v{i}]")
chain, cur, acc = [], "v0", lens[0]
for i in range(1, len(RUNS)):
    tr = RUNS[i].get("xfade", "fade")
    chain.append(f"[{cur}][v{i}]xfade=transition={tr}:duration={XF}:offset={acc - XF:.3f}[x{i}]")
    cur, acc = f"x{i}", acc + lens[i] - XF
fc = ";".join(parts + chain) + f";[{len(RUNS)}:a]apad[a]"
AUDIO = sys.argv[2] if len(sys.argv) > 2 else OUT + "audio/tuong-sang-phong-rong_xu-ly.wav"
ins += ["-i", AUDIO]
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", fc,
                "-map", f"[{cur}]", "-map", "[a]", "-t", f"{acc:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
                sys.argv[3] if len(sys.argv) > 3 else OUT + "reel_tuong-sang-phong-rong_final.mp4"], check=True)
print("xong", round(acc, 2), "giây")
