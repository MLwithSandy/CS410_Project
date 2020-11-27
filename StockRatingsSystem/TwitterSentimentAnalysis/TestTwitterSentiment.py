import sentimentAnalysis as sa
from datetime import date

stock_symbol="SKIPPER"
today_date = str(date.today())

sentiment = sa.getSentiment(stock_symbol)
tweets_fetched = sa.getTweets(stock_symbol)

if (len(tweets_fetched)<=5):
    print(len(tweets_fetched))
else:
    tweets_fetched = tweets_fetched[:5]

sentiment = {
        "stockSymbol": stock_symbol,
        "refreshDate": today_date,
        "sentiment": sentiment,
        "tweets_fetched": tweets_fetched
}

print(sentiment)

#for t in tweets_fetched:
#    print(t)