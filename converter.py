import subprocess
import os

def convert_mkv_to_mp4(input_path, output_path=None):
    """
    Convert MKV video file to MP4 format while preserving audio streams
    
    Args:
        input_path (str): Path to input MKV file
        output_path (str, optional): Path for output MP4 file. 
                                    If None, uses same directory with .mp4 extension
    Returns:
        str: Path to converted file
    """
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if output_path is None:
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}.mp4"
    
    # FFmpeg command:
    # -c:v copy -> Copy video stream without re-encoding (preserves quality)
    # -c:a aac  -> Convert audio to AAC (widest compatibility)
    # -movflags +faststart -> Enable streaming playback
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-c:v', 'copy',          # Copy video stream
        '-c:a', 'aac',           # Convert audio to AAC
        '-b:a', '192k',          # Audio bitrate
        '-movflags', '+faststart', # Web optimization
        '-y',                    # Overwrite output
        output_path
    ]
    
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE)
        print(f"Successfully converted: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        print(f"Conversion failed: {e.stderr.decode()}")
        raise
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

# Example usage
if __name__ == "__main__":
    input_file = "deadpool.mkv"  # Change to your file
    output_file = "output.mp4" # Optional
    
    try:
        convert_mkv_to_mp4(input_file, output_file)
    except Exception as e:
        print(f"Conversion error: {e}")