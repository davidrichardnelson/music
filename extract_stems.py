#!/usr/bin/env python3

import os
import argparse
import subprocess
import sys
from mutagen.mp4 import MP4
from mutagen.id3 import TIT2, TALB, TPE1
from mutagen import File as MutagenFile

def extract_stems(input_path, output_formats, vocals_only=False):
    """
    Stream Mapping for NI Stems: 
    0: Master, 1: Drums, 2: Bass, 3: Other (Inst), 4: Vocals
    """
    full_stem_map = {
        "1": "drums",
        "2": "bass",
        "3": "inst",
        "4": "vocals"
    }

    # Filter map if --vocals flag is present
    if vocals_only:
        stem_map = {"4": "vocals"}
    else:
        stem_map = full_stem_map

    input_path = os.path.expanduser(input_path)
    
    try:
        files = [f for f in os.listdir(input_path) if f.endswith(".stem.m4a")]
    except FileNotFoundError:
        print(f"Error: The path '{input_path}' does not exist.")
        return

    if not files:
        print(f"No .stem.m4a files found in: {input_path}")
        return

    for file in files:
        base_name = file.replace(".stem.m4a", "")
        input_file = os.path.join(input_path, file)
        
        original_title, original_artist, original_album = base_name, 'Unknown Artist', 'Unknown Album'
        try:
            audio = MP4(input_file)
            original_title = audio.get('\xa9nam', [base_name])[0]
            original_artist = audio.get('\xa9ART', ['Unknown Artist'])[0]
            original_album = audio.get('\xa9alb', ['Unknown Album'])[0]
        except Exception:
            print(f"Note: Could not read full metadata from {file}, using filenames as default.")

        for fmt in output_formats:
            mode_text = "VOCALS" if vocals_only else "ALL STEMS"
            print(f"--- Extracting {mode_text} ({fmt.upper()}) from: {file} ---")
            
            cmd_base = ["ffmpeg", "-i", input_file, "-y", "-hide_banner", "-loglevel", "error"]
            output_files_to_tag = []

            # We run a single FFmpeg command per format for efficiency
            cmd = list(cmd_base)
            for stream_id, name in stem_map.items():
                output_name = f"{base_name}_{name}.{fmt}"
                output_file_path = os.path.join(input_path, output_name)
                
                cmd.extend(["-map", f"0:a:{stream_id}"])
                if fmt == "m4a":
                    cmd.extend(["-c", "copy"])
                cmd.append(output_file_path)
                output_files_to_tag.append((output_file_path, name))
            
            subprocess.run(cmd)

            for file_path, stem_name in output_files_to_tag:
                new_title = f"{original_title} {stem_name}"
                try:
                    audio_out = MutagenFile(file_path)
                    if fmt == "m4a":
                        audio_out['\xa9nam'] = [new_title]
                        audio_out['\xa9ART'] = [original_artist]
                        audio_out['\xa9alb'] = [original_album]
                    elif fmt == "wav":
                        if not audio_out.tags:
                            audio_out.add_tags()
                        audio_out.tags.add(TIT2(encoding=3, text=[new_title]))
                        audio_out.tags.add(TPE1(encoding=3, text=[original_artist]))
                        audio_out.tags.add(TALB(encoding=3, text=[original_album]))
                    audio_out.save()
                except Exception as e:
                    print(f"Warning: Could not tag {os.path.basename(file_path)}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fast batch extraction of individual stems from .stem.m4a files.",
        epilog="Example: ./extract_stems.py --path ~/Music/Stems --wav --vocals",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--path", type=str, default=os.getcwd(), help="Target directory")
    parser.add_argument("--wav", action="store_true", help="Extract into .wav files")
    parser.add_argument("--m4a", action="store_true", help="Extract into .m4a files")
    parser.add_argument("--vocals", action="store_true", help="Only extract the vocal stem")

    """
    # move to clean mp3 for rekordbox
    mkdir converted; for f in *.m4a; do ffmpeg -i "$f" -codec:a libmp3lame -b:a 320k -ar 44100 "converted/${f%.m4a}.mp3"; done
    """
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    
    formats = []
    if args.wav: formats.append("wav")
    if args.m4a: formats.append("m4a")
    
    if not formats:
        print("Error: Specify at least one format (--wav or --m4a).")
    else:
        extract_stems(args.path, formats, vocals_only=args.vocals)
        print("\nFinished!")
