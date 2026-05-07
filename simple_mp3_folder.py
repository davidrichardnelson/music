#!/usr/bin/env python3
"""
David Richard Nelson

https://www.ventosum.com
https://github.com/davidrichardnelson/music
https://soundcloud.com/davidrichardnelson
https://www.mixcloud.com/davidrichardnelson

Tool:
Flatten MP3 files into a single collection folder.

Description:
Recursively scans all subdirectories for MP3 files and copies them
into a unified SIMPLE_MP3 directory.

Construction:
- Uses pathlib recursive traversal
- Uses shutil copy operations
- Prevents filename collisions
"""

import shutil
from pathlib import Path

SOURCE_DIR = Path.cwd()
DEST_DIR = SOURCE_DIR / "SIMPLE_MP3"

DEST_DIR.mkdir(exist_ok=True)


def safe_copy(src: Path, dst_dir: Path):
    """
    Safely copy an MP3 file while avoiding filename conflicts.

    Method Construction:
    - Checks for existing filenames
    - Appends incremental suffixes if collisions occur
    - Copies metadata using shutil.copy2

    Args:
        src (Path):
            Source MP3 file.

        dst_dir (Path):
            Destination directory.

    Returns:
        None
    """

    dst = dst_dir / src.name

    if dst.exists():
        stem = src.stem
        suffix = src.suffix
        i = 1

        while (dst_dir / f"{stem}_{i}{suffix}").exists():
            i += 1

        dst = dst_dir / f"{stem}_{i}{suffix}"

    shutil.copy2(src, dst)
    print(f"Copied: {src} -> {dst}")


def main():
    """
    Collect all MP3 files recursively into the SIMPLE_MP3 directory.

    Returns:
        None
    """

    for mp3 in SOURCE_DIR.rglob("*.mp3"):
        if DEST_DIR in mp3.parents:
            continue

        safe_copy(mp3, DEST_DIR)


if __name__ == "__main__":
    main()
