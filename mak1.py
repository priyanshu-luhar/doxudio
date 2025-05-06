import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QTextEdit, QListWidget,
    QGroupBox, QSplitter, QMessageBox
)
from PyQt6.QtCore import Qt


class BookSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Book Search with OpenLibrary")
        self.setGeometry(100, 100, 900, 600)
        
        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Search area
        search_group = QGroupBox("Search Options")
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search term...")
        
        self.title_btn = QPushButton("Search by Title")
        self.author_btn = QPushButton("Search by Author")
        self.isbn_btn = QPushButton("Search by ISBN")
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.title_btn)
        search_layout.addWidget(self.author_btn)
        search_layout.addWidget(self.isbn_btn)
        search_group.setLayout(search_layout)
        
        # Results and preview area
        results_preview_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Results list
        self.results_list = QListWidget()
        self.results_list.setMinimumWidth(300)
        
        # Preview pane
        preview_group = QGroupBox("Book Preview")
        preview_layout = QVBoxLayout()
        
        self.preview_title = QLabel("No book selected")
        self.preview_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.preview_author = QLabel("")
        self.preview_details = QTextEdit()
        self.preview_details.setReadOnly(True)
        
        preview_layout.addWidget(self.preview_title)
        preview_layout.addWidget(self.preview_author)
        preview_layout.addWidget(self.preview_details)
        preview_group.setLayout(preview_layout)
        
        results_preview_splitter.addWidget(self.results_list)
        results_preview_splitter.addWidget(preview_group)
        results_preview_splitter.setSizes([300, 600])
        
        # Add widgets to main layout
        main_layout.addWidget(search_group)
        main_layout.addWidget(results_preview_splitter)
        
        # Connect signals
        self.title_btn.clicked.connect(lambda: self.search_books("title"))
        self.author_btn.clicked.connect(lambda: self.search_books("author"))
        self.isbn_btn.clicked.connect(lambda: self.search_books("isbn"))
        self.results_list.itemClicked.connect(self.show_book_preview)
        self.results_list.itemDoubleClicked.connect(self.open_book_details)
        
        # Store search results
        self.current_results = []
    
    def search_books(self, search_type):
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Warning", "Please enter a search term.")
            return
        
        base_url = "https://openlibrary.org/search.json"
        params = {search_type: query}
        
        try:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                self.current_results = data.get('docs', [])
                self.display_results()
            else:
                QMessageBox.critical(self, "Error", "Failed to fetch data from OpenLibrary API.")
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Error", f"Network error: {str(e)}")
    
    def display_results(self):
        self.results_list.clear()
        
        if not self.current_results:
            self.results_list.addItem("No results found")
            return
        
        for book in self.current_results[:50]:  # Limit to 50 results
            title = book.get('title', 'N/A')
            author = ", ".join(book.get('author_name', ['Unknown']))
            year = book.get('first_publish_year', '')
            
            item_text = f"{title}"
            if author:
                item_text += f" by {author}"
            if year:
                item_text += f" ({year})"
            
            self.results_list.addItem(item_text)
    
    def show_book_preview(self, item):
        index = self.results_list.row(item)
        if index < 0 or index >= len(self.current_results):
            return
        
        book = self.current_results[index]
        
        # Set title and author
        title = book.get('title', 'N/A')
        authors = ", ".join(book.get('author_name', ['Unknown']))
        self.preview_title.setText(title)
        self.preview_author.setText(f"by {authors}")
        
        # Build details text
        details = []
        
        if 'first_publish_year' in book:
            details.append(f"First Published: {book['first_publish_year']}")
        
        if 'publisher' in book:
            details.append(f"Publisher: {', '.join(book['publisher'])}")
        
        if 'language' in book:
            details.append(f"Language: {', '.join(book['language'])}")
        
        if 'subject' in book:
            details.append("\nSubjects:")
            details.extend([f"- {s}" for s in book['subject'][:5]])
        
        if 'isbn' in book:
            details.append("\nISBNs:")
            details.extend([f"- {isbn}" for isbn in book['isbn'][:3]])
        
        self.preview_details.setText("\n".join(details))
    
    def open_book_details(self, item):
        index = self.results_list.row(item)
        if index < 0 or index >= len(self.current_results):
            return
        
        book = self.current_results[index]
        details_window = BookDetailsWindow(book)
        details_window.show()


class BookDetailsWindow(QMainWindow):
    def __init__(self, book_data):
        super().__init__()
        self.setWindowTitle("Book Details")
        self.setGeometry(200, 200, 600, 500)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Title
        title = book_data.get('title', 'N/A')
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Author
        authors = ", ".join(book_data.get('author_name', ['Unknown']))
        author_label = QLabel(f"by {authors}")
        author_label.setStyleSheet("font-size: 14px;")
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(author_label)
        
        # Details
        details_text = QTextEdit()
        details_text.setReadOnly(True)
        
        details = []
        
        if 'first_publish_year' in book_data:
            details.append(f"First Published: {book_data['first_publish_year']}")
        
        if 'publisher' in book_data:
            details.append(f"Publisher: {', '.join(book_data['publisher'])}")
        
        if 'language' in book_data:
            details.append(f"Language: {', '.join(book_data['language'])}")
        
        if 'subject' in book_data:
            details.append("\nSubjects:")
            details.extend([f"- {s}" for s in book_data['subject'][:10]])
        
        if 'isbn' in book_data:
            details.append("\nISBNs:")
            details.extend([f"- {isbn}" for isbn in book_data['isbn'][:5]])
        
        if 'edition_count' in book_data:
            details.append(f"\nEdition Count: {book_data['edition_count']}")
        
        if 'cover_edition_key' in book_data:
            cover_url = f"https://covers.openlibrary.org/b/olid/{book_data['cover_edition_key']}-L.jpg"
            details.append(f"\nCover Image: {cover_url}")
        
        details_text.setText("\n".join(details))
        layout.addWidget(details_text)
        
        # OpenLibrary link
        if 'key' in book_data:
            ol_key = book_data['key']
            ol_link = f"https://openlibrary.org{ol_key}"
            link_label = QLabel(f'<a href="{ol_link}">View on OpenLibrary</a>')
            link_label.setOpenExternalLinks(True)
            layout.addWidget(link_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookSearchApp()
    window.show()
    sys.exit(app.exec())