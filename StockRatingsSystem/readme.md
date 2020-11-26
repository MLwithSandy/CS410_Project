# Stocks Recommender Engine Backend

## Usage

All response will have the form
```json
{
    "data" : "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

Subsequent respose definition will only detail the expected value of the `data field` 

### List of supported APIs


**Definition**

- Get list of all stocks in the corpus

`GET /stock/all`

**Response**

- `200 OK` on success

```json
[
    {
        "Symbol":"AAPL",
        "Security Name": "Apple Inc",
        "Market": "NASDAQ",
        "Sector": "Technology"
    },
    {
        "Symbol":"TSLA",
        "Security Name": "FaceBook Inc",
        "Market": "NASDAQ",
        "Sector": "Technology"
    }
]
```

**Definition**

- Get ratings for a given stock from a given market

`GET /stock/ratings/<market>/<stock_symbol>`

e.g. http://localhost:5000/stock/ratings/NASDAQ/AAPL

**Response**

- `404 Not Found` if the stockShortName is not found
- `200 OK` on success

```json 
[
    {
    "stockSymbol": "AAPL",
    "marketPlace": "NASDAQ",
    "refreshData": "2020-11-25",
    "overallRating": "HOLD",
    "analystsRatings": [
            {
                "level_0": 0,
                "index": 1,
                "ratingDate": "2020-11-19",
                "ratingAgency": "The Goldman Sachs Group",
                "ratingAssigned": "Sell",
                "newRatings": -1,
                "scaledRatings": "SELL"
            },
            {
                "level_0": 1,
                "index": 2,
                "ratingDate": "2020-11-17",
                "ratingAgency": "Credit Suisse Group",
                "ratingAssigned": "Neutral",
                "newRatings": 0,
                "scaledRatings": "HOLD"
            },
            {
                "level_0": 2,
                "index": 3,
                "ratingDate": "2020-11-16",
                "ratingAgency": "JPMorgan Chase & Co.",
                "ratingAssigned": "Buy",
                "newRatings": 1,
                "scaledRatings": "BUY"
            },
            {
                "level_0": 3,
                "index": 4,
                "ratingDate": "2020-10-30",
                "ratingAgency": "Fundamental Research",
                "ratingAssigned": "Hold",
                "newRatings": 0,
                "scaledRatings": "HOLD"
            },
            {
                "level_0": 4,
                "index": 5,
                "ratingDate": "2020-10-30",
                "ratingAgency": "DA Davidson",
                "ratingAssigned": "Buy",
                "newRatings": 1,
                "scaledRatings": "BUY"
            },
            {
                "level_0": 5,
                "index": 6,
                "ratingDate": "2020-10-30",
                "ratingAgency": "Raymond James",
                "ratingAssigned": "Outperform",
                "newRatings": 1,
                "scaledRatings": "BUY"
            },
            {
                "level_0": 6,
                "index": 7,
                "ratingDate": "2020-10-30",
                "ratingAgency": "UBS Group",
                "ratingAssigned": "Neutral",
                "newRatings": 0,
                "scaledRatings": "HOLD"
            },
            {
                "level_0": 7,
                "index": 8,
                "ratingDate": "2020-10-30",
                "ratingAgency": "Barclays",
                "ratingAssigned": "Neutral",
                "newRatings": 0,
                "scaledRatings": "HOLD"
            },
            {
                "level_0": 8,
                "index": 9,
                "ratingDate": "2020-10-26",
                "ratingAgency": "Loop Capital",
                "ratingAssigned": "Hold",
                "newRatings": 0,
                "scaledRatings": "HOLD"
            },
            {
                "level_0": 9,
                "index": 11,
                "ratingDate": "2020-10-26",
                "ratingAgency": "Atlantic Securities",
                "ratingAssigned": "Overweight",
                "newRatings": 1,
                "scaledRatings": "BUY"
            }
        ]
    }
]
```

**Definition**

- Get list of recommended stocks, similar to given stock

`GET /stock/recommendation/<stock_symbol>`

e.g. http://localhost:5000/stock/recommendation/MSFT

**Response**

- `200 OK` on success

```json
[
    {
        "seq": 1,
        "stockSymbol": "HAFC",
        "stockName": "Hanmi Financial Corporation",
        "sector": "Finance",
        "rating": "SELL"
    },
    {
        "seq": 2,
        "stockSymbol": "UBOH",
        "stockName": "United Bancshares, Inc.",
        "sector": "Finance",
        "rating": "SELL"
    },
    {
        "seq": 3,
        "stockSymbol": "SVBI",
        "stockName": "Severn Bancorp Inc",
        "sector": "Finance",
        "rating": "HOLD"
    },
    {
        "seq": 4,
        "stockSymbol": "TTMI",
        "stockName": "TTM Technologies, Inc.",
        "sector": "Technology",
        "rating": "HOLD"
    },
    {
        "seq": 5,
        "stockSymbol": "HDSN",
        "stockName": "Hudson Technologies, Inc.",
        "sector": "Consumer Durables",
        "rating": "HOLD"
    }
]
```

**Definition**

- Get Twitter sentiment for given stock - 1: Positive, 
0: Neutral, -1: Negative

`GET /stock/sentiments/<market>/<stock_symbol>`

e.g. http://localhost:5000/stock/sentiments/NASDAQ/AAPL

**Response**

- `200 OK` on success

```json
{
    "stockSymbol": "AAPL",
    "refreshDate": "2020-11-25",
    "sentiment": 1
}
```


**Definition**

- Get list of user request log

`GET /requests/all`

**Response**

- `200 OK` on success

```json
[
    {
        "datetime": "2020-11-25T21:55:52.924706",
        "symbol": "TSLA",
        "market": "NASDAQ"
    },
    {
        "datetime": "2020-11-25T21:56:48.750286",
        "symbol": "TSLA",
        "market": "NASDAQ"
    }
]
```
