#!/bin/sh
# Ghép video chính (ảnh 12) + đoạn cảnh 8 (ảnh 11, engine phụ) + giọng đọc đã xử lý -> reel_..._final.mp4
set -e
cd "$(dirname "$0")/.."
M=video/reel_cung-mau-khac-be-mat_silent.mp4
B=bep_tmp/video/reel_bep_silent.mp4
T8=33.0; CUT=5.0; LEN=5.0
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $M)
ffmpeg -y -loglevel error -i $M -i $B -i audio/bai-006_xu-ly.wav -filter_complex "\
[0:v]trim=0:$T8,setpts=PTS-STARTPTS[a];\
[1:v]trim=$CUT:$(echo "$CUT+$LEN" | bc),setpts=PTS-STARTPTS[b];\
[0:v]trim=$(echo "$T8+$LEN" | bc),setpts=PTS-STARTPTS[c];\
[a][b][c]concat=n=3:v=1:a=0,format=yuv420p[v];\
[2:a]apad[au]" -map "[v]" -map "[au]" -t $DUR -r 30 -c:v libx264 -preset medium -crf 17 -c:a aac -b:a 192k -ar 48000 -movflags +faststart reel_cung-mau-khac-be-mat_final.mp4
ffprobe -v error -show_entries stream=codec_name,width,height,sample_rate:format=duration -of default=nw=1 reel_cung-mau-khac-be-mat_final.mp4
