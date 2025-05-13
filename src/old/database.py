import customtkinter as ctk
from PIL import Image
from io import BytesIO
import requests
import globals
from server_utils import search_book

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

class DatabaseApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Database - Doxudio")
        self.geometry("+0+0")
        self.geometry("1200x800")
        self.resizable(False, False)

        self.top_nav_font = ctk.CTkFont(family="Silom", size=18)
        self.default_font = ctk.CTkFont(family="Silom", size=14)

        # Top Navigation
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

        # Search Bar
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(pady=20, padx=20, fill="x")

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search by title, author, or ISBN...", font=self.default_font)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=10)

        self.search_button = ctk.CTkButton(self.search_frame, text="Search", font=self.default_font, command=self.search_books)
        self.search_button.pack(side="right", pady=10)

        # Content Frames
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.results_frame = ctk.CTkScrollableFrame(self.content_frame)
        self.results_frame.grid(row=0, column=0, sticky="nsew")

        self.details_frame = ctk.CTkFrame(self.content_frame)
        self.details_frame.grid(row=0, column=0, sticky="nsew")
        self.details_frame.grid_remove()

    def show_book_details(self, book):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        self.results_frame.grid_remove()
        self.details_frame.grid()

        title = book.get("title", "Unknown Title")
        author = book.get("author", "Unknown Author")
        year = str(book.get("published", "N/A"))[:4]
        abstract = book.get("abstract", "No summary available.")
        cover_path = book.get("coverpath", None)

        if cover_path:
            cover_path = cover_path.replace("/home/stu/pluhar/public_html/doxudio/public/", "")
            try:
                img_data = requests.get(f"https://artemis.cs.csub.edu/~pluhar/doxudio/public/{cover_path}").content
                img = Image.open(BytesIO(img_data)).resize((200, 300))
                ctk_img = ctk.CTkImage(light_image=img, size=(200, 300))
                ctk.CTkLabel(self.details_frame, image=ctk_img, text="").pack(pady=(10, 10))
            except:
                ctk.CTkLabel(self.details_frame, text="[No Cover]", width=200, height=300).pack()
        else:
            ctk.CTkLabel(self.details_frame, text="[No Cover]", width=200, height=300).pack()

        ctk.CTkLabel(self.details_frame, text=f"Title: {title}", font=self.default_font).pack(pady=5)
        ctk.CTkLabel(self.details_frame, text=f"Author: {author}", font=self.default_font).pack(pady=5)
        ctk.CTkLabel(self.details_frame, text=f"Published: {year}", font=self.default_font).pack(pady=5)
        ctk.CTkLabel(self.details_frame, text=f"Abstract:\n{abstract}", font=self.default_font, wraplength=600, justify="left").pack(pady=10)

        ctk.CTkButton(self.details_frame, text="Back to Results", font=self.default_font, command=self.back_to_results).pack(pady=20)

    def back_to_results(self):
        self.details_frame.grid_remove()
        self.results_frame.grid()

    def search_books(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        query = self.search_entry.get().strip()
        if not query:
            return

        response = search_book(title=query) or search_book(author=query) or search_book(isbn=query)
        books = response if isinstance(response, list) else []

        row, col = 0, 0
        for book in books:
            frame = ctk.CTkFrame(self.results_frame)
            frame.grid(row=row, column=col, padx=40, pady=20)

            def make_callback(b=book):
                return lambda: self.show_book_details(b)

            if book.get("coverpath"):
                try:
                    cover_path = book["coverpath"].replace("/home/stu/pluhar/public_html/doxudio/public/", "")
                    img_data = requests.get(f"https://artemis.cs.csub.edu/~pluhar/doxudio/public/{cover_path}").content
                    img = Image.open(BytesIO(img_data)).resize((200, 300))
                    ctk_img = ctk.CTkImage(light_image=img, size=(200, 300))
                    btn = ctk.CTkButton(frame, image=ctk_img, text="", command=make_callback())
                    btn.image = ctk_img
                    btn.pack()
                except:
                    ctk.CTkButton(frame, text="[No Cover]", width=200, height=300, command=make_callback()).pack()
            else:
                ctk.CTkButton(frame, text="[No Cover]", width=200, height=300, command=make_callback()).pack()

            title = book.get("title", "Unknown Title")
            author = book.get("author", "Unknown Author")
            year = str(book.get("published", "N/A"))[:4]

            ctk.CTkLabel(frame, text=f"{title}\n{author}\n{year}", font=self.default_font, justify="center", wraplength=160).pack(pady=(5, 0))

            col += 1
            if col >= 4:
                col = 0
                row += 1

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
        elif view_name == "library":
            from library import LibraryApp
            LibraryApp().mainloop()
        elif view_name == "profile":
            from profile import ProfileWindow
            ProfileWindow(globals.me).mainloop()

if __name__ == "__main__":
    app = DatabaseApp()
    app.mainloop()
