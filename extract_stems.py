#!/usr/bin/env python3
"""
David Richard Nelson

https://www.ventosum.com
https://github.com/davidrichardnelson/music
https://soundcloud.com/davidrichardnelson
https://www.mixcloud.com/davidrichardnelson


Tool:
Extract individual Native Instruments STEM audio channels.

Description:
This utility processes .stem.m4a files and extracts the embedded
audio stems such as drums, bass, instrumental, and vocals.

Construction:
- Uses FFmpeg stream mapping
- Reads metadata using Mutagen
- Writes tagged WAV or M4A files
- Supports full extraction or vocals-only extraction
"""

import os
import argparse
import subprocess
import sys

from mutagen.mp4 import MP4
from mutagen.id3 import TIT2, TALB, TPE1
from mutagen import File as MutagenFile


def extract_stems(input_path, output_formats, vocals_only=False):
    """
    Extract stems from Native Instruments STEM files.

    Method Construction:
    - Detects all .stem.m4a files in the target directory
    - Reads metadata from the source file
    - Uses FFmpeg stream mapping to isolate stems
    - Exports stems to WAV or M4A
    - Re-applies metadata tags to exported files

    Stem Mapping:
    0 = Master
    1 = Drums
    2 = Bass
    3 = Instrumental
    4 = Vocals

    Args:
        input_path (str):
            Directory containing .stem.m4a files.

        output_formats (list):
            List of output formats such as ["wav"] or ["m4a"].

        vocals_only (bool):
            If True, only the vocal stem is extracted.

    Returns:
        None
    """

    full_stem_map = {
        "1": "drums",
        "2": "bass",
        "3": "inst",
        "4": "vocals"
    }

    stem_map = {"4": "vocals"} if vocals_only else full_stem_map

    input_path = os.path.expanduser(input_path)

    try:
        files = [f for f in os.listdir(input_path) if f.endswith(".stem.m4a")]
    except FileNotFoundError:
        print(f"Error: Path not found: {input_path}")
        return

    if not files:
        print("No STEM files found.")
        return

    for file in files:
        base_name = file.replace(".stem.m4a", "")
        input_file = os.path.join(input_path, file)

        original_title = base_name
        original_artist = "Unknown Artist"
        original_album = "Unknown Album"

        try:
            audio = MP4(input_file)
            original_title = audio.get("\xa9nam", [base_name])[0]
            original_artist = audio.get("\xa9ART", ["Unknown Artist"])[0]
            original_album = audio.get("\xa9alb", ["Unknown Album"])[0]
        except Exception:
            print(f"Metadata fallback used for {file}")

        for fmt in output_formats:
            cmd = [
                "ffmpeg",
                "-i", input_file,
                "-y",
                "-hide_banner",
                "-loglevel", "error"
            ]

            output_files = []

            for stream_id, name in stem_map.items():
                output_name = f"{base_name}_{name}.{fmt}"
                output_path = os.path.join(input_path, output_name)

                cmd.extend(["-map", f"0:a:{stream_id}"])

                if fmt == "m4a":
                    cmd.extend(["-c", "copy"])

                cmd.append(output_path)
                output_files.append((output_path, name))

            subprocess.run(cmd)

            for file_path, stem_name in output_files:
                new_title = f"{original_title} {stem_name}"

                try:
                    audio_out = MutagenFile(file_path)

                    if fmt == "m4a":
                        audio_out["\xa9nam"] = [new_title]
                        audio_out["\xa9ART"] = [original_artist]
                        audio_out["\xa9alb"] = [original_album]

                    elif fmt == "wav":
                        if not audio_out.tags:
                            audio_out.add_tags()

                        audio_out.tags.add(TIT2(encoding=3, text=[new_title]))
                        audio_out.tags.add(TPE1(encoding=3, text=[original_artist]))
                        audio_out.tags.add(TALB(encoding=3, text=[original_album]))

                    audio_out.save()

                except Exception as e:
                    print(f"Tagging failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extract stems from Native Instruments STEM files."
    )

    parser.add_argument("--path", type=str, default=os.getcwd())
    parser.add_argument("--wav", action="store_true")
    parser.add_argument("--m4a", action="store_true")
    parser.add_argument("--vocals", action="store_true")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    formats = []

    if args.wav:
        formats.append("wav")

    if args.m4a:
        formats.append("m4a")

    if not formats:
        print("Specify at least one output format.")
    else:
        extract_stems(args.path, formats, vocals_only=args.vocals)
        print("Finished.")
