import os
import pandas as pd
import openai

# Load API key from environment variable
client = openai.OpenAI(api_key="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")

# Replace with your actual CSV file path
csv_file_path = "books_list.csv"

def generate_abstract(title, author):
    prompt = f"Write a 100-word abstract for the book titled '{title}' by {author}."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


try:
    # Read the full CSV, and convert relevant columns to appropriate types
    df = pd.read_csv(csv_file_path)

    df['isbn13'] = df['isbn13'].astype(int)
    df['original_publication_year'] = df['original_publication_year'].astype(int)

    print("Selected columns from the CSV file:")
    line = "insert into book (title, author, published, abstract, isbn10, isbn13, coverpath) values"
    
    # Generate abstracts for up to 5 books
    for i, (_, row) in enumerate(df.iterrows()):
        if i == 5:
            break

        title = row['original_title']
        author = row['authors']
        isbn13 = str(row['isbn13'])
        year = row['original_publication_year']

        abstract = generate_abstract(title, author)
        print(f"\nAbstract for '{title}' by {author}:\n{abstract}\n")

except FileNotFoundError:
    print(f"Error: The file '{csv_file_path}' was not found.")
except ValueError as e:
    print(f"ValueError: {e}")
except pd.errors.EmptyDataError:
    print(f"Error: The file '{csv_file_path}' is empty.")
except pd.errors.ParserError:
    print(f"Error: The file '{csv_file_path}' could not be parsed.")

