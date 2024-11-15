import pandas as pd
import json

# Reads data from json
def json_reader(file):
    with open(file, 'r') as f:
        data = json.load(f)
    book_club = pd.DataFrame(data['data'])
    dtype_dict = {col: dtype for col, dtype in data['dtypes'].items()}
    for col, dtype in dtype_dict.items():
        if dtype == 'datetime64[ns]':
            book_club[col] = pd.to_datetime(book_club[col])
        else:
            book_club[col] = book_club[col].astype(dtype)
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

# saves the data to the given filetype if prompt accepted
def save(df, filename, filetype):
    prompt = input(f'Save data to {filetype}? (y/n): ')
    if prompt == 'y':
        try:
            if filetype == 'csv':
                df.to_csv(filename + '.' + filetype, index=False)
            elif filetype == 'json':
                data = {
                    'data': df.to_dict(orient='records'),
                    'dtypes': df.dtypes.apply(lambda x: x.name).to_dict()
                }
                with open(filename + '.' + filetype, 'w') as f:
                    json.dump(data, f)
        except Exception as e:
            print(f"Error: {e}")