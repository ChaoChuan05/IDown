from common_import import *

progress = 0 #Progress bar 
DELAY = 1000

#Important before proceed: the function need to implement root.after since it's using thread
#The UI might crash or freeze if we not using it
def monitor_network(root, show_pop_up, interval = 5) -> None:
    """
        Check network connection every "interval" seconds
        If network is down, shows a popup
        Runs in a background thread so UI remains responsive.
    """

    def check_loop():
        while True:
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=3)
                network_ok = True
            except OSError:
                network_ok = False

            if not network_ok:
                root.after(DELAY, lambda: show_pop_up("Network connection lost", "#E30B5C"))

            time.sleep(interval)

        threading.Thread(target=check_loop, daemon=True).start()

def is_network_ok(timeout = 3) -> bool:
    """
        Return true if network is reachable, false if not
        Tries to connecting to a well-known host on port 53 (DNS)
    """

    try:
        #Attempt TCP connection to Google DNS
        socket.create_connection(("8.8.8.8, 53", timeout))
        return True

    except OSError:
        return False

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

    #2. Check connection
    if not is_network_ok:
        show_pop_up("Network connection seems bad. Please check your internet!", "#E30B5C")

    #3. Prepare UI
    setup_progress_ui(progress_bar, progress_label)
    root.update_idletasks()

    #4. Start the background thread
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

    """
    The function define four nested function

    1. path step (Check if download folder exists)
    2. url step (Check if the URL is valid)
    3. playlist step (Check if the URL is a playlist and if playlist is allowed)
    4. install step (Start the actual download)

    Each step does two things
    1. Run blocking work in thread
    2. When done, schedule the next step on the main thread using root.after(0, next_step)
    
    Main thread: customtkinter UI loop (.mainloop())
    Thread 2: run background check()
    Thread 3: run path_check()
    Thread 4: run check_playlist()
    Thread 5: run install()


    """

    def path_step():
        def task():
            success = path_check(root, progress_bar, progress_label)
            if success:
                root.after(DELAY, url_step)
        threading.Thread(target=task, daemon=True).start()

    def url_step():
        def task():
            success = check_url(root, url, progress_bar, progress_label, app_entry, show_pop_up)
            if success:
                root.after(DELAY, playlist_step)
        threading.Thread(target=task, daemon=True).start()

    def playlist_step():
        def task():
            success = check_playlist(root, url, progress_bar, progress_label, app_entry, show_pop_up)
            if success:
                root.after(DELAY, install_step)
        threading.Thread(target=task, daemon=True).start()

    def install_step():
        # Download already runs in a separate thread in your original code
        threading.Thread(
            target=install,
            args=(root, url, progress_bar, progress_label, show_pop_up),
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
        root.after(DELAY, lambda: progress_bar.set(progress))
        root.after(DELAY, lambda: progress_label.configure(text="URL check complete"))
        
        return True

    except Exception:
        root.after(DELAY, lambda: progress_bar.place_forget())
        root.after(DELAY, lambda: progress_label.configure(text=""))
        root.after(DELAY, lambda: app_entry.delete(0, "end"))
        root.after(DELAY, lambda: show_pop_up("Invalid or Unsupported URL!", "#E30B5C"))
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
            root.after(DELAY, lambda: progress_bar.set(progress))
            root.after(DELAY, lambda: progress_label.configure(text="Playlist is not allowed"))
            return True
        
        elif is_playlist and allow_playlist:
            progress += 0.25
            root.after(DELAY, lambda: progress_bar.set(progress))
            root.after(DELAY, lambda: progress_label.configure(text="Playlist is allowed"))
            return True

        else:
            progress += 0.25
            root.after(DELAY, lambda: progress_bar.set(progress))
            root.after(DELAY, lambda: progress_label.configure(text="Single video or audio is detected!")) 
            return True
            

    except Exception:  
        root.after(DELAY, lambda: progress_bar.place_forget())
        root.after(DELAY, lambda: progress_label.configure(text=""))
        root.after(DELAY, lambda: app_entry.delete(0, "end"))
        root.after(DELAY, lambda: show_pop_up("The playlist might not supported!", "#E30B5C"))
        return False
        
def path_check(root, progress_bar, progress_label) -> bool:

    global progress

    settings = load_setting()
    path = settings.get("download_path", os.path.join(os.path.expanduser("~"), "Downloads"))

    root.after(0, lambda: progress_label.configure(text="Check path"))

    if not os.path.isdir(path):

        try:
            os.makedirs(path)
            root.after(DELAY, lambda: progress_label.configure(text="Create directory..."))
            progress += 0.25
            root.after(DELAY, lambda: progress_bar.set(progress))
            return True

        except Exception: 
            root.after(DELAY, lambda: progress_label.configure(text="Custom path failed! Using default path"))
            path = os.path.join(os.path.expanduser("~"), "Downloads")
            progress += 0.25
            root.after(DELAY, lambda: progress_bar.set(progress))
            return False

    else: 
        progress += 0.25
        root.after(DELAY, lambda: progress_bar.set(progress))
        root.after(DELAY, lambda: progress_label.configure(text="Path is correct"))
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
            "keepvideo" : False,
            "postprocessor_args": ["-y"],

            "postprocessors" : [{
                "key" : "FFmpegExtractAudio",
                "preferredcodec" : "mp3",
                "preferredquality" : "192"
            }],

            "headers" : {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            },

            "prefer_ffmpeg" : True,
            "ffmpeg_location" : ffmpeg_path
        }
        
    else: 
        options = {
            "format" : "bestvideo+bestaudio/best",
            "merge_output_format" : "mp4",
            "outtmpl" : f"{path}/%(title)s.%(ext)s",
            "noplaylist" : not allow_playlist,
            "progress_hooks" : [progress_hook],
            "keepvideo" : False,
            "postprocessor_args": ["-y"],  # same reason

            "headers" : {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
            },

            "prefer_ffmpeg" : True,
            "ffmpeg_location" : ffmpeg_path
        }

    progress += 0.25
    root.after(DELAY, lambda: progress_bar.set(progress))
    root.after(DELAY, lambda: progress_label.configure(text="Prepare to download..."))

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
            root.after(0, lambda: progress_label.configure(text=f"{percent:.1f}%"))
    
        elif d["status"] == "finished":
            root.after(0, lambda: progress_bar.set(1.0))
            root.after(0, lambda: progress_label.configure(text="Download finished!"))
            root.after(0, lambda: show_pop_up("Download finished!", "#4ADE80"))

    return install_progress

   

