import reader
import goodreads_scraper as gs
from os.path import exists
if exists('book_club.json'):
    book_club = reader.json_reader('book_club.json')
else:
    book_club = reader.csv_reader('Book Club - Ratings.csv')
if 'goodreads' in book_club.columns:
    mask = book_club['goodreads'].isnull()
    book_club.loc[mask,['g_rating', 'g_genre', 'g_author', 'g_pages', 'g_published']] = book_club[mask].apply(gs.url, axis=1).apply(gs.scrape)
    book_club.to_json('book_club.json', orient='records')
else:
    book_club[['g_rating', 'g_genre', 'g_author', 'g_pages', 'g_published']] = book_club.apply(gs.url, axis=1).apply(gs.scrape)
    book_club.to_json('book_club.json', orient='records')