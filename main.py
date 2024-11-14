import reader
import goodreads_scraper as gscr
import audible_scraper as ascr
from os.path import exists

def json_save_prompt(df, filename):
    # saves the data to a json file if prompt accepted
    prompt = input('Save data to json? (y/n): ')
    if prompt == 'y':
        df.to_json(filename + '.json', orient='records')

def csv_save_prompt(df, filename):
    # saves the data to a csv file if prompt accepted
    prompt = input('Save data to csv? (y/n): ')
    if prompt == 'y':
        df.to_csv(filename + '.csv', index=False)

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
    book_club = reader.json_reader('book_club.json')
    print(book_club.head())
    # attempts to fill in all missing values
    book_club = column_backfill(book_club, ['g_rating', 'g_genre', 'g_author', 'g_pages', 'g_published'], gscr.scrape)
    json_save_prompt(book_club, 'book_club')
    book_club = column_backfill(book_club, ['a_ratings', 'a_runtime', 'a_author', 'a_narrator', 'a_categories', 'a_tags'], ascr.scrape)
    json_save_prompt(book_club, 'book_club')
    
else:
    try:
        book_club = reader.csv_reader('Book Club - Ratings.csv')
        print(book_club.head())
        # scrapes goodreads data from urls
        book_club[['g_rating', 'g_genre', 'g_author', 'g_pages', 'g_published']] = book_club.apply(gscr.scrape, axis=1)
        json_save_prompt(book_club, 'book_club')
        # scrapes audible data from urls
        book_club[['a_ratings', 'a_runtime', 'a_author', 'a_narrator', 'a_categories', 'a_tags']] = book_club.apply(ascr.scrape, axis=1)
        json_save_prompt(book_club, 'book_club')
    except Exception as e:
        print(f"Error: {e}")

csv_save_prompt(book_club, 'book_club')