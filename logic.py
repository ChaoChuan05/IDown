from yt_dlp import YoutubeDL
import os

def pathCheck(path) -> bool:
    try:

        #path doesn't exits, create it
        if not (os.path.exists(path)):
            os.makedirs(path)
            print(f"\nCreated directory: {path}")
        
        #path exists but not a directory
        elif not (os.path.isdir(path)):
            print(f"\nPath exists but is not a directory: {path}")
            return False
        
        #path is valid
        print("Path is valid to use")
        return True
    
    except Exception as error:
        print(f"\nFailed to validate or create directory")
        return False
    
        
def urlCheck(url) -> bool:
    try:
        with YoutubeDL({}) as UrlCheck:
            UrlCheck.extract_info(url, download=False)
            print("\nURL is valid and supported!")
            return True

    except Exception as error:
        print(f"\nInvalid URL or unsupported: {error}")
        return False


def playlistCheck(url):

    """Return true if single video, false if playlist, none on error"""

    options = {
        "quiet" : True,
        "extract_flat" : True
    }

    try:
        with YoutubeDL(options) as DownloadCheck:
            info = DownloadCheck.extract_info(url, download=False)
            return "entries" not in info
        
    except Exception as error:
        print(f"\nError checking URL: {error}")
        return None