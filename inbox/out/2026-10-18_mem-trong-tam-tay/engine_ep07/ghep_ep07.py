"""Ghép video tập 7: cắt đoạn của từng run (runs.json: cut_from, cut_len) từ vid/<tag>/video/<tag>_silent.mp4 rồi nối
bằng hoà tan XF giây (xfade), giữ nguyên mốc thời gian: mỗi run (trừ run đầu) lấy thêm XF giây phía trước điểm cắt
(cảnh nối của run đó đứng yên trên đúng camera cảnh đầu run, cùng chữ cảnh trước), nên chữ không nhảy khi hoà tan.
Sau đó ghép giọng đã xử lý audio/bai-007_xu-ly.wav (AAC 48 kHz)."""
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
    ins += ["-i", OUT + f"vid/{r['tag']}/video/{r['tag']}_silent.mp4"]
    parts.append(f"[{i}:v]trim=start_frame={f0}:end_frame={f0 + n},setpts=PTS-STARTPTS,fps={FPS},format=yuv420p[v{i}]")
chain, cur, acc = [], "v0", lens[0]
for i in range(1, len(RUNS)):
    tr = RUNS[i].get("xfade", "fade")
    chain.append(f"[{cur}][v{i}]xfade=transition={tr}:duration={XF}:offset={acc - XF:.3f}[x{i}]")
    cur, acc = f"x{i}", acc + lens[i] - XF
fc = ";".join(parts + chain) + f";[{len(RUNS)}:a]apad[a]"
ins += ["-i", OUT + "audio/bai-007_xu-ly.wav"]
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", fc,
                "-map", f"[{cur}]", "-map", "[a]", "-t", f"{acc:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
                OUT + "reel_mem-trong-tam-tay_final.mp4"], check=True)
print("xong", round(acc, 2), "giây")
