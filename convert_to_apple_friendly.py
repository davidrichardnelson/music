import os
import subprocess

def convert_to_apple_friendly():
    # Define paths
    cwd = os.getcwd()
    output_dir = os.path.join(cwd, 'ip')
    
    # Create 'ip' folder if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory created: {output_dir}")

    # Get all .mp4 files in the current directory
    files = [f for f in os.listdir(cwd) if f.lower().endswith('.mp4') and os.path.isfile(os.path.join(cwd, f))]

    if not files:
        print("No MP4 files found to convert.")
        return

    for filename in files:
        input_path = os.path.join(cwd, filename)
        
        # Prepare output filename (e.g., video.ip.mp4)
        name_without_ext = os.path.splitext(filename)[0]
        output_filename = f"{name_without_ext}.ip.mp4"
        output_path = os.path.join(output_dir, output_filename)

        print(f"Converting: {filename}...")

        # Your specific FFmpeg command
        command = [
            'ffmpeg',
            '-i', input_path,
            '-c:v', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-profile:v', 'main',
            '-c:a', 'aac',
            '-movflags', '+faststart',
            output_path,
            '-y'  # Overwrite file if it already exists in the 'ip' folder
        ]

        try:
            subprocess.run(command, check=True)
            print(f"Done: {output_filename}")
        except subprocess.CalledProcessError:
            print(f"Error: Failed to convert {filename}")
        except FileNotFoundError:
            print("Error: FFmpeg not found. Please install it and add it to your system PATH.")
            return

if __name__ == "__main__":
    convert_to_apple_friendly()

