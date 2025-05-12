import customtkinter as ctk

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class DynamicViewApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Dynamic View Example")
        self.geometry("600x400")

        # Font
        self.default_font = ctk.CTkFont(size=14)

        # Top menu
        self.menu = ctk.CTkOptionMenu(self, values=["Home", "Library", "Settings"], command=self.switch_view, font=self.default_font)
        self.menu.pack(pady=20)
        self.menu.set("Home")

        # View container
        self.view_frame = ctk.CTkFrame(self)
        self.view_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Initial view
        self.switch_view("Home")

    def clear_view(self):
        for widget in self.view_frame.winfo_children():
            widget.destroy()

    def switch_view(self, view_name):
        self.clear_view()

        if view_name == "Home":
            label = ctk.CTkLabel(self.view_frame, text="🏠 Welcome to Home!", font=self.default_font)
            label.pack(pady=50)
        elif view_name == "Library":
            entry = ctk.CTkEntry(self.view_frame, placeholder_text="Search Library...", font=self.default_font)
            entry.pack(pady=20)
            search_btn = ctk.CTkButton(self.view_frame, text="Search", font=self.default_font)
            search_btn.pack()
        elif view_name == "Settings":
            toggle = ctk.CTkSwitch(self.view_frame, text="Enable Feature X", font=self.default_font)
            toggle.pack(pady=40)

if __name__ == "__main__":
    app = DynamicViewApp()
    app.mainloop()

