import shutil #Check if a program exists, copying files, deleting directories, etc.
import platform #Detect operation system and environment
import subprocess #Run system commands 
import sys #Control the python program itself

def checkFFmpeg():
    if(shutil.which("ffmpeg")) is not None:
        print("✅ FFmpeg is already installed")
        return True
    
    else:
        print("✅ FFmpeg not found on this system")
        return False

def installFFmpeg():

    system = platform.system()
    print(f"Attempt to install FFmpeg for {system}")

    try:
        if(system == "Window"): 
            subprocess.run(["winget", "install", "-e", "--id", "Gyan.FFmpeg"], check=True)

        elif(system == "Linux"): 
            subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"], check=True)

        elif(system == "Darwin"):  
            subprocess.run(["brew", "install", "ffmpeg"], check=True)

        else: 
            print("Unsupported OS, please install FFmped manually") 
            return False
        
        print("FFmpeg installed successfully!")
        return True

    except Exception as error:
        print(f"Failed to install FFmpeg: {error}")
        return False
    
def ensureFFmpeg():
    if not checkFFmpeg():
        user_choice = input("Do you want to instal FFmpeg automatically (Y/N): ")

        if(user_choice == "Y" and user_choice == "y"): 
            installFFmpeg()

        else: 
            print("Please install FFmpeg manually before continuing!")
            sys.exit(1)