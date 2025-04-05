import subprocess
import os
import sys

def get_ffmpeg_path():
    """Locate ffmpeg executable"""
    try:
        # Try system PATH first
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return 'ffmpeg'
    except FileNotFoundError:
        # Check common installation paths
        paths = [
            r'C:\ffmpeg\bin\ffmpeg.exe',
            r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
            r'C:\tools\ffmpeg\bin\ffmpeg.exe'
        ]
        for path in paths:
            if os.path.exists(path):
                return path
        raise Exception("FFmpeg not found. Please install it and add to PATH")

def convert_mkv_to_mp4(input_path, output_path=None):
    """Convert MKV to MP4 with proper Windows handling"""
    ffmpeg = get_ffmpeg_path()
    
    # Fix path slashes for Windows
    input_path = os.path.abspath(input_path).replace('/', '\\')
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if output_path is None:
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}.mp4"
    else:
        output_path = os.path.abspath(output_path).replace('/', '\\')
    
    cmd = [
        ffmpeg,
        '-i', input_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-b:a', '192k',
        '-movflags', '+faststart',
        '-y',
        output_path
    ]
    
    try:
        print(f"Converting: {input_path} → {output_path}")
        subprocess.run(cmd, check=True)
        print("Conversion successful!")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e.stderr.decode() if e.stderr else str(e)}")
        raise
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python converter.py input.mkv [output.mp4]")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        convert_mkv_to_mp4(input_file, output_file)
    except Exception as e:
        print(f"Failed to convert: {e}")
        sys.exit(1)