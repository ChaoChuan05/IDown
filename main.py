from core import downloader
from logic import urlCheck, pathCheck, playlistCheck

def main():

    while True:

        while True:
            url = input("Enter your url (playlist or video): ").strip()
            download_path = input("File path: ").strip()

            if not (urlCheck(url) and pathCheck(download_path)): continue
            noplaylist = playlistCheck(url)

            user_choice = 0
            while(user_choice not in [1, 2]):

                print("\nChoose your mode")
                print("1. Best quality audio")
                print("2. Best quality video")

                user_choice = int(input("\nSelect (1 or 2): "))

                if(user_choice == 1): 
                    downloader(url, "mp3", download_path, noplaylist)
                    break

                elif(user_choice == 2): 
                    downloader(url, "mp4", download_path, noplaylist)
                    break

                else: print("\nInvalid choice")

            download_again = input("\nDo you want to download again? (Y/N): ").strip().lower()

            if(download_again != "y"):
                print("\nExit...")
                break

    
if( __name__ == "__main__"): main()


#this only work on linux
#use this command if you want a executable file
#pyinstaller --onefile --add-binary "ffmpeg/ffmpeg:ffmpeg" main.py







 

