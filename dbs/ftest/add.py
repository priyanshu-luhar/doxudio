import os
import pandas as pd
import requests

# Create output folder for cover images
os.makedirs("cov", exist_ok=True)

# Load the dataset
df = pd.read_csv("books_list.csv")

# Clean and convert types
df['isbn13'] = df['isbn13'].astype('int64').astype(str)
df['original_publication_year'] = df['original_publication_year'].astype(int)

# SQL: Create table
print("""CREATE TABLE IF NOT EXISTS book (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    published DATE NOT NULL,
    abstract TEXT NOT NULL,
    isbn10 TEXT NOT NULL,
    isbn13 TEXT NOT NULL,
    coverpath TEXT
);\n""")

print("-- Insert Statements --")

# Process each book
for idx, row in df.iterrows():
    if not all(k in row and pd.notna(row[k]) for k in ['original_title', 'authors', 'isbn', 'isbn13', 'original_publication_year', 'image_url']):
        continue

    title = row['original_title'].replace("'", "''")
    author = row['authors'].replace("'", "''")
    isbn10 = str(row['isbn'])
    isbn13 = str(row['isbn13'])
    year = int(row['original_publication_year'])

    # Image download
    img_url = row['image_url']
    img_path = f"cov/{isbn13}.jpg"
    simg_path = f"/home/stu/pluhar/public_html/doxudio/public/str/cov/{isbn13}.jpg"
    try:
        img_data = requests.get(img_url, timeout=10)
        with open(img_path, "wb") as f:
            f.write(img_data.content)
    except Exception as e:
        print(f"-- Failed to download image for '{title}': {e}")
        img_path = ""

    # Use placeholder for abstract
    abstract = "No abstract available."

    # SQL Insert
    print(f"INSERT INTO book (title, author, published, abstract, isbn10, isbn13, coverpath) VALUES ('{title}', '{author}', '{year}', '{abstract}', '{isbn10}', '{isbn13}', '{simg_path}');")

    # Uncomment below to test with first few records only
    # if idx == 4: break

