import os
import subprocess

def format_audio(input_path: str, output_path: str, output_format: str, mono: bool = True, target_sr: int = 16000):
    """
    Convert audio using ffmpeg CLI to the desired format/sample rate.
    Requires: ffmpeg installed and on PATH.
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File {input_path} not found")

    channels = '1' if mono else '2'
    # Ensure output_path has the right extension if missing
    root, ext = os.path.splitext(output_path)
    if not ext:
        output_path = f"{root}.{output_format}"

    cmd = [
        'ffmpeg', '-y',
        '-i', input_path,
        '-ac', channels,
        '-ar', str(target_sr),
        output_path
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"ffmpeg failed: {e.stderr.decode(errors='ignore')}")

    return output_path
