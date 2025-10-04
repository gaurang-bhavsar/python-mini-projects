import requests
from bs4 import BeautifulSoup

def simple_wiki_scraper(url):
    """
    Scrapes the title and all paragraph texts from a given URL.

    Args:
        url (str): The URL of the webpage to scrape.
    """
    try:
        # 1. Fetch the webpage content
        # Use a common User-Agent header to mimic a browser, which can help
        # avoid being blocked by some websites.
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        # 2. Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        print(f"--- Successfully Scraped: {url} ---")
        print("\n")

        # 3. Extract the Title
        title = soup.find('h1', id='firstHeading')
        if title:
            print("🚀 **TITLE** 🚀")
            print(title.text)
            print("-" * 30)

        # 4. Extract all Paragraphs
        print("\n📝 **PARAGRAPH TEXTS** 📝")
        paragraphs = soup.find_all('p') # Finds all <p> tags on the page

        # Limit the output to the first few paragraphs for conciseness
        for i, p in enumerate(paragraphs[:5]):
            if p.text.strip(): # Check if the paragraph is not just empty space
                print(f"Paragraph {i+1}:\n{p.text.strip()}\n")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# URL to scrape (Wikipedia page for Web scraping)
WIKI_URL = 'https://en.wikipedia.org/wiki/Web_scraping'

# Run the scraper
simple_wiki_scraper(WIKI_URL)
