from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
from datetime import datetime
import time
import pandas as pd


# create a webdriver object and set options for headless browsing
def load_webdriver():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('./chromedriver', options=options)
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


# Main function

def main():
    market = "NASDAQ"
    stock_symbol = "AAPL"

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
    data_header = ["Date [MM/dd/YYYY]", "Market analyst", "Action", "Rating", "Price target", "Price impact"]
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
        df['Date'] = pd.to_datetime(df['Date [MM/dd/YYYY]'],
                                    format="%m/%d/%Y",
                                    errors='coerce')
        print("total no of rows: ", df.shape)

        # drop unnecessary columns from dataframe
        df_rel = df.drop(columns=dropped_columns)

        # create mask to filter current month data only
        current_month = datetime.now().strftime("%Y-%m")
        current_month_mask = df_rel['Date'].map(lambda x: x.strftime("%Y-%m")) == current_month
        df_current_month_desc = df_rel[current_month_mask].sort_values(by=['Date'], ascending=False)

        # move date column as first column first
        cols = list(df_current_month_desc)
        cols = [cols[-1]] + cols[:-1]
        df_current_month_desc = df_current_month_desc[cols]

        # print(df.sample(n=10))
        # print(df_current_month_desc)

        print("total no of relevant rows: ", df_current_month_desc.shape)

        json_obj = df_current_month_desc.to_json(orient='records', date_format='iso')

        print(json_obj)
        return json_obj


if __name__ == '__main__':
    main()
