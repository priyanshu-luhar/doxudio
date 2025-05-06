import sys
import requests
from io import BytesIO
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QComboBox, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame
)
from PyQt6.QtGui import QPixmap, QDesktopServices
from PyQt6.QtCore import Qt, QUrl


class BookSearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OpenLibrary Book Search")
        self.setGeometry(100, 100, 600, 600)

        # Search bar
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter your search term")

        self.search_type_dropdown = QComboBox()
        self.search_type_dropdown.addItems(["title", "author", "isbn"])

        self.search_button = QPushButton("Search")

        # Results
        self.results_area = QScrollArea()
        self.results_content = QVBoxLayout()
        self.results_widget = QWidget()
        self.results_widget.setLayout(self.results_content)
        self.results_area.setWidget(self.results_widget)
        self.results_area.setWidgetResizable(True)

        # Layout
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.query_input)
        top_layout.addWidget(self.search_type_dropdown)
        top_layout.addWidget(self.search_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.results_area)
        self.setLayout(main_layout)

        # Events
        self.search_button.clicked.connect(self.search_books)

    def search_books(self):
        # Clear previous results
        for i in reversed(range(self.results_content.count())):
            widget = self.results_content.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        query = self.query_input.text().strip()
        search_type = self.search_type_dropdown.currentText()
        if not query:
            self.add_text_result("Please enter a search term.")
            return

        url = "https://openlibrary.org/search.json"
        params = {search_type: query}

        try:
            response = requests.get(url, params=params)
            if response.status_code != 200:
                self.add_text_result("Failed to fetch data.")
                return

            data = response.json()
            books = data.get("docs", [])
            if not books:
                self.add_text_result("No results found.")
                return

            for book in books[:10]:
                title = book.get("title", "N/A")
                authors = ", ".join(book.get("author_name", ["Unknown"]))
                year = book.get("first_publish_year", "N/A")
                cover_id = book.get("cover_i", None)
                key = book.get("key", "")

                # Full OpenLibrary URL
                book_url = f"https://openlibrary.org{key}" if key else ""

                book_frame = QFrame()
                book_layout = QHBoxLayout()

                # Cover image
                if cover_id:
                    img_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                    try:
                        img_data = requests.get(img_url).content
                        pixmap = QPixmap()
                        pixmap.loadFromData(BytesIO(img_data).read())
                        img_label = QLabel()
                        img_label.setPixmap(pixmap.scaledToHeight(120, Qt.TransformationMode.SmoothTransformation))
                        book_layout.addWidget(img_label)
                    except:
                        pass

                # Book info with link
                book_info = f"<b>{title}</b><br>by {authors}<br>First Published: {year}"
                if book_url:
                    book_info += f'<br><a href="{book_url}">View on OpenLibrary</a>'

                info_label = QLabel(book_info)
                info_label.setOpenExternalLinks(True)
                info_label.setTextFormat(Qt.TextFormat.RichText)
                info_label.setWordWrap(True)

                book_layout.addWidget(info_label)
                book_frame.setLayout(book_layout)
                self.results_content.addWidget(book_frame)

        except Exception as e:
            self.add_text_result(f"Error: {e}")

    def add_text_result(self, message):
        msg = QLabel(message)
        self.results_content.addWidget(msg)


# Run app
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookSearchApp()
    window.show()
    sys.exit(app.exec())
