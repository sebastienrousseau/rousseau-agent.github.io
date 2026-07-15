#!/usr/bin/env bash
# Provide the WebM walkthrough + WebVTT captions + poster PNG under
# public/assets/. Preferred path is to copy the committed source from
# local-assets/media/. FFmpeg is a fallback regenerator for when the
# source is missing (dev bootstrapping) — its drawtext filter needs a
# working font resolver which not every CI runner ships.
set -euo pipefail
cd "$(dirname "$0")/.."

PUB=public
ASSETS="$PUB/assets"
SRC=local-assets/media
mkdir -p "$ASSETS"

# Always ship the WebVTT captions (they're plain text, tiny, checked-in)
cp "$SRC/rousseau-chat.vtt" "$ASSETS/rousseau-chat.vtt"

# Prefer the committed WebM + poster
if [ -f "$SRC/rousseau-chat.webm" ] && [ -s "$SRC/rousseau-chat.webm" ]; then
    cp "$SRC/rousseau-chat.webm" "$ASSETS/rousseau-chat.webm"
    cp "$SRC/rousseau-chat-poster.png" "$ASSETS/rousseau-chat-poster.png"
    SIZE=$(stat -c%s "$ASSETS/rousseau-chat.webm")
    echo "    video:    shipped committed WebM ($(printf '%d KB' $((SIZE / 1024))))"
    exit 0
fi

# Fallback: regenerate via ffmpeg (dev bootstrap only)
if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "    video:    ffmpeg missing and no committed source — skipping" >&2
    exit 1
fi

OUT="$ASSETS/rousseau-chat.webm"
POSTER="$ASSETS/rousseau-chat-poster.png"
# Try to find a usable font on the host (DejaVu ships on Ubuntu runners)
FONT=""
for f in \
  /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf \
  /usr/share/fonts/TTF/DejaVuSans.ttf \
  /usr/share/fonts/liberation-sans/LiberationSans-Bold.ttf \
  /usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf; do
    if [ -f "$f" ]; then FONT="$f"; break; fi
done
if [ -z "$FONT" ]; then
    echo "    video:    no usable font found for ffmpeg drawtext — skipping WebM regen" >&2
    exit 1
fi

ffmpeg -y -loglevel error \
  -f lavfi -i "color=c=0x0d1117:s=820x360:d=8:r=24" \
  -vf "\
drawtext=fontfile=$FONT:text='rousseau chat':fontcolor=0x8b949e:fontsize=13:x=10:y=10:enable='between(t,0,8)',\
drawtext=fontfile=$FONT:text='\$ rousseau chat':fontcolor=0xe6edf3:fontsize=14:x=20:y=50:enable='gte(t,0.6)',\
drawtext=fontfile=$FONT:text='session bc4a-42d1 provider=claudecli':fontcolor=0x8b949e:fontsize=13:x=20:y=75:enable='gte(t,1.4)',\
drawtext=fontfile=$FONT:text='you > What does internal/agent/session.go do?':fontcolor=0x79c0ff:fontsize=13:x=20:y=105:enable='gte(t,2.2)',\
drawtext=fontfile=$FONT:text='-> tool_use read internal/agent/session.go':fontcolor=0xa5d6ff:fontsize=12:x=20:y=135:enable='gte(t,3.0)',\
drawtext=fontfile=$FONT:text='<- tool_result 1847 bytes':fontcolor=0xa5d6ff:fontsize=12:x=20:y=160:enable='gte(t,3.8)',\
drawtext=fontfile=$FONT:text='rousseau > Session holds the conversation':fontcolor=0xe6edf3:fontsize=13:x=20:y=195:enable='gte(t,4.6)',\
drawtext=fontfile=$FONT:text='history and metadata for one chat thread.':fontcolor=0xe6edf3:fontsize=13:x=20:y=220:enable='gte(t,5.4)',\
drawtext=fontfile=$FONT:text='It carries the sliding window of messages':fontcolor=0xe6edf3:fontsize=13:x=20:y=245:enable='gte(t,6.2)',\
drawtext=fontfile=$FONT:text='and per-session context.':fontcolor=0xe6edf3:fontsize=13:x=20:y=270:enable='gte(t,7.0)'\
" \
  -c:v libvpx-vp9 -crf 35 -b:v 0 -pix_fmt yuv420p \
  "$OUT"
ffmpeg -y -loglevel error -i "$OUT" -ss 3 -vframes 1 "$POSTER"
SIZE=$(stat -c%s "$OUT")
echo "    video:    regenerated $(printf '%d KB' $((SIZE / 1024))) with ffmpeg"
