import json

from bs4 import BeautifulSoup
from flask import jsonify, make_response
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from datetime import datetime, date
import time
import pandas as pd
from ratings_system import dboperations as dbo


# create a webdriver object and set options for headless browsing
def load_webdriver():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage");
    driver = webdriver.Chrome(chrome_options=options)
    return driver


# read web document using beutifulsoup
def get_js_soup(url_web, driver):
    driver.get(url_web)
    time.sleep(5)

    redirected_url = driver.current_url

    if url_web != redirected_url:
        print("redirected URL : " + redirected_url)
        new_url = redirected_url + "price-target/"
        print("new URL for Analysts rating : " + new_url)
        driver.get(url_web)
    else:
        print("URL for Analysts rating: " + redirected_url)

    time.sleep(5)
    res_html = driver.execute_script('return document.body.innerHTML')
    soup_obj = BeautifulSoup(res_html, 'html.parser')  # beautiful soup object to be used for parsing html content
    # print(soup_obj)
    return soup_obj


# More tidying
# Sometimes the text extracted HTML webpage may contain javascript code and some style elements.
# This function removes script and style tags from HTML so that extracted text does not contain them.


def remove_script(soup_obj):
    for script in soup_obj(["script", "style"]):
        script.decompose()
    return soup_obj


# MarketBeat URL builder

def get_mb_url(market, stock_symbol):
    base_url = 'https://www.marketbeat.com/stocks/{market}/{stock_symbol}/price-target/'
    final_url = base_url.format(market=market, stock_symbol=stock_symbol)
    return final_url


# Map various ratings on scale of {-1: sell, 0: hold, 1: buy} for rating

def scale_ratings(ratings):
    ratings_dict = {
        "SELL": -1,
        "STRONG SELL": -1,
        "BEARISH": -1,
        "UNDERPERFORM": -1,
        "MODERATE SELL": -1,
        "WEAK HOLD": -1,
        "UNDERWEIGHT": -1,
        "REDUCE": -1,
        "HOLD": 0,
        "NEUTRAL": 0,
        "MARKET PERFORM": 0,
        "PEER PERFORM": 0,
        "OUTPERFORM": 1,
        "MODERATE BUY": 1,
        "ACCUMULATE": 1,
        "OVER-WEIGHT": 1,
        "OVERWEIGHT": 1,
        "ADD": 1,
        "BULLISH": 1,
        "BUY": 1,
        "STRONG BUY": 1
    }

    return ratings_dict[ratings.upper()]


# reverse mapping of average ratings

def ratings_assignment(average_rating):
    ratings_dict = {
        1: "BUY",
        0: "HOLD",
        -1: "SELL"
    }
    return ratings_dict[average_rating]


# calculate overall rating

def calculate_overall_ratings(df_calc):
    df_temp = df_calc.copy();

    # scale ratings from various analysts on scale of {-1, 0, 1}
    df_temp['new_ratings'] = df_calc['ratingAssigned'].map(lambda x: scale_ratings(x))

    # average rating
    average_rating = round(df_temp['new_ratings'].mean(), 0)

    # rating assignment
    overall_ratings = ratings_assignment(average_rating)
    return overall_ratings


# scrape web in case result is not stored in db

