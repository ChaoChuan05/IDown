from yt_dlp import YoutubeDL
from setting_page_manager import load_setting
import threading
import os

progress = 0 #Progress bar 

#Important before proceed: the function need to implement root.after since it's using thread
#The UI might crash or freeze if we not using it

def start_download(root, url, progress_bar, progress_label, app_entry, show_pop_up) -> None:
    """
    Start the background download process

        root            - the Tkinter root (for .after)
        url             - the URL string
        progress_bar    - the CTkProgressBar instance
        progress_label  - the CTkLabel instance
        app_entry       - the CTkEntry instance
        show_pop_up     - callback function from main to show messages
    """
    global progress
    progress = 0 #reset everytime

    #1. Validate the URL
    url = url.strip()

    if not url: 
        show_pop_up("Please insert a URL first!", "#E30B5C")
        return

    #2. Prepare UI
    setup_progress_ui(progress_bar, progress_label)
    root.update_idletasks()

    #3. Start the background thread (Check URL > playlist > mp3/mp4 > download)
    threading.Thread(
        target=background_check,
        args=(root, url, progress_bar, progress_label, app_entry, show_pop_up),
        daemon=True
    ).start()

def setup_progress_ui(progress_bar, progress_label) -> None:
    progress_bar.place(
        relx=0.5,
        rely=0.5,
        relwidth=0.5,
        anchor="center"
    )

    progress_label.place(
        relx=0.5,
        rely=0.6,
        relwidth=0.5,
        anchor="center"
    )

    progress_bar.set(progress)
    progress_label.configure(text="Checking URL Path")

def background_check(root, url, progress_bar, progress_label, app_entry, show_pop_up) -> None:
    global progress

    # Path check > Url check > playlist check > mp3
    #Use nested function because to ensure all function in one thread 

    def path_step() -> None:
        if not path_check(root, progress_bar, progress_label): return
        root.after(500, url_step)

    def url_step() -> None:
        if not check_url(root, url, progress_bar, progress_label, app_entry, show_pop_up): return
        root.after(500, playlist_step)

    def playlist_step() -> None:
        if not check_playlist(root, url, progress_bar, progress_label, app_entry, show_pop_up): return
        root.after(500, install_step)

    def install_step() -> None:
        threading.Thread(
            target=install,
            args=(root, url,  progress_bar, progress_label, show_pop_up),
            daemon=True
        ).start()

    #start the chain progress
    path_step()
    
def check_url(root, url, progress_bar, progress_label, app_entry, show_pop_up) -> bool:
    """Run the URL check in a seperate thread"""
    global progress

    try:

        root.after(0, lambda: progress_label.configure(text="Checking URL..."))

        #To avoid fetching whole video
        options = {
            "quiet" : True,
            "extract_flat" : True
        }

        with YoutubeDL(options) as UrlCheck:
            UrlCheck.extract_info(url, download=False)

        progress += 0.25
        root.after(0, lambda: progress_bar.set(progress))
        return True

    except Exception:
        root.after(0, lambda: progress_bar.place_forget())
        root.after(0, lambda: progress_label.configure(text=""))
        root.after(0, lambda: app_entry.delete(0, "end"))
        root.after(0, lambda: show_pop_up("Invalid or Unsupported URL!", "#E30B5C"))
        return False
   
