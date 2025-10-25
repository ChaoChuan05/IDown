from common_import import *

# Determine base folder depending on if running from PyInstaller or script
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # PyInstaller temp folder
else:
    base_path = os.path.abspath(".")

#path inside packaged EXE
ffmpeg_path = os.path.join(base_path, "ffmpeg_window", "ffmpeg.exe")

# Use ffmpeg
try:
    subprocess.run(
        [ffmpeg_path, "-version"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    
except Exception as e:
    print(f"FFmpeg not found or failed to run: {e}")