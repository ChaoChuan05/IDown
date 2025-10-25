from common_import import *
from core import start_download, monitor_network

WIDGET_COLOR= "#7C3AED" 
BACKGROUND_COLOR = "#2B2543"
HOVER_COLOR =  "#9F67FF"
TEXT_COLOR = "#EDE9FE"

class App:

    #Constructor
    def __init__(self) -> None:
        #Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        #Window
        self.root = ctk.CTk()
        self.root.title("IDown")
        self.root.minsize(800, 700) #width x height
        self.root.resizable(True, True) #width x height

        if getattr(sys, 'frozen', False):
            # If running as bundled EXE, use temp folder PyInstaller extracts
            icon_path = os.path.join(sys._MEIPASS, "icon.ico")
        else:
            # If running as script, use local path
            icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")

        self.root.iconbitmap(icon_path)

        #Font family initialise
        self.title_font = ctk.CTkFont(
            family="Segoe UI Black",
            size=48,
            weight="bold"
        )

        self.widget_font = ctk.CTkFont(
            family="Segoe UI Semibold",
            size=20,
            weight="bold"
        )

        self.input_font = ctk.CTkFont(
            family="Arial",
            size=14
        )

        #Tab view initialise
        self.tab = ctk.CTkTabview(
            self.root,
            segmented_button_fg_color=WIDGET_COLOR,
            segmented_button_selected_color=WIDGET_COLOR,
            segmented_button_selected_hover_color=HOVER_COLOR,
            text_color=TEXT_COLOR,
            fg_color="transparent"
            
        )

        self.tab.pack(
            fill="both",
            expand=True
        )

        self.main_page_tab = self.tab.add("Main Page")
        self.setting_tab = self.tab.add("Settings")

        #Pages
        self.main_page()
        self.setting_page()

        #start monitor network once when app starts
        monitor_network(self.root, self.show_pop_up)

    def main_page(self) -> None:

        #Title
        self.app_name_label = ctk.CTkLabel(
            self.main_page_tab,
            text="IDown",
            font=self.title_font,
            text_color=TEXT_COLOR,
        )

        self.app_name_label.place(
            relx=0.5,
            rely=0.1,
            anchor="center"
        )

        #App entry
        self.app_entry = ctk.CTkEntry(
            self.main_page_tab,
            height=40,
            placeholder_text="Insert your URL here",
            font=self.input_font,
            text_color=TEXT_COLOR,
            placeholder_text_color=TEXT_COLOR,
            corner_radius=20,
            border_color=WIDGET_COLOR,
            fg_color=BACKGROUND_COLOR
        )

        self.app_entry.place(
            relx = 0.5,
            rely = 0.2,
            relwidth=0.8, #responsive width
            anchor="center",
        )

        #Frame for button
        self.button_frame = ctk.CTkFrame(
            self.main_page_tab,
            corner_radius=20,
            height=100,
            fg_color=BACKGROUND_COLOR
        )

        self.button_frame.place(
            relx=0.5,
            rely=0.35,
            relwidth=0.8,
            anchor="center"
        )

        #Inner frame to hold the buttons
        self.inner_button_frame = ctk.CTkFrame(
            self.button_frame, 
            fg_color="transparent"
        )

        self.inner_button_frame.pack(
            expand = True
        )

        #Button inside the frame
        self.download_button = ctk.CTkButton(
            self.inner_button_frame,
            text="Download",
            font=self.widget_font,
            width=200,
            height=80,
            fg_color=WIDGET_COLOR,
            hover_color=HOVER_COLOR,
            corner_radius=20,
            command=self.download,
        )

        self.download_button.pack(
            side="left",
            padx=20,
            pady=20
        )

        self.clear_button = ctk.CTkButton(
            self.inner_button_frame,
            text="Clear",
            font=self.widget_font,
            width=200,
            height=80,
            fg_color=WIDGET_COLOR,
            hover_color=HOVER_COLOR,
            corner_radius=20,
            command=self.clear_url
        )

        self.clear_button.pack(
            side="left",
            padx=20,
            pady=20
        )

        #Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.main_page_tab,
            orientation="horizontal",
            mode="determinate",
            determinate_speed=10,
            progress_color=WIDGET_COLOR
        )

        #Progress label
        self.progress_label = ctk.CTkLabel(
            self.main_page_tab,
            text="",
            font=self.input_font
        )

    def setting_page(self) -> None:
        
        self.setting_label = ctk.CTkLabel(
            self.setting_tab,
            text="Setting",
            font=self.title_font,
            text_color=TEXT_COLOR
        )

        self.setting_label.place(
            relx= 0.5,
            rely=0.1,
            anchor="center"
        )

        #Frame for the setting list
        self.setting_frame = ctk.CTkFrame(
            self.setting_tab,
            fg_color="transparent"
        )

        self.setting_frame.place(
            relx=0.5,
            rely=0.35,
            relwidth=0.8,
            relheight=0.8,
            anchor="center"
        )

        #Inner frame for download path setting (label, entry)

        self.inner_setting_path_frame = ctk.CTkFrame(
            self.setting_frame,
            fg_color="transparent"
        )

        self.inner_setting_path_frame.place(
            relx=0.5,
            rely=0.15,
            relwidth=0.93,
            anchor='center'
        )
        
        #Setup download path and switch
        self.settings = load_setting()
        self.download_path_var = ctk.StringVar(value=self.settings["download_path"])
        self.mp3_mp4_switch_var = ctk.BooleanVar(value=self.settings.get("always_mp3", True)) # load from file or default True
        self.playlist_var = ctk.BooleanVar(value=self.settings.get("allow_playlist", True))

        #Download path setting (label, entry)
        self.download_path_label = ctk.CTkLabel(
            self.inner_setting_path_frame,
            text="Download Path: ",
            font=self.widget_font,
        )

        self.download_path_label.pack(
            side="left",
            padx=20,
            pady=20
        )

        self.download_path_entry = ctk.CTkEntry(
            self.inner_setting_path_frame,
            textvariable=self.download_path_var,
            font=self.input_font,
            height=40,
            width=600,
            text_color=TEXT_COLOR,
            placeholder_text_color=TEXT_COLOR,
            corner_radius=20,
            border_color=WIDGET_COLOR,
            fg_color=BACKGROUND_COLOR
        )

        self.download_path_entry.pack(
            side="left",
            padx=20,
            pady=20
        )

        #MP3 / MP4 switching
        self.mp3_mp4_switch = ctk.CTkSwitch(
            self.setting_frame,
            text="Always MP3",
            font=self.widget_font,
            variable=self.mp3_mp4_switch_var,
            text_color=TEXT_COLOR,
            button_color=WIDGET_COLOR,
            button_hover_color=HOVER_COLOR,
            onvalue=True,
            offvalue=False,
        )

        self.mp3_mp4_switch.place(
            relx = 0.5,
            rely = 0.25,
            relwidth=0.9,
            anchor="n"
        )

        #Playlist checking
        self.allow_playlist_switch = ctk.CTkSwitch(
            self.setting_frame,
            text="Allow Playlist",
            font=self.widget_font,
            variable=self.playlist_var,
            text_color=TEXT_COLOR,
            button_color=WIDGET_COLOR,
            button_hover_color=HOVER_COLOR,
            onvalue=True,
            offvalue=False,
        )

        self.allow_playlist_switch.place(
            relx = 0.5,
            rely = 0.35,
            relwidth=0.9,
            anchor="n"
        )

        #Save button
        self.save_button = ctk.CTkButton(
            self.setting_frame,
            text="Save",
            font=self.widget_font,
            width=200,
            height=80,
            fg_color=WIDGET_COLOR,
            hover_color=HOVER_COLOR,
            corner_radius=20,
            command=self.save_user_setting,
        )

        self.save_button.place(
            relx=0.5,
            rely=0.6,
            relwidth=0.8,
            anchor="center"
        )

    #Main page function
    def download(self) -> None:
        url = self.app_entry.get()

        start_download(
            self.root, 
            url, 
            self.progress_bar,
            self.progress_label,
            self.app_entry,
            self.show_pop_up
        )

    def clear_url(self) -> None:

        current_text = self.app_entry.get()

        if current_text.strip():
            self.app_entry.delete(0, "end")
            self.show_pop_up("Successfully deleted!", "#4ADE80")
        
        else: self.show_pop_up("Nothing to delete!", "#E30B5C")

    #Setting page function
    def save_user_setting(self) -> None:
        """Event handler for save button (Setting page)"""

        download_path = self.download_path_var.get()
        always_mp3 = self.mp3_mp4_switch_var.get()
        allow_playlist = self.playlist_var.get()

        save_setting({
            "download_path" : download_path,
            "always_mp3" : always_mp3,
            "allow_playlist" : allow_playlist
        })

        self.show_pop_up("Settings saved successfully!", "#4ADE80")

    #Other
    def show_pop_up(self, text : str, frame_color : str) -> None:

        """Show a temporary confirmation message"""

        popup = ctk.CTkFrame(
            self.root,
            fg_color=frame_color,
            bg_color="transparent",
        )

        popup.place(
            relx=0.5,
            rely=0.8,
            anchor="center"
        )

        label = ctk.CTkLabel(
            popup,
            text=text,
            text_color=TEXT_COLOR,
            font=self.widget_font
        )

        label.pack(
            padx=20,
            pady=20
        )

        self.root.after(2000, popup.destroy)

    def run(self) -> None: 
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
        

