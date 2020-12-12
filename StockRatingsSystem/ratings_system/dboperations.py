# import json
#
# from pymongo import MongoClient
# from pymongo.errors import ServerSelectionTimeoutError
# from datetime import datetime, date
# import pandas as pd
#
# # mongo db client
#
# maxSevSelDelay = 1
# dbConnection = True
# try:
#
#     client = MongoClient(host=['db:27017'],
#                          serverSelectionTimeoutMS=maxSevSelDelay)
#     client.server_info()
# except ServerSelectionTimeoutError() as err:
#     # do whatever you need
#     dbConnection = False
#
#
# # insert request item in requestlogdb db
#
# def insert_request_log_db(request_item_do):
#     if not dbConnection:
#         return
#
#     db = client.requestlogdb
#     db.requestlogdb.insert_one(request_item_do)
#     return
#
#
# # read all request items from requestlogdb db
#
# def read_all_request_log_db(col_hide_dict):
#     if not dbConnection:
#         return
#
#     db = client.requestlogdb
#     _items = db.requestlogdb.find({}, col_hide_dict)
#     return _items
#
#
# # insert request item in requestlogdb db
#
# def insert_ratings_db(data_dict):
#     if not dbConnection:
#         return
#
#     db = client.ratingsdb
#
#     print("record to be inserted: ", data_dict)
#     db.ratingsdb.insert_many(data_dict)
#     return
#
#
# # read all ratings items in requestlogdb db
#
# def read_all_ratings_db():
#     if not dbConnection:
#         return
#
#     db = client.ratingsdb
#
#     _items = db.ratingsdb.find()
#     return _items
#
#
# # # read all ratings items in ratings db with matching criteria
# #
# # def read_ratings_db(search_dict, col_hide_dict):
# #     db = client.ratingsdb
# #     print("search criteria: ", search_dict)
# #     _items = list(db.ratingsdb.find(search_dict, col_hide_dict))
# #     print("_items", _items)
# #     return _items
#
#
# # read all ratings items in ratings db with matching criteria
#
# def read_n_stocks_rating(search_dict, no_items, col_hide_dict):
#     if not dbConnection:
#         return
#
#     db = client.ratingsdb
#     print("search criteria: ", search_dict)
#     _items = list(db.ratingsdb.find(search_dict, col_hide_dict).limit(no_items))
#     print("_items", _items)
#     return _items
