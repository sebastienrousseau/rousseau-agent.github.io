#!/usr/bin/env bash
# Encode a genuine WebM video from an animated PNG timeline of the
# TUI demo. Ships to /assets/rousseau-chat.webm and /assets/rousseau-chat.vtt.
#
# We don't need a browser — we emit SVG frames representing the terminal
# at each animation step, rasterise to PNG (via imagemagick or resvg if
# available; otherwise skip encoding and just emit VTT captions), then
# feed the PNG sequence into ffmpeg to produce WebM.
set -euo pipefail
cd "$(dirname "$0")/.."

PUB=public
ASSETS="$PUB/assets"
mkdir -p "$ASSETS"

# Emit WebVTT captions for the animated TUI timeline (matches the CSS animation-delay values).
cat > "$ASSETS/rousseau-chat.vtt" <<'VTT'
WEBVTT

1
00:00.6 --> 00:01.3
$ rousseau chat

2
00:01.4 --> 00:02.1
session bc4a-42d1 — provider claudecli — workspace ~/team-rousseau

3
00:02.2 --> 00:03.0
you: What does internal/agent/session.go do?

4
00:03.0 --> 00:03.7
Tool call: read internal/agent/session.go

5
00:03.8 --> 00:04.5
Tool result: 1,847 bytes returned

6
00:04.6 --> 00:07.0
rousseau: Session holds the conversation history and metadata for one chat thread. It carries the sliding window of messages, the session ID used with the LLM provider, and per-session context.
VTT

# Try to produce a real WebM. We use ffmpeg's built-in lavfi to synthesise
# a video from a scripted drawtext filter chain. This is a real encoded
# video artifact (not just an animated SVG), suitable for <video> embedding.
if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "    video:    ffmpeg missing; skipping WebM encode (VTT emitted at /assets/rousseau-chat.vtt)"
    exit 0
fi

OUT="$ASSETS/rousseau-chat.webm"
POSTER="$ASSETS/rousseau-chat-poster.png"

# Compose the video via ffmpeg lavfi + drawtext. 9 timed lines, ~8s total.
ffmpeg -y -loglevel error \
  -f lavfi -i "color=c=0x0d1117:s=820x360:d=8:r=24" \
  -vf "\
drawtext=text='rousseau chat':fontcolor=0x8b949e:fontsize=13:x=10:y=10:enable='between(t,0,8)',\
drawtext=text='\$ rousseau chat':fontcolor=0xe6edf3:fontsize=14:x=20:y=50:enable='gte(t,0.6)',\
drawtext=text='session bc4a-42d1 provider=claudecli':fontcolor=0x8b949e:fontsize=13:x=20:y=75:enable='gte(t,1.4)',\
drawtext=text='you > What does internal/agent/session.go do?':fontcolor=0x79c0ff:fontsize=13:x=20:y=105:enable='gte(t,2.2)',\
drawtext=text='-> tool_use read internal/agent/session.go':fontcolor=0xa5d6ff:fontsize=12:x=20:y=135:enable='gte(t,3.0)',\
drawtext=text='<- tool_result 1847 bytes':fontcolor=0xa5d6ff:fontsize=12:x=20:y=160:enable='gte(t,3.8)',\
drawtext=text='rousseau > Session holds the conversation':fontcolor=0xe6edf3:fontsize=13:x=20:y=195:enable='gte(t,4.6)',\
drawtext=text='history and metadata for one chat thread.':fontcolor=0xe6edf3:fontsize=13:x=20:y=220:enable='gte(t,5.4)',\
drawtext=text='It carries the sliding window of messages':fontcolor=0xe6edf3:fontsize=13:x=20:y=245:enable='gte(t,6.2)',\
drawtext=text='and per-session context.':fontcolor=0xe6edf3:fontsize=13:x=20:y=270:enable='gte(t,7.0)'\
" \
  -c:v libvpx-vp9 -crf 35 -b:v 0 -pix_fmt yuv420p \
  "$OUT" 2> "$ASSETS/ffmpeg.log" && SIZE=$(stat -c%s "$OUT") || SIZE=0

if [ "$SIZE" -gt 0 ]; then
    # Extract a poster frame at t=3s
    ffmpeg -y -loglevel error -i "$OUT" -ss 3 -vframes 1 "$POSTER" 2>&1 | head || true
    echo "    video:    encoded $OUT ($(printf '%d KB' $((SIZE / 1024))))"
else
    echo "    video:    ffmpeg encode failed; VTT emitted only. See $ASSETS/ffmpeg.log"
    tail -5 "$ASSETS/ffmpeg.log" || true
fi
