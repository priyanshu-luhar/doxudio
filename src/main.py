import os
import fitz  # PyMuPDF
from PIL import Image
import customtkinter as ctk
from tkinter import filedialog

DISPLAY_NAME = "Priyanshu"

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class PDFReaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("doxudio")
        self.geometry("1200x800")

        # Layout
        self.grid_columnconfigure(0, minsize=350)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)

        self.grid_rowconfigure(1, weight=1)  # Top navigation bar row
        
        #self.top_nav_font = ctk.CTkFont(family="Rockwell", size=18)
        self.top_nav_font = ctk.CTkFont(family="Silom", size=18)
        self.sidebar_font = ctk.CTkFont(family="Silom", size=14)
        self.sidebar_file_font = ctk.CTkFont(family="Silom", size=10)

        # Top Navigation Bar
        self.top_nav = ctk.CTkFrame(self, height=50)
        self.top_nav.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.top_nav.grid_columnconfigure(0, weight=0)
        self.top_nav.grid_columnconfigure(1, weight=0)
        self.top_nav.grid_columnconfigure(2, weight=0)
        self.top_nav.grid_columnconfigure(3, weight=1)
        self.top_nav.grid_columnconfigure(4, weight=0)

        self.home_button = ctk.CTkButton(self.top_nav, text="Home", font=self.top_nav_font, command=lambda: self.switch_view("home"))
        self.library_button = ctk.CTkButton(self.top_nav, text="Library", font=self.top_nav_font, command=lambda: self.switch_view("library"))
        self.audio_button = ctk.CTkButton(self.top_nav, text="Audiobooks", font=self.top_nav_font, command=lambda: self.switch_view("audiobooks"))
        self.profile_menu = ctk.CTkOptionMenu(self.top_nav, font=self.top_nav_font, values=["Profile", "Settings", "Logout"])
        self.profile_menu.set(DISPLAY_NAME)

        self.home_button.grid(row=0, column=0, padx=10, pady=8)
        self.library_button.grid(row=0, column=1, padx=10, pady=8)
        self.audio_button.grid(row=0, column=2, padx=10, pady=8)
        self.profile_menu.grid(row=0, column=4, padx=20, pady=8)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=350)

        self.sidebar.grid(row=1, column=0, sticky="nswe")
        self.sidebar.grid_propagate(False)

        self.load_button = ctk.CTkButton(self.sidebar, text="Add PDF", font=self.sidebar_font, command=self.load_pdf_file, border_width=2, border_color="white")
        self.load_button.pack(pady=10)
        
        self.load_dir_button = ctk.CTkButton(self.sidebar, text="Load Folder", font=self.sidebar_font,  command=self.load_pdf_folder, border_width=2, border_color="white")
        self.load_dir_button.pack(pady=10)

        self.file_listbox = ctk.CTkScrollableFrame(self.sidebar)
        self.file_listbox.pack(fill="both", expand=True)

        self.pdf_buttons = []
        self.loaded_pdfs = {}

        # Main content
        self.content_frame = ctk.CTkFrame(self)
        self.content_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.viewer = ctk.CTkLabel(self.content_frame, text="")
        self.viewer.grid(row=0, column=0, columnspan=3, sticky="nsew")
        
        self.icon_left = ctk.CTkImage(light_image=Image.open("icons/prev_page.png"), size=(24, 24))
        self.icon_right = ctk.CTkImage(light_image=Image.open("icons/next_page.png"), size=(24, 24))
        
# Navigation container frame
        self.nav_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.nav_frame.grid(row=1, column=0, sticky="ew", pady=(5, 0), columnspan=1)
        self.nav_frame.grid_columnconfigure(0, weight=0)
        self.nav_frame.grid_columnconfigure(1, weight=0)
        self.nav_frame.grid_columnconfigure(2, weight=1)  # spacer
        self.nav_frame.grid_columnconfigure(3, weight=0)

# Navigation widgets
        self.prev_button = ctk.CTkButton(self.nav_frame, image=self.icon_left, text="", width=40, command=self.prev_page, border_width=2, border_color="white")
        self.next_button = ctk.CTkButton(self.nav_frame, image=self.icon_right, text="", width=40, command=self.next_page, border_width=2, border_color="white")
        self.page_label = ctk.CTkLabel(self.nav_frame, text="Page: -", font=ctk.CTkFont(size=14, weight="bold"))

        self.prev_button.grid(row=0, column=0, padx=(10, 5))
        self.next_button.grid(row=0, column=1, padx=(5, 10))
        self.page_label.grid(row=0, column=3, padx=(0, 20), sticky="e")

        # PDF state
        self.current_doc = None
        self.current_page = 0
        self.total_pages = 0

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

            # Get viewer size
            viewer_width = self.viewer.winfo_width()
            viewer_height = self.viewer.winfo_height()

            # Avoid 1x1 default fallback on first render
            if viewer_width < 10 or viewer_height < 10:
                viewer_width = 800
                viewer_height = 1000

            # Maintain aspect ratio
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
            self.page_label.configure(text=f"Page: {self.current_page + 1} / {self.total_pages}")
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


    def switch_view(self, view_name):
        # Placeholder for switching views
        self.viewer.configure(image=None, text=f"{view_name.capitalize()} view - under construction")
        self.page_label.configure(text="Page: -")
        self.current_doc = None
        self.total_pages = 0
        self.current_page = 0


if __name__ == "__main__":
    app = PDFReaderApp()
    app.mainloop()

