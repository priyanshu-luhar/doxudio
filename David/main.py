import os
import fitz  # PyMuPDF
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog
import requests
from io import BytesIO

DISPLAY_NAME = "Priyanshu"
SERVER_URL = "http://127.0.0.1:5000"

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class PDFReaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("doxudio")
        self.geometry("1200x800")

        self.grid_columnconfigure(0, minsize=350)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_nav_font = ctk.CTkFont(family="Silom", size=18)
        self.sidebar_font = ctk.CTkFont(family="Silom", size=14)
        self.sidebar_file_font = ctk.CTkFont(family="Silom", size=10)

        self.top_nav = ctk.CTkFrame(self, height=50)
        self.top_nav.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.top_nav.grid_columnconfigure((0, 1, 2, 3), weight=0)
        self.top_nav.grid_columnconfigure(4, weight=1)

        self.home_button = ctk.CTkButton(self.top_nav, text="Home", font=self.top_nav_font, command=lambda: self.switch_view("home"))
        self.library_button = ctk.CTkButton(self.top_nav, text="Library", font=self.top_nav_font, command=lambda: self.switch_view("library"))
        self.audio_button = ctk.CTkButton(self.top_nav, text="Audiobooks", font=self.top_nav_font, command=lambda: self.switch_view("audiobooks"))
        self.profile_menu = ctk.CTkOptionMenu(self.top_nav, font=self.top_nav_font, values=["Profile", "Settings", "Logout"])
        self.profile_menu.set(DISPLAY_NAME)

        self.home_button.grid(row=0, column=0, padx=10, pady=8)
        self.library_button.grid(row=0, column=1, padx=10, pady=8)
        self.audio_button.grid(row=0, column=2, padx=10, pady=8)
        self.profile_menu.grid(row=0, column=4, padx=20, pady=8)

        self.sidebar = ctk.CTkFrame(self, width=350)
        self.sidebar.grid(row=1, column=0, sticky="nswe")
        self.sidebar.grid_propagate(False)

        self.load_button = ctk.CTkButton(self.sidebar, text="Add PDF", font=self.sidebar_font, command=self.load_pdf_file, border_width=2, border_color="white")
        self.load_button.pack(pady=10)

        self.load_dir_button = ctk.CTkButton(self.sidebar, text="Load Folder", font=self.sidebar_font, command=self.load_pdf_folder, border_width=2, border_color="white")
        self.load_dir_button.pack(pady=10)

        self.upload_button = ctk.CTkButton(self.sidebar, text="Upload Selected PDF", font=self.sidebar_font, command=self.upload_selected_pdf, border_width=2, border_color="white")
        self.upload_button.pack(pady=10)

        self.file_listbox = ctk.CTkScrollableFrame(self.sidebar)
        self.file_listbox.pack(fill="both", expand=True)

        self.pdf_buttons = []
        self.loaded_pdfs = {}

        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        # Tabbed view inside Home
        self.tab_view = ctk.CTkTabview(self.content_frame)
        self.tab_view.pack(fill="both", expand=True)

        self.books_tab = self.tab_view.add("Books")
        self.files_tab = self.tab_view.add("Server Files")

        # Book Search UI in Books Tab
        self.query_input = ctk.CTkEntry(self.books_tab, placeholder_text="Enter search term")
        self.query_input.pack(pady=5, padx=10, fill="x")

        self.search_type_dropdown = ctk.CTkOptionMenu(self.books_tab, values=["title", "author", "isbn"])
        self.search_type_dropdown.set("title")
        self.search_type_dropdown.pack(pady=5, padx=10)

        self.search_button = ctk.CTkButton(self.books_tab, text="Search Books", command=self.search_books)
        self.search_button.pack(pady=5)

        self.results_container = ctk.CTkScrollableFrame(self.books_tab)
        self.results_container.pack(pady=5, padx=10, fill="both", expand=True)

        # File list shown in server files tab
        self.server_files_container = ctk.CTkScrollableFrame(self.files_tab)
        self.server_files_container.pack(fill="both", expand=True, padx=10, pady=5)

        self.viewer = ctk.CTkLabel(self.content_frame, text="")
        self.viewer.pack()

        self.current_doc = None
        self.current_page = 0
        self.total_pages = 0

    def switch_view(self, view_name):
        if view_name == "home":
            self.fetch_server_files()

    def fetch_server_files(self):
        for child in self.server_files_container.winfo_children():
            child.destroy()
        try:
            r = requests.get(f"{SERVER_URL}/files")
            if r.status_code == 200:
                for file_id, filename, uploaded_at in r.json():
                    btn = ctk.CTkButton(self.server_files_container, text=f"[Server] {filename}", font=self.sidebar_file_font,
                                        command=lambda fid=file_id, fname=filename: self.download_and_open_pdf(fid, fname))
                    btn.pack(fill="x", pady=5, padx=5)
        except Exception as e:
            ctk.CTkLabel(self.server_files_container, text=f"Error fetching files:\n{str(e)}").pack()

    def search_books(self):
        for child in self.results_container.winfo_children():
            child.destroy()

        query = self.query_input.get().strip()
        search_type = self.search_type_dropdown.get()
        if not query:
            ctk.CTkLabel(self.results_container, text="Please enter a search term.").pack()
            return

        url = "https://openlibrary.org/search.json"
        params = {search_type: query}

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                ctk.CTkLabel(self.results_container, text="Failed to fetch data.").pack()
                return

            data = response.json()
            books = data.get("docs", [])
            if not books:
                ctk.CTkLabel(self.results_container, text="No results found.").pack()
                return

            for book in books[:10]:
                title = book.get("title", "N/A")
                authors = ", ".join(book.get("author_name", ["Unknown"]))
                year = book.get("first_publish_year", "N/A")
                key = book.get("key", "")

                book_info = f"{title}\nby {authors}\nFirst Published: {year}"
                book_url = f"https://openlibrary.org{key}" if key else ""

                frame = ctk.CTkFrame(self.results_container)
                frame.pack(pady=5, fill="x")

                label = ctk.CTkLabel(frame, text=book_info, justify="left")
                label.pack(side="left", padx=5)

                if book_url:
                    link_button = ctk.CTkButton(frame, text="View", width=50, command=lambda url=book_url: os.system(f"open {url}"))
                    link_button.pack(side="right", padx=5)

        except Exception as e:
            ctk.CTkLabel(self.results_container, text=f"Error: {str(e)}").pack()

    def load_pdf_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if filepath:
            filename = os.path.basename(filepath)
            if filename not in self.loaded_pdfs:
                self.loaded_pdfs[filename] = filepath
                btn = ctk.CTkButton(self.file_listbox, text=filename, font=self.sidebar_file_font,
                                    command=lambda path=filepath: self.open_pdf(path))
                btn.pack(fill="x", pady=5, padx=5)
                self.pdf_buttons.append(btn)

    def load_pdf_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            for file in os.listdir(folder_path):
                if file.lower().endswith(".pdf"):
                    full_path = os.path.join(folder_path, file)
                    if file not in self.loaded_pdfs:
                        self.loaded_pdfs[file] = full_path
                        btn = ctk.CTkButton(self.file_listbox, text=file, font=self.sidebar_file_font,
                                            command=lambda path=full_path: self.open_pdf(path))
                        btn.pack(fill="x", pady=5, padx=5)
                        self.pdf_buttons.append(btn)

    def upload_selected_pdf(self):
        if not self.current_doc:
            self.viewer.configure(text="No PDF open to upload.")
            return
        try:
            filepath = self.loaded_pdfs.get(self.current_doc.name.split("/")[-1])
            if not filepath:
                self.viewer.configure(text="Could not locate file path.")
                return
            with open(filepath, 'rb') as f:
                files = {'file': (os.path.basename(filepath), f)}
                r = requests.post(f"{SERVER_URL}/upload", files=files)
                if r.status_code == 200:
                    self.viewer.configure(text="Upload successful!")
                else:
                    self.viewer.configure(text=f"Upload failed: {r.status_code}")
        except Exception as e:
            self.viewer.configure(text=f"Upload error:\n{str(e)}")

    def download_and_open_pdf(self, file_id, filename):
        try:
            url = f"{SERVER_URL}/download/{file_id}"
            r = requests.get(url)
            if r.status_code == 200:
                os.makedirs("downloads", exist_ok=True)
                path = os.path.join("downloads", filename)
                with open(path, "wb") as f:
                    f.write(r.content)
                self.open_pdf(path)
            else:
                self.viewer.configure(text="Download failed.")
        except Exception as e:
            self.viewer.configure(text=f"Error downloading:\n{str(e)}")

    def open_pdf(self, filepath):
        try:
            self.current_doc = fitz.open(filepath)
            self.total_pages = len(self.current_doc)
            self.current_page = 0
            self.display_current_page()
        except Exception as e:
            self.viewer.configure(text=f"Failed to open PDF:\n{str(e)}")

    def display_current_page(self):
        if self.current_doc is None or not (0 <= self.current_page < self.total_pages):
            return
        try:
            page = self.current_doc.load_page(self.current_page)
            pix = page.get_pixmap(matrix=fitz.Matrix(4, 4))
            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            viewer_width = self.viewer.winfo_width() or 800
            viewer_height = self.viewer.winfo_height() or 1000

            aspect = image.width / image.height
            if viewer_width / viewer_height > aspect:
                new_height = viewer_height
                new_width = int(viewer_height * aspect)
            else:
                new_width = viewer_width
                new_height = int(viewer_width / aspect)

            image = image.resize((new_width, new_height), Image.LANCZOS)
            ctk_image = ctk.CTkImage(light_image=image, size=(new_width, new_height))

            self.viewer.configure(image=ctk_image, text="")
            self.viewer.image = ctk_image
        except Exception as e:
            self.viewer.configure(text=f"Failed to render page:\n{str(e)}")

    def next_page(self):
        if self.current_doc and self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.display_current_page()

    def prev_page(self):
        if self.current_doc and self.current_page > 0:
            self.current_page -= 1
            self.display_current_page()

if __name__ == "__main__":
    app = PDFReaderApp()
    app.mainloop()
