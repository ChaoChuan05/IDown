from core import downloader, playlistCheck, urlCheck, pathCheck

def main():

    #Initialise
    download_again = 'y'
    user_choice = 0

    while(download_again == "y"):

        while True:
            url = input("Enter your url (playlist or video): ").strip()
            download_path = input("File path: ").strip()

            url_valid = urlCheck(url)
            path_valid = pathCheck(download_path)

            if(url_valid and path_valid): 
                print("Both URL and Path are vlaid, ready to donwload")
                break

            else:
                if(not url_valid): print("Invalid URL, please try again!")
                elif(not path_valid): print("Invalid path, please try again!")

        if(playlistCheck(url)):
            print("This is a playlist!")
            playlist_confirm = input("Do you want to download the entire playlsit? (Y/N): ").strip().lower() #strip remove whitespace, while lower force everything lowercase
            noplaylist = playlist_confirm != "y"
        
        else:
            print("This is a not a playlist")
            noplaylist = True

        while(user_choice not in [1, 2]):

            print("\nChoose your mode")
            print("1. Best quality audio")
            print("2. Best quality video")

            user_choice = int(input("Select (1 or 2): "))

            if(user_choice == 1): downloader(url, "mp3", download_path, noplaylist)
            elif(user_choice == 2): downloader(url, "mp4", download_path, noplaylist)
            else: print("Invalid choice")

        download_again = input("Do you want to download again? (Y/N): ").strip().lower()
    
if( __name__ == "__main__"): main()











 

