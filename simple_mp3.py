#!/usr/bin/env python3
"""
David Richard Nelson

https://www.ventosum.com
https://github.com/davidrichardnelson/music
https://soundcloud.com/davidrichardnelson
https://www.mixcloud.com/davidrichardnelson

Tool:
Simple MP3 conversion utility.

Description:
Converts WAV, M4A, and MP3 source files into organized MP3 folders
using FFmpeg while preserving metadata.

Construction:
- Uses pathlib for filesystem traversal
- Uses FFmpeg for encoding
- Creates one output folder per source file
"""

import subprocess
from pathlib import Path

SOURCE_DIR = Path.cwd()
TARGET_BITRATE = "320k"

AUDIO_EXTS = {".wav", ".m4a", ".mp3"}


def convert_to_mp3(src_path: Path):
    """
    Convert a source audio file into a high bitrate MP3.

    Method Construction:
    - Creates an output directory matching the source filename
    - Executes FFmpeg MP3 conversion
    - Preserves source metadata

    Args:
        src_path (Path):
            Source audio file path.

    Returns:
        None
    """

    stem_name = src_path.stem
    out_dir = src_path.parent / stem_name
    out_dir.mkdir(exist_ok=True)

    out_mp3 = out_dir / f"{stem_name}.mp3"

    cmd = [
        "ffmpeg",
        "-y",
        "-i", str(src_path),
        "-vn",
        "-acodec", "libmp3lame",
        "-ab", TARGET_BITRATE,
        "-map_metadata", "0",
        str(out_mp3),
    ]

    print(f"Converting: {src_path.name}")
    subprocess.run(cmd, check=True)


def main():
    """
    Scan the current directory and convert supported audio files.

    Supported Extensions:
    - WAV
    - M4A
    - MP3

    Returns:
        None
    """

    for file in SOURCE_DIR.iterdir():
        if file.is_file() and file.suffix.lower() in AUDIO_EXTS:
            convert_to_mp3(file)


if __name__ == "__main__":
    main()
