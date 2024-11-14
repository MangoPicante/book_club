import reader
import goodreads_scraper as gscr
import audible_scraper as ascr
from os.path import exists
if exists('book_club.json'):
    book_club = reader.json_reader('book_club.json')
else:
    book_club = reader.csv_reader('Book Club - Ratings.csv')
    # scrapes goodreads search column for book urls
    book_club['g_url'] = book_club.apply(gscr.url, axis=1)
    # scrapes goodreads data from urls
    book_club[['g_rating', 'g_genre', 'g_author', 'g_pages', 'g_published']] = book_club.apply(gscr.scrape)
    # scrapes audible search column for book urls
    book_club['a_url'] = book_club.apply(ascr.url, axis=1)
    # scrapes audible data from urls
    book_club[['a_ratings', 'a_runtime', 'a_author', 'a_narrator', 'a_categories', 'a_tags']] = book_club.apply(ascr.scrape)
    
    # saves the data to a json file
    book_club.to_json('book_club.json', orient='records')