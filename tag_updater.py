#!/usr/bin/env python3
"""
David Richard Nelson

https://www.ventosum.com
https://github.com/davidrichardnelson/music
https://soundcloud.com/davidrichardnelson
https://www.mixcloud.com/davidrichardnelson

Tool:
MP3 metadata tag updater.

Description:
Updates MP3 artist and title tags automatically based on filename formatting.

Construction:
- Uses Mutagen EasyID3\n- Parses filenames using Artist - Title formatting\n- Batch processes MP3 collections
"""

import os
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import glob


def update_tags(folder_path):
    """
    Update MP3 artist and title metadata using filename parsing.

    Method Construction:
    - Scans the target directory for MP3 files
    - Splits filenames using the pattern:
        Artist - Title.mp3
    - Uses Mutagen EasyID3 for metadata writing
    - Saves updated artist and title tags directly into each file

    Args:
        folder_path (str):
            Directory containing MP3 files.

    Returns:
        None
    """

    search_path = os.path.join(folder_path, '*.mp3')
    mp3_files = glob.glob(search_path)

    if not mp3_files:
        print(f"No MP3 files found in '{folder_path}'")
        return

    for filepath in mp3_files:
        filename = os.path.basename(filepath)
        name_without_ext = os.path.splitext(filename)[0]

        if ' - ' in name_without_ext:
            try:
                artist, title = name_without_ext.split(' - ', 1)

                audio = MP3(filepath, ID3=EasyID3)
                audio['artist'] = artist.strip()
                audio['title'] = title.strip()
                audio.save()

                print(
                    f"Updated tags for: {filename} "
                    f"-> Artist: '{artist.strip()}', "
                    f"Title: '{title.strip()}'"
                )

            except Exception as e:
                print(f"Error processing file {filename}: {e}")

        else:
            print(
                f"Skipping file "
                f"(no ' - ' separator found): {filename}"
            )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=(
            "Update MP3 tags from filenames using the format "
            "'Artist - Title.mp3'"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        'folder',
        type=str,
        nargs='?',
        default='.',
        help=(
            'Folder containing MP3 files. '
            'Defaults to current directory.'
        )
    )

    args = parser.parse_args()

    update_tags(args.folder)
