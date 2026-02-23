#!/usr/bin/env python3

import subprocess
from pathlib import Path

# ===== CONFIG =====
SOURCE_DIR = Path.cwd()
TARGET_BITRATE = "320k"     # mp3 quality
# ==================

AUDIO_EXTS = {".wav", ".m4a", ".mp3"}

def convert_to_mp3(src_path: Path):
    stem_name = src_path.stem
    out_dir = src_path.parent / stem_name
    out_dir.mkdir(exist_ok=True)

    out_mp3 = out_dir / f"{stem_name}.mp3"

    cmd = [
        "ffmpeg",
        "-y",                    # overwrite
        "-i", str(src_path),
        "-vn",                   # no video
        "-acodec", "libmp3lame",
        "-ab", TARGET_BITRATE,
        "-map_metadata", "0",    # keep metadata if present
        str(out_mp3),
    ]

    print(f"Converting: {src_path.name} → {out_mp3}")
    subprocess.run(cmd, check=True)

def main():
    for file in SOURCE_DIR.iterdir():
        if file.is_file() and file.suffix.lower() in AUDIO_EXTS:
            convert_to_mp3(file)

if __name__ == "__main__":
    main()
