import requests
from bs4 import BeautifulSoup
import csv

base_url = input("Enter website URL: ").strip()

if not base_url.startswith(("http://", "https://")):
    base_url = "https://" + base_url

url = base_url

with open("quotes.csv", "w", newline="", encoding="utf-8-sig") as file:
    writer = csv.writer(file, delimiter=";")

    writer.writerow(["Quote", "Author", "Tags"])

    page = 1

    while url:
        print(f"Scraping page {page}...")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(f"❌ Could not access the website: {error}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        quotes = soup.find_all("div", class_="quote")

        for quote in quotes:
            text = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text

            tags = quote.find_all("a", class_="tag")
            tags_text = ", ".join(tag.text for tag in tags)

            writer.writerow([text, author, tags_text])

        next_page = soup.find("li", class_="next")

        if next_page:
            next_url = next_page.find("a")["href"]
            url = base_url + next_url
            page += 1
        else:
            url = None

print("Scraping completed!")
print(f"Total pages scraped: {page}")
print("Data saved to quotes.csv")