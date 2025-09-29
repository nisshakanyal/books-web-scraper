import requests
from bs4 import BeautifulSoup
import pandas as pd

books = []

# Loop through all 50 pages
for page in range(1, 51):
    print(f"Scraping page {page}...")  # <-- This line shows progress
    url = f"http://books.toscrape.com/catalogue/page-{page}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    for book in soup.find_all("article", class_="product_pod"):
        title = book.h3.a["title"]
        price = book.find("p", class_="price_color").text
        rating = book.p["class"][1]
        availability = book.find("p", class_="instock availability").text.strip()
        
        books.append([title, price, rating, availability])

df = pd.DataFrame(books, columns=["Title", "Price", "Rating", "Availability"])
# Remove any non-numeric characters and convert to float
df['Price'] = df['Price'].str.replace('£', '').str.replace('Â', '').astype(float)
rating_map = {'One':1, 'Two':2, 'Three':3, 'Four':4, 'Five':5}
df['Rating'] = df['Rating'].map(rating_map)
df.to_csv("all_books.csv", index=False)

print("Scraping complete. Data saved to all_books.csv")
