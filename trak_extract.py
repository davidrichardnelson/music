#!/usr/bin/env python3

import os
import shutil
import argparse
import subprocess

def extract_all_trak_files(input_dir, output_base):
    os.makedirs(output_base, exist_ok=True)
    
    # Filter for .trak files only
    trak_files = [f for f in os.listdir(input_dir) if f.lower().endswith(".trak")]
    
    if not trak_files:
        print(f"No .trak files found in {input_dir}")
        return

    for filename in trak_files:
        trak_path = os.path.join(input_dir, filename)
        set_name = os.path.splitext(filename)[0]
        final_folder = os.path.join(output_base, set_name)
        temp_extract = os.path.join(output_base, f"temp_{set_name}")
        
        os.makedirs(final_folder, exist_ok=True)
        print(f"Processing: {set_name}...")

        try:
            # Use system 'unzip' to handle Traktor's non-standard zip headers
            subprocess.run(['unzip', '-q', trak_path, '-d', temp_extract], check=True)
            
            m3u_lines = []
            valid_exts = ('.wav', '.aif', '.aiff', '.mp3', '.flac')

            for root, _, files in os.walk(temp_extract):
                for file in files:
                    if file.lower().endswith(valid_exts):
                        src = os.path.join(root, file)
                        dest = os.path.join(final_folder, file)
                        shutil.copy2(src, dest)
                        m3u_lines.append(file)

            if m3u_lines:
                m3u_path = os.path.join(final_folder, f"{set_name}.m3u")
                with open(m3u_path, "w") as f:
                    f.write("#EXTM3U\n")
                    for line in m3u_lines:
                        f.write(f"{line}\n")
                print(f" Successfully created {set_name}.m3u")
            else:
                print(f" No audio files found in {filename}")

        except Exception as e:
            print(f" Error processing {filename}: {e}")
        finally:
            if os.path.exists(temp_extract):
                shutil.rmtree(temp_extract)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch extract Traktor .trak files for Rekordbox")
    parser.add_argument("input_folder", help="Directory containing .trak files")
    parser.add_argument("-o", "--output", default="./Extracted_Sets", help="Output directory")
    args = parser.parse_args()
    
    # Expand user path (e.g., ~/) for the input directory
    extract_all_trak_files(os.path.expanduser(args.input_folder), args.output)


