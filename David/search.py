import requests

def search_openlibrary():
    print("Search OpenLibrary")
    print("Choose search type:")
    print("1. Title")
    print("2. Author")
    print("3. ISBN")
    
    choice = input("Enter choice (1/2/3): ").strip()
    
    search_types = {"1": "title", "2": "author", "3": "isbn"}
    search_type = search_types.get(choice)

    if not search_type:
        print("Invalid choice.")
        return

    query = input(f"Enter the {search_type}: ").strip()
    base_url = "https://openlibrary.org/search.json"
    params = {search_type: query}

    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        results = data.get('docs', [])
        
        if not results:
            print("No results found.")
            return
        
        print(f"\nTop results for {search_type} '{query}':")
        for i, book in enumerate(results[:10], 1):  
            title = book.get('title', 'N/A')
            author = ", ".join(book.get('author_name', ['Unknown']))
            year = book.get('first_publish_year', 'N/A')
            print(f"{i}. {title} by {author} (First Published: {year})")
    else:
        print("Error fetching data from OpenLibrary API.")

# Run 
search_openlibrary()
