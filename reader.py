import pandas as pd
# Reads data from json
def json_reader(file):
    book_club = pd.read_json(file, orient='records')
    book_club['meeting'] = pd.to_datetime(book_club['meeting'],unit='ms')
    return book_club
# Reads data from book club csv and formats it pythonically into a multiindex dataframe
def csv_reader(file):
    book_club = pd.read_csv(file)
    book_club.columns = book_club.columns.str.lower()
    book_club.drop('search key', axis=1, inplace=True)
    book_club['meeting'] = pd.to_datetime(book_club['meeting'], format='%m/%d/%Y')
    book_club['suggestor'] = book_club['suggestor'].str.lower()
    book_club.to_json('book_club.json', orient='records')
    return book_club