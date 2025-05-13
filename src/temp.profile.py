import customtkinter as ctk
import hashlib

class ProfileWindow(ctk.CTk):
    def __init__(self, user):
        super().__init__()
        self.title("User Profile")
        self.geometry("1200x800")
        self.resizable(False, False)

        # Fonts
        self.font_title = ctk.CTkFont(family="Silom", size=36, weight="bold")
        self.font_label = ctk.CTkFont(family="Silom", size=24)
        self.font_value = ctk.CTkFont(family="Silom", size=24)
        self.font_button = ctk.CTkFont(family="Silom", size=22)

        # Main frame without padding
        self.frame = ctk.CTkFrame(self, corner_radius=0)
        self.frame.pack(fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(self.frame, text="User Profile", font=self.font_title)
        self.title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(10, 40))

        # Info row by row
        self.add_info_row("Username:", user["uname"], 1)
        self.add_info_row("First Name:", user["fname"], 2)
        self.add_info_row("Last Name:", user["lname"], 3)

        hex_id = hex(int(user["user_id"]))
        self.add_info_row("User ID (Hex):", hex_id, 4, pady=10)
        
        # Change password button
        ctk.CTkButton(self.frame, text="Change Password", font=self.font_button,
                      command=self.change_password).grid(row=5, column=0, sticky="w", pady=(30, 0))

    def add_info_row(self, label_text, value_text, row):
        ctk.CTkLabel(self.frame, text=label_text, font=self.font_label).grid(row=row, column=0, sticky="w", padx=(20, 5))
        ctk.CTkLabel(self.frame, text=value_text, font=self.font_value, text_color="yellow").grid(row=row, column=1, sticky="w")

    def change_password(self):
        ctk.CTkLabel(self.frame, text="Change password clicked (not implemented)",
                     font=self.font_label, text_color="orange").grid(row=6, column=0, columnspan=2, sticky="w", pady=10)

if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Example dummy user (replace with actual user from login)
    dummy_user = {
        "uname": "pluhar",
        "fname": "Priyanshu",
        "lname": "Luhar",
        "user_id": 42
    }

    app = ProfileWindow(dummy_user)
    app.mainloop()

