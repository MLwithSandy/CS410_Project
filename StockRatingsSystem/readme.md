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
