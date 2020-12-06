from datetime import date
import sys

from ratings_system import webscrapper as ws
from nasdaq import listStocks as lst
import pandas as pd

# list of stocks
def stock_list_t(stockFirstChar):
    listOfStocks = lst.main('nasdaq/nasdaq_result_list.csv')['Symbol'].tolist()
    exceptionDF = pd.read_csv('nasdaq/exceptionList.csv', sep=',', header=0, engine='python')
    exceptionList = exceptionDF['Symbol'].tolist()

    relevantStocks = []

    if stockFirstChar.isalnum():
        for item in listOfStocks:
            if item[0].lower() == stockFirstChar and item not in exceptionList:
                relevantStocks.append(item)
    else:
        for item in listOfStocks:
            if not item[0].isalpha() and item not in exceptionList:
                relevantStocks.append(item)
    return relevantStocks


# update the ratings
def main():
    print('system arguement:', sys.argv[1])
    stockFirstChar = sys.argv[1]

    stock_list = stock_list_t(stockFirstChar)

    print('stock_list: ', stock_list)

    today_date = str(date.today())

    for stock in stock_list:
        print('stock: ', stock)
        ws.main('NASDAQ', stock, today_date)
    return


if __name__ == '__main__':
    main()
