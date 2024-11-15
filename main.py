import file_io
import goodreads_scraper as gscr
import audible_scraper as ascr
from os.path import exists

def column_backfill(df, columns, scraper):
    if not all(column in df.columns for column in columns):
        print(f'Columns {columns} not found in dataframe')
        df[columns] = df.apply(scraper, axis=1)
    else:
        mask = df[columns].isnull().any(axis=1)
        print(f'Filling {mask.sum().sum()} missing values in {columns} with {scraper.__name__}')
        df.loc[mask, columns] = df[mask].apply(scraper, axis=1)
    return df

if exists('book_club.json'):
    book_club = file_io.json_reader('book_club.json')
    print(book_club.head())
    # attempts to fill in all missing values
    book_club = column_backfill(book_club, ['g_rating', 'g_genre', 'g_author', 'g_pages', 'g_published'], gscr.scrape)
    file_io.save(book_club, 'book_club', 'json')
    book_club = column_backfill(book_club, ['a_ratings', 'a_runtime', 'a_author', 'a_narrator', 'a_categories', 'a_tags'], ascr.scrape)
    file_io.save(book_club, 'book_club', 'json')
    
else:
    try:
        book_club = file_io.csv_reader('Book Club - Ratings.csv')
        print(book_club.head())
        # scrapes goodreads data from urls
        book_club[['g_rating', 'g_genre', 'g_author', 'g_pages', 'g_published']] = book_club.apply(gscr.scrape, axis=1)
        file_io.save(book_club, 'book_club', 'json')
        # scrapes audible data from urls
        book_club[['a_ratings', 'a_runtime', 'a_author', 'a_narrator', 'a_categories', 'a_tags']] = book_club.apply(ascr.scrape, axis=1)
        file_io.save(book_club, 'book_club', 'json')
    except Exception as e:
        print(f"Error: {e}")
print(book_club.dtypes)
file_io.save(book_club, 'book_club', 'csv')