def check_playlist(root, url, progress_bar, progress_label, app_entry, show_pop_up) -> bool:

    global progress

    try:

        settings = load_setting()
        allow_playlist = settings.get("allow_playlist", True)

        options = {
            "quiet" : True,
            "extract_flat" : True
        }

        with YoutubeDL(options) as DownloadCheck:
            info = DownloadCheck.extract_info(url, download=False)
            is_playlist = "entries" in info

        if is_playlist and not allow_playlist: 
            progress += 0.25
            root.after(0, lambda: progress_bar.set(progress))
            root.after(0, lambda: progress_label.configure(text="Playlist is not allowed"))
            return True
        
        elif is_playlist and allow_playlist:
            progress += 0.25
            root.after(0, lambda: progress_bar.set(progress))
            root.after(0, lambda: progress_label.configure(text="Playlist is allowed"))
            return True

        else:
            progress += 0.25
            root.after(0, lambda: progress_bar.set(progress))
            root.after(0, lambda: progress_label.configure(text="Single video or audio is detected!")) 
            return True
            

    except Exception:  
        root.after(0, lambda: progress_bar.place_forget())
        root.after(0, lambda: progress_label.configure(text=""))
        root.after(0, lambda: app_entry.delete(0, "end"))
        root.after(0, lambda: show_pop_up("The playlist might not supported!", "#E30B5C"))
        return False
        
def path_check(root, progress_bar, progress_label) -> bool:

    global progress

    settings = load_setting()
    path = settings.get("download_path", os.path.join(os.path.expanduser("~"), "Downloads"))

    root.after(0, lambda: progress_label.configure(text="Check path"))

    if not os.path.isdir(path):

        try:
            os.makedirs(path)
            root.after(0, lambda: progress_label.configure(text="Create directory..."))
            progress += 0.25
            root.after(0, lambda: progress_bar.set(progress))
            return True

        except Exception: 
            root.after(0, lambda: progress_label.configure(text="Custom path failed! Using default path"))
            path = os.path.join(os.path.expanduser("~"), "Downloads")
            progress += 0.25
            root.after(0, lambda: progress_bar.set(progress))
            return False

    else: 
        progress += 0.25
        root.after(0, lambda: progress_bar.set(progress))
        return True

def install(root, url, progress_bar, progress_label, show_pop_up) -> None:
    global progress

    settings = load_setting()
    allow_mp3 = settings.get("always_mp3", True)
    path = settings.get("download_path", os.path.join(os.path.expanduser("~"), "Downloads"))
    allow_playlist = settings.get("allow_playlist", True)
    progress_hook = make_install_progress(root, progress_bar, progress_label, show_pop_up)


    if allow_mp3:

        options = {
            "format" : "bestaudio/best",
            "outtmpl" : f"{path}/%(title)s.%(ext)s",
            "noplaylist" : not allow_playlist,
            "progress_hooks" : [progress_hook],

            "postprocessors" : [{
                "key" : "FFmpegExtractAudio",
                "preferredcodec" : "mp3",
                "preferredquality" : "192"
            }],

            "headers" : {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            }
        }
        
    else: 
        options = {
            "format" : "bestvideo+bestaudio/best",
            "merge_output_format" : "mp4",
            "outtmpl" : f"{path}/%(title)s.%(ext)s",
            "noplaylist" : not allow_playlist,
            "progress_hooks" : [progress_hook],

            "headers" : {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            },

            "ffmpeg_location" : "../bin"
        }

    progress += 0.25
    root.after(0, lambda: progress_bar.set(progress))
    root.after(0, lambda: progress_label.configure(text="Prepare to download..."))

    with YoutubeDL(options) as confirm: confirm.download([url])

def make_install_progress(root, progress_bar, progress_label, show_pop_up):

    #progress hooks are always called with exactly one argument, hence nested function is implemented
    def install_progress(d : dict):

        root.after(0, lambda: progress_label.configure(text="Installing..."))

        """
            d contains key like:
                status : "downloading" or "finished"
                downloaded_bytes
                total bytes
                filename
        """
        if d["status"] == "downloading":
            downloaded = d.get("downloaded_bytes", 0)
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            percent = (downloaded / total * 100) if total else 0.0
            root.after(0, lambda: progress_bar.set(percent / 100))
            root.after(0, lambda: progress_label.configure(text=f"({percent:.1f}%)"))
    
        elif d["status"] == "finished":
            root.after(0, lambda: progress_bar.set(1.0))
            root.after(0, lambda: progress_label.configure(text="Download finished!"))
            root.after(0, lambda: show_pop_up("Download finished!", "#4ADE80"))

    return install_progress

   

