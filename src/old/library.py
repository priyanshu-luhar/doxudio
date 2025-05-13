import customtkinter as ctk
import requests
from PIL import Image
from io import BytesIO
import globals

ctk.set_appearance_mode("System")
#ctk.set_default_color_theme("blue")
ctk.set_default_color_theme("green")

class LibraryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library - Doxudio")
        self.geometry("+0+0")
        self.geometry("1200x800")
        self.resizable(False, False)

        # Fonts
        self.top_nav_font = ctk.CTkFont(family="Silom", size=18)
        self.default_font = ctk.CTkFont(family="Silom", size=14)


        # Top Navigation Bar
        self.top_nav = ctk.CTkFrame(self, height=50)
        self.top_nav.grid_columnconfigure(4, weight=1)
        self.top_nav.pack(fill="x")

        self.home_button = ctk.CTkButton(self.top_nav, text="Home", font=self.top_nav_font, command=lambda: self.switch_view("home"))
        self.library_button = ctk.CTkButton(self.top_nav, text="Library", font=self.top_nav_font, command=lambda: self.switch_view("library"))
        self.database_button = ctk.CTkButton(self.top_nav, text="Database", font=self.top_nav_font)
        self.audio_button = ctk.CTkButton(self.top_nav, text="Audiobooks", font=self.top_nav_font)
        self.profile_menu = ctk.CTkOptionMenu(self.top_nav, font=self.top_nav_font, values=["Profile", "Settings", "Logout"], command=self.handle_profile_menu)
        self.profile_menu.set(globals.me["fname"])

        self.home_button.grid(row=0, column=0, padx=10, pady=8)
        self.library_button.grid(row=0, column=1, padx=10, pady=8)
        self.audio_button.grid(row=0, column=2, padx=10, pady=8)
        self.database_button.grid(row=0, column=3, padx=10, pady=8)
        self.profile_menu.grid(row=0, column=5, padx=20, pady=8)
        
        # Search bar
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(pady=20, padx=20, fill="x")

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search by title, author, or ISBN...", font=self.default_font)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=10)

        self.search_button = ctk.CTkButton(self.search_frame, text="Search", font=self.default_font, command=self.search_books)
        self.search_button.pack(side="right", pady=10)

        # Results
        self.results_frame = ctk.CTkScrollableFrame(self)
        self.results_frame.pack(fill="both", expand=True, padx=20, pady=10)

    def search_books(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        query = self.search_entry.get()
        if not query:
            return

        url = f"https://openlibrary.org/search.json?q={query}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                books = data.get("docs", [])[:40]
                row, col = 0, 0

                for book in books:
                    cover_id = book.get("cover_i", None)
                    title = book.get("title", "Unknown Title")
                    author = ", ".join(book.get("author_name", ["Unknown Author"]))
                    year = book.get("first_publish_year", "N/A")

                    book_frame = ctk.CTkFrame(self.results_frame)
                    book_frame.grid(row=row, column=col, padx=40, pady=20)

                    if cover_id:
                        img_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                        img_data = requests.get(img_url).content
                        img = Image.open(BytesIO(img_data)).resize((200, 300))
                        ctk_img = ctk.CTkImage(light_image=img, size=(200, 300))
                        img_label = ctk.CTkLabel(book_frame, image=ctk_img, text="")
                        img_label.image = ctk_img
                        img_label.pack()
                    else:
                        ctk.CTkLabel(book_frame, text="[No Cover]", width=200, height=300).pack()

                    text_label = ctk.CTkLabel(
                        book_frame, 
                        text=f"{title}\n{author}\n{year}", 
                        font=self.default_font, 
                        justify="center", 
                        wraplength=160
                    )
                    text_label.pack(pady=(5, 0))

                    col += 1
                    if col >= 4:
                        col = 0
                        row += 1
            else:
                self.show_error(f"API returned status code: {response.status_code}")
        except Exception as e:
            self.show_error(str(e))

    def show_error(self, msg):
        ctk.CTkLabel(self.results_frame, text=f"Error: {msg}", text_color="red", font=self.default_font).pack(pady=10)

    def handle_profile_menu(self, choice):
        if choice == "Profile":
            self.switch_view("profile")
        elif choice == "Logout":
            self.destroy()
            from login import AuthWindow
            AuthWindow().mainloop()

    def switch_view(self, view_name):
        self.destroy()
        if view_name == "home":
            from main import PDFReaderApp
            PDFReaderApp().mainloop()
        elif view_name == "profile":
            from profile import ProfileWindow
            ProfileWindow(globals.me).mainloop()

if __name__ == "__main__":
    app = LibraryApp()
    app.mainloop()

