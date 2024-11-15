# Scrapes goodreads for book data
import scraper_utils as scu
import pandas as pd

# Returns the soup's rating
def rating(soup):
    rating = float(soup.find('div', {'class': 'RatingStatistics__rating'}).text)
    return rating
# Returns the soup's genre
def genre(soup):
    # generates a list of genre tags
    tags = soup.find('ul', {'aria-label': 'Top genres for this book'}).find_all('span', {'class' : 'Button__labelItem'})
    # gets the content of each tag in the list
    genres = [genre.contents[0] for genre in tags]
    # removes the last category if it is ...more
    if genres[-1] == '...more':
        del genres[-1]
    return genres
# Returns the soup's publication date
def published(soup):
    contents = soup.find('p', {'data-testid' : 'publicationInfo'}).text
    date = contents.replace('First published ', '').replace('Published ', '')
    return pd.to_datetime(date, format='%B %d, %Y')
# Returns the soup's page count
def pages(soup):
    contents = soup.find('p', {'data-testid' : 'pagesFormat'}).text
    return int(contents.split(' ')[0])
# Returns the soup's author
def author(soup):
    author = soup.find('span', {'class' : 'ContributorLink__name'}).text
    return author
# Returns a Series of the scraped data from goodreads
def scrape(row):
    # cooks the url into a soup
    soup = scu.soup_cooker(row['g_url'])
    # collects all the scraped data and returns it as a Series
    ser = pd.Series([scu.try_except_wrapper(rating, soup), scu.try_except_wrapper(genre, soup), scu.try_except_wrapper(author, soup), scu.try_except_wrapper(pages, soup), scu.try_except_wrapper(published, soup)])
    return ser