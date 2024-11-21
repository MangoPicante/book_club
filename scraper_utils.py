# Contains common utility functions for scrapers
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

# Returns BeautifulSoup for the given url
def soup_cooker(url, js_bool=False):
    print('Scraping:', url)
    # gets the html from the url using requests
    html = None
    if not js_bool: # use requests to fetch the HTML content
        # set the headers
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
    else: # fetch the HTML content from the URL using Selenium
        # set the options
        options = Options()
        options.headless = True
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        html = driver.page_source
        driver.quit()
    # parse into soup
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def try_except_wrapper(func, arg):
    try:
        return func(arg)
    except Exception as e:
        print(f'Error scraping {func.__name__}')
        print(f'Exception: {e}')
        return None