import requests
import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def add_user_to_server(uname, fname, lname, password_hash):
    url = "https://artemis.cs.csub.edu/~pluhar/doxudio/public/api/add_user.php"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "uname": uname,
        "fname": fname,
        "lname": lname,
        "hash": password_hash
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

def add_book_to_server(title, author, published, abstract, isbn10, isbn13, coverpath=None):
    url = "https://artemis.cs.csub.edu/~pluhar/doxudio/public/api/add_book.php"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "title": title,
        "author": author,
        "published": published,  # format: YYYY-MM-DD
        "abstract": abstract,
        "isbn10": isbn10,
        "isbn13": isbn13,
        "coverpath": coverpath
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

def add_library_to_server(name, creator_id):
    url = "https://artemis.cs.csub.edu/~pluhar/doxudio/public/api/add_library.php"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "name": name,
        "creator_id": creator_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

def add_review_to_server(book_id, reviewer_id, rating, content):
    url = "https://artemis.cs.csub.edu/~pluhar/doxudio/public/api/add_review.php"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "book_id": book_id,
        "reviewer_id": reviewer_id,
        "rating": rating,
        "content": content
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

def add_book_to_library(library_id, book_id):
    url = "https://artemis.cs.csub.edu/~pluhar/doxudio/public/api/add_lib_book.php"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "library_id": library_id,
        "book_id": book_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

def search_book(isbn=None, title=None, author=None):
    url = "https://artemis.cs.csub.edu/~pluhar/doxudio/public/api/get_book.php"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {}
    if isbn:
        payload['isbn'] = isbn
    if title:
        payload['title'] = title
    if author:
        payload['author'] = author

    if not payload:
        return {"error": "You must provide at least one of: isbn, title, or author."}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

def get_library_with_books(library_id):
    url = "https://artemis.cs.csub.edu/~pluhar/doxudio/public/api/get_library.php"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "library_id": library_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

def get_reviews_for_book(book_id):
    url = "https://artemis.cs.csub.edu/~pluhar/doxudio/public/api/get_review.php"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "book_id": book_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

def login_user(uname, password_hash):
    url = "https://artemis.cs.csub.edu/~pluhar/doxudio/public/api/get_user.php"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "uname": uname,
        "password_hash": password_hash
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "success":
            return {"status": "success", "user": data["user"]}
        elif data.get("status") == "wrong_password":
            return {"status": "wrong_password", "message": "Incorrect password."}
        elif data.get("status") == "no_user":
            return {"status": "no_user", "message": "Username does not exist."}
        else:
            return {"status": "error", "message": "Unexpected response."}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": f"Request failed: {e}"}

if __name__ == "__main__":

    '''
    user_data = {
        "uname": "pluhar",
        "fname": "Priyanshu",
        "lname": "Luhar",
        "password_hash": hash_password("hello")  # Hash before passing here
    }
    result = add_user_to_server(**user_data)
    result = add_book_to_server(
        title="Clean Code",
        author="Robert C. Martin",
        published="2008-08-01",
        abstract="A handbook of agile software craftsmanship.",
        isbn10="0132350882",
        isbn13="9780132350884",
        coverpath="/covers/cleancode.jpg"
    )
    result = add_library_to_server(
        name="Digital Physics Library",
        creator_id=4
    )
    result = add_review_to_server(
        book_id=1,
        reviewer_id=4,
        rating=5,
        content="An insightful book with a compelling narrative."
    )
    result = add_book_to_library(
        library_id=1,
        book_id=1
    )
    # Search by ISBN
    result = search_book(isbn="0132350882")
    print("Search by ISBN:", result)

    # Search by title
    result = search_book(title="clean")
    print("Search by title:", result)

    # Search by author
    result = search_book(author="martin")
    print("Search by author:", result)
    result = get_library_with_books(1)
    result = get_reviews_for_book(1)
    result = login_user("pluhar", hash_password("hello"))
    '''
    
    print(result)


