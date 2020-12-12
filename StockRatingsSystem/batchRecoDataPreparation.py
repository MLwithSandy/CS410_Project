import json
from random import sample

import pandas as pd
import numpy as np
import pathlib

from ratings_system import webscrapper as ws

filePath = pathlib.Path(__file__).parent.absolute()


def getRating(df_raw):
    print('input dataframe size: ', df_raw.shape)

    listOfStocks = df_raw['stock_symbol'].tolist()
    # print('listOfStocks: ', listOfStocks)

    ratings_dict = {
        "BUY": 1,
        "HOLD": 0,
        "SELL": -1,
        " ": 0
    }

    listOfRatings = []

    for stock in listOfStocks:
        stockSymbol = stock
        # stockSymbol = 'AAPL'
        ratingJson = ws.main('NASDAQ', stockSymbol, '');
        rating = ' '

        if ratingJson and not ratingJson.isspace():
            json_decode = json.loads(ratingJson)
            for item in json_decode:
                rating = item.get('overallRating')
        else:
            print('no rating available')

        print('rating: ', rating)
        ratingScale = ratings_dict[rating]
        listOfRatings.append(ratingScale)

    ratingDF = listOfRatings
    print(sample(ratingDF, 15))
    print('ratings list size: ', len(ratingDF))

    return ratingDF


def main():
    pd.set_option('display.max_columns', None)

    nasdaqList = pd.read_csv(filePath/'nasdaq/nasdaq_result_list.csv', sep=',', header=0, engine='python')
    # print('nasdaqList: ', nasdaqList.head(5))

    # remove stocks in exception list
    exceptionDF = pd.read_csv(filePath/'nasdaq/exceptionList.csv', sep=',', header=0, engine='python')
    stock_df_wo_rating = pd.merge(nasdaqList, exceptionDF, how='inner', on=['Symbol', 'Symbol'])
    nasdaqList = pd.concat([nasdaqList, stock_df_wo_rating, stock_df_wo_rating]).drop_duplicates(keep=False)

    nasdaqSymbolList = nasdaqList['Symbol']

    df = pd.read_csv(filePath/'nasdaq/2018_Financial_Data.csv', index_col=0)
    print('df shape: ', df.shape)
    df['Symbol'] = df.index

    # only those stocks which are listed in NASDAQ
    df_nasdaq = pd.merge(df, nasdaqSymbolList, how='inner', on=['Symbol', 'Symbol'])
    print('df_nasdaq shape: ', df_nasdaq.shape)

    df = df_nasdaq.copy()
    df.set_index('Symbol', inplace=True)
    # print(df.head(1))

    # READ in sp500.csv for list of sp500 ticker symbols [actually 480...]
    sp_500 = pd.read_csv(filePath/'sp500/sp500.csv')
    # print(sp_500[:5])

    #
    # Drop rows with no information
    # df.dropna(how='all', inplace=True)
    #

    # replace NaNs
    df['Market Cap'] = df['Market Cap'].mask(df['Market Cap'].isna(), np.inf)

    # replace 0 with infinite in case market cap is 0
    df['Market Cap'] = df['Market Cap'].mask(df['Market Cap'] == 0, np.inf)

    df_new = pd.DataFrame(df[['Gross Profit']].to_numpy() / df[['Market Cap']].to_numpy(),
                          columns=['gross_profit_per_market_cap'])
    df_new['stock_symbol'] = df.index
    df_new.index = df.index

    print(df_new[0:5])

    a_dict = {'Consumer Cyclical': 0, 'Energy': 1, 'Technology': 2, 'Industrials': 3,
              'Financial Services': 4, 'Basic Materials': 5, 'Communication Services': 6,
              'Consumer Defensive': 7, 'Healthcare': 8, 'Real Estate': 9, 'Utilities': 10}

    df_new['Sector'] = df.replace({'Sector': a_dict})['Sector']

    a_list = []

    for item in df_new.index:
        # if item not in sp_500:
        a_list.append(int(item in sp_500))

    df_new['is_SP500'] = a_list

    df_new['is_profitable_3yr'] = (df['3Y Net Income Growth (per Share)'] > 0).map(lambda x: int(x))

    df_new['is_revenue_growth_3yr'] = (df['3Y Revenue Growth (per Share)'] > 0).map(lambda x: int(x))

    df_new['analyst_rating'] = getRating(df_new)

    # print(df_new.head(20))
    # print('reco_data size:', df_new.shape)
    df_new.to_csv(filePath/'recommender_system/reco_data.csv', index=False)

    return


if __name__ == '__main__':
    main()
