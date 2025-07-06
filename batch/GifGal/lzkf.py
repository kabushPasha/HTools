import os
import glob
import subprocess
import sys

def get_keyframe_timestamps(video_file):
    cmd = [
        "ffprobe",
        "-select_streams", "v",
        "-skip_frame", "nokey",
        "-show_frames",
        "-print_format", "csv",
        video_file,
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    lines = result.stdout.splitlines()

    timestamps = []
    for line in lines:
        parts = line.split(',')
        if len(parts) > 5:
            ts_str = parts[5]
            try:
                # Validate it's a float number before adding
                ts = float(ts_str)
                timestamps.append(ts)
            except ValueError:
                # Skip non-numeric timestamps safely
                pass
    return timestamps

def process_videos_in_folder(folder_path, extensions=("*.mp4", "*.mov", "*.mkv", "*.avi")):
    video_files = []
    for ext in extensions:
        video_files.extend(glob.glob(os.path.join(folder_path, ext)))

    if not video_files:
        print("No video files found.")
        return

    for video in video_files:
        base_name = os.path.splitext(os.path.basename(video))[0]
        txt_path = os.path.join(folder_path, f"{base_name}.txt")

        if os.path.exists(txt_path):
            print(f"⏭️ Skipping {video} because keyframe file already exists.")
            continue

        keyframes = get_keyframe_timestamps(video)
        if not keyframes:
            print(f"No keyframes found for {video}")
            continue

        with open(txt_path, 'w') as f:
            f.write(','.join(f"{ts:.3f}" for ts in sorted(keyframes)))
        print(f"✅ Keyframes saved to: {txt_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_keyframes.py <source_folder>")
        sys.exit(1)

    src_folder = sys.argv[1].replace(os.sep, "/")
    print(f"Processing videos in folder: {src_folder}")
    process_videos_in_folder(src_folder)
