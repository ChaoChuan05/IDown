import customtkinter as ctk

class App:

    #Constructor
    def __init__(self) -> None:

        #Color initialise
        self.widget_coloring = "#7C3AED" 
        self.backgrond_coloring = "#2B2543"
        self.hover_coloring =  "#9F67FF"
        self.text_coloring = "#EDE9FE"

        #Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        #Window
        self.root = ctk.CTk()
        self.root.title("IDown")
        self.root.minsize(800, 800)
        self.root.resizable(True, True) #width x height
        self.root.iconbitmap("Icon.ico")

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

        #Pages
        self.main_page()



    def main_page(self) -> None:

        #Title
        self.app_name_label = ctk.CTkLabel(
            self.root,
            text="IDown",
            font=self.title_font,
            text_color=self.text_coloring,
        )

        self.app_name_label.place(
            relx=0.5,
            rely=0.1,
            anchor="center"
        )

        #App entry
        self.app_entry = ctk.CTkEntry(
            self.root,
            height=40,
            placeholder_text="Insert your URL here",
            font=self.input_font,
            text_color=self.text_coloring,
            placeholder_text_color=self.text_coloring,
            corner_radius=20,
            border_color=self.widget_coloring,
            fg_color=self.backgrond_coloring
        )

        self.app_entry.place(
            relx = 0.5,
            rely = 0.2,
            relwidth=0.8, #responsive width
            anchor="center",
        )

        #Frame for button
        self.button_frame = ctk.CTkFrame(
            self.root,
            corner_radius=20,
            height=100,
            fg_color=self.backgrond_coloring
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
            fg_color=self.widget_coloring,
            hover_color=self.hover_coloring,
            corner_radius=20
            #command=,
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
            fg_color=self.widget_coloring,
            hover_color=self.hover_coloring,
            corner_radius=20
            #command=,
        )

        self.clear_button.pack(
            side="left",
            padx=20,
            pady=20
        )

        #Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.root,
            orientation="horizontal",
            mode="determinate",
            determinate_speed=10,
        )

        self.progress_bar.place(
            relx=0.5,
            rely=0.5,
            relwidth=0.5,
            anchor="center"
        )

        self.progress_update()

        #Progress label
        self.progress_label = ctk.CTkLabel(
            self.root,
            text="",
            font=self.input_font
        )

        self.progress_label.place(
            relx=0.5,
            rely=0.6,
            relwidth=0.5,
            anchor="center"
        )


    #Function
    def run(self) -> None: 
        self.root.mainloop()

    def download(self) -> None:
        pass

    def clear(self) -> None:
        pass

    def progress_update(self) -> None:
        self.progress_bar.set(0)

if __name__ == "__main__":
    app = App()
    app.run()
        