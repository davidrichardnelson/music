#!/usr/bin/env python3

import os
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import glob

def update_tags(folder_path):
    """
    Splits MP3 filenames by ' - ' and updates the 'artist' and 'title' tags.
    """
    # Find all MP3 files in the specified folder
    search_path = os.path.join(folder_path, '*.mp3')
    mp3_files = glob.glob(search_path)

    if not mp3_files:
        print(f"No MP3 files found in '{folder_path}'")
        return

    for filepath in mp3_files:
        filename = os.path.basename(filepath)
        # Remove the .mp3 extension for splitting
        name_without_ext = os.path.splitext(filename)[0]

        if ' - ' in name_without_ext:
            try:
                artist, title = name_without_ext.split(' - ', 1)
                
                # Use EasyID3 interface for simple tag editing
                audio = MP3(filepath, ID3=EasyID3)
                audio['artist'] = artist.strip()
                audio['title'] = title.strip()
                audio.save()
                print(f"Updated tags for: {filename} -> Artist: '{artist.strip()}', Title: '{title.strip()}'")

            except Exception as e:
                print(f"Error processing file {filename}: {e}")
        else:
            print(f"Skipping file (no ' - ' separator found): {filename}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Update MP3 tags (artist and title) from filenames using the format 'Artist - Title.mp3'.",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('folder', type=str, nargs='?', default='.',
                        help='The path to the folder containing MP3 files. Defaults to the current directory.')
    
    # Add an explicit --help flag functionality that argparse handles automatically

    args = parser.parse_args()
    update_tags(args.folder)
