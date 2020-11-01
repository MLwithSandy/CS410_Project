from datetime import datetime
from bson.json_util import dumps

import markdown
import os
from flask import Flask, Response
from ratings_system import webscrapper as ws
from ratings_system import dboperations as dbo

# create an instance of Flask
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


# print(os.environ)


@app.route("/")
def index():
    """Present readme.md"""
    # Open readme.md file
    with open(os.path.dirname(app.root_path) + '/readme.md', 'r') as markdown_file:
        # Read the content of the file
        content = markdown_file.read()

        # Convert it to HTML
        return markdown.markdown(content)
        # return "test 1 2 3"


@app.route("/stock/ratings/<market>/<stock_symbol>")
def rating(market, stock_symbol):
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

    return Response(ws.main(market, stock_symbol), mimetype='text/plain')


@app.route("/requests/all")
def request_log_all():
    # read all requests from db
    _items = dbo.read_all_request_log_db()
    # items = [item for item in _items]
    resp = dumps(_items)

    return Response(resp, mimetype='text/bytes')


# read all ratings from db

@app.route("/stock/ratings/all")
def stocks_all():
    # read all ratings from db
    _items = dbo.read_all_ratings_db()
    # items = [item for item in _items]
    resp = dumps(_items)

    return Response(resp, mimetype='text/bytes')


@app.route("/stock/ratings/refresh/<date>")
def stocks_all_refresh_date(date):
    # read all ratings from db
    column_name = 'last refresh date'
    search_criteria = date
    _items = dbo.read_ratings_db(column_name, search_criteria)
    # items = [item for item in _items]
    resp = dumps(_items)

    return Response(resp, mimetype='text/bytes')
