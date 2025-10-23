from yt_dlp import YoutubeDL

def downloader(url, mode, path, noplaylist):

    #Donwload best quality audio only
    if(mode == "mp3"):

        options = {
            "format" : "bestaudio/best",
            "outtmpl" : f"{path}/%(title)s.%(ext)s",
            "noplaylist" : noplaylist,
            "progress_hooks" : [downloaderStatus],

            "postprocessors" : [{
                "key" : "FFmpegExtractAudio",
                "preferredcodec" : "mp3",
                "preferredquality" : "192"
            }],
        }
    
    elif(mode == "mp4"):

        user_choice = 0

        while(user_choice not in [1, 2, 3, 4]):

            print("\nChoose quality")
            print("1. The best quality ")
            print("2. 1080p")
            print("3. 720p")
            print("4. 480p")

            user_choice = int(input("Select (1 - 4): "))
        
        if(user_choice == 1): format_set = "bestvideo+bestaudio/best"
        elif(user_choice == 2): format_set = "bestvideo[height=1080]+bestaudio/best[height=1080]"
        elif(user_choice == 3): format_set = "bestvideo[height=720]+bestaudio/best[height=720]"
        elif(user_choice == 4): format_set = "bestvideo[height=480]+bestaudio/best[height=480]"

        options = {
            "format" : format_set,
            "merge_output_format" : "mp4",
            "outtmpl" : f"{path}/%(title)s.%(ext)s",
            "noplaylist" : noplaylist,
            "progress_hooks" : [downloaderStatus],
        }

    else:
        print("unknow mode. Using best quality by default")
        options = {"format" : "best"}

    with YoutubeDL(options) as confirm: 
        confirm.download([url])
        print("\n✅ All task complete")


        
