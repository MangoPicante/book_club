# Contains common utility functions for scrapers
from bs4 import BeautifulSoup
import requests

# Returns BeautifulSoup for the given url
def soup_cooker(url):
    print('Scraping:', url)
    # gets the html from the url and parses it with BeautifulSoup
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    session = requests.Session()
    session.headers.update(headers)
    try:
        # fetch the HTML content from the URL
        response = session.get(url, timeout=10)
        # raise an exception for HTTP errors
        response.raise_for_status()
        html = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
    # parse into soup
    soup = BeautifulSoup(html, 'html.parser')
    # extracts title from soup
    title = soup.find('title').text
    print('Scraping:', title)
    return soup