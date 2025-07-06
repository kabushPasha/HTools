import subprocess

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
            try:
                ts = float(parts[5])
                timestamps.append(ts)
            except ValueError:
                continue
    return timestamps
