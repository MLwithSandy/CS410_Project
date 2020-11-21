from datetime import date

from ratings_system import webscrapper as ws
from ratings_system import dboperations as dbo

# list of stocks
def stock_list_t():
    columns = ['stock_symbol', 'market']
    stock_list = [
        ['AAPL', 'NASDAQ'],
        ['FB', 'NASDAQ'],
        ['TSLA', 'NASDAQ'],
        ['MSFT', 'NASDAQ'],
        ['BYND', 'NASDAQ'],
        ['AMZN', 'NASDAQ'],
        ['DOCU', 'NASDAQ'],
        ['SWKS', 'NASDAQ'],
        ['AYX', 'NYSE'],
        ['TDOC', 'NYSE']
    ]
    return stock_list


# update the ratings
def main():
    stock_list = stock_list_t()
    today_date = str(date.today())

    for stock in stock_list:
        ws.main(stock[1], stock[0], today_date)
    return


if __name__ == '__main__':
    main()