def scrape_web(market, stock_symbol):
    # get MarketBeat URL
    url_mb = get_mb_url(market, stock_symbol)

    # load web driver
    web_driver = load_webdriver();

    # get soup object using web url and web driver
    soup_obj = get_js_soup(url_mb, web_driver)

    # clean soup object - remove scripts
    soup_obj = remove_script(soup_obj)

    # Get the ratings data

    data = []
    data_header = ["Date [MM/dd/YYYY]", "ratingAgency", "Action", "ratingAssigned", "Price target", "Price impact"]
    dropped_columns = ["Date [MM/dd/YYYY]", "Action", "Price target", "Price impact"]

    table = soup_obj.find("table", attrs={"class": "scroll-table sort-table fixed-left-column fixed-header"})
    if table is None:
        print("No table found for market analyst rating")
    else:
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele.split("➝")[-1].strip() for ele in cols if ele])

        # create dataframe for ease-of-processing
        # drop records with None
        df = pd.DataFrame(data).dropna();
        df.columns = data_header
        # add new column with date
        df['ratingDate'] = pd.to_datetime(df['Date [MM/dd/YYYY]'],
                                          format="%m/%d/%Y",
                                          errors='coerce')
        print("total no of rows: ", df.shape)

        # drop unnecessary columns from dataframe
        df_rel = df.drop(columns=dropped_columns)

        # create mask to filter current month data only
        current_month = datetime.now().strftime("%Y-%m")
        current_month_mask = df_rel['ratingDate'].map(lambda x: x.strftime("%Y-%m")) == current_month
        df_current_month_desc = df_rel[current_month_mask].sort_values(by=['ratingDate'], ascending=False)

        if df_current_month_desc.empty or df_current_month_desc.shape[0] < 5:
            now = datetime.now()
            last_month = now.month - 1 if now.month > 1 else 12
            last_month_mask = df_rel['ratingDate'].map(lambda x: x.strftime("%Y-%m")) == str(now.year) + "-" + str(
                last_month)
            df_last_month_desc = df_rel[last_month_mask].sort_values(by=['ratingDate'], ascending=False)
            df_current_month_desc = df_current_month_desc.append(df_last_month_desc)

        # move date column as first column first
        cols = list(df_current_month_desc)
        cols = [cols[-1]] + cols[:-1]
        df_current_month_desc = df_current_month_desc[cols]

        # print(df.sample(n=10))
        # print(df_current_month_desc)

        print("total no of relevant rows: ", df_current_month_desc.shape)

        # convert date
        df_current_month_desc['ratingDate'] = df_current_month_desc['ratingDate'].apply(
            lambda x: str(x.strftime("%Y-%m-%d")))

        # consider only max 10 ratings

        return df_current_month_desc[:10]


def scrape_web_t(market, stock_symbol):
    test_data = [['2020-10-17', 'TEST ANALYST 1', 'BUY'], ['2020-10-17', 'TEST ANALYST 2', 'SELL']]

    df_test = pd.DataFrame(test_data, columns=['ratingDate', "ratingAgency", "ratingAssigned"])
    return df_test


# Main function

def main(market, stock_symbol):
    # check db first

    column_list = ['stockSymbol', 'marketPlace', 'refreshData', 'overallRating', 'analystsRatings']

    today_date = str(date.today())

    search_dict = {
        column_list[0]: stock_symbol,
        column_list[1]: market,
        column_list[2]: today_date
    }

    col_hide_dict = {
        "_id": 0,
        # "index": 0,
        # "analystsRatings.index": 0
    }

    data_from_db = dbo.read_ratings_db(search_dict, col_hide_dict)

    if not bool(data_from_db):
        # if not present in db, get the data via web
        df = scrape_web(market, stock_symbol)
        overall_ratings = calculate_overall_ratings(df)

        df.reset_index(inplace=True)
        data_dict_df = df.to_dict("records")
        print(data_dict_df)

        result = [[stock_symbol, market, today_date, overall_ratings, data_dict_df]]
        df_result = pd.DataFrame(result, columns=column_list)

        df_result.reset_index(inplace=True)
        result_doc = df_result.to_dict("records")

        dbo.insert_ratings_db(result_doc);

        json_obj = df_result.to_json(orient='records', date_format='iso')

        print('data read from webscrapper')
    else:
        result_doc = data_from_db
        json_obj = json.dumps(result_doc)
        print('data read from db')

    # print(json_obj)
    return json_obj


if __name__ == '__main__':
    market = "NASDAQ"
    stock_symbol = "AAPL"
    main(market, stock_symbol)
