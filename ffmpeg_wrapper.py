from common_import import *

# Determine base folder depending on if running from PyInstaller or script
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS  # PyInstaller temp folder
else:
    base_path = os.path.abspath(".")

ffmpeg_path = r"D:\Code\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe"

# Use ffmpeg
subprocess.run([ffmpeg_path, "-version"])