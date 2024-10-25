# Contains common utility functions for scrapers
from bs4 import BeautifulSoup
import requests

# Returns BeautifulSoup for the given url
def soup_cooker(url):
    fetched = False
    # fetch, retrying if connection fails
    while not fetched:
        try:
            response = requests.get(url)
        except Exception as e:
            print('Connection Error', str(e))
            return None
        else:
            fetched = True
    # parse into soup
    soup = BeautifulSoup(response.text, 'html.parser')
    # extracts title from soup
    title = soup.find('title').contents[0]
    print('Scraping:',title)
    return soup