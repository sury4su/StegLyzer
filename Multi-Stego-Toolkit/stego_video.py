import os
import subprocess
import json

SUPPORTED_VIDEO = [".mp4", ".mkv", ".mov", ".avi", ".webm", ".flv", ".wmv"]

FFMPEG_PATH = os.path.normpath(r"C:\Users\LENOVO\OneDrive\Desktop\ImageStegoAnalyzer\Stego Analyser\Multi-Stego-Toolkit\Tools\ffmpeg.exe")
FFPROBE_PATH = os.path.normpath(r"C:\Users\LENOVO\OneDrive\Desktop\ImageStegoAnalyzer\Stego Analyser\Multi-Stego-Toolkit\Tools\ffprobe.exe")

def is_supported_video(path):
    """Check if the video has a supported extension."""
    ext = os.path.splitext(path)[1].lower()
    return ext in SUPPORTED_VIDEO

def embed_text_in_video(input_path, output_path, secret_text):
    """
    Embed a secret text message into video metadata using FFmpeg.
    """
    if not is_supported_video(input_path):
        return False, "❌ Unsupported video format."

    try:
        cmd = [
            FFMPEG_PATH, "-y",                
            "-i", input_path,
            "-metadata", f"comment={secret_text}",
            "-codec", "copy",                    
            output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True, f"✅ Message embedded in video: {output_path}"

    except subprocess.CalledProcessError:
        return False, "❌ FFmpeg failed to process the video."
    except Exception as e:
        return False, f"❌ Unexpected error: {str(e)}"

def extract_text_from_video(video_path):
    """
    Extract the secret text from video metadata using FFprobe.
    """
    if not is_supported_video(video_path):
        return False, "❌ Unsupported video format."

    try:
        cmd = [
            FFPROBE_PATH,
            "-v", "quiet",                      # Suppress all output
            "-print_format", "json",            # Output as JSON
            "-show_format",                     # Show format tags
            video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        metadata = json.loads(result.stdout)

        comment = metadata.get("format", {}).get("tags", {}).get("comment")
        if comment:
            return True, comment
        else:
            return False, "⚠️ No hidden message found in metadata."

    except subprocess.CalledProcessError:
        return False, "❌ FFprobe failed to analyze the video."
    except Exception as e:
        return False, f"❌ Unexpected error: {str(e)}"
