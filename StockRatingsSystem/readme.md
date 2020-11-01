Stocks rating system

## Usuage

All response will have the form
```json
{
    "data" : "Mixed type holding the content of the response",
    "message": "Description of what happened"
}
```

Subsequent respose definition will only detail the expected value of the `data field` 

### List of supported stocks


**Definition**

`GET /stocks`

**Response**

- `200 OK` on success

```json
[
    {
        "stockShortName":"AAPL",
        "Company Name": "Apple Inc",
        "Market": "NASDAQ"
    },
    {
        "stockShortName":"TSLA",
        "Company Name": "FaceBook Inc",
        "Market": "NASDAQ"
    }
]
```

**Definition**

`GET /stock/ratings/<stockShortName>`

**Response**

- `404 Not Found` if the stockShortName is not found
- `200 OK` on success

```json 
{
        "stockShortName":"AAPL",
        "averageRating": 1.0
}
```

**Definition**

`GET /requests/all`

**Response**

- `200 OK` on success

```json
[
    {
        "datetime" : "2020-10-31, 21.00.00",
        "stock_symbol":"AAPL",
        "market": "NASDAQ"
    },
    {
        "datetime" : "2020-10-31, 21.00.00",
        "stock_symbol":"FB",
        "Market": "NASDAQ"
    }
]
```
