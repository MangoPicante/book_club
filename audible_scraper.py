# Scrapes audible for book data
import scraper_utils as scu
import pandas as pd
import webbrowser
import re

# Returns the soup's ratings
def ratings(soup):
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
def runtime(soup):
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
def author(soup):
    # finds the author li tag
    li_tag = soup.find('li', class_='bc-list-item authorLabel')
    # returns the author from the a tag within the li tag
    return li_tag.find('a').text
def narrator(soup):
    # finds the narrator li tag
    li_tag = soup.find('li', class_='bc-list-item narratorLabel')
    # returns the narrator from the a tag within the li tag
    return li_tag.find('a').text
def categories(soup):
    # finds the categories li tag
    li_tag = soup.find('li', class_='bc-list-item categoriesLabel')
    # returns the categories from the a tag within the li tag
    category_string = li_tag.find('a').text
    # parses the categories into a list
    categories = re.split(r',\s*|\s&\s', category_string)
    return categories
def tags(soup):
    # finds the tags div tag
    div_tag = soup.find('div', class_='bc-section bc-chip-group')
    # finds all the span tags with class bc-chip-text within the div tag
    span_tags = div_tag.find_all('span', class_='bc-chip-text')
    tags = [span_tag.text.strip() for span_tag in span_tags]
    return tags
def scrape(row):
    soup = scu.soup_cooker(row['a_url'])
    return pd.Series([scu.try_except_wrapper(ratings, soup), scu.try_except_wrapper(runtime, soup), scu.try_except_wrapper(author, soup), scu.try_except_wrapper(narrator, soup), scu.try_except_wrapper(categories, soup), scu.try_except_wrapper(tags, soup)])