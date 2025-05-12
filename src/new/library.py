import customtkinter as ctk
import requests
from PIL import Image
from io import BytesIO

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class LibraryApp(ctk.CTkFrame):
    def __init__(self, master=None):
        super().__init__(master)
        # Font
        self.default_font = ctk.CTkFont(family="Silom", size=14)

        # Search bar frame
        self.search_frame = ctk.CTkFrame(self)
        self.search_frame.pack(pady=20, padx=20, fill="x")

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search by title, author, or ISBN...", font=self.default_font)
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=10)

        self.search_button = ctk.CTkButton(self.search_frame, text="Search", font=self.default_font, command=self.search_books)
        self.search_button.pack(side="right", pady=10)

        # Results frame
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
                books = data.get("docs", [])[:20]
                row, col = 0, 0

                for book in books:
                    cover_id = book.get("cover_i", None)
                    title = book.get("title", "Unknown Title")
                    author = ", ".join(book.get("author_name", ["Unknown Author"]))
                    year = book.get("first_publish_year", "N/A")

                    # Create frame for each book
                    book_frame = ctk.CTkFrame(self.results_frame)
                    book_frame.grid(row=row, column=col, padx=10, pady=10)

                    if cover_id:
                        img_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                        img_data = requests.get(img_url).content
                        img = Image.open(BytesIO(img_data)).resize((100, 150))
                        ctk_img = ctk.CTkImage(light_image=img, size=(100, 150))
                        img_label = ctk.CTkLabel(book_frame, image=ctk_img, text="")
                        img_label.image = ctk_img  # Keep reference
                        img_label.pack()
                    else:
                        no_img_label = ctk.CTkLabel(book_frame, text="[No Cover]", width=100, height=150)
                        no_img_label.pack()

                    text_label = ctk.CTkLabel(book_frame, text=f"{title}\n{author}\n{year}", font=self.default_font, justify="center", wraplength=120)
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
        error_label = ctk.CTkLabel(self.results_frame, text=f"Error: {msg}", text_color="red", font=self.default_font)
        error_label.pack(pady=10)


