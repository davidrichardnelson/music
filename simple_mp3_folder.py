#!/usr/bin/env python3
import shutil
from pathlib import Path

SOURCE_DIR = Path.cwd()
DEST_DIR = SOURCE_DIR / "SIMPLE_MP3"

DEST_DIR.mkdir(exist_ok=True)

def safe_copy(src: Path, dst_dir: Path):
    dst = dst_dir / src.name

    if dst.exists():
        stem = src.stem
        suffix = src.suffix
        i = 1
        while (dst_dir / f"{stem}_{i}{suffix}").exists():
            i += 1
        dst = dst_dir / f"{stem}_{i}{suffix}"

    shutil.copy2(src, dst)
    print(f"Copied: {src} → {dst}")

def main():
    for mp3 in SOURCE_DIR.rglob("*.mp3"):
        if DEST_DIR in mp3.parents:
            continue
        safe_copy(mp3, DEST_DIR)

if __name__ == "__main__":
    main()
