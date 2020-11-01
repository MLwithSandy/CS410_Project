from pymongo import MongoClient
from datetime import datetime, date

# mongo db client
# client = MongoClient(os.environ['stockratingssystem_db_1_PORT_27017_TCP_ADDR'], 27017)
client = MongoClient(host=['172.27.0.2:27017'])


# insert request item in requestlogdb db

def insert_request_log_db(request_item_do):
    db = client.requestlogdb
    db.requestlogdb.insert_one(request_item_do)
    return


# read all request items from requestlogdb db

def read_all_request_log_db():
    db = client.requestlogdb
    _items = db.requestlogdb.find()
    return _items


# insert request item in requestlogdb db

def insert_ratings_db(df):
    db = client.ratingsdb

    df.reset_index(inplace=True)
    data_dict = df.to_dict("records")
    print(data_dict)
    db.ratingsdb.insert_one({"last refresh date": str(date.today()), "data": data_dict})
    return


# read all ratings items in requestlogdb db

def read_all_ratings_db():
    db = client.ratingsdb

    _items = db.ratingsdb.find()
    return _items


# read all ratings items in requestlogdb db with matching criteria

def read_ratings_db(column_name, search_criteria):
    db = client.ratingsdb
    search_dict = {
        column_name: search_criteria
    }
    print(search_dict)
    _items = db.ratingsdb.find_one(search_dict)
    return _items
