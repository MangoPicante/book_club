from bs4 import BeautifulSoup
import pandas as pd
import requests
import webbrowser
# Returns BeautifulSoup for the given url
def soup_cooker(url):
    # Fetch
    try:
        response = requests.get(url)
    except Exception as e:
        print('Connection Error', str(e))
        return None
    # Parse
    soup = BeautifulSoup(response.text, 'html.parser')
    # extracts title from soup
    title = soup.find('title').contents[0]
    print('Scraping:',title)
    return soup
# Returns the url that matches the book name 
def url(row):
    book = row['book'].lower()
    soup = soup_cooker(row['goodreads search'])
    # finds the anchor tags of the first page
    anchor_tags = soup.find_all('a', {'class' : 'bookTitle'})
    # splits the anchor tags into title and converts href into a full url, trimming search info
    title_url_tuples = [(anchor_tag.span.text.lower(), 'https://www.goodreads.com' + anchor_tag['href'].split('?')[0]) for anchor_tag in anchor_tags]
    # finds the author tags of the first page
    author_tags = soup.find_all('span', {'itemprop' : 'author'})
    # creates a mask of any results that contain an adapter in the author list
    mask = [len(author_tag.find_all(string='(Adapter)')) == 0 for author_tag in author_tags]
    search_results = [tuple for tuple, bool in zip(title_url_tuples, mask) if bool]
    # checks search results for exact matches to the title, returns the first matching url
    for result in search_results:
        if result[0] == book:
            return result[1]
    # checks search results for titles that start with the book, returns first matching url
    for result in search_results:
        if result[0].startswith(book):
            return result[1]
    # automatically opens the search url of a book title that isn't found
    browser = webbrowser.get('windows-default')
    browser.open(row['goodreads search'])
    return None
# Returns the soup's rating
def rating(soup):
    try:
        return float(soup.find('div', {'class': 'RatingStatistics__rating'}).contents[0])
    except:
        print('Error finding the rating in soup:', soup.find('title').contents[0])
        return None
# Returns the soup's genre
def genre(soup):
    try:
        # generates a list of genre tags
        tags = soup.find('ul', {'aria-label': 'Top genres for this book'}).find_all('span', {'class' : 'Button__labelItem'})
        # gets the content of each tag in the list
        genres = [genre.contents[0] for genre in tags]
        # removes the last category if it is ...more
        if genres[-1] == '...more':
            del genres[-1]
        return genres
    except:
        print('Error finding the categories in soup:', soup.find('title').contents[0])
        return None
# Returns the soup's publication date
def published(soup):
    try:
        contents = soup.find('p', {'data-testid' : 'publicationInfo'}).contents[0]
        date = contents.replace('First published ', '').replace('Published ', '')
        return pd.to_datetime(date, format='%B %d, %Y')
    except:
        print('Error finding the publication info in soup:', soup.find('title').contents[0])
        return None
# Returns the soup's page count
def pages(soup):
    try:
        contents = soup.find('p', {'data-testid' : 'pagesFormat'}).contents[0]
        return int(contents.split(' ')[0])
    except:
        print('Error finding the pages in soup:', soup.find('title').contents[0])
        return None
# Returns the soup's author
def author(soup):
    try:
        return soup.find('span', {'class' : 'ContributorLink__name'}).contents[0]
    except:
        print('Error finding the author in soup:', soup.find('title').contents[0])
        return None
# Returns a Series of the scraped data
def scrape(url):
    # cooks the url into a soup
    soup = soup_cooker(url)
    # collects all the scraped data and returns it as a Series
    return pd.Series([rating(soup), genre(soup), author(soup), pages(soup), published(soup)])