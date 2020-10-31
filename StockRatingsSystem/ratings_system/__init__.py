import markdown
import os
from flask import Flask, Response
from ratings_system import webscrapper as ws

# Create an instance of Flask
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


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
    return Response(ws.main(market, stock_symbol), mimetype='text/plain')
