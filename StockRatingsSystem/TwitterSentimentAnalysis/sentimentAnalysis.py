from TwitterSentimentAnalysis import getTweets as gt
import pickle
import re


def getTweets(stock_symbol):
    ''' 
    # initialize api instance
    twitter_api = twitter.Api(consumer_key='nd7CFVu8evt6hOmKy5foUiKtr',
                            consumer_secret='nFzQAdPle23I43sBrVKFPqWNhnBBXSLpksTg2T28KRFBhgO9u7',
                            access_token_key='1316625307479269378-Vf6yfXm70yS0U30rrh19fAdaUBCcPD',
                            access_token_secret='WpuIB7iYV0XvQScPIW1uDxvK2V0yAyD0y9U7H6d34I0M8')
    
    search_string = stock_symbol + "stock"
    
    
    tweets_fetched = twitter_api.GetSearch(search_string, count = 100)
    
       
    print("Fetched " + str(len(tweets_fetched)) + " tweets for the term " + "APPL stock")
    
    for t in tweets_fetched:
        print(t.text.encode("utf-8"))
    
    '''
    return gt.getTweets(stock_symbol, max_result='100')


def getSentiment(stock_symbol):
    with open('TwitterSentimentAnalysis/classifier.pickle', 'rb') as f:
        clf = pickle.load(f)

    with open('TwitterSentimentAnalysis/vectorizerTFIDF.pickle', 'rb') as f:
        vectorizer = pickle.load(f)

    # fetched_tweets = []
    tot_positive = 0
    tot_negetive = 0
    positive_percentage = 0

    tweets_fetched = getTweets(stock_symbol)

    for t in tweets_fetched:
        # fetched_tweets.append(t.text.encode("utf-8"))
        # t = (str)(t.text.encode("utf-8"))
        # t = t.decode('utf-8')
        t = re.sub(r'^https://t.co/[a-zA-Z0-9]*\s', ' ', t)
        t = re.sub(r'\s+https://t.co/[a-zA-Z0-9]*\s', ' ', t)
        t = re.sub(r'\s+https://t.co/[a-zA-Z0-9]*$', ' ', t)
        t = t.lower()
        t = re.sub(r"that's", 'that is', t)
        t = re.sub(r"there's", 'there is', t)
        t = re.sub(r"what's", 'what is', t)
        t = re.sub(r"where's", 'where is', t)
        t = re.sub(r"it's", 'it is', t)
        t = re.sub(r"who's", 'who is', t)
        t = re.sub(r"i'm", 'i am', t)
        t = re.sub(r"she's", 'she is', t)
        t = re.sub(r"he's", 'he is', t)
        t = re.sub(r"they're", 'they are', t)
        t = re.sub(r"who're", 'who are', t)
        t = re.sub(r"shouldn't", 'should not', t)
        t = re.sub(r"wouldn't", 'would not', t)
        t = re.sub(r"couldn't", 'could not', t)
        t = re.sub(r"can't", 'can not', t)
        t = re.sub(r"won't", 'will not', t)
        t = re.sub(r'\W', ' ', t)
        t = re.sub(r'\d', ' ', t)
        t = re.sub(r'\s+[a-z]\s+', ' ', t)
        t = re.sub(r'\s+[a-z]$', ' ', t)
        t = re.sub(r'^[a-z]\s+', ' ', t)
        t = re.sub(r'\s+', ' ', t)
        sentiment = clf.predict(vectorizer.transform([t]).toarray())
        print(t, ":", sentiment)
        if sentiment[0] == 1:
            tot_positive += 1
        else:
            tot_negetive += 1
        # fetched_tweets.append(t)

    if (tot_positive + tot_negetive) > 0:
        positive_percentage = tot_positive / (tot_positive + tot_negetive)
    print("positive_percentage :", positive_percentage * 100, "%")

    if positive_percentage > 0.65:
        print("stock is buy")
        return 1
    elif positive_percentage < 0.35 and positive_percentage > 0:
        print("stock is sell")
        return -1
    else:
        print("stock is neutral")
        return 0


if __name__ == '__main__':
    getSentiment(stock_symbol)
    getTweets(stock_symbol)
