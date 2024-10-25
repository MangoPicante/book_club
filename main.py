import reader
import goodreads_scraper as gs
from os.path import exists
if exists('book_club.json'):
    book_club = reader.json_reader('book_club.json')
else:
    book_club = reader.csv_reader('Book Club - Ratings.csv')
    # scrapes goodreads search column for book urls
    book_club['g_url'] = book_club.apply(gs.url, axis=1)
    # scrapes goodreads data from urls
    book_club[['g_rating', 'g_genre', 'g_author', 'g_pages', 'g_published']] = book_club.apply(gs.scrape)
        
    # scrape audible data
    
    # saves the data to a json file
    book_club.to_json('book_club.json', orient='records')
    
print(book_club)