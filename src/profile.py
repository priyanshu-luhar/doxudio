import customtkinter as ctk
import hashlib
import globals

class ProfileWindow(ctk.CTk):
    def __init__(self, user):
        super().__init__()
        self.title("User Profile")
        self.geometry("+0+0")
        self.geometry("1200x800")
        self.resizable(False, False)

        self.user = user

        # Fonts
        self.top_nav_font = ctk.CTkFont(family="Silom", size=18)
        self.font_title = ctk.CTkFont(family="Silom", size=36, weight="bold")
        self.font_label = ctk.CTkFont(family="Silom", size=24)
        self.font_value = ctk.CTkFont(family="Silom", size=24)
        self.font_button = ctk.CTkFont(family="Silom", size=22)

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Top Navigation Bar
        self.top_nav = ctk.CTkFrame(self, height=50)
        self.top_nav.grid(row=0, column=0, sticky="ew")
        self.top_nav.grid_columnconfigure(0, weight=0)
        self.top_nav.grid_columnconfigure(1, weight=0)
        self.top_nav.grid_columnconfigure(2, weight=0)
        self.top_nav.grid_columnconfigure(3, weight=0)
        self.top_nav.grid_columnconfigure(4, weight=1)
        self.top_nav.grid_columnconfigure(5, weight=0)

        self.home_button = ctk.CTkButton(self.top_nav, text="Home", font=self.top_nav_font, command=lambda: self.switch_view("home"))
        self.library_button = ctk.CTkButton(self.top_nav, text="Library", font=self.top_nav_font, command=lambda: self.switch_view("library"))
        self.database_button = ctk.CTkButton(self.top_nav, text="Database", font=self.top_nav_font, command=lambda: self.switch_view("database"))
        self.audio_button = ctk.CTkButton(self.top_nav, text="Audiobooks", font=self.top_nav_font, command=lambda: self.switch_view("audiobooks"))
        self.profile_menu = ctk.CTkOptionMenu(self.top_nav, font=self.top_nav_font, values=["Profile", "Settings", "Logout"])
        self.profile_menu.set(user["fname"])

        self.home_button.grid(row=0, column=0, padx=10, pady=8)
        self.library_button.grid(row=0, column=1, padx=10, pady=8)
        self.audio_button.grid(row=0, column=2, padx=10, pady=8)
        self.database_button.grid(row=0, column=3, padx=10, pady=8)
        self.profile_menu.grid(row=0, column=5, padx=20, pady=8)

        # Main content frame
        self.frame = ctk.CTkFrame(self, corner_radius=0)
        self.frame.grid(row=1, column=0, sticky="nsew")

        self.title_label = ctk.CTkLabel(self.frame, text="User Profile", font=self.font_title)
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(10, 40), padx=20)

        # Info display
        self.add_info_row("Username:", user["uname"], 1)
        self.add_info_row("First Name:", user["fname"], 2)
        self.add_info_row("Last Name:", user["lname"], 3)

        hex_id = hex(int(user["user_id"]))
        self.add_info_row("User ID (Hex):", hex_id, 4)

        # Change password button
        ctk.CTkButton(self.frame, text="Change Password", font=self.font_button,
                      command=self.change_password).grid(row=5, column=0, sticky="w", pady=(30, 0), padx=20)

    def add_info_row(self, label_text, value_text, row):
        ctk.CTkLabel(self.frame, text=label_text, font=self.font_label)\
            .grid(row=row, column=0, sticky="w", padx=(20, 5), pady=15)
        ctk.CTkLabel(self.frame, text=value_text, font=self.font_value, text_color="yellow")\
            .grid(row=row, column=1, sticky="w", pady=15)

    def change_password(self):
        ctk.CTkLabel(self.frame, text="Change password clicked (not implemented)",
                     font=self.font_label, text_color="orange")\
            .grid(row=6, column=0, columnspan=2, sticky="w", pady=10, padx=20)

    def switch_view(self, view_name):
        self.destroy()
        if view_name == "home":
            from main import PDFReaderApp  # <--- moved here
            PDFReaderApp().mainloop()
        elif view_name == "library":
            from library import LibraryApp
            LibraryApp().mainloop()
        elif view_name == "database":
            from database import DatabaseApp
            self.destroy()
            db_app = DatabaseApp()
            db_app.mainloop()
        elif view_name == "profile":
            ProfileWindow(globals.me).mainloop()

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    #ctk.set_default_color_theme("blue")
    ctk.set_default_color_theme("green")

    dummy_user = {
        "uname": "pluhar",
        "fname": "Priyanshu",
        "lname": "Luhar",
        "user_id": 42
    }

    app = ProfileWindow(globals.me)
    app.mainloop()

