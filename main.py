import reader
import goodreads_scraper as gscr
import audible_scraper as ascr
from os.path import exists

def json_save_prompt(df, filename):
    # saves the data to a json file if prompt accepted
    prompt = input('Save data to json? (y/n): ')
    if prompt == 'y':
        df.to_json(filename + '.json', orient='records')

def column_backfill(df, columns, scraper):
    if not all(column in df.columns for column in columns):
        df[columns] = df.apply(scraper, axis=1)
    else:
        mask = df[columns].isnull()
        df.loc[mask, columns] = df[mask].apply(scraper, axis=1)
    return df

if exists('book_club.json'):
    book_club = reader.json_reader('book_club.json')
    # attempts to fill in all missing values
    book_club = column_backfill(book_club, 'g_url', gscr.url)
    json_save_prompt(book_club, 'book_club')
    book_club = column_backfill(book_club, ['g_rating', 'g_genre', 'g_author', 'g_pages', 'g_published'], gscr.scrape)
    json_save_prompt(book_club, 'book_club')
    book_club = column_backfill(book_club, 'a_url', ascr.url)
    json_save_prompt(book_club, 'book_club')
    book_club = column_backfill(book_club, ['a_ratings', 'a_runtime', 'a_author', 'a_narrator', 'a_categories', 'a_tags'], ascr.scrape)
    json_save_prompt(book_club, 'book_club')
    
else:
    try:
        book_club = reader.csv_reader('Book Club - Ratings.csv')
        print(book_club.head())
        # scrapes goodreads search column for book urls
        book_club['g_url'] = book_club.apply(gscr.url, axis=1)
        json_save_prompt(book_club, 'book_club')
        # scrapes goodreads data from urls
        book_club[['g_rating', 'g_genre', 'g_author', 'g_pages', 'g_published']] = book_club.apply(gscr.scrape)
        json_save_prompt(book_club, 'book_club')
        # scrapes audible search column for book urls
        book_club['a_url'] = book_club.apply(ascr.url, axis=1)
        json_save_prompt(book_club, 'book_club')
        # scrapes audible data from urls
        book_club[['a_ratings', 'a_runtime', 'a_author', 'a_narrator', 'a_categories', 'a_tags']] = book_club.apply(ascr.scrape)
        json_save_prompt(book_club, 'book_club')
    except Exception as e:
        print(f"Error: {e}")
    