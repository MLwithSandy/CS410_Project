from tinydb import TinyDB, Query, where
from tinydb.operations import delete
import pathlib

# tiny db client

dbPath = pathlib.Path(__file__).parent.absolute()

print('dbPath: ', pathlib.Path(__file__).parent.absolute())

log_db = TinyDB(dbPath / 'db/requestLogDB.json')


# insert request item in requestlogdb db

def insert_request_log_db(request_item_do):
    log_db.insert(request_item_do)
    return


# read all request items from requestlogdb db

def read_all_request_log_db(col_hide_dict):
    _items = log_db.all()
    return _items


# insert request item in requestlogdb db
def insert_ratings_db(stock_symbol, data_dict):
    stock_firstLetter = stock_symbol[0]
    if stock_firstLetter.isalpha():
        stock_firstLetter = stock_firstLetter.lower();
    else:
        stock_firstLetter = ''

    dbFilePath = str(dbPath) + '/db/ratingsDB_' + stock_firstLetter + '.json'
    print('dbFilePath: ', dbFilePath)
    ratings_db = TinyDB(dbFilePath)

    print("record to be inserted: ", data_dict)
    print("first remove... ")
    ratings_db.update(delete('stockSymbol'), where('stockSymbol') == stock_symbol)
    print("... then insert ")
    ratings_db.insert_multiple(data_dict)
    return


# read all ratings items in requestlogdb db
# def read_all_ratings_db():
#     _items = ratings_db.all()
#     return _items


# # read all ratings items in ratings db with matching criteria
#
# def read_ratings_db(search_dict, col_hide_dict):
#     db = client.ratingsdb
#     print("search criteria: ", search_dict)
#     _items = list(db.ratingsdb.find(search_dict, col_hide_dict))
#     print("_items", _items)
#     return _items


# read all ratings items in ratings db with matching criteria
def read_n_stocks_rating(search_dict, no_items, col_hide_dict):
    q = Query()

    refreshData = ''

    if 'stockSymbol' in search_dict.keys():
        stockSymbolCriteria = search_dict['stockSymbol']
    if 'marketPlace' in search_dict.keys():
        marketPlaceCriteria = search_dict['marketPlace']
    if 'refreshData' in search_dict.keys():
        refreshDataCriteria = search_dict['refreshData']

    stock_firstLetter = stockSymbolCriteria[0]
    if stock_firstLetter.isalpha():
        stock_firstLetter = stock_firstLetter.lower();
    else:
        stock_firstLetter = ''

    dbFilePath = str(dbPath) + '/db/ratingsDB_' + stock_firstLetter + '.json'
    print('dbFilePath: ', dbFilePath)

    ratings_db = TinyDB(dbFilePath)

    if refreshData > '':
        _items = ratings_db.search((q.stockSymbol == stockSymbolCriteria) & (q.marketPlace == marketPlaceCriteria) & (
                q.refreshData == refreshDataCriteria))
    else:
        _items = ratings_db.search((q.stockSymbol == stockSymbolCriteria) & (q.marketPlace == marketPlaceCriteria))

    # print("_items", _items)
    return _items
