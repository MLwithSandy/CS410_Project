import json
from datetime import datetime, date
import random

from bson.json_util import dumps

import markdown
import os
from flask import Flask, Response
from flask_cors import CORS, cross_origin

from ratings_system import webscrapper as ws
from ratings_system import dboperations as dbo
from nasdaq import listStocks as lst

# create an instance of Flask
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config["MONGO_URI"] = "mongodb://localhost:27017"
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['CORS_HEADERS'] = 'Content-Type'


# print(os.environ)


@app.route("/")
@cross_origin()
def index():
    """Present readme.md"""
    # Open readme.md file
    with open(os.path.dirname(app.root_path) + '/app/readme.md', 'r') as markdown_file:
        print('os.path.dirname(app.root_path)', os.path.dirname(app.root_path))
        # Read the content of the file
        content = markdown_file.read()

        # Convert it to HTML
        return markdown.markdown(content)
        # return "test 1 2 3"


@app.route("/requests/all")
@cross_origin()
def request_log_all():
    col_hide_dict = {
        "_id": 0,
        # "index": 0,
        # "analystsRatings.index": 0
    }

    # read all requests from db
    _items = dbo.read_all_request_log_db(col_hide_dict)
    # items = [item for item in _items]
    resp = dumps(_items)

    return Response(resp, mimetype='text/bytes')


# read all ratings from db

@app.route("/stock/ratings/all")
@cross_origin()
def stocks_all():
    # read all ratings from db
    _items = dbo.read_all_ratings_db()
    # items = [item for item in _items]
    resp = dumps(_items)

    return Response(resp, mimetype='text/bytes')


@app.route("/stock/ratings/refresh/<date>")
@cross_origin()
def stocks_all_refresh_date(date):
    # read all ratings from db
    column_name = 'last refresh date'
    search_criteria = date
    _items = dbo.read_ratings_db(column_name, search_criteria)
    # items = [item for item in _items]
    resp = dumps(_items)

    return Response(resp, mimetype='text/bytes')


@app.route("/stock/sentiments/<market>/<stock_symbol>")
@cross_origin()
def stocks_sentiment(market, stock_symbol):
    sentiment_resp = getSentimentFromBackend(market, stock_symbol)

    print('sentiment_resp: ', sentiment_resp)
    resp = json.dumps(sentiment_resp)

    return Response(resp, mimetype='text/bytes')


@app.route("/stock/recommendation/list")
@cross_origin()
def recommendation_list():
    today_date = str(date.today())
    # request item
    search_dict = {
        'refreshData': today_date
    }

    col_hide_dict = {
        "_id": 0,
        # "index": 0,
        # "analystsRatings.index": 0
    }

    # read 5 items from db
    _items = dbo.read_n_stocks_rating(search_dict, 5, col_hide_dict)

    resp = dumps(_items)
    return Response(resp, mimetype='text/plain')


@app.route("/stock/ratings/<market>/<stock_symbol>")
@cross_origin()
def rating(market, stock_symbol):
    rating_response = getRatingFromBackend(market, stock_symbol)

    return Response(rating_response, mimetype='text/plain')


@app.route("/stock/ratings/combined/<market>/<stock_symbol>")
@cross_origin()
def overallRating(market, stock_symbol):
    rating_analyst = getRatingFromBackend(market, stock_symbol)
    sentiment_resp = getSentimentFromBackend(market, stock_symbol)

    overall_ratings = {
        "analyst": rating_analyst.to_json(),
        "sentiment": sentiment_resp,
    }

    response = json.dumps(overall_ratings)

    return Response(response, mimetype='text/plain')


def getRatingFromBackend(market, stock_symbol):
    print("market: ", market)
    print("stock_symbol: ", stock_symbol)
    date = datetime.now().isoformat();

    # request item
    request_doc = {
        'datetime': date,
        'symbol': stock_symbol,
        'market': market
    }

    # log the request into db
    dbo.insert_request_log_db(request_doc)

    rating = ws.main(market, stock_symbol);
    return rating;


def getSentimentFromBackend(market, stock_symbol):
    print("market: ", market)
    print("stock_symbol: ", stock_symbol)

    today_date = str(date.today())

    sentiment = random.randint(1, 3)

    sentiment = {
        "stockSymbol": stock_symbol,
        "refreshDate": today_date,
        "sentiment": sentiment
    }

    return sentiment;


@app.route("/stock/all")
@cross_origin()
def listOfStocks():
    listOfStocks = lst.main('nasdaq/nasdaq_result_list.csv')
    listOfStocks_res = listOfStocks['Symbol'] + ': ' + listOfStocks['Security Name']
    print(listOfStocks[0:5])
    response = listOfStocks_res.to_json()
    return Response(response, mimetype='text/plain')
