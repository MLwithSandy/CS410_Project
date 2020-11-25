import json

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from datetime import datetime, date
import pandas as pd
from tinydb import TinyDB, Query, where

# tiny db client

log_db = TinyDB('requestLogDB.json')
ratings_db = TinyDB('ratingsDB.json')


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
    print("record to be inserted: ", data_dict)
    # print("first remove... ")
    # ratings_db.remove(where('stockSymbol') == stock_symbol)
    # print("... then insert ")
    ratings_db.insert_multiple(data_dict)
    return


# read all ratings items in requestlogdb db
def read_all_ratings_db():
    _items = ratings_db.all()
    return _items


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

    if refreshData > '':
        _items = ratings_db.search((q.stockSymbol == stockSymbolCriteria) & (q.marketPlace == marketPlaceCriteria) & (q.refreshData == refreshDataCriteria))
    else:
        _items = ratings_db.search((q.stockSymbol == stockSymbolCriteria) & (q.marketPlace == marketPlaceCriteria))

    print("_items", _items)
    return _items
