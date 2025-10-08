from yt_dlp import YoutubeDL
import os

def pathCheck(path):
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
    
        
def urlCheck(url):
    try:
        with YoutubeDL({}) as UrlCheck:
            UrlCheck.extract_info(url, download=False)
            print("\nURL is valid and supported!")
            return True

    except Exception as error:
        print(f"\nInvalid URL or unsupported: {error}")
        return False


def playlistCheck(url):

    options = {
        "quiet" : True,
        "extract_flat" : True
    }

    try:
        with YoutubeDL(options) as DownloadCheck:
            info = DownloadCheck.extract_info(url, download=False)
            
            if("entries" in info):
                print("\nThis URL is playlist")
                playlist_confirm = input("\nDo you want to download the entire playlsit? (Y/N): ").strip().lower() #strip remove whitespace, while lower force everything lowercase
                noplaylist = playlist_confirm != "y"
                return noplaylist

            else: 
                print("\nThis is a not a playlist")
                return True
        
    except Exception as error:
        print(f"\nError checking URL: {error}")
        return False