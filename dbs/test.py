import os
import pandas as pd
import openai

# Replace with your actual CSV file path
csv_file_path = "books_list.csv"

# List the specific columns you want to print
columns_to_display = ["isbn13", "original_title"]

openai.api_key = "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"


def generate_abstract(title, author):
    prompt = f"Write a 100-word abstract for the book titled '{title}' by {author}."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message["content"]


try:
    # Read only the specified columns from the CSV file
    #df = pd.read_csv(csv_file_path, usecols=columns_to_display)
    df = pd.read_csv(csv_file_path)

    df['isbn13'] = df['isbn13'].astype(int)
    #df['isbn'] = df['isbn'].astype(int)
    df['original_publication_year'] = df['original_publication_year'].astype(int)

    # Print the selected columns
    print("Selected columns from the CSV file:")
    line = "insert into book (title, author, published, abstract, isbn10, isbn13, coverpath) values"
    i = 0
    for index, row in df.iterrows():
        title = row['original_title']
        author = row['authors']
        #isbn10 = str(row['isbn'])
        isbn13 = str(row['isbn13'])
        year = row['original_publication_year']
        i = i + 1
        if i == 5:
            break

        res = generate_abstract(title, author)
        print(res)
        #print(f"{isbn13}    {title}    {year}")
        

except FileNotFoundError:
    print(f"Error: The file '{csv_file_path}' was not found.")
except ValueError as e:
    print(f"Error: {e}")
except pd.errors.EmptyDataError:
    print(f"Error: The file '{csv_file_path}' is empty.")
except pd.errors.ParserError:
    print(f"Error: The file '{csv_file_path}' could not be parsed.")

