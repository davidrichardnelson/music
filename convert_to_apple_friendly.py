#!/usr/bin/env python3
"""
David Richard Nelson

https://www.ventosum.com
https://github.com/davidrichardnelson/music
https://soundcloud.com/davidrichardnelson
https://www.mixcloud.com/davidrichardnelson


Tool:
Batch converts MP4 video files into Apple-friendly H.264/AAC MP4 files.

Description:
This utility scans the current working directory for MP4 files and
converts them into a more compatible format for Apple devices and
software ecosystems such as QuickTime, iOS, macOS, and Final Cut workflows.

Construction:
- Uses FFmpeg through Python subprocess execution
- Converts video using libx264
- Converts audio using AAC
- Writes converted files into an "ip" subdirectory
"""

import os
import subprocess


def convert_to_apple_friendly():
    """
    Convert all MP4 files in the current directory into Apple-friendly MP4 files.

    Method Construction:
    - Detects the current working directory
    - Creates an output folder named "ip"
    - Scans for MP4 files
    - Executes FFmpeg conversion commands for each file
    - Writes converted outputs into the output directory

    FFmpeg Parameters:
    - libx264 video codec
    - yuv420p pixel format for compatibility
    - AAC audio codec
    - +faststart for streaming optimization

    Returns:
        None
    """

    cwd = os.getcwd()
    output_dir = os.path.join(cwd, "ip")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory created: {output_dir}")

    files = [
        f for f in os.listdir(cwd)
        if f.lower().endswith(".mp4")
        and os.path.isfile(os.path.join(cwd, f))
    ]

    if not files:
        print("No MP4 files found to convert.")
        return

    for filename in files:
        input_path = os.path.join(cwd, filename)

        name_without_ext = os.path.splitext(filename)[0]
        output_filename = f"{name_without_ext}.ip.mp4"
        output_path = os.path.join(output_dir, output_filename)

        print(f"Converting: {filename}...")

        command = [
            "ffmpeg",
            "-i", input_path,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-profile:v", "main",
            "-c:a", "aac",
            "-movflags", "+faststart",
            output_path,
            "-y"
        ]

        try:
            subprocess.run(command, check=True)
            print(f"Done: {output_filename}")
        except subprocess.CalledProcessError:
            print(f"Error: Failed to convert {filename}")
        except FileNotFoundError:
            print("Error: FFmpeg not found.")
            return


if __name__ == "__main__":
    convert_to_apple_friendly()
