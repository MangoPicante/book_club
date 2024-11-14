# Scrapes audible for book data
from scraper_utils import soup_cooker
import pandas as pd
import webbrowser
import re

# Returns the url that matches the book name in the dataframe's row using row['audible search'] and row['book']
def url(row):
    book = row['book'].lower()
    soup = soup_cooker(row['audible search'])
    # finds all of the list items containing search result info
    search_results = soup.find_all('div', class_='bc-col-responsive bc-col-12')
    # for each search result list item, finds the title, url, and number of ratings and appends them to search_result_tuples
    search_result_tuples = []
    for search_result in search_results:
        #skips search results that don't have a title tag
        title_tag = search_result.find('h3', class_="bc-heading bc-color-link bc-pub-break-word bc-size-medium")
        if title_tag is None:
            continue
        title_tag = title_tag.a
        # finds the title
        title = title_tag.text.lower()
        # finds the href
        href = title_tag['href']
        # converts href into a full url, trimming search info
        url = 'https://www.audible.com' + href.split('?')[0]
        tuple = (title, url)
        search_result_tuples.append(tuple)
    # checks search results for exact matches to the title, returns the first matching url
    for result in search_result_tuples:
        if result[0] == book:
            return result[1]
    # checks search results for titles that start with the book, returns first matching url
    for result in search_result_tuples:
        if result[0].startswith(book):
            return result[1]
    # automatically opens the search url of a book title that isn't found
    browser = webbrowser.get('windows-default')
    browser.open(row['audible search'])
    return None
# Returns the soup's ratings
def ratings(soup):
    try:
        # finds the potential rating div tags
        div_tags = soup.find_all('div', class_='bc-col-responsive bc-col-4')
        # finds the div tag with the rating
        rating_div_tags = []
        for div_tag in div_tags:
            if div_tag.find('span', class_='full-review-star') is not None:
                rating_div_tags.append(div_tag)
                continue
        print(rating_div_tags)
        # finds the rating span tag within the div tag
        span_tags = [rating_div_tag.find('span', class_='bc-text bc-pub-offscreen') for rating_div_tag in rating_div_tags]
        ratings = [float(span_tag.text.split()[0]) for span_tag in span_tags]
        # labels the ratings with their corresponding categories
        labels = ["Overall", "Performance", "Story"]
        labelled_ratings = dict(zip(labels, ratings))
        return labelled_ratings
    except:
        print('Error finding the rating')
        return None
def runtime(soup):
    try:
        # finds the li tag with the runtime
        runtime_text = soup.find('li', class_='bc-list-item runtimeLabel').text
        # converts the runtime text into a list of integers
        runtime_list = re.findall(r'\d+', runtime_text)
        # converts the list of integers into a single integer
        if len(runtime_list) == 2:
            runtime = int(runtime_list[0]) * 60 + int(runtime_list[1])
        else:
            runtime = int(runtime_list[0] * 60)
        return runtime
    except:
        print('Error finding the runtime')
        return None
def author(soup):
    try:
        # finds the author li tag
        li_tag = soup.find('li', class_='bc-list-item authorLabel')
        # returns the author from the a tag within the li tag
        return li_tag.find('a').text
    except:
        print('Error finding the author')
        return None
def narrator(soup):
    try:
        # finds the narrator li tag
        li_tag = soup.find('li', class_='bc-list-item narratorLabel')
        # returns the narrator from the a tag within the li tag
        return li_tag.find('a').text
    except:
        print('Error finding the narrator')
        return None
def categories(soup):
    try:
        # finds the categories li tag
        li_tag = soup.find('li', class_='bc-list-item categoriesLabel')
        # returns the categories from the a tag within the li tag
        category_string = li_tag.find('a').text
        # parses the categories into a list
        categories = re.split(r',\s*|\s&\s', category_string)
        return categories
    except:
        print('Error finding the categories')
        return None
def tags(soup):
    try:
        # finds the tags div tag
        div_tag = soup.find('div', class_='bc-section bc-chip-group')
        # finds all the span tags with class bc-chip-text within the div tag
        span_tags = div_tag.find_all('span', class_='bc-chip-text')
        tags = [span_tag.text.strip() for span_tag in span_tags]
        return tags
    except:
        print('Error finding the tags')
        return None
def scrape(row):
    soup = soup_cooker(row['a_url'])
    return pd.Series([ratings(soup), runtime(soup), author(soup), narrator(soup), categories(soup), tags(soup)])