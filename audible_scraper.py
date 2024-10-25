# Scrapes audible for book data
from scraper_utils import soup_cooker
import pandas as pd
import webbrowser
import re

# Returns the url that matches the book name in the dataframe's row using row['audible search'] and row['book']
def url(row):
    book = row['book'].lower()
    soup = soup_cooker(row['audible search'])
    # finds the anchor tags of the first page
    anchor_tags = soup.find_all('a', {'class' : 'bc-link bc-color-link'})
    # splits the anchor tags into title and converts href into a full url, trimming search info
    title_url_tuples = [(anchor_tag.text.lower(), 'https://www.audible.com' + anchor_tag['href'].split('?')[0]) for anchor_tag in anchor_tags]
    # checks search results for exact matches to the title, returns the first matching url
    for result in title_url_tuples:
        if result[0] == book:
            return result[1]
    # checks search results for titles that start with the book, returns first matching url
    for result in title_url_tuples:
        if result[0].startswith(book):
            return result[1]
    # automatically opens the search url of a book title that isn't found
    browser = webbrowser.get('windows-default')
    browser.open(row['audible search'])
    return None
# Returns the soup's rating
def rating(soup):
    try:
        # finds the li tag with the rating using regex to match the class
        li_tag = soup.find('li', class_=re.compile(r'\bbc-list-item\s+ratingsLabel\}'))
        # returns the rating from the span tag within the li tag
        return float(li_tag.find('span', {'class': 'bc-text', 'aria-hidden': 'true'}).text)
    except:
        print('Error finding the rating in soup:', soup.find('title').contents[0])
        return None
def runtime(soup):
    try:
        # finds the li tag with the runtime
        runtime_text = soup.find('li', {'class': 'bc-list-item runtimeLabel'}).text
        # converts the runtime text into a list of integers
        runtime_list = re.findall(r'\d+', runtime_text)
        # converts the list of integers into a single integer
        if len(runtime_list) == 2:
            runtime = int(runtime_list[0]) * 60 + int(runtime_list[1])
        else:
            runtime = int(runtime_list[0] * 60)
        return runtime
    except:
        print('Error finding the runtime in soup:', soup.find('title').contents[0])
        return None
def author(soup):
    try:
        # finds the author li tag
        li_tag = soup.find('li', {'class': 'bc-list-item authorLabel'})
        # returns the author from the a tag within the li tag
        return li_tag.find('a').text
    except:
        print('Error finding the author in soup:', soup.find('title').contents[0])
        return None
def narrator(soup):
    try:
        # finds the narrator li tag
        li_tag = soup.find('li', {'class': 'bc-list-item narratorLabel'})
        # returns the narrator from the a tag within the li tag
        return li_tag.find('a').text
    except:
        print('Error finding the narrator in soup:', soup.find('title').contents[0])
        return None
def categories(soup):
    try:
        # finds the categories li tag
        li_tag = soup.find('li', {'class': 'bc-list-item categoriesLabel'})
        # returns the categories from the a tag within the li tag
        category_string = li_tag.find('a').text
        # parses the categories into a list
        categories = re.split(r',\s*|\s&\s', category_string)
        return categories
    except:
        print('Error finding the categories in soup:', soup.find('title').contents[0])
        return None
def tags(soup):
    try:
        # finds the tags div tag
        div_tag = soup.find('div', {'class': 'bc-section bc-chip-group'})
        # finds all the span tags with class bc-chip-text within the div tag
        span_tags = div_tag.find_all('span', {'class': 'bc-chip-text'})
        tags = [span_tag.text.strip() for span_tag in span_tags]
        return tags
    except:
        print('Error finding the tags in soup:', soup.find('title').contents[0])
        return None
def scrape(row):
    a_url = url(row)
    soup = soup_cooker(a_url)
    return pd.Series([a_url, rating(soup), runtime(soup), author(soup), narrator(soup), categories(soup), tags(soup)])